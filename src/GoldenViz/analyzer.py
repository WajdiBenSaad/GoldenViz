"""Core analysis entry points for GoldenViz."""

from __future__ import annotations

import matplotlib.pyplot as plt

from GoldenViz._results import AxisReport, FigureReport
from GoldenViz._utils import ensure_canvas_drawn, visible_axes
from GoldenViz.display import display_report
from GoldenViz.rules import AxisLabelsRule, ChartTypeRule, ReadabilityRule, ScaleRule, TitleRule

DEFAULT_RULES = [
    TitleRule(),
    AxisLabelsRule(),
    ScaleRule(),
    ChartTypeRule(),
    ReadabilityRule(),
]
"""Default rule set applied to every visible axis."""



def analyze(fig=None) -> FigureReport:
    """Analyze a Matplotlib figure and return a structured report.

    Args:
        fig: Target figure. When omitted, the current active Matplotlib figure is used.

    Returns:
        A :class:`FigureReport` containing one :class:`AxisReport` per visible axis.
    """
    if fig is None:
        fig = plt.gcf()
    ensure_canvas_drawn(fig)
    axes_reports = []
    for index, ax in enumerate(visible_axes(fig)):
        results = [rule.evaluate(ax) for rule in DEFAULT_RULES]
        axes_reports.append(
            AxisReport(
                axis_index=index,
                axis_title=(ax.get_title() or "").strip() or None,
                rule_results=results,
            )
        )
    return FigureReport(figure_number=getattr(fig, "number", None), axes_reports=axes_reports)



def check(fig=None, *, display: bool = True):
    """Analyze a figure and optionally render the report immediately.

    Args:
        fig: Target figure. Defaults to the current active figure.
        display: Whether to render the report immediately. When ``False``, the
            structured report is returned for programmatic use.

    Returns:
        ``None`` when ``display`` is ``True``. Otherwise returns a
        :class:`FigureReport`.
    """
    report = analyze(fig)
    if display:
        display_report(report)
        return None
    return report



def check_current(*, display: bool = True):
    """Shortcut for checking the current active Matplotlib figure."""
    return check(plt.gcf(), display=display)
