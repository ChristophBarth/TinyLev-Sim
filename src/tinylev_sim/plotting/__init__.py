from tinylev_sim.plotting.plot_data import PlotData

_PLOT_EXPORTS = {
    "create_simulation",
    "plot_directivity_function",
    "plot_interference",
    "plot_plane",
    "plot_pressure_change",
    "plot_pressure_over_time",
    "plot_pressure_waves",
    "plot_transducers",
}

__all__ = [
    "PlotData",
    *_PLOT_EXPORTS,
]


def __getattr__(name: str):
    if name in _PLOT_EXPORTS:
        from tinylev_sim.plotting import plots

        return getattr(plots, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
