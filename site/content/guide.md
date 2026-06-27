---
document_type: long_doc
locale: zh-CN
title: Momo Paper 使用指南
description: 推荐通过 Skill 方式使用——AI agent 自动处理安装和渲染。也支持手动 CLI 和直接 HTML 模板两种替代工作流。
---

使用 Momo Paper 最简单的方式是通过 Claude Code Skill：AI agent 自动完成从安装到渲染的全部步骤，你只需描述想要什么文档。

偏好手动操作时，可直接使用 CLI 命令或编辑 HTML 模板。三种方式共享同一套设计令牌，输出效果一致。

:::callout
tone: insight
title: 三条工作流速览
body: 推荐方式 Skill（AI agent 全自动处理安装和渲染）· 备选方式 CLI 手动（momo2 validate → render）· 快速方式直接 HTML 模板（打开文件 → 编辑内容 → 浏览器预览）。5 种图表块，嵌入 DSL 的 chart 块即可。
:::

## 推荐方式：通过 Skill 使用

Momo Paper 提供 Claude Code Skill（SKILL.md），这是最推荐的使用方式。无需手动安装——告诉 AI agent 想要创建什么文档，Skill 会自动触发。

Skill 自动处理：检查并安装 momo2 CLI → 选择合适的文档样板 → 生成 Markdown DSL 骨架 → 引导填充内容 → 渲染 HTML。整个过程只需描述需求、确认内容。

```text
# 你只需要这样说：
"帮我生成一份 Q2 产品增长方案"
"帮我做一份简历"
"把这个数据分析渲染成报告"

# Skill 会自动：
# 1. 检测并安装 momo2 CLI（如未安装）
# 2. 选择合适的文档类型
# 3. 生成 Markdown DSL
# 4. 渲染为 HTML 文档
# 5. 打开浏览器预览
```

## 手动安装 CLI

如果你需要直接使用 CLI 命令（而非通过 Skill），可以手动安装引擎。前提条件：Python 3.10+。

```bash
# 1. 创建并激活虚拟环境
python3 -m venv .venv
source .venv/bin/activate

# 2. 安装引擎（可编辑模式）
pip install -e .

# 3.（可选）安装开发依赖，运行测试
pip install -e ".[dev]"

# 验证安装
momo2 --help
```

## CLI 命令参考

安装完成后，你会获得 momo2 命令，用于校验和渲染 Markdown DSL 文档。

```bash
# 校验 DSL 文件的语法和必填元数据
momo2 validate examples/landing.md

# 将 DSL 渲染为单文件 HTML（CSS 内联）
momo2 render examples/landing.md -o dist/landing.html

# 使用不同的视觉主题渲染
momo2 render examples/landing.md -o dist/landing.html --css momo_dsl/styles/vercel.css
```

## Markdown DSL 数据格式

每个文档都以 frontmatter 开头，声明文档类型和元数据，正文混合使用 Markdown 与 `:::block` 结构化块。

- **document_type**：文档语义标签，例如 landing、long_doc、equity_report，出现在页头并引导 Skill 选模板。引擎不按类型校验结构。
- **locale**：zh-CN 或 en。
- **title / description**：文档标题与摘要，用于页头和 SEO。
- **正文**：普通 Markdown 写散文，`:::tag-name` 块写结构化内容，块以 `:::` 结束。

```md
---
document_type: one_pager
locale: zh-CN
title: Q2 增长方案
description: 聚焦留存与激活
---

## 执行摘要

本方案的核心目标是提升留存与激活。

:::stats
items:
  - value: +18%
    label: DAU
  - value: +8pp
    label: 留存
:::

:::recommendation
title: 行动建议
actions:
  - title: Phase 1
    desc: 重设计 onboarding
:::
```

## 嵌入图表

在正文中声明 chart 块，引擎会自动渲染为交互式图表。支持 5 种图表类型：

- **bar-chart（柱状图）**：适合类别对比，items 含 label / value / share。
- **line-chart（折线图）**：适合时间序列和趋势，items 含 period / value / growth。
- **donut-chart（环形图）**：适合比例分解，segments 含 label / value，可设 center_value。
- **candlestick-chart（K 线图）**：适合 OHLC 价格序列，items 含 date / open / high / low / close。
- **waterfall-chart（瀑布图）**：适合数值分解和桥接，items 含 label / value / type。

```md
:::line-chart
title: 月度活跃用户
unit: 万
items:
  - period: 1月
    value: 240
  - period: 2月
    value: 258
  - period: 3月
    value: 275
:::
```

## 直接 HTML 模板（替代方式）

如果你不想用 Skill 或 CLI，可以直接编辑渲染好的独立 HTML 文件。这是零门槛的「直接编辑」模式：

- 打开模板，替换占位内容为你自己的文字。
- 无需 CLI、DSL 或构建步骤——只需要 HTML 和 CSS。
- 设计令牌以 CSS 自定义属性的形式嵌入在每个文件中。

适合需要快速生成一次性文档、或偏好直接操作 HTML 的场景。三种方式共享同一套设计令牌、字体系统与视觉语言。

:::cta
title: 开始创建你的第一份文档
body: 无论选择哪种方式——Skill（AI 自动）、CLI（手动命令）还是 HTML 模板（直接编辑）——输出都共享同一套设计令牌。
button:
  label: 浏览示例画廊
  href: /demo/
:::
