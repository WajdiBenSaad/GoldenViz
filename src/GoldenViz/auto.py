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
    original_inline_flush: Optional[Callable] = None
    wrapped_inline_flush: Optional[Callable] = None
    reported_tokens: set = field(default_factory=set)


_STATE = _AutoState()


def _figure_token(fig) -> tuple[int, int]:
    stale = int(getattr(fig, "stale", False))
    return (id(fig), len(fig.axes) + stale)



def _report_figures(figures: List[object]) -> None:
    for fig in figures:
        if fig is None:
            continue
        token = _figure_token(fig)
        if token in _STATE.reported_tokens:
            continue
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
        _report_figures(figures)
        return result

    plt.show = wrapped_show



def _patch_inline_backend() -> bool:
    try:
        from IPython import get_ipython
        import matplotlib_inline.backend_inline as backend_inline
    except Exception:
        return False

    if _STATE.original_inline_flush is not None:
        return True

    ip = get_ipython()
    if ip is None or not hasattr(ip, "events"):
        return False

    _STATE.original_inline_flush = backend_inline.flush_figures

    def wrapped_flush_figures(*args, **kwargs):
        show_fn = backend_inline.show
        active = set(fm.canvas.figure for fm in plt._pylab_helpers.Gcf.get_all_fig_managers())
        to_draw = [fig for fig in getattr(show_fn, "_to_draw", []) if fig in active]
        result = _STATE.original_inline_flush(*args, **kwargs)
        if to_draw:
            _report_figures(to_draw)
        return result

    _STATE.wrapped_inline_flush = wrapped_flush_figures
    backend_inline.flush_figures = wrapped_flush_figures

    try:
        ip.events.unregister("post_execute", _STATE.original_inline_flush)
    except Exception:
        pass
    ip.events.register("post_execute", wrapped_flush_figures)
    return True



def auto() -> None:
    if _STATE.enabled:
        return

    notebook_mode = is_notebook_environment() and _patch_inline_backend()
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
        from IPython import get_ipython
        import matplotlib_inline.backend_inline as backend_inline

        if _STATE.original_inline_flush is not None:
            if _STATE.wrapped_inline_flush is not None:
                try:
                    ip = get_ipython()
                    if ip is not None and hasattr(ip, "events"):
                        ip.events.unregister("post_execute", _STATE.wrapped_inline_flush)
                        ip.events.register("post_execute", _STATE.original_inline_flush)
                except Exception:
                    pass
            backend_inline.flush_figures = _STATE.original_inline_flush
    except Exception:
        pass

    _STATE.original_inline_flush = None
    _STATE.wrapped_inline_flush = None
    _STATE.enabled = False
    _STATE.mode = None
    _STATE.reported_tokens.clear()



def is_auto_enabled() -> bool:
    return _STATE.enabled
