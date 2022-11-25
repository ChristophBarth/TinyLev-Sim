import numpy as np

from models.params import HEIGHT, CENTER, TRANSDUCER_RADIUS, TRANSDUCER_OFFSET
from models.transducer import transducer


def generate_transducers():
    bottom_origin = np.array([0,0,0])
    top_origin = np.array([0, 0, HEIGHT])

    vector_0MB = CENTER - bottom_origin
    vector_0MT = CENTER - top_origin

    bottom_transducers = []
    top_transducers = []


    for i in range(1,4):
        num_of_transducers = 6*i
        min_circumference = num_of_transducers*(TRANSDUCER_RADIUS * 2 + TRANSDUCER_OFFSET)
        radius = min_circumference/(2*np.pi)
        z_offset = (HEIGHT / 2) - np.sqrt((HEIGHT / 2) ** 2 - radius ** 2)

        for n in range(num_of_transducers):

            alpha = n*np.pi*2/num_of_transducers
            x_offset = np.cos(alpha)*radius
            y_offset = np.sin(alpha)*radius

            vector_transducer = np.array([x_offset, y_offset, z_offset])
            norm = vector_0MB-vector_transducer
            bottom_transducers.append(transducer((bottom_origin + vector_transducer), norm, 0))

            vector_transducer = np.array([x_offset, y_offset, -z_offset])
            norm = vector_0MT-vector_transducer
            top_transducers.append(transducer((top_origin + vector_transducer), norm, np.pi))
            pass
    return bottom_transducers,top_transducers


def get_distance_to_transducer(p, transducer):
    return( np.sqrt(
        (p[0]-transducer.pos[0])**2+
        (p[1]-transducer.pos[1])**2+
        (p[2]-transducer.pos[2])**2)
    )


def get_angle_to_transducer_normal(vector_0P, transducer):
    vector_0T = transducer.pos #vector from origin to transducer
    vector_TP = vector_0P-vector_0T #vector from transducer to point

    dot_product = np.dot(transducer.norm,vector_TP)
    return(np.arccos(dot_product/(np.sqrt(np.dot(transducer.norm, transducer.norm))*np.sqrt(np.dot(vector_TP, vector_TP)))))
