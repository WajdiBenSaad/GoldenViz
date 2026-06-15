"""Rule implementation for date-axis formatting checks."""

from __future__ import annotations

import re

from matplotlib.axes import Axes

from GoldenViz._results import RuleResult
from GoldenViz.rules.base import Rule

DATE_PATTERN = re.compile(r"\d{4}[-/]\d{1,2}[-/]\d{1,2}")


class DateAxisRule(Rule):
    """Warn when date-like tick labels are dense or verbose."""

    rule_id = "R15"
    rule_name = "Date axis formatting"

    def evaluate(self, ax: Axes) -> RuleResult:
        axis_title = (ax.get_title() or "").strip() or None
        labels = [tick.get_text() for tick in ax.get_xticklabels() if tick.get_text()]
        date_labels = [label for label in labels if DATE_PATTERN.search(label)]

        if len(date_labels) > 6:
            return RuleResult(
                self.rule_id,
                self.rule_name,
                "WARNING",
                "Date axis uses many verbose date labels.",
                "Use fewer ticks or shorter date formats so the time axis remains readable.",
                axis_title,
                {"date_label_count": len(date_labels)},
            )

        return RuleResult(self.rule_id, self.rule_name, "PASS", "No obvious date-axis formatting issue detected.", axis_title, {"date_label_count": len(date_labels)})
