"""Automatic integration hooks for notebooks and regular Matplotlib usage."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Optional

import matplotlib.pyplot as plt

from GoldenViz.analyzer import analyze
from GoldenViz.display import display_report
from GoldenViz._utils import is_notebook_environment


@dataclass
class _AutoState:
    """Mutable runtime state for GoldenViz auto mode."""

    enabled: bool = False
    mode: Optional[str] = None
    original_show: Optional[Callable] = None
    original_figure_repr_mimebundle: Optional[Callable] = None
    reported_tokens: set = field(default_factory=set)


_STATE = _AutoState()



def _figure_token(fig) -> int:
    """Return a stable runtime token used to avoid duplicate reports."""
    return id(fig)



def _report_figure(fig) -> None:
    """Render an analysis report for one figure if it has not been reported yet."""
    if fig is None or not getattr(fig, "axes", None):
        return
    token = _figure_token(fig)
    if token in _STATE.reported_tokens:
        return
    _STATE.reported_tokens.add(token)
    display_report(analyze(fig))



def _patch_matplotlib_show() -> None:
    """Wrap :func:`matplotlib.pyplot.show` for non-notebook environments."""
    if _STATE.original_show is not None:
        return
    _STATE.original_show = plt.show

    def wrapped_show(*args, **kwargs):
        """Display the original figures first, then render GoldenViz reports."""
        managers = list(plt._pylab_helpers.Gcf.get_all_fig_managers())
        figures = [manager.canvas.figure for manager in managers]
        result = _STATE.original_show(*args, **kwargs)
        for fig in figures:
            _report_figure(fig)
        return result

    plt.show = wrapped_show



def _patch_notebook_figure_display() -> bool:
    """Wrap notebook figure MIME rendering so reports appear below displayed charts."""
    try:
        from matplotlib.figure import Figure
    except Exception:
        return False

    if _STATE.original_figure_repr_mimebundle is not None:
        return True

    original = getattr(Figure, "_repr_mimebundle_", None)
    if original is None:
        return False

    _STATE.original_figure_repr_mimebundle = original

    def wrapped_repr_mimebundle(self, *args, **kwargs):
        """Render the figure normally and then append the GoldenViz report."""
        bundle = _STATE.original_figure_repr_mimebundle(self, *args, **kwargs)
        _report_figure(self)
        return bundle

    Figure._repr_mimebundle_ = wrapped_repr_mimebundle
    return True



def auto() -> None:
    """Enable automatic report display for future Matplotlib figures."""
    if _STATE.enabled:
        return

    notebook_mode = is_notebook_environment() and _patch_notebook_figure_display()
    if not notebook_mode:
        _patch_matplotlib_show()
        _STATE.mode = "matplotlib_show"
    else:
        _STATE.mode = "jupyter_inline"

    _STATE.enabled = True



def disable() -> None:
    """Disable auto mode and restore original Matplotlib behavior."""
    if _STATE.original_show is not None:
        plt.show = _STATE.original_show
        _STATE.original_show = None

    try:
        from matplotlib.figure import Figure

        if _STATE.original_figure_repr_mimebundle is not None:
            Figure._repr_mimebundle_ = _STATE.original_figure_repr_mimebundle
    except Exception:
        pass

    _STATE.original_figure_repr_mimebundle = None
    _STATE.enabled = False
    _STATE.mode = None
    _STATE.reported_tokens.clear()



def is_auto_enabled() -> bool:
    """Return whether GoldenViz auto mode is currently active."""
    return _STATE.enabled
