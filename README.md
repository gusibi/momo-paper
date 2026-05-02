# Momo Paper

> A routed design system for documents and visual narratives.

用一套路由规则统一 one-pager、长文、简历、幻灯片、研报、信息图与文档内图示。

## What it is

Momo Paper is a document-first design system for agents. It does two jobs:

- route user intent to the correct document type, internal route, and starter template
- keep visual narratives inside one quiet, credible, print-safe visual language

If unsure, ask a one-liner rather than guess.
不确定时先问一句，不要猜。

## JSON Rendering Engine

Momo Paper includes a JSON-driven rendering engine (`json-engine/`). Instead of filling HTML templates by hand, you write structured JSON and the engine renders it to print-safe HTML with design tokens applied automatically.

### Install

```bash
cd json-engine
pip install -e .
```

This gives you the `momo` CLI.

### CLI Commands

```bash
# List all supported document types
momo list

# Generate an empty JSON skeleton for a document type
momo init -t equity_report -o my-report.json

# Render JSON data to HTML
momo render -d data/report.json -o output/report.html

# Render from stdin
cat report.json | momo render -d - -o output.html

# Extract a chart as standalone SVG
momo chart -d data/report.json -k sections.trends.chart -o chart.svg
```

### JSON Data Format

Every document shares the same top-level structure:

```json
{
  "document_type": "equity_report",
  "locale": "zh-CN",
  "meta": {
    "title": "...",
    "subtitle": "...",
    "eyebrow": "Momo Paper / equity_report / zh-CN",
    "date": "2025-04-27",
    "analyst": "..."
  },
  "sections": {
    ...
  }
}
```

- `document_type` — one of the 14 supported types (see `momo list`)
- `locale` — `zh-CN` or `en` (auto-switches section headings)
- `meta` — title, subtitle, and optional fields (eyebrow, date, author, disclaimer)
- `sections` — document-specific content, defined by JSON Schema in `json-engine/momo_paper/schemas/`

### Embedding Charts

Add a `chart` object inside any section to embed an SVG chart:

```json
{
  "chart": {
    "type": "line",
    "title": "MAU Growth",
    "height": 260,
    "data": {
      "labels": ["Jan", "Feb", "Mar"],
      "values": [100, 120, 150]
    }
  }
}
```

Supported chart types: `bar`, `line`, `donut`.

### MCP Tool

The engine can be called as an MCP tool (`momo-paper-render`) — see `json-engine/mcp-tool.json` for the tool definition.

### Files

| File | Purpose |
| --- | --- |
| `json-engine/momo_paper/engine.py` | Core rendering engine |
| `json-engine/momo_paper/cli.py` | CLI entry point |
| `json-engine/momo_paper/charts.py` | SVG chart rendering |
| `json-engine/momo_paper/templates/*.html.j2` | Jinja2 templates (14 types) |
| `json-engine/momo_paper/schemas/*.schema.json` | JSON Schema for each document type |
| `json-engine/momo_paper/examples/sample-*.json` | Sample data files |
| `json-engine/render_all.py` | Batch render all samples via engine API |
| `json-engine/tests/` | Test suite |

## Step 1 · Pick the language

- `zh-CN`: choose the CN template
- `en`: choose the EN template

If the user mixes languages, use the dominant reading language of the final output.

## Step 2 · Pick the document type

| User says | Document Type | Internal Route | CN template | EN template |
| --- | --- | --- | --- | --- |
| `one-pager / 方案 / 执行摘要 / exec summary` | `one_pager` | `web_dual.explainer` | `assets/templates/one-pager.html` | `assets/templates/one-pager-en.html` |
| `white paper / 白皮书 / 长文 / 年度总结 / technical report` | `long_doc` | `web_dual.editorial_article` | `assets/templates/long-doc.html` | `assets/templates/long-doc-en.html` |
| `formal letter / 信件 / 辞职信 / 推荐信 / memo` | `letter` | `web_dual.letter` | `assets/templates/letter.html` | `assets/templates/letter-en.html` |
| `portfolio / 作品集 / case studies` | `portfolio` | `web_dual.portfolio` | `assets/templates/portfolio.html` | `assets/templates/portfolio-en.html` |
| `resume / CV / 简历` | `resume` | `web_dual.resume_profile` | `assets/templates/resume.html` | `assets/templates/resume-en.html` |
| `slides / PPT / deck / 演示` | `slides` | `slides.explainer` | `assets/templates/slides.py` | `assets/templates/slides-en.py` |
| `个股研报 / equity report / 估值分析 / investment memo / 股票分析` | `equity_report` | `web_dual.equity_report` | `assets/templates/equity-report.html` | `assets/templates/equity-report-en.html` |
| `更新日志 / changelog / release notes / 版本记录` | `changelog` | `web_dual.changelog` | `assets/templates/changelog.html` | `assets/templates/changelog-en.html` |
| `流程图说明 / workflow page / SOP` | `process_flow` | `web_dual.process_flow` | `assets/templates/process-flow.html` | `assets/templates/process-flow-en.html` |
| `timeline / 时间线 / roadmap / milestone page` | `timeline` | `web_dual.timeline` | `assets/templates/timeline.html` | `assets/templates/timeline-en.html` |
| `faq / 常见问题 / help center page` | `faq_page` | `web_dual.faq_page` | `assets/templates/faq-page.html` | `assets/templates/faq-page-en.html` |
| `case study / 案例拆解 / 项目复盘` | `case_study` | `web_dual.case_study` | `assets/templates/case-study.html` | `assets/templates/case-study-en.html` |
| `research summary / 研究摘要 / brief report` | `research_summary` | `web_dual.research_summary` | `assets/templates/research-summary.html` | `assets/templates/research-summary-en.html` |
| `stats report / 数据报告 / KPI report` | `stats_report` | `web_dual.stats_report` | `assets/templates/stats-report.html` | `assets/templates/stats-report-en.html` |
| `infographic / 信息图 / visual summary` | `infographic` | `visual_sheet.infographic` | `assets/templates/infographic.html` | `assets/templates/infographic-en.html` |

Long deck (>20 slides): also read Deck Recipe in [DESIGN.md](./DESIGN.md) section 8.

## Step 3 · Add diagrams only when they teach better than prose

Diagrams are primitives inside long docs, portfolios, slide decks, equity reports, or research summaries. They are not a separate document type.

Read [references/diagrams.md](./references/diagrams.md) before drawing.

| User says | Diagram | Template |
| --- | --- | --- |
| `架构图 / architecture / 系统图 / components diagram` | `architecture` | `assets/diagrams/architecture.html` |
| `流程图 / flowchart / 决策流 / branching logic` | `flowchart` | `assets/diagrams/flowchart.html` |
| `象限图 / quadrant / 优先级矩阵 / 2×2 matrix` | `quadrant` | `assets/diagrams/quadrant.html` |
| `柱状图 / bar chart / 分类对比 / grouped bars` | `bar_chart` | `assets/diagrams/bar-chart.html` |
| `折线图 / line chart / 趋势 / 股价 / time series` | `line_chart` | `assets/diagrams/line-chart.html` |
| `环形图 / donut / pie / 占比 / 分布结构` | `donut_chart` | `assets/diagrams/donut-chart.html` |
| `状态机 / state machine / 状态图 / lifecycle` | `state_machine` | `assets/diagrams/state-machine.html` |
| `时间线 / timeline / 里程碑 / milestones / roadmap` | `timeline_diagram` | `assets/diagrams/timeline.html` |
| `泳道图 / swimlane / 跨角色流程 / cross-team flow` | `swimlane` | `assets/diagrams/swimlane.html` |
| `树状图 / tree / hierarchy / 层级 / 组织架构` | `tree` | `assets/diagrams/tree.html` |
| `分层图 / layer stack / 分层架构 / OSI / stack` | `layer_stack` | `assets/diagrams/layer-stack.html` |
| `维恩图 / venn / 交集 / overlap / 集合关系` | `venn` | `assets/diagrams/venn.html` |
| `K 线 / candlestick / OHLC / 股价走势 / price history` | `candlestick` | `assets/diagrams/candlestick.html` |
| `瀑布图 / waterfall / 收入桥 / revenue bridge / decomposition` | `waterfall` | `assets/diagrams/waterfall.html` |

Before drawing, ask: would a well-written paragraph teach the reader less than this diagram? If no, do not draw.

## Auto-select charts from data

When the content contains structured numerical data, choose the appropriate chart type and embed it. Do not wait for the user to request a chart.

- proportional breakdown -> donut
- time series -> line
- category comparison -> bar
- price history -> candlestick
- value decomposition -> waterfall

If a paragraph explains the point better, do not force a chart.

## Files to read

- [SKILL.md](./SKILL.md): runtime agent usage
- [AGENTS.md](./AGENTS.md): repository maintenance rules
- [DESIGN.md](./DESIGN.md): taxonomy, foundations, deck recipe, non-negotiables
- [references/document-types.md](./references/document-types.md): full document type routing table
- [references/diagrams.md](./references/diagrams.md): diagram guide, token map, anti-patterns
- [artifact-presets.json](./artifact-presets.json): machine-readable route registry
- [json-engine/](./json-engine/): JSON-driven rendering engine, CLI, templates, schemas

## Current exclusions

- `dashboard` is intentionally out of scope for the current system
- `comparison_matrix` and `topic_cover` remain pattern candidates, not document types
