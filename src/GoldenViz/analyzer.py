from __future__ import annotations

from typing import Iterable, Optional

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



def analyze(fig=None) -> FigureReport:
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



def check(fig=None, *, display: bool = True) -> FigureReport:
    report = analyze(fig)
    if display:
        return display_report(report)
    return report



def check_current(*, display: bool = True) -> FigureReport:
    return check(plt.gcf(), display=display)
