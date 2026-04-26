# Momo Paper

> A routed design system for documents and visual narratives.

用一套路由规则统一文档、图示与可视叙事。

## 1. Purpose

Momo Paper keeps agent-generated documents inside one coherent visual family across browser pages, print-safe long documents, decks, infographics, and embedded diagrams.

Primary goals:
- Keep outputs stable across runs and across agents.
- Make routing decisions explicit and reusable.
- Favor clarity, credibility, and information density over spectacle.

Core rule:
`Resolve document_type -> route -> template -> tokens -> checklist.`

## 2. Brand DNA

### Keywords
- Rational
- Credible
- Quiet
- Clear
- Information-first

### Anti-keywords
- Flashy
- Over-decorated
- Poster-like marketing
- Random futuristic UI
- Decoration before information

### Design stance
- Conclusions appear early.
- Headlines are short and factual.
- Visual hierarchy is strong but quiet.
- Diagrams serve teaching, not ornament.
- Color encodes structure and emphasis, not personality drift.

## 3. Taxonomy

### Public document type overlay

The public routing layer is the user-facing entrypoint:

- `one_pager`
- `long_doc`
- `letter`
- `portfolio`
- `resume`
- `slides`
- `equity_report`
- `changelog`
- `process_flow`
- `timeline`
- `faq_page`
- `case_study`
- `research_summary`
- `stats_report`
- `infographic`

### Internal route model

The internal route model controls structure and constraints:

- `surface`: `web_dual | slides | visual_sheet`
- `document_shape`: route-specific structure inside each surface

### Diagram primitive

Diagrams are embedded primitives inside documents, not a document type:
- architecture
- flowchart
- quadrant
- bar chart
- line chart
- donut
- state machine
- timeline
- swimlane
- tree
- layer stack
- venn
- candlestick
- waterfall

### Pattern candidates

These remain outside the public catalog:
- `comparison_matrix`
- `topic_cover`

### Legacy aliases

The old `artifact_type` values remain as compatibility aliases only:
- `web_page` -> `web_dual.explainer`
- `ppt_slide` -> `slides.explainer`
- `infographic` -> `visual_sheet.infographic`
- `article` -> `web_dual.editorial_article`
- `stats_report` -> `web_dual.stats_report`

## 4. Foundations

### Color system
Use only the colors defined in `design-tokens.json`.

Color roles:
- `ink`: primary text and key shapes
- `paper`: background
- `canvas`: secondary background
- `line`: borders and dividers
- `brand`: primary emphasis
- `brandMuted`: restrained fills and light emphasis
- `accent`: secondary emphasis
- `success`, `warning`, `danger`, `info`: semantic states
- `data.*`: chart and diagram colors only

Rules:
- Do not invent new brand colors per route.
- One route may use at most 1 primary brand color and 1 accent color.
- Large backgrounds must stay neutral or use muted brand fills.
- Semantic colors are not decorative.

### Typography
Use only the defined stacks:
- Chinese primary: `Noto Serif SC`, `Source Han Serif SC`, `Songti SC`, serif
- UI and body sans: `Inter`, `Noto Sans SC`, `PingFang SC`, sans-serif
- Numeric/data emphasis: `IBM Plex Sans`, `Inter`, sans-serif
- Mono: `IBM Plex Mono`, `SFMono-Regular`, monospace

Typography rules:
- Headlines: serif by default for editorial authority.
- UI labels and dense support text: sans.
- Data values: sans, medium or semibold.
- Code or raw metrics: mono only when necessary.

### Type scale
Sizes are fixed by token.

Usage bands:
- Display: cover slides, hero statements, section openers
- Title: route titles, chart lead headings
- Subtitle: subheads and section intros
- Body: paragraphs and explanations
- Caption: figure notes, metadata, footnotes
- Metric: KPI values and scoreboard numbers

### Spacing
Use the spacing scale from `design-tokens.json` only.

Rules:
- Never free-type arbitrary spacing values.
- Prefer outer whitespace before adding decorative separators.
- Tighten only in dense data layouts.

### Shape and elevation
- Radius is subtle, never playful.
- Borders are thin and structural.
- Shadows are minimal and only for layered cards or floating panels.

### Motion
Motion is optional and minimal.

Allowed:
- fade in
- rise
- stagger
- slide between sections

Disallowed:
- bounce
- spinning
- overscaled zoom
- decorative particle effects

## 5. Shared Composition Rules

### Information hierarchy
Every route should expose this order:
1. Main conclusion
2. Support argument or evidence
3. Detail and annotation
4. Method or source notes

### Density
Use one of three density modes only:
- `calm`: reading-first routes
- `standard`: default for document pages and slides
- `dense`: data pages and visual sheets

### Section behavior
- One section, one primary purpose.
- One chart, one key takeaway.
- Long routes should alternate dense and calm rhythm where applicable.

### Print-safe behavior for `web_dual`
- The first screen should still read as a first printed page.
- Section hierarchy, chart captions, and footer/meta content must survive PDF export.
- Avoid sticky-heavy, motion-dependent, or screen-only decorative structures.

## 6. Components

### Core components
- Title block
- Eyebrow
- Summary strip
- Body paragraph
- Quote block
- Fact card
- Divider section
- Footer/meta bar

### Data components
- KPI card
- Chart frame
- Legend
- Insight callout
- Method note
- Table block

### Navigation components
- Table of contents
- Section anchor
- Step rail
- Pagination marker

### Component constraints
Every route implementation must define:
- purpose
- approved surface and document shape
- spacing relationship
- maximum density
- forbidden use cases

## 7. Diagrams and Charts

### When to draw
- Draw only when the visual teaches better than a well-written paragraph.
- If the visual does not reduce ambiguity, do not draw it.
- Diagrams belong inside `long_doc`, `portfolio`, `slides`, `equity_report`, or `research_summary`.

### Auto chart selection
- proportional breakdown -> donut
- time series -> line
- category comparison -> bar
- price history -> candlestick
- value decomposition -> waterfall

### Diagram behavior
- Extract the `<svg>` block from `assets/diagrams/`.
- Embed it as a `<figure>` inside the target document.
- Keep chart titles factual and takeaway-first.
- Keep legends and labels secondary to the main reading path.

## 8. Deck Recipe

Use this section whenever a slide deck exceeds 20 slides.

Long deck rules:
- Start with cover, agenda, and one clear framing slide.
- Group slides into chapters of 4 to 6 slides.
- Use one chapter opener per chapter to reset context.
- Alternate evidence-heavy slides with lighter synthesis slides.
- Do not chain more than 3 dense evidence slides without a recap or transition.
- Reserve appendix slides for supporting detail, not key conclusions.
- If a concept needs a diagram, prefer one clean diagram over multiple half-explained slides.

Recommended long deck rhythm:
1. Cover
2. Agenda
3. Framing
4. Chapter opener
5. Evidence block
6. Synthesis
7. Chapter opener
8. Evidence block
9. Recommendation
10. Appendix

## 9. Surface Rules

### `web_dual`
- Browser-readable and print-safe
- Section-based and document-first
- Motion may decorate entry, but cannot carry meaning

### `slides`
- One slide, one point
- Large readable type
- Minimal annotation per slide
- For decks over 20 slides, follow Section 8

### `visual_sheet`
- Strong directional reading path
- Large numeric emphasis when justified
- Compact explanatory copy

## 10. Non-negotiables

- No new fonts without updating tokens.
- No ad hoc gradients, neon palettes, or random texture overlays.
- No mixing decorative visual languages in one route.
- No chart styling outside approved palette and annotation rules.
- No component outside the selected route whitelist.
- No unsupported `document_type` or route combination.
- No dashboard route in the current system.

## 11. Source of Truth

Use these files as authoritative:
- `README.md`
- `SKILL.md`
- `AGENTS.md`
- `DESIGN.md`
- `PLAYBOOK.md`
- `VOICE.md`
- `design-tokens.json`
- `artifact-presets.json`
- `prompt-contracts.md`
- `style-checklist.md`
- `references/document-types.md`
- `references/diagrams.md`
