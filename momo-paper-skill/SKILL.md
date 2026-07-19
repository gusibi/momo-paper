---
name: momo-paper
description: >
  Use when generating, rendering, validating, or revising a document-style web page or report with Momo Paper Markdown DSL, including landing pages, research summaries, financial reports, health trackers, visual narratives, and documentation sites.
argument-hint: "[output_path] — optional file path for the generated HTML"
version: 2.1
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

1. For a task that matches a formal template, read `references/templates/INDEX.md`, then read only the selected template reference.
2. Use `"$SKILL_DIR/momo" schema list` or `schema describe <name> --json` when you need machine-readable template details.
3. Use `references/REFERENCE.md` for open DSL syntax, experimental tags, or repair guidance not covered by a formal template.
4. Use `examples/reference.md` when the user wants to see all component examples.
5. Use `examples/landing-page.md`, `examples/research-summary.md`, or `examples/deep-research.md` for the three formal flagship templates.
6. Existing finance, health, slides, and other examples remain experimental open-mode documents unless a formal schema reference exists.
7. Write a Markdown DSL source file. Do not add a schema or DSL version field; select the formal contract with the CLI `--schema` argument.
8. Run `validate <input.md> --schema <name> --json`. For every `errors[]` item, repair the source using `code`, `path`, `line`, `block`, and `field`; repeat until `ok` is `true`.
9. Run `render <input.md> --schema <name> -o <output.html>` only after the formal validation passes. See [Output Path](#output-path).
10. For an intentionally experimental document, omit `--schema`; free mode preserves valid unknown blocks and fields, but its warnings are not a formal contract.
11. Return only the output file path. Do NOT return the HTML content as a string.

### Output Path

The rendered HTML must always be written to a file. The calling Agent receives only the file path, not the HTML content.

- If the user provides an output path (via `output_path` argument or explicitly in the conversation), use that path directly.
- If no output path is specified, default to `dist/output.html` under the skill directory.
- The caller Agent decides what to do with the file (read, upload, preview, etc.) — this skill does not handle those operations.

Example with user-specified path:

```bash
"$SKILL_DIR/momo" render input.md --schema <name> -o /Users/me/reports/my-report.html
```

Example with default path:

```bash
"$SKILL_DIR/momo" render input.md --schema <name> -o dist/output.html
```

## CLI

This skill bundles a complete, zero-dependency `runtime/` copy of the engine, so
**no installation is needed** (no `pip install`). The bundled `momo` wrapper script
sits next to this SKILL.md and self-locates its own `runtime/` via `BASH_SOURCE`, so
it works no matter where this skill is installed.

Find this skill's directory (`SKILL_DIR` — the folder that contains this SKILL.md;
you already know its absolute path from loading this skill), then call the wrapper.
Do NOT hardcode any user-specific or machine-specific path.

```bash
# Replace <name> with the selected formal Schema, for example landing-page.
"$SKILL_DIR/momo" validate input.md --schema <name> --json
"$SKILL_DIR/momo" render  input.md --schema <name> -o output.html
```

Additional commands:

- `schema list` — list formal template contracts available to the Skill.
- `schema describe <name>` — print one machine schema; add `--json` for raw data.
- `validate input.md --json` — infer a formal schema when possible and emit all semantic errors and warnings. Add `--schema <name>` to select a contract explicitly.
- `bench input.md` — compare DSL token cost vs rendered HTML; add `--json` for machine output.
- `render input.md --schema <name> -o out.html` — validate and render a formal document. It refuses semantic errors before writing output.
- `render input.md -o out.html` — render an intentionally experimental/free document.
- `render input.md -o out.pdf --format pdf` — print to PDF. Requires the optional `playwright` dependency (`pip install playwright && playwright install chromium`).

`validate` is strict for a uniquely selected formal template. Experimental or ambiguous documents use free mode with warnings. For a formal deliverable, always pass the selected schema explicitly to both `validate` and `render`; `render --schema` refuses semantic errors. Without `--schema`, render remains permissive and preserves syntactically valid unknown blocks and fields for intentional experimental documents.

`input.md` / `output.html` may be relative to your current directory or absolute —
the wrapper does not change the working directory, so you can run it from anywhere.

The wrapper handles the Python interpreter and `PYTHONPATH` for you. If you cannot use
the wrapper, the equivalent direct call is (note `runtime` must be resolved against
`SKILL_DIR`, not your current directory):

```bash
PYTHONPATH="$SKILL_DIR/runtime" python3 -m momo_dsl.cli validate input.md --schema <name> --json
PYTHONPATH="$SKILL_DIR/runtime" python3 -m momo_dsl.cli render  input.md --schema <name> -o output.html
```

> Requires Python >= 3.10 (the runtime uses `str | None` syntax). The wrapper checks
> this and fails with a clear message. On macOS, `/usr/bin/python3` is often 3.9 and
> would otherwise fail with a cryptic `TypeError: unsupported operand type(s) for |`.
> (Optional, for interactive use only: `pip install -e "$SKILL_DIR/runtime"` gives a
> global `momo` command; not needed for the wrapper above.)

Rendering writes one standalone HTML file. CSS is inlined into `<style>`. To use another visual system, pass a CSS file to inline:

```bash
"$SKILL_DIR/momo" render input.md --schema <name> -o output.html --css "$SKILL_DIR/themes/custom.css"
```

Do not leave the generated page dependent on an external CSS file unless the user explicitly asks for that.

## DSL Rules

Every document must start with frontmatter:

```md
---
document_type: landing-page
locale: zh-CN
title: Page title
description: Optional summary
---
```

For a formal document, use the selected reference's accepted `document_type` and pass its Schema name to both validation and rendering. Experimental documents may use an unregistered type and intentionally run in free mode.

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

Before handing off generated or changed DSL, run (`$SKILL_DIR` = this skill's directory, see the CLI section above):

```bash
# Formal document: use the same selected Schema for both commands.
"$SKILL_DIR/momo" validate <input.md> --schema <name> --json
"$SKILL_DIR/momo" render <input.md> --schema <name> -o <output.html>
```

Read every `errors[]` item from the JSON response and repair `code`, `path`, `line`, `block`, and `field` before retrying. Do not render a formal deliverable until `ok` is `true`.

For an intentionally experimental document, omit `--schema`; review free-mode warnings before rendering.
suite (this one needs the skill dir as CWD because tests use relative paths):

```bash
cd "$SKILL_DIR"
PYTHONPATH=runtime python3 -m unittest discover -s tests -v
```

If validation fails, repair the DSL at the reported line/block. Do not loosen parser rules unless the user explicitly asks to expand the DSL.

## Legacy System

The old JSON skeleton/template workflow is legacy during the 2.0 migration. Do not use it for new generation unless the user explicitly asks for the old `momo` pipeline or a legacy template.
