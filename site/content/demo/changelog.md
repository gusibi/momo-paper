---
document_type: changelog
locale: zh-CN
title: Momo Paper v4.0 更新日志
description: 架构升级：agentskills.io spec 对齐、CLI-first 工作流、研报模板重设计。
---

:::callout
tone: insight
title: v4.0.0 · 2026-05-02
body: 架构升级：agentskills.io spec 对齐、CLI-first 工作流、研报模板重设计。新增 K 线图和风险矩阵，slides 支持双模式，69 个测试用例覆盖所有渲染路径。
:::

## 亮点

- 项目结构重构为 agentskills.io 规范，统一 agent skill 定义格式
- CLI-first 工作流：init / render / chart / list 四大命令
- 研报（equity_report）模板全面重设计，新增 K 线图和风险矩阵
- slides 类型支持模板 + Python 生成双模式
- 新增 69 个测试用例，覆盖所有文档类型和图表渲染路径

## 新增 (Added)

- 新增 slides 类型模板，支持 cover/closing/comparison 布局
- 新增 candlestick 和 waterfall 图表类型，图表引擎扩展至 5 种
- 新增 MCP 工具定义文件，引擎可作为 MCP 工具被 AI agent 调用
- 新增批量渲染脚本
- 新增 CLI --version 选项

## 变更 (Changed)

- 项目目录重构：从扁平结构改为 scripts/assets/references 三层架构
- CLI 入口扩展为双别名
- equity_report 模板重设计：新增 KPI 卡片、K 线图、风险矩阵、催化剂时间线
- 设计令牌从分散的 CSS 变量改为统一的 design-tokens 定义
- 结构校验从模板内联提取到独立目录

## 修复 (Fixed)

- 修复 long_doc 模板中引用块在移动端的布局溢出问题
- 修复 stats_report KPI 卡片在单列布局时居中对齐失效
- 修复 chart 在空数据时抛出异常的问题，改为返回空字符串
- 修复 portfolio 模板中 metrics 为空数组时仍然渲染空卡片的问题

## 废弃 (Deprecated)

- 旧版独立 HTML 文件已迁移到新的 templates 目录
- 旧版 Build 脚本 build_all.sh 已由批量渲染脚本替代

## 迁移指南

从 v3.x 升级到 v4.0 需要注意以下变更：

1. 模板路径变更：自定义模板请更新扩展名并继承基础模板。
2. CLI 命令变更：generate 已改为 render，template 已改为 init。
3. 数据格式向后兼容，v3.x 的数据文件可直接使用。
4. 图表类型名称变更：kline 已改为 candlestick，旧名称仍可用但将在 v5.0 移除。
