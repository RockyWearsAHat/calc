#!/usr/bin/env python3
"""
Visual QA Crawler — Navigates every page/state of the Calc Mastery site,
takes screenshots, and detects KaTeX rendering errors via DOM inspection.

Outputs:
  qa-output/screenshots/  — PNG screenshots of every view
  qa-output/crawl.json    — Structured manifest of all findings

Usage:
  python scripts/visual-qa/crawl.py [--base-url http://localhost:5173]
"""

import asyncio
import json
import sys
import time
from pathlib import Path
from datetime import datetime

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("ERROR: playwright not installed. Run: pip install playwright && playwright install chromium")
    sys.exit(1)

BASE_URL = "http://localhost:5173"
OUTPUT_DIR = Path(__file__).resolve().parent.parent.parent / "qa-output"
SCREENSHOT_DIR = OUTPUT_DIR / "screenshots"
TIMEOUT = 30_000  # 30s page load timeout
TOPIC_TIMEOUT = 60_000  # 60s for topic pages (may generate lessons)


async def wait_for_katex(page, timeout=5000):
    """Wait for KaTeX to finish rendering (look for .katex elements)."""
    try:
        await page.wait_for_selector(".katex", timeout=timeout)
    except Exception:
        pass  # Page may not have math
    # Extra settle time for complex renders
    await page.wait_for_timeout(500)


async def detect_katex_errors(page):
    """Inspect the DOM for KaTeX rendering failures."""
    js_code = (
        "() => {"
        "  const issues = [];"
        "  document.querySelectorAll('.katex-error').forEach((el, i) => {"
        "    issues.push({type:'katex-error-class', text:el.textContent.substring(0,200), title:el.getAttribute('title')||'', index:i});"
        "  });"
        "  document.querySelectorAll('.katex .mord').forEach((el, i) => {"
        "    const color = window.getComputedStyle(el).color;"
        "    if (color==='rgb(204, 0, 0)'||color==='rgb(255, 0, 0)') {"
        "      issues.push({type:'red-math-text', text:el.textContent.substring(0,200), index:i});"
        "    }"
        "  });"
        "  document.querySelectorAll('.katex').forEach((el, i) => {"
        "    if (el.textContent.trim()==='' && el.innerHTML.trim()!=='') {"
        "      issues.push({type:'empty-katex', html:el.innerHTML.substring(0,200), index:i});"
        "    }"
        "  });"
        "  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null);"
        "  let node, textIdx = 0;"
        "  const latexRe = /\\\\(frac|sqrt|int|sum|cdot|left|right|ln|log|sin|cos|text|begin|end)\\b/;"
        "  const dollarRe = /\\$[^$]+\\$/;"
        "  while ((node = walker.nextNode())) {"
        "    const t = node.textContent;"
        "    const parent = node.parentElement;"
        "    if (!parent || ['SCRIPT','STYLE','CODE','PRE','TEXTAREA'].includes(parent.tagName)) continue;"
        "    if (parent.closest('.katex')) continue;"
        "    if (latexRe.test(t)) {"
        "      issues.push({type:'leaked-latex-command', text:t.substring(0,300), parentTag:parent.tagName, index:textIdx});"
        "    }"
        "    if (dollarRe.test(t)) {"
        "      issues.push({type:'leaked-dollar-delimiters', text:t.substring(0,300), parentTag:parent.tagName, index:textIdx});"
        "    }"
        "    textIdx++;"
        "  }"
        "  return issues;"
        "}"
    )
    errors = await page.evaluate(js_code)
    return errors


async def get_page_metrics(page):
    """Collect basic page health metrics."""
    return await page.evaluate("""() => {
        const katexEls = document.querySelectorAll('.katex');
        const mathMdEls = document.querySelectorAll('[class*="MathMarkdown"], [class*="mathmarkdown"]');
        const formulaBoxes = document.querySelectorAll('[class*="formulaBox"], [class*="formula-box"], [class*="FormulaBox"]');
        const emptyStates = document.querySelectorAll('[class*="emptyState"], [class*="empty-state"]');
        const errorStates = document.querySelectorAll('[class*="errorState"], [class*="error-state"]');
        const loaders = document.querySelectorAll('[class*="spin"], [class*="loader"], [class*="Loader"]');

        return {
            katex_count: katexEls.length,
            formula_boxes: formulaBoxes.length,
            empty_states: emptyStates.length,
            error_states: errorStates.length,
            active_loaders: loaders.length,
            body_text_length: document.body.innerText.length,
            title: document.title,
        };
    }""")


async def screenshot(page, name, full_page=True):
    """Take a screenshot and return the file path."""
    path = SCREENSHOT_DIR / f"{name}.png"
    await page.screenshot(path=str(path), full_page=full_page)
    return str(path.relative_to(OUTPUT_DIR))


async def crawl_static_pages(page, results):
    """Crawl pages that don't require dynamic topic selection."""
    static_routes = [
        ("/", "dashboard"),
        ("/formulas", "formulas"),
        ("/course", "course"),
        ("/settings", "settings"),
    ]

    for route, name in static_routes:
        print(f"  📸 {name} ({route})")
        await page.goto(f"{BASE_URL}{route}", wait_until="networkidle", timeout=TIMEOUT)
        await wait_for_katex(page)
        
        ss = await screenshot(page, name)
        errors = await detect_katex_errors(page)
        metrics = await get_page_metrics(page)

        results.append({
            "page": name,
            "route": route,
            "screenshot": ss,
            "katex_errors": errors,
            "metrics": metrics,
            "timestamp": datetime.now().isoformat(),
        })


async def crawl_learn_topics(page, results):
    """Crawl the Learn page for each topic — concepts, formulas, examples, practice."""
    print("  📚 Loading topic list...")

    # Read topic IDs directly from curriculum JSON (most reliable)
    curriculum_path = Path(__file__).resolve().parent.parent.parent / "backend" / "data" / "personalized_curriculum.json"
    topic_ids = []
    if curriculum_path.exists():
        import json as _json
        data = _json.loads(curriculum_path.read_text())
        topic_ids = [t["id"] for t in data.get("topics", [])]

    if not topic_ids:
        # Fallback: try the API via browser
        print("    ⚠️  No curriculum file — trying API")
        await page.goto(f"{BASE_URL}/learn", wait_until="domcontentloaded", timeout=TIMEOUT)
        await page.wait_for_timeout(2000)
        try:
            topic_ids = await page.evaluate("""async () => {
                const r = await fetch('/api/curriculum/topics');
                const data = await r.json();
                return (data.topics || []).map(t => t.id);
            }""")
        except Exception:
            pass

    print(f"    Found {len(topic_ids)} topics")

    for tid in topic_ids:
        topic_name = str(tid).replace(".", "_")
        print(f"  📖 Topic {tid}", end="", flush=True)

        try:
            # Navigate to the topic
            await page.goto(f"{BASE_URL}/learn/{tid}", wait_until="domcontentloaded", timeout=TOPIC_TIMEOUT)

            # Wait for actual content (not just "Loading your curriculum...")
            try:
                await page.wait_for_selector(
                    'h1:not(:has-text("Loading")), [class*="generatingLesson"], [class*="Generation Failed"]',
                    timeout=20_000
                )
            except Exception:
                pass
            await page.wait_for_timeout(1500)

            # Check if still generating
            generating = await page.query_selector('[class*="generatingLesson"]')
            if generating:
                print(f" ⏳ generating...", end="", flush=True)
                try:
                    await page.wait_for_selector('[class*="generatingLesson"]', state="hidden", timeout=120_000)
                except Exception:
                    ss = await screenshot(page, f"learn_{topic_name}_generating")
                    results.append({
                        "page": f"learn/{tid}",
                        "route": f"/learn/{tid}",
                        "screenshot": ss,
                        "katex_errors": [],
                        "metrics": {"status": "still_generating"},
                        "timestamp": datetime.now().isoformat(),
                    })
                    print(" (timed out)")
                    continue

            await wait_for_katex(page)

            # --- Learn tab: screenshot the key formula + each concept ---
            ss = await screenshot(page, f"learn_{topic_name}_overview")
            errors = await detect_katex_errors(page)
            metrics = await get_page_metrics(page)

            results.append({
                "page": f"learn/{tid}",
                "tab": "learn",
                "route": f"/learn/{tid}",
                "screenshot": ss,
                "katex_errors": errors,
                "metrics": metrics,
                "timestamp": datetime.now().isoformat(),
            })

            # Count concepts
            concept_count = await page.evaluate("""() => {
                const dots = document.querySelectorAll('[class*="dot"]');
                return dots.length;
            }""")

            # Navigate through each concept
            for ci in range(min(concept_count, 10)):
                if ci > 0:
                    next_btn = await page.query_selector('button:has-text("Next Concept")')
                    if next_btn:
                        await next_btn.click()
                        await page.wait_for_timeout(800)
                        await wait_for_katex(page)

                ss = await screenshot(page, f"learn_{topic_name}_concept_{ci}")
                errors = await detect_katex_errors(page)

                results.append({
                    "page": f"learn/{tid}/concept/{ci}",
                    "tab": "learn",
                    "concept_index": ci,
                    "screenshot": ss,
                    "katex_errors": errors,
                    "metrics": await get_page_metrics(page),
                    "timestamp": datetime.now().isoformat(),
                })

            # --- Practice tab ---
            practice_btn = await page.query_selector('button:has-text("Practice")')
            if practice_btn:
                await practice_btn.click()
                await page.wait_for_timeout(1000)
                await wait_for_katex(page)

                ss = await screenshot(page, f"learn_{topic_name}_practice")
                errors = await detect_katex_errors(page)

                results.append({
                    "page": f"learn/{tid}/practice",
                    "tab": "practice",
                    "screenshot": ss,
                    "katex_errors": errors,
                    "metrics": await get_page_metrics(page),
                    "timestamp": datetime.now().isoformat(),
                })

                # Open walkthrough if available
                wt_btn = await page.query_selector('button:has-text("Show Walkthrough")')
                if wt_btn:
                    await wt_btn.click()
                    await page.wait_for_timeout(800)
                    await wait_for_katex(page)

                    ss = await screenshot(page, f"learn_{topic_name}_walkthrough")
                    errors = await detect_katex_errors(page)
                    results.append({
                        "page": f"learn/{tid}/walkthrough",
                        "tab": "practice",
                        "screenshot": ss,
                        "katex_errors": errors,
                        "metrics": await get_page_metrics(page),
                        "timestamp": datetime.now().isoformat(),
                    })

            err_count = sum(len(r.get("katex_errors", [])) for r in results if r.get("page", "").startswith(f"learn/{tid}"))
            print(f" ✓ ({err_count} errors)" if err_count else " ✓")

        except Exception as e:
            print(f" ❌ {type(e).__name__}: {str(e)[:80]}")
            try:
                ss = await screenshot(page, f"learn_{topic_name}_error")
                results.append({
                    "page": f"learn/{tid}",
                    "route": f"/learn/{tid}",
                    "screenshot": ss,
                    "katex_errors": [],
                    "metrics": {"status": "error", "error": str(e)[:200]},
                    "timestamp": datetime.now().isoformat(),
                })
            except Exception:
                pass


async def crawl_practice_page(page, results):
    """Crawl the standalone Practice page."""
    print("  🎯 Practice page")
    await page.goto(f"{BASE_URL}/practice", wait_until="networkidle", timeout=TIMEOUT)
    await page.wait_for_timeout(2000)
    await wait_for_katex(page)

    ss = await screenshot(page, "practice_main")
    errors = await detect_katex_errors(page)
    metrics = await get_page_metrics(page)

    results.append({
        "page": "practice",
        "route": "/practice",
        "screenshot": ss,
        "katex_errors": errors,
        "metrics": metrics,
        "timestamp": datetime.now().isoformat(),
    })


async def run_crawl(base_url=None):
    global BASE_URL
    if base_url:
        BASE_URL = base_url

    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

    results = []
    console_errors = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1440, "height": 900},
            device_scale_factor=2,  # Retina screenshots
        )
        page = await context.new_page()

        # Capture console errors
        page.on("console", lambda msg: (
            console_errors.append({
                "type": msg.type,
                "text": msg.text,
                "url": page.url,
            }) if msg.type == "error" else None
        ))

        print("🔍 Visual QA Crawler starting...")
        print(f"   Base URL: {BASE_URL}")
        print(f"   Output:   {OUTPUT_DIR}\n")

        # Check site is reachable
        try:
            resp = await page.goto(BASE_URL, timeout=10_000)
            if not resp or resp.status >= 400:
                print(f"❌ Site returned HTTP {resp.status if resp else 'no response'}. Is the dev server running?")
                print(f"   Start it with: cd {Path(__file__).resolve().parent.parent.parent} && npm run dev")
                await browser.close()
                return None
        except Exception as e:
            print(f"❌ Cannot reach {BASE_URL}: {e}")
            print(f"   Start the dev server: cd {Path(__file__).resolve().parent.parent.parent} && npm run dev")
            await browser.close()
            return None

        start = time.time()

        await crawl_static_pages(page, results)
        await crawl_learn_topics(page, results)
        await crawl_practice_page(page, results)

        elapsed = time.time() - start
        await browser.close()

    # Build summary
    total_errors = sum(len(r.get("katex_errors", [])) for r in results)
    pages_with_errors = sum(1 for r in results if r.get("katex_errors"))

    manifest = {
        "crawl_time": datetime.now().isoformat(),
        "elapsed_seconds": round(elapsed, 1),
        "base_url": BASE_URL,
        "total_pages": len(results),
        "total_katex_errors": total_errors,
        "pages_with_errors": pages_with_errors,
        "console_errors": console_errors[:50],
        "pages": results,
    }

    manifest_path = OUTPUT_DIR / "crawl.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))

    print(f"\n{'='*60}")
    print(f"✅ Crawl complete in {elapsed:.1f}s")
    print(f"   Pages screenshotted: {len(results)}")
    print(f"   KaTeX errors found:  {total_errors} across {pages_with_errors} pages")
    print(f"   Console errors:      {len(console_errors)}")
    print(f"   Manifest:            {manifest_path}")
    print(f"   Screenshots:         {SCREENSHOT_DIR}")
    print(f"{'='*60}")

    if total_errors > 0:
        print(f"\n⚠️  Pages with KaTeX issues:")
        for r in results:
            errs = r.get("katex_errors", [])
            if errs:
                print(f"   {r['page']}: {len(errs)} error(s)")
                for e in errs[:3]:
                    print(f"      - [{e['type']}] {e.get('text', e.get('html', ''))[:80]}")

    return manifest


if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1].startswith("http") else None
    asyncio.run(run_crawl(url))
