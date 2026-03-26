from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Literal, Optional

Status = Literal["PASS", "WARNING", "FAIL", "INFO"]


@dataclass(slots=True)
class RuleResult:
    rule_id: str
    rule_name: str
    status: Status
    message: str
    suggestion: Optional[str] = None
    axis_title: Optional[str] = None
    details: Dict[str, object] = field(default_factory=dict)


@dataclass(slots=True)
class AxisReport:
    axis_index: int
    axis_title: Optional[str]
    rule_results: List[RuleResult]


@dataclass(slots=True)
class FigureReport:
    figure_number: Optional[int]
    axes_reports: List[AxisReport]
    rendered_in_notebook: bool = False

    @property
    def rule_results(self) -> List[RuleResult]:
        results: List[RuleResult] = []
        for axis_report in self.axes_reports:
            results.extend(axis_report.rule_results)
        return results

    @property
    def summary_counts(self) -> Dict[str, int]:
        counts = {"PASS": 0, "WARNING": 0, "FAIL": 0, "INFO": 0}
        for result in self.rule_results:
            counts[result.status] += 1
        return counts
