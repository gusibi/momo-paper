# Momo Paper

> A routed design system for documents and visual narratives.
> 用一套路由规则统一 one-pager、长文、简历、幻灯片、研报、信息图与文档内图示。

## Two Approaches

Momo Paper gives you two ways to create documents:

| | Direct HTML Templates | JSON Rendering Engine |
|---|---|---|
| **How** | Pick a starter HTML, fill in content | Write structured JSON, engine renders to HTML |
| **Best for** | Quick one-offs, manual editing | AI agents, batch generation, API-driven workflows |
| **Design tokens** | Hardcoded in each template | Centralized, applied automatically |
| **Charts** | Static SVG from `assets/diagrams/` | Programmatic via `charts.py` (5 types) |
| **Validation** | None | JSON Schema per document type |
| **Output** | Standalone HTML files | Print-safe HTML with CSS custom properties |

Both approaches share the same design tokens, typography, and visual language.

## Quick Start

**Prerequisites:** Python 3.10+

```bash
# 1. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install the JSON engine
cd scripts/json-engine
pip install -e .

# 3. List available document types
momo list

# 4. Generate a skeleton and render your first document
momo init -t one_pager -o my-doc.json
# edit my-doc.json with your content
momo render -d my-doc.json -o my-doc.html
# open my-doc.html in your browser
```

That's it. You now have a print-safe, design-token-aware HTML document.

## JSON Rendering Engine

The engine (`scripts/json-engine/`) takes structured JSON data and renders it through Jinja2 templates with centralized design tokens.

### Install

```bash
cd scripts/json-engine

# Editable install (for development)
pip install -e .

# With dev dependencies (tests)
pip install -e ".[dev]"
```

This gives you two CLI entry points: `momo` and `momo-paper` (they're the same).

### CLI Commands

```bash
# List all 15 document types (with Chinese + English names)
momo list

# Generate a JSON skeleton for any type
momo init -t equity_report -o my-report.json
momo init -t slides -o my-deck.json
momo init -t resume -l en -o my-resume.json

# Render JSON to HTML
momo render -d my-report.json -o output/report.html

# Render from stdin
cat my-report.json | momo render -d - -o output.html

# Render a chart as standalone SVG
momo chart -d my-report.json -k sections.trends.chart -o chart.svg

# Batch render all sample files
python render_all.py
```

### JSON Data Format

Every document shares this top-level structure (except `slides`, which uses `slides` instead of `sections`):

```json
{
  "document_type": "equity_report",
  "locale": "zh-CN",
  "meta": {
    "title": "...",
    "subtitle": "...",
    "eyebrow": "Momo Paper / equity_report / zh-CN",
    "date": "2025-04-27",
    "author": "..."
  },
  "sections": {
    ...
  }
}
```

| Field | Description |
|---|---|
| `document_type` | One of 15 supported types (see `momo list`) |
| `locale` | `zh-CN` or `en` (auto-switches section headings) |
| `meta` | Title, subtitle, and optional fields (eyebrow, date, author) |
| `sections` | Document-specific content, defined by JSON Schema in `momo_paper/schemas/` |

### Embedding Charts

Add a `chart` object inside any section. The engine renders it to inline SVG.

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

**Programmatic chart types** (data-driven, rendered by `charts.py`):

| Type | Use case | Data shape |
|---|---|---|
| `bar` | Category comparison | `values: [n, ...]` |
| `line` | Time series, trends | `values: [n, ...]` |
| `donut` | Proportional breakdown | `values: [n, ...]` |
| `candlestick` | OHLC price history | `values: [{o,h,l,c}, ...]` |
| `waterfall` | Value decomposition, bridge | `values: [n, ...]` |

For K-line/candlestick, use short keys (`o`, `h`, `l`, `c`) or long keys (`open`, `high`, `low`, `close`).

### Run Tests

```bash
cd scripts/json-engine
pip install -e ".[dev]"
python -m pytest tests/ -v
```

### MCP Tool

The engine can be called as an MCP server tool (`momo-paper-render`). See `scripts/json-engine/mcp-tool.json` for the definition.

## Direct HTML Templates

The `assets/templates/` directory contains 30 standalone HTML files (15 types x 2 locales). These are the direct-edit approach:

- Open the template, replace placeholder content with your own
- No CLI, no JSON, no build step — just HTML and CSS
- Design tokens are embedded as CSS custom properties in each file

Use these when you need a quick one-off document or prefer working directly with HTML.

## Document Types

| User says | Type | CN template | EN template |
|---|---|---|---|
| `one-pager / 方案 / 执行摘要` | `one_pager` | `assets/templates/one-pager.html` | `assets/templates/one-pager-en.html` |
| `white paper / 白皮书 / 长文` | `long_doc` | `assets/templates/long-doc.html` | `assets/templates/long-doc-en.html` |
| `letter / 信件 / 推荐信 / memo` | `letter` | `assets/templates/letter.html` | `assets/templates/letter-en.html` |
| `portfolio / 作品集` | `portfolio` | `assets/templates/portfolio.html` | `assets/templates/portfolio-en.html` |
| `resume / CV / 简历` | `resume` | `assets/templates/resume.html` | `assets/templates/resume-en.html` |
| `slides / PPT / deck / 演示` | `slides` | `assets/templates/slides.py` | `assets/templates/slides-en.py` |
| `equity report / 研报 / 估值分析` | `equity_report` | `assets/templates/equity-report.html` | `assets/templates/equity-report-en.html` |
| `changelog / 更新日志 / release notes` | `changelog` | `assets/templates/changelog.html` | `assets/templates/changelog-en.html` |
| `process flow / 流程图说明 / SOP` | `process_flow` | `assets/templates/process-flow.html` | `assets/templates/process-flow-en.html` |
| `timeline / 时间线 / roadmap` | `timeline` | `assets/templates/timeline.html` | `assets/templates/timeline-en.html` |
| `faq / 常见问题` | `faq_page` | `assets/templates/faq-page.html` | `assets/templates/faq-page-en.html` |
| `case study / 案例拆解 / 项目复盘` | `case_study` | `assets/templates/case-study.html` | `assets/templates/case-study-en.html` |
| `research summary / 研究摘要` | `research_summary` | `assets/templates/research-summary.html` | `assets/templates/research-summary-en.html` |
| `stats report / 数据报告 / KPI` | `stats_report` | `assets/templates/stats-report.html` | `assets/templates/stats-report-en.html` |
| `infographic / 信息图` | `infographic` | `assets/templates/infographic.html` | `assets/templates/infographic-en.html` |

> **slides** uses Python-based generation for complex layouts. The JSON engine supports it with a Jinja2 template (`slides.html.j2`) and 16:9 viewport.

## Diagrams & Charts

14 diagram primitives in `assets/diagrams/`. The 5 programmatic chart types (bar, line, donut, candlestick, waterfall) can also be rendered via the JSON engine — see [Embedding Charts](#embedding-charts).

| Diagram | Template | Programmatic? |
|---|---|---|
| Architecture / 架构图 | `architecture.html` | — |
| Flowchart / 流程图 | `flowchart.html` | — |
| Quadrant / 象限图 | `quadrant.html` | — |
| Bar chart / 柱状图 | `bar-chart.html` | yes |
| Line chart / 折线图 | `line-chart.html` | yes |
| Donut chart / 环形图 | `donut-chart.html` | yes |
| Candlestick / K线 | `candlestick.html` | yes |
| Waterfall / 瀑布图 | `waterfall.html` | yes |
| State machine / 状态机 | `state-machine.html` | — |
| Timeline / 时间线 | `timeline.html` | — |
| Swimlane / 泳道图 | `swimlane.html` | — |
| Tree / 树状图 | `tree.html` | — |
| Layer stack / 分层图 | `layer-stack.html` | — |
| Venn / 维恩图 | `venn.html` | — |

## Development

```bash
# Install with dev dependencies
cd scripts/json-engine
pip install -e ".[dev]"

# Run tests
python -m pytest tests/ -v

# Batch render all samples
python render_all.py

# Render a sample to verify
momo render -d momo_paper/examples/sample-letter.json -o /tmp/letter.html
```

## Files Reference

| File | Purpose |
|---|---|
| `scripts/json-engine/momo_paper/engine.py` | Core rendering engine |
| `scripts/json-engine/momo_paper/cli.py` | CLI entry point (Click) |
| `scripts/json-engine/momo_paper/charts.py` | SVG chart rendering (5 types) |
| `scripts/json-engine/momo_paper/templates/*.html.j2` | Jinja2 templates (15 types) |
| `scripts/json-engine/momo_paper/schemas/*.schema.json` | JSON Schema per document type |
| `scripts/json-engine/momo_paper/examples/sample-*.json` | Sample data files |
| `scripts/json-engine/render_all.py` | Batch render all samples via engine API |
| `scripts/json-engine/tests/` | Test suite (69 tests) |
| `assets/design-tokens.json` | Design tokens (colors, fonts, spacing) |
| `assets/artifact-presets.json` | Machine-readable route registry |
| `references/DESIGN.md` | Taxonomy, foundations, non-negotiables |
| `references/prompt-contracts.md` | Agent workflow rules and input contracts |
| `references/` | Per-route reference docs |

## Current Exclusions

- `dashboard` is intentionally out of scope
- `comparison_matrix` and `topic_cover` remain pattern candidates, not document types
