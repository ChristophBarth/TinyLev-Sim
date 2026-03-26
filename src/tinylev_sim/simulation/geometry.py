from dataclasses import dataclass

import numpy as np

from tinylev_sim.simulation.config import DEFAULT_CONFIG, SimulationConfig


@dataclass(slots=True)
class Transducer:
    pos: np.ndarray
    norm: np.ndarray
    phase_shift: float = 0.0

    def __post_init__(self) -> None:
        self.pos = np.asarray(self.pos, dtype=float)
        self.norm = np.asarray(self.norm, dtype=float)

    def plot(self, ax, config: SimulationConfig = DEFAULT_CONFIG) -> None:
        from matplotlib.patches import Circle
        from mpl_toolkits.mplot3d import art3d

        ax.quiver(
            self.pos[0],
            self.pos[1],
            self.pos[2],
            self.norm[0],
            self.norm[1],
            self.norm[2],
            length=0.025,
            normalize=True,
        )

        patch = Circle((0, 0), config.transducer_radius, color="black", alpha=0.3)
        ax.add_patch(patch)
        art3d.pathpatch_2d_to_3d(patch, self.pos[2], "z")
        ax.scatter(self.pos[0], self.pos[1], self.pos[2], color="black")


def generate_transducers(
    rings: int = 4,
    config: SimulationConfig = DEFAULT_CONFIG,
) -> tuple[list[Transducer], list[Transducer]]:
    bottom_origin = np.array([0.0, 0.0, 0.0], dtype=float)
    top_origin = np.array([0.0, 0.0, config.height], dtype=float)

    bottom_target = config.center - bottom_origin
    top_target = config.center - top_origin

    bottom_transducers: list[Transducer] = []
    top_transducers: list[Transducer] = []

    for ring_index in range(1, rings):
        transducer_count = 6 * ring_index
        min_circumference = transducer_count * (config.transducer_radius * 2.0 + config.transducer_offset)
        radius = min_circumference / (2.0 * np.pi)
        z_offset = (config.height / 2.0) - np.sqrt((config.height / 2.0) ** 2 - radius**2)

        for transducer_index in range(transducer_count):
            alpha = transducer_index * 2.0 * np.pi / transducer_count
            x_offset = np.cos(alpha) * radius
            y_offset = np.sin(alpha) * radius

            bottom_vector = np.array([x_offset, y_offset, z_offset], dtype=float)
            bottom_transducers.append(Transducer(bottom_origin + bottom_vector, bottom_target - bottom_vector, 0.0))

            top_vector = np.array([x_offset, y_offset, -z_offset], dtype=float)
            top_transducers.append(Transducer(top_origin + top_vector, top_target - top_vector, np.pi))

    return bottom_transducers, top_transducers
