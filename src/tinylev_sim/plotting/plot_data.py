from dataclasses import dataclass
from typing import Any

import numpy as np


@dataclass(slots=True)
class PlotData:
    data: np.ndarray
    cmap: Any
    vmin: float | None = None
    vmax: float | None = None
    desc: str = ""
    xlabel: str = ""
    ylabel: str = ""
