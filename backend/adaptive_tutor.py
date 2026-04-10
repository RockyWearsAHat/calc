"""
Adaptive Calculus Tutor - Actually teaches you, doesn't just quiz you
- Multi-level hint system
- Dynamic difficulty scaling
- Step-by-step walkthroughs
- Tracks mastery and weak spots
"""
import json
import random
import re
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

# ==================== COMPREHENSIVE PROBLEM BANK ====================
# Organized by topic, with multiple difficulty levels and full solutions

PROBLEM_BANK = {
    # ==================== INTEGRATION BY PARTS ====================
    "integration_by_parts": {
        "name": "Integration by Parts",
        "prerequisite": "integration_basics",
        "problems": [
            # LEVEL 1 - Basic
            {
                "id": "ibp_1_1",
                "level": 1,
                "question": "Evaluate: ∫ x·eˣ dx",
                "answer": "eˣ(x - 1) + C",
                "hints": [
                    "This is a product of x and eˣ - perfect for integration by parts",
                    "Use the LIATE rule: Algebraic before Exponential, so let u = x",
                    "If u = x, then dv = eˣ dx. What is du? What is v?",
                ],
                "walkthrough": [
                    {
                        "step": 1,
                        "title": "Identify u and dv using LIATE",
                        "explanation": "LIATE tells us to choose u from: Logs, Inverse trig, Algebraic, Trig, Exponential (in that order). Here x is Algebraic and eˣ is Exponential, so u = x.",
                        "math": "u = x, \\quad dv = e^x \\, dx"
                    },
                    {
                        "step": 2,
                        "title": "Find du and v",
                        "explanation": "Differentiate u to get du, integrate dv to get v.",
                        "math": "du = dx, \\quad v = \\int e^x \\, dx = e^x"
                    },
                    {
                        "step": 3,
                        "title": "Apply the IBP formula",
                        "explanation": "The formula is ∫u dv = uv - ∫v du",
                        "math": "\\int x \\cdot e^x \\, dx = x \\cdot e^x - \\int e^x \\, dx"
                    },
                    {
                        "step": 4,
                        "title": "Evaluate the remaining integral",
                        "explanation": "∫eˣ dx is just eˣ",
                        "math": "= x \\cdot e^x - e^x + C"
                    },
                    {
                        "step": 5,
                        "title": "Factor and simplify",
                        "explanation": "Factor out eˣ for a cleaner answer",
                        "math": "= e^x(x - 1) + C"
                    }
                ],
                "key_concept": "Integration by parts formula: ∫u dv = uv - ∫v du"
            },
            {
                "id": "ibp_1_2",
                "level": 1,
                "question": "Evaluate: ∫ x·cos(x) dx",
                "answer": "x·sin(x) + cos(x) + C",
                "hints": [
                    "Product of algebraic (x) and trig (cos x) - use integration by parts",
                    "LIATE: Algebraic before Trig, so u = x",
                    "What is ∫cos(x) dx?",
                ],
                "walkthrough": [
                    {
                        "step": 1,
                        "title": "Choose u and dv",
                        "explanation": "By LIATE, algebraic (x) comes before trig (cos x)",
                        "math": "u = x, \\quad dv = \\cos(x) \\, dx"
                    },
                    {
                        "step": 2,
                        "title": "Find du and v",
                        "explanation": "Differentiate u, integrate dv",
                        "math": "du = dx, \\quad v = \\sin(x)"
                    },
                    {
                        "step": 3,
                        "title": "Apply IBP formula",
                        "explanation": "∫u dv = uv - ∫v du",
                        "math": "\\int x \\cos(x) \\, dx = x \\sin(x) - \\int \\sin(x) \\, dx"
                    },
                    {
                        "step": 4,
                        "title": "Evaluate ∫sin(x) dx",
                        "explanation": "The integral of sin(x) is -cos(x)",
                        "math": "= x \\sin(x) - (-\\cos(x)) + C = x \\sin(x) + \\cos(x) + C"
                    }
                ],
                "key_concept": "LIATE rule helps choose u: Logs, Inverse trig, Algebraic, Trig, Exponential"
            },
            {
                "id": "ibp_1_3",
                "level": 1,
                "question": "Evaluate: ∫ ln(x) dx",
                "answer": "x·ln(x) - x + C",
                "hints": [
                    "There's only one function here, but you can write it as ln(x)·1",
                    "Let u = ln(x) and dv = dx (just 1·dx)",
                    "What is the derivative of ln(x)?",
                ],
                "walkthrough": [
                    {
                        "step": 1,
                        "title": "Rewrite as a product",
                        "explanation": "Even though there's only ln(x), we can think of it as ln(x)·1",
                        "math": "\\int \\ln(x) \\, dx = \\int \\ln(x) \\cdot 1 \\, dx"
                    },
                    {
                        "step": 2,
                        "title": "Choose u and dv",
                        "explanation": "By LIATE, Logs come first, so u = ln(x), dv = dx",
                        "math": "u = \\ln(x), \\quad dv = dx"
                    },
                    {
                        "step": 3,
                        "title": "Find du and v",
                        "explanation": "d/dx[ln(x)] = 1/x, and ∫dx = x",
                        "math": "du = \\frac{1}{x} \\, dx, \\quad v = x"
                    },
                    {
                        "step": 4,
                        "title": "Apply IBP formula",
                        "explanation": "∫u dv = uv - ∫v du",
                        "math": "= x \\ln(x) - \\int x \\cdot \\frac{1}{x} \\, dx = x \\ln(x) - \\int 1 \\, dx"
                    },
                    {
                        "step": 5,
                        "title": "Finish the integral",
                        "explanation": "∫1 dx = x",
                        "math": "= x \\ln(x) - x + C"
                    }
                ],
                "key_concept": "∫ln(x) dx requires IBP with u = ln(x), dv = dx"
            },
            # LEVEL 2 - Intermediate
            {
                "id": "ibp_2_1",
                "level": 2,
                "question": "Evaluate: ∫ x²·eˣ dx",
                "answer": "eˣ(x² - 2x + 2) + C",
                "hints": [
                    "This needs integration by parts TWICE (or use tabular method)",
                    "Start with u = x², which will become 2x after first IBP",
                    "After first IBP you'll have ∫2x·eˣ dx - do IBP again!",
                    "Or use tabular method: derivatives of x² down, integrals of eˣ across"
                ],
                "walkthrough": [
                    {
                        "step": 1,
                        "title": "Set up tabular method",
                        "explanation": "For polynomial × exponential, tabular method is fastest. List derivatives of x² and integrals of eˣ.",
                        "math": "\\begin{array}{c|c|c} \\text{Sign} & u \\text{ (diff)} & dv \\text{ (int)} \\\\ \\hline + & x^2 & e^x \\\\ - & 2x & e^x \\\\ + & 2 & e^x \\\\ - & 0 & e^x \\end{array}"
                    },
                    {
                        "step": 2,
                        "title": "Multiply diagonally with alternating signs",
                        "explanation": "Connect each u term to the v term one row down, alternating + and -",
                        "math": "(+)(x^2)(e^x) + (-)(2x)(e^x) + (+)(2)(e^x)"
                    },
                    {
                        "step": 3,
                        "title": "Write the result",
                        "explanation": "Combine the terms",
                        "math": "= x^2 e^x - 2x e^x + 2e^x + C"
                    },
                    {
                        "step": 4,
                        "title": "Factor out eˣ",
                        "explanation": "Factor for a cleaner final answer",
                        "math": "= e^x(x^2 - 2x + 2) + C"
                    }
                ],
                "key_concept": "Tabular method is efficient for polynomial × (eˣ or sin/cos)"
            },
            {
                "id": "ibp_2_2",
                "level": 2,
                "question": "Evaluate: ∫ eˣ·sin(x) dx",
                "answer": "(eˣ/2)(sin(x) - cos(x)) + C",
                "hints": [
                    "This is a CYCLIC integral - IBP brings you back to the original!",
                    "Do IBP twice. After the second time, you'll see ∫eˣsin(x)dx on both sides",
                    "When you get I = ... - I, solve for I algebraically",
                    "Let I = ∫eˣsin(x)dx and solve 2I = ..."
                ],
                "walkthrough": [
                    {
                        "step": 1,
                        "title": "First IBP",
                        "explanation": "Let u = eˣ, dv = sin(x)dx",
                        "math": "u = e^x, \\; dv = \\sin(x)\\,dx \\implies du = e^x\\,dx, \\; v = -\\cos(x)"
                    },
                    {
                        "step": 2,
                        "title": "Apply formula",
                        "explanation": "∫u dv = uv - ∫v du",
                        "math": "I = -e^x\\cos(x) - \\int (-\\cos(x))(e^x)\\,dx = -e^x\\cos(x) + \\int e^x\\cos(x)\\,dx"
                    },
                    {
                        "step": 3,
                        "title": "Second IBP on ∫eˣcos(x)dx",
                        "explanation": "u = eˣ, dv = cos(x)dx gives v = sin(x)",
                        "math": "\\int e^x\\cos(x)\\,dx = e^x\\sin(x) - \\int e^x\\sin(x)\\,dx = e^x\\sin(x) - I"
                    },
                    {
                        "step": 4,
                        "title": "Substitute back",
                        "explanation": "Replace the second integral in our equation",
                        "math": "I = -e^x\\cos(x) + e^x\\sin(x) - I"
                    },
                    {
                        "step": 5,
                        "title": "Solve for I",
                        "explanation": "Add I to both sides, then divide by 2",
                        "math": "2I = e^x(\\sin(x) - \\cos(x)) \\implies I = \\frac{e^x}{2}(\\sin(x) - \\cos(x)) + C"
                    }
                ],
                "key_concept": "Cyclic IBP: when ∫ reappears, solve algebraically!"
            },
            # LEVEL 3 - Advanced
            {
                "id": "ibp_3_1",
                "level": 3,
                "question": "Evaluate: ∫ x·arctan(x) dx",
                "answer": "(x²/2)arctan(x) - x/2 + (1/2)arctan(x) + C  or  ((x²+1)/2)arctan(x) - x/2 + C",
                "hints": [
                    "LIATE: Inverse trig (arctan) before Algebraic (x), so u = arctan(x)",
                    "What is d/dx[arctan(x)]?",
                    "After IBP, you'll need to simplify ∫x²/(1+x²) dx",
                    "For ∫x²/(1+x²) dx, try adding and subtracting 1 in numerator"
                ],
                "walkthrough": [
                    {
                        "step": 1,
                        "title": "Choose u and dv",
                        "explanation": "By LIATE, inverse trig comes before algebraic",
                        "math": "u = \\arctan(x), \\quad dv = x\\,dx"
                    },
                    {
                        "step": 2,
                        "title": "Find du and v",
                        "explanation": "d/dx[arctan(x)] = 1/(1+x²), and ∫x dx = x²/2",
                        "math": "du = \\frac{1}{1+x^2}\\,dx, \\quad v = \\frac{x^2}{2}"
                    },
                    {
                        "step": 3,
                        "title": "Apply IBP",
                        "explanation": "∫u dv = uv - ∫v du",
                        "math": "= \\frac{x^2}{2}\\arctan(x) - \\int \\frac{x^2}{2} \\cdot \\frac{1}{1+x^2}\\,dx"
                    },
                    {
                        "step": 4,
                        "title": "Simplify the remaining integral",
                        "explanation": "Write x² = (1+x²) - 1 to split the fraction",
                        "math": "\\frac{x^2}{1+x^2} = \\frac{(1+x^2)-1}{1+x^2} = 1 - \\frac{1}{1+x^2}"
                    },
                    {
                        "step": 5,
                        "title": "Integrate",
                        "explanation": "Now integrate 1 - 1/(1+x²)",
                        "math": "\\int \\left(1 - \\frac{1}{1+x^2}\\right)dx = x - \\arctan(x)"
                    },
                    {
                        "step": 6,
                        "title": "Combine everything",
                        "explanation": "Put it all together",
                        "math": "= \\frac{x^2}{2}\\arctan(x) - \\frac{1}{2}(x - \\arctan(x)) + C = \\frac{x^2+1}{2}\\arctan(x) - \\frac{x}{2} + C"
                    }
                ],
                "key_concept": "For ∫x²/(1+x²), use the trick: x² = (1+x²) - 1"
            }
        ]
    },
    
    # ==================== PARTIAL FRACTIONS ====================
    "partial_fractions": {
        "name": "Partial Fractions",
        "prerequisite": "integration_basics",
        "problems": [
            {
                "id": "pf_1_1",
                "level": 1,
                "question": "Evaluate: ∫ 1/((x-1)(x+1)) dx",
                "answer": "(1/2)ln|x-1| - (1/2)ln|x+1| + C  or  (1/2)ln|(x-1)/(x+1)| + C",
                "hints": [
                    "This is a rational function with distinct linear factors - use partial fractions",
                    "Set up: 1/((x-1)(x+1)) = A/(x-1) + B/(x+1)",
                    "To find A, multiply both sides by (x-1) and set x = 1",
                    "To find B, multiply both sides by (x+1) and set x = -1"
                ],
                "walkthrough": [
                    {
                        "step": 1,
                        "title": "Set up partial fractions",
                        "explanation": "For distinct linear factors, each gets a constant numerator",
                        "math": "\\frac{1}{(x-1)(x+1)} = \\frac{A}{x-1} + \\frac{B}{x+1}"
                    },
                    {
                        "step": 2,
                        "title": "Find A using cover-up",
                        "explanation": "Cover (x-1) in the original, substitute x = 1",
                        "math": "A = \\frac{1}{(1)+1} = \\frac{1}{2}"
                    },
                    {
                        "step": 3,
                        "title": "Find B using cover-up",
                        "explanation": "Cover (x+1) in the original, substitute x = -1",
                        "math": "B = \\frac{1}{(-1)-1} = -\\frac{1}{2}"
                    },
                    {
                        "step": 4,
                        "title": "Rewrite and integrate",
                        "explanation": "Now integrate each simple fraction",
                        "math": "\\int \\left(\\frac{1/2}{x-1} - \\frac{1/2}{x+1}\\right)dx = \\frac{1}{2}\\ln|x-1| - \\frac{1}{2}\\ln|x+1| + C"
                    }
                ],
                "key_concept": "Cover-up method: to find A for factor (x-a), cover it and plug in x = a"
            },
            {
                "id": "pf_1_2",
                "level": 1,
                "question": "Evaluate: ∫ (3x+5)/(x²-x-2) dx",
                "answer": "4·ln|x-2| - ln|x+1| + C",
                "hints": [
                    "First factor the denominator: x² - x - 2 = ?",
                    "x² - x - 2 = (x-2)(x+1)",
                    "Set up: (3x+5)/((x-2)(x+1)) = A/(x-2) + B/(x+1)",
                    "Use cover-up or clearing denominators to find A and B"
                ],
                "walkthrough": [
                    {
                        "step": 1,
                        "title": "Factor the denominator",
                        "explanation": "Find two numbers that multiply to -2 and add to -1",
                        "math": "x^2 - x - 2 = (x-2)(x+1)"
                    },
                    {
                        "step": 2,
                        "title": "Set up partial fractions",
                        "explanation": "Two distinct linear factors",
                        "math": "\\frac{3x+5}{(x-2)(x+1)} = \\frac{A}{x-2} + \\frac{B}{x+1}"
                    },
                    {
                        "step": 3,
                        "title": "Find A (cover-up, x = 2)",
                        "explanation": "Cover (x-2), plug in x = 2",
                        "math": "A = \\frac{3(2)+5}{(2)+1} = \\frac{11}{3} \\approx 3.67... \\text{ Let me recalculate: } A = \\frac{11}{3}"
                    },
                    {
                        "step": 4,
                        "title": "Find B (cover-up, x = -1)",
                        "explanation": "Cover (x+1), plug in x = -1",
                        "math": "B = \\frac{3(-1)+5}{(-1)-2} = \\frac{2}{-3} = -\\frac{2}{3}"
                    },
                    {
                        "step": 5,
                        "title": "Integrate",
                        "explanation": "Integrate each term",
                        "math": "\\int \\left(\\frac{11/3}{x-2} - \\frac{2/3}{x+1}\\right)dx = \\frac{11}{3}\\ln|x-2| - \\frac{2}{3}\\ln|x+1| + C"
                    }
                ],
                "key_concept": "Always factor the denominator first before setting up partial fractions"
            },
            {
                "id": "pf_2_1",
                "level": 2,
                "question": "Evaluate: ∫ 1/(x²(x+1)) dx",
                "answer": "-1/x + ln|x| - ln|x+1| + C",
                "hints": [
                    "The factor x² is REPEATED - this changes the setup",
                    "For x², you need: A/x + B/x² (both powers!)",
                    "Setup: 1/(x²(x+1)) = A/x + B/x² + C/(x+1)",
                    "Clear denominators and match coefficients, or use strategic substitution"
                ],
                "walkthrough": [
                    {
                        "step": 1,
                        "title": "Set up for repeated factor",
                        "explanation": "x² requires TWO terms: one for x, one for x²",
                        "math": "\\frac{1}{x^2(x+1)} = \\frac{A}{x} + \\frac{B}{x^2} + \\frac{C}{x+1}"
                    },
                    {
                        "step": 2,
                        "title": "Clear denominators",
                        "explanation": "Multiply both sides by x²(x+1)",
                        "math": "1 = Ax(x+1) + B(x+1) + Cx^2"
                    },
                    {
                        "step": 3,
                        "title": "Find B (let x = 0)",
                        "explanation": "When x = 0, only the B term survives",
                        "math": "1 = B(0+1) \\implies B = 1"
                    },
                    {
                        "step": 4,
                        "title": "Find C (let x = -1)",
                        "explanation": "When x = -1, only the C term survives",
                        "math": "1 = C(-1)^2 = C \\implies C = 1"
                    },
                    {
                        "step": 5,
                        "title": "Find A (compare coefficients of x²)",
                        "explanation": "Expand and compare x² coefficients: A + C = 0",
                        "math": "A + C = 0 \\implies A = -1"
                    },
                    {
                        "step": 6,
                        "title": "Integrate",
                        "explanation": "Integrate each term separately",
                        "math": "\\int \\left(-\\frac{1}{x} + \\frac{1}{x^2} + \\frac{1}{x+1}\\right)dx = -\\ln|x| - \\frac{1}{x} + \\ln|x+1| + C"
                    }
                ],
                "key_concept": "Repeated factor (x-a)ⁿ needs n terms: A₁/(x-a) + A₂/(x-a)² + ... + Aₙ/(x-a)ⁿ"
            }
        ]
    },
    
    # ==================== IMPROPER INTEGRALS ====================
    "improper_integrals": {
        "name": "Improper Integrals",
        "prerequisite": "integration_basics",
        "problems": [
            {
                "id": "imp_1_1",
                "level": 1,
                "question": "Determine if ∫₁^∞ 1/x² dx converges or diverges. If it converges, find the value.",
                "answer": "Converges to 1",
                "hints": [
                    "This is a Type I improper integral (infinite upper limit)",
                    "Replace ∞ with a variable t, evaluate the definite integral, then take the limit",
                    "What is ∫1/x² dx = ∫x⁻² dx?",
                    "This is the p-integral with p = 2. What's the rule for p-integrals?"
                ],
                "walkthrough": [
                    {
                        "step": 1,
                        "title": "Set up the limit definition",
                        "explanation": "Replace ∞ with t and take limit as t → ∞",
                        "math": "\\int_1^{\\infty} \\frac{1}{x^2}\\,dx = \\lim_{t \\to \\infty} \\int_1^t \\frac{1}{x^2}\\,dx"
                    },
                    {
                        "step": 2,
                        "title": "Find the antiderivative",
                        "explanation": "∫x⁻² dx = x⁻¹/(-1) = -1/x",
                        "math": "\\int \\frac{1}{x^2}\\,dx = -\\frac{1}{x}"
                    },
                    {
                        "step": 3,
                        "title": "Evaluate the definite integral",
                        "explanation": "Apply the bounds",
                        "math": "\\left[-\\frac{1}{x}\\right]_1^t = -\\frac{1}{t} - \\left(-\\frac{1}{1}\\right) = -\\frac{1}{t} + 1"
                    },
                    {
                        "step": 4,
                        "title": "Take the limit",
                        "explanation": "As t → ∞, 1/t → 0",
                        "math": "\\lim_{t \\to \\infty} \\left(1 - \\frac{1}{t}\\right) = 1 - 0 = 1"
                    },
                    {
                        "step": 5,
                        "title": "Conclusion",
                        "explanation": "The limit exists and is finite, so the integral converges",
                        "math": "\\text{Converges to } 1"
                    }
                ],
                "key_concept": "p-integral rule: ∫₁^∞ 1/xᵖ dx converges iff p > 1"
            },
            {
                "id": "imp_1_2",
                "level": 1,
                "question": "Determine if ∫₁^∞ 1/x dx converges or diverges.",
                "answer": "Diverges",
                "hints": [
                    "This is the p-integral with p = 1",
                    "What is ∫1/x dx?",
                    "What is lim(t→∞) ln(t)?",
                ],
                "walkthrough": [
                    {
                        "step": 1,
                        "title": "Set up the limit",
                        "explanation": "Replace ∞ with t",
                        "math": "\\int_1^{\\infty} \\frac{1}{x}\\,dx = \\lim_{t \\to \\infty} \\int_1^t \\frac{1}{x}\\,dx"
                    },
                    {
                        "step": 2,
                        "title": "Find antiderivative and evaluate",
                        "explanation": "∫1/x dx = ln|x|",
                        "math": "= \\lim_{t \\to \\infty} [\\ln|x|]_1^t = \\lim_{t \\to \\infty} (\\ln t - \\ln 1) = \\lim_{t \\to \\infty} \\ln t"
                    },
                    {
                        "step": 3,
                        "title": "Evaluate the limit",
                        "explanation": "ln(t) → ∞ as t → ∞",
                        "math": "\\lim_{t \\to \\infty} \\ln t = \\infty"
                    },
                    {
                        "step": 4,
                        "title": "Conclusion",
                        "explanation": "The limit is infinite, so the integral diverges",
                        "math": "\\text{Diverges}"
                    }
                ],
                "key_concept": "The harmonic integral ∫1/x diverges! (p = 1 is the boundary case)"
            },
            {
                "id": "imp_2_1",
                "level": 2,
                "question": "Determine if ∫₀^∞ xe⁻ˣ dx converges. If so, find its value.",
                "answer": "Converges to 1",
                "hints": [
                    "This needs integration by parts first, then take the limit",
                    "For ∫xe⁻ˣ dx, let u = x, dv = e⁻ˣ dx",
                    "You'll need L'Hôpital's rule to evaluate lim(t→∞) t/eᵗ"
                ],
                "walkthrough": [
                    {
                        "step": 1,
                        "title": "Set up as a limit",
                        "explanation": "Replace ∞ with t",
                        "math": "\\int_0^{\\infty} xe^{-x}\\,dx = \\lim_{t \\to \\infty} \\int_0^t xe^{-x}\\,dx"
                    },
                    {
                        "step": 2,
                        "title": "Integration by parts",
                        "explanation": "u = x, dv = e⁻ˣdx, so du = dx, v = -e⁻ˣ",
                        "math": "\\int xe^{-x}dx = -xe^{-x} - \\int(-e^{-x})dx = -xe^{-x} - e^{-x} = -e^{-x}(x+1)"
                    },
                    {
                        "step": 3,
                        "title": "Evaluate from 0 to t",
                        "explanation": "Apply the bounds",
                        "math": "[-e^{-x}(x+1)]_0^t = -e^{-t}(t+1) - (-e^0(0+1)) = -e^{-t}(t+1) + 1"
                    },
                    {
                        "step": 4,
                        "title": "Take the limit",
                        "explanation": "As t→∞, (t+1)/eᵗ → 0 by L'Hôpital (exponential beats polynomial)",
                        "math": "\\lim_{t \\to \\infty}\\left(1 - \\frac{t+1}{e^t}\\right) = 1 - 0 = 1"
                    }
                ],
                "key_concept": "Exponential decay (e⁻ˣ) beats polynomial growth (xⁿ) as x → ∞"
            }
        ]
    },
    
    # ==================== SERIES ====================
    "series_strategy": {
        "name": "Series Convergence Tests",
        "prerequisite": "limits",
        "problems": [
            {
                "id": "ser_1_1",
                "level": 1,
                "question": "Determine if Σ(n=1 to ∞) n/(n+1) converges or diverges.",
                "answer": "Diverges by Divergence Test",
                "hints": [
                    "Always try the Divergence Test FIRST",
                    "What is lim(n→∞) n/(n+1)?",
                    "If the limit is NOT zero, what does that tell you?"
                ],
                "walkthrough": [
                    {
                        "step": 1,
                        "title": "Apply Divergence Test",
                        "explanation": "Check if lim(n→∞) aₙ = 0",
                        "math": "\\lim_{n \\to \\infty} \\frac{n}{n+1} = \\lim_{n \\to \\infty} \\frac{1}{1+1/n} = 1"
                    },
                    {
                        "step": 2,
                        "title": "Conclusion",
                        "explanation": "Since the limit is 1 ≠ 0, the series diverges",
                        "math": "\\text{Diverges by Divergence Test}"
                    }
                ],
                "key_concept": "Divergence Test: if lim aₙ ≠ 0, the series DIVERGES"
            },
            {
                "id": "ser_1_2",
                "level": 1,
                "question": "Determine if Σ(n=1 to ∞) 1/n² converges or diverges.",
                "answer": "Converges (p-series with p = 2 > 1)",
                "hints": [
                    "This is a p-series: Σ 1/nᵖ",
                    "What is p in this case?",
                    "p-series converges if p > 1, diverges if p ≤ 1"
                ],
                "walkthrough": [
                    {
                        "step": 1,
                        "title": "Identify as p-series",
                        "explanation": "This has the form Σ 1/nᵖ with p = 2",
                        "math": "\\sum_{n=1}^{\\infty} \\frac{1}{n^2} \\text{ is a p-series with } p = 2"
                    },
                    {
                        "step": 2,
                        "title": "Apply p-series test",
                        "explanation": "p-series converges iff p > 1",
                        "math": "p = 2 > 1 \\implies \\text{Converges}"
                    }
                ],
                "key_concept": "p-series test: Σ 1/nᵖ converges iff p > 1"
            },
            {
                "id": "ser_2_1",
                "level": 2,
                "question": "Determine if Σ(n=1 to ∞) n!/3ⁿ converges or diverges.",
                "answer": "Diverges by Ratio Test",
                "hints": [
                    "Factorials and exponentials → use Ratio Test",
                    "Compute lim |aₙ₊₁/aₙ|",
                    "aₙ₊₁/aₙ = [(n+1)!/3ⁿ⁺¹] / [n!/3ⁿ] = (n+1)/3"
                ],
                "walkthrough": [
                    {
                        "step": 1,
                        "title": "Set up Ratio Test",
                        "explanation": "Compute the ratio of consecutive terms",
                        "math": "\\frac{a_{n+1}}{a_n} = \\frac{(n+1)!/3^{n+1}}{n!/3^n} = \\frac{(n+1)!}{n!} \\cdot \\frac{3^n}{3^{n+1}}"
                    },
                    {
                        "step": 2,
                        "title": "Simplify",
                        "explanation": "(n+1)!/n! = n+1 and 3ⁿ/3ⁿ⁺¹ = 1/3",
                        "math": "= (n+1) \\cdot \\frac{1}{3} = \\frac{n+1}{3}"
                    },
                    {
                        "step": 3,
                        "title": "Take the limit",
                        "explanation": "Find L = lim |aₙ₊₁/aₙ|",
                        "math": "L = \\lim_{n \\to \\infty} \\frac{n+1}{3} = \\infty"
                    },
                    {
                        "step": 4,
                        "title": "Conclusion",
                        "explanation": "L > 1 means divergence",
                        "math": "L = \\infty > 1 \\implies \\text{Diverges}"
                    }
                ],
                "key_concept": "Ratio Test: L < 1 converges, L > 1 diverges, L = 1 inconclusive"
            },
            {
                "id": "ser_2_2",
                "level": 2,
                "question": "Determine if Σ(n=1 to ∞) (-1)ⁿ/n converges or diverges.",
                "answer": "Converges (conditionally) by Alternating Series Test",
                "hints": [
                    "This has alternating signs: (-1)ⁿ",
                    "Use the Alternating Series Test",
                    "Check: (1) is 1/n decreasing? (2) does 1/n → 0?"
                ],
                "walkthrough": [
                    {
                        "step": 1,
                        "title": "Identify alternating series",
                        "explanation": "This is Σ(-1)ⁿbₙ with bₙ = 1/n",
                        "math": "\\sum_{n=1}^{\\infty} \\frac{(-1)^n}{n} = \\sum (-1)^n b_n \\text{ where } b_n = \\frac{1}{n}"
                    },
                    {
                        "step": 2,
                        "title": "Check condition 1: bₙ decreasing",
                        "explanation": "Is 1/n > 1/(n+1)?",
                        "math": "b_n = \\frac{1}{n} > \\frac{1}{n+1} = b_{n+1} \\; ✓"
                    },
                    {
                        "step": 3,
                        "title": "Check condition 2: bₙ → 0",
                        "explanation": "Does 1/n → 0 as n → ∞?",
                        "math": "\\lim_{n \\to \\infty} \\frac{1}{n} = 0 \\; ✓"
                    },
                    {
                        "step": 4,
                        "title": "Conclusion",
                        "explanation": "Both conditions met, so it converges",
                        "math": "\\text{Converges by Alternating Series Test}"
                    }
                ],
                "key_concept": "Alternating Series Test: Σ(-1)ⁿbₙ converges if bₙ↓ and bₙ→0"
            }
        ]
    },
    
    # ==================== TAYLOR SERIES ====================
    "taylor_maclaurin": {
        "name": "Taylor and Maclaurin Series",
        "prerequisite": "series_strategy",
        "problems": [
            {
                "id": "tay_1_1",
                "level": 1,
                "question": "Write the first 4 nonzero terms of the Maclaurin series for e^(2x).",
                "answer": "1 + 2x + 2x² + (4/3)x³",
                "hints": [
                    "Start with the Maclaurin series for eˣ = 1 + x + x²/2! + x³/3! + ...",
                    "Replace x with 2x everywhere",
                    "(2x)² = 4x², (2x)³ = 8x³"
                ],
                "walkthrough": [
                    {
                        "step": 1,
                        "title": "Recall eˣ series",
                        "explanation": "The Maclaurin series for eˣ is memorized",
                        "math": "e^x = 1 + x + \\frac{x^2}{2!} + \\frac{x^3}{3!} + ..."
                    },
                    {
                        "step": 2,
                        "title": "Substitute 2x for x",
                        "explanation": "Replace every x with 2x",
                        "math": "e^{2x} = 1 + (2x) + \\frac{(2x)^2}{2!} + \\frac{(2x)^3}{3!} + ..."
                    },
                    {
                        "step": 3,
                        "title": "Simplify each term",
                        "explanation": "Compute the powers and simplify",
                        "math": "= 1 + 2x + \\frac{4x^2}{2} + \\frac{8x^3}{6} + ... = 1 + 2x + 2x^2 + \\frac{4}{3}x^3 + ..."
                    }
                ],
                "key_concept": "To get series for e^(f(x)), substitute f(x) for x in the eˣ series"
            },
            {
                "id": "tay_1_2",
                "level": 1,
                "question": "Find the Maclaurin series for 1/(1+x²). Write the first 4 nonzero terms.",
                "answer": "1 - x² + x⁴ - x⁶",
                "hints": [
                    "Start with the geometric series: 1/(1-u) = 1 + u + u² + u³ + ...",
                    "What should u be to get 1/(1+x²)?",
                    "1/(1+x²) = 1/(1-(-x²)), so u = -x²"
                ],
                "walkthrough": [
                    {
                        "step": 1,
                        "title": "Identify the form",
                        "explanation": "Rewrite to match 1/(1-u)",
                        "math": "\\frac{1}{1+x^2} = \\frac{1}{1-(-x^2)}"
                    },
                    {
                        "step": 2,
                        "title": "Apply geometric series",
                        "explanation": "1/(1-u) = Σuⁿ with u = -x²",
                        "math": "= \\sum_{n=0}^{\\infty} (-x^2)^n = \\sum_{n=0}^{\\infty} (-1)^n x^{2n}"
                    },
                    {
                        "step": 3,
                        "title": "Write out terms",
                        "explanation": "First 4 nonzero terms",
                        "math": "= 1 - x^2 + x^4 - x^6 + ..."
                    }
                ],
                "key_concept": "Modify 1/(1-x) = Σxⁿ by substitution to get many other series"
            },
            {
                "id": "tay_2_1",
                "level": 2,
                "question": "Use Taylor series to evaluate: lim(x→0) (sin(x) - x + x³/6) / x⁵",
                "answer": "1/120",
                "hints": [
                    "Write out the Maclaurin series for sin(x)",
                    "sin(x) = x - x³/3! + x⁵/5! - x⁷/7! + ...",
                    "Substitute and simplify: sin(x) - x + x³/6 = ?",
                    "The x, x³ terms should cancel!"
                ],
                "walkthrough": [
                    {
                        "step": 1,
                        "title": "Write sin(x) series",
                        "explanation": "Recall the Maclaurin series for sin",
                        "math": "\\sin(x) = x - \\frac{x^3}{6} + \\frac{x^5}{120} - \\frac{x^7}{5040} + ..."
                    },
                    {
                        "step": 2,
                        "title": "Compute sin(x) - x + x³/6",
                        "explanation": "Substitute and combine like terms",
                        "math": "\\sin(x) - x + \\frac{x^3}{6} = \\left(x - \\frac{x^3}{6} + \\frac{x^5}{120} - ...\\right) - x + \\frac{x^3}{6}"
                    },
                    {
                        "step": 3,
                        "title": "Simplify",
                        "explanation": "The x terms cancel, the x³ terms cancel!",
                        "math": "= \\frac{x^5}{120} - \\frac{x^7}{5040} + ..."
                    },
                    {
                        "step": 4,
                        "title": "Divide by x⁵ and take limit",
                        "explanation": "Factor out x⁵, then x → 0",
                        "math": "\\lim_{x \\to 0} \\frac{x^5/120 - x^7/5040 + ...}{x^5} = \\lim_{x \\to 0}\\left(\\frac{1}{120} - \\frac{x^2}{5040} + ...\\right) = \\frac{1}{120}"
                    }
                ],
                "key_concept": "Taylor series is often easier than L'Hôpital's Rule for limits"
            }
        ]
    },
    
    # ==================== POLAR COORDINATES ====================
    "polar_calculus": {
        "name": "Polar Coordinates",
        "prerequisite": "integration_basics",
        "problems": [
            {
                "id": "pol_1_1",
                "level": 1,
                "question": "Find the area enclosed by r = 2cos(θ).",
                "answer": "π",
                "hints": [
                    "This is a circle! It's traced as θ goes from 0 to π",
                    "Area formula: A = (1/2)∫r² dθ",
                    "You'll need the identity: cos²(θ) = (1 + cos(2θ))/2"
                ],
                "walkthrough": [
                    {
                        "step": 1,
                        "title": "Identify the curve and bounds",
                        "explanation": "r = 2cos(θ) is a circle traced from θ = 0 to θ = π",
                        "math": "\\text{Circle, traced for } 0 \\leq \\theta \\leq \\pi"
                    },
                    {
                        "step": 2,
                        "title": "Set up area integral",
                        "explanation": "Use polar area formula A = (1/2)∫r² dθ",
                        "math": "A = \\frac{1}{2}\\int_0^{\\pi} (2\\cos\\theta)^2 d\\theta = \\frac{1}{2}\\int_0^{\\pi} 4\\cos^2\\theta\\, d\\theta"
                    },
                    {
                        "step": 3,
                        "title": "Use half-angle identity",
                        "explanation": "cos²θ = (1 + cos(2θ))/2",
                        "math": "= 2\\int_0^{\\pi} \\frac{1+\\cos(2\\theta)}{2}\\,d\\theta = \\int_0^{\\pi}(1+\\cos(2\\theta))\\,d\\theta"
                    },
                    {
                        "step": 4,
                        "title": "Integrate",
                        "explanation": "∫1 dθ = θ, ∫cos(2θ) dθ = sin(2θ)/2",
                        "math": "= \\left[\\theta + \\frac{\\sin(2\\theta)}{2}\\right]_0^{\\pi} = \\pi + 0 - 0 - 0 = \\pi"
                    }
                ],
                "key_concept": "Polar area: A = (1/2)∫r² dθ. Don't forget the 1/2!"
            }
        ]
    },
    
    # ==================== PARAMETRIC ====================
    "parametric_calculus": {
        "name": "Parametric Equations",
        "prerequisite": "derivatives",
        "problems": [
            {
                "id": "par_1_1",
                "level": 1,
                "question": "Find dy/dx for the parametric curve x = t², y = t³.",
                "answer": "(3/2)t  or  3t/2",
                "hints": [
                    "For parametric curves: dy/dx = (dy/dt) / (dx/dt)",
                    "Find dy/dt and dx/dt separately",
                    "dx/dt = 2t, dy/dt = 3t²"
                ],
                "walkthrough": [
                    {
                        "step": 1,
                        "title": "Find dx/dt",
                        "explanation": "Differentiate x = t² with respect to t",
                        "math": "\\frac{dx}{dt} = 2t"
                    },
                    {
                        "step": 2,
                        "title": "Find dy/dt",
                        "explanation": "Differentiate y = t³ with respect to t",
                        "math": "\\frac{dy}{dt} = 3t^2"
                    },
                    {
                        "step": 3,
                        "title": "Apply the formula",
                        "explanation": "dy/dx = (dy/dt)/(dx/dt)",
                        "math": "\\frac{dy}{dx} = \\frac{3t^2}{2t} = \\frac{3t}{2}"
                    }
                ],
                "key_concept": "Parametric derivative: dy/dx = (dy/dt)/(dx/dt)"
            }
        ]
    }
}


class AdaptiveTutor:
    """Adaptive tutoring system that actually teaches"""
    
    def __init__(self):
        self.progress_file = DATA_DIR / "tutor_progress.json"
        self.progress = self.load_progress()
    
    def load_progress(self) -> Dict:
        if self.progress_file.exists():
            with open(self.progress_file) as f:
                return json.load(f)
        return {
            "mastery": {},  # topic -> {level: score, attempts: count, correct: count}
            "current_level": {},  # topic -> current difficulty level
            "weak_spots": [],  # list of (topic, concept) pairs
            "history": [],  # recent problem attempts
            "streak": 0,
        }
    
    def save_progress(self):
        with open(self.progress_file, 'w') as f:
            json.dump(self.progress, f, indent=2)
    
    def get_recommended_topic(self) -> str:
        """Get the topic the student should work on next"""
        # Priority order based on prerequisites and mastery
        topic_order = [
            "integration_by_parts",
            "partial_fractions", 
            "improper_integrals",
            "series_strategy",
            "taylor_maclaurin",
            "polar_calculus",
            "parametric_calculus"
        ]
        
        for topic in topic_order:
            mastery = self.progress["mastery"].get(topic, {})
            score = mastery.get("score", 0)
            if score < 0.8:  # Less than 80% mastery
                return topic
        
        # All topics mastered - return weakest
        return min(topic_order, key=lambda t: self.progress["mastery"].get(t, {}).get("score", 0))
    
    def get_problem_for_level(self, topic: str, level: int) -> Optional[Dict]:
        """Get a problem at the specified difficulty level"""
        if topic not in PROBLEM_BANK:
            return None
        
        problems = [p for p in PROBLEM_BANK[topic]["problems"] if p["level"] == level]
        if not problems:
            # Try adjacent levels
            problems = PROBLEM_BANK[topic]["problems"]
        
        # Avoid recently seen problems
        recent_ids = [h["problem_id"] for h in self.progress["history"][-10:]]
        unseen = [p for p in problems if p["id"] not in recent_ids]
        
        return random.choice(unseen) if unseen else random.choice(problems)
    
    def get_next_problem(self, topic: str) -> Dict:
        """Get the next problem, adapting to student's level"""
        current_level = self.progress["current_level"].get(topic, 1)
        problem = self.get_problem_for_level(topic, current_level)
        
        if not problem:
            problem = PROBLEM_BANK[topic]["problems"][0]
        
        return {
            "problem": problem,
            "current_level": current_level,
            "topic": topic,
            "topic_name": PROBLEM_BANK[topic]["name"],
            "hint_index": 0,
            "walkthrough_step": 0
        }
    
    def get_hint(self, problem: Dict, hint_level: int) -> Dict:
        """Get a hint at the specified level (0=nudge, 1=hint, 2=bigger hint, etc.)"""
        hints = problem.get("hints", [])
        
        if hint_level < len(hints):
            return {
                "type": "hint",
                "level": hint_level + 1,
                "total_hints": len(hints),
                "content": hints[hint_level],
                "has_more_hints": hint_level < len(hints) - 1,
                "can_walkthrough": True
            }
        else:
            return {
                "type": "no_more_hints",
                "message": "No more hints available. Try the step-by-step walkthrough!",
                "can_walkthrough": True
            }
    
    def get_walkthrough_step(self, problem: Dict, step: int) -> Dict:
        """Get a single step of the walkthrough"""
        walkthrough = problem.get("walkthrough", [])
        
        if step < len(walkthrough):
            ws = walkthrough[step]
            return {
                "type": "walkthrough_step",
                "step": step + 1,
                "total_steps": len(walkthrough),
                "title": ws["title"],
                "explanation": ws["explanation"],
                "math": ws.get("math", ""),
                "has_more_steps": step < len(walkthrough) - 1
            }
        else:
            return {
                "type": "walkthrough_complete",
                "message": "That's the full solution!",
                "key_concept": problem.get("key_concept", "")
            }
    
    def record_attempt(self, topic: str, problem_id: str, correct: bool, used_hints: int, used_walkthrough: bool):
        """Record a problem attempt and adjust difficulty"""
        # Update history
        self.progress["history"].append({
            "topic": topic,
            "problem_id": problem_id,
            "correct": correct,
            "used_hints": used_hints,
            "used_walkthrough": used_walkthrough,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        # Update mastery
        if topic not in self.progress["mastery"]:
            self.progress["mastery"][topic] = {"attempts": 0, "correct": 0, "score": 0}
        
        mastery = self.progress["mastery"][topic]
        mastery["attempts"] += 1
        
        # Weighted scoring: full credit for no help, partial for hints, less for walkthrough
        if correct:
            if used_walkthrough:
                credit = 0.3  # Still learned something!
            elif used_hints > 2:
                credit = 0.5
            elif used_hints > 0:
                credit = 0.7
            else:
                credit = 1.0
            mastery["correct"] += credit
            self.progress["streak"] += 1
        else:
            self.progress["streak"] = 0
        
        # Update score (running average)
        mastery["score"] = mastery["correct"] / mastery["attempts"]
        
        # Adjust difficulty level
        current_level = self.progress["current_level"].get(topic, 1)
        if correct and not used_walkthrough and used_hints <= 1:
            # Doing well - increase difficulty
            self.progress["current_level"][topic] = min(3, current_level + 1)
        elif not correct or used_walkthrough:
            # Struggling - decrease difficulty
            self.progress["current_level"][topic] = max(1, current_level - 1)
            # Mark as weak spot
            if (topic, problem_id) not in self.progress["weak_spots"]:
                self.progress["weak_spots"].append((topic, problem_id))
        
        self.save_progress()
        
        return {
            "mastery_score": mastery["score"],
            "new_level": self.progress["current_level"].get(topic, 1),
            "streak": self.progress["streak"],
            "feedback": self._generate_feedback(correct, used_hints, used_walkthrough)
        }
    
    def _generate_feedback(self, correct: bool, used_hints: int, used_walkthrough: bool) -> str:
        if correct:
            if used_walkthrough:
                return "Good job following along! Try a similar problem without the walkthrough next time."
            elif used_hints > 2:
                return "You got there! The hints helped. Review the key concept and try another."
            elif used_hints > 0:
                return "Nice work! A hint helped point the way. Getting stronger!"
            else:
                return "Excellent! You solved it without help. Keep this momentum!"
        else:
            return "That's okay - learning from mistakes is how we improve. Review the walkthrough and try again."
    
    def get_diagnostic(self) -> Dict:
        """Get a diagnostic summary of the student's knowledge"""
        topics_status = []
        for topic_id, topic_data in PROBLEM_BANK.items():
            mastery = self.progress["mastery"].get(topic_id, {})
            topics_status.append({
                "id": topic_id,
                "name": topic_data["name"],
                "mastery": mastery.get("score", 0),
                "attempts": mastery.get("attempts", 0),
                "level": self.progress["current_level"].get(topic_id, 1),
                "status": "mastered" if mastery.get("score", 0) >= 0.8 else "learning" if mastery.get("attempts", 0) > 0 else "not_started"
            })
        
        return {
            "topics": topics_status,
            "overall_progress": sum(t["mastery"] for t in topics_status) / len(topics_status) if topics_status else 0,
            "streak": self.progress["streak"],
            "weak_spots": self.progress["weak_spots"][-5:],
            "recommended_topic": self.get_recommended_topic()
        }
    
    def get_all_problems_for_topic(self, topic: str) -> List[Dict]:
        """Get all problems for a topic, organized by level"""
        if topic not in PROBLEM_BANK:
            return []
        
        problems = PROBLEM_BANK[topic]["problems"]
        return {
            "topic": topic,
            "name": PROBLEM_BANK[topic]["name"],
            "problems_by_level": {
                1: [p for p in problems if p["level"] == 1],
                2: [p for p in problems if p["level"] == 2],
                3: [p for p in problems if p["level"] == 3],
            },
            "total_problems": len(problems)
        }


# Create singleton instance
tutor = AdaptiveTutor()


def get_tutor():
    return tutor
