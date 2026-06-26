---
document_type: infographic
locale: zh-CN
title: Momo Paper 2026 引擎能力一览
description: 一份信息图概览：文档样板、图表能力、设计令牌和生态集成。
---

Momo Paper 是一个面向文档与视觉叙事的 Markdown DSL 文档引擎。以下是一份信息图概览，用可视化的方式展示了引擎的核心能力。

:::stats
items:
  - value: 15
    label: 文档样板
  - value: 5
    label: 图表块
  - value: 4
    label: 健康块
  - value: 2
    label: 可切换视觉主题
:::

## 核心处理链路

从用户输入到渲染输出，Momo Paper 的完整处理链路：

:::steps
title: 处理链路
items:
  - step: 1
    title: 提供内容
    desc: 用户提供 Markdown DSL（手动编写或 AI agent 生成）
  - step: 2
    title: 校验
    desc: 引擎校验 frontmatter 与块结构
  - step: 3
    title: 标注语义
    desc: document_type 标注文档语义，引导 Skill 选模板
  - step: 4
    title: 渲染
    desc: 块约定 + 设计令牌 = HTML 输出
  - step: 5
    title: 图表
    desc: chart 块渲染为交互式图表
  - step: 6
    title: 输出
    desc: 可在浏览器中查看、打印或分享
:::

## 文档样板使用分布（社区调研）

:::donut-chart
title: 文档样板使用分布
center_value: 100%
center_label: 社区调研
segments:
  - label: 方案 / one_pager
    value: 28
  - label: 研报 / equity
    value: 22
  - label: 简历 / resume
    value: 18
  - label: 长文 / long_doc
    value: 15
  - label: 信息图 / infographic
    value: 10
  - label: 其他 10 种
    value: 7
:::

:::callout
tone: insight
title: 核心价值主张
body: Momo Paper 让文档排版从「手工调 CSS」升级为「声明式 DSL」。你的内容 + 我们的设计令牌 = 永远排版精良、打印就绪的文档。整个系统的设计哲学是「约束即解放」——通过预定义的样板和设计令牌，消除排版决策的认知负担，让用户（和 AI agent）专注于内容本身。
:::
