"""SVG chart rendering: bar, line, donut."""

import math

CHART_COLORS = {
    "primary": "#244C7A",
    "secondary": "#5C7FA3",
    "tertiary": "#8EAAC3",
    "accent": "#B65C3A",
    "positive": "#2F6B4F",
    "negative": "#9A3D3D",
    "neutral": "#7D8798",
    "categorical": ["#244C7A", "#B65C3A", "#2F6B4F", "#8A6D3B", "#5E6177", "#7A8EA1"],
}


def _svg_tag(width: int, height: int, title: str = "") -> str:
    t = f' aria-label="{title}"' if title else ""
    return f'<svg width="100%" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg"{t}>'


def render_bar(chart: dict) -> str:
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

    parts = [_svg_tag(w, h, chart.get("title", ""))]

    if chart.get("title"):
        parts.append(
            f'<text x="{margin["left"]}" y="24" font-family="Inter, sans-serif" '
            f'font-size="14" font-weight="600" fill="#172033">{chart["title"]}</text>'
        )

    for i in range(6):
        y = margin["top"] + ch - (ch * i / 5)
        val = max_v * i / 5
        parts.append(
            f'<line x1="{margin["left"]}" y1="{y}" x2="{w - margin["right"]}" '
            f'y2="{y}" stroke="#D8D2C4" stroke-width="0.5"/>'
        )
        parts.append(
            f'<text x="{margin["left"] - 8}" y="{y + 4}" text-anchor="end" '
            f'font-family="IBM Plex Mono, monospace" font-size="10" fill="#4C566A">{val:.0f}</text>'
        )

    for i, (label, value) in enumerate(zip(labels, values)):
        x = margin["left"] + gap / 2 + i * (bar_w + gap)
        bar_h = (value / max_v) * ch
        y = margin["top"] + ch - bar_h
        parts.append(
            f'<rect x="{x}" y="{y}" width="{bar_w}" height="{bar_h}" fill="{color}" rx="2"/>'
        )
        lx = x + bar_w / 2
        parts.append(
            f'<text x="{lx}" y="{margin["top"] + ch + 18}" text-anchor="middle" '
            f'font-family="Inter, sans-serif" font-size="11" fill="#4C566A">{label}</text>'
        )
        parts.append(
            f'<text x="{lx}" y="{y - 6}" text-anchor="middle" '
            f'font-family="IBM Plex Mono, monospace" font-size="10" fill="#172033">{value}</text>'
        )

    parts.append("</svg>")
    return "\n".join(parts)


def render_line(chart: dict) -> str:
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

    parts = [_svg_tag(w, h, chart.get("title", ""))]

    if chart.get("title"):
        parts.append(
            f'<text x="{margin["left"]}" y="24" font-family="Inter, sans-serif" '
            f'font-size="14" font-weight="600" fill="#172033">{chart["title"]}</text>'
        )

    for i in range(6):
        y = margin["top"] + ch - (ch * i / 5)
        val = min_v + range_v * i / 5
        parts.append(
            f'<line x1="{margin["left"]}" y1="{y}" x2="{w - margin["right"]}" '
            f'y2="{y}" stroke="#D8D2C4" stroke-width="0.5"/>'
        )
        parts.append(
            f'<text x="{margin["left"] - 8}" y="{y + 4}" text-anchor="end" '
            f'font-family="IBM Plex Mono, monospace" font-size="10" fill="#4C566A">{val:.0f}</text>'
        )

    step = cw / (len(values) - 1) if len(values) > 1 else cw
    points = []
    for i, v in enumerate(values):
        x = margin["left"] + i * step
        y = margin["top"] + ch - ((v - min_v) / range_v) * ch
        points.append((x, y))

    area_path = f"M {points[0][0]} {margin['top'] + ch}"
    for x, y in points:
        area_path += f" L {x} {y}"
    area_path += f" L {points[-1][0]} {margin['top'] + ch} Z"
    parts.append(f'<path d="{area_path}" fill="{CHART_COLORS["primary"]}" opacity="0.08"/>')

    line_path = f"M {points[0][0]} {points[0][1]}"
    for x, y in points[1:]:
        line_path += f" L {x} {y}"
    parts.append(
        f'<path d="{line_path}" fill="none" stroke="{color}" '
        f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
    )

    for i, (x, y) in enumerate(points):
        parts.append(f'<circle cx="{x}" cy="{y}" r="4" fill="{color}"/>')
        parts.append(f'<circle cx="{x}" cy="{y}" r="2" fill="#FAF8F4"/>')
        parts.append(
            f'<text x="{x}" y="{y - 10}" text-anchor="middle" '
            f'font-family="IBM Plex Mono, monospace" font-size="10" fill="#172033">{values[i]}</text>'
        )
        parts.append(
            f'<text x="{x}" y="{margin["top"] + ch + 18}" text-anchor="middle" '
            f'font-family="Inter, sans-serif" font-size="11" fill="#4C566A">{labels[i]}</text>'
        )

    parts.append("</svg>")
    return "\n".join(parts)


def render_donut(chart: dict) -> str:
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
    parts = [_svg_tag(w, h, chart.get("title", ""))]

    if chart.get("title"):
        parts.append(
            f'<text x="{cx}" y="24" text-anchor="middle" '
            f'font-family="Inter, sans-serif" font-size="14" font-weight="600" fill="#172033">{chart["title"]}</text>'
        )

    start_angle = -math.pi / 2
    for i, (label, value) in enumerate(zip(labels, values)):
        angle = (value / total) * 2 * math.pi
        end_angle = start_angle + angle
        color = colors[i % len(colors)]

        x1 = cx + radius * math.cos(start_angle)
        y1 = cy + radius * math.sin(start_angle)
        x2 = cx + radius * math.cos(end_angle)
        y2 = cy + radius * math.sin(end_angle)
        large_arc = 1 if angle > math.pi else 0

        ix2 = cx + inner_r * math.cos(end_angle)
        iy2 = cy + inner_r * math.sin(end_angle)
        ix1 = cx + inner_r * math.cos(start_angle)
        iy1 = cy + inner_r * math.sin(start_angle)

        path = (
            f"M {x1} {y1} A {radius} {radius} 0 {large_arc} 1 {x2} {y2} "
            f"L {ix2} {iy2} A {inner_r} {inner_r} 0 {large_arc} 0 {ix1} {iy1} Z"
        )
        parts.append(f'<path d="{path}" fill="{color}"/>')
        start_angle = end_angle

    parts.append(
        f'<text x="{cx}" y="{cy - 6}" text-anchor="middle" '
        f'font-family="IBM Plex Mono, monospace" font-size="12" fill="#4C566A">Total</text>'
    )
    parts.append(
        f'<text x="{cx}" y="{cy + 16}" text-anchor="middle" '
        f'font-family="Inter, sans-serif" font-size="20" font-weight="600" fill="#172033">{total}</text>'
    )

    legend_x = cx + radius + 30
    legend_y = cy - (len(labels) * 20) / 2
    for i, (label, value) in enumerate(zip(labels, values)):
        y = legend_y + i * 24
        color = colors[i % len(colors)]
        pct = f"{(value / total * 100):.1f}%"
        parts.append(f'<rect x="{legend_x}" y="{y - 6}" width="10" height="10" fill="{color}" rx="2"/>')
        parts.append(
            f'<text x="{legend_x + 18}" y="{y + 2}" '
            f'font-family="Inter, sans-serif" font-size="12" fill="#172033">{label}</text>'
        )
        parts.append(
            f'<text x="{legend_x + 18}" y="{y + 14}" '
            f'font-family="IBM Plex Mono, monospace" font-size="10" fill="#4C566A">{pct} ({value})</text>'
        )

    parts.append("</svg>")
    return "\n".join(parts)


def render(chart_data: dict) -> str:
    """Render a chart dict to SVG HTML string."""
    if not chart_data or not isinstance(chart_data, dict):
        return ""
    chart_type = chart_data.get("type", "bar")
    if chart_type == "bar":
        return render_bar(chart_data)
    elif chart_type == "line":
        return render_line(chart_data)
    elif chart_type == "donut":
        return render_donut(chart_data)
    return f"<!-- unsupported chart type: {chart_type} -->"
