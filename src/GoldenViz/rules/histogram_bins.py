"""Rule implementation for histogram bin-count checks."""

from __future__ import annotations

from matplotlib.axes import Axes

from GoldenViz._results import RuleResult
from GoldenViz._utils import axis_kind
from GoldenViz.rules.base import Rule


class HistogramBinsRule(Rule):
    """Warn when histogram bin counts look too coarse or too dense."""

    rule_id = "R23"
    rule_name = "Histogram bin quality"

    def evaluate(self, ax: Axes) -> RuleResult:
        axis_title = (ax.get_title() or "").strip() or None
        if axis_kind(ax) != "histogram":
            return RuleResult(self.rule_id, self.rule_name, "PASS", "No histogram bin issue detected.", axis_title, {"chart_type": axis_kind(ax)})

        bin_count = len(ax.patches)
        if bin_count < 5 or bin_count > 50:
            return RuleResult(
                self.rule_id,
                self.rule_name,
                "WARNING",
                f"Histogram uses {bin_count} bins.",
                "Choose a bin count that reveals distribution shape without hiding or exaggerating patterns.",
                axis_title,
                {"bin_count": bin_count},
            )

        return RuleResult(self.rule_id, self.rule_name, "PASS", "Histogram bin count appears reasonable.", axis_title, {"bin_count": bin_count})
