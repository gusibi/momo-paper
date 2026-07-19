<!-- Generated from momo_dsl/schemas. Do not edit by hand. -->

# Research Summary

A concise research deliverable organized around a question, findings, implications, method, limitations, and traceable sources.

## Selection

- Schema: `research-summary`
- Accepted `document_type`: `research-summary`
- Required frontmatter: `document_type`, `locale`, `title`

## Document Contract

- Required blocks: `research-question`, `key-findings`
- Allowed blocks: `research-question`, `key-findings`, `implications`, `methodology`, `limitations`, `sources`, `callout`
- Ordering rules:
  - `research-question` before `key-findings`
  - `key-findings` before `implications`
  - `key-findings` before `methodology`
  - `key-findings` before `sources`
  - `limitations` before `sources`

## Block Fields

### `research-question`

- `question` — string, required
- `scope` — string, optional

### `key-findings`

- `title` — string, optional
- `items` — finding-items, required
  - `items[].title` — string, required
  - `items[].body` — string, required
  - `items[].citations` — array, optional

### `implications`

- `title` — string, optional
- `items` — titled-items, required
  - `items[].title` — string, required
  - `items[].body` — string, optional
  - `items[].desc` — string, optional

### `methodology`

- `title` — string, optional
- `summary` — string, required
- `methods` — array, optional
- `sample` — string, optional

### `limitations`

- `title` — string, optional
- `items` — array, required

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
"$SKILL_DIR/momo" validate input.md --schema research-summary --json
"$SKILL_DIR/momo" render input.md --schema research-summary -o output.html
```

If validation reports errors, repair the DSL and validate again before rendering the final document.
