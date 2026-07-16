---
document_type: landing-page
locale: zh-CN
title: Momo Paper — AI Agent 的文档编译器
description: AI Agent 的文档编译器。Agent 生成紧凑、可验证的 Markdown DSL，Momo Paper 编译成品牌一致、打印就绪的 HTML 与 PDF。
show_header: false
---

:::hero
eyebrow: Agent-native Document Compiler · 2.1
title: AI Agent 的文档编译器
subtitle: Agent 生成紧凑、可验证的 Markdown DSL；Momo Paper 负责 Schema 校验、主题渲染，并输出品牌一致的 HTML 与 PDF。这个官网本身就是通过 landing-page 契约构建的第一个正式模板。
primary_cta:
  label: 在 GitHub 立即试用
  href: https://github.com/gusibi/momo-paper#quick-start
secondary_cta:
  label: 查看正式模板
  href: /demo/research-summary/
:::

## 五分钟跑出第一份报告

无需账号或服务端。Python 3.10+ 环境中克隆仓库，运行内置的研报示例：

```bash
git clone https://github.com/gusibi/momo-paper.git
cd momo-paper
python3 -m venv .venv && source .venv/bin/activate
pip install -e .
momo schema list
momo validate examples/landing-page.md --json
momo render examples/landing-page.md -o dist/landing-page.html
```

先看[正式研究摘要](/demo/research-summary/)和[深度研究报告](/demo/deep-research/)，再让 Agent 按对应 Schema 生成自己的文档。Skill 用户可以直接调用仓库内自带的 `momo-paper-skill/momo`，无需安装 Python package。

:::comparison
title: 为什么 Agent 输出应该被编译
left:
  title: Agent 手写 HTML/CSS
  items:
    - token 占用大，CSS 反复重复输出
    - 样式随 prompt 漂移，每次结果不一致
    - 修改成本高，改一处往往要重写一段
    - 无法校验，出错只能人工排查
right:
  title: Agent 写 Momo DSL
  items:
    - 紧凑的结构化块，token 更省
    - 渲染器补全 HTML/CSS，样式始终稳定
    - 改字段即改文档，修改成本低
    - momo validate 返回全部 Schema 错误与字段路径
:::

## 引擎实际提供什么

Momo Paper 的能力分三层：正式模板契约负责稳定结构，开放 DSL 负责实验扩展，主题与渲染器负责最终视觉。组合后既能可靠生成正式文档，也不会丢失尚未注册的新 block。

:::feature-grid
columns: 3
items:
  - title: 正式 Schema 契约
    desc: landing-page、research-summary 与 deep-research 定义必需章节、字段类型、顺序和引用关系；构建失败时返回全部结构化错误。
  - title: Experimental Free Mode
    desc: 未注册的文档类型仍可解析和渲染，未知 block 与字段不会被丢弃，适合快速探索新模板。
  - title: 引用完整性
    desc: 研究模板支持 source ID 与 citations，validate 会发现重复来源和未解析引用。
  - title: 双主题令牌
    desc: Momo Paper 暖调与 Vercel 极简两套主题共享 --mp-* 变量，正式模板和实验文档都可切换。
  - title: HTML 与 PDF
    desc: 默认输出单文件 HTML，并可通过 Playwright 打印为 PDF；输出格式与 Agent 内容生成解耦。
  - title: Skill-first 工作流
    desc: Agent 按需读取模板 Schema，执行 validate → 自修复 → render；CLI 是 Skill 的执行后端。
:::

## 用 Skill 使用

Skill 自动选择文档样板、构造 DSL、调用引擎渲染并预览。Agent 只需描述想要的文档，Skill 负责校验、渲染、落地——无需手动跑命令，也无需编辑 HTML。

- 自然语言驱动，自动构造 DSL
- 自动选择样板与组件
- 校验通过后渲染单文件 HTML

:::stats
items:
  - value: 3
    label: 正式 Schema 模板
  - value: strict
    label: validate 聚合校验
  - value: free
    label: 实验文档兼容模式
:::

## 探索更多

- [正式研究摘要](/demo/research-summary/) — strict Schema：研究问题、发现、影响、方法与来源
- [深度研究报告](/demo/deep-research/) — strict Schema：执行摘要、证据、反方观点、建议与引用
- [研报 / 估值分析](/demo/equity-report/) — experimental/free 示例：KPI、K 线图、估值与风险矩阵
- [组件目录](/components/) — 全部组件的渲染效果与 DSL 源码
- [图表演示](/charts/) — 5 种图表块的交互示例
- [示例画廊](/demo/) — 15 份样板的结构说明与完整渲染示例
- [设计系统](/design/) — 色彩、字体、间距令牌与设计哲学

:::cta
title: 用一个真实任务生成第一份文档
body: 从研报示例开始，把内容换成自己的研究材料；遇到第一处阻塞时，请在 GitHub 提交 issue。真实任务反馈比功能清单更重要。
button:
  label: 打开 GitHub Quick Start
  href: https://github.com/gusibi/momo-paper#quick-start
:::
