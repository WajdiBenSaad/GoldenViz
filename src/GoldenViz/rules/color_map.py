"""Rule implementation for misleading color-map checks."""

from __future__ import annotations

from matplotlib.axes import Axes

from GoldenViz._results import RuleResult
from GoldenViz.rules.base import Rule

PROBLEMATIC_CMAPS = {"gist_rainbow", "hsv", "jet", "nipy_spectral", "rainbow", "turbo"}


class ColorMapRule(Rule):
    """Warn when charts use color maps known to be hard to interpret."""

    rule_id = "R19"
    rule_name = "Color map quality"

    def evaluate(self, ax: Axes) -> RuleResult:
        """Assess image and collection color maps."""
        axis_title = (ax.get_title() or "").strip() or None
        color_mapped = [*ax.images, *ax.collections]
        used = []
        for artist in color_mapped:
            cmap = getattr(artist, "cmap", None)
            name = getattr(cmap, "name", None)
            if name:
                used.append(name)

        problematic = sorted({name for name in used if name in PROBLEMATIC_CMAPS})
        if problematic:
            return RuleResult(
                rule_id=self.rule_id,
                rule_name=self.rule_name,
                status="WARNING",
                message=f"Potentially misleading color map detected: {', '.join(problematic)}.",
                suggestion="Prefer perceptually ordered maps such as viridis, cividis, magma, or a domain-specific sequential/diverging map.",
                axis_title=axis_title,
                details={"colormaps": used, "problematic": problematic},
            )

        return RuleResult(
            rule_id=self.rule_id,
            rule_name=self.rule_name,
            status="PASS",
            message="No problematic color map detected.",
            axis_title=axis_title,
            details={"colormaps": used},
        )
