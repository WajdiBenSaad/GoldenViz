"""Rule implementation for category-color consistency checks."""

from __future__ import annotations

from matplotlib.axes import Axes

from GoldenViz._results import RuleResult
from GoldenViz._utils import axis_kind
from GoldenViz.rules.base import Rule


class CategoryColorRule(Rule):
    """Warn when categories are not encoded with distinct colors."""

    rule_id = "R24"
    rule_name = "Category color consistency"

    def evaluate(self, ax: Axes) -> RuleResult:
        axis_title = (ax.get_title() or "").strip() or None
        if axis_kind(ax) != "bar" or len(ax.patches) < 3:
            return RuleResult(self.rule_id, self.rule_name, "PASS", "No category color issue detected.", axis_title, {"chart_type": axis_kind(ax)})

        colors = [tuple(round(value, 3) for value in patch.get_facecolor()[:3]) for patch in ax.patches]
        unique_colors = set(colors)
        if 1 < len(unique_colors) < len(colors):
            return RuleResult(
                self.rule_id,
                self.rule_name,
                "WARNING",
                "Some categories share colors while others use distinct colors.",
                "Use color consistently: either one neutral color for all bars or a clear mapping for meaningful groups.",
                axis_title,
                {"bar_count": len(colors), "color_count": len(unique_colors)},
            )

        return RuleResult(self.rule_id, self.rule_name, "PASS", "Category colors appear consistent.", axis_title, {"bar_count": len(colors), "color_count": len(unique_colors)})
