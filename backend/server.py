"""
FastAPI Backend for Calculus Mastery Platform
Provides API endpoints for study features - works standalone without Canvas API.
"""
import os
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional, List
from fastapi import FastAPI, HTTPException, Query, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Calculus Mastery API", version="1.0.0")

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:2000", "http://127.0.0.1:2000", "http://localhost:5173", "http://localhost:5174", "http://127.0.0.1:5173", "http://127.0.0.1:5174", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data storage path
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

# ============ Models ============

class ProblemSubmission(BaseModel):
    problem_id: str
    answer: str

class StudyProgress(BaseModel):
    topic: str
    completed_problems: int
    correct_problems: int

class ManualCourseContent(BaseModel):
    syllabus: Optional[str] = None
    assignments: Optional[List[dict]] = None
    notes: Optional[str] = None

class ManualAssignment(BaseModel):
    title: str
    description: str
    due_date: Optional[str] = None
    url: Optional[str] = None

# ============ Manual Course Content (No Canvas API needed) ============

MANUAL_COURSE_FILE = DATA_DIR / "manual_course.json"

def load_manual_course():
    if MANUAL_COURSE_FILE.exists():
        with open(MANUAL_COURSE_FILE) as f:
            return json.load(f)
    return {"syllabus": "", "assignments": [], "notes": "", "updated_at": None}

def save_manual_course(data):
    data["updated_at"] = datetime.utcnow().isoformat()
    with open(MANUAL_COURSE_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.get("/api/manual-course")
async def get_manual_course():
    """Get manually entered course content"""
    return load_manual_course()

@app.post("/api/manual-course/syllabus")
async def save_syllabus(data: dict):
    """Save pasted syllabus content"""
    course = load_manual_course()
    course["syllabus"] = data.get("content", "")
    save_manual_course(course)
    return {"status": "saved"}

@app.post("/api/manual-course/assignment")
async def add_assignment(assignment: ManualAssignment):
    """Add a manually entered assignment"""
    course = load_manual_course()
    course["assignments"].append({
        "id": len(course["assignments"]) + 1,
        "title": assignment.title,
        "description": assignment.description,
        "due_date": assignment.due_date,
        "url": assignment.url,
        "added_at": datetime.utcnow().isoformat()
    })
    save_manual_course(course)
    return {"status": "added", "assignment_id": len(course["assignments"])}

@app.delete("/api/manual-course/assignment/{assignment_id}")
async def delete_assignment(assignment_id: int):
    """Delete a manually entered assignment"""
    course = load_manual_course()
    course["assignments"] = [a for a in course["assignments"] if a.get("id") != assignment_id]
    save_manual_course(course)
    return {"status": "deleted"}

@app.post("/api/manual-course/notes")
async def save_notes(data: dict):
    """Save study notes"""
    course = load_manual_course()
    course["notes"] = data.get("content", "")
    save_manual_course(course)
    return {"status": "saved"}

# ============ Course Data Endpoints ============

@app.get("/api/course/data")
async def get_course_data():
    """Get the synced course data - checks both regular and comprehensive scrapes"""
    # Check for comprehensive scrape first (preferred)
    comprehensive_files = list(DATA_DIR.glob("comprehensive_*.json"))
    if comprehensive_files:
        latest = max(comprehensive_files, key=lambda p: p.stat().st_mtime)
        with open(latest) as f:
            data = json.load(f)
        return {"synced": True, "comprehensive": True, "data": data}
    
    # Fall back to regular course files
    course_files = list(DATA_DIR.glob("course_*.json"))
    if not course_files:
        return {"synced": False}
    
    latest = max(course_files, key=lambda p: p.stat().st_mtime)
    with open(latest) as f:
        data = json.load(f)
    
    return {"synced": True, "comprehensive": False, "data": data}

@app.get("/api/course/problems")
async def get_course_problems():
    """Get all scraped problems from the course"""
    # Check comprehensive scrape
    comprehensive_files = list(DATA_DIR.glob("comprehensive_*.json"))
    if comprehensive_files:
        latest = max(comprehensive_files, key=lambda p: p.stat().st_mtime)
        with open(latest) as f:
            data = json.load(f)
        return {"problems": data.get("problems", []), "count": len(data.get("problems", []))}
    
    # Check dedicated problems file
    problems_files = list(DATA_DIR.glob("problems_*.json"))
    if problems_files:
        latest = max(problems_files, key=lambda p: p.stat().st_mtime)
        with open(latest) as f:
            problems = json.load(f)
        return {"problems": problems, "count": len(problems)}
    
    return {"problems": [], "count": 0}

@app.get("/api/course/exams")
async def get_course_exams():
    """Get scraped exam content"""
    comprehensive_files = list(DATA_DIR.glob("comprehensive_*.json"))
    if comprehensive_files:
        latest = max(comprehensive_files, key=lambda p: p.stat().st_mtime)
        with open(latest) as f:
            data = json.load(f)
        return {"exams": data.get("exams", []), "count": len(data.get("exams", []))}
    return {"exams": [], "count": 0}

@app.post("/api/course/scrape")
async def trigger_scrape():
    """Trigger a comprehensive scrape (returns immediately, scrape runs in background)"""
    import subprocess
    import sys
    
    # Run scraper as subprocess
    scraper_path = Path(__file__).parent / "comprehensive_scraper.py"
    subprocess.Popen([sys.executable, str(scraper_path)], 
                     cwd=str(Path(__file__).parent),
                     stdout=subprocess.DEVNULL,
                     stderr=subprocess.DEVNULL)
    
    return {"status": "scrape_started", "message": "Check the browser window for login"}

@app.get("/api/course/assignments")
async def get_assignments():
    """Get all assignments from synced course"""
    course_files = list(DATA_DIR.glob("course_*.json"))
    if not course_files:
        raise HTTPException(status_code=404, detail="No course synced yet")
    
    latest = max(course_files, key=lambda p: p.stat().st_mtime)
    with open(latest) as f:
        data = json.load(f)
    
    return {"assignments": data.get("assignments", [])}

@app.get("/api/course/modules")
async def get_modules():
    """Get all modules from synced course"""
    course_files = list(DATA_DIR.glob("course_*.json"))
    if not course_files:
        raise HTTPException(status_code=404, detail="No course synced yet")
    
    latest = max(course_files, key=lambda p: p.stat().st_mtime)
    with open(latest) as f:
        data = json.load(f)
    
    return {"modules": data.get("modules", [])}

@app.get("/api/course/topics")
async def get_topics():
    """Get extracted topics from the course"""
    course_files = list(DATA_DIR.glob("course_*.json"))
    if not course_files:
        raise HTTPException(status_code=404, detail="No course synced yet")
    
    latest = max(course_files, key=lambda p: p.stat().st_mtime)
    with open(latest) as f:
        data = json.load(f)
    
    return {"topics": data.get("topics", [])}

@app.get("/api/course/syllabus")
async def get_syllabus():
    """Get the course syllabus"""
    course_files = list(DATA_DIR.glob("course_*.json"))
    if not course_files:
        raise HTTPException(status_code=404, detail="No course synced yet")
    
    latest = max(course_files, key=lambda p: p.stat().st_mtime)
    with open(latest) as f:
        data = json.load(f)
    
    return {"syllabus": data.get("syllabus", {})}

# ============ AI Course Analysis ============

@app.get("/api/course/analyze")
async def analyze_course():
    """Run AI analysis on scraped course data and generate study guide"""
    from analyzer import CourseAnalyzer
    
    analyzer = CourseAnalyzer()
    if not analyzer.load_course_data():
        raise HTTPException(status_code=404, detail="No course data to analyze. Run the scraper first.")
    
    study_guide = analyzer.generate_study_guide()
    return {"status": "success", "study_guide": study_guide}

@app.get("/api/course/study-guide")
async def get_study_guide():
    """Get the generated study guide"""
    study_guide_file = DATA_DIR / "study_guide.json"
    if not study_guide_file.exists():
        return {"exists": False}
    
    with open(study_guide_file) as f:
        guide = json.load(f)
    
    return {"exists": True, "study_guide": guide}

# ============ Study Content - Built-in Calculus Teaching ============

CALCULUS_CONTENT = {
    "limits": {
        "title": "Limits and Continuity",
        "description": "Understanding the foundational concept of calculus",
        "concepts": [
            {
                "name": "Definition of a Limit",
                "explanation": """A limit describes the value a function approaches as the input approaches some value.

**Formal Definition:** We say lim(x→a) f(x) = L if for every ε > 0, there exists a δ > 0 such that if 0 < |x - a| < δ, then |f(x) - L| < ε.

**Intuitive Understanding:** As x gets closer and closer to a, f(x) gets closer and closer to L.

**Key Points:**
• The limit may exist even if f(a) is undefined
• The limit describes behavior near a point, not at the point
• Left-hand and right-hand limits must agree for the limit to exist""",
                "formula": "\\lim_{x \\to a} f(x) = L",
                "examples": [
                    {"problem": "Find lim(x→2) (x² - 4)/(x - 2)", "solution": "Factor: (x-2)(x+2)/(x-2) = x+2. As x→2, this equals 4."},
                    {"problem": "Find lim(x→0) sin(x)/x", "solution": "This famous limit equals 1. Use L'Hôpital's Rule or geometric argument."},
                ]
            },
            {
                "name": "Limit Laws",
                "explanation": """Limit laws allow us to break down complex limits into simpler parts.

**Sum Law:** lim[f(x) + g(x)] = lim f(x) + lim g(x)
**Product Law:** lim[f(x) · g(x)] = lim f(x) · lim g(x)  
**Quotient Law:** lim[f(x)/g(x)] = lim f(x) / lim g(x), if lim g(x) ≠ 0
**Power Law:** lim[f(x)]ⁿ = [lim f(x)]ⁿ
**Constant Multiple:** lim[c · f(x)] = c · lim f(x)""",
                "formula": "\\lim_{x \\to a} [f(x) + g(x)] = \\lim_{x \\to a} f(x) + \\lim_{x \\to a} g(x)",
            },
            {
                "name": "Continuity",
                "explanation": """A function f is continuous at a point a if three conditions are met:

1. **f(a) is defined** - the function has a value at a
2. **lim(x→a) f(x) exists** - the limit exists
3. **lim(x→a) f(x) = f(a)** - the limit equals the function value

**Types of Discontinuities:**
• **Removable:** Limit exists but f(a) is undefined or different
• **Jump:** Left and right limits exist but are different  
• **Infinite:** Function approaches infinity""",
                "formula": "\\lim_{x \\to a} f(x) = f(a)",
            },
            {
                "name": "Squeeze Theorem",
                "explanation": """If g(x) ≤ f(x) ≤ h(x) for all x near a (except possibly at a), and lim g(x) = lim h(x) = L, then lim f(x) = L.

**When to Use:** When direct computation is difficult, but you can bound the function between two simpler functions.

**Classic Example:** Prove lim(x→0) x²sin(1/x) = 0
Since -1 ≤ sin(1/x) ≤ 1, we have -x² ≤ x²sin(1/x) ≤ x²
Both -x² and x² approach 0 as x→0, so by Squeeze Theorem, the limit is 0.""",
                "formula": "g(x) \\leq f(x) \\leq h(x) \\Rightarrow \\lim_{x \\to a} f(x) = L",
            }
        ],
        "practice_problems": [
            {"question": "Evaluate: lim(x→3) (x² - 9)/(x - 3)", "answer": "6", "hint": "Factor the numerator as a difference of squares."},
            {"question": "Evaluate: lim(x→0) (1 - cos(x))/x²", "answer": "1/2", "hint": "Use L'Hôpital's Rule twice or the identity 1-cos(x) = 2sin²(x/2)."},
            {"question": "Is f(x) = |x|/x continuous at x = 0?", "answer": "No", "hint": "Check the left and right hand limits."},
        ]
    },
    "derivatives": {
        "title": "Derivatives",
        "description": "The rate of change and slope of tangent lines",
        "concepts": [
            {
                "name": "Definition of the Derivative",
                "explanation": """The derivative measures the instantaneous rate of change of a function.

**Limit Definition:**
f'(x) = lim(h→0) [f(x+h) - f(x)] / h

**Alternative Form:**
f'(a) = lim(x→a) [f(x) - f(a)] / (x - a)

**Interpretations:**
• **Geometric:** Slope of the tangent line at a point
• **Physical:** Instantaneous velocity (if f is position)
• **General:** Rate of change of f with respect to x

**Notation:** f'(x), dy/dx, d/dx[f(x)], Df(x)""",
                "formula": "f'(x) = \\lim_{h \\to 0} \\frac{f(x+h) - f(x)}{h}",
                "examples": [
                    {"problem": "Find f'(x) if f(x) = x² using the definition", "solution": "f'(x) = lim(h→0) [(x+h)² - x²]/h = lim(h→0) [2xh + h²]/h = lim(h→0) (2x + h) = 2x"},
                ]
            },
            {
                "name": "Basic Derivative Rules",
                "explanation": """Master these rules to differentiate any polynomial or basic function:

**Power Rule:** d/dx[xⁿ] = nxⁿ⁻¹
**Constant Rule:** d/dx[c] = 0
**Constant Multiple:** d/dx[cf(x)] = c·f'(x)
**Sum/Difference:** d/dx[f(x) ± g(x)] = f'(x) ± g'(x)

**Common Derivatives:**
• d/dx[eˣ] = eˣ
• d/dx[ln(x)] = 1/x
• d/dx[sin(x)] = cos(x)
• d/dx[cos(x)] = -sin(x)
• d/dx[tan(x)] = sec²(x)""",
                "formula": "\\frac{d}{dx}[x^n] = nx^{n-1}",
            },
            {
                "name": "Product Rule",
                "explanation": """Used when differentiating a product of two functions.

**Formula:** d/dx[f(x)·g(x)] = f'(x)·g(x) + f(x)·g'(x)

**Memory Aid:** "First times derivative of second, plus second times derivative of first"

**Example:** d/dx[x²·sin(x)]
= (2x)·sin(x) + x²·cos(x)
= 2x·sin(x) + x²·cos(x)""",
                "formula": "\\frac{d}{dx}[f(x) \\cdot g(x)] = f'(x) \\cdot g(x) + f(x) \\cdot g'(x)",
            },
            {
                "name": "Quotient Rule",
                "explanation": """Used when differentiating a quotient of two functions.

**Formula:** d/dx[f(x)/g(x)] = [f'(x)·g(x) - f(x)·g'(x)] / [g(x)]²

**Memory Aid:** "Low d-high minus high d-low, over low squared"
(Lo · dHi - Hi · dLo) / Lo²

**Example:** d/dx[sin(x)/x]
= [cos(x)·x - sin(x)·1] / x²
= [x·cos(x) - sin(x)] / x²""",
                "formula": "\\frac{d}{dx}\\left[\\frac{f(x)}{g(x)}\\right] = \\frac{f'(x) \\cdot g(x) - f(x) \\cdot g'(x)}{[g(x)]^2}",
            },
            {
                "name": "Chain Rule",
                "explanation": """**The most important rule!** Used for composite functions.

**Formula:** d/dx[f(g(x))] = f'(g(x)) · g'(x)

**In Leibniz Notation:** dy/dx = (dy/du) · (du/dx)

**Process:**
1. Identify the "outer" function f and "inner" function g
2. Differentiate the outer function, leaving the inner function alone
3. Multiply by the derivative of the inner function

**Example:** d/dx[sin(x²)]
- Outer: sin(u), Inner: u = x²
- = cos(x²) · 2x = 2x·cos(x²)""",
                "formula": "\\frac{d}{dx}[f(g(x))] = f'(g(x)) \\cdot g'(x)",
            }
        ],
        "practice_problems": [
            {"question": "Find d/dx[x³ - 4x² + 7x - 2]", "answer": "3x² - 8x + 7", "hint": "Apply the power rule term by term."},
            {"question": "Find d/dx[e^(3x)]", "answer": "3e^(3x)", "hint": "Use the chain rule with outer function eᵘ and inner function 3x."},
            {"question": "Find d/dx[x²·ln(x)]", "answer": "2x·ln(x) + x", "hint": "Use the product rule."},
            {"question": "Find d/dx[sin(x)/cos(x)]", "answer": "sec²(x)", "hint": "Use quotient rule, or recognize this as tan(x)."},
        ]
    },
    "integration_basics": {
        "title": "Integration Fundamentals",
        "description": "Antiderivatives and the Fundamental Theorem",
        "concepts": [
            {
                "name": "Antiderivatives",
                "explanation": """An antiderivative of f(x) is a function F(x) such that F'(x) = f(x).

**Notation:** ∫f(x)dx = F(x) + C

**The +C is essential!** Since the derivative of a constant is 0, there are infinitely many antiderivatives differing by a constant.

**Basic Antiderivative Rules:**
• ∫xⁿ dx = xⁿ⁺¹/(n+1) + C  (n ≠ -1)
• ∫1/x dx = ln|x| + C
• ∫eˣ dx = eˣ + C
• ∫sin(x) dx = -cos(x) + C
• ∫cos(x) dx = sin(x) + C
• ∫sec²(x) dx = tan(x) + C""",
                "formula": "\\int x^n \\, dx = \\frac{x^{n+1}}{n+1} + C \\quad (n \\neq -1)",
            },
            {
                "name": "Fundamental Theorem of Calculus",
                "explanation": """**Part 1:** If F(x) = ∫ₐˣ f(t)dt, then F'(x) = f(x)

This says differentiation and integration are inverse operations!

**Part 2:** ∫ₐᵇ f(x)dx = F(b) - F(a)

where F is any antiderivative of f.

**This is how we evaluate definite integrals:**
1. Find an antiderivative F(x)
2. Compute F(b) - F(a)

**Example:** ∫₀² x² dx = [x³/3]₀² = 8/3 - 0 = 8/3""",
                "formula": "\\int_a^b f(x) \\, dx = F(b) - F(a)",
            },
            {
                "name": "U-Substitution",
                "explanation": """The reverse of the chain rule. Used when you see a function and its derivative.

**Method:**
1. Choose u = g(x) (usually the "inside" function)
2. Compute du = g'(x)dx
3. Substitute to get an integral in terms of u
4. Integrate
5. Substitute back x

**Example:** ∫2x·cos(x²)dx
- Let u = x², then du = 2x dx
- ∫cos(u)du = sin(u) + C = sin(x²) + C

**Key Insight:** Look for a function-derivative pair. If you see f(g(x))·g'(x), try u = g(x).""",
                "formula": "\\int f(g(x)) \\cdot g'(x) \\, dx = \\int f(u) \\, du",
            },
            {
                "name": "Integration by Parts",
                "explanation": """The reverse of the product rule.

**Formula:** ∫u dv = uv - ∫v du

**LIATE Rule for choosing u:** (in order of preference)
• **L**ogarithmic functions (ln x)
• **I**nverse trig (arctan x)
• **A**lgebraic (x², x)
• **T**rigonometric (sin x, cos x)
• **E**xponential (eˣ)

**Example:** ∫x·eˣ dx
- u = x, dv = eˣ dx
- du = dx, v = eˣ
- = x·eˣ - ∫eˣ dx = x·eˣ - eˣ + C = eˣ(x-1) + C""",
                "formula": "\\int u \\, dv = uv - \\int v \\, du",
            }
        ],
        "practice_problems": [
            {"question": "Evaluate: ∫(3x² + 2x - 1)dx", "answer": "x³ + x² - x + C", "hint": "Integrate term by term using the power rule."},
            {"question": "Evaluate: ∫₀¹ 2x dx", "answer": "1", "hint": "Antiderivative is x², evaluate at bounds."},
            {"question": "Evaluate: ∫cos(3x)dx using substitution", "answer": "(1/3)sin(3x) + C", "hint": "Let u = 3x, so du = 3dx."},
            {"question": "Evaluate: ∫x·sin(x)dx", "answer": "-x·cos(x) + sin(x) + C", "hint": "Use integration by parts with u = x, dv = sin(x)dx."},
        ]
    },
    "applications_derivatives": {
        "title": "Applications of Derivatives",
        "description": "Optimization, related rates, and curve sketching",
        "concepts": [
            {
                "name": "Critical Points and Extrema",
                "explanation": """**Critical Points:** Points where f'(x) = 0 or f'(x) is undefined.

**Finding Absolute Extrema on [a,b]:**
1. Find all critical points in (a,b)
2. Evaluate f at critical points and endpoints
3. Largest value is absolute max, smallest is absolute min

**First Derivative Test:**
• If f' changes from + to - at c, then f(c) is a local max
• If f' changes from - to + at c, then f(c) is a local min

**Second Derivative Test:**
• If f'(c) = 0 and f''(c) > 0, then f(c) is a local min
• If f'(c) = 0 and f''(c) < 0, then f(c) is a local max""",
                "formula": "f'(c) = 0 \\text{ or undefined} \\Rightarrow c \\text{ is critical}",
            },
            {
                "name": "Optimization Problems",
                "explanation": """**Strategy for Optimization:**

1. **Draw a picture** and identify variables
2. **Write the objective function** (what you're maximizing/minimizing)
3. **Write constraint equations** relating the variables
4. **Use constraints to eliminate variables** so objective has one variable
5. **Find critical points** by setting derivative = 0
6. **Test critical points** and endpoints if applicable
7. **Answer the question** with units!

**Common Setups:**
• Maximize area with fixed perimeter
• Minimize material for fixed volume
• Minimize distance or time""",
                "formula": "\\text{Optimize } f(x) \\text{ subject to constraints}",
            },
            {
                "name": "Related Rates",
                "explanation": """Problems where multiple quantities change with time.

**Strategy:**
1. **Identify variables** and which are changing
2. **Write an equation** relating the variables
3. **Differentiate both sides** with respect to time t
4. **Substitute known values** (at the instant in question)
5. **Solve for the unknown rate**

**Example Setup:** A ladder sliding down a wall
- Variables: x (base distance), y (height), L (ladder length)
- Equation: x² + y² = L²
- Differentiate: 2x(dx/dt) + 2y(dy/dt) = 0

**Key:** Don't substitute values until AFTER differentiating!""",
                "formula": "\\frac{d}{dt}[\\text{equation}] \\text{ gives related rates}",
            },
            {
                "name": "Curve Sketching",
                "explanation": """**Complete Analysis Checklist:**

1. **Domain:** Where is f defined?
2. **Intercepts:** Where does f cross axes?
3. **Symmetry:** Is f even, odd, or neither?
4. **Asymptotes:** 
   - Vertical: where denominator = 0
   - Horizontal: lim as x→±∞
5. **First Derivative Analysis:**
   - Critical points (f' = 0 or undefined)
   - Intervals of increase/decrease
   - Local max/min
6. **Second Derivative Analysis:**
   - Inflection points (f'' = 0)
   - Intervals of concave up/down
7. **Sketch the curve** using all information""",
                "formula": "f''(x) > 0 \\Rightarrow \\text{concave up}, \\quad f''(x) < 0 \\Rightarrow \\text{concave down}",
            }
        ],
        "practice_problems": [
            {"question": "Find the critical points of f(x) = x³ - 3x + 2", "answer": "x = -1 and x = 1", "hint": "Set f'(x) = 3x² - 3 = 0."},
            {"question": "Find the absolute maximum of f(x) = x² on [-2, 3]", "answer": "9 at x = 3", "hint": "Check critical points and endpoints."},
            {"question": "A 10ft ladder slides down a wall. When the base is 6ft from the wall moving at 2ft/s, how fast is the top sliding down?", "answer": "-3/2 ft/s", "hint": "Use x² + y² = 100 and differentiate."},
        ]
    },
    "applications_integration": {
        "title": "Applications of Integration",
        "description": "Area, volume, and physical applications",
        "concepts": [
            {
                "name": "Area Between Curves",
                "explanation": """**Formula:** Area = ∫ₐᵇ |f(x) - g(x)| dx

**Method:**
1. Find intersection points (set f(x) = g(x))
2. Determine which function is on top in each region
3. Integrate (top - bottom) over each region

**When integrating with respect to y:**
Area = ∫ₐᵇ |right(y) - left(y)| dy

**Choose the variable that makes setup easier!**""",
                "formula": "A = \\int_a^b [f(x) - g(x)] \\, dx",
            },
            {
                "name": "Disk Method",
                "explanation": """For solids of revolution around an axis.

**Around x-axis:** V = π∫ₐᵇ [f(x)]² dx

**Around y-axis:** V = π∫ₐᵇ [g(y)]² dy

**Key Insight:** Each cross-section is a disk with:
- Radius = distance from curve to axis
- Area = πr²
- Volume = ∫(area)dx

**Use when:** The region is bounded by one curve and the axis of rotation.""",
                "formula": "V = \\pi \\int_a^b [f(x)]^2 \\, dx",
            },
            {
                "name": "Washer Method",
                "explanation": """For solids with a hole in the middle.

**Formula:** V = π∫ₐᵇ ([R(x)]² - [r(x)]²) dx

where:
- R(x) = outer radius (distance from axis to outer curve)
- r(x) = inner radius (distance from axis to inner curve)

**Use when:** Region is bounded by two curves, rotated around an axis.

**Tip:** Always draw the region and visualize the rotation!""",
                "formula": "V = \\pi \\int_a^b ([R(x)]^2 - [r(x)]^2) \\, dx",
            },
            {
                "name": "Shell Method",
                "explanation": """An alternative to disk/washer, using cylindrical shells.

**Around y-axis:** V = 2π∫ₐᵇ x·f(x) dx

**Around x-axis:** V = 2π∫ₐᵇ y·g(y) dy

**Each shell has:**
- Radius = distance from axis
- Height = function value
- Thickness = dx (or dy)

**Use when:** 
- Rotating around y-axis with function of x
- Disk/washer setup is complicated""",
                "formula": "V = 2\\pi \\int_a^b x \\cdot f(x) \\, dx",
            }
        ],
        "practice_problems": [
            {"question": "Find the area between y = x² and y = x", "answer": "1/6", "hint": "Curves intersect at x=0 and x=1. Integrate (x - x²)."},
            {"question": "Find the volume when y = √x from x=0 to x=4 is rotated about the x-axis", "answer": "8π", "hint": "Use disk method: V = π∫[√x]²dx = π∫x dx."},
            {"question": "Set up (don't evaluate) the integral for the volume when y = x² (0≤x≤2) is rotated about the y-axis", "answer": "V = 2π∫₀² x·x² dx = 2π∫₀² x³ dx", "hint": "Use shell method with radius x and height x²."},
        ]
    },
    "series": {
        "title": "Infinite Series",
        "description": "Sequences, series, and convergence tests",
        "concepts": [
            {
                "name": "Sequences",
                "explanation": """A sequence is an ordered list of numbers: a₁, a₂, a₃, ...

**Convergence:** lim(n→∞) aₙ = L means the sequence converges to L.

**Divergence:** If the limit doesn't exist or is ±∞.

**Key Theorem:** If lim aₙ ≠ 0, then Σaₙ diverges.
(But lim aₙ = 0 does NOT guarantee convergence!)

**Common Limits:**
• lim(n→∞) 1/nᵖ = 0 for p > 0
• lim(n→∞) rⁿ = 0 for |r| < 1
• lim(n→∞) n^(1/n) = 1
• lim(n→∞) (1 + 1/n)ⁿ = e""",
                "formula": "\\lim_{n \\to \\infty} a_n = L",
            },
            {
                "name": "Geometric Series",
                "explanation": """**Form:** Σ arⁿ = a + ar + ar² + ar³ + ...

**Convergence:** Converges if |r| < 1

**Sum Formula:** Σ(n=0 to ∞) arⁿ = a/(1-r) when |r| < 1

**Partial Sum:** Σ(n=0 to N) arⁿ = a(1-rᴺ⁺¹)/(1-r)

**Examples:**
• Σ(1/2)ⁿ = 1/(1-1/2) = 2
• Σ(-1/3)ⁿ = 1/(1+1/3) = 3/4""",
                "formula": "\\sum_{n=0}^{\\infty} ar^n = \\frac{a}{1-r} \\quad (|r| < 1)",
            },
            {
                "name": "p-Series",
                "explanation": """**Form:** Σ 1/nᵖ = 1 + 1/2ᵖ + 1/3ᵖ + ...

**Convergence Rule:**
• Converges if p > 1
• Diverges if p ≤ 1

**Important Special Cases:**
• p = 1: Harmonic series Σ1/n diverges
• p = 2: Σ1/n² = π²/6 converges
• p = 1/2: Σ1/√n diverges""",
                "formula": "\\sum_{n=1}^{\\infty} \\frac{1}{n^p} \\begin{cases} \\text{converges} & p > 1 \\\\ \\text{diverges} & p \\leq 1 \\end{cases}",
            },
            {
                "name": "Convergence Tests",
                "explanation": """**Test for Divergence:** If lim aₙ ≠ 0, series diverges.

**Integral Test:** If f is positive, continuous, decreasing, and f(n) = aₙ, then Σaₙ and ∫f(x)dx both converge or both diverge.

**Comparison Test:** 
• If 0 ≤ aₙ ≤ bₙ and Σbₙ converges, then Σaₙ converges
• If 0 ≤ bₙ ≤ aₙ and Σbₙ diverges, then Σaₙ diverges

**Limit Comparison:** If lim(aₙ/bₙ) = c > 0, both series have same behavior.

**Ratio Test:** If lim|aₙ₊₁/aₙ| = L:
• L < 1: converges absolutely
• L > 1: diverges  
• L = 1: inconclusive

**Root Test:** If lim|aₙ|^(1/n) = L, same rules as ratio test.

**Alternating Series Test:** If aₙ > 0, aₙ₊₁ ≤ aₙ, and lim aₙ = 0, then Σ(-1)ⁿaₙ converges.""",
                "formula": "\\text{Ratio: } L = \\lim_{n \\to \\infty} \\left| \\frac{a_{n+1}}{a_n} \\right|",
            }
        ],
        "practice_problems": [
            {"question": "Does Σ(n=1 to ∞) 1/n² converge or diverge?", "answer": "Converges (p-series with p=2>1)", "hint": "This is a p-series with p=2."},
            {"question": "Find the sum: Σ(n=0 to ∞) (2/3)ⁿ", "answer": "3", "hint": "Geometric series with a=1, r=2/3."},
            {"question": "Use the ratio test on Σ n!/nⁿ", "answer": "Converges (L = 1/e < 1)", "hint": "Compute lim[(n+1)!/(n+1)^(n+1)] / [n!/n^n]."},
            {"question": "Does Σ(-1)ⁿ/n converge?", "answer": "Yes, conditionally", "hint": "Apply alternating series test."},
        ]
    },
    "power_series": {
        "title": "Power Series and Taylor Series",
        "description": "Representing functions as infinite series",
        "concepts": [
            {
                "name": "Power Series",
                "explanation": """**Form:** Σ cₙ(x-a)ⁿ = c₀ + c₁(x-a) + c₂(x-a)² + ...

**Radius of Convergence (R):**
The series converges for |x-a| < R and diverges for |x-a| > R.

**Finding R:** Use ratio test:
R = lim|cₙ/cₙ₊₁| or R = 1/lim|cₙ|^(1/n)

**Interval of Convergence:**
After finding R, test endpoints separately!

**Operations:** Power series can be added, multiplied, differentiated, and integrated term-by-term within the radius of convergence.""",
                "formula": "\\sum_{n=0}^{\\infty} c_n(x-a)^n \\text{ converges for } |x-a| < R",
            },
            {
                "name": "Taylor Series",
                "explanation": """**Taylor series centered at a:**
f(x) = Σ [f⁽ⁿ⁾(a)/n!](x-a)ⁿ

**Maclaurin series (a=0):**
f(x) = Σ [f⁽ⁿ⁾(0)/n!]xⁿ

**Common Series (memorize these!):**
• eˣ = 1 + x + x²/2! + x³/3! + ... = Σxⁿ/n!
• sin(x) = x - x³/3! + x⁵/5! - ... = Σ(-1)ⁿx^(2n+1)/(2n+1)!
• cos(x) = 1 - x²/2! + x⁴/4! - ... = Σ(-1)ⁿx^(2n)/(2n)!
• 1/(1-x) = 1 + x + x² + x³ + ... = Σxⁿ (|x|<1)
• ln(1+x) = x - x²/2 + x³/3 - ... = Σ(-1)^(n+1)xⁿ/n (|x|<1)""",
                "formula": "f(x) = \\sum_{n=0}^{\\infty} \\frac{f^{(n)}(a)}{n!}(x-a)^n",
            },
            {
                "name": "Taylor Polynomials and Approximation",
                "explanation": """**Taylor Polynomial of degree n:**
Pₙ(x) = Σ(k=0 to n) [f⁽ᵏ⁾(a)/k!](x-a)ᵏ

This is the best polynomial approximation of degree n near x=a.

**Remainder (Error):**
Rₙ(x) = f(x) - Pₙ(x)

**Taylor's Inequality:**
|Rₙ(x)| ≤ M|x-a|^(n+1)/(n+1)!

where M is an upper bound for |f⁽ⁿ⁺¹⁾| on the interval.

**Use:** Approximate function values and estimate errors.""",
                "formula": "P_n(x) = \\sum_{k=0}^{n} \\frac{f^{(k)}(a)}{k!}(x-a)^k",
            }
        ],
        "practice_problems": [
            {"question": "Find the radius of convergence of Σ xⁿ/n", "answer": "R = 1", "hint": "Use ratio test: lim|n/(n+1)| = 1."},
            {"question": "Write the first 4 nonzero terms of the Maclaurin series for e^(2x)", "answer": "1 + 2x + 2x² + (4/3)x³", "hint": "Use eˣ series with x replaced by 2x."},
            {"question": "Find the Taylor series for 1/(1+x²) centered at 0", "answer": "1 - x² + x⁴ - x⁶ + ... = Σ(-1)ⁿx^(2n)", "hint": "Use 1/(1-u) = Σuⁿ with u = -x²."},
        ]
    },
}

@app.get("/api/content/topics")
async def get_all_topics():
    """Get all available calculus topics"""
    topics = []
    for key, content in CALCULUS_CONTENT.items():
        topics.append({
            "id": key,
            "title": content["title"],
            "description": content["description"],
            "concept_count": len(content["concepts"]),
            "problem_count": len(content.get("practice_problems", []))
        })
    return {"topics": topics}

@app.get("/api/content/topic/{topic_id}")
async def get_topic_content(topic_id: str):
    """Get detailed content for a specific topic"""
    if topic_id not in CALCULUS_CONTENT:
        raise HTTPException(status_code=404, detail="Topic not found")
    return {"topic": CALCULUS_CONTENT[topic_id]}

@app.get("/api/content/problems/{topic_id}")
async def get_topic_problems(topic_id: str):
    """Get practice problems for a specific topic"""
    if topic_id not in CALCULUS_CONTENT:
        raise HTTPException(status_code=404, detail="Topic not found")
    return {"problems": CALCULUS_CONTENT[topic_id].get("practice_problems", [])}

# ============ Progress Tracking ============

PROGRESS_FILE = DATA_DIR / "progress.json"

def load_progress():
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE) as f:
            return json.load(f)
    return {"completed_problems": [], "topic_progress": {}}

def save_progress(progress):
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress, f, indent=2)

@app.get("/api/progress")
async def get_progress():
    """Get user's study progress"""
    return load_progress()

@app.post("/api/progress/complete")
async def mark_complete(data: dict):
    """Mark a problem or concept as completed"""
    progress = load_progress()
    
    if "problem_id" in data:
        if data["problem_id"] not in progress["completed_problems"]:
            progress["completed_problems"].append(data["problem_id"])
    
    if "topic_id" in data:
        topic = data["topic_id"]
        if topic not in progress["topic_progress"]:
            progress["topic_progress"][topic] = {"viewed": 0, "completed": 0}
        progress["topic_progress"][topic]["viewed"] += 1
        if data.get("correct"):
            progress["topic_progress"][topic]["completed"] += 1
    
    save_progress(progress)
    return {"status": "updated", "progress": progress}

# ============ Formula Sheet ============

FORMULA_SHEET = {
    "derivatives": {
        "title": "Derivative Rules",
        "formulas": [
            {"name": "Power Rule", "formula": "\\frac{d}{dx}\\left[x^n\\right] = nx^{n-1}"},
            {"name": "Product Rule", "formula": "\\frac{d}{dx}\\left[fg\\right] = f'g + fg'"},
            {"name": "Quotient Rule", "formula": "\\frac{d}{dx}\\left[\\frac{f}{g}\\right] = \\frac{f'g - fg'}{g^2}"},
            {"name": "Chain Rule", "formula": "\\frac{d}{dx}\\left[f\\left(g(x)\\right)\\right] = f'\\left(g(x)\\right) \\cdot g'(x)"},
            {"name": "Exponential", "formula": "\\frac{d}{dx}\\left[e^x\\right] = e^x"},
            {"name": "Natural Log", "formula": "\\frac{d}{dx}\\left[\\ln x\\right] = \\frac{1}{x}"},
            {"name": "Sine", "formula": "\\frac{d}{dx}\\left[\\sin x\\right] = \\cos x"},
            {"name": "Cosine", "formula": "\\frac{d}{dx}\\left[\\cos x\\right] = -\\sin x"},
            {"name": "Tangent", "formula": "\\frac{d}{dx}\\left[\\tan x\\right] = \\sec^2 x"},
        ]
    },
    "integrals": {
        "title": "Integration Rules",
        "formulas": [
            {"name": "Power Rule", "formula": "\\int x^n \\, dx = \\frac{x^{n+1}}{n+1} + C \\quad (n \\neq -1)"},
            {"name": "Exponential", "formula": "\\int e^x \\, dx = e^x + C"},
            {"name": "Natural Log", "formula": "\\int \\frac{1}{x} \\, dx = \\ln|x| + C"},
            {"name": "Sine", "formula": "\\int \\sin x \\, dx = -\\cos x + C"},
            {"name": "Cosine", "formula": "\\int \\cos x \\, dx = \\sin x + C"},
            {"name": "Secant Squared", "formula": "\\int \\sec^2 x \\, dx = \\tan x + C"},
            {"name": "By Parts", "formula": "\\int u \\, dv = uv - \\int v \\, du"},
        ]
    },
    "series": {
        "title": "Series Formulas",
        "formulas": [
            {"name": "Geometric Series", "formula": "\\sum_{n=0}^{\\infty} ar^n = \\frac{a}{1-r} \\quad \\left(|r| < 1\\right)"},
            {"name": "p-Series", "formula": "\\sum_{n=1}^{\\infty} \\frac{1}{n^p} \\text{ converges iff } p > 1"},
            {"name": "Taylor Series", "formula": "f(x) = \\sum_{n=0}^{\\infty} \\frac{f^{(n)}(a)}{n!}\\left(x-a\\right)^n"},
            {"name": "e^x", "formula": "e^x = \\sum_{n=0}^{\\infty} \\frac{x^n}{n!}"},
            {"name": "sin(x)", "formula": "\\sin x = \\sum_{n=0}^{\\infty} \\frac{(-1)^n x^{2n+1}}{(2n+1)!}"},
            {"name": "cos(x)", "formula": "\\cos x = \\sum_{n=0}^{\\infty} \\frac{(-1)^n x^{2n}}{(2n)!}"},
        ]
    },
    "applications": {
        "title": "Application Formulas",
        "formulas": [
            {"name": "Area Between Curves", "formula": "A = \\int_a^b \\left[f(x) - g(x)\\right] \\, dx"},
            {"name": "Disk Method", "formula": "V = \\pi \\int_a^b \\left[f(x)\\right]^2 \\, dx"},
            {"name": "Washer Method", "formula": "V = \\pi \\int_a^b \\left(\\left[R\\right]^2 - \\left[r\\right]^2\\right) \\, dx"},
            {"name": "Shell Method", "formula": "V = 2\\pi \\int_a^b x \\cdot f(x) \\, dx"},
            {"name": "Arc Length", "formula": "L = \\int_a^b \\sqrt{1 + \\left[f'(x)\\right]^2} \\, dx"},
        ]
    }
}

@app.get("/api/formulas")
async def get_formula_sheet():
    """Get the complete formula sheet"""
    return {"formulas": FORMULA_SHEET}

# ============ ADAPTIVE TUTOR ENDPOINTS ============
from adaptive_tutor import get_tutor, PROBLEM_BANK

@app.get("/api/tutor/diagnostic")
async def get_tutor_diagnostic():
    """Get diagnostic summary of student's knowledge state"""
    tutor = get_tutor()
    return tutor.get_diagnostic()

@app.get("/api/tutor/topics")
async def get_tutor_topics():
    """Get all available topics with problem counts"""
    topics = []
    for topic_id, topic_data in PROBLEM_BANK.items():
        problems = topic_data.get("problems", [])
        topics.append({
            "id": topic_id,
            "name": topic_data["name"],
            "prerequisite": topic_data.get("prerequisite"),
            "problem_count": len(problems),
            "levels": list(set(p["level"] for p in problems))
        })
    return {"topics": topics}

@app.get("/api/tutor/topic/{topic_id}")
async def get_tutor_topic_details(topic_id: str):
    """Get detailed information about a topic"""
    if topic_id not in PROBLEM_BANK:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    tutor = get_tutor()
    topic_data = PROBLEM_BANK[topic_id]
    mastery = tutor.progress["mastery"].get(topic_id, {})
    
    return {
        "id": topic_id,
        "name": topic_data["name"],
        "prerequisite": topic_data.get("prerequisite"),
        "problems": topic_data["problems"],
        "mastery": mastery.get("score", 0),
        "attempts": mastery.get("attempts", 0),
        "current_level": tutor.progress["current_level"].get(topic_id, 1)
    }

@app.get("/api/tutor/next-problem/{topic_id}")
async def get_next_problem(topic_id: str):
    """Get the next problem for the student, adapted to their level"""
    if topic_id not in PROBLEM_BANK:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    tutor = get_tutor()
    return tutor.get_next_problem(topic_id)

@app.get("/api/tutor/problem/{topic_id}/{problem_id}")
async def get_specific_problem(topic_id: str, problem_id: str):
    """Get a specific problem by ID"""
    if topic_id not in PROBLEM_BANK:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    problem = next(
        (p for p in PROBLEM_BANK[topic_id]["problems"] if p["id"] == problem_id),
        None
    )
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    
    tutor = get_tutor()
    return {
        "problem": problem,
        "topic": topic_id,
        "topic_name": PROBLEM_BANK[topic_id]["name"],
        "current_level": tutor.progress["current_level"].get(topic_id, 1)
    }

class HintRequest(BaseModel):
    topic_id: str
    problem_id: str
    hint_level: int = 0

@app.post("/api/tutor/hint")
async def get_hint(request: HintRequest):
    """Get a hint for a problem (multi-level hints)"""
    if request.topic_id not in PROBLEM_BANK:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    problem = next(
        (p for p in PROBLEM_BANK[request.topic_id]["problems"] if p["id"] == request.problem_id),
        None
    )
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    
    tutor = get_tutor()
    return tutor.get_hint(problem, request.hint_level)

class WalkthroughRequest(BaseModel):
    topic_id: str
    problem_id: str
    step: int = 0

@app.post("/api/tutor/walkthrough")
async def get_walkthrough_step(request: WalkthroughRequest):
    """Get a step of the walkthrough (step-by-step guidance)"""
    if request.topic_id not in PROBLEM_BANK:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    problem = next(
        (p for p in PROBLEM_BANK[request.topic_id]["problems"] if p["id"] == request.problem_id),
        None
    )
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    
    tutor = get_tutor()
    return tutor.get_walkthrough_step(problem, request.step)

@app.get("/api/tutor/walkthrough-full/{topic_id}/{problem_id}")
async def get_full_walkthrough(topic_id: str, problem_id: str):
    """Get the complete walkthrough for a problem"""
    if topic_id not in PROBLEM_BANK:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    problem = next(
        (p for p in PROBLEM_BANK[topic_id]["problems"] if p["id"] == problem_id),
        None
    )
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    
    return {
        "problem": problem["question"],
        "answer": problem["answer"],
        "walkthrough": problem.get("walkthrough", []),
        "key_concept": problem.get("key_concept", "")
    }

class AttemptRequest(BaseModel):
    topic_id: str
    problem_id: str
    answer: str
    used_hints: int = 0
    used_walkthrough: bool = False

@app.post("/api/tutor/submit")
async def submit_answer(request: AttemptRequest):
    """Submit an answer and get feedback"""
    if request.topic_id not in PROBLEM_BANK:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    problem = next(
        (p for p in PROBLEM_BANK[request.topic_id]["problems"] if p["id"] == request.problem_id),
        None
    )
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    
    # Normalize answer for comparison (handle unicode symbols, spacing, etc.)
    def normalize_answer(ans: str) -> str:
        return (ans.lower()
                .replace(" ", "")
                .replace("\\", "")
                .replace("·", "*")     # middle dot to asterisk
                .replace("×", "*")     # multiplication sign
                .replace("÷", "/")     # division sign
                .replace("²", "^2")    # superscript 2
                .replace("³", "^3")    # superscript 3
                .replace("⁴", "^4")    # superscript 4
                .replace("ˣ", "^x")    # superscript x
                .replace("π", "pi")    # pi symbol
                .replace("∞", "inf")   # infinity
                .replace("−", "-")     # minus sign
                .replace("–", "-"))    # en dash
    
    correct_answer = normalize_answer(problem["answer"])
    user_answer = normalize_answer(request.answer)
    
    # Try multiple matching strategies
    is_correct = (
        user_answer == correct_answer or
        correct_answer.startswith(user_answer) or
        user_answer in correct_answer or
        # Handle multiple answer formats (separated by "or")
        any(normalize_answer(alt) == user_answer or user_answer in normalize_answer(alt) 
            for alt in problem["answer"].split(" or "))
    )
    
    tutor = get_tutor()
    result = tutor.record_attempt(
        request.topic_id,
        request.problem_id,
        is_correct,
        request.used_hints,
        request.used_walkthrough
    )
    
    return {
        "correct": is_correct,
        "expected_answer": problem["answer"],
        "key_concept": problem.get("key_concept", ""),
        **result
    }

@app.post("/api/tutor/reset")
async def reset_progress():
    """Reset all progress (start fresh)"""
    tutor = get_tutor()
    tutor.progress = {
        "mastery": {},
        "current_level": {},
        "weak_spots": [],
        "history": [],
        "streak": 0,
    }
    tutor.save_progress()
    return {"status": "reset", "message": "All progress has been reset"}


# ============ AI-Powered Smart Tutoring (GPT-5-mini - FREE) ============

from smart_ai_tutor import SmartAITutor, CALC2_TOPICS

# Singleton AI tutor instance
_ai_tutor = None

def get_ai_tutor() -> SmartAITutor:
    global _ai_tutor
    if _ai_tutor is None:
        _ai_tutor = SmartAITutor(default_model="gpt-5-mini")
    return _ai_tutor


class AITutorMessage(BaseModel):
    message: str
    topic_id: Optional[str] = None
    mastery_level: Optional[float] = 0.5
    recent_mistakes: Optional[List[str]] = None
    problem: Optional[str] = None       # current problem text for context
    step_index: Optional[int] = None    # current walkthrough step index
    conversation_history: Optional[List[dict]] = None  # full chat history from frontend


class AIProblemRequest(BaseModel):
    topic_id: str
    difficulty: Optional[int] = 1


class AIHintRequest(BaseModel):
    problem: str
    hint_level: Optional[int] = 1
    user_attempt: Optional[str] = None


class AICheckAnswerRequest(BaseModel):
    problem: str
    correct_answer: str
    user_answer: str


class AIQuizRequest(BaseModel):
    topic_ids: List[str]
    num_questions: Optional[int] = 5


@app.get("/api/ai/topics")
async def get_ai_topics():
    """Get all available Calc II topics for AI tutoring"""
    return {
        "topics": CALC2_TOPICS,
        "model": "gpt-5-mini (FREE)"
    }


@app.get("/api/ai/lesson/{topic_id}")
async def get_ai_lesson(topic_id: str):
    """
    Get a comprehensive AI-generated lesson for a topic.
    CACHED: Same lesson returned for efficiency.
    """
    if topic_id not in CALC2_TOPICS:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    ai_tutor = get_ai_tutor()
    lesson = await ai_tutor.get_topic_lesson(topic_id)
    
    return {
        "topic_id": topic_id,
        "topic_name": CALC2_TOPICS[topic_id]["name"],
        "lesson": lesson,
        "cached": True  # Lessons are always cached after first generation
    }


@app.get("/api/ai/explain")
async def explain_concept(concept: str = Query(..., description="The concept to explain")):
    """
    Get an AI explanation of any calculus concept.
    CACHED: Common explanations are cached.
    """
    ai_tutor = get_ai_tutor()
    explanation = await ai_tutor.get_concept_explanation(concept)
    
    return {
        "concept": concept,
        "explanation": explanation
    }


@app.post("/api/ai/generate-problem")
async def generate_ai_problem(request: AIProblemRequest):
    """
    Generate a fresh practice problem.
    NOT CACHED: New problems each time for variety.
    Uses gpt-5-mini (FREE).
    """
    if request.topic_id not in CALC2_TOPICS:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    ai_tutor = get_ai_tutor()
    problem = await ai_tutor.generate_problem(request.topic_id, request.difficulty)
    
    return {
        "topic_id": request.topic_id,
        "problem": problem,
        "generated_by": "gpt-5-mini (FREE)"
    }


@app.post("/api/ai/hint")
async def get_ai_hint(request: AIHintRequest):
    """
    Get a personalized hint for a problem.
    NOT CACHED: Personalized to user's attempt.
    Uses gpt-5-mini (FREE).
    """
    ai_tutor = get_ai_tutor()
    hint = await ai_tutor.get_hint(
        request.problem,
        request.hint_level,
        request.user_attempt
    )
    
    return {
        "hint_level": request.hint_level,
        "hint": hint,
        "next_level": min(request.hint_level + 1, 3)
    }


@app.post("/api/ai/check-answer")
async def check_ai_answer(request: AICheckAnswerRequest):
    """
    Check an answer and get AI feedback.
    NOT CACHED: Personalized feedback.
    Uses gpt-5-mini (FREE).
    """
    ai_tutor = get_ai_tutor()
    result = await ai_tutor.check_answer(
        request.problem,
        request.correct_answer,
        request.user_answer
    )
    
    return result


@app.post("/api/ai/explain-solution")
async def explain_solution(data: dict):
    """
    Get a detailed explanation of a solution.
    CACHED: Solutions don't change.
    """
    problem = data.get("problem", "")
    solution = data.get("solution", "")
    
    if not problem or not solution:
        raise HTTPException(status_code=400, detail="Problem and solution required")
    
    ai_tutor = get_ai_tutor()
    explanation = await ai_tutor.explain_solution(problem, solution)
    
    return {
        "explanation": explanation,
        "cached": True  # Solutions are cached
    }


@app.post("/api/ai/chat")
async def ai_tutor_chat(request: AITutorMessage):
    """
    Main AI tutoring interface — contextual to topic, problem, and walkthrough step.
    NOT CACHED: Conversational and personalized.
    Uses gpt-5-mini (FREE).
    """
    ai_tutor = get_ai_tutor()

    # Build a richer context message when problem/step are provided
    message = request.message
    if request.problem or request.step_index is not None:
        context_parts = []
        if request.topic_id:
            context_parts.append(f"Topic: {request.topic_id}")
        if request.problem:
            context_parts.append(f"Current problem: {request.problem}")
        if request.step_index is not None:
            context_parts.append(f"Student is on walkthrough step {request.step_index + 1}")
        context = "\n".join(context_parts)
        message = f"[Context]\n{context}\n\n[Student question]\n{request.message}"

    response = await ai_tutor.adaptive_tutor_response(
        message,
        request.topic_id,
        request.mastery_level,
        request.recent_mistakes,
        request.conversation_history
    )

    return {
        "response": response,
        "model": "gpt-5-mini (FREE)"
    }


@app.post("/api/ai/quiz")
async def generate_ai_quiz(request: AIQuizRequest):
    """
    Generate a multi-topic quiz.
    NOT CACHED: Fresh problems each time.
    Uses gpt-5-mini (FREE).
    """
    # Validate topics
    valid_topics = [t for t in request.topic_ids if t in CALC2_TOPICS]
    if not valid_topics:
        raise HTTPException(status_code=400, detail="No valid topics provided")
    
    ai_tutor = get_ai_tutor()
    questions = await ai_tutor.generate_quiz(valid_topics, request.num_questions)
    
    return {
        "quiz": questions,
        "topics": valid_topics,
        "generated_by": "gpt-5-mini (FREE)"
    }


@app.post("/api/ai/clear-history")
async def clear_ai_history():
    """Clear the AI tutor's conversation history"""
    ai_tutor = get_ai_tutor()
    ai_tutor.clear_history()
    return {"status": "cleared"}


# ============ Personalized Curriculum (Canvas-scraped + AI-generated) ============

CURRICULUM_FILE = DATA_DIR / "personalized_curriculum.json"

def load_curriculum() -> dict:
    if CURRICULUM_FILE.exists():
        return json.loads(CURRICULUM_FILE.read_text())
    return {}


@app.get("/api/curriculum")
async def get_curriculum():
    """Get curriculum summary. Returns empty state gracefully if not generated yet."""
    curriculum = load_curriculum()
    if not curriculum:
        return {"topics_count": 0, "total_topics": 0, "course": "", "generated_at": None, "ready": False}
    return {**curriculum, "topics_count": len(curriculum.get("topics", [])), "ready": True}


@app.get("/api/curriculum/topics")
async def get_curriculum_topics():
    """Get topic list with metadata (no full lesson content). Returns empty list if not ready."""
    curriculum = load_curriculum()
    if not curriculum:
        return {"topics": [], "course": "", "generated_at": None, "scrape_status": None}
    topics = []
    for t in curriculum.get("topics", []):
        topics.append({
            "id": t.get("id"),
            "section_id": t.get("section_id", ""),
            "title": t.get("title"),
            "calc_level": t.get("calc_level", 2),
            "order": t.get("order", 0),
            "description": t.get("description", ""),
            "concept_count": len(t.get("concepts", [])),
            "problem_count": len(t.get("practice_problems", [])),
        })
    return {"topics": topics, "course": curriculum.get("course", ""), "generated_at": curriculum.get("generated_at", "")}


@app.get("/api/curriculum/topic/{topic_id}")
async def get_curriculum_topic(topic_id: str):
    """Get full lesson for one topic"""
    curriculum = load_curriculum()
    for t in curriculum.get("topics", []):
        if t.get("id") == topic_id:
            return t
    raise HTTPException(status_code=404, detail=f"Topic '{topic_id}' not found in curriculum")


@app.get("/api/curriculum/topic/{topic_id}/problems")
async def get_curriculum_problems(topic_id: str):
    """Get just the practice problems + walkthroughs for a topic"""
    curriculum = load_curriculum()
    for t in curriculum.get("topics", []):
        if t.get("id") == topic_id:
            return {"topic_id": topic_id, "problems": t.get("practice_problems", [])}
    raise HTTPException(status_code=404, detail="Topic not found")


@app.get("/api/curriculum/topic/{topic_id}/problem/{problem_index}/walkthrough")
async def get_curriculum_walkthrough(topic_id: str, problem_index: int):
    """Get the walkthrough for a specific problem"""
    curriculum = load_curriculum()
    for t in curriculum.get("topics", []):
        if t.get("id") == topic_id:
            problems = t.get("practice_problems", [])
            if 0 <= problem_index < len(problems):
                prob = problems[problem_index]
                return {
                    "topic_id": topic_id,
                    "problem_index": problem_index,
                    "question": prob.get("question",""),
                    "answer": prob.get("answer",""),
                    "walkthrough": prob.get("walkthrough", []),
                    "total_steps": len(prob.get("walkthrough", [])),
                }
            raise HTTPException(status_code=404, detail="Problem index out of range")
    raise HTTPException(status_code=404, detail="Topic not found")



def _generate_topic_lesson(topic_id: str, topic_title: str) -> dict:
    """Call Copilot CLI gpt-5-mini to generate a from-scratch lesson. Raises on failure so caller doesn't cache bad content."""
    prompt = (
        f"You are a calculus tutor teaching a student who only knows high school algebra.\n"
        f"Teach: {topic_id} - {topic_title}\n\n"
        "IMPORTANT: All mathematical expressions MUST use LaTeX wrapped in dollar-sign "
        "delimiters: $...$ for inline math, $$...$$ for display math. "
        "For example: $\\int x\\,dx$, $$\\frac{d}{dx}[f(g(x))] = f'(g(x)) \\cdot g'(x)$$\n\n"
        "Output ONLY a JSON object with this exact structure (no markdown, no explanation):\n"
        "{\n"
        '  "description": "one sentence overview",\n'
        '  "key_formula": "main formula in LaTeX with $$...$$ delimiters",\n'
        '  "concepts": [\n'
        '    {"title": "concept name", "explanation": "teach it from scratch in 2-3 sentences (use $...$ for inline math)", "formula": "LaTeX with $$...$$ delimiters, or empty string", "example": "fully worked example (use $...$ for inline math)"}\n'
        "  ],\n"
        '  "practice_problems": [\n'
        '    {"question": "problem text (use $...$ for math)", "answer": "the answer", "difficulty": "easy",\n'
        '      "walkthrough": [{"step": 1, "title": "step name", "content": "explanation (use $...$ for math)", "formula": "LaTeX with $$...$$ or empty string"}]}\n'
        "  ]\n"
        "}\n\n"
        "Include 4 concepts and 3 problems (easy, medium, hard). "
        "Each problem needs 4+ walkthrough steps. Output ONLY the JSON."
    )
    result = subprocess.run(
        ["copilot", "-p", prompt, "--model", "gpt-5-mini", "-s"],
        capture_output=True, text=True, timeout=300
    )
    raw = result.stdout.strip()
    if not raw:
        raise RuntimeError(f"Empty response from Copilot CLI for {topic_id}")
    # Strip markdown fences if present
    if "```" in raw:
        for part in raw.split("```"):
            part = part.strip().lstrip("json").strip()
            if part.startswith("{"):
                raw = part
                break
    parsed = json.loads(raw)
    # Validate we got real content, not a stub
    if len(parsed.get("concepts", [])) < 2:
        raise RuntimeError(f"Insufficient content generated for {topic_id}: only {len(parsed.get('concepts', []))} concepts")
    return parsed


@app.post("/api/curriculum/topic/{topic_id}/generate")
async def generate_curriculum_topic(topic_id: str, force: bool = False):
    """
    On-demand lesson generation. First call generates via gpt-5-mini (~90s).
    Cached permanently — subsequent calls return instantly.
    Pass ?force=true to regenerate even if already cached.
    """
    curriculum = load_curriculum()
    if not curriculum:
        raise HTTPException(status_code=503, detail="Curriculum file not found.")

    topics = curriculum.get("topics", [])
    idx = next((i for i, t in enumerate(topics) if t.get("id") == topic_id), None)
    if idx is None:
        raise HTTPException(status_code=404, detail=f"Topic '{topic_id}' not found in curriculum")

    topic = topics[idx]

    # Cache hit — already generated with real content
    if topic.get("generated") and not force:
        return topic

    # Generate content — raises on failure so we don't cache bad data
    try:
        content = _generate_topic_lesson(topic_id, topic.get("title", topic_id))
    except Exception as e:
        print(f"Lesson generation failed for {topic_id}: {e}")
        raise HTTPException(status_code=503, detail=f"AI generation failed: {e}. Try again in a moment.")

    # Merge into topic record and cache permanently
    topic.update({
        "generated": True,
        "generated_at": datetime.now().isoformat(),
        "description": content.get("description", ""),
        "key_formula": content.get("key_formula", ""),
        "concepts": content.get("concepts", []),
        "practice_problems": content.get("practice_problems", []),
    })

    curriculum["topics"][idx] = topic
    CURRICULUM_FILE.write_text(json.dumps(curriculum, indent=2))
    return topic


@app.post("/api/curriculum/scrape")
async def trigger_canvas_scrape(background_tasks: BackgroundTasks):
    """
    Trigger a Canvas scrape + AI curriculum build.
    Opens Chrome, scrapes Canvas, builds personalized curriculum.
    This runs in the background — poll /api/curriculum/scrape/status for progress.
    """
    scrape_status_file = DATA_DIR / "scrape_status.json"
    scrape_status_file.write_text(json.dumps({"status": "running", "started_at": datetime.now().isoformat()}))

    async def run_scraper():
        import subprocess
        scraper_path = Path(__file__).parent / "canvas_scraper.py"
        result = subprocess.run(
            ["python3", str(scraper_path)],
            capture_output=True, text=True
        )
        status = {
            "status": "complete" if result.returncode == 0 else "error",
            "finished_at": datetime.now().isoformat(),
            "output": result.stdout[-2000:],
            "error": result.stderr[-1000:] if result.returncode != 0 else "",
        }
        scrape_status_file.write_text(json.dumps(status))

    background_tasks.add_task(run_scraper)
    return {"status": "started", "message": "Canvas scraper launched. Check /api/curriculum/scrape/status for progress."}


@app.get("/api/curriculum/scrape/status")
async def get_scrape_status():
    """Check scraper progress"""
    status_file = DATA_DIR / "scrape_status.json"
    if not status_file.exists():
        return {"status": "idle"}
    return json.loads(status_file.read_text())


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
