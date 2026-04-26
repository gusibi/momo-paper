---
name: momo-paper
description: Use this skill whenever the user wants to generate, route, plan, or review a document or visual narrative with Momo Paper. Trigger on requests about one-pagers, long docs, letters, portfolios, resumes, slide decks, equity reports, changelogs, infographics, document templates, route selection, diagram selection, print-safe pages, or how to use the Momo Paper system.
---

# Momo Paper

> A routed design system for documents and visual narratives.

用一套路由规则统一 one-pager、长文、简历、幻灯片、研报、信息图与文档内图示。

Use this skill when the task is about:
- generating a document or visual narrative with Momo Paper
- choosing the correct `document_type`, `surface + document_shape`, or template
- deciding whether a diagram should be embedded inside a long doc, portfolio, deck, equity report, or research summary
- reviewing whether an output follows Momo Paper rules

Do not use this skill for:
- generic app UI design outside this repository's taxonomy
- dashboards; `dashboard` is intentionally out of scope
- freeform branding work that ignores the system constraints

## Resource layout

- `references/`: loadable routing guides and route references
- `assets/templates/`: starter templates for public document types
- `assets/diagrams/`: diagram primitives for embedding
- `assets/showcase/`: visual showcase artifacts

## Reading order

1. Read [README.md](./README.md) for the public usage model.
2. Read [prompt-contracts.md](./prompt-contracts.md) for the formal input schema and route resolution rules.
3. Read [artifact-presets.json](./artifact-presets.json) for the legal routes, mappings, and whitelists.
4. Read [DESIGN.md](./DESIGN.md) for taxonomy, foundations, deck recipe, and non-negotiables.
5. Read [VOICE.md](./VOICE.md) for copy tone.
6. Read [style-checklist.md](./style-checklist.md) before finalizing.

Then read the relevant route reference from `references/routes/` and the matching template from `assets/templates/`.

## Step 1 · Resolve locale

- `zh-CN` -> CN template
- `en` -> EN template

If the user mixes languages, use the dominant reading language of the final output.

## Step 2 · Pick the document type

Use [references/document-types.md](./references/document-types.md) as the authoritative table.

Resolution rules:
1. Prefer `document_type + locale`.
2. If the user provided `surface + document_shape`, use them directly.
3. If the user used legacy `artifact_type`, map it through the alias table.
4. If multiple inputs conflict, fail instead of guessing.

Public document types:
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

Long deck (>20 slides): also read Deck Recipe in [DESIGN.md](./DESIGN.md) section 8.

If unsure, ask a one-liner rather than guess.

## Step 3 · Add diagrams only when they teach better than prose

Diagrams are primitives, not a document type.

Use [references/diagrams.md](./references/diagrams.md) before drawing. It contains:
- the selection guide
- the Momo Paper token map
- the AI-slop anti-pattern table

When a diagram is needed:
- choose the matching template from `assets/diagrams/`
- extract the `<svg>` block
- embed it inside a `<figure>` in the target document

Before drawing, ask: would a well-written paragraph teach the reader less than this diagram? If no, do not draw.

## Auto-select charts from data

When the content contains structured numerical data, choose the chart type automatically:

- proportional breakdown -> donut
- time series -> line
- category comparison -> bar
- price history -> candlestick
- value decomposition -> waterfall

Do not wait for the user to explicitly request a chart. If prose teaches better than the chart, skip the chart.

## Output rules

- Follow the exact `sectionRecipe` for the selected internal route.
- Use only the route's allowed components, patterns, and charts.
- Preserve the quiet, credible, document-first tone. Do not drift into marketing language.
- For `web_dual`, keep the output readable both in browser and as print/PDF.
- Use motion only decoratively. The structure must still work without animation.

## Refusal conditions

Push back or ask for clarification if:
- the requested route is not present in `artifact-presets.json`
- the user wants a separate dashboard system
- the user wants `comparison_matrix` or `topic_cover` promoted into a document type
- the user wants a visual style that breaks the token or voice constraints

## Planning skeleton

```yaml
document_type:
locale:
surface:
document_shape:
route_used:
template_used:
goal:
audience:
sections:
  - name:
    purpose:
    components:
    pattern:
    chart_type:
    takeaway:
diagram_candidates: []
checklist_risks: []
```
