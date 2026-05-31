# Momo Paper 2.0 DSL

Momo Paper 2.0 converts Agent-generated Markdown DSL into standalone HTML.

The runtime is a parser and converter. It does not define business components in Python. Tags such as `hero`, `feature-grid`, and `cta` are Agent-facing writing conventions. The parser accepts any valid `:::tag-name` block, validates syntax and metadata, and renders it as HTML with `data-block="tag-name"`.

## Quick Start

```bash
cd v2
PYTHONPATH=. python -m momo_dsl.cli validate examples/landing.md
PYTHONPATH=. python -m momo_dsl.cli render examples/landing.md -o dist/landing.html
```

`render` writes a single standalone HTML file with CSS inlined into `<style>`. To use a different visual system, pass a CSS file to inline:

```bash
PYTHONPATH=. python -m momo_dsl.cli render examples/landing.md -o dist/landing.html --css themes/report.css
```

After package installation:

```bash
momo2 validate examples/landing.md
momo2 render examples/landing.md -o dist/landing.html
```

## Minimal Document

```md
---
document_type: landing
locale: en
title: AI Agent Sandbox Platform
description: Policy-based runtime for safer AI agents.
---

## Why DSL

AI should generate **structure**, not fragile HTML.

:::hero
eyebrow: Agent Runtime
title: Run AI agents safely
subtitle: Give agents tools without losing control.
primary_cta:
  label: Start Free
  href: /signup
:::
```

## Required Frontmatter

Every document must start with frontmatter:

```md
---
document_type: landing
locale: zh-CN
title: Page title
---
```

Required fields:

- `document_type`
- `locale`
- `title`

Optional common fields:

- `description`
- `author`
- `date`

`document_type: dashboard` is invalid.

## Block Syntax

Use fenced DSL blocks for structured content:

```md
:::tag-name
key: value
nested:
  key: value
items:
  - title: First item
    desc: Description
:::
```

Tag names must:

- start with a lowercase letter
- use only lowercase letters, numbers, and hyphens
- match `^[a-z][a-z0-9-]*$`

## Recommended Agent Tags

These tags are recommended for landing-style documents. They are conventions, not Python component classes.

| Tag | Use |
| --- | --- |
| `hero` | Opening claim, subtitle, and calls to action |
| `section` | Generic content section |
| `feature-grid` | Feature or capability list |
| `timeline` | Steps, process, roadmap, or milestones |
| `comparison` | Before/after or left/right contrast |
| `stats` | Metrics and short quantified claims |
| `cta` | Action section |
| `faq` | Question and answer list |

The parser also accepts other valid tags, for example `:::custom-block`.

## Supported Markdown

The Markdown subset outside DSL blocks supports:

- `#`, `##`, `###` headings
- paragraphs
- unordered lists using `-`
- ordered lists using `1.`
- links: `[label](https://example.com)`
- bold: `**text**`
- italic: `*text*`
- inline code: `` `code` ``

See [REFERENCE.md](REFERENCE.md) for the complete syntax reference, Agent guidance, examples, and validation rules.
