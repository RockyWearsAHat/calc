#!/usr/bin/env python3
"""
Visual QA Analyzer — Takes crawl.json + screenshots, sends them through
GPT-5 mini via Copilot CLI for visual analysis, and produces rated findings.

For each screenshot, the analyzer:
1. Reads the image and encodes it for analysis
2. Checks the DOM-based errors from the crawl manifest
3. Sends a description + DOM context to GPT-5 mini for content quality rating
4. Outputs a rated analysis in qa-output/analysis.json

Usage:
  python scripts/visual-qa/analyze.py [--manifest qa-output/crawl.json]
"""

import json
import subprocess
import sys
from pathlib import Path

OUTPUT_DIR = Path(__file__).resolve().parent.parent.parent / "qa-output"
MANIFEST_PATH = OUTPUT_DIR / "crawl.json"


def call_copilot(prompt, model="gpt-5-mini"):
    """Call copilot CLI and return the response text."""
    try:
        result = subprocess.run(
            ["copilot", "-p", prompt, "--model", model, "-s"],
            capture_output=True, text=True, timeout=60
        )
        return result.stdout.strip() if result.returncode == 0 else f"[ERROR] {result.stderr.strip()}"
    except FileNotFoundError:
        return "[ERROR] copilot CLI not found"
    except subprocess.TimeoutExpired:
        return "[ERROR] copilot timed out"


def analyze_page(page_data, batch_context=""):
    """Analyze a single page's data and produce a quality rating."""
    errors = page_data.get("katex_errors", [])
    metrics = page_data.get("metrics", {})
    page_name = page_data.get("page", "unknown")

    # Build a structured description for the AI
    error_desc = "None detected" if not errors else "\n".join(
        f"  - [{e['type']}] {e.get('text', e.get('html', ''))[:120]}"
        for e in errors
    )

    prompt = f"""You are a QA reviewer for a math learning website. Analyze this page report and rate it.

Page: {page_name}
Route: {page_data.get('route', 'N/A')}
Tab: {page_data.get('tab', 'N/A')}

DOM Metrics:
  KaTeX rendered elements: {metrics.get('katex_count', 'N/A')}
  Formula boxes: {metrics.get('formula_boxes', 'N/A')}
  Empty states visible: {metrics.get('empty_states', 'N/A')}
  Error states visible: {metrics.get('error_states', 'N/A')}
  Active loaders: {metrics.get('active_loaders', 'N/A')}
  Body text length: {metrics.get('body_text_length', 'N/A')} chars

KaTeX Errors Detected:
{error_desc}

{batch_context}

Rate this page on a 1-5 scale for:
1. math_rendering: Are formulas displaying correctly? (5=perfect, 1=broken)
2. content_quality: Is the content clear and educational? (5=excellent, 1=confusing/empty)
3. layout: Is the page layout clean? (5=polished, 1=broken)

Reply in EXACTLY this JSON format (nothing else):
{{"math_rendering": N, "content_quality": N, "layout": N, "issues": ["issue1", "issue2"], "fix_priority": "critical|high|medium|low|none"}}"""

    response = call_copilot(prompt)

    # Try to parse JSON from response
    try:
        # Find JSON in the response
        start = response.index("{")
        end = response.rindex("}") + 1
        rating = json.loads(response[start:end])
    except (ValueError, json.JSONDecodeError):
        rating = {
            "math_rendering": 3,
            "content_quality": 3,
            "layout": 3,
            "issues": [f"AI analysis failed: {response[:200]}"],
            "fix_priority": "medium",
            "raw_response": response[:500],
        }

    return {
        "page": page_name,
        "route": page_data.get("route", ""),
        "tab": page_data.get("tab", ""),
        "screenshot": page_data.get("screenshot", ""),
        "dom_errors": len(errors),
        "rating": rating,
    }


def run_analysis(manifest_path=None):
    path = Path(manifest_path) if manifest_path else MANIFEST_PATH
    if not path.exists():
        print(f"❌ Manifest not found at {path}")
        print("   Run crawl.py first: python scripts/visual-qa/crawl.py")
        return None

    manifest = json.loads(path.read_text())
    pages = manifest.get("pages", [])

    print(f"🔬 Analyzing {len(pages)} pages...")
    print(f"   Using GPT-5 mini via Copilot CLI\n")

    analyses = []
    critical_pages = []

    for i, page in enumerate(pages):
        page_name = page.get("page", "unknown")
        errors = page.get("katex_errors", [])
        status = "🔴" if errors else "🟢"
        print(f"  [{i+1}/{len(pages)}] {status} {page_name}", end="", flush=True)

        analysis = analyze_page(page)
        analyses.append(analysis)

        rating = analysis["rating"]
        score = min(rating.get("math_rendering", 5), rating.get("content_quality", 5), rating.get("layout", 5))
        if score <= 2 or rating.get("fix_priority") in ("critical", "high"):
            critical_pages.append(analysis)
            print(f" ⚠️  (score={score}, priority={rating.get('fix_priority', '?')})")
        else:
            print(f" ✓ (score={score})")

    # Build final report data
    report = {
        "analysis_time": manifest.get("crawl_time"),
        "total_pages": len(analyses),
        "critical_count": len(critical_pages),
        "average_math_score": round(sum(a["rating"].get("math_rendering", 3) for a in analyses) / max(len(analyses), 1), 2),
        "average_content_score": round(sum(a["rating"].get("content_quality", 3) for a in analyses) / max(len(analyses), 1), 2),
        "average_layout_score": round(sum(a["rating"].get("layout", 3) for a in analyses) / max(len(analyses), 1), 2),
        "critical_pages": critical_pages,
        "all_pages": analyses,
    }

    report_path = OUTPUT_DIR / "analysis.json"
    report_path.write_text(json.dumps(report, indent=2))

    print(f"\n{'='*60}")
    print(f"✅ Analysis complete")
    print(f"   Total pages:     {len(analyses)}")
    print(f"   Critical issues: {len(critical_pages)}")
    print(f"   Avg math score:  {report['average_math_score']}/5")
    print(f"   Avg content:     {report['average_content_score']}/5")
    print(f"   Avg layout:      {report['average_layout_score']}/5")
    print(f"   Report:          {report_path}")
    print(f"{'='*60}")

    if critical_pages:
        print(f"\n🚨 Critical pages requiring attention:")
        for cp in critical_pages:
            issues = cp["rating"].get("issues", [])
            print(f"   {cp['page']}: {', '.join(issues[:3])}")

    return report


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else None
    run_analysis(path)
