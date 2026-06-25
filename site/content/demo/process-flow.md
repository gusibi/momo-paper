---
document_type: process_flow
locale: zh-CN
title: Momo Paper 文档生成工作流
description: 从用户需求到渲染输出，完整的文档生成 SOP。
---

本文档描述 Momo Paper 引擎处理文档生成的完整流程，涵盖输入校验、模板选择、渲染执行和输出验证四个阶段。此流程适用于 CLI 模式和 MCP 工具模式。

:::steps
title: 处理流程
items:
  - step: 1
    title: 接收输入
    desc: CLI 从文件路径或 stdin 读取 DSL；MCP 从 tool call 参数中接收文档内容。
  - step: 2
    title: 解析与校验
    desc: 解析 frontmatter 与块结构，检查必填字段（document_type/locale/title）。校验通过后提取 document_type。
  - step: 3
    title: 路由与样式选择
    desc: 根据 document_type 决定文档语义，根据 --css 参数选择主题样式表（默认 momo-paper.css）。
  - step: 4
    title: 块渲染
    desc: 将每个 :::block 转换为带 data-block 属性的 HTML 区块，chart 块渲染为交互式图表配置。
  - step: 5
    title: HTML 输出
    desc: 渲染后的 HTML 写入目标文件或 stdout，包含完整的内联/外链 CSS 和图表运行时。
  - step: 6
    title: 验证（可选）
    desc: 可通过测试套件验证输出 HTML 的结构完整性、CSS 变量完整性和打印样式正确性。
:::

## 条件分支

系统在以下节点支持条件分支：

- document_type 为 slides 时，按幻灯片语义组织 :::slide 块
- 指定 --css 参数时，使用显式主题而非默认主题
- 输入为 '-' 时，从 stdin 而非文件读取
- 图表渲染仅在 chart 块存在且类型为 5 种支持类型之一时执行

## 设计原则

整个流程的核心设计原则是关注点分离：DSL 负责内容，块约定负责结构，设计令牌负责视觉一致性，图表模块负责数据可视化。这四个层次各司其职，互不侵入。

:::callout
tone: insight
title: 上线检查清单
body: DSL 输入是否包含所有必填字段？document_type 是否为 15 种支持类型之一？图表数据格式是否符合对应类型要求？输出 HTML 是否在目标浏览器中正确渲染？打印样式是否正常（@media print）？
:::
