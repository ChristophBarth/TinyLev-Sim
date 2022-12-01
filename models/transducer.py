import numpy as np
from matplotlib.patches import Circle
from mpl_toolkits.mplot3d import art3d as art3d
from models.params import TRANSDUCER_RADIUS, HEIGHT, CENTER, TRANSDUCER_OFFSET

class Transducer:
    def __init__(self, x,y,z,norm, phase_shift):
        self.pos = np.array([x,y,z])
        self.norm = norm
        self.phase_shift = phase_shift

    def __init__(self, pos, norm, phase_shift):
        self.pos = pos
        self.norm = norm
        self.phase_shift = phase_shift

    def plot(self, ax):
        ax.quiver(self.pos[0], self.pos[1], self.pos[2],
                  self.norm[0], self.norm[1], self.norm[2],
                  length=.025,
                  normalize=True)

        p = Circle((0, 0), TRANSDUCER_RADIUS, color='black', alpha=.3)
        ax.add_patch(p)
        art3d.pathpatch_2d_to_3d(p, self.pos[2], 'z')

        ax.scatter(self.pos[0],self.pos[1], self.pos[2], color='black')

def generate_transducers(rings=4):
    bottom_origin = np.array([0,0,0])
    top_origin = np.array([0, 0, HEIGHT])

    vector_0MB = CENTER - bottom_origin
    vector_0MT = CENTER - top_origin

    bottom_transducers = []
    top_transducers = []


    for i in range(1,rings):
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
            bottom_transducers.append(Transducer((bottom_origin + vector_transducer), norm, 0))

            vector_transducer = np.array([x_offset, y_offset, -z_offset])
            norm = vector_0MT-vector_transducer
            top_transducers.append(Transducer((top_origin + vector_transducer), norm, np.pi))
            pass
    return bottom_transducers,top_transducers
