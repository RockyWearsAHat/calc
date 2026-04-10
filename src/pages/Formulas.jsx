import { useState, useEffect } from 'react';
import { Loader2 } from 'lucide-react';
import { formulaAPI } from '../utils/api';
import { Formula } from '../components/Math';
import styles from './Formulas.module.css';

export default function Formulas() {
  const [formulas, setFormulas] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  async function loadFormulas() {
    setLoading(true);
    setError(null);
    try {
      const res = await formulaAPI.getAll();
      setFormulas(res.formulas);
    } catch (err) {
      console.error('Failed to load formulas:', err);
      setError(err?.message || 'Unknown error');
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadFormulas();
  }, []);

  if (loading) {
    return (
      <div className={styles.page}>
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: '1rem', minHeight: '60vh' }}>
          <Loader2 size={32} style={{ animation: 'spin 1s linear infinite' }} />
          <p>Loading formulas...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={styles.page}>
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: '1rem', minHeight: '60vh', textAlign: 'center', padding: '1rem' }}>
          <p>Failed to load formulas: {error}</p>
          <button onClick={loadFormulas}>Retry</button>
        </div>
      </div>
    );
  }

  return (
    <div className={styles.page}>
      <header className={styles.header}>
        <h1 className={styles.title}><span aria-hidden="true">📋</span> Formula Sheet</h1>
        <p className={styles.subtitle}>
          Quick reference for all the formulas you need
        </p>
      </header>

      <div className={styles.categories}>
        {formulas && Object.entries(formulas).map(([key, category]) => (
          <div key={key} className={styles.category}>
            <div className={styles.categoryHeader}>
              <h2 className={styles.categoryTitle}>{category.title}</h2>
            </div>
            <div className={styles.formulaGrid}>
              {category.formulas.map((f, i) => (
                <div
                  key={i}
                  className={`${styles.formulaCard} ${i === category.formulas.length - 1 && category.formulas.length % 2 !== 0 ? styles.formulaCardSpan : ''}`}
                >
                  <span className={styles.formulaName}>{f.name}</span>
                  <div className={styles.formulaMath}>
                    <Formula math={f.formula} display />
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>

      <div className={styles.quickRef}>
        <h3 className={styles.quickRefTitle}><span aria-hidden="true">⚡</span> Quick Reference - Common Values</h3>
        <div className={styles.quickRefList}>
          <div className={styles.quickRefItem}>
            <span className={styles.quickRefLabel}>sin(0)</span>
            <span className={styles.quickRefValue}>0</span>
          </div>
          <div className={styles.quickRefItem}>
            <span className={styles.quickRefLabel}>sin(π/6)</span>
            <span className={styles.quickRefValue}>1/2</span>
          </div>
          <div className={styles.quickRefItem}>
            <span className={styles.quickRefLabel}>sin(π/4)</span>
            <span className={styles.quickRefValue}>√2/2</span>
          </div>
          <div className={styles.quickRefItem}>
            <span className={styles.quickRefLabel}>sin(π/3)</span>
            <span className={styles.quickRefValue}>√3/2</span>
          </div>
          <div className={styles.quickRefItem}>
            <span className={styles.quickRefLabel}>sin(π/2)</span>
            <span className={styles.quickRefValue}>1</span>
          </div>
          <div className={styles.quickRefItem}>
            <span className={styles.quickRefLabel}>cos(0)</span>
            <span className={styles.quickRefValue}>1</span>
          </div>
          <div className={styles.quickRefItem}>
            <span className={styles.quickRefLabel}>cos(π/6)</span>
            <span className={styles.quickRefValue}>√3/2</span>
          </div>
          <div className={styles.quickRefItem}>
            <span className={styles.quickRefLabel}>cos(π/4)</span>
            <span className={styles.quickRefValue}>√2/2</span>
          </div>
          <div className={styles.quickRefItem}>
            <span className={styles.quickRefLabel}>cos(π/3)</span>
            <span className={styles.quickRefValue}>1/2</span>
          </div>
          <div className={styles.quickRefItem}>
            <span className={styles.quickRefLabel}>cos(π/2)</span>
            <span className={styles.quickRefValue}>0</span>
          </div>
          <div className={styles.quickRefItem}>
            <span className={styles.quickRefLabel}>e</span>
            <span className={styles.quickRefValue}>2.71828...</span>
          </div>
          <div className={styles.quickRefItem}>
            <span className={styles.quickRefLabel}>ln(e)</span>
            <span className={styles.quickRefValue}>1</span>
          </div>
        </div>
      </div>
    </div>
  );
}
