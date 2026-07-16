---
document_type: long_doc
locale: zh-CN
title: 组件目录
description: Momo Paper 引擎支持的 Markdown 特性与结构化块全集。每条均含渲染效果与 DSL 源码，可直接复用。
---

引擎的能力由三层组成：Markdown 散文渲染、结构化块（`:::block`）、以及按主题令牌自动着色的图表。本页逐条列出可用组件，每条配渲染效果与 DSL 源码。图表块共 5 种，详见[图表演示](/charts/)。

`document_type` 用于选择文档契约。正式类型会进入 strict Schema 校验；未注册类型进入 experimental/free mode，并继续允许任意合法 block 通过通用 renderer 展示。下方组件主要用于开放探索，正式模板允许的 block 以对应 Schema 为准。

## Markdown 基础

正文按 CommonMark 子集渲染：标题、段落、列表、引用、表格、分隔线、行内标记与代码块。

### 标题层级

`#` 与 `##` 都映射为 `<h2>`，`###` 映射为 `<h3>`，不存在正文 `<h1>`（页头标题是唯一的 `<h1>`），层级不跳级。

## 二级标题

### 三级标题

```md
## 二级标题

### 三级标题
```

### 段落与行内标记

支持加粗、斜体、链接、行内代码与图片。行内代码内的 `![x](y)` 保持字面，不会被解析为图片。

这是一段正文，含 **加粗**、*斜体*、[链接](/guide/) 与 `行内代码`。

```md
这是一段正文，含 **加粗**、*斜体*、[链接](/guide/) 与 `行内代码`。
```

### 列表

无序列表用 `-`，有序列表用 `数字.`。

- 声明 frontmatter
- 编写 Markdown 散文
- 嵌入 `:::block` 结构化块

1. 校验 DSL 语法
2. 渲染为单文件 HTML
3. 浏览器或打印预览

```md
- 声明 frontmatter
- 编写 Markdown 散文
- 嵌入 `:::block` 结构化块

1. 校验 DSL 语法
2. 渲染为单文件 HTML
3. 浏览器或打印预览
```

### 引用

引用块用于强调或摘录，带品牌色边框。

> 约束即解放：当排版决策由系统承担，创作者只需专注内容本身。

```md
> 约束即解放：当排版决策由系统承担，创作者只需专注内容本身。
```

### 表格

表格自动识别分隔行，表头使用 `<th scope="col">`。

| 组件 | 用途 | 是否引擎特化 |
|------|------|--------------|
| chart 块 | 数据图表 | 是 |
| 通用块 | 结构化布局 | 否，主题 CSS 样式化 |
| Markdown | 散文与行内 | 是 |

```md
| 组件 | 用途 | 是否引擎特化 |
|------|------|--------------|
| chart 块 | 数据图表 | 是 |
| 通用块 | 结构化布局 | 否，主题 CSS 样式化 |
| Markdown | 散文与行内 | 是 |
```

### 代码块

围栏代码块按语言高亮（highlight.js）。

```python
from momo_dsl import parse_file, render_html

doc = parse_file("report.md")
html = render_html(doc)
Path("report.html").write_text(html, encoding="utf-8")
```

````md
```python
from momo_dsl import parse_file, render_html

doc = parse_file("report.md")
html = render_html(doc)
Path("report.html").write_text(html, encoding="utf-8")
```
````

### 分隔线

`---` 渲染为水平分隔线，用于强章节断开。

---

```md
---
```

## 通用结构块

任意 `:::tag-name` 都会被渲染为带 `data-block="tag-name"` 的区块，键值字段自动展开。主题 CSS 按标签名赋予样式，因此组件库可由样式表扩展，无需改引擎。`id`、`layout`、标量 `columns` 是展示提示，会从字段中剥离并提升为属性。

### hero · 首屏

用于落地页首屏，含 eyebrow、title、subtitle 与两个行动按钮。

:::hero
eyebrow: 开源文档引擎 · 2.1
title: 用 Markdown DSL 产出排版精良的 HTML 文档
subtitle: 声明结构化块，引擎渲染为打印就绪的单文件 HTML。
primary_cta:
  label: 查看使用指南
  href: /guide/
secondary_cta:
  label: 浏览组件
  href: /components/
:::

```md
:::hero
eyebrow: 开源文档引擎 · 2.1
title: 用 Markdown DSL 产出排版精良的 HTML 文档
subtitle: 声明结构化块，引擎渲染为打印就绪的单文件 HTML。
primary_cta:
  label: 查看使用指南
  href: /guide/
secondary_cta:
  label: 浏览组件
  href: /components/
:::
```

### stats · 指标条

横向排列的大数字指标。

:::stats
items:
  - value: 5
    label: 图表块
  - value: 4
    label: 健康块
  - value: 11
    label: 通用结构块
  - value: 2
    label: 内置主题
:::

```md
:::stats
items:
  - value: 5
    label: 图表块
  - value: 4
    label: 健康块
  - value: 11
    label: 通用结构块
  - value: 2
    label: 内置主题
:::
```

### kpi-row · KPI 行

带说明的指标卡行，note 作为副说明。

:::kpi-row
title: 引擎输出特性
items:
  - label: 输出格式
    value: 单文件 HTML
    note: CSS 内联，零外部依赖
  - label: 图表渲染
    value: SVG
    note: 随主题令牌重着色
  - label: 打印
    value: 内置
    note: @media print 自动处理
:::

```md
:::kpi-row
title: 引擎输出特性
items:
  - label: 输出格式
    value: 单文件 HTML
    note: CSS 内联，零外部依赖
  - label: 图表渲染
    value: SVG
    note: 随主题令牌重着色
  - label: 打印
    value: 内置
    note: @media print 自动处理
:::
```

### feature-grid · 特性网格

`columns` 设为 2、3 或 4 控制列数。

:::feature-grid
columns: 3
items:
  - title: Markdown DSL
    desc: frontmatter 声明元数据，正文混排散文与结构化块。
  - title: 主题令牌
    desc: 所有视觉属性集中在 --mp-* 变量，切换主题即重着色。
  - title: 打印安全
    desc: 样式内置 @media print，屏幕与纸张表现一致。
:::

```md
:::feature-grid
columns: 3
items:
  - title: Markdown DSL
    desc: frontmatter 声明元数据，正文混排散文与结构化块。
  - title: 主题令牌
    desc: 所有视觉属性集中在 --mp-* 变量，切换主题即重着色。
  - title: 打印安全
    desc: 样式内置 @media print，屏幕与纸张表现一致。
:::
```

### card-grid · 卡片网格

用于列举文档样板或并列条目。

:::card-grid
title: 常见文档样板
cards:
  - title: 方案 / 执行摘要
    desc: 摘要 → 背景 → 证据 → 建议
  - title: 研报 / 估值
    desc: KPI + K 线 + 风险矩阵
  - title: 数据报告
    desc: KPI 大数字 + 趋势图
:::

```md
:::card-grid
title: 常见文档样板
cards:
  - title: 方案 / 执行摘要
    desc: 摘要 → 背景 → 证据 → 建议
  - title: 研报 / 估值
    desc: KPI + K 线 + 风险矩阵
  - title: 数据报告
    desc: KPI 大数字 + 趋势图
:::
```

### comparison · 对比

左右双栏对比，适合「之前 / 之后」或两种方案对照。

:::comparison
title: DSL 与手写 HTML 对照
left:
  title: 手写 HTML
  items:
    - 排版决策反复，风格难一致
    - 打印需单独调整
    - AI 生成时格式不稳定
right:
  title: Momo Paper DSL
  items:
    - 主题令牌统一管控视觉
    - 内置 @media print 规则
    - 结构化块输出稳定可控
:::

```md
:::comparison
title: DSL 与手写 HTML 对照
left:
  title: 手写 HTML
  items:
    - 排版决策反复，风格难一致
    - 打印需单独调整
    - AI 生成时格式不稳定
right:
  title: Momo Paper DSL
  items:
    - 主题令牌统一管控视觉
    - 内置 @media print 规则
    - 结构化块输出稳定可控
:::
```

### three-columns · 三栏

三栏并列内容，每栏含 title 与 body。

:::three-columns
title: 从声明到成品
columns:
  - title: 声明
    body: frontmatter + :::block 描述结构
  - title: 渲染
    body: 引擎解析并生成 HTML
  - title: 输出
    body: 单文件，屏幕与打印一致
:::

```md
:::three-columns
title: 从声明到成品
columns:
  - title: 声明
    body: frontmatter + :::block 描述结构
  - title: 渲染
    body: 引擎解析并生成 HTML
  - title: 输出
    body: 单文件，屏幕与打印一致
:::
```

### callout · 提示框

`tone` 区分提示类型，配图标与文字，不单靠颜色传达状态。

:::callout
tone: insight
title: 关于 document_type
body: 正式 document_type 会选择对应 Schema，并校验允许的 block 与字段；未注册类型进入 free mode，任意合法 block 仍可通用渲染。
:::

```md
:::callout
tone: insight
title: 关于 document_type
body: 正式 document_type 会选择对应 Schema，并校验允许的 block 与字段；未注册类型进入 free mode，任意合法 block 仍可通用渲染。
:::
```

### cta · 行动召唤

带标题、正文与单按钮的收尾区块。

:::cta
title: 查看图表块
body: 5 种 echarts 图表块的完整演示与 DSL 源码见图表演示页。
button:
  label: 打开图表演示
  href: /charts/
:::

```md
:::cta
title: 查看图表块
body: 5 种 echarts 图表块的完整演示与 DSL 源码见图表演示页。
button:
  label: 打开图表演示
  href: /charts/
:::
```

### faq · 问答组

分组问答，问题加粗、回答次级文字。

:::faq
items:
  - question: 引擎依赖外部库吗？
    answer: 解析与渲染零依赖。仅图表块按需加载 echarts，代码块按需加载 highlight.js，加载失败均优雅降级。
  - question: 可以自定义组件吗？
    answer: 可以。任意 :::tag-name 都会渲染为带 data-block 的区块，在主题 CSS 中按选择器添加样式即得新组件，无需改动引擎。
:::

```md
:::faq
items:
  - question: 引擎依赖外部库吗？
    answer: 解析与渲染零依赖。仅图表块按需加载 echarts，代码块按需加载 highlight.js，加载失败均优雅降级。
  - question: 可以自定义组件吗？
    answer: 可以。任意 :::tag-name 都会渲染为带 data-block 的区块，在主题 CSS 中按选择器添加样式即得新组件，无需改动引擎。
:::
```

### footer-note · 脚注

页面底部的补充说明。

:::footer-note
title: 关于本目录
body: 本页展示的组件由 momo-paper.css 与 vercel.css 两套主题共同样式化，切换右上角主题即可观察同一 DSL 在两套令牌下的呈现差异。
:::

```md
:::footer-note
title: 关于本目录
body: 本页展示的组件由 momo-paper.css 与 vercel.css 两套主题共同样式化，切换右上角主题即可观察同一 DSL 在两套令牌下的呈现差异。
:::
```

## nav · 文档导航

`nav` 是引擎特化块，渲染为带品牌、链接与 CTA 的文档内导航（区别于本站顶部站点导航）。

:::nav
brand: Momo Paper
items:
  - label: 使用指南
    href: /guide/
  - label: 示例画廊
    href: /demo/
cta:
  label: 查看图表
  href: /charts/
:::

```md
:::nav
brand: Momo Paper
items:
  - label: 使用指南
    href: /guide/
  - label: 示例画廊
    href: /demo/
cta:
  label: 查看图表
  href: /charts/
:::
```

## 健康块

4 种引擎特化块，用于健康追踪与报告场景。字段由引擎直接解析为结构化 HTML。

### weekly-summary · 周报摘要

:::weekly-summary
title: 第 24 周回顾
period: 2026-06-15 至 2026-06-21
summary: 本周运动与睡眠达标，饮食需控制糖分摄入。
positives:
  - title: 运动达标
    desc: 跑步 3 次，累计 18 公里
  - title: 睡眠稳定
    desc: 日均 7.5 小时
improvements:
  - title: 糖分超标
    desc: 甜品摄入 4 次，需减半
:::

```md
:::weekly-summary
title: 第 24 周回顾
period: 2026-06-15 至 2026-06-21
summary: 本周运动与睡眠达标，饮食需控制糖分摄入。
positives:
  - title: 运动达标
    desc: 跑步 3 次，累计 18 公里
  - title: 睡眠稳定
    desc: 日均 7.5 小时
improvements:
  - title: 糖分超标
    desc: 甜品摄入 4 次，需减半
:::
```

### goal-tracker · 目标进度

:::goal-tracker
title: 月度目标
goals:
  - title: 跑步里程
    target: 80
    current: 52
    unit: 公里
    desc: 进度正常
  - title: 体重
    target: 70
    current: 72
    unit: 公斤
    desc: 接近目标
:::

```md
:::goal-tracker
title: 月度目标
goals:
  - title: 跑步里程
    target: 80
    current: 52
    unit: 公里
    desc: 进度正常
  - title: 体重
    target: 70
    current: 72
    unit: 公斤
    desc: 接近目标
:::
```

### metrics-panel · 指标面板

:::metrics-panel
title: 健康指标
metrics:
  - label: 静息心率
    value: 62
    change: 比上周 -2
    status: good
  - label: 体脂率
    value: 22%
    change: 比上周 +0.5
    status: warning
  - label: 血压
    value: 138
    change: 偏高
    status: danger
:::

```md
:::metrics-panel
title: 健康指标
metrics:
  - label: 静息心率
    value: 62
    change: 比上周 -2
    status: good
  - label: 体脂率
    value: 22%
    change: 比上周 +0.5
    status: warning
  - label: 血压
    value: 138
    change: 偏高
    status: danger
:::
```

### report-header · 报告页头

不含 `score` 时为常规页头；含 `score` 时切换为评分卡布局。

:::report-header
title: 6 月健康报告
eyebrow: 月度评估
date_range: 2026-06
weigh_day: 每周一
meta:
  - label: 评估周期
    value: 4 周
  - label: 数据来源
    value: 智能秤 + 手环
:::

```md
:::report-header
title: 6 月健康报告
eyebrow: 月度评估
date_range: 2026-06
weigh_day: 每周一
meta:
  - label: 评估周期
    value: 4 周
  - label: 数据来源
    value: 智能秤 + 手环
:::
```

含评分的变体：

:::report-header
title: 综合健康评估
eyebrow: 月度报告
date_range: 2026-06
status: 良好
score: 82
score_label: 综合评分
score_max: 100
meta:
  - label: 对比上月
    value: +6
:::

```md
:::report-header
title: 综合健康评估
eyebrow: 月度报告
date_range: 2026-06
status: 良好
score: 82
score_label: 综合评分
score_max: 100
meta:
  - label: 对比上月
    value: +6
:::
```

## 图表块

5 种 echarts 图表块由引擎特化渲染，颜色随主题 `--chart-*` 变量自动适配：`bar-chart`（类别对比）、`line-chart`（时间序列）、`donut-chart`（构成分解）、`candlestick-chart`（OHLC 价格）、`waterfall-chart`（数值分解）。

完整演示与 DSL 源码见[图表演示](/charts/)页。以下是一个柱状图示例：

:::bar-chart
title: 各地区营收（M）
unit: M
items:
  - label: 华北
    value: 120
  - label: 华东
    value: 310
  - label: 华南
    value: 240
  - label: 华西
    value: 95
:::

```md
:::bar-chart
title: 各地区营收（M）
unit: M
items:
  - label: 华北
    value: 120
  - label: 华东
    value: 310
  - label: 华南
    value: 240
  - label: 华西
    value: 95
:::
```

:::cta
title: 开始写你的第一份文档
body: 三种工作流任选其一：Claude Code Skill 自动渲染、CLI 手动控制、或直接编辑 HTML 模板。输出共享同一套设计令牌。
button:
  label: 查看使用指南
  href: /guide/
:::
