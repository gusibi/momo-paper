---
document_type: deep-research
locale: zh-CN
title: Agent 原生文档编译器深度研究
description: 研究结构化文档中间层在 Agent 工作流中的价值、边界与验证方法。
author: Momo Paper Research
---

:::research-header
topic: Agent 原生文档编译器
scope: 结构化 DSL、Schema 校验、HTML/PDF 渲染与 Skill 集成
period: 2026 Q3
status: draft
:::

:::research-question
question: Agent 的正式文档输出是否应该经过可验证的中间表示，而不是直接生成最终 HTML？
scope: 关注 token 成本、输出稳定性、品牌一致性和可维护性。
:::

:::executive-summary
summary: 文档 DSL 可以把内容生成与视觉实现分离，使 Agent 输出更紧凑，并让 Schema、主题和渲染器成为可重复使用的基础设施。
citations:
  - compiler-contract
:::

:::key-findings
title: 核心发现
items:
  - title: DSL 的核心价值是可治理而非单纯压缩
    body: Token 节省适合传播，但长期价值来自契约校验、品牌一致和可复现构建。
    confidence: high
    citations:
      - compiler-contract
  - title: 严格校验与宽松渲染应该分离
    body: validate 负责暴露未知字段和结构错误，render 则必须避免丢失合法解析出来的内容。
    confidence: high
    citations:
      - validation-contract
:::

:::evidence
title: 工程证据
items:
  - claim: 通用 renderer 已经能够保留未知 block
    body: 每个合法 tag 都会渲染为带 data-block 属性的 section。
    citations:
      - renderer-source
:::

:::counterarguments
title: 反方观点
items:
  - title: 模型直接生成 HTML 的能力持续提高
    body: 如果只强调生成能力，DSL 的优势会下降；因此产品必须强化验证与治理。
:::

:::methodology
summary: 结合代码能力审计、固定质量门槛的 A/B benchmark 和真实用户任务验证产品假设。
methods:
  - 审计 parser、validator、renderer 和 Skill 的职责边界
  - 对比 direct HTML 与 DSL 的 API 输出 token
  - 盲评最终 HTML/PDF 的完整性与可读性
sample: research summary、deep research 和 landing page 三种旗舰任务。
:::

:::limitations
items:
  - 当前尚未完成足够规模的公开 A/B 数据。
  - PDF 分页与完全离线资源打包仍需要后续工程验证。
:::

:::recommendations
title: 建议
items:
  - title: 优先完成 Schema 纵向链路
    body: 先证明 Agent 能发现契约、修复错误并稳定渲染。
  - title: 用三个旗舰模板建立质量基线
    body: 深度研究、研究摘要和 Landing Page 足以覆盖正式报告与视觉发布。
:::

:::sources
title: 来源
items:
  - id: compiler-contract
    title: Agent-native Document Compiler Product Contract
    url: README.md
    publisher: Momo Paper
  - id: validation-contract
    title: Machine Schema and Validation Runtime
    url: momo_dsl/schema.py
    publisher: Momo Paper
  - id: renderer-source
    title: Generic HTML Renderer
    url: momo_dsl/renderer.py
    publisher: Momo Paper
:::
