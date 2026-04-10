const fs = require('fs');

let content = fs.readFileSync('src/pages/Learn.jsx', 'utf-8');

// Replace imports
content = content.replace(
  /import { curriculumAPI, aiAPI } from '\.\.\/utils\/api';/,
  "import { curriculumAPI } from '../utils/api';\nimport { generateChatResponse, checkAnswerLocally } from '../utils/localAI';"
);

// Replace aiAPI.chat
content = content.replace(
  /const resp = await aiAPI\.chat\([\s\S]*?\);\n      setMessages\(prev => \[\.\.\.prev, \{ role: 'assistant', content: resp\.response \}\]\);/,
  `// Pass via Local WebLLM
      const systemContext = "You are a helpful AI calculus tutor. The student is viewing the page context: " + context;
      const respText = await generateChatResponse(userMsg, history, systemContext);
      setMessages(prev => [...prev, { role: 'assistant', content: respText }]);`
);

// Replace aiAPI.checkAnswer
content = content.replace(
  /const r = await aiAPI\.checkAnswer\(prob\.question, prob\.answer, answer\);/,
  `const r = await checkAnswerLocally(prob.question, prob.answer, answer);`
);

fs.writeFileSync('src/pages/Learn.jsx', content);
console.log("Patched Learn.jsx.");
