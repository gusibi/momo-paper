# Momo Paper 2.0: Markdown DSL Parser

## 结论

Momo Paper 2.0 的核心不是重新做一套组件库，而是做一层标准化转换工具：

```txt
Agent / AI / 人类作者
  -> 生成 Markdown DSL
  -> Momo Paper 解析和校验
  -> 输出标准 standalone HTML
```

也就是说，2.0 只负责“把已经生成好的 DSL 文档解析成 HTML”。DSL 怎么写、用哪些标签、页面是什么内容，由 Agent 或用户输入决定。脚本的职责是：

```txt
1. 解析 frontmatter
2. 解析普通 Markdown
3. 解析 :::tag-name block
4. 校验语法和必要元数据
5. 在出错时告诉 Agent 哪一行哪里错了
6. 把合法 DSL 转成标准 HTML
```

2.0 会和当前功能完全分割，先放在独立 `v2/` 目录中实现。现有 JSON engine、HTML templates、showcase 和旧文档在 2.0 完成前保留，不作为新 runtime 的依赖。

## 不采用的路线

第一期不引入 Markdoc、MDX、Astro、Slidev、Marp 或其他外部页面/演示框架。

第一期也不在 Python 里定义业务组件，例如 `landing.py`、`hero.py`、`feature_grid.py` 这类文件都不应该出现。

原因：

```txt
1. Momo Paper 2.0 需要的是通用 DSL 解析层，不是组件定义层。
2. 组件/标签定义应该来自用户或 Agent 生成的 Markdown DSL。
3. Python runtime 只负责解析、校验、转换 HTML。
4. 如果每个标签都写成 Python 组件，会把系统重新变成模板/组件框架。
```

`dashboard` 不能作为 `document_type`。如果需要 dashboard-like 的视觉，只能作为普通 block tag 或内容结构出现，不能成为公共文档类型。

## DSL 设计原则

### 1. 用户输入定义结构

用户或 Agent 写：

```md
---
document_type: landing
locale: zh-CN
title: AI Agent Sandbox Platform
description: Policy-based runtime for safer AI agents.
---

:::hero
eyebrow: Agent Runtime
title: Run AI agents safely
subtitle: Give agents tools without losing control.
primary_cta:
  label: Start Free
  href: /signup
:::
```

脚本不需要知道 `hero` 是业务组件。它只需要知道：

```txt
1. hero 是一个合法 tag name
2. block body 是合法的 key/value 数据
3. 这些数据可以被转换成 HTML section
```

### 2. 标签是 Agent 写作约定，不是 runtime 组件

文档可以推荐 Agent 使用这些标签：

```txt
hero
section
feature-grid
timeline
comparison
stats
cta
faq
```

但第一期 parser 不应该把它们写死成 Python 组件类。推荐标签的价值是让 Agent 知道“生成 landing 时该怎么组织内容”；runtime 应该保持通用，能解析任意合法 `:::tag-name`。

### 3. Markdown 负责普通内容，block 负责结构化内容

普通标题、段落、列表、强调、链接等内容继续使用 Markdown。复杂结构用 block DSL 表达：

```md
## Why it matters

普通正文继续写 Markdown。

:::feature-grid
columns: 3
items:
  - title: Fast
    desc: Generate pages quickly.
  - title: Stable
    desc: Keep output predictable.
:::
```

### 4. 输出 HTML 应该通用而稳定

每个 block 可以统一渲染为：

```html
<section class="dsl-block" data-block="feature-grid">
  ...
</section>
```

字段、对象和列表按通用规则渲染成可读 HTML。这样第一期可以先验证解析和转换闭环，不需要提前设计每个 block 的视觉组件。

## Phase 1 目录边界

建议目录：

```txt
v2/
  README.md
  pyproject.toml
  momo_dsl/
    __init__.py
    cli.py
    parser.py
    renderer.py
    errors.py
  examples/
    landing.md
  tests/
    test_parser.py
    test_renderer.py
    test_cli.py
```

边界规则：

```txt
1. v2 不调用 scripts/json-engine。
2. v2 不依赖 assets/templates 里的旧 HTML 模板。
3. v2 不包含业务组件目录。
4. v2 输出第一目标是 standalone HTML。
5. 旧功能只在 2.0 完成后再整体迁移或删除。
```

## Phase 1 支持的输入

```txt
frontmatter
普通 Markdown 段落
一级到三级标题
无序列表
有序列表
链接
粗体
斜体
inline code
:::tag-name block
```

## Phase 1 校验规则

Phase 1 必须 fail fast：

```txt
1. 缺少 frontmatter 时失败。
2. frontmatter 格式错误时失败。
3. 缺少 document_type 时失败。
4. document_type 是 dashboard 时失败。
5. 缺少 locale 时失败。
6. 缺少 title 时失败。
7. tag name 不合法时失败。
8. block 未闭合时失败。
9. block 字段格式无法解析时失败。
```

错误信息要尽量包含：

```txt
file path
line number
block name
reason
```

## Agent 标签参考

这些标签只是推荐约定，用于让 Agent 生成更稳定的 landing DSL。parser 不应该依赖这些标签才能工作。

### hero

用于页面开头。

```md
:::hero
eyebrow: Agent Runtime
title: Run AI agents safely
subtitle: Give agents tools without losing control.
primary_cta:
  label: Start Free
  href: /signup
secondary_cta:
  label: View Docs
  href: /docs
:::
```

### section

用于普通内容区。

```md
:::section
title: Why this matters
body: AI should generate structure, not fragile HTML.
:::
```

### feature-grid

用于功能列表。

```md
:::feature-grid
columns: 3
items:
  - title: Policy-first permissions
    desc: Define which actions need approval.
  - title: Stable HTML output
    desc: Convert the same DSL into repeatable HTML.
:::
```

### timeline

用于步骤、流程或路线图。

```md
:::timeline
title: How it works
items:
  - step: 1
    title: Write DSL
    desc: Agent creates Markdown with structured blocks.
  - step: 2
    title: Render HTML
    desc: Momo Paper parses and converts it.
:::
```

### comparison

用于左右对比。

```md
:::comparison
title: Before vs After
left:
  title: Direct HTML
  items:
    - Hard to validate
    - Easy to drift
right:
  title: Markdown DSL
  items:
    - Easy to parse
    - Stable output
:::
```

### stats

用于关键数字。

```md
:::stats
items:
  - value: 1
    label: Source file
  - value: 100%
    label: HTML generated from DSL
:::
```

### cta

用于行动区。

```md
:::cta
title: Generate the page
button:
  label: Render HTML
  href: /render
:::
```

### faq

用于问答。

```md
:::faq
items:
  - question: Does the runtime define components?
    answer: No. It parses user-defined tags and renders generic HTML.
:::
```

## Phase 1 示例

```md
---
document_type: landing
locale: zh-CN
title: AI Agent Sandbox Platform
description: Policy-based runtime for safer AI agents.
---

:::hero
eyebrow: Agent Runtime
title: Run AI agents safely with policy-based control
subtitle: Give agents tools, files and browser access without losing control.
primary_cta:
  label: Start Free
  href: /signup
:::

## Why DSL

AI should generate structure, not fragile HTML.

:::feature-grid
columns: 3
items:
  - title: Policy-first permissions
    desc: Define which tools can run automatically and which need approval.
  - title: Isolated runtime
    desc: Run operations inside controlled environments.
  - title: Stable rendering
    desc: Keep HTML output predictable.
:::
```

## 成功标准

Phase 1 完成时应该满足：

```txt
1. 可以用一份 Markdown DSL 生成 standalone HTML。
2. 生成结果不依赖旧 JSON engine。
3. runtime 不定义业务组件。
4. Agent 可以通过 README 知道推荐使用什么标签。
5. 语法错误、frontmatter 错误、block 错误都会 fail fast。
6. CLI 可以 render 和 validate。
7. 代码、示例、测试都在 v2 目录内闭环。
```

## Phase 2

第一期不做：

```txt
1. 严格的业务组件 schema
2. 业务组件 Python 文件
3. 自定义视觉组件库
4. PDF / PPT / PNG 输出
5. chart / diagram 引擎
6. 多主题系统
7. 多文件 include
8. 旧功能迁移和删除
```
