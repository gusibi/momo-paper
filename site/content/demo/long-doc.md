---
document_type: long_doc
locale: zh-CN
title: 白皮书 / 长文示例
description: Long Document 类型展示多章节长文、引用块和结论结构。
---

## 摘要

本示例展示 long_doc 类型的核心特性：摘要、无限可迭代的章节（每章含标题、正文和可选的引用块）、以及带下一步行动的结论。此类型适合技术白皮书、深度分析报告和长篇文档。

- 章节数量不限，每章独立渲染
- 内置引用块样式（左边框 + 品牌色）
- 结论包含 checklist 式的下一步行动

## 设计令牌系统

Momo Paper 的设计令牌定义在样式表的 `:root` 块中，包括颜色（`--mp-ink`、`--mp-brand`、`--mp-accent` 等）、字体（serif/sans/mono 三套）、间距和圆角。所有组件通过这些变量取色，自动获得统一的视觉语言。

这种设计的核心优势是：一次定义，全局生效。修改 `--mp-brand` 的值，所有组件的品牌色都会同步更新。

> 设计令牌是视觉一致性的唯一真相源。
> — Momo Paper 设计原则

## document_type 语义

`document_type` 是 frontmatter 中的语义标签，出现在页头并引导 Skill 选择模板；引擎本身是通用渲染器，不按类型做结构校验。内容与排版由此彻底解耦——同一套结构化块在所有类型中通用。

如果需要自定义视觉，可以通过 `--css` 参数指定不同的主题样式表，markup 完全不变即可重新着色。

## 块约定

每种结构化块都有明确的字段约定，定义了键值与用法。约定确保输入数据的一致性，让 AI agent 生成的 DSL 在渲染前即可被检查。约定由块本身定义，与 document_type 无关。

## 结论

long_doc 是 Momo Paper 中通用性最强的类型之一。它的可迭代章节结构让它适应各种长度的内容——从 3 节的简短报告到 20 节的详细白皮书。

:::recommendation
title: 下一步
actions:
  - title: 生成骨架
    desc: 用 frontmatter + Markdown 章节快速搭建结构
  - title: 填充内容
    desc: 为每个章节添加标题和正文
  - title: 高亮观点
    desc: 用引用块（> 开头）来高亮重要观点
:::
