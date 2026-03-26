import math

import numpy as np

from tinylev_sim.simulation.config import DEFAULT_CONFIG, SimulationConfig
from tinylev_sim.simulation.helpers import get_angle_to_transducer_normal, get_distance_to_transducer


def _bessel_j1(values: np.ndarray, terms: int = 12) -> np.ndarray:
    result = np.zeros_like(values, dtype=float)
    half_values = values / 2.0

    for order in range(terms):
        numerator = (-1.0) ** order * np.power(half_values, (2 * order) + 1)
        denominator = math.factorial(order) * math.factorial(order + 1)
        result += numerator / denominator

    return result


def far_field_directivity(theta: np.ndarray, config: SimulationConfig = DEFAULT_CONFIG) -> np.ndarray:
    temp = config.k * config.transducer_radius * np.sin(theta)
    numerator = 2.0 * _bessel_j1(temp)
    return np.where(np.isclose(temp, 0.0), 1.0, numerator / temp)


def get_pressure_by_transducer_in_point(
    point: np.ndarray,
    transducer,
    phase: float,
    mode: str,
    config: SimulationConfig = DEFAULT_CONFIG,
) -> np.ndarray:
    distance = get_distance_to_transducer(point, transducer)
    shifted_phase = phase + transducer.phase_shift

    if mode == "complex":
        theta = get_angle_to_transducer_normal(point, transducer)
        directivity = far_field_directivity(theta, config)
        return (
            config.base_amplitude
            * directivity
            / distance
            * np.real(np.exp(1j * (-(shifted_phase + (np.pi / 2.0)) + config.k * distance)))
        )
    if mode == "simple":
        return config.base_amplitude * np.sin(-shifted_phase + config.k * distance)
    raise ValueError(f'Unsupported value "{mode}" for parameter "mode"')


def get_directivity_data(point: np.ndarray, transducer, config: SimulationConfig = DEFAULT_CONFIG) -> np.ndarray:
    theta = get_angle_to_transducer_normal(point, transducer)
    return far_field_directivity(theta, config)


def pressure_change_by_transducer_in_point(
    phase: float,
    distance: np.ndarray,
    amplitude: np.ndarray,
    config: SimulationConfig = DEFAULT_CONFIG,
) -> np.ndarray:
    return amplitude * np.exp(1j * (-(phase + (np.pi / 2.0)) + config.k * distance))


def get_pressure_change_by_transducer_in_point(
    point: np.ndarray,
    transducer,
    mode: str,
    config: SimulationConfig = DEFAULT_CONFIG,
) -> np.ndarray:
    distance = get_distance_to_transducer(point, transducer)

    if mode == "complex":
        theta = get_angle_to_transducer_normal(point, transducer)
        directivity = far_field_directivity(theta, config)
        amplitude = config.base_amplitude * directivity / distance
        return np.abs(
            np.real(pressure_change_by_transducer_in_point(np.pi, distance, amplitude, config))
            - np.real(pressure_change_by_transducer_in_point(0.0, distance, amplitude, config))
        ) + np.abs(
            np.real(pressure_change_by_transducer_in_point(2.0 * np.pi, distance, amplitude, config))
            - np.real(pressure_change_by_transducer_in_point(np.pi, distance, amplitude, config))
        )
    if mode == "simple":
        return np.abs(np.cos(config.k * distance + np.pi) - np.cos(config.k * distance)) + np.abs(
            np.cos(config.k * distance + 2.0 * np.pi) - np.cos(config.k * distance + np.pi)
        )
    raise ValueError(f'Unsupported value "{mode}" for parameter "mode"')
