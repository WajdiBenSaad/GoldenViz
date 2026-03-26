"""Abstract base class for GoldenViz rules."""

from __future__ import annotations

from abc import ABC, abstractmethod

from matplotlib.axes import Axes

from GoldenViz._results import RuleResult


class Rule(ABC):
    """Base interface shared by all GoldenViz rules."""

    rule_id: str
    rule_name: str

    @abstractmethod
    def evaluate(self, ax: Axes) -> RuleResult:
        """Evaluate the rule on one Matplotlib axis and return a structured result."""
        raise NotImplementedError
