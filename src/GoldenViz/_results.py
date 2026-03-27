"""Structured result models used across analysis and rendering.

The package keeps analysis results in small dataclasses so that the same report can
be rendered in different ways, such as plain text in a terminal or HTML in a
Jupyter notebook.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Literal, Optional

Status = Literal["PASS", "WARNING", "FAIL", "INFO"]
"""Allowed status labels for a rule evaluation."""


@dataclass(slots=True)
class RuleResult:
    """Outcome for a single rule on a single axis.

    Attributes:
        rule_id: Stable identifier for the rule, such as ``R1``.
        rule_name: Human-readable rule name shown in the report.
        status: Final status returned by the rule.
        message: Main assessment message for the user.
        suggestion: Optional improvement advice shown when relevant.
        axis_title: Title of the axis the rule was evaluated on, when available.
        details: Extra structured information useful for debugging or future renderers.
    """

    rule_id: str
    rule_name: str
    status: Status
    message: str
    suggestion: Optional[str] = None
    axis_title: Optional[str] = None
    details: Dict[str, object] = field(default_factory=dict)


@dataclass(slots=True)
class AxisReport:
    """Aggregated report for one Matplotlib axis.

    Attributes:
        axis_index: Zero-based position of the axis inside the figure.
        axis_title: Current title of the axis, when available.
        rule_results: Ordered results returned by the active GoldenViz rules.
    """

    axis_index: int
    axis_title: Optional[str]
    rule_results: List[RuleResult]


@dataclass(slots=True)
class FigureReport:
    """Top-level report returned for one Matplotlib figure.

    Attributes:
        figure_number: Matplotlib figure number when available.
        axes_reports: Per-axis reports collected from visible axes.
        rendered_in_notebook: Whether the report was displayed through the HTML renderer.
    """

    figure_number: Optional[int]
    axes_reports: List[AxisReport]
    rendered_in_notebook: bool = False

    @property
    def rule_results(self) -> List[RuleResult]:
        """Return a flat list of all rule results across every visible axis."""
        results: List[RuleResult] = []
        for axis_report in self.axes_reports:
            results.extend(axis_report.rule_results)
        return results

    @property
    def summary_counts(self) -> Dict[str, int]:
        """Count how many rule results fall into each status bucket."""
        counts = {"PASS": 0, "WARNING": 0, "FAIL": 0, "INFO": 0}
        for result in self.rule_results:
            counts[result.status] += 1
        return counts
