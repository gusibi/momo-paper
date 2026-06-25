"""Generic HTML renderer for Momo Paper DSL documents."""

from __future__ import annotations

import json
from html import escape
from pathlib import Path
import re
from typing import Any

from .parser import BlockNode, Document, MarkdownNode

DEFAULT_CSS_FILENAME = "momo-paper.css"
# CDN assets are served from npmmirror (Alibaba), a 1:1 npm mirror with reliable
# access from mainland China; both scripts degrade gracefully if unreachable.
ECHARTS_CDN = "https://registry.npmmirror.com/echarts/5.6.0/files/dist/echarts.min.js"
# Syntax highlighting engine (common-language build). Token COLORS come from the
# active theme's own `.hljs-*` rules, so highlighting matches each design.
HLJS_CDN = "https://registry.npmmirror.com/@highlightjs/cdn-assets/11.9.0/files/highlight.min.js"
CHART_BLOCKS = {
    "bar-chart",
    "candlestick-chart",
    "donut-chart",
    "line-chart",
    "waterfall-chart",
}
HEALTH_BLOCKS = {
    "weekly-summary",
    "goal-tracker",
    "metrics-panel",
    "report-header",
}
# Fields that represent a single action and carry an `href`. They render as a
# real anchor so the link works and is keyboard-focusable, instead of a div
# with a hidden href.
ACTION_FIELDS = {"primary-cta", "secondary-cta", "button", "cta"}


def get_default_css_path() -> Path:
    """Return the bundled default stylesheet path."""
    return Path(__file__).parent / "styles" / DEFAULT_CSS_FILENAME


def render_html(document: Document, css: str | None = None) -> str:
    meta = document.meta
    title = str(meta.get("title", "Untitled"))
    description = str(meta.get("description", ""))
    lang = str(meta.get("locale", "en"))
    nodes = "\n".join(_render_node(node) for node in document.nodes)
    css_text = css if css is not None else get_default_css_path().read_text(encoding="utf-8")
    chart_runtime = _render_chart_runtime() if any(isinstance(node, BlockNode) and node.name in CHART_BLOCKS for node in document.nodes) else ""
    highlight_runtime = _render_highlight_runtime() if any(isinstance(node, MarkdownNode) and "```" in node.text for node in document.nodes) else ""
    return f"""<!DOCTYPE html>
<html lang="{escape(lang)}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <style>
{css_text}
  </style>
</head>
<body>
  <main class="page">
    <header class="doc-header" id="top">
      <div class="doc-header-inner">
        <div class="doc-type">{escape(str(meta.get("document_type", "")))}</div>
        <h1>{escape(title)}</h1>
        {f'<p class="description">{escape(description)}</p>' if description else ''}
      </div>
    </header>
    {nodes}
  </main>
  {chart_runtime}
  {highlight_runtime}
</body>
</html>
"""


def _render_node(node: MarkdownNode | BlockNode) -> str:
    if isinstance(node, MarkdownNode):
        return f'<section class="markdown-node"><div class="markdown-inner">{_render_markdown(node.text)}</div></section>'
    if node.name == "nav":
        return _render_nav(node.props if isinstance(node.props, dict) else {})

    props = node.props
    attrs = ""
    if isinstance(props, dict):
        # `id`, `layout`, and a scalar `columns` are presentation hints, not
        # content: lift them onto the section element (as id / data-* attrs) and
        # drop them from props so they don't render as stray fields. A *list*
        # `columns` (e.g. three-columns) is real content and is left alone.
        drop: set[str] = set()
        if props.get("id"):
            attrs += f' id="{escape(str(props["id"]))}"'
            drop.add("id")
        if props.get("layout"):
            attrs += f' data-layout="{escape(str(props["layout"]))}"'
            drop.add("layout")
        cols = props.get("columns")
        if cols is not None and not isinstance(cols, (list, dict)):
            attrs += f' data-columns="{escape(str(cols))}"'
            drop.add("columns")
        if drop:
            props = {k: v for k, v in props.items() if k not in drop}

    if node.name in CHART_BLOCKS:
        fields = _render_chart_block(node.name, props)
    elif node.name in HEALTH_BLOCKS:
        fields = _render_health_block(node.name, props)
    else:
        fields = _render_value(props)
    return (
        f'<section class="dsl-block" data-block="{escape(node.name)}"{attrs}>'
        f'<div class="block-inner">{fields}</div></section>'
    )


def _render_nav(props: dict[str, Any]) -> str:
    brand = props.get("brand", "")
    items = props.get("items", []) or []
    cta = props.get("cta")

    links: list[str] = []
    for item in items:
        if isinstance(item, dict):
            label = item.get("label", "")
            href = item.get("href", "")
            links.append(f'<a class="nav-link" href="{escape(str(href))}">{_inline(str(label))}</a>')

    brand_html = ""
    if brand:
        brand_html = f'<a class="nav-brand" href="#top">{_inline(str(brand))}</a>'

    cta_html = ""
    if isinstance(cta, dict) and cta.get("label"):
        cta_html = (
            f'<a class="nav-cta" href="{escape(str(cta.get("href", "#")))}">'
            f'{_inline(str(cta.get("label")))}</a>'
        )

    return (
        '<nav class="dsl-nav" data-block="nav">'
        '<div class="nav-inner">'
        f"{brand_html}"
        f'<div class="nav-links">{"".join(links)}</div>'
        f"{cta_html}"
        "</div>"
        "</nav>"
    )


def _render_value(value: Any) -> str:
    if isinstance(value, dict):
        return '<div class="object">' + "".join(_render_field(k, v) for k, v in value.items()) + "</div>"
    if isinstance(value, list):
        return '<ul class="items">' + "".join(f'<li class="item">{_render_value(v)}</li>' for v in value) + "</ul>"
    if value is None:
        return ""
    return f"<p>{_inline(str(value))}</p>"


def _render_field(key: str, value: Any) -> str:
    class_name = re.sub(r"[^a-z0-9-]+", "-", str(key).lower().replace("_", "-")).strip("-")
    if class_name in ACTION_FIELDS and isinstance(value, dict) and value.get("href"):
        label = value.get("label", value.get("text", ""))
        href = escape(str(value.get("href")))
        return (
            f'<div class="field field--{escape(class_name)}">'
            f'<a class="object" href="{href}">{_inline(str(label))}</a>'
            "</div>"
        )
    return (
        f'<div class="field field--{escape(class_name)}">'
        f'<span class="field-key">{escape(str(key).replace("_", " "))}</span>'
        f"{_render_value(value)}"
        "</div>"
    )


def _md_table_cells(row: str) -> list[str]:
    return [c.strip() for c in row.strip().strip("|").split("|")]


def _md_table_is_separator(row: str) -> bool:
    cells = _md_table_cells(row)
    return bool(cells) and all(re.fullmatch(r":?-{1,}:?", c) for c in cells)


def _render_markdown(text: str) -> str:
    lines = text.splitlines()
    out: list[str] = []
    paragraph: list[str] = []
    list_items: list[str] = []
    list_type: str | None = None
    quote: list[str] = []
    table: list[str] = []
    code: list[str] | None = None
    code_lang = ""

    def flush_paragraph() -> None:
        if paragraph:
            out.append(f"<p>{_inline(' '.join(line.strip() for line in paragraph))}</p>")
            paragraph.clear()

    def flush_list() -> None:
        nonlocal list_type
        if list_items:
            tag = "ol" if list_type == "ol" else "ul"
            out.append(f"<{tag}>" + "".join(list_items) + f"</{tag}>")
            list_items.clear()
            list_type = None

    def flush_quote() -> None:
        if quote:
            inner = "".join(f"<p>{_inline(q)}</p>" for q in quote)
            out.append(f"<blockquote>{inner}</blockquote>")
            quote.clear()

    def flush_table() -> None:
        if not table:
            return
        rows = table[:]
        table.clear()
        if len(rows) >= 2 and _md_table_is_separator(rows[1]):
            header = _md_table_cells(rows[0])
            body = [_md_table_cells(r) for r in rows[2:]]
            thead = "<thead><tr>" + "".join(f'<th scope="col">{_inline(c)}</th>' for c in header) + "</tr></thead>"
            trs = "".join("<tr>" + "".join(f"<td>{_inline(c)}</td>" for c in r) + "</tr>" for r in body)
            out.append(f'<div class="table-scroll"><table>{thead}<tbody>{trs}</tbody></table></div>')
        else:
            for r in rows:
                out.append(f"<p>{_inline(r)}</p>")

    def flush_all() -> None:
        flush_paragraph()
        flush_list()
        flush_quote()
        flush_table()

    for raw in lines:
        # Fenced code blocks are copied verbatim (no inline processing).
        if code is not None:
            if raw.strip().startswith("```"):
                lang = f' class="language-{escape(code_lang)}"' if code_lang else ""
                out.append(f"<pre><code{lang}>{escape(chr(10).join(code))}</code></pre>")
                code = None
                code_lang = ""
            else:
                code.append(raw)
            continue

        line = raw.strip()
        is_table_row = line.startswith("|")
        if table and not is_table_row:
            flush_table()
        if line.startswith("```"):
            flush_all()
            code = []
            code_lang = line[3:].strip()
            continue
        if not line:
            flush_all()
            continue
        if is_table_row:
            flush_paragraph()
            flush_list()
            flush_quote()
            table.append(line)
            continue
        if line in {"---", "***", "___"}:
            flush_all()
            out.append("<hr>")
            continue
        if line.startswith("> "):
            flush_paragraph()
            flush_list()
            quote.append(line[2:])
            continue
        if line.startswith("### "):
            flush_all()
            out.append(f"<h3>{_inline(line[4:])}</h3>")
        elif line.startswith("## "):
            flush_all()
            # The page <h1> is the document title (doc-header, or a host-page
            # sr-only h1). Body sections map straight to <h2>, subsections to
            # <h3> — no level skips, and `#` is clamped to <h2> so the page
            # never has a second <h1>.
            out.append(f"<h2>{_inline(line[3:])}</h2>")
        elif line.startswith("# "):
            flush_all()
            out.append(f"<h2>{_inline(line[2:])}</h2>")
        elif line.startswith("- "):
            flush_paragraph()
            flush_quote()
            if list_type not in {None, "ul"}:
                flush_list()
            list_type = "ul"
            list_items.append(f"<li>{_inline(line[2:])}</li>")
        elif re.match(r"^\d+\.\s+", line):
            flush_paragraph()
            flush_quote()
            if list_type not in {None, "ol"}:
                flush_list()
            list_type = "ol"
            list_items.append(f"<li>{_inline(re.sub(r'^\d+\.\s+', '', line))}</li>")
        else:
            flush_list()
            flush_quote()
            paragraph.append(line)

    if code is not None:  # unterminated fence — emit what we have
        out.append(f"<pre><code>{escape(chr(10).join(code))}</code></pre>")
    flush_all()
    return "\n".join(out)


def _inline(text: str) -> str:
    safe = escape(text)
    # Stash inline code so its content is not re-processed (a literal
    # `![x](y)` inside backticks must stay literal, not become an image).
    spans: list[str] = []

    def _stash(match: re.Match[str]) -> str:
        spans.append(match.group(1))
        return f"\x00{len(spans) - 1}\x00"

    safe = re.sub(r"`([^`]+)`", _stash, safe)
    # Images before links so the `[..](..)` of an image is not matched as a link.
    safe = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r'<img src="\2" alt="\1" loading="lazy">', safe)
    safe = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", safe)
    safe = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", safe)
    safe = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', safe)
    safe = re.sub(r"\x00(\d+)\x00", lambda m: f"<code>{spans[int(m.group(1))]}</code>", safe)
    return safe


def _render_chart_block(name: str, props: dict[str, Any]) -> str:
    if name == "bar-chart":
        return _render_echart_block("bar-chart", props, _build_bar_option(props))
    if name == "line-chart":
        return _render_echart_block("line-chart", props, _build_line_option(props))
    if name == "donut-chart":
        return _render_echart_block("donut-chart", props, _build_donut_option(props))
    if name == "candlestick-chart":
        return _render_echart_block("candlestick-chart", props, _build_candlestick_option(props))
    if name == "waterfall-chart":
        return _render_echart_block("waterfall-chart", props, _build_waterfall_option(props))
    return _render_value(props)


def _render_health_block(name: str, props: dict[str, Any]) -> str:
    if name == "weekly-summary":
        return _render_weekly_summary(props)
    if name == "goal-tracker":
        return _render_goal_tracker(props)
    if name == "metrics-panel":
        return _render_metrics_panel(props)
    if name == "report-header":
        return _render_report_header(props)
    return _render_value(props)


def _render_weekly_summary(props: dict[str, Any]) -> str:
    title = props.get("title", "")
    period = props.get("period", "")
    summary = props.get("summary", "")
    positives = props.get("positives", [])
    improvements = props.get("improvements", [])

    parts = ['<div class="health-block health-block--weekly-summary">']
    if title:
        parts.append(f'<h2 class="health-title">{_inline(str(title))}</h2>')
    if period:
        parts.append(f'<div class="health-period">{_inline(str(period))}</div>')
    if summary:
        parts.append(f'<p class="health-summary">{_inline(str(summary))}</p>')

    if positives:
        parts.append('<div class="health-section">')
        parts.append('<h3 class="health-section-title">做得好的方面</h3>')
        parts.append('<div class="health-list health-list--positive">')
        for item in positives:
            if isinstance(item, dict):
                item_title = item.get("title", "")
                item_desc = item.get("desc", "")
                parts.append('<div class="health-item health-item--positive">')
                parts.append(f'<span class="health-icon">✅</span>')
                parts.append('<div class="health-item-content">')
                if item_title:
                    parts.append(f'<div class="health-item-title">{_inline(str(item_title))}</div>')
                if item_desc:
                    parts.append(f'<div class="health-item-desc">{_inline(str(item_desc))}</div>')
                parts.append('</div>')
                parts.append('</div>')
        parts.append('</div>')
        parts.append('</div>')

    if improvements:
        parts.append('<div class="health-section">')
        parts.append('<h3 class="health-section-title">需要改进的方面</h3>')
        parts.append('<div class="health-list health-list--improvement">')
        for item in improvements:
            if isinstance(item, dict):
                item_title = item.get("title", "")
                item_desc = item.get("desc", "")
                parts.append('<div class="health-item health-item--improvement">')
                parts.append(f'<span class="health-icon">💪</span>')
                parts.append('<div class="health-item-content">')
                if item_title:
                    parts.append(f'<div class="health-item-title">{_inline(str(item_title))}</div>')
                if item_desc:
                    parts.append(f'<div class="health-item-desc">{_inline(str(item_desc))}</div>')
                parts.append('</div>')
                parts.append('</div>')
        parts.append('</div>')
        parts.append('</div>')

    parts.append('</div>')
    return "".join(parts)


def _render_goal_tracker(props: dict[str, Any]) -> str:
    title = props.get("title", "")
    goals = props.get("goals", [])

    parts = ['<div class="health-block health-block--goal-tracker">']
    if title:
        parts.append(f'<h2 class="health-title">{_inline(str(title))}</h2>')

    if goals:
        parts.append('<div class="goals-grid">')
        for goal in goals:
            if isinstance(goal, dict):
                goal_title = goal.get("title", "")
                target = goal.get("target", "")
                current = goal.get("current", "")
                unit = goal.get("unit", "")
                desc = goal.get("desc", "")

                target_num = _to_number(target) if target is not None else 0
                current_num = _to_number(current) if current is not None else 0
                progress = 0
                if target_num > 0:
                    progress = min(100, max(0, (current_num / target_num) * 100))

                status_class = "goal-status--good" if progress >= 80 else "goal-status--normal" if progress >= 50 else "goal-status--warning"

                parts.append('<div class="goal-card">')
                parts.append(f'<div class="goal-title">{_inline(str(goal_title))}</div>')
                parts.append('<div class="goal-progress">')
                parts.append(f'<div class="goal-progress-bar" style="width: {progress}%"></div>')
                parts.append('</div>')
                parts.append('<div class="goal-values">')
                parts.append(f'<span class="goal-current">{_inline(str(current))}{_inline(str(unit))}</span>')
                parts.append(f'<span class="goal-separator">/</span>')
                parts.append(f'<span class="goal-target">{_inline(str(target))}{_inline(str(unit))}</span>')
                parts.append('</div>')
                if desc:
                    parts.append(f'<div class="goal-desc">{_inline(str(desc))}</div>')
                parts.append('</div>')
        parts.append('</div>')

    parts.append('</div>')
    return "".join(parts)


def _render_metrics_panel(props: dict[str, Any]) -> str:
    title = props.get("title", "")
    metrics = props.get("metrics", [])

    parts = ['<div class="health-block health-block--metrics-panel">']
    if title:
        parts.append(f'<h2 class="health-title">{_inline(str(title))}</h2>')

    if metrics:
        parts.append('<div class="metrics-grid">')
        for metric in metrics:
            if isinstance(metric, dict):
                label = metric.get("label", "")
                value = metric.get("value", "")
                change = metric.get("change", "")
                status = metric.get("status", "")

                status_class = ""
                if status == "good":
                    status_class = "metric-status--good"
                elif status == "warning":
                    status_class = "metric-status--warning"
                elif status == "danger":
                    status_class = "metric-status--danger"

                parts.append(f'<div class="metric-card {status_class}">')
                parts.append(f'<div class="metric-label">{_inline(str(label))}</div>')
                parts.append(f'<div class="metric-value">{_inline(str(value))}</div>')
                if change:
                    parts.append(f'<div class="metric-change">{_inline(str(change))}</div>')
                parts.append('</div>')
        parts.append('</div>')

    parts.append('</div>')
    return "".join(parts)


def _render_report_header(props: dict[str, Any]) -> str:
    title = props.get("title", "")
    eyebrow = props.get("eyebrow", "")
    date_range = props.get("date_range", "")
    weigh_day = props.get("weigh_day", "")
    meta = props.get("meta", [])
    score = props.get("score", None)

    if score is not None:
        return _render_report_header_scored(props)

    parts = ['<div class="health-block health-block--report-header">']
    parts.append('<div class="report-header">')

    parts.append('<div class="report-header-left">')
    if title:
        parts.append(f'<h2 class="report-title">{_inline(str(title))}</h2>')
    if eyebrow:
        parts.append(f'<div class="report-eyebrow">{_inline(str(eyebrow))}</div>')
    parts.append('</div>')

    has_meta = date_range or weigh_day or meta
    if has_meta:
        parts.append('<div class="report-header-right">')
        parts.append('<div class="report-meta">')
        if date_range:
            parts.append(f'<div class="report-meta-item"><strong>{_inline(str(date_range))}</strong></div>')
        if weigh_day:
            parts.append(f'<div class="report-meta-item">称重日：{_inline(str(weigh_day))}</div>')
        if meta and isinstance(meta, list):
            for item in meta:
                if isinstance(item, dict):
                    label = item.get("label", "")
                    value = item.get("value", "")
                    if label and value:
                        parts.append(f'<div class="report-meta-item">{_inline(str(label))}：{_inline(str(value))}</div>')
                    elif value:
                        parts.append(f'<div class="report-meta-item">{_inline(str(value))}</div>')
        parts.append('</div>')
        parts.append('</div>')

    parts.append('</div>')
    parts.append('</div>')
    return "".join(parts)


def _render_report_header_scored(props: dict[str, Any]) -> str:
    title = props.get("title", "")
    eyebrow = props.get("eyebrow", "")
    date_range = props.get("date_range", "")
    status = props.get("status", "")
    score = props.get("score", "")
    score_label = props.get("score_label", "综合评分")
    score_max = props.get("score_max", "")
    meta = props.get("meta", [])

    parts = ['<div class="health-block health-block--report-header">']
    parts.append('<div class="report-header report-header--scored">')

    parts.append('<div class="report-header-left">')
    if eyebrow:
        parts.append(f'<div class="report-eyebrow">{_inline(str(eyebrow))}</div>')
    if title:
        parts.append(f'<h2 class="report-title">{_inline(str(title))}</h2>')
    inline_bits: list[str] = []
    if date_range:
        inline_bits.append(f'<span class="report-date">{_inline(str(date_range))}</span>')
    if meta and isinstance(meta, list):
        for item in meta:
            if isinstance(item, dict):
                label = item.get("label", "")
                value = item.get("value", "")
                if label and value:
                    inline_bits.append(f'<span>{_inline(str(label))}：{_inline(str(value))}</span>')
                elif value:
                    inline_bits.append(f'<span>{_inline(str(value))}</span>')
    if inline_bits:
        parts.append('<div class="report-inline-meta">' + "".join(inline_bits) + '</div>')
    parts.append('</div>')

    parts.append('<div class="report-header-right">')
    if status:
        parts.append(f'<div class="report-status">{_inline(str(status))}</div>')
    score_text = f"{escape(str(score))}"
    if score_max not in (None, ""):
        label_line = f"{_inline(str(score_label))} · /{_inline(str(score_max))}"
    else:
        label_line = _inline(str(score_label))
    parts.append('<div class="report-score-card">')
    parts.append(f'<strong>{score_text}</strong>')
    parts.append(f'<span>{label_line}</span>')
    parts.append('</div>')
    parts.append('</div>')

    parts.append('</div>')
    parts.append('</div>')
    return "".join(parts)


def _render_chart_header(props: dict[str, Any]) -> str:
    parts: list[str] = ['<div class="chart-header">']
    title = props.get("title")
    subtitle = props.get("subtitle")
    if title is not None:
        # A chart is a sub-component that sits under a section heading, so its
        # title is an <h3> — keeping it below body <h2> sections in the outline.
        parts.append(f'<h3 class="chart-title">{_inline(str(title))}</h3>')
    if subtitle is not None:
        parts.append(f'<p class="chart-subtitle">{_inline(str(subtitle))}</p>')
    parts.append("</div>")
    return "".join(parts)


def _render_chart_meta(pairs: list[tuple[str, Any]]) -> str:
    items = [(label, value) for label, value in pairs if value not in (None, "")]
    if not items:
        return ""
    out = ['<dl class="chart-meta">']
    for label, value in items:
        out.append(f"<div><dt>{escape(label)}</dt><dd>{_inline(str(value))}</dd></div>")
    out.append("</dl>")
    return "".join(out)


def _render_echart_block(kind: str, props: dict[str, Any], option: dict[str, Any]) -> str:
    meta_pairs: list[tuple[str, Any]] = []
    if kind in {"bar-chart", "line-chart"}:
        meta_pairs.append(("单位", props.get("unit")))
    elif kind == "candlestick-chart":
        meta_pairs.extend([("X 轴", props.get("x_axis")), ("Y 轴", props.get("y_axis"))])
    elif kind == "waterfall-chart":
        meta_pairs.extend([("起点", props.get("start")), ("终点", props.get("end"))])
    return (
        f'<div class="chart-block chart-block--echart chart-block--{escape(kind)}">'
        f"{_render_chart_header(props)}"
        f"{_render_chart_meta(meta_pairs)}"
        '<div class="chart-surface chart-surface--echart">'
        f'<div class="echart-canvas" data-chart-kind="{escape(kind)}"></div>'
        f'<script type="application/json" class="echart-config">{_json_text(option)}</script>'
        "</div>"
        "</div>"
    )


def _build_bar_option(props: dict[str, Any]) -> dict[str, Any]:
    items = [item for item in props.get("items", []) if isinstance(item, dict)]
    labels = [str(item.get("label", "")) for item in items]
    values = [_to_number(item.get("value")) for item in items]
    shares = [str(item.get("share", "")) for item in items]
    return {
        "color": ["#244c7a"],
        "grid": {"left": 72, "right": 24, "top": 20, "bottom": 48, "containLabel": True},
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {"type": "shadow"},
            "formatter": _js_function(
                "params",
                "const item = params[0]; const note = item.data.share ? `<br/>占比: ${item.data.share}` : ''; return `${item.axisValue}<br/>数值: ${item.data.value}${note}`;",
            ),
        },
        "xAxis": {
            "type": "category",
            "data": labels,
            "axisTick": {"show": False},
            "axisLine": {"lineStyle": {"color": "#d8d2c4"}},
            "axisLabel": {"color": "#4c566a", "interval": 0},
        },
        "yAxis": {
            "type": "value",
            "name": str(props.get("unit", "")),
            "nameTextStyle": {"color": "#4c566a"},
            "splitLine": {"lineStyle": {"color": "rgba(76, 86, 106, 0.12)"}},
            "axisLabel": {"color": "#4c566a"},
        },
        "series": [{
            "type": "bar",
            "barWidth": "44%",
            "itemStyle": {"borderRadius": [6, 6, 0, 0]},
            "label": {"show": True, "position": "top", "color": "#172033"},
            "data": [{"value": value, "share": share} for value, share in zip(values, shares)],
        }],
    }


def _build_line_option(props: dict[str, Any]) -> dict[str, Any]:
    items = [item for item in props.get("items", []) if isinstance(item, dict)]
    labels = [str(item.get("period", "")) for item in items]
    values = [_to_number(item.get("value")) for item in items]
    growth = [str(item.get("growth", "")) for item in items]
    return {
        "color": ["#244c7a"],
        "grid": {"left": 64, "right": 24, "top": 24, "bottom": 48, "containLabel": True},
        "tooltip": {
            "trigger": "axis",
            "formatter": _js_function(
                "params",
                "const item = params[0]; const growth = item.data.growth ? `<br/>增速: ${item.data.growth}` : ''; return `${item.axisValue}<br/>数值: ${item.data.value}${growth}`;",
            ),
        },
        "xAxis": {
            "type": "category",
            "boundaryGap": False,
            "data": labels,
            "axisLine": {"lineStyle": {"color": "#d8d2c4"}},
            "axisLabel": {"color": "#4c566a", "interval": 0},
        },
        "yAxis": {
            "type": "value",
            "name": str(props.get("unit", "")),
            "nameTextStyle": {"color": "#4c566a"},
            "splitLine": {"lineStyle": {"color": "rgba(76, 86, 106, 0.12)"}},
            "axisLabel": {"color": "#4c566a"},
        },
        "series": [{
            "type": "line",
            "smooth": True,
            "symbolSize": 10,
            "lineStyle": {"width": 4},
            "areaStyle": {"color": "rgba(36, 76, 122, 0.12)"},
            "data": [{"value": value, "growth": note} for value, note in zip(values, growth)],
        }],
    }


def _build_donut_option(props: dict[str, Any]) -> dict[str, Any]:
    items = [item for item in props.get("segments", []) if isinstance(item, dict)]
    center_value = str(props.get("center_value", ""))
    center_label = str(props.get("center_label", ""))
    return {
        "color": ["#244c7a", "#5c7fa3", "#b65c3a", "#2f6b4f", "#8eaac3"],
        "tooltip": {"trigger": "item", "formatter": "{b}: {c}"},
        "legend": {
            "bottom": 0,
            "left": "center",
            "textStyle": {"color": "#4c566a"},
            "itemWidth": 10,
            "itemHeight": 10,
        },
        "graphic": [{
            "type": "group",
            "left": "center",
            "top": "center",
            "children": [
                {"type": "text", "style": {"text": center_value, "fill": "#244c7a", "font": "700 30px Noto Serif SC"}},
                {"type": "text", "top": 34, "style": {"text": center_label, "fill": "#4c566a", "font": "500 11px IBM Plex Mono"}},
            ],
        }],
        "series": [{
            "type": "pie",
            "radius": ["56%", "74%"],
            "center": ["50%", "42%"],
            "label": {"show": False},
            "labelLine": {"show": False},
            "data": [{"name": str(item.get("label", "")), "value": _to_number(item.get("value"))} for item in items],
        }],
    }


def _build_candlestick_option(props: dict[str, Any]) -> dict[str, Any]:
    items = [item for item in props.get("items", []) if isinstance(item, dict)]
    dates = [str(item.get("date", "")) for item in items]
    values = [[_to_number(item.get("open")), _to_number(item.get("close")), _to_number(item.get("low")), _to_number(item.get("high"))] for item in items]
    notes = [str(item.get("note", "")) for item in items]
    return {
        "animation": False,
        "grid": {"left": 64, "right": 24, "top": 28, "bottom": 52, "containLabel": True},
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {"type": "cross"},
            "formatter": _js_function(
                "params",
                "const p = params[0]; const d = p.data || []; const note = p.data && p.data.note ? `<br/>备注: ${p.data.note}` : ''; return `${p.axisValue}<br/>开: ${d[0]}<br/>收: ${d[1]}<br/>低: ${d[2]}<br/>高: ${d[3]}${note}`;",
            ),
        },
        "xAxis": {
            "type": "category",
            "data": dates,
            "scale": True,
            "boundaryGap": True,
            "axisLine": {"lineStyle": {"color": "#d8d2c4"}},
            "axisLabel": {"color": "#4c566a", "interval": 0},
        },
        "yAxis": {
            "type": "value",
            "name": str(props.get("y_axis", "")),
            "scale": True,
            "splitArea": {"show": False},
            "splitLine": {"lineStyle": {"color": "rgba(76, 86, 106, 0.12)"}},
            "axisLabel": {"color": "#4c566a"},
        },
        "series": [{
            "type": "candlestick",
            "data": [{"value": value, "note": note} for value, note in zip(values, notes)],
            "itemStyle": {
                "color": "#2f6b4f",
                "color0": "#9a3d3d",
                "borderColor": "#2f6b4f",
                "borderColor0": "#9a3d3d",
            },
        }],
    }


def _build_waterfall_option(props: dict[str, Any]) -> dict[str, Any]:
    items = [item for item in props.get("items", []) if isinstance(item, dict)]
    labels = [str(item.get("label", "")) for item in items]
    values = [_to_number(item.get("value")) for item in items]
    types = [str(item.get("type", "")) for item in items]
    cumulative = 0.0
    base: list[float] = []
    positive: list[float | str] = []
    negative: list[float | str] = []
    total: list[float | str] = []
    for value, item_type in zip(values, types):
        if item_type in {"start", "end"}:
            base.append(0.0)
            positive.append("-")
            negative.append("-")
            total.append(value)
            cumulative = value
        elif value >= 0:
            base.append(cumulative)
            positive.append(value)
            negative.append("-")
            total.append("-")
            cumulative += value
        else:
            base.append(cumulative + value)
            positive.append("-")
            negative.append(abs(value))
            total.append("-")
            cumulative += value
    return {
        "grid": {"left": 64, "right": 24, "top": 24, "bottom": 56, "containLabel": True},
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {"type": "shadow"},
            "formatter": _js_function(
                "params",
                "const rows = params.filter(Boolean).filter(p => p.data !== '-'); if (!rows.length) return ''; const item = rows[rows.length - 1]; return `${item.axisValue}<br/>${item.seriesName}: ${item.data}`;",
            ),
        },
        "legend": {"bottom": 0, "textStyle": {"color": "#4c566a"}},
        "xAxis": {
            "type": "category",
            "data": labels,
            "axisLabel": {"color": "#4c566a", "interval": 0},
            "axisLine": {"lineStyle": {"color": "#d8d2c4"}},
        },
        "yAxis": {
            "type": "value",
            "splitLine": {"lineStyle": {"color": "rgba(76, 86, 106, 0.12)"}},
            "axisLabel": {"color": "#4c566a"},
        },
        "series": [
            {"name": "基线", "type": "bar", "stack": "total", "silent": True, "itemStyle": {"color": "transparent"}, "data": base},
            {"name": "上行", "type": "bar", "stack": "total", "itemStyle": {"color": "#2f6b4f", "borderRadius": [6, 6, 0, 0]}, "data": positive},
            {"name": "下行", "type": "bar", "stack": "total", "itemStyle": {"color": "#9a3d3d", "borderRadius": [6, 6, 0, 0]}, "data": negative},
            {"name": "总值", "type": "bar", "stack": "total", "itemStyle": {"color": "#244c7a", "borderRadius": [6, 6, 0, 0]}, "data": total},
        ],
    }


def _to_number(value: Any) -> float:
    if isinstance(value, (int, float)):
        return float(value)
    if value is None:
        return 0.0
    text = str(value).strip().replace(",", "")
    match = re.search(r"-?\d+(?:\.\d+)?", text)
    return float(match.group(0)) if match else 0.0


def _to_percent_fraction(value: Any) -> float:
    text = str(value).strip()
    if text.endswith("%"):
        return _to_number(text) / 100.0
    number = _to_number(text)
    return number if 0 <= number <= 1 else number / 100.0


def _clamp01(value: float) -> float:
    return max(0.0, min(1.0, value))


def _json_text(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False).replace("</", "<\\/")


def _js_function(arg_name: str, body: str) -> dict[str, str]:
    return {"__js_function__": f"function({arg_name}){{{body}}}"}


def _render_highlight_runtime() -> str:
    return f"""
  <script src="{HLJS_CDN}"></script>
  <script>
    (() => {{
      if (typeof hljs === "undefined") return;
      hljs.configure({{ ignoreUnescapedHTML: true }});
      document.querySelectorAll("pre code").forEach((el) => hljs.highlightElement(el));
    }})();
  </script>"""


def _render_chart_runtime() -> str:
    return f"""
  <script src="{ECHARTS_CDN}"></script>
  <script>
    (() => {{
      const revive = (value) => {{
        if (Array.isArray(value)) return value.map(revive);
        if (value && typeof value === "object") {{
          if (typeof value.__js_function__ === "string") {{
            return Function(`return (${{value.__js_function__}})`)();
          }}
          for (const key of Object.keys(value)) value[key] = revive(value[key]);
        }}
        return value;
      }};
      // Resolve chart colors from the active theme's CSS variables so the same
      // markup renders correctly under any stylesheet. Each variable falls back
      // to the color baked into the option when it is not defined.
      const css = getComputedStyle(document.documentElement);
      const v = (name) => css.getPropertyValue(name).trim();
      const merge = (base, extra) => Object.assign({{}}, base || {{}}, extra);
      const applyTheme = (opt) => {{
        const series = ["--chart-1", "--chart-2", "--chart-3", "--chart-4", "--chart-5"].map(v).filter(Boolean);
        if (series.length) opt.color = series;
        const axisLine = v("--chart-axis-line");
        const splitLine = v("--chart-split-line");
        const axisLabel = v("--chart-axis-label");
        const axisName = v("--chart-axis-name");
        const legend = v("--chart-legend");
        const dataLabel = v("--chart-data-label");
        for (const ax of ["xAxis", "yAxis"]) {{
          let group = opt[ax];
          if (!group) continue;
          for (const a of (Array.isArray(group) ? group : [group])) {{
            if (axisLine) a.axisLine = merge(a.axisLine, {{ lineStyle: merge(a.axisLine && a.axisLine.lineStyle, {{ color: axisLine }}) }});
            if (splitLine) a.splitLine = merge(a.splitLine, {{ lineStyle: merge(a.splitLine && a.splitLine.lineStyle, {{ color: splitLine }}) }});
            if (axisLabel) a.axisLabel = merge(a.axisLabel, {{ color: axisLabel }});
            if (axisName) a.nameTextStyle = merge(a.nameTextStyle, {{ color: axisName }});
          }}
        }}
        if (legend && opt.legend) {{
          for (const l of (Array.isArray(opt.legend) ? opt.legend : [opt.legend])) l.textStyle = merge(l.textStyle, {{ color: legend }});
        }}
        const up = v("--chart-up");
        const down = v("--chart-down");
        for (const s of (opt.series || [])) {{
          if (dataLabel && s.label && s.label.show) s.label = merge(s.label, {{ color: dataLabel }});
          if (s.type === "candlestick" && (up || down)) {{
            s.itemStyle = merge(s.itemStyle, {{
              color: up || (s.itemStyle && s.itemStyle.color),
              color0: down || (s.itemStyle && s.itemStyle.color0),
              borderColor: up || (s.itemStyle && s.itemStyle.borderColor),
              borderColor0: down || (s.itemStyle && s.itemStyle.borderColor0),
            }});
          }}
          if (s.type === "bar" && s.name === "上行" && up) s.itemStyle = merge(s.itemStyle, {{ color: up }});
          if (s.type === "bar" && s.name === "下行" && down) s.itemStyle = merge(s.itemStyle, {{ color: down }});
          if (s.type === "bar" && s.name === "总值" && series[0]) s.itemStyle = merge(s.itemStyle, {{ color: series[0] }});
          if (s.type === "line" && series[0]) s.areaStyle = merge(s.areaStyle, {{ color: v("--chart-area") || (s.areaStyle && s.areaStyle.color) }});
        }}
        const centerValue = v("--chart-center-value");
        const centerLabel = v("--chart-center-label");
        for (const g of (opt.graphic || [])) {{
          const kids = g.children || [];
          if (kids[0] && centerValue) kids[0].style = merge(kids[0].style, {{ fill: centerValue }});
          if (kids[1] && centerLabel) kids[1].style = merge(kids[1].style, {{ fill: centerLabel }});
        }}
        return opt;
      }};
      const nodes = document.querySelectorAll(".echart-config");
      const charts = [];
      for (const node of nodes) {{
        const canvas = node.previousElementSibling;
        if (!canvas || typeof echarts === "undefined") continue;
        const option = applyTheme(revive(JSON.parse(node.textContent)));
        const chart = echarts.init(canvas, null, {{ renderer: "svg" }});
        chart.setOption(option);
        charts.push(chart);
      }}
      window.addEventListener("resize", () => charts.forEach(chart => chart.resize()));
    }})();
  </script>"""
