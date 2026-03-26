import numpy as np

from tinylev_sim.simulation.config import DEFAULT_CONFIG, SimulationConfig
from tinylev_sim.simulation.helpers import make_list
from tinylev_sim.simulation.physics import (
    get_directivity_data,
    get_pressure_by_transducer_in_point,
    get_pressure_change_by_transducer_in_point,
)


def build_point_grid(x: np.ndarray, z: np.ndarray) -> np.ndarray:
    zeros = np.zeros_like(x, dtype=float)
    return np.stack((x, zeros, z), axis=0)


def create_cross_section_grid(
    config: SimulationConfig = DEFAULT_CONFIG,
    x_limits: tuple[float, float] = (-0.05, 0.05),
    z_limits: tuple[float, float] = (0.0, 0.1),
) -> tuple[np.ndarray, np.ndarray]:
    x_values = np.linspace(x_limits[0], x_limits[1], config.resolution)
    z_values = np.linspace(z_limits[0], z_limits[1], config.resolution)
    return np.meshgrid(x_values, z_values)


def create_focus_grid(
    config: SimulationConfig = DEFAULT_CONFIG,
    x_limits: tuple[float, float] = (-0.01, 0.01),
    z_span: float = 0.015,
) -> tuple[np.ndarray, np.ndarray]:
    x_values = np.linspace(x_limits[0], x_limits[1], config.resolution)
    z_values = np.linspace((config.height / 2.0) - z_span, (config.height / 2.0) + z_span, config.resolution)
    return np.meshgrid(x_values, z_values)


def get_far_field_directivity(x: np.ndarray, z: np.ndarray, transducer, config: SimulationConfig = DEFAULT_CONFIG) -> np.ndarray:
    return get_directivity_data(build_point_grid(x, z), transducer, config)


def get_pressure_wave(
    x: np.ndarray,
    z: np.ndarray,
    transducers,
    phase: float = 0.0,
    mode: str = "complex",
    config: SimulationConfig = DEFAULT_CONFIG,
) -> np.ndarray:
    point_grid = build_point_grid(x, z)
    wave = np.zeros_like(x, dtype=float)

    for transducer in make_list(transducers):
        wave += get_pressure_by_transducer_in_point(point_grid, transducer, phase, mode, config)

    return wave


def get_interference(
    x: np.ndarray,
    z: np.ndarray,
    transducers,
    phase: float = 0.0,
    mode: str = "complex",
    config: SimulationConfig = DEFAULT_CONFIG,
) -> np.ndarray:
    bottom_wave = get_pressure_wave(x, z, transducers[0], phase, mode=mode, config=config)
    top_wave = get_pressure_wave(x, z, transducers[1], phase, mode=mode, config=config)
    return bottom_wave + top_wave


def get_pressure_change(
    x: np.ndarray,
    z: np.ndarray,
    transducers,
    mode: str = "complex",
    config: SimulationConfig = DEFAULT_CONFIG,
) -> np.ndarray:
    point_grid = build_point_grid(x, z)
    interference = np.zeros_like(x, dtype=float)

    for transducer in transducers[0]:
        interference += get_pressure_change_by_transducer_in_point(point_grid, transducer, mode, config)

    for transducer in transducers[1]:
        interference += get_pressure_change_by_transducer_in_point(point_grid, transducer, mode, config)

    return interference
