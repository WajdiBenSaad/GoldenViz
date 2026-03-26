from __future__ import annotations

from html import escape
from typing import Iterable

from GoldenViz._results import FigureReport, RuleResult


STATUS_COLORS = {
    "PASS": "#1f7a4d",
    "WARNING": "#9a6700",
    "FAIL": "#b42318",
    "INFO": "#0c4a6e",
}

STATUS_BADGES = {
    "PASS": "PASS",
    "WARNING": "WARNING",
    "FAIL": "FAIL",
    "INFO": "INFO",
}


def render_text_report(report: FigureReport) -> str:
    lines = [f"GoldenViz Report - score: {report.score}/100"]
    for axis_report in report.axes_reports:
        axis_name = axis_report.axis_title or f"Axis {axis_report.axis_index + 1}"
        lines.append(f"\n[{axis_name}]")
        for result in axis_report.rule_results:
            lines.append(f"- {result.rule_name}: {result.status} - {result.message}")
            if result.suggestion:
                lines.append(f"  suggestion: {result.suggestion}")
    return "\n".join(lines)



def _render_rule_row(result: RuleResult) -> str:
    color = STATUS_COLORS[result.status]
    suggestion = f"<div style='margin-top:4px;color:#475467;'>{escape(result.suggestion)}</div>" if result.suggestion else ""
    return f"""
    <tr>
      <td style='padding:10px 12px;border-top:1px solid #eaecf0;vertical-align:top;font-weight:600;'>{escape(result.rule_name)}</td>
      <td style='padding:10px 12px;border-top:1px solid #eaecf0;vertical-align:top;'>
        <span style='display:inline-block;padding:2px 8px;border-radius:999px;background:{color}18;color:{color};font-weight:700;font-size:12px;'>{STATUS_BADGES[result.status]}</span>
      </td>
      <td style='padding:10px 12px;border-top:1px solid #eaecf0;vertical-align:top;'>
        <div>{escape(result.message)}</div>
        {suggestion}
      </td>
    </tr>
    """



def render_html_report(report: FigureReport) -> str:
    counts = report.summary_counts
    sections = []
    for axis_report in report.axes_reports:
        axis_name = axis_report.axis_title or f"Axis {axis_report.axis_index + 1}"
        rows = "".join(_render_rule_row(result) for result in axis_report.rule_results)
        sections.append(
            f"""
            <div style='margin-top:18px;'>
              <div style='font-weight:700;font-size:15px;margin-bottom:8px;color:#101828;'>{escape(axis_name)}</div>
              <table style='border-collapse:collapse;width:100%;font-size:13px;'>
                <thead>
                  <tr style='text-align:left;background:#f8fafc;'>
                    <th style='padding:10px 12px;border-bottom:1px solid #eaecf0;'>Rule</th>
                    <th style='padding:10px 12px;border-bottom:1px solid #eaecf0;'>Status</th>
                    <th style='padding:10px 12px;border-bottom:1px solid #eaecf0;'>Assessment</th>
                  </tr>
                </thead>
                <tbody>{rows}</tbody>
              </table>
            </div>
            """
        )

    return f"""
    <div style='margin:16px 0 8px 0;border:1px solid #e4e7ec;border-radius:16px;padding:16px 18px;background:white;box-shadow:0 1px 2px rgba(16,24,40,.06);font-family:Inter,Segoe UI,Arial,sans-serif;'>
      <div style='display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;'>
        <div>
          <div style='font-size:18px;font-weight:800;color:#101828;'>GoldenViz report</div>
          <div style='font-size:13px;color:#475467;margin-top:4px;'>Automatic visual QA for the first five Golden Rules.</div>
        </div>
        <div style='padding:8px 12px;border-radius:12px;background:#fff7e6;border:1px solid #fedf89;font-weight:800;color:#7a4b00;'>Score: {report.score}/100</div>
      </div>
      <div style='display:flex;gap:10px;flex-wrap:wrap;margin-top:14px;'>
        <span style='padding:4px 8px;border-radius:999px;background:#ecfdf3;color:#067647;font-weight:700;font-size:12px;'>PASS {counts['PASS']}</span>
        <span style='padding:4px 8px;border-radius:999px;background:#fffaeb;color:#b54708;font-weight:700;font-size:12px;'>WARNING {counts['WARNING']}</span>
        <span style='padding:4px 8px;border-radius:999px;background:#fef3f2;color:#b42318;font-weight:700;font-size:12px;'>FAIL {counts['FAIL']}</span>
      </div>
      {''.join(sections)}
    </div>
    """
