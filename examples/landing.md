---
document_type: landing
locale: zh-CN
title: AI Agent Sandbox Platform
description: Policy-based runtime for safer AI agents.
---

:::hero
eyebrow: Agent Runtime
title: Run AI agents safely with policy-based control
subtitle: Give agents tools, files and browser access without losing control.
primary_cta:
  label: Start Free
  href: /signup
secondary_cta:
  label: View Docs
  href: /docs
:::

## Why DSL

AI should generate **structure**, not fragile HTML. Momo Paper parses the generated DSL and turns it into stable standalone HTML.

:::section
title: What the runtime does
body: The runtime parses frontmatter, Markdown, and structured blocks. It does not define business components in Python.
points:
  - Validate Agent-generated DSL.
  - Convert valid blocks into generic HTML sections.
  - Preserve tag names for downstream tools.
:::

:::feature-grid
columns: 3
items:
  - title: Policy-first permissions
    desc: Define which tools can run automatically and which need approval.
  - title: Isolated runtime
    desc: Run operations inside controlled environments.
  - title: Stable rendering
    desc: Keep HTML output predictable.
:::

:::timeline
title: How it works
items:
  - step: 1
    title: Write DSL
    desc: Agent creates Markdown with structured blocks.
  - step: 2
    title: Validate
    desc: Momo Paper reports syntax and metadata errors.
  - step: 3
    title: Render HTML
    desc: The same DSL becomes standalone HTML.
:::

:::comparison
title: Before vs After
left:
  title: Direct HTML
  items:
    - Hard to validate
    - Easy to drift
right:
  title: Markdown DSL
  items:
    - Easy to parse
    - Stable output
:::

:::stats
items:
  - value: 1
    label: Source Markdown DSL file
  - value: 100%
    label: HTML generated from parsed structure
:::

:::cta
title: Generate the page
button:
  label: Render HTML
  href: /render
:::

:::faq
items:
  - question: Does the runtime define components?
    answer: No. It parses user-defined tags and renders generic HTML.
  - question: Can Agents use recommended tags?
    answer: Yes. The tags are documented conventions for consistent generation.
:::
