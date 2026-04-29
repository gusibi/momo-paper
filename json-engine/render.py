#!/usr/bin/env python3
"""
Momo Paper JSON Rendering Engine

Reads a JSON data file + a Jinja2 template, outputs rendered HTML.

Usage:
    python render.py --data data/sample-equity-report.json --output output/report.html
    python render.py --data data/sample.json --template templates/custom.html.j2 --output out.html
"""

import argparse
import json
import math
import sys
from pathlib import Path

try:
    from jinja2 import Environment, FileSystemLoader, select_autoescape
except ImportError:
    print("Error: jinja2 is required. Install with: pip install jinja2")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Chart rendering (SVG)
# ---------------------------------------------------------------------------

CHART_COLORS = {
    "primary": "#244C7A",
    "secondary": "#5C7FA3",
    "tertiary": "#8EAAC3",
    "accent": "#B65C3A",
    "positive": "#2F6B4F",
    "negative": "#9A3D3D",
    "neutral": "#7D8798",
    "muted": "#B8CAD9",
    "categorical": ["#244C7A", "#B65C3A", "#2F6B4F", "#8A6D3B", "#5E6177", "#7A8EA1"],
}


def _svg_header(width: int, height: int, title: str = "") -> str:
    t = f' aria-label="{title}"' if title else ""
    return f'<svg width="100%" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg"{t}>'


def render_bar_chart(chart: dict) -> str:
    """Render a bar chart as SVG."""
    data = chart.get("data", {})
    labels = data.get("labels", [])
    values = data.get("values", [])
    if not labels or not values:
        return ""

    w, h = 720, chart.get("height", 280)
    margin = {"top": 40, "right": 20, "bottom": 50, "left": 50}
    cw = w - margin["left"] - margin["right"]
    ch = h - margin["top"] - margin["bottom"]

    max_v = max(values) * 1.1 if values else 1
    bar_w = (cw / len(values)) * 0.6
    gap = (cw / len(values)) * 0.4
    color = CHART_COLORS["primary"]

    parts = [_svg_header(w, h, chart.get("title", ""))]

    # Title
    if chart.get("title"):
        parts.append(f'<text x="{margin['left']}" y="24" font-family="Inter, sans-serif" font-size="14" font-weight="600" fill="#172033">{chart['title']}</text>')

    # Grid lines
    grid_count = 5
    for i in range(grid_count + 1):
        y = margin["top"] + ch - (ch * i / grid_count)
        val = max_v * i / grid_count
        parts.append(f'<line x1="{margin["left"]}" y1="{y}" x2="{w - margin["right"]}" y2="{y}" stroke="#D8D2C4" stroke-width="0.5"/>')
        parts.append(f'<text x="{margin["left"] - 8}" y="{y + 4}" text-anchor="end" font-family="IBM Plex Mono, monospace" font-size="10" fill="#4C566A">{val:.0f}</text>')

    # Bars
    for i, (label, value) in enumerate(zip(labels, values)):
        x = margin["left"] + gap / 2 + i * (bar_w + gap)
        bar_h = (value / max_v) * ch
        y = margin["top"] + ch - bar_h
        parts.append(f'<rect x="{x}" y="{y}" width="{bar_w}" height="{bar_h}" fill="{color}" rx="2"/>')
        # Label
        lx = x + bar_w / 2
        ly = margin["top"] + ch + 18
        parts.append(f'<text x="{lx}" y="{ly}" text-anchor="middle" font-family="Inter, sans-serif" font-size="11" fill="#4C566A">{label}</text>')
        # Value on top
        parts.append(f'<text x="{lx}" y="{y - 6}" text-anchor="middle" font-family="IBM Plex Mono, monospace" font-size="10" fill="#172033">{value}</text>')

    parts.append("</svg>")
    return "\n".join(parts)


def render_line_chart(chart: dict) -> str:
    """Render a line chart as SVG."""
    data = chart.get("data", {})
    labels = data.get("labels", [])
    values = data.get("values", [])
    if not labels or not values:
        return ""

    w, h = 720, chart.get("height", 280)
    margin = {"top": 40, "right": 30, "bottom": 50, "left": 50}
    cw = w - margin["left"] - margin["right"]
    ch = h - margin["top"] - margin["bottom"]

    max_v = max(values) * 1.1 if values else 1
    min_v = min(0, min(values) * 0.9)
    range_v = max_v - min_v if max_v != min_v else 1
    color = CHART_COLORS["primary"]

    parts = [_svg_header(w, h, chart.get("title", ""))]

    if chart.get("title"):
        parts.append(f'<text x="{margin['left']}" y="24" font-family="Inter, sans-serif" font-size="14" font-weight="600" fill="#172033">{chart['title']}</text>')

    # Grid lines
    grid_count = 5
    for i in range(grid_count + 1):
        y = margin["top"] + ch - (ch * i / grid_count)
        val = min_v + range_v * i / grid_count
        parts.append(f'<line x1="{margin["left"]}" y1="{y}" x2="{w - margin["right"]}" y2="{y}" stroke="#D8D2C4" stroke-width="0.5"/>')
        parts.append(f'<text x="{margin["left"] - 8}" y="{y + 4}" text-anchor="end" font-family="IBM Plex Mono, monospace" font-size="10" fill="#4C566A">{val:.0f}</text>')

    # Points and path
    step = cw / (len(values) - 1) if len(values) > 1 else cw
    points = []
    for i, v in enumerate(values):
        x = margin["left"] + i * step
        y = margin["top"] + ch - ((v - min_v) / range_v) * ch
        points.append((x, y))

    # Area fill
    area_path = f"M {points[0][0]} {margin['top'] + ch}"
    for x, y in points:
        area_path += f" L {x} {y}"
    area_path += f" L {points[-1][0]} {margin['top'] + ch} Z"
    parts.append(f'<path d="{area_path}" fill="{CHART_COLORS['primary']}" opacity="0.08"/>')

    # Line
    line_path = f"M {points[0][0]} {points[0][1]}"
    for x, y in points[1:]:
        line_path += f" L {x} {y}"
    parts.append(f'<path d="{line_path}" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')

    # Dots
    for i, (x, y) in enumerate(points):
        parts.append(f'<circle cx="{x}" cy="{y}" r="4" fill="{color}"/>')
        parts.append(f'<circle cx="{x}" cy="{y}" r="2" fill="#FAF8F4"/>')
        # Value label
        parts.append(f'<text x="{x}" y="{y - 10}" text-anchor="middle" font-family="IBM Plex Mono, monospace" font-size="10" fill="#172033">{values[i]}</text>')
        # X-axis label
        lx = x
        ly = margin["top"] + ch + 18
        parts.append(f'<text x="{lx}" y="{ly}" text-anchor="middle" font-family="Inter, sans-serif" font-size="11" fill="#4C566A">{labels[i]}</text>')

    parts.append("</svg>")
    return "\n".join(parts)


def render_donut_chart(chart: dict) -> str:
    """Render a donut chart as SVG."""
    data = chart.get("data", {})
    labels = data.get("labels", [])
    values = data.get("values", [])
    if not labels or not values:
        return ""

    w = 720
    h = chart.get("height", 320)
    cx, cy = w / 2, h / 2
    radius = min(cx, cy) - 40
    inner_r = radius * 0.55
    total = sum(values)
    if total == 0:
        return ""

    colors = CHART_COLORS["categorical"]
    parts = [_svg_header(w, h, chart.get("title", ""))]

    if chart.get("title"):
        parts.append(f'<text x="{cx}" y="24" text-anchor="middle" font-family="Inter, sans-serif" font-size="14" font-weight="600" fill="#172033">{chart['title']}</text>')

    # Draw arcs
    start_angle = -math.pi / 2
    for i, (label, value) in enumerate(zip(labels, values)):
        angle = (value / total) * 2 * math.pi
        end_angle = start_angle + angle
        color = colors[i % len(colors)]

        # Outer arc
        x1 = cx + radius * math.cos(start_angle)
        y1 = cy + radius * math.sin(start_angle)
        x2 = cx + radius * math.cos(end_angle)
        y2 = cy + radius * math.sin(end_angle)
        large_arc = 1 if angle > math.pi else 0

        # Inner arc (reverse direction)
        ix2 = cx + inner_r * math.cos(end_angle)
        iy2 = cy + inner_r * math.sin(end_angle)
        ix1 = cx + inner_r * math.cos(start_angle)
        iy1 = cy + inner_r * math.sin(start_angle)

        path = f"M {x1} {y1} A {radius} {radius} 0 {large_arc} 1 {x2} {y2} L {ix2} {iy2} A {inner_r} {inner_r} 0 {large_arc} 0 {ix1} {iy1} Z"
        parts.append(f'<path d="{path}" fill="{color}"/>')

        start_angle = end_angle

    # Center text
    parts.append(f'<text x="{cx}" y="{cy - 6}" text-anchor="middle" font-family="IBM Plex Mono, monospace" font-size="12" fill="#4C566A">Total</text>')
    parts.append(f'<text x="{cx}" y="{cy + 16}" text-anchor="middle" font-family="Inter, sans-serif" font-size="20" font-weight="600" fill="#172033">{total}</text>')

    # Legend
    legend_x = cx + radius + 30
    legend_y = cy - (len(labels) * 20) / 2
    for i, (label, value) in enumerate(zip(labels, values)):
        y = legend_y + i * 24
        color = colors[i % len(colors)]
        pct = f"{(value / total * 100):.1f}%"
        parts.append(f'<rect x="{legend_x}" y="{y - 6}" width="10" height="10" fill="{color}" rx="2"/>')
        parts.append(f'<text x="{legend_x + 18}" y="{y + 2}" font-family="Inter, sans-serif" font-size="12" fill="#172033">{label}</text>')
        parts.append(f'<text x="{legend_x + 18}" y="{y + 14}" font-family="IBM Plex Mono, monospace" font-size="10" fill="#4C566A">{pct} ({value})</text>')

    parts.append("</svg>")
    return "\n".join(parts)


def render_chart_filter(chart_data: dict) -> str:
    """Jinja2 filter: render chart dict to SVG HTML."""
    if not chart_data or not isinstance(chart_data, dict):
        return ""
    chart_type = chart_data.get("type", "bar")
    if chart_type == "bar":
        return render_bar_chart(chart_data)
    elif chart_type == "line":
        return render_line_chart(chart_data)
    elif chart_type == "donut":
        return render_donut_chart(chart_data)
    return f"<!-- unsupported chart type: {chart_type} -->"


# ---------------------------------------------------------------------------
# Route registry
# ---------------------------------------------------------------------------
DEFAULT_TEMPLATE_MAP = {
    "equity_report": "equity-report.html.j2",
    "one_pager": "one-pager.html.j2",
    "long_doc": "long-doc.html.j2",
    "letter": "letter.html.j2",
    "portfolio": "portfolio.html.j2",
    "resume": "resume.html.j2",
    "changelog": "changelog.html.j2",
    "process_flow": "process-flow.html.j2",
    "timeline": "timeline.html.j2",
    "faq_page": "faq-page.html.j2",
    "case_study": "case-study.html.j2",
    "research_summary": "research-summary.html.j2",
    "stats_report": "stats-report.html.j2",
    "infographic": "infographic.html.j2",
}


def resolve_template(document_type: str, template_dir: Path, explicit_template: str | None = None) -> str:
    if explicit_template:
        return explicit_template
    default = DEFAULT_TEMPLATE_MAP.get(document_type)
    if not default:
        raise ValueError(
            f"No default template for document_type '{document_type}'. "
            f"Known types: {list(DEFAULT_TEMPLATE_MAP.keys())}"
        )
    return default


def load_json(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError("JSON root must be an object")
    required = ["document_type", "locale", "meta", "sections"]
    missing = [k for k in required if k not in data]
    if missing:
        raise ValueError(f"Missing required fields: {missing}")
    return data


def render(data: dict, template_path: str, template_dir: Path) -> str:
    env = Environment(
        loader=FileSystemLoader(str(template_dir)),
        autoescape=select_autoescape(["html", "xml"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.filters["render_chart"] = render_chart_filter
    template = env.get_template(template_path)
    return template.render(**data)


def main():
    parser = argparse.ArgumentParser(description="Momo Paper JSON Rendering Engine")
    parser.add_argument("--data", "-d", required=True, help="Path to JSON data file")
    parser.add_argument("--template", "-t", help="Explicit template file (overrides document_type mapping)")
    parser.add_argument("--output", "-o", required=True, help="Output HTML file path")
    parser.add_argument("--template-dir", default="templates", help="Directory containing Jinja2 templates")
    args = parser.parse_args()

    data_path = Path(args.data)
    output_path = Path(args.output)
    template_dir = Path(args.template_dir)

    if not data_path.exists():
        print(f"Error: Data file not found: {data_path}")
        sys.exit(1)
    if not template_dir.exists():
        print(f"Error: Template directory not found: {template_dir}")
        sys.exit(1)

    try:
        data = load_json(data_path)
    except (json.JSONDecodeError, ValueError) as e:
        print(f"Error loading data: {e}")
        sys.exit(1)

    try:
        template_file = resolve_template(data["document_type"], template_dir, args.template)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    try:
        html = render(data, template_file, template_dir)
    except Exception as e:
        print(f"Error rendering template: {e}")
        sys.exit(1)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Rendered: {output_path}")
    print(f"  document_type : {data['document_type']}")
    print(f"  locale        : {data['locale']}")
    print(f"  template      : {template_file}")
    print(f"  sections      : {list(data.get('sections', {}).keys())}")


if __name__ == "__main__":
    main()
