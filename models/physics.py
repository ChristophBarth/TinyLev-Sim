import numpy as np
import scipy.special as sp

import models.transducer
from models.helpers import get_distance_to_transducer, get_angle_to_transducer_normal
from models.params import TRANSDUCER_RADIUS, BASE_AMP, K


def far_field_directivity(theta, k=K, a=TRANSDUCER_RADIUS):
    temp = k * a * np.sin(theta)

    if temp == 0:
        return 1
    else:
        return (2 * sp.jn(1, (temp))) / (temp)


get_far_field_directivity = np.vectorize(far_field_directivity)


def get_pressure_by_transducer_in_point(p, transducer, phase, type):
    d = get_distance_to_transducer(p, transducer)
    if type == 'complex':
        theta = get_angle_to_transducer_normal(p, transducer)
        far_field_directivity = get_far_field_directivity(theta, K, TRANSDUCER_RADIUS)
        return BASE_AMP * far_field_directivity / d * np.exp(1j * (-phase + K * d)).real
    elif type == 'simple':
        return BASE_AMP * np.sin(-phase + K * d)
    else:
        raise ValueError(f"Unsupported value \"{type}\" for parameter \"type\"")

def get_directivity_data(p, transducer):
    d = get_distance_to_transducer(p, transducer)
    theta = get_angle_to_transducer_normal(p, transducer)
    far_field_directivity = get_far_field_directivity(theta, K, TRANSDUCER_RADIUS)
    return far_field_directivity


def pressure_change_by_transducer_in_point(t, d, k):
    return k * np.exp(1j * (-t + K * d))


def get_pressure_change_by_transducer_in_point(p, transducer, type):
    d = get_distance_to_transducer(p, transducer)
    if type == 'complex':
        theta = get_angle_to_transducer_normal(p, transducer)
        far_field_directivity = get_far_field_directivity(K, TRANSDUCER_RADIUS, theta)
        k = BASE_AMP * far_field_directivity / d
        return \
            abs(
                pressure_change_by_transducer_in_point(np.pi, d, k).real
                - pressure_change_by_transducer_in_point(0, d, k).real
            ) + \
            abs(
                pressure_change_by_transducer_in_point(2 * np.pi, d, k).real
                - pressure_change_by_transducer_in_point(np.pi, d, k).real
            )
    elif type == 'simple':
        return abs(np.cos(K * d + np.pi) - np.cos(K * d)) + abs(np.cos(K * d + np.pi * 2) - np.cos(K * d + np.pi))
    else:
        raise ValueError(f"Unsupported value \"{type}\" for parameter \"type\"")

if __name__ == "__main__":
    test_transducer = models.transducer.Transducer(np.array([0,0,0]), np.array([0,0,1]), 0)
    print(get_pressure_change_by_transducer_in_point(np.array([0,0,1E-3]), test_transducer, "complex"))