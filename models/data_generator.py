import numpy as np
from matplotlib import pyplot as plt

from models.helpers import make_list
from models.physics import get_amp_at_point_from_transducer, get_simplified_amp_at_point_from_transducer, get_integral, \
    get_simple_integral

from models.transducer import transducer

def get_pressure_wave(x, z, transducers, phase=0, type='complex'):
    transducers = make_list(transducers) #TODO: Hier landen jetzt in der Regel Tupel -> Tupelinhalt muss geändert werden

    wave_parts = []

    if(type == 'complex'):
        for transducer in transducers:
            wave_parts.append(get_amp_at_point_from_transducer(np.array([x, 0, z]), transducer, 0 + phase))
    elif(type == 'simple'):
        for transducer in transducers:
            wave_parts.append(get_simplified_amp_at_point_from_transducer(np.array([x, 0, z]), transducer, 0 + phase))
    else:
        raise ValueError(f'unsupported value \"{type}\" for argument \"type\" in data generation')

    return sum(wave_parts)

def get_interference(x,z, transducers, phase=0, phase_shift=0, type='complex'):

    bottom_wave = get_pressure_wave(x,z,transducers[0], phase, type)
    top_wave = get_pressure_wave(x,z,transducers[1], phase, type)

    return bottom_wave + top_wave

def get_pressure_change(x,z,transducers, phase_shift=0, type="complex"):

    transducers = make_list(transducers)

    bottom_parts = []
    top_parts = []

    if(type=="complex"):
        for transducer in transducers[0]:
            bottom_parts.append(get_integral(np.array([x,0,z], dtype=object), transducer))
        for transducer in transducers[1]:
            top_parts.append(get_integral(np.array([x, 0, z], dtype=object), transducer))
    elif(type=="simple"):
        for transducer in transducers[0]:
            bottom_parts.append(get_simple_integral(np.array([x,0,z], dtype=object), transducer))
        for transducer in transducers[1]:
            top_parts.append(get_integral(np.array([x, 0, z], dtype=object), transducer))
    else:
        raise ValueError(f'unsupported value \"{type}\" for argument \"type\" in data generation')

    bottom_parts = sum(bottom_parts)
    top_parts = sum(top_parts)


    return sum(bottom_parts, top_parts) #TODO: Einzelne Interferenzen nicht erst in Listen speichern, sondern diret in einer einzigen Hauptliste addieren


if(__name__ == "__main__"):
    print(get_integral([0,0,0.05], transducer(np.array([0,0,0]), np.array([0,0,1]), 0) ))