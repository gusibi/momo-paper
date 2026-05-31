"""Generic HTML renderer for Momo Paper DSL documents."""

from __future__ import annotations

import json
from html import escape
from pathlib import Path
import re
from typing import Any

from .parser import BlockNode, Document, MarkdownNode

DEFAULT_CSS_FILENAME = "momo-paper.css"
ECHARTS_CDN = "https://cdn.jsdelivr.net/npm/echarts@6/dist/echarts.min.js"
CHART_BLOCKS = {
    "bar-chart",
    "candlestick-chart",
    "donut-chart",
    "line-chart",
    "waterfall-chart",
}


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
    <header class="doc-header">
      <div class="doc-header-inner">
        <div class="doc-type">{escape(str(meta.get("document_type", "")))}</div>
        <h1>{escape(title)}</h1>
        {f'<p class="description">{escape(description)}</p>' if description else ''}
      </div>
    </header>
    {nodes}
  </main>
  {chart_runtime}
</body>
</html>
"""


def _render_node(node: MarkdownNode | BlockNode) -> str:
    if isinstance(node, MarkdownNode):
        return f'<section class="markdown-node"><div class="markdown-inner">{_render_markdown(node.text)}</div></section>'
    if node.name in CHART_BLOCKS:
        fields = _render_chart_block(node)
    else:
        fields = _render_value(node.props)
    return (
        f'<section class="dsl-block" data-block="{escape(node.name)}">'
        f'<div class="block-inner"><div class="block-kicker">{escape(node.name)}</div>{fields}</div></section>'
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
    return (
        f'<div class="field field--{escape(class_name)}">'
        f'<span class="field-key">{escape(str(key).replace("_", " "))}</span>'
        f"{_render_value(value)}"
        "</div>"
    )


def _render_markdown(text: str) -> str:
    lines = text.splitlines()
    out: list[str] = []
    paragraph: list[str] = []
    list_items: list[str] = []
    list_type: str | None = None

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

    for raw in lines:
        line = raw.strip()
        if not line:
            flush_paragraph()
            flush_list()
            continue
        if line.startswith("### "):
            flush_paragraph()
            flush_list()
            out.append(f"<h3>{_inline(line[4:])}</h3>")
        elif line.startswith("## "):
            flush_paragraph()
            flush_list()
            out.append(f"<h2>{_inline(line[3:])}</h2>")
        elif line.startswith("# "):
            flush_paragraph()
            flush_list()
            out.append(f"<h1>{_inline(line[2:])}</h1>")
        elif line.startswith("- "):
            flush_paragraph()
            if list_type not in {None, "ul"}:
                flush_list()
            list_type = "ul"
            list_items.append(f"<li>{_inline(line[2:])}</li>")
        elif re.match(r"^\d+\.\s+", line):
            flush_paragraph()
            if list_type not in {None, "ol"}:
                flush_list()
            list_type = "ol"
            list_items.append(f"<li>{_inline(re.sub(r'^\d+\.\s+', '', line))}</li>")
        else:
            flush_list()
            paragraph.append(line)

    flush_paragraph()
    flush_list()
    return "\n".join(out)


def _inline(text: str) -> str:
    safe = escape(text)
    safe = re.sub(r"`([^`]+)`", r"<code>\1</code>", safe)
    safe = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", safe)
    safe = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", safe)
    safe = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', safe)
    return safe


def _render_chart_block(node: BlockNode) -> str:
    if node.name == "bar-chart":
        return _render_echart_block("bar-chart", node.props, _build_bar_option(node.props))
    if node.name == "line-chart":
        return _render_echart_block("line-chart", node.props, _build_line_option(node.props))
    if node.name == "donut-chart":
        return _render_echart_block("donut-chart", node.props, _build_donut_option(node.props))
    if node.name == "candlestick-chart":
        return _render_echart_block("candlestick-chart", node.props, _build_candlestick_option(node.props))
    if node.name == "waterfall-chart":
        return _render_echart_block("waterfall-chart", node.props, _build_waterfall_option(node.props))
    return _render_value(node.props)


def _render_chart_header(props: dict[str, Any]) -> str:
    parts: list[str] = ['<div class="chart-header">']
    title = props.get("title")
    subtitle = props.get("subtitle")
    if title is not None:
        parts.append(f'<h2 class="chart-title">{_inline(str(title))}</h2>')
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
      const nodes = document.querySelectorAll(".echart-config");
      const charts = [];
      for (const node of nodes) {{
        const canvas = node.previousElementSibling;
        if (!canvas || typeof echarts === "undefined") continue;
        const option = revive(JSON.parse(node.textContent));
        const chart = echarts.init(canvas, null, {{ renderer: "svg" }});
        chart.setOption(option);
        charts.push(chart);
      }}
      window.addEventListener("resize", () => charts.forEach(chart => chart.resize()));
    }})();
  </script>"""
