"""Rule implementation for scatter overplotting checks."""

from __future__ import annotations

from matplotlib.axes import Axes

from GoldenViz._results import RuleResult
from GoldenViz._utils import axis_kind
from GoldenViz.rules.base import Rule


class OverplottingRule(Rule):
    """Warn when scatter plots may suffer from overplotting."""

    rule_id = "R13"
    rule_name = "Scatter overplotting"

    def evaluate(self, ax: Axes) -> RuleResult:
        axis_title = (ax.get_title() or "").strip() or None
        if axis_kind(ax) != "scatter":
            return RuleResult(self.rule_id, self.rule_name, "PASS", "No scatter overplotting issue detected.", axis_title, {"chart_type": axis_kind(ax)})

        point_count = 0
        duplicate_count = 0
        for collection in ax.collections:
            offsets = collection.get_offsets()
            point_count += len(offsets)
            rounded = [tuple(round(float(value), 3) for value in pair) for pair in offsets]
            duplicate_count += len(rounded) - len(set(rounded))

        if point_count > 500 or duplicate_count > 0:
            return RuleResult(
                self.rule_id,
                self.rule_name,
                "WARNING",
                "Scatter plot may have overplotting.",
                "Use transparency, smaller markers, jitter, hexbin, or aggregation when many points overlap.",
                axis_title,
                {"point_count": point_count, "duplicate_count": duplicate_count},
            )

        return RuleResult(self.rule_id, self.rule_name, "PASS", "No obvious scatter overplotting detected.", axis_title, {"point_count": point_count})
