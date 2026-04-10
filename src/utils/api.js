
// Static API (Decentralized WebGPU / Local Storage Mode)
// No backend required.

let cachedCurriculum = null;

async function loadStaticCurriculum() {
  if (cachedCurriculum) return cachedCurriculum;
  try {
    const response = await fetch('/calc/curriculum.json');
    if (!response.ok) throw new Error('Failed to load curriculum');
    cachedCurriculum = await response.json();
    return cachedCurriculum;
  } catch(e) {
    console.error("Static curriculum not found. Using fallback.");
    return { topics: [] };
  }
}

export const contentAPI = {
  getTopics: async () => await loadStaticCurriculum(),
  getTopic: async (id) => {
    const c = await loadStaticCurriculum();
    return c.topics.find(t => t.id === id);
  }
};

export const aiAPI = {};
export const tutorAPI = {};
export const progressAPI = {};

export const formulaAPI = {
  getAll: async () => {
    // Return some basic formulas for the formulas page so it doesn't crash
    return {
      formulas: {
        derivatives: {
          title: "Derivatives",
          formulas: [
            { name: "Power Rule", formula: "\\frac{d}{dx} x^n = nx^{n-1}" },
            { name: "Product Rule", formula: "(fg)' = f'g + fg'" },
            { name: "Quotient Rule", formula: "\\left(\\frac{f}{g}\\right)' = \\frac{f'g - fg'}{g^2}" },
            { name: "Chain Rule", formula: "\\frac{d}{dx} f(g(x)) = f'(g(x))g'(x)" }
          ]
        },
        integrals: {
          title: "Integrals",
          formulas: [
            { name: "Power Rule", formula: "\\int x^n dx = \\frac{x^{n+1}}{n+1} + C" },
            { name: "By Parts", formula: "\\int u dv = uv - \\int v du" }
          ]
        }
      }
    };
  }
};

export const courseAPI = {
  getData: async () => {
    return { modules: [], assignments: [], topics: [] };
  }
};

export const curriculumAPI = {
  getTopics: async () => {
    const curriculum = await loadStaticCurriculum();
    return { topics: curriculum.topics || [] };
  },
  getTopic: async (topicId) => {
    const curriculum = await loadStaticCurriculum();
    const topic = curriculum.topics?.find(t => t.id === topicId);
    if (!topic) throw new Error(`Topic ${topicId} not found`);
    return topic;
  },
  getProblems: async (topicId) => {
    const curriculum = await loadStaticCurriculum();
    const topic = curriculum.topics?.find(t => t.id === topicId);
    if (!topic) throw new Error(`Topic ${topicId} not found`);
    return { problems: topic.practice_problems || [] };
  },
  generateTopic: async (topicId) => {
    const curriculum = await loadStaticCurriculum();
    const topic = curriculum.topics?.find(t => t.id === topicId);
    if (!topic) throw new Error(`Topic ${topicId} not found`);
    
    // Simulate generation delay
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    return {
      ...topic,
      generated: true,
      description: `This lesson on ${topic.title} was generated locally. Advanced generation is available in the full version.`,
      concepts: [
        {
          title: `Introduction to ${topic.title}`,
          explanation: `In this section, we explore the fundamentals of ${topic.title}. As this is running purely in your browser, this is a placeholder lesson structure.`,
          formula: "f(x) = y",
          example: `Consider how ${topic.title} applies in a standard context.`
        }
      ],
      practice_problems: [
        {
          question: `What is the core idea behind ${topic.title}?`,
          answer: "The fundamentals",
          difficulty: "easy",
          walkthrough: [
            { title: "Review", content: "Review the main definition." },
            { title: "Apply", content: "Apply it to the problem." }
          ]
        }
      ]
    };
  },
  forceTopic: async (topicId) => { },
  triggerScrape: async () => { },
  getScrapeStatus: async () => { }
};
