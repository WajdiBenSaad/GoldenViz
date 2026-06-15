"""Rule implementation for figure aspect-ratio checks."""

from __future__ import annotations

from matplotlib.axes import Axes

from GoldenViz._results import RuleResult
from GoldenViz.rules.base import Rule


class AspectRatioRule(Rule):
    """Warn about extreme figure aspect ratios."""

    rule_id = "R22"
    rule_name = "Aspect ratio sanity"

    def evaluate(self, ax: Axes) -> RuleResult:
        axis_title = (ax.get_title() or "").strip() or None
        width, height = ax.figure.get_size_inches()
        ratio = width / height if height else 0

        if ratio > 3.0 or ratio < 0.33:
            return RuleResult(
                self.rule_id,
                self.rule_name,
                "WARNING",
                f"Figure aspect ratio is extreme ({ratio:.2f}).",
                "Use an aspect ratio that preserves visual comparisons and leaves room for labels.",
                axis_title,
                {"aspect_ratio": ratio},
            )

        return RuleResult(self.rule_id, self.rule_name, "PASS", "Figure aspect ratio appears reasonable.", axis_title, {"aspect_ratio": ratio})
