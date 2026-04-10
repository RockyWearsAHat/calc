import { useState, useRef, useEffect } from 'react';
import { MessageCircle, X, Send, Loader2, Minimize2, GraduationCap } from 'lucide-react';
import { generateChatResponse, setProgressCallback } from '../utils/localAI';
import MathMarkdown from './MathMarkdown';
import styles from './GlobalChat.module.css';

const WELCOME = `Hi! I'm your personal calculus tutor.
I'm here to help you understand **anything** in your course — from basic limits to Taylor series. Ask me to:
- **Explain a concept** from scratch ("What even is an integral?")
- **Walk through a problem** step by step
- **Check your work** — I'll tell you straight if you got it right
- **Show patterns** for recognizing which technique to use

No question is too basic. What would you like to work on?`;

export default function GlobalChat({ topicId = null, topicTitle = null, problem = null, stepIndex = null }) {
  const [open, setOpen] = useState(false);
  const [minimized, setMinimized] = useState(false);
  const [messages, setMessages] = useState([{ role: 'assistant', content: WELCOME }]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [engineStatus, setEngineStatus] = useState('Initializing 1-bit AI Core...');
  const [isInitializing, setIsInitializing] = useState(false);

  const bottomRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    setProgressCallback((report) => {
      setEngineStatus(report.text);
    });
  }, []);

  useEffect(() => {
    if (open && !minimized) {
      bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
      setTimeout(() => inputRef.current?.focus(), 100);
    }
  }, [messages, open, minimized, engineStatus, isInitializing]);

  async function send() {
    const text = input.trim();
    if (!text || loading) return;
    setInput('');
    const updatedMessages = [...messages, { role: 'user', content: text }];
    setMessages(updatedMessages);
    setLoading(true);
    
    // First message starts initialization if not done
    setIsInitializing(true);

    try {
      const history = updatedMessages
        .filter((m, i) => i > 0 && m.role !== 'system') 
        .map(m => ({ role: m.role, content: m.content }));
      
      const systemPrompt = "You are a helpful and brilliant calculus AI tutor running directly in the browser using a lightweight WebGPU quantised engine. Keep answers brief, specific, and direct to the point. Focus strictly on their calculus questions. Use markdown math formatting when useful.";

      // WebLLM chat generation
      const resp = await generateChatResponse(text, history.slice(0, -1), systemPrompt);
      
      setIsInitializing(false);
      setMessages(prev => [...prev, { role: 'assistant', content: resp }]);
    } catch(err) {
      setIsInitializing(false);
      setMessages(prev => [...prev, { role: 'assistant', content: `SYSTEM ERROR: WebGPU/Model failure. Make sure you are using Chrome/Edge with WebGPU enabled. (${err.message})` }]);
    } finally {
      setLoading(false);
      setEngineStatus('');
    }
  }

  function handleKey(e) {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send(); }
  }

  return (
    <>
      {/* Floating button */}
      {!open && (
        <button className={styles.fab} aria-label="Open AI Tutor Chat" onClick={() => setOpen(true)} title="Ask your AI tutor">
          <MessageCircle size={22} />
          <span className={styles.fabLabel}>Mech Tutor</span>
        </button>
      )}

      {/* Chat window */}
      {open && (
        <div className={`${styles.window} ${minimized ? styles.windowMinimized : ''}`} role="dialog" aria-label="AI Tutor Chat">
          <div className={styles.header}>
            <div className={styles.headerLeft}>
              <GraduationCap size={16} className={styles.headerIcon} />
              <div>
                <div className={styles.headerTitle}>WebGPU 1-bit Tutor</div>
                {topicTitle && <div className={styles.headerSub}>{topicTitle}</div>}
              </div>
            </div>
            <div className={styles.headerActions}>
              <button className={styles.headerBtn} onClick={() => setMinimized(v => !v)} title={minimized ? 'Expand' : 'Minimize'}>
                <Minimize2 size={14} />
              </button>
              <button className={styles.headerBtn} onClick={() => setOpen(false)} title="Close">
                <X size={14} />
              </button>
            </div>
          </div>

          {!minimized && (
            <>
              <div className={styles.messages}>
                {messages.map((m, i) => (
                  <div key={i} className={`${styles.msg} ${m.role === 'user' ? styles.msgUser : styles.msgBot}`}>
                    <div className={styles.bubble}>
                      {m.role === 'assistant'
                        ? <MathMarkdown>{m.content}</MathMarkdown>
                        : <span>{m.content}</span>}
                    </div>
                  </div>
                ))}
                {loading && isInitializing && engineStatus && (
                  <div className={`${styles.msg} ${styles.msgBot}`}>
                     <div className={styles.bubble} style={{ fontSize: '0.85em', color: '#888' }}>
                       {engineStatus}... <br /> <br />
                       [This model downloads once to your browser cache. Subsequent loads are instant. A ~600MB payload is deploying...]
                     </div>
                  </div>
                )}
                {loading && !isInitializing && (
                   <div className={`${styles.msg} ${styles.msgBot}`}>
                    <div className={styles.bubble}>
                      <Loader2 size={15} className={styles.spin} />
                    </div>
                  </div>
                )}
                <div ref={bottomRef} />
              </div>

              <div className={styles.suggestions}>
                {['Explain limits like I am five', 'Help me find the derivative of sin(x)', "Why do we need calculus?"].map(s => (
                  <button key={s} className={styles.suggestion} onClick={() => { setInput(s); inputRef.current?.focus(); }}>
                    {s}
                  </button>
                ))}
              </div>

              <div className={styles.inputRow}>
                <textarea
                  ref={inputRef}
                  className={styles.inputField}
                  value={input}
                  onChange={e => setInput(e.target.value)}
                  onKeyDown={handleKey}
                  placeholder="Ask anything about calculus..."
                  rows={1}
                />
                <button className={styles.sendBtn} onClick={send} disabled={loading || !input.trim()}>
                  <Send size={15} />
                </button>
              </div>
            </>
          )}
        </div>
      )}
    </>
  );
}
