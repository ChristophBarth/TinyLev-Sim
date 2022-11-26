import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sb  # TODO: use plt.imshow instead

from models.data_generator import get_pressure_wave, get_interference, get_pressure_change
from models.transducer import transducer, generate_transducers
from models.helpers import make_list

custom_cmap = LinearSegmentedColormap.from_list("custom", ["red", "white", "blue"])
integral_cmap = LinearSegmentedColormap.from_list("custom", ["black", "black", "red", "yellow", "white"])
expose_cmap = LinearSegmentedColormap.from_list("custom",
                                                ["yellow", "red", "red", "red", "black", "red", "red", "red", "yellow"])
gif_cmap = LinearSegmentedColormap.from_list("custom", ["black", "white", "black"])

x = np.linspace(-0.05, 0.05, 200)
z = np.linspace(0, 0.1, 200)
x, z = np.meshgrid(x, z)

transducers = generate_transducers()


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

    fig, axs = plt.subplots(1, 2)

    ax1 = sb.heatmap(get_pressure_change(x, z, transducers, type=left), xticklabels=10, yticklabels=10, ax=axs[0], cmap=integral_cmap, vmin=2500, vmax=5000)
    ax1.invert_yaxis()
    ax1.set_aspect('equal')

    ax2 = sb.heatmap(get_pressure_change(x, z, transducers, type=right), xticklabels=10, yticklabels=10, ax=axs[1], cmap=integral_cmap, vmin=150, vmax=250)
    ax2.invert_yaxis()
    ax2.set_aspect('equal')

    plt.show()


if (__name__ == "__main__"):
    plot_pressure_change()

#TODO: Phase Shift als Argument wahrscheinlich ungeeignet, da bereits in Transducer Klasse enthalten