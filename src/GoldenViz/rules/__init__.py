"""Rule implementations for the currently supported GoldenViz checks."""

from .axis_labels import AxisLabelsRule
from .annotation import AnnotationRule
from .area_baseline import AreaBaselineRule
from .aspect_ratio import AspectRatioRule
from .bar_sorting import BarSortingRule
from .category_colors import CategoryColorRule
from .category_count import CategoryCountRule
from .chartjunk import ChartjunkRule
from .color_accessibility import ColorAccessibilityRule
from .color_map import ColorMapRule
from .chart_type import ChartTypeRule
from .date_axis import DateAxisRule
from .diverging_zero import DivergingZeroRule
from .direct_labeling import DirectLabelingRule
from .dual_axis import DualAxisRule
from .histogram_bins import HistogramBinsRule
from .legend import LegendRule
from .overplotting import OverplottingRule
from .precision import PrecisionRule
from .readability import ReadabilityRule
from .scale import ScaleRule
from .title import TitleRule
from .units import UnitsRule
from .uncertainty import UncertaintyRule
from .visual_economy import VisualEconomyRule

__all__ = [
    "TitleRule",
    "AxisLabelsRule",
    "ScaleRule",
    "ChartTypeRule",
    "ReadabilityRule",
    "UnitsRule",
    "ColorMapRule",
    "ColorAccessibilityRule",
    "LegendRule",
    "DirectLabelingRule",
    "ChartjunkRule",
    "CategoryCountRule",
    "BarSortingRule",
    "AnnotationRule",
    "DualAxisRule",
    "AreaBaselineRule",
    "AspectRatioRule",
    "OverplottingRule",
    "HistogramBinsRule",
    "UncertaintyRule",
    "CategoryColorRule",
    "PrecisionRule",
    "DateAxisRule",
    "DivergingZeroRule",
    "VisualEconomyRule",
]
