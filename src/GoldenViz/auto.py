from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, List, Optional

import matplotlib.pyplot as plt

from GoldenViz.analyzer import analyze
from GoldenViz.display import display_report
from GoldenViz._utils import is_notebook_environment


@dataclass
class _AutoState:
    enabled: bool = False
    mode: Optional[str] = None
    original_show: Optional[Callable] = None
    original_figure_repr_mimebundle: Optional[Callable] = None
    reported_tokens: set = field(default_factory=set)


_STATE = _AutoState()


def _figure_token(fig) -> int:
    return id(fig)


def _report_figure(fig) -> None:
    if fig is None or not getattr(fig, "axes", None):
        return
    token = _figure_token(fig)
    if token in _STATE.reported_tokens:
        return
    _STATE.reported_tokens.add(token)
    display_report(analyze(fig))


def _patch_matplotlib_show() -> None:
    if _STATE.original_show is not None:
        return
    _STATE.original_show = plt.show

    def wrapped_show(*args, **kwargs):
        managers = list(plt._pylab_helpers.Gcf.get_all_fig_managers())
        figures = [manager.canvas.figure for manager in managers]
        result = _STATE.original_show(*args, **kwargs)
        for fig in figures:
            _report_figure(fig)
        return result

    plt.show = wrapped_show


def _patch_notebook_figure_display() -> bool:
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
        bundle = _STATE.original_figure_repr_mimebundle(self, *args, **kwargs)
        _report_figure(self)
        return bundle

    Figure._repr_mimebundle_ = wrapped_repr_mimebundle
    return True


def auto() -> None:
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
    return _STATE.enabled
