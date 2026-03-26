from __future__ import annotations

from matplotlib.axes import Axes

from GoldenViz._results import RuleResult
from GoldenViz._utils import axis_kind
from GoldenViz.rules.base import Rule


class ScaleRule(Rule):
    rule_id = "R3"
    rule_name = "Appropriate scale"

    def evaluate(self, ax: Axes) -> RuleResult:
        axis_title = (ax.get_title() or "").strip() or None
        kind = axis_kind(ax)
        ymin, ymax = ax.get_ylim()

        if kind == "bar" and ymin > 0:
            return RuleResult(
                rule_id=self.rule_id,
                rule_name=self.rule_name,
                status="FAIL",
                message=f"Bar chart y-axis starts at {ymin:.2f} instead of zero.",
                suggestion="Start bar charts at zero unless you clearly justify a truncated scale.",
                axis_title=axis_title,
                details={"ymin": ymin, "ymax": ymax, "chart_type": kind},
            )

        if ymax <= ymin:
            return RuleResult(
                rule_id=self.rule_id,
                rule_name=self.rule_name,
                status="FAIL",
                message="Axis scale appears invalid because the upper bound is not greater than the lower bound.",
                suggestion="Check axis limits and data values.",
                axis_title=axis_title,
                details={"ymin": ymin, "ymax": ymax},
            )

        if ax.get_yscale() == "log":
            return RuleResult(
                rule_id=self.rule_id,
                rule_name=self.rule_name,
                status="WARNING",
                message="Logarithmic y-scale detected.",
                suggestion="Ensure the title or axis label makes the log scale explicit.",
                axis_title=axis_title,
                details={"yscale": "log"},
            )

        return RuleResult(
            rule_id=self.rule_id,
            rule_name=self.rule_name,
            status="PASS",
            message="No obvious scale issue detected.",
            axis_title=axis_title,
            details={"ymin": ymin, "ymax": ymax, "chart_type": kind},
        )
