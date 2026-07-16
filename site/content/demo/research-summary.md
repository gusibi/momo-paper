---
document_type: research-summary
locale: zh-CN
title: Agent 文档生成方案研究摘要
description: 使用正式 research-summary Schema 展示研究问题、关键发现、影响、方法、限制与可追溯来源。
---

:::callout
tone: insight
title: 正式模板说明
body: 本页通过 research-summary Schema 严格校验。站点构建会检查必需章节、字段类型、block 顺序和 citation 引用关系，失败时不会覆盖上一版站点输出。
:::

:::research-question
question: 当 AI Agent 需要生成可交付的正式文档时，为什么应该先输出结构化 DSL，再由文档编译器生成 HTML 或 PDF？
scope: 关注输出 token、结构可验证性、视觉一致性、修改成本和跨 Agent 复用。
:::

:::key-findings
title: 关键发现
items:
  - title: Agent 输出应当被编译，而不是直接成为最终页面
    body: HTML 是浏览器渲染目标。DSL 让 Agent 只表达内容与语义结构，把重复布局、主题和打印规则交给固定渲染器。
    citations:
      - compiler-contract
  - title: Schema 校验提供直接的 Agent 修复闭环
    body: validate 一次返回全部错误、字段路径、block 和行号，Agent 可以针对性修改，而不必重新检查整份 HTML。
    citations:
      - schema-runtime
  - title: 严格契约与开放渲染可以同时存在
    body: 正式模板使用 strict Schema；未注册的文档类型进入 free mode，未知 block 和字段仍会被通用 renderer 保留。
    citations:
      - schema-runtime
:::

:::implications
title: 对 Agent 工作流的影响
items:
  - title: 模板成为可执行契约
    body: Skill 不再只给 Agent 一份示例，而是提供可以被 Python 验证的文档结构。
  - title: 视觉系统可以独立演进
    body: 同一份 DSL 可以切换主题和输出格式，而不要求 Agent 重写内容。
  - title: 站点本身成为持续回归测试
    body: 官网首页和两个研究页面必须 strict 通过后，构建器才会生成新的静态站点。
:::

:::methodology
title: 验证方法
summary: 先审计现有 parser、renderer 与 Skill 的职责，再用三个正式模板建立端到端链路，并保留旧示例验证 free mode 兼容性。
methods:
  - 校验 landing-page、research-summary 与 deep-research 三个正式模板
  - 检查旧 equity、health、slides 等示例仍能进入 free mode 并渲染
  - 对 direct HTML 与 DSL 使用相同任务和质量门槛执行真实 A/B benchmark
sample: 官网首页、研究摘要、深度研究报告，以及现有 experimental demo 画廊。
:::

:::limitations
title: 当前边界
items:
  - Token 收益仍需以相同模型、相同任务和相同质量门槛的 API usage 实验为准。
  - 当前引用系统校验 source ID 完整性，尚未实现复杂脚注编号和引用样式。
  - ECharts 与代码高亮的完全离线打包、PDF 高级分页仍属于后续工作。
:::

:::sources
title: 来源
items:
  - id: compiler-contract
    title: Momo Paper Agent-native Document Compiler
    url: https://github.com/gusibi/momo-paper
    publisher: Momo Paper
  - id: schema-runtime
    title: Momo Paper Machine Schema Runtime
    url: https://github.com/gusibi/momo-paper/tree/main/momo_dsl
    publisher: Momo Paper
:::
