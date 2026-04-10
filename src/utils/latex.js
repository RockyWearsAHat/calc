/**
 * LaTeX preprocessing utilities.
 *
 * The AI backend sometimes returns LaTeX without the $...$ or $$...$$ delimiters
 * that remark-math needs. These helpers detect bare LaTeX and add delimiters so
 * KaTeX renders correctly.
 */

const LATEX_CMD_RE =
  /\\(?:frac|sqrt|int|sum|prod|lim|log|ln|sin|cos|tan|sec|csc|cot|exp|text|left|right|cdot|times|pm|mp|infty|partial|nabla|alpha|beta|gamma|delta|epsilon|theta|lambda|mu|pi|rho|sigma|phi|psi|omega|Delta|Sigma|Pi|Omega|leq|geq|neq|approx|equiv|to|rightarrow|leftarrow|mathbb|mathrm|operatorname|displaystyle|begin|end)(?![a-zA-Z])/;

const BRACED_SUB_SUPER = /[_^]\{[^}]*\}/;

// Bare subscript: log_b, x_0, a_n  (letter/digit followed by _ then letter/digit)
const BARE_SUBSCRIPT = /[a-zA-Z0-9]_[a-zA-Z0-9]/;

// Unescaped math functions written as plain text: ln(...), log(...), sin(...)
const PLAIN_MATH_FN = /(?:^|[^a-zA-Z])(?:ln|log|sin|cos|tan|exp|lim)\s*\(/;

function containsLatex(s) {
  return (
    LATEX_CMD_RE.test(s) ||
    BRACED_SUB_SUPER.test(s) ||
    BARE_SUBSCRIPT.test(s) ||
    PLAIN_MATH_FN.test(s)
  );
}

const COMMON_WORDS_2 = new Set([
  'is', 'of', 'if', 'in', 'an', 'to', 'so', 'or', 'no', 'be', 'do',
  'we', 'he', 'it', 'at', 'by', 'on', 'as', 'up', 'am', 'my',
]);

function isMathLike(token) {
  if (!token || /^\s+$/.test(token)) return false;
  const clean = token.replace(/[,;:.!?]+$/, '');
  if (!clean) return false;
  if (containsLatex(clean)) return true;
  if (/^[0-9.]+$/.test(clean)) return true;
  if (clean.length === 1 && /[a-zA-Z0-9=+\-*/<>]/.test(clean)) return true;
  if (/^[=+\-*/<>≤≥≈·×]+$/.test(clean)) return true;
  if (/^[a-zA-Z]\([^)]*\)$/.test(clean)) return true;
  if (/^[a-zA-Z]{2,}\([^)]*\)$/.test(clean)) return true;  // ln(2.5), log(x)
  if (/^[a-zA-Z]{2,}\([^)]*\)\/?$/.test(clean)) return true;  // ln(c/a)/
  if (/^[a-zA-Z]{2}$/.test(clean) && !COMMON_WORDS_2.has(clean.toLowerCase())) return true;
  if (/[{}^_\\]/.test(clean)) return true;
  return false;
}

/**
 * Wrap a known-formula string in display-math delimiters.
 * No-ops if already delimited.
 */
export function wrapFormula(text) {
  if (!text) return '';
  const t = text.trim();
  if (t.startsWith('$')) return t;
  return `$$${latexifyDisplay(t)}$$`;
}

/**
 * Preprocess text that may contain undelimited LaTeX.
 * - Content already containing $ delimiters is returned as-is.
 * - Short formula-like lines are wrapped as display math.
 * - Prose lines get individual math expressions wrapped inline.
 */
export function preprocessLatex(text) {
  if (!text || typeof text !== 'string') return text || '';

  // Replace asterisk multiplication inside existing $ delimiters too
  let result = text.replace(/(\$\$?)([^$]+?)(\$\$?)/g, (m, open, body, close) => {
    return open + body.replace(/(?<=[0-9a-zA-Z})])\s*\*\s*(?=[0-9a-zA-Z({\\])/g, ' \\cdot ') + close;
  });

  if (result.includes('$')) return result;
  if (!containsLatex(result)) return result;

  return result.split('\n').map(processLine).join('\n');
}

function processLine(line) {
  const t = line.trim();
  if (!t || !containsLatex(t)) return line;
  if (/^[#\-*>|`]/.test(t)) return line;

  const words = t.split(/\s+/);
  const hasProseWord = words.some(
    (w) => /^[a-zA-Z]{3,}$/.test(w.replace(/[,;:.!?]+$/, ''))
  );

  if (!hasProseWord) {
    return `$$${latexifyDisplay(t)}$$`;
  }

  return wrapMathInProse(t);
}

/**
 * Find math expressions in prose text and wrap each in $...$.
 *
 * Splits on whitespace, marks LaTeX-containing tokens, then expands outward
 * to absorb adjacent math-like tokens (variables, operators, numbers).
 * Expansion stops at English words (3+ lowercase letters).
 */
function wrapMathInProse(text) {
  const parts = text.split(/(\s+)/);
  const n = parts.length;
  const inMath = new Array(n).fill(false);

  for (let i = 0; i < n; i++) {
    if (/^\s*$/.test(parts[i]) || !containsLatex(parts[i])) continue;
    inMath[i] = true;

    // Expand left — properly skip whitespace to reach adjacent tokens
    let j = i - 1;
    while (j >= 0) {
      if (/^\s+$/.test(parts[j])) {
        if (j > 0 && isMathLike(parts[j - 1])) {
          inMath[j] = true;
          inMath[j - 1] = true;
          j -= 2;
        } else {
          break;
        }
      } else if (isMathLike(parts[j])) {
        inMath[j] = true;
        j--;
      } else {
        break;
      }
    }

    // Expand right
    j = i + 1;
    while (j < n) {
      if (/^\s+$/.test(parts[j])) {
        if (j + 1 < n && isMathLike(parts[j + 1])) {
          inMath[j] = true;
          inMath[j + 1] = true;
          j += 2;
        } else {
          break;
        }
      } else if (isMathLike(parts[j])) {
        inMath[j] = true;
        j++;
      } else {
        break;
      }
    }
  }

  // Build result — consecutive inMath parts become one expression.
  // Expressions containing fraction patterns (/) are promoted to display math
  // for full-size rendering, like a textbook does.
  const FRACTION_PATTERN = /[a-zA-Z0-9)}\]]\s*\/\s*[a-zA-Z0-9({\\]/;

  let result = '';
  let i = 0;
  while (i < n) {
    if (inMath[i]) {
      let expr = '';
      while (i < n && inMath[i]) {
        expr += parts[i];
        i++;
      }
      expr = expr.trim();
      let trailing = '';
      const pm = expr.match(/([,;:.!?]+)$/);
      if (pm) {
        trailing = pm[1];
        expr = expr.slice(0, -trailing.length).trim();
      }
      if (expr) {
        if (FRACTION_PATTERN.test(expr)) {
          expr = latexifyDisplay(expr);
          if (result && !/\s$/.test(result)) result += ' ';
          result += `\n\n$$${expr}$$${trailing}\n\n`;
        } else {
          expr = latexifyInline(expr);
          if (result && !/\s$/.test(result)) result += ' ';
          result += `$${expr}$${trailing}`;
        }
      }
    } else {
      result += parts[i];
      i++;
    }
  }

  return result;
}

/**
 * Convert bare math function names (ln, log, sin, etc.) to LaTeX commands
 * (\ln, \log, \sin) so KaTeX renders them upright.
 * Also normalizes multiplication signs: * → \cdot
 */
function latexifyFunctions(expr) {
  let s = expr.replace(
    /(?<!\\)\b(ln|log|sin|cos|tan|sec|csc|cot|exp|lim|min|max|det|gcd)(?=[^a-zA-Z]|$)/g,
    '\\$1'
  );
  // Convert * to proper multiplication dot
  s = s.replace(/\s*\*\s*/g, ' \\cdot ');
  return s;
}

/**
 * Convert slash-division notation into LaTeX fractions.
 * @param {string} expr - The expression to process
 * @param {string} cmd - The fraction command: 'frac' for inline, 'dfrac' for display
 */
function latexifyFractions(expr, cmd = 'frac') {
  let s = expr;

  // 1. Function/function: \func(...) / \func(...)
  s = s.replace(
    /(\\[a-z]+)\(([^()]*)\)\s*\/\s*(\\[a-z]+)\(([^()]*)\)/g,
    `\\${cmd}{$1($2)}{$3($4)}`
  );

  // 2. (X)/(Y) style
  s = s.replace(
    /\(([^()]+)\)\s*\/\s*\(([^()]+)\)/g,
    `\\${cmd}{$1}{$2}`
  );

  // 3. Simple token/token: dy/dx, a/b
  s = s.replace(
    /(?<![a-zA-Z0-9}\\()])([a-zA-Z0-9]+(?:\^{[^}]*})?)\s*\/\s*([a-zA-Z0-9]+(?:\^{[^}]*})?)(?![a-zA-Z0-9({])/g,
    `\\${cmd}{$1}{$2}`
  );

  return s;
}

/**
 * Promote plain delimiters to \left...\right when they contain tall content
 * like fractions, integrals, sums, or superscripts/subscripts with braces.
 * This makes parentheses and brackets grow to match their content height.
 */
function autoSizeDelimiters(expr) {
  // Already has \left/\right — skip
  if (/\\left/.test(expr)) return expr;

  const TALL_CONTENT = /\\(?:frac|dfrac|int|sum|prod|sqrt)|[_^]\{/;

  // Match outermost paired delimiters: (...) and [...]
  // Process from innermost outward by repeated passes
  let s = expr;
  let prev;
  do {
    prev = s;
    // Parentheses containing tall content
    s = s.replace(
      /(?<!\\left)\(([^()]*(?:\\(?:frac|dfrac|int|sum|prod|sqrt)[^()]*|[_^]\{[^}]*\}[^()]*))\)(?!\\right)/g,
      (m, inner) => TALL_CONTENT.test(inner) ? `\\left(${inner}\\right)` : m
    );
    // Square brackets containing tall content
    s = s.replace(
      /(?<!\\left)\[([^\[\]]*(?:\\(?:frac|dfrac|int|sum|prod|sqrt)[^\[\]]*|[_^]\{[^}]*\}[^\[]*))\](?!\\right)/g,
      (m, inner) => TALL_CONTENT.test(inner) ? `\\left[${inner}\\right]` : m
    );
  } while (s !== prev);

  return s;
}

/** Prettify for inline math — functions + inline fractions (\frac) + auto-sized delimiters. */
function latexifyInline(expr) {
  let s = latexifyFunctions(expr);
  s = latexifyFractions(s, 'frac');
  s = autoSizeDelimiters(s);
  return s;
}

/** Prettify for display math — functions + full-size fractions (\dfrac) + auto-sized delimiters. */
function latexifyDisplay(expr) {
  let s = latexifyFunctions(expr);
  s = latexifyFractions(s, 'dfrac');
  s = autoSizeDelimiters(s);
  return s;
}
