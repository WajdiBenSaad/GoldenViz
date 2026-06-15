"""Rule implementation for area-chart baseline checks."""

from __future__ import annotations

from matplotlib.axes import Axes
from matplotlib.collections import PolyCollection

from GoldenViz._results import RuleResult
from GoldenViz.rules.base import Rule


class AreaBaselineRule(Rule):
    """Warn when area-like charts use a truncated baseline."""

    rule_id = "R21"
    rule_name = "Area baseline"

    def evaluate(self, ax: Axes) -> RuleResult:
        axis_title = (ax.get_title() or "").strip() or None
        has_area = any(isinstance(collection, PolyCollection) for collection in ax.collections)
        ymin, ymax = ax.get_ylim()

        if has_area and ymin > 0:
            return RuleResult(
                self.rule_id,
                self.rule_name,
                "WARNING",
                f"Area-like chart y-axis starts at {ymin:.2f} instead of zero.",
                "Area encodings usually need a zero baseline because filled area implies magnitude.",
                axis_title,
                {"ymin": ymin, "ymax": ymax},
            )

        return RuleResult(self.rule_id, self.rule_name, "PASS", "No area baseline issue detected.", axis_title, {"has_area": has_area})
