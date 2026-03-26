"""Small internal helpers used by analyzers and rules."""

from __future__ import annotations

from typing import List

from matplotlib.axes import Axes


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
    return len(widths) >= 5 and len(set(widths)) <= max(1, len(widths) // 3)



def axis_kind(ax: Axes) -> str:
    """Classify an axis into a small set of chart types used by the rules."""
    if is_bar_chart(ax):
        return "bar"
    if is_histogram(ax):
        return "histogram"
    if is_scatter_chart(ax) and not ax.lines:
        return "scatter"
    if is_line_chart(ax):
        return "line"
    return "other"



def stringify_label(label: str) -> str:
    """Normalize axis label text by converting ``None``-like values to empty strings."""
    return (label or "").strip()
