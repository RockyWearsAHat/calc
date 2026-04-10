import { useState, useEffect, useRef } from 'react';
import { BookOpen, ChevronDown, MessageCircle, X,
         Send, Loader2, CheckCircle, ArrowRight, ArrowLeft,
         Sparkles, GraduationCap, Calculator, AlertCircle, RefreshCw, Zap } from 'lucide-react';
import { useParams } from 'react-router-dom';
import { curriculumAPI } from '../utils/api';
import { generateChatResponse, checkAnswerLocally } from '../utils/localAI';
import { useLocalStorage } from '../hooks/useAPI';
import MathMarkdown from '../components/MathMarkdown';
import MathInput from '../components/MathInput';
import styles from './Learn.module.css';

function TopicSidebar({ topics, selectedId, onSelect, progress, topicsError }) {
  const [openSection, setOpenSection] = useState({ 1: true, 2: false });
  const calc1 = topics.filter(t => t.calc_level === 1);
  const calc2 = topics.filter(t => t.calc_level === 2);

  function Section({ level, label, items }) {
    const isOpen = openSection[level];
    return (
      <div className={styles.sidebarSection}>
        <button
          className={styles.sidebarSectionHeader}
          onClick={() => setOpenSection(p => ({ ...p, [level]: !p[level] }))}
        >
          <span className={styles.sectionLabel}>{label}</span>
          <ChevronDown size={14} className={isOpen ? styles.chevronOpen : styles.chevronClosed} />
        </button>
        {isOpen && (
          <ul className={styles.topicList}>
            {items.map(t => {
              const done = progress[t.id]?.conceptsDone === true;
              const started = !done && progress[t.id] !== undefined;
              return (
                <li key={t.id}>
                  <button
                    className={`${styles.topicItem} ${selectedId === t.id ? styles.topicActive : ''}`}
                    onClick={() => onSelect(t.id)}
                  >
                    <span className={styles.topicSection}>{t.id}</span>
                    <span className={styles.topicTitle}>{t.title}</span>
                    {done && <CheckCircle size={12} className={styles.topicDone} />}
                    {started && <span className={styles.topicStarted} title="In progress" />}
                  </button>
                </li>
              );
            })}
          </ul>
        )}
      </div>
    );
  }

  return (
    <nav className={styles.sidebar}>
      <div className={styles.sidebarHeader}>
        <BookOpen size={16} />
        <span>All Topics</span>
      </div>
      {topicsError && <div className={styles.sidebarError}>{topicsError}</div>}
      <div className={styles.sidebarScroll}>
        {calc1.length > 0 && <Section level={1} label={`Calculus I (${calc1.length})`} items={calc1} />}
        {calc2.length > 0 && <Section level={2} label={`Calculus II (${calc2.length})`} items={calc2} />}
      </div>
    </nav>
  );
}


function ConceptPanel({ concept, index, total }) {
  return (
    <div className={styles.conceptCard}>
      <div className={styles.conceptHeader}>
        <span className={styles.conceptNum}>{index + 1} of {total}</span>
        <h3><MathMarkdown>{concept.title}</MathMarkdown></h3>
      </div>
      <div className={styles.conceptBody}>
        <MathMarkdown>{concept.explanation}</MathMarkdown>
        {concept.formula && (
          <div className={styles.formulaBox}>
            <span className={styles.formulaLabel}>Formula</span>
            <MathMarkdown formula>{concept.formula}</MathMarkdown>
          </div>
        )}
        {concept.example && (
          <div className={styles.exampleBox}>
            <span className={styles.exampleLabel}>Worked Example</span>
            <MathMarkdown>{concept.example}</MathMarkdown>
          </div>
        )}
      </div>
    </div>
  );
}


function WalkthroughPanel({ problem, stepIndex, onStep, onClose }) {
  const steps = problem.walkthrough || [];
  const step = steps[stepIndex];
  if (!steps.length) return null;

  return (
    <div className={styles.walkthroughPanel}>
      <div className={styles.walkthroughHeader}>
        <span className={styles.walkthroughTitle}>Step-by-Step Walkthrough</span>
        <button className={styles.iconBtn} onClick={onClose}><X size={16} /></button>
      </div>

      <div className={styles.walkthroughProgress}>
        {steps.map((s, i) => (
          <button
            key={i}
            className={`${styles.stepDot} ${i < stepIndex ? styles.stepDone : ''} ${i === stepIndex ? styles.stepActive : ''}`}
            onClick={() => onStep(i)}
            title={s.title}
          />
        ))}
      </div>

      {step && (
        <div className={styles.stepContent}>
          <div className={styles.stepHeader}>
            <span className={styles.stepNum}>Step {stepIndex + 1} of {steps.length}</span>
            <h4><MathMarkdown>{step.title}</MathMarkdown></h4>
          </div>
          <div className={styles.stepBody}>
            <MathMarkdown>{step.content}</MathMarkdown>
            {step.formula && (
              <div className={styles.formulaBox}>
                <MathMarkdown formula>{step.formula}</MathMarkdown>
              </div>
            )}
          </div>
        </div>
      )}

      <div className={styles.walkthroughNav}>
        <button
          className={styles.navBtn}
          onClick={() => onStep(Math.max(0, stepIndex - 1))}
          disabled={stepIndex === 0}
        >
          <ArrowLeft size={16} /> Previous
        </button>
        <span className={styles.stepCounter}>{stepIndex + 1} / {steps.length}</span>
        <button
          className={`${styles.navBtn} ${styles.navBtnPrimary}`}
          onClick={() => onStep(Math.min(steps.length - 1, stepIndex + 1))}
          disabled={stepIndex === steps.length - 1}
        >
          Next <ArrowRight size={16} />
        </button>
      </div>
    </div>
  );
}


function ChatPanel({ topicId, topicTitle, problem, stepIndex, currentConcept, currentTab, onClose }) {
  const welcomeMsg = (() => {
    if (currentConcept) {
      return `Hi! I'm your tutor for **${topicTitle}**. You're viewing **"${currentConcept.title}"** — ask me anything about this concept, the formula, or the worked example.`;
    }
    if (problem) {
      return `Hi! I'm your tutor for **${topicTitle}**. I can see the practice problem you're working on — ask me anything! I'll guide your thinking, not just hand over the answer.`;
    }
    return `Hi! I'm your personal tutor for **${topicTitle}**. Ask me anything about the concepts or practice problems!`;
  })();

  const [messages, setMessages] = useState([{ role: 'assistant', content: welcomeMsg }]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  async function send() {
    if (!input.trim() || loading) return;
    const userMsg = input.trim();
    setInput('');
    const updatedMessages = [...messages, { role: 'user', content: userMsg }];
    setMessages(updatedMessages);
    setLoading(true);
    try {
      const contextParts = [`Topic: ${topicId} - ${topicTitle}`];
      if (currentTab === 'learn' && currentConcept) {
        contextParts.push(`Student is viewing concept: "${currentConcept.title}"`);
        if (currentConcept.explanation) contextParts.push(`Concept explanation: ${currentConcept.explanation}`);
        if (currentConcept.formula) contextParts.push(`Formula: ${currentConcept.formula}`);
        if (currentConcept.example) contextParts.push(`Worked example: ${currentConcept.example}`);
      }
      if (problem) {
        contextParts.push(`Practice problem: ${problem.question}`);
        if (problem.answer) contextParts.push(`Expected answer: ${problem.answer}`);
      }
      if (stepIndex !== null && problem?.walkthrough?.[stepIndex]) {
        const step = problem.walkthrough[stepIndex];
        contextParts.push(`Viewing walkthrough step ${stepIndex + 1}: "${step.title}" — ${step.content}`);
        if (step.formula) contextParts.push(`Step formula: ${step.formula}`);
      }
      const context = contextParts.join('. ');
      // Pass conversation history (exclude the system welcome message)
      const history = updatedMessages
        .filter((m, i) => i > 0)
        .map(m => ({ role: m.role, content: m.content }));
      // Pass via Local WebLLM
      const systemContext = "You are a helpful AI calculus tutor. The student is viewing the page context: " + context;
      const respText = await generateChatResponse(userMsg, history, systemContext);
      setMessages(prev => [...prev, { role: 'assistant', content: respText }]);
    } catch {
      setMessages(prev => [...prev, { role: 'assistant', content: 'Sorry, something went wrong. Try again.' }]);
    } finally {
      setLoading(false);
    }
  }

  const chips = currentConcept ? [
    `Explain "${currentConcept.title}" in simple terms`,
    'What is the key formula?',
    'Show a different example',
    'What are common mistakes here?',
  ] : [
    'Can you explain this differently?',
    'What is the key formula?',
    'Show me a simpler example',
    'What are common mistakes?',
  ];

  const contextLabel = currentConcept
    ? currentConcept.title
    : problem
    ? 'Practice Problem'
    : topicTitle;

  return (
    <div className={styles.chatPanel}>
      <div className={styles.chatHeader}>
        <div className={styles.chatTitle}>
          <MessageCircle size={16} />
          <span>AI Tutor</span>
        </div>
        <span className={styles.chatContextPill}>{contextLabel}</span>
        <button className={styles.iconBtn} onClick={onClose}><X size={16} /></button>
      </div>

      <div className={styles.chatMessages}>
        {messages.map((m, i) => (
          <div key={i} className={`${styles.chatMsg} ${m.role === 'user' ? styles.chatMsgUser : styles.chatMsgBot}`}>
            <div className={styles.chatBubble}>
              <MathMarkdown>{m.content}</MathMarkdown>
            </div>
          </div>
        ))}
        {loading && (
          <div className={`${styles.chatMsg} ${styles.chatMsgBot}`}>
            <div className={`${styles.chatBubble} ${styles.chatTyping}`}>
              <span /><span /><span />
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {messages.length < 3 && (
        <div className={styles.chatChips}>
          {chips.map(c => (
            <button key={c} className={styles.chip} onClick={() => setInput(c)}>
              {c}
            </button>
          ))}
        </div>
      )}

      <div className={styles.chatInput}>
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && !e.shiftKey && send()}
          placeholder="Ask anything about this topic..."
          className={styles.chatInputField}
        />
        <button className={styles.chatSendBtn} onClick={send} disabled={loading || !input.trim()}>
          <Send size={16} />
        </button>
      </div>
    </div>
  );
}


function PracticeTab({ problems, topicId, topicTitle, onProblemChange, onStepChange }) {
  const [current, setCurrent] = useState(0);
  const [answer, setAnswer] = useState('');
  const [result, setResult] = useState(null);
  const [checking, setChecking] = useState(false);
  const [showWalkthrough, setShowWalkthrough] = useState(false);
  const [stepIndex, setStepIndex] = useState(0);
  const [showChat, setShowChat] = useState(false);

  const prob = problems[current];

  // Notify parent of current problem context (for top-level chat panel)
  useEffect(() => { onProblemChange?.(prob || null); }, [current, problems]);
  useEffect(() => { onStepChange?.(showWalkthrough ? stepIndex : null); }, [stepIndex, showWalkthrough]);

  function next() { setCurrent(i => Math.min(problems.length - 1, i + 1)); reset(); }
  function prev() { setCurrent(i => Math.max(0, i - 1)); reset(); }
  function reset() {
    setAnswer(''); setResult(null); setShowWalkthrough(false); setStepIndex(0);
    onStepChange?.(null);
  }

  async function checkAnswer() {
    if (!answer.trim()) return;
    setChecking(true);
    try {
      const r = await checkAnswerLocally(prob.question, prob.answer, answer);
      setResult(r);
    } catch {
      setResult({ is_correct: false, feedback: 'Could not check answer. Try again.' });
    } finally {
      setChecking(false);
    }
  }

  if (!prob) {
    return (
      <div className={styles.emptyState}>
        <Zap size={32} />
        <p>No practice problems yet for this topic. The AI will generate them — click the refresh icon to regenerate.</p>
      </div>
    );
  }

  return (
    <div className={styles.practiceLayout}>
      <div className={styles.practiceMain}>
        <div className={styles.problemCard}>
          <div className={styles.problemHeader}>
            <span className={styles.problemNav}>Problem {current + 1} of {problems.length}</span>
            <span className={`${styles.diffBadge} ${styles[prob.difficulty || 'medium']}`}>
              {prob.difficulty || 'medium'}
            </span>
          </div>
          <div className={styles.problemQuestion}>
            <MathMarkdown>{prob.question}</MathMarkdown>
          </div>
          <div className={styles.answerRow}>
            <MathInput
              className={styles.answerInput}
              value={answer}
              onChange={e => setAnswer(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && checkAnswer()}
              placeholder="Type math: x^2, a/b, sqrt(x)..."
            />
            <button className={styles.checkBtn} onClick={checkAnswer} disabled={checking || !answer.trim()}>
              {checking ? <Loader2 size={16} className={styles.spin} /> : 'Check'}
            </button>
          </div>

          {result && (
            <div className={`${styles.resultBox} ${result.is_correct ? styles.resultCorrect : styles.resultWrong}`}>
              {result.is_correct ? <CheckCircle size={16} /> : <AlertCircle size={16} />}
              <MathMarkdown>{result.feedback || (result.is_correct ? 'Correct!' : 'Not quite — try again.')}</MathMarkdown>
            </div>
          )}

          <div className={styles.problemActions}>
            <button className={styles.actionBtn} onClick={prev} disabled={current === 0}>
              <ArrowLeft size={15} /> Prev
            </button>
            <button
              className={`${styles.actionBtn} ${showWalkthrough ? styles.actionBtnActive : ''}`}
              onClick={() => { setShowWalkthrough(v => !v); setStepIndex(0); }}
            >
              <BookOpen size={15} />
              {showWalkthrough ? 'Hide Walkthrough' : 'Show Walkthrough'}
            </button>
            <button
              className={`${styles.actionBtn} ${showChat ? styles.actionBtnActive : ''}`}
              onClick={() => setShowChat(v => !v)}
            >
              <MessageCircle size={15} /> Ask Tutor
            </button>
            <button className={styles.actionBtn} onClick={next} disabled={current === problems.length - 1}>
              Next <ArrowRight size={15} />
            </button>
          </div>
        </div>

        {showWalkthrough && prob.walkthrough?.length > 0 && (
          <WalkthroughPanel
            problem={prob}
            stepIndex={stepIndex}
            onStep={setStepIndex}
            onClose={() => setShowWalkthrough(false)}
          />
        )}
      </div>

      {showChat && (
        <ChatPanel
          topicId={topicId}
          topicTitle={topicTitle}
          problem={prob}
          stepIndex={showWalkthrough ? stepIndex : null}
          onClose={() => setShowChat(false)}
        />
      )}
    </div>
  );
}


function GeneratingLesson({ topicTitle }) {
  const steps = [
    'Analyzing topic structure...',
    'Building lesson from scratch...',
    'Writing concept explanations...',
    'Creating worked examples...',
    'Writing practice problems...',
    'Building step-by-step walkthroughs...',
  ];
  const [step, setStep] = useState(0);
  const [elapsed, setElapsed] = useState(0);

  useEffect(() => {
    const t = setInterval(() => {
      setStep(s => (s + 1) % steps.length);
      setElapsed(e => e + 1);
    }, 2500);
    return () => clearInterval(t);
  }, []);

  return (
    <div className={styles.generatingLesson}>
      <Loader2 size={40} className={styles.spin} />
      <h3>Building Your Lesson: {topicTitle}</h3>
      <p className={styles.genStep}>{steps[step]}</p>
      <p className={styles.genNote}>
        The AI is writing your lesson from scratch. This takes 60–90 seconds and is permanently cached after.
      </p>
      {elapsed >= 40 && (
        <p className={styles.genNote} style={{ marginTop: '8px', opacity: 0.6 }}>
          Still working... AI generation can take up to 2 minutes on first load.
        </p>
      )}
    </div>
  );
}


export default function Learn() {
  const { topicId: urlTopicId } = useParams();
  const [topics, setTopics] = useState([]);
  const [selectedId, setSelectedId] = useLocalStorage('calc-last-topic', null);
  const [topic, setTopic] = useState(null);
  const [tab, setTab] = useState('learn');
  const [conceptIdx, setConceptIdx] = useState(0);
  const [loading, setLoading] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [topicsLoading, setTopicsLoading] = useState(true);
  const [topicsError, setTopicsError] = useState(null);
  const [progress, setProgress] = useLocalStorage('calc-progress', {});
  const [savedConceptIdx, setSavedConceptIdx] = useLocalStorage('calc-concept-idx', {});
  const [showChat, setShowChat] = useState(false);
  const [currentPracticeProb, setCurrentPracticeProb] = useState(null);
  const [currentWalkthroughStep, setCurrentWalkthroughStep] = useState(null);

  // Load topic list on mount
  useEffect(() => {
    curriculumAPI.getTopics()
      .then(data => {
        setTopicsError(null);
        const list = data.topics || [];
        setTopics(list);
        if (list.length > 0) {
          if (urlTopicId && list.some(t => t.id === urlTopicId)) {
            setSelectedId(urlTopicId);
          } else {
            // Restore last-visited topic if it still exists; otherwise use first
            const hasSaved = selectedId && list.some(t => t.id === selectedId);
            if (!hasSaved) setSelectedId(list[0].id);
          }
        }
      })
      .catch(() => setTopicsError('Failed to load topics. Make sure the backend is running.'))
      .finally(() => setTopicsLoading(false));
  }, []);

  // Load (and auto-generate) topic when selected
  useEffect(() => {
    if (!selectedId) return;
    setLoading(true);
    setTopic(null);
    setConceptIdx(savedConceptIdx[selectedId] || 0);
    setTab('learn');
    setShowChat(false);
    setCurrentPracticeProb(null);
    setCurrentWalkthroughStep(null);

    curriculumAPI.getTopic(selectedId)
      .then(async data => {
        if (!data.generated) {
          // Not generated yet — generate now and cache permanently
          setLoading(false);
          setGenerating(true);
          try {
            const enriched = await curriculumAPI.generateTopic(selectedId);
            setTopic(enriched);
            setTopics(prev => prev.map(t => t.id === selectedId ? { ...t, generated: true } : t));
          } catch (err) {
            // Generation failed — leave as not-generated so user can retry
            setTopic({ ...data, generated: false, _error: true, _errorMsg: err.message });
          } finally {
            setGenerating(false);
          }
        } else {
          setTopic(data);
        }
      })
      .catch(() => setTopic(null))
      .finally(() => setLoading(false));
  }, [selectedId]);

  async function regenerate() {
    if (!selectedId) return;
    const prev = topic;
    setTopic(null);
    setGenerating(true);
    try {
      const enriched = await curriculumAPI.forceTopic(selectedId);
      setTopic(enriched);
      setTopics(ts => ts.map(t => t.id === selectedId ? { ...t, generated: true } : t));
    } catch (err) {
      setTopic({ ...prev, _error: true, _errorMsg: err.message });
    } finally {
      setGenerating(false);
    }
  }

  if (topicsLoading) {
    return (
      <div className={styles.loadingCenter}>
        <Loader2 size={32} className={styles.spin} />
        <span>Loading your curriculum...</span>
      </div>
    );
  }

  if (topics.length === 0 && !topicsError) {
    return (
      <div className={styles.page}>
        <div className={styles.scrapePrompt}>
          <GraduationCap size={48} className={styles.scrapeIcon} />
          <h2>Curriculum Not Found</h2>
          <p>Something went wrong loading the curriculum. Make sure the backend is running on port 8000.</p>
        </div>
      </div>
    );
  }

  return (
    <div className={styles.page}>
      <TopicSidebar
        topics={topics}
        selectedId={selectedId}
        onSelect={id => setSelectedId(id)}
        progress={progress}
        topicsError={topicsError}
      />

      <main className={styles.main}>
        {loading && (
          <div className={styles.loadingCenter}>
            <Loader2 size={28} className={styles.spin} />
            <span>Loading...</span>
          </div>
        )}

        {generating && topic === null && selectedId && (
          <GeneratingLesson topicTitle={topics.find(t => t.id === selectedId)?.title || selectedId} />
        )}

        {!loading && !generating && topic?._error && (
          <div className={styles.errorState}>
            <AlertCircle size={32} />
            <h3>Generation Failed</h3>
            <p>{topic._errorMsg || 'Could not generate lesson. The AI may be busy — try again in a moment.'}</p>
            <button className={styles.navBtnPrimary} onClick={regenerate}>
              <RefreshCw size={16} /> Try Again
            </button>
          </div>
        )}

        {!loading && !generating && topic && !topic?._error && (
          <>
            {/* Topic header */}
            <div className={styles.topicHeader}>
              <div className={styles.topicMeta}>
                <span className={styles.sectionBadge}>{topic.id}</span>
                <span className={`${styles.levelBadge} ${topic.calc_level === 1 ? styles.calc1 : styles.calc2}`}>
                  Calc {topic.calc_level}
                </span>
                {topic.priority && (
                  <span className={styles.priorityBadge}>{topic.priority}</span>
                )}
              </div>
              <h1 className={styles.topicHeading}>{topic.title}</h1>
              {topic.description && (
                <div className={styles.topicDesc}><MathMarkdown>{topic.description}</MathMarkdown></div>
              )}
              {topic.key_formula && (
                <div className={styles.keyFormula}>
                  <span className={styles.keyFormulaLabel}>Key Formula</span>
                  <div className={styles.keyFormulaDisplay}>
                    <MathMarkdown formula>{topic.key_formula}</MathMarkdown>
                  </div>
                </div>
              )}
            </div>

            {/* Tabs */}
            <div className={styles.tabs}>
              <button
                className={`${styles.tab} ${tab === 'learn' ? styles.tabActive : ''}`}
                onClick={() => setTab('learn')}
              >
                <BookOpen size={15} /> Learn
              </button>
              <button
                className={`${styles.tab} ${tab === 'practice' ? styles.tabActive : ''}`}
                onClick={() => setTab('practice')}
              >
                <Calculator size={15} /> Practice ({topic.practice_problems?.length || 0})
              </button>
              <div className={styles.tabSpacer} />
              <button
                className={`${styles.tab} ${showChat ? styles.tabActive : ''}`}
                onClick={() => setShowChat(v => !v)}
              >
                <MessageCircle size={15} /> Ask Tutor
              </button>
              <button className={styles.iconBtn} onClick={regenerate} title="Regenerate lesson">
                <RefreshCw size={15} />
              </button>
            </div>

            {/* Tab content */}
            <div className={styles.tabContent}>
              {tab === 'learn' && (
                <div className={styles.learnLayout}>
                  <div className={styles.learnMain}>
                    {topic.concepts?.length > 0 ? (
                      <>
                        <ConceptPanel
                          concept={topic.concepts[Math.min(conceptIdx, topic.concepts.length - 1)]}
                          index={Math.min(conceptIdx, topic.concepts.length - 1)}
                          total={topic.concepts.length}
                        />
                        <div className={styles.conceptNav}>
                          <button
                            className={styles.navBtn}
                            onClick={() => {
                              const next = Math.max(0, conceptIdx - 1);
                              setConceptIdx(next);
                              setSavedConceptIdx(p => ({ ...p, [selectedId]: next }));
                            }}
                            disabled={conceptIdx === 0}
                          >
                            <ArrowLeft size={16} /> Previous
                          </button>
                          <div className={styles.conceptDots}>
                            {topic.concepts.map((_, i) => (
                              <button
                                key={i}
                                className={`${styles.dot} ${i === conceptIdx ? styles.dotActive : ''}`}
                                aria-label={`Go to concept ${i + 1}`}
                                onClick={() => {
                                  setConceptIdx(i);
                                  setSavedConceptIdx(p => ({ ...p, [selectedId]: i }));
                                }}
                              />
                            ))}
                          </div>
                          <button
                            className={`${styles.navBtn} ${styles.navBtnPrimary}`}
                            onClick={() => {
                              if (conceptIdx < topic.concepts.length - 1) {
                                const next = conceptIdx + 1;
                                setConceptIdx(next);
                                setSavedConceptIdx(p => ({ ...p, [selectedId]: next }));
                              } else {
                                setTab('practice');
                                // Mark concepts as done when reaching the end
                                setProgress(p => ({
                                  ...p,
                                  [selectedId]: { ...(p[selectedId] || {}), conceptsDone: true },
                                }));
                              }
                            }}
                          >
                            {conceptIdx < topic.concepts.length - 1 ? (
                              <>Next Concept <ArrowRight size={16} /></>
                            ) : (
                              <>Practice Problems <Calculator size={16} /></>
                            )}
                          </button>
                        </div>
                      </>
                    ) : (
                      <div className={styles.emptyState}>
                        <Sparkles size={32} />
                        <p>No lesson content yet. Click the refresh icon to generate it.</p>
                      </div>
                    )}
                  </div>
                  {showChat && (
                    <ChatPanel
                      topicId={topic.id}
                      topicTitle={topic.title}
                      problem={null}
                      stepIndex={null}
                      currentConcept={topic.concepts?.[Math.min(conceptIdx, topic.concepts.length - 1)]}
                      currentTab={tab}
                      onClose={() => setShowChat(false)}
                    />
                  )}
                </div>
              )}

              {tab === 'practice' && (
                <div className={styles.learnLayout}>
                  <div className={styles.learnMain}>
                    <PracticeTab
                      problems={topic.practice_problems || []}
                      topicId={topic.id}
                      topicTitle={topic.title}
                      onProblemChange={setCurrentPracticeProb}
                      onStepChange={setCurrentWalkthroughStep}
                    />
                  </div>
                  {showChat && (
                    <ChatPanel
                      topicId={topic.id}
                      topicTitle={topic.title}
                      problem={currentPracticeProb}
                      stepIndex={currentWalkthroughStep}
                      currentTab={tab}
                      onClose={() => setShowChat(false)}
                    />
                  )}
                </div>
              )}
            </div>
          </>
        )}
      </main>
    </div>
  );
}
