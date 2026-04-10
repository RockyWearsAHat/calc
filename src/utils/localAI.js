import { CreateMLCEngine } from "@mlc-ai/web-llm";

let engine = null;
let loadPromise = null;
let progressCallback = null;

export function setProgressCallback(cb) {
  progressCallback = cb;
}

export async function getAIEngine() {
  if (engine) return engine;
  if (loadPromise) return loadPromise;

  const initProgressCallback = (report) => {
    if (progressCallback) {
      progressCallback(report);
    }
  };

  loadPromise = (async () => {
    try {
      engine = await CreateMLCEngine(
        "Llama-3.2-1B-Instruct-q4f16_1-MLC", // Ultra fast, sub-GB size (simulates the 1-bit efficiency)
        { 
          initProgressCallback,
        }
      );
      return engine;
    } catch (e) {
      loadPromise = null;
      throw e;
    }
  })();

  return loadPromise;
}

export async function generateChatResponse(message, history = [], systemPrompt = "") {
  const llm = await getAIEngine();
  
  const messages = [];
  if (systemPrompt) {
    messages.push({ role: "system", content: systemPrompt });
  }

  // push past history
  for (const h of history) {
    messages.push(h);
  }
  
  // push fresh user msg
  messages.push({ role: "user", content: message });

  const reply = await llm.chat.completions.create({
    messages,
    temperature: 0.1, // Keep it highly deterministic and capable
    max_tokens: 500,
  });

  return reply.choices[0].message.content;
}

export async function generatePracticeProblem(topic, userLevel, examples = []) {
  const llm = await getAIEngine();

  const systemPrompt = `You are a brilliant calculus engine running natively in the browser. 
  The student's Mastery Level is ${userLevel} (1 is beginner, higher is advanced).
  Generate exactly ONE unique practice problem matching the complexity of their typical homework.
  Format your response STRICTLY as a JSON object, with exactly three keys:
  "question" (string, the problem statement, format math with standard LaTeX)
  "answer" (string, just the final correct answer)
  "explanation" (string, the step-by-step walkthrough).
  DO NOT include markdown codeblock tags around the JSON.
  `;

  let prompt = `Topic: ${topic.title || topic.name}.`;
  if (examples && examples.length > 0) {
    prompt += `\nHere are some examples of their actual homework problems for context:\n${examples.slice(0,3).join("\n")}`;
  }
  prompt += `\nOutput JSON now.`;

  const reply = await llm.chat.completions.create({
    messages: [
      { role: "system", content: systemPrompt },
      { role: "user", content: prompt }
    ],
    temperature: 0.5,
    max_tokens: 500,
  });

  try {
    let raw = reply.choices[0].message.content.trim();
    if (raw.startsWith("```json")) raw = raw.replace(/```json/g, "").replace(/```/g, "").trim();
    return JSON.parse(raw);
  } catch(e) {
    // Fallback if parsing fails from 1-bit LLM
    return {
      question: "Solve the following problem related to " + (topic.title || topic.name) + ": Calculate the derivative (Fallback generation).",
      answer: "Check steps",
      explanation: "The LLM responded with malformed JSON:\n" + reply.choices[0].message.content
    };
  }
}
export async function checkAnswerLocally(question, expectedAnswer, studentAnswer) {
  const llm = await getAIEngine();
  
  const systemPrompt = `You are a brilliant calculus engine grading student work.
  The question was: ${question}
  The correct answer is: ${expectedAnswer}
  The student answered: ${studentAnswer}
  
  Are they mathematically equivalent? (e.g. "1/2" is equivalent to "0.5").
  Respond ONLY with a JSON object containing:
  "is_correct" (boolean)
  "feedback" (string, short feedback if wrong, or "Correct!" if right)
  DO NOT use markdown tags.
  `;

  const reply = await llm.chat.completions.create({
    messages: [
      { role: "system", content: systemPrompt },
      { role: "user", content: "Grade the student's answer now. Output JSON." }
    ],
    temperature: 0.1,
    max_tokens: 150,
  });

  try {
    let raw = reply.choices[0].message.content.trim();
    if (raw.startsWith("```json")) raw = raw.replace(/```json/g, "").replace(/```/g, "").trim();
    return JSON.parse(raw);
  } catch(e) {
    return {
      is_correct: studentAnswer.trim() === expectedAnswer.trim(),
      feedback: "Could not parse LLM grading output."
    };
  }
}

export async function generateHintLocally(question, stepNum, studentAttempt) {
  const llm = await getAIEngine();
  
  const systemPrompt = `You are a brilliant calculus engine providing a hint.
  The question is: ${question}
  The student has asked for Hint #${stepNum}.
  The student's current work: ${studentAttempt || "None given"}
  
  Provide a concise, helpful hint to guide them to the next step without giving away the full answer.
  Respond ONLY with a JSON object:
  "hint" (string)
  DO NOT use markdown tags.
  `;

  const reply = await llm.chat.completions.create({
    messages: [
      { role: "system", content: systemPrompt },
      { role: "user", content: "Provide Hint #" + stepNum + " now. Output JSON." }
    ],
    temperature: 0.3,
    max_tokens: 200,
  });

  try {
    let raw = reply.choices[0].message.content.trim();
    if (raw.startsWith("```json")) raw = raw.replace(/```json/g, "").replace(/```/g, "").trim();
    return JSON.parse(raw);
  } catch(e) {
    return { hint: "Try reviewing the core formula for this topic." };
  }
}

export async function generateLessonLocally(topicTitle) {
  const llm = await getAIEngine();
  
  const systemPrompt = `You are a brilliant calculus engine teaching a student.
  The topic is: ${topicTitle}
  
  Write a concise, engaging crash-course lesson on this topic (about 3-4 paragraphs).
  Include a clear explanation of the core concept and exactly ONE worked out example using LaTeX math formatted correctly block by block.
  Respond ONLY with the markdown format lesson, nothing else.`;

  const reply = await llm.chat.completions.create({
    messages: [
      { role: "system", content: systemPrompt },
      { role: "user", content: "Teach me this topic now." }
    ],
    temperature: 0.4,
    max_tokens: 800,
  });

  return reply.choices[0].message.content.trim();
}
