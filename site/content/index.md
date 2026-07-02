---
document_type: landing
locale: zh-CN
title: Momo Paper — 给 AI Agent 用的省 token 文档引擎
description: 给 AI Agent 用的省 token 文档引擎。Agent 写简洁 Markdown DSL，Momo Paper 渲染为排版精良的单文件 HTML——比手写 HTML/CSS 省 token、样式稳定、可校验。通过 Skill 自动使用。
show_header: false
---

:::hero
eyebrow: AI Agent 文档生成 · 2.1
title: 给 AI Agent 用的省 token 文档生成
subtitle: 让 Agent 只写简洁 Markdown DSL，Momo Paper 渲染为排版精良的单文件 HTML。比让 Agent 手写 HTML/CSS 省 token、样式稳定、可校验——别再让 Agent 从零拼 HTML。
primary_cta:
  label: 查看使用指南
  href: /guide/
secondary_cta:
  label: 浏览组件目录
  href: /components/
:::

:::comparison
title: 为什么不让 Agent 直接写 HTML
left:
  title: Agent 手写 HTML/CSS
  items:
    - token 占用大，CSS 反复重复输出
    - 样式随 prompt 漂移，每次结果不一致
    - 修改成本高，改一处往往要重写一段
    - 无法校验，出错只能人工排查
right:
  title: Agent 写 Momo DSL
  items:
    - 紧凑的结构化块，token 更省
    - 渲染器补全 HTML/CSS，样式始终稳定
    - 改字段即改文档，修改成本低
    - momo2 validate 校验语法与元数据
:::

## 引擎实际提供什么

Momo Paper 的能力分三层。每一层都可独立使用，组合后覆盖从商业方案到数据报告的常见文档场景。

:::feature-grid
columns: 3
items:
  - title: Markdown 渲染
    desc: 标题、列表、引用、表格、代码块与行内标记的 CommonMark 子集，含 highlight.js 语法高亮。
  - title: 5 种图表块
    desc: bar / line / donut / candlestick / waterfall，声明 :::chart 块即渲染为 echarts 交互图，颜色随主题令牌自适应。
  - title: 4 种健康块
    desc: weekly-summary、goal-tracker、metrics-panel、report-header，字段直接解析为结构化报告组件。
  - title: 通用结构块
    desc: hero、stats、feature-grid、card-grid、comparison、callout、faq 等，由主题 CSS 按标签名样式化。
  - title: 双主题令牌
    desc: Momo Paper 暖调与 Vercel 极简两套主题，共享 --mp-* 变量名，切换 <link> 即整体重着色。
  - title: 打印安全
    desc: 所有样式内置 @media print 规则，自动处理背景、边距与分页，无需为打印单独准备文档。
:::

## 用 Skill 使用

Skill 自动选择文档样板、构造 DSL、调用引擎渲染并预览。Agent 只需描述想要的文档，Skill 负责校验、渲染、落地——无需手动跑命令，也无需编辑 HTML。

- 自然语言驱动，自动构造 DSL
- 自动选择样板与组件
- 校验通过后渲染单文件 HTML

:::stats
items:
  - value: 5
    label: 图表块
  - value: 4
    label: 健康块
  - value: 2
    label: 内置主题
:::

## 探索更多

- [组件目录](/components/) — 全部组件的渲染效果与 DSL 源码
- [图表演示](/charts/) — 5 种图表块的交互示例
- [示例画廊](/demo/) — 15 份样板的结构说明与完整渲染示例
- [设计系统](/design/) — 色彩、字体、间距令牌与设计哲学

:::cta
title: 让 Agent 三分钟产出第一份文档
body: 告诉 Agent 想要什么文档，Skill 自动生成 Markdown DSL 并渲染为 HTML——打开浏览器即可看到排版精良、打印就绪的成品。
button:
  label: 查看使用指南
  href: /guide/
:::
