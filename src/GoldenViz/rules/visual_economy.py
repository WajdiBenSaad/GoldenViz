"""Rule implementation for visual economy checks."""

from __future__ import annotations

from matplotlib.axes import Axes

from GoldenViz._results import RuleResult
from GoldenViz.rules.base import Rule


class VisualEconomyRule(Rule):
    """Warn when a chart contains many visible graphical elements."""

    rule_id = "R16"
    rule_name = "Visual economy"

    def evaluate(self, ax: Axes) -> RuleResult:
        axis_title = (ax.get_title() or "").strip() or None
        element_count = len(ax.lines) + len(ax.patches) + len(ax.collections) + len(ax.texts)

        if element_count > 80:
            return RuleResult(
                self.rule_id,
                self.rule_name,
                "WARNING",
                f"Chart contains many visible elements ({element_count}).",
                "Simplify, aggregate, facet, or filter the chart so the main comparison is clear.",
                axis_title,
                {"element_count": element_count},
            )

        return RuleResult(self.rule_id, self.rule_name, "PASS", "Chart appears visually economical.", axis_title, {"element_count": element_count})
