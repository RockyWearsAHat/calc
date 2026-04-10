"""
Copilot-Powered Calculus II Tutor
Uses GitHub Copilot CLI (GPT-5-mini) to generate unlimited, personalized tutoring content.
This runs locally using whatever Copilot authentication is on the machine.
"""

import subprocess
import json
import asyncio
import re
from typing import Optional, Dict, List, Any
from dataclasses import dataclass, asdict
import hashlib
import os
from pathlib import Path

# Cache directory for generated content
CACHE_DIR = Path(__file__).parent / "data" / "ai_cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

@dataclass
class GeneratedProblem:
    question: str
    answer: str
    hints: List[str]
    walkthrough: List[Dict[str, str]]
    key_concept: str
    difficulty: int
    topic: str
    explanation: str  # Why this answer is correct

@dataclass
class ConceptExplanation:
    topic: str
    title: str
    intuition: str  # Plain English explanation
    formal_definition: str
    key_formulas: List[str]
    worked_examples: List[Dict[str, str]]
    common_mistakes: List[str]
    when_to_use: str
    practice_recognition: List[str]  # How to recognize when to use this technique

# Calculus II Topics with context for the AI
CALC2_TOPICS = {
    "integration_by_parts": {
        "name": "Integration by Parts",
        "description": "Used when integrand is a product of two functions. Formula: ∫u·dv = u·v - ∫v·du",
        "typical_forms": ["∫x·eˣ dx", "∫x·sin(x) dx", "∫ln(x) dx", "∫x²·eˣ dx", "∫eˣ·cos(x) dx"],
        "key_insight": "Choose u to be the function that simplifies when differentiated (LIATE rule: Logs, Inverse trig, Algebraic, Trig, Exponential)",
    },
    "partial_fractions": {
        "name": "Partial Fractions",
        "description": "Decompose rational functions into simpler fractions for integration",
        "typical_forms": ["∫1/(x²-1) dx", "∫(2x+3)/(x²+x-2) dx", "∫1/(x²+1)² dx"],
        "key_insight": "Factor denominator, set up A/(x-a) + B/(x-b) form, solve for constants",
    },
    "improper_integrals": {
        "name": "Improper Integrals",
        "description": "Integrals with infinite limits or discontinuous integrands",
        "typical_forms": ["∫₁^∞ 1/x² dx", "∫₀^1 1/√x dx", "∫₋∞^∞ e⁻ˣ² dx"],
        "key_insight": "Replace infinity with limit variable, evaluate limit. Converges if limit exists and is finite.",
    },
    "sequences_series": {
        "name": "Sequences and Series",
        "description": "Infinite sums, convergence tests, and series manipulation",
        "typical_forms": ["Σ 1/n²", "Σ (-1)ⁿ/n", "Σ n/2ⁿ", "geometric series", "p-series"],
        "key_insight": "Use convergence tests: ratio, root, comparison, integral, alternating series tests",
    },
    "taylor_series": {
        "name": "Taylor and Maclaurin Series",
        "description": "Represent functions as infinite polynomials centered at a point",
        "typical_forms": ["eˣ = Σ xⁿ/n!", "sin(x) = Σ (-1)ⁿx²ⁿ⁺¹/(2n+1)!", "1/(1-x) = Σ xⁿ"],
        "key_insight": "f(x) = Σ f⁽ⁿ⁾(a)(x-a)ⁿ/n! - Maclaurin is Taylor centered at a=0",
    },
    "polar_coordinates": {
        "name": "Polar Coordinates and Calculus",
        "description": "Calculus in polar form: r = f(θ), area = ½∫r²dθ",
        "typical_forms": ["r = 2cos(θ)", "r = 1 + sin(θ)", "area between curves"],
        "key_insight": "Area = ½∫r²dθ, Arc length = ∫√(r² + (dr/dθ)²)dθ",
    },
    "parametric_equations": {
        "name": "Parametric Equations",
        "description": "Curves defined by x(t), y(t) - derivatives and integrals",
        "typical_forms": ["x=cos(t), y=sin(t)", "x=t², y=t³", "cycloid"],
        "key_insight": "dy/dx = (dy/dt)/(dx/dt), Arc length = ∫√((dx/dt)² + (dy/dt)²)dt",
    },
}


def get_cache_key(prompt: str) -> str:
    """Generate cache key from prompt"""
    return hashlib.md5(prompt.encode()).hexdigest()


def get_cached_response(cache_key: str) -> Optional[str]:
    """Get cached AI response if exists"""
    cache_file = CACHE_DIR / f"{cache_key}.json"
    if cache_file.exists():
        try:
            with open(cache_file, 'r') as f:
                data = json.load(f)
                return data.get('response')
        except:
            pass
    return None


def save_to_cache(cache_key: str, response: str):
    """Cache AI response"""
    cache_file = CACHE_DIR / f"{cache_key}.json"
    with open(cache_file, 'w') as f:
        json.dump({'response': response}, f)


async def call_copilot_cli(prompt: str, use_cache: bool = True) -> str:
    """
    Call GitHub Copilot CLI to generate content.
    Uses GPT-5-mini (free) through the authenticated Copilot CLI.
    """
    # Check cache first
    cache_key = get_cache_key(prompt)
    if use_cache:
        cached = get_cached_response(cache_key)
        if cached:
            return cached
    
    # Build the command - use copilot CLI with explain mode
    # We'll pipe our prompt to it
    full_prompt = f"""You are an expert Calculus II tutor. Respond with ONLY valid JSON, no markdown formatting.

{prompt}"""
    
    try:
        # Try using the standalone copilot CLI first
        process = await asyncio.create_subprocess_exec(
            'copilot',
            '-e',  # explain mode
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await asyncio.wait_for(
            process.communicate(input=full_prompt.encode()),
            timeout=60.0
        )
        response = stdout.decode().strip()
        
        if response and process.returncode == 0:
            save_to_cache(cache_key, response)
            return response
            
    except Exception as e:
        print(f"Copilot CLI error: {e}")
    
    # Fallback: try gh copilot
    try:
        process = await asyncio.create_subprocess_shell(
            f'echo "{full_prompt.replace('"', '\\"')}" | gh copilot explain -',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await asyncio.wait_for(
            process.communicate(),
            timeout=60.0
        )
        response = stdout.decode().strip()
        
        if response:
            save_to_cache(cache_key, response)
            return response
            
    except Exception as e:
        print(f"gh copilot error: {e}")
    
    return ""


def extract_json_from_response(response: str) -> Optional[Dict]:
    """Extract JSON from AI response, handling markdown code blocks"""
    # Try to find JSON in code blocks first
    json_match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', response)
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except json.JSONDecodeError:
            pass
    
    # Try parsing the whole response as JSON
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        pass
    
    # Try to find JSON-like structure
    json_match = re.search(r'\{[\s\S]*\}', response)
    if json_match:
        try:
            return json.loads(json_match.group(0))
        except json.JSONDecodeError:
            pass
    
    return None


async def generate_problem(topic: str, difficulty: int, avoid_problems: List[str] = None) -> Optional[GeneratedProblem]:
    """
    Generate a new calculus problem using Copilot.
    
    Args:
        topic: One of the CALC2_TOPICS keys
        difficulty: 1-3 (basic, intermediate, advanced)
        avoid_problems: List of problem questions to avoid duplicating
    """
    topic_info = CALC2_TOPICS.get(topic, {})
    topic_name = topic_info.get('name', topic)
    description = topic_info.get('description', '')
    typical_forms = topic_info.get('typical_forms', [])
    key_insight = topic_info.get('key_insight', '')
    
    difficulty_desc = {1: "basic/introductory", 2: "intermediate", 3: "advanced/challenging"}
    
    avoid_str = ""
    if avoid_problems:
        avoid_str = f"\n\nDO NOT generate these problems (already seen): {avoid_problems[:5]}"
    
    prompt = f"""Generate a {difficulty_desc[difficulty]} Calculus II problem about {topic_name}.

Topic: {topic_name}
Description: {description}
Typical forms: {', '.join(typical_forms)}
Key insight: {key_insight}
{avoid_str}

IMPORTANT: All mathematical expressions MUST use LaTeX wrapped in dollar-sign delimiters:
- Use $...$ for inline math (e.g. $\\int x\\,dx$)
- Use $$...$$ for display math (e.g. $$\\frac{{d}}{{dx}}[f(g(x))]$$)

Return ONLY this JSON structure:
{{
    "question": "The problem statement with math in $...$ or $$...$$ delimiters",
    "answer": "The final answer (simplified, with $...$ if it contains math)",
    "hints": [
        "First hint - gentle nudge (use $...$ for math)",
        "Second hint - more specific guidance", 
        "Third hint - almost gives it away"
    ],
    "walkthrough": [
        {{"step": "Step 1 title", "content": "Detailed explanation (use $...$ for math)", "formula": "LaTeX formula in $$...$$ if applicable, or empty string"}},
        {{"step": "Step 2 title", "content": "Detailed explanation", "formula": ""}},
        {{"step": "Step 3 title", "content": "Detailed explanation", "formula": ""}}
    ],
    "key_concept": "The main concept this tests",
    "explanation": "Why this answer is correct - teach the student (use $...$ for math)"
}}"""

    response = await call_copilot_cli(prompt, use_cache=False)  # Don't cache problems for variety
    
    if response:
        data = extract_json_from_response(response)
        if data:
            return GeneratedProblem(
                question=data.get('question', ''),
                answer=data.get('answer', ''),
                hints=data.get('hints', []),
                walkthrough=data.get('walkthrough', []),
                key_concept=data.get('key_concept', ''),
                difficulty=difficulty,
                topic=topic,
                explanation=data.get('explanation', '')
            )
    
    return None


async def generate_concept_explanation(topic: str) -> Optional[ConceptExplanation]:
    """
    Generate a deep conceptual explanation of a Calc II topic.
    """
    topic_info = CALC2_TOPICS.get(topic, {})
    topic_name = topic_info.get('name', topic)
    description = topic_info.get('description', '')
    
    prompt = f"""Create a comprehensive teaching explanation for {topic_name} in Calculus II.

Topic: {topic_name}
Description: {description}

The student knows nothing - teach from the ground up but don't be condescending.
Include intuitive explanations, then formalize.

IMPORTANT: All mathematical expressions MUST use LaTeX wrapped in dollar-sign delimiters:
- Use $...$ for inline math (e.g. $\\int x\\,dx$)
- Use $$...$$ for display math (e.g. $$\\frac{{d}}{{dx}}[f(g(x))]$$)

Return ONLY this JSON:
{{
    "title": "{topic_name}",
    "intuition": "Plain English explanation - why does this technique exist? What problem does it solve?",
    "formal_definition": "The mathematical definition with LaTeX in $...$ or $$...$$ delimiters",
    "key_formulas": [
        "$$formula_1$$ with explanation",
        "$$formula_2$$ with explanation"
    ],
    "worked_examples": [
        {{
            "problem": "Example problem (use $...$ for math)",
            "solution": "Step-by-step solution with $...$ math at each step"
        }},
        {{
            "problem": "Another example",
            "solution": "Step-by-step solution"
        }}
    ],
    "common_mistakes": [
        "Mistake 1 and how to avoid it",
        "Mistake 2 and how to avoid it"
    ],
    "when_to_use": "How to recognize when this technique is needed",
    "practice_recognition": [
        "Pattern 1 that signals this technique",
        "Pattern 2 that signals this technique"
    ]
}}"""

    response = await call_copilot_cli(prompt)
    
    if response:
        data = extract_json_from_response(response)
        if data:
            return ConceptExplanation(
                topic=topic,
                title=data.get('title', topic_name),
                intuition=data.get('intuition', ''),
                formal_definition=data.get('formal_definition', ''),
                key_formulas=data.get('key_formulas', []),
                worked_examples=data.get('worked_examples', []),
                common_mistakes=data.get('common_mistakes', []),
                when_to_use=data.get('when_to_use', ''),
                practice_recognition=data.get('practice_recognition', [])
            )
    
    return None


async def analyze_wrong_answer(problem: str, user_answer: str, correct_answer: str, topic: str) -> Dict[str, Any]:
    """
    Analyze why a student got an answer wrong and provide targeted help.
    """
    prompt = f"""A student is learning {topic} in Calculus II.

Problem: {problem}
Student's answer: {user_answer}
Correct answer: {correct_answer}

Analyze what misconception or error led to their answer. Be encouraging but educational.

Return ONLY this JSON:
{{
    "error_type": "calculation_error|conceptual_error|notation_error|incomplete|other",
    "diagnosis": "What specific mistake did they make?",
    "misconception": "What misunderstanding might have caused this?",
    "correction": "How to fix this specific error",
    "encouragement": "Positive, encouraging message",
    "mini_lesson": "Brief re-teaching of the relevant concept",
    "similar_problem": "A simpler problem to practice the weak area"
}}"""

    response = await call_copilot_cli(prompt, use_cache=False)
    
    if response:
        data = extract_json_from_response(response)
        if data:
            return data
    
    return {
        "error_type": "unknown",
        "diagnosis": "Let's look at this together.",
        "correction": f"The correct answer is {correct_answer}. Let's work through why.",
        "encouragement": "Making mistakes is part of learning! Let's figure this out.",
    }


async def generate_hint_for_stuck_student(problem: str, topic: str, hints_seen: int) -> str:
    """
    Generate a contextual hint based on how stuck the student is.
    """
    hint_level = min(hints_seen + 1, 5)
    
    hint_descriptions = {
        1: "very gentle nudge - just point them in the right direction",
        2: "slightly more specific - mention the technique to use",
        3: "quite helpful - outline the first step",
        4: "very helpful - walk through the setup",
        5: "almost giving it away - show most of the work"
    }
    
    prompt = f"""Student is stuck on this {topic} problem:
{problem}

They've already seen {hints_seen} hints and need more help.
Generate hint level {hint_level}: {hint_descriptions[hint_level]}

Return ONLY this JSON:
{{
    "hint": "The hint text",
    "encouragement": "Brief encouraging message"
}}"""

    response = await call_copilot_cli(prompt, use_cache=False)
    
    if response:
        data = extract_json_from_response(response)
        if data:
            return data.get('hint', 'Try breaking the problem into smaller steps.')
    
    return "Try breaking the problem into smaller steps."


async def explain_step(problem: str, step_number: int, topic: str) -> Dict[str, str]:
    """
    Generate a detailed explanation for a specific step in solving a problem.
    """
    prompt = f"""For this {topic} problem:
{problem}

Explain step {step_number} of the solution in detail. Assume the student doesn't understand why we do this step.

Return ONLY this JSON:
{{
    "step_title": "Brief title for this step",
    "what_we_do": "What action we take",
    "why_we_do_it": "Why this step is necessary - the reasoning",
    "how_to_do_it": "The mechanics of doing this step",
    "formula": "Any relevant formula in LaTeX (or empty string)",
    "common_pitfall": "What students often get wrong here"
}}"""

    response = await call_copilot_cli(prompt)
    
    if response:
        data = extract_json_from_response(response)
        if data:
            return data
    
    return {"step_title": f"Step {step_number}", "what_we_do": "Continue solving..."}


async def generate_practice_quiz(topics: List[str], num_questions: int = 5) -> List[Dict]:
    """
    Generate a quick practice quiz covering multiple topics.
    """
    topic_names = [CALC2_TOPICS.get(t, {}).get('name', t) for t in topics]
    
    prompt = f"""Generate a {num_questions}-question Calculus II practice quiz covering: {', '.join(topic_names)}

Mix difficulties. Each question should test a different concept.

Return ONLY this JSON:
{{
    "questions": [
        {{
            "question": "Problem text",
            "topic": "topic_key",
            "difficulty": 1-3,
            "answer": "correct answer",
            "quick_hint": "one-line hint"
        }}
    ]
}}"""

    response = await call_copilot_cli(prompt, use_cache=False)
    
    if response:
        data = extract_json_from_response(response)
        if data:
            return data.get('questions', [])
    
    return []


# Synchronous wrappers for non-async contexts
def sync_generate_problem(topic: str, difficulty: int, avoid_problems: List[str] = None) -> Optional[GeneratedProblem]:
    """Synchronous wrapper for generate_problem"""
    return asyncio.run(generate_problem(topic, difficulty, avoid_problems))

def sync_generate_concept_explanation(topic: str) -> Optional[ConceptExplanation]:
    """Synchronous wrapper for generate_concept_explanation"""
    return asyncio.run(generate_concept_explanation(topic))

def sync_analyze_wrong_answer(problem: str, user_answer: str, correct_answer: str, topic: str) -> Dict[str, Any]:
    """Synchronous wrapper for analyze_wrong_answer"""
    return asyncio.run(analyze_wrong_answer(problem, user_answer, correct_answer, topic))


# Pre-built fallback content for when AI is unavailable
FALLBACK_PROBLEMS = {
    "integration_by_parts": [
        {
            "question": "Evaluate: ∫ x·cos(x) dx",
            "answer": "x·sin(x) + cos(x) + C",
            "hints": [
                "This is a product of x and cos(x) - integration by parts!",
                "Let u = x (algebraic) and dv = cos(x)dx",
                "Then du = dx and v = sin(x). Apply the formula."
            ],
            "walkthrough": [
                {"step": "Identify the technique", "content": "We have a product of x and cos(x). Use integration by parts.", "formula": "\\int u \\, dv = uv - \\int v \\, du"},
                {"step": "Choose u and dv", "content": "Using LIATE: u = x (Algebraic), dv = cos(x)dx", "formula": "u = x, \\quad dv = \\cos(x)dx"},
                {"step": "Find du and v", "content": "Differentiate u and integrate dv", "formula": "du = dx, \\quad v = \\sin(x)"},
                {"step": "Apply the formula", "content": "Substitute into ∫udv = uv - ∫vdu", "formula": "= x\\sin(x) - \\int \\sin(x)dx"},
                {"step": "Evaluate remaining integral", "content": "∫sin(x)dx = -cos(x)", "formula": "= x\\sin(x) + \\cos(x) + C"}
            ],
            "key_concept": "LIATE rule for choosing u in integration by parts",
            "explanation": "We use integration by parts because the integrand is a product. The LIATE rule helps us choose u = x because algebraic functions simplify when differentiated.",
            "difficulty": 1
        }
    ],
    # Add more fallback problems for other topics...
}


async def get_problem_with_fallback(topic: str, difficulty: int, avoid: List[str] = None) -> Dict:
    """Get a problem, falling back to pre-built if AI fails"""
    # Try AI generation first
    problem = await generate_problem(topic, difficulty, avoid)
    
    if problem:
        return asdict(problem)
    
    # Fallback to pre-built problems
    fallbacks = FALLBACK_PROBLEMS.get(topic, [])
    for fb in fallbacks:
        if fb['difficulty'] == difficulty and fb['question'] not in (avoid or []):
            return {**fb, 'topic': topic}
    
    # Last resort - return a generic problem
    return {
        "question": f"Practice problem for {CALC2_TOPICS.get(topic, {}).get('name', topic)} (AI generation unavailable)",
        "answer": "See solution",
        "hints": ["Try reviewing the concept first"],
        "walkthrough": [{"step": "Review needed", "content": "Please review this topic's learning materials"}],
        "key_concept": topic,
        "explanation": "This is a placeholder - AI generation was unavailable",
        "difficulty": difficulty,
        "topic": topic
    }
