import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

import GoldenViz as gv
from GoldenViz._results import FigureReport


EXPECTED_RULE_IDS = [f"R{index}" for index in range(1, 26)]


def test_public_api_exports_expected_symbols():
    expected_symbols = [
        "analyze",
        "check",
        "check_current",
        "auto",
        "disable",
        "is_auto_enabled",
        "__version__",
    ]

    for symbol in expected_symbols:
        assert hasattr(gv, symbol)


def test_analyze_returns_report_for_visible_axis():
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [2, 4, 8])
    ax.set_title("Revenue trend")
    ax.set_xlabel("Year")
    ax.set_ylabel("Revenue")

    report = gv.analyze(fig)

    assert isinstance(report, FigureReport)
    assert len(report.axes_reports) == 1
    assert len(report.rule_results) == 25
    assert report.summary_counts["PASS"] >= 1
    plt.close(fig)


def test_analyze_empty_figure_returns_empty_report():
    fig = plt.figure()

    report = gv.analyze(fig)

    assert isinstance(report, FigureReport)
    assert report.axes_reports == []
    assert report.rule_results == []
    assert report.summary_counts == {"PASS": 0, "WARNING": 0, "FAIL": 0, "INFO": 0}
    plt.close(fig)


def test_analyze_multiple_visible_axes_returns_axis_reports():
    fig, axes = plt.subplots(1, 2)
    for index, ax in enumerate(axes):
        ax.plot([1, 2, 3], [index + 1, index + 2, index + 3])
        ax.set_title(f"Revenue trend {index + 1}")
        ax.set_xlabel("Year")
        ax.set_ylabel("Revenue (EUR)")

    report = gv.analyze(fig)

    assert len(report.axes_reports) == 2
    assert [axis_report.axis_index for axis_report in report.axes_reports] == [0, 1]
    assert all(len(axis_report.rule_results) == 25 for axis_report in report.axes_reports)
    plt.close(fig)


def test_analyze_ignores_hidden_axes():
    fig, axes = plt.subplots(1, 2)
    axes[0].plot([1, 2, 3], [2, 4, 8])
    axes[0].set_title("Revenue trend")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Revenue (EUR)")
    axes[1].set_visible(False)

    report = gv.analyze(fig)

    assert len(report.axes_reports) == 1
    assert report.axes_reports[0].axis_index == 0
    plt.close(fig)


def test_rule_results_use_expected_order_and_status_values():
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [2, 4, 8])
    ax.set_title("Revenue trend by year")
    ax.set_xlabel("Year")
    ax.set_ylabel("Revenue (EUR)")

    report = gv.analyze(fig)

    assert [result.rule_id for result in report.rule_results] == EXPECTED_RULE_IDS
    assert {result.status for result in report.rule_results} <= {
        "PASS",
        "WARNING",
        "FAIL",
        "INFO",
    }
    plt.close(fig)


def test_check_returns_report_when_display_is_false():
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [2, 4, 8])
    ax.set_title("Revenue trend")
    ax.set_xlabel("Year")
    ax.set_ylabel("Revenue")

    report = gv.check(fig, display=False)

    assert report is not None
    assert report.axes_reports[0].axis_title == "Revenue trend"
    plt.close(fig)


def test_check_current_returns_report_for_current_figure_when_display_is_false():
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [2, 4, 8])
    ax.set_title("Current revenue trend")
    ax.set_xlabel("Year")
    ax.set_ylabel("Revenue (EUR)")

    report = gv.check_current(display=False)

    assert report is not None
    assert report.axes_reports[0].axis_title == "Current revenue trend"
    plt.close(fig)


def test_auto_mode_state_toggles_cleanly():
    gv.disable()

    assert gv.is_auto_enabled() is False

    gv.auto()
    assert gv.is_auto_enabled() is True

    gv.disable()
    assert gv.is_auto_enabled() is False
