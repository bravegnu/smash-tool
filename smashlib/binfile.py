### Bin File Parsing ###
import os
from .hexfile import HexError

class BinFile(object):
    def __init__(self, filename, addr = 0x0):
        self.binfile = open(filename, "rb")
        self.len_data = os.path.getsize(filename)
        self.count = 0
        self.start_addr = addr
        self.end_addr = addr + self.len_data

    def __iter__(self):
        return self

    def __next__(self):
        ch = self.binfile.read(1)
        if ch == b"":
            raise StopIteration("Reached EOF")
        return ch

    def count_data_bytes(self):
        return self.len_data

    def data_bytes(self):
        addr = self.start_addr
        for byte in self:
            yield (addr, byte)
            addr += 1

    def used_blocks(self, block_ranges):
        blocks = []
        sblock = eblock = None

        for i, br in enumerate(block_ranges):
            if self.start_addr >= br[0] and self.start_addr <= br[1]:
                sblock = i
                break

        if sblock is None:
            raise HexError("address out of device address range",
                            self.binfile.name, i)

        for i, br in enumerate(block_ranges):
            if self.end_addr >= br[0] and self.end_addr <= br[1]:
                eblock = i
                break

        if eblock is None:
            raise HexError("address out of device address range",
                            self.binfile.name, i)

        for b in range(sblock, eblock + 1):
            blocks.append(b)

        return blocks
