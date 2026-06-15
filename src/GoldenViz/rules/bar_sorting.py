"""Rule implementation for categorical bar sorting."""

from __future__ import annotations

from matplotlib.axes import Axes

from GoldenViz._results import RuleResult
from GoldenViz._utils import axis_kind, bar_orientation
from GoldenViz.rules.base import Rule


def _is_monotonic(values) -> bool:
    return all(left <= right for left, right in zip(values, values[1:])) or all(left >= right for left, right in zip(values, values[1:]))


class BarSortingRule(Rule):
    """Warn when categorical bars are not sorted by value."""

    rule_id = "R12"
    rule_name = "Sort categorical bars"

    def evaluate(self, ax: Axes) -> RuleResult:
        axis_title = (ax.get_title() or "").strip() or None
        if axis_kind(ax) != "bar":
            return RuleResult(self.rule_id, self.rule_name, "PASS", "No categorical bar sorting issue detected.", axis_title, {"chart_type": axis_kind(ax)})

        patches = [patch for patch in ax.patches if hasattr(patch, "get_width") and hasattr(patch, "get_height")]
        if len(patches) < 4:
            return RuleResult(self.rule_id, self.rule_name, "PASS", "Too few bars for sorting guidance.", axis_title, {"bar_count": len(patches)})

        orientation = bar_orientation(ax)
        values = [patch.get_width() if orientation == "horizontal" else patch.get_height() for patch in patches]
        if not _is_monotonic(values):
            return RuleResult(
                self.rule_id,
                self.rule_name,
                "WARNING",
                "Categorical bars are not sorted by value.",
                "Sort bars by value unless the category order has a natural meaning.",
                axis_title,
                {"bar_count": len(patches), "orientation": orientation},
            )

        return RuleResult(self.rule_id, self.rule_name, "PASS", "Categorical bars appear sorted or ordered.", axis_title, {"bar_count": len(patches)})
