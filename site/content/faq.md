---
document_type: faq_page
locale: zh-CN
title: 常见问题
description: 关于 Momo Paper 安装、使用与设计系统的常见问题解答。涵盖 DSL 引擎、AI agent 集成、图表嵌入、主题令牌与打印支持。
---

Momo Paper 是 AI Agent 的文档编译器：Agent 生成 Markdown DSL，正式模板通过 Schema 校验，渲染器输出品牌一致、打印就绪的 HTML/PDF。以下是按主题分组的常见问题。

## 快速入门

:::faq
items:
  - question: Momo Paper 是什么？
    answer: AI Agent 的文档编译器。Agent 生成紧凑 Markdown DSL，正式模板用机器 Schema 校验章节、字段和引用，渲染器输出 HTML/PDF。Token 更少是潜在收益之一，核心价值是结果可验证、可复现且品牌一致。
  - question: 需要什么前置条件？
    answer: 直接编辑 HTML 模板无需任何前置条件，打开文件改内容即可。使用 DSL 引擎需要 Python 3.10+。通过 Claude Code Skill 使用时，Skill 自动处理安装。
  - question: 如何安装 DSL 引擎？
    answer: 在仓库根目录运行 pip install -e .。安装后获得 momo 命令：momo --help 查看用法，momo validate 校验 DSL，momo render 渲染 HTML。旧的 momo2 命令继续作为兼容别名。
  - question: 可以在 AI agent 中使用吗？
    answer: 可以。仓库提供平台无关的 Skill 定义（SKILL.md），Agent 通过自带的 momo wrapper 生成文档。当前实际可用的集成路径是 Skill + CLI。
:::

## 引擎使用

:::faq
items:
  - question: document_type 有什么作用？
    answer: 正式 document_type 会选择对应 Schema，校验文档组成、block 字段、顺序和引用；当前包括 landing-page、research-summary、deep-research。未注册类型进入 experimental/free mode，未知 block 和字段仍可渲染。
  - question: Markdown DSL 的结构是什么？
    answer: 每个文档以 frontmatter 开头（document_type、locale、title、description），正文混排 Markdown 散文与 :::block 结构化块，块以 ::: 结束。语法详见组件目录页。
  - question: 如何嵌入图表？
    answer: 在正文中声明 chart 块，例如 :::bar-chart 后跟 title 与 items 列表，块以 ::: 结束。引擎自动渲染为 echarts 交互图。支持 bar、line、donut、candlestick、waterfall 五种。
  - question: 支持哪些语言？
    answer: 支持 zh-CN 与 en 两种 locale。locale 字段控制页面 lang 属性与排版。中英文各有完整样板。
  - question: 如何批量渲染？
    answer: 编写脚本循环调用 momo render，或直接调用 momo_dsl 的 parse_file 与 render_html API。本站点的 site/build.py 是一个批量渲染多页站点的完整示例。
:::

## 设计与定制

:::faq
items:
  - question: 设计令牌是如何工作的？
    answer: 颜色、字体、间距等视觉属性定义在样式表的 :root CSS 自定义属性（--mp-* 变量）中。组件通过变量取色，修改一处令牌即全局生效。本站提供 Momo Paper 与 Vercel 两套主题，共享同一组变量名。
  - question: 可以自定义主题吗？
    answer: 可以。render 命令支持 --css 参数指定样式文件。复制内置主题，修改 --mp-* 变量即得自定义主题，标记无需改动。
  - question: 文档支持打印吗？
    answer: 所有样式内置 @media print 规则。打印时自动移除背景色、调整页边距、避免内容跨页断裂。无需为打印单独准备文档。
  - question: 与 Word / LaTeX / Notion 有什么区别？
    answer: Momo Paper 是文档生成引擎，而非编辑器。输出是标准 HTML/CSS，任何浏览器可打开；设计令牌保证视觉一致；Markdown DSL 作为中间格式便于 AI agent 结构化生成；打印安全内置。适合批量生成或 AI 辅助生成场景。
:::

:::footer-note
title: 持续演进
body: 当前三个正式 Schema 模板承担兼容承诺，其余页面作为 experimental/free 示例保留。新模板只有在具备机器 Schema、Skill reference、示例与测试后才升级为正式契约。
:::
