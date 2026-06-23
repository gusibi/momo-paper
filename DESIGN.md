---
version: "alpha"
name: "Momo Paper"
description: "A routed design system for documents and visual narratives."
colors:
  primary: "#244C7A"
  on-primary: "#FAF8F4"
  primary-muted: "#DCE7F2"
  secondary: "#172033"
  on-secondary: "#FAF8F4"
  tertiary: "#B65C3A"
  on-tertiary: "#FFFFFF"
  tertiary-muted: "#F2E1D9"
  background: "#FAF8F4"
  surface: "#F2EFE8"
  text: "#172033"
  text-muted: "#4C566A"
  border: "#D8D2C4"
  primary-hover: "#1F426A"
  primary-active: "#1A3758"
  surface-hover: "#E8E5DE"
  surface-active: "#DFDCD5"
  border-hover: "#C2BDB0"
  border-active: "#B1ACA1"
  success: "#2F6B4F"
  warning: "#A46A21"
  on-warning: "#000000"
  danger: "#9A3D3D"
  info: "#3C6587"
  data-primary: "#244C7A"
  data-secondary: "#5C7FA3"
  data-tertiary: "#8EAAC3"
  data-accent: "#B65C3A"
  data-positive: "#2F6B4F"
  data-negative: "#9A3D3D"
  data-neutral: "#7D8798"
typography:
  display:
    fontFamily: "Noto Serif SC, Source Han Serif SC, Songti SC, serif"
    fontSize: 64px
    fontWeight: 700
    lineHeight: 1.15
    letterSpacing: -0.02em
  title:
    fontFamily: "Noto Serif SC, Source Han Serif SC, Songti SC, serif"
    fontSize: 40px
    fontWeight: 700
    lineHeight: 1.15
    letterSpacing: -0.02em
  section-title:
    fontFamily: "Noto Serif SC, Source Han Serif SC, Songti SC, serif"
    fontSize: 32px
    fontWeight: 600
    lineHeight: 1.3
  subtitle:
    fontFamily: "Inter, Noto Sans SC, PingFang SC, sans-serif"
    fontSize: 18px
    fontWeight: 500
    lineHeight: 1.55
  body:
    fontFamily: "Inter, Noto Sans SC, PingFang SC, sans-serif"
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.75
  body-small:
    fontFamily: "Inter, Noto Sans SC, PingFang SC, sans-serif"
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.55
  caption:
    fontFamily: "Inter, Noto Sans SC, PingFang SC, sans-serif"
    fontSize: 11px
    fontWeight: 500
    lineHeight: 1.3
    letterSpacing: 0.04em
  metric:
    fontFamily: "IBM Plex Sans, Inter, sans-serif"
    fontSize: 48px
    fontWeight: 600
    lineHeight: 1.15
  mono:
    fontFamily: "IBM Plex Mono, SFMono-Regular, monospace"
    fontSize: 12px
    fontWeight: 400
    lineHeight: 1.55
spacing:
  none: 0px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  2xl: 48px
  3xl: 64px
  4xl: 80px
  5xl: 96px
  6xl: 128px
rounded:
  none: 0px
  sm: 4px
  md: 8px
  lg: 12px
  pill: 999px
components:
  document-page:
    backgroundColor: "{colors.background}"
    textColor: "{colors.text}"
    typography: "{typography.body}"
    padding: 48px
  hero-title:
    textColor: "{colors.text}"
    typography: "{typography.display}"
  section-heading:
    textColor: "{colors.text}"
    typography: "{typography.section-title}"
  eyebrow:
    textColor: "{colors.primary}"
    typography: "{typography.caption}"
  card:
    backgroundColor: "{colors.background}"
    textColor: "{colors.text}"
    rounded: "{rounded.lg}"
    padding: 24px
  fact-card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.text}"
    rounded: "{rounded.md}"
    padding: 24px
  kpi-card:
    backgroundColor: "{colors.primary-muted}"
    textColor: "{colors.text}"
    rounded: "{rounded.md}"
    padding: 24px
  metric-value:
    textColor: "{colors.primary}"
    typography: "{typography.metric}"
  insight-callout:
    backgroundColor: "{colors.tertiary-muted}"
    textColor: "{colors.text}"
    rounded: "{rounded.md}"
    padding: 24px
  chart-frame:
    backgroundColor: "{colors.background}"
    textColor: "{colors.text}"
    rounded: "{rounded.md}"
    padding: 24px
  primary-action:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    rounded: "{rounded.sm}"
    padding: 12px
  footer-meta:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.text-muted}"
    typography: "{typography.caption}"
    padding: 16px
  section-band:
    backgroundColor: "{colors.secondary}"
    textColor: "{colors.on-secondary}"
    rounded: "{rounded.none}"
    padding: 32px
  accent-marker:
    backgroundColor: "{colors.tertiary}"
    textColor: "{colors.on-tertiary}"
    rounded: "{rounded.sm}"
    padding: 8px
  divider-line:
    backgroundColor: "{colors.border}"
    rounded: "{rounded.none}"
    height: 1px
  status-success:
    backgroundColor: "{colors.success}"
    textColor: "{colors.on-primary}"
    rounded: "{rounded.pill}"
    padding: 8px
  status-warning:
    backgroundColor: "{colors.warning}"
    textColor: "{colors.on-warning}"
    rounded: "{rounded.pill}"
    padding: 8px
  status-danger:
    backgroundColor: "{colors.danger}"
    textColor: "{colors.on-primary}"
    rounded: "{rounded.pill}"
    padding: 8px
  status-info:
    backgroundColor: "{colors.info}"
    textColor: "{colors.on-primary}"
    rounded: "{rounded.pill}"
    padding: 8px
  chart-series-primary:
    backgroundColor: "{colors.data-primary}"
    rounded: "{rounded.none}"
    size: 12px
  chart-series-secondary:
    backgroundColor: "{colors.data-secondary}"
    rounded: "{rounded.none}"
    size: 12px
  chart-series-tertiary:
    backgroundColor: "{colors.data-tertiary}"
    rounded: "{rounded.none}"
    size: 12px
  chart-series-accent:
    backgroundColor: "{colors.data-accent}"
    rounded: "{rounded.none}"
    size: 12px
  chart-series-positive:
    backgroundColor: "{colors.data-positive}"
    rounded: "{rounded.none}"
    size: 12px
  chart-series-negative:
    backgroundColor: "{colors.data-negative}"
    rounded: "{rounded.none}"
    size: 12px
  chart-series-neutral:
    backgroundColor: "{colors.data-neutral}"
    rounded: "{rounded.none}"
    size: 12px
---

## Overview

Momo Paper is a document-first design system for routed documents, slide decks, visual sheets, charts, and embedded diagrams. Its visual language is rational, editorial, quiet, credible, and information-first.

The system must make generated artifacts feel like members of one publishing family, not like separate UI experiments. Agents should resolve the requested artifact through `document_type -> route -> template -> tokens -> checklist` before designing or coding.

Canonical supporting files:

- `assets/design-tokens.json` is the detailed machine-readable token source.
- `assets/artifact-presets.json` is the route registry.
- `references/DESIGN.md` is the full design-system manual.
- `references/prompt-contracts.md` defines agent routing and input rules.
- `references/style-checklist.md` is the final QA gate.

## Colors

The palette uses warm paper neutrals, deep ink, restrained blue authority, and a single clay accent. Color should encode structure, emphasis, state, or data meaning. It should not create a new personality per screen.

### Role assignment

- Use `background` (`#FAF8F4`) for page paper and printed output.
- Use `surface` (`#F2EFE8`) for secondary panels, summary strips, and quiet contrast.
- Use `text` (`#172033`) for primary reading and `text-muted` (`#4C566A`) for metadata, captions, and secondary labels.
- Use `primary` (`#244C7A`) for route identity, key headings, selected states, and restrained emphasis.
- Use `primary-muted` (`#DCE7F2`) for light tinted backgrounds that need to carry the primary identity without heavy contrast.
- Use `tertiary` (`#B65C3A`) only as the secondary emphasis color. It should be rare and deliberate — a single accent per view at most.
- Use `tertiary-muted` (`#F2E1D9`) for insight callouts and warm-tinted backgrounds that need to stand apart from the primary palette.
- Use semantic colors only for states and claims: `success` (`#2F6B4F`), `warning` (`#A46A21`), `danger` (`#9A3D3D`), `info` (`#3C6587`).
- Use data colors only inside charts and diagram primitives. The data palette (`data-primary` through `data-neutral`) must not leak into page chrome or body text.

### Interaction states

Each interaction state resolves to an explicit token — never compute a shade at runtime. The `*-hover` / `*-active` tokens are the pre-derived tonal steps:

| State | Background token | Border token |
|---|---|---|
| **Default** | Base token as-is | `border` (`#D8D2C4`) |
| **Hover** | `primary-hover` (`#1F426A`) for primary fills; `surface-hover` (`#E8E5DE`) for surfaces | `border-hover` (`#C2BDB0`) |
| **Active / Pressed** | `primary-active` (`#1A3758`); `surface-active` (`#DFDCD5`) for surfaces | `border-active` (`#B1ACA1`) |
| **Disabled** | `surface` at 60 % opacity | `border` at 50 % opacity |
| **Selected** | `primary-muted` background, `primary` text | `primary` at 40 % opacity |

When the base is already dark (`secondary`, `primary`), the `*-active` step is already the darker end; do not darken further.

### Constraints

- Do not add ad hoc gradients, neon palettes, decorative glows, random textures, or route-specific brand colors.
- Large background areas must remain `background` or `surface`. Never fill a full-bleed section with `primary` or `tertiary` unless it is a `section-band` component.
- Body text on `background` must hold ≥ 7:1 contrast (WCAG AAA for long reading). Body text on `surface` must hold ≥ 4.5:1 (WCAG AA).
- Caption and `text-muted` on `background` must hold ≥ 4.5:1.
- Data colors inside charts do not need to meet text-contrast rules, but chart labels placed on data fills must hold ≥ 3:1.

## Typography

Momo Paper uses serif headlines for editorial authority, sans-serif body text for clarity, data sans for metrics, and mono only for code or raw technical values.

### Token assignment

- Use `display` (64 px, serif, 700) for covers, opening claims, and major section openers.
- Use `title` (40 px, serif, 700) and `section-title` (32 px, serif, 600) for route titles and chart-led headings.
- Use `subtitle` (18 px, sans, 500) for summary statements and short section intros.
- Use `body` (16 px, sans, 400) and `body-small` (14 px, sans, 400) for reading content.
- Use `caption` (11 px, sans, 500, 0.04 em tracking) for metadata, labels, figure notes, and source notes.
- Use `metric` (48 px, IBM Plex Sans, 600) for large numeric claims and KPI cards.
- Use `mono` (12 px, IBM Plex Mono, 400) only for code snippets, raw IDs, and technical strings.

### Constraints

- Headlines should be short, factual, and conclusion-led. Avoid slogan-like copy and generic AI phrasing.
- Use at most three distinct `fontWeight` values in a single view. The standard set is 400 (body), 500 (subtitle / caption), 600–700 (headings). Do not introduce 300 or 800+.
- Never set `fontSize`, `lineHeight`, `fontWeight`, or `letterSpacing` by hand. Always reference a typography token.
- Serif and sans-serif must not swap roles: serif is for headings and display only; sans-serif is for body, labels, and UI controls.
- `metric` font (IBM Plex Sans) is reserved for numeric emphasis. Do not use it for running text.
- When a heading and body text are vertically adjacent, keep at least a 1.5× size ratio between them so the hierarchy is unambiguous.

## Layout

Layouts are routed, not improvised. Choose one legal public `document_type` or one legal internal `surface.document_shape` from `assets/artifact-presets.json`. Unsupported combinations must fail fast instead of being approximated.

### Document types

Public document types:

- `one_pager`, `long_doc`, `letter`, `portfolio`, `resume`, `slides`, `equity_report`, `changelog`, `process_flow`, `timeline`, `faq_page`, `case_study`, `research_summary`, `stats_report`, `infographic`, `landing`

Internal surfaces:

- `web_dual`: browser-readable and print-safe documents.
- `slides`: one point per slide with large readable type.
- `visual_sheet`: one dominant reading path, compressed prose, and high information density.
- `landing`: marketing page route with its own route reference and template.

### Information hierarchy

Every layout should expose information in this order:

1. Main conclusion.
2. Supporting argument or evidence.
3. Detail and annotation.
4. Method, source, or metadata.

### Spacing rhythm

Use spacing from this file or `assets/design-tokens.json` only. Do not free-type arbitrary spacing values. Follow a three-step rhythm:

| Level | Token | Value | Usage |
|---|---|---|---|
| Intra-group | `sm` | 8 px | Between items inside a card, between label and value, between icon and text |
| Inter-group | `md` | 16 px | Between cards in a row, between heading and first paragraph, between form fields |
| Inter-section | `xl`–`2xl` | 32–48 px | Between major document sections, before and after dividers, hero-to-content gap |

- Page-level padding uses `3xl` (64 px) on desktop and `lg` (24 px) on mobile.
- Cards use `lg` (24 px) internal padding. Compact cards may use `md` (16 px). Hero areas use `xl` (32 px).
- Prefer whitespace and hierarchy before adding separators or decoration.

### Breakpoints

| Name | Min-width | Behavior |
|---|---|---|
| `xs` | 0 | Single column, `lg` (24 px) side padding |
| `sm` | 480 px | Single column, `xl` (32 px) side padding |
| `md` | 768 px | Optional two-column grid for cards and data panels |
| `lg` | 1024 px | Full two-column or three-column grid; side padding `2xl` (48 px) |
| `xl` | 1280 px | Content max-width 960 px, centered; side padding grows |

Content max-width is 960 px for reading-heavy routes (`one_pager`, `long_doc`, `letter`, `case_study`, `research_summary`). Data-heavy routes (`stats_report`, `equity_report`) may extend to 1120 px. `slides` and `visual_sheet` are viewport-width.

### Print layout

`web_dual` artifacts must produce usable print output:

- All content inside a 190 mm × 277 mm live area (A4 with 10 mm margins).
- No content hidden behind `overflow: hidden`, horizontal scroll, or viewport-dependent layout.
- Background colors print only for `section-band` and explicit data fills; all other surfaces degrade to white.

## Elevation & Depth

Depth is structural, not decorative. Hierarchy comes from tonal surfaces and borders first, so shadows stay subtle.

### Shadow tiers

Apply these `box-shadow` values:

| Tier | Usage | Value |
|---|---|---|
| **Flat** | Default cards, fact cards, chart frames | `none` — use `border` (`#D8D2C4`) 1 px solid instead |
| **Raised** | Floating panels, sticky headers, TOC sidebar | `0 1px 3px rgba(23, 32, 51, 0.06), 0 1px 2px rgba(23, 32, 51, 0.04)` |
| **Overlay** | Tooltips, popovers, dropdown menus | `0 4px 12px -2px rgba(23, 32, 51, 0.08), 0 2px 4px rgba(23, 32, 51, 0.04)` |
| **Modal** | Dialogs, lightboxes, full overlays | `0 8px 24px -4px rgba(23, 32, 51, 0.12), 0 4px 8px rgba(23, 32, 51, 0.06)` |

Shadow color is derived from `secondary` (`#172033`) to keep shadows warm rather than pure black.

### Constraints

- Avoid heavy drop shadows, glassmorphism, blur panels, skeuomorphic depth, and stacked card walls.
- Default document surfaces should look printable. If a `web_dual` artifact loses structure when shadows are removed, the design is invalid.
- Pair each shadow tier with its expected border-radius: flat and raised use `rounded.md` (8 px); overlay uses `rounded.lg` (12 px); modal uses `rounded.lg` (12 px).
- `@media print` must set all `box-shadow` to `none`. Structure must survive shadow removal.

## Motion

Motion is functional, not decorative. In a document-first system, most surfaces are static. Use motion only when it clarifies a state change or spatial transition.

### Easing and duration

| Category | Duration | Easing | Examples |
|---|---|---|---|
| **Micro** | 120 ms | `cubic-bezier(0.2, 0, 0, 1)` | Hover fill, focus ring, toggle state |
| **Standard** | 200 ms | `cubic-bezier(0.2, 0, 0, 1)` | Tooltip reveal, accordion expand, popover open |
| **Emphasis** | 300 ms | `cubic-bezier(0.175, 0.885, 0.32, 1.05)` | Modal enter, page-level overlay, slide transition |

- Use `0 ms` (no transition) as the default. Only add motion when the state change would be confusing without it.
- Never use motion longer than 400 ms. Never use looping, bouncing, or attention-grabbing animation.
- Color and opacity transitions use **Micro** timing. Layout and transform transitions use **Standard** or **Emphasis**.

### Reduced motion

- Honor `prefers-reduced-motion: reduce` by collapsing all durations to `0 ms` and disabling transform-based animations.
- Motion must never carry meaning. If disabling all motion makes a state change invisible, add a non-animated visual cue (color, icon, or text change).

### Print media

- `@media print` must disable all transitions and animations (`* { animation: none !important; transition: none !important; }`).

## Shapes

Corners are subtle. Each radius maps to a specific surface category:

| Token | Value | Usage |
|---|---|---|
| `rounded.none` | 0 px | Dividers, full-bleed section bands, rule lines |
| `rounded.sm` | 4 px | Buttons, action chips, accent markers, inline tags |
| `rounded.md` | 8 px | Document cards, fact cards, KPI cards, chart frames, callouts, input fields |
| `rounded.lg` | 12 px | Major containers, hero panels, modals, popovers |
| `rounded.pill` | 999 px | Status labels, metadata chips, compact tags, avatar badges |

### Constraints

- Keep one radius family per view. Do not mix sharp corners (`none`) and rounded corners (`md`, `lg`) on sibling elements at the same hierarchy level.
- Borders should be thin (1 px) and structural, using `border` color. Thick borders (2–3 px) are reserved for strong section breaks, selected states, or diagram emphasis — not routine decoration.
- Never use border-radius values outside the token set.

## Components

Compose documents from a small stable set of components:

- Core: title block, eyebrow, summary strip, body paragraph, quote block, fact card, divider section, footer/meta bar.
- Data: KPI card, chart frame, legend, insight callout, method note, table block.
- Navigation: table of contents, section anchor, step rail, pagination marker.
- Diagrams: architecture, flowchart, quadrant, bar chart, line chart, donut, state machine, timeline, swimlane, tree, layer stack, venn, candlestick, waterfall.

### Interaction states

Interactive components (buttons, links, table rows, nav anchors) must implement all four states:

| State | Background | Text | Border | Cursor |
|---|---|---|---|---|
| **Default** | Component token value | Component token value | Component token value | `pointer` for actions, `default` for content |
| **Hover** | `primary-hover` / `surface-hover` | No change | `border-hover` | `pointer` |
| **Active** | `primary-active` / `surface-active` | No change | `border-active` | `pointer` |
| **Disabled** | `surface` at 60 % opacity | `text-muted` at 50 % opacity | `border` at 50 % opacity | `not-allowed` |
| **Focus** | No change from default | No change | Two-layer ring (see Accessibility) | As default |

- Hover and active transitions use **Micro** timing (120 ms, `cubic-bezier(0.2, 0, 0, 1)`).
- Disabled elements must remove pointer events (`pointer-events: none` plus `cursor: not-allowed` on the wrapper).
- Selected state (for toggles, nav items, tabs) uses `primary-muted` background and `primary` text.

### Charts and diagrams

Charts and diagrams are embedded primitives, not standalone document types. Draw only when the visual teaches better than a paragraph. Auto-select charts from structured data:

- Proportional breakdown: donut.
- Time series: line.
- Category comparison: bar.
- Price history: candlestick.
- Value decomposition: waterfall.

Each chart needs one explicit takeaway, secondary legends, consistent number formats, and source or method notes when credibility depends on data.

## Voice & Content

Copy is part of the design. Keep it precise, evidence-aware, and free of filler. For the full tone guide, see `references/VOICE.md`. The following rules apply directly inside templates and generated output:

- **Headlines**: Write as a conclusion, not a topic label. `Revenue grew 23 % YoY` not `Revenue Overview`.
- **Case**: Use sentence case for all headings, body, labels, and captions. Title Case only for proper nouns and product names.
- **Actions**: Name actions with a verb and a noun (`Download Report`, `View Timeline`). Never use bare verbs (`Submit`, `Confirm`) or vague labels (`Click Here`, `OK`).
- **Numbers**: Use numerals for all quantities (`3 sections`, `¥12.4 B`). Spell out numbers only at the start of a sentence.
- **Errors and empty states**: State what happened, then what to do: `No data for this period. Try a wider date range.`
- **Avoid**: `successfully`, `please`, `simply`, `just`, marketing superlatives, and generic AI phrasing (`Let's dive in`, `Here's a comprehensive overview`).
- **Source attribution**: Every data claim must cite its source inline or in a method note. Unsourced claims are a design bug.
- Use proper punctuation: curly quotes (" "), em dashes (—), and the ellipsis character (…).

## Accessibility

Accessibility is structural, not optional. Every generated artifact must be usable without a mouse, without color vision, and at up to 200 % zoom.

### Contrast

| Element | Minimum contrast ratio | Standard |
|---|---|---|
| Body text on `background` | 7:1 | WCAG AAA |
| Body text on `surface` or `primary-muted` | 4.5:1 | WCAG AA |
| `caption` and `text-muted` on `background` | 4.5:1 | WCAG AA |
| Large text (≥ 24 px or ≥ 18.66 px bold) | 3:1 | WCAG AA |
| Chart labels on data fills | 3:1 | WCAG AA |
| Non-text elements (borders, icons, controls) | 3:1 | WCAG 1.4.11 |

### Focus indicators

Every interactive element must show a visible focus indicator at `:focus-visible`. Never remove `outline` without a visible replacement.

Default focus ring — two-layer `box-shadow`:

```css
box-shadow: 0 0 0 2px #FAF8F4, 0 0 0 4px #244C7A;
```

This creates a 2 px gap in the page `background` color, then a 2 px `primary` ring. When the surface is `surface` or `primary-muted`, swap the inner color to match.

### Semantic HTML

- Use a single `<h1>` per page matching the document title.
- Heading levels must not skip (`<h1>` → `<h3>` is invalid).
- Use `<main>`, `<nav>`, `<article>`, `<section>`, `<aside>`, `<footer>` landmarks appropriately.
- Tables must use `<thead>`, `<th scope="col">`, and `<th scope="row">` for data tables.
- Interactive elements must be `<button>` or `<a>`, never `<div onclick>`.
- All images must have `alt` text. Decorative images use `alt=""` and `aria-hidden="true"`.

### State signaling

- Do not signal state with color alone. Every color-based state (success, warning, danger, info) must be paired with an icon, text label, or pattern.
- Disabled elements must use both visual dimming and `aria-disabled="true"`.

## Do's and Don'ts

Do:

- Resolve the route before writing layout code.
- Lead with the conclusion in the first screen, first printed page, or first slide.
- Keep one section focused on one purpose.
- Use only approved tokens, components, chart types, and diagram primitives.
- Preserve print-safe behavior for `web_dual`.
- Keep copy restrained, specific, and evidence-aware.
- Hold WCAG AA contrast minimum (4.5:1 for body text); prefer AAA (7:1) for long reading.
- Show the focus ring on every interactive element at `:focus-visible`.
- Apply typography tokens instead of setting font size, line height, or weight by hand.
- Use the spacing rhythm: `sm` inside groups, `md` between groups, `xl`–`2xl` between sections.
- Run `references/style-checklist.md` before shipping.

Don't:

- Do not create dashboards; dashboards are outside this system.
- Do not treat `comparison_matrix` or `topic_cover` as document types.
- Do not reintroduce `preset_id` as a public model.
- Do not invent new fonts, colors, gradients, decorative motifs, or unsupported routes.
- Do not use motion to carry meaning; all motion must degrade gracefully.
- Do not make charts decorative.
- Do not document legacy aliases as the preferred interface.
- Do not signal state with color alone; pair it with an icon or text label.
- Do not use `surface` as a general fill; it is for secondary panels and subtle separation only.
- Do not mix rounded and sharp corners on sibling elements at the same hierarchy level.
- Do not use more than three `fontWeight` values in one view.
- Do not remove an `outline` without a visible `:focus-visible` replacement.
- Do not swap semantic colors for data colors or vice versa.

## Agent Implementation Rules

Before changing frontend, template, chart, diagram, or showcase code, read this file first. Then load the smallest supporting spec that covers the task:

- Routing changes: `assets/artifact-presets.json`, `references/prompt-contracts.md`, `references/DESIGN.md`, `references/document-types.md`, matching route reference, templates, and showcase copy.
- Token or style changes: `assets/design-tokens.json`, `references/DESIGN.md`, affected templates, diagrams, and showcase files.
- New document output: matching route reference, template, `references/VOICE.md`, and `references/style-checklist.md`.
- Diagram work: `references/diagrams.md` and the matching file in `assets/diagrams/`.

If this file and another design file disagree, treat the disagreement as a bug. Fix the contract instead of silently choosing one.
