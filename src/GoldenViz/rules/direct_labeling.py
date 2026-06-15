"""Rule implementation for direct-labeling opportunities."""

from __future__ import annotations

from matplotlib.axes import Axes

from GoldenViz._results import RuleResult
from GoldenViz.rules.base import Rule


class DirectLabelingRule(Rule):
    """Suggest direct labels when a small line chart uses a legend."""

    rule_id = "R9"
    rule_name = "Direct labeling"

    def evaluate(self, ax: Axes) -> RuleResult:
        """Assess whether direct labels would reduce legend lookup."""
        axis_title = (ax.get_title() or "").strip() or None
        visible_lines = [line for line in ax.lines if line.get_visible()]
        legend = ax.get_legend()

        if legend is not None and 2 <= len(visible_lines) <= 4:
            return RuleResult(
                rule_id=self.rule_id,
                rule_name=self.rule_name,
                status="WARNING",
                message="Small multi-line chart uses a legend.",
                suggestion="Consider labeling lines near their endpoints to reduce back-and-forth legend lookup.",
                axis_title=axis_title,
                details={"line_count": len(visible_lines), "has_legend": True},
            )

        return RuleResult(
            rule_id=self.rule_id,
            rule_name=self.rule_name,
            status="PASS",
            message="No direct-labeling opportunity detected.",
            axis_title=axis_title,
            details={"line_count": len(visible_lines), "has_legend": legend is not None},
        )
