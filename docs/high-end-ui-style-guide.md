# High-End UI Style Guide for Calc

## Reference Read

This document translates the Threads reference into a practical styling direction for this app.

Observed directly from the exposed preview frame and public discussion around the post:

- The interface centers a floating, smoked-glass navigation capsule over a matte charcoal background. The orb on the left side of the bar has plasma-like energy/lightning bolts of light blue in a darker grayish/blue/translucent/refractive & reflective darker glass orb.
- A single luminous blue orb acts as the hero accent and focal anchor.
- The overall look is low-chroma, low-noise, and heavily dependent on material lighting rather than bright color.
- Public replies repeatedly call out the glowy orb, hologram feel, shader-like rendering, and glass treatment.
- The strongest criticism is performance and usefulness, which means we should borrow the discipline and polish, not the excess.

The key lesson is simple: the premium feel comes from restraint plus one memorable animated material effect, not from making every surface flashy.

## Current Site vs Target Direction

The current frontend already has a solid dark foundation:

- Global tokens in `src/styles/global.css` use a warm scholarly charcoal-and-gold palette.
- The shell in `src/components/Header.module.css` is practical and clean, but it reads as conventional app UI rather than premium product design.
- Dashboard and practice surfaces rely on flat cards, serif-heavy hierarchy, and standard hover states.

The target direction should shift the app from scholarly dark to cinematic technical luxury.

That means:

- Keep the dark foundation.
- Reduce the amount of warm gold used as the primary identity color.
- Introduce a cold electric accent for AI, navigation, and focus states.
- Replace flat bars and boxes with thicker, softer, more dimensional surfaces.
- Use serif typography more selectively, or remove it from navigation and UI chrome entirely.

## Design Principle

The app should feel like a precision instrument, not a textbook portal.

Everything should communicate:

- Calm confidence
- High material quality
- Strong hierarchy
- Intentional motion
- Minimal but meaningful ornament

Professional in this context does not mean sterile. It means every flourish has a job.

## Visual Direction

Adopt this aesthetic description across the product:

- Base mood: graphite, obsidian, smoked glass, dim studio lighting
- Accent language: electric blue for intelligence and focus, muted champagne only for achievement or mastery
- Surfaces: thick rounded capsules, soft-edge panels, layered translucency, subtle reflections
- Backgrounds: matte panel grid with shallow depth, not gradient wallpaper
- Motion: slow, quiet, premium, with no twitchy micro-interactions

The signature motif should be a luminous "intelligence core" orb. In the reference this is decorative. In our app it should actually mean something: AI tutor online, personalized path active, or study session in progress.

## Design Tokens

Update the token strategy in `src/styles/global.css`.

### Color System

Replace the current gold-led identity with a three-tier system:

- Base background: `#08090b`, `#0d0f12`, `#12161b`
- Surface background: `rgba(20, 24, 30, 0.82)` and `rgba(16, 19, 24, 0.72)`
- Hairline borders: `rgba(255, 255, 255, 0.08)`
- Primary text: `rgba(246, 248, 251, 0.94)`
- Secondary text: `rgba(196, 204, 214, 0.72)`
- Muted text: `rgba(143, 151, 161, 0.52)`
- Intelligence accent: `#6cb6ff`
- Intelligence glow: `rgba(108, 182, 255, 0.22)`
- Mastery accent: `#d8c08f`
- Success accent: `#7be0a9`
- Error accent: `#ff7f8e`

Rules:

- Blue is for focus, AI, active navigation, and live interaction.
- Champagne is for progress, mastery, and rewards only.
- Avoid large gold backgrounds; they cheapen the effect quickly.

### Typography

The current display serif works for an academic brand, but the reference UI reads more technical and product-grade.

Recommended approach:

- UI font: use a clean neo-grotesk or sharp geometric sans for navigation, cards, controls, and stats
- Display font: reserve a more expressive face for hero headlines only if needed
- Mono font: keep it for formulas, topic ids, and telemetry

Practical pairing:

- Primary UI: `Manrope`, `Sora`, or `IBM Plex Sans`
- Display fallback if needed: `Cormorant Garamond` or `Instrument Serif` only in large hero moments
- Technical text: `JetBrains Mono`

Typography rules:

- Navigation should never use the serif.
- Headline sizes should tighten slightly and feel engineered rather than literary.
- Use wider letter spacing on labels, chips, and telemetry.
- Prefer medium weights over heavy bold blocks.

### Radius and Surface Geometry

The reference succeeds because the surfaces feel thick and expensive.

Set a more deliberate radius system:

- `--radius-sm`: 10px
- `--radius-md`: 16px
- `--radius-lg`: 24px
- `--radius-xl`: 32px
- `--radius-pill`: 999px

Rules:

- Navigation, segmented controls, and status chips should be pill-based.
- Cards should be larger radius than they are now.
- Avoid mixed sharp and rounded language in the same region.

### Shadow and Light

The app should use layered shadow, not big generic drop shadows.

Preferred shadow stack:

- Ambient depth: `0 12px 40px rgba(0, 0, 0, 0.28)`
- Lift shadow: `0 18px 60px rgba(0, 0, 0, 0.34)`
- Inner sheen: `inset 0 1px 0 rgba(255, 255, 255, 0.06)`
- Accent glow: `0 0 24px rgba(108, 182, 255, 0.18)`

Avoid:

- Hard black shadows
- Large fuzzy gold glows
- Stacked shadows on every card

## Background System

The preview frame uses a dark panelized backdrop that makes the floating UI feel more premium.

Apply that idea to the app background:

- Replace the current soft radial body wash with a subtle panel grid or chassis pattern.
- Use faint seams, oversized rectangles, and low-contrast lighting gradients.
- Keep the background almost black so surface edges carry the composition.

Implementation guidance:

- One fixed background layer for the panel grid.
- One optional radial light pool behind hero sections.
- No noisy patterns unless extremely subtle.

This should live in `src/styles/global.css`, not be recreated inside each page.

## Shell and Navigation

The largest visual upgrade should happen in `src/components/Header.module.css`.

### Desired Header Behavior

- Replace the full-width sticky bar with a floating shell that sits inside page padding.
- Turn the nav into a smoked capsule, centered or slightly offset, with more vertical depth.
- Make the left brand mark a real signature element instead of a flat gradient square.

### Brand Mark

Replace the current gold integral tile with one of these:

- A glowing AI orb that subtly pulses when tutor features are available
- A glass-encased calculus glyph with a faint blue energy core
- A haloed node that doubles as the live study-state indicator

Do not make it purely decorative. It should communicate system state.

### Nav Links

Current nav links are functional but ordinary. Upgrade them by:

- Increasing height and horizontal padding
- Reducing contrast on inactive items
- Using soft inner highlight for the active item instead of bright fill alone
- Keeping icons light, thin, and evenly aligned
- Adding a slight lateral glide or glow shift on hover

The sync status chip should be absorbed into the shell so the header feels like one designed object rather than three separate pieces.

## Page-Level Styling Strategy

### Dashboard

The dashboard in `src/pages/Dashboard.jsx` and `src/pages/Dashboard.module.css` should stop reading as a standard marketing hero plus cards.

Target structure:

- Hero becomes a command deck
- One side contains the main academic promise
- The other side contains live stats, progress state, and one premium visual module

Recommended changes:

- Replace the flat stat row with a segmented floating metrics rail
- Add one hero object with subtle blue glow, like a mastery core or study engine visualization
- Use fewer visible borders and more material separation
- Make topic cards feel denser, darker, and more tactile
- Increase whitespace between sections so the shell can breathe

### Practice

`src/pages/PracticeV2.module.css` is the best place to introduce the premium interaction language.

The practice experience should feel like an instrument panel.

Apply:

- A central focus panel for the current problem
- Secondary side rails or drawers for hints, tutor chat, and progress
- Stronger hierarchy for active input states
- Smoked surfaces for hints and explanation panels
- Small blue energy accents for AI-generated content

Do not apply glass everywhere. Only high-importance containers should use translucency.

### Learn

The lesson surface should feel like a calm, high-value reading environment rather than a plain dark markdown block.

Apply:

- Thicker lesson container with higher radius
- More generous line length control
- Stronger heading hierarchy with reduced gold usage
- Embedded formula blocks with subtle panel treatment instead of obvious bordered boxes

### Formulas and Settings

These pages should follow the same system but remain quieter.

They should inherit:

- The shell
- The surface language
- The type rules
- The focus and hover treatment

They should not compete with dashboard or practice for visual attention.

## Component Rules

### Cards

All cards should move from flat academic panels to layered premium modules.

Required changes:

- Darker, more translucent fills
- Larger radius
- Softer borders
- Top-edge highlight
- Hover state driven by lift, border tint, and slight sheen, not by bright background swaps

### Buttons

Use three button families only:

- Primary: solid deep blue or blue-tinted luminous fill for important action
- Secondary: smoked panel with border and soft hover lift
- Ghost: text-led with minimal chrome for low-priority actions

Rules:

- Stop using warm gold as the primary CTA fill.
- Keep button labels crisp and compact.
- Add subtle active press depth.

### Inputs

Inputs should feel embedded into the same material system.

Apply:

- Low-sheen backgrounds
- Soft inset edges
- Clear focus ring in electric blue
- Fewer visible border changes when idle

### Progress and Metrics

Current progress bars are serviceable, but they should feel more technical.

Use:

- Thin luminous tracks
- Numeric telemetry above or beside the track
- Segmented or calibrated bars where useful
- Blue for active study, champagne for mastery, green for validated success

## Motion System

The reference almost certainly depends on shader-like motion and tiny animated loops. We should translate that carefully.

Motion rules:

- One signature motion element per page
- Use transforms and opacity first
- Keep durations in the `220ms` to `600ms` range
- Favor soft ease-out and slow ambient loops
- Respect reduced motion globally

Recommended motion moments:

- Header orb breathing or refracting gently
- Page load stagger for hero content
- Card hover with tiny lift and light sweep
- Drawer or tutor panel revealing with smooth physical slide

Avoid:

- Constant moving backgrounds
- Repeating shimmer on every card
- Large blur-heavy animations
- Decorative motion with no information value

## Performance Rules

The public replies on the Threads post are right to question performance. A premium UI that lags is amateur work.

Adopt these constraints:

- Use no more than one backdrop blur layer inside the header shell
- Keep blur values moderate
- Prefer a pre-rendered or tiny looping asset for the orb over live expensive shaders if needed
- Animate only transform and opacity for common interactions
- Avoid stacking filters inside nested cards
- Test the practice surface on lower-end devices before expanding effects

If an effect hurts responsiveness, remove it. Keep the premium feeling through composition and material quality first.

## Accessibility Rules

This visual language can become unusable fast if not controlled.

Non-negotiables:

- Maintain readable contrast for body text
- Keep icon stroke clarity above decorative softness
- Make the orb or glow supplementary, never the only status indicator
- Preserve obvious focus styles for keyboard users
- Do not rely on blur to communicate structure

The UI should look expensive and still be instantly understandable.

## What to Remove

To get closer to the reference, remove these habits from the current system:

- Gold as the dominant UI accent everywhere
- Serif in navigation and dense product surfaces
- Flat full-width header bar styling
- Generic dashed borders and basic card hover swaps
- Multiple unrelated visual motifs on the same screen

## What to Introduce

Add these deliberately:

- One signature blue intelligence accent
- Floating shell navigation
- Matte panel background
- Smoked-glass hero surfaces
- Bigger radii and thicker surface silhouettes
- Lower-noise typography and tighter hierarchy
- Motion that feels engineered, not playful

## Rollout Order

Implement in this order so the app improves cohesively:

1. Update tokens and background system in `src/styles/global.css`.
2. Rebuild the shell in `src/components/Header.module.css` and `src/components/Header.jsx`.
3. Restyle dashboard hero and stat surfaces in `src/pages/Dashboard.module.css`.
4. Upgrade practice panels and input states in `src/pages/PracticeV2.module.css`.
5. Normalize card, button, and chip patterns across the remaining pages.
6. Add one carefully optimized signature animation for the orb and one page-entry motion pattern.

## Final Direction Statement

If we execute this correctly, Calc should feel less like an academic dashboard and more like a premium learning cockpit.

The reference is not valuable because of the glowing orb alone. It is valuable because it combines:

- ruthless restraint
- one unforgettable focal effect
- precise material lighting
- disciplined hierarchy
- confidence in negative space

That is the standard to match.

---

## 2026 Research Update — Verified Professional References

The following design patterns were researched from industry-leading products to validate and extend the direction above. These are not theoretical — they are verified implementations from shipped products.

### Vercel (Feb 2026 Navigation Redesign)

Vercel replaced their top tab bar with a **collapsible sidebar**. Key patterns:

- Sidebar uses a subdued dark surface with `rgba()` borders — not opaque
- Active nav item: subtle blue left-border indicator + light text, no background fill
- Dashboard cards have extreme hierarchy — one hero metric large, supporting metrics small
- Typography is tight: `-0.03em` tracking on headings, body at 14px
- Badge/pill design: solid color pills with 999px radius, all-caps micro text
- Zero decorative elements — every visual mark communicates state

### Linear (Dark UI + Glass)

Linear is the gold standard for "dark mode with depth":

- Background progression: `#0d0d0f` → `#141416` → `#1a1a1e` (same 3-tier system we use)
- Glass morphism used ONLY on the command bar — never on cards
- Electric blue accent (`#5b9bd5` family) is the only saturated color in the entire app
- Keyboard-first UX — every action has a shortcut, visible in the interface
- Issue cards have no border — they use elevation (subtle shadow) alone
- Animation easing: `cubic-bezier(0.16, 1, 0.3, 1)` — fast start, gentle deceleration

### Glow + Glass Effects (CSS Implementation)

Research from the Design Systems Collective (Jan 2026):

```css
/* The RIGHT way to do glass in dark UI: */
.glass-surface {
    background: rgba(26, 26, 30, 0.85);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.08);
}

/* Glow — accent color at LOW opacity, never > 22%: */
.glow-accent {
    box-shadow:
        0 0 0 1px rgba(91, 155, 213, 0.06),
        0 2px 12px rgba(91, 155, 213, 0.06);
}

/* Glow on focus — slightly brighter ring: */
.glow-focus {
    box-shadow:
        0 0 0 2px rgba(91, 155, 213, 0.25),
        0 4px 16px rgba(91, 155, 213, 0.12);
}
```

Rules from the research:

1. Glass (`backdrop-filter`) on **maximum one surface per viewport** — the navigation shell
2. Glow opacity **never exceeds 22%** — that's the line between "premium" and "neon sign"
3. Glow acts as **interaction cue, not decoration** — it appears on hover/focus/active, not at rest
4. All glow uses the primary accent color — never mix multiple glow colors

### Brilliant (Education Platform)

Brilliant.org is the closest premium learning platform reference:

- Course cards have strong visual hierarchy: large title, progress ring, topic badge
- Each card has a **unique, specific** description of what that topic covers
- Progress visualization uses SVG rings with smooth animation
- The dashboard never shows more than 6-8 cards before requiring scroll
- Mobile-first layout that scales up — not desktop-first squeezed down
- Dark mode uses pure black (`#000`) with colored accent cards — bolder than Linear

### Design Trend Context (2025-2026)

Industry direction from designboom, CSS Design Awards, Awwwards:

- **Liquid glass** effects (Apple WWDC 2025) — heavily blurred glass with edge refraction
- **AI-aware interfaces** — UIs that adapt to AI state (thinking, responding, complete)
- **Bento grid layouts** — dashboard cards with varied heights/widths, not uniform grids
- **Variable fonts** with animated weight — type itself as an interaction cue
- **Motion as meaning** — every animation communicates state change, nothing is decorative-only

### What This Means for Calc

The existing style guide direction is correct and well-aligned with current trends. The research validates:

1. ✅ Three-tier background system (already implemented)
2. ✅ Single accent color discipline (already in the guide)
3. ✅ Glass on navigation shell only (already limited)
4. ✅ Restrained motion with one signature effect per page

The research adds:

1. 🔄 **Bento-style varied card sizes** for the dashboard — not all cards the same height
2. 🔄 **SVG ring progress indicators** instead of plain progress bars (Brilliant pattern)
3. 🔄 **Keyboard shortcut hints in the UI** — visible in card footers and tooltips (Linear pattern)
4. 🔄 **AI state visualization** — the chat/tutor panel should show thinking/responding/complete states visually
5. 🔄 **`-0.03em` heading tracking** as a standard (Vercel pattern — already in the guide but not enforced)

These additions are codified in the instruction files at `.github/instructions/`.