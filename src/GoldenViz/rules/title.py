"""Rule implementation for chart-title quality checks."""

from __future__ import annotations

from matplotlib.axes import Axes

from GoldenViz._results import RuleResult
from GoldenViz.rules.base import Rule

GENERIC_TITLES = {
    "chart",
    "data",
    "graph",
    "plot",
    "results",
    "summary",
}


class TitleRule(Rule):
    """Check that a chart has a non-empty and reasonably descriptive title."""

    rule_id = "R1"
    rule_name = "Clear title"

    def evaluate(self, ax: Axes) -> RuleResult:
        """Assess title presence and basic descriptiveness for one axis."""
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
        normalized = title.casefold().strip()
        if normalized in GENERIC_TITLES:
            return RuleResult(
                rule_id=self.rule_id,
                rule_name=self.rule_name,
                status="WARNING",
                message=f"Title '{title}' is present but generic.",
                suggestion="Use the title to name the metric, group, period, or main message.",
                axis_title=axis_title,
            )
        word_count = len([word for word in title.replace("-", " ").split() if word])
        if word_count < 3:
            return RuleResult(
                rule_id=self.rule_id,
                rule_name=self.rule_name,
                status="WARNING",
                message=f"Title '{title}' may not provide enough context.",
                suggestion="Add enough context for a reader to understand the chart outside the notebook.",
                axis_title=axis_title,
                details={"word_count": word_count},
            )
        return RuleResult(
            rule_id=self.rule_id,
            rule_name=self.rule_name,
            status="PASS",
            message=f"Title detected: '{title}'.",
            axis_title=axis_title,
        )
