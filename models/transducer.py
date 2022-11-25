import numpy as np
from matplotlib.patches import Circle
from mpl_toolkits.mplot3d import art3d as art3d

from models.params import TRANSDUCER_RADIUS


class transducer:
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
