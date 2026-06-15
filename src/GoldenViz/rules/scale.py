"""Rule implementation for scale-related chart checks."""

from __future__ import annotations

from matplotlib.axes import Axes

from GoldenViz._results import RuleResult
from GoldenViz._utils import axis_kind, bar_orientation
from GoldenViz.rules.base import Rule


class ScaleRule(Rule):
    """Detect obvious scale issues such as truncated bar-chart baselines."""

    rule_id = "R17"
    rule_name = "Appropriate scale"

    def evaluate(self, ax: Axes) -> RuleResult:
        """Assess whether the axis scale appears misleading or invalid."""
        axis_title = (ax.get_title() or "").strip() or None
        kind = axis_kind(ax)
        ymin, ymax = ax.get_ylim()
        xmin, xmax = ax.get_xlim()

        if ymax <= ymin or xmax <= xmin:
            return RuleResult(
                rule_id=self.rule_id,
                rule_name=self.rule_name,
                status="FAIL",
                message="Axis scale appears invalid because an upper bound is not greater than its lower bound.",
                suggestion="Check axis limits and data values.",
                axis_title=axis_title,
                details={"xmin": xmin, "xmax": xmax, "ymin": ymin, "ymax": ymax},
            )

        if kind == "bar" and bar_orientation(ax) == "vertical" and ymin > 0:
            return RuleResult(
                rule_id=self.rule_id,
                rule_name=self.rule_name,
                status="FAIL",
                message=f"Bar chart y-axis starts at {ymin:.2f} instead of zero.",
                suggestion="Start bar charts at zero unless you clearly justify a truncated scale.",
                axis_title=axis_title,
                details={"ymin": ymin, "ymax": ymax, "chart_type": kind, "orientation": "vertical"},
            )

        if kind == "bar" and bar_orientation(ax) == "horizontal" and xmin > 0:
            return RuleResult(
                rule_id=self.rule_id,
                rule_name=self.rule_name,
                status="FAIL",
                message=f"Horizontal bar chart x-axis starts at {xmin:.2f} instead of zero.",
                suggestion="Start bar charts at zero unless you clearly justify a truncated scale.",
                axis_title=axis_title,
                details={"xmin": xmin, "xmax": xmax, "chart_type": kind, "orientation": "horizontal"},
            )

        if ax.get_yscale() == "log" or ax.get_xscale() == "log":
            return RuleResult(
                rule_id=self.rule_id,
                rule_name=self.rule_name,
                status="WARNING",
                message="Logarithmic axis scale detected.",
                suggestion="Ensure the title or axis label makes the log scale explicit.",
                axis_title=axis_title,
                details={"xscale": ax.get_xscale(), "yscale": ax.get_yscale()},
            )

        return RuleResult(
            rule_id=self.rule_id,
            rule_name=self.rule_name,
            status="PASS",
            message="No obvious scale issue detected.",
            axis_title=axis_title,
            details={"xmin": xmin, "xmax": xmax, "ymin": ymin, "ymax": ymax, "chart_type": kind},
        )
