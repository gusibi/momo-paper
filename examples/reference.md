---
document_type: landing
locale: en
title: Momo Paper DSL Reference Example
description: Complete Phase 1 example covering recommended Agent tags.
author: Momo Paper
date: 2026-05-31
---

# Momo Paper DSL

Use Markdown for prose and `:::tag-name` blocks for structured content.

- Tags are Agent-facing conventions.
- The runtime parses and renders them generically.
- Invalid syntax should fail with a useful error.

1. Write DSL.
2. Validate DSL.
3. Render HTML.

Inline formatting supports **bold**, *italic*, `code`, and [links](https://example.com).

:::hero
eyebrow: Reference
title: Generate HTML from Markdown DSL
subtitle: Use documented tags so Agents can produce predictable content.
primary_cta:
  label: Validate
  href: /validate
secondary_cta:
  label: Render
  href: /render
:::

:::section
title: Parser contract
body: The parser accepts frontmatter, Markdown body nodes, and structured DSL blocks.
points:
  - No Python business components are required.
  - Tags are preserved in data-block attributes.
  - Errors include line and block context when possible.
:::

:::feature-grid
columns: 3
items:
  - title: Frontmatter
    desc: Document metadata always appears first.
  - title: Markdown body
    desc: Ordinary prose stays readable and easy to edit.
  - title: DSL blocks
    desc: Structured data lives inside fenced tag blocks.
:::

:::timeline
title: Generation flow
items:
  - step: 1
    title: Agent writes DSL
    desc: The Agent follows this reference.
  - step: 2
    title: Parser validates
    desc: Momo Paper checks syntax and required metadata.
  - step: 3
    title: Renderer emits HTML
    desc: The output is a standalone HTML file.
:::

:::comparison
title: Direct HTML vs DSL
left:
  title: Direct HTML
  items:
    - Hard to validate
    - Hard to repair automatically
    - Easy to drift visually
right:
  title: Markdown DSL
  items:
    - Easy to parse
    - Easy for Agents to repair
    - Stable conversion path
:::

:::stats
items:
  - value: 8
    label: Recommended Agent tags
  - value: 1
    label: Generic parser
  - value: 0
    label: Python business components
:::

:::cta
title: Render this document
body: Use the CLI to validate the source and generate standalone HTML.
button:
  label: Run momo render
  href: /docs/render
:::

:::faq
items:
  - question: Are tags hard-coded components?
    answer: No. They are conventions that the generic parser preserves.
  - question: Can I add custom tags?
    answer: Yes. Use lowercase hyphenated tag names.
:::

:::custom-block
title: Custom tags are valid
items:
  - label: tag
    value: custom-block
  - label: output
    value: data-block attribute
:::

:::logo-cloud
title: Trusted by teams using
logos:
  - name: Northstar Bank
    src: /logos/northstar.svg
  - name: CloudWorks
    src: /logos/cloudworks.svg
  - name: Atlas Studio
    src: /logos/atlas.svg
:::

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

:::quote
text: The best generated pages are structured before they are styled.
source: Momo Paper Design Notes
:::

:::callout
tone: insight
title: Keep HTML out of the DSL
body: Agents should emit structured blocks; the renderer owns HTML and CSS.
:::

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

:::card-grid
title: Document routes
cards:
  - title: Landing
    desc: Product and marketing pages.
  - title: Equity report
    desc: Research notes and valuation pages.
  - title: Reference
    desc: Component catalog and syntax examples.
:::

:::two-columns
title: Split layout
left:
  title: Content
  body: Markdown DSL defines structure.
right:
  title: Rendering
  body: CSS defines presentation.
:::

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

:::metric-card
label: Render success rate
value: 99.9%
delta: +2.1pp
note: Measured on valid DSL inputs.
:::

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

:::thesis-panel
title: 投资结论
rating: 买入
target_price: HK$ 285
current_price: HK$ 198
summary: 这是一个财务报告组件示例，用于展示投资结论、目标价和核心驱动。
drivers:
  - title: AI 商业化加速
    desc: 付费用户和 ARPU 同步提升。
  - title: 海外市场扩张
    desc: 海外收入占比持续提升。
:::

:::business-snapshot
title: 业务快照
body: 用于公司简介、业务事实和经营摘要。
facts:
  - label: 头部客户续费率
    value: 97%
  - label: 海外收入占比
    value: 18%
  - label: ISV 合作伙伴
    value: 350+
:::

:::price-drivers
title: 股价与核心驱动
body: 用于展示当前价格、目标价和主要驱动因素。
price:
  current: HK$ 198
  low_52w: HK$ 132
  high_52w: HK$ 218
  target: HK$ 285
drivers:
  - title: AI 付费用户增长
    metric: Q1 +65% QoQ
    desc: 企业版渗透率提升。
  - title: 海外收入翻倍
    metric: DAU +80%
    desc: 本地化渠道贡献新增量。
:::

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
  - date: 2025-09
    open: 176
    high: 205
    low: 168
    close: 198
  - date: 2026-05
    open: 205
    high: 212
    low: 190
    close: 198
:::

:::line-chart
title: AI 付费用户趋势
unit: 万人
items:
  - period: 2025 Q1
    value: 18
    growth: baseline
  - period: 2025 Q4
    value: 52
    growth: +33%
  - period: 2026 Q1
    value: 65
    growth: +25%
:::

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
  - label: 海外订阅
    value: 5.4
    share: 11%
:::

:::donut-chart
title: 收入地区占比
center_value: 18%
center_label: 海外收入占比
segments:
  - label: 中国内地
    value: 72%
  - label: 东南亚
    value: 14%
  - label: 其他海外
    value: 4%
:::

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
  - label: 合规折价
    value: -8
    type: negative
  - label: 目标价
    value: 285
    type: end
:::

:::valuation-table
title: 估值
method: P/E 与 EV/Revenue 双维度估值
rows:
  - metric: FY2026 Forward P/E
    current: 32x
    peer_median: 40x
    target: 45x
  - metric: PEG
    current: 0.76
    peer_median: 1.10
    target: 0.95
insight:
  title: 安全边际
  desc: 当前估值低于目标倍数。
:::

:::financial-table
title: 财务预测
rows:
  - metric: 营收（亿元）
    fy2024: 23.1
    fy2025: 32.8
    fy2026e: 48.5
    fy2027e: 65.2
  - metric: 毛利率
    fy2024: 75%
    fy2025: 78%
    fy2026e: 80%
    fy2027e: 81%
:::

:::risk-matrix
title: 风险与催化剂
risks:
  - severity: high
    title: AI 合规政策风险
    desc: 合规要求可能延缓功能上线。
  - severity: medium
    title: 海外拓展不及预期
    desc: 海外付费意愿可能低于预期。
catalysts:
  - date: 2026 Q3
    title: AI 付费用户突破 100 万
    desc: 验证商业化路径。
:::

:::catalyst-timeline
title: 未来 12 个月催化剂
items:
  - date: 2026 Q2
    title: Q2 财报披露
    desc: 重点关注 AI 收入占比。
  - date: 2026 Q4
    title: ISV 平台交易额突破
    desc: 推动估值向平台型 SaaS 切换。
:::

:::kpi-row
title: 关键指标
items:
  - label: 目标价
    value: HK$ 285
    note: 较当前价上涨 44%
  - label: 当前股价
    value: HK$ 198
    note: FY2026 Forward P/E 32x
  - label: 海外收入占比
    value: 18%
    note: 同比快速提升
:::

:::recommendation
title: 最终建议
body: 用于总结评级、建仓区间、止损位和上修条件。
actions:
  - title: 建仓区间
    desc: 建议在合理区间分批建仓。
  - title: 上修条件
    desc: 若 AI ARPU 超预期，可上修目标价。
:::

:::footer-note
title: 免责声明
body: 本报告仅供研究参考，不构成买卖建议。
:::
