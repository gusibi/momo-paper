# Momo Paper DSL Reference

This document defines the Phase 1 Momo Paper 2.0 Markdown DSL.

Audience:

- Humans writing DSL by hand
- Agents generating DSL
- Tests verifying parser behavior

The goal is predictable conversion:

```txt
Markdown DSL -> parse -> validate -> standalone HTML
```

The runtime does not generate DSL and does not define business components. Users or Agents write the document. Momo Paper validates and converts it.

## 1. Document Structure

Every document has two parts:

```md
---
document_type: landing
locale: en
title: Page title
description: Optional description
---

Markdown content and :::tag-name blocks go here.
```

Rules:

- Frontmatter must be the first thing in the file.
- The first line must be `---`.
- The closing frontmatter line must be `---`.
- Body content starts after the closing `---`.
- Blank lines are allowed between body nodes.

Invalid:

```md
# Title before frontmatter

---
document_type: landing
locale: en
title: Page
---
```

## 2. Frontmatter

Frontmatter uses the same key/value data subset as block bodies.

Required fields:

| Field | Type | Rule |
| --- | --- | --- |
| `document_type` | string | Required. `dashboard` is invalid. |
| `locale` | string | Required. Recommended values: `zh-CN`, `en`. |
| `title` | string | Required. Used as the HTML `<title>` and page heading. |

Optional common fields:

| Field | Type | Rule |
| --- | --- | --- |
| `description` | string | Used as page intro text when present. |
| `author` | string | Parsed and available for future renderers. |
| `date` | string | Parsed and available for future renderers. |

Example:

```md
---
document_type: landing
locale: zh-CN
title: AI Agent Sandbox Platform
description: Policy-based runtime for safer AI agents.
author: Momo Paper
date: 2026-05-31
---
```

## 3. Markdown Body

Markdown body is for ordinary reading content. It is intentionally small and predictable.

### Headings

```md
# Page heading
## Section heading
### Subsection heading
```

Supported levels: `#`, `##`, `###`.

### Paragraphs

```md
This is a paragraph.

This is another paragraph.
```

Lines in the same paragraph are joined with a single space.

### Lists

Unordered:

```md
- First item
- Second item
```

Ordered:

```md
1. First step
2. Second step
```

Nested Markdown lists are not part of Phase 1. Use a DSL block for nested structures.

### Inline Formatting

```md
Use **bold**, *italic*, `inline code`, and [links](https://example.com).
```

Supported:

| Syntax | Output |
| --- | --- |
| `**text**` | bold |
| `*text*` | italic |
| `` `code` `` | inline code |
| `[label](href)` | link |

Not supported in Phase 1:

- fenced code blocks
- tables in Markdown body
- images
- blockquotes
- raw HTML
- nested Markdown lists

Use DSL blocks for structured content instead.

## 4. DSL Blocks

DSL blocks describe structured content.

```md
:::tag-name
key: value
items:
  - title: Item title
    desc: Item description
:::
```

Opening rule:

```txt
:::tag-name
```

Closing rule:

```txt
:::
```

Tag name rules:

- must start with a lowercase letter
- may contain lowercase letters, numbers, and hyphens
- must match `^[a-z][a-z0-9-]*$`

Valid:

```txt
hero
feature-grid
custom-block
section2
```

Invalid:

```txt
Hero
feature_grid
2columns
feature grid
```

## 5. Block Data Format

Block bodies use a small YAML-like subset.

### Scalar Fields

```md
:::section
title: Why DSL
body: Generate structure, not fragile HTML.
featured: true
count: 3
:::
```

Supported scalar values:

- strings
- integers
- floats
- booleans: `true`, `false`
- null: `null`, `~`

Strings do not need quotes unless the value should preserve leading/trailing spaces.

Quoted strings:

```md
title: "A quoted title"
label: 'A quoted label'
```

### Nested Objects

```md
:::cta
title: Generate the page
button:
  label: Render HTML
  href: /render
:::
```

Use spaces for indentation. The examples use two spaces. Tabs are invalid.

### Lists Of Objects

```md
:::feature-grid
items:
  - title: Stable rendering
    desc: Convert structured content into repeatable HTML.
  - title: Fast validation
    desc: Tell the Agent where the document is wrong.
:::
```

### Lists Of Scalars

```md
:::comparison
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
```

### Empty Blocks

Empty blocks are valid but discouraged:

```md
:::section
:::
```

Agents should avoid empty blocks unless the downstream renderer explicitly expects them.

### Unsupported Data Syntax

Not supported in Phase 1:

- multiline strings using `|` or `>`
- anchors and aliases
- inline objects like `{ label: Start }`
- inline arrays like `[one, two]`
- comments inside values

Write expanded key/value structures instead.

## 6. Recommended Agent Tags

These tags are conventions for Agent output. They help documents stay consistent across Telegram, high-scale generation, and other input channels.

The runtime does not require these tags. Any valid tag name can be parsed and rendered generically.

### `hero`

Use for the opening section.

```md
:::hero
eyebrow: Agent Runtime
title: Run AI agents safely
subtitle: Give agents tools without losing control.
primary_cta:
  label: Start Free
  href: /signup
secondary_cta:
  label: View Docs
  href: /docs
:::
```

Recommended fields:

- `eyebrow`
- `title`
- `subtitle`
- `primary_cta`
- `secondary_cta`

### `section`

Use for a generic content block.

```md
:::section
title: Why this exists
body: Momo Paper converts Agent-generated DSL into stable HTML.
points:
  - AI writes structured content.
  - The parser validates the structure.
  - The renderer outputs standalone HTML.
:::
```

Recommended fields:

- `title`
- `body`
- `points`

### `feature-grid`

Use for capabilities, benefits, or feature lists.

```md
:::feature-grid
columns: 3
items:
  - title: Predictable syntax
    desc: Agents write the same block structure every time.
  - title: Generic rendering
    desc: The runtime renders any valid tag.
  - title: Clear errors
    desc: Invalid DSL points back to line and block.
:::
```

Recommended fields:

- `columns`
- `items`
- `items[].title`
- `items[].desc`

### `timeline`

Use for processes, steps, roadmaps, or milestones.

```md
:::timeline
title: Generation flow
items:
  - step: 1
    title: Agent writes DSL
    desc: The Agent uses documented tags.
  - step: 2
    title: Momo validates
    desc: The parser checks syntax and frontmatter.
  - step: 3
    title: HTML is generated
    desc: The renderer outputs a standalone file.
:::
```

Recommended fields:

- `title`
- `items`
- `items[].step`
- `items[].title`
- `items[].desc`

### `comparison`

Use for before/after, left/right, or old/new framing.

```md
:::comparison
title: Before vs After
left:
  title: Direct HTML
  items:
    - Hard to validate
    - Visual output drifts
right:
  title: Markdown DSL
  items:
    - Easy to parse
    - Output is repeatable
:::
```

Recommended fields:

- `title`
- `left.title`
- `left.items`
- `right.title`
- `right.items`

### `stats`

Use for numeric claims or summary metrics.

```md
:::stats
items:
  - value: 1
    label: Source Markdown file
  - value: 8
    label: Recommended Agent tags
  - value: 100%
    label: HTML generated from DSL
:::
```

Recommended fields:

- `items`
- `items[].value`
- `items[].label`

### `cta`

Use for an action section.

```md
:::cta
title: Generate the page
body: Validate the DSL first, then render HTML.
button:
  label: Render HTML
  href: /render
:::
```

Recommended fields:

- `title`
- `body`
- `button.label`
- `button.href`

### `faq`

Use for question and answer lists.

```md
:::faq
items:
  - question: Does the runtime define components?
    answer: No. It parses tags written by the user or Agent.
  - question: Can I use a custom tag?
    answer: Yes, if the tag name follows the DSL rules.
:::
```

Recommended fields:

- `items`
- `items[].question`
- `items[].answer`

## 7. Financial Report Tags

These tags are conventions for equity reports, finance memos, and data-heavy research documents. They are still plain DSL tags: the parser treats them the same way as any other `:::tag-name` block.

### `thesis-panel`

Use for the main investment conclusion.

```md
:::thesis-panel
title: 投资结论
rating: 买入
target_price: HK$ 285
current_price: HK$ 198
summary: 当前估值尚未充分反映 AI 商业化和海外收入扩张。
drivers:
  - title: AI 商业化加速
    desc: 付费用户和 ARPU 同步提升。
  - title: 海外市场扩张
    desc: 东南亚企业客户快速增长。
:::
```

Recommended fields:

- `title`
- `rating`
- `target_price`
- `current_price`
- `summary`
- `drivers`

### `business-snapshot`

Use for company profile, facts, and operating summary.

```md
:::business-snapshot
title: 业务快照
body: 公司是企业协作 SaaS 龙头。
facts:
  - label: 头部客户续费率
    value: 97%
  - label: 海外收入占比
    value: 18%
:::
```

Recommended fields:

- `title`
- `body`
- `facts`
- `facts[].label`
- `facts[].value`

### `price-drivers`

Use for price context and core drivers.

```md
:::price-drivers
title: 股价与核心驱动
body: 当前股价对应 FY2026 Forward P/E 32x。
price:
  current: HK$ 198
  target: HK$ 285
drivers:
  - title: AI 付费用户增长
    metric: Q1 +65% QoQ
    desc: 企业版渗透率提升。
:::
```

Recommended fields:

- `title`
- `body`
- `price`
- `drivers`

### `candlestick-chart`

Use for OHLC price history.

```md
:::candlestick-chart
title: 股价区间与月度 K 线
x_axis: 2025-01 至 2026-05
y_axis: HKD
items:
  - date: 2025-01
    open: 140
    high: 155
    low: 132
    close: 148
:::
```

Recommended fields:

- `title`
- `x_axis`
- `y_axis`
- `items[].date`
- `items[].open`
- `items[].high`
- `items[].low`
- `items[].close`

### `line-chart`

Use for time series.

```md
:::line-chart
title: AI 付费用户趋势
unit: 万人
items:
  - period: 2025 Q1
    value: 18
    growth: baseline
  - period: 2026 Q1
    value: 65
    growth: +25%
:::
```

Recommended fields:

- `title`
- `unit`
- `items[].period`
- `items[].value`

### `bar-chart`

Use for category comparison.

```md
:::bar-chart
title: 收入结构变化
unit: 亿元
items:
  - label: 协作订阅
    value: 28.4
    share: 58%
  - label: AI 助手
    value: 8.6
    share: 18%
:::
```

Recommended fields:

- `title`
- `unit`
- `items[].label`
- `items[].value`

### `donut-chart`

Use for proportional breakdown.

```md
:::donut-chart
title: 收入地区占比
center_value: 18%
center_label: 海外收入占比
segments:
  - label: 中国内地
    value: 72%
  - label: 东南亚
    value: 14%
:::
```

Recommended fields:

- `title`
- `center_value`
- `center_label`
- `segments`

### `waterfall-chart`

Use for valuation bridges and value decomposition.

```md
:::waterfall-chart
title: 目标价桥
start: HK$ 198
end: HK$ 285
items:
  - label: 当前股价
    value: 198
    type: start
  - label: AI ARPU 重估
    value: 38
    type: positive
:::
```

Recommended fields:

- `title`
- `start`
- `end`
- `items[].label`
- `items[].value`
- `items[].type`

### `valuation-table`

Use for valuation assumptions.

```md
:::valuation-table
title: 估值
method: P/E 与 EV/Revenue 双维度估值
rows:
  - metric: FY2026 Forward P/E
    current: 32x
    peer_median: 40x
    target: 45x
insight:
  title: 安全边际
  desc: 当前倍数低于目标倍数。
:::
```

Recommended fields:

- `title`
- `method`
- `rows`
- `insight`

### `financial-table`

Use for forecast tables.

```md
:::financial-table
title: 财务预测
rows:
  - metric: 营收（亿元）
    fy2024: 23.1
    fy2025: 32.8
    fy2026e: 48.5
    fy2027e: 65.2
:::
```

Recommended fields:

- `title`
- `rows`
- period columns such as `fy2024`, `fy2025`, `fy2026e`

### `risk-matrix`

Use for risks and catalysts.

```md
:::risk-matrix
title: 风险与催化剂
risks:
  - severity: high
    title: AI 合规政策风险
    desc: 合规要求可能延缓功能上线。
catalysts:
  - date: 2026 Q3
    title: AI 付费用户突破 100 万
    desc: 验证商业化路径。
:::
```

Recommended fields:

- `title`
- `risks`
- `catalysts`

### `catalyst-timeline`

Use for dated catalysts or expected events.

```md
:::catalyst-timeline
title: 未来 12 个月催化剂
items:
  - date: 2026 Q2
    title: Q2 财报披露
    desc: 重点关注 AI 收入占比。
:::
```

Recommended fields:

- `title`
- `items[].date`
- `items[].title`
- `items[].desc`

### `kpi-row`

Use for KPI cards.

```md
:::kpi-row
title: 关键指标
items:
  - label: 目标价
    value: HK$ 285
    note: 较当前价上涨 44%
:::
```

Recommended fields:

- `title`
- `items[].label`
- `items[].value`
- `items[].note`

### `recommendation`

Use for final recommendation and actions.

```md
:::recommendation
title: 最终建议
body: 给予「买入」评级。
actions:
  - title: 建仓区间
    desc: 建议分批建仓。
:::
```

Recommended fields:

- `title`
- `body`
- `actions`

### `footer-note`

Use for disclosures, notes, and disclaimers.

```md
:::footer-note
title: 免责声明
body: 本报告仅供研究参考，不构成买卖建议。
:::
```

Recommended fields:

- `title`
- `body`

## 8. Health Report Tags

These tags are conventions for health tracking, weight management, and wellness reports. They are still plain DSL tags: the parser treats them the same way as any other `:::tag-name` block.

### `weekly-summary`

Use for weekly summary and assessment.

```md
:::weekly-summary
title: 本周总结
period: 2026年5月25日 - 5月31日
summary: 体重回落至目标区间，体脂率稳步下降，继续保持运动习惯。
positives:
  - title: 运动坚持
    desc: 完成 5 天运动计划
  - title: 饮食控制
    desc: 工作日热量摄入达标
improvements:
  - title: 周末饮食
    desc: 需要避免油腻食物
  - title: 睡眠时间
    desc: 尽量在 11 点前入睡
:::
```

Recommended fields:

- `title`
- `period`
- `summary`
- `positives`
- `positives[].title`
- `positives[].desc`
- `improvements`
- `improvements[].title`
- `improvements[].desc`

### `goal-tracker`

Use for goal tracking and progress.

```md
:::goal-tracker
title: 下周目标
goals:
  - title: 运动目标
    target: 5 天
    current: 0
    unit: 天
    desc: 至少运动 5 天，包含 3 次有氧和 2 次力量
  - title: 睡眠目标
    target: 7.5
    current: 7.3
    unit: 小时
    desc: 每晚 11 点前入睡，保证 7-8 小时睡眠
  - title: 饮水目标
    target: 2.0
    current: 1.8
    unit: 升
    desc: 每天至少 2.0 升水
:::
```

Recommended fields:

- `title`
- `goals`
- `goals[].title`
- `goals[].target`
- `goals[].current`
- `goals[].unit`
- `goals[].desc`

### `metrics-panel`

Use for health metrics panel.

```md
:::metrics-panel
title: 关键指标
metrics:
  - label: 周末体重
    value: 68.2 kg
    change: -0.8 kg
    status: good
  - label: BMI
    value: 22.1
    change: -0.3
    status: normal
  - label: 体脂率
    value: 18.5%
    change: -0.3%
    status: good
  - label: 运动天数
    value: 5 天
    change: +1 天
    status: good
  - label: 平均睡眠
    value: 7.3 小时
    change: +0.3 小时
    status: normal
:::
```

Recommended fields:

- `title`
- `metrics`
- `metrics[].label`
- `metrics[].value`
- `metrics[].change`
- `metrics[].status`

### `report-header`

Use for report header with date range and metadata.

```md
:::report-header
title: 减脂周报
eyebrow: Momo Coach · 第 12 周
date_range: 2026.05.19 – 2026.05.26
weigh_day: 2026-05-26
:::
```

Recommended fields:

- `title`
- `eyebrow`
- `date_range`
- `weigh_day`
- `meta` (for custom metadata items)

## 9. General Layout, Content, and Data Tags

These tags cover common website, report, and narrative-page sections. They are useful when an Agent needs richer structure than plain Markdown but does not need a route-specific financial tag.

### `logo-cloud`

Use for partner, customer, media, or integration logos. Since Phase 1 does not support image files as a special type, logos should be text labels or paths.

```md
:::logo-cloud
title: Trusted by teams using
logos:
  - name: Northstar Bank
    src: /logos/northstar.svg
  - name: CloudWorks
    src: /logos/cloudworks.svg
:::
```

Recommended fields:

- `title`
- `logos`
- `logos[].name`
- `logos[].src`

### `pricing`

Use for plan comparison.

```md
:::pricing
title: Pricing
plans:
  - name: Free
    price: $0
    desc: For experiments.
    features:
      - 3 documents
      - Basic HTML export
  - name: Pro
    price: $19
    desc: For production use.
    features:
      - Unlimited documents
      - Custom CSS
:::
```

Recommended fields:

- `title`
- `plans`
- `plans[].name`
- `plans[].price`
- `plans[].features`

### `footer`

Use for navigation, copyright, and legal links.

```md
:::footer
brand: Momo Paper
summary: Markdown DSL to standalone HTML.
links:
  - label: Docs
    href: /docs
  - label: GitHub
    href: /github
copyright: 2026 Momo Paper
:::
```

Recommended fields:

- `brand`
- `summary`
- `links`
- `copyright`

### `quote`

Use for pull quotes, testimonials, and cited claims.

```md
:::quote
text: The best generated pages are structured before they are styled.
source: Momo Paper Design Notes
:::
```

Recommended fields:

- `text`
- `source`

### `callout`

Use for notes, warnings, insights, and important reminders.

```md
:::callout
tone: insight
title: Keep HTML out of the DSL
body: Agents should emit structured blocks; the renderer owns HTML.
:::
```

Recommended fields:

- `tone`
- `title`
- `body`

### `image-grid`

Use for gallery-like image collections. In Phase 1, images are plain fields; the renderer treats them as structured data unless the active CSS theme enhances them.

```md
:::image-grid
title: Product states
images:
  - src: /images/editor.png
    alt: DSL editor
    caption: Author structured content.
  - src: /images/output.png
    alt: HTML output
    caption: Render standalone HTML.
:::
```

Recommended fields:

- `title`
- `images`
- `images[].src`
- `images[].alt`
- `images[].caption`

### `before-after`

Use for transformation stories and comparisons.

```md
:::before-after
title: Before and after
before:
  title: Direct HTML
  items:
    - Brittle structure
    - Hard to validate
after:
  title: Markdown DSL
  items:
    - Structured blocks
    - Clear validation
:::
```

Recommended fields:

- `title`
- `before`
- `after`

### `steps`

Use for ordered workflows.

```md
:::steps
title: Render workflow
items:
  - step: 1
    title: Write DSL
    desc: Agent writes Markdown with blocks.
  - step: 2
    title: Validate
    desc: Momo Paper reports syntax errors.
  - step: 3
    title: Render
    desc: The CLI emits standalone HTML.
:::
```

Recommended fields:

- `title`
- `items[].step`
- `items[].title`
- `items[].desc`

### `card-grid`

Use for collections of repeated cards.

```md
:::card-grid
title: Document routes
cards:
  - title: Landing
    desc: Product and marketing pages.
  - title: Equity report
    desc: Research notes and valuation pages.
:::
```

Recommended fields:

- `title`
- `cards`
- `cards[].title`
- `cards[].desc`

### `two-columns`

Use for paired content.

```md
:::two-columns
title: Split layout
left:
  title: Content
  body: Markdown DSL defines structure.
right:
  title: Rendering
  body: CSS defines presentation.
:::
```

Recommended fields:

- `title`
- `left`
- `right`

### `three-columns`

Use for three-part explanations.

```md
:::three-columns
title: System layers
columns:
  - title: Content
    body: Markdown and structured fields.
  - title: Parser
    body: Validation and AST.
  - title: Renderer
    body: HTML and CSS output.
:::
```

Recommended fields:

- `title`
- `columns`
- `columns[].title`
- `columns[].body`

### `table`

Use for generic row/column data. Prefer explicit keys instead of Markdown tables.

```md
:::table
title: Browser support
rows:
  - feature: Standalone HTML
    status: supported
    note: CSS is inlined.
  - feature: PDF export
    status: planned
    note: Phase 2.
:::
```

Recommended fields:

- `title`
- `rows`

### `chart`

Use for generic chart data when a specific chart tag is not needed. Prefer the more specific `line-chart`, `bar-chart`, `donut-chart`, `waterfall-chart`, or `candlestick-chart` when possible.

```md
:::chart
type: line
title: Monthly documents
x: month
y: count
data:
  - month: Jan
    count: 12
  - month: Feb
    count: 28
:::
```

Recommended fields:

- `type`
- `title`
- `data`

### `metric-card`

Use for a single highlighted metric.

```md
:::metric-card
label: Render success rate
value: 99.9%
delta: +2.1pp
note: Measured on valid DSL inputs.
:::
```

Recommended fields:

- `label`
- `value`
- `delta`
- `note`

### `funnel`

Use for conversion funnels.

```md
:::funnel
title: Agent generation funnel
steps:
  - label: Prompt accepted
    value: 1000
  - label: Valid DSL
    value: 860
  - label: HTML rendered
    value: 842
:::
```

Recommended fields:

- `title`
- `steps`
- `steps[].label`
- `steps[].value`

### `diagram`

Use for structured diagrams when a future renderer may enhance the output. Keep data explicit.

```md
:::diagram
type: flowchart
title: DSL render pipeline
nodes:
  - id: author
    label: Agent writes DSL
  - id: parser
    label: Parser validates
  - id: html
    label: HTML output
edges:
  - from: author
    to: parser
  - from: parser
    to: html
:::
```

Recommended fields:

- `type`
- `title`
- `nodes`
- `edges`

## 10. Custom Tags

Custom tags are valid:

```md
:::pricing-note
title: Pricing is illustrative
items:
  - Free tier
  - Pro tier
:::
```

The renderer preserves the tag name:

```html
<section class="dsl-block" data-block="pricing-note">
```

This lets future renderers or downstream tools detect and enhance specific tags without changing the parser.

## 11. Output Rules

The generic renderer outputs:

- a standalone HTML document
- inline CSS loaded from a replaceable CSS source file
- escaped user-provided text
- one `<section class="dsl-block" data-block="tag-name">` per DSL block
- full-width document and section bands
- an inner wrapper per section so each block can decide its own content width
- readable HTML for scalars, objects, and lists

The page shell does not impose a fixed-width container around the whole document. Each section owns its own spacing, background, borders, and inner width. This keeps the renderer usable for landing pages, slide-like pages, long documents, and future full-bleed blocks.

The default CLI inlines `momo-paper.css` into the generated HTML. Visual systems are replaceable at render time: keep the same DSL and render with a custom `--css path/to/theme.css`.

The output is intentionally generic. Phase 1 tests parsing and conversion, not final product-grade visual components.

## 12. Validation Errors

The parser fails fast on:

- missing frontmatter opening `---`
- missing frontmatter closing `---`
- missing `document_type`
- `document_type: dashboard`
- missing `locale`
- missing `title`
- invalid tag names
- unclosed `:::tag-name` blocks
- malformed key/value data
- tab indentation

Errors should include as much context as possible:

```txt
path/to/file.md: line 12: block hero: unclosed block directive
```

## 13. Agent Writing Rules

Agents should follow these rules:

1. Always start with frontmatter.
2. Always include `document_type`, `locale`, and `title`.
3. Do not use `document_type: dashboard`.
4. Use Markdown for prose and DSL blocks for structured data.
5. Prefer the recommended tags for landing documents.
6. Use lowercase hyphenated tag names.
7. Use spaces for indentation; prefer two spaces.
8. Do not use tabs.
9. Do not emit raw HTML.
10. Do not use unsupported Markdown features when predictable rendering matters.
11. Keep block data explicit; avoid clever shorthand.
12. If validation fails, fix the line and block named in the error.
