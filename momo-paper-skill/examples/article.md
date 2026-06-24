---
document_type: long_doc
locale: zh-CN
title: Momo Paper 使用指南：用 Markdown DSL 生成稳定文档
description: 一篇完整的上手教程，演示标准 Markdown 的全部排版能力——标题、列表、引用、代码、表格、图片与混排结构化块。
author: Momo Paper 团队
date: 2026-06-24
---

Momo Paper 是一个**文档优先**的生成系统。它的核心主张只有一句话：让模型生成*结构*，而不是像素。这篇指南本身就是一篇普通文章，正文全部用标准 Markdown 写成，顺带演示 `long_doc` / `article` 这类以阅读为主的排版长什么样。

读完你会知道：怎么写 frontmatter、怎么混排结构化块、以及 Markdown 到底支持哪些写法。

## 一分钟上手

最小的一篇文档只需要三步：

1. 写 frontmatter，声明 `document_type`、`locale`、`title`。
2. 用 Markdown 写正文，用 `:::块名` 写结构化内容。
3. 用命令行渲染成独立 HTML。

```bash
# 渲染为默认主题（Momo Paper）
python3 -m momo_dsl.cli render article.md -o article.html

# 换成 Vercel Geist 主题，内容一个字都不用改
python3 -m momo_dsl.cli render article.md -o article.html \
  --css momo_dsl/styles/vercel.css
```

> 同一份 DSL，换一个 `--css` 就能整体换肤。内容与样式彻底解耦，这是整个系统最值钱的部分。

## 文档结构

每篇文档都以 frontmatter 开头，三个必填字段，其余可选：

```yaml
---
document_type: long_doc   # 必填：路由与文档类型
locale: zh-CN             # 必填：语言
title: 我的文章           # 必填：页面唯一的 <h1>
description: 一句话摘要   # 可选
author: 你的名字          # 可选
date: 2026-06-24          # 可选
---
```

frontmatter 之后就是正文，可以自由混排 Markdown 段落和结构化块。

## Markdown 支持的全部写法

下面把渲染器支持的样式逐一演示一遍。

### 行内样式

正文里可以用 **加粗**、*斜体*、`行内代码`，以及[行内链接](https://github.com)。这些可以组合，例如 **加粗里的 `代码`** 也能正常工作。

### 列表

无序列表适合并列要点：

- 策略优先的权限控制
- 隔离的运行时环境
- 可预测的渲染输出

有序列表适合步骤或排名：

1. 解析 frontmatter 与正文
2. 校验块语法，出错即报（带行号）
3. 渲染为稳定的 HTML 区块

### 引用

引用块用来强调观点或引述他人，支持多段：

> 模型擅长决定*说什么*，不擅长稳定地决定*长什么样*。
>
> 把这两件事拆开，质量才稳得住。

### 代码块

围栏代码块会原样保留、不做行内解析，并标注语言。注意：**代码块里写 `:::块名` 也不会被当成真实的块**，所以可以放心地用它来演示 DSL 语法：

```markdown
:::feature-grid
columns: 3
items:
  - title: 策略优先
    desc: 哪些工具自动执行，哪些需要审批。
  - title: 隔离运行时
    desc: 在受控环境里执行操作。
:::
```

也可以展示 JSON、YAML、Shell 等任意语言：

```json
{
  "document_type": "long_doc",
  "blocks": ["hero", "feature-grid", "table"]
}
```

### 表格

标准 GFM 表格用来对比和罗列。下面是常用块类型的速查：

| 类别 | 代表块 | 用途 |
| --- | --- | --- |
| 内容 | `section` `callout` `quote` | 正文、提示、引述 |
| 数据 | `kpi-row` `table` `bar-chart` | 指标、表格、图表 |
| 金融 | `thesis-panel` `valuation-table` | 投资结论与估值 |
| 演示 | `hero` `slide` | 封面与幻灯片 |

### 分隔线与图片

用三个连字符可以插入一条分隔线：

---

图片用标准语法 `![描述](地址)`，渲染时自动响应式、带圆角边框：

![DSL 经解析器转为独立 HTML 的流程示意](data:image/svg+xml,%3Csvg%20xmlns%3D%27http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%27%20viewBox%3D%270%200%20960%20340%27%3E%3Crect%20width%3D%27960%27%20height%3D%27340%27%20fill%3D%27%23F2EFE8%27%2F%3E%3Cg%20font-family%3D%27Inter%2Csans-serif%27%20text-anchor%3D%27middle%27%3E%3Crect%20x%3D%2770%27%20y%3D%27120%27%20width%3D%27220%27%20height%3D%27100%27%20rx%3D%2714%27%20fill%3D%27%23244C7A%27%2F%3E%3Ctext%20x%3D%27180%27%20y%3D%27176%27%20fill%3D%27%23FFFFFF%27%20font-size%3D%2730%27%20font-weight%3D%27700%27%3EMarkdown%20DSL%3C%2Ftext%3E%3Ctext%20x%3D%27330%27%20y%3D%27182%27%20fill%3D%27%234C566A%27%20font-size%3D%2746%27%3E%26%238594%3B%3C%2Ftext%3E%3Crect%20x%3D%27370%27%20y%3D%27120%27%20width%3D%27220%27%20height%3D%27100%27%20rx%3D%2714%27%20fill%3D%27%23DCE7F2%27%2F%3E%3Ctext%20x%3D%27480%27%20y%3D%27176%27%20fill%3D%27%23244C7A%27%20font-size%3D%2730%27%20font-weight%3D%27700%27%3EParser%3C%2Ftext%3E%3Ctext%20x%3D%27630%27%20y%3D%27182%27%20fill%3D%27%234C566A%27%20font-size%3D%2746%27%3E%26%238594%3B%3C%2Ftext%3E%3Crect%20x%3D%27670%27%20y%3D%27120%27%20width%3D%27220%27%20height%3D%27100%27%20rx%3D%2714%27%20fill%3D%27%23B65C3A%27%2F%3E%3Ctext%20x%3D%27780%27%20y%3D%27176%27%20fill%3D%27%23FFFFFF%27%20font-size%3D%2730%27%20font-weight%3D%27700%27%3EHTML%3C%2Ftext%3E%3Ctext%20x%3D%27480%27%20y%3D%27285%27%20fill%3D%27%234C566A%27%20font-size%3D%2722%27%3Econtent%20in%2C%20stable%20HTML%20out%3C%2Ftext%3E%3C%2Fg%3E%3C%2Fsvg%3E)

## 在文章里混排结构化块

纯阅读内容用 Markdown 就够了；需要稳定版式的地方，直接插入结构化块。两者可以在同一篇文档里自由穿插，例如下面这个提示框：

:::callout
tone: 提示
title: 什么时候用块，什么时候用 Markdown
body: 连续阅读的内容（本文这样的）用 Markdown；数据卡片、图表、对比、报告头这类需要像素级稳定的版式，用结构化块。
:::

## 小结

- 让模型生成 **DSL**，而不是 HTML。
- 用固定主题承载样式，内容与样式解耦。
- 长文用 Markdown，复杂版式用结构化块。
- 一份内容，多套主题，随时换肤。

:::footer-note
title: 关于本文
body: 本文用于演示 Momo Paper 的标准 Markdown 排版（article / long_doc），覆盖标题、行内样式、有序与无序列表、引用、代码块、表格、分隔线、图片，以及与结构化块的混排。所有样式均来自主题 CSS，正文未写入任何内联样式。
:::
