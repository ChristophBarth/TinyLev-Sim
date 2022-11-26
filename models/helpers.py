import numpy as np

from models.transducer import transducer


def get_distance_to_transducer(p, transducer):
    return (np.sqrt(
        (p[0] - transducer.pos[0]) ** 2 +
        (p[1] - transducer.pos[1]) ** 2 +
        (p[2] - transducer.pos[2]) ** 2)
    )


def get_angle_to_transducer_normal(vector_0P, transducer):
    vector_0T = transducer.pos  # vector from origin to transducer
    vector_TP = vector_0P - vector_0T  # vector from transducer to point

    dot_product = np.dot(transducer.norm, vector_TP)
    return (np.arccos(
        dot_product / (np.sqrt(np.dot(transducer.norm, transducer.norm)) * np.sqrt(np.dot(vector_TP, vector_TP)))))


def make_list(input):
    if isinstance(input, transducer): input = [input]

    return input
