import numpy as np
import os

class radarSampleHeader:
    def __init__(self):
        self.version = -1
        self.n_rx = -1
        self.n_tx = -1
        self.n_range_bins = -1
        self.n_pulses = -1
        self.timestamp = -1
        self.data = -1

    def getNumberOfValues(self):
        return self.n_range_bins * self.n_rx  * self.n_pulses * 2


class radar_sample_reader:
    def __init__(self, filename):
        self.filename = filename
        self.statinfo = os.stat(filename)
        self.file_size = self.statinfo.st_size
        self.offset = 0
        self.f = open(self.filename, "r")

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

    def endOfFile(self):

        if ((self.offset) > self.file_size - 208896):
            return 1
        else:
            return 0

    def getNextSample(self):
        header = self.readFormat()
        n_values = header.getNumberOfValues()
        values = np.fromfile(self.filename, dtype=np.int16, count=n_values, offset=self.offset)
        self.offset = self.offset + n_values * np.dtype(np.int16).itemsize

        return header, values

    def reset(self):
        self.offset = 0

    def readFormat(self):
        n_vals = 6
        first_vals = np.fromfile(self.filename, dtype=np.int64, count=n_vals, offset=self.offset)
        self.offset = self.offset + n_vals * np.dtype(np.int64).itemsize
        header = radarSampleHeader()

        header.version = first_vals[0].astype(np.int64)
        header.n_rx = first_vals[1].astype(np.int64)
        header.n_tx = first_vals[2].astype(np.int64)
        header.n_range_bins = first_vals[3].astype(np.int64)
        header.n_pulses = first_vals[4].astype(np.int64)
        header.timestamp = first_vals[5].astype(np.int64)

        return header