---
document_type: deep-research
locale: zh-CN
title: Agent 原生文档编译器深度研究
description: 用正式 deep-research Schema 展示执行摘要、证据、反方观点、方法、限制、建议与可追溯来源。
author: Momo Paper Research
---

:::research-header
topic: Agent 原生文档编译器
scope: 结构化 DSL、Schema 校验、HTML/PDF 渲染与 Skill 集成
period: 2026 Q3
status: reviewed
:::

:::research-question
question: Agent 的正式文档输出是否应该经过可验证的中间表示，而不是直接生成最终 HTML？
scope: 关注输出成本、可靠性、品牌一致性、可维护性和开放扩展能力。
:::

:::executive-summary
title: 执行摘要
summary: Momo Paper 将 DSL 作为 Agent 与渲染器之间的公开中间表示。正式模板通过机器 Schema 约束结构，实验文档通过 free mode 保持开放；最终由同一主题系统输出 HTML 与 PDF。
citations:
  - compiler-contract
  - schema-runtime
:::

:::key-findings
title: 核心发现
items:
  - title: 可验证性比单纯 token 压缩更持久
    body: Token 节省是传播优势，但长期价值来自结构契约、品牌一致、错误可定位和同源多格式输出。
    confidence: high
    citations:
      - compiler-contract
  - title: strict validate 与 permissive render 应当分离
    body: 正式模板必须暴露未知字段和缺失章节；直接渲染则不能丢弃已经成功解析的未知内容。
    confidence: high
    citations:
      - schema-runtime
  - title: Skill 是产品入口，CLI 是执行后端
    body: Agent 按需读取模板 reference，执行 validate、自修复和 render；用户最终接收成品和可保存的 DSL 源文件。
    confidence: high
    citations:
      - skill-contract
:::

:::evidence
title: 工程证据
items:
  - claim: 官网首页已使用 landing-page 正式契约
    body: site/build.py 在删除旧输出前显式验证首页；如果必需字段或 block 失效，构建会直接停止。
    citations:
      - site-builder
  - claim: 研究页面具备来源引用完整性检查
    body: source ID 必须唯一，findings、evidence 与 executive summary 中的 citation 必须指向已声明来源。
    citations:
      - schema-runtime
  - claim: 历史模板仍可继续使用
    body: equity report、slides、health report 等未注册类型进入 experimental/free mode，未知 block 由通用 renderer 保留。
    citations:
      - compatibility-tests
:::

:::counterarguments
title: 反方观点
items:
  - title: 模型直接生成 HTML 的质量会持续提高
    body: 这会削弱“模型不会写 HTML”的论点，但不会消除团队对稳定结构、品牌治理、验证和重复构建的需求。
  - title: 新 DSL 会增加学习成本
    body: DSL 主要由 Agent 生成，用户不需要从零记忆语法；Skill reference 和结构化错误负责降低 Agent 的生成成本。
:::

:::methodology
title: 方法
summary: 通过代码能力审计、站点 dogfooding、兼容性回归和真实 A/B benchmark 四条路径验证产品方向。
methods:
  - 用机器 Schema 生成 Skill reference，避免说明与实现漂移
  - 让官网三个旗舰页面作为 strict 构建门禁
  - 让现有实验模板持续通过 free mode 渲染
  - 固定模型、任务与质量门槛，对比 direct HTML 和 DSL 的 API 输出 token
sample: landing-page、research-summary、deep-research 三个正式模板及现有 demo 画廊。
:::

:::limitations
title: 限制
items:
  - 当前正式 Schema 只有三个，其余目标模板仍待逐步定义。
  - 引用系统尚未提供脚注编号、引用样式和来源快照。
  - 完全离线资源打包和高级 PDF 分页仍未完成。
:::

:::recommendations
title: 建议
items:
  - title: 先用真实任务验证三个旗舰模板
    body: 重点观察首次 strict 通过率、修复轮数、最终文档质量和 token A/B 结果。
  - title: 继续从机器 Schema 生成所有 Agent 文档
    body: 新模板必须同时具备 Schema、Skill reference、示例和回归测试，避免出现半正式模板。
  - title: 把官网作为持续发布门禁
    body: 每次修改 runtime、Schema 或主题后，都应重新构建站点并检查三个旗舰页面。
:::

:::sources
title: 来源
items:
  - id: compiler-contract
    title: Momo Paper Project Overview
    url: https://github.com/gusibi/momo-paper
    publisher: Momo Paper
  - id: schema-runtime
    title: Machine Schema and Semantic Validation Runtime
    url: https://github.com/gusibi/momo-paper/blob/main/momo_dsl/schema.py
    publisher: Momo Paper
  - id: skill-contract
    title: Momo Paper Skill Contract
    url: https://github.com/gusibi/momo-paper/blob/main/momo-paper-skill/SKILL.md
    publisher: Momo Paper
  - id: site-builder
    title: Momo Paper Product Site Builder
    url: https://github.com/gusibi/momo-paper/blob/main/site/build.py
    publisher: Momo Paper
  - id: compatibility-tests
    title: Momo Paper Schema Compatibility Tests
    url: https://github.com/gusibi/momo-paper/blob/main/tests/test_schema.py
    publisher: Momo Paper
:::
