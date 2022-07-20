
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import csv
import os

font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 32}

matplotlib.rc('font', **font)

def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'same') / w

class Plotter:

    def plotter(plot):
        """Decorador para los métodos que grafican"""
        def wrapped(self, fig_params, filename, *args, **kwargs):
            fig = plt.figure(**fig_params)
            plot(self, filename, *args, **kwargs)
            fig.tight_layout(pad=5.0)
            plt.savefig(filename)
        return wrapped

    def __init__(self, out_folder, filename):
        with open(filename, "r") as file:
            reader = csv.DictReader(file)
            lineas = list(reader)
            self.times = np.array([int(x["time"]) for x in lineas])
            self.datetimes = np.array([x["datetime"] for x in lineas])
            self.cpu = np.array([float(x["cpu_percentage"]) for x in lineas])
            self.mem = np.array([float(x["mem_used_mb"]) for x in lineas])
        out_filename = os.path.split(filename)[-1]
        out_path = os.path.join(out_folder, f"{out_filename[:-4]}.png")
        self.plot({"figsize": (75, 50)}, out_path)

    @plotter
    def plot(self, filename):
        plt.subplot(2, 1, 1)
        plt.plot(self.times, self.cpu, linewidth=4, label="Instant")
        plt.plot(self.times, moving_average(self.cpu, 5), linewidth=2, color="red", label="Rolling mean (5s)", linestyle='dashed')
        plt.xlabel("Time [s]/[date]")
        plt.ylabel("[%]")
        plt.title("CPU Usage")
        plt.legend()
        tick_labels = [f"{x1}[s]\n{x2[:10]}\n{x2[11:]}" for x1, x2 in zip(self.times, self.datetimes)]
        step = len(tick_labels) // 5
        if step == 0:
            step = 1
        plt.xticks(range(0, len(tick_labels), step), tick_labels[::step])
        plt.yticks(np.arange(min(self.cpu), max(self.cpu)+.1, 8))
    
        plt.subplot(2, 1, 2)
        plt.plot(self.times, self.mem, linewidth=4, label="Instant")
        plt.plot(self.times, moving_average(self.mem, 5), linewidth=2, color="red", label="Rolling mean (5s)", linestyle='dashed')
        plt.xlabel("Time [s]/[date]")
        plt.ylabel("RAM [MB]")
        plt.title("Mem Usage")
        plt.legend()
        tick_labels = [f"{x1}[s]\n{x2[:10]}\n{x2[11:]}" for x1, x2 in zip(self.times, self.datetimes)]
        plt.xticks(range(0, len(tick_labels), step), tick_labels[::step])
        plt.yticks(np.arange(min(self.mem), max(self.mem)+1, 8))

if __name__ == "__main__":
    plotter = Plotter("", "")
