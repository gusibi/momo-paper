# Momo Paper Diagrams

Use this file before selecting or drawing a diagram.

## Selection rule

Diagrams are primitives inside a document. They are not a standalone document type.

Before drawing, ask:

> Would a well-written paragraph teach the reader less than this diagram?

If the answer is no, do not draw.

## Diagram selection guide

| User says | Diagram | Template |
| --- | --- | --- |
| `架构图 / architecture / 系统图 / components diagram` | `architecture` | `assets/diagrams/architecture.html` |
| `流程图 / flowchart / 决策流 / branching logic` | `flowchart` | `assets/diagrams/flowchart.html` |
| `象限图 / quadrant / 优先级矩阵 / 2×2 matrix` | `quadrant` | `assets/diagrams/quadrant.html` |
| `柱状图 / bar chart / 分类对比 / grouped bars` | `bar_chart` | `assets/diagrams/bar-chart.html` |
| `折线图 / line chart / 趋势 / 股价 / time series` | `line_chart` | `assets/diagrams/line-chart.html` |
| `环形图 / donut / pie / 占比 / 分布结构` | `donut_chart` | `assets/diagrams/donut-chart.html` |
| `状态机 / state machine / 状态图 / lifecycle` | `state_machine` | `assets/diagrams/state-machine.html` |
| `时间线 / timeline / 里程碑 / milestones / roadmap` | `timeline_diagram` | `assets/diagrams/timeline.html` |
| `泳道图 / swimlane / 跨角色流程 / cross-team flow` | `swimlane` | `assets/diagrams/swimlane.html` |
| `树状图 / tree / hierarchy / 层级 / 组织架构` | `tree` | `assets/diagrams/tree.html` |
| `分层图 / layer stack / 分层架构 / OSI / stack` | `layer_stack` | `assets/diagrams/layer-stack.html` |
| `维恩图 / venn / 交集 / overlap / 集合关系` | `venn` | `assets/diagrams/venn.html` |
| `K 线 / candlestick / OHLC / 股价走势 / price history` | `candlestick` | `assets/diagrams/candlestick.html` |
| `瀑布图 / waterfall / 收入桥 / revenue bridge / decomposition` | `waterfall` | `assets/diagrams/waterfall.html` |

## Auto-select charts from data

When structured numeric data appears, prefer:

- proportional breakdown -> donut
- time series -> line
- category comparison -> bar
- price history -> candlestick
- value decomposition -> waterfall

Do not wait for the user to explicitly request these charts.

## Embed rule

- Open the diagram template.
- Extract the `<svg>` block.
- Drop it into a `<figure>` inside the parent document.
- Add a factual figcaption only if it improves scanning.

## Momo Paper token map

- primary stroke / key structure -> `color.brand`
- supporting stroke / secondary structure -> `color.data.secondary`
- neutral dividers / axes -> `color.line`
- emphasis / highlight -> `color.accent`
- positive / negative deltas -> `color.success` / `color.danger`
- body copy in captions -> `font.family.sansUi`
- diagram titles or lead labels -> serif headline stack when the surrounding route uses it

## AI-slop anti-patterns

| Anti-pattern | Why it fails | Better move |
| --- | --- | --- |
| Decorative 3D boxes or fake isometric systems | Looks impressive but teaches little | Use flat structure and readable labels |
| Rainbow color coding with no semantic meaning | Turns attention into noise | Limit colors to structure and one highlight |
| Tiny labels packed everywhere | Makes the figure unreadable in print | Reduce nodes and move detail into the paragraph |
| Multiple diagrams that explain the same thing | Repeats information instead of clarifying | Pick one diagram with one teaching job |
| Diagram as ornament beside complete prose | Adds cost without information gain | Remove the diagram |
