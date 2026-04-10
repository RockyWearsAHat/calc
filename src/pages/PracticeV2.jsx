import { useState, useEffect, useRef } from 'react';
import { 
  Brain, Lightbulb, ChevronLeft, 
  CheckCircle, XCircle, RotateCcw, Zap, Trophy,
  ArrowRight, Play, TrendingUp, Flame, Target, MessageCircle,
  Send, Sparkles, GraduationCap, Eye,
  BookOpen, FileQuestion, Award, Clock
} from 'lucide-react';
import { curriculumAPI } from '../utils/api';
import { generatePracticeProblem, generateChatResponse, checkAnswerLocally, generateHintLocally, generateLessonLocally } from '../utils/localAI';
import { getAccount, updateMastery, getDiagnosticProgress } from '../utils/accountManager';
import MathMarkdown from '../components/MathMarkdown';
import MathInput from '../components/MathInput';
import styles from './PracticeV2.module.css';

// Learning Mode Selection
function ModeSelector({ onSelect }) {
  const modes = [
    {
      id: 'learn',
      icon: GraduationCap,
      title: 'Learn First',
      description: 'Read a lesson, then practice with problems',
      eyebrow: 'Guided runway',
      detail: 'Lesson + drills',
      color: '#7be0a9'
    },
    {
      id: 'practice',
      icon: Target,
      title: 'Practice',
      description: 'Jump straight into problems with AI hints',
      eyebrow: 'Adaptive reps',
      detail: 'Hints + feedback',
      color: '#6cb6ff'
    },
    {
      id: 'quiz',
      icon: FileQuestion,
      title: 'Quiz Mode',
      description: 'Test yourself across multiple topics',
      eyebrow: 'Pressure test',
      detail: 'Cross-topic check',
      color: '#d8c08f'
    },
    {
      id: 'tutor',
      icon: MessageCircle,
      title: 'Ask the Tutor',
      description: 'Chat with AI about any calculus concept',
      eyebrow: 'Live help',
      detail: 'Explain any block',
      color: '#95c9ff'
    }
  ];

  return (
    <div className={styles.modeSelector}>
      <h2 className={styles.modeSelectorTitle}>Choose your study mode</h2>
      <p className={styles.modeSelectorIntro}>
        Four focused entry points, each tuned for a different kind of momentum.
      </p>
      <div className={styles.modeGrid}>
        {modes.map((mode, index) => (
          <button
            key={mode.id}
            className={styles.modeCard}
            onClick={() => onSelect(mode.id)}
            style={{ '--mode-color': mode.color }}
          >
            <div className={styles.modeCardTop}>
              <span className={styles.modePill}>{mode.eyebrow}</span>
              <span className={styles.modeIndex}>0{index + 1}</span>
            </div>
            <mode.icon size={32} className={styles.modeIcon} />
            <div className={styles.modeCardBody}>
              <h3>{mode.title}</h3>
              <p>{mode.description}</p>
            </div>
            <div className={styles.modeCardFoot}>
              <span>{mode.detail}</span>
              <ArrowRight size={18} />
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}

// Topic Selector Component
function TopicSelector({ topics, diagnostic, onSelect, onBack }) {
  return (
    <div className={styles.topicSelector}>
      <button className={styles.backBtn} onClick={onBack}>
        <ChevronLeft size={20} /> Back
      </button>
      
      <h2>Select a Topic</h2>
      
      <div className={styles.topicGrid}>
        {Object.entries(topics).map(([id, topic]) => {
          const progress = diagnostic?.topics?.find(t => t.id === id);
          const mastery = progress?.mastery || 0;
          
          return (
            <button
              key={id}
              className={styles.topicCard}
              onClick={() => onSelect(id, topic)}
            >
              <div className={styles.topicHeader}>
                <h3>{topic.name}</h3>
                {mastery > 0.8 && <Trophy size={18} className={styles.trophyIcon} />}
              </div>
              
              <div className={styles.topicFormula}>{topic.formula}</div>
              
              <div className={styles.topicProgress}>
                <div 
                  className={styles.topicProgressBar}
                  style={{ width: `${mastery * 100}%` }}
                />
              </div>
              <span className={styles.topicMastery}>{Math.round(mastery * 100)}% mastery</span>
            </button>
          );
        })}
      </div>
    </div>
  );
}

// Learn Mode - Shows lesson then practice
function LearnMode({ topic, topicId, onBack, onPractice }) {
  const [lesson, setLesson] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showPractice, setShowPractice] = useState(false);

  useEffect(() => {
    loadLesson();
  }, [topicId]);

  const loadLesson = async () => {
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
  };

  if (loading) {
    return (
      <div className={styles.loadingContainer}>
        <div className={styles.loadingSpinner}>
          <Sparkles size={32} />
        </div>
        <p>Generating your personalized lesson...</p>
        <span className={styles.loadingNote}>Using AI to create comprehensive explanations</span>
      </div>
    );
  }

  return (
    <div className={styles.learnMode}>
      <div className={styles.learnHeader}>
        <button className={styles.backBtn} onClick={onBack}>
          <ChevronLeft size={20} /> Back
        </button>
        <h1>{topic.name}</h1>
        <button 
          className={styles.practiceBtn}
          onClick={() => onPractice(topicId)}
        >
          <Play size={18} /> Practice This
        </button>
      </div>

      <div className={styles.lessonContent}>
        <MathMarkdown>{lesson}</MathMarkdown>
      </div>

      <div className={styles.lessonFooter}>
        <button 
          className={styles.startPracticeBtn}
          onClick={() => onPractice(topicId)}
        >
          <Target size={20} />
          Ready to Practice?
          <ArrowRight size={20} />
        </button>
      </div>
    </div>
  );
}

// Practice Mode - AI-powered problems with hints
function PracticeMode({ topic, topicId, onBack, diagnostic }) {
  const [problem, setProblem] = useState(null);
  const [loading, setLoading] = useState(true);
  const [answer, setAnswer] = useState('');
  const [hints, setHints] = useState([]);
  const [hintLoading, setHintLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [wrongAnswers, setWrongAnswers] = useState([]);
  const [explanation, setExplanation] = useState(null);
  const [showExplanation, setShowExplanation] = useState(false);
  const [difficulty, setDifficulty] = useState(1);
  const [streak, setStreak] = useState(0);
  const [problemsAttempted, setProblemsAttempted] = useState(0);
  const [problemsCorrect, setProblemsCorrect] = useState(0);

  useEffect(() => {
    generateNewProblem();
  }, [topicId, difficulty]);

  const generateNewProblem = async () => {
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
  };

  const getHint = async () => {
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
  };

  const checkAnswer = async () => {
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
  };

  const showSolution = async () => {
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
  };

  const nextProblem = () => {
    generateNewProblem();
  };

  if (loading) {
    return (
      <div className={styles.loadingContainer}>
        <div className={styles.loadingSpinner}>
          <Target size={32} />
        </div>
        <p>Generating a problem for you...</p>
      </div>
    );
  }

  return (
    <div className={styles.practiceMode}>
      <div className={styles.practiceHeader}>
        <button className={styles.backBtn} onClick={onBack}>
          <ChevronLeft size={20} /> Back
        </button>
        
        <div className={styles.practiceInfo}>
          <h1>{topic.name}</h1>
          <div className={styles.difficultyBadge} data-level={difficulty}>
            Level {difficulty}
          </div>
        </div>
        
        <div className={styles.practiceStats}>
          {streak > 0 && (
            <span className={styles.streakBadge}>
              <Flame size={16} /> {streak} streak
            </span>
          )}
          <span className={styles.scoreBadge}>
            {problemsCorrect}/{problemsAttempted}
          </span>
        </div>
      </div>

      {problem && (
        <div className={styles.problemArea}>
          <div className={styles.problemCard}>
            <div className={styles.problemMeta}>
              <span className={styles.problemMetaLabel}>Current prompt</span>
              <span className={styles.problemMetaValue}>{topic.formula || 'Adaptive practice stream'}</span>
            </div>
            <div className={styles.problemQuestion}>
              <MathMarkdown>{problem.question}</MathMarkdown>
            </div>
          </div>

          {/* Hints display */}
          {hints.length > 0 && (
            <div className={styles.hintsArea}>
              {hints.map((hint, i) => (
                <div key={i} className={styles.hintCard}>
                  <div className={styles.hintHeader}>
                    <Lightbulb size={16} />
                    Hint {i + 1}
                  </div>
                  <MathMarkdown>{hint}</MathMarkdown>
                </div>
              ))}
            </div>
          )}

          {/* Answer area */}
          {!result && (
            <div className={styles.answerArea}>
              <label className={styles.answerLabel} htmlFor="practice-answer">Your answer</label>
              <MathInput
                id="practice-answer"
                className={styles.answerInput}
                value={answer}
                onChange={(e) => setAnswer(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && checkAnswer()}
                placeholder="Type math: x^2, a/b, sqrt(x)..."
                autoFocus
              />
              
              <div className={styles.actionRow}>
                <button 
                  className={styles.checkBtn}
                  onClick={checkAnswer}
                  disabled={!answer.trim()}
                >
                  <CheckCircle size={18} /> Check Answer
                </button>
                
                <div className={styles.helpBtns}>
                  <button 
                    className={styles.hintBtn}
                    onClick={getHint}
                    disabled={hintLoading}
                  >
                    <Lightbulb size={16} />
                    {hintLoading ? 'Getting hint...' : hints.length > 0 ? 'Another Hint' : 'Get a Hint'}
                  </button>
                  
                  <button 
                    className={styles.solveBtn}
                    onClick={showSolution}
                  >
                    <Eye size={16} /> Show Solution
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* Result display */}
          {result && (
            <div className={`${styles.resultCard} ${result.is_correct ? styles.correct : styles.incorrect}`}>
              <div className={styles.resultHeader}>
                {result.is_correct ? (
                  <>
                    <CheckCircle size={28} />
                    <span>Correct!</span>
                    {streak > 1 && <span className={styles.streakNote}>{streak} in a row!</span>}
                  </>
                ) : (
                  <>
                    <XCircle size={28} />
                    <span>Not quite</span>
                  </>
                )}
              </div>
              
              <div className={styles.resultFeedback}>
                <MathMarkdown>{result.feedback}</MathMarkdown>
              </div>
              
              {!result.is_correct && (
                <div className={styles.correctAnswer}>
                  <strong>Correct answer:</strong> {problem.answer}
                </div>
              )}
              
              {/* Explanation toggle */}
              {!showExplanation ? (
                <button 
                  className={styles.explainBtn}
                  onClick={showSolution}
                >
                  <BookOpen size={16} /> Explain this step-by-step
                </button>
              ) : explanation && (
                <div className={styles.explanationArea}>
                  <h4><GraduationCap size={16} /> Full Solution</h4>
                  <MathMarkdown>{explanation}</MathMarkdown>
                </div>
              )}
              
              <div className={styles.resultActions}>
                <button className={styles.nextBtn} onClick={nextProblem}>
                  <ArrowRight size={18} /> Next Problem
                </button>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

// Chat Tutor Mode - Free-form conversation
function TutorMode({ topics, onBack }) {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: "Hi! I'm your Calculus II tutor. Ask me anything about integration, series, polar coordinates, or any other topic. I can explain concepts, work through examples, or check your answers — I'll tell you straight if you got it right. What do you want to work on?" }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [currentTopic, setCurrentTopic] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim() || loading) return;
    
    const userMessage = input.trim();
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setLoading(true);
    
    try {
      const account = getAccount();
      const promptContext = "We are tutoring the student on " + (currentTopic ? (currentTopic.title || currentTopic.name) : "Calculus") + ". Ask guided questions, do not give out the answer. Their level is " + account.level + ".";
      const response = await generateChatResponse(userMessage, messages, promptContext);
      setMessages(prev => [...prev, { role: 'assistant', content: response }]);
    } catch (err) {
      console.error('Chat error:', err);
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: "Sorry, my WebGPU processor is overloaded. Reconnecting..." 
      }]);
    } finally {
      setLoading(false);
    }
  };

  const quickQuestions = [
    "Explain integration by parts",
    "When do I use partial fractions?",
    "What is the ratio test?",
    "How do Taylor series work?",
    "Explain polar coordinates"
  ];

  return (
    <div className={styles.tutorMode}>
      <div className={styles.tutorHeader}>
        <button className={styles.backBtn} onClick={onBack}>
          <ChevronLeft size={20} /> Back
        </button>
        <h1><MessageCircle size={24} /> AI Calculus Tutor</h1>
        <button 
          className={styles.clearBtn}
          onClick={() => {

            setMessages([{ role: 'assistant', content: "Chat cleared! What would you like to learn about?" }]);
          }}
        >
          <RotateCcw size={16} /> Clear
        </button>
      </div>

      {/* Quick questions */}
      <div className={styles.quickQuestions}>
        {quickQuestions.map((q, i) => (
          <button 
            key={i}
            className={styles.quickQuestion}
            onClick={() => setInput(q)}
          >
            {q}
          </button>
        ))}
      </div>

      {/* Chat messages */}
      <div className={styles.chatMessages}>
        {messages.map((msg, i) => (
          <div 
            key={i} 
            className={`${styles.chatMessage} ${styles[msg.role]}`}
          >
            <div className={styles.messageAvatar}>
              {msg.role === 'assistant' ? <Brain size={20} /> : <span>You</span>}
            </div>
            <div className={styles.messageContent}>
              <MathMarkdown>{msg.content}</MathMarkdown>
            </div>
          </div>
        ))}
        {loading && (
          <div className={`${styles.chatMessage} ${styles.assistant}`}>
            <div className={styles.messageAvatar}><Brain size={20} /></div>
            <div className={styles.messageContent}>
              <div className={styles.typingIndicator}>
                <span></span><span></span><span></span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input area */}
      <div className={styles.chatInputArea}>
        <input
          type="text"
          className={styles.chatInput}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
          placeholder="Ask anything about Calculus II..."
          disabled={loading}
        />
        <button 
          className={styles.sendBtn}
          onClick={sendMessage}
          disabled={!input.trim() || loading}
        >
          <Send size={20} />
        </button>
      </div>
    </div>
  );
}

// Quiz Mode - Test across multiple topics
function QuizMode({ topics, onBack }) {
  const [selectedTopics, setSelectedTopics] = useState([]);
  const [quiz, setQuiz] = useState(null);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState([]);
  const [currentAnswer, setCurrentAnswer] = useState('');
  const [showResults, setShowResults] = useState(false);
  const [loading, setLoading] = useState(false);

  const toggleTopic = (topicId) => {
    setSelectedTopics(prev => 
      prev.includes(topicId) 
        ? prev.filter(t => t !== topicId)
        : [...prev, topicId]
    );
  };

  const startQuiz = async () => {
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
  };

  const submitAnswer = async () => {
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
  };

  // Topic selection
  if (!quiz) {
    return (
      <div className={styles.quizSetup}>
        <button className={styles.backBtn} onClick={onBack}>
          <ChevronLeft size={20} /> Back
        </button>
        
        <h1>Quiz Mode</h1>
        <p>Select the topics you want to be tested on:</p>
        
        <div className={styles.topicCheckboxes}>
          {Object.entries(topics).map(([id, topic]) => (
            <label key={id} className={styles.topicCheckbox}>
              <input
                type="checkbox"
                checked={selectedTopics.includes(id)}
                onChange={() => toggleTopic(id)}
              />
              <span>{topic.name}</span>
            </label>
          ))}
        </div>
        
        <button 
          className={styles.startQuizBtn}
          onClick={startQuiz}
          disabled={selectedTopics.length === 0 || loading}
        >
          {loading ? 'Generating Quiz...' : `Start Quiz (${selectedTopics.length} topics)`}
        </button>
      </div>
    );
  }

  // Results
  if (showResults) {
    const score = answers.filter(a => a.correct).length;
    return (
      <div className={styles.quizResults}>
        <h1>Quiz Complete!</h1>
        
        <div className={styles.scoreDisplay}>
          <Award size={48} />
          <span className={styles.scoreNumber}>{score}/{quiz.length}</span>
          <span className={styles.scorePercent}>{Math.round(score / quiz.length * 100)}%</span>
        </div>
        
        <div className={styles.resultsReview}>
          {answers.map((a, i) => (
            <div key={i} className={`${styles.resultItem} ${a.correct ? styles.correct : styles.incorrect}`}>
              <div className={styles.resultIcon}>
                {a.correct ? <CheckCircle size={20} /> : <XCircle size={20} />}
              </div>
              <div className={styles.resultContent}>
                <MathMarkdown>{a.problem.question}</MathMarkdown>
                <div className={styles.resultAnswer}>
                  Your answer: <strong>{a.userAnswer}</strong>
                  {!a.correct && <> | Correct: <strong>{a.problem.answer}</strong></>}
                </div>
              </div>
            </div>
          ))}
        </div>
        
        <div className={styles.quizActions}>
          <button className={styles.quizActionBtn} onClick={() => { setQuiz(null); setShowResults(false); setAnswers([]); setCurrentIndex(0); }}>
            New Quiz
          </button>
          <button className={styles.quizActionBtn} onClick={onBack}>
            Back to Menu
          </button>
        </div>
      </div>
    );
  }

  // Active quiz
  const currentProblem = quiz[currentIndex];
  return (
    <div className={styles.activeQuiz}>
      <div className={styles.quizProgress}>
        <span>Question {currentIndex + 1} of {quiz.length}</span>
        <div className={styles.quizProgressBar}>
          <div style={{ width: `${(currentIndex / quiz.length) * 100}%` }} />
        </div>
      </div>
      
      <div className={styles.quizQuestion}>
        <MathMarkdown>{currentProblem.question}</MathMarkdown>
      </div>
      
      <div className={styles.quizAnswerArea}>
        <MathInput
          className={styles.quizInput}
          value={currentAnswer}
          onChange={(e) => setCurrentAnswer(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && submitAnswer()}
          placeholder="Type math: x^2, a/b, sqrt(x)..."
          autoFocus
        />
        <button className={styles.quizSubmitBtn} onClick={submitAnswer} disabled={!currentAnswer.trim()}>
          Submit <ArrowRight size={16} />
        </button>
      </div>
    </div>
  );
}

// Main Practice Component
export default function PracticeV2() {
  const [mode, setMode] = useState(null); // 'learn', 'practice', 'quiz', 'tutor'
  const [topics, setTopics] = useState({});
  const [diagnostic, setDiagnostic] = useState(null);
  const [selectedTopic, setSelectedTopic] = useState(null);
  const [selectedTopicData, setSelectedTopicData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadInitialData();
  }, []);

  const loadInitialData = async () => {
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
  };

  const handleModeSelect = (selectedMode) => {
    setMode(selectedMode);
    if (selectedMode === 'tutor') {
      setSelectedTopic(null);
    }
  };

  const handleTopicSelect = (topicId, topicData) => {
    setSelectedTopic(topicId);
    setSelectedTopicData(topicData);
  };

  const goBack = () => {
    if (selectedTopic) {
      setSelectedTopic(null);
      setSelectedTopicData(null);
    } else {
      setMode(null);
    }
  };

  const overallProgress = Math.round((diagnostic?.overall_progress || 0) * 100);
  const masteredTopics = diagnostic?.topics?.filter(t => t.status === 'mastered').length || 0;
  const currentStreak = diagnostic?.streak || 0;

  if (loading) {
    return (
      <div className={styles.page}>
        <div className={styles.loadingContainer}>
          <div className={styles.loadingSpinner}>
            <Brain size={48} />
          </div>
          <p>Loading your study session...</p>
        </div>
      </div>
    );
  }

  return (
    <div className={styles.page}>
      {/* No mode selected - show mode selector */}
      {!mode && (
        <>
          <section className={styles.pageHero}>
            <div className={styles.pageHeader}>
              <div className={styles.pageEyebrowRow}>
                <span className={styles.pageEyebrow}>Practice cockpit</span>
                <span className={diagnostic ? styles.pageStatusLive : styles.pageStatusIdle}>
                  <span className={styles.pageStatusDot} />
                  {diagnostic ? 'Telemetry synced' : 'Tutor network online'}
                </span>
              </div>
              <h1><Sparkles size={32} /> Train calculus like a precision instrument.</h1>
              <p>
                Switch between guided lessons, targeted drills, quiz runs, and live tutoring
                inside a calmer study surface that keeps the next move obvious.
              </p>
              <div className={styles.pageSignals}>
                <div className={styles.pageSignal}>
                  <TrendingUp size={16} />
                  Mastery telemetry
                </div>
                <div className={styles.pageSignal}>
                  <Zap size={16} />
                  Adaptive AI hints
                </div>
                <div className={styles.pageSignal}>
                  <Clock size={16} />
                  Session-based practice
                </div>
              </div>
            </div>

            <div className={styles.pageHeroConsole}>
              <div className={styles.heroReadout}>
                <span className={styles.heroReadoutEyebrow}>Session engine</span>
                <strong>{diagnostic ? 'Ready for deliberate reps' : 'Tutor systems online'}</strong>
                <p>
                  {diagnostic
                    ? 'Your progress model is loaded, difficulty can adapt, and every mode shares the same study state.'
                    : 'Topic data is ready. Start anywhere and let the tutor surface the next useful move.'}
                </p>

                <div className={styles.heroMeterRow}>
                  <span>Mastery load</span>
                  <span>{diagnostic ? `${overallProgress}%` : 'Live'}</span>
                </div>
                <div className={styles.heroMeter}>
                  <span style={{ width: `${diagnostic ? Math.max(overallProgress, 18) : 62}%` }} />
                </div>

                <div className={styles.heroMiniStats}>
                  <div className={styles.heroMiniStat}>
                    <span>Mastered</span>
                    <strong>{masteredTopics}</strong>
                  </div>
                  <div className={styles.heroMiniStat}>
                    <span>Streak</span>
                    <strong>{currentStreak}</strong>
                  </div>
                </div>
              </div>
            </div>
          </section>

          <div className={styles.modeSection}>
            <ModeSelector onSelect={handleModeSelect} />
          </div>
          
          {diagnostic && (
            <div className={styles.quickStats}>
              <div className={styles.stat}>
                <span className={styles.statValue}>{overallProgress}%</span>
                <span className={styles.statLabel}>Overall Mastery</span>
              </div>
              <div className={styles.stat}>
                <span className={styles.statValue}>{masteredTopics}</span>
                <span className={styles.statLabel}>Topics Mastered</span>
              </div>
              <div className={styles.stat}>
                <span className={styles.statValue}>{currentStreak}</span>
                <span className={styles.statLabel}>Current Streak</span>
              </div>
            </div>
          )}
        </>
      )}

      {/* Tutor mode - no topic selection needed */}
      {mode === 'tutor' && (
        <TutorMode topics={topics} onBack={() => setMode(null)} />
      )}

      {/* Quiz mode - has its own topic selection */}
      {mode === 'quiz' && (
        <QuizMode topics={topics} onBack={() => setMode(null)} />
      )}

      {/* Learn or Practice mode - needs topic selection */}
      {(mode === 'learn' || mode === 'practice') && !selectedTopic && (
        <TopicSelector 
          topics={topics}
          diagnostic={diagnostic}
          onSelect={handleTopicSelect}
          onBack={() => setMode(null)}
        />
      )}

      {/* Learn mode with topic selected */}
      {mode === 'learn' && selectedTopic && (
        <LearnMode 
          topic={selectedTopicData}
          topicId={selectedTopic}
          onBack={goBack}
          onPractice={(topicId) => {
            setMode('practice');
          }}
        />
      )}

      {/* Practice mode with topic selected */}
      {mode === 'practice' && selectedTopic && (
        <PracticeMode 
          topic={selectedTopicData}
          topicId={selectedTopic}
          diagnostic={diagnostic}
          onBack={goBack}
        />
      )}
    </div>
  );
}
