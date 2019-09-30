### Bin File Parsing ###
import os

class BinFile(object):
    def __init__(self, filename, addr = 0x0):
        self.binfile = open(filename, "rb")
        self.len_data = os.path.getsize(filename)
        self.count = 0
        self.start_addr = addr

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
        try:
            for byte in self:
                yield (self.start_addr, byte)
                self.start_addr += 1
        except Exception as e:
            raise e
