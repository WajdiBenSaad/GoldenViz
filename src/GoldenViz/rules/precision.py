"""Rule implementation for excessive numeric precision checks."""

from __future__ import annotations

import re

from matplotlib.axes import Axes

from GoldenViz._results import RuleResult
from GoldenViz.rules.base import Rule

DECIMAL_PATTERN = re.compile(r"-?\d+\.(\d+)")


class PrecisionRule(Rule):
    """Warn when tick labels show unnecessary decimal precision."""

    rule_id = "R14"
    rule_name = "Decimal precision"

    def evaluate(self, ax: Axes) -> RuleResult:
        axis_title = (ax.get_title() or "").strip() or None
        labels = [tick.get_text() for tick in [*ax.get_xticklabels(), *ax.get_yticklabels()] if tick.get_text()]
        precise = [label for label in labels if any(len(match) > 2 for match in DECIMAL_PATTERN.findall(label))]

        if precise:
            return RuleResult(
                self.rule_id,
                self.rule_name,
                "WARNING",
                "Tick labels show high decimal precision.",
                "Round tick labels to the precision readers need for the decision at hand.",
                axis_title,
                {"precise_label_count": len(precise)},
            )

        return RuleResult(self.rule_id, self.rule_name, "PASS", "Tick precision appears readable.", axis_title, {"label_count": len(labels)})
