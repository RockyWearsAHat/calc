import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { GraduationCap, BookOpen, ExternalLink, Loader2, AlertCircle, RefreshCw, Calendar, FileText, ChevronRight } from 'lucide-react';
import { courseAPI } from '../utils/api';
import styles from './Course.module.css';

export default function Course() {
  const [courseData, setCourseData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadCourseData();
  }, []);

  async function loadCourseData() {
    setLoading(true);
    setError(null);
    try {
      const data = await courseAPI.getData();
      setCourseData(data);
    } catch (err) {
      setError(err?.message || 'Failed to load course data');
    } finally {
      setLoading(false);
    }
  }

  if (loading) {
    return (
      <div className={styles.page}>
        <div className={styles.loadingState}>
          <Loader2 size={32} className={styles.spin} />
          <span>Loading your course data...</span>
        </div>
      </div>
    );
  }

  const hasData = courseData && (courseData.topics?.length > 0 || courseData.assignments?.length > 0 || courseData.modules?.length > 0);

  return (
    <div className={styles.page}>
      <header className={styles.header}>
        <div className={styles.headerMeta}>
          <span className={styles.eyebrow}>CANVAS INTEGRATION</span>
          <span className={hasData ? styles.statusLive : styles.statusIdle}>
            <span className={styles.statusDot} />
            {hasData ? 'Course synced' : 'Not synced'}
          </span>
        </div>
        <h1 className={styles.title}>My Course</h1>
        <p className={styles.subtitle}>
          {hasData
            ? 'Your Canvas course data, synced and organized for focused study.'
            : 'Sync your Canvas course to see assignments, modules, and progress here.'}
        </p>
      </header>

      {error && (
        <div className={styles.errorCard}>
          <AlertCircle size={20} />
          <div>
            <strong>Could not load course data</strong>
            <p>{error}</p>
          </div>
          <button className={styles.retryBtn} onClick={loadCourseData}>
            <RefreshCw size={16} /> Retry
          </button>
        </div>
      )}

      {!hasData && !error && (
        <div className={styles.emptyState}>
          <GraduationCap size={48} className={styles.emptyIcon} />
          <h2>No Course Data Yet</h2>
          <p>
            To sync your Canvas course, run the scraper from your terminal:
          </p>
          <div className={styles.codeBlock}>
            <code>cd backend && source ../venv/bin/activate && python scraper.py</code>
          </div>
          <p className={styles.emptyNote}>
            This opens Chrome so you can log in to Canvas. Your course content is saved locally and never leaves your machine.
          </p>
          <Link to="/settings" className={styles.settingsLink}>
            <FileText size={16} /> View setup instructions in Settings
          </Link>
        </div>
      )}

      {hasData && (
        <div className={styles.content}>
          {courseData.modules?.length > 0 && (
            <section className={styles.section}>
              <h2 className={styles.sectionTitle}>Course Modules</h2>
              <div className={styles.moduleGrid}>
                {courseData.modules.map((mod, i) => (
                  <div key={i} className={styles.moduleCard}>
                    <div className={styles.moduleIndex}>{String(i + 1).padStart(2, '0')}</div>
                    <div className={styles.moduleInfo}>
                      <h3>{mod.name || mod.title}</h3>
                      {mod.items_count && <span className={styles.moduleCount}>{mod.items_count} items</span>}
                    </div>
                    <ChevronRight size={16} className={styles.moduleArrow} />
                  </div>
                ))}
              </div>
            </section>
          )}

          {courseData.assignments?.length > 0 && (
            <section className={styles.section}>
              <h2 className={styles.sectionTitle}>Assignments</h2>
              <div className={styles.assignmentList}>
                {courseData.assignments.map((a, i) => (
                  <div key={i} className={styles.assignmentCard}>
                    <div className={styles.assignmentIcon}>
                      <FileText size={18} />
                    </div>
                    <div className={styles.assignmentInfo}>
                      <strong>{a.name || a.title}</strong>
                      {a.due_date && (
                        <span className={styles.dueDate}>
                          <Calendar size={13} />
                          Due: {new Date(a.due_date).toLocaleDateString()}
                        </span>
                      )}
                    </div>
                    {a.url && (
                      <a href={a.url} target="_blank" rel="noopener noreferrer" className={styles.externalLink}>
                        <ExternalLink size={14} />
                      </a>
                    )}
                  </div>
                ))}
              </div>
            </section>
          )}

          {courseData.topics?.length > 0 && (
            <section className={styles.section}>
              <h2 className={styles.sectionTitle}>Matched Topics</h2>
              <p className={styles.sectionSubtitle}>These Canvas topics match your curriculum. Click to study.</p>
              <div className={styles.topicGrid}>
                {courseData.topics.map((t, i) => (
                  <Link key={i} to={`/learn/${t.id || t.topic_id}`} className={styles.topicLink}>
                    <BookOpen size={16} />
                    <span>{t.name || t.title}</span>
                    <ChevronRight size={14} />
                  </Link>
                ))}
              </div>
            </section>
          )}
        </div>
      )}
    </div>
  );
}
