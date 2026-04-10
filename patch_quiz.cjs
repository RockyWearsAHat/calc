const fs = require('fs');

let content = fs.readFileSync('src/pages/PracticeV2.jsx', 'utf-8');

// Replace startQuiz
content = content.replace(/const startQuiz = async \(\) => {[\s\S]*?console.error\('Failed to generate quiz:', err\);\n    } finally {\n      setLoading\(false\);\n    }\n  };/,
`const startQuiz = async () => {
    if (selectedTopics.length === 0) return;
    setLoading(true);
    
    try {
      const account = getAccount();
      // Generate 5 questions by looping the local model.
      const quizProblems = [];
      const numQuestions = 5;
      
      // We pick random topics from the selected list
      for (let i = 0; i < numQuestions; i++) {
        const randomTopicId = selectedTopics[Math.floor(Math.random() * selectedTopics.length)];
        const topic = topics[randomTopicId] || { name: randomTopicId };
        const generated = await generatePracticeProblem(topic, account.level, []);
        // Save the topic on it so we know context
        generated.topic = randomTopicId;
        quizProblems.push(generated);
      }
      
      setQuiz(quizProblems);
      setAnswers([]);
      setCurrentIndex(0);
    } catch (err) {
      console.error('Failed to generate quiz locally:', err);
    } finally {
      setLoading(false);
    }
  };`);

// Replace submitAnswer for QuizMode
content = content.replace(/const submitAnswer = async \(\) => {[\s\S]*?setCurrentIndex\(prev => prev \+ 1\);\n    }\n  };/,
`const submitAnswer = async () => {
    if (!currentAnswer.trim()) return;
    
    const problem = quiz[currentIndex];
    const result = await checkAnswerLocally(problem.question, problem.answer, currentAnswer);
    
    setAnswers(prev => [...prev, {
      problem,
      userAnswer: currentAnswer,
      correct: result.is_correct,
      feedback: result.feedback
    }]);
    
    // Update mastery immediately
    if (problem.topic) {
      updateMastery(problem.topic, result.is_correct);
    }
    
    setCurrentAnswer('');
    
    if (currentIndex + 1 >= quiz.length) {
      setShowResults(true);
    } else {
      setCurrentIndex(prev => prev + 1);
    }
  };`);


fs.writeFileSync('src/pages/PracticeV2.jsx', content);
console.log("Patched startQuiz and submitAnswer.");
