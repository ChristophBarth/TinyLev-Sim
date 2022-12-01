import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sb  # TODO: use plt.imshow instead

import models.params
from models.data_generator import get_pressure_wave, get_interference, get_pressure_change, get_far_field_directivity
from models.transducer import Transducer, generate_transducers
from models.plot_data import Plot_Data
from models.helpers import make_list

from models.params import RES


custom_cmap = LinearSegmentedColormap.from_list("custom", ["red", "white", "blue"])
integral_cmap = LinearSegmentedColormap.from_list("custom", ["black", "black", "red", "yellow", "white"])
expose_cmap = LinearSegmentedColormap.from_list("custom", ["yellow", "red", "red", "red", "black", "red", "red", "red", "yellow"])
gif_cmap = LinearSegmentedColormap.from_list("custom", ["black", "white", "black"])
directivity_cmap = LinearSegmentedColormap.from_list("custom", ["white", "black"])

x = np.linspace(-0.05, 0.05, RES)
z = np.linspace(0, 0.1, RES)
x, z = np.meshgrid(x, z)

transducers = generate_transducers()
base_transducer = Transducer(np.array([0, 0, 0]), np.array([0, 0, 1]), 0)

def setup_levitator(rings=4, height=models.params.HEIGHT, transducer_offset=models.params.TRANSDUCER_OFFSET, frequency=models.params.BASE_FREQ, transducer_radius=models.params.TRANSDUCER_RADIUS):
    models.params.height = height
    models.params.TRANSDUCER_OFFSET = transducer_offset
    models.params.BASE_FREQ = frequency
    models.params.TRANSDUCER_RADIUS = transducer_radius


def plot(*plots):

    for index, plot in enumerate(plots):
        print(index)
        plt.subplot(1,len(plots),index+1)
        plt.imshow(plot.data, vmin=plot.vmin, vmax=plot.vmax, cmap=plot.cmap, origin='lower')
        plt.title(plot.desc)
        plt.xlabel(plot.xlabel)
        plt.ylabel(plot.ylabel)
        plt.colorbar(shrink=.43)

    plt.tight_layout();
    plt.show()


def plot_transducers(bottom_transducers=transducers[0], top_transducers=transducers[1]):
    bottom_transducers, top_transducers = make_list(bottom_transducers, top_transducers)

    ax = plt.figure().add_subplot(projection='3d')

    for transducer in top_transducers:
        transducer.plot(ax)

    for transducer in bottom_transducers:
        transducer.plot(ax)

    plt.show()


def plot_pressure_waves(transducers=transducers[0], phase=0, left="complex", right="simple"):
    fig, axs = plt.subplots(1, 2)

    ax1 = sb.heatmap(get_pressure_wave(x, z, transducers, phase, left), xticklabels=10, yticklabels=10, ax=axs[0],
                     vmin=-600, vmax=600,
                     cmap=gif_cmap)
    ax1.invert_yaxis()
    ax1.set_aspect('equal')

    ax2 = sb.heatmap(get_pressure_wave(x, z, transducers, phase, right), xticklabels=10, yticklabels=10, ax=axs[1],
                     cmap=gif_cmap, vmin=-32,
                     vmax=32)
    ax2.invert_yaxis()
    ax2.set_aspect('equal')

    plt.show()



def plot_interference(transducers=transducers, phase=0, phase_shift=0, left='complex', right='simple'):
    fig, axs = plt.subplots(1, 2)

    ax1 = sb.heatmap(get_interference(x, z, transducers, phase, phase_shift, left), xticklabels=10, yticklabels=10,
                     ax=axs[0],
                     vmin=-960, vmax=960, cmap=custom_cmap)
    ax1.invert_yaxis()
    ax1.set_aspect('equal')

    ax2 = sb.heatmap(get_interference(x,z, transducers, phase, phase_shift, right), xticklabels=10, yticklabels=10, ax=axs[1],
                     vmin=-50, vmax=50, cmap=custom_cmap)
    ax2.invert_yaxis()
    ax2.set_aspect('equal')

    plt.show()


def plot_pressure_change(transducers=transducers, phase_shift=0, left="complex", right="simple"):

    d1 = get_pressure_change(x, z, transducers, type=left)
    d2 = get_pressure_change(x, z, transducers, type=right)

    data1 = Plot_Data(d1, integral_cmap, vmin=2500, vmax=5000, desc="Komplexe Druckänderung")
    data2 = Plot_Data(d2, integral_cmap, vmin=150, vmax=250, desc="Vereinfachte Druckänderung")

    plot(data1, data2)


def plot_directivity_function(transducer=base_transducer):
    d = get_far_field_directivity(x,z,transducer)
    data = Plot_Data(d, directivity_cmap, desc="Direkticitätsfunktion")

    plot(data)


if (__name__ == "__main__"):
    setup_levitator()
    plot_pressure_change()

#TODO: Phase Shift als Argument wahrscheinlich ungeeignet, da bereits in Transducer Klasse enthalten