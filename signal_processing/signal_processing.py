import cupy as cp

class signal_processing():
    def __init__(self, num_channels, num_pulses, num_adc_samples):
        self.num_channels = num_channels
        self.num_pulses = num_pulses
        self.num_adc_samples = num_adc_samples
        self.num_range_samples = num_adc_samples/2

    def __exit__(self, type, value, traceback):
        return self

    def restructure_data(self):
        ret = cp.zeros(len(self.raw_data), dtype=float)
        quart_length = int(ret.shape[0] / 4)

        ret[0:quart_length] = self.raw_data[0::4]
        ret[quart_length:2 * quart_length] = self.raw_data[1::4]
        ret[2 * quart_length:3 * quart_length] = self.raw_data[2::4]
        ret[3 * quart_length:4 * quart_length] = self.raw_data[3::4]

        self.data_cube = ret.reshape((self.num_channels, self.num_pulses, self.num_adc_samples))

    def range_doppler_processing(self):
        range_processed = cp.fft.fft(self.data_cube.transpose() * cp.hamming(self.data_cube.shape[0]), axis=0).transpose()
        range_processed = range_processed[:, :, 0:int(range_processed.shape[2] / 2)]

        range_processed = cp.fft.fftshift(cp.fft.fft(range_processed, axis=1), axes=1)

        self.data_cube = range_processed

    def beam_forming_processing(self):
        self.data_cube = cp.fft.fftshift(cp.fft.fft(self.data_cube, axis=0), axes=0)

    def process_data(self, raw_data_cube):
        self.raw_data = cp.asarray(raw_data_cube, dtype=cp.float32)

        self.restructure_data()
        self.range_doppler_processing()
        self.beam_forming_processing()

        return cp.asnumpy(self.data_cube)
