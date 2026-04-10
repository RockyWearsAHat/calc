const fs = require('fs');

let content = fs.readFileSync('src/utils/api.js', 'utf-8');

// Completely rewrite api.js to be static only.
let newContent = `
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
            { name: "Power Rule", formula: "\\\\frac{d}{dx} x^n = nx^{n-1}" },
            { name: "Product Rule", formula: "(fg)' = f'g + fg'" },
            { name: "Quotient Rule", formula: "\\\\left(\\\\frac{f}{g}\\\\right)' = \\\\frac{f'g - fg'}{g^2}" },
            { name: "Chain Rule", formula: "\\\\frac{d}{dx} f(g(x)) = f'(g(x))g'(x)" }
          ]
        },
        integrals: {
          title: "Integrals",
          formulas: [
            { name: "Power Rule", formula: "\\\\int x^n dx = \\\\frac{x^{n+1}}{n+1} + C" },
            { name: "By Parts", formula: "\\\\int u dv = uv - \\\\int v du" }
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
    if (!topic) throw new Error(\`Topic \${topicId} not found\`);
    return topic;
  },
  getProblems: async (topicId) => {
    const curriculum = await loadStaticCurriculum();
    const topic = curriculum.topics?.find(t => t.id === topicId);
    if (!topic) throw new Error(\`Topic \${topicId} not found\`);
    return { problems: topic.practice_problems || [] };
  },
  generateTopic: async (topicId) => { },
  forceTopic: async (topicId) => { },
  triggerScrape: async () => { },
  getScrapeStatus: async () => { }
};
`;

fs.writeFileSync('src/utils/api.js', newContent);
console.log("Patched api.js.");
