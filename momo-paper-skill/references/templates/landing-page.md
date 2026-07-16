<!-- Generated from momo_dsl/schemas. Do not edit by hand. -->

# Landing Page

A document-style responsive landing page with a clear claim, supporting sections, and calls to action.

## Selection

- Schema: `landing-page`
- Accepted `document_type`: `landing-page`, `landing`
- Required frontmatter: `document_type`, `locale`, `title`

## Document Contract

- Required blocks: `hero`
- Allowed blocks: `nav`, `hero`, `section`, `feature-grid`, `card-grid`, `stats`, `comparison`, `timeline`, `steps`, `cta`, `faq`, `quote`, `callout`, `footer`
- Ordering rules:
  - `nav` before `hero`
  - `hero` before `footer`

## Block Fields

### `nav`

- `brand` — string, optional
- `items` — array, optional
  - `items[].label` — string, required
  - `items[].href` — string, required
- `cta` — action, optional
  - `cta.label` — string, required
  - `cta.href` — string, required

### `hero`

- `eyebrow` — string, optional
- `title` — string, required
- `subtitle` — string, optional
- `primary_cta` — action, optional
  - `primary_cta.label` — string, required
  - `primary_cta.href` — string, required
- `secondary_cta` — action, optional
  - `secondary_cta.label` — string, required
  - `secondary_cta.href` — string, required

### `section`

- `title` — string, required
- `body` — string, optional
- `points` — array, optional

### `feature-grid`

- `title` — string, optional
- `columns` — integer, optional
- `items` — titled-items, required
  - `items[].title` — string, required
  - `items[].desc` — string, optional
  - `items[].body` — string, optional

### `card-grid`

- `title` — string, optional
- `columns` — integer, optional
- `items` — titled-items, required
  - `items[].title` — string, required
  - `items[].desc` — string, optional
  - `items[].body` — string, optional

### `stats`

- `title` — string, optional
- `items` — array, required
  - `items[].value` — string | integer | number, required
  - `items[].label` — string, required
  - `items[].note` — string, optional

### `comparison`

- `title` — string, optional
- `left` — comparison-side, required
  - `left.title` — string, required
  - `left.items` — array, required
- `right` — comparison-side, required
  - `right.title` — string, required
  - `right.items` — array, required

### `timeline`

- `title` — string, optional
- `items` — step-items, required
  - `items[].step` — string | integer, optional
  - `items[].title` — string, required
  - `items[].desc` — string, optional

### `steps`

- `title` — string, optional
- `items` — step-items, required
  - `items[].step` — string | integer, optional
  - `items[].title` — string, required
  - `items[].desc` — string, optional

### `cta`

- `title` — string, required
- `body` — string, optional
- `button` — action, optional
  - `button.label` — string, required
  - `button.href` — string, required

### `faq`

- `title` — string, optional
- `items` — array, required
  - `items[].question` — string, required
  - `items[].answer` — string, required

### `quote`

- `quote` — string, optional
- `author` — string, optional
- `role` — string, optional

### `callout`

- `tone` — string, optional
- `title` — string, optional
- `body` — string, optional

### `footer`

- `brand` — string, optional
- `body` — string, optional
- `items` — array, optional
  - `items[].label` — string, required
  - `items[].href` — string, required

## Workflow

```bash
"$SKILL_DIR/momo" validate input.md --schema landing-page --json
"$SKILL_DIR/momo" render input.md -o output.html
```

If validation reports errors, repair the DSL and validate again before rendering the final document.
