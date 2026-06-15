"""Rule implementation for dual-axis detection."""

from __future__ import annotations

from matplotlib.axes import Axes

from GoldenViz._results import RuleResult
from GoldenViz.rules.base import Rule


class DualAxisRule(Rule):
    """Warn when an axis appears to share space with another axis."""

    rule_id = "R20"
    rule_name = "Avoid dual axes"

    def evaluate(self, ax: Axes) -> RuleResult:
        axis_title = (ax.get_title() or "").strip() or None
        position = ax.get_position().bounds
        overlapping = [
            other
            for other in ax.figure.axes
            if other is not ax and other.get_visible() and tuple(round(v, 4) for v in other.get_position().bounds) == tuple(round(v, 4) for v in position)
        ]

        if overlapping:
            return RuleResult(
                self.rule_id,
                self.rule_name,
                "WARNING",
                "Overlapping axes detected, possibly from a dual-axis chart.",
                "Avoid dual axes when possible; use small multiples or normalize values for fair comparison.",
                axis_title,
                {"overlapping_axes": len(overlapping)},
            )

        return RuleResult(self.rule_id, self.rule_name, "PASS", "No dual-axis layout detected.", axis_title, {"overlapping_axes": 0})
