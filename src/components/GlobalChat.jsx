import { useState, useRef, useEffect } from 'react';
import { MessageCircle, X, Send, Loader2, Minimize2, GraduationCap } from 'lucide-react';
import { aiAPI } from '../utils/api';
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
  const bottomRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    if (open && !minimized) {
      bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
      setTimeout(() => inputRef.current?.focus(), 100);
    }
  }, [messages, open, minimized]);

  async function send() {
    const text = input.trim();
    if (!text || loading) return;
    setInput('');
    const updatedMessages = [...messages, { role: 'user', content: text }];
    setMessages(updatedMessages);
    setLoading(true);
    try {
      // Pass conversation history (exclude the system welcome message)
      const history = updatedMessages
        .filter((m, i) => i > 0) // skip welcome message
        .map(m => ({ role: m.role, content: m.content }));
      const resp = await aiAPI.chat(text, topicId, 0.5, [], problem?.question || '', stepIndex, history);
      setMessages(prev => [...prev, { role: 'assistant', content: resp.response }]);
    } catch {
      setMessages(prev => [...prev, { role: 'assistant', content: 'Something went wrong — is the backend running? Try again.' }]);
    } finally {
      setLoading(false);
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
          <span className={styles.fabLabel}>Ask Tutor</span>
        </button>
      )}

      {/* Chat window */}
      {open && (
        <div className={`${styles.window} ${minimized ? styles.windowMinimized : ''}`} role="dialog" aria-label="AI Tutor Chat">
          <div className={styles.header}>
            <div className={styles.headerLeft}>
              <GraduationCap size={16} className={styles.headerIcon} />
              <div>
                <div className={styles.headerTitle}>AI Tutor</div>
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
                {loading && (
                  <div className={`${styles.msg} ${styles.msgBot}`}>
                    <div className={styles.bubble}>
                      <Loader2 size={15} className={styles.spin} />
                    </div>
                  </div>
                )}
                <div ref={bottomRef} />
              </div>

              <div className={styles.suggestions}>
                {['Explain this from scratch', 'Show me an example', "Why does this formula work?"].map(s => (
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
