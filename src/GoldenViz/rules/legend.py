"""Rule implementation for legend clarity checks."""

from __future__ import annotations

from matplotlib.axes import Axes

from GoldenViz._results import RuleResult
from GoldenViz.rules.base import Rule

GENERIC_LEGEND_LABELS = {"a", "b", "c", "data", "line", "series", "value", "values"}


def _series_count(ax: Axes) -> int:
    count = sum(1 for line in ax.lines if line.get_visible())
    count += sum(1 for container in ax.containers if getattr(container, "patches", None))
    count += sum(1 for collection in ax.collections if collection.get_visible())
    return count


class LegendRule(Rule):
    """Check whether multi-series charts have useful legends."""

    rule_id = "R4"
    rule_name = "Legend clarity"

    def evaluate(self, ax: Axes) -> RuleResult:
        """Assess legend presence and label quality."""
        axis_title = (ax.get_title() or "").strip() or None
        series_count = _series_count(ax)
        legend = ax.get_legend()

        if series_count > 1 and legend is None:
            return RuleResult(
                rule_id=self.rule_id,
                rule_name=self.rule_name,
                status="WARNING",
                message="Multiple visible series detected without a legend.",
                suggestion="Add a legend or direct labels so readers can identify each series.",
                axis_title=axis_title,
                details={"series_count": series_count},
            )

        if legend is not None:
            labels = [text.get_text().strip() for text in legend.get_texts()]
            weak = [label for label in labels if not label or label.startswith("_") or label.casefold() in GENERIC_LEGEND_LABELS]
            if weak:
                return RuleResult(
                    rule_id=self.rule_id,
                    rule_name=self.rule_name,
                    status="WARNING",
                    message="Legend labels may be too generic.",
                    suggestion="Use legend labels that describe the group, scenario, or metric.",
                    axis_title=axis_title,
                    details={"labels": labels, "weak_labels": weak},
                )

        return RuleResult(
            rule_id=self.rule_id,
            rule_name=self.rule_name,
            status="PASS",
            message="No obvious legend clarity issue detected.",
            axis_title=axis_title,
            details={"series_count": series_count, "has_legend": legend is not None},
        )
