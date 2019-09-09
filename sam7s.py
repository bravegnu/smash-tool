from .micro import micro_info
from xmodem import XMODEM


class Sam7S:
    def __init__(self, micro, freq, serial):
        self.micro = micro
        self.freq = freq
        self.serial = serial
        self.cache = {}

    def sync_baudrate(self):
        pass

    def _set_reset(self, val):
        pass

    def getc(self, size, timeout=1):
        gbytes = self.serial.read_timeo(size)
        print('Read Byte: {}'.format(gbytes))
        return gbytes or None

    def putc(self, data, timeout=1):
        pbytes = self.serial.write(data)
        print('Put Byte: {}, data: {}'.format(pbytes, data[3:]))
        return pbytes or None

    def prog_file(self, fname, complete_func=None):
        self.serial.write(b"S200000,#")
        fd = open(fname, "rb")
        modem = XMODEM(self.getc, self.putc)
        modem.send(fd)

    def write(self):
        pass

    def reset(self, isp):
        pass

    def set_osc_freq(self):
        pass

    def _read_info(self):
        pass

    def read_sec(self):
        pass

    def read_clock6(self):
        pass

    def erase_block(self, block):
        pass

    def erase_status_boot_vector(self):
        pass

    def erase_chip(self):
        pass

    def prog_status(self):
        pass

    def prog_boot_vector(self, addr):
        pass

    def prog_clock6(self):
        pass

    def prog_sec(self, w=False, r=False, x=False, p=False):
        pass

    def prog_serial(self, serialno):
        pass


common_sparams = {
    "data_bits": 8,
    "parity": False,
    "odd_parity": False,
    "stop_bits": 1,
    "soft_fc": False,
    "hard_fc": False,
    "bps": 115200
}

micro_info.update({
    "Sam7S": {
        "mfg": "ATMEL",
        "block_range": ((0x200000, 0x201000), ),
        "sparams": common_sparams,
        "class": Sam7S,
        "security": ("p", "serial")
    }
})
