import numpy as np
import threading
from multiprocessing import Pipe
import time
from datetime import datetime

from loader.radar_sample_writer import radar_sample_writer
import loader.udp_receiver as udp_receiver

#Import the parameters from the radar setup, edit params.py for different parameters
from params import numADCSamples, numTxAntennas,numRxAntennas, numLoopsPerFrame, numRangeBins

count = 0
if __name__ == '__main__':
    # Get the timestamp now and create the file
    now = datetime.now()
    last_timestamp = now
    date_time = now.strftime("%Y_%m_%d_%H_%M_%S")
    filename = str(date_time) + ".open_radar"

    # Create the instance of a datalogger
    logger = radar_sample_writer(filename)
    logging_header = np.array([1,numRxAntennas,numTxAntennas,numRangeBins,numLoopsPerFrame,1],dtype=np.int64)

    # Setup the threading and pass parameters to the UDP receiver
    is_running_event = threading.Event()
    output_p, input_p = Pipe(False)
    sampling_thread = udp_receiver.UDP_Receiver(is_running_event,input_p,n_chirps=numLoopsPerFrame, n_samples=numADCSamples)
    is_running_event.set()
    sampling_thread.start()


    while True:
        # Receive from the pipe
        np_raw_frame = output_p.recv()
        # Update the timestamp of the sample
        timestamp = datetime.now()
        logging_header[-1] = time.mktime(timestamp.timetuple()) * 1e3 + timestamp.microsecond / 1e3

        # Write the sample to disc
        logger.writeNextSample(logging_header,np_raw_frame)
        # Print the update time
        print(timestamp - last_timestamp)
        last_timestamp = timestamp


