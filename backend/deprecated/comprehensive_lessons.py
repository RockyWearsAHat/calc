"""
Deep Teaching Content for Calculus II
Comprehensive lessons with theory, worked examples, and intuition
"""

DEEP_LESSONS = {
    "integration_by_parts": {
        "title": "Integration by Parts",
        "subtitle": "Turning Products into Manageable Pieces",
        "estimated_time": "45 minutes",
        "prerequisites": ["Basic integration", "Product rule for derivatives"],
        
        "big_idea": """
**The Core Insight:** Integration by parts is the product rule in reverse. When you see
an integral of a PRODUCT of two different types of functions, this technique lets you 
"transfer" the derivative from one function to the other.

Think of it like a see-saw: one function goes UP (gets integrated) while the other goes 
DOWN (gets differentiated). The goal is to make the resulting integral SIMPLER than 
what you started with.
""",
        
        "formula": {
            "main": "$$\\int u \\, dv = uv - \\int v \\, du$$",
            "derivation": """
**Where does this come from?**

Start with the product rule: $(uv)' = u'v + uv'$

Integrate both sides: $\\int (uv)' = \\int u'v + \\int uv'$

The left side is just $uv$, so: $uv = \\int u'v + \\int uv'$

Rearrange: $\\boxed{\\int uv' = uv - \\int u'v}$

Or in differential notation: $\\int u \\, dv = uv - \\int v \\, du$
"""
        },
        
        "key_technique": {
            "name": "LIATE Rule",
            "explanation": """
**How to Choose u:** Pick $u$ to be the function that gets SIMPLER when differentiated.
Use this priority order (LIATE):

| Priority | Type | Examples | Why? |
|----------|------|----------|------|
| 1st | **L**ogarithmic | $\\ln x$, $\\log x$ | Differentiates to algebraic |
| 2nd | **I**nverse trig | $\\arctan x$, $\\arcsin x$ | Differentiates to algebraic |
| 3rd | **A**lgebraic | $x$, $x^2$, polynomials | Gets simpler each time |
| 4th | **T**rigonometric | $\\sin x$, $\\cos x$ | Cycles, doesn't simplify |
| 5th | **E**xponential | $e^x$, $2^x$ | Stays the same |

**The function higher on the list becomes $u$; the other becomes $dv$.**
"""
        },
        
        "worked_examples": [
            {
                "problem": "Evaluate $\\int x e^x \\, dx$",
                "difficulty": 1,
                "steps": [
                    {
                        "title": "Identify & Choose",
                        "content": """
We have a product: $x$ (algebraic) × $e^x$ (exponential)

Using LIATE: Algebraic > Exponential, so:
- Let $u = x$ (will simplify when differentiated)
- Let $dv = e^x \\, dx$ (easy to integrate)
"""
                    },
                    {
                        "title": "Find du and v",
                        "content": """
$u = x \\implies du = dx$

$dv = e^x \\, dx \\implies v = e^x$
"""
                    },
                    {
                        "title": "Apply the Formula",
                        "content": """
$$\\int u \\, dv = uv - \\int v \\, du$$

$$\\int x e^x \\, dx = (x)(e^x) - \\int (e^x)(dx)$$

$$= xe^x - \\int e^x \\, dx$$
"""
                    },
                    {
                        "title": "Evaluate Remaining Integral",
                        "content": """
$$= xe^x - e^x + C$$

$$= e^x(x - 1) + C$$
"""
                    },
                    {
                        "title": "Verify (Optional but Smart!)",
                        "content": """
Check: $\\frac{d}{dx}[e^x(x-1)] = e^x(x-1) + e^x(1) = e^x \\cdot x - e^x + e^x = xe^x$ ✓
"""
                    }
                ]
            },
            {
                "problem": "Evaluate $\\int x^2 \\cos x \\, dx$",
                "difficulty": 2,
                "steps": [
                    {
                        "title": "Identify - Need IBP Twice!",
                        "content": """
Product: $x^2$ (algebraic) × $\\cos x$ (trig)

LIATE says: $u = x^2$, $dv = \\cos x \\, dx$

Note: We'll need to do IBP twice because $x^2$ differentiates to $2x$, then $2$.
"""
                    },
                    {
                        "title": "First IBP",
                        "content": """
$u = x^2 \\implies du = 2x \\, dx$
$dv = \\cos x \\, dx \\implies v = \\sin x$

$$\\int x^2 \\cos x \\, dx = x^2 \\sin x - \\int 2x \\sin x \\, dx$$
"""
                    },
                    {
                        "title": "Second IBP (for the remaining integral)",
                        "content": """
For $\\int 2x \\sin x \\, dx$:
- $u = 2x \\implies du = 2 \\, dx$
- $dv = \\sin x \\, dx \\implies v = -\\cos x$

$$\\int 2x \\sin x \\, dx = -2x\\cos x - \\int -2\\cos x \\, dx$$
$$= -2x\\cos x + 2\\sin x$$
"""
                    },
                    {
                        "title": "Combine Everything",
                        "content": """
$$\\int x^2 \\cos x \\, dx = x^2 \\sin x - (-2x\\cos x + 2\\sin x) + C$$

$$= x^2 \\sin x + 2x\\cos x - 2\\sin x + C$$

$$= \\boxed{(x^2 - 2)\\sin x + 2x\\cos x + C}$$
"""
                    }
                ]
            },
            {
                "problem": "Evaluate $\\int e^x \\sin x \\, dx$ (Circular IBP)",
                "difficulty": 3,
                "steps": [
                    {
                        "title": "The Setup - This One's Tricky!",
                        "content": """
Product: $e^x$ × $\\sin x$ — both are at the same LIATE level!

Neither function simplifies when differentiated. We'll use a clever trick:
do IBP twice and solve algebraically.

First IBP: $u = e^x$, $dv = \\sin x \\, dx$
"""
                    },
                    {
                        "title": "First IBP",
                        "content": """
$u = e^x \\implies du = e^x \\, dx$
$dv = \\sin x \\, dx \\implies v = -\\cos x$

$$I = \\int e^x \\sin x \\, dx = -e^x \\cos x - \\int -e^x \\cos x \\, dx$$

$$I = -e^x \\cos x + \\int e^x \\cos x \\, dx$$
"""
                    },
                    {
                        "title": "Second IBP (same choice pattern)",
                        "content": """
For $\\int e^x \\cos x \\, dx$:
- $u = e^x \\implies du = e^x \\, dx$
- $dv = \\cos x \\, dx \\implies v = \\sin x$

$$\\int e^x \\cos x \\, dx = e^x \\sin x - \\int e^x \\sin x \\, dx$$
"""
                    },
                    {
                        "title": "The Magic - Solve for I",
                        "content": """
Substitute back:
$$I = -e^x \\cos x + e^x \\sin x - I$$

$$2I = e^x(\\sin x - \\cos x)$$

$$I = \\boxed{\\frac{e^x}{2}(\\sin x - \\cos x) + C}$$

**Key insight:** When IBP brings you back to the original integral, solve algebraically!
"""
                    }
                ]
            }
        ],
        
        "common_mistakes": [
            {
                "mistake": "Choosing u and dv backwards",
                "why_wrong": "If u gets more complicated when differentiated, the resulting integral will be harder, not easier",
                "how_to_fix": "Always use LIATE. The function higher on the list should be u."
            },
            {
                "mistake": "Forgetting the negative sign in the formula",
                "why_wrong": "The formula is uv MINUS ∫v du, not plus",
                "how_to_fix": "Write out the formula every time until it's automatic"
            },
            {
                "mistake": "Stopping too early with circular IBP",
                "why_wrong": "When the original integral reappears, students often think they made an error",
                "how_to_fix": "Call the integral I, then solve the equation for I"
            }
        ],
        
        "practice_problems": [
            {"problem": "$\\int x \\sin x \\, dx$", "answer": "$-x\\cos x + \\sin x + C$", "difficulty": 1},
            {"problem": "$\\int \\ln x \\, dx$", "answer": "$x \\ln x - x + C$", "difficulty": 1},
            {"problem": "$\\int x^2 e^x \\, dx$", "answer": "$e^x(x^2 - 2x + 2) + C$", "difficulty": 2},
            {"problem": "$\\int x \\arctan x \\, dx$", "answer": "$\\frac{x^2}{2}\\arctan x - \\frac{x}{2} + \\frac{1}{2}\\arctan x + C$", "difficulty": 3},
            {"problem": "$\\int e^x \\cos x \\, dx$", "answer": "$\\frac{e^x}{2}(\\sin x + \\cos x) + C$", "difficulty": 3}
        ],
        
        "when_to_use": [
            "Product of polynomial and exponential: $x^n e^{ax}$",
            "Product of polynomial and trig: $x^n \\sin(ax)$ or $x^n \\cos(ax)$",
            "Product of polynomial and logarithm: $x^n \\ln x$",
            "Logarithm alone: $\\ln x$, $\\arctan x$, $\\arcsin x$ (use dv = dx)",
            "Product of exponential and trig: $e^{ax}\\sin(bx)$ or $e^{ax}\\cos(bx)$"
        ],
        
        "connections": [
            "This technique appears again in solving differential equations",
            "The tabular method (for repeated IBP) is a shortcut worth learning",
            "Integration by parts relates to the Laplace transform"
        ]
    },
    
    "partial_fractions": {
        "title": "Partial Fraction Decomposition",
        "subtitle": "Breaking Down Complex Fractions",
        "estimated_time": "50 minutes",
        "prerequisites": ["Polynomial factoring", "Basic integration of 1/x and 1/(x-a)"],
        
        "big_idea": """
**The Core Insight:** Any complicated rational function can be broken into a sum of 
simple fractions that are easy to integrate individually.

It's like breaking down a complex LEGO structure into individual blocks — each piece 
is simple, and together they form the whole.
""",
        
        "formula": {
            "main": "$$\\frac{P(x)}{Q(x)} = \\text{sum of simple fractions}$$",
            "derivation": """
**The Decomposition Rules:**

| Denominator Factor | Decomposition |
|-------------------|---------------|
| $(x - a)$ | $\\frac{A}{x-a}$ |
| $(x - a)^2$ | $\\frac{A}{x-a} + \\frac{B}{(x-a)^2}$ |
| $(x - a)^n$ | $\\frac{A_1}{x-a} + \\frac{A_2}{(x-a)^2} + ... + \\frac{A_n}{(x-a)^n}$ |
| $(x^2 + bx + c)$ irreducible | $\\frac{Ax + B}{x^2 + bx + c}$ |
| $(x^2 + bx + c)^2$ irreducible | $\\frac{Ax + B}{x^2 + bx + c} + \\frac{Cx + D}{(x^2 + bx + c)^2}$ |

**Important:** Degree of numerator must be < degree of denominator. If not, do polynomial long division first!
"""
        },
        
        "key_technique": {
            "name": "Strategic Substitution",
            "explanation": """
**Two Methods to Find Constants:**

**Method 1: Strategic Values**
- Plug in x-values that make factors zero
- Each value eliminates most terms, leaving one constant

**Method 2: Coefficient Matching**
- Expand and collect like terms
- Match coefficients of each power of x
- Solve the resulting system of equations

**Pro tip:** Use strategic values first for linear factors, then coefficient matching for leftovers.
"""
        },
        
        "worked_examples": [
            {
                "problem": "Evaluate $\\int \\frac{1}{x^2 - 1} \\, dx$",
                "difficulty": 1,
                "steps": [
                    {
                        "title": "Factor the Denominator",
                        "content": """
$$x^2 - 1 = (x-1)(x+1)$$

This is a difference of squares — a must-know factorization!
"""
                    },
                    {
                        "title": "Set Up Partial Fractions",
                        "content": """
$$\\frac{1}{(x-1)(x+1)} = \\frac{A}{x-1} + \\frac{B}{x+1}$$

Two distinct linear factors = two simple fractions.
"""
                    },
                    {
                        "title": "Find Constants - Strategic Substitution",
                        "content": """
Multiply both sides by $(x-1)(x+1)$:
$$1 = A(x+1) + B(x-1)$$

**Let $x = 1$:** $1 = A(2) + B(0) \\implies A = 1/2$

**Let $x = -1$:** $1 = A(0) + B(-2) \\implies B = -1/2$
"""
                    },
                    {
                        "title": "Integrate",
                        "content": """
$$\\int \\frac{1}{x^2-1} dx = \\int \\frac{1/2}{x-1} dx + \\int \\frac{-1/2}{x+1} dx$$

$$= \\frac{1}{2}\\ln|x-1| - \\frac{1}{2}\\ln|x+1| + C$$

$$= \\boxed{\\frac{1}{2}\\ln\\left|\\frac{x-1}{x+1}\\right| + C}$$
"""
                    }
                ]
            },
            {
                "problem": "Evaluate $\\int \\frac{x+5}{(x-1)^2} \\, dx$",
                "difficulty": 2,
                "steps": [
                    {
                        "title": "Set Up - Repeated Linear Factor",
                        "content": """
$(x-1)^2$ is a repeated linear factor, so:

$$\\frac{x+5}{(x-1)^2} = \\frac{A}{x-1} + \\frac{B}{(x-1)^2}$$
"""
                    },
                    {
                        "title": "Find Constants",
                        "content": """
Multiply by $(x-1)^2$:
$$x + 5 = A(x-1) + B$$

**Let $x = 1$:** $6 = B$

**Compare x-coefficients:** $1 = A$

So $A = 1$, $B = 6$.
"""
                    },
                    {
                        "title": "Integrate",
                        "content": """
$$\\int \\frac{x+5}{(x-1)^2} dx = \\int \\frac{1}{x-1} dx + \\int \\frac{6}{(x-1)^2} dx$$

$$= \\ln|x-1| + 6 \\cdot \\frac{(x-1)^{-1}}{-1} + C$$

$$= \\boxed{\\ln|x-1| - \\frac{6}{x-1} + C}$$
"""
                    }
                ]
            }
        ],
        
        "common_mistakes": [
            {
                "mistake": "Forgetting to check degree of numerator",
                "why_wrong": "If numerator degree ≥ denominator degree, you must do long division first",
                "how_to_fix": "Always compare degrees before starting decomposition"
            },
            {
                "mistake": "Wrong decomposition for repeated factors",
                "why_wrong": "$(x-1)^2$ needs TWO terms: $\\frac{A}{x-1} + \\frac{B}{(x-1)^2}$",
                "how_to_fix": "For $(x-a)^n$, include ALL powers from 1 to n"
            },
            {
                "mistake": "Using just constants for irreducible quadratics",
                "why_wrong": "$(x^2+1)$ in denominator needs $\\frac{Ax+B}{x^2+1}$, not just $\\frac{A}{x^2+1}$",
                "how_to_fix": "Irreducible quadratic = linear numerator"
            }
        ],
        
        "practice_problems": [
            {"problem": "$\\int \\frac{3}{x^2-9} dx$", "answer": "$\\frac{1}{2}\\ln|\\frac{x-3}{x+3}| + C$", "difficulty": 1},
            {"problem": "$\\int \\frac{2x+1}{x^2+x-2} dx$", "answer": "$\\ln|(x-1)(x+2)| + C$", "difficulty": 2},
            {"problem": "$\\int \\frac{x^2+1}{x(x-1)^2} dx$", "answer": "partial fractions required", "difficulty": 3}
        ],
        
        "when_to_use": [
            "Rational functions (polynomial ÷ polynomial)",
            "After making a substitution that results in a rational function",
            "When the denominator can be factored"
        ]
    },
    
    "series_convergence": {
        "title": "Series Convergence Tests",
        "subtitle": "Does the Sum Have a Limit?",
        "estimated_time": "60 minutes",
        "prerequisites": ["Limits", "L'Hôpital's Rule", "Basic sequences"],
        
        "big_idea": """
**The Core Question:** When you add infinitely many terms, does the sum approach a finite 
number (converge) or grow without bound (diverge)?

$$\\sum_{n=1}^{\\infty} a_n = a_1 + a_2 + a_3 + ... = ???$$

Different series behave differently. We have a toolkit of tests to determine convergence.
""",
        
        "formula": {
            "main": "Tests summarized below",
            "derivation": """
**The Master Flowchart:**

```
START → Does lim(aₙ) = 0?
         ↓ No → DIVERGES (Divergence Test)
         ↓ Yes → Continue testing...
         
Is it a special form?
├─ 1/nᵖ → p-series test
├─ arⁿ → geometric series  
├─ Has factorials or nth powers → Ratio or Root Test
├─ Looks like another series → Comparison Test
└─ Positive decreasing function → Integral Test
```
"""
        },
        
        "key_technique": {
            "name": "Test Selection Guide",
            "explanation": """
**Quick Reference:**

| Series Form | Best Test | Converges When |
|-------------|-----------|----------------|
| $\\sum \\frac{1}{n^p}$ | p-series | $p > 1$ |
| $\\sum ar^n$ | Geometric | $|r| < 1$ |
| $\\sum \\frac{n!}{...}$ or $\\sum \\frac{a^n}{...}$ | Ratio Test | Limit $< 1$ |
| $\\sum (...)^n$ | Root Test | Limit $< 1$ |
| $\\sum a_n$ where $a_n \\sim b_n$ | Limit Comparison | Compare to known series |
| Alternating $\\sum (-1)^n b_n$ | Alternating Series | $b_n \\downarrow 0$ |
| $\\sum f(n)$ where f is continuous | Integral Test | Integral converges |
"""
        },
        
        "worked_examples": [
            {
                "problem": "Does $\\sum_{n=1}^{\\infty} \\frac{n}{2^n}$ converge?",
                "difficulty": 2,
                "steps": [
                    {
                        "title": "Check Divergence Test First",
                        "content": """
$$\\lim_{n \\to \\infty} \\frac{n}{2^n} = 0$$ (exponential beats polynomial)

The test is inconclusive (limit = 0 doesn't prove convergence).
"""
                    },
                    {
                        "title": "Choose a Test",
                        "content": """
We have $2^n$ in the denominator — this suggests the **Ratio Test**.

$$L = \\lim_{n \\to \\infty} \\left| \\frac{a_{n+1}}{a_n} \\right|$$
"""
                    },
                    {
                        "title": "Apply Ratio Test",
                        "content": """
$$L = \\lim_{n \\to \\infty} \\frac{(n+1)/2^{n+1}}{n/2^n}$$

$$= \\lim_{n \\to \\infty} \\frac{n+1}{2^{n+1}} \\cdot \\frac{2^n}{n}$$

$$= \\lim_{n \\to \\infty} \\frac{n+1}{2n} = \\frac{1}{2}$$
"""
                    },
                    {
                        "title": "Conclude",
                        "content": """
Since $L = \\frac{1}{2} < 1$, the series **CONVERGES** by the Ratio Test.
"""
                    }
                ]
            }
        ],
        
        "common_mistakes": [
            {
                "mistake": "Using Divergence Test to prove convergence",
                "why_wrong": "lim(aₙ) = 0 does NOT mean the series converges (counterexample: harmonic series)",
                "how_to_fix": "Divergence Test only proves divergence (when limit ≠ 0)"
            },
            {
                "mistake": "Wrong conclusion when Ratio/Root Test gives L = 1",
                "why_wrong": "L = 1 is INCONCLUSIVE — you must try a different test",
                "how_to_fix": "When L = 1, state 'inconclusive' and try another approach"
            }
        ],
        
        "practice_problems": [
            {"problem": "$\\sum_{n=1}^{\\infty} \\frac{1}{n^3}$", "answer": "Converges (p-series, p=3>1)", "difficulty": 1},
            {"problem": "$\\sum_{n=1}^{\\infty} \\frac{n!}{n^n}$", "answer": "Converges (Ratio Test)", "difficulty": 2},
            {"problem": "$\\sum_{n=2}^{\\infty} \\frac{1}{n\\ln n}$", "answer": "Diverges (Integral Test)", "difficulty": 2}
        ]
    },
    
    "taylor_maclaurin": {
        "title": "Taylor and Maclaurin Series",
        "subtitle": "Polynomials That Approximate Anything",
        "estimated_time": "55 minutes",
        "prerequisites": ["Derivatives", "Series basics"],
        
        "big_idea": """
**The Core Insight:** ANY smooth function can be represented as an infinite polynomial!

This is incredibly powerful — polynomials are easy to work with, so we can use them to 
approximate complex functions, evaluate impossible integrals, and find limits.
""",
        
        "formula": {
            "main": "$$f(x) = \\sum_{n=0}^{\\infty} \\frac{f^{(n)}(a)}{n!}(x-a)^n$$",
            "derivation": """
**Maclaurin Series (centered at 0):**
$$f(x) = f(0) + f'(0)x + \\frac{f''(0)}{2!}x^2 + \\frac{f'''(0)}{3!}x^3 + ...$$

**Must Memorize These:**

| Function | Series | Valid for |
|----------|--------|-----------|
| $e^x$ | $1 + x + \\frac{x^2}{2!} + \\frac{x^3}{3!} + ...$ | All $x$ |
| $\\sin x$ | $x - \\frac{x^3}{3!} + \\frac{x^5}{5!} - ...$ | All $x$ |
| $\\cos x$ | $1 - \\frac{x^2}{2!} + \\frac{x^4}{4!} - ...$ | All $x$ |
| $\\frac{1}{1-x}$ | $1 + x + x^2 + x^3 + ...$ | $|x| < 1$ |
| $\\ln(1+x)$ | $x - \\frac{x^2}{2} + \\frac{x^3}{3} - ...$ | $-1 < x \\leq 1$ |
"""
        },
        
        "worked_examples": [
            {
                "problem": "Find the Maclaurin series for $f(x) = e^{-x^2}$",
                "difficulty": 2,
                "steps": [
                    {
                        "title": "Start with Known Series",
                        "content": """
We know: $e^u = 1 + u + \\frac{u^2}{2!} + \\frac{u^3}{3!} + ...$

Let $u = -x^2$:
"""
                    },
                    {
                        "title": "Substitute",
                        "content": """
$$e^{-x^2} = 1 + (-x^2) + \\frac{(-x^2)^2}{2!} + \\frac{(-x^2)^3}{3!} + ...$$

$$= 1 - x^2 + \\frac{x^4}{2!} - \\frac{x^6}{3!} + ...$$

$$= \\boxed{\\sum_{n=0}^{\\infty} \\frac{(-1)^n x^{2n}}{n!}}$$
"""
                    }
                ]
            }
        ],
        
        "common_mistakes": [
            {
                "mistake": "Forgetting the n! in denominator",
                "why_wrong": "The factorial is crucial — it makes the series converge",
                "how_to_fix": "Taylor formula: coefficient of $(x-a)^n$ is $\\frac{f^{(n)}(a)}{n!}$"
            }
        ],
        
        "practice_problems": [
            {"problem": "Maclaurin series for $\\sin(x^2)$", "answer": "$x^2 - \\frac{x^6}{3!} + \\frac{x^{10}}{5!} - ...$", "difficulty": 2},
            {"problem": "Maclaurin series for $\\frac{1}{1+x^2}$", "answer": "$1 - x^2 + x^4 - x^6 + ...$", "difficulty": 2}
        ]
    },
    
    "improper_integrals": {
        "title": "Improper Integrals",
        "subtitle": "Integrating to Infinity and Beyond",
        "estimated_time": "40 minutes",
        "prerequisites": ["Definite integrals", "Limits"],
        
        "big_idea": """
**The Core Insight:** We can extend integration to infinite intervals or functions with 
discontinuities by using LIMITS.

**Type 1:** Infinite limits of integration: $\\int_a^{\\infty}$ or $\\int_{-\\infty}^b$

**Type 2:** Discontinuous integrand: integral where $f(x) \\to \\infty$ at some point
""",
        
        "formula": {
            "main": "$$\\int_a^{\\infty} f(x)\\,dx = \\lim_{t \\to \\infty} \\int_a^t f(x)\\,dx$$",
            "derivation": """
**Type 1 (Infinite Bounds):**
$$\\int_a^{\\infty} f(x)dx = \\lim_{t \\to \\infty} \\int_a^t f(x)dx$$

**Type 2 (Discontinuity at b):**
$$\\int_a^b f(x)dx = \\lim_{t \\to b^-} \\int_a^t f(x)dx$$

**Key p-integral:**
$$\\int_1^{\\infty} \\frac{1}{x^p} dx = \\begin{cases} \\frac{1}{p-1} & p > 1 \\text{ (converges)} \\\\ \\infty & p \\leq 1 \\text{ (diverges)} \\end{cases}$$
"""
        },
        
        "worked_examples": [
            {
                "problem": "Evaluate $\\int_1^{\\infty} \\frac{1}{x^2} dx$",
                "difficulty": 1,
                "steps": [
                    {
                        "title": "Set Up the Limit",
                        "content": """
$$\\int_1^{\\infty} \\frac{1}{x^2} dx = \\lim_{t \\to \\infty} \\int_1^t x^{-2} dx$$
"""
                    },
                    {
                        "title": "Integrate",
                        "content": """
$$= \\lim_{t \\to \\infty} \\left[ \\frac{x^{-1}}{-1} \\right]_1^t = \\lim_{t \\to \\infty} \\left[ -\\frac{1}{x} \\right]_1^t$$

$$= \\lim_{t \\to \\infty} \\left( -\\frac{1}{t} + 1 \\right)$$
"""
                    },
                    {
                        "title": "Evaluate the Limit",
                        "content": """
$$= 0 + 1 = \\boxed{1}$$

The integral **converges** to 1.
"""
                    }
                ]
            }
        ],
        
        "common_mistakes": [
            {
                "mistake": "Not using limits",
                "why_wrong": "You can't just plug in ∞ — you must take a limit",
                "how_to_fix": "Always write $\\lim_{t \\to \\infty}$ explicitly"
            }
        ],
        
        "practice_problems": [
            {"problem": "$\\int_0^{\\infty} e^{-x} dx$", "answer": "1 (converges)", "difficulty": 1},
            {"problem": "$\\int_1^{\\infty} \\frac{1}{x} dx$", "answer": "Diverges", "difficulty": 1}
        ]
    }
}

# Helper function to get lesson
def get_lesson(topic: str) -> dict:
    """Get a deep lesson by topic ID"""
    return DEEP_LESSONS.get(topic, None)

def get_all_topics() -> list:
    """Get list of all available topics"""
    return [
        {"id": k, "title": v["title"], "subtitle": v["subtitle"], "time": v["estimated_time"]}
        for k, v in DEEP_LESSONS.items()
    ]
