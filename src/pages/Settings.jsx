import { useState, useEffect } from 'react';
import { useTheme } from '../contexts/ThemeContext';
import { Sun, Moon, Download, Trash2, RefreshCw, Check } from 'lucide-react';
import styles from './Settings.module.css';

const DIFFICULTY_OPTIONS = ['adaptive', 'easy', 'medium', 'hard'];
const HINT_OPTIONS = ['always', 'after-attempt', 'never'];

function loadPrefs() {
  try {
    return JSON.parse(localStorage.getItem('calcPrefs') || '{}');
  } catch { return {}; }
}

function savePrefs(prefs) {
  localStorage.setItem('calcPrefs', JSON.stringify(prefs));
}

export default function Settings() {
  const { theme, toggleTheme } = useTheme();
  const [prefs, setPrefs] = useState(() => ({
    difficulty: 'adaptive',
    hintsMode: 'after-attempt',
    showStepByStep: true,
    questionsPerQuiz: 10,
    ...loadPrefs(),
  }));
  const [saved, setSaved] = useState(false);

  function updatePref(key, value) {
    setPrefs(p => {
      const next = { ...p, [key]: value };
      savePrefs(next);
      return next;
    });
    flashSaved();
  }

  function flashSaved() {
    setSaved(true);
    setTimeout(() => setSaved(false), 1500);
  }

  function handleExport() {
    const data = {};
    for (let i = 0; i < localStorage.length; i++) {
      const k = localStorage.key(i);
      data[k] = localStorage.getItem(k);
    }
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `calculus-mastery-backup-${new Date().toISOString().slice(0, 10)}.json`;
    a.click();
    URL.revokeObjectURL(url);
  }

  function handleClearProgress() {
    if (!window.confirm('Clear all practice progress and mastery data? Your settings will be kept.')) return;
    const keysToRemove = [];
    for (let i = 0; i < localStorage.length; i++) {
      const k = localStorage.key(i);
      if (k !== 'calcPrefs' && k !== 'theme') keysToRemove.push(k);
    }
    keysToRemove.forEach(k => localStorage.removeItem(k));
    flashSaved();
  }

  return (
    <div className={styles.page}>
      <header className={styles.header}>
        <h1 className={styles.title}>Settings</h1>
        <p className={styles.subtitle}>Configure your study platform</p>
        {saved && (
          <span className={styles.savedBadge}>
            <Check size={14} /> Saved
          </span>
        )}
      </header>

      {/* Appearance */}
      <div className={styles.section}>
        <h2 className={styles.sectionTitle}>Appearance</h2>
        <div className={styles.settingRow}>
          <div className={styles.settingInfo}>
            <span className={styles.settingLabel}>Theme</span>
            <span className={styles.settingHint}>Switch between dark and light mode</span>
          </div>
          <button className={styles.themeBtn} onClick={toggleTheme}>
            {theme === 'dark' ? <Sun size={16} /> : <Moon size={16} />}
            {theme === 'dark' ? 'Light Mode' : 'Dark Mode'}
          </button>
        </div>
      </div>

      {/* Practice Preferences */}
      <div className={styles.section}>
        <h2 className={styles.sectionTitle}>Practice</h2>

        <div className={styles.settingRow}>
          <div className={styles.settingInfo}>
            <span className={styles.settingLabel}>Difficulty</span>
            <span className={styles.settingHint}>Adaptive adjusts based on your performance</span>
          </div>
          <select
            className={styles.select}
            value={prefs.difficulty}
            onChange={e => updatePref('difficulty', e.target.value)}
          >
            {DIFFICULTY_OPTIONS.map(d => (
              <option key={d} value={d}>{d.charAt(0).toUpperCase() + d.slice(1)}</option>
            ))}
          </select>
        </div>

        <div className={styles.settingRow}>
          <div className={styles.settingInfo}>
            <span className={styles.settingLabel}>Hints</span>
            <span className={styles.settingHint}>When to show hints on practice problems</span>
          </div>
          <select
            className={styles.select}
            value={prefs.hintsMode}
            onChange={e => updatePref('hintsMode', e.target.value)}
          >
            {HINT_OPTIONS.map(h => (
              <option key={h} value={h}>{h === 'after-attempt' ? 'After Attempt' : h.charAt(0).toUpperCase() + h.slice(1)}</option>
            ))}
          </select>
        </div>

        <div className={styles.settingRow}>
          <div className={styles.settingInfo}>
            <span className={styles.settingLabel}>Step-by-step solutions</span>
            <span className={styles.settingHint}>Show detailed solution walkthroughs</span>
          </div>
          <label className={styles.toggle}>
            <input
              type="checkbox"
              checked={prefs.showStepByStep}
              onChange={e => updatePref('showStepByStep', e.target.checked)}
            />
            <span className={styles.toggleTrack} />
          </label>
        </div>

        <div className={styles.settingRow}>
          <div className={styles.settingInfo}>
            <span className={styles.settingLabel}>Questions per quiz</span>
            <span className={styles.settingHint}>Number of problems in each quiz session</span>
          </div>
          <select
            className={styles.select}
            value={prefs.questionsPerQuiz}
            onChange={e => updatePref('questionsPerQuiz', Number(e.target.value))}
          >
            {[5, 10, 15, 20, 25].map(n => (
              <option key={n} value={n}>{n}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Canvas Integration */}
      <div className={styles.section}>
        <h2 className={styles.sectionTitle}>Canvas Integration</h2>
        <div className={styles.infoBox}>
          <div className={styles.infoTitle}>How to sync your course</div>
          <div className={styles.infoText}>
            <ol>
              <li>Open a terminal in the project folder</li>
              <li>Run: <code>cd backend && source ../venv/bin/activate && python scraper.py</code></li>
              <li>Chrome will open — log in if needed</li>
              <li>Follow the prompts to scrape your calculus course</li>
              <li>Go to "My Course" page to see your content</li>
            </ol>
          </div>
        </div>
      </div>

      {/* Data Management */}
      <div className={styles.section}>
        <h2 className={styles.sectionTitle}>Data</h2>
        <div className={styles.settingRow}>
          <div className={styles.settingInfo}>
            <span className={styles.settingLabel}>Export all data</span>
            <span className={styles.settingHint}>Download your progress and settings as JSON</span>
          </div>
          <button className={styles.actionBtn} onClick={handleExport}>
            <Download size={16} /> Export
          </button>
        </div>
        <div className={styles.settingRow}>
          <div className={styles.settingInfo}>
            <span className={styles.settingLabel}>Clear progress</span>
            <span className={styles.settingHint}>Reset all practice data (keeps settings)</span>
          </div>
          <button className={`${styles.actionBtn} ${styles.dangerBtn}`} onClick={handleClearProgress}>
            <Trash2 size={16} /> Clear
          </button>
        </div>
      </div>

      {/* Keyboard shortcuts */}
      <div className={styles.section}>
        <h2 className={styles.sectionTitle}>Keyboard Shortcuts</h2>
        <div className={styles.shortcutGrid}>
          <div className={styles.shortcutRow}><kbd>Enter</kbd><span>Submit answer</span></div>
          <div className={styles.shortcutRow}><kbd>Tab</kbd><span>Next problem</span></div>
          <div className={styles.shortcutRow}><kbd>?</kbd><span>Show hint</span></div>
          <div className={styles.shortcutRow}><kbd>Esc</kbd><span>Close panels</span></div>
        </div>
      </div>

      <footer className={styles.footer}>
        <p>Calculus Mastery Platform · Built for acing the final.</p>
      </footer>
    </div>
  );
}
