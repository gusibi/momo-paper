<!-- Generated from momo_dsl/schemas. Do not edit by hand. -->

# Deep Research Report

An evidence-heavy research report with an executive summary, findings, methodology, limitations, counterarguments, recommendations, and traceable sources.

## Selection

- Schema: `deep-research`
- Accepted `document_type`: `deep-research`
- Required frontmatter: `document_type`, `locale`, `title`

## Document Contract

- Required blocks: `research-header`, `executive-summary`, `key-findings`, `methodology`, `sources`
- Allowed blocks: `research-header`, `research-question`, `executive-summary`, `key-findings`, `evidence`, `counterarguments`, `methodology`, `limitations`, `recommendations`, `sources`, `callout`
- Ordering rules:
  - `research-header` before `executive-summary`
  - `executive-summary` before `key-findings`
  - `key-findings` before `evidence`
  - `key-findings` before `methodology`
  - `methodology` before `limitations`
  - `recommendations` before `sources`
  - `limitations` before `sources`

## Block Fields

### `research-header`

- `topic` — string, required
- `scope` — string, optional
- `period` — string, optional
- `status` — string, optional

### `research-question`

- `question` — string, required
- `scope` — string, optional

### `executive-summary`

- `title` — string, optional
- `summary` — string, required
- `citations` — array, optional

### `key-findings`

- `title` — string, optional
- `items` — finding-items, required
  - `items[].title` — string, required
  - `items[].body` — string, required
  - `items[].confidence` — string, optional
  - `items[].citations` — array, optional

### `evidence`

- `title` — string, optional
- `items` — array, required
  - `items[].claim` — string, required
  - `items[].body` — string, required
  - `items[].citations` — array, optional

### `counterarguments`

- `title` — string, optional
- `items` — titled-items, required
  - `items[].title` — string, required
  - `items[].body` — string, optional
  - `items[].desc` — string, optional

### `methodology`

- `title` — string, optional
- `summary` — string, required
- `methods` — array, required
- `sample` — string, optional

### `limitations`

- `title` — string, optional
- `items` — array, required

### `recommendations`

- `title` — string, optional
- `items` — titled-items, required
  - `items[].title` — string, required
  - `items[].body` — string, optional
  - `items[].desc` — string, optional

### `sources`

- `title` — string, optional
- `items` — array, required
  - `items[].id` — string, required
  - `items[].title` — string, required
  - `items[].url` — string, required
  - `items[].publisher` — string, optional
  - `items[].published_at` — string, optional
  - `items[].accessed_at` — string, optional

### `callout`

- `tone` — string, optional
- `title` — string, optional
- `body` — string, optional

## Citations

Declare sources in `:::sources` with a unique `id`. Fields that allow `citations` must list those IDs. `momo validate --json` reports duplicate IDs and unresolved references.

## Workflow

```bash
"$SKILL_DIR/momo" validate input.md --schema deep-research --json
"$SKILL_DIR/momo" render input.md -o output.html
```

If validation reports errors, repair the DSL and validate again before rendering the final document.
