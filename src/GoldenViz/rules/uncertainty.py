"""Rule implementation for uncertainty-cue checks."""

from __future__ import annotations

from matplotlib.axes import Axes
from matplotlib.collections import LineCollection, PolyCollection

from GoldenViz._results import RuleResult
from GoldenViz._utils import axis_kind
from GoldenViz.rules.base import Rule


class UncertaintyRule(Rule):
    """Suggest uncertainty cues for multi-point trends and comparisons."""

    rule_id = "R6"
    rule_name = "Uncertainty cues"

    def evaluate(self, ax: Axes) -> RuleResult:
        axis_title = (ax.get_title() or "").strip() or None
        kind = axis_kind(ax)
        has_uncertainty = any(isinstance(collection, (LineCollection, PolyCollection)) for collection in ax.collections)
        point_count = sum(len(line.get_ydata()) for line in ax.lines)

        if kind in {"line", "scatter"} and point_count >= 5 and not has_uncertainty:
            return RuleResult(
                self.rule_id,
                self.rule_name,
                "INFO",
                "No uncertainty cue detected for a multi-point chart.",
                "When values are estimates or samples, consider confidence intervals, bands, or error bars.",
                axis_title,
                {"chart_type": kind, "point_count": point_count, "has_uncertainty": has_uncertainty},
            )

        return RuleResult(self.rule_id, self.rule_name, "PASS", "No uncertainty cue issue detected.", axis_title, {"chart_type": kind, "has_uncertainty": has_uncertainty})
