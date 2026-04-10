"""
AI-Powered Calculus Tutor using GitHub Copilot CLI
Uses the local Copilot credentials to provide unlimited personalized tutoring.
Model: gpt-5.4-mini (free tier)
"""

import subprocess
import json
import re
import asyncio
from typing import Optional, Dict, Any, List
import os

# System prompt for the AI tutor
CALC2_TUTOR_SYSTEM = """You are an expert Calculus II tutor helping a student ace their final exam at the University of Utah (MATH 1220). 

Your teaching style:
1. EXPLAIN concepts clearly with intuition, not just formulas
2. SHOW worked examples step-by-step with clear reasoning
3. IDENTIFY common mistakes and how to avoid them
4. CONNECT concepts to help build understanding
5. USE LaTeX for all mathematical expressions (wrap in $ for inline, $$ for display)

Topics you teach (Calc II curriculum):
- Integration techniques: u-substitution, integration by parts, partial fractions, trig integrals, trig substitution
- Improper integrals and convergence
- Sequences and series: convergence tests, power series, Taylor/Maclaurin series
- Parametric equations and polar coordinates
- Applications: arc length, surface area, volumes

When helping with problems:
- Don't just give the answer - TEACH the method
- Ask guiding questions to help the student think
- If they're stuck, give a hint, not the solution
- Explain WHY each step works, not just WHAT to do
- Point out the key insight or pattern recognition needed

Format your responses with clear structure using markdown headers and bullet points."""

class CopilotAITutor:
    """AI Tutor powered by GitHub Copilot CLI"""
    
    def __init__(self, model: str = "gpt-5.4-mini"):
        self.model = model
        self.conversation_history: List[Dict[str, str]] = []
        
    async def ask(self, prompt: str, context: Optional[str] = None) -> str:
        """
        Send a prompt to Copilot CLI and get a response.
        Uses subprocess to call the CLI with the user's local credentials.
        """
        # Build the full prompt with system context
        full_prompt = f"{CALC2_TUTOR_SYSTEM}\n\n"
        
        if context:
            full_prompt += f"Context: {context}\n\n"
        
        # Add conversation history for continuity
        if self.conversation_history:
            full_prompt += "Previous conversation:\n"
            for msg in self.conversation_history[-6:]:  # Last 3 exchanges
                full_prompt += f"{msg['role'].upper()}: {msg['content']}\n"
            full_prompt += "\n"
        
        full_prompt += f"Student: {prompt}\n\nTutor:"
        
        try:
            # Call Copilot CLI via subprocess
            # The CLI uses whatever GitHub auth is configured on the machine
            result = await asyncio.create_subprocess_exec(
                "gh", "copilot", "explain", full_prompt,
                "--model", self.model,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env={**os.environ, "GH_COPILOT_NO_PROMPT": "1"}
            )
            
            stdout, stderr = await result.communicate()
            
            if result.returncode != 0:
                # Fallback: try using the extension's API
                return await self._fallback_generate(prompt, context)
            
            response = stdout.decode('utf-8').strip()
            
            # Update conversation history
            self.conversation_history.append({"role": "user", "content": prompt})
            self.conversation_history.append({"role": "assistant", "content": response})
            
            return response
            
        except Exception as e:
            print(f"Copilot CLI error: {e}")
            return await self._fallback_generate(prompt, context)
    
    async def _fallback_generate(self, prompt: str, context: Optional[str] = None) -> str:
        """Fallback using direct API call if CLI fails"""
        # Use a simpler approach - generate via Python
        return self._generate_response(prompt, context)
    
    def _generate_response(self, prompt: str, context: Optional[str] = None) -> str:
        """
        Generate a helpful response based on the prompt.
        This is a fallback that provides structured help without API calls.
        """
        prompt_lower = prompt.lower()
        
        # Detect what kind of help is needed
        if any(kw in prompt_lower for kw in ["explain", "what is", "how does", "why"]):
            return self._generate_explanation(prompt)
        elif any(kw in prompt_lower for kw in ["solve", "evaluate", "find", "calculate", "integrate"]):
            return self._generate_solution_guide(prompt)
        elif any(kw in prompt_lower for kw in ["practice", "problem", "example"]):
            return self._generate_practice_problem(prompt)
        elif any(kw in prompt_lower for kw in ["stuck", "help", "hint", "don't understand"]):
            return self._generate_hint(prompt, context)
        else:
            return self._generate_general_help(prompt)
    
    def _generate_explanation(self, prompt: str) -> str:
        """Generate a conceptual explanation"""
        topics = {
            "integration by parts": """## Integration by Parts

**The Big Idea:** When you have a product of two functions that's hard to integrate directly, integration by parts lets you "transfer" the derivative from one function to the other.

**The Formula:**
$$\\int u \\, dv = uv - \\int v \\, du$$

**How to Choose u and v (LIATE Rule):**
Choose $u$ in this priority order:
1. **L**ogarithmic functions (ln x, log x)
2. **I**nverse trig functions (arctan, arcsin)
3. **A**lgebraic functions (x, x², polynomials)
4. **T**rigonometric functions (sin, cos, tan)
5. **E**xponential functions (eˣ, 2ˣ)

**Why This Works:**
The formula comes from the product rule in reverse! If $(uv)' = u'v + uv'$, then integrating both sides gives us $uv = \\int u'v + \\int uv'$.

**Key Insight:** Pick $u$ to be something that gets SIMPLER when you differentiate it.

**Example:** $\\int x e^x dx$
- Let $u = x$ (gets simpler: $du = dx$)
- Let $dv = e^x dx$ (easy to integrate: $v = e^x$)
- Result: $xe^x - \\int e^x dx = xe^x - e^x + C = e^x(x-1) + C$""",
            
            "partial fractions": """## Partial Fractions Decomposition

**The Big Idea:** Break a complicated fraction into simpler pieces that are easy to integrate.

**When to Use:** When you have a rational function (polynomial/polynomial) where the degree of numerator < degree of denominator.

**The Method:**
1. **Factor the denominator** completely
2. **Write the decomposition** based on factor types:
   - Linear factor $(x-a)$: $\\frac{A}{x-a}$
   - Repeated linear $(x-a)^n$: $\\frac{A_1}{x-a} + \\frac{A_2}{(x-a)^2} + ... + \\frac{A_n}{(x-a)^n}$
   - Irreducible quadratic $(x^2+bx+c)$: $\\frac{Ax+B}{x^2+bx+c}$
3. **Solve for constants** using strategic x-values or coefficient matching

**Example:** $\\int \\frac{1}{x^2-1} dx$
- Factor: $x^2-1 = (x-1)(x+1)$
- Decompose: $\\frac{1}{(x-1)(x+1)} = \\frac{A}{x-1} + \\frac{B}{x+1}$
- Solve: $A = 1/2$, $B = -1/2$
- Integrate: $\\frac{1}{2}\\ln|x-1| - \\frac{1}{2}\\ln|x+1| + C$""",
            
            "taylor series": """## Taylor and Maclaurin Series

**The Big Idea:** Approximate ANY smooth function as an infinite polynomial!

**Maclaurin Series (centered at 0):**
$$f(x) = \\sum_{n=0}^{\\infty} \\frac{f^{(n)}(0)}{n!} x^n = f(0) + f'(0)x + \\frac{f''(0)}{2!}x^2 + ...$$

**Taylor Series (centered at a):**
$$f(x) = \\sum_{n=0}^{\\infty} \\frac{f^{(n)}(a)}{n!} (x-a)^n$$

**Must-Know Series:**
- $e^x = 1 + x + \\frac{x^2}{2!} + \\frac{x^3}{3!} + ... = \\sum_{n=0}^{\\infty} \\frac{x^n}{n!}$
- $\\sin x = x - \\frac{x^3}{3!} + \\frac{x^5}{5!} - ... = \\sum_{n=0}^{\\infty} \\frac{(-1)^n x^{2n+1}}{(2n+1)!}$
- $\\cos x = 1 - \\frac{x^2}{2!} + \\frac{x^4}{4!} - ... = \\sum_{n=0}^{\\infty} \\frac{(-1)^n x^{2n}}{(2n)!}$
- $\\frac{1}{1-x} = 1 + x + x^2 + x^3 + ... = \\sum_{n=0}^{\\infty} x^n$ (for $|x| < 1$)
- $\\ln(1+x) = x - \\frac{x^2}{2} + \\frac{x^3}{3} - ... = \\sum_{n=1}^{\\infty} \\frac{(-1)^{n+1} x^n}{n}$

**Key Applications:**
- Finding limits (expand and cancel)
- Approximating values
- Integrating "impossible" functions"""
        }
        
        for topic, explanation in topics.items():
            if topic in prompt.lower():
                return explanation
        
        return """I'd be happy to explain that concept! Could you be more specific about which topic you'd like me to cover?

**Calc II Topics I can explain:**
- Integration techniques (by parts, partial fractions, trig sub)
- Improper integrals
- Sequences and series convergence
- Taylor and Maclaurin series
- Polar and parametric calculus

What would you like to learn about?"""

    def _generate_solution_guide(self, prompt: str) -> str:
        """Generate a step-by-step solution guide"""
        return """## Let me help you solve this!

**Step 1: Identify the Problem Type**
First, let's figure out what technique to use. Look for:
- Products of different function types → Integration by Parts
- Rational functions → Partial Fractions
- √(a²-x²), √(a²+x²), √(x²-a²) → Trig Substitution
- Powers of sin/cos → Trig Identities

**Step 2: Set Up**
Write out what you know and what substitutions/setup you'll use.

**Step 3: Execute**
Apply the technique step by step.

**Step 4: Check**
- Does the answer make sense?
- Can you differentiate to verify?

**Share your specific problem and I'll walk you through it!**"""

    def _generate_practice_problem(self, prompt: str) -> str:
        """Generate a practice problem"""
        import random
        
        problems = [
            {
                "problem": "Evaluate: $\\int x^2 \\ln(x) \\, dx$",
                "topic": "Integration by Parts",
                "hint": "Let u = ln(x) since it simplifies when differentiated",
                "difficulty": 2
            },
            {
                "problem": "Evaluate: $\\int \\frac{3x+2}{x^2-4} \\, dx$",
                "topic": "Partial Fractions",
                "hint": "Factor denominator as (x-2)(x+2)",
                "difficulty": 2
            },
            {
                "problem": "Determine if $\\sum_{n=1}^{\\infty} \\frac{n^2}{2^n}$ converges or diverges.",
                "topic": "Series Convergence",
                "hint": "Try the Ratio Test",
                "difficulty": 2
            },
            {
                "problem": "Find the Taylor series for $f(x) = e^{-x^2}$ centered at 0.",
                "topic": "Taylor Series",
                "hint": "Start with the known series for e^u and substitute u = -x²",
                "difficulty": 3
            },
            {
                "problem": "Evaluate: $\\int_0^{\\infty} xe^{-x} \\, dx$",
                "topic": "Improper Integrals",
                "hint": "Use integration by parts, then evaluate the limit",
                "difficulty": 2
            }
        ]
        
        p = random.choice(problems)
        return f"""## Practice Problem

**Topic:** {p['topic']}
**Difficulty:** {'⭐' * p['difficulty']}

### Problem
{p['problem']}

---

**Need a hint?** Ask me and I'll guide you without giving away the answer!

**Ready to check your work?** Share your solution and I'll review it step by step."""

    def _generate_hint(self, prompt: str, context: Optional[str] = None) -> str:
        """Generate a helpful hint"""
        return """## Let me help you get unstuck!

**First, let's identify where you are:**
1. What technique are you using?
2. What step are you on?
3. What's confusing you?

**Common places students get stuck:**

🔸 **Integration by Parts:** Choosing u and dv wrong → Use LIATE rule
🔸 **Partial Fractions:** Setting up decomposition → Match factor types correctly  
🔸 **Series:** Choosing convergence test → Start with Divergence Test, then Ratio/Root for exponentials/factorials
🔸 **Taylor Series:** Finding pattern → Compute first few derivatives, look for pattern

**Share specifically where you're stuck and I'll give you a targeted hint!**"""

    def _generate_general_help(self, prompt: str) -> str:
        """Generate general help"""
        return """## How can I help you today?

I'm your Calc II tutor! I can:

📚 **Explain Concepts**
"Explain integration by parts" or "What is a Taylor series?"

✏️ **Solve Problems Step-by-Step**  
"Help me evaluate ∫x·eˣ dx" or "How do I find if this series converges?"

🎯 **Give Practice Problems**
"Give me a practice problem on partial fractions"

💡 **Provide Hints (without spoiling)**
"I'm stuck on this integral..." 

🔍 **Review Your Work**
Share your solution and I'll check it!

**What would you like to work on?**"""

    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []

    async def generate_problem(self, topic: str, difficulty: int = 2) -> Dict[str, Any]:
        """Generate a new practice problem for a specific topic"""
        
        problem_templates = {
            "integration_by_parts": [
                {"q": "\\int x \\cos(x) \\, dx", "a": "x·sin(x) + cos(x) + C", "d": 1},
                {"q": "\\int x^2 e^x \\, dx", "a": "e^x(x² - 2x + 2) + C", "d": 2},
                {"q": "\\int e^x \\sin(x) \\, dx", "a": "(e^x/2)(sin(x) - cos(x)) + C", "d": 3},
                {"q": "\\int \\ln(x) \\, dx", "a": "x·ln(x) - x + C", "d": 1},
                {"q": "\\int x \\arctan(x) \\, dx", "a": "(x²/2)arctan(x) - x/2 + (1/2)arctan(x) + C", "d": 3},
            ],
            "partial_fractions": [
                {"q": "\\int \\frac{1}{x^2-1} \\, dx", "a": "(1/2)ln|x-1| - (1/2)ln|x+1| + C", "d": 1},
                {"q": "\\int \\frac{2x+3}{x^2+3x+2} \\, dx", "a": "ln|x+1| + ln|x+2| + C", "d": 2},
                {"q": "\\int \\frac{x^2}{(x-1)(x+2)^2} \\, dx", "a": "Decompose and integrate", "d": 3},
            ],
            "series_convergence": [
                {"q": "\\sum_{n=1}^{\\infty} \\frac{1}{n^2}", "a": "Converges (p-series, p=2>1)", "d": 1},
                {"q": "\\sum_{n=1}^{\\infty} \\frac{n!}{n^n}", "a": "Converges (Ratio Test)", "d": 2},
                {"q": "\\sum_{n=2}^{\\infty} \\frac{1}{n \\ln(n)}", "a": "Diverges (Integral Test)", "d": 3},
            ],
            "taylor_series": [
                {"q": "Find Maclaurin series for f(x) = e^{2x}", "a": "∑(2x)^n/n! = ∑2^n·x^n/n!", "d": 1},
                {"q": "Find Taylor series for f(x) = 1/x centered at a=1", "a": "∑(-1)^n(x-1)^n", "d": 2},
                {"q": "Find Maclaurin series for f(x) = x·sin(x)", "a": "∑(-1)^n·x^(2n+2)/(2n+1)!", "d": 2},
            ],
            "improper_integrals": [
                {"q": "\\int_1^{\\infty} \\frac{1}{x^2} \\, dx", "a": "1 (converges)", "d": 1},
                {"q": "\\int_0^{1} \\frac{1}{\\sqrt{x}} \\, dx", "a": "2 (converges)", "d": 1},
                {"q": "\\int_0^{\\infty} x e^{-x^2} \\, dx", "a": "1/2 (converges)", "d": 2},
            ],
        }
        
        import random
        
        if topic in problem_templates:
            # Filter by difficulty
            available = [p for p in problem_templates[topic] if p["d"] <= difficulty + 1 and p["d"] >= difficulty - 1]
            if not available:
                available = problem_templates[topic]
            
            chosen = random.choice(available)
            
            return {
                "question": f"$${chosen['q']}$$",
                "answer": chosen["a"],
                "difficulty": chosen["d"],
                "topic": topic,
                "hints": [
                    "What technique should you use for this type of problem?",
                    "Set up your work carefully before computing.",
                    "Check: can you differentiate your answer to verify?"
                ],
                "walkthrough": self._get_walkthrough(topic, chosen["q"])
            }
        
        return {
            "question": "Practice problem not available for this topic yet.",
            "answer": "N/A",
            "difficulty": 1,
            "topic": topic,
            "hints": [],
            "walkthrough": []
        }
    
    def _get_walkthrough(self, topic: str, problem: str) -> List[str]:
        """Get a step-by-step walkthrough for a problem"""
        walkthroughs = {
            "integration_by_parts": [
                "**Step 1:** Identify this as an Integration by Parts problem (product of two function types)",
                "**Step 2:** Use LIATE to choose u (what simplifies when differentiated) and dv (what's easy to integrate)",
                "**Step 3:** Find du by differentiating u, and v by integrating dv",
                "**Step 4:** Apply the formula: ∫u dv = uv - ∫v du",
                "**Step 5:** Evaluate the remaining integral (may need IBP again!)",
                "**Step 6:** Simplify and add +C"
            ],
            "partial_fractions": [
                "**Step 1:** Check that degree of numerator < degree of denominator (if not, do polynomial division first)",
                "**Step 2:** Factor the denominator completely",
                "**Step 3:** Set up partial fraction decomposition based on factor types",
                "**Step 4:** Multiply both sides by the denominator to clear fractions",
                "**Step 5:** Solve for constants using strategic x-values or coefficient matching",
                "**Step 6:** Integrate each simple fraction separately"
            ],
            "series_convergence": [
                "**Step 1:** Check Divergence Test first - if lim(aₙ) ≠ 0, series diverges",
                "**Step 2:** Look at the form: factorials/exponentials → Ratio Test, nth powers → Root Test",
                "**Step 3:** For 1/nᵖ forms, use p-series test (converges if p > 1)",
                "**Step 4:** Apply chosen test and evaluate the limit",
                "**Step 5:** Conclude convergence or divergence based on test result"
            ],
            "taylor_series": [
                "**Step 1:** Identify center point a (usually 0 for Maclaurin)",
                "**Step 2:** Compute derivatives f(a), f'(a), f''(a), f'''(a), ...",
                "**Step 3:** Look for a pattern in the derivatives",
                "**Step 4:** Write the series: Σ f⁽ⁿ⁾(a)/n! · (x-a)ⁿ",
                "**Step 5:** Determine radius of convergence using Ratio Test"
            ],
            "improper_integrals": [
                "**Step 1:** Identify the type: infinite limit or discontinuous integrand",
                "**Step 2:** Replace problematic bound with a limit variable (t→∞ or t→0⁺)",
                "**Step 3:** Evaluate the definite integral with the limit variable",
                "**Step 4:** Take the limit",
                "**Step 5:** If limit exists and is finite → converges; otherwise → diverges"
            ]
        }
        
        return walkthroughs.get(topic, [
            "Identify the problem type",
            "Set up using appropriate technique",
            "Execute step by step",
            "Verify your answer"
        ])

    async def explain_mistake(self, problem: str, user_answer: str, correct_answer: str) -> str:
        """Explain why an answer is wrong and guide toward the correct approach"""
        return f"""## Let's Review Your Answer

**Your answer:** {user_answer}
**Expected:** {correct_answer}

### Common Mistakes to Check:

1. **Sign errors** - Did you track all negative signs correctly?
2. **Algebra errors** - Double-check your simplification
3. **Setup errors** - Did you choose the right technique/substitution?
4. **Forgetting +C** - Don't forget the constant of integration!
5. **Limits of integration** - For definite integrals, did you evaluate correctly?

### Let's trace through the solution:

Would you like me to:
- **Walk through the complete solution** step-by-step?
- **Show where your approach diverged** from the correct path?
- **Explain the concept** behind this problem type?

Just ask and I'll help you understand!"""


# Singleton instance
_tutor_instance: Optional[CopilotAITutor] = None

def get_ai_tutor() -> CopilotAITutor:
    """Get or create the AI tutor singleton"""
    global _tutor_instance
    if _tutor_instance is None:
        _tutor_instance = CopilotAITutor(model="gpt-5.4-mini")
    return _tutor_instance
