"""Rule implementation for visual clutter and chartjunk checks."""

from __future__ import annotations

from matplotlib.axes import Axes

from GoldenViz._results import RuleResult
from GoldenViz.rules.base import Rule


class ChartjunkRule(Rule):
    """Warn about obvious non-data visual clutter."""

    rule_id = "R10"
    rule_name = "Avoid chartjunk"

    def evaluate(self, ax: Axes) -> RuleResult:
        axis_title = (ax.get_title() or "").strip() or None
        visible_spines = sum(spine.get_visible() for spine in ax.spines.values())
        x_grid = any(line.get_visible() for line in ax.get_xgridlines())
        y_grid = any(line.get_visible() for line in ax.get_ygridlines())

        if getattr(ax, "name", "") == "3d":
            return RuleResult(self.rule_id, self.rule_name, "WARNING", "3D axis detected.", "Use 3D charts only when the third dimension is necessary.", axis_title, {"axis_name": ax.name})

        if visible_spines == 4 and x_grid and y_grid:
            return RuleResult(
                self.rule_id,
                self.rule_name,
                "WARNING",
                "Heavy frame and two-direction gridlines detected.",
                "Reduce non-data ink by lightening the frame or using only the gridlines needed for reading values.",
                axis_title,
                {"visible_spines": visible_spines, "x_grid": x_grid, "y_grid": y_grid},
            )

        return RuleResult(self.rule_id, self.rule_name, "PASS", "No obvious chartjunk issue detected.", axis_title, {"visible_spines": visible_spines})
