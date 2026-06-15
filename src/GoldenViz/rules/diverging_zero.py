"""Rule implementation for diverging-data zero-reference checks."""

from __future__ import annotations

from matplotlib.axes import Axes

from GoldenViz._results import RuleResult
from GoldenViz.rules.base import Rule


def _y_values(ax: Axes):
    values = []
    for line in ax.lines:
        values.extend(float(value) for value in line.get_ydata())
    for patch in ax.patches:
        if hasattr(patch, "get_height"):
            values.append(float(patch.get_height()))
    return values


class DivergingZeroRule(Rule):
    """Warn when positive and negative values lack a visible zero reference."""

    rule_id = "R25"
    rule_name = "Diverging zero reference"

    def evaluate(self, ax: Axes) -> RuleResult:
        axis_title = (ax.get_title() or "").strip() or None
        values = _y_values(ax)
        has_diverging_values = any(value < 0 for value in values) and any(value > 0 for value in values)
        has_zero_line = any(len(line.get_ydata()) >= 2 and all(abs(float(value)) < 1e-9 for value in line.get_ydata()) for line in ax.lines)

        if has_diverging_values and not has_zero_line:
            return RuleResult(
                self.rule_id,
                self.rule_name,
                "WARNING",
                "Chart contains positive and negative values without an explicit zero reference line.",
                "Add a visible zero line so readers can separate gains from losses.",
                axis_title,
                {"value_count": len(values), "has_zero_line": has_zero_line},
            )

        return RuleResult(self.rule_id, self.rule_name, "PASS", "No diverging zero-reference issue detected.", axis_title, {"has_diverging_values": has_diverging_values})
