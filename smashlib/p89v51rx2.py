import time

from hex import Hex
from micro import Micro

class HexEraseBlock(Hex):
    def __init__(self):
        """Create an erase block command.
        """
        cmd = ":0100000301"
        self.hex = self.append_checksum(cmd)

class HexChipErase(Hex):
    def __init__(self):
        self.hex = ":00000007F9"

class HexProg6Clock(Hex):
    def __init__(self):
        cmd = ":020000030505"
        self.hex = self.append_checksum(cmd)

class HexProgSecBit(Hex):
    def __init__(self):
        cmd = ":020000030501"
        self.hex = self.append_checksum(cmd)
    
class P89V51Rx2(Micro):
    def _set_reset(self, val):
        """Set/clear the reset line.

        Raises:
        OSError, IOError -- if setting the RESET line fails.
        """
        self.serial.set_dtr(val)
        
    def reset(self, isp):
        self._set_reset(1)
        time.sleep(0.25)
        self._set_reset(0)
        time.sleep(0.1)

    def set_osc_freq(self):
        pass

    def read_sec(self):
        # FIXME: read parallel prog security bit
        return [True, True, True, True]

    def read_clock6(self):
        return True

    def erase_block(self, block):
        cmd = HexEraseBlock()
        self._send_cmd(cmd, 5)

    def erase_status_boot_vector(self):
        pass

    def erase_chip(self):
        cmd = HexChipErase()
        self._send_cmd(cmd)        

    def prog_status(self):
        pass

    def prog_boot_vector(self, addr):
        pass

    def prog_clock6(self):
        cmd = HexProg6Clock()
        self._send_cmd(cmd)

    def prog_sec(self, w=False, r=False, x=False, p=False):
        if p:
            cmd = HexProgSecBit()
            self._send_cmd(cmd)
