"""Text and HTML renderers for GoldenViz reports."""

from __future__ import annotations

from html import escape

from GoldenViz._results import FigureReport, RuleResult


STATUS_COLORS = {
    "PASS": "#1f7a4d",
    "WARNING": "#9a6700",
    "FAIL": "#b42318",
    "INFO": "#0c4a6e",
}
"""Badge colors used in the HTML renderer."""

STATUS_BADGES = {
    "PASS": "PASS",
    "WARNING": "WARNING",
    "FAIL": "FAIL",
    "INFO": "INFO",
}
"""Short badge labels displayed in reports."""



def render_text_report(report: FigureReport) -> str:
    """Render a compact plain-text report for terminals and logs."""
    lines = ["GoldenViz Report"]
    for axis_report in report.axes_reports:
        axis_name = axis_report.axis_title or f"Axis {axis_report.axis_index + 1}"
        lines.append(f"\n[{axis_name}]")
        for result in axis_report.rule_results:
            lines.append(f"- {result.rule_name}: {result.status} - {result.message}")
            if result.suggestion:
                lines.append(f"  suggestion: {result.suggestion}")
    return "\n".join(lines)



def _render_rule_row(result: RuleResult) -> str:
    """Render one HTML table row for a single rule result."""
    color = STATUS_COLORS[result.status]
    suggestion = f"<div style='margin-top:4px;color:#475467;text-align:left;'>{escape(result.suggestion)}</div>" if result.suggestion else ""
    return f"""
    <tr>
      <td style='padding:10px 12px;border-top:1px solid #eaecf0;vertical-align:top;font-weight:600;text-align:left;'>{escape(result.rule_name)}</td>
      <td style='padding:10px 12px;border-top:1px solid #eaecf0;vertical-align:top;text-align:left;'>
        <span style='display:inline-block;padding:2px 8px;border-radius:999px;background:{color}18;color:{color};font-weight:700;font-size:12px;text-align:left;'>{STATUS_BADGES[result.status]}</span>
      </td>
      <td style='padding:10px 12px;border-top:1px solid #eaecf0;vertical-align:top;text-align:left;'>
        <div style='text-align:left;'>{escape(result.message)}</div>
        {suggestion}
      </td>
    </tr>
    """



def render_html_report(report: FigureReport) -> str:
    """Render the notebook HTML card used by GoldenViz."""
    counts = report.summary_counts
    sections = []
    for axis_report in report.axes_reports:
        axis_name = axis_report.axis_title or f"Axis {axis_report.axis_index + 1}"
        rows = "".join(_render_rule_row(result) for result in axis_report.rule_results)
        sections.append(
            f"""
            <div style='margin-top:18px;'>
              <div style='padding:10px 12px;margin-bottom:8px;border:1px solid #d0d5dd;border-radius:12px;background:#f8fafc;color:#101828;font-weight:800;font-size:14px;text-align:left;'>Axis: {escape(axis_name)}</div>
              <table style='border-collapse:collapse;width:100%;font-size:13px;text-align:left;'>
                <thead>
                  <tr style='text-align:left;background:#f8fafc;'>
                    <th style='padding:10px 12px;border-bottom:1px solid #eaecf0;text-align:left;'>Rule</th>
                    <th style='padding:10px 12px;border-bottom:1px solid #eaecf0;text-align:left;'>Status</th>
                    <th style='padding:10px 12px;border-bottom:1px solid #eaecf0;text-align:left;'>Assessment</th>
                  </tr>
                </thead>
                <tbody>{rows}</tbody>
              </table>
            </div>
            """
        )

    return f"""
    <div style='margin:16px 0 8px 0;border:1px solid #e4e7ec;border-radius:16px;padding:16px 18px;background:white;box-shadow:0 1px 2px rgba(16,24,40,.06);font-family:Inter,Segoe UI,Arial,sans-serif;text-align:left;'>
      <details open style='text-align:left;'>
        <summary style='cursor:pointer;list-style:none;display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;'>
          <span style='display:block;'>
            <span style='display:block;font-size:18px;font-weight:800;color:#101828;'>GoldenViz report</span>
            <span style='display:block;font-size:13px;color:#475467;margin-top:4px;'>Automatic visual QA for the first five Golden Rules.</span>
          </span>
        </summary>
        <div style='display:flex;gap:10px;flex-wrap:wrap;margin-top:14px;'>
          <span style='padding:4px 8px;border-radius:999px;background:#ecfdf3;color:#067647;font-weight:700;font-size:12px;'>PASS {counts['PASS']}</span>
          <span style='padding:4px 8px;border-radius:999px;background:#fffaeb;color:#b54708;font-weight:700;font-size:12px;'>WARNING {counts['WARNING']}</span>
          <span style='padding:4px 8px;border-radius:999px;background:#fef3f2;color:#b42318;font-weight:700;font-size:12px;'>FAIL {counts['FAIL']}</span>
        </div>
        {''.join(sections)}
      </details>
    </div>
    """
