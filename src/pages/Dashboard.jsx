import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { BookOpen, Calculator, Target, ChevronRight, Play, Loader2 } from 'lucide-react';
import { curriculumAPI } from '../utils/api';
import MathMarkdown from '../components/MathMarkdown';
import styles from './Dashboard.module.css';

const CALC_LEVEL_LABELS = { 1: 'I', 2: 'II' };

export default function Dashboard() {
  const [topics, setTopics] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function load() {
      setError(null);
      try {
        const data = await curriculumAPI.getTopics();
        setTopics(data.topics || []);
      } catch (err) {
        setTopics([]);
        setError(err?.message || 'Failed to load curriculum');
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  const calc1 = topics.filter(t => t.calc_level === 1);
  const calc2 = topics.filter(t => t.calc_level === 2);
  const firstTopic = topics[0];

  if (loading) {
    return (
      <div className={styles.center}>
        <Loader2 size={24} className={styles.spin} />
        <span>Loading curriculum…</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className={styles.center}>
        <h2>Could not reach the backend</h2>
        <p>{error}</p>
      </div>
    );
  }

  return (
    <div className={styles.page}>
      <section className={styles.hero}>
        <span className={styles.eyebrow}>MATH 1220 · University of Utah</span>
        <h1 className={styles.title}>
          Calculus<span className={styles.accent}> Mastery</span>
        </h1>
        <p className={styles.subtitle}>
          Course-aligned lessons, deliberate practice, and AI tutoring — a calmer, more precise study surface built for real momentum.
        </p>

        <div className={styles.stats}>
          <Stat value={topics.length} label="topics" />
          <Stat value={calc1.length} label="Calc I" />
          <Stat value={calc2.length} label="Calc II" />
        </div>

        <div className={styles.actions}>
          <Link to={firstTopic ? "/learn/" + firstTopic.id : '/learn'} className={styles.btnPrimary}>
            <Play size={15} /> Start Learning
          </Link>
          <Link to="/practice" className={styles.btnGhost}>Practice Problems</Link>
        </div>
      </section>

      {calc1.length > 0 && <TopicSection title="Calculus I" count={calc1.length} topics={calc1} />}
      {calc2.length > 0 && <TopicSection title="Calculus II" count={calc2.length} topics={calc2} />}

      {topics.length === 0 && (
        <section className={styles.empty}>
          <p>Your curriculum has not been generated yet.</p>
          <Link to="/learn">Open the Learn page to build your study path →</Link>
        </section>
      )}

      <nav className={styles.quickNav}>
        <Link to="/formulas" className={styles.quickLink}><BookOpen size={15} /> Formulas</Link>
        <span className={styles.dot} aria-hidden="true">·</span>
        <Link to="/practice" className={styles.quickLink}><Calculator size={15} /> Practice</Link>
        <span className={styles.dot} aria-hidden="true">·</span>
        <Link to="/learn" className={styles.quickLink}><Target size={15} /> All Topics</Link>
      </nav>
    </div>
  );
}

function Stat({ value, label }) {
  return (
    <div className={styles.stat}>
      <span className={styles.statValue}>{value}</span>
      <span className={styles.statLabel}>{label}</span>
    </div>
  );
}

function TopicSection({ title, count, topics }) {
  return (
    <section className={styles.section}>
      <div className={styles.sectionHead}>
        <h2 className={styles.sectionTitle}>{title}</h2>
        <span className={styles.sectionCount}>{count}</span>
      </div>
      <div className={styles.list}>
        {topics.map(t => <TopicRow key={t.id} topic={t} />)}
      </div>
    </section>
  );
}

const TOPIC_DESCRIPTIONS = {
  'limits': 'Squeeze theorem, epsilon-delta, evaluating limits at infinity.',
  'derivatives': 'Rates of change, tangent lines, differentiation rules.',
  'chain_rule': 'Differentiating compositions with the chain rule.',
  'applications_of_derivatives': "Optimization, related rates, L'Hôpital's rule.",
  'integrals': 'Antiderivatives, the Fundamental Theorem, basic integration.',
  'integration_techniques': 'Substitution, by parts, trig sub, partial fractions.',
  'integration_by_parts': 'LIATE strategy, tabular integration, product integrands.',
  'partial_fractions': 'Decomposing rational functions for integration.',
  'trig_substitution': 'Eliminating radicals with Pythagorean identities.',
  'improper_integrals': 'Infinite limits and discontinuous integrands.',
  'sequences_series': 'Convergence tests — ratio, root, comparison, integral.',
  'power_series': 'Radius and interval of convergence.',
  'taylor_maclaurin': 'Taylor expansions and polynomial approximations.',
  'polar_coordinates': 'Polar curves, area, coordinate conversion.',
  'parametric_equations': 'Parametric curves, arc length, surface area.',
  'differential_equations': 'Separable ODEs and integrating factors.',
  'exponential': 'Growth, decay, and the natural base e^x.',
  'inverse': 'Reversing functions, horizontal line test.',
  'continuity': 'Removable, jump, and infinite discontinuities.',
  'derivative_rules': 'Power, product, quotient, chain rules.',
  'tangent': 'Tangent lines via derivatives and point-slope.',
  'optimization': 'Max/min with first and second derivatives.',
  'related_rates': 'Linking rates via implicit differentiation.',
  'area': 'Riemann sums and the definite integral.',
  'disk': 'Disks and washers for volumes of revolution.',
  'shell': 'Cylindrical shells for volumes around vertical axes.',
  'work': 'Work done by variable forces via integration.',
  'arc_length': 'Curve lengths via integration.',
  'substitution': 'Reversing the chain rule with u-substitution.',
  'fundamental_theorem': 'FTC Parts I & II — bridging derivatives and integrals.',
};

function getTopicDescription(topic) {
  if (topic.description?.trim() && topic.description.trim() !== 'AI lesson, guided examples, and practice linked to this section.') {
    return topic.description.trim();
  }
  const id = (topic.id || '').toLowerCase().replace(/[\s.]+/g, '_').replace(/[^a-z0-9_]/g, '');
  const title = (topic.title || '').toLowerCase();
  for (const [k, v] of Object.entries(TOPIC_DESCRIPTIONS)) {
    if (id.includes(k) || k.includes(id) || title.includes(k.replace(/_/g, ' '))) return v;
  }
  return "Build fluency in " + topic.title + ".";
}

function TopicRow({ topic }) {
  const desc = getTopicDescription(topic);
  return (
    <Link to={"/learn/" + topic.id} className={styles.row}>
      <span className={styles.rowId}>{topic.id}</span>
      <div className={styles.rowBody}>
        <span className={styles.rowTitle}>{topic.title}</span>
        <span className={styles.rowDesc}><MathMarkdown>{desc}</MathMarkdown></span>
      </div>
      <span className={styles.rowBadge}>{CALC_LEVEL_LABELS[topic.calc_level] || '–'}</span>
      <ChevronRight size={14} className={styles.rowArrow} />
    </Link>
  );
}
