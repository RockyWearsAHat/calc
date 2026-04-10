"""
Comprehensive Teaching Engine for Calculus II
Combines pre-built lessons with AI-generated content for a complete learning experience.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import asyncio

# Deep, comprehensive lessons for each Calc II topic
COMPREHENSIVE_LESSONS = {
    "integration_by_parts": {
        "title": "Integration by Parts",
        "subtitle": "Turning complex products into manageable integrals",
        "estimated_time": "45-60 minutes",
        
        "why_it_matters": """
Integration by parts is one of the most powerful techniques in Calculus II. 
It transforms integrals of PRODUCTS into simpler forms. Without it, integrals 
like ∫x·eˣdx or ∫ln(x)dx would be impossible to solve with basic techniques.

Think of it as the integration equivalent of the product rule for derivatives.
""",
        
        "intuition": """
**The Big Idea**: When you have two functions multiplied together, you can 
"transfer" the derivative from one to the other.

Imagine you're trying to find the area under x·eˣ. The x part is simple, 
but multiplied by eˣ makes it complex. Integration by parts lets you 
"move" the complexity around until it simplifies.

**Analogy**: It's like solving a puzzle by rearranging pieces. Sometimes 
the integral looks hard, but if you shuffle which part gets differentiated 
vs integrated, it becomes easy.
""",
        
        "the_formula": {
            "main": "∫u·dv = u·v - ∫v·du",
            "explanation": """
- **u** = the part you'll DIFFERENTIATE (it should get simpler)
- **dv** = the part you'll INTEGRATE (you need to be able to integrate it)
- **v** = the integral of dv
- **du** = the derivative of u

The formula says: the integral of u·dv equals u times v, minus the integral of v times du.
""",
            "derivation": """
This comes from the product rule for derivatives:
d(uv) = u·dv + v·du

Rearranging: u·dv = d(uv) - v·du

Integrating both sides: ∫u·dv = uv - ∫v·du
"""
        },
        
        "the_liate_rule": {
            "title": "LIATE: How to Choose u",
            "description": "Choose u in this priority order (whichever comes FIRST):",
            "order": [
                {"letter": "L", "type": "Logarithmic", "examples": "ln(x), log(x)", "why": "Differentiating logs gives simpler algebraic expressions"},
                {"letter": "I", "type": "Inverse Trig", "examples": "arcsin(x), arctan(x)", "why": "Differentiating removes the inverse trig"},
                {"letter": "A", "type": "Algebraic", "examples": "x, x², x³, polynomials", "why": "Each derivative reduces the power"},
                {"letter": "T", "type": "Trigonometric", "examples": "sin(x), cos(x), tan(x)", "why": "Trig functions cycle when differentiated"},
                {"letter": "E", "type": "Exponential", "examples": "eˣ, 2ˣ, e³ˣ", "why": "Stays the same when integrated - easy to work with as dv"}
            ],
            "key_insight": "The function that SIMPLIFIES when differentiated should be u. The function you CAN integrate should be dv."
        },
        
        "worked_examples": [
            {
                "problem": "∫ x·eˣ dx",
                "difficulty": "Basic",
                "setup": "Product of algebraic (x) and exponential (eˣ). By LIATE, u = x.",
                "steps": [
                    {
                        "title": "Identify u and dv using LIATE",
                        "content": "x is Algebraic, eˣ is Exponential. A comes before E in LIATE.",
                        "math": "u = x \\quad \\text{and} \\quad dv = e^x dx"
                    },
                    {
                        "title": "Find du and v",
                        "content": "Differentiate u to get du. Integrate dv to get v.",
                        "math": "du = dx \\quad \\text{and} \\quad v = e^x"
                    },
                    {
                        "title": "Apply the formula",
                        "content": "Substitute into ∫u·dv = u·v - ∫v·du",
                        "math": "\\int x \\cdot e^x dx = x \\cdot e^x - \\int e^x dx"
                    },
                    {
                        "title": "Evaluate the remaining integral",
                        "content": "∫eˣdx is just eˣ",
                        "math": "= x \\cdot e^x - e^x + C"
                    },
                    {
                        "title": "Simplify (optional)",
                        "content": "Factor out eˣ for a cleaner answer",
                        "math": "= e^x(x - 1) + C"
                    }
                ],
                "answer": "eˣ(x - 1) + C",
                "key_takeaway": "The integral simplified because differentiating x gave just 1."
            },
            {
                "problem": "∫ ln(x) dx",
                "difficulty": "Intermediate",
                "setup": "There's only one function! Trick: write it as ln(x)·1 = ln(x)·dx",
                "steps": [
                    {
                        "title": "Rewrite as a product",
                        "content": "Think of it as ∫ln(x)·1 dx. Now we have a product!",
                        "math": "\\int \\ln(x) dx = \\int \\ln(x) \\cdot 1 \\, dx"
                    },
                    {
                        "title": "Choose u and dv",
                        "content": "ln(x) is Logarithmic (first in LIATE), so u = ln(x). dv = dx.",
                        "math": "u = \\ln(x), \\quad dv = dx"
                    },
                    {
                        "title": "Find du and v",
                        "content": "Differentiate ln(x), integrate 1.",
                        "math": "du = \\frac{1}{x}dx, \\quad v = x"
                    },
                    {
                        "title": "Apply the formula",
                        "content": "∫u·dv = u·v - ∫v·du",
                        "math": "= x\\ln(x) - \\int x \\cdot \\frac{1}{x} dx = x\\ln(x) - \\int 1 \\, dx"
                    },
                    {
                        "title": "Finish",
                        "content": "∫1 dx = x",
                        "math": "= x\\ln(x) - x + C"
                    }
                ],
                "answer": "x·ln(x) - x + C  or  x(ln(x) - 1) + C",
                "key_takeaway": "Sometimes there's only one function. Pair it with '1' to use integration by parts."
            },
            {
                "problem": "∫ eˣ·cos(x) dx",
                "difficulty": "Advanced",
                "setup": "Neither function simplifies! This requires IBP TWICE and solving for the original integral.",
                "steps": [
                    {
                        "title": "First application of IBP",
                        "content": "Choose u = cos(x), dv = eˣdx (either choice works due to cycling)",
                        "math": "u = \\cos(x), dv = e^x dx \\Rightarrow du = -\\sin(x)dx, v = e^x"
                    },
                    {
                        "title": "Apply formula",
                        "content": "This creates a new integral with sin(x)",
                        "math": "\\int e^x \\cos(x) dx = e^x \\cos(x) + \\int e^x \\sin(x) dx"
                    },
                    {
                        "title": "Apply IBP again to new integral",
                        "content": "u = sin(x), dv = eˣdx → du = cos(x)dx, v = eˣ",
                        "math": "\\int e^x \\sin(x) dx = e^x \\sin(x) - \\int e^x \\cos(x) dx"
                    },
                    {
                        "title": "Substitute back",
                        "content": "Let I = ∫eˣcos(x)dx. We now have I = eˣcos(x) + eˣsin(x) - I",
                        "math": "I = e^x\\cos(x) + e^x\\sin(x) - I"
                    },
                    {
                        "title": "Solve for I",
                        "content": "Add I to both sides, then divide by 2",
                        "math": "2I = e^x(\\cos(x) + \\sin(x)) \\Rightarrow I = \\frac{e^x(\\cos(x) + \\sin(x))}{2} + C"
                    }
                ],
                "answer": "(eˣ/2)(cos(x) + sin(x)) + C",
                "key_takeaway": "When IBP cycles back to the original integral, call it 'I', substitute, and solve algebraically."
            }
        ],
        
        "common_mistakes": [
            {
                "mistake": "Wrong choice of u",
                "example": "Choosing u = eˣ in ∫x·eˣdx",
                "why_wrong": "Differentiating eˣ keeps it as eˣ, so the integral doesn't simplify",
                "fix": "Use LIATE. Algebraic (x) comes before Exponential (eˣ), so u = x"
            },
            {
                "mistake": "Forgetting to include dx in dv",
                "example": "Writing dv = eˣ instead of dv = eˣdx",
                "why_wrong": "The 'dx' is essential - without it, you can't properly find v",
                "fix": "Always write dv = (function)dx, then integrate to get v"
            },
            {
                "mistake": "Stopping after one IBP when two are needed",
                "example": "Giving up on ∫x²eˣdx after one round",
                "why_wrong": "Some integrals need multiple applications",
                "fix": "If the result still has a product, apply IBP again. x² → x → 1 takes two rounds."
            },
            {
                "mistake": "Sign errors in the formula",
                "example": "Writing u·v + ∫v·du instead of u·v - ∫v·du",
                "why_wrong": "The minus sign is critical to the formula",
                "fix": "Memorize: ∫u dv = uv MINUS ∫v du. The minus comes from the product rule derivation."
            }
        ],
        
        "recognition_patterns": [
            "Product of polynomial and exponential: x·eˣ, x²·e³ˣ",
            "Product of polynomial and trig: x·sin(x), x²·cos(x)",
            "Product of polynomial and logarithm: x·ln(x)",
            "Logarithm alone: ln(x), ln(x²)",
            "Inverse trig alone: arctan(x), arcsin(x)",
            "Product of exponential and trig: eˣ·sin(x), eˣ·cos(x) (requires IBP twice)"
        ],
        
        "practice_problems": [
            {"problem": "∫ x·sin(x) dx", "answer": "-x·cos(x) + sin(x) + C", "difficulty": 1},
            {"problem": "∫ x²·eˣ dx", "answer": "eˣ(x² - 2x + 2) + C", "difficulty": 2},
            {"problem": "∫ arctan(x) dx", "answer": "x·arctan(x) - ½ln(1+x²) + C", "difficulty": 2},
            {"problem": "∫ x·ln(x) dx", "answer": "(x²/2)ln(x) - x²/4 + C", "difficulty": 2},
            {"problem": "∫ eˣ·sin(x) dx", "answer": "(eˣ/2)(sin(x) - cos(x)) + C", "difficulty": 3}
        ],
        
        "quick_reference": {
            "formula": "∫u dv = uv - ∫v du",
            "liate": "L-I-A-T-E: Logs, Inverse trig, Algebraic, Trig, Exponential",
            "key_insight": "Choose u to be the function that SIMPLIFIES when differentiated"
        }
    },
    
    "partial_fractions": {
        "title": "Partial Fraction Decomposition",
        "subtitle": "Breaking complex fractions into simple, integrable pieces",
        "estimated_time": "45-60 minutes",
        
        "why_it_matters": """
Many real-world problems lead to integrals of rational functions (polynomial/polynomial).
Direct integration is often impossible, but by decomposing into simpler fractions,
each piece becomes easy to integrate using basic formulas.

This technique is essential for: differential equations, Laplace transforms, 
control systems, and anywhere rational functions appear.
""",
        
        "intuition": """
**The Big Idea**: Just like 7/12 = 1/3 + 1/4, we can split complex fractions 
into sums of simpler ones.

**Example**: 1/(x²-1) looks hard to integrate. But 1/(x²-1) = 1/(2(x-1)) - 1/(2(x+1)).
Now each piece is a simple ∫1/(x-a) = ln|x-a| integral!

**The Process**:
1. Factor the denominator completely
2. Write the form of the decomposition (based on factor types)
3. Solve for the unknown constants (A, B, C, etc.)
4. Integrate each simple piece
""",
        
        "the_method": {
            "prerequisite": "The degree of the numerator must be LESS than the degree of the denominator. If not, do polynomial long division first.",
            "factor_types": [
                {
                    "type": "Linear factors (x - a)",
                    "form": "A/(x-a)",
                    "example": "1/(x-2) gives term A/(x-2)"
                },
                {
                    "type": "Repeated linear factors (x - a)ⁿ",
                    "form": "A₁/(x-a) + A₂/(x-a)² + ... + Aₙ/(x-a)ⁿ",
                    "example": "1/(x-2)³ gives A/(x-2) + B/(x-2)² + C/(x-2)³"
                },
                {
                    "type": "Irreducible quadratic (ax² + bx + c)",
                    "form": "(Ax + B)/(ax² + bx + c)",
                    "example": "1/(x²+1) gives (Ax+B)/(x²+1)"
                },
                {
                    "type": "Repeated irreducible quadratic",
                    "form": "(A₁x + B₁)/(ax²+bx+c) + (A₂x + B₂)/(ax²+bx+c)² + ...",
                    "example": "1/(x²+1)² gives (Ax+B)/(x²+1) + (Cx+D)/(x²+1)²"
                }
            ]
        },
        
        "worked_examples": [
            {
                "problem": "∫ 1/(x²-1) dx",
                "difficulty": "Basic",
                "setup": "Factor denominator: x²-1 = (x-1)(x+1). Two distinct linear factors.",
                "steps": [
                    {
                        "title": "Factor the denominator",
                        "content": "x² - 1 is a difference of squares",
                        "math": "x^2 - 1 = (x-1)(x+1)"
                    },
                    {
                        "title": "Set up partial fractions",
                        "content": "Two distinct linear factors → A/(x-1) + B/(x+1)",
                        "math": "\\frac{1}{(x-1)(x+1)} = \\frac{A}{x-1} + \\frac{B}{x+1}"
                    },
                    {
                        "title": "Clear denominators",
                        "content": "Multiply both sides by (x-1)(x+1)",
                        "math": "1 = A(x+1) + B(x-1)"
                    },
                    {
                        "title": "Solve for A and B",
                        "content": "Plug in x=1: 1 = A(2) → A = 1/2. Plug in x=-1: 1 = B(-2) → B = -1/2",
                        "math": "A = \\frac{1}{2}, \\quad B = -\\frac{1}{2}"
                    },
                    {
                        "title": "Integrate",
                        "content": "Each term is ∫1/(x-a) dx = ln|x-a|",
                        "math": "\\int \\frac{1/2}{x-1} - \\frac{1/2}{x+1} dx = \\frac{1}{2}\\ln|x-1| - \\frac{1}{2}\\ln|x+1| + C"
                    },
                    {
                        "title": "Simplify (optional)",
                        "content": "Use log properties to combine",
                        "math": "= \\frac{1}{2}\\ln\\left|\\frac{x-1}{x+1}\\right| + C"
                    }
                ],
                "answer": "½ ln|(x-1)/(x+1)| + C",
                "key_takeaway": "For distinct linear factors, use clever substitution (x = root of each factor) to quickly find constants."
            },
            {
                "problem": "∫ (3x+5)/(x²+2x-3) dx",
                "difficulty": "Intermediate",
                "setup": "Factor: x²+2x-3 = (x+3)(x-1). Set up A/(x+3) + B/(x-1).",
                "steps": [
                    {
                        "title": "Factor denominator",
                        "content": "Find two numbers that multiply to -3 and add to 2: 3 and -1",
                        "math": "x^2 + 2x - 3 = (x+3)(x-1)"
                    },
                    {
                        "title": "Set up decomposition",
                        "content": "Two distinct linear factors",
                        "math": "\\frac{3x+5}{(x+3)(x-1)} = \\frac{A}{x+3} + \\frac{B}{x-1}"
                    },
                    {
                        "title": "Clear denominators",
                        "content": "Multiply through by (x+3)(x-1)",
                        "math": "3x + 5 = A(x-1) + B(x+3)"
                    },
                    {
                        "title": "Find A: plug in x = -3",
                        "content": "3(-3) + 5 = A(-4) + B(0)",
                        "math": "-4 = -4A \\Rightarrow A = 1"
                    },
                    {
                        "title": "Find B: plug in x = 1",
                        "content": "3(1) + 5 = A(0) + B(4)",
                        "math": "8 = 4B \\Rightarrow B = 2"
                    },
                    {
                        "title": "Integrate",
                        "content": "∫1/(x+3) dx + ∫2/(x-1) dx",
                        "math": "= \\ln|x+3| + 2\\ln|x-1| + C"
                    }
                ],
                "answer": "ln|x+3| + 2ln|x-1| + C",
                "key_takeaway": "When the numerator has x terms, the decomposition and integration still follow the same pattern."
            }
        ],
        
        "common_mistakes": [
            {
                "mistake": "Forgetting to factor completely",
                "example": "Using x²-4 instead of (x-2)(x+2)",
                "why_wrong": "You can't set up partial fractions without complete factorization",
                "fix": "Always factor the denominator fully before starting"
            },
            {
                "mistake": "Wrong form for repeated factors",
                "example": "Writing A/(x-1)² instead of A/(x-1) + B/(x-1)²",
                "why_wrong": "Repeated factors need multiple terms with increasing powers",
                "fix": "For (x-a)ⁿ, include terms for (x-a)¹, (x-a)², ..., (x-a)ⁿ"
            },
            {
                "mistake": "Wrong form for quadratic factors",
                "example": "Writing A/(x²+1) instead of (Ax+B)/(x²+1)",
                "why_wrong": "Irreducible quadratics need a linear numerator",
                "fix": "Always use (Ax + B) in the numerator for quadratic factors"
            }
        ],
        
        "recognition_patterns": [
            "Rational function where denominator factors into linear terms",
            "Fractions with (x-a)(x-b) in denominator",
            "Integrals that would be easy if the fraction were simpler",
            "Any polynomial/polynomial where degree(top) < degree(bottom)"
        ],
        
        "quick_reference": {
            "linear": "A/(x-a) → integrates to A·ln|x-a|",
            "repeated_linear": "A/(x-a)² → integrates to -A/(x-a)",
            "quadratic": "(Ax+B)/(x²+k²) → splits into A·ln + B·arctan terms"
        }
    },
    
    "improper_integrals": {
        "title": "Improper Integrals",
        "subtitle": "Handling infinity and discontinuities",
        "estimated_time": "30-45 minutes",
        
        "why_it_matters": """
Many important quantities in physics, probability, and engineering involve 
infinite intervals or functions that blow up. Improper integrals let us 
rigorously handle these cases.

Examples: The total probability in a normal distribution (integral from -∞ to ∞),
the energy of certain physical systems, signal processing.
""",
        
        "intuition": """
**The Big Idea**: We can't directly compute ∫₁^∞ or ∫ at a point where f(x) = ∞.
But we CAN take limits!

**Type 1 (Infinite limits)**: Replace ∞ with a variable t, integrate from 1 to t, 
then take the limit as t → ∞.

**Type 2 (Discontinuity)**: If f(x) blows up at x = c, integrate up to (c - ε), 
then take the limit as ε → 0.

**Key Question**: Does the limit exist and equal a finite number?
- YES → the integral CONVERGES (has a finite value)
- NO → the integral DIVERGES (is infinite or undefined)
""",
        
        "the_method": {
            "type_1": {
                "name": "Infinite Limits of Integration",
                "formula": "∫ₐ^∞ f(x)dx = lim_{t→∞} ∫ₐᵗ f(x)dx",
                "example": "∫₁^∞ 1/x² dx = lim_{t→∞} ∫₁ᵗ 1/x² dx = lim_{t→∞} [-1/x]₁ᵗ = lim_{t→∞} (-1/t + 1) = 1"
            },
            "type_2": {
                "name": "Discontinuous Integrand",
                "formula": "∫ₐᵇ f(x)dx where f has discontinuity at c ∈ (a,b)",
                "example": "∫₀¹ 1/√x dx = lim_{ε→0⁺} ∫_ε¹ x^{-1/2} dx = lim_{ε→0⁺} [2√x]_ε¹ = 2 - 0 = 2"
            }
        },
        
        "convergence_tests": [
            {
                "name": "p-test for ∫₁^∞ 1/xᵖ dx",
                "rule": "Converges if p > 1, diverges if p ≤ 1",
                "intuition": "1/x² falls off fast enough to have finite area, but 1/x falls off too slowly"
            },
            {
                "name": "Comparison Test",
                "rule": "If 0 ≤ f(x) ≤ g(x) and ∫g converges, then ∫f converges",
                "intuition": "If f is 'smaller' than something finite, f is also finite"
            }
        ],
        
        "worked_examples": [
            {
                "problem": "∫₁^∞ 1/x² dx",
                "difficulty": "Basic",
                "steps": [
                    {"title": "Replace ∞ with limit", "content": "Can't integrate to infinity directly", "math": "= \\lim_{t \\to \\infty} \\int_1^t \\frac{1}{x^2} dx"},
                    {"title": "Integrate", "content": "∫x⁻² dx = -x⁻¹ = -1/x", "math": "= \\lim_{t \\to \\infty} \\left[-\\frac{1}{x}\\right]_1^t"},
                    {"title": "Evaluate", "content": "Plug in limits", "math": "= \\lim_{t \\to \\infty} \\left(-\\frac{1}{t} + 1\\right)"},
                    {"title": "Take limit", "content": "-1/t → 0 as t → ∞", "math": "= 0 + 1 = 1"}
                ],
                "answer": "1 (converges)",
                "key_takeaway": "p = 2 > 1, so this converges by the p-test"
            },
            {
                "problem": "∫₁^∞ 1/x dx",
                "difficulty": "Basic",
                "steps": [
                    {"title": "Replace ∞ with limit", "content": "", "math": "= \\lim_{t \\to \\infty} \\int_1^t \\frac{1}{x} dx"},
                    {"title": "Integrate", "content": "∫1/x dx = ln|x|", "math": "= \\lim_{t \\to \\infty} [\\ln|x|]_1^t"},
                    {"title": "Evaluate", "content": "", "math": "= \\lim_{t \\to \\infty} (\\ln(t) - \\ln(1)) = \\lim_{t \\to \\infty} \\ln(t)"},
                    {"title": "Take limit", "content": "ln(t) → ∞ as t → ∞", "math": "= \\infty"}
                ],
                "answer": "∞ (diverges)",
                "key_takeaway": "p = 1, so this diverges. The area under 1/x from 1 to ∞ is infinite!"
            }
        ],
        
        "common_mistakes": [
            {
                "mistake": "Forgetting to use limits",
                "example": "Writing ∫₁^∞ 1/x² dx = [-1/x]₁^∞ = -1/∞ + 1",
                "why_wrong": "-1/∞ is meaningless notation",
                "fix": "Always write as a limit: lim_{t→∞} [-1/x]₁ᵗ"
            },
            {
                "mistake": "Not checking for discontinuities in the interval",
                "example": "∫₀² 1/x dx computed as [ln|x|]₀² = ln(2) - ln(0)",
                "why_wrong": "1/x has a discontinuity at x = 0; ln(0) is undefined",
                "fix": "Split at discontinuity: lim_{ε→0⁺} ∫_ε² 1/x dx"
            }
        ],
        
        "quick_reference": {
            "p_test": "∫₁^∞ 1/xᵖ: converges if p > 1, diverges if p ≤ 1",
            "key_formula": "∫ₐ^∞ f(x)dx = lim_{t→∞} ∫ₐᵗ f(x)dx"
        }
    },
    
    "sequences_series": {
        "title": "Sequences and Series",
        "subtitle": "Understanding infinite sums and their convergence",
        "estimated_time": "60-90 minutes",
        
        "why_it_matters": """
Series are the foundation of numerical analysis, signal processing, and much of applied mathematics.
They let us represent complex functions as infinite sums of simple terms (like Taylor series).
Understanding when a series converges vs diverges is critical for knowing when these representations are valid.
""",
        
        "intuition": """
**Sequence**: An ordered list of numbers: a₁, a₂, a₃, ...
Example: 1, 1/2, 1/4, 1/8, ... (each term is half the previous)

**Series**: The sum of a sequence: Σaₙ = a₁ + a₂ + a₃ + ...
Example: 1 + 1/2 + 1/4 + 1/8 + ... = 2 (this infinite sum equals a finite number!)

**The Big Question**: When does an infinite sum equal a finite number?
Answer: When the partial sums Sₙ = a₁ + a₂ + ... + aₙ approach a limit as n → ∞.
""",
        
        "key_series": [
            {
                "name": "Geometric Series",
                "formula": "Σ arⁿ = a/(1-r) if |r| < 1",
                "example": "1 + 1/2 + 1/4 + ... = 1/(1-1/2) = 2",
                "when_converges": "|r| < 1 (ratio between -1 and 1)"
            },
            {
                "name": "p-Series",
                "formula": "Σ 1/nᵖ",
                "example": "1 + 1/4 + 1/9 + 1/16 + ... = π²/6 (when p=2)",
                "when_converges": "p > 1"
            },
            {
                "name": "Harmonic Series",
                "formula": "Σ 1/n = 1 + 1/2 + 1/3 + ...",
                "example": "DIVERGES despite terms going to 0!",
                "when_converges": "Never - this is the classic divergent series"
            }
        ],
        
        "convergence_tests": [
            {
                "name": "Divergence Test (nth term test)",
                "rule": "If lim aₙ ≠ 0, the series DIVERGES",
                "warning": "If lim aₙ = 0, the test is INCONCLUSIVE (not proof of convergence!)",
                "example": "Σ n/(n+1): lim n/(n+1) = 1 ≠ 0, so diverges"
            },
            {
                "name": "Ratio Test",
                "rule": "L = lim |aₙ₊₁/aₙ|. If L < 1: converges. If L > 1: diverges. If L = 1: inconclusive.",
                "best_for": "Series with factorials or exponentials",
                "example": "Σ n!/nⁿ: ratio test works well here"
            },
            {
                "name": "Root Test",
                "rule": "L = lim ⁿ√|aₙ|. If L < 1: converges. If L > 1: diverges. If L = 1: inconclusive.",
                "best_for": "Series where aₙ involves nth powers",
                "example": "Σ (n/(2n+1))ⁿ"
            },
            {
                "name": "Comparison Test",
                "rule": "Compare to a known series. If smaller than convergent → converges. If larger than divergent → diverges.",
                "best_for": "Series that look like p-series or geometric series",
                "example": "Σ 1/(n²+1) < Σ 1/n², which converges (p=2)"
            },
            {
                "name": "Integral Test",
                "rule": "If f(n) = aₙ is positive, continuous, decreasing, then Σaₙ and ∫f(x)dx both converge or both diverge.",
                "best_for": "When the integral is easy to compute",
                "example": "Σ 1/n² converges because ∫ 1/x² dx converges"
            },
            {
                "name": "Alternating Series Test",
                "rule": "Σ(-1)ⁿbₙ converges if: (1) bₙ > 0, (2) bₙ₊₁ ≤ bₙ (decreasing), (3) lim bₙ = 0",
                "best_for": "Series with (-1)ⁿ factor",
                "example": "Σ (-1)ⁿ/n converges (alternating harmonic series)"
            }
        ],
        
        "common_mistakes": [
            {
                "mistake": "Thinking aₙ → 0 means the series converges",
                "example": "Σ 1/n: terms go to 0 but series diverges!",
                "fix": "aₙ → 0 is NECESSARY but not SUFFICIENT. The harmonic series proves this."
            },
            {
                "mistake": "Using ratio test when it gives L = 1",
                "example": "Σ 1/n: ratio test gives L = 1 (inconclusive)",
                "fix": "When ratio test is inconclusive, try comparison or integral test"
            }
        ],
        
        "quick_reference": {
            "divergence_test": "lim aₙ ≠ 0 → diverges (but lim aₙ = 0 doesn't prove convergence!)",
            "geometric": "Σarⁿ = a/(1-r) if |r| < 1",
            "p_series": "Σ1/nᵖ: converges if p > 1"
        }
    },
    
    "taylor_series": {
        "title": "Taylor and Maclaurin Series",
        "subtitle": "Representing functions as infinite polynomials",
        "estimated_time": "60-90 minutes",
        
        "why_it_matters": """
Taylor series let us approximate ANY smooth function with polynomials.
This is the foundation of how calculators compute sin, cos, eˣ, ln, etc.
It's also essential for solving differential equations and analyzing function behavior.
""",
        
        "intuition": """
**The Big Idea**: Any smooth function can be written as an infinite polynomial!

f(x) = f(a) + f'(a)(x-a) + f''(a)(x-a)²/2! + f'''(a)(x-a)³/3! + ...

**Why it works**: At x = a, all the (x-a) terms vanish except the first.
The coefficients are chosen so the polynomial matches not just f(a), but also
f'(a), f''(a), etc. - it matches the function's value AND all its derivatives!

**Maclaurin = Taylor centered at a = 0**: f(x) = f(0) + f'(0)x + f''(0)x²/2! + ...
""",
        
        "must_know_series": [
            {
                "function": "eˣ",
                "series": "1 + x + x²/2! + x³/3! + ... = Σ xⁿ/n!",
                "radius": "∞ (converges for all x)"
            },
            {
                "function": "sin(x)",
                "series": "x - x³/3! + x⁵/5! - ... = Σ (-1)ⁿx^(2n+1)/(2n+1)!",
                "radius": "∞"
            },
            {
                "function": "cos(x)",
                "series": "1 - x²/2! + x⁴/4! - ... = Σ (-1)ⁿx^(2n)/(2n)!",
                "radius": "∞"
            },
            {
                "function": "1/(1-x)",
                "series": "1 + x + x² + x³ + ... = Σ xⁿ",
                "radius": "1 (|x| < 1)"
            },
            {
                "function": "ln(1+x)",
                "series": "x - x²/2 + x³/3 - x⁴/4 + ... = Σ (-1)^(n+1)xⁿ/n",
                "radius": "1 (|x| ≤ 1, x ≠ -1)"
            }
        ],
        
        "worked_examples": [
            {
                "problem": "Find the Maclaurin series for eˣ",
                "steps": [
                    {"title": "List derivatives of eˣ", "content": "All derivatives of eˣ are eˣ", "math": "f(x) = f'(x) = f''(x) = ... = e^x"},
                    {"title": "Evaluate at x = 0", "content": "e⁰ = 1 for all derivatives", "math": "f(0) = f'(0) = f''(0) = ... = 1"},
                    {"title": "Write the series", "content": "Substitute into Maclaurin formula", "math": "e^x = 1 + x + \\frac{x^2}{2!} + \\frac{x^3}{3!} + ... = \\sum_{n=0}^{\\infty} \\frac{x^n}{n!}"}
                ],
                "answer": "eˣ = Σ xⁿ/n!"
            }
        ],
        
        "quick_reference": {
            "taylor_formula": "f(x) = Σ f⁽ⁿ⁾(a)(x-a)ⁿ/n!",
            "maclaurin": "Same as Taylor with a = 0"
        }
    },
    
    "polar_coordinates": {
        "title": "Polar Coordinates and Polar Calculus",
        "subtitle": "A different way to describe curves",
        "estimated_time": "45-60 minutes",
        
        "why_it_matters": """
Some curves are MUCH easier to describe in polar coordinates. Circles, spirals,
roses, and cardioids have simple polar equations but complex Cartesian ones.
Many physics problems (orbital mechanics, antenna patterns) naturally use polar coords.
""",
        
        "intuition": """
**Cartesian**: (x, y) = how far right, how far up
**Polar**: (r, θ) = how far from origin, at what angle

Conversion:
- x = r·cos(θ), y = r·sin(θ)
- r = √(x² + y²), θ = arctan(y/x)

**Why polar?** The equation r = 2 is just a circle of radius 2. 
In Cartesian, that's x² + y² = 4. Polar is simpler!
""",
        
        "key_formulas": {
            "area": {
                "formula": "A = ½ ∫ r² dθ",
                "explanation": "Area enclosed by polar curve from θ₁ to θ₂"
            },
            "arc_length": {
                "formula": "L = ∫ √(r² + (dr/dθ)²) dθ",
                "explanation": "Length of polar curve"
            },
            "slope": {
                "formula": "dy/dx = (r'sinθ + rcosθ)/(r'cosθ - rsinθ)",
                "explanation": "Slope of tangent line in polar"
            }
        },
        
        "common_curves": [
            {"name": "Circle", "equation": "r = a", "description": "Circle of radius a centered at origin"},
            {"name": "Cardioid", "equation": "r = 1 + cos(θ)", "description": "Heart-shaped curve"},
            {"name": "Rose", "equation": "r = cos(nθ)", "description": "n petals if n odd, 2n petals if n even"},
            {"name": "Spiral", "equation": "r = θ", "description": "Archimedean spiral"},
            {"name": "Limaçon", "equation": "r = a + b·cos(θ)", "description": "Varies based on a/b ratio"}
        ],
        
        "quick_reference": {
            "area": "A = ½ ∫ r² dθ",
            "arc_length": "L = ∫ √(r² + (dr/dθ)²) dθ"
        }
    },
    
    "parametric_equations": {
        "title": "Parametric Equations and Calculus",
        "subtitle": "Curves defined by x(t) and y(t)",
        "estimated_time": "45-60 minutes",
        
        "why_it_matters": """
Parametric equations describe motion: x(t) and y(t) give position at time t.
They can describe curves that aren't functions (like circles where y has two values for some x).
Essential for physics (projectile motion), computer graphics, and robotics.
""",
        
        "intuition": """
**Regular function**: y = f(x) - for each x, one y
**Parametric**: x = f(t), y = g(t) - both coordinates depend on parameter t

Think of t as TIME. As t increases, the point (x(t), y(t)) traces out a curve.

Example: x = cos(t), y = sin(t) traces a circle as t goes from 0 to 2π.
""",
        
        "key_formulas": {
            "slope": {
                "formula": "dy/dx = (dy/dt)/(dx/dt)",
                "explanation": "Chain rule: dy/dx = (dy/dt) ÷ (dx/dt)"
            },
            "second_derivative": {
                "formula": "d²y/dx² = (d/dt)(dy/dx) / (dx/dt)",
                "explanation": "Take derivative of dy/dx with respect to t, divide by dx/dt"
            },
            "arc_length": {
                "formula": "L = ∫ √((dx/dt)² + (dy/dt)²) dt",
                "explanation": "Length of parametric curve from t₁ to t₂"
            },
            "surface_area": {
                "formula": "S = 2π ∫ y·√((dx/dt)² + (dy/dt)²) dt",
                "explanation": "Surface area when rotated about x-axis"
            }
        },
        
        "worked_examples": [
            {
                "problem": "Find dy/dx for x = t², y = t³",
                "steps": [
                    {"title": "Find dx/dt", "math": "dx/dt = 2t"},
                    {"title": "Find dy/dt", "math": "dy/dt = 3t^2"},
                    {"title": "Apply formula", "math": "\\frac{dy}{dx} = \\frac{dy/dt}{dx/dt} = \\frac{3t^2}{2t} = \\frac{3t}{2}"}
                ],
                "answer": "dy/dx = 3t/2"
            }
        ],
        
        "quick_reference": {
            "slope": "dy/dx = (dy/dt)/(dx/dt)",
            "arc_length": "L = ∫ √((dx/dt)² + (dy/dt)²) dt"
        }
    }
}


class TeachingEngine:
    """
    Comprehensive teaching engine that combines pre-built lessons
    with AI-generated content for personalized learning.
    """
    
    def __init__(self):
        self.lessons = COMPREHENSIVE_LESSONS
        self.progress_file = Path(__file__).parent / "data" / "learning_progress.json"
        self.progress = self._load_progress()
    
    def _load_progress(self) -> Dict:
        """Load learning progress"""
        if self.progress_file.exists():
            try:
                with open(self.progress_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            "lessons_completed": [],
            "examples_worked": [],
            "concepts_mastered": [],
            "time_spent": {}
        }
    
    def _save_progress(self):
        """Save learning progress"""
        self.progress_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.progress_file, 'w') as f:
            json.dump(self.progress, f, indent=2)
    
    def get_lesson(self, topic: str) -> Optional[Dict]:
        """Get a comprehensive lesson for a topic"""
        return self.lessons.get(topic)
    
    def get_all_topics(self) -> List[Dict]:
        """Get list of all available topics"""
        return [
            {
                "id": topic_id,
                "title": lesson["title"],
                "subtitle": lesson.get("subtitle", ""),
                "estimated_time": lesson.get("estimated_time", "Unknown"),
                "completed": topic_id in self.progress.get("lessons_completed", [])
            }
            for topic_id, lesson in self.lessons.items()
        ]
    
    def mark_lesson_viewed(self, topic: str):
        """Mark a lesson as completed"""
        if topic not in self.progress["lessons_completed"]:
            self.progress["lessons_completed"].append(topic)
            self._save_progress()
    
    def get_quick_reference(self, topic: str) -> Optional[Dict]:
        """Get quick reference card for a topic"""
        lesson = self.lessons.get(topic)
        if lesson:
            return lesson.get("quick_reference", {})
        return None
    
    def get_all_formulas(self) -> List[Dict]:
        """Get all formulas across all topics for formula sheet"""
        formulas = []
        for topic_id, lesson in self.lessons.items():
            qr = lesson.get("quick_reference", {})
            for name, formula in qr.items():
                formulas.append({
                    "topic": lesson["title"],
                    "topic_id": topic_id,
                    "name": name.replace("_", " ").title(),
                    "formula": formula
                })
        return formulas


# Create singleton instance
teaching_engine = TeachingEngine()
