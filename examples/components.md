---
document_type: landing
locale: zh-CN
title: Momo Paper 组件库
description: 这是 Momo Paper DSL 支持的全部组件目录。每个组件都附带真实示例，可直接复制为模板使用。本页本身完全由 DSL 生成，未写入任何内联样式。
author: Momo Paper
date: 2026-06-14
---

:::nav
brand: Momo Paper 组件库
items:
  - label: 概览
    href: "#top"
  - label: 着陆页
    href: "#landing"
  - label: 布局
    href: "#layout"
  - label: 内容
    href: "#content"
  - label: 图表
    href: "#charts"
  - label: 金融
    href: "#finance"
  - label: 评分
    href: "#scoring"
  - label: 健康
    href: "#health"
cta:
  label: 查看规范
  href: "#about"
:::

## 如何阅读本页

每个组件都包含**它的用途**和**一个可直接复制的示例**。所有内容都用 `:::标签名` 语法编写，再经 Momo Paper 渲染为独立 HTML。

- 使用 Markdown 写正文（标题、段落、列表、`行内代码`、**加粗**、*斜体*、[链接](https://example.com)）。
- 使用 `:::标签名` 块写结构化内容。
- 任意块都可加 `id:` 字段，作为导航锚点跳转目标。
- 不要在文档里写 HTML 或内联样式，样式全部由主题 CSS 提供。

:::section
id: about
title: 文档结构与 Frontmatter
body: 每个文档以 frontmatter 开头，必须包含 document_type、locale、title 三个字段；description、author、date 为可选。frontmatter 之后即正文，可自由混排 Markdown 与 DSL 块。
points:
  - document_type：文档类型，如 landing、equity-report、health-report。
  - locale：语言，推荐 zh-CN 或 en。
  - title：页面标题，同时作为 HTML title 与页眉大标题。
  - description：可选，作为页面引导语。
:::

:::section
id: landing
title: 一、着陆页区块
body: 用于产品介绍页、营销页的主力组件：开场、特性、数据、流程、对比、行动号召与常见问题。
:::

## hero · 开场区

页面顶部的主视觉区，承载主张与主行动按钮。

:::hero
eyebrow: Markdown DSL
title: 用结构生成页面，而不是脆弱的 HTML
subtitle: 写下结构化的块，Momo Paper 负责校验并输出稳定的独立 HTML。
primary_cta:
  label: 开始使用
  href: "#landing"
secondary_cta:
  label: 阅读规范
  href: "#about"
:::

## feature-grid · 特性网格

用于罗列能力、卖点或功能清单，自动按列排布。

:::feature-grid
columns: 3
items:
  - title: 可预测的语法
    desc: Agent 每次都写出相同的块结构，渲染结果稳定。
  - title: 通用渲染
    desc: 任何合法标签都能被渲染，未知标签也能优雅降级。
  - title: 清晰的报错
    desc: 校验失败时直接指向出错的行与块。
:::

## stats · 关键数据

用于数字型主张或汇总指标。

:::stats
items:
  - value: 1
    label: 源 Markdown 文件
  - value: 40+
    label: 内置组件标签
  - value: 100%
    label: 由 DSL 生成的 HTML
:::

## timeline · 时间线

用于流程、步骤、路线图或里程碑。

:::timeline
title: 生成流程
items:
  - step: 1
    title: Agent 写 DSL
    desc: 使用文档化的标签编写结构化内容。
  - step: 2
    title: Momo 校验
    desc: 解析器检查语法与 frontmatter。
  - step: 3
    title: 输出 HTML
    desc: 渲染器输出独立可分发的文件。
:::

## comparison · 对比

用于前后、左右、新旧两栏对照。

:::comparison
title: 直写 HTML vs Markdown DSL
left:
  title: 直写 HTML
  items:
    - 难以校验
    - 视觉容易跑偏
    - 重复劳动多
right:
  title: Markdown DSL
  items:
    - 易于解析
    - 输出可复现
    - 结构与样式分离
:::

## cta · 行动号召

用于一个明确的行动区块。

:::cta
title: 现在就生成页面
body: 先校验 DSL，再渲染为 HTML。
button:
  label: 渲染 HTML
  href: "#charts"
:::

## faq · 常见问题

用于问答列表。

:::faq
items:
  - question: 运行时会定义组件吗？
    answer: 不会。它只解析用户或 Agent 写下的标签。
  - question: 可以使用自定义标签吗？
    answer: 可以，只要标签名符合命名规则，就会被通用渲染。
:::

:::section
id: layout
title: 二、布局组件
body: 用于把内容拆分到多栏、多卡片、有序步骤或前后对照的结构中。
:::

## two-columns · 双栏

用于成对内容。

:::two-columns
title: 分栏布局
left:
  title: 内容
  body: Markdown DSL 定义结构。
right:
  title: 渲染
  body: CSS 定义呈现。
:::

## three-columns · 三栏

用于三段式解释。

:::three-columns
title: 系统分层
columns:
  - title: 内容
    body: Markdown 与结构化字段。
  - title: 解析器
    body: 校验并生成 AST。
  - title: 渲染器
    body: 输出 HTML 与 CSS。
:::

## card-grid · 卡片网格

用于一组重复的卡片。

:::card-grid
title: 文档路由
cards:
  - title: 着陆页
    desc: 产品与营销页面。
  - title: 股票报告
    desc: 研究与估值页面。
  - title: 健康周报
    desc: 体重与习惯追踪页面。
:::

## steps · 步骤

用于有序工作流，自动编号。

:::steps
title: 渲染工作流
items:
  - step: 1
    title: 写 DSL
    desc: Agent 用块语法编写 Markdown。
  - step: 2
    title: 校验
    desc: Momo Paper 报告语法错误。
  - step: 3
    title: 渲染
    desc: CLI 输出独立 HTML。
:::

## before-after · 前后对比

用于转变故事与改造对照。

:::before-after
title: 改造前后
before:
  title: 直写 HTML
  items:
    - 结构脆弱
    - 难以校验
after:
  title: Markdown DSL
  items:
    - 结构化块
    - 校验清晰
:::

:::section
id: content
title: 三、内容组件
body: 用于强调、引用、定价、表格、漏斗、单指标卡与画廊等通用内容区块。
:::

## callout · 提示框

用于注记、提醒、洞察等需要强调的内容。

:::callout
tone: insight
title: 让 HTML 留在 DSL 之外
body: Agent 只产出结构化块，HTML 由渲染器掌控。
:::

## quote · 引用

用于金句、证言或被引用的观点。

:::quote
text: 最好的生成页面，是先有结构，再谈样式。
source: Momo Paper 设计笔记
:::

## table · 表格

用于通用行列数据，建议用显式键而非 Markdown 表格。

:::table
title: 浏览器支持
rows:
  - feature: 独立 HTML
    status: 已支持
    note: CSS 已内联。
  - feature: PDF 导出
    status: 计划中
    note: Phase 2。
:::

## metric-card · 单指标卡

用于单个被强调的指标。

:::metric-card
label: 渲染成功率
value: 99.9%
delta: +2.1pp
note: 在合法 DSL 输入上测得。
:::

## funnel · 漏斗

用于转化漏斗。

:::funnel
title: Agent 生成漏斗
steps:
  - label: 接受提示词
    value: 1000
  - label: 合法 DSL
    value: 860
  - label: 成功渲染
    value: 842
:::

## pricing · 定价

用于套餐对比。

:::pricing
title: 定价
plans:
  - name: Free
    price: $0
    desc: 适合体验。
    features:
      - 3 个文档
      - 基础 HTML 导出
  - name: Pro
    price: $19
    desc: 适合生产使用。
    features:
      - 无限文档
      - 自定义 CSS
:::

## logo-cloud · 标志墙

用于合作伙伴、客户或集成方的标志（Phase 1 中以文字标签呈现）。

:::logo-cloud
title: 正在使用 Momo Paper 的团队
logos:
  - name: Northstar Bank
    src: /logos/northstar.svg
  - name: CloudWorks
    src: /logos/cloudworks.svg
  - name: Helio Labs
    src: /logos/helio.svg
:::

## image-grid · 图片网格

用于画廊式图片集合。

:::image-grid
title: 产品状态
images:
  - src: /images/editor.png
    alt: DSL 编辑器
    caption: 编写结构化内容。
  - src: /images/output.png
    alt: HTML 输出
    caption: 渲染独立 HTML。
:::

## diagram · 结构图

用于结构化图示，保持数据显式以便未来渲染器增强。

:::diagram
type: flowchart
title: DSL 渲染管线
nodes:
  - id: author
    label: Agent 写 DSL
  - id: parser
    label: 解析器校验
  - id: html
    label: 输出 HTML
edges:
  - from: author
    to: parser
  - from: parser
    to: html
:::

## footer · 页脚

用于导航、版权与法律链接。

:::footer
brand: Momo Paper
summary: 从 Markdown DSL 到独立 HTML。
links:
  - label: 文档
    href: "#about"
  - label: GitHub
    href: "#top"
copyright: 2026 Momo Paper
:::

:::section
id: charts
title: 四、数据图表
body: 折线、柱状、环形、K 线、瀑布等图表由 ECharts 渲染为交互式 SVG；另有通用 chart 块用于简单数据。
:::

## line-chart · 折线图

用于时间序列。

:::line-chart
title: AI 付费用户趋势
unit: 万人
items:
  - period: 2025 Q1
    value: 18
    growth: baseline
  - period: 2025 Q3
    value: 34
    growth: +89%
  - period: 2026 Q1
    value: 65
    growth: +91%
:::

## bar-chart · 柱状图

用于分类对比。

:::bar-chart
title: 收入结构
unit: 亿元
items:
  - label: 协作订阅
    value: 28.4
    share: 58%
  - label: AI 助手
    value: 8.6
    share: 18%
  - label: 平台服务
    value: 11.8
    share: 24%
:::

## donut-chart · 环形图

用于占比分解。

:::donut-chart
title: 收入地区占比
center_value: 18%
center_label: 海外收入占比
segments:
  - label: 中国内地
    value: 72
  - label: 东南亚
    value: 14
  - label: 其他地区
    value: 14
:::

## candlestick-chart · K 线图

用于价格区间历史。

:::candlestick-chart
title: 股价区间与月度 K 线
x_axis: 2025-01 至 2025-05
y_axis: HKD
items:
  - date: 2025-01
    open: 140
    high: 155
    low: 132
    close: 148
  - date: 2025-02
    open: 148
    high: 168
    low: 145
    close: 162
  - date: 2025-03
    open: 162
    high: 175
    low: 150
    close: 154
  - date: 2025-04
    open: 154
    high: 190
    low: 152
    close: 186
:::

## waterfall-chart · 瀑布图

用于估值桥与价值分解。

:::waterfall-chart
title: 目标价桥
start: HK$ 198
end: HK$ 285
items:
  - label: 当前股价
    value: 198
    type: start
  - label: AI ARPU 重估
    value: 38
    type: positive
  - label: 海外扩张
    value: 60
    type: positive
  - label: 合规折价
    value: -11
    type: negative
  - label: 目标价
    value: 285
    type: end
:::

## chart · 通用图表

当不需要特定图表标签时，用于简单数据呈现。

:::chart
type: line
title: 月度文档量
x: month
y: count
data:
  - month: Jan
    count: 12
  - month: Feb
    count: 28
  - month: Mar
    count: 41
:::

:::section
id: finance
title: 五、金融报告组件
body: 面向股票研究与投资备忘录的专用组件：投资结论、业务快照、估值表、风险矩阵、催化剂与最终建议。
:::

## thesis-panel · 投资结论

用于核心投资结论。

:::thesis-panel
title: 投资结论
rating: 买入
target_price: HK$ 285
current_price: HK$ 198
summary: 当前估值尚未充分反映 AI 商业化与海外收入扩张。
drivers:
  - title: AI 商业化加速
    desc: 付费用户与 ARPU 同步提升。
  - title: 海外市场扩张
    desc: 东南亚企业客户快速增长。
:::

## business-snapshot · 业务快照

用于公司概况与经营摘要。

:::business-snapshot
title: 业务快照
body: 公司是企业协作 SaaS 龙头。
facts:
  - label: 头部客户续费率
    value: 97%
  - label: 海外收入占比
    value: 18%
  - label: 年营收
    value: 32.8 亿元
:::

## price-drivers · 股价与驱动

用于股价背景与核心驱动。

:::price-drivers
title: 股价与核心驱动
body: 当前股价对应 FY2026 Forward P/E 32x。
price:
  current: HK$ 198
  target: HK$ 285
drivers:
  - title: AI 付费用户增长
    metric: Q1 +65% QoQ
    desc: 企业版渗透率提升。
:::

## kpi-row · KPI 卡片行

用于关键指标卡片。

:::kpi-row
title: 关键指标
items:
  - label: 目标价
    value: HK$ 285
    note: 较当前价上涨 44%
  - label: 评级
    value: 买入
    note: 维持
  - label: 上行空间
    value: 44%
    note: 12 个月
:::

## valuation-table · 估值表

用于估值假设。

:::valuation-table
title: 估值
method: P/E 与 EV/Revenue 双维度估值
rows:
  - metric: FY2026 Forward P/E
    current: 32x
    peer_median: 40x
    target: 45x
  - metric: EV/Revenue
    current: 9x
    peer_median: 11x
    target: 12x
insight:
  title: 安全边际
  desc: 当前倍数低于目标倍数。
:::

## financial-table · 财务预测表

用于多期预测。

:::financial-table
title: 财务预测
rows:
  - metric: 营收（亿元）
    fy2024: 23.1
    fy2025: 32.8
    fy2026e: 48.5
    fy2027e: 65.2
  - metric: 毛利率
    fy2024: 71%
    fy2025: 73%
    fy2026e: 75%
    fy2027e: 76%
:::

## risk-matrix · 风险矩阵

用于风险与催化剂。

:::risk-matrix
title: 风险与催化剂
risks:
  - severity: high
    title: AI 合规政策风险
    desc: 合规要求可能延缓功能上线。
  - severity: medium
    title: 竞争加剧
    desc: 大厂入局压制定价权。
catalysts:
  - date: 2026 Q3
    title: AI 付费用户突破 100 万
    desc: 验证商业化路径。
:::

## catalyst-timeline · 催化剂时间线

用于带日期的催化剂或预期事件。

:::catalyst-timeline
title: 未来 12 个月催化剂
items:
  - date: 2026 Q2
    title: Q2 财报披露
    desc: 重点关注 AI 收入占比。
  - date: 2026 Q4
    title: 海外新区域上线
    desc: 验证扩张节奏。
:::

## recommendation · 最终建议

用于最终建议与行动。

:::recommendation
title: 最终建议
body: 给予「买入」评级。
actions:
  - title: 建仓区间
    desc: 建议分批建仓。
  - title: 止损纪律
    desc: 跌破关键支撑位减仓。
:::

## footer-note · 免责声明

用于披露、注记与免责声明。

:::footer-note
title: 免责声明
body: 本报告仅供研究参考，不构成买卖建议。
:::

:::section
id: scoring
title: 六、评分报告组件
body: 面向打分型分析报告的专用组件：综合评分、市场快照、评分明细、驱动逻辑、操作指引与关注清单。
:::

## score-summary · 综合评分

用于报告开头的综合评分卡：分数、状态标签与一句话结论。

:::score-summary
title: 综合评分
score: 5.5
status: 中性偏多
summary: 多空因素交织，方向性催化剂落地前以区间震荡对待，仓位保持中性。
:::

## market-snapshot · 市场快照

用于并排展示一组关键市场指标，每项含数值与备注。

:::market-snapshot
title: 市场快照
items:
  - label: 现货黄金
    value: $4,540.30
    note: 周末休市
  - label: 沪金 AU9999
    value: 984.02 元/克
    note: 上周收盘
  - label: 美元指数
    value: ~99.0
    note: 从 99.5 回落
  - label: 10Y 美债
    value: ~4.50%
    note: 高位回落
  - label: SPDR 持仓
    value: ~1,032 吨
    note: 持续流出
  - label: VIX
    value: 低位
    note: 等催化剂
:::

## scoring-breakdown · 评分明细

用于展示加权评分的构成：公式、加权总分与各因子明细。

:::scoring-breakdown
title: 评分明细
formula: 6×20% + 6×20% + 6×15% + 5×15% + 4×15% + 6×10% + 5×5% = 5.5
weighted_total: 5.5
items:
  - factor: 价格动量
    weight: 20%
    score: 6 分
  - factor: 美元/利率
    weight: 20%
    score: 6 分
  - factor: 通胀环境
    weight: 15%
    score: 6 分
  - factor: 地缘政治
    weight: 15%
    score: 5 分
  - factor: 资金流向
    weight: 15%
    score: 4 分
  - factor: 市场情绪
    weight: 10%
    score: 6 分
  - factor: 事件风险
    weight: 5%
    score: 5 分
:::

## driver-logic · 驱动逻辑

用于编号列出核心驱动因素的推理链条，每条是一段说明。

:::driver-logic
title: 核心驱动逻辑
items:
  - index: 1
    body: 金价上周深 V 反转，$4,380 确认实物需求底部，双底形态形成中，突破 $4,600 可上探 $4,800。
  - index: 2
    body: 核心 PCE 环比 +0.2% 低于预期、GDP 下修，缓解加息恐慌，美元回落至 ~99。
  - index: 3
    body: 本周焦点为周五非农，>100k 利空、50–100k 中性、<50k 强化降息预期利好黄金。
  - index: 4
    body: 地缘停火协议接近达成，避险溢价边际回落。
:::

## action-guidance · 操作指引

用于给出分场景的行动建议，每条含标题与说明。

:::action-guidance
title: 操作指引
items:
  - title: 长线配置
    desc: 央行购金与去美元化逻辑不变，$4,400–4,500 区间分批配置。
  - title: 中线观察
    desc: 本周五非农是关键方向催化剂，决定突破 $4,600 或回测 $4,400。
  - title: 短线等待
    desc: 非农前预计区间震荡，双底偏多但需数据确认。
:::

## watchlist · 关注清单

用于罗列需要持续跟踪的事件，每项一行。

:::watchlist
title: 本周关注
items:
  - 周五美国 5 月非农（预期 85k–96k）为核心焦点
  - 非农后市场对下次 FOMC 加息概率重新定价
  - 地缘停火协议落地进展
:::

:::section
id: health
title: 七、健康报告组件
body: 面向体重管理与健康追踪的专用组件：报告头、周总结、目标追踪与指标面板。
:::

## report-header · 报告头

用于报告头部，含日期范围与元数据。

:::report-header
title: 减脂周报
eyebrow: Momo Coach · 第 12 周
date_range: 2026.05.19 – 2026.05.26
weigh_day: 2026-05-26
:::

## weekly-summary · 周总结

用于周度总结与评估。

:::weekly-summary
title: 本周总结
period: 2026年5月25日 - 5月31日
summary: 体重回落至目标区间，体脂率稳步下降，继续保持运动习惯。
positives:
  - title: 运动坚持
    desc: 完成 5 天运动计划
  - title: 饮食控制
    desc: 工作日热量摄入达标
improvements:
  - title: 周末饮食
    desc: 需要避免油腻食物
  - title: 睡眠时间
    desc: 尽量在 11 点前入睡
:::

## goal-tracker · 目标追踪

用于目标追踪与进度条。

:::goal-tracker
title: 下周目标
goals:
  - title: 运动目标
    target: 5
    current: 3
    unit: 天
    desc: 至少运动 5 天，包含 3 次有氧和 2 次力量
  - title: 睡眠目标
    target: 7.5
    current: 7.3
    unit: 小时
    desc: 每晚 11 点前入睡，保证 7-8 小时睡眠
  - title: 饮水目标
    target: 2.0
    current: 1.8
    unit: 升
    desc: 每天至少 2.0 升水
:::

## metrics-panel · 指标面板

用于关键健康指标面板。

:::metrics-panel
title: 关键指标
metrics:
  - label: 周末体重
    value: 68.2 kg
    change: -0.8 kg
    status: good
  - label: BMI
    value: 22.1
    change: -0.3
    status: normal
  - label: 体脂率
    value: 18.5%
    change: -0.3%
    status: good
  - label: 运动天数
    value: 5 天
    change: +1 天
    status: good
:::

:::cta
id: end
title: 把这页当作模板
body: 复制任意一个块，替换数据即可。需要新组件时，用任意合法标签名编写，渲染器会优雅降级。
button:
  label: 回到顶部
  href: "#top"
:::
