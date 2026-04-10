import { useState, useRef, useCallback, useMemo } from 'react';
import katex from 'katex';
import 'katex/dist/katex.min.css';
import styles from './MathInput.module.css';

/**
 * Convert common shorthand math notation into LaTeX.
 * Handles fractions, powers, roots, Greek letters, etc.
 */
function toLatex(raw) {
  let s = raw.trim();
  if (!s) return '';

  // Greek letters
  s = s.replace(/\bpi\b/gi, '\\pi');
  s = s.replace(/\btheta\b/gi, '\\theta');
  s = s.replace(/\balpha\b/gi, '\\alpha');
  s = s.replace(/\bbeta\b/gi, '\\beta');
  s = s.replace(/\bgamma\b/gi, '\\gamma');
  s = s.replace(/\bdelta\b/gi, '\\delta');
  s = s.replace(/\bsigma\b/gi, '\\sigma');
  s = s.replace(/\blambda\b/gi, '\\lambda');
  s = s.replace(/\binfinity\b/gi, '\\infty');
  s = s.replace(/\binf\b/gi, '\\infty');

  // Common math functions
  s = s.replace(/(?<!\\)\b(ln|log|sin|cos|tan|sec|csc|cot|exp|lim|min|max|arcsin|arccos|arctan)\b/g, '\\$1');

  // sqrt(...) → \sqrt{...}
  s = s.replace(/sqrt\(([^)]*)\)/g, '\\sqrt{$1}');

  // Multiplication: * → \cdot
  s = s.replace(/(?<=[0-9a-zA-Z})])\s*\*\s*(?=[0-9a-zA-Z({\\])/g, ' \\cdot ');

  // Plus/minus symbols
  s = s.replace(/\+\/-/g, '\\pm ');
  s = s.replace(/-\+/g, '\\mp ');

  // Comparison operators
  s = s.replace(/<=/g, '\\leq ');
  s = s.replace(/>=/g, '\\geq ');
  s = s.replace(/!=/g, '\\neq ');
  s = s.replace(/~=/g, '\\approx ');

  // (X)/(Y) → \frac{X}{Y}
  s = s.replace(/\(([^()]+)\)\s*\/\s*\(([^()]+)\)/g, '\\frac{$1}{$2}');

  // Simple a/b → \frac{a}{b} (single tokens only, not inside existing \frac)
  s = s.replace(
    /(?<!\\frac\{[^}]*)(?<![a-zA-Z0-9}\\)])([a-zA-Z0-9]+(?:\^{[^}]*})?)\s*\/\s*([a-zA-Z0-9]+(?:\^{[^}]*})?)(?![a-zA-Z0-9({])/g,
    '\\frac{$1}{$2}'
  );

  // x^2 → x^{2}, x^(2n) → x^{2n}
  s = s.replace(/\^(\([^)]+\))/g, (_, inner) => `^{${inner.slice(1, -1)}}`);
  s = s.replace(/\^([0-9]+)/g, '^{$1}');

  // x_n → x_{n}, x_(2n) → x_{2n}
  s = s.replace(/_(\([^)]+\))/g, (_, inner) => `_{${inner.slice(1, -1)}}`);
  s = s.replace(/_([a-zA-Z0-9])/g, '_{$1}');

  return s;
}

/**
 * Try to render LaTeX; returns HTML string or null on error.
 */
function tryRender(latex) {
  if (!latex) return null;
  try {
    return katex.renderToString(latex, {
      throwOnError: false,
      displayMode: true,
      trust: true,
    });
  } catch {
    return null;
  }
}

/**
 * Math-aware input with live KaTeX preview.
 *
 * Props:
 *  - value, onChange, onKeyDown, placeholder, id, autoFocus, className
 *    (forwarded to the underlying <input>)
 *  - previewClassName: optional class for the preview container
 */
export default function MathInput({
  value,
  onChange,
  onKeyDown,
  placeholder,
  id,
  autoFocus,
  className,
  disabled,
}) {
  const inputRef = useRef(null);

  const latex = useMemo(() => toLatex(value || ''), [value]);
  const html = useMemo(() => tryRender(latex), [latex]);
  const showPreview = value && value.trim().length > 0 && html;

  return (
    <div className={styles.wrapper}>
      <input
        ref={inputRef}
        id={id}
        type="text"
        className={`${className || ''} ${styles.input}`}
        value={value}
        onChange={onChange}
        onKeyDown={onKeyDown}
        placeholder={placeholder || 'Type math: x^2, a/b, sqrt(x), pi...'}
        autoFocus={autoFocus}
        disabled={disabled}
        autoComplete="off"
        spellCheck={false}
      />
      {showPreview && (
        <div
          className={styles.preview}
          dangerouslySetInnerHTML={{ __html: html }}
          aria-label="Math preview"
        />
      )}
    </div>
  );
}
