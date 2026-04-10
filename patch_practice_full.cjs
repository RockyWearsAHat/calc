const fs = require('fs');

let content = fs.readFileSync('src/pages/PracticeV2.jsx', 'utf-8');

// Update imports
content = content.replace(
  /import { aiAPI, tutorAPI } from '\.\.\/utils\/api';/,
  "import { curriculumAPI } from '../utils/api';"
);
content = content.replace(
  /import { generatePracticeProblem, generateChatResponse, checkAnswerLocally, generateHintLocally } from '\.\.\/utils\/localAI';/,
  "import { generatePracticeProblem, generateChatResponse, checkAnswerLocally, generateHintLocally, generateLessonLocally } from '../utils/localAI';"
);
content = content.replace(
  /import { getAccount, updateMastery } from '\.\.\/utils\/accountManager';/,
  "import { getAccount, updateMastery, getDiagnosticProgress } from '../utils/accountManager';"
);

// Fix loadInitialData
content = content.replace(
  /const loadInitialData = async \(\) => {[\s\S]*?console.error\('Failed to load data:', err\);\n    } finally {\n      setLoading\(false\);\n    }\n  };/,
  `const loadInitialData = async () => {
    try {
      const aiTopics = await curriculumAPI.getTopics();
      const diag = getDiagnosticProgress();
      setTopics(aiTopics.topics || {});
      setDiagnostic(diag);
    } catch (err) {
      console.error('Failed to load local data:', err);
    } finally {
      setLoading(false);
    }
  };`
);

// Fix loadLesson in LearnMode
content = content.replace(
  /const loadLesson = async \(\) => {[\s\S]*?console.error\('Failed to load lesson:', err\);\n    } finally {\n      setLoading\(false\);\n    }\n  };/,
  `const loadLesson = async () => {
    setLoading(true);
    try {
      const topicTitle = topic ? (topic.title || topic.name) : "Calculus";
      const lessonText = await generateLessonLocally(topicTitle);
      setLesson(lessonText);
    } catch (err) {
      console.error('Failed to load local lesson:', err);
      setLesson("Failed to generate dynamic lesson. Please try again.");
    } finally {
      setLoading(false);
    }
  };`
);

// Fix TutorMode sendMessage
content = content.replace(
  /const sendMessage = async \(\) => {[\s\S]*?setMessages\(prev => \[\.\.\.prev, { \n        role: 'assistant',\n        content: 'Sorry, I am having trouble connecting to my neural net\. Please try again later\.'\n      }\]\);\n    } finally {\n      setLoading\(false\);\n    }\n  };/,
  `const sendMessage = async () => {
    if (!input.trim() || loading) return;
    
    const userMessage = input;
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setLoading(true);
    
    try {
      const account = getAccount();
      const promptContext = "We are tutoring the student on " + (currentTopic ? currentTopic.name : "Calculus") + ". Ask guided questions, do not give out the answer. Their level is " + account.level + ".";
      const response = await generateChatResponse(userMessage, messages, promptContext);
      setMessages(prev => [...prev, { role: 'assistant', content: response }]);
    } catch (err) {
      console.error('Chat error:', err);
      setMessages(prev => [...prev, { 
        role: 'assistant',
        content: 'Sorry, my WebGPU processor is overloaded. Reconnecting...'
      }]);
    } finally {
      setLoading(false);
    }
  };`
);

// Fix clear history
content = content.replace(
  /const clearChat = \(\) => {\n    setMessages\(\[\]\);\n    try {\n      aiAPI.clearHistory\(\);\n    } catch \(e\) {\n      \/\//,
  `const clearChat = () => {
    setMessages([]);
    try {
      // Local LLM handles states completely inside messages array, 
      // no backend clear history needed.
    } catch (e) {
      //`
);

fs.writeFileSync('src/pages/PracticeV2.jsx', content);
console.log("Patched full practice module.");
