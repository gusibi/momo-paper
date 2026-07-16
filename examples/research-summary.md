---
document_type: research-summary
locale: zh-CN
title: Agent 文档生成研究摘要
description: 比较 Agent 直接生成 HTML 与生成结构化 DSL 的工程差异。
---

:::research-question
question: 在内容质量相同的前提下，结构化 DSL 是否能减少 Agent 输出 token 并提高文档生成稳定性？
scope: 比较单文件 HTML 与 Momo Paper DSL 的生成、校验和渲染流程。
:::

:::key-findings
title: 关键发现
items:
  - title: DSL 将重复视觉实现移出模型输出
    body: Agent 只需要描述内容结构，主题和布局由固定渲染器补全。
    citations:
      - benchmark-protocol
  - title: 结构化校验缩短修复路径
    body: validate 可以返回字段、block 与行号，Agent 无需重新检查整份 HTML。
    citations:
      - validation-design
:::

:::implications
title: 对 Agent 工作流的影响
items:
  - title: 更适合作为工具输出协议
    body: DSL 可以保存、版本控制并重复渲染。
  - title: 模板需要成为正式契约
    body: 每种旗舰文档应定义必需章节、允许字段和引用规则。
:::

:::methodology
summary: 使用固定模型、相同任务和相同质量门槛，对 direct HTML 与 Momo DSL 进行重复 A/B 测试。
methods:
  - 记录模型 API 的实际输出 token
  - 检查内容完整性与浏览器渲染结果
  - 统计首次校验通过率和修复轮数
sample: 三种文档任务，每组至少重复五次。
:::

:::limitations
items:
  - 当前示例只定义实验方法，不包含尚未执行的结果。
  - 文件 tokenizer 只能作为辅助指标，不能替代 API usage。
:::

:::sources
title: 来源
items:
  - id: benchmark-protocol
    title: Momo Paper Benchmark Protocol
    url: docs/benchmark-protocol.md
    publisher: Momo Paper
  - id: validation-design
    title: Momo Paper Schema Validation Design
    url: momo_dsl/schema.py
    publisher: Momo Paper
:::
