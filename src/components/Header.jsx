import { useState, useEffect } from 'react';
import { NavLink } from 'react-router-dom';
import { BookOpen, Calculator, Settings, GraduationCap, Lightbulb, Sun, Moon, FolderOpen } from 'lucide-react';
import styles from './Header.module.css';
import { curriculumAPI } from '../utils/api';
import { useTheme } from '../contexts/ThemeContext';

export default function Header() {
  const [curriculumReady, setCurriculumReady] = useState(false);
  const { theme, toggleTheme } = useTheme();

  useEffect(() => {
    curriculumAPI.getTopics()
      .then(d => setCurriculumReady((d.topics_count || d.total_topics || d.topics?.length || 0) > 0))
      .catch(() => setCurriculumReady(false));
  }, []);

  return (
    <header className={styles.header}>
      <div className={styles.headerShell} data-live={curriculumReady ? 'true' : 'false'}>
        <NavLink to="/" className={styles.logo}>
          <span className={styles.logoIcon} aria-hidden="true">∫</span>
          <span className={styles.logoText}>Calculus</span>
        </NavLink>

        <nav className={styles.nav} aria-label="Primary">
          <div className={styles.navRail}>
            <NavLink
              to="/"
              className={({ isActive }) => isActive ? styles.navLinkActive : styles.navLink}
              end
            >
              <GraduationCap size={18} />
              Dashboard
            </NavLink>
            <NavLink
              to="/learn"
              className={({ isActive }) => isActive ? styles.navLinkActive : styles.navLink}
            >
              <BookOpen size={18} />
              Learn
            </NavLink>
            <NavLink
              to="/practice"
              className={({ isActive }) => isActive ? styles.navLinkActive : styles.navLink}
            >
              <Calculator size={18} />
              Practice
            </NavLink>
            <NavLink
              to="/formulas"
              className={({ isActive }) => isActive ? styles.navLinkActive : styles.navLink}
            >
              <Lightbulb size={18} />
              Formulas
            </NavLink>
            <NavLink
              to="/course"
              className={({ isActive }) => isActive ? styles.navLinkActive : styles.navLink}
            >
              <FolderOpen size={18} />
              My Course
            </NavLink>
            <NavLink
              to="/settings"
              className={({ isActive }) => isActive ? styles.navLinkActive : styles.navLink}
            >
              <Settings size={18} />
              Settings
            </NavLink>
          </div>
        </nav>

        <div className={styles.headerMeta}>
          <div className={styles.syncStatus} data-live={curriculumReady ? 'true' : 'false'} aria-live="polite">
            <span className={curriculumReady ? styles.syncDotConnected : styles.syncDot} />
            <span className={styles.syncLabel}>
              {curriculumReady ? 'AI Path Online' : 'Curriculum Pending'}
            </span>
          </div>
          <button
            onClick={toggleTheme}
            aria-label={theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'}
            className={styles.themeToggle}
            title={theme === 'dark' ? 'Light mode' : 'Dark mode'}
          >
            {theme === 'dark' ? <Sun size={18} /> : <Moon size={18} />}
          </button>
        </div>
      </div>
    </header>
  );
}
