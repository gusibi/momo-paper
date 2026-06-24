---
document_type: slides
locale: zh-CN
title: Momo Paper · 产品演示
description: 用 :::slide 的多种 layout 组织的演示文稿，展示图文混排、分栏、大数字、引用等排版。
---

:::hero
eyebrow: 产品演示 · 2026
title: 让 Agent 生成稳定的文档
subtitle: 内容用 DSL 表达，样式交给主题——一份内容，到处可渲染。
:::

:::slide
layout: agenda
eyebrow: 目录
title: 我们会聊什么
points:
  - 直接生成 HTML 的困境
  - DSL 的核心思路
  - 一份内容，多套主题
  - 数据说话
  - 适用场景与边界
:::

:::slide
layout: split-left
eyebrow: 问题
figure: 同一种卡片，三次生成三种样子
content:
  title: 直接生成 HTML 会塌方
  points:
    - 样式漂移：圆角、间距、配色每次都不一样
    - 结构失控：标题跳级、div 当按钮
    - 无法校验：纯 HTML 难判断是否合法
:::

:::slide
layout: split-right
eyebrow: 思路
figure: 内容与样式，从此各管各的
content:
  title: 把"说什么"和"长什么样"拆开
  points:
    - 模型只产出内容与结构（Markdown + 块）
    - 解析器转成稳定的 HTML 区块
    - 主题 CSS 决定最终像素
:::

:::slide
layout: statement
eyebrow: 一句话
title: 生成结构，而不是像素。
:::

:::slide
layout: metric
eyebrow: 数据说话
title: 一套源文件能做到
metrics:
  - value: 1 份
    label: Markdown DSL 源文件
  - value: 2 套
    label: 开箱即用主题（明 / 暗）
  - value: 49+
    label: 可复用结构化块
  - value: 0
    label: 内联样式
:::

:::slide
layout: two-col
eyebrow: 对比
title: 该用哪一种
col_a:
  title: 用 Markdown
  items:
    - 文章、博客、说明文档
    - 标题、段落、列表、引用
    - 代码块、表格、图片
col_b:
  title: 用结构化块
  items:
    - 数据卡片与图表
    - 对比、定价、报告头
    - 需要像素级稳定的版式
:::

:::slide
layout: quote
eyebrow: 用户说
quote: 我们终于不用再为模型生成的 HTML 做收尾了。
source: 某 AI 文档平台 · 工程负责人
:::

:::slide
layout: full-image
eyebrow: 一图看懂
title: 从 DSL 到 HTML
figure: DSL → 解析 → 校验 → 主题渲染 → 独立 HTML
caption: 模型只碰最左边一段，右边全部由固定流程保证。
:::

:::hero
eyebrow: 结论
title: 内容与样式解耦，质量才稳得住
subtitle: 一份 Markdown DSL，到处可渲染。
:::

:::footer
brand: Momo Paper
links:
  - label: 文档
    href: "#"
  - label: GitHub
    href: "#"
:::
