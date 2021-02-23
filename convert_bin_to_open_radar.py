import numpy as np
from loader.radar_sample_reader import radar_sample_reader
from loader.ti_raw_data_reader import ti_raw_data_reader
from loader.radar_sample_writer import radar_sample_writer
import matplotlib.pyplot as plt

#Import the parameters from the radar setup, edit params.py for different parameters
from params import numADCSamples, numTxAntennas,numRxAntennas, numLoopsPerFrame, numRangeBins

count = 0
if __name__ == '__main__':
    fg = plt.figure()
    ax = fg.gca()

    do_plot = False

    first_time = True
    im = 0
    # Opening datafile
    # filename = "../2021_02_12_18_40_25.open_radar"
    filename = "YOUR_TI_FILE.bin"
    filename_openradar = "converted.open_radar"

    logger = radar_sample_writer(filename_openradar)
    reader = ti_raw_data_reader(filename)


    logging_header = np.array([1,numRxAntennas,numTxAntennas,numRangeBins,numLoopsPerFrame,1],dtype=np.int64)

    while True:
        # Reading data from file
        np_raw_frame = reader.getNextSample()
        logging_header[-1] = logging_header[-1] + (1e3 * 0.05)

        logger.writeNextSample(logging_header,np_raw_frame)
        if(do_plot):
            raw_frame = np.array(np_raw_frame, dtype=np.float32)


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









import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import time
from loader.radar_sample_writer import radar_sample_writer

#Import the parameters from the radar setup, edit params.py for different parameters
from params import numADCSamples, numTxAntennas,numRxAntennas, numLoopsPerFrame, numRangeBins

count = 0
if __name__ == '__main__':
    fg = plt.figure()
    ax = fg.gca()

    now = datetime.now()
    date_time = now.strftime("%Y_%m_%d_%H_%M_%S")
    logging_header = np.array([1,numRxAntennas,numTxAntennas,numRangeBins,numLoopsPerFrame,1],dtype=np.int64)
    filename = str(date_time) + ".open_radar"
    filename = "/mnt/big_1/openradar/BikingBoth/BikingBoth" + ".open_radar"

    logger = radar_sample_writer(filename)

    test_data = np.fromfile("/mnt/big_1/openradar/BikingBoth/adc_data_Raw_Full.bin",np.int16)
    # test_data = np.fromfile("/home/muras/Downloads/adc_data_Raw_0.bin",np.int16)
    n_frames = int(test_data.shape[0] / int((numRxAntennas * numADCSamples * numLoopsPerFrame)))

    # del adcdata
    # test_data = parse_awr1843("/home/muras/Downloads/test_openradar_data_ignacio/data/adc_data_Raw_0.bin",numLoopsPerFrame,n_frames,numRxAntennas,numADCSamples)
    # test_data = parse_awr1843("/mnt/big_1/openradar/BikingPerson1/adc_data_Raw_Full.bin",numLoopsPerFrame,n_frames,numRxAntennas,numADCSamples)


    # num_chirps = int(adcdata.shape[0]/numADCSamples/numRxAntennas)
    #
    # adcdata = np.reshape(adcdata, ( numADCSamples*numRxAntennas , num_chirps))
    # adcdata = adcdata.transpose()
    #
    # adcData = np.zeros((numRxAntennas, num_chirps * numADCSamples))
    #
    # for row in range(0,numRxAntennas):
    #     for i in range(0,num_chirps-1):
    #         adcData[row,i*numADCSamples+1:(i+1)*numADCSamples] = adcdata[i,row*numADCSamples+1:(row+1)*numADCSamples]

    # adcdata = np.reshape(adcdata, (numRxAntennas, numADCSamples, numChirpsPerFrame, n_frames))
    # test_data = np.reshape(test_data, (numRxAntennas*  numChirpsPerFrame*numADCSamples, n_frames))
    # test_data = np.reshape(test_data, (n_frames,numRxAntennas*  numChirpsPerFrame*numADCSamples))
    # test = adcdata
    first_time = True

    timestamp = datetime.now()

    samples_in_frame = numRxAntennas*  numChirpsPerFrame*numADCSamples
    # for i in range(0,test.shape[-1]):
    for i in range(0,n_frames):

        # raw_frame = np.array(np.squeeze(test[:,:,:,i]), dtype=np.float32)

        logging_header[-1] = logging_header[-1] +(1e3*0.05)
        # raw_frame = test_data[i*samples_in_frame:(i+1)*numRxAntennas*  numChirpsPerFrame*numADCSamples]
        raw_frame = test_data[i*samples_in_frame:(i+1)*samples_in_frame]
        # raw_frame = np.array(np.squeeze(test_data[i,:]), dtype=np.int16)
        # logger.writeNextSample(logging_header,raw_frame)

        ret = np.zeros(len(raw_frame), dtype=float)
        quart_length = int(ret.shape[0] / 4)

        # ret[0:quart_length] = raw_frame[0::4]
        # ret[quart_length:2 * quart_length] = raw_frame[1::4]
        # ret[2 * quart_length:3 * quart_length] = raw_frame[2::4]
        # ret[3 * quart_length:4 * quart_length] = raw_frame[3::4]
        ret = raw_frame
        # ret = ret.reshape((numRxAntennas, numLoopsPerFrame, numADCSamples))
        ret = ret.reshape((numLoopsPerFrame,numRxAntennas , numADCSamples))
        ret = np.transpose(ret, (1, 0, 2))

        test = np.zeros(len(raw_frame), dtype=np.int16)
        quart_length = int(test.shape[0] / 4)

        test_ravel = ret.ravel()

        test[0::4] = test_ravel[0:quart_length]
        test[1::4] = test_ravel[quart_length:2 * quart_length]
        test[2::4] = test_ravel[2 * quart_length:3 * quart_length]
        test[3::4] = test_ravel[3 * quart_length:4 * quart_length]
        test = test.reshape((numRxAntennas, numLoopsPerFrame, numADCSamples))

        logger.writeNextSample(logging_header,test)
        #
        # test2 = np.zeros(len(raw_frame), dtype=float)
        # quart_length = int(test2.shape[0] / 4)
        #
        # test = test.ravel()
        # test2[0:quart_length] = test[0::4]
        # test2[quart_length:2 * quart_length] = test[1::4]
        # test2[2 * quart_length:3 * quart_length] = test[2::4]
        # test2[3 * quart_length:4 * quart_length] = test[3::4]
        #
        # ret = test2.reshape((numRxAntennas, numLoopsPerFrame, numADCSamples))
        #
        #
        #
        #
        #
        # ret = ret[:, 0:256, :]
        #
        # range_processed = np.fft.fft(ret.transpose() * np.hamming(ret.shape[0]), axis=0).transpose()
        # range_processed = range_processed[:, :, 0:int(range_processed.shape[2] / 2)]
        #
        #
        # range_processed = np.fft.fftshift(np.fft.fft(range_processed[0, :, :], axis=0), axes=0)
        #
        # doppler_view_np = (20 * np.log10(np.abs(range_processed)).transpose())
        # if count:
        #     if first_time:
        #
        #         im = ax.imshow(doppler_view_np,cmap='jet', aspect='auto', vmax=np.max(doppler_view_np) - 20, vmin=np.max(doppler_view_np) - 70,)
        #         ax.set_aspect('auto')
        #         plt.autoscale()
        #         plt.draw()
        #         plt.pause(1e-3)
        #         # plt.clf()
        #         first_time = 0
        #
        #     else:
        #         im.set_data(doppler_view_np)
        #         ax.set_aspect('auto')
        #         plt.autoscale()
        #         plt.draw()
        #         plt.pause(1e-3)
        #
        # count += 1
