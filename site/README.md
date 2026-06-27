# Momo Paper 产品站点

Momo Paper 的产品官网（https://momo.eztoolab.com）。站点本身用 Momo Paper 2.0 的 **Markdown DSL** 引擎渲染——既是产品介绍，也是引擎能力的自举演示。

每个页面是一个 Markdown DSL 文件，构建脚本通过 `momo_dsl` 解析渲染，再套上共享的导航、页脚、SEO 元数据和双主题切换。

## 快速开始

```bash
# 在仓库根目录执行
python site/build.py                                   # 构建到 site/output/
python3 -m http.server 8765 --directory site/output    # 本地预览
# 打开 http://localhost:8765/
```

> 也可以用 `.claude/launch.json` 里的 `site` 配置一键起预览服务器。

## 目录结构

```
site/
├── build.py          # 构建脚本：解析 DSL → 组装整页 HTML → 生成 SEO 文件
├── site.css          # 站点 chrome 样式（导航/页脚/主题切换器），用 --mp-* 变量
├── content/          # 页面源文件（Markdown DSL），每个文件 = 一个页面
│   ├── index.md          # 首页
│   ├── guide.md          # 使用指南
│   ├── components.md     # 组件目录
│   ├── demo.md           # 示例画廊（索引）
│   ├── charts.md         # 图表演示
│   ├── faq.md            # 常见问题
│   ├── design.md         # 设计系统
│   └── demo/             # 15 份文档样板的 demo 子页
│       ├── one-pager.md
│       ├── equity-report.md
│       └── ...
└── output/           # 构建产物（不要手改；每次构建会重建）
    ├── index.html, guide/index.html, ...
    ├── assets/           # momo-paper.css · vercel.css · site.css
    ├── robots.txt · sitemap.xml · llms.txt
```

## 工作原理

构建脚本 [`build.py`](build.py) 对 `PAGES` 列表里的每个页面：

1. **解析** `content/*.md` —— 调用 `momo_dsl.parser.parse_file`，得到 frontmatter + 节点（Markdown 段落 + `:::block` 结构块）。
2. **渲染正文** —— 复用 `momo_dsl.renderer` 把节点转成 HTML 区块；按需注入 ECharts（含 chart 块时）和代码高亮（含围栏代码时）运行时。
3. **组装整页** —— 套上导航、文档页头、页脚，注入 `<meta>`、Open Graph、JSON-LD 结构化数据。
4. **写出** 到 `output/<url_path>`。

最后生成 `robots.txt`、`sitemap.xml`、`llms.txt`（AI 可见性）。

## 页面清单

| 页面 | 源文件 | URL | document_type |
|------|--------|-----|---------------|
| 首页 | `content/index.md` | `/` | landing |
| 使用指南 | `content/guide.md` | `/guide/` | long_doc |
| 组件目录 | `content/components.md` | `/components/` | long_doc |
| 示例画廊 | `content/demo.md` | `/demo/` | one_pager |
| 图表演示 | `content/charts.md` | `/charts/` | stats_report |
| 常见问题 | `content/faq.md` | `/faq/` | faq_page |
| 设计系统 | `content/design.md` | `/design/` | one_pager |
| 15 个 demo 子页 | `content/demo/*.md` | `/demo/<slug>/` | 对应类型 |

15 个 demo 子页对应 15 份文档样板：one-pager、long-doc、letter、portfolio、resume、slides、equity-report、changelog、process-flow、timeline、faq-page、case-study、research-summary、stats-report、infographic。

## 编写页面

每个页面以 frontmatter 开头，正文混用 Markdown 散文与 `:::block` 结构化块：

```md
---
document_type: landing      # 文档语义（landing / long_doc / equity_report ...）
locale: zh-CN
title: 页面标题             # 用于 <title>、页头 <h1> 和 SEO
description: 页面摘要         # 用于 meta description 和页头副标题
show_header: false          # 可选：landing 类页面用 hero 时关掉默认文档页头
---

## 普通 Markdown 标题

正文段落，支持 **加粗**、`代码`、[链接](/guide/)、列表、表格、围栏代码块。

:::hero
title: 结构化块用 :::tag 声明
subtitle: 块以独立一行的 ::: 结束
:::
```

常用块：`hero` `feature-grid` `card-grid` `comparison` `stats` `cta` `steps`
`timeline` `kpi-row` `callout` `faq` `slide`，以及图表块 `bar-chart` `line-chart`
`donut-chart` `candlestick-chart` `waterfall-chart`。完整块参考见仓库
`examples/reference.md` 和 `examples/components.md`。

### 新增一个页面

1. 在 `content/` 下新建 `.md` 文件。
2. 在 `build.py` 的 `PAGES` 里加一行 `(content_file, url_path, page_id)`。
3. 如需出现在顶部导航，往 `NAV_ITEMS` 加一项；如需自定义 SEO 描述/schema 类型，往 `PAGE_META` 加一项。
4. 重新运行 `python site/build.py`。

## 双主题

站点内置两套视觉系统，右上角切换器即时切换、`localStorage` 记忆：

| 主题 | 样式表 | 风格 |
|------|--------|------|
| Momo Paper（默认） | `momo_dsl/styles/momo-paper.css` | 暖调中性 + 品牌蓝 |
| Vercel | `momo_dsl/styles/vercel.css` | Geist 极简（含暗色） |

两套样式表共用同一组 `--mp-*` 变量名和选择器，所以同一份 HTML 标记无需改动即可整体重着色。实现方式：两个 `<link>` 都注入页面，非激活的那个用 `media="not all"` 静默，切换时翻转 `media` 属性（详见 `build.py` 的 `THEME_BOOT_SCRIPT`）。站点 chrome（导航/页脚）和图表配色都从这些变量取值，自动跟随主题。

> 想加第三套主题：把 CSS 放进 `momo_dsl/styles/`，在 `build.py` 的 `THEMES` 列表加一项即可。

## 部署

`output/` 是纯静态文件，可直接部署到 Cloudflare Pages / Vercel / 任意静态托管。构建命令 `python site/build.py`，发布目录 `site/output`。

## 常见问题

**改了内容页面没更新？** `output/` 是构建产物，不会自动同步。每次改完 `content/` 或 `site.css` 都要重新跑 `python site/build.py`。

**图表/代码高亮不显示？** 图表（ECharts）和代码高亮（highlight.js）走 CDN（npmmirror 镜像），仅在页面含 chart 块或围栏代码时才注入。需要联网；离线预览时图表区域会留空。

**主题切换没反应 / 有闪烁？** 切换逻辑依赖 `output/assets/` 下的两个主题 CSS 与 `site.css`。确认它们存在（构建会自动拷贝）。首屏主题由 `<head>` 内联脚本在渲染前根据 `localStorage` 设定，正常不会闪烁。

**想加新的结构块？** DSL 解析器接受任意合法 `:::tag-name`，未知块会以通用 `data-block` 形式渲染。要让它有专属样式，在主题 CSS 里加 `[data-block="your-tag"]` 规则即可（参考 `momo_dsl/styles/momo-paper.css`）。

**端口被占用？** 换一个端口：`python3 -m http.server 8080 --directory site/output`。
