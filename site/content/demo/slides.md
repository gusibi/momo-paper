---
document_type: slides
locale: zh-CN
title: Momo Paper 项目路演
description: slides 类型用 :::slide 的多种 layout 组织演示文稿，16:9 视口。
---

:::hero
eyebrow: 开源项目 · 2026
title: Momo Paper 项目路演
subtitle: 面向文档与视觉叙事的 Markdown DSL 文档引擎
:::

:::slide
layout: agenda
eyebrow: 我们解决什么问题
title: AI 时代文档生成缺乏视觉一致性和设计约束
points:
  - AI agent 生成的 HTML 排版混乱，没有设计规范
  - 手工写 HTML/CSS 效率低，无法批量产出
  - 现有文档工具（Word/Notion）不易与 AI 工作流集成
  - 打印输出通常需要额外处理，样式严重退化
:::

:::slide
eyebrow: 核心方案
title: 设计令牌 + 结构化块 + DSL 引擎 = 一致的设计语言
points:
  - 15 份文档样板，覆盖商业、学术、个人全场景
  - 设计令牌（颜色/字体/间距）集中管理，自动注入
  - 块字段约定确保数据结构一致
  - 内置 @media print 规则，屏幕和纸张表现一致
:::

:::slide
layout: split-left
eyebrow: 两种工作流
figure: 手动编辑 HTML 模板 vs DSL 驱动渲染
content:
  title: 适配不同场景
  points:
    - 直接 HTML 模板：打开 → 编辑内容 → 浏览器预览，零学习成本
    - DSL 渲染引擎：写 Markdown DSL → CLI 渲染 → HTML 输出
    - 适合 AI agent 批量生成、API 驱动的文档工作流
:::

:::slide
eyebrow: 技术架构
title: Python CLI + 解析器 + 主题 CSS
points:
  - 纯 Python 实现，pip install -e . 一行安装
  - 解析器把 Markdown DSL 转成稳定的 HTML 区块
  - 5 种可编程图表（bar/line/donut/candlestick/waterfall）
  - 可作为 MCP 工具被 AI agent 直接调用
:::

:::slide
layout: metric
eyebrow: 数据一览
title: 从零到可用的完整项目
metrics:
  - value: 15
    label: 文档样板
  - value: 5
    label: 图表块
  - value: 2
    label: 可切换主题
:::

:::slide
layout: closing
eyebrow: 下一步
title: 开源社区 + 更多样板 + 在线 playground
points:
  - GitHub 开源：github.com/gusibi/momo-paper
  - 规划中的样板：dashboard、comparison matrix、topic cover
  - 在线 playground：浏览器内编辑实时预览
  - 欢迎贡献新的文档样板与结构化块
:::
