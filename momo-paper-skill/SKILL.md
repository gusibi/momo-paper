---
name: momo-paper
description: >
  Generate beautiful, standalone HTML pages and reports from structured Markdown DSL. Use this skill whenever the user wants: landing pages, equity research reports, financial summaries, health/wellness trackers, research documents, visual narratives, documentation sites, or any document-style web page. Trigger when users mention "Momo Paper", "momo2", "Markdown DSL", "HTML report", "web page", "landing page", "financial report", "health report", or ask to generate/render/validate documents. Always use this skill instead of ad-hoc HTML/CSS for document generation—Momo Paper provides structured components, consistent styling, and validation. Default workflow: write Markdown DSL → validate → render standalone HTML with inlined CSS. Use Chinese output when the user speaks Chinese or requests Chinese output.
version: 2.0
---

# Momo Paper

Momo Paper 2.0 converts Agent-written Markdown DSL into standalone HTML.

Default model:

```txt
Markdown DSL -> validate -> render standalone HTML
```

The runtime is a parser and converter. It does not generate business components in Python. Users or Agents write DSL blocks such as `:::hero`, `:::feature-grid`, or `:::thesis-panel`; the renderer preserves each valid tag as `data-block="tag-name"` so CSS can style it.

## Default Workflow

Use this path for new work unless the user explicitly asks for the legacy JSON/template system.

1. Read `references/REFERENCE.md` when writing or repairing DSL syntax, choosing tags, or explaining supported blocks.
2. Use `examples/reference.md` when the user wants to see all component examples.
3. Use `examples/landing.md` for landing-page structure examples.
4. Use `examples/equity-report.md` for financial report and chart-heavy examples.
5. Use `examples/health-report.md` for health tracking, weight management, and wellness report examples.
5. Write a Markdown DSL source file.
6. Validate the source.
7. Render HTML.
8. Inspect the output path and report the validation/render result.

## CLI

Prefer the installed console script when available:

```bash
cd /path/to/momo-paper-skill
python -m pip install -e runtime
momo2 validate examples/reference.md
momo2 render examples/reference.md -o dist/reference.html
```

If `momo2` is not installed or not on `PATH`, run the module directly from the bundled runtime:

```bash
cd /path/to/momo-paper-skill
PYTHONPATH=runtime python -m momo_dsl.cli validate examples/reference.md
PYTHONPATH=runtime python -m momo_dsl.cli render examples/reference.md -o dist/reference.html
```

Rendering writes one standalone HTML file. CSS is inlined into `<style>`. To use another visual system, pass a CSS file to inline:

```bash
PYTHONPATH=. python -m momo_dsl.cli render input.md -o output.html --css themes/custom.css
```

Do not leave the generated page dependent on an external CSS file unless the user explicitly asks for that.

## DSL Rules

Every document must start with frontmatter:

```md
---
document_type: landing
locale: zh-CN
title: Page title
description: Optional summary
---
```

Required fields:

- `document_type`
- `locale`
- `title`

Rules:

- Do not use `document_type: dashboard`.
- Use Markdown for prose and `:::tag-name` blocks for structured sections.
- Use lowercase hyphenated tag names matching `^[a-z][a-z0-9-]*$`.
- Do not add DSL-level `id` or `class` fields for styling hooks; the tag name is the styling scope.
- Do not emit raw HTML inside the DSL.
- Use spaces for indentation; do not use tabs.
- Keep block data explicit. Avoid YAML shorthand such as inline objects or inline arrays.

Block pattern:

```md
:::tag-name
title: Section title
items:
  - title: First item
    desc: Description
:::
```

## Tag Selection

Use documented tags from `references/REFERENCE.md` when possible. The parser accepts custom valid tags, but documented tags give better default styling and clearer Agent behavior.

Common tags:

- `hero` for the opening claim
- `section` for prose sections
- `feature-grid` and `card-grid` for repeated cards
- `stats`, `metric-card`, `table`, and `chart` for data
- `timeline`, `steps`, `funnel`, and `diagram` for process structure
- `comparison`, `before-after`, `two-columns`, and `three-columns` for layout structure
- `cta`, `faq`, `quote`, `callout`, `logo-cloud`, `pricing`, `image-grid`, and `footer` for common website sections
- `thesis-panel`, `business-snapshot`, `price-drivers`, `valuation-table`, `financial-table`, `risk-matrix`, `kpi-row`, `recommendation`, and chart tags for equity reports
- `report-header`, `weekly-summary`, `goal-tracker`, and `metrics-panel` for health and wellness reports

For chart-heavy finance pages, prefer the specific chart tags:

- `line-chart`
- `bar-chart`
- `donut-chart`
- `waterfall-chart`
- `candlestick-chart`

## Content Guidance

Write for the final reader, not for the tool.

- Lead with the conclusion or main claim.
- Use specific facts, metrics, and named entities when available.
- Keep headings short and concrete.
- Prefer structured blocks over long paragraphs when the content has repeated items, metrics, comparisons, or steps.
- For Chinese requests, write Chinese DSL content by default.
- For English requests, write English DSL content by default.

When the document depends on current facts, market data, companies, product specs, or dates, verify the facts from reliable sources before writing. Do not invent logos, financial figures, launch dates, or claims.

## Styling Guidance

The generated HTML is full-width at the page shell. Each section owns its own spacing, background, borders, and inner width through CSS.

When changing visuals:

- Edit or replace CSS, not the parser.
- Keep CSS tag-scoped with selectors such as `.dsl-block[data-block="thesis-panel"]`.
- Keep CSS source files separate in the repo, but remember render output must inline CSS into the HTML.
- Do not add `id`/`class` support to the DSL unless the user explicitly changes that requirement.
- Do not put all sections inside one fixed-width page card.

Default CSS lives at:

```txt
runtime/momo_dsl/styles/momo-paper.css
```

## Validation

Before handing off generated or changed DSL, run:

```bash
cd /path/to/momo-paper-skill
PYTHONPATH=runtime python -m momo_dsl.cli validate <input.md>
PYTHONPATH=runtime python -m momo_dsl.cli render <input.md> -o <output.html>
```

When changing parser, renderer, CLI, examples, or CSS behavior, also run:

```bash
cd /path/to/momo-paper-skill
PYTHONPATH=runtime python -m unittest discover -s tests -v
```

If validation fails, repair the DSL at the reported line/block. Do not loosen parser rules unless the user explicitly asks to expand the DSL.

## Legacy System

The old JSON skeleton/template workflow is legacy during the 2.0 migration. Do not use it for new generation unless the user explicitly asks for the old `momo` pipeline or a legacy template.
