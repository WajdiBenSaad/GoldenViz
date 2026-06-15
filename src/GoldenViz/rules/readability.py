"""Rule implementation for readability checks."""

from __future__ import annotations

from matplotlib.axes import Axes

from GoldenViz._results import RuleResult
from GoldenViz._utils import ensure_canvas_drawn
from GoldenViz.rules.base import Rule


class ReadabilityRule(Rule):
    """Detect crowded, overlapping, or tiny tick labels."""

    rule_id = "R7"
    rule_name = "Readable labels and ticks"

    def evaluate(self, ax: Axes) -> RuleResult:
        """Assess whether tick labels are likely to be difficult to read."""
        axis_title = (ax.get_title() or "").strip() or None
        ensure_canvas_drawn(ax.figure)

        xlabels = [tick for tick in ax.get_xticklabels() if tick.get_text()]
        ylabels = [tick for tick in ax.get_yticklabels() if tick.get_text()]
        tick_count = len(xlabels) + len(ylabels)

        renderer = ax.figure.canvas.get_renderer() if hasattr(ax.figure.canvas, "get_renderer") else None
        if renderer is not None:
            for axis_name, labels in {"x-axis": xlabels, "y-axis": ylabels}.items():
                boxes = [tick.get_window_extent(renderer=renderer) for tick in labels if tick.get_visible()]
                overlaps = sum(1 for left, right in zip(boxes, boxes[1:]) if left.overlaps(right))
                if overlaps:
                    return RuleResult(
                        rule_id=self.rule_id,
                        rule_name=self.rule_name,
                        status="FAIL",
                        message=f"Overlapping {axis_name} tick labels detected.",
                        suggestion="Rotate labels, enlarge the figure, or reduce the number of displayed ticks.",
                        axis_title=axis_title,
                        details={"axis": axis_name, "overlaps": overlaps},
                    )

        if len(xlabels) > 12 or len(ylabels) > 12:
            return RuleResult(
                rule_id=self.rule_id,
                rule_name=self.rule_name,
                status="WARNING",
                message=f"The axis shows many tick labels ({tick_count}).",
                suggestion="Reduce the number of ticks or rotate/simplify labels to improve legibility.",
                axis_title=axis_title,
                details={"x_tick_count": len(xlabels), "y_tick_count": len(ylabels), "tick_count": tick_count},
            )

        steep_rotations = [abs(tick.get_rotation()) for tick in xlabels if abs(tick.get_rotation()) > 75]
        if len(steep_rotations) >= 3:
            return RuleResult(
                rule_id=self.rule_id,
                rule_name=self.rule_name,
                status="WARNING",
                message="Several x-axis labels are nearly vertical.",
                suggestion="Shorten labels or use a wider figure when many category names need to be shown.",
                axis_title=axis_title,
                details={"steep_label_count": len(steep_rotations)},
            )

        font_sizes = [tick.get_fontsize() for tick in xlabels + ylabels]
        if font_sizes and min(font_sizes) < 8:
            return RuleResult(
                rule_id=self.rule_id,
                rule_name=self.rule_name,
                status="WARNING",
                message=f"Very small tick labels detected (minimum font size {min(font_sizes):.1f}).",
                suggestion="Increase the tick label font size for notebook or presentation use.",
                axis_title=axis_title,
                details={"min_fontsize": min(font_sizes)},
            )

        return RuleResult(
            rule_id=self.rule_id,
            rule_name=self.rule_name,
            status="PASS",
            message="No obvious readability issue detected.",
            axis_title=axis_title,
            details={"tick_count": tick_count},
        )
