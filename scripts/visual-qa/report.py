#!/usr/bin/env python3
"""
Visual QA Report Generator — Creates an HTML report with side-by-side
screenshots, ratings, and issue details for every crawled page.

Usage:
  python scripts/visual-qa/report.py
  open qa-output/report.html
"""

import json
import sys
from pathlib import Path
from datetime import datetime

OUTPUT_DIR = Path(__file__).resolve().parent.parent.parent / "qa-output"


def score_badge(score):
    """Return an HTML badge for a 1-5 score."""
    if score >= 4:
        color, label = "#22c55e", "Good"
    elif score >= 3:
        color, label = "#eab308", "OK"
    elif score >= 2:
        color, label = "#f97316", "Poor"
    else:
        color, label = "#ef4444", "Broken"
    return f'<span style="background:{color};color:#fff;padding:2px 8px;border-radius:4px;font-size:12px;font-weight:600">{score}/5 {label}</span>'


def priority_badge(priority):
    colors = {
        "critical": "#ef4444",
        "high": "#f97316",
        "medium": "#eab308",
        "low": "#3b82f6",
        "none": "#22c55e",
    }
    c = colors.get(priority, "#9ca3af")
    return f'<span style="background:{c};color:#fff;padding:2px 8px;border-radius:4px;font-size:12px;font-weight:600">{priority.upper()}</span>'


def generate_report(analysis_path=None, crawl_path=None):
    a_path = Path(analysis_path) if analysis_path else OUTPUT_DIR / "analysis.json"
    c_path = Path(crawl_path) if crawl_path else OUTPUT_DIR / "crawl.json"

    if not a_path.exists():
        print(f"❌ Analysis not found at {a_path}")
        return
    if not c_path.exists():
        print(f"❌ Crawl data not found at {c_path}")
        return

    analysis = json.loads(a_path.read_text())
    crawl = json.loads(c_path.read_text())

    pages = analysis.get("all_pages", [])
    crawl_pages = {p["page"]: p for p in crawl.get("pages", [])}

    # Build page cards
    page_cards = []
    for p in pages:
        r = p.get("rating", {})
        cp = crawl_pages.get(p["page"], {})
        errors = cp.get("katex_errors", [])
        ss_path = p.get("screenshot", "")

        math_score = r.get("math_rendering", "?")
        content_score = r.get("content_quality", "?")
        layout_score = r.get("layout", "?")
        issues = r.get("issues", [])
        priority = r.get("fix_priority", "none")

        error_rows = ""
        for e in errors:
            error_rows += f"""<tr>
                <td><code>{e.get('type', 'unknown')}</code></td>
                <td><code>{(e.get('text', '') or e.get('html', ''))[:100]}</code></td>
            </tr>"""

        issue_list = "".join(f"<li>{iss}</li>" for iss in issues)

        card = f"""
        <div class="page-card" id="page-{p['page'].replace('/', '-').replace('.', '-')}">
            <div class="card-header">
                <h3>{p['page']}</h3>
                <div class="badges">
                    {priority_badge(priority)}
                    <span class="badge-route">{p.get('route', '')}</span>
                </div>
            </div>
            <div class="card-body">
                <div class="screenshot-col">
                    <img src="{ss_path}" alt="{p['page']}" loading="lazy"
                         onclick="this.classList.toggle('expanded')" />
                </div>
                <div class="details-col">
                    <div class="scores">
                        <div>Math: {score_badge(math_score) if isinstance(math_score, int) else math_score}</div>
                        <div>Content: {score_badge(content_score) if isinstance(content_score, int) else content_score}</div>
                        <div>Layout: {score_badge(layout_score) if isinstance(layout_score, int) else layout_score}</div>
                    </div>
                    {'<div class="issues"><h4>Issues</h4><ul>' + issue_list + '</ul></div>' if issues else '<p class="no-issues">✅ No issues detected</p>'}
                    {'<div class="dom-errors"><h4>KaTeX DOM Errors (' + str(len(errors)) + ')</h4><table>' + error_rows + '</table></div>' if errors else ''}
                </div>
            </div>
        </div>
        """
        page_cards.append(card)

    # Summary stats
    critical = analysis.get("critical_count", 0)
    total = analysis.get("total_pages", 0)
    avg_math = analysis.get("average_math_score", 0)
    avg_content = analysis.get("average_content_score", 0)
    avg_layout = analysis.get("average_layout_score", 0)
    crawl_errors = crawl.get("total_katex_errors", 0)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Visual QA Report — Calc Mastery</title>
<style>
:root {{
    --bg: #0f172a;
    --card-bg: #1e293b;
    --text: #e2e8f0;
    --muted: #94a3b8;
    --border: #334155;
    --accent: #3b82f6;
}}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: var(--bg); color: var(--text); padding: 24px; }}
h1 {{ font-size: 28px; margin-bottom: 8px; }}
.subtitle {{ color: var(--muted); margin-bottom: 24px; }}
.summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 16px; margin-bottom: 32px; }}
.stat-card {{ background: var(--card-bg); border: 1px solid var(--border); border-radius: 12px; padding: 16px; text-align: center; }}
.stat-card .value {{ font-size: 32px; font-weight: 700; }}
.stat-card .label {{ color: var(--muted); font-size: 13px; margin-top: 4px; }}
.filters {{ display: flex; gap: 8px; margin-bottom: 24px; flex-wrap: wrap; }}
.filters button {{ background: var(--card-bg); border: 1px solid var(--border); color: var(--text); padding: 8px 16px; border-radius: 8px; cursor: pointer; font-size: 13px; }}
.filters button.active {{ background: var(--accent); border-color: var(--accent); }}
.page-card {{ background: var(--card-bg); border: 1px solid var(--border); border-radius: 12px; margin-bottom: 16px; overflow: hidden; }}
.card-header {{ display: flex; justify-content: space-between; align-items: center; padding: 12px 16px; border-bottom: 1px solid var(--border); }}
.card-header h3 {{ font-size: 16px; }}
.badges {{ display: flex; gap: 8px; align-items: center; }}
.badge-route {{ background: var(--bg); padding: 2px 8px; border-radius: 4px; font-size: 12px; color: var(--muted); font-family: monospace; }}
.card-body {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; padding: 16px; }}
.screenshot-col img {{ width: 100%; border-radius: 8px; border: 1px solid var(--border); cursor: pointer; transition: all 0.3s; }}
.screenshot-col img.expanded {{ position: fixed; top: 5vh; left: 5vw; width: 90vw; height: auto; max-height: 90vh; object-fit: contain; z-index: 1000; border: 3px solid var(--accent); }}
.scores {{ display: flex; flex-direction: column; gap: 8px; margin-bottom: 16px; }}
.issues h4, .dom-errors h4 {{ font-size: 14px; margin-bottom: 8px; color: var(--muted); }}
.issues ul {{ padding-left: 20px; font-size: 14px; }}
.issues li {{ margin-bottom: 4px; }}
.dom-errors table {{ width: 100%; font-size: 13px; border-collapse: collapse; }}
.dom-errors td {{ padding: 4px 8px; border-bottom: 1px solid var(--border); }}
.no-issues {{ color: #22c55e; font-size: 14px; }}
@media (max-width: 768px) {{
    .card-body {{ grid-template-columns: 1fr; }}
}}
</style>
</head>
<body>
<h1>🔍 Visual QA Report</h1>
<p class="subtitle">Generated {datetime.now().strftime('%Y-%m-%d %H:%M')} • {total} pages crawled • {crawl.get('elapsed_seconds', '?')}s crawl time</p>

<div class="summary">
    <div class="stat-card"><div class="value">{total}</div><div class="label">Pages Screenshotted</div></div>
    <div class="stat-card"><div class="value" style="color:{'#ef4444' if critical > 0 else '#22c55e'}">{critical}</div><div class="label">Critical Issues</div></div>
    <div class="stat-card"><div class="value" style="color:{'#ef4444' if crawl_errors > 0 else '#22c55e'}">{crawl_errors}</div><div class="label">KaTeX DOM Errors</div></div>
    <div class="stat-card"><div class="value">{avg_math}</div><div class="label">Avg Math Score</div></div>
    <div class="stat-card"><div class="value">{avg_content}</div><div class="label">Avg Content Score</div></div>
    <div class="stat-card"><div class="value">{avg_layout}</div><div class="label">Avg Layout Score</div></div>
</div>

<div class="filters">
    <button class="active" onclick="filterPages('all')">All ({total})</button>
    <button onclick="filterPages('critical')">🔴 Critical ({critical})</button>
    <button onclick="filterPages('errors')">⚠️ Has Errors ({crawl.get('pages_with_errors', 0)})</button>
    <button onclick="filterPages('clean')">✅ Clean ({total - critical})</button>
</div>

{''.join(page_cards)}

<script>
function filterPages(filter) {{
    document.querySelectorAll('.filters button').forEach(b => b.classList.remove('active'));
    event.target.classList.add('active');
    document.querySelectorAll('.page-card').forEach(card => {{
        const hasCritical = card.querySelector('[style*="ef4444"]') !== null;
        const hasErrors = card.querySelector('.dom-errors') !== null;
        if (filter === 'all') card.style.display = '';
        else if (filter === 'critical') card.style.display = hasCritical ? '' : 'none';
        else if (filter === 'errors') card.style.display = hasErrors ? '' : 'none';
        else if (filter === 'clean') card.style.display = (!hasCritical && !hasErrors) ? '' : 'none';
    }});
}}
// Click screenshot to expand
document.addEventListener('keydown', e => {{
    if (e.key === 'Escape') document.querySelectorAll('.expanded').forEach(el => el.classList.remove('expanded'));
}});
</script>
</body>
</html>"""

    report_path = OUTPUT_DIR / "report.html"
    report_path.write_text(html)

    print(f"📊 Report generated: {report_path}")
    print(f"   Open it: open {report_path}")
    return str(report_path)


if __name__ == "__main__":
    generate_report()
