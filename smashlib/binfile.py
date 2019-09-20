### Bin File Parsing ###
import os


class BinFile(object):
    def __init__(self, filename):
        self.binfile = open(filename, "rb")
        self.l_data = os.path.getsize(filename)
        self.count = 0
        self.addr = 0x0

    def __iter__(self):
        return self

    def is_eof(self, bytelines):
        byteline = bytelines
        for byte in byteline:
            self.count += 1
        return self.count

    def __next__(self):
        bytelines = self.binfile.__next__()
        if self.is_eof(bytelines) > self.l_data:
            raise StopIteration("read EOF")
        return bytelines

    def count_data_bytes(self):
        len_data = self.l_data - 512
        return len_data

    def data_bytes(self):
        try:
            for byteline in self:
                for byte in byteline:
                    if self.addr > 511:
                        yield (self.addr, byte)
                    self.addr += 1
        except Exception as e:
            raise e
