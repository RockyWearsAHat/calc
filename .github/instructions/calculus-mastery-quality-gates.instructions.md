---
applyTo: "src/**/*.{jsx,css,html}"
description: "Quality gates and verification rules for the Calculus Mastery platform. Agents MUST run these checks before declaring any UI work complete."
---

# Calculus Mastery — Quality Gates

Every agent MUST verify these gates before declaring frontend work complete. Each gate is a concrete, testable assertion.

---

## Gate 1: Content Integrity

**No placeholder or boilerplate text may exist in the rendered UI.**

Checks:
- [ ] Dashboard topic cards each have a UNIQUE description (not "AI lesson, guided examples...")
- [ ] No "lorem ipsum" or "coming soon" text in any visible component
- [ ] Study Engine console shows REAL state data, not "Ready for launch" placeholder
- [ ] All menu items link to functional routes
- [ ] Error messages are human-readable with recovery guidance

### How to verify
Open each page in the browser. Read every visible string. If any two cards share identical description text, FAIL.

---

## Gate 2: Visual Consistency

**The design system rules from `calculus-mastery-design-system.instructions.md` are applied uniformly.**

Checks:
- [ ] All cards use `border-radius: 24px` minimum
- [ ] All nav links use `border-radius: 999px` (pill)
- [ ] Primary CTAs are blue, not gold
- [ ] Gold accent appears ONLY on mastery/achievement elements
- [ ] All borders are `rgba(255,255,255, 0.06-0.18)` — no solid colors
- [ ] Icon weights are consistent (same Lucide stroke width across all icons)
- [ ] Only the header shell has `backdrop-filter: blur()`
- [ ] No competing glow effects in the same viewport

### How to verify
Inspect elements via DevTools. Check computed `border-radius`, `border-color`, `backdrop-filter`, and `color` values against the design system tokens.

---

## Gate 3: Math Rendering

**All mathematical content renders through KaTeX. No plain-text math.**

Checks:
- [ ] No asterisk `*` used for multiplication in any rendered content (must be `\cdot`, `\times`, or `×`)
- [ ] Inline math (`$...$`) renders in KaTeX serif, not the UI font
- [ ] Display math (`$$...$$`) is centered in a styled container
- [ ] Formula page cards render all LaTeX without errors
- [ ] Long formulas in the formula grid do not overflow their containers

### How to verify
Navigate to /formulas and /learn. Inspect the DOM — all math should be inside `.katex` wrapper elements. Search the rendered page for literal `*` characters adjacent to numbers.

---

## Gate 4: Grid Integrity

**No empty placeholder cells in any card grid.**

Checks:
- [ ] Formula page: every grid section has no empty trailing cells
- [ ] Dashboard: topic card grid fills completely or uses `grid-auto-flow` to avoid holes
- [ ] Practice: mode selector cards fill their row completely

### How to verify
On each page, inspect card grids. Count items per row. If the last row has fewer items than the grid column count, ensure the layout handles the gap gracefully (spanning, centering, or hiding).

---

## Gate 5: Navigation Completeness

**Every README-listed page is accessible via the header navigation.**

Expected routes:
- [ ] `/` — Dashboard
- [ ] `/learn` — Learn
- [ ] `/practice` — Practice
- [ ] `/formulas` — Formulas
- [ ] `/course` — My Course ← CURRENTLY MISSING
- [ ] `/settings` — Settings

### How to verify
Click every nav link in the header. Each must navigate to a functional page (not a 404 or blank screen). Verify via `App.jsx` routes.

---

## Gate 6: Theme Switching

**Dark and light themes both render correctly with no visual artifacts.**

Checks:
- [ ] Theme toggle in the header switches between dark and light
- [ ] All text maintains WCAG AA contrast ratio in both themes
- [ ] Cards do not have transparent text or invisible borders in either theme
- [ ] KaTeX formulas are legible in both themes
- [ ] Theme preference persists across page reloads (localStorage)

### How to verify
Toggle the theme. Visit every page in both themes. Check contrast ratios using DevTools accessibility audit.

---

## Gate 7: Responsive Layout

**The app is usable on viewports from 375px to 2560px.**

Checks:
- [ ] Header collapses to a compact format below 768px
- [ ] Card grids reflow to single column on mobile
- [ ] No horizontal overflow on any page at 375px width
- [ ] Formula containers support horizontal scroll for long expressions
- [ ] The global chat panel does not obscure critical content on small screens

### How to verify
Use DevTools responsive mode. Set viewport to 375px, 768px, 1024px, 1440px, 2560px. Navigate all pages at each breakpoint.

---

## Gate 8: API Integration

**All frontend API calls successfully connect to the backend.**

Checks:
- [ ] Backend is running on port 8000 (`curl http://localhost:8000/`)
- [ ] Dashboard loads topic data from `/api/curriculum/topics`
- [ ] Practice mode generates problems from `/api/practice/generate`
- [ ] Formula page loads from `/api/formulas/...`
- [ ] Settings page reads/writes user preferences
- [ ] AI tutor responses flow through the global chat and contextual panels
- [ ] Error states display graceful fallback UI (not blank screens or console errors)

### How to verify
Open browser DevTools Network tab. Navigate each page. Every API call should return 200/201. Check for failed requests or CORS errors.

---

## Gate 9: Accessibility

**Core accessibility requirements are met.**

Checks:
- [ ] Every interactive element is keyboard-focusable
- [ ] `focus-visible` ring appears on keyboard navigation
- [ ] Icon-only buttons have `aria-label`
- [ ] Main landmark regions (`<nav>`, `<main>`, `<section>`) are used correctly
- [ ] Color contrast passes WCAG AA (4.5:1 body text, 3:1 large text)
- [ ] `prefers-reduced-motion` disables all animations

### How to verify
Tab through the entire page. Run Lighthouse accessibility audit. Check with `prefers-reduced-motion: reduce` in DevTools emulation.

---

## Gate 10: Performance

**No visual effects degrade rendering performance.**

Checks:
- [ ] Only 1 `backdrop-filter: blur()` element visible at any time
- [ ] No more than 3 CSS transitions running simultaneously during page idle
- [ ] Page load (LCP) under 2.5s on fast 3G throttle
- [ ] No layout shifts (CLS) above 0.1 during page load

### How to verify
Run Lighthouse performance audit. Check DevTools Performance panel for long tasks during scroll.

---

## Gate 11: Feature Completeness (README Alignment)

**Every feature claimed in README.md is implemented and functional.**

README features to verify:
- [ ] "Your AI-powered calculus mastery companion" — AI tutor responds to questions
- [ ] "Structured learning path" — /learn page with progressive topic sequence
- [ ] "Adaptive practice" — /practice generates problems matching skill level
- [ ] "Comprehensive formula reference" — /formulas displays complete formula library
- [ ] "Personal course tracking" — /course page tracks progress ← MISSING
- [ ] "Canvas LMS integration" — settings or course page allows Canvas sync
- [ ] "Copilot CLI fallback" — AI works even if Copilot CLI unavailable ← NOT IMPLEMENTED
- [ ] "Dark mode / light mode" — toggle works
- [ ] "Keyboard shortcuts" — settings page lists shortcuts and they work

### How to verify
Open README.md. For every bullet point or feature claim, navigate to the relevant page and test the feature directly. Document any feature that does not work.

---

## Agent Workflow

When any agent completes frontend work:

1. Save all files
2. Open each affected page in the browser
3. Run through Gates 1-11 relevant to the changes
4. Fix any failures
5. Re-verify until all gates pass
6. Report which gates were checked and their pass/fail status
