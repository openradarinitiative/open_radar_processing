import numpy as np
from loader.radar_sample_reader import radar_sample_reader
from loader.ti_raw_data_reader import ti_raw_data_reader
import matplotlib.pyplot as plt

#Import the parameters from the radar setup, edit params.py for different parameters
from params import numADCSamples, numTxAntennas,numRxAntennas, numLoopsPerFrame, numRangeBins

count = 0
if __name__ == '__main__':
    fg = plt.figure()
    ax = fg.gca()

    first_time = True
    im = 0
    # Opening datafile
    # filename = "../2021_02_12_18_40_25.open_radar"
    filename = "YOUR_TI_FILE.bin"
    reader = ti_raw_data_reader(filename)


    while True:
        # Reading data from file
        header,np_raw_frame = reader.getNextSample()
        raw_frame = np.array(np_raw_frame, dtype=np.float32)
        # print("-----------")
        print(header.timestamp)
        # print("-----------")

        ret = np.zeros(len(raw_frame), dtype=float)
        quart_length = int(ret.shape[0] / 4)

        ret[0:quart_length] = raw_frame[0::4]
        ret[quart_length:2 * quart_length] = raw_frame[1::4]
        ret[2 * quart_length:3 * quart_length] = raw_frame[2::4]
        ret[3 * quart_length:4 * quart_length] = raw_frame[3::4]

        ret = ret.reshape((numRxAntennas, numLoopsPerFrame, numADCSamples))

        range_processed = np.fft.fft(ret.transpose() , axis=0).transpose()
        range_processed = range_processed[:, :, 0:int(range_processed.shape[2] / 2)]

        range_processed = np.fft.fftshift(np.fft.fft(range_processed[0, :, :], axis=0), axes=0)
        doppler_view_np = (20 * np.log10(np.abs(range_processed)).transpose())
        if count:
            if first_time:
                im = ax.imshow(doppler_view_np)
                ax.set_aspect('auto')
                plt.autoscale()
                plt.draw()
                plt.pause(1e-3)
                # plt.clf()
                first_time = 0

            else:
                im.set_data(doppler_view_np)
                ax.set_aspect('auto')
                plt.autoscale()
                plt.draw()
                plt.pause(1e-3)
        count += 1
