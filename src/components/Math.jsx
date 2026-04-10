import 'katex/dist/katex.min.css';
import { Component } from 'react';
import { InlineMath, BlockMath } from 'react-katex';

class MathFallbackBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error) {
    console.error('LaTeX error:', error);
  }

  render() {
    if (this.state.hasError) {
      return <code>{this.props.latex}</code>;
    }
    return this.props.children;
  }
}

// Parse text with LaTeX and render appropriately
export function MathText({ children }) {
  if (!children) return null;
  
  // Split by display math first ($$...$$)
  const parts = String(children).split(/(\$\$[\s\S]+?\$\$)/g);
  
  return (
    <>
      {parts.map((part, i) => {
        if (part.startsWith('$$') && part.endsWith('$$')) {
          const latex = part.slice(2, -2);
          return (
            <MathFallbackBoundary key={i} latex={latex}>
              <BlockMath math={latex} />
            </MathFallbackBoundary>
          );
        }
        // Then handle inline math ($...$)
        const inlineParts = part.split(/(\$[^\s$][^$]*?\$)/g);
        return inlineParts.map((inlinePart, j) => {
          if (inlinePart.startsWith('$') && inlinePart.endsWith('$')) {
            const latex = inlinePart.slice(1, -1);
            return (
              <MathFallbackBoundary key={`${i}-${j}`} latex={latex}>
                <InlineMath math={latex} />
              </MathFallbackBoundary>
            );
          }
          return <span key={`${i}-${j}`}>{inlinePart}</span>;
        });
      })}
    </>
  );
}

// Render a single formula with display style
export function Formula({ math, display = false }) {
  if (!math) return null;
  
  try {
    return display ? <BlockMath math={math} /> : <InlineMath math={math} />;
  } catch (e) {
    console.error('LaTeX error:', e);
    return <code>{math}</code>;
  }
}
