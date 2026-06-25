---
document_type: stats_report
locale: zh-CN
title: 可视化叙事全集
description: Momo Paper 视觉引擎展示：包含 5 种数据图表与 14 种图示原语。所有组件均支持 DSL 定义、设计令牌自适应及主题适配。
---

:::kpi-row
title: 核心视觉引擎
items:
  - label: 数值图表
    value: 5 种
    note: Bar / Line / Donut / K线 / 瀑布
  - label: 图示原语
    value: 14 种
    note: 涵盖逻辑、结构与流程
  - label: 样式方案
    value: Token
    note: CSS 变量全局适配
  - label: 输出格式
    value: SVG
    note: 极轻量、随主题重着色
:::

## 5 种数值图表 (Charts)

数值图表侧重于定量数据的趋势、对比和构成展示。在 DSL 中声明 chart 块即可，颜色随当前主题的设计令牌自动适配。

:::bar-chart
title: 图表库使用频率（模拟数据）
unit: 次
items:
  - label: 柱状图
    value: 45
  - label: 折线图
    value: 32
  - label: 环形图
    value: 28
  - label: K线图
    value: 15
  - label: 瀑布图
    value: 18
:::

### Bar · 柱状图

适合类别对比。items 含 label / value，可选 share 显示占比。

:::bar-chart
title: 各地区营收（M）
unit: M
items:
  - label: 华北
    value: 120
  - label: 华东
    value: 310
  - label: 华南
    value: 240
  - label: 华西
    value: 95
:::

### Line · 折线图

适合趋势展示。自动缩放 Y 轴。

:::line-chart
title: MAU 月度增长
unit: 万
items:
  - period: Q1
    value: 850
  - period: Q2
    value: 1200
  - period: Q3
    value: 1150
  - period: Q4
    value: 1600
:::

### Donut · 环形图

适合构成分析。自动计算百分比。

:::donut-chart
title: 成本构成
center_value: 100%
center_label: 总成本
segments:
  - label: 研发
    value: 40
  - label: 市场
    value: 25
  - label: 运营
    value: 20
  - label: 其他
    value: 15
:::

### Candlestick · K 线图

金融 OHLC 数据展示。

:::candlestick-chart
title: 资产价格走势
y_axis: 价格
items:
  - date: D1
    open: 100
    high: 105
    low: 98
    close: 103
  - date: D2
    open: 103
    high: 108
    low: 102
    close: 101
  - date: D3
    open: 101
    high: 110
    low: 100
    close: 107
  - date: D4
    open: 107
    high: 109
    low: 105
    close: 106
  - date: D5
    open: 106
    high: 112
    low: 106
    close: 110
:::

### Waterfall · 瀑布图

数值分解与桥接分析。

:::waterfall-chart
title: 利润变动分解
start: 期初
end: 期末
items:
  - label: 期初
    value: 100
    type: start
  - label: 增长
    value: 30
    type: positive
  - label: 成本
    value: -15
    type: negative
  - label: 汇率
    value: -5
    type: negative
  - label: 期末
    value: 110
    type: end
:::

## 14 种图示原语 (Diagrams)

图示原语专注于结构化逻辑表达，支持更细粒度的 SVG 控制，深度集成设计令牌。以下是内置的图示类型与适用场景。

:::card-grid
title: 结构化逻辑图示
cards:
  - title: Flowchart · 流程图
    desc: 逻辑跳转与步骤描述。开始 → 校验 → 执行/重试的横向标准布局。
  - title: Swimlane · 泳道图
    desc: 跨职能协作。左侧为泳道标识，流程从上至下、从左至右流动。
  - title: Architecture · 架构图
    desc: 展示分层、组件依赖与流向。
  - title: Timeline · 时间线
    desc: 关键里程碑展示。
  - title: Tree · 树状图
    desc: 层级结构展示。
  - title: Venn · 维恩图
    desc: 交集与重叠演示。
  - title: Quadrant · 象限图
    desc: 四象限优先级分析。
  - title: Layer Stack · 层级堆叠
    desc: 技术栈或协议栈展示。
  - title: State Machine · 状态机
    desc: 状态转移逻辑表现。
  - title: Bar / Line · 基础图元
    desc: 底层原语构建的条形与折线。
  - title: Donut · 基础环图
    desc: 环形路径原语。
  - title: Waterfall · 基础瀑布
    desc: 瀑布块原语。
  - title: Candlestick · 基础蜡烛
    desc: 金融 K 线原语。
:::

## 引擎说明

Momo Paper 的视觉叙事由两套引擎驱动：

1. **Charts 引擎**：专注于自动化数值呈现（Bar/Line/Donut/K线/瀑布），支持自动缩放、标签定位和百分比计算。
2. **Diagrams 引擎**：专注于结构化逻辑表达（架构、流程、时间线、维恩图等），支持更细粒度的 SVG 原语控制。

两者均深度集成设计令牌，确保全站视觉风格高度统一且易于扩展——同一份图表声明在 Momo Paper 与 Vercel 两套主题下都会自动重新着色。
