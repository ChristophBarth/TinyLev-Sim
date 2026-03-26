# TinyLev-Sim

TinyLev-Sim is a compact Python project for simulating acoustic pressure fields in a ring-based ultrasonic levitator.

## Project layout

- `src/tinylev_sim/simulation/`: configuration, geometry, physics, and field generation
- `src/tinylev_sim/plotting/`: plotting data models and matplotlib helpers
- `models/`: compatibility wrappers for the older notebook-oriented module layout
- `notebooks/`: exploratory notebook work

## Quick start

1. Create a virtual environment and install the project:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

2. Run a quick verification:

```bash
pytest
```

3. Open a notebook or use the plotting helpers:

```python
from tinylev_sim.plotting import plot_interference

plot_interference(left="simple", right="complex")
```

## Notes

- The simulation package is separated from plotting code under `src/tinylev_sim/`.
- The computation modules avoid import-time side effects.
- Legacy imports such as `models.plottings` and `models.data_generator` still work as compatibility shims.
- Notebook artifacts and Python cache files are ignored by default.
