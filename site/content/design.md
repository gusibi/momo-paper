---
document_type: one_pager
locale: zh-CN
title: 设计系统
description: Momo Paper 是一套路由式设计系统。设计令牌集中定义，路由规则自动分发到 15 种文档类型——你只需关注内容，排版和视觉一致性由系统保证。
---

设计系统的核心是一个简单但强大的思想：约束即解放。当你不需要在每次创建文档时重新决定颜色、字体、间距和排版规则，创造力的门槛就降到了最低。以下是在所有组件中自动生效的设计令牌和视觉原则。本站点提供 **Momo Paper** 与 **Vercel** 两套主题，共享同一组 `--mp-*` 变量名，可在右上角一键切换。

## 色彩系统

所有颜色都定义为 `--mp-*` CSS 自定义属性。背景/文字使用中性色，品牌色为强调色，辅助强调用于次级高亮，语义色用于状态标识。同一组变量名在两套主题下取不同的值，因此切换主题即可整体重着色。

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

三套字体系列。衬线体用于标题，传达正式感和权威性；无衬线体用于正文，保证屏幕可读性；等宽体用于数据、标签和代码。

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

- **Display 衬线体 · 标题**：Noto Serif SC · Source Han Serif SC · Songti SC，用于「让每一份文档都有设计感」这类标题。
- **Body 无衬线体 · 正文**：Inter · Noto Sans SC · PingFang SC，用于正文与 UI 文字，保证屏幕可读性。
- **Mono 等宽体 · 代码和数据**：IBM Plex Mono · SFMono-Regular，用于命令、标签和数据。

## 间距与布局

布局以 `--mp-max`（页面最大宽度）和 `--mp-reading`（正文最佳阅读行宽）为基准，确保所有文档的呼吸感一致。section 内边距使用 `clamp()` 实现响应式留白，无需为不同屏幕单独调整。

```css
--mp-max: 1120px;       /* 页面最大宽度 */
--mp-reading: 760px;    /* 正文最佳阅读行宽 */

/* 阴影层级 */
--mp-shadow-raised: 0 1px 3px rgba(23, 32, 51, 0.06);
--mp-shadow-overlay: 0 4px 12px -2px rgba(23, 32, 51, 0.08);

/* 动效 */
--mp-ease: cubic-bezier(0.2, 0, 0, 1);
--mp-dur-standard: 200ms;
```

## 设计哲学

Momo Paper 的设计原则源于对「AI 时代文档应该长什么样」的思考。当内容由人机协作产出，设计系统需要同时服务两个受众：人类创作者和 AI agent。

:::feature-grid
columns: 2
items:
  - title: 路由即设计
    desc: 声明 document_type，引擎自动选择令牌和校验规则。这不是「选择一个样式」，而是「声明你的内容是什么类型」——排版系统据此做出全部设计决策，让非设计师也能产出专业排版。
  - title: 约束即解放
    desc: 传统文档工具给了用户无限自由，但这些自由变成了认知负担。Momo Paper 反其道而行：提供精心调校的约束，让用户（和 AI）不再做排版决策，专注于内容本身。
  - title: 屏幕即纸张
    desc: 同一份 HTML 在屏幕和纸张上都应该表现一致。所有样式内置 @media print 规则，自动处理背景色、页边距和跨页断裂。这是设计的起点而非终点。
  - title: DSL 作为中间语言
    desc: Markdown DSL 是内容的结构化表达，HTML 是内容的视觉呈现。将两者分离意味着 AI agent 只需产出结构化 DSL（它的强项），引擎负责视觉呈现（模板的强项）。
  - title: 可编程但可读
    desc: 设计令牌和主题都是可编程的（修改 --mp-* 变量、提供自定义 CSS），但系统默认的「出厂设置」已经足够好。目标是让 80% 的用户不需要自定义任何东西。
  - title: 中英文一等公民
    desc: Momo Paper 从第一天起就将中英文作为平等的设计目标：中文字符的内置 serif 字体经过 CJK 排版调校，页面语言按 locale 自动切换。
:::
