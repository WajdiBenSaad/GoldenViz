from __future__ import annotations

from GoldenViz._results import FigureReport
from GoldenViz._utils import is_notebook_environment
from GoldenViz.renderers import render_html_report, render_text_report


def display_report(report: FigureReport) -> FigureReport:
    if is_notebook_environment():
        try:
            from IPython.display import HTML, display

            display(HTML(render_html_report(report)))
            report.rendered_in_notebook = True
            return report
        except Exception:
            pass

    print(render_text_report(report))
    return report
