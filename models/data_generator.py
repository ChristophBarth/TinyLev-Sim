import numpy as np
from models.helpers import make_list
from models.physics import get_pressure_by_transducer_in_point, get_pressure_change_by_transducer_in_point, get_directivity_data


def get_pressure_wave(x, z, transducers, phase=0, type='complex'):
    transducers = make_list(
        transducers)  # TODO: Hier landen jetzt in der Regel Tupel -> Tupelinhalt muss geändert werden


    wave = np.zeros((200,200))

    for transducer in transducers:
        wave += get_pressure_by_transducer_in_point(np.array([x, 0, z], dtype=object), transducer, 0 + phase, type)

    return wave


def get_interference(x, z, transducers, phase=0, phase_shift=0, type='complex'):
    bottom_wave = get_pressure_wave(x, z, transducers[0], phase, type)
    top_wave = get_pressure_wave(x, z, transducers[1], phase, type)

    return bottom_wave + top_wave


def get_pressure_change(x, z, transducers, phase_shift=0, type="complex"):
    transducers = make_list(transducers)

    interference = np.zeros((200,200))

    for transducer in transducers[0]:
        interference += get_pressure_change_by_transducer_in_point(np.array([x, 0, z], dtype=object), transducer, type)
    for transducer in transducers[1]:
        interference += get_pressure_change_by_transducer_in_point(np.array([x, 0, z], dtype=object), transducer, type)

    return interference

def get_far_field_directivity(x, z, transducer):
    return(get_directivity_data(np.array([x,0,z], dtype=object), transducer))

if __name__ == "__main__":
    pass
