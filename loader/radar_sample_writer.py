import numpy as np
import os

class radar_sample_writer():
    def __init__(self, filename):
        self.filename = filename
        self.offset = 0
        self.f = open(self.filename, "wb")

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.f.close()

    def __iter__(self):
        self.reset()
        return self

    def __next__(self):
        if self.endOfFile():
            raise StopIteration
        return self.getNextSample()

    def writeNextSample(self,header,data):
        header.tofile(self.f)
        data.tofile(self.f)

    def reset(self):
        self.offset = 0
