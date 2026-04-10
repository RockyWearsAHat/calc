#!/usr/bin/env python3
"""
Canvas course scraper + AI curriculum generator.
Uses Playwright with the user's existing Chrome profile (no login needed if already signed in).
Calls Copilot CLI with gpt-5-mini (FREE) to process raw data into structured curriculum JSON.

Usage:
  python3 canvas_scraper.py           - full pipeline: scrape + process
  python3 canvas_scraper.py --scrape  - scrape only (write raw JSON)
  python3 canvas_scraper.py --process - process raw JSON into curriculum
"""

import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

CANVAS_BASE = "https://utah.instructure.com"
COURSE_ID = "1220325"
CHROME_PROFILE = os.path.expanduser("~/Library/Application Support/Google/Chrome")

DATA_DIR = Path(__file__).parent / "data"
RAW_FILE = DATA_DIR / "canvas_raw_scrape.json"
CURRICULUM_FILE = DATA_DIR / "personalized_curriculum.json"
STATUS_FILE = DATA_DIR / "scrape_status.json"

DATA_DIR.mkdir(parents=True, exist_ok=True)


def _set_status(stage: str, pct: int, msg: str, error: str = ""):
    STATUS_FILE.write_text(json.dumps({
        "stage": stage, "percent": pct, "message": msg,
        "error": error, "updated_at": datetime.now().isoformat()
    }))


def _full_url(href: str) -> str:
    if not href:
        return ""
    return href if href.startswith("http") else CANVAS_BASE + href


def _wait_for_login_if_needed(page):
    """If we landed on a login page, wait up to 90s for the user to sign in."""
    if "login" in page.url or "cas.utah.edu" in page.url:
        print("\n  Login page detected. Please sign in to Canvas in the browser window.")
        print("  The scraper will continue automatically once you are logged in.\n")
        for _ in range(90):
            time.sleep(1)
            if "login" not in page.url and "cas.utah.edu" not in page.url:
                print("  Logged in! Continuing...\n")
                break
        else:
            raise TimeoutError("Timed out waiting for Canvas login (90s)")


def scrape_canvas() -> dict:
    """Launch Chrome with existing profile and scrape the entire course."""
    from playwright.sync_api import sync_playwright

    print("  Opening Chrome with your existing profile...")
    print("  If you see a login page, log in and the scraper will wait.\n")

    raw = {
        "scraped_at": datetime.now().isoformat(),
        "course_id": COURSE_ID,
        "modules": [],
        "assignments": [],
        "quizzes": [],
    }

    with sync_playwright() as pw:
        ctx = pw.chromium.launch_persistent_context(
            user_data_dir=CHROME_PROFILE,
            headless=False,
            channel="chrome",
            slow_mo=80,
        )
        page = ctx.new_page()
        page.set_default_timeout(15000)

        print("  Scraping modules...")
        page.goto(f"{CANVAS_BASE}/courses/{COURSE_ID}/modules", wait_until="networkidle")
        _wait_for_login_if_needed(page)

        modules = page.query_selector_all(".context_module")
        for mod in modules:
            name_el = mod.query_selector(".ig-header-title, .name")
            name = name_el.inner_text().strip() if name_el else "Unknown Module"
            items = []
            for item in mod.query_selector_all(".context_module_item"):
                t = item.query_selector(".item_name a, .title")
                a = item.query_selector("a[href]")
                items.append({
                    "title": t.inner_text().strip() if t else "",
                    "url": _full_url(a.get_attribute("href", "")) if a else "",
                })
            raw["modules"].append({"name": name, "items": items})
            print(f"    Module: {name} ({len(items)} items)")

        print("  Scraping assignments...")
        page.goto(f"{CANVAS_BASE}/courses/{COURSE_ID}/assignments", wait_until="networkidle")
        _wait_for_login_if_needed(page)

        for row in page.query_selector_all(".assignment"):
            title_el = row.query_selector(".ig-title a, .title a")
            due_el = row.query_selector(".assignment-date-due")
            a_el = row.query_selector("a[href]")
            if title_el:
                raw["assignments"].append({
                    "title": title_el.inner_text().strip(),
                    "due": due_el.inner_text().strip() if due_el else "",
                    "url": _full_url(a_el.get_attribute("href", "")) if a_el else "",
                })

        print(f"    Found {len(raw['assignments'])} assignments")

        print("  Scraping quizzes...")
        page.goto(f"{CANVAS_BASE}/courses/{COURSE_ID}/quizzes", wait_until="networkidle")

        for row in page.query_selector_all(".quiz"):
            title_el = row.query_selector(".ig-title a, .title a")
            a_el = row.query_selector("a[href]")
            if title_el:
                raw["quizzes"].append({
                    "title": title_el.inner_text().strip(),
                    "url": _full_url(a_el.get_attribute("href", "")) if a_el else "",
                })

        print(f"    Found {len(raw['quizzes'])} quizzes")
        ctx.close()

    return raw


def _call_copilot(prompt: str, model: str = "gpt-5-mini") -> str:
    """Call Copilot CLI synchronously. Returns text response."""
    result = subprocess.run(
        ["copilot", "-p", prompt, "--model", model, "-s"],
        capture_output=True, text=True, timeout=120
    )
    return result.stdout.strip()


def _default_topics() -> list:
    """Comprehensive Calc 1 to Calc 2 topic list in teaching order."""
    return [
        {"id": "1.1", "title": "Functions and Their Graphs", "calc": 1, "order": 1},
        {"id": "1.2", "title": "Combining and Transforming Functions", "calc": 1, "order": 2},
        {"id": "1.3", "title": "Trigonometric Functions Review", "calc": 1, "order": 3},
        {"id": "2.1", "title": "The Tangent Problem and The Idea of a Limit", "calc": 1, "order": 4},
        {"id": "2.2", "title": "The Limit of a Function", "calc": 1, "order": 5},
        {"id": "2.3", "title": "Calculating Limits Using the Limit Laws", "calc": 1, "order": 6},
        {"id": "2.4", "title": "Continuity", "calc": 1, "order": 7},
        {"id": "2.5", "title": "Limits at Infinity and Horizontal Asymptotes", "calc": 1, "order": 8},
        {"id": "2.6", "title": "Derivatives and Rates of Change", "calc": 1, "order": 9},
        {"id": "2.7", "title": "The Derivative as a Function", "calc": 1, "order": 10},
        {"id": "3.1", "title": "Derivatives of Polynomials and Exponential Functions", "calc": 1, "order": 11},
        {"id": "3.2", "title": "The Product and Quotient Rules", "calc": 1, "order": 12},
        {"id": "3.3", "title": "Derivatives of Trig Functions", "calc": 1, "order": 13},
        {"id": "3.4", "title": "The Chain Rule", "calc": 1, "order": 14},
        {"id": "3.5", "title": "Implicit Differentiation", "calc": 1, "order": 15},
        {"id": "3.6", "title": "Derivatives of Logarithmic Functions", "calc": 1, "order": 16},
        {"id": "3.9", "title": "Related Rates", "calc": 1, "order": 17},
        {"id": "3.10", "title": "Linear Approximations and Differentials", "calc": 1, "order": 18},
        {"id": "4.1", "title": "Maximum and Minimum Values", "calc": 1, "order": 19},
        {"id": "4.2", "title": "The Mean Value Theorem", "calc": 1, "order": 20},
        {"id": "4.3", "title": "How Derivatives Affect the Shape of a Graph", "calc": 1, "order": 21},
        {"id": "4.4", "title": "Indeterminate Forms and L Hopital Rule", "calc": 1, "order": 22},
        {"id": "4.5", "title": "Summary of Curve Sketching", "calc": 1, "order": 23},
        {"id": "4.7", "title": "Optimization Problems", "calc": 1, "order": 24},
        {"id": "4.9", "title": "Antiderivatives", "calc": 1, "order": 25},
        {"id": "5.1", "title": "Areas and Distances - The Definite Integral Idea", "calc": 1, "order": 26},
        {"id": "5.2", "title": "The Definite Integral", "calc": 1, "order": 27},
        {"id": "5.3", "title": "The Fundamental Theorem of Calculus", "calc": 1, "order": 28},
        {"id": "5.4", "title": "Indefinite Integrals and the Net Change Theorem", "calc": 1, "order": 29},
        {"id": "5.5", "title": "The Substitution Rule (u-substitution)", "calc": 1, "order": 30},
        {"id": "6.1", "title": "Areas Between Curves", "calc": 2, "order": 31},
        {"id": "6.2", "title": "Volumes by Cross-Sections - Disk and Washer Method", "calc": 2, "order": 32},
        {"id": "6.3", "title": "Volumes by Cylindrical Shells", "calc": 2, "order": 33},
        {"id": "6.4", "title": "Work", "calc": 2, "order": 34},
        {"id": "6.5", "title": "Average Value of a Function", "calc": 2, "order": 35},
        {"id": "7.1", "title": "Integration by Parts", "calc": 2, "order": 36},
        {"id": "7.2", "title": "Trigonometric Integrals", "calc": 2, "order": 37},
        {"id": "7.3", "title": "Trigonometric Substitution", "calc": 2, "order": 38},
        {"id": "7.4", "title": "Integration of Rational Functions by Partial Fractions", "calc": 2, "order": 39},
        {"id": "7.5", "title": "Strategy for Integration", "calc": 2, "order": 40},
        {"id": "7.7", "title": "Approximate Integration - Trapezoidal and Simpsons Rule", "calc": 2, "order": 41},
        {"id": "7.8", "title": "Improper Integrals", "calc": 2, "order": 42},
        {"id": "8.1", "title": "Arc Length", "calc": 2, "order": 43},
        {"id": "8.2", "title": "Surface Area of Revolution", "calc": 2, "order": 44},
        {"id": "9.1", "title": "Modeling with Differential Equations", "calc": 2, "order": 45},
        {"id": "9.3", "title": "Separable Differential Equations", "calc": 2, "order": 46},
        {"id": "9.5", "title": "Linear Equations and the Integrating Factor", "calc": 2, "order": 47},
        {"id": "10.1", "title": "Curves Defined by Parametric Equations", "calc": 2, "order": 48},
        {"id": "10.2", "title": "Calculus with Parametric Curves", "calc": 2, "order": 49},
        {"id": "10.3", "title": "Polar Coordinates", "calc": 2, "order": 50},
        {"id": "10.4", "title": "Areas and Lengths in Polar Coordinates", "calc": 2, "order": 51},
        {"id": "11.1", "title": "Sequences", "calc": 2, "order": 52},
        {"id": "11.2", "title": "Series", "calc": 2, "order": 53},
        {"id": "11.3", "title": "The Integral Test and Estimates of Sums", "calc": 2, "order": 54},
        {"id": "11.4", "title": "The Comparison Tests", "calc": 2, "order": 55},
        {"id": "11.5", "title": "Alternating Series and Absolute Convergence", "calc": 2, "order": 56},
        {"id": "11.6", "title": "The Ratio and Root Tests", "calc": 2, "order": 57},
        {"id": "11.7", "title": "Strategy for Testing Series", "calc": 2, "order": 58},
        {"id": "11.8", "title": "Power Series", "calc": 2, "order": 59},
        {"id": "11.9", "title": "Representations of Functions as Power Series", "calc": 2, "order": 60},
        {"id": "11.10", "title": "Taylor and Maclaurin Series", "calc": 2, "order": 61},
    ]


def _generate_lesson(topic: dict) -> dict:
    """Generate a full lesson + practice problems using gpt-5-mini."""
    prompt = (
        "You are teaching a calculus student who ONLY knows high school algebra and basic trig. "
        "They have NEVER seen calculus before. You are their personal patient tutor.\n\n"
        "Generate a complete lesson for: " + topic["id"] + " - " + topic["title"] + "\n\n"
        "TEACHING RULES:\n"
        "1. Start with a real-world motivation — WHY does this topic exist? What problem does it solve? Use a concrete scenario.\n"
        "2. Build from ZERO — assume the student never heard of this concept. Introduce every new symbol and notation before using it.\n"
        "3. Each concept explanation should be 4-6 sentences minimum. Don't just state what something is — explain WHY it works that way.\n"
        "4. For each formula, explain every piece: what does each letter mean? Where does it come from? Why is it shaped like that?\n"
        "5. The worked example MUST show every single step — including the calculator steps. Don't skip from 'take ln' to 'x = 5.03'. Show the actual numbers.\n"
        "6. Use everyday analogies (e.g., logarithms are like asking 'how many times did I multiply?', derivatives are like speedometers).\n"
        "7. End each concept with a 'check yourself' moment — a simple question the student should be able to answer if they understood.\n\n"
        "Return STRICT JSON with no markdown code fences. Structure:\n"
        "{\n"
        '  "description": "2-3 sentence plain English description that motivates WHY this topic matters",\n'
        '  "key_formula": "the single most important formula in LaTeX",\n'
        '  "concepts": [{"title":"...","explanation":"4-6 sentence explanation with intuition and analogies","formula":"LaTeX formula with EVERY variable explained","example":"Fully worked example showing EVERY step including calculator values"}],\n'
        '  "practice_problems": [{"question":"...","answer":"...","difficulty":"easy|medium|hard","walkthrough":[{"step":1,"title":"...","content":"detailed explanation of this step including WHY","formula":"..."}]}]\n'
        "}\n\n"
        "Include 4 concepts (building from simplest to most complex) and 3 practice problems (easy, medium, hard). "
        "Each problem needs at least 4 walkthrough steps. RETURN ONLY RAW JSON."
    )

    raw = _call_copilot(prompt)

    # Strip markdown fences if model added them
    if "```" in raw:
        parts = raw.split("```")
        for part in parts:
            part = part.strip()
            if part.startswith("{") or part.startswith("json\n{"):
                raw = part.lstrip("json").strip()
                break

    try:
        return json.loads(raw)
    except Exception as e:
        print(f"    Warning: JSON parse failed for {topic['id']}: {e}")
        return {
            "description": f"Introduction to {topic['title']}.",
            "key_formula": "",
            "concepts": [{"title": topic["title"], "explanation": "This lesson will be generated when you study this topic.", "formula": "", "example": ""}],
            "practice_problems": [],
        }


def run_full_pipeline():
    _set_status("starting", 0, "Initializing...")
    print("\n=== Calculus Mastery Platform - Canvas Scraper ===\n")

    _set_status("scraping", 5, "Launching Chrome and scraping Canvas...")
    print("Step 1: Scraping Canvas course data")
    try:
        raw = scrape_canvas()
    except Exception as e:
        print(f"  Scrape failed ({e}), using default curriculum")
        raw = {"scraped_at": datetime.now().isoformat(), "modules": [], "assignments": [], "quizzes": []}

    RAW_FILE.write_text(json.dumps(raw, indent=2))
    print(f"  Saved raw data to {RAW_FILE}\n")

    run_process_pipeline(raw)


def run_process_pipeline(raw: dict = None):
    if raw is None:
        raw = json.loads(RAW_FILE.read_text()) if RAW_FILE.exists() else {"modules": [], "assignments": [], "quizzes": []}

    _set_status("processing", 20, "Building topic list...")
    print("Step 2: Generating personalized curriculum")

    topics = _default_topics()
    print(f"  Using {len(topics)} comprehensive Calc 1+2 topics\n")

    curriculum = {
        "course": "MATH 1220 - Calculus II (University of Utah)",
        "generated_at": datetime.now().isoformat(),
        "total_topics": len(topics),
        "canvas_data": {
            "modules": len(raw.get("modules", [])),
            "assignments": len(raw.get("assignments", [])),
            "quizzes": len(raw.get("quizzes", [])),
        },
        "topics": [],
    }

    for i, topic in enumerate(topics):
        pct = 20 + int(75 * i / len(topics))
        _set_status("generating", pct, f"Generating: {topic['id']} - {topic['title']}")
        print(f"  [{i+1:2d}/{len(topics)}] {topic['id']} - {topic['title']}")

        lesson = _generate_lesson(topic)

        curriculum["topics"].append({
            "id": topic["id"],
            "title": topic["title"],
            "calc_level": topic["calc"],
            "order": topic["order"],
            "description": lesson.get("description", ""),
            "key_formula": lesson.get("key_formula", ""),
            "concepts": lesson.get("concepts", []),
            "practice_problems": lesson.get("practice_problems", []),
        })

    CURRICULUM_FILE.write_text(json.dumps(curriculum, indent=2))
    _set_status("done", 100, f"Done! {len(topics)} topics generated.")
    print(f"\n  Curriculum saved to {CURRICULUM_FILE}")
    print(f"  {len(topics)} topics with lessons and practice problems")


if __name__ == "__main__":
    if "--scrape" in sys.argv:
        _set_status("scraping", 5, "Scraping Canvas...")
        raw = scrape_canvas()
        RAW_FILE.write_text(json.dumps(raw, indent=2))
        print(f"Saved to {RAW_FILE}")
    elif "--process" in sys.argv:
        run_process_pipeline()
    else:
        run_full_pipeline()
