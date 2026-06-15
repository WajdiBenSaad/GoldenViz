"""Small internal helpers used by analyzers and rules."""

from __future__ import annotations

from statistics import median
from typing import List

from matplotlib.axes import Axes
from matplotlib.patches import Wedge


def is_notebook_environment() -> bool:
    """Return ``True`` when GoldenViz appears to run inside a notebook kernel.

    The check intentionally stays lightweight because it is called both by manual
    rendering code and by the automatic hook logic.
    """
    try:
        from IPython import get_ipython

        shell = get_ipython()
        if shell is None:
            return False
        return shell.__class__.__name__ in {"ZMQInteractiveShell", "Shell"}
    except Exception:
        return False



def visible_axes(fig) -> List[Axes]:
    """Return visible subplot axes from a Matplotlib figure.

    GoldenViz focuses on standard plotting axes and ignores invisible axes or axes
    that do not behave like regular subplots.
    """
    return [ax for ax in fig.axes if ax.get_visible() and hasattr(ax, "get_subplotspec")]



def ensure_canvas_drawn(fig) -> None:
    """Trigger a canvas draw when possible.

    Some rules depend on renderer information such as tick label extents. A best-
    effort draw makes those measurements available without failing hard if a backend
    does not support it.
    """
    try:
        fig.canvas.draw()
    except Exception:
        pass



def is_bar_chart(ax: Axes) -> bool:
    """Return whether the axis looks like a bar chart."""
    return len(ax.containers) > 0 and any(getattr(container, "patches", None) for container in ax.containers)



def is_line_chart(ax: Axes) -> bool:
    """Return whether the axis looks like a line chart."""
    return len(ax.lines) > 0 and not is_bar_chart(ax)



def is_scatter_chart(ax: Axes) -> bool:
    """Return whether the axis looks like a scatter plot."""
    return len(ax.collections) > 0



def is_histogram(ax: Axes) -> bool:
    """Heuristically detect histogram-like patch collections."""
    patches = ax.patches
    if not patches:
        return False
    widths = [round(p.get_width(), 8) for p in patches if hasattr(p, "get_width")]
    x_positions = sorted(round(p.get_x(), 8) for p in patches if hasattr(p, "get_x"))
    if len(widths) < 5 or len(set(widths)) > max(1, len(widths) // 3):
        return False
    if len(x_positions) < 2:
        return False
    typical_width = median(abs(width) for width in widths)
    gaps = [right - left for left, right in zip(x_positions, x_positions[1:])]
    return median(gaps) <= typical_width * 1.05


def is_pie_chart(ax: Axes) -> bool:
    """Return whether the axis looks like a pie chart."""
    wedges = [patch for patch in ax.patches if isinstance(patch, Wedge)]
    return len(wedges) >= 2 and ax.get_aspect() in {"equal", 1.0}


def bar_orientation(ax: Axes) -> str:
    """Infer whether bar marks are vertical, horizontal, or unclear."""
    patches = [patch for patch in ax.patches if hasattr(patch, "get_width") and hasattr(patch, "get_height")]
    if not patches:
        return "unknown"

    near_zero_x = sum(abs(patch.get_x()) < 1e-9 for patch in patches)
    near_zero_y = sum(abs(patch.get_y()) < 1e-9 for patch in patches)
    if near_zero_x > near_zero_y:
        return "horizontal"
    if near_zero_y > near_zero_x:
        return "vertical"

    widths = [abs(patch.get_width()) for patch in patches]
    heights = [abs(patch.get_height()) for patch in patches]
    if median(widths) > median(heights):
        return "horizontal"
    if median(heights) > median(widths):
        return "vertical"
    return "unknown"



def axis_kind(ax: Axes) -> str:
    """Classify an axis into a small set of chart types used by the rules."""
    if is_pie_chart(ax):
        return "pie"
    if is_histogram(ax):
        return "histogram"
    if is_bar_chart(ax):
        return "bar"
    if is_scatter_chart(ax) and not ax.lines:
        return "scatter"
    if is_line_chart(ax):
        return "line"
    return "other"



def stringify_label(label: str) -> str:
    """Normalize axis label text by converting ``None``-like values to empty strings."""
    return (label or "").strip()
