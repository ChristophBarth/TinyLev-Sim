import numpy as np
import scipy.special as sp

from models.helpers import get_distance_to_transducer, get_angle_to_transducer_normal
from models.params import TRANSDUCER_RADIUS, BASE_AMP, K


def get_far_field_directivity(k,a,theta):
    temp = k*a*np.sin(theta)
    if temp == 0: return 1
    else: return (2*sp.jn(1,(temp)))/(temp)
    #return (2 * sp.jn(1, (temp))) / (temp)

vfunc = np.vectorize(get_far_field_directivity)

def get_amp_at_point_from_transducer(p, transducer, phase):

    d = get_distance_to_transducer(p, transducer)
    theta = get_angle_to_transducer_normal(p, transducer)
    far_field_directivity = vfunc(K, TRANSDUCER_RADIUS, theta)

    return BASE_AMP * far_field_directivity / d * np.exp(1j * (-phase + K * d)).real

def get_simplified_amp_at_point_from_transducer(p, transducer, phase):
    d = get_distance_to_transducer(p, transducer)
    return(BASE_AMP * np.sin(-phase + K * d))

def F(t,d,k):
    return k*np.exp(1j * (-t + K * d))

def get_simple_integral(p,transducer):
    d = get_distance_to_transducer(p, transducer)
    return abs(np.cos(K * d + np.pi) - np.cos(K * d)) + abs(np.cos(K * d + np.pi * 2) - np.cos(K * d + np.pi))

def get_integral(p, transducer):
    d = get_distance_to_transducer(p, transducer)
    theta = get_angle_to_transducer_normal(p, transducer)
    far_field_directivity = vfunc(K, TRANSDUCER_RADIUS, theta)

    k = BASE_AMP * far_field_directivity / d
    return abs(F(np.pi,d,k).real-F(0,d,k).real)+abs(F(2*np.pi,d,k).real-F(np.pi,d,k).real)





if(__name__ == "__main__"):
    pass