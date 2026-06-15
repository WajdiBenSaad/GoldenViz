"""Rule implementation for annotation and context checks."""

from __future__ import annotations

from matplotlib.axes import Axes

from GoldenViz._results import RuleResult
from GoldenViz.rules.base import Rule


class AnnotationRule(Rule):
    """Suggest annotations for charts that contain several data marks."""

    rule_id = "R5"
    rule_name = "Annotation context"

    def evaluate(self, ax: Axes) -> RuleResult:
        axis_title = (ax.get_title() or "").strip() or None
        text_count = len([text for text in ax.texts if text.get_text().strip()])
        mark_count = len(ax.lines) + len(ax.patches) + len(ax.collections)

        if mark_count >= 6 and text_count == 0:
            return RuleResult(
                self.rule_id,
                self.rule_name,
                "WARNING",
                "Chart has several marks but no annotations.",
                "Add a short annotation for the key comparison, outlier, or takeaway when the chart is explanatory.",
                axis_title,
                {"mark_count": mark_count, "text_count": text_count},
            )

        return RuleResult(self.rule_id, self.rule_name, "PASS", "No obvious annotation context issue detected.", axis_title, {"mark_count": mark_count, "text_count": text_count})
