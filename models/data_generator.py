import numpy as np
from matplotlib import pyplot as plt

from models.helpers import make_list
from models.physics import get_amp_at_point_from_transducer, get_simplified_amp_at_point_from_transducer, get_integral, \
    get_simple_integral

from models.transducer import transducer


def get_pressure_wave(x, z, transducers, phase=0, type='complex'):
    transducers = make_list(
        transducers)  # TODO: Hier landen jetzt in der Regel Tupel -> Tupelinhalt muss geändert werden

    wave = np.zeros((200,200))

    if (type == 'complex'):
        for transducer in transducers:
            wave += get_amp_at_point_from_transducer(np.array([x, 0, z], dtype=object), transducer, 0 + phase)
    elif (type == 'simple'):
        for transducer in transducers:
            wave += get_simplified_amp_at_point_from_transducer(np.array([x, 0, z], dtype=object), transducer, 0 + phase)
    else:
        raise ValueError(f'unsupported value \"{type}\" for argument \"type\" in data generation')

    return wave


def get_interference(x, z, transducers, phase=0, phase_shift=0, type='complex'):
    bottom_wave = get_pressure_wave(x, z, transducers[0], phase, type)
    top_wave = get_pressure_wave(x, z, transducers[1], phase, type)

    return bottom_wave + top_wave


def get_pressure_change(x, z, transducers, phase_shift=0, type="complex"):
    transducers = make_list(transducers)

    interference = np.zeros((200,200))

    if type == "complex":
        for transducer in transducers[0]:
            interference += get_integral(np.array([x, 0, z], dtype=object), transducer)
        for transducer in transducers[1]:
            interference += get_integral(np.array([x, 0, z], dtype=object), transducer)
    elif type == "simple":
        for transducer in transducers[0]:
            interference += get_simple_integral(np.array([x, 0, z], dtype=object), transducer)
        for transducer in transducers[1]:
            interference += get_simple_integral(np.array([x, 0, z], dtype=object), transducer)
    else:
        raise ValueError(f'unsupported value \"{type}\" for argument \"type\" in data generation')


    return interference


if __name__ == "__main__":
    pass
