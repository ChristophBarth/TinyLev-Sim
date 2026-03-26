from collections.abc import Iterable

import numpy as np


def get_distance_to_transducer(point: np.ndarray, transducer) -> np.ndarray:
    return np.linalg.norm(point - transducer.pos[:, None, None], axis=0)


def get_angle_to_transducer_normal(point: np.ndarray, transducer) -> np.ndarray:
    transducer_to_point = point - transducer.pos[:, None, None]
    dot_product = np.sum(transducer.norm[:, None, None] * transducer_to_point, axis=0)
    normal_norm = np.linalg.norm(transducer.norm)
    point_norm = np.linalg.norm(transducer_to_point, axis=0)
    cosine = dot_product / (normal_norm * point_norm)
    return np.arccos(np.clip(cosine, -1.0, 1.0))


def make_list(value) -> list:
    if isinstance(value, Iterable) and not isinstance(value, np.ndarray):
        return list(value)
    return [value]
