import matplotlib.pyplot as plt
import numpy as np

class data_plotter:
    def __init__(self, num_plots):
        self.first_time = True
        self.num_plots = num_plots
        self.im = []
        self.fg, self.ax = plt.subplots(ncols=self.num_plots, nrows=1, figsize=(5,3))

    def plot_data(self, data_cube):
        if self.first_time:
            for k in range(0, self.num_plots):
                self.im.append(self.ax[k].imshow((20 * np.log10(np.abs(np.squeeze(data_cube[k, :, :]))))))

            plt.draw()
            plt.pause(1e-3)
            self.first_time = False
        else:
            for k in range(0, self.num_plots):
                self.im[k].set_data((20 * np.log10(np.abs(np.squeeze(data_cube[k, :, :])))))
            plt.draw()
            plt.pause(1e-3)
