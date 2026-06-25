---
document_type: timeline
locale: zh-CN
title: Momo Paper 产品路线图
description: 2026 年产品演进计划 — 从文档引擎到设计系统平台。
---

:::timeline
title: 里程碑
items:
  - step: 2025.10
    title: 项目启动 ✓
    desc: 确定路由式设计系统的核心架构，完成 15 种文档类型的分类和设计令牌初版。
  - step: 2025.12
    title: 引擎 v0.1 ✓
    desc: Python CLI + 模板引擎上线，支持前 5 种文档类型的渲染。
  - step: 2026.01
    title: v0.2 发布 ✓
    desc: 扩展至全部 15 种文档类型，新增 3 种图表（bar/line/donut）。
  - step: 2026.03
    title: v3.0 重构 ✓
    desc: 项目结构重组为 agentskills.io 规范，新增 slides 类型和 candlestick/waterfall 图表。
  - step: 2026.04
    title: v4.0 发布 ✓
    desc: CLI-first 工作流完善，MCP 工具集成，研报模板重设计，69 个测试用例。
  - step: 2026.05
    title: 产品网站上线 ✓
    desc: 使用 Momo Paper 引擎自举构建产品网站，在 Cloudflare Pages 部署。
  - step: 2026.06
    title: 在线 Playground（进行中）
    desc: 浏览器内编辑器 + 实时预览，降低新用户上手门槛。
  - step: 2026.07
    title: Dashboard 类型（计划）
    desc: 新增 dashboard 文档类型，支持多图表布局和实时数据绑定。
  - step: 2026.08
    title: 多语言支持（计划）
    desc: 扩展至日文、韩文模板，完善 CJK 排版细节。
  - step: 2026.09
    title: v5.0 发布（计划）
    desc: 插件系统 + 自定义模板市场 + Web API 服务。
:::

## 阶段规划

### Phase 1: 基础建设（2025.10 — 2026.03）

搭建引擎核心架构，覆盖全部 15 种文档类型，建立设计令牌和图表系统。已交付：CLI、模板、结构校验、图表引擎。

### Phase 2: 生态完善（2026.04 — 2026.06）

MCP 工具集成让 AI agent 可调用引擎，产品网站自举验证引擎能力，在线 Playground 降低使用门槛。

### Phase 3: 平台化（2026.07 — 2026.09）

Dashboard 扩展数据可视化场景，多语言覆盖亚洲市场，插件系统和模板市场构建开发者生态。v5.0 作为里程碑版本。

:::footer-note
title: 下一步
body: 当前重点推进 Playground 的 MVP 版本，同时收集社区对 Dashboard 类型的需求反馈。欢迎在 GitHub Issues 中提交功能建议。
:::
