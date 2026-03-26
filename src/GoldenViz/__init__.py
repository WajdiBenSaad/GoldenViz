"""GoldenViz public API."""

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
