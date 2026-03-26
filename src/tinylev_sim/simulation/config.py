from dataclasses import dataclass

import numpy as np


@dataclass(slots=True, frozen=True)
class SimulationConfig:
    transducer_offset: float = 0.0
    height: float = 0.1
    sound_velocity: float = 343.0
    transducer_radius: float = 0.005
    base_frequency: float = 40000.0
    base_amplitude: float = 1.0
    resolution: int = 200

    @property
    def period(self) -> float:
        return 1.0 / self.base_frequency

    @property
    def wave_length(self) -> float:
        return self.sound_velocity / self.base_frequency

    @property
    def k(self) -> float:
        return 2.0 * np.pi / self.wave_length

    @property
    def center(self) -> np.ndarray:
        return np.array([0.0, 0.0, self.height / 2.0], dtype=float)


DEFAULT_CONFIG = SimulationConfig()
