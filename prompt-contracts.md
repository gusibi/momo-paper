# Prompt Contracts

## System Contract
Use this system rule for any agent that renders artifacts:

```text
You are generating an artifact inside Momo Paper.
Resolve the request through `document_type + locale` when possible.
If that is not provided, resolve `surface + document_shape`, or map a legacy `artifact_type` alias.
Then use only approved design tokens, section recipes, components, patterns, chart types, and diagram primitives.
Do not invent new fonts, new colors, new layout styles, or new decorative motifs.
Prioritize quiet document-first clarity: conclusion first, evidence second, detail third.
If the route is unsupported or inputs conflict, fail instead of guessing.
Before finalizing, run the style checklist and revise any violating section.
```

## Input Schema
Expected inputs:

```yaml
topic: string
document_type: optional one_pager | long_doc | letter | portfolio | resume | slides | equity_report | changelog | process_flow | timeline | faq_page | case_study | research_summary | stats_report | infographic
locale: optional zh-CN | en
diagram_type: optional architecture | flowchart | quadrant | bar_chart | line_chart | donut_chart | state_machine | timeline_diagram | swimlane | tree | layer_stack | venn | candlestick | waterfall
surface: optional web_dual | slides | visual_sheet
document_shape: optional explainer | editorial_article | letter | portfolio | process_flow | timeline | resume_profile | faq_page | case_study | research_summary | stats_report | equity_report | changelog | infographic
artifact_type: optional legacy alias web_page | ppt_slide | infographic | article | stats_report
audience: internal | external | mixed
goal: string
data_type: none | qualitative | quantitative | mixed
tone_level: restrained | standard | assertive
length_limit: optional string
required_sections: optional array
```

Route resolution priority:
1. `document_type + locale`
2. `surface + document_shape`
3. legacy `artifact_type`

Conflict rule:
- If multiple layers are present, they must resolve to the same route.
- Unsupported combinations fail fast.

Legacy alias map:

```yaml
web_page: web_dual.explainer
ppt_slide: slides.explainer
infographic: visual_sheet.infographic
article: web_dual.editorial_article
stats_report: web_dual.stats_report
```

## Assembly Contract
The agent should follow this sequence:
1. Resolve the route.
2. Choose the correct template from `localeTemplateMap` if `document_type` is used.
3. Read `artifact-presets.json` and lock the matching surface and shape.
4. Read `design-tokens.json` and map color, type, spacing, and motion choices.
5. Apply `VOICE.md` for copy tone.
6. Compose only from approved section recipes, components, patterns, chart types, and diagram primitives.
7. If the deck exceeds 20 slides, read Deck Recipe in `DESIGN.md` section 8.
8. Run `style-checklist.md`.

## Diagram and chart rules

- Diagrams are primitives inside documents, not a document type.
- Read `references/diagrams.md` before selecting or embedding a diagram.
- When structured numerical data is present, auto-select the chart type unless prose is clearly better.

Chart selection guide:
- proportional breakdown -> donut
- time series -> line
- category comparison -> bar
- price history -> candlestick
- value decomposition -> waterfall

## Output Skeleton
When the agent is asked to plan before rendering, use this structured skeleton:

```yaml
document_type:
locale:
diagram_type:
surface:
document_shape:
legacy_artifact_type:
route_used:
template_used:
audience:
goal:
tone:
sections:
  - name:
    purpose:
    components:
    pattern:
    chart_type:
    takeaway:
diagram_candidates: []
token_usage:
  color_roles:
  type_roles:
  density:
checklist_result:
  violations: []
  fixes: []
```

## Public route prompts

### `one_pager`
```text
Create a one-pager using Momo Paper.
Use the `web_dual.explainer` route, keep the page print-safe, and lead with the main conclusion.
```

### `long_doc`
```text
Create a long-form document using Momo Paper.
Use the `web_dual.editorial_article` route, maintain reading comfort, and only add diagrams when they teach better than prose.
```

### `slides`
```text
Create a slide deck using Momo Paper.
Use the `slides.explainer` route, keep one slide to one point, and read Deck Recipe in `DESIGN.md` section 8 if the deck exceeds 20 slides.
```

### `equity_report`
```text
Create an equity report using Momo Paper.
Use the `web_dual.equity_report` route, make the thesis explicit, and include price, valuation, risk, and disclosure context.
```

## Preflight Self-check
The agent must ask itself:
- Did I resolve the correct `document_type` or internal route?
- If a legacy alias was provided, does it agree with the primary route?
- Did I use the correct locale template?
- Did I use only whitelisted components, patterns, chart types, and diagram primitives?
- Did I introduce any color or font outside the tokens?
- Does each section have one primary purpose?
- For `web_dual`, does the structure remain readable without motion and in print/PDF?
- If the content contains numeric data, did I select the appropriate chart or consciously skip it?
- Does the tone match `VOICE.md`?

## Fallback Rules
- Do not choose the nearest route by analogy.
- If the route is not implemented, stop and ask for a supported route.
- `comparison_matrix` and `topic_cover` remain pattern candidates, not valid `document_type` values.
