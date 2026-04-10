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