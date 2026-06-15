"""Rule implementation for chart-type consistency checks."""

from __future__ import annotations

from matplotlib.axes import Axes

from GoldenViz._results import RuleResult
from GoldenViz._utils import axis_kind
from GoldenViz.rules.base import Rule


def _is_numeric_like(value) -> bool:
    """Return whether a value can reasonably be interpreted as numeric."""
    try:
        float(value)
        return True
    except (TypeError, ValueError):
        return False


class ChartTypeRule(Rule):
    """Perform light heuristics to flag questionable chart-type choices."""

    rule_id = "R18"
    rule_name = "Chart type"

    def evaluate(self, ax: Axes) -> RuleResult:
        """Classify the chart and warn about obvious category-versus-line mismatches."""
        axis_title = (ax.get_title() or "").strip() or None
        kind = axis_kind(ax)

        if kind == "line":
            x_values = []
            for line in ax.lines:
                try:
                    x_values.extend(line.get_xdata(orig=True))
                except TypeError:
                    x_values.extend(line.get_xdata())
            labels = [tick.get_text() for tick in ax.get_xticklabels() if tick.get_text()]
            categorical_data = bool(x_values) and not all(_is_numeric_like(value) for value in x_values)
            categorical_labels = len(labels) > 0 and not all(_is_numeric_like(label) for label in labels)
            categorical_like = categorical_data or categorical_labels
            if categorical_like:
                return RuleResult(
                    rule_id=self.rule_id,
                    rule_name=self.rule_name,
                    status="WARNING",
                    message="Line chart uses categorical-looking x-axis labels.",
                    suggestion="Consider a bar chart if the x-axis represents discrete categories rather than a trend.",
                    axis_title=axis_title,
                    details={"chart_type": kind, "categorical_x": True},
                )

        if kind == "pie":
            return RuleResult(
                rule_id=self.rule_id,
                rule_name=self.rule_name,
                status="WARNING",
                message="Pie chart detected.",
                suggestion="Use pie charts carefully; compare categories with a bar chart when precise differences matter.",
                axis_title=axis_title,
                details={"chart_type": kind},
            )

        if kind == "other":
            return RuleResult(
                rule_id=self.rule_id,
                rule_name=self.rule_name,
                status="WARNING",
                message="GoldenViz could not confidently classify this chart type.",
                suggestion="Review whether the chosen chart type matches the structure of the data.",
                axis_title=axis_title,
                details={"chart_type": kind},
            )

        return RuleResult(
            rule_id=self.rule_id,
            rule_name=self.rule_name,
            status="PASS",
            message=f"Detected chart type: {kind}.",
            axis_title=axis_title,
            details={"chart_type": kind},
        )
