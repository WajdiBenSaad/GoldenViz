from GoldenViz._results import AxisReport, FigureReport, RuleResult
from GoldenViz.renderers import render_html_report, render_text_report


def sample_report():
    return FigureReport(
        figure_number=1,
        axes_reports=[
            AxisReport(
                axis_index=0,
                axis_title="Example",
                rule_results=[
                    RuleResult(
                        rule_id="R0",
                        rule_name="Missing title",
                        status="WARNING",
                        message="Title may need more context.",
                    ),
                    RuleResult(
                        rule_id="R1",
                        rule_name="Clear title",
                        status="PASS",
                        message="Title detected.",
                    )
                ],
            )
        ],
    )


def test_render_text_report_contains_rule_result():
    rendered = render_text_report(sample_report())

    assert "GoldenViz Report" in rendered
    assert "Clear title: PASS" in rendered


def test_render_html_report_contains_summary_counts():
    rendered = render_html_report(sample_report())

    assert "GoldenViz report" in rendered
    assert "PASS 1" in rendered
    assert "WARNING 1" in rendered


def test_render_html_report_prioritizes_attention_before_passes():
    rendered = render_html_report(sample_report())

    assert "View warnings and failures" in rendered
    assert "Needs attention (1)" in rendered
    assert "Passing checks (1)" in rendered
    assert rendered.index("Missing title") < rendered.index("Clear title")
