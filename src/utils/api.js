const API_BASE = 'http://localhost:8000/api';

async function fetchAPI(endpoint, options = {}) {
  const url = `${API_BASE}${endpoint}`;
  // Long timeout for slow AI endpoints; short for data fetches
  const isSlowAI = endpoint.includes('/generate') || endpoint.includes('/ai/chat')
    || endpoint.includes('/ai/hint') || endpoint.includes('/ai/explain')
    || endpoint.includes('/ai/lesson') || endpoint.includes('/ai/check-answer');
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), isSlowAI ? 120_000 : 15_000);
  try {
    const response = await fetch(url, {
      ...options,
      signal: controller.signal,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'An error occurred' }));
      throw new Error(error.detail || `HTTP ${response.status}`);
    }
    return response.json();
  } catch (err) {
    if (err.name === 'AbortError') {
      throw new Error('Request timed out — the AI may be busy. Try again.');
    }
    throw err;
  } finally {
    clearTimeout(timer);
  }
}

// Content API — built-in calculus teaching content
export const contentAPI = {
  getTopics: () => fetchAPI('/content/topics'),
  getTopic: (topicId) => fetchAPI(`/content/topic/${topicId}`),
  getProblems: (topicId) => fetchAPI(`/content/problems/${topicId}`),
  getWalkthrough: (topicId, problemIndex) =>
    fetchAPI(`/content/walkthrough/${topicId}/${problemIndex}`),
};

// AI Tutor API — GPT-powered smart tutor
export const aiAPI = {
  chat: (message, topicId = null, masteryLevel = 0.5, recentMistakes = [], problem = '', stepIndex = null, conversationHistory = null) =>
    fetchAPI('/ai/chat', {
      method: 'POST',
      body: JSON.stringify({
        message,
        topic_id: topicId,
        mastery_level: masteryLevel,
        recent_mistakes: recentMistakes,
        problem,
        step_index: stepIndex,
        conversation_history: conversationHistory,
      }),
    }),
  generateProblem: (topicId, difficulty = 'medium') =>
    fetchAPI('/ai/generate-problem', {
      method: 'POST',
      body: JSON.stringify({ topic_id: topicId, difficulty }),
    }),
  hint: (problem, hintLevel = 1, userAttempt = '') =>
    fetchAPI('/ai/hint', {
      method: 'POST',
      body: JSON.stringify({ problem, hint_level: hintLevel, user_attempt: userAttempt }),
    }),
  checkAnswer: (problem, correctAnswer, userAnswer) =>
    fetchAPI('/ai/check-answer', {
      method: 'POST',
      body: JSON.stringify({ problem, correct_answer: correctAnswer, user_answer: userAnswer }),
    }),
  explainSolution: (problem, solution) =>
    fetchAPI('/ai/explain-solution', {
      method: 'POST',
      body: JSON.stringify({ problem, solution }),
    }),
  explainConcept: (concept) => fetchAPI(`/ai/explain?concept=${encodeURIComponent(concept)}`),
  getLesson: (topicId) => fetchAPI(`/ai/lesson/${topicId}`),
  getTopics: () => fetchAPI('/ai/topics'),
  generateQuiz: (topicIds, numQuestions = 5) =>
    fetchAPI('/ai/quiz', {
      method: 'POST',
      body: JSON.stringify({ topic_ids: topicIds, num_questions: numQuestions }),
    }),
  clearHistory: () => fetchAPI('/ai/clear-history', { method: 'POST' }),
};

// Adaptive Tutor — mastery-based problem bank
export const tutorAPI = {
  getSession: (topicId, difficulty = 'medium') =>
    fetchAPI(`/tutor/session/${topicId}?difficulty=${difficulty}`),
  submitAnswer: (sessionId, answer) =>
    fetchAPI('/tutor/submit', {
      method: 'POST',
      body: JSON.stringify({ session_id: sessionId, answer }),
    }),
  getWalkthrough: (topicId, problemId) =>
    fetchAPI(`/tutor/walkthrough/${topicId}/${problemId}`),
  getFullWalkthrough: (topicId, problemId) =>
    fetchAPI(`/tutor/walkthrough-full/${topicId}/${problemId}`),
  getDiagnostic: () => fetchAPI('/tutor/diagnostic'),
  getNextProblem: (topicId) => fetchAPI(`/tutor/next-problem/${topicId}`),
};

// Progress API
export const progressAPI = {
  get: () => fetchAPI('/progress'),
  markComplete: (data) =>
    fetchAPI('/progress/complete', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
};

// Formula sheet
export const formulaAPI = {
  getAll: () => fetchAPI('/formulas'),
};

// Course data (Canvas integration)
export const courseAPI = {
  getData: () => fetchAPI('/course/data'),
  getTopics: () => fetchAPI('/course/topics'),
};

// Load curriculum from static file (works on GitHub Pages without backend)
let cachedCurriculum = null;

async function loadStaticCurriculum() {
  if (cachedCurriculum) return cachedCurriculum;
  const response = await fetch('/calc/curriculum.json');
  if (!response.ok) throw new Error('Failed to load curriculum');
  cachedCurriculum = await response.json();
  return cachedCurriculum;
}

// Personalized Curriculum API — Canvas-scraped + AI-generated
export const curriculumAPI = {
  getTopics: async () => {
    try {
      // Try backend first for real-time updates
      return await fetchAPI('/curriculum/topics');
    } catch {
      // Fall back to static file (works on GitHub Pages)
      const curriculum = await loadStaticCurriculum();
      return { topics: curriculum.topics || [] };
    }
  },
  getTopic: async (topicId) => {
    try {
      return await fetchAPI(`/curriculum/topic/${topicId}`);
    } catch {
      // Fall back to static file
      const curriculum = await loadStaticCurriculum();
      const topic = curriculum.topics?.find(t => t.id === topicId);
      if (!topic) throw new Error(`Topic ${topicId} not found`);
      return topic;
    }
  },
  getProblems: async (topicId) => {
    try {
      return await fetchAPI(`/curriculum/topic/${topicId}/problems`);
    } catch {
      // Fall back to static file
      const curriculum = await loadStaticCurriculum();
      const topic = curriculum.topics?.find(t => t.id === topicId);
      if (!topic) throw new Error(`Topic ${topicId} not found`);
      return { problems: topic.practice_problems || [] };
    }
  },
  getWalkthrough: (topicId, problemIndex) =>
    fetchAPI(`/curriculum/topic/${topicId}/problem/${problemIndex}/walkthrough`),
  generateTopic: (topicId) => fetchAPI(`/curriculum/topic/${topicId}/generate`, { method: 'POST' }),
  forceTopic: (topicId) => fetchAPI(`/curriculum/topic/${topicId}/generate?force=true`, { method: 'POST' }),
  triggerScrape: () => fetchAPI('/curriculum/scrape', { method: 'POST' }),
  getScrapeStatus: () => fetchAPI('/curriculum/scrape/status'),
};
