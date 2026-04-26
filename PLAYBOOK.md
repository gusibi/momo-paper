# Momo Paper Playbook

## 1. Workflow
For any request, follow this sequence:
1. Resolve `document_type + locale` if available.
2. Otherwise resolve `surface + document_shape`, or map a legacy `artifact_type` alias.
3. Load the matching route from `artifact-presets.json`.
4. Pull allowed tokens from `design-tokens.json`.
5. Compose only approved section recipes, components, patterns, chart types, and diagram primitives.
6. Apply voice rules from `VOICE.md`.
7. Run `style-checklist.md` before final output.

## 2. Input contract
Preferred public inputs:
- `topic`
- `document_type`
- `locale`
- `audience`
- `goal`

Optional:
- `diagram_type`
- `data_type`
- `source_credibility`
- `tone_level`
- `length_limit`
- `required_sections`

Advanced/internal inputs:
- `surface`
- `document_shape`
- legacy `artifact_type`

Resolution rules:
- `document_type + locale` is the primary public interface.
- `surface + document_shape` is the internal route interface.
- `artifact_type` is compatibility only.
- If multiple layers are present, they must resolve to the same route.
- Unsupported combinations fail fast. Do not guess.

## 3. Document type overlay

### Core document types
- `one_pager` -> `web_dual.explainer`
- `long_doc` -> `web_dual.editorial_article`
- `letter` -> `web_dual.letter`
- `portfolio` -> `web_dual.portfolio`
- `resume` -> `web_dual.resume_profile`
- `slides` -> `slides.explainer`
- `equity_report` -> `web_dual.equity_report`
- `changelog` -> `web_dual.changelog`

### Existing routed extensions
- `process_flow` -> `web_dual.process_flow`
- `timeline` -> `web_dual.timeline`
- `faq_page` -> `web_dual.faq_page`
- `case_study` -> `web_dual.case_study`
- `research_summary` -> `web_dual.research_summary`
- `stats_report` -> `web_dual.stats_report`
- `infographic` -> `visual_sheet.infographic`

If unsure, ask a one-liner rather than guess.

## 4. Diagrams and charts

Diagrams are primitives inside documents, not standalone document types.

Use `assets/diagrams/` only when the visual teaches better than prose. Read `references/diagrams.md` first.

Automatic chart selection:
- proportional breakdown -> donut
- time series -> line
- category comparison -> bar
- price history -> candlestick
- value decomposition -> waterfall

Do not wait for the user to explicitly request a chart when structured numeric data clearly benefits from one.

## 5. Special route notes

### `web_dual`
- browser-readable and print-safe
- first screen should still work as the first printed page
- avoid card-wall sprawl and motion-dependent structure

### `slides`
- one slide = one point
- for decks over 20 slides, read Deck Recipe in `DESIGN.md` section 8

### `visual_sheet`
- one sheet = one dominant reading path
- compress prose harder than on page or slide routes

## 6. Escalation rules

Escalate or ask for confirmation only if:
- the requested route or document type is not implemented
- the user gives conflicting route inputs
- the requested visual language conflicts with print-safe document rules
- the user wants a separate dashboard system

Otherwise, resolve the route and proceed.
