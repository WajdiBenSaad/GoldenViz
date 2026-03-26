from __future__ import annotations

from matplotlib.axes import Axes

from GoldenViz._results import RuleResult
from GoldenViz.rules.base import Rule


class TitleRule(Rule):
    rule_id = "R1"
    rule_name = "Clear title"

    def evaluate(self, ax: Axes) -> RuleResult:
        title = (ax.get_title() or "").strip()
        axis_title = title or None
        if not title:
            return RuleResult(
                rule_id=self.rule_id,
                rule_name=self.rule_name,
                status="FAIL",
                message="Missing chart title.",
                suggestion="Add a descriptive title that states what the chart shows.",
                axis_title=axis_title,
            )
        if len(title) < 8:
            return RuleResult(
                rule_id=self.rule_id,
                rule_name=self.rule_name,
                status="WARNING",
                message=f"Title '{title}' is present but may be too short to be descriptive.",
                suggestion="Make the title slightly more explicit so readers understand the message immediately.",
                axis_title=axis_title,
            )
        return RuleResult(
            rule_id=self.rule_id,
            rule_name=self.rule_name,
            status="PASS",
            message=f"Title detected: '{title}'.",
            axis_title=axis_title,
        )
