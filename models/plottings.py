import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

import models.params
from models.data_generator import get_pressure_wave, get_interference, get_pressure_change, get_far_field_directivity
from models.transducer import Transducer, generate_transducers
from models.plot_data import Plot_Data
from models.helpers import make_list

from models import params

import sys


custom_cmap = LinearSegmentedColormap.from_list("custom", ["red", "white", "blue"])
integral_cmap = LinearSegmentedColormap.from_list("custom", ["black", "black", "red", "yellow", "white"])
expose_cmap = LinearSegmentedColormap.from_list("custom", ["yellow", "red", "red", "red", "black", "red", "red", "red", "yellow"])
gif_cmap = LinearSegmentedColormap.from_list("custom", ["black", "white", "black"])
directivity_cmap = LinearSegmentedColormap.from_list("custom", ["white", "black"])
plane_map = LinearSegmentedColormap.from_list("custom", ["blue", "red"])

x = np.linspace(-0.05, 0.05, params.RES)
z = np.linspace(0, 0.1, params.RES)
x, z = np.meshgrid(x, z)

nx = np.linspace(-.01,.01, params.RES)
nz = np.linspace((params.HEIGHT/2)-.015, (params.HEIGHT/2)+.015, params.RES)
nx,nz = np.meshgrid(nx,nz)

transducers = generate_transducers()
base_transducer = Transducer(np.array([0, 0, 0]), np.array([0, 0, 1]), 0)



def setup_levitator(rings=4, height=models.params.HEIGHT, transducer_offset=models.params.TRANSDUCER_OFFSET, frequency=models.params.BASE_FREQ, transducer_radius=models.params.TRANSDUCER_RADIUS):
    print(sys.version)

    models.params.height = height
    models.params.TRANSDUCER_OFFSET = transducer_offset
    models.params.BASE_FREQ = frequency
    models.params.TRANSDUCER_RADIUS = transducer_radius

def plot(*plots):

    plt.rcParams["axes.grid"] = False

    if len(plots) == 1:
        fig=plt.figure(figsize=(4,2.8))

    for index, plot in enumerate(plots):
        plt.subplot(1,len(plots),index+1)
        plt.imshow(plot.data, vmin=plot.vmin, vmax=plot.vmax, cmap=plot.cmap, origin='lower')
        plt.title(plot.desc)
        plt.xlabel(plot.xlabel)
        plt.ylabel(plot.ylabel)
        plt.colorbar(shrink=.43)

    plt.tight_layout();
    plt.show()


def plot_directivity_function(transducer=base_transducer):
    d = get_far_field_directivity(x,z,transducer)
    data = Plot_Data(d, directivity_cmap, desc="Direkticitätsfunktion")

    plot(data)


def plot_transducers(bottom_transducers=transducers[0], top_transducers=transducers[1]):
    bottom_transducers, top_transducers = make_list(bottom_transducers),make_list(top_transducers)

    ax = plt.figure().add_subplot(projection='3d')

    for transducer in top_transducers:
        transducer.plot(ax)

    for transducer in bottom_transducers:
        transducer.plot(ax)

    plt.show()


def plot_pressure_waves(transducers=transducers[0], phase=0, left=None, right=None):

    transducers = make_list(transducers)

    d1 = get_pressure_wave(x, z, transducers, phase, left)

    if(left == "simple"): r = len(transducers)
    elif(left == "complex"): r = 650*(len(transducers)/32)
    else: r = d1.max

    data1 = Plot_Data(d1, gif_cmap, vmin=-r, vmax=r, desc=f"{left} Waves")

    if right is not None:

        if(right == "simple"): r = len(transducers)
        elif(right == "complex"): r = 650*(len(transducers)/32)

        else: r = d1.max
        d2 = get_pressure_wave(x,z, transducers, phase, right)
        data2 = Plot_Data(d2, gif_cmap, vmin=-r, vmax=r, desc=f"{right} Waves")
        plot(data1, data2)
    else:
        plot(data1)


def plot_interference(transducers=transducers, phase=0, phase_shift=0, left=None, right=None):

    d1 = get_interference(x, z, transducers, phase, phase_shift, left)

    if(left == "simple"):r = 50*(len(transducers[0]) / 36)
    elif(left == "complex"): r = 960*(len(transducers[0]) / 36)
    else: r = 0

    data1 = Plot_Data(d1, custom_cmap, vmin=-r, vmax=r, desc=f"{left} Interference")


    if(right is not None):

        d2 = get_interference(x,z, transducers, phase, phase_shift, right)

        if(right == "simple"):r = 50*(len(transducers[0]) / 36)
        elif(right == "complex"): r = 960*(len(transducers[0]) / 36)
        else: r = 0

        data2 = Plot_Data(d2, custom_cmap, vmin=-r, vmax=r, desc=f"{right} Interference")

        plot(data1, data2)
    else:
        plot(data1)


def plot_plane(x=nx, z=nz):

    data = get_pressure_change(x, z, transducers, type="simple")

    fig = plt.figure(num=1, clear=True)
    ax = fig.add_subplot(1, 1, 1, projection='3d')

    ax.plot_surface(x, z, data, cmap=plane_map, vmin=160, vmax=220)
    ax.set(xlabel='x', ylabel='y', zlabel='Pressure Change',
           title='Absolute Pressure Change (by avg)')

    fig.tight_layout()
    plt.show()


def plot_pressure_change(transducers=transducers, phase_shift=0, left=None, right=None, x=x, z=z):

    if left == "simple":basemin=150;basemax=250
    elif left == "complex": basemin=2500;basemax=5000

    d1 = get_pressure_change(x, z, transducers, type=left)
    data1 = Plot_Data(d1, integral_cmap, vmin=basemin*(len(transducers[0])/36), vmax=basemax*(len(transducers[0])/36), desc=f"{left} Pressure Change")

    if(right is not None):

        if right == "simple":base_min=150;basemax=250
        elif right == "complex": basemin=2500;basemax=5000

        d2 = get_pressure_change(x, z, transducers, type=right)
        data2 = Plot_Data(d2, integral_cmap, vmin=basemin*(len(transducers[0])/36), vmax=basemax*(len(transducers[0])/36), desc=f"{right} Pressure Change")

        plot(data1, data2)
    else:
        plot(data1)


def plot_pressure_over_time(transducer, point, type="simple"):

    x = []
    y = []

    for t in range(0,100):
        tn = t/100*2*np.pi
        x.append(tn)
        y.append(models.physics.get_pressure_by_transducer_in_point(point, transducer, tn, "complex"))

    fig=plt.figure(figsize=(5,2.8))
    plt.scatter(x,y)
    plt.show()


if (__name__ == "__main__"):
    setup_levitator()

    x = np.linspace(-.01, .01, params.RES)
    z = np.linspace((params.HEIGHT / 2) - .015, (params.HEIGHT / 2) + .015, params.RES)
    x, z = np.meshgrid(x, z)

    plot_plane()

#TODO: Phase Shift als Argument wahrscheinlich ungeeignet, da bereits in Transducer Klasse enthalten