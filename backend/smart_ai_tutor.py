"""
Smart AI-Powered Calculus Tutor with Caching
Uses GitHub Copilot CLI with gpt-5-mini (FREE) for most tasks.
Caches expensive/static content to minimize costs.

Model Strategy:
- gpt-5-mini (FREE): Problem hints, step explanations, answer feedback, problem generation
- gpt-5.4-mini (cheap): Complex explanations, multi-step walkthroughs (when cached version unavailable)
- Expensive models: NEVER used - everything is handled by mini models with good prompting

Caching Strategy:
- Lesson content: Cached permanently (never changes)
- Common explanations: Cached permanently
- Problem solutions: Cached by problem hash
- User-specific feedback: Not cached (personalized)
"""

import subprocess
import json
import hashlib
import asyncio
import os
import re
from typing import Optional, Dict, Any, List
from pathlib import Path
from datetime import datetime

# Cache directory
CACHE_DIR = Path(__file__).parent / "data" / "ai_cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# Topic definitions for Calc II
CALC2_TOPICS = {
    "integration_by_parts": {
        "name": "Integration by Parts",
        "formula": "∫ u dv = uv - ∫ v du",
        "keywords": ["LIATE", "product rule", "u-substitution fails"],
        "difficulty_range": [1, 2, 3]
    },
    "partial_fractions": {
        "name": "Partial Fractions",
        "formula": "Decompose rational functions",
        "keywords": ["linear factors", "repeated factors", "irreducible quadratic"],
        "difficulty_range": [1, 2, 3]
    },
    "trig_substitution": {
        "name": "Trigonometric Substitution",
        "formula": "√(a²-x²)→x=a·sin(θ), √(a²+x²)→x=a·tan(θ), √(x²-a²)→x=a·sec(θ)",
        "keywords": ["radical", "Pythagorean", "right triangle"],
        "difficulty_range": [1, 2, 3]
    },
    "improper_integrals": {
        "name": "Improper Integrals",
        "formula": "∫[a,∞] or discontinuous integrand",
        "keywords": ["limit", "convergent", "divergent", "comparison test"],
        "difficulty_range": [1, 2, 3]
    },
    "sequences_series": {
        "name": "Sequences and Series",
        "formula": "∑ aₙ convergence tests",
        "keywords": ["ratio test", "root test", "comparison", "integral test", "alternating"],
        "difficulty_range": [1, 2, 3]
    },
    "power_series": {
        "name": "Power Series",
        "formula": "∑ cₙ(x-a)ⁿ",
        "keywords": ["radius of convergence", "interval", "ratio test"],
        "difficulty_range": [1, 2, 3]
    },
    "taylor_maclaurin": {
        "name": "Taylor & Maclaurin Series",
        "formula": "f(x) = ∑ f⁽ⁿ⁾(a)/n! · (x-a)ⁿ",
        "keywords": ["derivatives", "expansion", "approximation"],
        "difficulty_range": [1, 2, 3]
    },
    "polar_coordinates": {
        "name": "Polar Coordinates",
        "formula": "r, θ; Area = ½∫r²dθ",
        "keywords": ["polar area", "polar curves", "conversion"],
        "difficulty_range": [1, 2, 3]
    },
    "parametric_equations": {
        "name": "Parametric Equations",
        "formula": "x=f(t), y=g(t)",
        "keywords": ["arc length", "surface area", "dy/dx = (dy/dt)/(dx/dt)"],
        "difficulty_range": [1, 2, 3]
    }
}


def cache_key(content: str) -> str:
    """Generate a cache key from content"""
    return hashlib.md5(content.encode()).hexdigest()[:16]


def get_cached(category: str, key: str) -> Optional[str]:
    """Retrieve cached content"""
    cache_file = CACHE_DIR / category / f"{key}.json"
    if cache_file.exists():
        try:
            data = json.loads(cache_file.read_text())
            return data.get("content")
        except:
            return None
    return None


def set_cached(category: str, key: str, content: str, metadata: dict = None):
    """Store content in cache"""
    cache_subdir = CACHE_DIR / category
    cache_subdir.mkdir(parents=True, exist_ok=True)
    
    cache_file = cache_subdir / f"{key}.json"
    data = {
        "content": content,
        "cached_at": datetime.now().isoformat(),
        "metadata": metadata or {}
    }
    cache_file.write_text(json.dumps(data, indent=2))


class SmartAITutor:
    """AI Tutor using Copilot CLI with intelligent caching"""
    
    def __init__(self, default_model: str = "gpt-5-mini"):
        self.default_model = default_model
        self.conversation_history: List[Dict[str, str]] = []
        
    async def _call_copilot(self, prompt: str, model: str = None, silent: bool = True) -> str:
        """Call Copilot CLI with the given prompt, falling back to built-in knowledge."""
        model = model or self.default_model
        
        cmd = ["copilot", "-p", prompt, "--model", model, "-s"]
        
        try:
            result = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await result.communicate()
            
            if result.returncode != 0:
                error = stderr.decode('utf-8')
                print(f"Copilot CLI error: {error}")
                return self._fallback_response(prompt)
            
            response = stdout.decode('utf-8').strip()
            if not response:
                return self._fallback_response(prompt)
            return response
        except FileNotFoundError:
            print("Copilot CLI not found — using built-in fallback")
            return self._fallback_response(prompt)
        except Exception as e:
            print(f"Exception calling Copilot: {e}")
            return self._fallback_response(prompt)
    
    def _fallback_response(self, prompt: str) -> str:
        """Generate a basic response from built-in topic knowledge when the AI CLI is unavailable."""
        prompt_lower = prompt.lower()
        
        for topic_id, topic in CALC2_TOPICS.items():
            name_lower = topic["name"].lower()
            if name_lower in prompt_lower or topic_id.replace("_", " ") in prompt_lower:
                keywords = ", ".join(topic.get("keywords", []))
                return (
                    f"# {topic['name']}\n\n"
                    f"**Key Formula:** {topic['formula']}\n\n"
                    f"**Key Concepts:** {keywords}\n\n"
                    f"*Note: The AI tutor is currently offline. "
                    f"This is a summary from the built-in knowledge base. "
                    f"Please check that the Copilot CLI is installed and accessible.*"
                )
        
        return (
            "The AI tutor is temporarily unavailable. Please check that the "
            "Copilot CLI is installed (`copilot --version`) and try again.\n\n"
            "In the meantime, try the **Formulas** page for quick reference, "
            "or review your notes on the topic."
        )
    
    async def get_topic_lesson(self, topic_id: str) -> str:
        """
        Get a comprehensive lesson for a topic.
        CACHED: Lessons are static and don't change.
        """
        # Check cache first
        cached = get_cached("lessons", topic_id)
        if cached:
            return cached
        
        topic = CALC2_TOPICS.get(topic_id)
        if not topic:
            return "Topic not found."
        
        prompt = f"""Create a comprehensive from-scratch lesson on "{topic['name']}" for a student who only knows high school algebra.

CRITICAL TEACHING RULES:
- Assume ZERO prior calculus knowledge for this topic. Rebuild any needed prerequisites.
- Start with WHY this topic exists — what problem does it solve?
- Use analogies and intuition BEFORE formulas.
- Every formula must be explained piece by piece.
- Show 2 worked examples: one dead-simple, one intermediate.
- Use LaTeX for all math: $inline$ or $$display math$$

Structure:
## {topic['name']}

### Why This Exists (The Problem We're Solving)
(2-3 sentences: What gap in our math toolbox does this fill? Give a real-world motivation.)

### Building the Intuition
(Explain the concept using everyday language and analogies BEFORE any formulas.)

### The Formula / Method
(State the key formula(s). Then explain EVERY symbol — what it means, where it comes from.)

### Step-by-Step: How to Apply It
(A numbered process to follow every time. Be specific — "identify ___", "set up ___", etc.)

### Worked Example 1 — The Simplest Possible Case
(Walk through a trivial example showing every single step. NO skipping.)

### Worked Example 2 — A Step Up
(Slightly more complex. Point out what changed and why the process adapts.)

### Patterns to Recognize
(How do you know you need this technique? What does the problem "look like"?)

### Pitfalls and Exam Traps
(3-5 specific mistakes students make, with how to avoid them.)

### How This Connects to What You'll Learn Next
(One sentence bridge to the next topic.)

Be thorough. This is Alex's PRIMARY resource for learning calculus from scratch."""

        content = await self._call_copilot(prompt)
        
        # Cache the lesson
        set_cached("lessons", topic_id, content, {"topic": topic_id, "name": topic['name']})
        
        return content
    
    async def get_concept_explanation(self, concept: str) -> str:
        """
        Explain a specific concept or formula.
        CACHED: Common concepts don't change.
        """
        key = cache_key(concept.lower().strip())
        cached = get_cached("concepts", key)
        if cached:
            return cached
        
        prompt = f"""Explain this Calculus II concept clearly: "{concept}"

Include:
1. What it means intuitively (not just the definition)
2. The mathematical formulation using LaTeX ($..$ or $$...$$)
3. A simple example showing how it works
4. When/why you would use it
5. Common mistakes students make with this concept

Be clear and concise. Focus on understanding, not just memorization."""

        content = await self._call_copilot(prompt)
        set_cached("concepts", key, content, {"concept": concept})
        
        return content
    
    async def generate_problem(self, topic_id: str, difficulty: int = 1) -> Dict[str, Any]:
        """
        Generate a practice problem.
        NOT CACHED: Want variety in problems.
        Uses gpt-5-mini (FREE).
        """
        topic = CALC2_TOPICS.get(topic_id)
        if not topic:
            return {"error": "Topic not found"}
        
        diff_desc = {1: "basic/introductory", 2: "intermediate", 3: "challenging/exam-level"}
        
        prompt = f"""Generate a {diff_desc.get(difficulty, 'intermediate')} Calculus II problem on "{topic['name']}".

Return ONLY valid JSON (no markdown, no explanation):
{{
    "question": "The problem statement using LaTeX ($$...$$)",
    "answer": "The final answer",
    "solution_steps": ["Step 1: ...", "Step 2: ...", "..."],
    "hints": ["First hint (small nudge)", "Second hint (bigger help)", "Third hint (nearly gives it away)"],
    "key_concept": "The main idea being tested",
    "difficulty": {difficulty}
}}

Make it realistic for a university Calc II final exam.
Keywords for this topic: {', '.join(topic['keywords'])}"""

        response = await self._call_copilot(prompt)
        
        # Parse JSON from response
        try:
            # Try to extract JSON from the response
            json_match = re.search(r'\{[\s\S]*\}', response)
            if json_match:
                return json.loads(json_match.group())
            else:
                return {"error": "Could not parse problem", "raw": response}
        except json.JSONDecodeError as e:
            return {"error": f"JSON parse error: {e}", "raw": response}
    
    async def get_hint(self, problem: str, hint_level: int = 1, user_attempt: str = None) -> str:
        """
        Get a hint for a problem.
        NOT CACHED: Personalized based on user's attempt.
        Uses gpt-5-mini (FREE).
        """
        context = f"User's attempt: {user_attempt}" if user_attempt else "User hasn't attempted yet"
        
        hint_guidance = {
            1: "Give a small nudge - point them in the right direction without giving away the method",
            2: "Give moderate help - identify the technique to use and the first step",
            3: "Give substantial help - walk through the setup but let them do the calculation"
        }
        
        prompt = f"""A student needs a level {hint_level} hint for this Calculus II problem:

Problem: {problem}
{context}

Hint Level Guidance: {hint_guidance.get(hint_level, hint_guidance[2])}

Give ONLY the hint - don't solve it. Use Socratic questioning when possible.
Use LaTeX for any math: $..$ or $$..$$"""

        return await self._call_copilot(prompt)
    
    async def check_answer(self, problem: str, correct_answer: str, user_answer: str) -> Dict[str, Any]:
        """
        Check user's answer and provide feedback.
        NOT CACHED: Personalized feedback.
        Uses gpt-5-mini (FREE).
        """
        prompt = f"""Check this Calculus II answer and provide feedback.

Problem: {problem}
Correct Answer: {correct_answer}
Student's Answer: {user_answer}

Return ONLY valid JSON:
{{
    "is_correct": true/false,
    "feedback": "Specific feedback on their answer",
    "common_mistake": "If wrong, what mistake did they likely make?" or null,
    "encouragement": "Brief encouraging message",
    "next_tip": "What to focus on next"
}}

Be encouraging but honest. If partially correct, acknowledge what they got right."""

        response = await self._call_copilot(prompt)
        
        try:
            json_match = re.search(r'\{[\s\S]*\}', response)
            if json_match:
                return json.loads(json_match.group())
            else:
                # Fallback: simple check
                return {
                    "is_correct": self._simple_answer_check(correct_answer, user_answer),
                    "feedback": response,
                    "common_mistake": None,
                    "encouragement": "Keep practicing!",
                    "next_tip": "Try another problem"
                }
        except:
            return {
                "is_correct": self._simple_answer_check(correct_answer, user_answer),
                "feedback": "Could not generate detailed feedback.",
                "common_mistake": None,
                "encouragement": "Keep going!",
                "next_tip": "Try the next problem"
            }
    
    def _simple_answer_check(self, correct: str, user: str) -> bool:
        """Simple answer comparison as fallback"""
        def normalize(s):
            return (s.lower().replace(" ", "").replace("\\", "")
                    .replace("·", "*").replace("×", "*").replace("÷", "/")
                    .replace("²", "^2").replace("³", "^3")
                    .replace("π", "pi").replace("−", "-"))
        return normalize(correct) == normalize(user)
    
    async def explain_solution(self, problem: str, solution: str) -> str:
        """
        Provide a detailed explanation of a solution.
        CACHED by problem hash: Solutions don't change.
        """
        key = cache_key(problem)
        cached = get_cached("solutions", key)
        if cached:
            return cached
        
        prompt = f"""Explain this Calculus II solution step-by-step, as if teaching a student who got it wrong.

Problem: {problem}
Solution: {solution}

For EACH step:
1. State what we're doing
2. Explain WHY we do this (the mathematical reasoning)
3. Show the calculation
4. Point out any tricks or things to watch for

Use LaTeX for all math. Be thorough - explain the thinking process, not just the mechanics."""

        content = await self._call_copilot(prompt)
        set_cached("solutions", key, content, {"problem": problem[:100]})
        
        return content
    
    def _detect_confusion(self, user_message: str, conversation_history: List[Dict[str, str]] = None) -> int:
        """
        Detect how confused the student is and how many times we've already
        tried explaining. Returns a confusion_level 0-3:
          0 = new question / not confused
          1 = mildly confused (asking for clarification)
          2 = clearly confused (asking for simpler terms, expressing frustration)
          3 = very confused (multiple failed explanations, strong frustration)
        """
        msg_lower = user_message.lower().strip()

        strong_signals = [
            "what", "huh", "i don't get", "i dont get", "confused",
            "makes no sense", "don't understand", "dont understand",
            "lost", "can you simplify", "simpler", "too complicated",
            "what are you saying", "what does that mean", "explain like",
            "eli5", "dumb it down", "not the same", "still don't",
            "still dont", "why does", "how does", "wait what",
            "teach me", "i'm so lost", "im so lost",
        ]
        mild_signals = [
            "can you explain", "a bit more", "more detail",
            "say that again", "repeat", "what do you mean",
            "not sure", "kind of", "sort of", "i think",
        ]

        is_strong = any(s in msg_lower for s in strong_signals)
        is_mild = any(s in msg_lower for s in mild_signals)

        # Count how many assistant messages already exist in this conversation
        prior_explanations = 0
        if conversation_history:
            prior_explanations = sum(1 for m in conversation_history if m.get("role") == "assistant")

        if is_strong and prior_explanations >= 3:
            return 3
        if is_strong and prior_explanations >= 1:
            return 2
        if is_strong or (is_mild and prior_explanations >= 2):
            return 1
        return 0

    def _build_teaching_strategy(self, confusion_level: int) -> str:
        """Return strategy instructions based on how confused the student is."""
        if confusion_level == 0:
            return ""

        if confusion_level == 1:
            return """
IMPORTANT — The student is asking for clarification. Do NOT repeat your previous explanation in different words. Instead:
- Pick ONE small piece of what you said and zoom in on just that piece
- Use a concrete real-world analogy (money, distance, time — something physical)
- Ask a guiding question to find out exactly what's confusing them
- Keep it SHORT — 3-5 sentences max, not another wall of text"""

        if confusion_level == 2:
            return """
CRITICAL — The student is clearly confused. Your previous explanation(s) DID NOT WORK. You MUST try a completely different approach:
- STOP using formal math notation for now. Use plain English and numbers only.
- Walk through ONE specific numerical example with actual calculator-button steps
  (e.g., "Type 2.5 into your calculator. Now hit the 'ln' button. You get 0.916...")
- Break the problem into tiny yes/no checkpoints: "So far we have 2.5 — does that make sense before we go on?"
- Do NOT show the general formula. Show the specific numbers first, and ONLY generalize after they say they understand.
- Maximum 5-6 sentences. Then ASK what part is still confusing."""

        # confusion_level >= 3
        return """
CRITICAL — Multiple explanations have failed. The student is frustrated. COMPLETELY CHANGE YOUR APPROACH:
- Start from absolute scratch. Pretend they have never seen this problem before.
- Use ONLY a concrete numbers-only walkthrough. No variables, no formulas, no notation.
- Narrate it like you're sitting next to them with a calculator:
  "OK, forget everything I said. Let's start fresh with just the numbers.
   We have 4 times (1.2 to the power of x) equals 10.
   Step 1: Get rid of the 4. Divide both sides by 4. Now we have 1.2^x = 2.5.
   Step 2: We need to find x. Your calculator has an 'ln' button. Press ln(2.5). You get about 0.916.
   Step 3: Now press ln(1.2). You get about 0.182.
   Step 4: Divide: 0.916 / 0.182 = about 5.03. That's x!"
- After the numbers-only walkthrough, ask: "Does that make sense? Want me to explain WHY those steps work, or do you want to try one yourself?"
- ONLY explain the 'why' if they ask for it. Don't volunteer it."""

    async def adaptive_tutor_response(self, 
                                       user_message: str, 
                                       current_topic: str = None,
                                       mastery_level: float = 0.5,
                                       recent_mistakes: List[str] = None,
                                       conversation_history: List[Dict[str, str]] = None) -> str:
        """
        Main tutoring interface - responds to any user question.
        NOT CACHED: Conversational and personalized.
        Uses gpt-5-mini (FREE).
        
        conversation_history: Full chat history from the frontend (list of {role, content} dicts).
        """
        context_parts = []
        
        if current_topic and current_topic in CALC2_TOPICS:
            topic = CALC2_TOPICS[current_topic]
            context_parts.append(f"Current topic: {topic['name']}")
        
        if mastery_level < 0.3:
            context_parts.append("Student level: Beginner — needs foundational explanation with lots of examples")
        elif mastery_level < 0.7:
            context_parts.append("Student level: Intermediate — understands basics, working on applying them")
        else:
            context_parts.append("Student level: Advanced — ready for harder problems and deeper theory")
        
        if recent_mistakes:
            context_parts.append(f"Recent struggles: {', '.join(recent_mistakes[:3])}")

        # Use frontend conversation history if provided, otherwise fall back to self-managed
        chat_history = conversation_history or self.conversation_history
        
        # Detect confusion and pick a teaching strategy
        confusion_level = self._detect_confusion(user_message, chat_history)
        strategy = self._build_teaching_strategy(confusion_level)

        # Build readable history — show FULL messages, not truncated
        history = ""
        if chat_history:
            # Show up to last 10 messages (5 exchanges) with full content
            recent = chat_history[-10:]
            history = "\n--- Conversation so far ---\n"
            for msg in recent:
                role = msg.get("role", "user").title()
                content = msg.get("content", "")
                # Truncate only extremely long messages (> 800 chars)
                if len(content) > 800:
                    content = content[:800] + "..."
                history += f"{role}: {content}\n"
            history += "--- End of conversation ---\n"
        
        context = "\n".join(context_parts)
        
        prompt = f"""You are Alex's personal calculus tutor — like a patient older sibling who's great at math. Alex is taking MATH 1220 at the University of Utah. Assume Alex knows algebra and pre-calc but nothing beyond that.

YOUR TEACHING RULES (follow these strictly):
1. KEEP IT SHORT. Answer in 5-8 sentences unless Alex asks for a full walkthrough. Walls of text are overwhelming.
2. One idea at a time. Finish one thought completely before introducing the next.
3. When explaining a new concept, start with a CONCRETE example using specific numbers BEFORE showing any general formula.
4. Use LaTeX for math: $inline$ for short, $$display$$ for important formulas.
5. After explaining something, ask a quick check question ("Does that click?" or "Want me to go deeper on any part?") instead of dumping more info.
6. NEVER repeat what you already said. If Alex is still confused, read the conversation history carefully and try a COMPLETELY DIFFERENT angle — different analogy, different example, different level of detail.
7. If you already explained with formulas and it didn't work, switch to pure numbers. If numbers didn't work, switch to a real-world analogy. Always change approach.
8. Match Alex's energy. If Alex uses casual language, be casual. If Alex asks a precise question, give a precise answer.
9. WHEN ALEX IS CORRECT, SAY SO IMMEDIATELY AND MOVE ON. If Alex answers a question correctly or demonstrates understanding, confirm it in 1-2 sentences ("Yes, exactly right!" or "Spot on.") and then offer to move forward ("Want a harder one?" or "Ready for the next concept?"). Do NOT re-explain what they already understand. Do NOT give another example of something they just solved correctly. Celebrate the win and advance.
10. When Alex asks "did I get it right?", "is this correct?", or similar — read what they said carefully. If their reasoning and answer are correct, just confirm clearly: "Yes, you nailed it." Don't hedge, don't re-derive, don't add unnecessary caveats.
{strategy}

CONTEXT:
{context}
{history}

Alex says: {user_message}

Remember: you're a person helping a friend understand math, not a textbook generating content. Be real. Be helpful. Be brief."""

        response = await self._call_copilot(prompt)
        
        # Update self-managed history as fallback (used when frontend doesn't send history)
        self.conversation_history.append({"role": "user", "content": user_message})
        self.conversation_history.append({"role": "assistant", "content": response})
        
        if len(self.conversation_history) > 20:
            self.conversation_history = self.conversation_history[-20:]
        
        return response
    
    async def generate_quiz(self, topic_ids: List[str], num_questions: int = 5) -> List[Dict]:
        """
        Generate a quiz covering multiple topics.
        NOT CACHED: Want fresh problems each time.
        Uses gpt-5-mini (FREE).
        """
        topics_str = ", ".join([CALC2_TOPICS[t]['name'] for t in topic_ids if t in CALC2_TOPICS])
        
        prompt = f"""Generate a {num_questions}-question Calculus II quiz covering: {topics_str}

Return ONLY a JSON array (no markdown):
[
    {{
        "question": "Problem text with LaTeX ($$...$$)",
        "topic": "topic_id",
        "answer": "correct answer",
        "difficulty": 1-3
    }},
    ...
]

Mix difficulty levels. Make problems exam-realistic."""

        response = await self._call_copilot(prompt)
        
        try:
            json_match = re.search(r'\[[\s\S]*\]', response)
            if json_match:
                return json.loads(json_match.group())
            return []
        except:
            return []
    
    def get_all_topics(self) -> Dict[str, Dict]:
        """Return all available topics"""
        return CALC2_TOPICS
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []


# Pre-cache common lessons on first import (can run async later)
async def precache_lessons():
    """Pre-generate and cache all topic lessons"""
    tutor = SmartAITutor()
    for topic_id in CALC2_TOPICS:
        cached = get_cached("lessons", topic_id)
        if not cached:
            print(f"Caching lesson for {topic_id}...")
            await tutor.get_topic_lesson(topic_id)
            await asyncio.sleep(1)  # Rate limit


if __name__ == "__main__":
    # Test the tutor
    async def test():
        tutor = SmartAITutor()
        
        print("Testing topic lesson (cached after first call)...")
        lesson = await tutor.get_topic_lesson("integration_by_parts")
        print(lesson[:500] + "...")
        
        print("\n\nTesting problem generation...")
        problem = await tutor.generate_problem("integration_by_parts", difficulty=1)
        print(json.dumps(problem, indent=2))
        
        print("\n\nTesting adaptive tutor...")
        response = await tutor.adaptive_tutor_response(
            "I don't understand when to use integration by parts vs u-substitution",
            current_topic="integration_by_parts",
            mastery_level=0.4
        )
        print(response)
    
    asyncio.run(test())
