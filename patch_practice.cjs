const fs = require('fs');

let content = fs.readFileSync('src/pages/PracticeV2.jsx', 'utf-8');

content = content.replace(/const generateNewProblem = async \(\) => {[\s\S]*?setLoading\(false\);\n    }\n  };/, 
`const generateNewProblem = async () => {
    setLoading(true);
    setProblem(null);
    setAnswer('');
    setHints([]);
    setResult(null);
    setWrongAnswers([]);
    setExplanation(null);
    setShowExplanation(false);
    
    try {
      const account = getAccount();
      // Try AI-generated problem locally using the WebGPU LLC engine
      const generated = await generatePracticeProblem(topic, Math.max(1, account.level + difficulty - 1), []);
      setProblem(generated);
    } catch (err) {
      console.error('Failed to generate problem:', err);
    } finally {
      setLoading(false);
    }
  };`);

content = content.replace(/const getHint = async \(\) => {[\s\S]*?setHintLoading\(false\);\n    }\n  };/,
`const getHint = async () => {
    if (!problem) return;
    setHintLoading(true);
    
    try {
      const data = await generateHintLocally(problem.question, hints.length + 1, answer);
      if (data.hint) {
        setHints(prev => [...prev, data.hint]);
      }
    } catch (err) {
      console.error('Failed to get hint:', err);
    } finally {
      setHintLoading(false);
    }
  };`);

content = content.replace(/const checkAnswer = async \(\) => {[\s\S]*?console.error\('Failed to check answer:', err\);\n    }\n  };/,
`const checkAnswer = async () => {
    if (!problem || !answer.trim()) return;
    
    try {
      const data = await checkAnswerLocally(problem.question, problem.answer, answer);
      setResult(data);
      setProblemsAttempted(prev => prev + 1);
      
      if (data.is_correct) {
        setStreak(prev => {
          const newStreak = prev + 1;
          if (newStreak % 3 === 0) {
            setDifficulty(d => Math.min(3, d + 1));
          }
          return newStreak;
        });
        setProblemsCorrect(prev => prev + 1);
        updateMastery(topicId, true);
      } else {
        setStreak(0);
        setWrongAnswers(prev => {
          const updated = [...prev, answer];
          if (updated.length >= 2) {
            setDifficulty(d => Math.max(1, d - 1));
          }
          return updated;
        });
        updateMastery(topicId, false);
      }
    } catch (err) {
      console.error('Failed to check answer:', err);
    }
  };`);

content = content.replace(/const showSolution = async \(\) => {[\s\S]*?console.error\('Failed to get solution:', err\);\n    }\n  };/,
`const showSolution = async () => {
    if (!problem) return;
    setShowExplanation(true);
    
    try {
      if (problem.explanation) {
        setExplanation(problem.explanation);
      } else {
        setExplanation("The mecha-copilot LLM did not provide an explanation.");
      }
    } catch (err) {
      console.error('Failed to get solution:', err);
    }
  };`);

fs.writeFileSync('src/pages/PracticeV2.jsx', content);
console.log("Patched PracticeV2.");
