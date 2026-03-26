# GoldenViz

GoldenViz is a lightweight visual QA layer for Matplotlib charts. It checks whether a figure follows the first five Golden Rules of data visualization and can render the result directly under charts in Jupyter notebooks.

## Implemented rules

GoldenViz currently checks these five rules:

1. clear title
2. axis labels
3. appropriate scale
4. chart type
5. readable labels and ticks

## Installation

```bash
pip install -e .
```

## Quick start

### Manual check

```python
import matplotlib.pyplot as plt
import GoldenViz as gv

fig, ax = plt.subplots()
ax.bar(["A", "B", "C"], [10, 15, 8])
ax.set_title("Sales by category")
ax.set_xlabel("Category")
ax.set_ylabel("Sales ($)")

gv.check(fig)
```

### Automatic mode in Jupyter

```python
import GoldenViz as gv

gv.auto()
```

After `gv.auto()` is enabled, GoldenViz hooks into Matplotlib display and shows a report below each generated chart in notebook environments.

## Public API

- `gv.analyze(fig=None)` returns a structured figure report
- `gv.check(fig=None, display=True)` analyzes and displays the report
- `gv.check_current(display=True)` analyzes the current figure
- `gv.auto()` enables automatic reporting
- `gv.disable()` disables automatic reporting

## Project structure

```text
src/GoldenViz/
├── __init__.py
├── analyzer.py
├── auto.py
├── display.py
├── renderers.py
├── _results.py
├── _utils.py
└── rules/
    ├── axis_labels.py
    ├── chart_type.py
    ├── readability.py
    ├── scale.py
    └── title.py
```

## Notebook examples

See `notebooks/first_five_rules_demo.ipynb` for working examples of every implemented rule, including both problematic and corrected charts.

## Documentation

The Sphinx docs in `docs/` are ready to publish to Read the Docs and cover installation, notebook usage, automatic mode, and the implemented rule set.
