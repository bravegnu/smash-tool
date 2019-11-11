"""LPC1343 FLASH MEMORY PROGRAMMING FIRMWARE"""
import os
import time
import binascii
import logging
from io import BytesIO

from .micro import micro_info
from .micro import ProtoError, IspTimeoutError, IspChecksumError, IspProgError
from .binfile import BinFile

class LPC13xx(object):
    def __init__(self, micro, freq, serial):
        self.micro = micro
        self.freq = freq
        self.serial = serial
        self.data_dict = {}
        self.sector_used = 0
        self.start_sector = 0
        self.end_sector = 0
        self.flash_addr = 0x0
        self.clear_stats()

    def clear_stats(self):
        self.retry_stats = 0
        self.timeo_stats = 0
        self.cksum_stats = 0
        self.proto_stats = 0
        self.proge_stats = 0

    def retry(self, tries, func, args):
        ex = None
        while tries > 0:
            try:
                return func(*args)
            except IspTimeoutError as e:
                ex = e
                self.timeo_stats += 1
            except IspProgError as e:
                ex = e
                self.proge_stats += 1
            except IspChecksumError as e:
                ex = e
                self.cksum_stats += 1
            except ProtoError as e:
                ex = e
                self.proto_stats += 1
            tries -= 1
            self.retry_stats += 1

        raise ex

    def _write_and_expect(self, cmd, expected):
        """Write to Microcontroller and check the Expected Response"""
        self.serial.clear_output_buffer()
        self.serial.write(cmd + b"\r\n")
        if expected:
            expected += b"\r\n"
            cmd += b"\r"
        else:
            cmd += b"\r\n"

        self.serial.clear_input_buffer()
        resp = self.serial.read_timeo(len(cmd) + len(expected))

        if resp != (cmd + expected):
            logging.basicConfig(filename='smash.log', filemode='w',
                                format='%(asctime)s-%(process)s-%(levelname)s\n%(message)s')
            logging.error(" Cmmd>{}\n Expt>{}\n Resp>{}\n".format(cmd, cmd + expected, resp))
            raise IspTimeoutError("Unexpected Response")

    def write_and_expect(self, cmd, expected):
        self.retry(8, self._write_and_expect, (cmd, expected))

    def _sync_baudrate(self):
        """Synchronizing baudrate"""
        self.serial.write(b"?")
        expected = b"Synchronized\r\n"
        resp = self.serial.read_timeo(len(expected))
        if resp != expected:
            IspTimeoutError("Unable to Sync ...")

        self.write_and_expect(b"Synchronized", b"OK")

    def sync_baudrate(self):
        self.retry(8, self._sync_baudrate, ())

    def reset(self, isp):
        pass

    def unlock_and_checkid(self):
        """To unlock erase, write commands and
        to check the device we are going to flash.
        U 23130 --> Used to unlock flash write and erase commands
        J --> is used to read the part identification number """
        self.write_and_expect(b"U 23130", b"0")
        self.write_and_expect(b"J", b"0\r\n1023410219")

    def set_osc_freq(self):
        """To Set the CCLK frequency,
        CClk --> should be greater than or equal to 10MHz"""
        self.write_and_expect(b"12000", b"OK")

        self.unlock_and_checkid()

    def erase_block(self, block):
        """To Erase Selected Sectors in Flash"""

        cmd = ("P {0} {0}".format(block)).encode("ascii")
        self.write_and_expect(cmd, b"0")
        cmd = ("E {0} {0}".format(block)).encode("ascii")
        self.write_and_expect(cmd, b"0")

    def erase_status_boot_vector(self):
        pass

    def erase_chip(self):
        pass

    def prog_status(self):
        pass

    def prog_boot_vector(self):
        pass

    def prog_sec(self):
        pass

    def prog_clock6(self):
        pass

    def select_sector(self):
        """Select the Sectors for COPY command"""
        sector_size = 4096

        if self.sector_used == sector_size:
            self.start_sector += 1
            self.end_sector += 1
            self.sector_used = 0

    def copy_to_sector(self, len_block, sram_addr):
        """To Copy from RAM to FLASH Memory"""
        while len_block > 0:
            self.sector_used += 256
            cmd = ("P {} {}".format(self.start_sector, self.end_sector)).encode("ascii")
            self.write_and_expect(cmd, b"0")
            cmd = ("C {} {} 256".format(self.flash_addr, sram_addr)).encode("ascii")
            self.write_and_expect(cmd, b"0")
            self.flash_addr += 0x00000100
            sram_addr += 0x00000100
            len_block -= 256
            self.select_sector()

    def chunked(self, fopen, size):
        """To get the Blocks of data from Bin file"""
        while True:
            data = fopen.read(size)
            if data:
                yield data
            else:
                return "EOF reached"


    def chunkedio(self, string, size):
        """To get chunk of data from Blocks"""
        string_buf = BytesIO(string)
        return self.chunked(string_buf, size)


    def prog_file(self, fname, complete_func=None):
        """To Program the Microcontroller"""
        if complete_func:
            complete_func(0)

        data_len = os.path.getsize(fname)
        binfile = open(fname, "rb")

        block_crc = 0
        wr_byts = 0
        for block in self.chunked(binfile, 11520):
            cmd = ("W {} {}".format(0x10000300, len(block))).encode("ascii")
            self.write_and_expect(cmd, b"0")

            for chunk in self.chunkedio(block, 900):

                for number, line in enumerate(self.chunkedio(chunk, 45)):

                    for i, byts in enumerate(line):
                        block_crc += byts
                        wr_byts += 1
                        if complete_func:
                            complete_func(wr_byts / data_len)

                    cmd = binascii.b2a_uu(line).replace(b" ", b"`").strip()
                    self.write_and_expect(cmd, b"")

                self.write_and_expect(("{}".format(block_crc)).encode("ascii"), b"OK")
                block_crc = 0

            self.copy_to_sector(len(block), 0x10001000)

    def _update_cache_with_data(self, cmd):
        self.serial.write(cmd + b"\r\n")

        resp = self.serial.read_timeo(256)
        self.split_resp = resp.split(b"\r\n")
        self.bdata = binascii.a2b_uu(self.split_resp[-3][:-2])

    def _update_cache(self, addr):
        baddr = addr
        cmd = ("R {} {}".format(baddr, 16).encode("ascii"))
        self._update_cache_with_data(cmd)

        if sum(self.bdata) == int(self.split_resp[-2]):
            self.serial.write(b"OK\r\n")
        else:
            cmd = b"RESEND"
            self._update_cache_with_data(cmd)

        for i in self.bdata:
            self.data_dict[baddr] = i
            baddr += 1

    def _getitem(self, addr):
        if addr not in self.data_dict:
            self._update_cache(addr)

        return self.data_dict[addr]

    def __getitem__(self, addr):
        """Return the bytes at specified address"""
        return self.retry(8, self._getitem, (addr,))

    def verify_program(self, filename, gerror, complete_func=None):
        bfile = BinFile(filename)
        total = float(bfile.count_data_bytes())
        if complete_func:
            complete_func(0)
        for i, addr_data in enumerate(bfile.data_bytes()):
            addr, rdata = addr_data
            data = int(rdata.hex(), 16)
            if addr > 511:
                if self[addr] != data:
                    gerror("Verify failed at %s!"
                           "Please try re-programming." % addr)
                    return
            if complete_func:
                complete_func((i+1) / total)

common_sparams = {
    "data_bits": 8,
    "parity": False,
    "odd_parity": False,
    "stop_bits": 1,
    "soft_fc": False,
    "hard_fc": False,
}

micro_info.update({
    "LPC1343" : {
        "mfg": "NXP",
        "block_range": ((0x0, 0xFFF), (0x1000, 0x1FFF), (0x2000, 0x2FFF), (0x3000, 0x3FFF),
                        (0x4000, 0x4FFF), (0x5000, 0x5FFF), (0x6000, 0x6FFF), (0x7000, 0x7FFF)),
        "sparams": common_sparams,
        "class": LPC13xx,
        "security": ("CRP1", "CRP2", "CRP3")
        }
    })
