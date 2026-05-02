#!/usr/bin/env python3
"""Build the Momo Paper static product site.

Renders each JSON data file through the momo-paper engine, then injects
shared site navigation and footer into the rendered HTML output.
"""

import shutil
import sys
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
            "body": ["FAQ 类型将问答内容按组分类，每组有独立标题。每个问答以卡片形式呈现——问题加粗突出，回答以次级文字显示。适合产品帮助中心、活动 FAQ、政策解读等场景。"]
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


def load_nav(page_id: str) -> str:
    raw = (SITE_DIR / "nav.html").read_text(encoding="utf-8")
    for _, _, p, _, _ in PAGES:
        raw = raw.replace(f"__active_{p}__", "active" if p == page_id else "")
    return raw


def load_footer() -> str:
    return (SITE_DIR / "footer.html").read_text(encoding="utf-8")


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

        html = html.replace("<body>", "<body>\n" + load_nav(page_id), 1)
        html = html.replace("</body>", load_footer() + "\n</body>", 1)

        out_path = OUTPUT_DIR / url_path
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(html, encoding="utf-8")
        print(f"  OK: {data_file} -> {url_path}")

    print(f"\nBuilt {len(PAGES)} pages to {OUTPUT_DIR.resolve()}")


if __name__ == "__main__":
    build()
