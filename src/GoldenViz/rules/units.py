"""Rule implementation for unit and scale clarity checks."""

from __future__ import annotations

import re

from matplotlib.axes import Axes

from GoldenViz._results import RuleResult
from GoldenViz._utils import axis_kind, stringify_label
from GoldenViz.rules.base import Rule

UNIT_PATTERN = re.compile(
    r"(%|\$|\u20ac|\(|\[|\bkg\b|\bkm\b|\bm\b|\bcm\b|\bmm\b|\bms\b|\bs\b|\bmin\b|\bh\b|\busd\b|\beur\b|\bgbp\b|\bscore\b|\bpoints?\b|\bunits?\b|\bindex\b|\byears?\b|\bmonths?\b|\bdays?\b|\bquarters?\b)",
    re.IGNORECASE,
)


def _has_unit_or_scale(label: str) -> bool:
    return bool(UNIT_PATTERN.search(label))


def _has_numeric_y_data(ax: Axes) -> bool:
    if ax.lines:
        return any(len(line.get_ydata()) > 0 for line in ax.lines)
    if ax.collections:
        return any(getattr(collection, "get_offsets", lambda: [])().size for collection in ax.collections)
    if ax.patches:
        return any(hasattr(patch, "get_height") for patch in ax.patches)
    if ax.images:
        return True
    return False


class UnitsRule(Rule):
    """Check whether numeric axes describe their units or scale."""

    rule_id = "R3"
    rule_name = "Units and scale clarity"

    def evaluate(self, ax: Axes) -> RuleResult:
        """Assess whether numeric axes explain their measurement scale."""
        axis_title = (ax.get_title() or "").strip() or None
        xlabel = stringify_label(ax.get_xlabel())
        ylabel = stringify_label(ax.get_ylabel())
        kind = axis_kind(ax)

        missing = []
        if _has_numeric_y_data(ax) and ylabel and not _has_unit_or_scale(ylabel):
            missing.append("y-axis")
        if kind in {"scatter", "line"} and xlabel and not _has_unit_or_scale(xlabel):
            missing.append("x-axis")

        if missing:
            return RuleResult(
                rule_id=self.rule_id,
                rule_name=self.rule_name,
                status="WARNING",
                message=f"Numeric label(s) may be missing units or scale: {', '.join(missing)}.",
                suggestion="Add units or scale where relevant, such as %, EUR, kg, index, score, or units.",
                axis_title=axis_title,
                details={"xlabel": xlabel, "ylabel": ylabel, "missing_units": missing, "chart_type": kind},
            )

        return RuleResult(
            rule_id=self.rule_id,
            rule_name=self.rule_name,
            status="PASS",
            message="Numeric labels include detectable units or scale where applicable.",
            axis_title=axis_title,
            details={"xlabel": xlabel, "ylabel": ylabel, "chart_type": kind},
        )
