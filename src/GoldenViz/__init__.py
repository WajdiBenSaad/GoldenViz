"""Public package interface for GoldenViz.

GoldenViz provides a small rule-based quality checker for Matplotlib charts.
The package currently exposes two main usage patterns:

- manual analysis with :func:`analyze`, :func:`check`, and :func:`check_current`
- automatic notebook or script integration with :func:`auto` and :func:`disable`
"""

from .analyzer import analyze, check, check_current
from .auto import auto, disable, is_auto_enabled

__all__ = [
    "analyze",
    "check",
    "check_current",
    "auto",
    "disable",
    "is_auto_enabled",
]

__version__ = "0.1.0"
