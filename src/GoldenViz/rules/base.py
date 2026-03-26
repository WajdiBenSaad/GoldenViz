from __future__ import annotations

from abc import ABC, abstractmethod

from matplotlib.axes import Axes

from GoldenViz._results import RuleResult


class Rule(ABC):
    rule_id: str
    rule_name: str

    @abstractmethod
    def evaluate(self, ax: Axes) -> RuleResult:
        raise NotImplementedError
