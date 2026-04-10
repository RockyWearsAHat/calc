"""
Deep Teaching Module for Calculus II Mastery
============================================
This module provides comprehensive teaching content - not just problems,
but full conceptual explanations, worked examples, visual intuition,
common mistakes, and the "why" behind every technique.

Each topic has:
- Core concept explanation (the "big picture")
- Key formulas with derivations/intuition
- Multiple worked examples (easy → hard)
- Common mistakes and how to avoid them
- When to use this technique vs others
- Practice problem generator
"""

import random
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum

class ConceptDepth(Enum):
    INTUITION = "intuition"      # Big picture, why it matters
    FORMULA = "formula"          # The actual formulas
    TECHNIQUE = "technique"      # Step-by-step how to apply
    EXAMPLES = "examples"        # Worked examples
    PITFALLS = "pitfalls"        # Common mistakes
    CONNECTIONS = "connections"  # Links to other topics

@dataclass
class WorkedExample:
    problem: str
    solution_steps: List[Dict[str, str]]  # Each step has "action" and "result"
    key_insight: str
    difficulty: int  # 1-5

@dataclass
class Concept:
    id: str
    name: str
    intuition: str
    formulas: List[Dict[str, str]]  # formula, meaning, when_to_use
    technique_steps: List[str]
    worked_examples: List[WorkedExample]
    common_mistakes: List[Dict[str, str]]  # mistake, why_wrong, correct_approach
    when_to_use: str
    connections: List[str]  # Related concept IDs
    prerequisites: List[str]


# =============================================================================
# COMPREHENSIVE CALCULUS II TEACHING CONTENT
# =============================================================================

DEEP_TEACHING_CONTENT = {
    # =========================================================================
    # INTEGRATION BY PARTS
    # =========================================================================
    "integration_by_parts": {
        "name": "Integration by Parts",
        "emoji": "🔄",
        "big_picture": """
Integration by Parts is essentially the **Product Rule in reverse**. 

When you learned derivatives, you learned: d/dx[f(x)·g(x)] = f'(x)·g(x) + f(x)·g'(x)

Integration by Parts says: if you have an integral that's a PRODUCT of two different types 
of functions, you can trade one integral for a potentially easier one.

**The Formula:** ∫u dv = uv - ∫v du

**The Key Insight:** You're choosing to differentiate one part (u) and integrate another (dv).
The goal is to make the NEW integral (∫v du) simpler than what you started with.
        """,
        
        "the_formula": {
            "main": "∫u dv = uv - ∫v du",
            "expanded": "∫f(x)g'(x)dx = f(x)g(x) - ∫f'(x)g(x)dx",
            "memory_trick": "**LIATE** - When choosing u, prioritize in this order: Logarithmic, Inverse trig, Algebraic (polynomials), Trigonometric, Exponential"
        },
        
        "when_to_use": [
            "Product of polynomial × exponential: x²eˣ, x³e⁻ˣ",
            "Product of polynomial × trig: x·sin(x), x²·cos(x)",
            "Product of polynomial × logarithm: x·ln(x), x²·ln(x)",
            "Inverse trig alone: arctan(x), arcsin(x)",
            "Logarithm alone: ln(x)",
            "Product of exponential × trig: eˣ·sin(x) [requires IBP twice!]"
        ],
        
        "technique_steps": [
            {
                "step": 1,
                "title": "Identify the Product",
                "action": "Recognize you have two different types of functions multiplied together",
                "example": "∫x·eˣ dx has polynomial (x) × exponential (eˣ)"
            },
            {
                "step": 2,
                "title": "Choose u and dv using LIATE",
                "action": "Let u = the function that appears EARLIER in LIATE (it will be differentiated)",
                "example": "For ∫x·eˣ dx: u = x (algebraic) because A comes before E in LIATE"
            },
            {
                "step": 3,
                "title": "Find du and v",
                "action": "Differentiate u to get du, integrate dv to get v",
                "example": "u = x → du = dx; dv = eˣ dx → v = eˣ"
            },
            {
                "step": 4,
                "title": "Apply the Formula",
                "action": "Plug into ∫u dv = uv - ∫v du",
                "example": "∫x·eˣ dx = x·eˣ - ∫eˣ dx"
            },
            {
                "step": 5,
                "title": "Solve the New Integral",
                "action": "The new integral should be simpler. Evaluate it.",
                "example": "∫eˣ dx = eˣ, so answer = x·eˣ - eˣ + C = eˣ(x-1) + C"
            }
        ],
        
        "worked_examples": [
            {
                "title": "Basic: ∫x·eˣ dx",
                "difficulty": 1,
                "problem": "Evaluate ∫x·eˣ dx",
                "solution": [
                    {"step": "Identify", "work": "Product of polynomial (x) and exponential (eˣ)", "result": "Use Integration by Parts"},
                    {"step": "Choose u, dv", "work": "LIATE: A before E, so u = x, dv = eˣ dx", "result": "u = x, dv = eˣ dx"},
                    {"step": "Find du, v", "work": "du = dx, v = ∫eˣ dx = eˣ", "result": "du = dx, v = eˣ"},
                    {"step": "Apply formula", "work": "∫u dv = uv - ∫v du = x·eˣ - ∫eˣ dx", "result": "x·eˣ - ∫eˣ dx"},
                    {"step": "Evaluate", "work": "∫eˣ dx = eˣ", "result": "x·eˣ - eˣ + C"},
                    {"step": "Simplify", "work": "Factor out eˣ", "result": "eˣ(x - 1) + C ✓"}
                ],
                "key_insight": "The polynomial x becomes simpler when differentiated (just 1), while eˣ stays the same when integrated."
            },
            {
                "title": "Medium: ∫x²·sin(x) dx",
                "difficulty": 2,
                "problem": "Evaluate ∫x²·sin(x) dx",
                "solution": [
                    {"step": "Identify", "work": "Polynomial × Trig → IBP", "result": "Need IBP twice (x² will need 2 derivatives to vanish)"},
                    {"step": "First IBP", "work": "u = x², dv = sin(x)dx → du = 2x dx, v = -cos(x)", "result": "Setup complete"},
                    {"step": "Apply", "work": "x²(-cos x) - ∫(-cos x)(2x)dx", "result": "-x²cos(x) + 2∫x·cos(x)dx"},
                    {"step": "Second IBP", "work": "For ∫x·cos(x)dx: u = x, dv = cos(x)dx", "result": "du = dx, v = sin(x)"},
                    {"step": "Apply again", "work": "x·sin(x) - ∫sin(x)dx = x·sin(x) + cos(x)", "result": "Solved inner integral"},
                    {"step": "Combine", "work": "-x²cos(x) + 2[x·sin(x) + cos(x)]", "result": "-x²cos(x) + 2x·sin(x) + 2cos(x) + C ✓"}
                ],
                "key_insight": "When the polynomial has degree n, you'll need IBP n times. Each time the polynomial degree drops by 1."
            },
            {
                "title": "Hard: ∫eˣ·sin(x) dx",
                "difficulty": 3,
                "problem": "Evaluate ∫eˣ·sin(x) dx",
                "solution": [
                    {"step": "Identify", "work": "Exponential × Trig → Special case! Neither simplifies.", "result": "IBP will create a cycle - use the 'loop back' trick"},
                    {"step": "First IBP", "work": "u = eˣ, dv = sin(x)dx → du = eˣ dx, v = -cos(x)", "result": "Setup"},
                    {"step": "Apply", "work": "eˣ(-cos x) - ∫(-cos x)(eˣ)dx", "result": "-eˣcos(x) + ∫eˣcos(x)dx"},
                    {"step": "Second IBP", "work": "For ∫eˣcos(x)dx: u = eˣ, dv = cos(x)dx", "result": "du = eˣ dx, v = sin(x)"},
                    {"step": "Apply again", "work": "eˣsin(x) - ∫eˣsin(x)dx", "result": "Notice: original integral appeared!"},
                    {"step": "Let I = ∫eˣsin(x)dx", "work": "I = -eˣcos(x) + eˣsin(x) - I", "result": "2I = eˣ(sin x - cos x)"},
                    {"step": "Solve for I", "work": "I = ½eˣ(sin x - cos x) + C", "result": "(eˣ/2)(sin x - cos x) + C ✓"}
                ],
                "key_insight": "When IBP leads back to the original integral, call it 'I', set up an equation, and solve algebraically!"
            },
            {
                "title": "Tricky: ∫ln(x) dx",
                "difficulty": 2,
                "problem": "Evaluate ∫ln(x) dx",
                "solution": [
                    {"step": "Identify", "work": "Logarithm alone - where's the product?", "result": "Trick: write as ∫ln(x)·1 dx"},
                    {"step": "Choose u, dv", "work": "u = ln(x), dv = 1·dx", "result": "du = (1/x)dx, v = x"},
                    {"step": "Apply formula", "work": "ln(x)·x - ∫x·(1/x)dx", "result": "x·ln(x) - ∫1 dx"},
                    {"step": "Evaluate", "work": "∫1 dx = x", "result": "x·ln(x) - x + C"},
                    {"step": "Factor", "work": "x(ln x - 1) + C", "result": "x·ln(x) - x + C ✓"}
                ],
                "key_insight": "When you have a function alone that's hard to integrate directly (like ln x, arctan x), multiply by 1 and use IBP!"
            }
        ],
        
        "common_mistakes": [
            {
                "mistake": "Choosing u and dv backwards",
                "example": "For ∫x·eˣ dx, setting u = eˣ and dv = x dx",
                "why_wrong": "This makes the integral HARDER: you'd get ∫(x²/2)·eˣ dx which is worse!",
                "correct": "Always use LIATE: Logarithmic > Inverse trig > Algebraic > Trig > Exponential"
            },
            {
                "mistake": "Forgetting the minus sign in the formula",
                "example": "Writing ∫u dv = uv + ∫v du",
                "why_wrong": "The formula is uv MINUS ∫v du, not plus!",
                "correct": "∫u dv = uv - ∫v du (the minus comes from the product rule derivation)"
            },
            {
                "mistake": "Not recognizing when to use IBP twice",
                "example": "For ∫x²·cos(x) dx, stopping after one application",
                "why_wrong": "After one IBP you still have ∫x·sin(x) dx which needs another IBP",
                "correct": "Polynomial of degree n requires n applications of IBP"
            },
            {
                "mistake": "Missing the 'cycle' pattern with eˣ × trig",
                "example": "Doing IBP forever on ∫eˣ·sin(x) dx",
                "why_wrong": "After 2 IBPs, you get the original integral back - this is a signal!",
                "correct": "Set I = original integral, solve the algebraic equation I = ... - I"
            }
        ],
        
        "practice_templates": [
            {"template": "∫{a}x·e^({b}x) dx", "params": {"a": [1,2,3], "b": [1,2,-1]}},
            {"template": "∫x^{n}·sin({a}x) dx", "params": {"n": [1,2], "a": [1,2]}},
            {"template": "∫x^{n}·cos({a}x) dx", "params": {"n": [1,2], "a": [1,2]}},
            {"template": "∫x^{n}·ln(x) dx", "params": {"n": [1,2,3]}},
            {"template": "∫e^({a}x)·sin({b}x) dx", "params": {"a": [1,2], "b": [1,2]}},
            {"template": "∫arctan(x) dx", "params": {}},
            {"template": "∫arcsin(x) dx", "params": {}},
            {"template": "∫x·arctan(x) dx", "params": {}},
        ]
    },
    
    # =========================================================================
    # PARTIAL FRACTIONS
    # =========================================================================
    "partial_fractions": {
        "name": "Partial Fraction Decomposition",
        "emoji": "🧩",
        "big_picture": """
Partial Fractions is about **breaking apart** a complicated fraction into simpler pieces.

Think of it like this: If I give you 5/6, you could write it as 1/2 + 1/3. Each piece is simpler!

For integration, we use this because:
- ∫1/(x-a) dx = ln|x-a| + C (easy!)  
- ∫1/(x²+1) dx = arctan(x) + C (known!)

But ∫(2x+3)/((x-1)(x+2)) dx is hard... unless we SPLIT it into simpler fractions first!

**The Key Insight:** Any rational function (polynomial/polynomial) where the numerator degree 
is less than the denominator degree can be split into a sum of simpler fractions.
        """,
        
        "the_formula": {
            "main": "P(x)/Q(x) = A₁/(factor₁) + A₂/(factor₂) + ...",
            "types": {
                "distinct_linear": "(ax+b)/((x-r₁)(x-r₂)) = A/(x-r₁) + B/(x-r₂)",
                "repeated_linear": "P(x)/(x-r)ⁿ = A₁/(x-r) + A₂/(x-r)² + ... + Aₙ/(x-r)ⁿ",
                "irreducible_quadratic": "P(x)/(x²+bx+c) = (Ax+B)/(x²+bx+c)",
                "repeated_quadratic": "P(x)/(x²+1)² = (Ax+B)/(x²+1) + (Cx+D)/(x²+1)²"
            }
        },
        
        "when_to_use": [
            "Rational function where degree(numerator) < degree(denominator)",
            "Denominator can be factored",
            "After polynomial long division (if degree num ≥ degree denom)"
        ],
        
        "technique_steps": [
            {
                "step": 1,
                "title": "Check Degrees",
                "action": "If degree(numerator) ≥ degree(denominator), do polynomial long division first",
                "example": "(x³+1)/(x²-1) → divide first, then decompose the remainder"
            },
            {
                "step": 2,
                "title": "Factor the Denominator Completely",
                "action": "Factor into linear and irreducible quadratic factors",
                "example": "x³-x = x(x²-1) = x(x-1)(x+1)"
            },
            {
                "step": 3,
                "title": "Set Up the Decomposition",
                "action": "Write one fraction for each factor (with unknowns A, B, C...)",
                "example": "1/(x(x-1)(x+1)) = A/x + B/(x-1) + C/(x+1)"
            },
            {
                "step": 4,
                "title": "Clear Denominators",
                "action": "Multiply both sides by the full denominator",
                "example": "1 = A(x-1)(x+1) + Bx(x+1) + Cx(x-1)"
            },
            {
                "step": 5,
                "title": "Solve for Constants",
                "action": "Use strategic substitution (plug in roots) or compare coefficients",
                "example": "x=0: 1 = A(-1)(1) → A = -1; x=1: 1 = B(1)(2) → B = 1/2"
            },
            {
                "step": 6,
                "title": "Integrate Each Piece",
                "action": "∫A/(x-a) dx = A·ln|x-a|, etc.",
                "example": "∫-1/x + (1/2)/(x-1) + (1/2)/(x+1) dx = -ln|x| + ½ln|x-1| + ½ln|x+1| + C"
            }
        ],
        
        "worked_examples": [
            {
                "title": "Basic: Distinct Linear Factors",
                "difficulty": 1,
                "problem": "∫(3x+5)/((x+1)(x+2)) dx",
                "solution": [
                    {"step": "Setup", "work": "(3x+5)/((x+1)(x+2)) = A/(x+1) + B/(x+2)", "result": "Decomposition form"},
                    {"step": "Clear denominators", "work": "3x+5 = A(x+2) + B(x+1)", "result": "Equation to solve"},
                    {"step": "Find A (let x=-1)", "work": "3(-1)+5 = A(1) + B(0) → 2 = A", "result": "A = 2"},
                    {"step": "Find B (let x=-2)", "work": "3(-2)+5 = A(0) + B(-1) → -1 = -B", "result": "B = 1"},
                    {"step": "Rewrite", "work": "∫2/(x+1) + 1/(x+2) dx", "result": "Ready to integrate"},
                    {"step": "Integrate", "work": "2ln|x+1| + ln|x+2| + C", "result": "2ln|x+1| + ln|x+2| + C ✓"}
                ],
                "key_insight": "Plugging in the roots of each factor zeros out all other terms, making it easy to find each constant."
            },
            {
                "title": "Medium: Repeated Linear Factor",
                "difficulty": 2,
                "problem": "∫(x+3)/(x²(x-1)) dx",
                "solution": [
                    {"step": "Setup", "work": "(x+3)/(x²(x-1)) = A/x + B/x² + C/(x-1)", "result": "Note: x² needs TWO terms"},
                    {"step": "Clear denominators", "work": "x+3 = Ax(x-1) + B(x-1) + Cx²", "result": "Expand and solve"},
                    {"step": "Find B (let x=0)", "work": "3 = B(-1) → B = -3", "result": "B = -3"},
                    {"step": "Find C (let x=1)", "work": "4 = C(1) → C = 4", "result": "C = 4"},
                    {"step": "Find A (compare x² terms)", "work": "0 = A + C → A = -4", "result": "A = -4"},
                    {"step": "Integrate", "work": "∫-4/x - 3/x² + 4/(x-1) dx", "result": "-4ln|x| + 3/x + 4ln|x-1| + C ✓"}
                ],
                "key_insight": "Repeated factor (x-a)ⁿ needs n separate fractions: A/(x-a), B/(x-a)², ..., up to 1/(x-a)ⁿ"
            },
            {
                "title": "Hard: Irreducible Quadratic",
                "difficulty": 3,
                "problem": "∫(2x+1)/(x(x²+1)) dx",
                "solution": [
                    {"step": "Setup", "work": "(2x+1)/(x(x²+1)) = A/x + (Bx+C)/(x²+1)", "result": "Quadratic gets (Bx+C) on top"},
                    {"step": "Clear denominators", "work": "2x+1 = A(x²+1) + (Bx+C)x", "result": "Expand: 2x+1 = Ax²+A + Bx²+Cx"},
                    {"step": "Compare coefficients", "work": "x²: 0=A+B; x¹: 2=C; x⁰: 1=A", "result": "A=1, B=-1, C=2"},
                    {"step": "Rewrite", "work": "∫1/x + (-x+2)/(x²+1) dx", "result": "Split the second term"},
                    {"step": "Split further", "work": "∫1/x - x/(x²+1) + 2/(x²+1) dx", "result": "Three integrals"},
                    {"step": "Integrate", "work": "ln|x| - ½ln(x²+1) + 2arctan(x) + C", "result": "ln|x| - ½ln(x²+1) + 2arctan(x) + C ✓"}
                ],
                "key_insight": "For irreducible quadratic x²+bx+c, the numerator must be linear (Ax+B), not just a constant!"
            }
        ],
        
        "common_mistakes": [
            {
                "mistake": "Using A instead of (Ax+B) for quadratic factors",
                "example": "1/(x(x²+1)) ≠ A/x + B/(x²+1)",
                "why_wrong": "Quadratic denominators need linear numerators to have enough 'degrees of freedom'",
                "correct": "1/(x(x²+1)) = A/x + (Bx+C)/(x²+1)"
            },
            {
                "mistake": "Forgetting to handle repeated factors",
                "example": "1/(x-1)³ ≠ A/(x-1)",
                "why_wrong": "Need one term for each power: 1/(x-1) + 1/(x-1)² + 1/(x-1)³",
                "correct": "1/(x-1)³ = A/(x-1) + B/(x-1)² + C/(x-1)³"
            },
            {
                "mistake": "Not doing long division when degree(num) ≥ degree(denom)",
                "example": "∫x³/(x²-1) dx - jumping straight to partial fractions",
                "why_wrong": "Must divide first: x³/(x²-1) = x + x/(x²-1)",
                "correct": "Divide, then decompose the proper fraction part"
            }
        ],
        
        "practice_templates": [
            {"template": "∫({a}x+{b})/((x+{c})(x+{d})) dx", "params": {"a": [1,2,3], "b": [1,2,-1], "c": [1,2], "d": [3,4]}},
            {"template": "∫{a}/(x(x-{b})) dx", "params": {"a": [1,2], "b": [1,2,3]}},
            {"template": "∫(x+{a})/(x²(x-{b})) dx", "params": {"a": [1,2], "b": [1,2]}},
            {"template": "∫({a}x+{b})/(x(x²+{c})) dx", "params": {"a": [1,2], "b": [1,2], "c": [1,4]}}
        ]
    },
    
    # =========================================================================
    # IMPROPER INTEGRALS  
    # =========================================================================
    "improper_integrals": {
        "name": "Improper Integrals",
        "emoji": "∞",
        "big_picture": """
Improper integrals handle two situations where "normal" integration breaks:

1. **Infinite limits:** ∫₁^∞ 1/x² dx - How do you integrate to infinity?
2. **Infinite integrand:** ∫₀^1 1/√x dx - The function blows up at x=0!

**The Key Idea:** Replace the "bad" point with a limit.

- ∫₁^∞ f(x)dx = lim(b→∞) ∫₁^b f(x)dx
- ∫₀^1 1/√x dx = lim(a→0⁺) ∫ₐ^1 1/√x dx

If the limit exists (finite number), the integral **converges**.
If the limit is ±∞ or doesn't exist, the integral **diverges**.
        """,
        
        "the_formula": {
            "infinite_upper": "∫ₐ^∞ f(x)dx = lim(b→∞) ∫ₐ^b f(x)dx",
            "infinite_lower": "∫₋∞^b f(x)dx = lim(a→-∞) ∫ₐ^b f(x)dx",
            "both_infinite": "∫₋∞^∞ f(x)dx = ∫₋∞^c f(x)dx + ∫c^∞ f(x)dx (split at any c)",
            "discontinuity": "∫ₐ^b f(x)dx with discontinuity at c: lim(t→c⁻) ∫ₐ^t + lim(t→c⁺) ∫t^b"
        },
        
        "key_results": {
            "p_integral": "∫₁^∞ 1/xᵖ dx converges iff p > 1 (equals 1/(p-1))",
            "exponential": "∫₀^∞ e⁻ˣ dx = 1 (converges)",
            "at_zero": "∫₀^1 1/xᵖ dx converges iff p < 1"
        },
        
        "technique_steps": [
            {
                "step": 1,
                "title": "Identify the Problem",
                "action": "Is it infinite limits? Or does the integrand blow up somewhere?",
                "example": "∫₁^∞ 1/x² dx - infinite upper limit"
            },
            {
                "step": 2,
                "title": "Replace with a Limit",
                "action": "Replace ∞ with b, or replace the discontinuity with a→0⁺",
                "example": "∫₁^∞ 1/x² dx = lim(b→∞) ∫₁^b 1/x² dx"
            },
            {
                "step": 3,
                "title": "Evaluate the 'Nice' Integral",
                "action": "Integrate as usual with the variable limit",
                "example": "∫₁^b 1/x² dx = [-1/x]₁^b = -1/b + 1"
            },
            {
                "step": 4,
                "title": "Take the Limit",
                "action": "Evaluate the limit of your answer",
                "example": "lim(b→∞) (-1/b + 1) = 0 + 1 = 1"
            },
            {
                "step": 5,
                "title": "Conclude",
                "action": "Finite → converges to that value. Infinite → diverges.",
                "example": "∫₁^∞ 1/x² dx = 1 (converges)"
            }
        ],
        
        "worked_examples": [
            {
                "title": "Basic: Infinite Upper Limit",
                "difficulty": 1,
                "problem": "Determine if ∫₁^∞ 1/x² dx converges or diverges. If it converges, find its value.",
                "solution": [
                    {"step": "Setup", "work": "Replace ∞ with b: lim(b→∞) ∫₁^b x⁻² dx", "result": "Limit setup"},
                    {"step": "Integrate", "work": "∫x⁻² dx = x⁻¹/(-1) = -1/x", "result": "Antiderivative found"},
                    {"step": "Evaluate bounds", "work": "[-1/x]₁^b = -1/b - (-1/1) = -1/b + 1", "result": "Expression in b"},
                    {"step": "Take limit", "work": "lim(b→∞) (-1/b + 1) = 0 + 1 = 1", "result": "Limit exists!"},
                    {"step": "Conclude", "work": "The integral converges", "result": "∫₁^∞ 1/x² dx = 1 ✓"}
                ],
                "key_insight": "This is the p-integral with p=2. Since p>1, it converges."
            },
            {
                "title": "Comparison: ∫₁^∞ 1/x dx (the critical case)",
                "difficulty": 1,
                "problem": "Determine if ∫₁^∞ 1/x dx converges or diverges.",
                "solution": [
                    {"step": "Setup", "work": "lim(b→∞) ∫₁^b 1/x dx", "result": "Limit setup"},
                    {"step": "Integrate", "work": "∫1/x dx = ln|x|", "result": "Antiderivative"},
                    {"step": "Evaluate bounds", "work": "[ln|x|]₁^b = ln(b) - ln(1) = ln(b)", "result": "Expression in b"},
                    {"step": "Take limit", "work": "lim(b→∞) ln(b) = ∞", "result": "Limit is infinite!"},
                    {"step": "Conclude", "work": "The integral diverges", "result": "∫₁^∞ 1/x dx = ∞ (diverges) ✓"}
                ],
                "key_insight": "This is p=1, the boundary case. It DIVERGES! Memorize: 1/x diverges, 1/x² converges."
            },
            {
                "title": "Type 2: Discontinuity at Endpoint",
                "difficulty": 2,
                "problem": "Evaluate ∫₀^1 1/√x dx",
                "solution": [
                    {"step": "Identify problem", "work": "1/√x → ∞ as x → 0⁺", "result": "Discontinuity at lower limit"},
                    {"step": "Setup", "work": "lim(a→0⁺) ∫ₐ^1 x⁻¹/² dx", "result": "Replace 0 with a"},
                    {"step": "Integrate", "work": "∫x⁻¹/² dx = x^(1/2)/(1/2) = 2√x", "result": "Antiderivative"},
                    {"step": "Evaluate bounds", "work": "[2√x]ₐ^1 = 2√1 - 2√a = 2 - 2√a", "result": "Expression in a"},
                    {"step": "Take limit", "work": "lim(a→0⁺) (2 - 2√a) = 2 - 0 = 2", "result": "Finite limit!"},
                    {"step": "Conclude", "work": "The integral converges", "result": "∫₀^1 1/√x dx = 2 ✓"}
                ],
                "key_insight": "Even though 1/√x blows up at 0, the area underneath is finite! (p=1/2 < 1 at left endpoint)"
            },
            {
                "title": "Hard: Comparison Test",
                "difficulty": 3,
                "problem": "Determine if ∫₁^∞ 1/(x²+1) dx converges or diverges",
                "solution": [
                    {"step": "Compare", "work": "For x≥1: x²+1 > x², so 1/(x²+1) < 1/x²", "result": "Smaller than known convergent"},
                    {"step": "Known result", "work": "∫₁^∞ 1/x² dx converges (p=2>1)", "result": "Comparison integral converges"},
                    {"step": "Apply Comparison Test", "work": "Since 0 < 1/(x²+1) < 1/x² and ∫1/x² converges...", "result": "By comparison, our integral converges"},
                    {"step": "Verify by computing", "work": "lim(b→∞)[arctan(x)]₁^b = π/2 - π/4 = π/4", "result": "∫₁^∞ 1/(x²+1) dx = π/4 ✓"}
                ],
                "key_insight": "Comparison Test: if 0 ≤ f(x) ≤ g(x) and ∫g converges, then ∫f converges too."
            }
        ],
        
        "common_mistakes": [
            {
                "mistake": "Not checking for discontinuities inside the interval",
                "example": "∫₋₁^1 1/x² dx - treating as normal integral",
                "why_wrong": "1/x² is undefined at x=0, which is INSIDE [-1,1]!",
                "correct": "Split: ∫₋₁^0 + ∫₀^1, each with its own limit. (This one diverges!)"
            },
            {
                "mistake": "Thinking ∫₁^∞ 1/x dx converges because 1/x → 0",
                "example": "\"1/x gets small, so the integral should be finite\"",
                "why_wrong": "Going to 0 isn't enough - it has to go to 0 FAST enough. 1/x is too slow.",
                "correct": "Need p>1 for convergence. 1/x (p=1) diverges logarithmically."
            },
            {
                "mistake": "Splitting ∫₋∞^∞ incorrectly",
                "example": "∫₋∞^∞ x dx = [x²/2]₋∞^∞ = ∞ - ∞ = 0? NO!",
                "why_wrong": "You MUST split at a finite point and BOTH halves must converge separately",
                "correct": "∫₋∞^∞ x dx diverges because each half ∫₋∞^0 x dx and ∫₀^∞ x dx diverges"
            }
        ],
        
        "practice_templates": [
            {"template": "∫₁^∞ 1/x^{p} dx", "params": {"p": [0.5, 1, 1.5, 2, 3]}},
            {"template": "∫₀^∞ e^(-{a}x) dx", "params": {"a": [1, 2, 0.5]}},
            {"template": "∫₀^1 1/x^{p} dx", "params": {"p": [0.5, 1, 1.5]}},
            {"template": "∫₁^∞ 1/(x²+{a}) dx", "params": {"a": [1, 4, 9]}}
        ]
    },
    
    # =========================================================================
    # SERIES CONVERGENCE
    # =========================================================================
    "series_convergence": {
        "name": "Infinite Series & Convergence Tests",
        "emoji": "📊",
        "big_picture": """
An infinite series Σaₙ is about adding infinitely many terms: a₁ + a₂ + a₃ + ...

**The Big Question:** Does this infinite sum equal a finite number?

- If yes → the series **converges**
- If no → the series **diverges**

**Key Insight:** A series converges if its partial sums Sₙ = a₁ + a₂ + ... + aₙ approach a finite limit.

We have many **tests** to determine convergence WITHOUT computing the actual sum:
1. Divergence Test (quick elimination)
2. Geometric Series (formula exists!)
3. p-Series (simple rule)
4. Comparison Tests
5. Ratio Test (great for factorials/exponentials)
6. Root Test
7. Integral Test
8. Alternating Series Test
        """,
        
        "the_tests": {
            "divergence_test": {
                "statement": "If lim(n→∞) aₙ ≠ 0, then Σaₙ DIVERGES",
                "warning": "If lim aₙ = 0, the test is INCONCLUSIVE (not proof of convergence!)",
                "example_fail": "Σ1/n: lim(1/n)=0 but it still DIVERGES"
            },
            "geometric_series": {
                "statement": "Σarⁿ converges iff |r| < 1, and sum = a/(1-r)",
                "example": "Σ(1/2)ⁿ = 1/(1-1/2) = 2"
            },
            "p_series": {
                "statement": "Σ1/nᵖ converges iff p > 1",
                "examples": "Σ1/n² converges (p=2>1), Σ1/n diverges (p=1)"
            },
            "ratio_test": {
                "statement": "Let L = lim|aₙ₊₁/aₙ|. If L<1: converges. If L>1: diverges. If L=1: inconclusive",
                "best_for": "Factorials, exponentials, combinations"
            },
            "root_test": {
                "statement": "Let L = lim ⁿ√|aₙ|. If L<1: converges. If L>1: diverges. If L=1: inconclusive",
                "best_for": "Terms raised to the nth power"
            },
            "comparison_test": {
                "statement": "If 0 ≤ aₙ ≤ bₙ and Σbₙ converges, then Σaₙ converges",
                "reverse": "If 0 ≤ bₙ ≤ aₙ and Σbₙ diverges, then Σaₙ diverges"
            },
            "limit_comparison": {
                "statement": "If lim(aₙ/bₙ) = c where 0 < c < ∞, then Σaₙ and Σbₙ either both converge or both diverge",
                "best_for": "When direct comparison is tricky"
            },
            "alternating_series": {
                "statement": "Σ(-1)ⁿbₙ converges if: (1) bₙ > 0, (2) bₙ₊₁ ≤ bₙ (decreasing), (3) lim bₙ = 0",
                "example": "Σ(-1)ⁿ/n converges (alternating harmonic)"
            }
        },
        
        "strategy_flowchart": """
**TEST SELECTION STRATEGY:**

1. First, check: does aₙ → 0? If NOT → DIVERGES (Divergence Test)

2. Recognize special forms:
   - Looks like arⁿ → Geometric Series
   - Looks like 1/nᵖ → p-Series
   - Has (-1)ⁿ → Alternating Series Test

3. For everything else:
   - Has n! or aⁿ → Ratio Test (usually best)
   - Has (...)ⁿ form → Root Test
   - Comparable to p-series → Comparison or Limit Comparison
   - Can integrate the function → Integral Test
        """,
        
        "worked_examples": [
            {
                "title": "Geometric Series",
                "difficulty": 1,
                "problem": "Determine if Σ(2/3)ⁿ from n=0 to ∞ converges. If so, find the sum.",
                "solution": [
                    {"step": "Identify", "work": "This is geometric with a=1, r=2/3", "result": "Geometric series form"},
                    {"step": "Check |r|", "work": "|2/3| = 2/3 < 1", "result": "Converges!"},
                    {"step": "Apply formula", "work": "Sum = a/(1-r) = 1/(1-2/3) = 1/(1/3)", "result": "= 3"},
                    {"step": "Conclude", "work": "Σ(2/3)ⁿ = 3", "result": "Converges to 3 ✓"}
                ],
                "key_insight": "Geometric series are the ONLY common series where we can easily find the exact sum."
            },
            {
                "title": "Ratio Test with Factorial",
                "difficulty": 2,
                "problem": "Determine if Σ n!/nⁿ converges or diverges",
                "solution": [
                    {"step": "Choose test", "work": "Factorial → Ratio Test", "result": "Compute aₙ₊₁/aₙ"},
                    {"step": "Setup ratio", "work": "aₙ₊₁/aₙ = [(n+1)!/(n+1)ⁿ⁺¹] · [nⁿ/n!]", "result": "Simplify..."},
                    {"step": "Simplify", "work": "= (n+1)·nⁿ/(n+1)ⁿ⁺¹ = nⁿ/(n+1)ⁿ", "result": "= [n/(n+1)]ⁿ"},
                    {"step": "Take limit", "work": "lim [n/(n+1)]ⁿ = lim [1/(1+1/n)]ⁿ = 1/e", "result": "L = 1/e ≈ 0.368"},
                    {"step": "Conclude", "work": "L = 1/e < 1", "result": "CONVERGES by Ratio Test ✓"}
                ],
                "key_insight": "Ratio test is perfect for factorials because n!/(n-1)! = n simplifies beautifully."
            },
            {
                "title": "p-Series Recognition",
                "difficulty": 1,
                "problem": "Does Σ1/n³ converge or diverge?",
                "solution": [
                    {"step": "Identify", "work": "This is Σ1/nᵖ with p=3", "result": "p-series"},
                    {"step": "Apply rule", "work": "p=3 > 1", "result": "Converges!"},
                    {"step": "Conclude", "work": "Σ1/n³ converges", "result": "CONVERGES ✓"}
                ],
                "key_insight": "p-series: p>1 converges, p≤1 diverges. That's it!"
            },
            {
                "title": "Limit Comparison",
                "difficulty": 2,
                "problem": "Does Σ(n+1)/(n³+2n) converge or diverge?",
                "solution": [
                    {"step": "Identify dominant terms", "work": "For large n: (n+1)/(n³+2n) ≈ n/n³ = 1/n²", "result": "Compare to 1/n²"},
                    {"step": "Compute limit", "work": "lim [(n+1)/(n³+2n)] / [1/n²]", "result": "= lim (n+1)·n²/(n³+2n)"},
                    {"step": "Simplify", "work": "= lim (n³+n²)/(n³+2n) = lim n³/n³ = 1", "result": "L = 1 (finite, positive)"},
                    {"step": "Conclude", "work": "Since Σ1/n² converges (p=2>1) and L=1...", "result": "Our series CONVERGES ✓"}
                ],
                "key_insight": "For rational functions, compare to 1/n^(degree diff). Here: degree 3 - degree 1 = 2."
            },
            {
                "title": "Alternating Series",
                "difficulty": 2,
                "problem": "Does Σ(-1)ⁿ/√n converge or diverge?",
                "solution": [
                    {"step": "Identify", "work": "Has (-1)ⁿ → alternating series", "result": "Use Alternating Series Test"},
                    {"step": "Check bₙ = 1/√n > 0", "work": "Yes, 1/√n > 0 for all n≥1", "result": "Condition 1: ✓"},
                    {"step": "Check decreasing", "work": "1/√(n+1) < 1/√n? Yes!", "result": "Condition 2: ✓"},
                    {"step": "Check limit", "work": "lim 1/√n = 0", "result": "Condition 3: ✓"},
                    {"step": "Conclude", "work": "All conditions met", "result": "CONVERGES ✓"}
                ],
                "key_insight": "Alternating series can converge even when the non-alternating version diverges! Σ(-1)ⁿ/√n converges but Σ1/√n diverges."
            }
        ],
        
        "common_mistakes": [
            {
                "mistake": "Thinking lim aₙ = 0 means the series converges",
                "example": "Σ1/n: lim(1/n) = 0, so it converges? NO!",
                "why_wrong": "The Divergence Test only works one way: lim≠0 → diverges. lim=0 tells you NOTHING.",
                "correct": "Σ1/n diverges (harmonic series). Always use a proper convergence test."
            },
            {
                "mistake": "Using Ratio Test when L=1",
                "example": "For Σ1/n², ratio test gives L=1, so... ???",
                "why_wrong": "L=1 is INCONCLUSIVE. You must use a different test.",
                "correct": "For Σ1/n², recognize it's a p-series (p=2>1), so it converges."
            },
            {
                "mistake": "Comparing to the wrong series",
                "example": "Comparing Σ1/(n²+1) to Σ1/n (which diverges)",
                "why_wrong": "1/(n²+1) < 1/n, but Σ1/n diverges, so comparison tells you nothing!",
                "correct": "Compare to Σ1/n² instead: 1/(n²+1) < 1/n² and Σ1/n² converges → our series converges"
            },
            {
                "mistake": "Forgetting to check decreasing for Alternating Series Test",
                "example": "Σ(-1)ⁿ sin(1/n): lim sin(1/n) = 0, so it converges?",
                "why_wrong": "You must also verify that bₙ is decreasing!",
                "correct": "sin(1/n) IS decreasing for n≥1, so yes it converges, but you must check."
            }
        ],
        
        "practice_templates": [
            {"template": "Σ({a}/{b})ⁿ", "params": {"a": [1,2,3], "b": [2,3,4]}},
            {"template": "Σ1/n^{p}", "params": {"p": [0.5, 1, 1.5, 2, 3]}},
            {"template": "Σn^{k}/{a}ⁿ", "params": {"k": [1,2], "a": [2,3]}},
            {"template": "Σn!/n^{n}", "params": {}},
            {"template": "Σ(-1)ⁿ/n^{p}", "params": {"p": [0.5, 1, 2]}}
        ]
    },

    # =========================================================================
    # TAYLOR AND MACLAURIN SERIES
    # =========================================================================
    "taylor_series": {
        "name": "Taylor & Maclaurin Series",
        "emoji": "📈",
        "big_picture": """
Taylor series let you write ANY smooth function as an infinite polynomial!

**The Idea:** Near a point x=a, we can approximate f(x) using:
- The value f(a)
- The slope f'(a)  
- The curvature f''(a)
- Higher derivatives...

**Maclaurin series** = Taylor series centered at a=0.

**The Power:** Once you have a series, you can:
- Approximate difficult functions with polynomials
- Integrate "impossible" functions term by term
- Solve differential equations
- Compute limits without L'Hôpital

**Key Series to MEMORIZE:**
- eˣ = 1 + x + x²/2! + x³/3! + ... = Σxⁿ/n!
- sin(x) = x - x³/3! + x⁵/5! - ... = Σ(-1)ⁿx²ⁿ⁺¹/(2n+1)!
- cos(x) = 1 - x²/2! + x⁴/4! - ... = Σ(-1)ⁿx²ⁿ/(2n)!
- 1/(1-x) = 1 + x + x² + x³ + ... = Σxⁿ (|x|<1)
- ln(1+x) = x - x²/2 + x³/3 - ... = Σ(-1)ⁿ⁺¹xⁿ/n (|x|<1)
        """,
        
        "the_formula": {
            "taylor": "f(x) = Σ f⁽ⁿ⁾(a)/n! · (x-a)ⁿ",
            "maclaurin": "f(x) = Σ f⁽ⁿ⁾(0)/n! · xⁿ",
            "radius": "R = lim |aₙ/aₙ₊₁| or use ratio test on the series"
        },
        
        "essential_series": [
            {"function": "eˣ", "series": "Σxⁿ/n! = 1 + x + x²/2! + x³/3! + ...", "radius": "R = ∞"},
            {"function": "sin(x)", "series": "Σ(-1)ⁿx²ⁿ⁺¹/(2n+1)! = x - x³/3! + x⁵/5! - ...", "radius": "R = ∞"},
            {"function": "cos(x)", "series": "Σ(-1)ⁿx²ⁿ/(2n)! = 1 - x²/2! + x⁴/4! - ...", "radius": "R = ∞"},
            {"function": "1/(1-x)", "series": "Σxⁿ = 1 + x + x² + x³ + ...", "radius": "R = 1"},
            {"function": "1/(1+x)", "series": "Σ(-1)ⁿxⁿ = 1 - x + x² - x³ + ...", "radius": "R = 1"},
            {"function": "ln(1+x)", "series": "Σ(-1)ⁿ⁺¹xⁿ/n = x - x²/2 + x³/3 - ...", "radius": "R = 1"},
            {"function": "arctan(x)", "series": "Σ(-1)ⁿx²ⁿ⁺¹/(2n+1) = x - x³/3 + x⁵/5 - ...", "radius": "R = 1"},
            {"function": "(1+x)ᵏ", "series": "1 + kx + k(k-1)x²/2! + ... (binomial)", "radius": "R = 1"}
        ],
        
        "technique_steps": [
            {
                "step": 1,
                "title": "Identify: Build from scratch or manipulate known series?",
                "action": "If the function is related to eˣ, sin, cos, 1/(1-x), ln(1+x), use known series",
                "example": "e⁻ˣ² → start with eˣ, substitute -x² for x"
            },
            {
                "step": 2,
                "title": "For manipulation: Apply substitution, multiplication, or calculus",
                "action": "Replace x with something, multiply by xᵏ, differentiate, or integrate",
                "example": "xe^x = x·(1 + x + x²/2! + ...) = x + x² + x³/2! + ..."
            },
            {
                "step": 3,
                "title": "For building from scratch: Compute derivatives at center",
                "action": "Find f(a), f'(a), f''(a), ... and plug into Taylor formula",
                "example": "For f(x)=√x at a=4: f(4)=2, f'(4)=1/4, f''(4)=-1/32, ..."
            },
            {
                "step": 4,
                "title": "Find the radius of convergence",
                "action": "Use ratio test: R = lim |aₙ/aₙ₊₁|",
                "example": "For eˣ: |aₙ₊₁/aₙ| = |x|/(n+1) → 0 as n→∞, so R = ∞"
            }
        ],
        
        "worked_examples": [
            {
                "title": "Manipulation: Find series for e^(-x²)",
                "difficulty": 2,
                "problem": "Find the Maclaurin series for e^(-x²)",
                "solution": [
                    {"step": "Start with known", "work": "eˣ = 1 + x + x²/2! + x³/3! + ... = Σxⁿ/n!", "result": "Known series"},
                    {"step": "Substitute", "work": "Replace x with -x²", "result": "e^(-x²) = Σ(-x²)ⁿ/n!"},
                    {"step": "Simplify", "work": "(-x²)ⁿ = (-1)ⁿx²ⁿ", "result": "e^(-x²) = Σ(-1)ⁿx²ⁿ/n!"},
                    {"step": "Write out terms", "work": "= 1 - x² + x⁴/2! - x⁶/3! + ...", "result": "Series complete ✓"},
                    {"step": "Radius", "work": "eˣ converges for all x, so does e^(-x²)", "result": "R = ∞"}
                ],
                "key_insight": "Most Taylor series problems are about MANIPULATING known series, not computing derivatives!"
            },
            {
                "title": "Integration: ∫e^(-x²)dx",
                "difficulty": 3,
                "problem": "Find the Maclaurin series for ∫₀ˣ e^(-t²)dt (this integral has no elementary antiderivative!)",
                "solution": [
                    {"step": "Use series", "work": "e^(-t²) = Σ(-1)ⁿt²ⁿ/n!", "result": "From previous example"},
                    {"step": "Integrate term by term", "work": "∫₀ˣ t²ⁿ dt = x²ⁿ⁺¹/(2n+1)", "result": "Each term integrates"},
                    {"step": "Combine", "work": "∫₀ˣ e^(-t²)dt = Σ(-1)ⁿx²ⁿ⁺¹/[n!(2n+1)]", "result": "Antiderivative series!"},
                    {"step": "Write terms", "work": "= x - x³/3 + x⁵/10 - x⁷/42 + ...", "result": "Series for erf(x) ✓"}
                ],
                "key_insight": "Taylor series let you 'integrate' functions that have no closed-form antiderivative!"
            },
            {
                "title": "Building from scratch: √(1+x)",
                "difficulty": 2,
                "problem": "Find the first 4 terms of the Maclaurin series for √(1+x)",
                "solution": [
                    {"step": "Setup", "work": "f(x) = (1+x)^(1/2), need f(0), f'(0), f''(0), f'''(0)", "result": "Use binomial series"},
                    {"step": "Use binomial", "work": "(1+x)^k = 1 + kx + k(k-1)x²/2! + k(k-1)(k-2)x³/3! + ...", "result": "k = 1/2"},
                    {"step": "Compute", "work": "k=1/2, k(k-1)=1/2·(-1/2)=-1/4, k(k-1)(k-2)=-1/4·(-3/2)=3/8", "result": "Coefficients found"},
                    {"step": "Write series", "work": "√(1+x) = 1 + x/2 - x²/8 + x³/16 - ...", "result": "First 4 terms ✓"},
                    {"step": "Radius", "work": "Binomial series converges for |x| < 1", "result": "R = 1"}
                ],
                "key_insight": "The binomial series (1+x)^k works for ANY k, not just positive integers!"
            }
        ],
        
        "common_mistakes": [
            {
                "mistake": "Using the wrong formula: n! vs (2n)! vs (2n+1)!",
                "example": "Writing sin(x) = Σ(-1)ⁿxⁿ/n! instead of x²ⁿ⁺¹/(2n+1)!",
                "why_wrong": "sin(x) only has ODD powers: x, x³, x⁵, ... with (2n+1)! denominators",
                "correct": "Memorize: sin has odds/(2n+1)!, cos has evens/(2n)!, eˣ has all/n!"
            },
            {
                "mistake": "Forgetting the radius of convergence",
                "example": "Using 1/(1-x) = 1 + x + x² + ... for x = 2",
                "why_wrong": "This series only converges for |x| < 1!",
                "correct": "Always state R. For 1/(1-x), R=1. For eˣ, sin, cos: R=∞."
            },
            {
                "mistake": "Computing derivatives when manipulation would work",
                "example": "Finding derivatives of e^(3x) to build its series",
                "why_wrong": "Just substitute 3x into the known eˣ series: e^(3x) = Σ(3x)ⁿ/n!",
                "correct": "First ask: can I manipulate eˣ, sin, cos, 1/(1-x), or ln(1+x)?"
            }
        ],
        
        "practice_templates": [
            {"template": "Find Maclaurin series for e^({a}x)", "params": {"a": [2, -1, 3]}},
            {"template": "Find Maclaurin series for sin({a}x)", "params": {"a": [2, 3]}},
            {"template": "Find Maclaurin series for x·cos(x)", "params": {}},
            {"template": "Find Maclaurin series for 1/(1+{a}x)", "params": {"a": [1, 2]}},
            {"template": "Find Maclaurin series for ln(1+{a}x)", "params": {"a": [1, 2]}},
            {"template": "Use series to evaluate lim(x→0) (sin x - x)/x³", "params": {}}
        ]
    }
}

# Add polar and parametric sections
DEEP_TEACHING_CONTENT["polar_calculus"] = {
    "name": "Polar Coordinates & Calculus",
    "emoji": "🎯",
    "big_picture": """
Polar coordinates describe points by **distance from origin (r)** and **angle from positive x-axis (θ)**.

Instead of (x, y), we use (r, θ).
- x = r·cos(θ)
- y = r·sin(θ)
- r² = x² + y²
- tan(θ) = y/x

**Why polar?** Some curves are MUCH simpler in polar:
- Circle: r = a (constant!) vs x² + y² = a²
- Spiral: r = θ
- Rose: r = cos(nθ) 
- Cardioid: r = 1 + cos(θ)

**Calculus in Polar:**
- Area: A = ½∫r² dθ
- Arc length: L = ∫√(r² + (dr/dθ)²) dθ
- Slope: dy/dx = (r'sinθ + rcosθ)/(r'cosθ - rsinθ)
    """,
    
    "key_formulas": [
        {"name": "Area", "formula": "A = ½∫ₐᵇ r² dθ", "note": "Between angles α and β"},
        {"name": "Arc Length", "formula": "L = ∫ₐᵇ √(r² + (dr/dθ)²) dθ", "note": ""},
        {"name": "Area Between Curves", "formula": "A = ½∫[r₂² - r₁²] dθ", "note": "Outer minus inner"},
    ],
    
    "common_curves": [
        {"name": "Circle", "equation": "r = a", "description": "Centered at origin, radius a"},
        {"name": "Circle through origin", "equation": "r = a·cos(θ) or a·sin(θ)", "description": "Radius a/2"},
        {"name": "Cardioid", "equation": "r = a(1 + cos θ) or a(1 + sin θ)", "description": "Heart-shaped"},
        {"name": "Limaçon", "equation": "r = a + b·cos(θ)", "description": "Has inner loop if |b| > |a|"},
        {"name": "Rose", "equation": "r = a·cos(nθ)", "description": "n petals if n odd, 2n if n even"},
        {"name": "Lemniscate", "equation": "r² = a²cos(2θ)", "description": "Figure-8 shape"},
    ],
    
    "worked_examples": [
        {
            "title": "Area of a Cardioid",
            "difficulty": 2,
            "problem": "Find the area enclosed by r = 1 + cos(θ)",
            "solution": [
                {"step": "Setup", "work": "A = ½∫₀²π r² dθ = ½∫₀²π (1 + cos θ)² dθ", "result": "Area formula"},
                {"step": "Expand", "work": "(1 + cos θ)² = 1 + 2cos θ + cos²θ", "result": "Use cos²θ = (1+cos2θ)/2"},
                {"step": "Simplify", "work": "= 1 + 2cos θ + ½ + ½cos(2θ) = 3/2 + 2cos θ + ½cos(2θ)", "result": "Ready to integrate"},
                {"step": "Integrate", "work": "½∫₀²π [3/2 + 2cos θ + ½cos(2θ)] dθ", "result": "½[3θ/2 + 2sin θ + ¼sin(2θ)]₀²π"},
                {"step": "Evaluate", "work": "½[(3π) + 0 + 0 - 0] = 3π/2", "result": "A = 3π/2 ✓"}
            ],
            "key_insight": "Always use the identity cos²θ = (1+cos2θ)/2 when squaring trig functions."
        }
    ],
    
    "common_mistakes": [
        {
            "mistake": "Using A = ∫r dθ instead of A = ½∫r² dθ",
            "example": "Area of r = 2: ∫₀²π 2 dθ = 4π instead of ½∫₀²π 4 dθ = 4π... wait, same! Lucky.",
            "why_wrong": "For r = θ: ∫₀²π θ dθ ≠ ½∫₀²π θ² dθ. The ½ and square are critical!",
            "correct": "Always use A = ½∫r² dθ. Think of it as summing tiny pie slices."
        },
        {
            "mistake": "Wrong bounds for symmetric curves",
            "example": "Rose r = cos(2θ): integrating 0 to 2π gives 0!",
            "why_wrong": "Roses have petals that cancel. For area of ONE petal, find where r=0.",
            "correct": "For r = cos(2θ): r=0 when θ = π/4, 3π/4. One petal: θ ∈ [-π/4, π/4]."
        }
    ],
    
    "practice_templates": [
        {"template": "Find area enclosed by r = {a}(1 + cos θ)", "params": {"a": [1, 2]}},
        {"template": "Find area of one petal of r = cos({n}θ)", "params": {"n": [2, 3, 4]}},
        {"template": "Find area inside r = {a} and outside r = {b}cos(θ)", "params": {"a": [2, 3], "b": [2, 4]}}
    ]
}

DEEP_TEACHING_CONTENT["parametric_calculus"] = {
    "name": "Parametric Equations & Calculus",
    "emoji": "🔀",
    "big_picture": """
Parametric equations describe x and y **separately as functions of a third variable t** (usually time).

Instead of y = f(x), we have:
- x = f(t)
- y = g(t)

**Why parametric?** 
- Describe motion: where is the particle at time t?
- Curves that aren't functions: circles, figure-8s, self-intersecting curves
- Natural for physics: position components depend on time

**Calculus in Parametric:**
- Slope: dy/dx = (dy/dt)/(dx/dt)
- Second derivative: d²y/dx² = (d/dt)(dy/dx) / (dx/dt)
- Arc length: L = ∫√((dx/dt)² + (dy/dt)²) dt
- Area: A = ∫y(t) · (dx/dt) dt (careful with direction!)
    """,
    
    "key_formulas": [
        {"name": "Slope", "formula": "dy/dx = (dy/dt)/(dx/dt)", "note": "Chain rule!"},
        {"name": "Second Derivative", "formula": "d²y/dx² = [d/dt(dy/dx)]/(dx/dt)", "note": "NOT d²y/dt² / d²x/dt²!"},
        {"name": "Arc Length", "formula": "L = ∫ₐᵇ √((dx/dt)² + (dy/dt)²) dt", "note": "Speed integrated over time"},
        {"name": "Area", "formula": "A = ∫y dx = ∫y(t) · x'(t) dt", "note": "Watch orientation!"},
    ],
    
    "common_parametrizations": [
        {"curve": "Circle radius a", "equations": "x = a·cos(t), y = a·sin(t)", "parameter": "t ∈ [0, 2π]"},
        {"curve": "Ellipse", "equations": "x = a·cos(t), y = b·sin(t)", "parameter": "t ∈ [0, 2π]"},
        {"curve": "Cycloid", "equations": "x = r(t - sin t), y = r(1 - cos t)", "parameter": "One arch: t ∈ [0, 2π]"},
        {"curve": "Line segment", "equations": "x = x₁ + t(x₂-x₁), y = y₁ + t(y₂-y₁)", "parameter": "t ∈ [0, 1]"},
    ],
    
    "worked_examples": [
        {
            "title": "Arc Length of a Cycloid",
            "difficulty": 2,
            "problem": "Find the arc length of one arch of the cycloid x = t - sin(t), y = 1 - cos(t), t ∈ [0, 2π]",
            "solution": [
                {"step": "Find derivatives", "work": "dx/dt = 1 - cos(t), dy/dt = sin(t)", "result": "Derivatives found"},
                {"step": "Compute speed²", "work": "(dx/dt)² + (dy/dt)² = (1-cos t)² + sin²t", "result": "Expand..."},
                {"step": "Simplify", "work": "= 1 - 2cos t + cos²t + sin²t = 2 - 2cos t = 2(1-cos t)", "result": "Use identity: 1-cos t = 2sin²(t/2)"},
                {"step": "Simplify more", "work": "= 4sin²(t/2), so speed = 2|sin(t/2)| = 2sin(t/2) for t∈[0,2π]", "result": "Speed found"},
                {"step": "Integrate", "work": "L = ∫₀²π 2sin(t/2) dt = [-4cos(t/2)]₀²π = -4(-1) - (-4)(1) = 8", "result": "L = 8 ✓"}
            ],
            "key_insight": "The half-angle identity 1 - cos t = 2sin²(t/2) is crucial for cycloid problems!"
        }
    ],
    
    "common_mistakes": [
        {
            "mistake": "Computing d²y/dx² as (d²y/dt²)/(d²x/dt²)",
            "example": "For x=t², y=t³: d²y/dx² ≠ 6t/2 = 3t",
            "why_wrong": "d²y/dx² requires differentiating dy/dx with respect to t, then dividing by dx/dt",
            "correct": "dy/dx = 3t²/2t = 3t/2. d²y/dx² = (3/2)/(2t) = 3/(4t)"
        }
    ],
    
    "practice_templates": [
        {"template": "Find dy/dx for x = t², y = t³ at t = {a}", "params": {"a": [1, 2]}},
        {"template": "Find arc length of x = cos(t), y = sin(t), t ∈ [0, π]", "params": {}},
        {"template": "Find d²y/dx² for x = e^t, y = e^(2t)", "params": {}}
    ]
}


class DeepTeacher:
    """
    Provides comprehensive teaching content and intelligent problem generation.
    """
    
    def __init__(self):
        self.content = DEEP_TEACHING_CONTENT
    
    def get_topic_overview(self, topic_id: str) -> Optional[Dict]:
        """Get the full teaching content for a topic."""
        if topic_id not in self.content:
            return None
        
        topic = self.content[topic_id]
        return {
            "id": topic_id,
            "name": topic.get("name", topic_id),
            "emoji": topic.get("emoji", "📚"),
            "big_picture": topic.get("big_picture", ""),
            "formulas": topic.get("the_formula", {}),
            "when_to_use": topic.get("when_to_use", []),
            "technique_steps": topic.get("technique_steps", []),
            "worked_examples_count": len(topic.get("worked_examples", [])),
            "common_mistakes_count": len(topic.get("common_mistakes", []))
        }
    
    def get_technique_steps(self, topic_id: str) -> List[Dict]:
        """Get the step-by-step technique for a topic."""
        if topic_id not in self.content:
            return []
        return self.content[topic_id].get("technique_steps", [])
    
    def get_worked_example(self, topic_id: str, difficulty: int = None, index: int = None) -> Optional[Dict]:
        """Get a worked example, optionally filtered by difficulty."""
        if topic_id not in self.content:
            return None
        
        examples = self.content[topic_id].get("worked_examples", [])
        if not examples:
            return None
        
        if difficulty is not None:
            examples = [e for e in examples if e.get("difficulty", 1) == difficulty]
        
        if not examples:
            return None
        
        if index is not None and 0 <= index < len(examples):
            return examples[index]
        
        return random.choice(examples)
    
    def get_all_worked_examples(self, topic_id: str) -> List[Dict]:
        """Get all worked examples for a topic."""
        if topic_id not in self.content:
            return []
        return self.content[topic_id].get("worked_examples", [])
    
    def get_common_mistakes(self, topic_id: str) -> List[Dict]:
        """Get common mistakes for a topic."""
        if topic_id not in self.content:
            return []
        return self.content[topic_id].get("common_mistakes", [])
    
    def get_all_topics(self) -> List[Dict]:
        """Get overview of all available topics."""
        topics = []
        for topic_id, topic_data in self.content.items():
            topics.append({
                "id": topic_id,
                "name": topic_data.get("name", topic_id),
                "emoji": topic_data.get("emoji", "📚"),
                "has_big_picture": bool(topic_data.get("big_picture")),
                "has_technique_steps": bool(topic_data.get("technique_steps")),
                "worked_examples_count": len(topic_data.get("worked_examples", [])),
                "common_mistakes_count": len(topic_data.get("common_mistakes", []))
            })
        return topics
    
    def search_content(self, query: str) -> List[Dict]:
        """Search across all content for a query term."""
        results = []
        query_lower = query.lower()
        
        for topic_id, topic_data in self.content.items():
            relevance = 0
            matches = []
            
            # Check topic name
            if query_lower in topic_data.get("name", "").lower():
                relevance += 10
                matches.append("topic name")
            
            # Check big picture
            if query_lower in topic_data.get("big_picture", "").lower():
                relevance += 5
                matches.append("explanation")
            
            # Check worked examples
            for i, example in enumerate(topic_data.get("worked_examples", [])):
                if query_lower in example.get("problem", "").lower():
                    relevance += 3
                    matches.append(f"example {i+1}")
            
            # Check common mistakes
            for mistake in topic_data.get("common_mistakes", []):
                if query_lower in mistake.get("mistake", "").lower():
                    relevance += 2
                    matches.append("common mistakes")
                    break
            
            if relevance > 0:
                results.append({
                    "topic_id": topic_id,
                    "topic_name": topic_data.get("name", topic_id),
                    "relevance": relevance,
                    "matches": matches
                })
        
        return sorted(results, key=lambda x: x["relevance"], reverse=True)


# Global instance
deep_teacher = DeepTeacher()
