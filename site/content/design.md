---
document_type: one_pager
locale: zh-CN
title: 设计系统
description: Momo Paper 的视觉属性集中在 --mp-* CSS 变量中，组件通过变量取色，修改一处即全局生效。两套主题共享变量名，可一键切换。
---

设计系统的核心是约束即解放。颜色、字体、间距等视觉属性集中在 `--mp-*` CSS 自定义属性中，组件通过变量取色，因此修改一处令牌即全局生效，无需逐处调整。本站提供 **Momo Paper** 与 **Vercel** 两套主题，共享同一组变量名，可在右上角一键切换。

## 色彩系统

所有颜色定义为 `--mp-*` CSS 自定义属性。背景与文字用中性色，品牌色为强调色，辅助强调用于次级高亮，语义色用于状态标识。同一组变量名在两套主题下取不同值，切换主题即整体重着色。

| 令牌 | 变量 | Momo Paper | Vercel |
|------|------|-----------|--------|
| 主文字 | `--mp-ink` | #172033 | #171717 |
| 次级文字 | `--mp-ink-subtle` | #4c566a | #4d4d4d |
| 页面背景 | `--mp-canvas` | #f2efe8 | #fafafa |
| 卡片表面 | `--mp-surface` | #faf8f4 | #ffffff |
| 分隔线 | `--mp-line` | #d8d2c4 | #ebebeb |
| 品牌色 | `--mp-brand` | #244c7a | #006bff |
| 辅助强调 | `--mp-accent` | #b65c3a | #7d00cc |
| 成功 | `--mp-success` | #2f6b4f | #28a948 |
| 警告 | `--mp-warning` | #a46a21 | #aa4d00 |
| 危险 | `--mp-danger` | #9a3d3d | #ea001d |

```css
:root {
  --mp-ink: #172033;
  --mp-ink-subtle: #4c566a;
  --mp-canvas: #f2efe8;
  --mp-surface: #faf8f4;
  --mp-line: #d8d2c4;
  --mp-brand: #244c7a;     /* 品牌蓝 */
  --mp-accent: #b65c3a;    /* 陶土橙 */
  --mp-success: #2f6b4f;
  --mp-warning: #a46a21;
  --mp-danger: #9a3d3d;
}
```

## 字体系统

三套字体系列，角色不互换：衬线体用于标题与展示，无衬线体用于正文与 UI，等宽体用于数据、标签与代码。

```css
/* Display · 标题 */
--mp-font-display: "Noto Serif SC",
  "Source Han Serif SC", "Songti SC", serif;

/* Body · 正文 & UI */
--mp-font-body: "Inter", "Noto Sans SC",
  "PingFang SC", sans-serif;

/* Mono · 代码 & 数据 */
--mp-font-mono: "IBM Plex Mono",
  "SFMono-Regular", monospace;
```

- **Display 衬线体 · 标题**：Noto Serif SC · Source Han Serif SC · Songti SC，用于页头与正文标题。
- **Body 无衬线体 · 正文**：Inter · Noto Sans SC · PingFang SC，用于正文与 UI 文字。
- **Mono 等宽体 · 代码与数据**：IBM Plex Mono · SFMono-Regular，用于命令、标签与数据。

## 间距与布局

布局以 `--mp-max`（页面最大宽度）与 `--mp-reading`（正文阅读行宽）为基准。section 内边距使用 `clamp()` 实现响应式留白，无需为不同屏幕单独调整。

```css
--mp-max: 1120px;       /* 页面最大宽度 */
--mp-reading: 760px;    /* 正文阅读行宽 */

/* 阴影层级 */
--mp-shadow-raised: 0 1px 3px rgba(23, 32, 51, 0.06);
--mp-shadow-overlay: 0 4px 12px -2px rgba(23, 32, 51, 0.08);

/* 动效 */
--mp-ease: cubic-bezier(0.2, 0, 0, 1);
--mp-dur-standard: 200ms;
```

## 设计哲学

设计原则源于对 AI 时代文档形态的思考。当内容由人机协作产出，设计系统需同时服务人类创作者与 AI agent。

:::feature-grid
columns: 2
items:
  - title: 约束即解放
    desc: 传统文档工具给用户无限自由，自由变成认知负担。Momo Paper 提供调校过的约束，让用户与 AI 不再做排版决策，专注内容本身。
  - title: 屏幕即纸张
    desc: 同一份 HTML 在屏幕与纸张上表现一致。所有样式内置 @media print 规则，自动处理背景色、页边距与跨页断裂。
  - title: DSL 作为中间语言
    desc: Markdown DSL 是内容的结构化表达，HTML 是视觉呈现。两者分离意味着 AI agent 只需产出结构化 DSL，引擎负责视觉呈现。
  - title: 可编程但可读
    desc: 令牌与主题可编程——修改 --mp-* 变量或提供自定义 CSS。但默认出厂已足够好，多数用户无需自定义任何东西。
  - title: 组件由样式表扩展
    desc: 任意 :::tag-name 都渲染为带 data-block 的区块。新组件只需在主题 CSS 中按选择器添加样式，无需改动引擎。
  - title: 中英文一等公民
    desc: 从第一天起将中英文作为平等设计目标。中文字符的 serif 字体经 CJK 排版调校，页面语言按 locale 自动切换。
:::
