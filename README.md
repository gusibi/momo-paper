# Momo Paper

Momo Paper is a document renderer for AI Agents. Agents write compact Markdown DSL; Momo Paper validates the structure and renders consistent, print-ready standalone HTML or PDF.

The runtime is a parser and converter. It does not define business components in Python. Tags such as `hero`, `feature-grid`, and `cta` are Agent-facing writing conventions. The parser accepts any valid `:::tag-name` block, validates syntax and metadata, and renders it as HTML with `data-block="tag-name"`.

## Quick Start

Python 3.10+ is required. Clone the repository and generate the formal research-summary example:

```bash
git clone https://github.com/gusibi/momo-paper.git
cd momo-paper
python3 -m venv .venv
source .venv/bin/activate
pip install -e .

momo schema list
momo validate examples/research-summary.md --schema research-summary --json
momo render examples/research-summary.md --schema research-summary -o dist/research-summary.html
open dist/research-summary.html  # macOS; use your browser on Linux/Windows
```

`render` writes a standalone HTML file with CSS inlined into `<style>`. No server or account is required.

### Use the self-contained Skill runtime

The bundled Skill includes its own runtime and only needs Python 3.10+. This path does not install a global command:

```bash
./momo-paper-skill/momo validate examples/research-summary.md --schema research-summary --json
./momo-paper-skill/momo render examples/research-summary.md --schema research-summary -o dist/research-summary.html
```

Copy `momo-paper-skill/` into your Agent's skills directory when you want automatic skill discovery. The same package can also be called from any Agent tool layer through its `momo` wrapper.

### Use a custom visual theme

```bash
momo render examples/research-summary.md --schema research-summary -o dist/research-summary.html --css path/to/theme.css
```

`momo2` remains available as a compatibility alias for existing integrations.

See the [rendered equity-report example](https://momo.eztoolab.com/demo/equity-report/) before installing, or read the [Agent usage guide](https://momo.eztoolab.com/guide/).

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

## Product Site

The product website (https://momo.eztoolab.com) is built from this DSL — it both introduces Momo Paper and dogfoods the engine. Each page is a Markdown DSL file under `site/content/`, rendered by `site/build.py` with shared navigation, SEO metadata, and a Momo Paper / Vercel theme switcher. See [site/README.md](site/README.md) for how it works and how to build it locally.
