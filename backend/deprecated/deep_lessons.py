"""
Deep Teaching Content for Calculus II
Comprehensive lessons that ACTUALLY TEACH, not just quiz

Each topic has:
- Full conceptual explanation (WHY this works)
- Step-by-step method
- Multiple worked examples with commentary
- Common mistakes and how to avoid them
- Practice problems with solutions
- Connection to other topics
"""

DEEP_LESSONS = {
    "integration_by_parts": {
        "title": "Integration by Parts",
        "subtitle": "The reverse product rule - for when substitution fails",
        "estimated_time": "45 min",
        "prerequisites": ["basic_integration", "product_rule"],
        
        "conceptual_intro": """
## The Big Picture

Integration by Parts is essentially the **reverse of the product rule** for derivatives.

Remember: d/dx[u·v] = u·(dv/dx) + v·(du/dx)

Rearranging: u·(dv/dx) = d/dx[u·v] - v·(du/dx)

Integrating both sides: **∫u·dv = u·v - ∫v·du**

### When Do You Use This?

Use IBP when you have a **product of two different types of functions** that can't be simplified by substitution:
- Polynomial × Trig (∫x·sin(x)dx)
- Polynomial × Exponential (∫x·eˣdx)
- Polynomial × Log (∫x·ln(x)dx)
- Trig × Exponential (∫eˣ·cos(x)dx)
- Inverse trig alone (∫arctan(x)dx)
- Log alone (∫ln(x)dx)
""",
        
        "key_formula": {
            "latex": "\\int u \\, dv = uv - \\int v \\, du",
            "plain": "∫u·dv = u·v - ∫v·du",
            "explanation": "Choose u (to differentiate) and dv (to integrate). The goal is to make ∫v·du simpler than ∫u·dv."
        },
        
        "method_steps": [
            {
                "step": 1,
                "title": "Identify that you need IBP",
                "content": "The integrand is a product of two different function types that substitution won't handle.",
                "tip": "If you can see a u-sub that works, use that instead! IBP is for when substitution fails."
            },
            {
                "step": 2,
                "title": "Choose u and dv using LIATE",
                "content": """**LIATE** gives the priority for choosing u:
- **L**ogarithmic (ln x, log x) - FIRST choice for u
- **I**nverse trig (arctan x, arcsin x)
- **A**lgebraic (x, x², polynomials)
- **T**rigonometric (sin x, cos x)
- **E**xponential (eˣ, 2ˣ) - LAST choice for u

Pick u from the **earliest** category in your integrand. Whatever's left is dv.""",
                "tip": "LIATE isn't perfect, but it works 90% of the time. The goal is: after differentiating u and integrating dv, is ∫v·du simpler?"
            },
            {
                "step": 3,
                "title": "Find du and v",
                "content": "Differentiate u to get du. Integrate dv to get v (ignore +C for now).",
                "tip": "Don't forget: dv must include dx! If dv = cos(x)dx, then v = sin(x)."
            },
            {
                "step": 4,
                "title": "Apply the formula",
                "content": "Plug into ∫u·dv = u·v - ∫v·du",
                "tip": "Watch your signs! The minus sign trips up many students."
            },
            {
                "step": 5,
                "title": "Evaluate ∫v·du",
                "content": "This new integral should be simpler. If it's not, you may have chosen u and dv wrong.",
                "tip": "Sometimes you need IBP multiple times (for x²·eˣ) or the integral 'loops back' (for eˣ·sin(x))."
            }
        ],
        
        "worked_examples": [
            {
                "title": "Basic Example: ∫x·eˣ dx",
                "difficulty": 1,
                "problem": "Evaluate ∫x·eˣ dx",
                "solution": [
                    {
                        "step": "Identify: Product of Algebraic (x) and Exponential (eˣ). Need IBP.",
                        "math": "\\int x \\cdot e^x \\, dx"
                    },
                    {
                        "step": "LIATE: A comes before E, so u = x (Algebraic), dv = eˣdx",
                        "math": "u = x, \\quad dv = e^x \\, dx"
                    },
                    {
                        "step": "Find du and v:",
                        "math": "du = dx, \\quad v = e^x"
                    },
                    {
                        "step": "Apply formula: ∫u·dv = uv - ∫v·du",
                        "math": "= x \\cdot e^x - \\int e^x \\, dx"
                    },
                    {
                        "step": "Evaluate the remaining integral:",
                        "math": "= x \\cdot e^x - e^x + C"
                    },
                    {
                        "step": "Factor if desired:",
                        "math": "= e^x(x - 1) + C"
                    }
                ],
                "key_insight": "The polynomial 'decreases' when differentiated (x → 1 → 0), while eˣ stays the same when integrated. This makes the new integral simpler.",
                "common_mistakes": [
                    "Choosing u = eˣ would give a HARDER integral",
                    "Forgetting the minus sign in the formula"
                ]
            },
            {
                "title": "Logarithm Example: ∫ln(x) dx",
                "difficulty": 1,
                "problem": "Evaluate ∫ln(x) dx",
                "solution": [
                    {
                        "step": "This looks like there's no 'dv', but we can write it as ln(x)·1",
                        "math": "\\int \\ln(x) \\cdot 1 \\, dx"
                    },
                    {
                        "step": "LIATE: L comes first! u = ln(x), dv = 1·dx = dx",
                        "math": "u = \\ln(x), \\quad dv = dx"
                    },
                    {
                        "step": "Find du and v:",
                        "math": "du = \\frac{1}{x} \\, dx, \\quad v = x"
                    },
                    {
                        "step": "Apply formula:",
                        "math": "= x \\ln(x) - \\int x \\cdot \\frac{1}{x} \\, dx"
                    },
                    {
                        "step": "Simplify and integrate:",
                        "math": "= x \\ln(x) - \\int 1 \\, dx = x \\ln(x) - x + C"
                    }
                ],
                "key_insight": "When integrating a single log or inverse trig, let dv = dx. The '1' is your dv!",
                "common_mistakes": [
                    "Not recognizing you can use IBP on a 'single' function",
                    "Trying to integrate ln(x) directly (there's no elementary antiderivative without IBP)"
                ]
            },
            {
                "title": "Repeated IBP: ∫x²·eˣ dx (Tabular Method)",
                "difficulty": 2,
                "problem": "Evaluate ∫x²·eˣ dx",
                "solution": [
                    {
                        "step": "Need IBP multiple times. Use the TABULAR METHOD for efficiency.",
                        "math": "\\text{Set up table with derivatives of } x^2 \\text{ and integrals of } e^x"
                    },
                    {
                        "step": "Create the table with alternating signs (+, -, +, ...):",
                        "math": "\\begin{array}{c|c|c} \\text{Sign} & D & I \\\\ \\hline + & x^2 & e^x \\\\ - & 2x & e^x \\\\ + & 2 & e^x \\\\ - & 0 & e^x \\end{array}"
                    },
                    {
                        "step": "Multiply diagonally and add:",
                        "math": "= (+)(x^2)(e^x) + (-)(2x)(e^x) + (+)(2)(e^x) + C"
                    },
                    {
                        "step": "Simplify:",
                        "math": "= x^2 e^x - 2x e^x + 2e^x + C = e^x(x^2 - 2x + 2) + C"
                    }
                ],
                "key_insight": "Tabular method: differentiate u until you get 0, integrate dv repeatedly. Multiply diagonals with alternating signs.",
                "common_mistakes": [
                    "Wrong signs (remember: +, -, +, -, ...)",
                    "Not continuing until the derivative reaches 0"
                ]
            },
            {
                "title": "Cycling IBP: ∫eˣ·cos(x) dx",
                "difficulty": 3,
                "problem": "Evaluate ∫eˣ·cos(x) dx",
                "solution": [
                    {
                        "step": "Both eˣ and cos(x) 'reproduce' when differentiated/integrated. Either can be u.",
                        "math": "\\text{Let } u = e^x, \\, dv = \\cos(x) \\, dx"
                    },
                    {
                        "step": "First IBP:",
                        "math": "du = e^x dx, \\, v = \\sin(x)"
                    },
                    {
                        "step": "Apply formula:",
                        "math": "I = e^x \\sin(x) - \\int e^x \\sin(x) \\, dx"
                    },
                    {
                        "step": "Do IBP again on the new integral (keep u as eˣ):",
                        "math": "u = e^x, \\, dv = \\sin(x) dx \\Rightarrow du = e^x dx, \\, v = -\\cos(x)"
                    },
                    {
                        "step": "Second application:",
                        "math": "I = e^x \\sin(x) - \\left[ -e^x \\cos(x) - \\int -e^x \\cos(x) \\, dx \\right]"
                    },
                    {
                        "step": "Simplify (notice the original integral I appears!):",
                        "math": "I = e^x \\sin(x) + e^x \\cos(x) - I"
                    },
                    {
                        "step": "Solve for I:",
                        "math": "2I = e^x(\\sin(x) + \\cos(x))"
                    },
                    {
                        "step": "Final answer:",
                        "math": "I = \\frac{e^x(\\sin(x) + \\cos(x))}{2} + C"
                    }
                ],
                "key_insight": "When IBP 'cycles back' to the original integral, call the integral I, and solve the resulting equation for I.",
                "common_mistakes": [
                    "Switching which function is u in the second IBP (this will just undo the first IBP!)",
                    "Sign errors when the integral 'comes back'"
                ]
            }
        ],
        
        "practice_problems": [
            {"problem": "∫x·sin(x) dx", "answer": "-x·cos(x) + sin(x) + C", "difficulty": 1},
            {"problem": "∫x·cos(2x) dx", "answer": "(x/2)·sin(2x) + (1/4)·cos(2x) + C", "difficulty": 1},
            {"problem": "∫arctan(x) dx", "answer": "x·arctan(x) - (1/2)·ln(1+x²) + C", "difficulty": 2},
            {"problem": "∫x²·sin(x) dx", "answer": "-x²·cos(x) + 2x·sin(x) + 2cos(x) + C", "difficulty": 2},
            {"problem": "∫eˣ·sin(x) dx", "answer": "(eˣ/2)·(sin(x) - cos(x)) + C", "difficulty": 3},
            {"problem": "∫x·ln(x) dx", "answer": "(x²/2)·ln(x) - x²/4 + C", "difficulty": 2},
        ],
        
        "common_mistakes": [
            {
                "mistake": "Wrong choice of u and dv",
                "why_it_happens": "Not using LIATE or choosing the function that makes the integral harder",
                "how_to_avoid": "Always use LIATE. Ask: will differentiating u and integrating dv make ∫v·du simpler?"
            },
            {
                "mistake": "Forgetting the minus sign",
                "why_it_happens": "The formula has a subtraction that's easy to overlook",
                "how_to_avoid": "Write out the formula every time: ∫u·dv = uv - ∫v·du. Circle the minus."
            },
            {
                "mistake": "Not including dx in dv",
                "why_it_happens": "Treating dv as just the function, forgetting the differential",
                "how_to_avoid": "dv always includes dx. Write 'dv = [function] dx' explicitly."
            },
            {
                "mistake": "Switching u in cyclic problems",
                "why_it_happens": "Trying to alternate which function is u",
                "how_to_avoid": "In cycling problems, always keep the SAME function as u in each application."
            }
        ],
        
        "connections": {
            "leads_to": ["partial_fractions", "trigonometric_integrals"],
            "used_in": ["differential_equations", "physics_applications"],
            "similar_techniques": ["u_substitution", "tabular_method"]
        },
        
        "exam_tips": [
            "IBP shows up on almost every Calc II exam. Master it!",
            "Know the tabular method for polynomial × exponential problems",
            "Cycling problems (eˣ·sin or eˣ·cos) are common - practice until automatic",
            "∫ln(x)dx and ∫arctan(x)dx are classic 'surprise' IBP problems"
        ]
    },
    
    "partial_fractions": {
        "title": "Partial Fractions Decomposition",
        "subtitle": "Breaking rational functions into integrable pieces",
        "estimated_time": "50 min",
        "prerequisites": ["polynomial_factoring", "basic_integration"],
        
        "conceptual_intro": """
## The Big Picture

When you have a **rational function** (polynomial over polynomial), partial fractions lets you break it into simpler fractions that you can actually integrate.

### Why Does This Work?

It's the reverse of adding fractions! Just like:
1/2 + 1/3 = 5/6

We can go backwards:
5/6 = 1/2 + 1/3 (if we know how to find them)

### When Do You Use This?

Use partial fractions when:
- Integrating P(x)/Q(x) where degree of P < degree of Q
- The denominator can be factored
- Substitution won't simplify it
""",
        
        "key_formula": {
            "latex": "\\frac{P(x)}{Q(x)} = \\frac{A}{x-a} + \\frac{B}{x-b} + \\cdots",
            "plain": "P(x)/Q(x) = A/(x-a) + B/(x-b) + ...",
            "explanation": "Factor the denominator, then set up partial fractions based on factor types."
        },
        
        "method_steps": [
            {
                "step": 1,
                "title": "Check degrees",
                "content": "If degree of numerator ≥ degree of denominator, do polynomial long division first.",
                "tip": "After division, work with the remainder (which will have smaller degree than denominator)."
            },
            {
                "step": 2,
                "title": "Factor the denominator completely",
                "content": "Factor into linear factors (x-a) and irreducible quadratics (x²+bx+c where b²-4c<0).",
                "tip": "This is often the hardest step! Review factoring techniques."
            },
            {
                "step": 3,
                "title": "Set up the decomposition",
                "content": """Based on factor types:
• **Linear factor (x-a)**: Add A/(x-a)
• **Repeated linear (x-a)ⁿ**: Add A₁/(x-a) + A₂/(x-a)² + ... + Aₙ/(x-a)ⁿ
• **Irreducible quadratic (x²+bx+c)**: Add (Ax+B)/(x²+bx+c)
• **Repeated quadratic**: Similar pattern with increasing powers""",
                "tip": "Count your unknowns. You should have the same number as the degree of the denominator."
            },
            {
                "step": 4,
                "title": "Clear the denominator",
                "content": "Multiply both sides by the original denominator to eliminate fractions.",
                "tip": "This gives you a polynomial equation to solve for A, B, C, etc."
            },
            {
                "step": 5,
                "title": "Solve for constants",
                "content": """Two methods:
• **Substitution**: Plug in x values that make factors zero (fast!)
• **Comparing coefficients**: Expand and match powers of x (always works)""",
                "tip": "Usually substitution gets most constants. Use coefficient comparison for the rest."
            },
            {
                "step": 6,
                "title": "Integrate each piece",
                "content": """• A/(x-a) → A·ln|x-a|
• A/(x-a)² → -A/(x-a)
• (Ax+B)/(x²+bx+c) → Often needs completing the square, then arctan and ln""",
                "tip": "The whole point was to get integrals you know how to do!"
            }
        ],
        
        "worked_examples": [
            {
                "title": "Distinct Linear Factors",
                "difficulty": 1,
                "problem": "Evaluate ∫ 1/((x-1)(x+2)) dx",
                "solution": [
                    {
                        "step": "Set up partial fractions:",
                        "math": "\\frac{1}{(x-1)(x+2)} = \\frac{A}{x-1} + \\frac{B}{x+2}"
                    },
                    {
                        "step": "Multiply both sides by (x-1)(x+2):",
                        "math": "1 = A(x+2) + B(x-1)"
                    },
                    {
                        "step": "Substitution method - let x = 1:",
                        "math": "1 = A(3) + B(0) \\Rightarrow A = \\frac{1}{3}"
                    },
                    {
                        "step": "Let x = -2:",
                        "math": "1 = A(0) + B(-3) \\Rightarrow B = -\\frac{1}{3}"
                    },
                    {
                        "step": "Rewrite and integrate:",
                        "math": "\\int \\left( \\frac{1/3}{x-1} - \\frac{1/3}{x+2} \\right) dx"
                    },
                    {
                        "step": "Final answer:",
                        "math": "= \\frac{1}{3}\\ln|x-1| - \\frac{1}{3}\\ln|x+2| + C = \\frac{1}{3}\\ln\\left|\\frac{x-1}{x+2}\\right| + C"
                    }
                ],
                "key_insight": "Substituting the roots of each factor is the fastest way to find the constants.",
                "common_mistakes": [
                    "Forgetting absolute values in ln",
                    "Sign errors when factoring the denominator"
                ]
            },
            {
                "title": "Repeated Linear Factor",
                "difficulty": 2,
                "problem": "Evaluate ∫ (2x+1)/((x-1)²(x+1)) dx",
                "solution": [
                    {
                        "step": "Set up for repeated factor (x-1)²:",
                        "math": "\\frac{2x+1}{(x-1)^2(x+1)} = \\frac{A}{x-1} + \\frac{B}{(x-1)^2} + \\frac{C}{x+1}"
                    },
                    {
                        "step": "Multiply by (x-1)²(x+1):",
                        "math": "2x+1 = A(x-1)(x+1) + B(x+1) + C(x-1)^2"
                    },
                    {
                        "step": "Let x = 1:",
                        "math": "3 = A(0) + B(2) + C(0) \\Rightarrow B = \\frac{3}{2}"
                    },
                    {
                        "step": "Let x = -1:",
                        "math": "-1 = A(0) + B(0) + C(4) \\Rightarrow C = -\\frac{1}{4}"
                    },
                    {
                        "step": "For A, compare x² coefficients: Left has 0, Right has A + C",
                        "math": "0 = A + C = A - \\frac{1}{4} \\Rightarrow A = \\frac{1}{4}"
                    },
                    {
                        "step": "Integrate:",
                        "math": "\\int \\left( \\frac{1/4}{x-1} + \\frac{3/2}{(x-1)^2} - \\frac{1/4}{x+1} \\right) dx"
                    },
                    {
                        "step": "Final answer:",
                        "math": "= \\frac{1}{4}\\ln|x-1| - \\frac{3}{2(x-1)} - \\frac{1}{4}\\ln|x+1| + C"
                    }
                ],
                "key_insight": "Repeated factors need multiple terms: (x-a)² requires both A/(x-a) AND B/(x-a)²",
                "common_mistakes": [
                    "Only writing one term for repeated factors",
                    "Forgetting that ∫1/(x-a)² = -1/(x-a), not ln"
                ]
            },
            {
                "title": "Irreducible Quadratic",
                "difficulty": 2,
                "problem": "Evaluate ∫ (x+2)/(x(x²+1)) dx",
                "solution": [
                    {
                        "step": "x²+1 doesn't factor (discriminant < 0). Set up:",
                        "math": "\\frac{x+2}{x(x^2+1)} = \\frac{A}{x} + \\frac{Bx+C}{x^2+1}"
                    },
                    {
                        "step": "Multiply by x(x²+1):",
                        "math": "x+2 = A(x^2+1) + (Bx+C)(x)"
                    },
                    {
                        "step": "Let x = 0:",
                        "math": "2 = A(1) + 0 \\Rightarrow A = 2"
                    },
                    {
                        "step": "Compare x² coefficients:",
                        "math": "0 = A + B = 2 + B \\Rightarrow B = -2"
                    },
                    {
                        "step": "Compare x coefficients:",
                        "math": "1 = C"
                    },
                    {
                        "step": "Rewrite:",
                        "math": "\\int \\left( \\frac{2}{x} + \\frac{-2x+1}{x^2+1} \\right) dx"
                    },
                    {
                        "step": "Split the quadratic term:",
                        "math": "= \\int \\frac{2}{x} \\, dx - \\int \\frac{2x}{x^2+1} \\, dx + \\int \\frac{1}{x^2+1} \\, dx"
                    },
                    {
                        "step": "Integrate (middle term: u-sub with u = x²+1):",
                        "math": "= 2\\ln|x| - \\ln(x^2+1) + \\arctan(x) + C"
                    }
                ],
                "key_insight": "For irreducible quadratics, put (Ax+B) in numerator. Then split into a ln piece and an arctan piece.",
                "common_mistakes": [
                    "Putting just A (not Ax+B) over the quadratic",
                    "Not splitting the integral to get ln and arctan separately"
                ]
            }
        ],
        
        "practice_problems": [
            {"problem": "∫ 1/(x²-1) dx", "answer": "(1/2)ln|(x-1)/(x+1)| + C", "difficulty": 1},
            {"problem": "∫ x/(x²-4) dx", "answer": "(1/2)ln|x²-4| + C (or u-sub!)", "difficulty": 1},
            {"problem": "∫ 1/(x²+2x) dx", "answer": "(1/2)ln|x/(x+2)| + C", "difficulty": 1},
            {"problem": "∫ (x+1)/((x-2)²) dx", "answer": "ln|x-2| - 3/(x-2) + C", "difficulty": 2},
            {"problem": "∫ 1/(x³-x) dx", "answer": "-ln|x| + (1/2)ln|x²-1| + C", "difficulty": 2},
            {"problem": "∫ 1/(x²+1)² dx", "answer": "(x/(2(x²+1))) + (1/2)arctan(x) + C", "difficulty": 3},
        ],
        
        "common_mistakes": [
            {
                "mistake": "Forgetting to check degrees first",
                "why_it_happens": "Jumping straight to partial fractions without checking if numerator degree ≥ denominator degree",
                "how_to_avoid": "Always compare degrees first. If num ≥ den, do long division!"
            },
            {
                "mistake": "Wrong setup for repeated factors",
                "why_it_happens": "Writing only one term for (x-a)² instead of two",
                "how_to_avoid": "(x-a)ⁿ needs n terms: A₁/(x-a) + A₂/(x-a)² + ... + Aₙ/(x-a)ⁿ"
            },
            {
                "mistake": "Only A over irreducible quadratic",
                "why_it_happens": "Treating x²+bx+c like a linear factor",
                "how_to_avoid": "Irreducible quadratics need (Ax+B) on top, not just A"
            },
            {
                "mistake": "Arithmetic errors solving for constants",
                "why_it_happens": "The algebra can get messy",
                "how_to_avoid": "Check by substituting your A, B, C back in and simplifying"
            }
        ],
        
        "exam_tips": [
            "Factor the denominator FIRST - everything depends on this",
            "Use substitution for quick wins, then coefficient comparison for remaining unknowns",
            "Remember: degree of numerator should be less than degree of denominator",
            "Know your resulting integrals: ln for linear, arctan for irreducible quadratics"
        ]
    },
    
    "sequences_series": {
        "title": "Sequences and Series",
        "subtitle": "Does it add up to something, or blow up to infinity?",
        "estimated_time": "60 min",
        "prerequisites": ["limits", "basic_integration"],
        
        "conceptual_intro": """
## The Big Picture

A **sequence** is a list of numbers: a₁, a₂, a₃, ...
A **series** is what happens when you try to ADD them: a₁ + a₂ + a₃ + ...

### The Central Question

**Does the series CONVERGE (add up to a finite number) or DIVERGE (grow without bound)?**

This is perhaps THE most important question in Calc II series work.

### Why Does This Matter?

Series aren't just abstract math - they let us:
- Represent functions as infinite polynomials (Taylor series!)
- Approximate calculations (how calculators work)
- Solve differential equations
- Model real-world processes (finance, physics, etc.)
""",
        
        "key_formulas": [
            {
                "name": "Geometric Series",
                "latex": "\\sum_{n=0}^{\\infty} ar^n = \\frac{a}{1-r} \\text{ if } |r| < 1",
                "plain": "Σarⁿ = a/(1-r) if |r| < 1",
                "explanation": "The most important series formula! Converges only when |r| < 1."
            },
            {
                "name": "p-Series",
                "latex": "\\sum_{n=1}^{\\infty} \\frac{1}{n^p} \\text{ converges iff } p > 1",
                "plain": "Σ1/nᵖ converges if and only if p > 1",
                "explanation": "p = 1 (harmonic series) diverges! p = 2 converges to π²/6."
            }
        ],
        
        "method_steps": [
            {
                "step": 1,
                "title": "Divergence Test (always try first!)",
                "content": "If lim(n→∞) aₙ ≠ 0, the series DIVERGES.",
                "tip": "CAUTION: If the limit IS 0, this test tells you NOTHING! The series might still diverge (like the harmonic series)."
            },
            {
                "step": 2,
                "title": "Recognize special series",
                "content": """Check if it's:
• Geometric: Σarⁿ → converges if |r| < 1
• p-series: Σ1/nᵖ → converges if p > 1
• Telescoping: Terms cancel in partial sums""",
                "tip": "These are the 'easy wins' - if you recognize one, you're done!"
            },
            {
                "step": 3,
                "title": "Comparison Tests",
                "content": """Compare to a known series:
• Direct: If aₙ ≤ bₙ and Σbₙ converges → Σaₙ converges
• Limit: If lim(aₙ/bₙ) = L > 0, both series behave the same""",
                "tip": "Compare to geometric or p-series. Limit comparison is often easier."
            },
            {
                "step": 4,
                "title": "Ratio Test (great for factorials/exponentials)",
                "content": "L = lim |aₙ₊₁/aₙ|. If L < 1 converges, L > 1 diverges, L = 1 inconclusive.",
                "tip": "Best when terms have n!, nⁿ, or aⁿ in them."
            },
            {
                "step": 5,
                "title": "Root Test (for nth powers)",
                "content": "L = lim ⁿ√|aₙ|. Same rules as ratio test.",
                "tip": "Best when the whole term is raised to the nth power."
            },
            {
                "step": 6,
                "title": "Integral Test (when terms look like f(n))",
                "content": "If f is positive, continuous, decreasing, then Σf(n) and ∫f(x)dx behave the same.",
                "tip": "Useful when terms involve ln(n) or other functions you can integrate."
            },
            {
                "step": 7,
                "title": "Alternating Series Test",
                "content": "For Σ(-1)ⁿbₙ: converges if bₙ→0 AND bₙ is decreasing.",
                "tip": "This tests CONDITIONAL convergence. Check absolute convergence separately."
            }
        ],
        
        "worked_examples": [
            {
                "title": "Geometric Series",
                "difficulty": 1,
                "problem": "Does Σ(n=0 to ∞) (2/3)ⁿ converge? If so, find the sum.",
                "solution": [
                    {
                        "step": "Identify as geometric: a = 1, r = 2/3",
                        "math": "\\sum_{n=0}^{\\infty} \\left(\\frac{2}{3}\\right)^n = \\sum_{n=0}^{\\infty} 1 \\cdot \\left(\\frac{2}{3}\\right)^n"
                    },
                    {
                        "step": "Check |r| < 1:",
                        "math": "|r| = \\frac{2}{3} < 1 \\quad \\checkmark"
                    },
                    {
                        "step": "Apply formula:",
                        "math": "= \\frac{a}{1-r} = \\frac{1}{1-\\frac{2}{3}} = \\frac{1}{\\frac{1}{3}} = 3"
                    }
                ],
                "key_insight": "Geometric series is the bread and butter. Memorize: |r| < 1 converges to a/(1-r).",
                "common_mistakes": [
                    "Forgetting to check |r| < 1",
                    "Using wrong formula (it's a/(1-r), not a/(r-1))"
                ]
            },
            {
                "title": "Ratio Test with Factorials",
                "difficulty": 2,
                "problem": "Does Σ(n=1 to ∞) n!/nⁿ converge?",
                "solution": [
                    {
                        "step": "Ratio test is perfect for factorials:",
                        "math": "L = \\lim_{n\\to\\infty} \\left| \\frac{a_{n+1}}{a_n} \\right|"
                    },
                    {
                        "step": "Write the ratio:",
                        "math": "= \\lim_{n\\to\\infty} \\frac{(n+1)!}{(n+1)^{n+1}} \\cdot \\frac{n^n}{n!}"
                    },
                    {
                        "step": "Simplify factorials: (n+1)!/n! = n+1",
                        "math": "= \\lim_{n\\to\\infty} (n+1) \\cdot \\frac{n^n}{(n+1)^{n+1}}"
                    },
                    {
                        "step": "Simplify powers:",
                        "math": "= \\lim_{n\\to\\infty} \\frac{n^n}{(n+1)^n} = \\lim_{n\\to\\infty} \\left(\\frac{n}{n+1}\\right)^n"
                    },
                    {
                        "step": "Recognize the limit:",
                        "math": "= \\lim_{n\\to\\infty} \\left(\\frac{1}{1+\\frac{1}{n}}\\right)^n = \\frac{1}{e}"
                    },
                    {
                        "step": "Since L = 1/e < 1, the series CONVERGES",
                        "math": "L = \\frac{1}{e} \\approx 0.368 < 1 \\quad \\Rightarrow \\text{converges}"
                    }
                ],
                "key_insight": "Ratio test + factorial simplification is a powerful combination. The (1+1/n)ⁿ→e pattern appears often!",
                "common_mistakes": [
                    "Algebra errors when simplifying the ratio",
                    "Not recognizing the e limit"
                ]
            },
            {
                "title": "Integral Test",
                "difficulty": 2,
                "problem": "Does Σ(n=2 to ∞) 1/(n·ln(n)) converge?",
                "solution": [
                    {
                        "step": "Check conditions: f(x) = 1/(x·ln(x)) is positive, continuous, decreasing for x ≥ 2 ✓",
                        "math": "\\text{Integral test applies}"
                    },
                    {
                        "step": "Evaluate the improper integral:",
                        "math": "\\int_2^{\\infty} \\frac{1}{x \\ln(x)} \\, dx"
                    },
                    {
                        "step": "Substitution: u = ln(x), du = (1/x)dx",
                        "math": "= \\int_{\\ln 2}^{\\infty} \\frac{1}{u} \\, du"
                    },
                    {
                        "step": "Evaluate:",
                        "math": "= \\left[ \\ln|u| \\right]_{\\ln 2}^{\\infty} = \\ln(\\infty) - \\ln(\\ln 2) = \\infty"
                    },
                    {
                        "step": "Integral diverges, so series DIVERGES",
                        "math": "\\sum_{n=2}^{\\infty} \\frac{1}{n \\ln(n)} \\text{ diverges}"
                    }
                ],
                "key_insight": "When you see ln(n) in the denominator, integral test with u = ln(x) often works.",
                "common_mistakes": [
                    "Trying ratio test (gives L = 1, inconclusive)",
                    "Forgetting to change limits when substituting"
                ]
            }
        ],
        
        "convergence_test_flowchart": """
## Which Test Should I Use? Decision Tree

1. **Does lim aₙ = 0?**
   - NO → Series DIVERGES (Divergence Test)
   - YES → Continue...

2. **Is it a special series?**
   - Geometric (arⁿ) → Use |r| < 1 rule
   - p-series (1/nᵖ) → Use p > 1 rule
   - Alternating → Try Alternating Series Test

3. **Does it have factorials or aⁿ?**
   - YES → Use Ratio Test

4. **Is the term raised to the nth power?**
   - YES → Use Root Test

5. **Can you compare to a known series?**
   - YES → Use Comparison or Limit Comparison

6. **Can you integrate f(x)?**
   - YES → Use Integral Test
""",
        
        "practice_problems": [
            {"problem": "Does Σ(n=1 to ∞) n/(n+1) converge?", "answer": "Diverges (lim aₙ = 1 ≠ 0)", "difficulty": 1},
            {"problem": "Does Σ(n=1 to ∞) 1/n² converge?", "answer": "Converges (p-series, p=2>1)", "difficulty": 1},
            {"problem": "Does Σ(n=1 to ∞) n/2ⁿ converge?", "answer": "Converges (ratio test, L=1/2)", "difficulty": 2},
            {"problem": "Does Σ(n=1 to ∞) 1/√n converge?", "answer": "Diverges (p-series, p=1/2<1)", "difficulty": 1},
            {"problem": "Find sum of Σ(n=1 to ∞) 3/4ⁿ", "answer": "1 (geometric, a=3/4, r=1/4)", "difficulty": 1},
            {"problem": "Does Σ(n=1 to ∞) (-1)ⁿ/n converge?", "answer": "Converges conditionally (alt series test)", "difficulty": 2},
        ],
        
        "exam_tips": [
            "ALWAYS try divergence test first - it's quick and catches many divergent series",
            "Memorize geometric and p-series - they're the foundation for comparisons",
            "Ratio test is your best friend for factorials and exponentials",
            "When in doubt, try limit comparison with a p-series"
        ]
    },
    
    "taylor_series": {
        "title": "Taylor and Maclaurin Series",
        "subtitle": "Representing any function as an infinite polynomial",
        "estimated_time": "55 min",
        "prerequisites": ["derivatives", "sequences_series"],
        
        "conceptual_intro": """
## The Big Picture

Taylor series lets you write **any smooth function as an infinite polynomial**:

f(x) = c₀ + c₁(x-a) + c₂(x-a)² + c₃(x-a)³ + ...

The magic is figuring out what c₀, c₁, c₂, ... should be!

### The Key Insight

If f(x) = c₀ + c₁(x-a) + c₂(x-a)² + ..., then:
- f(a) = c₀
- f'(a) = c₁
- f''(a) = 2·c₂, so c₂ = f''(a)/2
- f'''(a) = 6·c₃, so c₃ = f'''(a)/6
- Pattern: **cₙ = f⁽ⁿ⁾(a)/n!**

### Taylor vs Maclaurin

- **Taylor series**: Centered at x = a (any point)
- **Maclaurin series**: Centered at x = 0 (special case of Taylor)
""",
        
        "key_formula": {
            "latex": "f(x) = \\sum_{n=0}^{\\infty} \\frac{f^{(n)}(a)}{n!}(x-a)^n",
            "plain": "f(x) = Σ f⁽ⁿ⁾(a)/n! · (x-a)ⁿ",
            "explanation": "The coefficient of (x-a)ⁿ is the nth derivative at a, divided by n!."
        },
        
        "must_memorize": [
            {
                "function": "eˣ",
                "series": "1 + x + x²/2! + x³/3! + ... = Σxⁿ/n!",
                "latex": "e^x = \\sum_{n=0}^{\\infty} \\frac{x^n}{n!}",
                "radius": "R = ∞ (converges for all x)"
            },
            {
                "function": "sin(x)",
                "series": "x - x³/3! + x⁵/5! - ... = Σ(-1)ⁿx²ⁿ⁺¹/(2n+1)!",
                "latex": "\\sin(x) = \\sum_{n=0}^{\\infty} \\frac{(-1)^n x^{2n+1}}{(2n+1)!}",
                "radius": "R = ∞"
            },
            {
                "function": "cos(x)",
                "series": "1 - x²/2! + x⁴/4! - ... = Σ(-1)ⁿx²ⁿ/(2n)!",
                "latex": "\\cos(x) = \\sum_{n=0}^{\\infty} \\frac{(-1)^n x^{2n}}{(2n)!}",
                "radius": "R = ∞"
            },
            {
                "function": "1/(1-x)",
                "series": "1 + x + x² + x³ + ... = Σxⁿ",
                "latex": "\\frac{1}{1-x} = \\sum_{n=0}^{\\infty} x^n",
                "radius": "R = 1 (|x| < 1)"
            },
            {
                "function": "ln(1+x)",
                "series": "x - x²/2 + x³/3 - ... = Σ(-1)ⁿ⁺¹xⁿ/n",
                "latex": "\\ln(1+x) = \\sum_{n=1}^{\\infty} \\frac{(-1)^{n+1} x^n}{n}",
                "radius": "R = 1 (-1 < x ≤ 1)"
            },
            {
                "function": "arctan(x)",
                "series": "x - x³/3 + x⁵/5 - ... = Σ(-1)ⁿx²ⁿ⁺¹/(2n+1)",
                "latex": "\\arctan(x) = \\sum_{n=0}^{\\infty} \\frac{(-1)^n x^{2n+1}}{2n+1}",
                "radius": "R = 1 (-1 ≤ x ≤ 1)"
            }
        ],
        
        "method_steps": [
            {
                "step": 1,
                "title": "Choose center a",
                "content": "For Maclaurin, a = 0. For Taylor, choose a value where derivatives are easy.",
                "tip": "Common choices: a = 0, 1, π/2, etc. - wherever f and its derivatives are simple."
            },
            {
                "step": 2,
                "title": "Compute derivatives at a",
                "content": "Find f(a), f'(a), f''(a), f'''(a), ... Look for a pattern!",
                "tip": "You often only need 4-5 derivatives to spot the pattern."
            },
            {
                "step": 3,
                "title": "Write the series",
                "content": "f(x) = f(a) + f'(a)(x-a) + f''(a)(x-a)²/2! + f'''(a)(x-a)³/3! + ...",
                "tip": "If you see the pattern, write the general term with Σ notation."
            },
            {
                "step": 4,
                "title": "Find the radius of convergence",
                "content": "Use ratio test on the series to find R. The series converges for |x-a| < R.",
                "tip": "Check endpoints separately! They might converge at one, both, or neither."
            }
        ],
        
        "worked_examples": [
            {
                "title": "Build from Scratch: Maclaurin for eˣ",
                "difficulty": 1,
                "problem": "Find the Maclaurin series for f(x) = eˣ",
                "solution": [
                    {
                        "step": "Find derivatives at x = 0:",
                        "math": "f(x) = e^x, f'(x) = e^x, f''(x) = e^x, \\ldots"
                    },
                    {
                        "step": "All derivatives equal eˣ, so at x = 0:",
                        "math": "f(0) = f'(0) = f''(0) = \\cdots = e^0 = 1"
                    },
                    {
                        "step": "Apply Taylor formula:",
                        "math": "e^x = \\sum_{n=0}^{\\infty} \\frac{1}{n!} x^n = 1 + x + \\frac{x^2}{2!} + \\frac{x^3}{3!} + \\cdots"
                    },
                    {
                        "step": "Find radius: Ratio test",
                        "math": "L = \\lim_{n\\to\\infty} \\left| \\frac{x^{n+1}/(n+1)!}{x^n/n!} \\right| = \\lim_{n\\to\\infty} \\frac{|x|}{n+1} = 0"
                    },
                    {
                        "step": "Since L = 0 < 1 for all x, R = ∞",
                        "math": "\\text{Series converges for all } x \\in \\mathbb{R}"
                    }
                ],
                "key_insight": "eˣ is its own derivative! This makes it the simplest Taylor series to derive.",
                "common_mistakes": [
                    "Forgetting the n! in the denominator"
                ]
            },
            {
                "title": "Using Known Series: Find series for e⁻ˣ²",
                "difficulty": 2,
                "problem": "Find the Maclaurin series for f(x) = e⁻ˣ²",
                "solution": [
                    {
                        "step": "Start with the known series for eˣ:",
                        "math": "e^u = \\sum_{n=0}^{\\infty} \\frac{u^n}{n!}"
                    },
                    {
                        "step": "Substitute u = -x²:",
                        "math": "e^{-x^2} = \\sum_{n=0}^{\\infty} \\frac{(-x^2)^n}{n!} = \\sum_{n=0}^{\\infty} \\frac{(-1)^n x^{2n}}{n!}"
                    },
                    {
                        "step": "Write out first few terms:",
                        "math": "= 1 - x^2 + \\frac{x^4}{2!} - \\frac{x^6}{3!} + \\cdots"
                    }
                ],
                "key_insight": "You can often find new series by substituting into known series. Much faster than computing derivatives!",
                "common_mistakes": [
                    "Forgetting that (-x²)ⁿ = (-1)ⁿx²ⁿ, not -x²ⁿ"
                ]
            },
            {
                "title": "Taylor Polynomial Approximation",
                "difficulty": 2,
                "problem": "Use T₃(x) (degree 3 Taylor polynomial) to approximate √(1.1)",
                "solution": [
                    {
                        "step": "Let f(x) = √x = x^(1/2), centered at a = 1 (since 1.1 is close to 1)",
                        "math": "f(x) = x^{1/2}"
                    },
                    {
                        "step": "Compute derivatives:",
                        "math": "f(1) = 1, \\quad f'(x) = \\frac{1}{2}x^{-1/2} \\Rightarrow f'(1) = \\frac{1}{2}"
                    },
                    {
                        "step": "More derivatives:",
                        "math": "f''(x) = -\\frac{1}{4}x^{-3/2} \\Rightarrow f''(1) = -\\frac{1}{4}"
                    },
                    {
                        "step": "Third derivative:",
                        "math": "f'''(x) = \\frac{3}{8}x^{-5/2} \\Rightarrow f'''(1) = \\frac{3}{8}"
                    },
                    {
                        "step": "Build T₃(x):",
                        "math": "T_3(x) = 1 + \\frac{1}{2}(x-1) - \\frac{1/4}{2!}(x-1)^2 + \\frac{3/8}{3!}(x-1)^3"
                    },
                    {
                        "step": "Simplify:",
                        "math": "= 1 + \\frac{1}{2}(x-1) - \\frac{1}{8}(x-1)^2 + \\frac{1}{16}(x-1)^3"
                    },
                    {
                        "step": "Evaluate at x = 1.1:",
                        "math": "T_3(1.1) = 1 + \\frac{1}{2}(0.1) - \\frac{1}{8}(0.01) + \\frac{1}{16}(0.001)"
                    },
                    {
                        "step": "Calculate:",
                        "math": "= 1 + 0.05 - 0.00125 + 0.0000625 \\approx 1.048813"
                    },
                    {
                        "step": "Compare to actual: √1.1 ≈ 1.048809",
                        "math": "\\text{Error} \\approx 0.000004 \\text{ (very small!)}"
                    }
                ],
                "key_insight": "Taylor polynomials give excellent approximations near the center. The farther from center, the more terms needed.",
                "common_mistakes": [
                    "Forgetting to divide by n!",
                    "Using wrong center (should be close to the point you're approximating)"
                ]
            }
        ],
        
        "practice_problems": [
            {"problem": "Find Maclaurin series for sin(x²)", "answer": "Σ(-1)ⁿx^(4n+2)/(2n+1)!", "difficulty": 1},
            {"problem": "Find Maclaurin series for x·eˣ", "answer": "Σx^(n+1)/n! = x + x² + x³/2! + ...", "difficulty": 1},
            {"problem": "Find Taylor series for ln(x) at a=1", "answer": "Σ(-1)^(n+1)(x-1)ⁿ/n", "difficulty": 2},
            {"problem": "Find first 4 terms of Maclaurin for tan(x)", "answer": "x + x³/3 + 2x⁵/15 + ...", "difficulty": 3},
            {"problem": "Use T₂(x) at a=0 to approx e^0.1", "answer": "1 + 0.1 + 0.005 = 1.105", "difficulty": 2},
        ],
        
        "exam_tips": [
            "MEMORIZE the 6 key Maclaurin series - they appear constantly",
            "To find new series, substitute into known series instead of computing derivatives",
            "For approximation problems, choose center a close to the target value",
            "Know how to find radius of convergence using ratio test"
        ]
    },
    
    "polar_coordinates": {
        "title": "Polar Coordinates and Calculus",
        "subtitle": "When rectangular won't cut it",
        "estimated_time": "45 min",
        "prerequisites": ["trig_functions", "basic_integration"],
        
        "conceptual_intro": """
## The Big Picture

Some curves are **incredibly messy** in rectangular (x,y) coordinates but **beautifully simple** in polar (r,θ).

For example:
- Circle centered at origin: x² + y² = 4 becomes r = 2
- Spiral: Complicated in (x,y), simple as r = θ

### The Conversion

**Polar to Rectangular:**
- x = r·cos(θ)
- y = r·sin(θ)

**Rectangular to Polar:**
- r² = x² + y²
- tan(θ) = y/x
""",
        
        "key_formulas": [
            {
                "name": "Area in Polar",
                "latex": "A = \\frac{1}{2} \\int_{\\alpha}^{\\beta} r^2 \\, d\\theta",
                "plain": "A = ½∫[α,β] r² dθ",
                "explanation": "The ½ comes from the area of a circular sector: ½r²θ"
            },
            {
                "name": "Arc Length in Polar",
                "latex": "L = \\int_{\\alpha}^{\\beta} \\sqrt{r^2 + \\left(\\frac{dr}{d\\theta}\\right)^2} \\, d\\theta",
                "plain": "L = ∫√(r² + (dr/dθ)²) dθ",
                "explanation": "Derived from the Pythagorean theorem in polar"
            }
        ],
        
        "common_curves": [
            {
                "name": "Circle through origin",
                "equation": "r = 2a·cos(θ) or r = 2a·sin(θ)",
                "description": "Circle of radius a passing through origin"
            },
            {
                "name": "Cardioid",
                "equation": "r = a(1 + cos(θ)) or r = a(1 + sin(θ))",
                "description": "Heart-shaped curve"
            },
            {
                "name": "Rose",
                "equation": "r = a·cos(nθ) or r = a·sin(nθ)",
                "description": "n petals if n is odd, 2n petals if n is even"
            },
            {
                "name": "Limaçon",
                "equation": "r = a + b·cos(θ)",
                "description": "Snail-shaped curve (inner loop if |b| > |a|)"
            },
            {
                "name": "Spiral",
                "equation": "r = aθ",
                "description": "Archimedes spiral"
            }
        ],
        
        "worked_examples": [
            {
                "title": "Area Inside a Cardioid",
                "difficulty": 2,
                "problem": "Find the area enclosed by r = 1 + cos(θ)",
                "solution": [
                    {
                        "step": "Identify: This is a cardioid. It traces once as θ goes from 0 to 2π.",
                        "math": "A = \\frac{1}{2} \\int_0^{2\\pi} r^2 \\, d\\theta"
                    },
                    {
                        "step": "Substitute r² = (1 + cos(θ))²:",
                        "math": "= \\frac{1}{2} \\int_0^{2\\pi} (1 + \\cos\\theta)^2 \\, d\\theta"
                    },
                    {
                        "step": "Expand:",
                        "math": "= \\frac{1}{2} \\int_0^{2\\pi} (1 + 2\\cos\\theta + \\cos^2\\theta) \\, d\\theta"
                    },
                    {
                        "step": "Use identity: cos²θ = (1 + cos(2θ))/2",
                        "math": "= \\frac{1}{2} \\int_0^{2\\pi} \\left(1 + 2\\cos\\theta + \\frac{1+\\cos 2\\theta}{2}\\right) d\\theta"
                    },
                    {
                        "step": "Simplify:",
                        "math": "= \\frac{1}{2} \\int_0^{2\\pi} \\left(\\frac{3}{2} + 2\\cos\\theta + \\frac{\\cos 2\\theta}{2}\\right) d\\theta"
                    },
                    {
                        "step": "Integrate (note: ∫cos terms over full period = 0):",
                        "math": "= \\frac{1}{2} \\left[ \\frac{3\\theta}{2} + 2\\sin\\theta + \\frac{\\sin 2\\theta}{4} \\right]_0^{2\\pi}"
                    },
                    {
                        "step": "Evaluate:",
                        "math": "= \\frac{1}{2} \\cdot \\frac{3(2\\pi)}{2} = \\frac{3\\pi}{2}"
                    }
                ],
                "key_insight": "When integrating trig functions over a full period, cos and sin terms vanish. Only constants contribute!",
                "common_mistakes": [
                    "Wrong limits of integration",
                    "Forgetting the ½ in the area formula"
                ]
            }
        ],
        
        "exam_tips": [
            "Know the standard polar curves by sight",
            "For area, always use A = ½∫r² dθ - don't forget the ½!",
            "Symmetry can halve your work: if symmetric about x-axis, integrate 0 to π and double"
        ]
    },
    
    "parametric_equations": {
        "title": "Parametric Equations",
        "subtitle": "When x and y both depend on a third variable",
        "estimated_time": "40 min",
        "prerequisites": ["derivatives", "chain_rule"],
        
        "conceptual_intro": """
## The Big Picture

Sometimes it's easier to describe x and y **separately** as functions of a parameter t:
- x = f(t)
- y = g(t)

As t changes, the point (x,y) traces out a curve.

### Classic Example: Circle
Instead of x² + y² = 1, we can write:
- x = cos(t)
- y = sin(t)
- 0 ≤ t ≤ 2π

This traces the unit circle as t goes from 0 to 2π.
""",
        
        "key_formulas": [
            {
                "name": "First Derivative",
                "latex": "\\frac{dy}{dx} = \\frac{dy/dt}{dx/dt}",
                "plain": "dy/dx = (dy/dt)/(dx/dt)",
                "explanation": "Chain rule! Cancel the dt's (sort of)."
            },
            {
                "name": "Second Derivative",
                "latex": "\\frac{d^2y}{dx^2} = \\frac{d}{dt}\\left(\\frac{dy}{dx}\\right) \\cdot \\frac{1}{dx/dt}",
                "plain": "d²y/dx² = (d/dt)(dy/dx) / (dx/dt)",
                "explanation": "Take derivative of first derivative with respect to t, then divide by dx/dt."
            },
            {
                "name": "Arc Length",
                "latex": "L = \\int_a^b \\sqrt{\\left(\\frac{dx}{dt}\\right)^2 + \\left(\\frac{dy}{dt}\\right)^2} \\, dt",
                "plain": "L = ∫√((dx/dt)² + (dy/dt)²) dt",
                "explanation": "Pythagorean theorem applied to infinitesimal displacements."
            }
        ],
        
        "worked_examples": [
            {
                "title": "Finding dy/dx Parametrically",
                "difficulty": 1,
                "problem": "Find dy/dx for x = t³ - t, y = t² at t = 2",
                "solution": [
                    {
                        "step": "Find dx/dt and dy/dt:",
                        "math": "\\frac{dx}{dt} = 3t^2 - 1, \\quad \\frac{dy}{dt} = 2t"
                    },
                    {
                        "step": "Apply formula:",
                        "math": "\\frac{dy}{dx} = \\frac{dy/dt}{dx/dt} = \\frac{2t}{3t^2 - 1}"
                    },
                    {
                        "step": "Evaluate at t = 2:",
                        "math": "\\frac{dy}{dx}\\bigg|_{t=2} = \\frac{2(2)}{3(4) - 1} = \\frac{4}{11}"
                    }
                ],
                "key_insight": "The slope at a point depends on t, not directly on x or y.",
                "common_mistakes": [
                    "Dividing in wrong order",
                    "Forgetting to evaluate at specific t"
                ]
            },
            {
                "title": "Arc Length of Parametric Curve",
                "difficulty": 2,
                "problem": "Find arc length of x = cos(t), y = sin(t) for 0 ≤ t ≤ π",
                "solution": [
                    {
                        "step": "Find derivatives:",
                        "math": "\\frac{dx}{dt} = -\\sin(t), \\quad \\frac{dy}{dt} = \\cos(t)"
                    },
                    {
                        "step": "Compute (dx/dt)² + (dy/dt)²:",
                        "math": "\\sin^2(t) + \\cos^2(t) = 1"
                    },
                    {
                        "step": "Apply arc length formula:",
                        "math": "L = \\int_0^{\\pi} \\sqrt{1} \\, dt = \\int_0^{\\pi} 1 \\, dt = \\pi"
                    },
                    {
                        "step": "This is half the circumference of the unit circle ✓",
                        "math": "\\text{Full circumference} = 2\\pi, \\text{ so half} = \\pi"
                    }
                ],
                "key_insight": "The identity sin²t + cos²t = 1 makes circle arc lengths very clean!",
                "common_mistakes": [
                    "Forgetting the square root in the formula",
                    "Wrong limits of integration"
                ]
            }
        ],
        
        "exam_tips": [
            "dy/dx = (dy/dt)/(dx/dt) - memorize this!",
            "For second derivative, don't just differentiate dy/dx with respect to x directly",
            "Arc length formula: √((dx/dt)² + (dy/dt)²) - Pythagorean!"
        ]
    }
}

# Function to get a specific lesson
def get_lesson(topic: str) -> dict:
    """Get the full lesson content for a topic"""
    return DEEP_LESSONS.get(topic, {})

# Function to get all topic names
def get_all_topics() -> list:
    """Get list of all available topics"""
    return list(DEEP_LESSONS.keys())

# Function to get a lesson summary
def get_lesson_summary(topic: str) -> dict:
    """Get a brief summary of a lesson"""
    lesson = DEEP_LESSONS.get(topic, {})
    return {
        "title": lesson.get("title", ""),
        "subtitle": lesson.get("subtitle", ""),
        "estimated_time": lesson.get("estimated_time", ""),
        "num_examples": len(lesson.get("worked_examples", [])),
        "num_practice": len(lesson.get("practice_problems", []))
    }
