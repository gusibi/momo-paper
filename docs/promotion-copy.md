# Momo Paper 推广文案库

文案中的链接占位符：

- `{github}`：`https://github.com/gusibi/momo-paper`
- `{site}`：`https://momo.eztoolab.com`
- `{case}`：英雄案例页面或目录
- `{demo}`：30–45 秒 GIF/视频

发布前删除没有对应内容的链接。不要把尚未完成的 benchmark 数字补进文案。

## A1 · 中文技术长文

### 不要再让 AI Agent 从零手写正式文档的 HTML

我最近一直在解决一个很具体的问题：怎样让 AI Agent 稳定地产出可以交付的研究报告、产品方案和演示文档。

最直接的做法是让 Agent 写 HTML 和 CSS。它确实能做出来，但很快会遇到三个问题。

第一，模型需要同时负责内容、结构和视觉实现。每生成一份文档，它都要重新输出容器、字体、颜色、间距和打印规则。第二，样式会跟着 prompt 漂移。同一种报告生成两次，标题层级、卡片结构和强调方式可能完全不同。第三，修改成本高。用户只是想换一个数字或调整章节顺序，Agent 却可能重写一大段 HTML。

普通 Markdown 解决了简洁问题，但正式交付物通常还需要更明确的视觉层级、图表、版面和打印规则。

我最后采用的方案，是把 Agent 的输出和浏览器的输出拆开：

```text
用户需求
  → Agent 生成 Markdown DSL
  → validate 检查结构
  → renderer 生成单文件 HTML / PDF
```

Agent 只描述文档是什么，不再描述每个像素怎么画。比如一段结构可以写成：

```md
---
document_type: equity_report
locale: zh-CN
title: 某公司投资研究
---

:::stats
items:
  - value: 32.4%
    label: 收入增速
  - value: 18.7%
    label: 毛利率
:::
```

Momo Paper 负责把它变成风格统一、可以打印的文档。结构有问题时，`validate --json` 会返回路径、行号和块名，Agent 可以定位后重写 DSL，而不是在一整页 HTML 里猜哪里坏了。

这不是为了发明另一种 Markdown。它要解决的是 Agent 工作流里的边界问题：模型适合组织内容和结构，渲染器适合负责稳定、重复、可验证的视觉实现。

目前 Momo Paper 已经支持：

- frontmatter、Markdown 和结构化 block；
- 单文件 HTML 输出与可选 PDF 输出；
- 折线、柱状、环形、K 线和瀑布图；
- 研究摘要、投资报告、one-pager、slides 等示例；
- 可直接放进 Agent 环境的 Skill 包。

我没有把具体“节省多少 token”写进结论。仓库里有工程计数工具，但真正比较 Agent 直接写 HTML 和使用 DSL，需要固定模型、任务和质量门槛，重复实验并公开原始输出。这套实验协议已经写好，数据完成后再发布。

现在更想验证的是实际使用：如果你正在让 Codex、Claude Code 或自己的 Agent 生成报告，可以带一个不含敏感信息的真实任务试试。先跑通示例，再生成第一份自己的文档。如果卡住，请告诉我你停在哪一步。

项目：{github}

演示：{demo}

案例：{case}

## C1 · V2EX 完整帖子

### 标题

做了一个让 AI Agent 生成正式报告的 Markdown DSL + HTML renderer，想找真实任务测试

### 正文

最近在做 Momo Paper，起因是我让 Agent 生成研究报告时，经常遇到两个极端：

- 只写 Markdown，内容清楚，但不像能直接交付的正式文档；
- 直接写 HTML/CSS，能做得更完整，但代码很长，样式容易漂移，修改也经常牵一大片。

现在的做法是让 Agent 只输出 frontmatter、Markdown 和 `:::block` 结构，渲染器负责布局、主题、图表和打印规则：

```text
需求 → Agent 写 DSL → validate → 单文件 HTML / PDF
```

目前仓库里有研究摘要、投资报告、one-pager、slides 等示例，也有可以直接调用的 Skill 包。CLI 支持结构化校验、HTML/PDF 渲染，以及文件 token 的工程计数。

我现在不想继续闭门加功能，想先找真实使用场景。特别想听正在用 Codex、Claude Code 或自研 Agent 生成报告的人反馈：

1. 你最常让 Agent 生成什么文档？
2. 目前最痛的是排版、修改、导出，还是稳定性？
3. 如果愿意试，能否用一个不含敏感信息的真实任务跑一遍，并告诉我第一处卡点？

项目：{github}

演示：{demo}

我是项目作者，会在帖子里持续回复。具体 token 收益还在按公开协议做对照实验，所以这里不先报百分比。

## C2 · 掘金发布导语

### 标题

Agent 不该每次重新发明 HTML：用 DSL 和 renderer 生成正式文档

### 导语

让 AI Agent 直接写 HTML，可以很快做出一份看起来完整的报告。但当你开始批量生成、反复修改或要求打印一致时，HTML 就从输出格式变成了模型每次都要重新实现的样式系统。

这篇文章介绍 Momo Paper 的取舍：Agent 只生成内容结构，确定性的 renderer 负责 HTML、主题、图表和打印。重点不是 DSL 语法，而是为什么这条边界能让 Agent 文档更容易校验、修改和复用。

正文使用上方 A1。文章结尾只保留一个动作：

> 如果你正在让 Agent 生成报告，请拿一个真实任务试跑，并把第一处卡点发给我：{github}

## C3 · 公众号版本开头与结尾

### 标题

我为什么不再让 Agent 直接写正式报告的 HTML

### 开头

AI 很会写内容，也能写 HTML。但“能生成”不等于“适合长期生成”。当报告需要统一样式、图表、打印和反复修改时，让模型同时承担内容编辑与前端实现，会把一次生成变成每次都重新搭建页面。

我做 Momo Paper，不是为了替代 Markdown，而是想给 Agent 加一条更清晰的生产线：它负责结构，渲染器负责成品。

### 结尾

这个项目目前最需要的不是更多功能清单，而是真实文档任务。如果你平时会让 AI 生成研究报告、产品方案或复盘文档，可以回复你的场景，或者直接用一个不含敏感信息的任务试跑。项目地址：{github}

## C4 · Reddit 帖子草稿

> 发布前必须阅读目标 subreddit 的规则并按社区重写；披露作者身份，不要在多个社区复制粘贴。

### Title

I built a document renderer so agents can write structure instead of recreating HTML/CSS

### Body

I’m the author of Momo Paper. I built it after repeatedly asking coding agents to produce research reports and ending up with one of two outputs: readable Markdown that was too plain to deliver, or large HTML/CSS files whose layout changed between runs.

The workflow is deliberately small:

```text
request → agent writes Markdown DSL → validate → standalone HTML/PDF
```

The agent owns content and document structure. The renderer owns layout, themes, charts, and print styles. Validation can return machine-readable path, line, and block information so the agent can revise the source.

The repository includes report, one-pager, slide, and research-summary examples plus a self-contained skill package. I’m not claiming a universal token-saving percentage yet; I’m preparing controlled runs with public prompts and raw outputs.

I’m looking for feedback from people already generating reports with coding agents:

- What document do you generate most often?
- Where does your current workflow break: layout, editing, export, or consistency?
- Would you be willing to try one non-sensitive real task and report the first point of friction?

Project: {github}

Demo: {demo}

## HN · 仅供本人重写的事实提纲

HN 官方规则明确禁止发布生成式或 AI 编辑文本。以下内容**不能直接粘贴到 HN**，只能作为事实核对表，由项目作者本人重新组织语言。

- 建议标题事实：`Show HN: Momo Paper – a Markdown DSL renderer for agent-generated documents`
- 你亲自做了什么：parser、validator、standalone HTML/PDF renderer、Skill bundle。
- 为什么做：Agent 直接输出 HTML/CSS 时重复视觉实现，普通 Markdown 又不够正式。
- 用户现在能做什么：克隆仓库，不注册，运行示例，生成 HTML。
- 最短试用命令：从 README 复制经过干净环境验证的命令。
- 项目限制：不是在线编辑器；PDF 需要可选依赖；真实 Agent A/B benchmark 尚未完成。
- 你希望获得什么反馈：真实文档类型、第一处安装或生成阻塞、DSL 与直接 HTML 的边界是否合理。
- 发布要求：提交可直接试用的项目，不提交纯文章或注册页；本人在线回复；不请求点赞或组织朋友顶帖。

## S1–S6 · 短帖

### S1 · 问题认知

让 Agent 写正式报告时，HTML 是输出格式，不一定是合适的写作格式。

如果模型每次都要重新输出布局、字体、颜色和打印规则，它其实是在反复实现同一个渲染器。

Momo Paper 的做法：Agent 写结构，renderer 生成单文件 HTML/PDF。

我想找正在用 Agent 生成报告的人测试真实任务：{github}

### S2 · 开发取舍

这周删掉了一个很诱人的宣传方式：在没有公开原始数据前，不写“节省 80% token”。

文件长度的工程估算，不等于真实 Agent A/B 结果。后者需要固定模型、任务、质量门槛，并保存每次输出。

先把产品演示和实验方法公开，再谈百分比。{github}

### S3 · 修改成本

Agent 文档的隐藏成本不只是第一次生成，而是第二次修改。

直接改 HTML，模型可能重写整段结构；改 DSL，通常只需要调整字段或章节，视觉实现仍由 renderer 负责。

这也是我把内容结构和视觉输出拆开的主要原因。{demo}

### S4 · 产品演示

一个真实任务，四步变成正式报告：

1. 描述需求
2. Agent 生成 Markdown DSL
3. validate 检查结构
4. renderer 输出可打印 HTML/PDF

这里是 45 秒完整过程：{demo}

如果你愿意，可以拿自己的研究材料试一次：{github}

### S5 · 用户反馈征集

正在找 10 位会用 Codex / Claude Code / 自研 Agent 生成报告的开发者。

不是做问卷，希望你拿一个不含敏感信息的真实任务跑一遍，然后告诉我第一处卡点。

研究报告、产品方案、复盘文档都可以。愿意试请回复或私信你的场景。{github}

### S6 · 月度复盘模板

Momo Paper 推广第一个月，我只看一个指标：有多少人成功生成了第一份自己的文档。

本月：
- 触达：{outreach_count}
- 示例成功：{example_success}
- 自有文档成功：{own_doc_success}
- 最大阻塞：{top_blocker}
- 下月只改：{next_focus}

流量和 star 会记录，但不代替使用结果。

## E1–E4 · English launch copy

### E1 · GitHub description

Momo Paper is a document renderer for AI agents. Agents write compact Markdown DSL; Momo Paper validates the structure and renders consistent, print-ready standalone HTML or PDF.

### E2 · Short launch post

I built Momo Paper because coding agents kept recreating the same layout and CSS whenever I asked for a formal report.

The agent now writes document structure. A deterministic renderer handles themes, charts, print styles, and standalone HTML/PDF output.

I’m looking for developers who already generate reports with agents and are willing to try one real, non-sensitive task: {github}

### E3 · Demo post

One report task, four steps:

1. Describe the document
2. Let the agent write Markdown DSL
3. Validate the structure
4. Render standalone HTML/PDF

Here is the full workflow in 45 seconds: {demo}

If you generate research reports, product briefs, or retrospectives with an agent, I’d like to hear where this workflow first breaks for you.

### E4 · Evidence note

Momo Paper moves repeated layout and CSS out of the agent’s output, but I’m not publishing a universal token-saving percentage yet.

A meaningful comparison needs the same model, prompt, quality threshold, repeated runs, and public raw outputs. The protocol is in the repository; results will be published with their limits instead of as a headline without evidence: {github}

## XHS1 · 小红书 / 视频号 6 页轮播

### 封面

AI 做报告总像网页草稿？

问题可能是你让它直接写 HTML

### 第 2 页：两个极端

只写 Markdown：清楚，但不够像正式交付物。

直接写 HTML/CSS：更完整，但代码长、样式会漂、修改牵一片。

### 第 3 页：换一条生产线

让 Agent 写“文档结构”，不要让它每次重新实现“视觉系统”。

需求 → Markdown DSL → 校验 → HTML/PDF

### 第 4 页：Agent 实际写什么

展示 15–20 行真实 DSL 截图：frontmatter、一个 stats block、一个章节。

配文：内容和结构由 Agent 负责，主题、图表与打印由 renderer 负责。

### 第 5 页：最后得到什么

展示同一份 equity report 的桌面全页、局部图表和打印预览。

配文：单文件 HTML，可以浏览、分享和打印；需要时导出 PDF。

### 第 6 页：邀请试用

我正在找 10 位会用 AI Agent 生成报告的人。

拿一个不含敏感信息的真实任务试一次，告诉我第一处卡点。

项目：{github}

### 配套正文

我做 Momo Paper，不是想再造一个在线编辑器，而是想解决 Agent 生成正式文档时的边界问题：模型负责内容结构，渲染器负责稳定的视觉输出。

目前有研究报告、投资分析、one-pager、slides 等示例。真实 token 对照还在按公开协议测试，所以这次先展示完整工作流，不报没有原始数据的百分比。

如果你已经在用 Codex、Claude Code 或自研 Agent 做报告，欢迎带一个真实任务试用。项目链接放在评论/主页：{github}

## D1–D3 · 一对一触达

### D1 · 发给认识的 Agent 开发者

最近我在做 Momo Paper：让 Agent 写 Markdown DSL，再渲染成统一样式的 HTML/PDF，主要解决正式报告直接写 HTML 太长、样式不稳定的问题。

你之前提过会用 Agent 做 `{对方的具体场景}`。我现在不缺泛泛建议，想找人拿一个真实但不敏感的任务跑一遍，看第一处卡在哪里。你愿意试的话，我可以按你的场景准备最小示例；不方便也完全没关系。

### D2 · 发给开源项目作者

你好，我是 Momo Paper 的作者。看到你的项目在做 `{具体功能/工作流}`，其中似乎会生成 `{报告/文档}`。

Momo Paper 的思路是让 Agent 只输出内容结构，由确定性的 renderer 负责 HTML/PDF、主题和打印。我想验证它是否适合真实 Agent 工作流，不是来推集成合作。

如果你愿意，我可以基于你项目里一个公开样例做一次最小演示，并把源文件和结果都公开。你只需要告诉我这个场景有没有意义；不合适我就不继续打扰。

### D3 · 用户试用后的追问

谢谢你实际跑了一遍。为了避免问一堆空泛问题，我只想确认三件事：

1. 你在哪一步第一次犹豫或停住？
2. 最终结果和你原来的做法相比，哪一点更好、哪一点更差？
3. 如果下周只能改一件事，什么会让你愿意再用一次？

我会按原话记录，除非得到你许可，不会公开你的任务或内容。

## R1–R8 · 评论回复模板

### “这不就是 Markdown 转 HTML？”

底层确实包含 Markdown 到 HTML，但边界不同：Agent 输出 frontmatter、散文和结构化 block，validator 提供机器可读错误，renderer 统一处理主题、图表和打印。重点不是格式转换本身，而是让 Agent 不再为每份文档重新实现视觉层。

### “为什么不用现有静态站点生成器？”

如果目标是网站，静态站点生成器更成熟。Momo Paper 聚焦单份正式文档和 Agent 工作流：结构化错误、单文件输出、文档模板、图表与打印。两者可以组合，不需要互相替代。

### “为什么不直接让模型写 React/HTML？”

一次性页面完全可以直接写。Momo Paper 更适合需要重复生成、统一风格、反复修改和打印的文档。如果任务只做一次且高度定制，直接 HTML 可能更合适。

### “真的省 token 吗？”

结构上会把重复 CSS 和标记移出 Agent 输出，但具体节省比例取决于模型、任务和质量要求。目前只公开工程计数，不把它当真实 Agent A/B 结论；受控实验会同时公开 prompt 和原始输出。

### “为什么还要发明 DSL？”

DSL 很薄：frontmatter、Markdown 加结构化 block。它不是为了覆盖任意网页，而是为了把文档意图交给 renderer。代价是自由度较低，换来可校验和一致性。

### “能不能生成 DOCX/PPTX？”

当前核心输出是单文件 HTML，可选 PDF。DOCX/PPTX 还不是已交付能力。如果你的场景必须编辑 Office 原生文件，这一版不适合，我会把它记录为需求而不是承诺时间。

### “安装太麻烦了”

这是有效问题。能否告诉我你停在 Skill 安装、Python 环境、命令名还是首个示例？我会优先修最早出现的阻塞，不先增加新功能。

### “有在线版吗？”

当前重点是本地 CLI/Skill 和可复现输出，不要求上传用户文档。在线编辑器不在首阶段范围；如果你需要的是免安装体验，我会记录它对试用转化的影响。
