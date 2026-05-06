---
name: momo-paper
description: >
  Use this skill whenever the user wants to create, generate, design, format, or
  build any document, page, slide, chart, diagram, resume, report, letter,
  infographic, or visual narrative. This skill MUST be used for all document
  generation tasks including one-pagers, white papers, portfolios, equity
  reports, changelogs, case studies, research summaries, stats reports, process
  flows, timelines, FAQ pages, formal letters, memos, exec summaries, and
  slide decks. Also trigger when the user asks about template selection,
  document routing, print-safe formatting, embedding diagrams or charts inside
  documents, or choosing between document types. If the user wants to generate
  HTML output for any content, use this skill. When no matching template exists,
  build the HTML from scratch using Momo Paper's design tokens, typography, and
  voice — the system covers the style even when the format is new. Do not skip this skill even if
  the user does not explicitly mention Momo Paper. Use Chinese output when the
  user speaks Chinese or requests Chinese output.
compatibility: requires momo CLI — run `./install.sh` for guided setup, `./install.sh --check` to verify, `./install.sh --upgrade` to update. Install locations are recorded in `.momo-install.json`.
---

# Momo Paper

> A routed design system for documents and visual narratives.
> 用一套路由规则统一 one-pager、长文、简历、幻灯片、研报、信息图与文档内图示。

## Overview

Momo Paper generates documents via a CLI pipeline: resolve the document type → generate a JSON skeleton → fill content → render to HTML. The HTML template direct-edit path remains available for cases that need fine-grained CSS control, but the CLI is the default.

Core principle: **conclusion first, evidence second, detail third.** Every document leads with its main point visible in the first screen or slide.

---

## Step 0 · Ensure CLI is installed

The `momo` CLI must be available before any generation work. Use the config file to locate it reliably across installations.

### 0a · Locate the config file

Read `.momo-install.json` in the skill root directory (same directory as this SKILL.md). This file records where the engine was installed:

```json
{
  "version": "0.2.2",
  "install_dir": "/path/to/momo-paper",
  "engine_dir": "/path/to/momo-paper/scripts/json-engine",
  "python": "/path/to/momo-paper/scripts/json-engine/.venv/bin/python",
  "install_date": "2026-05-06T...",
  "last_check": "2026-05-06T..."
}
```

If the config file exists, use `engine_dir` to find the engine and `python` as the preferred Python interpreter. The `momo` binary lives at `{engine_dir}/.venv/bin/momo`.

### 0b · Verify the CLI

Run the following from the recorded install directory:

```bash
# Check using the venv binary from config
{engine_dir}/.venv/bin/momo list

# Or if momo is already on PATH
momo list

# Verify version matches config
{engine_dir}/.venv/bin/momo --version
```

### 0c · If not installed

If `.momo-install.json` does not exist, or the CLI is not found at the recorded path:

```bash
# Guided install (recommended)
./install.sh

# Or install to a custom directory
./install.sh --dir /your/preferred/path

# Check status
./install.sh --check
```

This runs `pip install -e .` inside `scripts/json-engine/`, creates (or reuses) a `.venv`, and writes `.momo-install.json`.

### 0d · Version check and upgrade

Compare the installed version (from `.momo-install.json` or `momo --version`) against the package version in `scripts/json-engine/pyproject.toml`. If the installed version is older:

```bash
./install.sh --upgrade
```

When the user's repo is updated (git pull), the engine source may have changed. The editable install (`pip install -e .`) means code changes take effect immediately, but if dependencies changed (e.g. new Jinja2 version), re-run `./install.sh --upgrade` to refresh them.

### 0e · CLI quick reference

| Command | Purpose |
|---|---|
| `momo list` | List 15 document types + chart types + locales |
| `momo init -t <type> -l <locale> -o data.json` | Generate JSON skeleton |
| `momo render -d data.json -o output.html` | Render JSON to HTML |
| `momo chart -d data.json -k sections.<key>.chart -o chart.svg` | Extract chart as standalone SVG |
| `momo --version` | Show installed version |

---

## Step 1 · Resolve locale

| User language | Template suffix |
|---|---|
| Chinese (`zh-CN`, primary) | `*.html` / `slides.py` |
| English (`en`) | `*-en.html` / `slides-en.py` |
| Other (best-effort) | Choose by script coverage, then verify |

When ambiguous (e.g. a one-word command like "resume"), ask a one-liner rather than guess. If the user mixes languages, use the dominant reading language of the final output.

---

## Step 2 · Pick the document type

Match the user's wording to a `document_type`. For the full routing table with internal routes, read `references/document-types.md`.

| User says | Type | CN template | EN template |
|---|---|---|---|
| one-pager / 方案 / 执行摘要 / exec summary | `one_pager` | `one-pager.html` | `one-pager-en.html` |
| white paper / 白皮书 / 长文 / 年度总结 / technical report | `long_doc` | `long-doc.html` | `long-doc-en.html` |
| formal letter / 信件 / 辞职信 / 推荐信 / memo | `letter` | `letter.html` | `letter-en.html` |
| portfolio / 作品集 / case studies | `portfolio` | `portfolio.html` | `portfolio-en.html` |
| resume / CV / 简历 | `resume` | `resume.html` | `resume-en.html` |
| slides / PPT / deck / 演示 | `slides` | `slides.py` | `slides-en.py` |
| 个股研报 / equity report / 估值分析 / investment memo / 股票分析 | `equity_report` | `equity-report.html` | `equity-report-en.html` |
| 更新日志 / changelog / release notes / 版本记录 | `changelog` | `changelog.html` | `changelog-en.html` |
| 流程图说明 / workflow page / SOP | `process_flow` | `process-flow.html` | `process-flow-en.html` |
| timeline / 时间线 / roadmap / milestone page | `timeline` | `timeline.html` | `timeline-en.html` |
| faq / 常见问题 / help center page | `faq_page` | `faq-page.html` | `faq-page-en.html` |
| case study / 案例拆解 / 项目复盘 | `case_study` | `case-study.html` | `case-study-en.html` |
| research summary / 研究摘要 / brief report | `research_summary` | `research-summary.html` | `research-summary-en.html` |
| stats report / 数据报告 / KPI report | `stats_report` | `stats-report.html` | `stats-report-en.html` |
| infographic / 信息图 / visual summary | `infographic` | `infographic.html` | `infographic-en.html` |
| landing page / 首页 / 产品页 | `landing` | `landing.html.j2` | `landing.html.j2` |

Resolution rules:
1. Prefer `document_type + locale`.
2. If the user provided `surface + document_shape`, use them directly.
3. If the user used legacy `artifact_type`, map through the alias table in `assets/artifact-presets.json`.
4. If multiple inputs conflict, ask — do not guess.

Long deck (>20 slides): also read Deck Recipe in `references/DESIGN.md` section 8.

### Diagrams (primitives, not a document type)

When the user asks for **a diagram inside** a document (not standalone), route to `assets/diagrams/`:

| User says | Diagram | Template |
|---|---|---|
| 架构图 / architecture / 系统图 / components diagram | Architecture | `assets/diagrams/architecture.html` |
| 流程图 / flowchart / 决策流 / branching logic | Flowchart | `assets/diagrams/flowchart.html` |
| 象限图 / quadrant / 优先级矩阵 / 2×2 matrix | Quadrant | `assets/diagrams/quadrant.html` |
| 柱状图 / bar chart / 分类对比 / grouped bars | Bar Chart | `assets/diagrams/bar-chart.html` |
| 折线图 / line chart / 趋势 / 股价 / time series | Line Chart | `assets/diagrams/line-chart.html` |
| 环形图 / donut / pie / 占比 / 分布结构 | Donut Chart | `assets/diagrams/donut-chart.html` |
| 状态机 / state machine / 状态图 / lifecycle | State Machine | `assets/diagrams/state-machine.html` |
| 时间线 / timeline / 里程碑 / milestones / roadmap | Timeline | `assets/diagrams/timeline.html` |
| 泳道图 / swimlane / 跨角色流程 / cross-team flow | Swimlane | `assets/diagrams/swimlane.html` |
| 树状图 / tree / hierarchy / 层级 / 组织架构 | Tree | `assets/diagrams/tree.html` |
| 分层图 / layer stack / 分层架构 / OSI / stack | Layer Stack | `assets/diagrams/layer-stack.html` |
| 维恩图 / venn / 交集 / overlap / 集合关系 | Venn | `assets/diagrams/venn.html` |
| K 线 / candlestick / OHLC / 股价走势 / price history | Candlestick | `assets/diagrams/candlestick.html` |
| 瀑布图 / waterfall / 收入桥 / revenue bridge / decomposition | Waterfall | `assets/diagrams/waterfall.html` |

Read `references/diagrams.md` before drawing — it has the selection guide, token map, and anti-pattern table. Extract the `<svg>` block from the template and drop it into a `<figure>` inside the target document.

Before drawing, always ask: **would a well-written paragraph teach the reader less than this diagram?** If no, don't draw.

**Auto-select charts from data.** When content contains structured numerical data, choose the chart type automatically:

| Data pattern | Chart type |
|---|---|
| proportional breakdown | donut |
| time series | line |
| category comparison | bar |
| price history | candlestick |
| value decomposition | waterfall |

Do not wait for the user to explicitly request a chart. If prose teaches better than the chart, skip it.

---

## Step 2a · Source and material pass

Run this before filling content when the document depends on facts or materials outside the user's draft. Skip only for personal drafts where the user already supplied everything needed.

### Source check

Trigger when the document mentions a specific company, product, person, release date, version, funding round, metric, market fact, technical spec, or any current fact likely to change.

- Use primary sources before writing: user-provided material, official site, docs, filings, press release, app store page, or repo release
- Keep a short note of source names and dates for facts that drive the document
- If sources conflict or a fact cannot be checked quickly, ask the user instead of choosing silently
- Avoid current-sounding claims such as "latest", "recent", "new", version numbers, launch dates, or financial figures unless they are checked

### Material check

Trigger when the document is about a company, product, project, venue, or personal brand.

Confirm the materials that make the subject recognizable before layout:

| Need | Required when | Accept |
|---|---|---|
| Logo | Any branded document | User file or official SVG/PNG |
| Product image | Physical product / venue / object | Official image, user image, or marked gap |
| UI screenshot | App / SaaS / website / tool | Current screenshot, official product image, or user capture |
| Brand colors | Branded one-pager / portfolio / deck | Official value, extracted asset value, or keep system default |
| Fonts | Only if brand typography matters | Official font, close system fallback, or default |

If a required item is missing, use a compact gap table and ask once. Do not replace missing material with generic imagery, approximate logo drawings, or invented values.

---

## Step 2b · Distill raw content (if applicable)

Skip this step if the user already provides structured content (clear sections, bullet points, metrics in place).

When the user hands over **raw material** (meeting notes, brain dump, existing doc in different format, chat transcript, scattered points):

1. **Extract**: pull out every factual claim, number, date, name, source, material reference, and action item
2. **Classify**: map each extract to the target template's sections (read the matching route reference in `references/routes/` for section structure)
3. **Gap-check**: list what the template needs but the raw content doesn't have — include missing facts, missing proof, and missing materials
4. **Ask once**: share the gap table with the user. Do not guess to fill gaps.

Example gap-check:

| Template needs | Found | Missing |
|---|---|---|
| 4 metric cards | "8 years", "50-person team" | 2 more quantifiable results |
| 3-5 core projects | 2 mentioned | at least 1 more with outcome |
| Materials | logo file provided | product screenshot source |

Then proceed to Step 3 with structured, distilled content.

---

## Step 3 · Load the right amount of spec

Pick the tier that matches the task. Default to the lowest tier that covers the work.

| Tier | When | Read |
|---|---|---|
| **Content-only** | Updating text, swapping bullets, translating an existing doc. Layout stays untouched. | Matching route reference from `references/routes/` + template |
| **Layout tweak** | Adjusting spacing, moving sections, changing visual hierarchy within spec. | Route reference + template + `references/DESIGN.md` (spacing, tokens) |
| **New document** | Building from scratch or from raw content. | All: route reference + template + `references/DESIGN.md` + `references/VOICE.md` + `assets/artifact-presets.json` |
| **Sources / materials** | Company, product, market, launch, funding, specs, or branded subject. | Add `references/prompt-contracts.md` source rules + user/source material |
| **Deck (>20 slides)** | Long presentation needing section headers, dividers, varied layouts. | Add `references/DESIGN.md` section 8 (Deck Recipe) |
| **Diagram** | Embedding SVG in a doc. | `references/diagrams.md` only (has its own token map) + matching diagram template |
| **Review / QA** | Final check before shipping. | `references/style-checklist.md` |

You can always escalate mid-task if the work turns out to need more than the initial tier.

The full spec files for reference:

- Design foundations: `references/DESIGN.md`
- Copy tone: `references/VOICE.md`
- Input schema & contracts: `references/prompt-contracts.md`
- Style QA: `references/style-checklist.md`
- Diagrams: `references/diagrams.md`

---

## Step 4 · CLI-first generation

The default path is CLI-driven. Use the HTML direct-edit path only when the JSON schema cannot express the needed layout.

### 4a · Generate JSON skeleton

Use the `momo` binary from the install recorded in `.momo-install.json`. If the venv binary is not on PATH, invoke it directly:

```bash
# If momo is on PATH (after install.sh setup)
momo init -t <document_type> -l <locale> -o data.json

# Or use the full path from config
{engine_dir}/.venv/bin/momo init -t <document_type> -l <locale> -o data.json
```

This writes a JSON skeleton with the correct `document_type`, `locale`, and placeholder `meta` / `sections` structure. Each document type has a JSON Schema in `scripts/json-engine/momo_paper/schemas/` — read the matching schema to understand available section fields.

### 4b · Fill content into the JSON

- Edit `data.json` with the user's content
- Each section maps to a key under `sections` (or `slides` for slide decks)
- Content follows `references/VOICE.md`: data over adjectives, distinctive phrasing over industry clichés
- Preserve the quiet, credible, document-first tone. Do not drift into marketing language
- For `web_dual` documents, keep the output readable both in browser and as print/PDF
- Use motion only decoratively. The structure must still work without animation

**Charts in JSON:** Add a `chart` object inside any section:

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

### 4c · Render

```bash
momo render -d data.json -o output.html
# or: {engine_dir}/.venv/bin/momo render -d data.json -o output.html
```

For standalone chart SVG:
```bash
momo chart -d data.json -k sections.<key>.chart -o chart.svg
```

### 4d · HTML direct-edit path

There are two scenarios where you build HTML directly instead of using the CLI:

**A. Template exists but JSON is too rigid.** Copy the template from `assets/templates/` and edit the HTML body directly. CSS stays untouched.

**B. No matching template.** When the user's request doesn't map to any document type in Step 2's table (e.g. a landing page, event page, certificate, gallery, recipe card), build a standalone HTML page from scratch — but stay inside the Momo Paper design system.

When building without a template, apply these constraints:

- **Tokens**: Read `assets/design-tokens.json` and `references/DESIGN.md`. Use only the defined colors (`ink`, `paper`, `canvas`, `line`, `brand`), typography (system font stack), and spacing scale. Embed them as CSS custom properties at the top of the `<style>` block, matching the pattern used in `assets/templates/`.
- **Layout**: Follow the surface rules — `web_dual` (browser + print-safe), `slides` (16:9 single-viewport), or `visual_sheet` (single reading path, compressed prose).
- **Voice**: Content follows `references/VOICE.md` — data over adjectives, distinctive phrasing over clichés.
- **Structure**: Conclusion first, evidence second, detail third. Each section has one purpose. Main point visible without scrolling.

The goal is not to stretch a template that doesn't fit, but to apply the same visual language to a new layout. The design system is the constant; the template is just one shape it takes.

### Output rules

- Follow the exact `sectionRecipe` for the selected internal route
- Use only the route's allowed components, patterns, and charts
- The main conclusion is visible in the first screen, first slide, or first section
- Each section has one main purpose

### Auto-select output format

Do not ask the user which format to export. Decide from context:

| Signal | Output | Why |
|---|---|---|
| Any document request | HTML + PDF | PDF is the default deliverable, HTML is the source |
| Slides / PPT / deck | HTML + PDF + PPTX | Presentations need a projectable format |
| "分享" / "发朋友圈" / "share" / "post" / "preview" | + PNG | Social platforms and messaging need images |
| "嵌入" / "插图" / "embed in another doc" | PNG only | Used as material inside other documents |
| User explicitly says a format | Follow the user | Explicit request overrides auto-selection |

PDF always ships. PPTX follows slides. PNG follows sharing context. The user should never need to think about formats.

---

## Step 5 · Review & verify

Before shipping, run through this checklist:

1. **Route integrity**: Does the output use only whitelisted components, patterns, chart types, and diagram primitives from the selected route?
2. **Locale**: Is the correct CN or EN template used? Does the final output language match the chosen locale?
3. **Visual**: Do all colors come from `assets/design-tokens.json`? No extra gradients or decorative textures? Spacing follows token scale?
4. **Hierarchy**: Is the main conclusion visible above the fold / on the first slide? Are titles factual and short?
5. **Diagrams**: Is each diagram justified (teaches better than prose)? Does each chart have a title and one explicit takeaway?
6. **Voice**: Is the copy clear, restrained, and specific? No hype, slogans, or generic AI filler?
7. **Print-safe**: For `web_dual`, does the page still reveal the main conclusion and structure when printed?

Run `references/style-checklist.md` for the full formal checklist.

---

## Fallback and refusal

**Fallback — no matching template.** When the user's request doesn't match any document type in Step 2, do not refuse. Instead, use Step 4d-B: build a standalone HTML page using Momo Paper's design tokens, typography, and voice. The design system is the constant; the template list is not exhaustive.

**Refusal — push back or ask for clarification if:**

- The user wants a separate dashboard system
- The user wants `comparison_matrix` or `topic_cover` promoted into a document type
- The user wants a visual style that breaks the token or voice constraints (e.g. dark mode, neon, cartoon, saturated multi-color)
- The user explicitly wants Material / Fluent / Tailwind default instead of Momo Paper's visual language

---

## Feedback protocol

When the user gives **vague visual feedback** ("looks off", "太挤了", "not elegant"), do not guess. Ask back with current values:

| User says | Ask about |
|---|---|
| "太挤了" / "too cramped" | Which element? Line-height? Padding? Page margin? |
| "太松了" / "too loose" | Same direction, reversed |
| "颜色不对" / "color feels wrong" | Which element? Accent overused? A gray reading too cool? |
| "不够好看" / "not polished" | Font rendering? Alignment? Whitespace distribution? Hierarchy? |
| "看着不专业" / "unprofessional" | Content wording? Or layout (alignment, consistency)? |

Template response: "X is currently set to Y. Would you like (a) [specific alternative within spec] or (b) [another option]?"

Never say "I'll adjust the spacing" without naming the exact property and its new value.

---

## Planning skeleton

When asked to plan before rendering, use this YAML skeleton (full spec in `references/prompt-contracts.md`):

```yaml
document_type:
locale:
surface:
document_shape:
route_used:
template_used:
goal:
audience:
sections:
  - name:
    purpose:
    components:
    pattern:
    chart_type:
    takeaway:
diagram_candidates: []
checklist_risks: []
```
