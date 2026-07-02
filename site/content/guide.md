---
document_type: long_doc
locale: zh-CN
title: Agent 使用手册
description: 为什么不要让 Agent 直接写 HTML、Momo DSL 如何省 token、在 Agent 中安装与调用、validate → render 闭环，以及真实 token 对比。
---

这份手册写给让 AI Agent 生成文档的人。核心观点一句话：**Agent 不应该手写 HTML，应该写紧凑的 Markdown DSL，再由 Momo Paper 渲染成 HTML。**

## 01 · 为什么不要让 Agent 直接写 HTML

让 Agent 直接输出 HTML 看似可行，实际有三个痛点：

:::comparison
title: Agent 手写 HTML vs 写 Momo DSL
left:
  title: Agent 手写 HTML/CSS
  items:
    - token 占用大，CSS 在每份文档里反复输出
    - 样式随 prompt 漂移，每次生成结果不一致
    - 修改成本高，改一处往往要重写一段结构
    - 无法校验，出错只能人工排查
right:
  title: Agent 写 Momo DSL
  items:
    - 紧凑的结构化块，token 更省
    - 渲染器补全 HTML/CSS，样式始终稳定
    - 改字段即改文档，修改成本低
    - momo2 validate 校验语法与元数据
:::

HTML 是给浏览器的渲染目标，不是给 Agent 的书写格式。让 Agent 写 HTML，等于让它每次都重新发明一遍样式系统——又费 token，又不稳定。

## 02 · Momo DSL 如何节省 token

Momo Paper 把「内容声明」和「样式补全」分开：

- **Agent 只写 DSL**：frontmatter 元数据 + Markdown 散文 + `:::block` 结构化块。这是 Agent 实际输出的 token。
- **渲染器补全 HTML/CSS**：主题 CSS 是固定资产，跨所有文档复用，不占 Agent 的输出 token。

所以省 token 的来源不是魔法，而是把重复的样式声明从 Agent 输出里移走，交给渲染器。

:::callout
tone: insight
title: 两种口径，别混
body: 对比 token 节省时有两个口径。body-based：DSL vs Agent 手写时会输出的 HTML 主体标记——这是每份文档真正省下的。vs-total：DSL vs 含主题 CSS 的完整 HTML——这个数字更大，但 CSS 是跨文档复用的固定成本，不该算进单份文档的节省。下面的真实对比两个口径都给。
:::

## 03 · 在 Agent 中使用

Momo Paper 的 skill 是**一份平台无关的 `SKILL.md`**——skill 本质是一段文本，不分平台，Claude Code、Codex、自研 Agent 读的是同一份文件。区别只在 skill 目录装在哪、由谁触发。

### Claude Code Skill（推荐）

把 `momo-paper-skill/` 目录放到 Claude Code 扫描的 skills 路径，例如 `~/.claude/skills/momo-paper/` 或项目内 `.claude/skills/momo-paper/`。Claude Code 读 `SKILL.md` 的 `description` 决定何时触发，触发后调用自带的 `momo` wrapper：

```bash
"$SKILL_DIR/momo" validate input.md
"$SKILL_DIR/momo" render  input.md -o output.html
```

skill 自带完整 `runtime/`，**无需 `pip install`**。wrapper 通过 `BASH_SOURCE` 自定位，无硬编码路径。唯一要求是 `python3 >= 3.10`。

### 手动 CLI

偏好命令行或要接入 CI/CD 时，直接安装引擎（Python 3.10+）：

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e .

momo2 validate examples/landing.md
momo2 render  examples/landing.md -o dist/landing.html
```

### 自研 Agent

skill 自带的 `momo` 是个普通 bash 脚本，从你的 Agent 工具层调用即可。由你的 Agent 决定何时触发（用 `SKILL.md` 的 `description` 作为触发判据）：

```bash
SKILL_DIR=/absolute/path/to/momo-paper-skill
"$SKILL_DIR/momo" validate input.md
"$SKILL_DIR/momo" render  input.md -o output.html
"$SKILL_DIR/momo" bench   input.md
```

Codex 等其他 Agent 平台读的是同一份 `SKILL.md`，只是 skill 目录位置按各自约定放置。

## 04 · validate → render 闭环

Agent 集成最怕生成失败后不知道怎么修。Momo Paper 的做法是**结构化错误 + Agent 自修**：

```bash
# 1. 校验，失败时输出结构化 JSON
momo2 validate report.md --json
```

失败时返回：

```json
{
  "ok": false,
  "errors": [
    {
      "message": "invalid block tag name",
      "path": "report.md",
      "line": 42,
      "block": "chart"
    }
  ]
}
```

Agent 读 `line` 和 `block` 定位问题，改 DSL 后重新校验。通过后渲染：

```bash
# 2. 渲染为单文件 HTML（CSS 内联）
momo2 render report.md -o report.html
```

:::callout
tone: insight
title: 为什么没有 momo repair 命令
body: 半结构化 DSL 的修复本质是 LLM 的活——该由 Agent 读 validate --json 的错误后自己改，而不是让 CLI 猜怎么改。确定性 repair 对这种输入不现实，也容易改错。结构化错误 + Agent 自修才是稳定闭环。
:::

## 05 · 真实 token 对比

以下数字由 `momo2 bench` 实测生成，可复现。tokenizer 默认用 tiktoken（未安装时回退到 chars/4 估算并标注）。

:::stats
items:
  - value: 81.1%
    label: 投资报告 body 节省
  - value: 70.9%
    label: 落地页 body 节省
  - value: 20,020
    label: 主题 CSS（跨文档复用）
:::

| 文档 | DSL token | HTML 主体 token | 每文档节省 | vs 完整 HTML |
| --- | --- | --- | --- | --- |
| 投资报告（equity-report） | 1,497 | 7,927 | 81.1% | 94.6% |
| 落地页（landing） | 534 | 1,837 | 70.9% | 97.6% |

「每文档节省」是 DSL vs Agent 手写时会输出的 HTML 主体标记——这是单份文档真正省下的。「vs 完整 HTML」含主题 CSS，数字更大但 CSS 是跨文档复用的固定成本。自己复现：

```bash
momo2 bench examples/equity-report.md
momo2 bench examples/equity-report.md --json
```

## 06 · 常见模板

引擎本身是通用渲染器，不按类型校验结构。`document_type` 是语义标签，引导选模板。常见起点见[示例画廊](/demo/)，全部组件与 DSL 源码见[组件目录](/components/)。

:::cta
title: 让 Agent 生成第一份文档
body: 告诉 Agent 想要什么文档，Skill 自动生成 Markdown DSL 并渲染为单文件 HTML——比手写 HTML 省 token、样式稳定、可校验。
button:
  label: 浏览示例画廊
  href: /demo/
:::
