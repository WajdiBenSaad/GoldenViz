"""Rule implementation for simple color accessibility checks."""

from __future__ import annotations

from itertools import combinations

from matplotlib.axes import Axes
from matplotlib.colors import to_rgb

from GoldenViz._results import RuleResult
from GoldenViz.rules.base import Rule


def _rgb_distance(left, right) -> float:
    return sum((a - b) ** 2 for a, b in zip(left, right)) ** 0.5


def _collect_mark_colors(ax: Axes):
    colors = []
    for line in ax.lines:
        colors.append(line.get_color())
    for patch in ax.patches:
        colors.append(patch.get_facecolor())
    for collection in ax.collections:
        facecolors = collection.get_facecolors()
        if len(facecolors):
            colors.extend(facecolors)
    converted = []
    for color in colors:
        try:
            converted.append(tuple(round(value, 3) for value in to_rgb(color)))
        except ValueError:
            continue
    return sorted(set(converted))


class ColorAccessibilityRule(Rule):
    """Warn about color sets that may be difficult to distinguish."""

    rule_id = "R8"
    rule_name = "Color accessibility"

    def evaluate(self, ax: Axes) -> RuleResult:
        """Assess simple categorical color distinctness."""
        axis_title = (ax.get_title() or "").strip() or None
        colors = _collect_mark_colors(ax)

        if len(colors) > 8:
            return RuleResult(
                rule_id=self.rule_id,
                rule_name=self.rule_name,
                status="WARNING",
                message=f"The chart uses many distinct colors ({len(colors)}).",
                suggestion="Limit categorical colors or group minor categories so differences remain easy to see.",
                axis_title=axis_title,
                details={"color_count": len(colors)},
            )

        close_pairs = [
            (left, right)
            for left, right in combinations(colors, 2)
            if _rgb_distance(left, right) < 0.18
        ]
        if close_pairs:
            return RuleResult(
                rule_id=self.rule_id,
                rule_name=self.rule_name,
                status="WARNING",
                message="Some chart colors may be hard to distinguish.",
                suggestion="Use a more separated palette and avoid relying on color alone to encode meaning.",
                axis_title=axis_title,
                details={"color_count": len(colors), "close_pair_count": len(close_pairs)},
            )

        return RuleResult(
            rule_id=self.rule_id,
            rule_name=self.rule_name,
            status="PASS",
            message="No obvious color accessibility issue detected.",
            axis_title=axis_title,
            details={"color_count": len(colors)},
        )
