import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

from tinylev_sim.plotting.plot_data import PlotData
from tinylev_sim.simulation import DEFAULT_CONFIG, SimulationConfig, Transducer, generate_transducers
from tinylev_sim.simulation.fields import (
    create_cross_section_grid,
    create_focus_grid,
    get_far_field_directivity,
    get_interference,
    get_pressure_change,
    get_pressure_wave,
)
from tinylev_sim.simulation.helpers import make_list
from tinylev_sim.simulation.physics import get_pressure_by_transducer_in_point


CUSTOM_CMAP = LinearSegmentedColormap.from_list("custom", ["red", "white", "blue"])
INTEGRAL_CMAP = LinearSegmentedColormap.from_list("custom", ["black", "black", "red", "yellow", "white"])
GIF_CMAP = LinearSegmentedColormap.from_list("custom", ["black", "white", "black"])
DIRECTIVITY_CMAP = LinearSegmentedColormap.from_list("custom", ["white", "black"])
PLANE_MAP = LinearSegmentedColormap.from_list("custom", ["blue", "red"])


def _plot(*plots: PlotData) -> None:
    plt.rcParams["axes.grid"] = False

    if len(plots) == 1:
        plt.figure(figsize=(4, 2.8))

    for index, plot_data in enumerate(plots):
        plt.subplot(1, len(plots), index + 1)
        plt.imshow(plot_data.data, vmin=plot_data.vmin, vmax=plot_data.vmax, cmap=plot_data.cmap, origin="lower")
        plt.title(plot_data.desc)
        plt.xlabel(plot_data.xlabel)
        plt.ylabel(plot_data.ylabel)
        plt.colorbar(shrink=0.43)

    plt.tight_layout()
    plt.show()


def create_simulation(
    rings: int = 4,
    config: SimulationConfig = DEFAULT_CONFIG,
) -> tuple[tuple[list[Transducer], list[Transducer]], np.ndarray, np.ndarray]:
    transducers = generate_transducers(rings=rings, config=config)
    x, z = create_cross_section_grid(config=config, z_limits=(0.0, config.height))
    return transducers, x, z


def plot_directivity_function(
    transducer: Transducer | None = None,
    config: SimulationConfig = DEFAULT_CONFIG,
) -> None:
    x, z = create_cross_section_grid(config=config, z_limits=(0.0, config.height))
    active_transducer = transducer or Transducer(np.array([0.0, 0.0, 0.0]), np.array([0.0, 0.0, 1.0]), 0.0)
    directivity = get_far_field_directivity(x, z, active_transducer, config)
    _plot(PlotData(directivity, DIRECTIVITY_CMAP, desc="Directivity"))


def plot_transducers(
    bottom_transducers: list[Transducer] | Transducer | None = None,
    top_transducers: list[Transducer] | Transducer | None = None,
    config: SimulationConfig = DEFAULT_CONFIG,
) -> None:
    if bottom_transducers is not None and top_transducers is not None:
        active_bottom = make_list(bottom_transducers)
        active_top = make_list(top_transducers)
    else:
        active_bottom, active_top = generate_transducers(config=config)

    ax = plt.figure().add_subplot(projection="3d")

    for transducer in active_top:
        transducer.plot(ax, config)

    for transducer in active_bottom:
        transducer.plot(ax, config)

    plt.show()


def plot_pressure_waves(
    transducers: list[Transducer] | Transducer | None = None,
    phase: float = 0.0,
    phase_shift: float = 0.0,
    left: str = "simple",
    right: str | None = "complex",
    config: SimulationConfig = DEFAULT_CONFIG,
) -> None:
    del phase_shift
    active_transducers = make_list(transducers) if transducers is not None else generate_transducers(config=config)[0]
    x, z = create_cross_section_grid(config=config, z_limits=(0.0, config.height))

    left_wave = get_pressure_wave(x, z, active_transducers, phase=phase, mode=left, config=config)
    left_range = len(active_transducers) if left == "simple" else 650 * (len(active_transducers) / 32)
    left_plot = PlotData(left_wave, GIF_CMAP, vmin=-left_range, vmax=left_range, desc=f"{left} Waves")

    if right is None:
        _plot(left_plot)
        return

    right_wave = get_pressure_wave(x, z, active_transducers, phase=phase, mode=right, config=config)
    right_range = len(active_transducers) if right == "simple" else 650 * (len(active_transducers) / 32)
    right_plot = PlotData(right_wave, GIF_CMAP, vmin=-right_range, vmax=right_range, desc=f"{right} Waves")
    _plot(left_plot, right_plot)


def plot_interference(
    transducers: tuple[list[Transducer], list[Transducer]] | None = None,
    phase: float = 0.0,
    phase_shift: float = 0.0,
    left: str = "simple",
    right: str | None = "complex",
    config: SimulationConfig = DEFAULT_CONFIG,
) -> None:
    del phase_shift
    active_transducers = transducers or generate_transducers(config=config)
    x, z = create_cross_section_grid(config=config, z_limits=(0.0, config.height))

    left_data = get_interference(x, z, active_transducers, phase=phase, mode=left, config=config)
    left_range = 50 * (len(active_transducers[0]) / 36) if left == "simple" else 960 * (len(active_transducers[0]) / 36)
    left_plot = PlotData(left_data, CUSTOM_CMAP, vmin=-left_range, vmax=left_range, desc=f"{left} Interference")

    if right is None:
        _plot(left_plot)
        return

    right_data = get_interference(x, z, active_transducers, phase=phase, mode=right, config=config)
    right_range = (
        50 * (len(active_transducers[0]) / 36) if right == "simple" else 960 * (len(active_transducers[0]) / 36)
    )
    right_plot = PlotData(right_data, CUSTOM_CMAP, vmin=-right_range, vmax=right_range, desc=f"{right} Interference")
    _plot(left_plot, right_plot)


def plot_plane(
    transducers: tuple[list[Transducer], list[Transducer]] | None = None,
    x: np.ndarray | None = None,
    z: np.ndarray | None = None,
    config: SimulationConfig = DEFAULT_CONFIG,
) -> None:
    active_transducers = transducers or generate_transducers(config=config)
    if x is None or z is None:
        x, z = create_focus_grid(config=config)
    data = get_pressure_change(x, z, active_transducers, mode="simple", config=config)

    fig = plt.figure(num=1, clear=True)
    ax = fig.add_subplot(1, 1, 1, projection="3d")
    ax.plot_surface(x, z, data, cmap=PLANE_MAP, vmin=160, vmax=220)
    ax.set(xlabel="x", ylabel="y", zlabel="Pressure Change", title="Absolute Pressure Change")
    fig.tight_layout()
    plt.show()


def plot_pressure_change(
    transducers: tuple[list[Transducer], list[Transducer]] | None = None,
    phase_shift: float = 0.0,
    left: str = "simple",
    right: str | None = "complex",
    x: np.ndarray | None = None,
    z: np.ndarray | None = None,
    config: SimulationConfig = DEFAULT_CONFIG,
) -> None:
    active_transducers = transducers or generate_transducers(config=config)
    if x is None or z is None:
        x, z = create_cross_section_grid(config=config, z_limits=(0.0, config.height))

    base_min, base_max = (150, 250) if left == "simple" else (2500, 5000)
    left_data = get_pressure_change(x, z, active_transducers, mode=left, config=config)
    left_plot = PlotData(
        left_data,
        INTEGRAL_CMAP,
        vmin=base_min * (len(active_transducers[0]) / 36),
        vmax=base_max * (len(active_transducers[0]) / 36),
        desc=f"{left} Pressure Change",
    )

    if right is None:
        _plot(left_plot)
        return

    right_min, right_max = (150, 250) if right == "simple" else (2500, 5000)
    right_data = get_pressure_change(x, z, active_transducers, mode=right, config=config)
    right_plot = PlotData(
        right_data,
        INTEGRAL_CMAP,
        vmin=right_min * (len(active_transducers[0]) / 36),
        vmax=right_max * (len(active_transducers[0]) / 36),
        desc=f"{right} Pressure Change",
    )
    _plot(left_plot, right_plot)


def plot_pressure_over_time(
    transducer: Transducer,
    point: np.ndarray,
    mode: str = "complex",
    config: SimulationConfig = DEFAULT_CONFIG,
) -> None:
    phases = np.linspace(0.0, 2.0 * np.pi, 100)
    point_grid = np.asarray(point, dtype=float).reshape(3, 1, 1)
    pressures = [get_pressure_by_transducer_in_point(point_grid, transducer, phase, mode, config).item() for phase in phases]

    plt.figure(figsize=(5, 2.8))
    plt.scatter(phases, pressures)
    plt.show()
