import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import time

#Import the parameters from the radar setup, edit params.py for different parameters

class ti_raw_data_reader:
    def __init__(self, filename):
        self.filename = filename
        from ..params import numADCSamples, numTxAntennas, numRxAntennas, numLoopsPerFrame, numRangeBins
        self.numADCSamples = numADCSamples
        self.numTxAntennas = numTxAntennas
        self.numRxAntennas = numRxAntennas
        self.numLoopsPerFrame = numLoopsPerFrame
        self.numRangeBins = numRangeBins
        self.data = np.fromfile(filename,np.int16)
        self.n_frames = int(self.data.shape[0] / int((numRxAntennas * numADCSamples * numLoopsPerFrame)))
        self.current_frame = 0


    def getFrame(self, sample_number):
        raw_frame = self.data[sample_number* self.samples_in_frame:(sample_number + 1) * self.samples_in_frame]
        raw_frame = raw_frame.reshape((self.numLoopsPerFrame, self.numRxAntennas, self.numADCSamples))
        raw_frame = np.transpose(raw_frame, (1, 0, 2))

        final_frame = np.zeros(len(raw_frame), dtype=np.int16)
        quart_length = int(final_frame.shape[0] / 4)

        test_ravel = raw_frame.ravel()

        final_frame[0::4] = test_ravel[0:quart_length]
        final_frame[1::4] = test_ravel[quart_length:2 * quart_length]
        final_frame[2::4] = test_ravel[2 * quart_length:3 * quart_length]
        final_frame[3::4] = test_ravel[3 * quart_length:4 * quart_length]
        final_frame = final_frame.reshape((self.numRxAntennas, self.numLoopsPerFrame, self.numADCSamples))
        return final_frame

    def getNextSample(self):
        if(self.current_frame >= self.n_frames):
            print("Reached end of file, going back to start:")
            self.current_frame = 0
        final_frame = self.getFrame(self.current_frame)
        self.current_frame += 1
        return final_frame

    def reset(self):
        self.current_frame = 0
