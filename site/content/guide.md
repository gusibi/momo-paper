---
document_type: long_doc
locale: zh-CN
title: Agent 使用手册
description: Agent 文档编译器使用手册：Schema 发现、strict/free 校验、Agent 自修、HTML/PDF 渲染与真实 token A/B 方法。
---

这份手册写给让 AI Agent 生成正式文档的人。核心观点一句话：**Agent 生成结构化 DSL，Momo Paper 用 Schema 校验并编译为 HTML/PDF。**

## 00 · 最快试用

Python 3.10+ 环境中运行内置研报示例：

```bash
git clone https://github.com/gusibi/momo-paper.git
cd momo-paper
python3 -m venv .venv && source .venv/bin/activate
pip install -e .
momo schema list
momo validate examples/research-summary.md --schema research-summary --json
momo render examples/research-summary.md --schema research-summary -o dist/research-summary.html
```

成功后打开 `dist/research-summary.html`。如果只想先看结果，可以浏览[正式研究摘要](/demo/research-summary/)和[深度研究报告](/demo/deep-research/)；如果使用 Agent Skill，可以跳到第 03 节。

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
    - momo validate 校验模板契约并一次返回全部问题
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
body: `momo bench` 默认给两个工程估算。body-based 比较 DSL 与渲染器生成的 HTML 主体标记；vs-total 还包含固定主题 CSS。两者都不是 Agent 直接生成 HTML 的受控实验结果。要证明真实 Agent token 收益，必须提供独立生成的 HTML baseline，并记录模型 API usage。
:::

## 03 · 在 Agent 中使用

Momo Paper 的 skill 是**一份平台无关的 `SKILL.md`**——skill 本质是一段文本，不分平台，Claude Code、Codex、自研 Agent 读的是同一份文件。区别只在 skill 目录装在哪、由谁触发。

### Claude Code Skill（推荐）

把 `momo-paper-skill/` 目录放到 Claude Code 扫描的 skills 路径，例如 `~/.claude/skills/momo-paper/` 或项目内 `.claude/skills/momo-paper/`。Claude Code 读 `SKILL.md` 的 `description` 决定何时触发，触发后调用自带的 `momo` wrapper：

```bash
"$SKILL_DIR/momo" validate input.md --schema research-summary --json
"$SKILL_DIR/momo" render  input.md --schema research-summary -o output.html
```

skill 自带完整 `runtime/`，**无需 `pip install`**。wrapper 通过 `BASH_SOURCE` 自定位，无硬编码路径。唯一要求是 `python3 >= 3.10`。

### 手动 CLI

偏好命令行或要接入 CI/CD 时，直接安装引擎（Python 3.10+）：

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e .

momo validate examples/landing-page.md --schema landing-page --json
momo render  examples/landing-page.md --schema landing-page -o dist/landing-page.html
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

## 04 · Schema → validate → render 闭环

Agent 集成最怕生成失败后不知道怎么修。Momo Paper 的做法是**按需发现 Schema + 聚合结构化错误 + Agent 自修**：

```bash
# 1. 查看正式模板
momo schema list
momo schema describe research-summary

# 2. 用选定契约严格校验，并获取 Agent 可消费的 JSON 错误
momo validate report.md --schema research-summary --json
```

失败时返回：

```json
{
  "ok": false,
  "schema": "research-summary",
  "mode": "strict",
  "errors": [
    {
      "code": "unresolved_citation",
      "message": "citation does not resolve to a source id: missing-source",
      "path": "report.md",
      "line": 42,
      "block": "key-findings",
      "field": "items[0].citations[0]"
    }
  ],
  "warnings": []
}
```

Agent 读 `code`、`path`、`line`、`block` 和 `field` 定位问题，修复全部错误后用同一 Schema 重新校验。正式交付物必须显式指定契约；未注册类型才进入 free mode 并给出 warning。`render --schema` 同样会拒绝未通过语义校验的正式文档。通过后渲染：

```bash
# 3. 渲染为单文件 HTML（CSS 内联）
momo render report.md --schema research-summary -o report.html
```

:::callout
tone: insight
title: 为什么没有 momo repair 命令
body: 半结构化 DSL 的修复本质是 LLM 的活——该由 Agent 读 validate --json 的错误后自己改，而不是让 CLI 猜怎么改。确定性 repair 对这种输入不现实，也容易改错。结构化错误 + Agent 自修才是稳定闭环。
:::

## 05 · 可复现的 token 工程估算

以下数字由 `momo bench` 对 DSL 和渲染器输出计数，可复现。它们说明结构压缩比例，不代表 Agent 直接生成同等质量 HTML 时一定节省相同比例。tokenizer 默认用 tiktoken（未安装时回退到 chars/4 估算并标注）。

:::stats
items:
  - value: 81.1%
    label: 投资报告结构压缩估算
  - value: 70.9%
    label: 落地页结构压缩估算
  - value: 20,020
    label: 主题 CSS（跨文档复用）
:::

| 文档 | DSL token | 渲染后 HTML 主体 token | 结构压缩估算 | vs 完整 HTML |
| --- | --- | --- | --- | --- |
| 投资报告（equity-report） | 1,497 | 7,927 | 81.1% | 94.6% |
| 落地页（landing） | 534 | 1,837 | 70.9% | 97.6% |

「结构压缩估算」比较 DSL 与渲染器生成的 HTML 主体标记。「vs 完整 HTML」还含主题 CSS，因此不能作为 Agent 输出节省量。自己复现工程估算：

```bash
momo bench examples/equity-report.md
momo bench examples/equity-report.md --json
```

如果已有同一任务独立生成的 HTML 基线，可运行：

```bash
momo bench examples/equity-report.md --baseline-html benchmarks/equity/direct.html --json
```

公开对比前应固定模型与任务、重复运行并保存原始输出；完整方法见仓库的 `docs/benchmark-protocol.md`。

## 06 · 正式模板与实验模式

当前正式 Schema 模板是 `landing-page`、`research-summary` 和 `deep-research`。它们会校验文档级组成、block 字段、顺序、出现次数和研究引用关系。Skill 中的模板 reference 由同一份机器 Schema 自动生成。

未注册的 `document_type` 进入 experimental/free mode：仍校验通用 frontmatter，并保留任意合法 block 的通用渲染。这样新模板可以先探索，再在结构稳定后升级为正式契约。完整列表和成品见[正式模板与实验示例](/demo/)，开放 block 参考见[组件目录](/components/)。

:::cta
title: 让 Agent 生成第一份文档
body: 告诉 Agent 想要什么文档，Skill 自动生成 Markdown DSL 并渲染为单文件 HTML——比手写 HTML 省 token、样式稳定、可校验。
button:
  label: 浏览示例画廊
  href: /demo/
:::
