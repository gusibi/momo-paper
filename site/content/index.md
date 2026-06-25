---
document_type: landing
locale: zh-CN
title: Momo Paper — 面向文档与视觉叙事的路由式设计系统
description: 一个路由式设计系统，将 15 种文档类型、5 种可编程图表和 14 种图示原语统一到一套设计令牌中。
show_header: false
---

:::hero
eyebrow: 开源文档引擎 · 2.1
title: 让每一份文档都有设计感
subtitle: Momo Paper 是一个路由式设计系统，将 15 种文档类型、5 种可编程图表和 14 种图示原语统一到一套设计令牌中。无论是手写 Markdown DSL 还是让 AI agent 调用引擎，输出始终排版精良、打印就绪。
primary_cta:
  label: 快速开始
  href: /guide/
secondary_cta:
  label: 浏览文档类型
  href: /types/
:::

:::three-columns
title: 从声明到成品
columns:
  - title: Markdown DSL
    body: 用 :::block 声明结构化内容
  - title: Engine
    body: 路由 + 设计令牌 + 渲染
  - title: HTML
    body: 排版精良 · 打印就绪
:::

## 两种方式，同一套设计语言

无论你偏好哪种工作流，输出的文档都共享统一的视觉语言。

:::feature-grid
columns: 3
items:
  - title: 15 种文档类型
    desc: 覆盖 one-pager、白皮书、简历、研报、幻灯片、信息图等全场景，每种类型都有中英文双模板和结构校验。
  - title: 5 种可编程图表
    desc: 柱状图、折线图、环形图、K 线图、瀑布图 — 在 DSL 中声明 chart 块，引擎自动渲染。
  - title: 14 种图示原语
    desc: 架构图、流程图、泳道图、象限图、维恩图等可直接使用或嵌入文档的独立图示。
  - title: 双主题系统
    desc: Momo Paper 暖调主题与 Vercel 极简主题，共享同一套 --mp-* 设计令牌，一键切换。
  - title: AI Agent 原生集成
    desc: 引擎可作为 Skill 被 Claude Code 直接调用。Agent 构造结构化 DSL，引擎返回设计精良的 HTML — 告别不稳定的 prompt 输出。
  - title: 打印安全内置
    desc: 所有样式都内置 @media print 规则，自动处理背景、边距和分页。同一份 HTML 在屏幕和纸张上都表现一致。
:::

## 选择最适合你的工作流

从零依赖的 HTML 模板到 AI agent 全自动渲染，Momo Paper 适配不同场景。

### 01 · Claude Code Skill（推荐）

**AI agent 自动完成全流程。** 只需用自然语言描述需求，Skill 自动选择合适的文档类型、构造 DSL 数据、调用引擎渲染、在浏览器中打开结果。

- 自然语言驱动
- 自动类型选择 + DSL 构造
- 一键渲染并预览

### 02 · CLI 命令行（灵活）

**精确控制每一步。** 通过 momo2 命令验证、渲染 HTML。适合需要精确控制输出或集成到自动化流水线的场景。

- momo2 validate / render 命令
- 结构与元数据校验
- CI/CD 流水线友好

### 03 · HTML 模板直接编辑（零依赖）

**打开即编辑，无需任何构建。** 独立 HTML 文件，设计令牌、排版、间距已全部预设。用任意编辑器打开即可修改内容，适合快速原型和非技术人员。

- 无需 Python / Node.js
- 设计令牌 CSS 变量内联
- 浏览器直接预览

:::card-grid
title: 覆盖 15 种文档场景
cards:
  - title: 方案 / 执行摘要
    desc: 四段结构：摘要 → 背景 → 证据 → 建议
  - title: 白皮书 / 长文
    desc: 可迭代章节 + 引用块 + 结论
  - title: 信件 / 推荐信
    desc: 信头、正文、请求、签名
  - title: 作品集
    desc: STAR 框架 + 数据指标卡
  - title: 简历 / CV
    desc: 时间线 + 技能标签
  - title: 幻灯片
    desc: 16:9 视口，多种布局
  - title: 研报 / 估值分析
    desc: KPI + K 线图 + 风险矩阵
  - title: 更新日志
    desc: 按变更类型分类
  - title: 流程 / SOP
    desc: 步骤编号 + 负责人标注
  - title: 时间线
    desc: completed / in_progress / upcoming
  - title: 常见问题
    desc: 分组问答卡片
  - title: 案例拆解
    desc: 背景 → 问题 → 方案 → 结果
  - title: 研究摘要
    desc: 论题 + 关键发现 + 方法说明
  - title: 数据报告
    desc: KPI 大数字 + 趋势图
  - title: 信息图
    desc: 大数字 + 环形图 + 步骤路径
:::

## 对比传统文档工具

Momo Paper 不是又一个编辑器。它是一个文档生成引擎，从根本上改变了文档的创建和维护方式。

:::comparison
title: 为什么选择 Momo Paper
left:
  title: 传统方式 · Word / LaTeX / Notion
  items:
    - 每次新建文档都要重新调整格式
    - 团队协作时风格无法保证一致
    - AI 输出格式不稳定，需要手动修正
    - 打印需额外调整边距和分页
    - 图表需要第三方工具单独制作
right:
  title: Momo Paper · 路由式设计系统
  items:
    - 设计令牌统一管理，修改一次全局生效
    - 结构校验保证数据正确
    - AI agent 原生集成，结构化输出稳定可控
    - 内置 @media print 规则，屏幕和纸张表现一致
    - 图表在 DSL 中声明，引擎自动渲染
:::

:::stats
items:
  - value: 15
    label: 文档类型
  - value: 5
    label: 图表类型
  - value: 14
    label: 图示原语
  - value: 2
    label: 可切换主题
:::

## EZTOLAB 生态 · 一个工具做好一件事

Momo Paper 是 EZTOLAB 工具实验室的一员。每个工具独立解决一个具体问题，共同构成高效工作流。

- [MoliBot](https://molibot.eztoolab.com) — 多渠道 AI 助手运行时
- [MoliShot](https://molishot.eztoolab.com) — macOS 截图与 OCR 工具
- [MoliTodo](https://molitodo.eztoolab.com) — AI 驱动的桌面悬浮 todo
- [MoliTutu](https://tutu.eztoolab.com) — 图片压缩与 CDN 上传
- [LLM Wiki](https://llmwiki.eztoolab.com) — AI 知识编译器

:::cta
title: 三分钟产出第一份文档
body: 安装只需一行命令，Markdown DSL 声明内容，引擎渲染 HTML。打开浏览器即可看到排版精良、打印就绪的文档。
button:
  label: 查看使用指南
  href: /guide/
:::
