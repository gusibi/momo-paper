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

- Use `background` for page paper and printed output.
- Use `surface` for secondary panels, summary strips, and quiet contrast.
- Use `text` for primary reading and `text-muted` for metadata, captions, and secondary labels.
- Use `primary` for route identity, key headings, selected states, and restrained emphasis.
- Use `tertiary` only as the secondary emphasis color. It should be rare and deliberate.
- Use semantic colors only for states and claims: success, warning, danger, and info.
- Use data colors only inside charts and diagram primitives.

Do not add ad hoc gradients, neon palettes, decorative glows, random textures, or route-specific brand colors. Large background areas must remain neutral or muted.

## Typography

Momo Paper uses serif headlines for editorial authority, sans-serif body text for clarity, data sans for metrics, and mono only for code or raw technical values.

- Use `display` for covers, opening claims, and major section openers.
- Use `title` and `section-title` for route titles and chart-led headings.
- Use `subtitle` for summary statements and short section intros.
- Use `body` and `body-small` for reading content.
- Use `caption` for metadata, labels, figure notes, and source notes.
- Use `metric` for large numeric claims and KPI cards.

Headlines should be short, factual, and conclusion-led. Avoid slogan-like copy and generic AI phrasing.

## Layout

Layouts are routed, not improvised. Choose one legal public `document_type` or one legal internal `surface.document_shape` from `assets/artifact-presets.json`. Unsupported combinations must fail fast instead of being approximated.

Public document types:

- `one_pager`, `long_doc`, `letter`, `portfolio`, `resume`, `slides`, `equity_report`, `changelog`, `process_flow`, `timeline`, `faq_page`, `case_study`, `research_summary`, `stats_report`, `infographic`, `landing`

Internal surfaces:

- `web_dual`: browser-readable and print-safe documents.
- `slides`: one point per slide with large readable type.
- `visual_sheet`: one dominant reading path, compressed prose, and high information density.
- `landing`: marketing page route with its own route reference and template.

Every layout should expose information in this order:

1. Main conclusion.
2. Supporting argument or evidence.
3. Detail and annotation.
4. Method, source, or metadata.

Use spacing from this file or `assets/design-tokens.json` only. Do not free-type arbitrary spacing. Prefer whitespace and hierarchy before adding separators or decoration.

## Elevation & Depth

Depth is structural, not decorative. Use thin borders and low shadows to clarify layers such as cards, chart frames, or floating panels. Avoid heavy drop shadows, glassmorphism, blur panels, skeuomorphic depth, and stacked card walls.

Default surfaces should look printable. If a `web_dual` artifact loses structure when printed or when motion is disabled, the design is invalid.

## Shapes

Corners are subtle. Use small and medium radii for document cards, chart frames, KPI cards, and callouts. Use large radius sparingly for major containers. Use pill radius only for compact tags, status labels, and metadata chips.

Borders should be thin and structural. Thick borders are reserved for strong section breaks or diagram emphasis, not routine decoration.

## Components

Compose documents from a small stable set of components:

- Core: title block, eyebrow, summary strip, body paragraph, quote block, fact card, divider section, footer/meta bar.
- Data: KPI card, chart frame, legend, insight callout, method note, table block.
- Navigation: table of contents, section anchor, step rail, pagination marker.
- Diagrams: architecture, flowchart, quadrant, bar chart, line chart, donut, state machine, timeline, swimlane, tree, layer stack, venn, candlestick, waterfall.

Charts and diagrams are embedded primitives, not standalone document types. Draw only when the visual teaches better than a paragraph. Auto-select charts from structured data:

- Proportional breakdown: donut.
- Time series: line.
- Category comparison: bar.
- Price history: candlestick.
- Value decomposition: waterfall.

Each chart needs one explicit takeaway, secondary legends, consistent number formats, and source or method notes when credibility depends on data.

## Do's and Don'ts

Do:

- Resolve the route before writing layout code.
- Lead with the conclusion in the first screen, first printed page, or first slide.
- Keep one section focused on one purpose.
- Use only approved tokens, components, chart types, and diagram primitives.
- Preserve print-safe behavior for `web_dual`.
- Keep copy restrained, specific, and evidence-aware.
- Run `references/style-checklist.md` before shipping.

Don't:

- Do not create dashboards; dashboards are outside this system.
- Do not treat `comparison_matrix` or `topic_cover` as document types.
- Do not reintroduce `preset_id` as a public model.
- Do not invent new fonts, colors, gradients, decorative motifs, or unsupported routes.
- Do not use motion to carry meaning.
- Do not make charts decorative.
- Do not document legacy aliases as the preferred interface.

## Agent Implementation Rules

Before changing frontend, template, chart, diagram, or showcase code, read this file first. Then load the smallest supporting spec that covers the task:

- Routing changes: `assets/artifact-presets.json`, `references/prompt-contracts.md`, `references/DESIGN.md`, `references/document-types.md`, matching route reference, templates, and showcase copy.
- Token or style changes: `assets/design-tokens.json`, `references/DESIGN.md`, affected templates, diagrams, and showcase files.
- New document output: matching route reference, template, `references/VOICE.md`, and `references/style-checklist.md`.
- Diagram work: `references/diagrams.md` and the matching file in `assets/diagrams/`.

If this file and another design file disagree, treat the disagreement as a bug. Fix the contract instead of silently choosing one.
