import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

import GoldenViz as gv


def statuses_by_rule(report):
    return {result.rule_id: result.status for result in report.rule_results}


def test_missing_title_and_axis_labels_fail():
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [2, 4, 8])

    statuses = statuses_by_rule(gv.analyze(fig))

    assert statuses["R1"] == "FAIL"
    assert statuses["R2"] == "FAIL"
    plt.close(fig)


def test_bar_chart_with_truncated_y_axis_fails_scale_rule():
    fig, ax = plt.subplots()
    ax.bar(["A", "B"], [100, 105])
    ax.set_title("Revenue by segment")
    ax.set_xlabel("Segment")
    ax.set_ylabel("Revenue (EUR)")
    ax.set_ylim(90, 110)

    statuses = statuses_by_rule(gv.analyze(fig))

    assert statuses["R17"] == "FAIL"
    plt.close(fig)


def test_generic_title_warns():
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [2, 4, 8])
    ax.set_title("Results")
    ax.set_xlabel("Year")
    ax.set_ylabel("Revenue (EUR)")

    statuses = statuses_by_rule(gv.analyze(fig))

    assert statuses["R1"] == "WARNING"
    plt.close(fig)


def test_numeric_y_label_without_unit_warns():
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [2, 4, 8])
    ax.set_title("Revenue trend by year")
    ax.set_xlabel("Year")
    ax.set_ylabel("Revenue")

    statuses = statuses_by_rule(gv.analyze(fig))

    assert statuses["R3"] == "WARNING"
    plt.close(fig)


def test_horizontal_bar_with_truncated_x_axis_fails_scale_rule():
    fig, ax = plt.subplots()
    ax.barh(["A", "B"], [100, 105])
    ax.set_title("Revenue by segment")
    ax.set_xlabel("Revenue (EUR)")
    ax.set_ylabel("Segment")
    ax.set_xlim(90, 110)

    statuses = statuses_by_rule(gv.analyze(fig))

    assert statuses["R17"] == "FAIL"
    plt.close(fig)


def test_categorical_line_chart_warns_about_chart_type():
    fig, ax = plt.subplots()
    ax.plot(["Q1", "Q2", "Q3"], [2, 4, 8])
    ax.set_title("Revenue trend by quarter")
    ax.set_xlabel("Quarter")
    ax.set_ylabel("Revenue (EUR)")

    statuses = statuses_by_rule(gv.analyze(fig))

    assert statuses["R18"] == "WARNING"
    plt.close(fig)


def test_pie_chart_warns_about_chart_type():
    fig, ax = plt.subplots()
    ax.pie([40, 35, 25], labels=["A", "B", "C"])
    ax.set_title("Share of revenue")

    statuses = statuses_by_rule(gv.analyze(fig))

    assert statuses["R18"] == "WARNING"
    plt.close(fig)


def test_problematic_colormap_warns():
    fig, ax = plt.subplots()
    ax.imshow([[1, 2], [3, 4]], cmap="jet")
    ax.set_title("Temperature map by region")

    statuses = statuses_by_rule(gv.analyze(fig))

    assert statuses["R19"] == "WARNING"
    plt.close(fig)


def test_many_colors_warns_about_accessibility():
    fig, ax = plt.subplots()
    colors = [f"C{i % 10}" for i in range(10)]
    ax.bar([str(i) for i in range(10)], list(range(10)), color=colors)
    ax.set_title("Revenue by segment")
    ax.set_xlabel("Segment")
    ax.set_ylabel("Revenue (EUR)")

    statuses = statuses_by_rule(gv.analyze(fig))

    assert statuses["R8"] == "WARNING"
    plt.close(fig)


def test_multiple_lines_without_legend_warns():
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [2, 4, 8])
    ax.plot([1, 2, 3], [3, 5, 9])
    ax.set_title("Revenue trend by year")
    ax.set_xlabel("Year")
    ax.set_ylabel("Revenue (EUR)")

    statuses = statuses_by_rule(gv.analyze(fig))

    assert statuses["R4"] == "WARNING"
    plt.close(fig)


def test_small_multiline_legend_warns_about_direct_labeling():
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [2, 4, 8], label="Baseline")
    ax.plot([1, 2, 3], [3, 5, 9], label="Reviewed")
    ax.set_title("Revenue trend by year")
    ax.set_xlabel("Year")
    ax.set_ylabel("Revenue (EUR)")
    ax.legend()

    statuses = statuses_by_rule(gv.analyze(fig))

    assert statuses["R9"] == "WARNING"
    plt.close(fig)


def test_chartjunk_warns_on_heavy_frame_and_grid():
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [2, 4, 8])
    ax.set_title("Revenue trend by year")
    ax.set_xlabel("Year")
    ax.set_ylabel("Revenue (EUR)")
    ax.grid(True, axis="both")

    statuses = statuses_by_rule(gv.analyze(fig))

    assert statuses["R10"] == "WARNING"
    plt.close(fig)


def test_many_bar_categories_warns():
    fig, ax = plt.subplots()
    labels = [f"C{i}" for i in range(13)]
    ax.bar(labels, list(range(13)))
    ax.set_title("Revenue by category")
    ax.set_xlabel("Category")
    ax.set_ylabel("Revenue (EUR)")

    statuses = statuses_by_rule(gv.analyze(fig))

    assert statuses["R11"] == "WARNING"
    plt.close(fig)


def test_unsorted_bars_warn():
    fig, ax = plt.subplots()
    ax.bar(["A", "B", "C", "D"], [4, 1, 3, 2])
    ax.set_title("Revenue by category")
    ax.set_xlabel("Category")
    ax.set_ylabel("Revenue (EUR)")

    statuses = statuses_by_rule(gv.analyze(fig))

    assert statuses["R12"] == "WARNING"
    plt.close(fig)


def test_annotation_context_warns_for_many_marks_without_text():
    fig, ax = plt.subplots()
    ax.bar([str(i) for i in range(6)], [1, 2, 3, 4, 5, 6])
    ax.set_title("Revenue by category")
    ax.set_xlabel("Category")
    ax.set_ylabel("Revenue (EUR)")

    statuses = statuses_by_rule(gv.analyze(fig))

    assert statuses["R5"] == "WARNING"
    plt.close(fig)


def test_dual_axis_warns():
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [2, 4, 8])
    twin = ax.twinx()
    twin.plot([1, 2, 3], [20, 40, 80], color="C1")
    ax.set_title("Revenue and margin by year")
    ax.set_xlabel("Year")
    ax.set_ylabel("Revenue (EUR)")
    twin.set_ylabel("Margin (%)")

    statuses = statuses_by_rule(gv.analyze(fig))

    assert statuses["R20"] == "WARNING"
    plt.close(fig)


def test_area_baseline_warns_on_truncated_area():
    fig, ax = plt.subplots()
    ax.fill_between([1, 2, 3], [10, 12, 14])
    ax.set_ylim(8, 15)
    ax.set_title("Revenue area by year")
    ax.set_xlabel("Year")
    ax.set_ylabel("Revenue (EUR)")

    statuses = statuses_by_rule(gv.analyze(fig))

    assert statuses["R21"] == "WARNING"
    plt.close(fig)


def test_extreme_aspect_ratio_warns():
    fig, ax = plt.subplots(figsize=(12, 2))
    ax.plot([1, 2, 3], [2, 4, 8])
    ax.set_title("Revenue trend by year")
    ax.set_xlabel("Year")
    ax.set_ylabel("Revenue (EUR)")

    statuses = statuses_by_rule(gv.analyze(fig))

    assert statuses["R22"] == "WARNING"
    plt.close(fig)


def test_scatter_overplotting_warns_on_duplicate_points():
    fig, ax = plt.subplots()
    ax.scatter([1, 1, 2], [3, 3, 4])
    ax.set_title("Revenue relationship by segment")
    ax.set_xlabel("Input score")
    ax.set_ylabel("Revenue (EUR)")

    statuses = statuses_by_rule(gv.analyze(fig))

    assert statuses["R13"] == "WARNING"
    plt.close(fig)


def test_histogram_bin_count_warns():
    fig, ax = plt.subplots()
    ax.hist(np.arange(100), bins=60)
    ax.set_title("Revenue distribution by account")
    ax.set_xlabel("Revenue (EUR)")
    ax.set_ylabel("Account count")

    statuses = statuses_by_rule(gv.analyze(fig))

    assert statuses["R23"] == "WARNING"
    plt.close(fig)


def test_uncertainty_info_for_line_without_band():
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3, 4, 5], [2, 4, 8, 9, 12])
    ax.set_title("Revenue trend by year")
    ax.set_xlabel("Year")
    ax.set_ylabel("Revenue (EUR)")

    statuses = statuses_by_rule(gv.analyze(fig))

    assert statuses["R6"] == "INFO"
    plt.close(fig)


def test_category_color_consistency_warns():
    fig, ax = plt.subplots()
    ax.bar(["A", "B", "C", "D"], [1, 2, 3, 4], color=["C0", "C1", "C0", "C0"])
    ax.set_title("Revenue by category")
    ax.set_xlabel("Category")
    ax.set_ylabel("Revenue (EUR)")

    statuses = statuses_by_rule(gv.analyze(fig))

    assert statuses["R24"] == "WARNING"
    plt.close(fig)


def test_decimal_precision_warns():
    fig, ax = plt.subplots()
    ax.plot([0.1111, 0.2222, 0.3333], [1.1111, 2.2222, 3.3333])
    ax.set_title("Revenue trend by year")
    ax.set_xlabel("Share")
    ax.set_ylabel("Revenue (EUR)")
    ax.set_xticks([0.1111, 0.2222, 0.3333])

    statuses = statuses_by_rule(gv.analyze(fig))

    assert statuses["R14"] == "WARNING"
    plt.close(fig)


def test_date_axis_formatting_warns():
    fig, ax = plt.subplots()
    labels = [f"2026-01-{day:02d}" for day in range(1, 9)]
    ax.plot(labels, list(range(8)))
    ax.set_title("Revenue trend by day")
    ax.set_xlabel("Date")
    ax.set_ylabel("Revenue (EUR)")

    statuses = statuses_by_rule(gv.analyze(fig))

    assert statuses["R15"] == "WARNING"
    plt.close(fig)


def test_diverging_zero_reference_warns():
    fig, ax = plt.subplots()
    ax.bar(["A", "B", "C"], [-2, 3, 4])
    ax.set_title("Profit by segment")
    ax.set_xlabel("Segment")
    ax.set_ylabel("Profit (EUR)")

    statuses = statuses_by_rule(gv.analyze(fig))

    assert statuses["R25"] == "WARNING"
    plt.close(fig)


def test_visual_economy_warns():
    fig, ax = plt.subplots()
    ax.bar([str(i) for i in range(81)], list(range(81)))
    ax.set_title("Revenue by category")
    ax.set_xlabel("Category")
    ax.set_ylabel("Revenue (EUR)")

    statuses = statuses_by_rule(gv.analyze(fig))

    assert statuses["R16"] == "WARNING"
    plt.close(fig)
