---
description: "Run a full visual QA audit of the Calculus Mastery site. Crawls every page, screenshots it, detects broken KaTeX/LaTeX, rates quality via AI, and generates an HTML report with findings. Use this to find and fix rendering issues across the entire site."
mode: "agent"
tools: ["bash", "analyze_images", "view", "edit", "grep", "glob"]
---

# Visual QA — Full Site Audit

You are running a visual quality audit of the Calculus Mastery web app. Your job is to crawl every page, visually inspect the output, identify broken math rendering and layout issues, and fix them.

## What You Have

The project has a Playwright-based visual QA pipeline in `scripts/visual-qa/`:

| Script | Purpose |
|--------|---------|
| `crawl.py` | Navigate every route, take screenshots, detect KaTeX DOM errors |
| `analyze.py` | Send page data through GPT-5 mini for content quality ratings |
| `report.py` | Generate an HTML report with screenshots + ratings + issues |
| `run.py` | Master orchestrator — runs all three in sequence |

Output goes to `qa-output/` with screenshots in `qa-output/screenshots/`.

## The Workflow

### Phase 1: Crawl

```bash
cd /Users/alexwaldmann/Desktop/Calc
python3 scripts/visual-qa/crawl.py http://localhost:2000
```

This produces `qa-output/crawl.json` with every page's:
- Screenshot path
- KaTeX DOM errors (`.katex-error` elements, leaked LaTeX commands, empty renders)
- Page metrics (KaTeX count, empty states, body text length)

### Phase 2: Visual Review

After crawling, **visually inspect the screenshots yourself** using `analyze_images`. Prioritize:

1. Pages flagged with KaTeX DOM errors in `crawl.json`
2. Pages with math content (Learn concepts, Practice problems, Formulas)
3. A representative sample of clean pages for spot-checking

For each screenshot, evaluate:
- **Math rendering**: Are all formulas displaying as proper typeset math? No raw `\frac`, `\sqrt`, dollar signs, or red error text?
- **Content quality**: Is the explanation clear, complete, educational?
- **Layout**: Clean spacing, nothing overlapping, responsive?

Rate each on a 1–5 scale. Log issues found.

### Phase 3: AI Analysis

```bash
python3 scripts/visual-qa/analyze.py
```

Uses GPT-5 mini (free via Copilot CLI) to rate each page based on DOM metrics. Produces `qa-output/analysis.json`.

### Phase 4: Report

```bash
python3 scripts/visual-qa/report.py
open qa-output/report.html
```

Generates a visual HTML report with all screenshots, ratings, and issues side-by-side.

### Phase 5: Fix

For each issue found:
1. Identify the source — is it in the LaTeX content (`personalized_curriculum.json`), the preprocessing (`src/utils/latex.js`), or the rendering components?
2. Fix the root cause
3. Re-crawl the affected page to verify the fix
4. Re-screenshot and visually confirm

## Key Files for Fixes

| Issue Type | Fix Location |
|-----------|-------------|
| Broken LaTeX in lesson content | `backend/data/personalized_curriculum.json` |
| LaTeX preprocessing bugs | `src/utils/latex.js` |
| KaTeX rendering component issues | `src/components/MathMarkdown.jsx` |
| Formula display issues | `src/components/Math.jsx` |
| Lesson generation quality | `backend/canvas_scraper.py` (`_generate_lesson`) |
| AI tutor response formatting | `backend/smart_ai_tutor.py` |

## KaTeX Error Types

| DOM Signal | Meaning |
|-----------|---------|
| `.katex-error` class | KaTeX parser failed — check the LaTeX syntax |
| Red text in `.katex .mord` | Parse error rendered inline |
| Empty `.katex` container | Render produced nothing — likely empty/malformed input |
| Raw `\frac`, `\sqrt` in text | LaTeX commands not wrapped in math delimiters |
| Raw `$...$` in text | Dollar delimiters not processed by remark-math |

## Important Context

- Frontend runs on `http://localhost:2000` (Vite dev server)
- Backend runs on `http://localhost:8000` (FastAPI)
- Math rendering has TWO paths:
  1. `MathMarkdown.jsx` — ReactMarkdown + remark-math + rehype-katex (Learn, Practice, Chat)
  2. `Math.jsx` — react-katex directly (Formulas page)
- `src/utils/latex.js` preprocesses ALL LaTeX before rendering — it auto-detects bare LaTeX, converts `*` to `\cdot`, `/` to `\frac`. This is the most common source of bugs.
- There are ~60 topics in the curriculum, each with 3-4 concepts + practice problems.
