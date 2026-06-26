#!/usr/bin/env python3
"""Build the Momo Paper static product site from Markdown DSL.

Each page is authored as a Momo Paper 2.0 Markdown DSL file under ``content/``.
The build parses every file through ``momo_dsl`` and assembles a full HTML page
with shared navigation, footer, SEO meta tags, JSON-LD structured data, and a
two-theme switcher (Momo Paper / Vercel). Also generates llms.txt,
llms-full.txt, robots.txt and sitemap.xml.

The previous JSON-engine build is preserved in git history; this is the DSL
rewrite. Content was migrated 1:1 from the old ``data/*.json`` files.
"""

import json
import shutil
import sys
from datetime import date
from pathlib import Path

# Make the DSL engine importable without pip install.
ENGINE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ENGINE_DIR))

from momo_dsl import renderer  # noqa: E402
from momo_dsl.parser import BlockNode, MarkdownNode, parse_file  # noqa: E402

SITE_DIR = Path(__file__).resolve().parent
CONTENT_DIR = SITE_DIR / "content"
OUTPUT_DIR = SITE_DIR / "output"
ASSETS_DIR = OUTPUT_DIR / "assets"

BASE_URL = "https://momo.eztoolab.com"
TODAY = date.today().isoformat()

# Two visual systems shipped with the DSL engine. Both stylesheets share the
# same `--mp-*` variables and selectors, so swapping the active <link> retheme
# the whole page instantly.
THEMES = [
    ("momo", "Momo Paper", "momo-paper.css"),
    ("vercel", "Vercel", "vercel.css"),
]
DEFAULT_THEME = "momo"

# (content_file, url_path, page_id)
PAGES = [
    ("index.md", "index.html", "index"),
    ("guide.md", "guide/index.html", "guide"),
    ("types.md", "types/index.html", "types"),
    ("components.md", "components/index.html", "components"),
    ("demo.md", "demo/index.html", "demo"),
    ("charts.md", "charts/index.html", "charts"),
    ("faq.md", "faq/index.html", "faq"),
    ("design.md", "design/index.html", "design"),
    # Demo gallery pages — one per document type.
    ("demo/one-pager.md", "demo/one-pager/index.html", "demo"),
    ("demo/long-doc.md", "demo/long-doc/index.html", "demo"),
    ("demo/letter.md", "demo/letter/index.html", "demo"),
    ("demo/portfolio.md", "demo/portfolio/index.html", "demo"),
    ("demo/resume.md", "demo/resume/index.html", "demo"),
    ("demo/slides.md", "demo/slides/index.html", "demo"),
    ("demo/equity-report.md", "demo/equity-report/index.html", "demo"),
    ("demo/changelog.md", "demo/changelog/index.html", "demo"),
    ("demo/process-flow.md", "demo/process-flow/index.html", "demo"),
    ("demo/timeline.md", "demo/timeline/index.html", "demo"),
    ("demo/faq-page.md", "demo/faq-page/index.html", "demo"),
    ("demo/case-study.md", "demo/case-study/index.html", "demo"),
    ("demo/research-summary.md", "demo/research-summary/index.html", "demo"),
    ("demo/stats-report.md", "demo/stats-report/index.html", "demo"),
    ("demo/infographic.md", "demo/infographic/index.html", "demo"),
]

# Top navigation entries: (url, label, page_id)
NAV_ITEMS = [
    ("/", "首页", "index"),
    ("/guide/", "使用指南", "guide"),
    ("/types/", "文档样板", "types"),
    ("/components/", "组件", "components"),
    ("/demo/", "示例", "demo"),
    ("/charts/", "图表", "charts"),
    ("/faq/", "常见问题", "faq"),
    ("/design/", "设计", "design"),
]

# ---------------------------------------------------------------------------
# Per-page meta descriptions for SEO / AI visibility
# ---------------------------------------------------------------------------
PAGE_META = {
    "index": {
        "description": "Momo Paper 是一个开源的 Markdown DSL 文档引擎，输入 frontmatter 与结构化块，输出排版精良、打印就绪的单文件 HTML。含 5 种图表块、4 种健康块、一组通用结构组件与 15 份文档样板，双主题令牌一键切换。",
        "schema_type": "SoftwareApplication",
    },
    "guide": {
        "description": "Momo Paper 使用指南：推荐通过 Claude Code Skill 自动使用，也支持 CLI 手动渲染和直接 HTML 模板编辑三种工作流。安装、命令参考、Markdown DSL 格式和图表嵌入完整说明。",
        "schema_type": "TechArticle",
    },
    "types": {
        "description": "Momo Paper 15 份文档样板全景：one_pager、long_doc、letter、portfolio、resume、slides、equity_report、changelog、process_flow、timeline、faq_page、case_study、research_summary、stats_report、infographic。",
        "schema_type": "CollectionPage",
    },
    "components": {
        "description": "Momo Paper 组件目录：Markdown 特性、通用结构块、nav、4 种健康块与 5 种图表块的渲染效果与 DSL 源码，可直接复用。",
        "schema_type": "TechArticle",
    },
    "faq": {
        "description": "Momo Paper 常见问题：安装方式、DSL 引擎使用、AI agent 集成、文档类型选择、图表嵌入、设计令牌系统、自定义模板和打印支持等常见问题解答。",
        "schema_type": "FAQPage",
    },
    "design": {
        "description": "Momo Paper 设计系统：色彩系统、字体层级（serif/sans/mono）、间距令牌和设计哲学。所有视觉属性集中定义在 CSS 自定义属性中，模板自动生效。",
        "schema_type": "WebPage",
    },
    "charts": {
        "description": "Momo Paper 交互式图表演示：支持柱状图、折线图、环形图、K 线图和瀑布图 5 种类型，在 DSL 中声明 chart 块自动渲染。",
        "schema_type": "WebPage",
    },
    "demo": {
        "description": "Momo Paper 全部 15 份文档样板的完整渲染示例，涵盖商业方案、白皮书、简历、研报、幻灯片、信息图等场景。",
        "schema_type": "CollectionPage",
    },
}

# Map demo slug to (Chinese name, summary) for Article schema.
DEMO_TYPE_NAMES = {
    "one-pager": ("方案 / 执行摘要", "四段结构：摘要、背景、证据、建议"),
    "long-doc": ("白皮书 / 长文", "可迭代章节 + 引用块 + 结论"),
    "letter": ("信件 / 推荐信", "信头、正文、请求、签名"),
    "portfolio": ("作品集", "案例卡片 + 指标卡"),
    "resume": ("简历 / CV", "经历时间线 + 技能标签"),
    "slides": ("幻灯片 / 演示", "16:9 视口，多种布局"),
    "equity-report": ("研报 / 估值分析", "KPI 卡片 + K 线图 + 风险矩阵"),
    "changelog": ("更新日志", "版本列表，按变更类型分类"),
    "process-flow": ("流程 / SOP", "步骤编号 + 负责人标注"),
    "timeline": ("时间线 / Roadmap", "竖线时间线，三种状态"),
    "faq-page": ("常见问题", "分组问答卡片"),
    "case-study": ("案例拆解", "背景、问题、方案、结果"),
    "research-summary": ("研究摘要", "论题 + 关键发现 + 方法说明"),
    "stats-report": ("数据报告 / KPI", "KPI 大数字 + 趋势折线图"),
    "infographic": ("信息图", "大数字 + 环形图 + 步骤路径"),
}


# ---------------------------------------------------------------------------
# Document rendering
# ---------------------------------------------------------------------------
def render_body(document) -> tuple[str, bool, bool]:
    """Render DSL nodes to HTML; report whether chart / highlight runtimes are needed."""
    nodes = "\n".join(renderer._render_node(node) for node in document.nodes)
    needs_charts = any(
        isinstance(node, BlockNode) and node.name in renderer.CHART_BLOCKS
        for node in document.nodes
    )
    needs_highlight = any(
        isinstance(node, MarkdownNode) and "```" in node.text for node in document.nodes
    )
    return nodes, needs_charts, needs_highlight


def render_doc_header(meta: dict) -> str:
    """Render the standard document header, unless the page opts out.

    Pages that opt out (landing pages whose hero acts as the visual title)
    still emit a single screen-reader-only <h1> so every page has exactly one
    top-level heading for accessibility and SEO.
    """
    if str(meta.get("show_header", "true")).lower() == "false":
        return f'<h1 class="visually-hidden">{_esc(str(meta.get("title", "")))}</h1>'
    title = _esc(str(meta.get("title", "")))
    description = str(meta.get("description", ""))
    doc_type = _esc(str(meta.get("document_type", "")))
    desc_html = f'<p class="description">{_esc(description)}</p>' if description else ""
    return (
        '<header class="doc-header" id="top"><div class="doc-header-inner">'
        f'<div class="doc-type">{doc_type}</div>'
        f"<h1>{title}</h1>{desc_html}"
        "</div></header>"
    )


# ---------------------------------------------------------------------------
# Navigation, footer, theme switcher
# ---------------------------------------------------------------------------
def render_nav(active_page_id: str) -> str:
    links = []
    for url, label, pid in NAV_ITEMS:
        cls = "site-nav-link active" if pid == active_page_id else "site-nav-link"
        links.append(f'<a class="{cls}" href="{url}">{_esc(label)}</a>')

    options = "".join(
        f'<button class="theme-option" data-theme-value="{tid}">{_esc(tname)}</button>'
        for tid, _, tname in [(t[0], t[1], t[1]) for t in THEMES]
    )

    return f"""<nav class="site-nav" id="siteNav">
  <div class="site-nav-inner">
    <a href="/" class="site-nav-brand"><span class="site-nav-mark">M</span>Momo Paper</a>
    <button class="site-nav-burger" id="siteNavBurger" aria-label="Menu"><span></span><span></span><span></span></button>
    <div class="site-nav-links" id="siteNavLinks">
      {"".join(links)}
      <div class="theme-switch" role="group" aria-label="主题切换">{options}</div>
    </div>
  </div>
</nav>"""


def render_footer() -> str:
    return """<footer class="site-footer">
  <div class="site-footer-inner">
    <div class="site-footer-left">
      <span>Momo Paper 2.1</span><span class="dot">&middot;</span>
      <span>MIT License</span><span class="dot">&middot;</span>
      <span>by <a href="https://github.com/gusibi">gusibi</a></span>
    </div>
    <div class="site-footer-right">
      <a href="https://github.com/gusibi/momo-paper">GitHub</a>
      <a href="/components/">组件</a>
      <a href="/guide/">使用指南</a>
      <a href="/types/">文档样板</a>
      <a href="https://eztoolab.com">EZTOLAB</a>
    </div>
  </div>
</footer>"""


def theme_links() -> str:
    """Both theme stylesheets; the inactive one is muted via `media`."""
    out = []
    for tid, _, filename in THEMES:
        active = "all" if tid == DEFAULT_THEME else "not all"
        out.append(
            f'<link rel="stylesheet" id="theme-{tid}" data-theme-id="{tid}" '
            f'href="/assets/{filename}" media="{active}">'
        )
    return "\n  ".join(out)


THEME_BOOT_SCRIPT = f"""<script>
  (function() {{
    var KEY = 'momo-site-theme';
    var DEFAULT = '{DEFAULT_THEME}';
    function apply(theme) {{
      document.querySelectorAll('link[data-theme-id]').forEach(function(link) {{
        link.media = (link.getAttribute('data-theme-id') === theme) ? 'all' : 'not all';
      }});
      document.documentElement.setAttribute('data-site-theme', theme);
    }}
    var stored = localStorage.getItem(KEY) || DEFAULT;
    apply(stored);
    window.__setSiteTheme = function(theme) {{ localStorage.setItem(KEY, theme); apply(theme); }};
  }})();
</script>"""

THEME_UI_SCRIPT = """<script>
  (function() {
    var current = document.documentElement.getAttribute('data-site-theme');
    function sync() {
      current = document.documentElement.getAttribute('data-site-theme');
      document.querySelectorAll('.theme-option').forEach(function(btn) {
        btn.classList.toggle('active', btn.getAttribute('data-theme-value') === current);
      });
    }
    document.querySelectorAll('.theme-option').forEach(function(btn) {
      btn.addEventListener('click', function() {
        window.__setSiteTheme(btn.getAttribute('data-theme-value'));
        sync();
      });
    });
    sync();
    var burger = document.getElementById('siteNavBurger');
    var links = document.getElementById('siteNavLinks');
    if (burger && links) burger.addEventListener('click', function() { links.classList.toggle('open'); });
    var nav = document.getElementById('siteNav');
    if (nav) window.addEventListener('scroll', function() { nav.classList.toggle('scrolled', window.scrollY > 10); });
  })();
</script>"""


# ---------------------------------------------------------------------------
# SEO meta + JSON-LD
# ---------------------------------------------------------------------------
def _esc(s: str) -> str:
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")


def build_page_url(url_path: str) -> str:
    path = url_path.rstrip("/")
    if path == "index.html":
        return BASE_URL + "/"
    return BASE_URL + "/" + path.replace("/index.html", "/")


def build_meta_block(url_path: str, page_id: str, title: str, description: str) -> str:
    page_url = build_page_url(url_path)
    meta_block = f"""<meta name="description" content="{_esc(description)}">
  <link rel="canonical" href="{page_url}">
  <meta property="og:title" content="{_esc(title)}">
  <meta property="og:description" content="{_esc(description)}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{page_url}">
  <meta property="og:site_name" content="Momo Paper">
  <meta property="og:locale" content="zh_CN">
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="{_esc(title)}">
  <meta name="twitter:description" content="{_esc(description)}">"""
    return meta_block + "\n  " + build_jsonld(page_id, url_path, title, description)


def build_jsonld(page_id, url_path, title, description) -> str:
    page_url = build_page_url(url_path)
    schema_type = PAGE_META.get(page_id, {}).get("schema_type", "WebPage")

    if page_id == "demo" and url_path != "demo/index.html":
        slug = url_path.split("/")[1]
        return _wrap_jsonld(_jsonld_demo_article(slug, page_url, title, description))
    if page_id == "index":
        return _wrap_jsonld_multi(_jsonld_software_app(page_url, description))
    if page_id in ("types", "demo"):
        return _wrap_jsonld(_jsonld_collection(page_url, title, description, schema_type))
    return _wrap_jsonld(_jsonld_webpage(page_url, title, description, schema_type))


def _jsonld_software_app(page_url, description):
    return [
        {
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            "name": "Momo Paper",
            "description": description,
            "url": page_url,
            "applicationCategory": "DeveloperApplication",
            "operatingSystem": "Cross-platform",
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
            "author": {"@type": "Person", "name": "gusibi", "url": "https://github.com/gusibi"},
            "softwareVersion": "2.1",
            "license": "https://opensource.org/licenses/MIT",
        },
        {
            "@context": "https://schema.org",
            "@type": "WebSite",
            "name": "Momo Paper",
            "url": BASE_URL,
            "description": description,
            "inLanguage": "zh-CN",
        },
    ]


def _jsonld_collection(page_url, title, description, schema_type):
    return {
        "@context": "https://schema.org",
        "@type": schema_type,
        "name": title,
        "description": description,
        "url": page_url,
        "inLanguage": "zh-CN",
        "isPartOf": {"@type": "WebSite", "name": "Momo Paper", "url": BASE_URL},
    }


def _jsonld_demo_article(slug, page_url, title, description):
    name_info = DEMO_TYPE_NAMES.get(slug, (title, description))
    return {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": name_info[0],
        "description": name_info[1],
        "url": page_url,
        "inLanguage": "zh-CN",
        "author": {"@type": "Organization", "name": "Momo Paper"},
        "publisher": {"@type": "Organization", "name": "Momo Paper"},
        "isPartOf": {"@type": "WebSite", "name": "Momo Paper", "url": BASE_URL},
    }


def _jsonld_webpage(page_url, title, description, schema_type):
    return {
        "@context": "https://schema.org",
        "@type": schema_type,
        "name": title,
        "description": description,
        "url": page_url,
        "inLanguage": "zh-CN",
        "isPartOf": {"@type": "WebSite", "name": "Momo Paper", "url": BASE_URL},
    }


def _wrap_jsonld(data):
    return f'<script type="application/ld+json">\n{json.dumps(data, ensure_ascii=False, indent=2)}\n</script>'


def _wrap_jsonld_multi(data_list):
    return "\n  ".join(_wrap_jsonld(d) for d in data_list)


# ---------------------------------------------------------------------------
# Page assembly
# ---------------------------------------------------------------------------
def assemble_page(document, url_path: str, page_id: str) -> str:
    meta = document.meta
    lang = str(meta.get("locale", "zh-CN"))
    title = str(meta.get("title", "Momo Paper"))

    # Demo subpages get type-specific title + description.
    description = None
    if page_id == "demo" and url_path != "demo/index.html":
        slug = url_path.split("/")[1]
        info = DEMO_TYPE_NAMES.get(slug)
        if info:
            title = f"{info[0]} — Momo Paper 示例"
            description = f"Momo Paper {info[0]}类型示例。{info[1]}。"
    if description is None:
        description = str(meta.get("description") or PAGE_META.get(page_id, {}).get(
            "description", "Momo Paper — 面向文档与视觉叙事的开源路由式设计系统"
        ))

    body, needs_charts, needs_highlight = render_body(document)
    chart_runtime = renderer._render_chart_runtime() if needs_charts else ""
    highlight_runtime = renderer._render_highlight_runtime() if needs_highlight else ""

    return f"""<!DOCTYPE html>
<html lang="{_esc(lang)}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{_esc(title)}</title>
  {build_meta_block(url_path, page_id, title, description)}
  {theme_links()}
  <link rel="stylesheet" href="/assets/site.css">
  {THEME_BOOT_SCRIPT}
</head>
<body>
  {render_nav(page_id)}
  <main class="page has-site-chrome">
    {render_doc_header(meta)}
    {body}
  </main>
  {render_footer()}
  {chart_runtime}
  {highlight_runtime}
  {THEME_UI_SCRIPT}
</body>
</html>
"""


# ---------------------------------------------------------------------------
# Static asset generation
# ---------------------------------------------------------------------------
def copy_assets():
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    styles_dir = ENGINE_DIR / "momo_dsl" / "styles"
    for _, _, filename in THEMES:
        shutil.copy(styles_dir / filename, ASSETS_DIR / filename)
    shutil.copy(SITE_DIR / "site.css", ASSETS_DIR / "site.css")
    print(f"  OK: copied {len(THEMES)} theme stylesheets + site.css")


def generate_robots_txt():
    content = f"""User-agent: *
Allow: /

# Search & retrieval crawlers — allow (power AI search results)
User-agent: OAI-SearchBot
Allow: /

User-agent: Claude-SearchBot
Allow: /

User-agent: PerplexityBot
Allow: /

# User-triggered crawlers — allow (fire when user explicitly shares URL with AI)
User-agent: ChatGPT-User
Allow: /

User-agent: Claude-User
Allow: /

User-agent: Perplexity-User
Allow: /

User-agent: Google-Agent
Allow: /

# Training crawlers — disallow (use content for model training, not search visibility)
User-agent: GPTBot
Disallow: /

User-agent: ClaudeBot
Disallow: /

User-agent: Meta-ExternalAgent
Disallow: /

User-agent: CCBot
Disallow: /

# Opt-out tokens — disallow (AI training opt-out signals)
User-agent: Google-Extended
Disallow: /

User-agent: Applebot-Extended
Disallow: /

# Undeclared crawlers — disallow (no clear purpose stated)
User-agent: Bytespider
Disallow: /

Sitemap: {BASE_URL}/sitemap.xml
"""
    (OUTPUT_DIR / "robots.txt").write_text(content.strip() + "\n", encoding="utf-8")
    print("  OK: robots.txt")


def generate_sitemap():
    entries = []
    for _, url_path, page_id in PAGES:
        page_url = build_page_url(url_path)
        priority = "1.0" if page_id == "index" else "0.8" if page_id in ("guide", "types", "components", "faq") else "0.6" if page_id == "demo" else "0.5"
        freq = "weekly" if page_id in ("index", "guide", "types", "components", "faq") else "monthly"
        entries.append(f"""  <url>
    <loc>{page_url}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>{freq}</changefreq>
    <priority>{priority}</priority>
  </url>""")
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(entries)}
</urlset>"""
    (OUTPUT_DIR / "sitemap.xml").write_text(xml, encoding="utf-8")
    print("  OK: sitemap.xml")


def generate_llms_txt():
    content = f"""# Momo Paper

> 开源 Markdown DSL 文档引擎。输入 frontmatter 与结构化块，输出排版精良、打印就绪的单文件 HTML。含 5 种图表块、4 种健康块与一组通用结构组件。

## 项目简介

Momo Paper 是一个开源的文档生成引擎，输入 Markdown DSL，输出排版精良、打印就绪的 HTML 文档。引擎是通用渲染器：解析 frontmatter + Markdown 散文 + :::block 结构化块，渲染为单文件 HTML。`document_type` 是语义标签（出现在页头、引导 Skill 选模板），引擎不按类型做结构校验。

- GitHub: https://github.com/gusibi/momo-paper
- License: MIT
- Author: gusibi
- Version: 2.1

## 核心能力

- **Markdown 渲染**: 标题、列表、引用、表格、代码块（highlight.js）与行内标记的 CommonMark 子集
- **5 种图表块**: bar、line、donut、candlestick、waterfall — 声明 :::chart 块，echarts 渲染，颜色随主题令牌自适应
- **4 种健康块**: weekly-summary、goal-tracker、metrics-panel、report-header — 字段直接解析为结构化报告组件
- **通用结构块**: hero、stats、feature-grid、card-grid、comparison、three-columns、callout、faq 等，由主题 CSS 按标签名样式化
- **nav 块**: 文档内导航
- **双主题系统**: Momo Paper 暖调与 Vercel 极简，共享 --mp-* 变量，一键切换
- **打印安全**: 所有样式内置 @media print 规则
- **AI Agent 集成**: Claude Code Skill + CLI

## 关键页面

- [首页]({BASE_URL}/) — 项目概述与核心能力
- [使用指南]({BASE_URL}/guide/) — 三种工作流：Skill（AI 自动）、CLI（手动）、HTML 模板（直接编辑）
- [组件目录]({BASE_URL}/components/) — 全部组件的渲染效果与 DSL 源码
- [文档样板]({BASE_URL}/types/) — 15 份样板的章节结构与适用场景
- [示例画廊]({BASE_URL}/demo/) — 全部 15 份样板的渲染示例
- [图表演示]({BASE_URL}/charts/) — 5 种图表块的交互示例与 DSL 源码
- [常见问题]({BASE_URL}/faq/) — 安装、使用与设计相关 FAQ
- [设计系统]({BASE_URL}/design/) — 色彩、字体、间距令牌与设计哲学

## Related Projects (EZTOLAB 生态)

- [EZTOLAB](https://eztoolab.com) — 工具实验室主页
- [MoliBot](https://molibot.eztoolab.com) — 多渠道个人 AI 助手运行时
- [MoliShot](https://molishot.eztoolab.com) — macOS 截图与 OCR 工具
- [MoliTodo](https://molitodo.eztoolab.com) — AI 驱动的桌面悬浮 todo 管理器
- [MoliTutu](https://tutu.eztoolab.com) — 智能图片压缩与 CDN 上传工具
- [LLM Wiki](https://llmwiki.eztoolab.com) — AI 驱动的个人知识编译器
"""
    (OUTPUT_DIR / "llms.txt").write_text(content.strip() + "\n", encoding="utf-8")
    print("  OK: llms.txt")


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------
def build():
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir()

    for content_file, url_path, page_id in PAGES:
        src = CONTENT_DIR / content_file
        if not src.exists():
            print(f"  SKIP: {content_file} not found")
            continue
        document = parse_file(src)
        html = assemble_page(document, url_path, page_id)
        out_path = OUTPUT_DIR / url_path
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(html, encoding="utf-8")
        print(f"  OK: {content_file} -> {url_path}")

    copy_assets()
    generate_robots_txt()
    generate_sitemap()
    generate_llms_txt()

    print(f"\nBuilt site to {OUTPUT_DIR.resolve()}")


if __name__ == "__main__":
    build()
