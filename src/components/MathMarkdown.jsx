import ReactMarkdown from 'react-markdown';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import 'katex/dist/katex.min.css';
import { wrapFormula, preprocessLatex } from '../utils/latex';

const remarkPlugins = [remarkMath];
const rehypePlugins = [rehypeKatex];

/**
 * Renders markdown with KaTeX math support.
 *
 * Props:
 *  - children: markdown string
 *  - className: optional wrapper class
 *  - formula: when true, the content is a pure LaTeX formula and will be
 *             wrapped in $$...$$ display-math delimiters automatically.
 */
export default function MathMarkdown({ children, className, formula }) {
  if (!children) return null;

  const raw = String(children);
  const content = formula ? wrapFormula(raw) : preprocessLatex(raw);

  return (
    <div className={className} style={{ lineHeight: 1.7 }}>
      <ReactMarkdown remarkPlugins={remarkPlugins} rehypePlugins={rehypePlugins}>
        {content}
      </ReactMarkdown>
    </div>
  );
}
