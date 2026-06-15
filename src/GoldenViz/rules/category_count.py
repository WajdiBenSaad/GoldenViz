"""Rule implementation for excessive category counts."""

from __future__ import annotations

from matplotlib.axes import Axes

from GoldenViz._results import RuleResult
from GoldenViz._utils import axis_kind
from GoldenViz.rules.base import Rule


class CategoryCountRule(Rule):
    """Warn when categorical charts contain too many categories."""

    rule_id = "R11"
    rule_name = "Too many categories"

    def evaluate(self, ax: Axes) -> RuleResult:
        axis_title = (ax.get_title() or "").strip() or None
        kind = axis_kind(ax)
        labels = [tick.get_text() for tick in ax.get_xticklabels() if tick.get_text()]
        category_count = len(labels)

        if kind == "bar" and category_count > 12:
            return RuleResult(
                self.rule_id,
                self.rule_name,
                "WARNING",
                f"Bar chart shows many categories ({category_count}).",
                "Consider grouping small categories, showing a top-N view, or switching to a table.",
                axis_title,
                {"category_count": category_count},
            )

        return RuleResult(self.rule_id, self.rule_name, "PASS", "Category count appears manageable.", axis_title, {"category_count": category_count})
