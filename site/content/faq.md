---
document_type: faq_page
locale: zh-CN
title: 常见问题
description: 关于 Momo Paper 的安装、使用和设计理念，这里有最常被问到的问题和解答。
---

Momo Paper 是一个路由式设计系统，将文档排版从「手工调 CSS」升级为「声明式路由」。以下是最常见的问题，按主题分组，帮助你快速找到答案。

如果你在这里没找到答案，欢迎在 GitHub 提交 Issue 或查看仓库内的详细文档。

## 快速入门

:::faq
items:
  - question: Momo Paper 是什么？
    answer: Momo Paper 是一个面向文档与视觉叙事的开源设计系统。它提供 15 种文档类型、一个 Markdown DSL 渲染引擎和 14 种图示原语。你可以直接编辑 HTML 模板，也可以通过 DSL 驱动渲染——两种方式输出排版精良、打印就绪的 HTML 文档。
  - question: 需要什么前置条件？
    answer: 如果你只使用直接 HTML 模板，不需要任何前置条件——打开文件、编辑内容、在浏览器中打开即可。如果要使用 DSL 渲染引擎，需要 Python 3.10+。
  - question: 如何安装 DSL 引擎？
    answer: 在仓库根目录运行 pip install -e . 即可。安装后你会获得 momo2 命令，输入 momo2 --help 查看用法，momo2 validate 校验 DSL，momo2 render 渲染 HTML。
  - question: 可以在 AI agent 中使用吗？
    answer: 可以。Momo Paper 提供了 Claude Code Skill 定义（SKILL.md），AI agent 通过 bash 直接调用 momo2 CLI 命令即可生成文档。当前实际可用的集成路径是 Skill + CLI 模式。
:::

## 引擎使用

:::faq
items:
  - question: 如何选择文档类型？
    answer: 根据你的内容需求选择：商业方案用 one_pager，深度长文用 long_doc，正式信函用 letter，简历用 resume，金融研报用 equity_report，数据报告用 stats_report，演示用 slides。完整列表见文档类型页面。
  - question: Markdown DSL 的结构是什么？
    answer: 每个文档以 frontmatter 开头（document_type、locale、title、description），正文混合使用 Markdown 散文和 :::block 结构化块，块以 ::: 结束。每种类型的结构由对应的块约定描述。
  - question: 如何嵌入图表？
    answer: 在正文中声明 chart 块，例如 :::bar-chart 后跟 title 与 items 列表，块以 ::: 结束。引擎自动将其渲染为交互式图表。支持 bar、line、donut、candlestick 和 waterfall 五种类型。
  - question: 支持哪些语言？
    answer: 目前支持 zh-CN（中文）和 en（英文）两种 locale。locale 字段控制页面语言和排版的自动切换。中英文各有完整模板。
  - question: 如何批量渲染？
    answer: 你可以编写脚本循环调用 momo2 render，或直接调用 momo_dsl 的 parse_file 和 render_html API。本站点的 site/build.py 就是一个批量渲染多页站点的完整示例。
:::

## 设计与定制

:::faq
items:
  - question: 设计令牌是如何工作的？
    answer: 所有颜色、字体、间距等视觉属性都定义在样式表的 :root CSS 自定义属性（--mp-* 变量）中。每个组件通过这些变量取色，因此修改一处令牌即可全局生效。本站点提供 Momo Paper 与 Vercel 两套主题，共享同一组变量名。
  - question: 可以自定义主题吗？
    answer: 可以。引擎的 render 命令支持 --css 参数指定任意样式文件。你可以复制内置主题，修改 --mp-* 变量值创建自己的主题，markup 完全不变即可重新着色。
  - question: 文档支持打印吗？
    answer: 所有样式都内置了 @media print 规则。打印时会自动移除背景色、调整页边距、避免内容跨页断裂。这是 Momo Paper 的核心设计原则之一——你不需要为打印单独准备文档。
  - question: 和传统的文档工具（Word/LaTeX/Notion）有什么区别？
    answer: Momo Paper 的定位是「文档生成引擎」，而非编辑器。它的优势在于：输出是标准 HTML/CSS（任何浏览器都能打开），设计令牌确保视觉一致性，Markdown DSL 作为中间格式让 AI agent 可以结构化生成内容，打印安全内置无需额外处理。适合需要批量生成或 AI 辅助生成的场景。
:::

:::footer-note
title: 持续演进
body: Momo Paper 正在持续演进中。当前的 15 种文档类型覆盖了大多数商业和个人文档场景。如果你有新的文档类型建议或功能需求，欢迎在 github.com/gusibi/momo-paper 参与贡献。
:::
