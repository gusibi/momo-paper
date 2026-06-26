---
document_type: stats_report
locale: zh-CN
title: 图表演示
description: Momo Paper 引擎内置 5 种 echarts 图表块：柱状图、折线图、环形图、K 线图、瀑布图。在 DSL 中声明 chart 块即自动渲染，颜色随主题令牌自适应。
---

引擎内置 5 种图表块，由 echarts 渲染为 SVG。在正文中声明 `:::chart-name` 块，引擎生成图表配置并注入运行时脚本，颜色从当前主题的 `--chart-*` 变量读取，因此同一份 DSL 在两套主题下自动重着色。每条均附 DSL 源码。

:::kpi-row
title: 图表块概览
items:
  - label: 图表种类
    value: 5 种
    note: Bar / Line / Donut / K线 / 瀑布
  - label: 渲染方式
    value: echarts SVG
    note: 按需加载，失败降级
  - label: 着色
    value: 主题令牌
    note: --chart-* 变量驱动
  - label: 适用
    value: 定量数据
    note: 趋势 / 对比 / 构成
:::

## Bar · 柱状图

适合类别对比。`items` 含 `label` 与 `value`，可选 `share` 在悬浮时显示占比。

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

```md
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
```

## Line · 折线图

适合时间序列与趋势。`items` 含 `period` 与 `value`，可选 `growth` 在悬浮时显示增速。

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

```md
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
```

## Donut · 环形图

适合构成分析。`segments` 含 `label` 与 `value`，`center_value` 与 `center_label` 显示环心文字。

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

```md
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
```

## Candlestick · K 线图

适合 OHLC 价格序列。`items` 含 `date`、`open`、`high`、`low`、`close`，可选 `note`。

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

```md
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
```

## Waterfall · 瀑布图

适合数值分解与桥接分析。`items` 含 `label`、`value`、`type`，`type` 为 `start` / `positive` / `negative` / `end`。

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

```md
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
```

## 选图与着色

按数据形态选择图表：比例分解用 donut，时间序列用 line，类别对比用 bar，价格历史用 candlestick，数值分解用 waterfall。每张图应有一个明确结论，必要时附数据来源或方法说明。

图表颜色不取自 `--mp-*` 文字令牌，而取自 `--chart-1` 至 `--chart-5` 等图表专用变量，柱体、轴线、标签、涨跌色各有独立变量。两套主题分别定义这些变量，因此切换主题时图表与文档同步重着色。

:::cta
title: 查看其他组件
body: nav、健康块与通用结构块的演示与源码见组件目录页。
button:
  label: 打开组件目录
  href: /components/
:::
