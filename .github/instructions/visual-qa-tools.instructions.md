---
applyTo: "{scripts/visual-qa/**,qa-output/**,src/utils/latex.js,src/components/Math*.jsx,backend/data/personalized_curriculum.json}"
description: "Visual QA tools and workflow for the Calculus Mastery site. Guides agents on how to use the Playwright-based visual QA pipeline, interpret findings, and fix rendering issues."
---

# Visual QA Tools — Usage Guide

## Available Tools

The `scripts/visual-qa/` directory contains a Playwright-based visual QA pipeline:

- **`crawl.py`** — Crawl all routes, screenshot every page, detect KaTeX DOM errors
- **`analyze.py`** — Rate pages via GPT-5 mini (free, uses `copilot` CLI)
- **`report.py`** — Generate HTML report with embedded screenshots
- **`run.py`** — Orchestrate: `python3 scripts/visual-qa/run.py [full|crawl|analyze|report|review]`

Output lives in `qa-output/`. The HTML report is at `qa-output/report.html`.

## Running the Pipeline

```bash
# Full pipeline (crawl → analyze → report)
python3 scripts/visual-qa/run.py full --base-url=http://localhost:2000

# Just crawl (fast — screenshots + DOM checks only)
python3 scripts/visual-qa/run.py crawl --base-url=http://localhost:2000

# Just regenerate the report from existing data
python3 scripts/visual-qa/run.py report
```

## Reading the Output

### crawl.json
```json
{
  "pages": [{
    "page": "learn/1.5",
    "screenshot": "screenshots/learn_1_5_overview.png",
    "katex_errors": [{"type": "katex-error-class", "text": "...", "title": "..."}],
    "metrics": {"katex_count": 12, "empty_states": 0}
  }]
}
```

### analysis.json
```json
{
  "all_pages": [{
    "page": "learn/1.5",
    "rating": {"math_rendering": 4, "content_quality": 3, "layout": 5, "issues": [...], "fix_priority": "medium"}
  }]
}
```

## Visual Inspection Protocol

When visually reviewing screenshots (via `analyze_images` or manually):

1. **Math first**: Every formula should be typeset, not raw LaTeX. Look for:
   - Red error text (KaTeX parse failure)
   - Raw backslash commands (`\frac`, `\sqrt`, `\cdot`) visible as text
   - Dollar signs (`$`, `$$`) visible instead of rendered math
   - Overlapping or clipped math expressions
   - Fractions that render flat instead of stacked

2. **Content second**: Is the explanation actually teaching something?
   - Does it explain WHY, not just WHAT?
   - Are worked examples shown step-by-step?
   - Is the language accessible (not overly formal)?

3. **Layout third**: Does the page look professional?
   - Proper spacing between elements
   - Nothing overlapping or cut off
   - Responsive (no horizontal scroll at 1440px)
   - Dark theme consistent (no white flash, no contrast issues)

## Common Fix Patterns

### Broken LaTeX in curriculum content
**File**: `backend/data/personalized_curriculum.json`
**Pattern**: LaTeX strings with unescaped backslashes in JSON
**Fix**: Ensure all `\` in LaTeX are `\\` in JSON strings

### LaTeX preprocessing misfire
**File**: `src/utils/latex.js`
**Pattern**: The `preprocessLatex()` regex wrongly converts valid text into broken LaTeX
**Fix**: Add exclusion patterns or fix the regex. Be careful — this file affects ALL math rendering.

### Missing math delimiters
**Pattern**: Content has LaTeX but no `$...$` or `$$...$$` wrappers
**Fix**: Either add delimiters in the source content OR ensure `preprocessLatex()` auto-wraps correctly

### KaTeX unsupported command
**Pattern**: `.katex-error` with title like "KaTeX: Unsupported command: \foo"
**Fix**: Replace with KaTeX-supported equivalent (e.g., `\text{}` instead of `\mathrm{}`)

## After Fixing

Always re-verify after a fix:
1. Re-run the crawler on the specific page
2. Visually confirm the screenshot looks correct
3. Check that no NEW errors were introduced in neighboring content
