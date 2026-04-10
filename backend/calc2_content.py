"""
Comprehensive Calculus II Content - Based on Stewart's Calculus
Covers all topics for MATH 1220 Calculus II Final Exam
"""

CALC2_CONTENT = {
    "integration_by_parts": {
        "title": "Integration by Parts",
        "description": "The product rule for integration - essential technique for Calc II",
        "priority": "HIGH",
        "concepts": [
            {
                "name": "The Integration by Parts Formula",
                "explanation": """Integration by parts is derived from the product rule for derivatives.

**The Formula:**
∫u dv = uv - ∫v du

**How to Choose u and v:**
Use the LIATE rule (choose u in this order):
• **L**ogarithmic functions (ln x, log x)
• **I**nverse trig functions (arctan x, arcsin x)
• **A**lgebraic functions (x², x³, polynomials)
• **T**rigonometric functions (sin x, cos x)
• **E**xponential functions (eˣ, 2ˣ)

**The one LOWER on the list becomes dv.**

**Step-by-Step Process:**
1. Identify u and dv from the integrand
2. Compute du (differentiate u)
3. Compute v (integrate dv)
4. Apply the formula: uv - ∫v du
5. Solve the new integral (may need to repeat)""",
                "formula": "\\int u \\, dv = uv - \\int v \\, du",
                "examples": [
                    {
                        "problem": "∫x·eˣ dx",
                        "solution": """Let u = x, dv = eˣ dx
Then du = dx, v = eˣ

∫x·eˣ dx = x·eˣ - ∫eˣ dx
         = x·eˣ - eˣ + C
         = eˣ(x - 1) + C"""
                    },
                    {
                        "problem": "∫ln(x) dx",
                        "solution": """Let u = ln(x), dv = dx
Then du = 1/x dx, v = x

∫ln(x) dx = x·ln(x) - ∫x·(1/x) dx
          = x·ln(x) - ∫1 dx
          = x·ln(x) - x + C
          = x(ln(x) - 1) + C"""
                    }
                ]
            },
            {
                "name": "Tabular Integration (Repeated IBP)",
                "explanation": """When integrating a polynomial times eˣ or sin/cos, use the tabular method:

**Setup:**
1. Make a table with derivatives of u on the left
2. Integrals of dv on the right
3. Alternate + and - signs
4. Multiply diagonally and add

**Example: ∫x³·eˣ dx**

| Signs | u (and derivatives) | dv (and integrals) |
|-------|---------------------|-------------------|
|   +   |        x³           |        eˣ         |
|   -   |        3x²          |        eˣ         |
|   +   |        6x           |        eˣ         |
|   -   |        6            |        eˣ         |
|   +   |        0            |        eˣ         |

Result: x³·eˣ - 3x²·eˣ + 6x·eˣ - 6·eˣ + C
      = eˣ(x³ - 3x² + 6x - 6) + C""",
                "formula": "\\int x^n e^x dx = e^x \\sum_{k=0}^{n} (-1)^k \\frac{n!}{(n-k)!} x^{n-k} + C",
            },
            {
                "name": "Cyclic Integration by Parts",
                "explanation": """Sometimes IBP brings you back to the original integral. This is actually useful!

**Example: ∫eˣ·sin(x) dx**

First application:
Let u = eˣ, dv = sin(x) dx
du = eˣ dx, v = -cos(x)

∫eˣ sin(x) dx = -eˣ cos(x) + ∫eˣ cos(x) dx

Second application (on the new integral):
Let u = eˣ, dv = cos(x) dx
du = eˣ dx, v = sin(x)

∫eˣ cos(x) dx = eˣ sin(x) - ∫eˣ sin(x) dx

Substituting back:
∫eˣ sin(x) dx = -eˣ cos(x) + eˣ sin(x) - ∫eˣ sin(x) dx

**Move the integral to the left:**
2∫eˣ sin(x) dx = eˣ(sin(x) - cos(x))

**Solve:**
∫eˣ sin(x) dx = (eˣ/2)(sin(x) - cos(x)) + C""",
                "formula": "\\int e^x \\sin(x) \\, dx = \\frac{e^x}{2}(\\sin x - \\cos x) + C",
            }
        ],
        "practice_problems": [
            {"question": "∫x·cos(x) dx", "answer": "x·sin(x) + cos(x) + C", "hint": "Let u = x, dv = cos(x)dx"},
            {"question": "∫x²·eˣ dx", "answer": "eˣ(x² - 2x + 2) + C", "hint": "Use tabular method or apply IBP twice"},
            {"question": "∫arctan(x) dx", "answer": "x·arctan(x) - (1/2)ln(1+x²) + C", "hint": "Let u = arctan(x), dv = dx"},
            {"question": "∫x·ln(x) dx", "answer": "(x²/2)ln(x) - x²/4 + C", "hint": "Let u = ln(x), dv = x dx"},
            {"question": "∫eˣ·cos(x) dx", "answer": "(eˣ/2)(sin(x) + cos(x)) + C", "hint": "Apply IBP twice and solve for the integral"},
        ]
    },
    
    "partial_fractions": {
        "title": "Partial Fractions",
        "description": "Decomposing rational functions for easier integration",
        "priority": "HIGH",
        "concepts": [
            {
                "name": "When to Use Partial Fractions",
                "explanation": """Use partial fractions when integrating rational functions P(x)/Q(x) where:
1. The degree of P(x) < degree of Q(x) (if not, do polynomial long division first)
2. Q(x) can be factored

**Types of Factors in the Denominator:**

**Case 1: Distinct Linear Factors**
(x - a)(x - b)(x - c)...
Decomposition: A/(x-a) + B/(x-b) + C/(x-c) + ...

**Case 2: Repeated Linear Factors**
(x - a)ⁿ
Decomposition: A₁/(x-a) + A₂/(x-a)² + ... + Aₙ/(x-a)ⁿ

**Case 3: Irreducible Quadratic Factors**
(ax² + bx + c) where b² - 4ac < 0
Decomposition: (Ax + B)/(ax² + bx + c)

**Case 4: Repeated Quadratic Factors**
(ax² + bx + c)ⁿ
Decomposition: Sum of (Aₖx + Bₖ)/(ax² + bx + c)ᵏ for k = 1 to n""",
                "formula": "\\frac{P(x)}{(x-a)(x-b)} = \\frac{A}{x-a} + \\frac{B}{x-b}",
            },
            {
                "name": "Solving for Coefficients",
                "explanation": """**Method 1: Multiply and Compare Coefficients**
1. Multiply both sides by the common denominator
2. Expand and collect like terms
3. Set up equations by matching coefficients
4. Solve the system of equations

**Method 2: Strategic Substitution (Cover-Up Method)**
To find A in A/(x-a), substitute x = a into the remaining expression.

**Example:** Decompose 1/((x-1)(x+2))

1/(x-1)(x+2) = A/(x-1) + B/(x+2)

**Cover-up for A:** Set x = 1
A = 1/(1+2) = 1/3

**Cover-up for B:** Set x = -2
B = 1/(-2-1) = -1/3

**Result:** 1/((x-1)(x+2)) = (1/3)/(x-1) - (1/3)/(x+2)""",
                "formula": "\\frac{1}{(x-a)(x-b)} = \\frac{1}{a-b}\\left(\\frac{1}{x-a} - \\frac{1}{x-b}\\right)",
                "examples": [
                    {
                        "problem": "Decompose: (2x+3)/((x+1)(x-2))",
                        "solution": """(2x+3)/((x+1)(x-2)) = A/(x+1) + B/(x-2)

Cover-up for A (x = -1):
A = (2(-1)+3)/((-1)-2) = 1/(-3) = -1/3

Cover-up for B (x = 2):
B = (2(2)+3)/((2)+1) = 7/3

Result: -1/(3(x+1)) + 7/(3(x-2))"""
                    }
                ]
            },
            {
                "name": "Integrating After Decomposition",
                "explanation": """After decomposition, you'll encounter these standard integrals:

**Linear Factors:**
• ∫A/(x-a) dx = A·ln|x-a| + C

**Repeated Linear Factors:**
• ∫A/(x-a)ⁿ dx = A·(x-a)^(1-n)/(1-n) + C  (n ≠ 1)

**Irreducible Quadratics (completing the square):**
• ∫1/(x²+a²) dx = (1/a)arctan(x/a) + C
• ∫x/(x²+a²) dx = (1/2)ln(x²+a²) + C

**For (Ax+B)/(x²+bx+c):**
Split into: A/2 · 2x+b/(x²+bx+c) + (B-Ab/2) · 1/(x²+bx+c)
First part → ln, second part → arctan after completing square""",
                "formula": "\\int \\frac{1}{x^2 + a^2} \\, dx = \\frac{1}{a}\\arctan\\left(\\frac{x}{a}\\right) + C",
            }
        ],
        "practice_problems": [
            {"question": "∫1/((x-1)(x+1)) dx", "answer": "(1/2)ln|(x-1)/(x+1)| + C", "hint": "Decompose: A/(x-1) + B/(x+1)"},
            {"question": "∫(3x+5)/(x²+4x+3) dx", "answer": "2·ln|x+3| + ln|x+1| + C", "hint": "Factor denominator: (x+1)(x+3)"},
            {"question": "∫1/(x²(x+1)) dx", "answer": "-1/x + ln|x| - ln|x+1| + C", "hint": "Repeated factor: A/x + B/x² + C/(x+1)"},
            {"question": "∫x/((x+1)(x²+1)) dx", "answer": "(1/2)ln(x²+1) - (1/2)ln|x+1| + C", "hint": "A/(x+1) + (Bx+C)/(x²+1)"},
        ]
    },
    
    "improper_integrals": {
        "title": "Improper Integrals",
        "description": "Integrals with infinite limits or discontinuous integrands",
        "priority": "HIGH",
        "concepts": [
            {
                "name": "Type 1: Infinite Limits",
                "explanation": """When the interval of integration extends to infinity.

**Definition:**
∫ₐ^∞ f(x) dx = lim(t→∞) ∫ₐᵗ f(x) dx

∫₋∞^b f(x) dx = lim(t→-∞) ∫ₜᵇ f(x) dx

∫₋∞^∞ f(x) dx = ∫₋∞^c f(x) dx + ∫_c^∞ f(x) dx (for any c)

**Convergence:** The integral **converges** if the limit exists and is finite.
**Divergence:** The integral **diverges** if the limit is infinite or doesn't exist.

**Key Example - The p-integral:**
∫₁^∞ 1/xᵖ dx
• Converges if p > 1 (equals 1/(p-1))
• Diverges if p ≤ 1""",
                "formula": "\\int_1^{\\infty} \\frac{1}{x^p} \\, dx \\text{ converges iff } p > 1",
                "examples": [
                    {
                        "problem": "Evaluate ∫₁^∞ 1/x² dx",
                        "solution": """∫₁^∞ 1/x² dx = lim(t→∞) ∫₁ᵗ x⁻² dx
= lim(t→∞) [-1/x]₁ᵗ
= lim(t→∞) (-1/t - (-1/1))
= lim(t→∞) (1 - 1/t)
= 1

The integral converges to 1."""
                    },
                    {
                        "problem": "Evaluate ∫₁^∞ 1/x dx",
                        "solution": """∫₁^∞ 1/x dx = lim(t→∞) ∫₁ᵗ 1/x dx
= lim(t→∞) [ln|x|]₁ᵗ
= lim(t→∞) (ln(t) - ln(1))
= lim(t→∞) ln(t)
= ∞

The integral diverges."""
                    }
                ]
            },
            {
                "name": "Type 2: Discontinuous Integrands",
                "explanation": """When the integrand has a vertical asymptote in [a,b].

**Asymptote at endpoint a:**
∫ₐᵇ f(x) dx = lim(t→a⁺) ∫ₜᵇ f(x) dx

**Asymptote at endpoint b:**
∫ₐᵇ f(x) dx = lim(t→b⁻) ∫ₐᵗ f(x) dx

**Asymptote at interior point c:**
∫ₐᵇ f(x) dx = ∫ₐᶜ f(x) dx + ∫ᶜᵇ f(x) dx
(Both parts must converge!)

**Key Example:**
∫₀¹ 1/xᵖ dx
• Converges if p < 1
• Diverges if p ≥ 1""",
                "formula": "\\int_0^1 \\frac{1}{x^p} \\, dx \\text{ converges iff } p < 1",
                "examples": [
                    {
                        "problem": "Evaluate ∫₀¹ 1/√x dx",
                        "solution": """Asymptote at x = 0 (p = 1/2 < 1, should converge)

∫₀¹ 1/√x dx = lim(t→0⁺) ∫ₜ¹ x⁻¹/² dx
= lim(t→0⁺) [2x¹/²]ₜ¹
= lim(t→0⁺) (2(1) - 2√t)
= 2 - 0 = 2

The integral converges to 2."""
                    }
                ]
            },
            {
                "name": "Comparison Tests for Improper Integrals",
                "explanation": """When direct evaluation is hard, compare to known integrals.

**Direct Comparison Test:**
For 0 ≤ f(x) ≤ g(x) on [a,∞):
• If ∫ₐ^∞ g(x) dx converges, then ∫ₐ^∞ f(x) dx converges
• If ∫ₐ^∞ f(x) dx diverges, then ∫ₐ^∞ g(x) dx diverges

**Limit Comparison Test:**
If lim(x→∞) f(x)/g(x) = L where 0 < L < ∞, then:
∫ₐ^∞ f(x) dx and ∫ₐ^∞ g(x) dx either both converge or both diverge.

**Common Comparisons:**
• 1/x² converges (p = 2 > 1)
• 1/x diverges (p = 1)
• e⁻ˣ converges very fast
• 1/(x·ln²x) converges for x > e""",
                "formula": "\\text{If } 0 \\leq f(x) \\leq g(x) \\text{ and } \\int g \\text{ converges, then } \\int f \\text{ converges}",
            }
        ],
        "practice_problems": [
            {"question": "Does ∫₁^∞ 1/x³ dx converge?", "answer": "Yes, equals 1/2", "hint": "p = 3 > 1"},
            {"question": "Does ∫₁^∞ 1/√x dx converge?", "answer": "No, diverges", "hint": "p = 1/2 ≤ 1"},
            {"question": "Evaluate ∫₀^∞ e⁻ˣ dx", "answer": "1", "hint": "lim(t→∞) [-e⁻ˣ]₀ᵗ"},
            {"question": "Does ∫₀¹ 1/x² dx converge?", "answer": "No, diverges", "hint": "Type 2: p = 2 ≥ 1 at x = 0"},
            {"question": "Evaluate ∫₀^∞ xe⁻ˣ dx", "answer": "1", "hint": "Use integration by parts"},
        ]
    },
    
    "series_strategy": {
        "title": "Series Convergence Strategy",
        "description": "Master all convergence tests and know when to use each",
        "priority": "HIGH",
        "concepts": [
            {
                "name": "The Convergence Test Flowchart",
                "explanation": """**Step 1: Check the Divergence Test first!**
If lim(n→∞) aₙ ≠ 0, the series DIVERGES. Stop here.
(But if the limit IS 0, the test is inconclusive - continue to Step 2)

**Step 2: Identify the series type**

**Geometric Series:** Σarⁿ
• Converges if |r| < 1 (sum = a/(1-r))
• Diverges if |r| ≥ 1

**p-Series:** Σ1/nᵖ
• Converges if p > 1
• Diverges if p ≤ 1

**Step 3: Choose the right test based on form**

**Contains factorial (n!) or exponentials (aⁿ)?** → Ratio Test

**Contains n-th powers?** → Root Test

**Looks like a p-series or geometric?** → Comparison or Limit Comparison

**Alternating signs ((-1)ⁿ)?** → Alternating Series Test

**Easy to integrate f(x)?** → Integral Test""",
                "formula": "\\text{If } \\lim_{n \\to \\infty} a_n \\neq 0, \\text{ then } \\sum a_n \\text{ diverges}",
            },
            {
                "name": "Ratio Test",
                "explanation": """**Best for:** Factorials, exponentials, products of these

**The Test:** Let L = lim(n→∞) |aₙ₊₁/aₙ|

• If L < 1: Series converges (absolutely)
• If L > 1 or L = ∞: Series diverges  
• If L = 1: Test is inconclusive

**Common Patterns:**
• n!/nⁿ → Ratio test gives L < 1 (converges)
• aⁿ/n! → Ratio test gives L = 0 (converges)
• n!/aⁿ → Ratio test gives L = ∞ (diverges)

**Example:** Σ n!/3ⁿ
aₙ₊₁/aₙ = [(n+1)!/3ⁿ⁺¹] / [n!/3ⁿ]
        = (n+1)/3
L = lim(n→∞) (n+1)/3 = ∞
Diverges!""",
                "formula": "L = \\lim_{n \\to \\infty} \\left|\\frac{a_{n+1}}{a_n}\\right|",
                "examples": [
                    {
                        "problem": "Test Σ 2ⁿ/n! for convergence",
                        "solution": """Using Ratio Test:
aₙ₊₁/aₙ = [2ⁿ⁺¹/(n+1)!] / [2ⁿ/n!]
        = 2ⁿ⁺¹ · n! / (2ⁿ · (n+1)!)
        = 2/(n+1)

L = lim(n→∞) 2/(n+1) = 0 < 1

The series converges (absolutely)."""
                    }
                ]
            },
            {
                "name": "Root Test",
                "explanation": """**Best for:** Terms raised to the n-th power: (...)ⁿ

**The Test:** Let L = lim(n→∞) |aₙ|^(1/n) = lim(n→∞) ⁿ√|aₙ|

• If L < 1: Series converges (absolutely)
• If L > 1: Series diverges
• If L = 1: Test is inconclusive

**Key Identity:** lim(n→∞) n^(1/n) = 1

**Example:** Σ (2n/(3n+1))ⁿ
ⁿ√|aₙ| = 2n/(3n+1)
L = lim(n→∞) 2n/(3n+1) = 2/3 < 1
Converges!""",
                "formula": "L = \\lim_{n \\to \\infty} \\sqrt[n]{|a_n|}",
            },
            {
                "name": "Comparison Tests",
                "explanation": """**Direct Comparison:**
For 0 ≤ aₙ ≤ bₙ:
• If Σbₙ converges, then Σaₙ converges
• If Σaₙ diverges, then Σbₙ diverges

**Limit Comparison:**
If lim(n→∞) aₙ/bₙ = L where 0 < L < ∞:
Then Σaₙ and Σbₙ either both converge or both diverge.

**Choosing a comparison series bₙ:**
• Keep the dominant term(s) in the expression
• 1/(n² + 3n) ~ 1/n² (converges, p = 2)
• n/(n³ - 5) ~ 1/n² (converges)
• 1/(2ⁿ - 1) ~ 1/2ⁿ (geometric, converges)
• 1/(√n + ln n) ~ 1/√n (diverges, p = 1/2)""",
                "formula": "\\text{If } \\lim_{n \\to \\infty} \\frac{a_n}{b_n} = L, \\; 0 < L < \\infty, \\text{ same convergence}",
            },
            {
                "name": "Alternating Series Test",
                "explanation": """**For series of the form:** Σ(-1)ⁿbₙ or Σ(-1)ⁿ⁺¹bₙ where bₙ > 0

**The series converges if BOTH:**
1. bₙ is eventually decreasing: bₙ₊₁ ≤ bₙ
2. lim(n→∞) bₙ = 0

**Error Estimate (very useful!):**
If Sₙ is the n-th partial sum, then:
|S - Sₙ| ≤ bₙ₊₁

This means the error is at most the first omitted term!

**Example:** Σ(-1)ⁿ⁺¹/n = 1 - 1/2 + 1/3 - 1/4 + ...
• bₙ = 1/n is decreasing ✓
• lim(n→∞) 1/n = 0 ✓
Converges! (This is the alternating harmonic series, sum = ln 2)""",
                "formula": "\\sum_{n=1}^{\\infty} \\frac{(-1)^{n+1}}{n} = \\ln 2",
            },
            {
                "name": "Integral Test",
                "explanation": """**When to use:** When you can integrate f(x) easily

**Setup:** Let f(x) be positive, continuous, and decreasing for x ≥ 1.
If aₙ = f(n), then:
Σaₙ and ∫₁^∞ f(x)dx either both converge or both diverge.

**Note:** The sum and the integral don't have the same value, just the same convergence behavior!

**Example:** Σ 1/(n·ln²(n)) for n ≥ 2
∫₂^∞ 1/(x·ln²(x)) dx
Let u = ln(x), du = 1/x dx
= ∫_{ln2}^∞ 1/u² du = [-1/u]_{ln2}^∞ = 1/ln(2)

Converges! So the series converges.""",
                "formula": "\\sum_{n=1}^{\\infty} a_n \\text{ and } \\int_1^{\\infty} f(x) \\, dx \\text{ converge/diverge together}",
            }
        ],
        "practice_problems": [
            {"question": "Does Σ n/(n²+1) converge?", "answer": "No, diverges", "hint": "Limit compare to 1/n"},
            {"question": "Does Σ 3ⁿ/n! converge?", "answer": "Yes, converges", "hint": "Ratio test"},
            {"question": "Does Σ (-1)ⁿn/(n+1) converge?", "answer": "No, diverges", "hint": "Divergence test: limit ≠ 0"},
            {"question": "Does Σ 1/(n·ln(n)) converge (n≥2)?", "answer": "No, diverges", "hint": "Integral test"},
            {"question": "Does Σ (n/(2n+1))ⁿ converge?", "answer": "Yes, converges", "hint": "Root test: L = 1/2"},
            {"question": "Does Σ 1/(n²+3n+2) converge?", "answer": "Yes, converges", "hint": "Compare to 1/n²"},
        ]
    },
    
    "taylor_maclaurin": {
        "title": "Taylor and Maclaurin Series",
        "description": "Representing functions as infinite power series - CRITICAL for final",
        "priority": "HIGH",
        "concepts": [
            {
                "name": "Taylor Series Definition",
                "explanation": """**Taylor series of f(x) centered at x = a:**

f(x) = Σ f⁽ⁿ⁾(a)/n! · (x-a)ⁿ  for n = 0 to ∞

= f(a) + f'(a)(x-a) + f''(a)(x-a)²/2! + f'''(a)(x-a)³/3! + ...

**Maclaurin series** is the special case when a = 0:
f(x) = Σ f⁽ⁿ⁾(0)/n! · xⁿ

**Key Concept:** Taylor series approximate functions with polynomials. The more terms you take, the better the approximation near the center.

**Radius of Convergence (R):**
The series converges for |x - a| < R and diverges for |x - a| > R.
Use the ratio test to find R: R = lim |aₙ/aₙ₊₁|""",
                "formula": "f(x) = \\sum_{n=0}^{\\infty} \\frac{f^{(n)}(a)}{n!}(x-a)^n",
            },
            {
                "name": "MUST MEMORIZE: Common Maclaurin Series",
                "explanation": """**MEMORIZE THESE - they appear constantly on exams!**

**Exponential:**
eˣ = 1 + x + x²/2! + x³/3! + ... = Σ xⁿ/n!  (all x)

**Sine:**
sin(x) = x - x³/3! + x⁵/5! - x⁷/7! + ... = Σ (-1)ⁿx^(2n+1)/(2n+1)!  (all x)

**Cosine:**
cos(x) = 1 - x²/2! + x⁴/4! - x⁶/6! + ... = Σ (-1)ⁿx^(2n)/(2n)!  (all x)

**Natural Log:**
ln(1+x) = x - x²/2 + x³/3 - x⁴/4 + ... = Σ (-1)ⁿ⁺¹xⁿ/n  (-1 < x ≤ 1)

**Geometric:**
1/(1-x) = 1 + x + x² + x³ + ... = Σ xⁿ  (|x| < 1)

**Arctangent:**
arctan(x) = x - x³/3 + x⁵/5 - x⁷/7 + ... = Σ (-1)ⁿx^(2n+1)/(2n+1)  (|x| ≤ 1)

**Binomial (for |x| < 1):**
(1+x)ᵏ = 1 + kx + k(k-1)x²/2! + k(k-1)(k-2)x³/3! + ...""",
                "formula": "e^x = \\sum_{n=0}^{\\infty} \\frac{x^n}{n!}, \\quad \\sin x = \\sum_{n=0}^{\\infty} \\frac{(-1)^n x^{2n+1}}{(2n+1)!}",
            },
            {
                "name": "Deriving New Series from Known Ones",
                "explanation": """**Don't re-derive everything! Modify known series.**

**Substitution:**
e^(-x²) → Replace x with -x² in eˣ series:
= 1 + (-x²) + (-x²)²/2! + (-x²)³/3! + ...
= 1 - x² + x⁴/2! - x⁶/3! + ...

**Differentiation:**
d/dx[1/(1-x)] = d/dx[1 + x + x² + ...]
1/(1-x)² = 1 + 2x + 3x² + 4x³ + ... = Σ(n+1)xⁿ

**Integration:**
∫ 1/(1+x²) dx = arctan(x) → Integrate 1 - x² + x⁴ - x⁶ + ...
arctan(x) = x - x³/3 + x⁵/5 - x⁷/7 + ...

**Multiplication:**
eˣ·sin(x) = (1 + x + x²/2 + ...)(x - x³/6 + ...)
Multiply and collect terms carefully""",
                "formula": "\\frac{1}{1-x} = \\sum_{n=0}^{\\infty} x^n \\implies \\frac{1}{(1-x)^2} = \\sum_{n=1}^{\\infty} n x^{n-1}",
                "examples": [
                    {
                        "problem": "Find the Maclaurin series for e^(2x)",
                        "solution": """Start with eˣ = Σ xⁿ/n!
Replace x with 2x:

e^(2x) = Σ (2x)ⁿ/n! = Σ 2ⁿxⁿ/n!
= 1 + 2x + 4x²/2! + 8x³/3! + ...
= 1 + 2x + 2x² + (4/3)x³ + ..."""
                    },
                    {
                        "problem": "Find the Maclaurin series for x·cos(x)",
                        "solution": """Start with cos(x) = 1 - x²/2! + x⁴/4! - ...
Multiply by x:

x·cos(x) = x(1 - x²/2! + x⁴/4! - ...)
         = x - x³/2! + x⁵/4! - x⁷/6! + ...
         = x - x³/2 + x⁵/24 - ..."""
                    }
                ]
            },
            {
                "name": "Applications of Taylor Series",
                "explanation": """**1. Evaluating Limits (L'Hôpital's alternative):**
lim(x→0) (sin x - x)/x³
= lim(x→0) ((x - x³/6 + ...) - x)/x³
= lim(x→0) (-x³/6 + ...)/x³ = -1/6

**2. Evaluating Integrals:**
∫ e^(-x²) dx has no elementary antiderivative
But: ∫ e^(-x²) dx = ∫ (1 - x² + x⁴/2! - ...) dx
= x - x³/3 + x⁵/10 - x⁷/42 + ... + C

**3. Approximating Values:**
e^(0.1) ≈ 1 + 0.1 + 0.01/2 + 0.001/6 ≈ 1.1052

**4. Solving Differential Equations:**
Assume y = Σ aₙxⁿ and solve for coefficients""",
                "formula": "\\lim_{x \\to 0} \\frac{e^x - 1 - x}{x^2} = \\frac{1}{2}",
            }
        ],
        "practice_problems": [
            {"question": "Write the first 4 nonzero terms of the Maclaurin series for e^(-x)", "answer": "1 - x + x²/2 - x³/6", "hint": "Replace x with -x in eˣ series"},
            {"question": "Write the Maclaurin series for sin(x²)", "answer": "x² - x⁶/6 + x¹⁰/120 - ...", "hint": "Replace x with x² in sin(x)"},
            {"question": "Find lim(x→0) (1-cos(x))/x² using Taylor series", "answer": "1/2", "hint": "Use cos(x) = 1 - x²/2 + ..."},
            {"question": "Find the Maclaurin series for 1/(1+x²)", "answer": "1 - x² + x⁴ - x⁶ + ...", "hint": "Replace x with -x² in 1/(1-x)"},
            {"question": "What is the radius of convergence of Σ xⁿ/n?", "answer": "R = 1", "hint": "This is -ln(1-x)"},
        ]
    },
    
    "power_series": {
        "title": "Power Series",
        "description": "Understanding convergence, operations, and representations",
        "priority": "HIGH",
        "concepts": [
            {
                "name": "Power Series Basics",
                "explanation": """**Definition:** A power series centered at a is:
Σ cₙ(x-a)ⁿ = c₀ + c₁(x-a) + c₂(x-a)² + ...

**Three Possibilities for Convergence:**
1. Converges only at x = a (R = 0)
2. Converges for all x (R = ∞)
3. Converges for |x-a| < R, diverges for |x-a| > R

At the endpoints x = a ± R, you must check separately!

**Finding the Radius R:**
Use the ratio test on |cₙ₊₁(x-a)ⁿ⁺¹|/|cₙ(x-a)ⁿ|
Set the limit < 1 and solve for |x-a|

Or use: R = lim |cₙ/cₙ₊₁| (if this limit exists)
Or use: R = 1/lim |cₙ|^(1/n) (root test)""",
                "formula": "\\sum_{n=0}^{\\infty} c_n (x-a)^n, \\quad R = \\lim_{n \\to \\infty} \\left|\\frac{c_n}{c_{n+1}}\\right|",
                "examples": [
                    {
                        "problem": "Find the radius of convergence of Σ xⁿ/n!",
                        "solution": """Using ratio test:
|aₙ₊₁/aₙ| = |x^(n+1)/(n+1)!| / |xⁿ/n!|
         = |x|/(n+1)

lim(n→∞) |x|/(n+1) = 0 < 1 for all x

R = ∞ (converges for all x)
This is the series for eˣ!"""
                    }
                ]
            },
            {
                "name": "Operations on Power Series",
                "explanation": """**Within the radius of convergence, power series behave like polynomials!**

**Addition/Subtraction:**
Σaₙxⁿ ± Σbₙxⁿ = Σ(aₙ ± bₙ)xⁿ

**Multiplication:**
(Σaₙxⁿ)(Σbₙxⁿ) = Σcₙxⁿ where cₙ = Σₖ₌₀ⁿ aₖbₙ₋ₖ (Cauchy product)

**Differentiation (term by term):**
d/dx[Σcₙxⁿ] = Σncₙxⁿ⁻¹
The radius stays the same!

**Integration (term by term):**
∫Σcₙxⁿ dx = Σcₙxⁿ⁺¹/(n+1) + C
The radius stays the same!""",
                "formula": "\\frac{d}{dx}\\left[\\sum c_n x^n\\right] = \\sum n c_n x^{n-1}",
            },
            {
                "name": "Representing Functions as Power Series",
                "explanation": """**Strategy:** Transform f(x) into a form matching a known series.

**Geometric Series Manipulation:**
1/(1-x) = Σxⁿ, valid for |x| < 1

**To find series for 1/(3-x):**
1/(3-x) = (1/3) · 1/(1-x/3) = (1/3)Σ(x/3)ⁿ = Σxⁿ/3ⁿ⁺¹

**To find series for 1/(1+x²):**
= 1/(1-(-x²)) = Σ(-x²)ⁿ = Σ(-1)ⁿx^(2n)

**To find series for x/(1-x²):**
= x · 1/(1-x²) = x · Σ(x²)ⁿ = Σx^(2n+1)

**Partial Fractions + Series:**
For 1/((1-x)(1+x)), decompose first:
= (1/2)/(1-x) + (1/2)/(1+x)
Then expand each fraction as a series.""",
                "formula": "\\frac{1}{1-u} = \\sum_{n=0}^{\\infty} u^n \\text{ for } |u| < 1",
            }
        ],
        "practice_problems": [
            {"question": "Find the radius of convergence: Σ nxⁿ", "answer": "R = 1", "hint": "Ratio test: |x|(n+1)/n → |x|"},
            {"question": "Find the radius of convergence: Σ xⁿ/n²", "answer": "R = 1", "hint": "Ratio test or comparison"},
            {"question": "Express 1/(2+x) as a power series", "answer": "(1/2)Σ(-x/2)ⁿ = Σ(-1)ⁿxⁿ/2ⁿ⁺¹", "hint": "Write as (1/2)·1/(1-(-x/2))"},
            {"question": "Express x²/(1-x³) as a power series", "answer": "Σx^(3n+2)", "hint": "x² · Σ(x³)ⁿ"},
        ]
    },
    
    "parametric_calculus": {
        "title": "Calculus with Parametric Curves",
        "description": "Derivatives, areas, and arc length for parametric equations",
        "priority": "HIGH",
        "concepts": [
            {
                "name": "Parametric Equations Basics",
                "explanation": """**Parametric equations:** x = f(t), y = g(t)
The parameter t traces out a curve as it varies.

**Examples:**
• Circle: x = cos(t), y = sin(t), 0 ≤ t ≤ 2π
• Ellipse: x = a·cos(t), y = b·sin(t)
• Line through (x₀,y₀) with direction (a,b): x = x₀ + at, y = y₀ + bt
• Cycloid: x = t - sin(t), y = 1 - cos(t)

**Converting to Cartesian:**
Eliminate the parameter t by solving for t in one equation and substituting into the other.

**Direction of motion:** Increasing t determines the direction the curve is traced.""",
                "formula": "x = f(t), \\quad y = g(t)",
            },
            {
                "name": "Derivatives of Parametric Curves",
                "explanation": """**First Derivative (slope of tangent):**
dy/dx = (dy/dt)/(dx/dt) = y'(t)/x'(t)

• Horizontal tangent: dy/dt = 0 and dx/dt ≠ 0
• Vertical tangent: dx/dt = 0 and dy/dt ≠ 0

**Second Derivative (concavity):**
d²y/dx² = d/dx[dy/dx] = (d/dt[dy/dx])/(dx/dt)

= [x'(t)·y''(t) - y'(t)·x''(t)] / [x'(t)]³

Simpler formula:
d²y/dx² = [d/dt(dy/dx)] / (dx/dt)""",
                "formula": "\\frac{dy}{dx} = \\frac{dy/dt}{dx/dt} = \\frac{y'(t)}{x'(t)}",
                "examples": [
                    {
                        "problem": "Find dy/dx for x = t², y = t³",
                        "solution": """dx/dt = 2t
dy/dt = 3t²

dy/dx = (dy/dt)/(dx/dt) = 3t²/2t = 3t/2"""
                    },
                    {
                        "problem": "Find d²y/dx² for x = t², y = t³",
                        "solution": """From above: dy/dx = 3t/2

d/dt[dy/dx] = d/dt[3t/2] = 3/2

d²y/dx² = (3/2)/(2t) = 3/(4t)"""
                    }
                ]
            },
            {
                "name": "Arc Length (Parametric)",
                "explanation": """**Arc Length Formula:**
L = ∫ₐᵇ √[(dx/dt)² + (dy/dt)²] dt

= ∫ₐᵇ √[x'(t)² + y'(t)²] dt

**Derivation:** Small arc length ds = √(dx² + dy²)
= √[(dx/dt)² + (dy/dt)²] dt

**Example:** Circle x = cos(t), y = sin(t), 0 ≤ t ≤ 2π
x'(t) = -sin(t), y'(t) = cos(t)
√[sin²(t) + cos²(t)] = 1
L = ∫₀^(2π) 1 dt = 2π ✓""",
                "formula": "L = \\int_a^b \\sqrt{\\left(\\frac{dx}{dt}\\right)^2 + \\left(\\frac{dy}{dt}\\right)^2} \\, dt",
            },
            {
                "name": "Area Under Parametric Curves",
                "explanation": """**Area Formula:**
A = ∫ₐᵇ y(t) · x'(t) dt

(assuming the curve is traced from left to right as t goes from a to b)

For curves traced right-to-left, use:
A = -∫ₐᵇ y(t) · x'(t) dt = ∫ₐᵇ y(t) · (-x'(t)) dt

**Example:** Area under one arch of cycloid
x = t - sin(t), y = 1 - cos(t), 0 ≤ t ≤ 2π

x'(t) = 1 - cos(t)
A = ∫₀^(2π) (1-cos(t))(1-cos(t)) dt
  = ∫₀^(2π) (1-cos(t))² dt
  = 3π""",
                "formula": "A = \\int_a^b y(t) \\cdot x'(t) \\, dt",
            }
        ],
        "practice_problems": [
            {"question": "Find dy/dx for x = e^t, y = e^(2t)", "answer": "2e^t", "hint": "dy/dx = (2e^(2t))/(e^t)"},
            {"question": "Find horizontal tangent points for x = t³-3t, y = t²-4", "answer": "t = 0, point (-0, -4)", "hint": "Set dy/dt = 2t = 0"},
            {"question": "Find arc length of x = 3t², y = 2t³ from t=0 to t=1", "answer": "2(2^(3/2) - 1) = 2√8 - 2", "hint": "√(36t² + 36t⁴) = 6t√(1+t²)"},
            {"question": "Find dy/dx at t = π/4 for x = cos(t), y = sin(t)", "answer": "-1", "hint": "dy/dx = -cot(t)"},
        ]
    },
    
    "polar_calculus": {
        "title": "Calculus in Polar Coordinates",
        "description": "Graphing, area, and arc length in polar form",
        "priority": "HIGH",
        "concepts": [
            {
                "name": "Polar Coordinate Basics",
                "explanation": """**Polar coordinates:** (r, θ)
• r = distance from origin
• θ = angle from positive x-axis (counterclockwise)

**Converting:**
• x = r·cos(θ)
• y = r·sin(θ)
• r² = x² + y²
• tan(θ) = y/x

**Common Polar Curves:**
• Circle: r = a (radius a centered at origin)
• Circle through origin: r = a·cos(θ) or r = a·sin(θ)
• Cardioid: r = a(1 + cos(θ)) or r = a(1 + sin(θ))
• Rose: r = a·cos(nθ) or r = a·sin(nθ)
  - n odd: n petals
  - n even: 2n petals
• Lemniscate: r² = a²cos(2θ) or r² = a²sin(2θ)
• Limaçon: r = a + b·cos(θ)
  - |a| > |b|: convex
  - |a| = |b|: cardioid
  - |a| < |b|: inner loop""",
                "formula": "x = r\\cos\\theta, \\quad y = r\\sin\\theta, \\quad r^2 = x^2 + y^2",
            },
            {
                "name": "Area in Polar Coordinates",
                "explanation": """**Area Formula:**
A = (1/2)∫_α^β r² dθ

**Where α and β are the angles that bound the region.**

**Key insight:** This comes from the area of a sector:
Area of sector = (1/2)r²·Δθ

**Area Between Two Curves:**
If r₁(θ) ≤ r₂(θ) for α ≤ θ ≤ β:
A = (1/2)∫_α^β [r₂(θ)² - r₁(θ)²] dθ

**Common Mistake:** Make sure you integrate over the correct range of θ! Sketch the curve first.""",
                "formula": "A = \\frac{1}{2}\\int_{\\alpha}^{\\beta} r^2 \\, d\\theta",
                "examples": [
                    {
                        "problem": "Find area enclosed by r = 2cos(θ)",
                        "solution": """This is a circle of diameter 2 (radius 1).
The curve is traced for 0 ≤ θ ≤ π.

A = (1/2)∫₀^π (2cos(θ))² dθ
  = (1/2)∫₀^π 4cos²(θ) dθ
  = 2∫₀^π (1+cos(2θ))/2 dθ
  = ∫₀^π (1+cos(2θ)) dθ
  = [θ + sin(2θ)/2]₀^π
  = π

Check: Circle with r=1 has area π ✓"""
                    },
                    {
                        "problem": "Find area of one petal of r = cos(2θ)",
                        "solution": """One petal is traced for -π/4 ≤ θ ≤ π/4.

A = (1/2)∫_{-π/4}^{π/4} cos²(2θ) dθ
  = (1/2)∫_{-π/4}^{π/4} (1+cos(4θ))/2 dθ
  = (1/4)[θ + sin(4θ)/4]_{-π/4}^{π/4}
  = (1/4)(π/2) = π/8"""
                    }
                ]
            },
            {
                "name": "Arc Length in Polar Coordinates",
                "explanation": """**Arc Length Formula:**
L = ∫_α^β √[r² + (dr/dθ)²] dθ

**Derivation:** From parametric arc length with:
x = r·cos(θ), y = r·sin(θ)
dx/dθ = r'·cos(θ) - r·sin(θ)
dy/dθ = r'·sin(θ) + r·cos(θ)

(dx/dθ)² + (dy/dθ)² = r² + (r')² after simplification.

**Example:** Arc length of r = eθ from θ = 0 to θ = π
r' = eθ
L = ∫₀^π √[(eθ)² + (eθ)²] dθ = ∫₀^π eθ√2 dθ = √2(e^π - 1)""",
                "formula": "L = \\int_{\\alpha}^{\\beta} \\sqrt{r^2 + \\left(\\frac{dr}{d\\theta}\\right)^2} \\, d\\theta",
            },
            {
                "name": "Tangent Lines in Polar",
                "explanation": """**Slope of tangent line:**
dy/dx = (dr/dθ · sin(θ) + r·cos(θ)) / (dr/dθ · cos(θ) - r·sin(θ))

**Horizontal tangent:** numerator = 0
dr/dθ · sin(θ) + r·cos(θ) = 0

**Vertical tangent:** denominator = 0
dr/dθ · cos(θ) - r·sin(θ) = 0

**Tangent at the pole (r = 0):**
The tangent line is θ = constant (the angle where r = 0).""",
                "formula": "\\frac{dy}{dx} = \\frac{\\frac{dr}{d\\theta}\\sin\\theta + r\\cos\\theta}{\\frac{dr}{d\\theta}\\cos\\theta - r\\sin\\theta}",
            }
        ],
        "practice_problems": [
            {"question": "Find the area inside r = 1 + cos(θ)", "answer": "3π/2", "hint": "Integrate (1/2)(1+cos(θ))² from 0 to 2π"},
            {"question": "Find the area of one petal of r = sin(3θ)", "answer": "π/12", "hint": "One petal: 0 to π/3"},
            {"question": "Find the area inside r = 2sin(θ)", "answer": "π", "hint": "Circle with diameter 2"},
            {"question": "Find the area inside r = 3cos(θ) but outside r = 1 + cos(θ)", "answer": "π", "hint": "Find where curves intersect, then subtract areas"},
        ]
    }
}

# Export for use in server.py
def get_calc2_content():
    return CALC2_CONTENT

def get_calc2_topics():
    """Return topic list for the API"""
    return [
        {
            "id": topic_id,
            "title": topic["title"],
            "description": topic["description"],
            "priority": topic.get("priority", "MEDIUM"),
            "concept_count": len(topic["concepts"]),
            "problem_count": len(topic["practice_problems"])
        }
        for topic_id, topic in CALC2_CONTENT.items()
    ]
