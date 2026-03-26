from __future__ import annotations

from typing import Iterable, List

import matplotlib
from matplotlib.axes import Axes


def is_notebook_environment() -> bool:
    try:
        from IPython import get_ipython

        shell = get_ipython()
        if shell is None:
            return False
        return shell.__class__.__name__ in {"ZMQInteractiveShell", "Shell"}
    except Exception:
        return False



def visible_axes(fig) -> List[Axes]:
    return [ax for ax in fig.axes if ax.get_visible() and hasattr(ax, "get_subplotspec")]



def ensure_canvas_drawn(fig) -> None:
    try:
        fig.canvas.draw()
    except Exception:
        pass



def is_bar_chart(ax: Axes) -> bool:
    return len(ax.containers) > 0 and any(getattr(container, "patches", None) for container in ax.containers)



def is_line_chart(ax: Axes) -> bool:
    return len(ax.lines) > 0 and not is_bar_chart(ax)



def is_scatter_chart(ax: Axes) -> bool:
    return len(ax.collections) > 0



def is_histogram(ax: Axes) -> bool:
    patches = ax.patches
    if not patches:
        return False
    widths = [round(p.get_width(), 8) for p in patches if hasattr(p, "get_width")]
    return len(widths) >= 5 and len(set(widths)) <= max(1, len(widths) // 3)



def axis_kind(ax: Axes) -> str:
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
    return (label or "").strip()
