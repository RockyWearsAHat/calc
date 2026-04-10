---
applyTo: "src/**/*.{jsx,css,html}"
description: "Calculus Mastery design system. Enforces visual quality, component patterns, and professional polish across the entire frontend. Research-backed by Linear, Vercel, Raycast, Stripe, and Brilliant design systems."
---

# Calculus Mastery — Design System Instructions

This document is the single source of truth for all visual, component, and interaction design decisions in the Calculus Mastery platform. Every agent editing frontend files MUST read and follow these rules.

## Design Philosophy

The app is a **precision learning instrument**, not a textbook portal. Every surface should communicate:

- **Calm confidence** — dark, low-chroma, no visual noise
- **High material quality** — layered translucency, thick rounded surfaces, subtle reflections
- **Strong hierarchy** — one dominant element per viewport, clear scan path
- **Intentional motion** — slow, quiet, premium; no twitchy micro-interactions
- **Minimal but meaningful ornament** — every flourish has a job; decorative-only elements are removed

### Design References (Researched)

These products define the quality bar. Study their patterns before making any visual change:

| Product | What to learn from it |
|---------|----------------------|
| **Linear** | Dark sidebar navigation, glass morphism with restraint, electric blue accent discipline, keyboard-first UX |
| **Vercel** | Dashboard card hierarchy, metric telemetry layout, sidebar-to-content ratio, minimal badge/pill design |
| **Raycast** | Floating command bar, pill-based navigation, smoked-glass panels, monospace telemetry, clean icon system |
| **Stripe** | Typography scale precision, documentation layout, code block treatment, gradient accent restraint |
| **Brilliant** | Educational card design, progress visualization, interactive problem layout, mastery state indicators |

### Anti-References (What NOT to do)

- Generic edtech brightness (white backgrounds, cartoon icons, rainbow badges)
- Dashboard-builder aesthetics (cramped stat grids, competing charts)
- Material Design defaults without customization
- Gratuitous glass/blur on every surface (performance killer, visual noise)

---

## Color System

### Dark Theme (Primary)

```
Background tiers:
  --color-bg-primary:    #0d0d0f     (deepest, body)
  --color-bg-secondary:  #141416     (recessed panels)
  --color-bg-tertiary:   #17171b     (raised surfaces)
  --color-bg-card:       #1a1a1e     (cards, containers)
  --color-bg-elevated:   #202024     (popovers, dropdowns)
  --color-bg-hover:      #25252a     (hover states)
  --color-bg-glass:      rgba(26, 26, 30, 0.85) (backdrop-filter surfaces)

Accent system (THREE accents only):
  Intelligence:  #5b9bd5 / #6cb6ff   — AI features, active nav, focus rings, CTAs
  Mastery:       #d4a84a / #d8c08f   — achievement, progress completion, rewards ONLY
  Success:       #4ade80 / #7be0a9   — correct answers, validation passes

Rules:
  - Blue is the PRIMARY accent for ALL interactive elements
  - Gold/champagne is ONLY for earned achievements — never on buttons, nav, or generic UI
  - Green is ONLY for success states — correct answers, passed checks
  - Red (#f87171) is ONLY for errors and destructive actions
  - Warning yellow (#fbbf24) is ONLY for caution states
```

### Light Theme

The light theme must feel equally premium — NOT a white version of a dark app.

```
Background tiers:
  --color-bg-primary:    #ffffff
  --color-bg-secondary:  #f7f7f8
  --color-bg-card:       #ffffff with subtle border
  
Accent system:
  Intelligence:  #2563eb (darker blue for white backgrounds)
  Mastery:       #c4922a
  
Text hierarchy must maintain WCAG AA contrast on all surfaces.
```

### Color Rules (Enforced)

1. **Never use gold as a CTA fill.** Primary buttons are blue.
2. **Never use more than 3 accent colors on a single screen.**
3. **Border colors are `rgba(255, 255, 255, 0.06-0.18)` in dark mode** — never solid colors.
4. **Glow effects use the accent color at 6-22% opacity** — never higher.
5. **No colored backgrounds on cards** — cards are `--color-bg-card` with border only.

---

## Typography

### Font Stack

```
UI / Body:     'Noto Sans', 'Segoe UI', system-ui, sans-serif
Display:       'Lato', 'Noto Sans', 'Segoe UI', system-ui, sans-serif
Mono / Code:   'JetBrains Mono', 'Fira Code', monospace
Math:          'KaTeX_Main', 'Times New Roman', serif (via KaTeX)
```

### Type Scale

```
Hero headline:     clamp(3rem, 6vw, 5rem)  — weight 700, tracking -0.03em
Page title:        1.8rem                   — weight 700, tracking -0.03em
Section title:     1.38rem                  — weight 700, tracking -0.03em
Card title:        1rem                     — weight 700
Body:              0.95rem                  — weight 400, line-height 1.6
Small / Labels:    0.84rem                  — weight 600
Eyebrow / Badge:   0.72rem                 — weight 700, tracking 0.12em, uppercase
Mono telemetry:    0.78rem                  — JetBrains Mono, tracking 0.08em
```

### Typography Rules (Enforced)

1. **Navigation NEVER uses serif fonts.** Always the UI sans-serif.
2. **Headings use the display font** with tight tracking (`-0.03em`).
3. **Eyebrow labels are ALWAYS** uppercase, wide-tracked (0.12em), weight 700, small (0.72rem).
4. **Math formulas render through KaTeX** — never use plain text for math expressions.
5. **Multiplication uses `\cdot` or `×`** — never asterisk `*`.
6. **No text shadow anywhere.** Hierarchy comes from weight and opacity, not effects.

---

## Spacing System

```
--space-xs:   0.25rem (4px)
--space-sm:   0.5rem  (8px)
--space-md:   1rem    (16px)
--space-lg:   1.5rem  (24px)
--space-xl:   2rem    (32px)
--space-2xl:  2.5rem  (40px)
--space-3xl:  4rem    (64px)
```

### Spacing Rules

1. **Section-to-section gaps are `--space-xl` minimum** (32px).
2. **Card internal padding is `--space-lg`** (24px) for standard cards, `--space-xl` for hero cards.
3. **Grid gutters are 16px** for dense grids, 20px for card grids.
4. **Header height is 56px.** Content starts below header with `--space-lg` gap minimum.
5. **Max content width is 1400px** for dashboards, 900px for reading content, 800px for settings.

---

## Border Radius System

```
--radius-xs:   8px    (small badges, code blocks)
--radius-sm:   10px   (buttons, inputs, small cards)
--radius-md:   16px   (standard cards, panels)
--radius-lg:   24px   (large cards, sections)
--radius-xl:   32px   (hero sections)
--radius-pill: 999px  (nav links, chips, badges, status pills)
```

### Radius Rules

1. **Navigation links and badges are ALWAYS pill radius** (999px).
2. **Cards use `--radius-lg` (24px) minimum** — never less.
3. **Hero sections use 32-36px radius.**
4. **Never mix sharp corners and rounded corners** in the same visual region.
5. **Buttons match their container language** — pill buttons in pill contexts, `--radius-md` in card contexts.

---

## Shadow System

```
--shadow-xs:          0 1px 2px rgba(0, 0, 0, 0.2)
--shadow-sm:          0 1px 3px rgba(0, 0, 0, 0.24), 0 1px 2px rgba(0, 0, 0, 0.12)
--shadow-md:          0 3px 8px rgba(0, 0, 0, 0.28), 0 1px 3px rgba(0, 0, 0, 0.16)
--shadow-lg:          0 8px 24px rgba(0, 0, 0, 0.32), 0 2px 6px rgba(0, 0, 0, 0.16)
--shadow-panel:       0 16px 48px rgba(0, 0, 0, 0.4), 0 4px 12px rgba(0, 0, 0, 0.2)
--shadow-glow:        0 0 0 1px rgba(91, 155, 213, 0.06), 0 2px 12px rgba(91, 155, 213, 0.06)
--shadow-card-hover:  0 8px 24px rgba(0, 0, 0, 0.32), 0 0 0 1px rgba(91, 155, 213, 0.1)
```

### Shadow Rules

1. **Cards at rest use `--shadow-xs`** — barely visible, just enough to separate from background.
2. **Card hover uses `--shadow-card-hover`** — lift + subtle blue ring.
3. **Never use hard black drop shadows.**
4. **Glow is reserved for AI-related elements and active focus states.**
5. **Maximum one `backdrop-filter: blur()` surface per viewport** — the header shell.

---

## Component Patterns

### Navigation (Header Shell)

```
Structure: Sticky floating shell with glass background
Layout:    Grid: [logo] [nav rail] [status + theme toggle]
Behavior:  Stays on top, glass effect, pointer-events passthrough on padding
```

Rules:
- The header shell is the ONLY element with `backdrop-filter: blur()`
- Nav links are pill-shaped, 36px min-height
- Active nav link: blue background at 10% opacity + blue border at 30% opacity + subtle bottom indicator
- Inactive nav links: `--color-text-secondary`, hover → `--color-text-primary` with `--color-bg-hover`
- The sync status chip is INSIDE the shell — never a separate floating element

### Cards

```
Default:   --color-bg-card bg, 1px --color-border border, --radius-lg radius, --shadow-xs shadow
Hover:     translateY(-2px), border-color → accent, shadow → --shadow-card-hover
Content:   Never identical boilerplate across cards — each must have unique descriptive content
```

Rules:
- **Every card must have unique, meaningful content.** Repeating the same description across multiple cards is PROHIBITED.
- Cards hover with lift + border tint + shadow — never with background color swap.
- Card grids must not have empty placeholder cells. If the item count is odd, either add content or adjust the grid to accommodate.

### Buttons

Three families ONLY:

```
Primary:    Solid blue fill (--color-accent-primary), white text, used for THE main action
Secondary:  --color-bg-tertiary bg, --color-border border, used for alternatives
Ghost:      Transparent bg, --color-text-secondary text, used for low-priority
```

Rules:
- **Primary buttons are BLUE, never gold.**
- All buttons: `--radius-md` in card contexts, `--radius-pill` in hero/nav contexts.
- Hover: `translateY(-1px)` lift + darker shade.
- Active: `scale(0.98)` press.
- Disabled: `opacity: 0.5; cursor: not-allowed;`

### Inputs

```
Background:    --color-bg-secondary (darker than card)
Border:        1px solid --color-border
Focus:         border-color → accent, box-shadow → 0 0 0 3px --color-accent-ring
Focus-visible: 2px outline in accent color
```

Rules:
- Inputs embed into the surface — slightly darker than their container.
- Focus ring is electric blue at 25% opacity.
- Placeholder text uses `--color-text-muted`.

### Progress Indicators

```
Track:      Thin (4-6px), --color-bg-secondary bg, pill radius
Fill:       Accent color gradient
Minimum:    Even at 1%, the fill bar must be visibly rendered (min-width: 8px)
Telemetry:  Numeric value displayed above or beside the track
```

Rules:
- Blue for active study progress.
- Gold for mastery completion.
- Green for validated success.
- **Near-invisible progress bars (< 3%) must still be visually discernible.**

### Formula / Math Blocks

```
Container:    --color-bg-secondary bg, 1px --color-border-subtle border, --radius-sm radius
Left accent:  2px blue bar at 30% opacity
Padding:      0.75rem 1.25rem
Overflow:     overflow-x: auto for long formulas
```

Rules:
- All math renders through KaTeX. Plain text math expressions are PROHIBITED.
- Display math (`$$...$$`) gets the container treatment.
- Inline math (`$...$`) flows naturally in text.

### Chat / Tutor Panel

```
Window:     Fixed bottom-right, 380px wide, max-height 580px
Surface:    --color-bg-card, --radius-xl, --shadow-panel
Messages:   User bubbles right-aligned, bot bubbles left-aligned
Input:      Bottom-anchored with border-top separator
```

Rules:
- The FAB ("Ask Tutor") must NOT overlap other interactive elements.
- If a page already has a dedicated tutor interface (e.g., Practice mode), the global FAB is hidden.
- Bot messages render through `MathMarkdown` for formula support.

---

## Motion System

```
--transition-fast:    140ms cubic-bezier(0.16, 1, 0.3, 1)
--transition-base:    240ms cubic-bezier(0.16, 1, 0.3, 1)
--transition-slow:    480ms cubic-bezier(0.16, 1, 0.3, 1)
--transition-spring:  500ms cubic-bezier(0.34, 1.56, 0.64, 1)
```

### Motion Rules

1. **One signature animation per page.** Dashboard: hero stagger. Practice: mode card stagger. Learn: concept card slide.
2. **All hover/focus transitions use `--transition-fast`** (140ms).
3. **Page entry animations use `fadeInUp`** with staggered delays (60ms per child, max 6 children).
4. **The header sync dot is the ONLY permanently animating element** — its pulse is slow (2.5s) and subtle.
5. **Respect `prefers-reduced-motion`** — all animations collapse to 0.01ms.
6. **Animate ONLY `transform` and `opacity`** for performance. Never animate `width`, `height`, `margin`, or `padding`.

---

## Page-Specific Rules

### Dashboard

- Hero section: Two-column grid on desktop (content + console), single column on mobile.
- The hero headline uses the largest type size in the app.
- The "Study Engine" panel must display REAL state — not placeholder "Ready for launch" text.
- Topic cards must have UNIQUE descriptions per topic — never identical boilerplate.
- The "Quick Access" section should use the same card language as topic cards.

### Learn

- Sidebar + content layout: sidebar 280px fixed, content fills remainder.
- Sidebar topic list must have clear visual grouping between Calc I and Calc II sections.
- Concept cards use step-through navigation (prev/next) with progress indicator.
- Formula boxes inside lessons have the standard formula container treatment.
- The contextual chat panel (not global) appears inline or in a drawer.

### Practice

- Mode selector: 2×2 grid on desktop, stacked on mobile.
- Each mode card has a unique accent color (`--mode-color` CSS custom property).
- The active problem panel is the dominant visual element — center stage.
- Hints/walkthroughs use progressive disclosure — not all visible at once.
- The session telemetry (mastery, streak, accuracy) uses monospace font and the metric card pattern.

### Formulas

- Category sections with left-accent header bars.
- Formula grids must NOT have empty placeholder cells.
- If a section has an odd number of formulas, the last card spans full width OR the grid adjusts.
- The "Quick Reference" section matches the card language of formula categories.

### Settings

- Settings page must have ACTUAL configurable settings — a settings page with zero settings is a credibility failure.
- At minimum: theme toggle, AI model preference, Canvas sync status, data export.
- Each setting group uses the section card pattern with left blue accent bar.

---

## Accessibility Requirements

1. **WCAG AA contrast** on all text — minimum 4.5:1 for body text, 3:1 for large text.
2. **Focus-visible rings** on all interactive elements — never `outline: none` without replacement.
3. **The glow/orb accent is supplementary** — never the only status indicator.
4. **Icon stroke weight is consistent** across the entire app — all icons from the same Lucide weight.
5. **`aria-label` on all icon-only buttons.**
6. **`prefers-reduced-motion` respected** everywhere.
7. **Semantic HTML** — `<nav>`, `<main>`, `<section>`, `<article>` used correctly.

---

## Performance Constraints

1. **Maximum one `backdrop-filter: blur()` surface** in the viewport (the header).
2. **No stacked CSS filters** inside nested cards.
3. **Blur values ≤ 20px.**
4. **No constantly moving backgrounds or repeating shimmer animations.**
5. **Images use lazy loading** (`loading="lazy"`) for below-fold content.
6. **Bundle size awareness** — no unnecessary dependencies for visual effects.

---

## Content Quality Rules

1. **No placeholder or boilerplate text in production.** Every visible string must be meaningful.
2. **Topic card descriptions must be UNIQUE per topic** — describe what that specific topic covers.
3. **Math expressions use proper notation** — `×` not `*`, `·` not `*`, KaTeX for all formulas.
4. **Error messages are human-readable and actionable** — not raw HTTP codes or stack traces.
5. **Loading states use skeleton patterns or spinner** — never blank white space.
6. **Empty states have intentional design** — illustration + explanation + CTA to resolve.
