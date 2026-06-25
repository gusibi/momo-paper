---
document_type: stats_report
locale: zh-CN
title: 数据报告 / KPI 示例
description: 展示 KPI 指标卡、趋势图、数据分群和方法说明。
---

:::metrics-panel
title: 核心 KPI · 2026 Q1
metrics:
  - label: 总用户数
    value: 1,280 万
    change: +18%
    status: good
  - label: 月活用户
    value: 320 万
    change: +12%
    status: good
  - label: 付费率
    value: 8.5%
    change: +1.2pp
    status: good
  - label: 流失率
    value: 3.2%
    change: -0.8pp
    status: good
:::

## 趋势

Q1 整体指标呈上升趋势，用户增长和付费转化均好于预期。以下为月度用户增长趋势：

:::line-chart
title: 月度活跃用户增长
unit: 万
items:
  - period: 1月
    value: 240
  - period: 2月
    value: 258
  - period: 3月
    value: 275
  - period: 4月
    value: 290
  - period: 5月
    value: 305
  - period: 6月
    value: 320
:::

## 数据分群

### 新用户（注册 < 30 天）

占比 35%，月环比增长 22%。主要来自自然搜索和口碑推荐。7 日留存率 42%，高于行业平均 35%。

### 活跃用户（月活跃 > 15 天）

占比 28%，核心功能使用频次 12 次/周。平均使用时长 45 分钟/天。付费转化率 18%。

### 沉默用户（30 天未活跃）

占比 37%，其中 60% 在注册后 3 天内流失。主要流失原因是 onboarding 流程缺失关键引导步骤。

## 方法说明

数据来源：产品分析平台 + 用户行为数据库。用户分群基于 RFM 模型（最近活跃、使用频次、功能深度）。月度数据为去重后的独立用户数。
