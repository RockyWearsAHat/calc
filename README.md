# ∫ Calculus Mastery

**A personal AI-powered calculus tutoring platform built to actually learn the material — not just watch 5 hours of lectures a week and pray.**

After failing two calculus midterms through inefficient study methods and scattered online resources, I built this to centralize everything: pull in all my Canvas course data, have AI distill it into digestible lessons, practice with adaptive problems that scale to my level, and get real-time tutoring powered by GitHub Copilot CLI — all **completely free** with a GitHub Copilot subscription.

This isn't a generic study app. It's built specifically for Calculus I & II (MATH 1210 / 1220) at the University of Utah, pulling directly from my Canvas course, and teaching every concept from integration by parts through Taylor series with step-by-step walkthroughs, progressive hints, and mastery tracking.

---

## What It Does

| Page | Purpose |
|---|---|
| **Dashboard** | At-a-glance view of all topics, progress tracking, and high-priority alerts from the AI study guide |
| **Learn** | Deep conceptual teaching — big-picture intuition, formulas with derivations, worked examples (easy → hard), common mistakes, and connections between topics |
| **Practice** | Adaptive problem sets with a multi-level hint system, full step-by-step walkthroughs, difficulty scaling, and mastery tracking per topic |
| **Formulas** | Quick-reference formula sheet rendered with KaTeX — every formula you need for the final in one place |
| **My Course** | Canvas sync + AI analysis — scrapes your actual course content and generates a personalized study guide with prioritized topics |
| **Settings** | Canvas integration instructions and platform configuration |

## How the AI Tutoring Works

The platform uses **GitHub Copilot CLI** as its AI backend (GPT-5 mini by default — free and unlimited with a Copilot subscription, never exceeding Sonnet 4.6 complexity). The AI tutor:

- **Generates unlimited practice problems** matched to your current skill level
- **Provides personalized explanations** — not canned answers, but real teaching tailored to where you're stuck
- **Walks through solutions step-by-step** — each step explains *what* to do and *why*
- **Analyzes your mistakes** — tracks patterns in wrong answers and targets weak spots
- **Falls back to a comprehensive built-in knowledge base** when Copilot CLI is unavailable (covers all Calc II topics with full explanations)

### Adaptive Learning

The practice system doesn't just quiz you — it teaches:

1. **Diagnostic assessment** identifies your starting strengths and weaknesses
2. **Progressive hints** (3 levels) guide you toward the answer without giving it away
3. **Full walkthroughs** break every problem into numbered steps with explanations
4. **Difficulty scaling** — problems get harder as you master concepts, easier when you struggle
5. **Mastery tracking** per topic so you know exactly where to focus

## Topics Covered (Calc II)

- Integration by Parts (LIATE rule, tabular method)
- Trigonometric Integrals & Substitution
- Partial Fractions
- Improper Integrals (convergence/divergence)
- Arc Length & Surface Area
- Parametric Equations & Calculus
- Polar Coordinates & Calculus
- Sequences & Series (all convergence tests)
- Power Series & Representations
- Taylor & Maclaurin Series

Every topic includes: core concept explanation, key formulas, technique steps, multiple worked examples, common mistakes to avoid, and when to use each technique vs. alternatives.

## Canvas Integration

Since the University of Utah doesn't allow Canvas API tokens, this platform uses **Playwright browser automation** to scrape your actual course content:

- Assignments, modules, and syllabus from Canvas
- Homework problems from MyLab/Pearson
- Exam content from Gradescope
- Any linked external platform content (Cengage, Wiley, McGraw-Hill)

Once scraped, the **AI analyzer** processes everything to:
- Identify which topics are weighted most heavily in your course
- Generate a prioritized study guide (HIGH / MEDIUM / LOW priority topics)
- Match practice problems to your actual exam style

---

## Tech Stack

| Layer | Tech |
|---|---|
| Frontend | React 19, React Router 7, Vite 8, KaTeX (math rendering), Lucide icons |
| Backend | Python FastAPI, Pydantic |
| AI | GitHub Copilot CLI (GPT-5 mini) with built-in fallback knowledge base |
| Scraping | Playwright (headless Chrome), BeautifulSoup |
| Canvas | REST API client + browser-based scraper |

## Quick Start

### Prerequisites

- Node.js 18+
- Python 3.10+
- [GitHub Copilot CLI](https://docs.github.com/en/copilot/github-copilot-in-the-cli) installed and authenticated
- Chrome browser (for Canvas scraping)

### 1. Install & run the frontend

```bash
npm install
npm run dev
```

Frontend starts at **http://localhost:2000**

### 2. Set up & run the backend

```bash
python -m venv venv
source venv/bin/activate
pip install fastapi uvicorn aiohttp beautifulsoup4 python-dotenv pydantic playwright
playwright install chromium

cd backend
uvicorn server:app --reload --port 8000
```

Backend API runs at **http://localhost:8000**

### 3. (Optional) Sync your Canvas course

```bash
cd backend
source ../venv/bin/activate
python comprehensive_scraper.py
```

Chrome opens → log in to Canvas → the scraper pulls everything. Then go to **My Course** in the app and hit "Analyze" to generate your personalized study guide.

## Project Structure

```
├── src/                    # React frontend
│   ├── pages/
│   │   ├── Dashboard.jsx   # Progress overview + priority alerts
│   │   ├── Learn.jsx       # Deep teaching content viewer
│   │   ├── Practice.jsx    # Adaptive practice with hints/walkthroughs
│   │   ├── Formulas.jsx    # KaTeX formula reference sheet
│   │   ├── Course.jsx      # Canvas sync + AI study guide
│   │   └── Settings.jsx    # Configuration
│   ├── components/
│   │   ├── Header.jsx      # Navigation bar
│   │   └── Math.jsx        # KaTeX math rendering component
│   └── utils/
│       └── api.js          # API client for all backend endpoints
│
├── backend/                # Python FastAPI backend
│   ├── server.py           # API server (all endpoints)
│   ├── ai_tutor.py         # Copilot CLI AI integration
│   ├── adaptive_tutor.py   # Problem bank + hint system + mastery tracking
│   ├── deep_teaching.py    # Comprehensive teaching content per topic
│   ├── calc2_content.py    # Built-in Calc II curriculum content
│   ├── analyzer.py         # Course content analyzer + study guide generator
│   ├── comprehensive_scraper.py  # Playwright Canvas/Pearson/Gradescope scraper
│   ├── canvas_client.py    # Canvas REST API client
│   └── data/               # Scraped course data + progress JSON files
│
├── index.html              # Entry point
├── vite.config.js          # Vite dev server (port 2000)
└── package.json            # Node dependencies
```

## Why This Exists

Online courses dump 5 forty-minute lecture videos per week plus 4-6 assignments plus a writing assignment. The resources exist — they're just buried across Canvas, Pearson MyLab, Gradescope, and random instructor links. Nobody has time to hunt through all of that AND actually learn calculus.

This platform pulls it all together, lets AI figure out what matters most, and teaches it to you in a way that actually sticks — with real practice, real feedback, and zero time wasted on busywork.

---

*Built with frustration, caffeine, and GitHub Copilot. Let's ace this final.*
