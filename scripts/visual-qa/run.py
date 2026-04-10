#!/usr/bin/env python3
"""
Visual QA Master Orchestrator — Runs the full crawl → analyze → report pipeline.

Modes:
  full     — Crawl, analyze, and generate report (default)
  crawl    — Only take screenshots and detect DOM errors
  analyze  — Only run AI analysis on existing crawl data
  report   — Only generate HTML report from existing analysis
  review   — Agent-assisted visual review (prints screenshot paths for MCP tools)

Usage:
  python scripts/visual-qa/run.py [full|crawl|analyze|report|review]
  python scripts/visual-qa/run.py full --base-url http://localhost:5173
"""

import asyncio
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent.parent
OUTPUT_DIR = PROJECT_DIR / "qa-output"

sys.path.insert(0, str(SCRIPT_DIR))

from crawl import run_crawl
from analyze import run_analysis
from report import generate_report


def print_review_instructions(manifest_path=None):
    """Print instructions for agent-assisted visual review using MCP tools."""
    path = manifest_path or OUTPUT_DIR / "crawl.json"
    if not path.exists():
        print("❌ No crawl data found. Run crawl first.")
        return

    manifest = json.loads(Path(path).read_text())
    pages = manifest.get("pages", [])

    # Prioritize pages with errors
    errored = [p for p in pages if p.get("katex_errors")]
    clean = [p for p in pages if not p.get("katex_errors")]

    print(f"\n🔍 Agent Visual Review Mode")
    print(f"{'='*60}")
    print(f"Total pages: {len(pages)}")
    print(f"With KaTeX errors: {len(errored)}")
    print(f"Clean: {len(clean)}")
    print(f"\nScreenshot directory: {OUTPUT_DIR / 'screenshots'}")

    if errored:
        print(f"\n🔴 PRIORITY — Pages with DOM errors (review these first):")
        for p in errored:
            ss = OUTPUT_DIR / p["screenshot"]
            print(f"   {p['page']}: {ss}")
            for e in p["katex_errors"][:2]:
                print(f"      └─ [{e['type']}] {e.get('text', '')[:80]}")

    print(f"\n🟢 Clean pages (spot-check a sample):")
    for p in clean[:10]:
        ss = OUTPUT_DIR / p["screenshot"]
        print(f"   {p['page']}: {ss}")

    print(f"\nUse gsh-analyze_images to visually review screenshots.")
    print(f"Use gsh-take_screenshot to capture live state if needed.")


async def main():
    mode = "full"
    base_url = None

    for arg in sys.argv[1:]:
        if arg.startswith("http"):
            base_url = arg
        elif arg.startswith("--base-url="):
            base_url = arg.split("=", 1)[1]
        elif arg in ("full", "crawl", "analyze", "report", "review"):
            mode = arg

    print(f"🚀 Visual QA Pipeline — mode: {mode}")
    print(f"{'='*60}\n")

    if mode in ("full", "crawl"):
        manifest = await run_crawl(base_url)
        if not manifest:
            print("\n❌ Crawl failed. Aborting.")
            sys.exit(1)
        if mode == "crawl":
            return

    if mode in ("full", "analyze"):
        analysis = run_analysis()
        if not analysis:
            print("\n❌ Analysis failed. Aborting.")
            sys.exit(1)
        if mode == "analyze":
            return

    if mode in ("full", "report"):
        generate_report()

    if mode == "review":
        print_review_instructions()

    if mode == "full":
        print(f"\n✨ Full pipeline complete!")
        print(f"   Open report: open {OUTPUT_DIR / 'report.html'}")


if __name__ == "__main__":
    asyncio.run(main())
