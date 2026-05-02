#!/usr/bin/env python3
"""Build the Momo Paper static product site.

Renders each JSON data file through the momo-paper engine, then injects
shared site navigation, footer, meta tags, and JSON-LD structured data.
Also generates llms.txt, llms-full.txt, robots.txt, and sitemap.xml.
"""

import json
import shutil
import sys
from datetime import date
from pathlib import Path

# Make the engine importable without pip install
ENGINE_DIR = Path(__file__).resolve().parent.parent / "scripts" / "json-engine"
sys.path.insert(0, str(ENGINE_DIR))

from momo_paper.engine import render  # noqa: E402

SITE_DIR = Path(__file__).resolve().parent
DATA_DIR = SITE_DIR / "data"
DEMO_DIR = SITE_DIR / "data" / "demo"
OUTPUT_DIR = SITE_DIR / "output"

SITE_TEMPLATES = SITE_DIR / "templates"

BASE_URL = "https://momo.eztoolab.com"
TODAY = date.today().isoformat()

PAGES = [
    # (data_file, url_path, page_id, template_file or None, data_subdir or None)
    ("index.json",   "index.html",            "index",  "landing.html.j2", None),
    ("guide.json",   "guide/index.html",      "guide",  None,              None),
    ("types.json",   "types/index.html",      "types",  None,              None),
    ("index.json",   "demo/index.html",       "demo",   "demo-index.html.j2", "demo"),
    ("charts.json",  "charts/index.html",     "charts", None,              None),
    ("faq.json",     "faq/index.html",        "faq",    None,              None),
    ("design.json",  "design/index.html",      "design", "design-tokens.html.j2", None),
    # Demo pages for all document types not already used as site pages
    ("one-pager.json",        "demo/one-pager/index.html",        "demo", None, "demo"),
    ("long-doc.json",         "demo/long-doc/index.html",         "demo", None, "demo"),
    ("letter.json",           "demo/letter/index.html",           "demo", None, "demo"),
    ("portfolio.json",        "demo/portfolio/index.html",        "demo", None, "demo"),
    ("resume.json",           "demo/resume/index.html",           "demo", None, "demo"),
    ("slides.json",           "demo/slides/index.html",           "demo", None, "demo"),
    ("equity-report.json",    "demo/equity-report/index.html",    "demo", None, "demo"),
    ("changelog.json",        "demo/changelog/index.html",        "demo", None, "demo"),
    ("process-flow.json",     "demo/process-flow/index.html",     "demo", None, "demo"),
    ("timeline.json",         "demo/timeline/index.html",         "demo", None, "demo"),
    ("faq-page.json",         "demo/faq-page/index.html",         "demo", None, "demo"),
    ("case-study.json",       "demo/case-study/index.html",       "demo", None, "demo"),
    ("research-summary.json", "demo/research-summary/index.html", "demo", None, "demo"),
    ("stats-report.json",     "demo/stats-report/index.html",     "demo", None, "demo"),
    ("infographic.json",      "demo/infographic/index.html",      "demo", None, "demo"),
]

# ---------------------------------------------------------------------------
# Per-page meta descriptions for SEO / AI visibility
# ---------------------------------------------------------------------------
PAGE_META = {
    "index": {
        "description": "Momo Paper 是面向文档与视觉叙事的开源路由式设计系统，提供 15 种文档类型、5 种可编程图表、14 种图示原语和 30 个 HTML 模板。JSON 声明内容，引擎渲染设计精良的 HTML。",
        "schema_type": "SoftwareApplication",
    },
    "guide": {
        "description": "Momo Paper 使用指南：推荐通过 Claude Code Skill 自动使用，也支持 CLI 手动渲染和直接 HTML 模板编辑三种工作流。安装、命令参考、JSON 格式和图表嵌入完整说明。",
        "schema_type": "TechArticle",
    },
    "types": {
        "description": "Momo Paper 15 种文档类型全景：one_pager、long_doc、letter、portfolio、resume、slides、equity_report、changelog、process_flow、timeline、faq_page、case_study、research_summary、stats_report、infographic。",
        "schema_type": "CollectionPage",
    },
    "faq": {
        "description": "Momo Paper 常见问题：安装方式、JSON 引擎使用、AI agent 集成、文档类型选择、图表嵌入、设计令牌系统、自定义模板和打印支持等 12 个常见问题解答。",
        "schema_type": "FAQPage",
    },
    "design": {
        "description": "Momo Paper 设计系统：色彩系统（12 色）、字体层级（serif/sans/mono）、间距令牌和设计哲学。所有视觉属性集中定义在 CSS 自定义属性中，30 个模板自动生效。",
        "schema_type": "WebPage",
    },
    "charts": {
        "description": "Momo Paper 交互式图表演示：支持柱状图、折线图、环形图、K 线图和瀑布图 5 种类型，在 JSON 中声明 chart 对象自动渲染为内联 SVG。",
        "schema_type": "WebPage",
    },
    "demo": {
        "description": "Momo Paper 全部 15 种文档类型的完整渲染示例，涵盖商业方案、白皮书、简历、研报、幻灯片、信息图等全场景。",
        "schema_type": "CollectionPage",
    },
}

# Map demo slug to Chinese name for Article schema
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
# Inline demo data (from original build.py)
# ---------------------------------------------------------------------------
LONG_DOC_DEMO = {
    "document_type": "long_doc",
    "locale": "zh-CN",
    "meta": {
        "title": "白皮书 / 长文示例",
        "subtitle": "Long Document 类型展示多章节长文、引用块和结论结构。",
        "eyebrow": "Momo Paper / long_doc / zh-CN",
        "date": "2026-05-02",
        "author": "Momo Paper"
    },
    "sections": {
        "abstract": {
            "body": ["本示例展示 long_doc 类型的核心特性：摘要、无限可迭代的章节（每章含标题、正文和可选的引用块）、以及带下一步行动的结论。此类型适合技术白皮书、深度分析报告和长篇文档。"],
            "findings": ["章节数量不限，每章独立渲染", "内置引用块样式（左边框 + 品牌色）", "结论包含 checklist 式的下一步行动"]
        },
        "sections": [
            {"heading": "设计令牌系统", "body": ["Momo Paper 的设计令牌定义在 _base.html.j2 的 :root 块中，包括颜色（--ink、--brand、--accent 等）、字体（serif/sans/mono 三套）、间距和圆角。所有子模板通过 Jinja2 继承机制自动获得这些令牌。", "这种设计的核心优势是：一次定义，全局生效。修改 --brand 的值，所有 30 个模板的品牌色都会同步更新。"], "quote": {"text": "设计令牌是视觉一致性的唯一真相源。", "source": "Momo Paper 设计原则"}},
            {"heading": "路由规则", "body": ["document_type 字段是路由的核心：用户在 JSON 中声明文档类型，引擎在 DEFAULT_TEMPLATE_MAP 中查找对应的 Jinja2 模板。这种映射关系是 1:1 的——一种类型对应一个模板。", "如果需要自定义，可以传入 --template 参数显式指定模板文件名，或通过 --template-dir 指定自定义模板目录。"]},
            {"heading": "JSON Schema 校验", "body": ["每种文档类型都有对应的 JSON Schema 文件（存放在 schemas/ 目录中），定义了 sections 的结构、必需字段和数据类型。Schema 确保了输入数据的一致性，让 AI agent 生成的结构化 JSON 在渲染前就能被验证。"]}
        ],
        "conclusion": {
            "body": ["long_doc 是 Momo Paper 中通用性最强的类型之一。它的可迭代章节结构让它适应各种长度的内容——从 3 节的简短报告到 20 节的详细白皮书。"],
            "next_steps": ["尝试用 momo init -t long_doc 生成骨架", "在 JSON 中为每个章节添加 heading 和 body", "可选添加 quote 对象来高亮重要观点"]
        }
    }
}

PORTFOLIO_DEMO = {
    "document_type": "portfolio",
    "locale": "zh-CN",
    "meta": {
        "title": "作品集 / Portfolio 示例",
        "subtitle": "展示项目案例和支持指标。每个案例含背景/行动/结果三段式叙述和可选的数据卡片。",
        "eyebrow": "Momo Paper / portfolio / zh-CN",
        "date": "2026-05-02",
        "author": "Momo Paper"
    },
    "sections": {
        "overview": {
            "body": ["Portfolio 类型采用经典的 STAR（情境-行动-结果）框架来展示案例。每个案例独立的 section 包含标题、背景、行动、结果和可选的数据指标卡。", "适合设计师作品集、咨询案例展示、项目汇报等场景。"]
        },
        "cases": [
            {"title": "设计系统从零到一", "context": "公司产品线扩张至 8 款产品后，各产品视觉风格分裂，用户投诉「不像一家公司的产品」。设计团队面临挑战：如何在不重写所有产品的前提下统一视觉语言？", "action": "采用 Momo Paper 的路由式设计系统思路，建立中心化设计令牌库。从 8 款产品中提取共性组件（按钮、表单、导航、卡片等），归纳为 50+ 设计令牌。各产品逐步迁移，而非一次性替换。", "result": "6 个月内 8 款产品全部完成迁移。设计令牌修改一次，全产品线同步生效。品牌一致性从 32% 提升至 95%。", "metrics": [{"label": "设计令牌数", "value": "50+"}, {"label": "产品迁移", "value": "8 款"}, {"label": "一致性提升", "value": "63pp"}]},
            {"title": "移动端信息架构重构", "context": "App 功能膨胀导致导航混乱，核心功能路径从 3 步延长至 6 步。用户反馈「找不到想要的功能」。", "action": "基于用户使用数据和 20 场深度访谈，重新设计信息架构。采用「渐进式披露」策略，将 40+ 功能按使用频率分为三层。核心功能 1 步可达。", "result": "核心任务完成率从 58% 提升至 87%。用户满意度 NPS 从 22 提升至 41。功能发现率提升 3 倍。", "metrics": [{"label": "任务完成率", "value": "87%"}, {"label": "NPS", "value": "41"}, {"label": "功能发现", "value": "3x"}]}
        ],
        "capabilities": {
            "body": ["Portfolio 模板在案例卡片中内置了数据指标展示，每个指标以 fact-card 形式呈现——大数字 + 标签，适合快速传达关键成果。"],
            "skills": ["案例背景叙述", "三段式结构（背景/行动/结果）", "数据指标卡展示", "能力总结与方法论"]
        }
    }
}

STATS_REPORT_DEMO = {
    "document_type": "stats_report",
    "locale": "zh-CN",
    "meta": {
        "title": "数据报告 / KPI 示例",
        "subtitle": "展示 KPI 指标卡、趋势图、数据分群和方法说明。",
        "eyebrow": "Momo Paper / stats_report / zh-CN",
        "date": "2026-05-02",
        "author": "Momo Paper",
        "period": "2026 Q1"
    },
    "sections": {
        "kpis": [
            {"label": "总用户数", "value": "1,280 万", "change": "+18%", "trend": "up"},
            {"label": "月活用户", "value": "320 万", "change": "+12%", "trend": "up"},
            {"label": "付费率", "value": "8.5%", "change": "+1.2pp", "trend": "up"},
            {"label": "流失率", "value": "3.2%", "change": "-0.8pp", "trend": "down"}
        ],
        "trends": {
            "body": ["Q1 整体指标呈上升趋势，用户增长和付费转化均好于预期。以下为月度用户增长趋势："],
            "chart": {
                "type": "line",
                "title": "月度活跃用户增长（万）",
                "height": 280,
                "data": {
                    "labels": ["1月", "2月", "3月", "4月", "5月", "6月"],
                    "values": [240, 258, 275, 290, 305, 320]
                }
            }
        },
        "segments": [
            {"name": "新用户（注册 < 30 天）", "body": ["占比 35%，月环比增长 22%。主要来自自然搜索和口碑推荐。7 日留存率 42%，高于行业平均 35%。"]},
            {"name": "活跃用户（月活跃 > 15 天）", "body": ["占比 28%，核心功能使用频次 12 次/周。平均使用时长 45 分钟/天。付费转化率 18%。"]},
            {"name": "沉默用户（30 天未活跃）", "body": ["占比 37%，其中 60% 在注册后 3 天内流失。主要流失原因是 onboarding 流程缺失关键引导步骤。"]}
        ],
        "method": {
            "body": ["数据来源：产品分析平台 + 用户行为数据库。用户分群基于 RFM 模型（最近活跃、使用频次、功能深度）。月度数据为去重后的独立用户数。"]
        }
    }
}

FAQ_PAGE_DEMO = {
    "document_type": "faq_page",
    "locale": "zh-CN",
    "meta": {
        "title": "常见问题示例",
        "subtitle": "FAQ 类型支持分组问答、引导语和总结说明。适合产品帮助中心、事件回应、政策说明。",
        "eyebrow": "Momo Paper / faq_page / zh-CN",
        "date": "2026-05-02",
        "author": "Momo Paper"
    },
    "sections": {
        "lead": {
            "body": ["FAQ 类型将问答内容按组分类，每组有独立标题。每个问答以卡片形式呈现——问题加粗突出，回答以次级文字显示。适合产品帮助中心、活动常见问题、政策解读等场景。"]
        },
        "groups": [
            {"title": "关于此类型", "items": [{"question": "faq_page 类型适合哪些场景？", "answer": "适合需要结构化呈现「问答」内容的场景，如产品帮助中心、活动常见问题、政策解读、社区指南等。分组机制让你可以按主题组织问题，方便用户快速定位。"}, {"question": "FAQ 卡片支持什么内容？", "answer": "每个 FAQ 卡片包含一个问题（question）和一个回答（answer），都是纯文本字段。卡片自动以 canvas 色为背景，和页面整体设计令牌保持一致。"}]},
            {"title": "使用方式", "items": [{"question": "如何创建 FAQ 页面？", "answer": "运行 momo init -t faq_page -o faq.json 生成骨架，填入你的分组和问答内容，然后运行 momo render -d faq.json -o faq.html 渲染。在 JSON 中，groups 是一个数组，每个元素有 title 和 items 字段。"}, {"question": "可以有多少个分组？", "answer": "分组数量没有限制。每个分组内的 FAQ 条目数量也没有限制。模板使用 for 循环遍历，实际数量取决于你放入 JSON 的数据。"}]}
        ],
        "summary": {
            "body": ["这是 faq_page 类型的演示示例。实际使用时，你可以根据需要创建任意数量的分组和问答条目。"],
            "next_step": "运行 momo init -t faq_page 创建你自己的 FAQ 页面"
        }
    }
}

DEMO_INLINE_DATA = {
    "long-doc.json": LONG_DOC_DEMO,
    "portfolio.json": PORTFOLIO_DEMO,
    "stats-report.json": STATS_REPORT_DEMO,
    "faq-page.json": FAQ_PAGE_DEMO,
}


# ---------------------------------------------------------------------------
# Navigation & footer
# ---------------------------------------------------------------------------
def load_nav(page_id: str) -> str:
    raw = (SITE_DIR / "nav.html").read_text(encoding="utf-8")
    for _, _, p, _, _ in PAGES:
        raw = raw.replace(f"__active_{p}__", "active" if p == page_id else "")
    return raw


def load_footer() -> str:
    return (SITE_DIR / "footer.html").read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Meta tag + JSON-LD injection
# ---------------------------------------------------------------------------
def _esc(s: str) -> str:
    """Escape HTML attribute characters."""
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")


def build_page_url(url_path: str) -> str:
    path = url_path.rstrip("/")
    if path == "index.html":
        return BASE_URL + "/"
    return BASE_URL + "/" + path.replace("/index.html", "/")


def inject_meta(html: str, url_path: str, page_id: str, title: str, description: str, data_source=None) -> str:
    """Inject meta description, Open Graph, canonical, and JSON-LD into <head>."""
    page_url = build_page_url(url_path)
    meta_block = f"""  <meta name="description" content="{_esc(description)}">
  <link rel="canonical" href="{page_url}">
  <meta property="og:title" content="{_esc(title)}">
  <meta property="og:description" content="{_esc(description)}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{page_url}">
  <meta property="og:site_name" content="Momo Paper">
  <meta property="og:locale" content="zh_CN">
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="{_esc(title)}">
  <meta name="twitter:description" content="{_esc(description)}">
"""
    jsonld = build_jsonld(page_id, url_path, title, description, data_source)
    return html.replace("<!-- META_INJECT -->", meta_block + jsonld + "\n", 1)


def build_jsonld(page_id: str, url_path: str, title: str, description: str, data_source=None) -> str:
    """Build JSON-LD structured data for a page."""
    page_url = build_page_url(url_path)
    meta = PAGE_META.get(page_id, {})
    schema_type = meta.get("schema_type", "WebPage")

    # Detect individual demo pages by url_path
    if page_id == "demo" and url_path != "demo/index.html":
        slug = url_path.split("/")[1]  # e.g. "one-pager"
        return _jsonld_demo_article(slug, page_url, title, description)

    if page_id == "index":
        return _jsonld_software_app(page_url, title, description)
    elif page_id == "faq":
        return _jsonld_faq(page_url, title, description, data_source)
    elif page_id in ("types", "demo"):
        return _jsonld_collection(page_url, title, description, schema_type)
    else:
        return _jsonld_webpage(page_url, title, description, schema_type)


def _jsonld_software_app(page_url, title, description):
    data = [
        {
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            "name": "Momo Paper",
            "description": description,
            "url": page_url,
            "applicationCategory": "DeveloperApplication",
            "operatingSystem": "Cross-platform",
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
            "author": {
                "@type": "Person",
                "name": "gusibi",
                "url": "https://github.com/gusibi"
            },
            "softwareVersion": "0.2.2",
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
    return _wrap_jsonld_multi(data)


def _jsonld_faq(page_url, title, description, data_source=None):
    """Build FAQPage schema from actual FAQ data."""
    main_entity = []
    if data_source and isinstance(data_source, dict):
        groups = data_source.get("sections", {}).get("groups", [])
        for group in groups:
            for item in group.get("items", []):
                q = item.get("question", "")
                a = item.get("answer", "")
                if q and a:
                    main_entity.append({
                        "@type": "Question",
                        "name": q,
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": a,
                        }
                    })

    data = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "name": title,
        "description": description,
        "url": page_url,
        "inLanguage": "zh-CN",
        "mainEntity": main_entity,
    }
    return _wrap_jsonld(data)


def _jsonld_collection(page_url, title, description, schema_type):
    data = {
        "@context": "https://schema.org",
        "@type": schema_type,
        "name": title,
        "description": description,
        "url": page_url,
        "inLanguage": "zh-CN",
        "isPartOf": {"@type": "WebSite", "name": "Momo Paper", "url": BASE_URL},
    }
    return _wrap_jsonld(data)


def _jsonld_demo_article(page_id, page_url, title, description):
    slug = page_id
    name_info = DEMO_TYPE_NAMES.get(slug, (title, description))
    data = {
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
    return _wrap_jsonld(data)


def _jsonld_webpage(page_url, title, description, schema_type):
    data = {
        "@context": "https://schema.org",
        "@type": schema_type,
        "name": title,
        "description": description,
        "url": page_url,
        "inLanguage": "zh-CN",
        "isPartOf": {"@type": "WebSite", "name": "Momo Paper", "url": BASE_URL},
    }
    return _wrap_jsonld(data)


def _wrap_jsonld(data):
    return f'<script type="application/ld+json">\n{json.dumps(data, ensure_ascii=False, indent=2)}\n</script>'


def _wrap_jsonld_multi(data_list):
    parts = [_wrap_jsonld(d) for d in data_list]
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# llms.txt generation
# ---------------------------------------------------------------------------
def generate_llms_txt():
    content = f"""# Momo Paper

> 面向文档与视觉叙事的开源路由式设计系统。将 15 种文档类型、5 种可编程图表和 14 种图示原语统一到一套设计令牌中。

## 项目简介

Momo Paper 是一个开源的文档生成引擎，输入 JSON 数据，输出排版精良、打印就绪的 HTML 文档。核心思想是「路由式设计系统」——你声明 document_type，引擎自动选择对应的 Jinja2 模板、设计令牌和 JSON Schema。

- GitHub: https://github.com/gusibi/momo-paper
- License: MIT
- Author: gusibi
- Version: 0.2.2

## 核心能力

- **15 种文档类型**: one_pager, long_doc, letter, portfolio, resume, slides, equity_report, changelog, process_flow, timeline, faq_page, case_study, research_summary, stats_report, infographic
- **5 种可编程图表**: bar, line, donut, candlestick, waterfall — JSON 声明 chart 对象，引擎自动渲染内联 SVG
- **14 种图示原语**: 架构图、流程图、象限图、状态机、泳道图、时间线、树状图、分层图、维恩图等
- **30 个 HTML 模板**: 15 种类型 × 中英文双语言
- **设计令牌系统**: CSS 自定义属性集中定义颜色、字体、间距，所有模板自动生效
- **AI Agent 集成**: 支持 Claude Code Skill 和 CLI 调用，JSON Schema 校验输入
- **打印安全**: 所有模板内置 @media print 样式规则

## 关键页面

- [首页]({BASE_URL}/) — 项目概述和核心特性
- [使用指南]({BASE_URL}/guide/) — 三种工作流：Skill（AI 自动）、CLI（手动）、HTML 模板（直接编辑）
- [文档类型]({BASE_URL}/types/) — 15 种文档类型的详细说明和适用场景
- [示例画廊]({BASE_URL}/demo/) — 全部 15 种类型的渲染示例
- [图表演示]({BASE_URL}/charts/) — 5 种图表类型的交互示例
- [常见问题]({BASE_URL}/faq/) — 安装、使用和设计相关 FAQ
- [设计系统]({BASE_URL}/design/) — 色彩、字体、间距和设计哲学

## AI 使用提示

Momo Paper 专为 AI agent 设计了结构化工作流：
1. AI 通过 `momo list` 获取支持的文档类型
2. 通过 `momo init -t <type>` 生成 JSON 骨架
3. 填充 JSON 数据后通过 `momo render -d data.json -o output.html` 渲染
4. 图表通过在 JSON 中声明 chart 对象自动渲染

JSON Schema 定义了每种类型的字段结构，确保 AI 生成的数据在渲染前即可校验。
"""
    (OUTPUT_DIR / "llms.txt").write_text(content.strip() + "\n", encoding="utf-8")
    print("  OK: llms.txt")


def generate_llms_full_txt():
    content = f"""# Momo Paper — 完整知识库

> 面向文档与视觉叙事的开源路由式设计系统。

## 项目概述

Momo Paper 是一个开源的文档生成引擎（v0.2.2），将 15 种文档类型、5 种可编程图表和 14 种图示原语统一到一套设计令牌系统中。核心思想是「路由式设计系统」——用户声明 document_type，引擎自动选择对应的 Jinja2 模板、CSS 设计令牌和 JSON Schema 进行渲染。

- GitHub: https://github.com/gusibi/momo-paper
- 作者: gusibi (https://github.com/gusibi)
- 许可证: MIT
- Python: 3.10+
- 依赖: jinja2, click

## 使用方式

### 方式一：Claude Code Skill（推荐）

Momo Paper 提供了 Claude Code Skill（SKILL.md），AI agent 自动完成从安装到渲染的全部步骤。

```
# 用户只需描述需求：
"帮我生成一份 Q2 产品增长方案"
"帮我做一份简历"

# Skill 自动处理：
# 1. 检测并安装 momo CLI
# 2. 选择合适的文档类型
# 3. 生成 JSON 数据
# 4. 渲染为 HTML 文档
# 5. 打开浏览器预览
```

### 方式二：CLI 手动操作

```bash
# 安装
cd scripts/json-engine
pip install -e .

# 使用
momo list                              # 列出全部文档类型
momo init -t one_pager -o doc.json     # 生成骨架
momo render -d doc.json -o output.html # 渲染 HTML
momo chart -d doc.json -k sections.trends.chart -o chart.svg  # 渲染图表
```

### 方式三：直接 HTML 模板

assets/templates/ 目录下提供了 30 个独立 HTML 文件，打开即编辑，无需任何构建步骤。

## 文档类型详解

### 1. one_pager — 方案/执行摘要
- 适用: 商业方案、项目提案、执行摘要
- 结构: summary → context → evidence → recommendation（四段固定结构）
- 特性: 数据卡片、要点列表

### 2. long_doc — 白皮书/长文
- 适用: 技术白皮书、深度分析报告、长篇文档
- 结构: abstract + 可迭代 sections（每章含 heading/body/quote）+ conclusion
- 特性: 章节数量无限，引用块有品牌色边框

### 3. letter — 信件/推荐信/Memo
- 适用: 正式信函、推荐信、内部备忘录
- 结构: 信头（收件人/发件人/日期）→ 正文段落 → 签名区

### 4. portfolio — 作品集
- 适用: 设计师作品集、咨询案例、项目汇报
- 结构: overview → cases（每项含 title/context/action/result/metrics）→ capabilities
- 特性: STAR 框架叙述，数据指标卡

### 5. resume — 简历/CV
- 适用: 求职、个人简介
- 结构: 个人信息 → 工作经历（时间线）→ 教育 → 技能标签 → 项目列表
- 特性: 打印友好，时间线组件

### 6. slides — 幻灯片/演示
- 适用: 汇报、路演、教学
- 结构: 16:9 视口，支持 cover/closing/content/toc 多种布局
- 特性: 基于 Python 生成 + Jinja2 模板

### 7. equity_report — 研报/估值分析
- 适用: 金融研究、股票分析、估值报告
- 结构: 投资论点 → KPI → 趋势图 → 估值 → 风险矩阵 → 催化剂 → 免责声明
- 特性: KPI 卡片、K 线图、风险/催化剂卡片

### 8. changelog — 更新日志/Release Notes
- 适用: 版本更新说明
- 结构: 版本列表，按新增/变更/修复/废弃分类
- 特性: 彩色标签区分变更类型

### 9. process_flow — 流程/SOP
- 适用: 操作流程、标准作业程序
- 结构: 步骤列表（含标题/描述/负责人）
- 特性: 自动编号，负责人标注，支持泳道图

### 10. timeline — 时间线/Roadmap
- 适用: 项目路线图、历史事件序列
- 结构: 时间线列表，每项含日期/标题/描述
- 特性: completed/in_progress/upcoming 三种状态

### 11. faq_page — 常见问题
- 适用: 产品帮助中心、活动 FAQ
- 结构: lead → groups（每组含 title 和 items）→ summary
- 特性: 分组问答卡片

### 12. case_study — 案例拆解/项目复盘
- 适用: 内部分享、对外宣传
- 结构: 背景 → 挑战 → 方案（步骤）→ 结果指标 → 经验教训
- 特性: 步骤编号，指标卡

### 13. research_summary — 研究摘要
- 适用: 文献综述、市场研究
- 结构: 研究问题 → 关键发现 → 方法 → 局限性 → 下一步
- 特性: 发现编号卡片

### 14. stats_report — 数据报告/KPI
- 适用: 数据分析报告
- 结构: KPI 指标卡 → 趋势图 → 数据分群 → 方法说明
- 特性: KPI 大数字、内联 SVG 图表、异常警报

### 15. infographic — 信息图
- 适用: 年报摘要、数据故事
- 结构: 灵活布局，支持大数字、图表、要点列表
- 特性: 视觉冲击力强

## 图表系统

Momo Paper 支持 5 种可编程图表，通过在 JSON 中声明 chart 对象自动渲染为内联 SVG：

| 类型 | 名称 | 数据格式 | 适用场景 |
|------|------|---------|---------|
| bar | 柱状图 | values: [n, ...] | 类别对比 |
| line | 折线图 | values: [n, ...] + labels | 时间序列趋势 |
| donut | 环形图 | values: [n, ...] | 比例分解 |
| candlestick | K 线图 | values: [{{o,h,l,c}}, ...] | OHLC 价格 |
| waterfall | 瀑布图 | values: [n, ...] | 数值桥接 |

chart 对象可嵌入任意 section，也可通过 `momo chart` 命令独立渲染为 SVG 文件。

## 图示原语

14 种图示原语以独立 HTML 文件提供在 assets/diagrams/ 目录中：

- architecture.html — 系统架构和组件关系
- flowchart.html — 业务流程和决策树
- quadrant.html — 2×2 矩阵分析
- state-machine.html — 状态转移图
- swimlane.html — 跨角色流程
- timeline.html — 事件序列图
- tree.html — 层级结构
- layer-stack.html — 技术栈分层
- venn.html — 集合关系

## 设计系统

### 色彩系统
12 种核心颜色，分五组：
- 文本色: --ink (#172033), --ink-subtle (#4C566A)
- 表面色: --paper (#FAF8F4), --canvas (#F2EFE8), --line (#D8D2C4)
- 品牌色: --brand (#244C7A), --brand-muted (#DCE7F2)
- 强调色: --accent (#B65C3A), --accent-muted (#F2E1D9)
- 语义色: --success (#2F6B4F), --warning (#A46A21), --danger (#9A3D3D)

### 字体系统
- 标题: "Noto Serif SC" / "Source Han Serif SC" / serif
- 正文: "Inter" / "Noto Sans SC" / "PingFang SC" / sans-serif
- 代码: "IBM Plex Mono" / "SFMono-Regular" / monospace

### 设计哲学
- 约束即解放: 设计令牌消除决策疲劳
- 内容优先: 结构决定排版，内容决定结构
- 打印安全: @media print 内置，屏幕与纸张表现一致
- JSON 即接口: JSON 作为 AI agent 与渲染引擎的契约

## JSON 数据格式

```json
{{
  "document_type": "<类型名>",
  "locale": "zh-CN",
  "meta": {{
    "title": "文档标题",
    "subtitle": "副标题",
    "eyebrow": "面包屑/标签",
    "date": "2026-05-02",
    "author": "作者"
  }},
  "sections": {{
    // 类型特定的结构，由 JSON Schema 定义
  }}
}}
```

每种类型的 sections 结构由对应的 JSON Schema 文件定义，确保数据一致性。

## 常见问题

**Q: Momo Paper 是什么？**
A: 面向文档与视觉叙事的开源设计系统。提供 15 种文档类型模板、JSON 渲染引擎和 14 种图示原语。

**Q: 需要什么前置条件？**
A: 仅用 HTML 模板不需要任何依赖。使用 JSON 引擎需要 Python 3.10+、jinja2 和 click。

**Q: 可以在 AI agent 中使用吗？**
A: 可以。支持 Claude Code Skill 和 CLI 调用模式。AI 通过 momo init 和 momo render 命令生成文档。

**Q: 如何选择文档类型？**
A: 根据内容需求选择——商业方案用 one_pager，长文用 long_doc，简历用 resume，研报用 equity_report，数据报告用 stats_report。

**Q: 和 Word/LaTeX/Notion 有什么区别？**
A: Momo Paper 是文档生成引擎而非编辑器。优势在于：标准 HTML 输出、设计令牌保证一致性、JSON 让 AI 可结构化生成、打印安全内置。

**Q: 设计令牌如何工作？**
A: 所有视觉属性定义在 _base.html.j2 的 :root CSS 自定义属性中。子模板通过 Jinja2 继承自动获得。修改一处，全局生效。

**Q: 支持哪些语言？**
A: zh-CN（中文）和 en（英文），各 15 套模板共 30 个。

**Q: 文档支持打印吗？**
A: 所有模板内置 @media print 规则。自动移除背景色、调整页边距、避免跨页断裂。

## 站点页面

- 首页: {BASE_URL}/
- 使用指南: {BASE_URL}/guide/
- 文档类型: {BASE_URL}/types/
- 示例画廊: {BASE_URL}/demo/
- 图表演示: {BASE_URL}/charts/
- 常见问题: {BASE_URL}/faq/
- 设计系统: {BASE_URL}/design/
"""
    (OUTPUT_DIR / "llms-full.txt").write_text(content.strip() + "\n", encoding="utf-8")
    print("  OK: llms-full.txt")


# ---------------------------------------------------------------------------
# robots.txt generation
# ---------------------------------------------------------------------------
def generate_robots_txt():
    content = f"""User-agent: *
Allow: /

# AI Search Crawlers (allowed — these power AI search results, not training)
User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: Claude-SearchBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Perplexity-User
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: Bytespider
Disallow: /

User-agent: CCBot
Disallow: /

Sitemap: {BASE_URL}/sitemap.xml
"""
    (OUTPUT_DIR / "robots.txt").write_text(content.strip() + "\n", encoding="utf-8")
    print("  OK: robots.txt")


# ---------------------------------------------------------------------------
# sitemap.xml generation
# ---------------------------------------------------------------------------
def generate_sitemap():
    url_entries = []
    for _, url_path, page_id, _, _ in PAGES:
        page_url = build_page_url(url_path)
        priority = "1.0" if page_id == "index" else "0.8" if page_id in ("guide", "types", "faq") else "0.6" if page_id == "demo" else "0.5"
        freq = "weekly" if page_id in ("index", "guide", "types", "faq") else "monthly"
        url_entries.append(f"""  <url>
    <loc>{page_url}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>{freq}</changefreq>
    <priority>{priority}</priority>
  </url>""")

    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(url_entries)}
</urlset>"""
    (OUTPUT_DIR / "sitemap.xml").write_text(xml, encoding="utf-8")
    print("  OK: sitemap.xml")


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------
def build():
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir()

    for data_file, url_path, page_id, template_file, data_subdir in PAGES:
        # Resolve data source: file path or inline dict
        if data_subdir == "demo" and data_file in DEMO_INLINE_DATA:
            data_source = DEMO_INLINE_DATA[data_file]
        else:
            base = DEMO_DIR if data_subdir == "demo" else DATA_DIR
            data_source = str(base / data_file)
            if not Path(data_source).exists():
                print(f"  SKIP: {data_file} not found")
                continue

        kwargs = {}
        if template_file:
            kwargs["template_dir"] = str(SITE_TEMPLATES)
            kwargs["template_file"] = template_file
        html = render(data_source, **kwargs)

        # Inject navigation and footer
        html = html.replace("<body>", "<body>\n" + load_nav(page_id), 1)
        html = html.replace("</body>", load_footer() + "\n</body>", 1)

        # Resolve title and description for meta injection
        if isinstance(data_source, dict):
            title = data_source.get("meta", {}).get("title", "Momo Paper")
            resolved_data = data_source
        else:
            with open(data_source, encoding="utf-8") as f:
                resolved_data = json.load(f)
            title = resolved_data.get("meta", {}).get("title", "Momo Paper")

        # For demo pages, use type-specific title and description
        description = None
        if data_subdir == "demo" and page_id == "demo" and data_file != "index.json":
            slug = url_path.split("/")[1]  # e.g. "one-pager"
            demo_info = DEMO_TYPE_NAMES.get(slug)
            if demo_info:
                title = f"{demo_info[0]} — Momo Paper 示例"
                description = f"Momo Paper {demo_info[0]}类型示例。{demo_info[1]}。展示 JSON 数据结构与 HTML 渲染效果的对应关系。"

        if description is None:
            meta_info = PAGE_META.get(page_id, {})
            description = meta_info.get("description", "Momo Paper — 面向文档与视觉叙事的开源路由式设计系统")

        # Inject meta tags and JSON-LD in a single pass
        html = inject_meta(html, url_path, page_id, title, description, resolved_data)

        out_path = OUTPUT_DIR / url_path
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(html, encoding="utf-8")
        print(f"  OK: {data_file} -> {url_path}")

    # Generate static files
    generate_robots_txt()
    generate_sitemap()
    generate_llms_txt()
    generate_llms_full_txt()

    print(f"\nBuilt {len(PAGES)} pages + AI visibility files to {OUTPUT_DIR.resolve()}")


if __name__ == "__main__":
    build()
