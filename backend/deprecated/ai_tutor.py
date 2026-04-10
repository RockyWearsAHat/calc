"""
AI-Powered Calculus II Tutor using GitHub Copilot CLI
Uses GPT-5 mini (free) for unlimited tutoring
"""

import subprocess
import json
import re
import asyncio
from typing import Optional, Dict, Any, List
import random

class AITutor:
    """
    AI Tutor that leverages GitHub Copilot CLI for:
    - Generating unlimited practice problems
    - Providing personalized explanations
    - Creating step-by-step walkthroughs
    - Analyzing mistakes and giving targeted feedback
    """
    
    CALC2_TOPICS = {
        "integration_by_parts": {
            "name": "Integration by Parts",
            "formula": "∫u·dv = u·v - ∫v·du",
            "key_concepts": [
                "LIATE rule for choosing u (Logs, Inverse trig, Algebraic, Trig, Exponential)",
                "Tabular method for repeated integration by parts",
                "Recognizing when IBP loops back (∫eˣsin(x)dx)"
            ],
            "common_types": [
                "∫x·eˣdx", "∫x·sin(x)dx", "∫x·ln(x)dx", "∫ln(x)dx", 
                "∫x²·eˣdx", "∫eˣ·cos(x)dx", "∫arctan(x)dx"
            ]
        },
        "partial_fractions": {
            "name": "Partial Fractions",
            "formula": "Decompose P(x)/Q(x) into simpler fractions",
            "key_concepts": [
                "Factor denominator completely",
                "Linear factors → A/(x-a)",
                "Repeated linear → A/(x-a) + B/(x-a)²",
                "Irreducible quadratic → (Ax+B)/(x²+bx+c)"
            ],
            "common_types": [
                "1/((x-1)(x+2))", "x/((x-1)²(x+1))", 
                "(x+1)/(x²+1)", "1/(x³-x)"
            ]
        },
        "improper_integrals": {
            "name": "Improper Integrals",
            "formula": "∫[a,∞) f(x)dx = lim[b→∞] ∫[a,b] f(x)dx",
            "key_concepts": [
                "Type 1: Infinite limits of integration",
                "Type 2: Discontinuous integrand",
                "Comparison test for convergence",
                "p-integral: ∫1/xᵖ converges if p>1"
            ],
            "common_types": [
                "∫[1,∞) 1/x² dx", "∫[0,∞) e⁻ˣ dx",
                "∫[0,1] 1/√x dx", "∫[-∞,∞) 1/(1+x²) dx"
            ]
        },
        "sequences_series": {
            "name": "Sequences and Series",
            "formula": "Σaₙ converges if limₙ→∞ Sₙ exists",
            "key_concepts": [
                "Divergence test (if lim aₙ ≠ 0, diverges)",
                "Geometric series: Σarⁿ = a/(1-r) if |r|<1",
                "p-series: Σ1/nᵖ converges if p>1",
                "Comparison, ratio, root tests"
            ],
            "common_types": [
                "Σ1/n²", "Σ(1/2)ⁿ", "Σn/2ⁿ", "Σ1/(n·ln(n))"
            ]
        },
        "taylor_series": {
            "name": "Taylor & Maclaurin Series",
            "formula": "f(x) = Σ f⁽ⁿ⁾(a)/n! · (x-a)ⁿ",
            "key_concepts": [
                "Maclaurin = Taylor at a=0",
                "Key series: eˣ, sin(x), cos(x), 1/(1-x), ln(1+x)",
                "Radius and interval of convergence",
                "Taylor polynomial approximations"
            ],
            "common_types": [
                "eˣ = Σxⁿ/n!", "sin(x) = Σ(-1)ⁿx²ⁿ⁺¹/(2n+1)!",
                "1/(1-x) = Σxⁿ", "ln(1+x) = Σ(-1)ⁿ⁺¹xⁿ/n"
            ]
        },
        "polar_coordinates": {
            "name": "Polar Coordinates & Calculus",
            "formula": "Area = ½∫[α,β] r² dθ",
            "key_concepts": [
                "x = r·cos(θ), y = r·sin(θ)",
                "Common curves: cardioids, roses, limaçons",
                "Arc length in polar",
                "Converting between rectangular and polar"
            ],
            "common_types": [
                "r = 1 + cos(θ)", "r = sin(2θ)", "r = 2cos(θ)", "r = θ"
            ]
        },
        "parametric_equations": {
            "name": "Parametric Equations",
            "formula": "dy/dx = (dy/dt)/(dx/dt)",
            "key_concepts": [
                "Eliminating the parameter",
                "Arc length: ∫√((dx/dt)² + (dy/dt)²) dt",
                "Surface area of revolution",
                "Second derivative: d²y/dx²"
            ],
            "common_types": [
                "x=cos(t), y=sin(t)", "x=t², y=t³",
                "x=a·cos(t), y=b·sin(t)", "cycloid"
            ]
        }
    }
    
    def __init__(self):
        self.conversation_history = []
        self.student_profile = {
            "strengths": [],
            "weaknesses": [],
            "recent_mistakes": [],
            "mastery_levels": {topic: 0.0 for topic in self.CALC2_TOPICS}
        }
    
    async def call_copilot(self, prompt: str, context: str = "") -> str:
        """Call GitHub Copilot CLI with a prompt"""
        full_prompt = f"""You are an expert Calculus II tutor. Be precise, clear, and educational.
Use proper mathematical notation. Format math expressions clearly.

{context}

{prompt}"""
        
        try:
            # Use copilot CLI in non-interactive mode
            process = await asyncio.create_subprocess_exec(
                "copilot",
                "-t", full_prompt,  # -t for text/prompt mode
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await asyncio.wait_for(
                process.communicate(), 
                timeout=60
            )
            
            if process.returncode == 0:
                return stdout.decode('utf-8').strip()
            else:
                # Fallback: try gh copilot
                return await self._fallback_copilot(full_prompt)
                
        except asyncio.TimeoutError:
            return await self._fallback_copilot(full_prompt)
        except Exception as e:
            return await self._fallback_copilot(full_prompt)
    
    async def _fallback_copilot(self, prompt: str) -> str:
        """Fallback using gh copilot explain"""
        try:
            # Try using subprocess with shell
            result = subprocess.run(
                f'echo "{prompt}" | copilot -t -',
                shell=True,
                capture_output=True,
                text=True,
                timeout=60
            )
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
        except:
            pass
        
        # Final fallback: use built-in knowledge
        return self._builtin_response(prompt)
    
    def _builtin_response(self, prompt: str) -> str:
        """Built-in responses when Copilot is unavailable"""
        prompt_lower = prompt.lower()
        
        if "integration by parts" in prompt_lower:
            return """Integration by Parts Formula: ∫u·dv = u·v - ∫v·du

**LIATE Rule for choosing u** (in order of priority):
- **L**ogarithmic functions (ln x, log x)
- **I**nverse trig functions (arctan x, arcsin x)
- **A**lgebraic functions (x², x, polynomials)
- **T**rigonometric functions (sin x, cos x)
- **E**xponential functions (eˣ, 2ˣ)

Choose u from the earliest category that appears in your integrand.
Whatever's left becomes dv.

**Example:** ∫x·eˣ dx
- u = x (Algebraic) → du = dx
- dv = eˣdx → v = eˣ
- Answer: x·eˣ - ∫eˣdx = x·eˣ - eˣ + C = eˣ(x-1) + C"""
        
        elif "partial fraction" in prompt_lower:
            return """Partial Fractions Decomposition:

**Step 1:** Factor the denominator completely

**Step 2:** Set up the decomposition based on factor types:
- Linear factor (x-a): A/(x-a)
- Repeated linear (x-a)²: A/(x-a) + B/(x-a)²
- Irreducible quadratic (x²+bx+c): (Ax+B)/(x²+bx+c)

**Step 3:** Multiply both sides by the denominator
**Step 4:** Solve for A, B, C... by:
- Substituting convenient x values, OR
- Comparing coefficients

**Example:** 1/((x-1)(x+2))
= A/(x-1) + B/(x+2)
Multiply: 1 = A(x+2) + B(x-1)
x=1: 1 = 3A → A = 1/3
x=-2: 1 = -3B → B = -1/3"""
        
        elif "taylor" in prompt_lower or "maclaurin" in prompt_lower:
            return """Taylor Series: f(x) = Σ f⁽ⁿ⁾(a)/n! · (x-a)ⁿ

**Key Maclaurin Series (memorize these!):**
- eˣ = 1 + x + x²/2! + x³/3! + ... = Σxⁿ/n!
- sin(x) = x - x³/3! + x⁵/5! - ... = Σ(-1)ⁿx²ⁿ⁺¹/(2n+1)!
- cos(x) = 1 - x²/2! + x⁴/4! - ... = Σ(-1)ⁿx²ⁿ/(2n)!
- 1/(1-x) = 1 + x + x² + x³ + ... = Σxⁿ (|x|<1)
- ln(1+x) = x - x²/2 + x³/3 - ... = Σ(-1)ⁿ⁺¹xⁿ/n (|x|≤1)

**Finding Taylor Series:**
1. Compute derivatives f(a), f'(a), f''(a), ...
2. Plug into formula: f(a) + f'(a)(x-a) + f''(a)(x-a)²/2! + ..."""
        
        elif "series" in prompt_lower and "test" in prompt_lower:
            return """Series Convergence Tests (in order to try):

**1. Divergence Test:** If lim aₙ ≠ 0, series DIVERGES
   (If lim = 0, test is inconclusive!)

**2. Geometric Series:** Σarⁿ converges to a/(1-r) if |r|<1

**3. p-Series:** Σ1/nᵖ converges if p>1, diverges if p≤1

**4. Comparison Test:** Compare to known series
   - If aₙ ≤ bₙ and Σbₙ converges → Σaₙ converges
   - If aₙ ≥ bₙ and Σbₙ diverges → Σaₙ diverges

**5. Ratio Test:** L = lim |aₙ₊₁/aₙ|
   - L < 1 → converges
   - L > 1 → diverges
   - L = 1 → inconclusive

**6. Root Test:** L = lim ⁿ√|aₙ|
   (Same rules as ratio test)

**7. Alternating Series:** Σ(-1)ⁿbₙ converges if bₙ→0 and bₙ is decreasing"""
        
        elif "polar" in prompt_lower:
            return """Polar Coordinates:

**Conversion:**
- x = r·cos(θ), y = r·sin(θ)
- r² = x² + y², tan(θ) = y/x

**Area in Polar:** A = ½∫[α,β] r² dθ

**Arc Length:** L = ∫[α,β] √(r² + (dr/dθ)²) dθ

**Common Polar Curves:**
- Circle: r = a (centered at origin) or r = 2a·cos(θ) (through origin)
- Cardioid: r = a(1 + cos(θ))
- Rose: r = a·cos(nθ) - n petals if odd, 2n if even
- Limaçon: r = a + b·cos(θ)
- Spiral: r = aθ"""
        
        elif "parametric" in prompt_lower:
            return """Parametric Equations:

**First Derivative:** dy/dx = (dy/dt)/(dx/dt)

**Second Derivative:** d²y/dx² = (d/dt)(dy/dx) / (dx/dt)

**Arc Length:** L = ∫[a,b] √((dx/dt)² + (dy/dt)²) dt

**Surface Area (revolution around x-axis):**
S = 2π∫y·√((dx/dt)² + (dy/dt)²) dt

**Common Parametric Curves:**
- Circle: x = r·cos(t), y = r·sin(t)
- Ellipse: x = a·cos(t), y = b·sin(t)
- Cycloid: x = a(t - sin(t)), y = a(1 - cos(t))"""
        
        else:
            return "I can help you with this! Please be more specific about which Calc II topic you need help with: Integration by Parts, Partial Fractions, Improper Integrals, Series, Taylor Series, Polar Coordinates, or Parametric Equations."
    
    async def generate_problem(self, topic: str, difficulty: int = 1, 
                               avoid_types: List[str] = None) -> Dict[str, Any]:
        """Generate a new practice problem using AI"""
        topic_info = self.CALC2_TOPICS.get(topic, {})
        
        difficulty_desc = {
            1: "basic, straightforward application of the formula",
            2: "intermediate, requires multiple steps or combining concepts",
            3: "advanced, challenging problem that tests deep understanding"
        }
        
        prompt = f"""Generate a {difficulty_desc.get(difficulty, 'intermediate')} {topic_info.get('name', topic)} problem for Calculus II.

Topic: {topic_info.get('name', topic)}
Key Formula: {topic_info.get('formula', '')}

Return ONLY a JSON object with this exact structure:
{{
    "question": "the problem statement with proper math notation",
    "answer": "the final answer",
    "solution_steps": ["step 1", "step 2", ...],
    "key_insight": "the main concept being tested",
    "common_mistake": "a mistake students often make on this type"
}}"""
        
        try:
            response = await self.call_copilot(prompt)
            # Try to parse JSON from response
            json_match = re.search(r'\{[\s\S]*\}', response)
            if json_match:
                problem = json.loads(json_match.group())
                problem['topic'] = topic
                problem['difficulty'] = difficulty
                return problem
        except:
            pass
        
        # Fallback: use predefined problems
        return self._generate_fallback_problem(topic, difficulty)
    
    def _generate_fallback_problem(self, topic: str, difficulty: int) -> Dict[str, Any]:
        """Generate problem from predefined templates"""
        problems = {
            "integration_by_parts": [
                {
                    "question": "Evaluate: ∫x·cos(x) dx",
                    "answer": "x·sin(x) + cos(x) + C",
                    "solution_steps": [
                        "Use LIATE: u = x (Algebraic), dv = cos(x)dx",
                        "Then du = dx, v = sin(x)",
                        "Apply formula: ∫u·dv = u·v - ∫v·du",
                        "= x·sin(x) - ∫sin(x)dx",
                        "= x·sin(x) - (-cos(x)) + C",
                        "= x·sin(x) + cos(x) + C"
                    ],
                    "key_insight": "LIATE rule helps choose u: Algebraic before Trigonometric",
                    "common_mistake": "Forgetting the negative sign when integrating sin(x)"
                },
                {
                    "question": "Evaluate: ∫x²·eˣ dx",
                    "answer": "eˣ(x² - 2x + 2) + C",
                    "solution_steps": [
                        "Need IBP twice (or use tabular method)",
                        "First: u = x², dv = eˣdx → x²eˣ - 2∫xeˣdx",
                        "Second: u = x, dv = eˣdx → xeˣ - eˣ",
                        "Combine: x²eˣ - 2(xeˣ - eˣ) + C",
                        "= x²eˣ - 2xeˣ + 2eˣ + C",
                        "= eˣ(x² - 2x + 2) + C"
                    ],
                    "key_insight": "Tabular method is faster for polynomial × exponential",
                    "common_mistake": "Losing track of signs in repeated IBP"
                },
                {
                    "question": "Evaluate: ∫ln(x) dx",
                    "answer": "x·ln(x) - x + C",
                    "solution_steps": [
                        "Use IBP with u = ln(x), dv = dx",
                        "Then du = (1/x)dx, v = x",
                        "∫ln(x)dx = x·ln(x) - ∫x·(1/x)dx",
                        "= x·ln(x) - ∫1 dx",
                        "= x·ln(x) - x + C"
                    ],
                    "key_insight": "For ∫ln(x)dx, let dv = dx (the '1')",
                    "common_mistake": "Not realizing you can use IBP when there's 'no dv'"
                }
            ],
            "partial_fractions": [
                {
                    "question": "Evaluate: ∫ 1/((x-1)(x+1)) dx",
                    "answer": "½·ln|x-1| - ½·ln|x+1| + C = ½·ln|(x-1)/(x+1)| + C",
                    "solution_steps": [
                        "Set up: 1/((x-1)(x+1)) = A/(x-1) + B/(x+1)",
                        "Multiply both sides by (x-1)(x+1):",
                        "1 = A(x+1) + B(x-1)",
                        "Let x = 1: 1 = 2A → A = 1/2",
                        "Let x = -1: 1 = -2B → B = -1/2",
                        "∫[1/2·1/(x-1) - 1/2·1/(x+1)]dx",
                        "= ½·ln|x-1| - ½·ln|x+1| + C"
                    ],
                    "key_insight": "Substituting roots eliminates terms quickly",
                    "common_mistake": "Forgetting absolute values in ln"
                },
                {
                    "question": "Evaluate: ∫ x/((x-1)²) dx",
                    "answer": "ln|x-1| - 1/(x-1) + C",
                    "solution_steps": [
                        "Repeated linear factor: x/((x-1)²) = A/(x-1) + B/(x-1)²",
                        "Multiply by (x-1)²: x = A(x-1) + B",
                        "Let x = 1: 1 = B",
                        "Compare x coefficients: 1 = A",
                        "∫[1/(x-1) + 1/(x-1)²]dx",
                        "= ln|x-1| - 1/(x-1) + C"
                    ],
                    "key_insight": "Repeated factors need multiple terms with increasing powers",
                    "common_mistake": "Only including one term for repeated factors"
                }
            ],
            "sequences_series": [
                {
                    "question": "Determine if the series converges: Σ(n=1 to ∞) n/(2ⁿ)",
                    "answer": "Converges (to 2)",
                    "solution_steps": [
                        "Use Ratio Test: L = lim |aₙ₊₁/aₙ|",
                        "aₙ = n/2ⁿ, aₙ₊₁ = (n+1)/2ⁿ⁺¹",
                        "L = lim [(n+1)/2ⁿ⁺¹] · [2ⁿ/n]",
                        "= lim (n+1)/(2n) = 1/2",
                        "Since L = 1/2 < 1, series CONVERGES"
                    ],
                    "key_insight": "Ratio test is ideal when terms have factorials or exponentials",
                    "common_mistake": "Forgetting to take the limit after simplifying"
                },
                {
                    "question": "Does Σ(n=1 to ∞) 1/(n·ln(n)) converge or diverge? (for n ≥ 2)",
                    "answer": "Diverges",
                    "solution_steps": [
                        "Use Integral Test (positive, decreasing, continuous)",
                        "∫[2,∞) 1/(x·ln(x)) dx",
                        "Let u = ln(x), du = (1/x)dx",
                        "= ∫[ln2,∞) 1/u du = [ln(u)]|[ln2,∞)",
                        "= ln(ln(x))|[2,∞) = ∞",
                        "Integral diverges, so series DIVERGES"
                    ],
                    "key_insight": "Integral test connects series to improper integrals",
                    "common_mistake": "Trying ratio test (gives L=1, inconclusive)"
                }
            ],
            "taylor_series": [
                {
                    "question": "Find the Maclaurin series for f(x) = eˣ·sin(x) up to x³ terms",
                    "answer": "x + x² + x³/3 + ...",
                    "solution_steps": [
                        "Use known series: eˣ = 1 + x + x²/2 + x³/6 + ...",
                        "sin(x) = x - x³/6 + ...",
                        "Multiply and collect terms:",
                        "(1 + x + x²/2 + x³/6)(x - x³/6)",
                        "= x + x² + x³/2 - x³/6 + ...",
                        "= x + x² + x³(3/6 - 1/6) + ...",
                        "= x + x² + x³/3 + ..."
                    ],
                    "key_insight": "Multiply known series and collect like terms",
                    "common_mistake": "Including terms beyond the requested degree"
                },
                {
                    "question": "Find the Taylor series of ln(x) centered at a = 1",
                    "answer": "(x-1) - (x-1)²/2 + (x-1)³/3 - ... = Σ(-1)ⁿ⁺¹(x-1)ⁿ/n",
                    "solution_steps": [
                        "f(x) = ln(x), need derivatives at x = 1",
                        "f(1) = ln(1) = 0",
                        "f'(x) = 1/x → f'(1) = 1",
                        "f''(x) = -1/x² → f''(1) = -1",
                        "f'''(x) = 2/x³ → f'''(1) = 2",
                        "Pattern: fⁿ(1) = (-1)ⁿ⁺¹(n-1)!",
                        "Series: Σ(-1)ⁿ⁺¹(x-1)ⁿ/n for n ≥ 1"
                    ],
                    "key_insight": "Recognize the pattern in derivatives to find general term",
                    "common_mistake": "Wrong signs from the factorial pattern"
                }
            ],
            "polar_coordinates": [
                {
                    "question": "Find the area enclosed by r = 2cos(θ)",
                    "answer": "π",
                    "solution_steps": [
                        "r = 2cos(θ) is a circle through origin",
                        "Curve traces from θ = -π/2 to θ = π/2",
                        "Area = ½∫r² dθ = ½∫[-π/2,π/2] 4cos²(θ) dθ",
                        "= 2∫[-π/2,π/2] cos²(θ) dθ",
                        "Use: cos²θ = (1 + cos(2θ))/2",
                        "= 2 · ½∫[-π/2,π/2] (1 + cos(2θ)) dθ",
                        "= [θ + sin(2θ)/2]|[-π/2,π/2] = π"
                    ],
                    "key_insight": "Know your trig identities! cos²θ = (1+cos2θ)/2",
                    "common_mistake": "Wrong limits - this circle only needs -π/2 to π/2"
                }
            ],
            "parametric_equations": [
                {
                    "question": "Find dy/dx for x = t² - 1, y = t³ at t = 2",
                    "answer": "3",
                    "solution_steps": [
                        "dy/dx = (dy/dt)/(dx/dt)",
                        "dx/dt = 2t",
                        "dy/dt = 3t²",
                        "dy/dx = 3t²/(2t) = 3t/2",
                        "At t = 2: dy/dx = 3(2)/2 = 3"
                    ],
                    "key_insight": "Chain rule: dy/dx = (dy/dt)·(dt/dx) = (dy/dt)/(dx/dt)",
                    "common_mistake": "Dividing in wrong order"
                },
                {
                    "question": "Find the arc length of x = cos(t), y = sin(t) for 0 ≤ t ≤ 2π",
                    "answer": "2π",
                    "solution_steps": [
                        "Arc length: L = ∫√((dx/dt)² + (dy/dt)²) dt",
                        "dx/dt = -sin(t), dy/dt = cos(t)",
                        "(dx/dt)² + (dy/dt)² = sin²(t) + cos²(t) = 1",
                        "L = ∫[0,2π] √1 dt = ∫[0,2π] 1 dt",
                        "= t|[0,2π] = 2π",
                        "This is the circumference of unit circle!"
                    ],
                    "key_insight": "Unit circle parametrization gives √(sin²+cos²) = 1",
                    "common_mistake": "Forgetting to take square root"
                }
            ],
            "improper_integrals": [
                {
                    "question": "Evaluate: ∫[1,∞) 1/x² dx",
                    "answer": "1 (converges)",
                    "solution_steps": [
                        "Replace ∞ with limit: lim[b→∞] ∫[1,b] x⁻² dx",
                        "Antiderivative: -x⁻¹ = -1/x",
                        "= lim[b→∞] [-1/x]|[1,b]",
                        "= lim[b→∞] (-1/b - (-1/1))",
                        "= lim[b→∞] (-1/b + 1)",
                        "= 0 + 1 = 1"
                    ],
                    "key_insight": "p-integral ∫1/xᵖ converges for p > 1",
                    "common_mistake": "Forgetting to use limits for improper integrals"
                }
            ]
        }
        
        topic_problems = problems.get(topic, problems["integration_by_parts"])
        # Filter by difficulty (use index as proxy)
        idx = min(difficulty - 1, len(topic_problems) - 1)
        problem = topic_problems[idx].copy()
        problem['topic'] = topic
        problem['difficulty'] = difficulty
        return problem
    
    async def explain_concept(self, topic: str, specific_question: str = None) -> str:
        """Get a detailed explanation of a concept"""
        topic_info = self.CALC2_TOPICS.get(topic, {})
        
        if specific_question:
            prompt = f"""Explain this Calculus II concept in detail:
Topic: {topic_info.get('name', topic)}
Student's question: {specific_question}

Provide:
1. Clear explanation of the underlying concept
2. The key formula(s) and when to use them
3. A worked example with step-by-step solution
4. Common pitfalls to avoid
5. How to recognize when to use this technique"""
        else:
            prompt = f"""Give a comprehensive lesson on {topic_info.get('name', topic)} for Calculus II.

Cover:
1. What is this technique and why do we need it?
2. The main formula: {topic_info.get('formula', '')}
3. Step-by-step method to apply it
4. 2-3 worked examples from simple to complex
5. Tips for recognizing when to use this technique
6. Common mistakes and how to avoid them"""
        
        response = await self.call_copilot(prompt)
        
        # If we got a good response, return it
        if len(response) > 100:
            return response
        
        # Otherwise use built-in
        return self._builtin_response(topic)
    
    async def analyze_mistake(self, problem: Dict, user_answer: str, 
                             correct_answer: str) -> Dict[str, str]:
        """Analyze why an answer is wrong and provide targeted help"""
        prompt = f"""A student got this Calculus II problem wrong. Analyze their mistake.

Problem: {problem.get('question', '')}
Student's answer: {user_answer}
Correct answer: {correct_answer}
Topic: {problem.get('topic', '')}

Provide:
1. What specific error did the student likely make?
2. A clear explanation of why their answer is wrong
3. How to get the correct answer (key steps)
4. A similar practice problem they should try
5. The concept they need to review

Be encouraging but direct."""
        
        response = await self.call_copilot(prompt)
        
        return {
            "analysis": response,
            "topic": problem.get('topic', ''),
            "needs_review": True
        }
    
    async def get_hint(self, problem: Dict, hint_level: int) -> str:
        """Get a progressive hint for a problem"""
        hints = [
            "What technique should you use? Look at the form of the expression.",
            "What's the first step of the method?",
            "Here's how to set it up...",
            "Here's the key calculation...",
            "Here's the full solution path..."
        ]
        
        if 'solution_steps' in problem and hint_level <= len(problem['solution_steps']):
            return problem['solution_steps'][hint_level - 1]
        
        prompt = f"""Give hint #{hint_level} (out of 5) for this Calculus II problem:
{problem.get('question', '')}

Topic: {problem.get('topic', '')}
Hint level {hint_level} should be: {hints[min(hint_level-1, 4)]}

Just give the hint, nothing else. Be concise but helpful."""
        
        return await self.call_copilot(prompt)
    
    async def generate_similar_problem(self, original_problem: Dict) -> Dict[str, Any]:
        """Generate a similar problem for more practice"""
        prompt = f"""Generate a similar Calculus II problem to this one:
{original_problem.get('question', '')}

Keep the same topic ({original_problem.get('topic', '')}) and difficulty level.
Change the numbers/functions but test the same concept.

Return ONLY JSON:
{{
    "question": "new problem",
    "answer": "correct answer",
    "solution_steps": ["step 1", "step 2", ...],
    "key_insight": "what this tests"
}}"""
        
        try:
            response = await self.call_copilot(prompt)
            json_match = re.search(r'\{[\s\S]*\}', response)
            if json_match:
                problem = json.loads(json_match.group())
                problem['topic'] = original_problem.get('topic', '')
                problem['difficulty'] = original_problem.get('difficulty', 1)
                return problem
        except:
            pass
        
        # Fallback
        return self._generate_fallback_problem(
            original_problem.get('topic', 'integration_by_parts'),
            original_problem.get('difficulty', 1)
        )
    
    async def get_study_plan(self, mastery_data: Dict) -> Dict[str, Any]:
        """Generate a personalized study plan based on mastery levels"""
        weak_topics = [t for t, m in mastery_data.items() if m < 0.5]
        strong_topics = [t for t, m in mastery_data.items() if m >= 0.8]
        
        prompt = f"""Create a study plan for a Calculus II final exam.

Student's mastery levels:
{json.dumps(mastery_data, indent=2)}

Weak areas needing focus: {weak_topics}
Strong areas: {strong_topics}

Create a structured study plan with:
1. Priority order of topics to study
2. Time allocation suggestions
3. Specific things to practice for each weak area
4. Tips for maintaining strong areas
5. Exam strategy suggestions"""
        
        response = await self.call_copilot(prompt)
        
        return {
            "plan": response,
            "priority_topics": weak_topics,
            "review_topics": strong_topics,
            "mastery_data": mastery_data
        }


# Create singleton instance
ai_tutor = AITutor()
