from __future__ import annotations

from matplotlib.axes import Axes

from GoldenViz._results import RuleResult
from GoldenViz._utils import ensure_canvas_drawn
from GoldenViz.rules.base import Rule


class ReadabilityRule(Rule):
    rule_id = "R5"
    rule_name = "Readable labels and ticks"

    def evaluate(self, ax: Axes) -> RuleResult:
        axis_title = (ax.get_title() or "").strip() or None
        ensure_canvas_drawn(ax.figure)

        xlabels = [tick for tick in ax.get_xticklabels() if tick.get_text()]
        ylabels = [tick for tick in ax.get_yticklabels() if tick.get_text()]
        tick_count = len(xlabels) + len(ylabels)

        if tick_count > 24:
            return RuleResult(
                rule_id=self.rule_id,
                rule_name=self.rule_name,
                status="WARNING",
                message=f"The axis shows many tick labels ({tick_count}).",
                suggestion="Reduce the number of ticks or rotate/simplify labels to improve legibility.",
                axis_title=axis_title,
                details={"tick_count": tick_count},
            )

        renderer = ax.figure.canvas.get_renderer() if hasattr(ax.figure.canvas, "get_renderer") else None
        if renderer is not None:
            xboxes = [tick.get_window_extent(renderer=renderer) for tick in xlabels]
            overlaps = 0
            for left, right in zip(xboxes, xboxes[1:]):
                if left.overlaps(right):
                    overlaps += 1
            if overlaps:
                return RuleResult(
                    rule_id=self.rule_id,
                    rule_name=self.rule_name,
                    status="FAIL",
                    message="Overlapping x-axis tick labels detected.",
                    suggestion="Rotate labels, enlarge the figure, or reduce the number of displayed ticks.",
                    axis_title=axis_title,
                    details={"overlaps": overlaps},
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
