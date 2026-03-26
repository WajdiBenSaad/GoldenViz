"""Rule implementation for axis-label checks."""

from __future__ import annotations

from matplotlib.axes import Axes

from GoldenViz._results import RuleResult
from GoldenViz._utils import stringify_label
from GoldenViz.rules.base import Rule


class AxisLabelsRule(Rule):
    """Check whether both x-axis and y-axis labels are present and usable."""

    rule_id = "R2"
    rule_name = "Axis labels"

    def evaluate(self, ax: Axes) -> RuleResult:
        """Assess label presence and detect labels that are probably too short."""
        axis_title = (ax.get_title() or "").strip() or None
        xlabel = stringify_label(ax.get_xlabel())
        ylabel = stringify_label(ax.get_ylabel())

        missing = []
        if not xlabel:
            missing.append("x-axis")
        if not ylabel:
            missing.append("y-axis")

        if missing:
            return RuleResult(
                rule_id=self.rule_id,
                rule_name=self.rule_name,
                status="FAIL",
                message=f"Missing label(s): {', '.join(missing)}.",
                suggestion="Add labels for both axes, and include units when relevant.",
                axis_title=axis_title,
                details={"xlabel": xlabel, "ylabel": ylabel},
            )

        too_short = [name for name, value in {"x-axis": xlabel, "y-axis": ylabel}.items() if len(value) < 2]
        if too_short:
            return RuleResult(
                rule_id=self.rule_id,
                rule_name=self.rule_name,
                status="WARNING",
                message=f"Axis labels exist but may be too short: {', '.join(too_short)}.",
                suggestion="Use labels that are explicit enough for a reader who has not seen the dataset.",
                axis_title=axis_title,
                details={"xlabel": xlabel, "ylabel": ylabel},
            )

        return RuleResult(
            rule_id=self.rule_id,
            rule_name=self.rule_name,
            status="PASS",
            message="Both x-axis and y-axis labels are present.",
            axis_title=axis_title,
            details={"xlabel": xlabel, "ylabel": ylabel},
        )
