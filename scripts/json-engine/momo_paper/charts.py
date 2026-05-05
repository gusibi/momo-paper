"""SVG chart rendering: bar, line, donut, candlestick, waterfall.
Refactored to use CSS variables for theme consistency.
"""

import math

# Using CSS variables for colors to support themes
CHART_COLORS = {
    "primary": "var(--accent)",
    "secondary": "var(--accent-dim)",
    "tertiary": "var(--accent-glow)",
    "accent": "var(--accent-2)",
    "positive": "var(--green)",
    "negative": "var(--red)",
    "neutral": "var(--text-muted)",
    "grid": "var(--border-light)",
    "text": "var(--text-primary)",
    "text_muted": "var(--text-secondary)",
    "heading": "var(--text-heading)",
    "bg": "var(--bg-primary)",
    "categorical": [
        "var(--accent)",
        "var(--accent-2)",
        "var(--green)",
        "var(--orange)",
        "var(--blue)",
        "var(--accent-dim)"
    ],
}


def _svg_tag(width: int, height: int, title: str = "") -> str:
    t = f' aria-label="{title}"' if title else ""
    # Inherit fonts from the document
    return (
        f'<svg width="100%" viewBox="0 0 {width} {height}" '
        f'xmlns="http://www.w3.org/2000/svg"{t} '
        f'style="font-family: var(--font-body);">'
    )


def render_bar(chart: dict) -> str:
    result = _validate_chart(chart)
    if result is None:
        return ""
    labels, values = result

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
            f'<text x="{margin["left"]}" y="24" font-family="var(--font-display)" '
            f'font-size="14" font-weight="600" fill="{CHART_COLORS["heading"]}">{chart["title"]}</text>'
        )

    for i in range(6):
        y = margin["top"] + ch - (ch * i / 5)
        val = max_v * i / 5
        parts.append(
            f'<line x1="{margin["left"]}" y1="{y}" x2="{w - margin["right"]}" '
            f'y2="{y}" stroke="{CHART_COLORS["grid"]}" stroke-width="0.5"/>'
        )
        parts.append(
            f'<text x="{margin["left"] - 8}" y="{y + 4}" text-anchor="end" '
            f'font-family="var(--font-mono)" font-size="10" fill="{CHART_COLORS["text_muted"]}">{val:.0f}</text>'
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
            f'font-family="var(--font-body)" font-size="11" fill="{CHART_COLORS["text_muted"]}">{label}</text>'
        )
        parts.append(
            f'<text x="{lx}" y="{y - 6}" text-anchor="middle" '
            f'font-family="var(--font-mono)" font-size="10" fill="{CHART_COLORS["text"]}">{value}</text>'
        )

    parts.append("</svg>")
    return "\n".join(parts)


def render_line(chart: dict) -> str:
    result = _validate_chart(chart)
    if result is None:
        return ""
    labels, values = result

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
            f'<text x="{margin["left"]}" y="24" font-family="var(--font-display)" '
            f'font-size="14" font-weight="600" fill="{CHART_COLORS["heading"]}">{chart["title"]}</text>'
        )

    for i in range(6):
        y = margin["top"] + ch - (ch * i / 5)
        val = min_v + range_v * i / 5
        parts.append(
            f'<line x1="{margin["left"]}" y1="{y}" x2="{w - margin["right"]}" '
            f'y2="{y}" stroke="{CHART_COLORS["grid"]}" stroke-width="0.5"/>'
        )
        parts.append(
            f'<text x="{margin["left"] - 8}" y="{y + 4}" text-anchor="end" '
            f'font-family="var(--font-mono)" font-size="10" fill="{CHART_COLORS["text_muted"]}">{val:.0f}</text>'
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
    parts.append(f'<path d="{area_path}" fill="{color}" opacity="0.08"/>')

    line_path = f"M {points[0][0]} {points[0][1]}"
    for x, y in points[1:]:
        line_path += f" L {x} {y}"
    parts.append(
        f'<path d="{line_path}" fill="none" stroke="{color}" '
        f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
    )

    for i, (x, y) in enumerate(points):
        parts.append(f'<circle cx="{x}" cy="{y}" r="4" fill="{color}"/>')
        parts.append(f'<circle cx="{x}" cy="{y}" r="2" fill="var(--bg-primary)"/>')
        parts.append(
            f'<text x="{x}" y="{y - 10}" text-anchor="middle" '
            f'font-family="var(--font-mono)" font-size="10" fill="{CHART_COLORS["text"]}">{values[i]}</text>'
        )
        parts.append(
            f'<text x="{x}" y="{margin["top"] + ch + 18}" text-anchor="middle" '
            f'font-family="var(--font-body)" font-size="11" fill="{CHART_COLORS["text_muted"]}">{labels[i]}</text>'
        )

    parts.append("</svg>")
    return "\n".join(parts)


def render_donut(chart: dict) -> str:
    result = _validate_chart(chart)
    if result is None:
        return ""
    labels, values = result

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
            f'font-family="var(--font-display)" font-size="14" font-weight="600" fill="{CHART_COLORS["heading"]}">{chart["title"]}</text>'
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
        f'font-family="var(--font-mono)" font-size="12" fill="{CHART_COLORS["text_muted"]}">Total</text>'
    )
    parts.append(
        f'<text x="{cx}" y="{cy + 16}" text-anchor="middle" '
        f'font-family="var(--font-body)" font-size="20" font-weight="600" fill="{CHART_COLORS["text"]}">{total}</text>'
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
            f'font-family="var(--font-body)" font-size="12" fill="{CHART_COLORS["text"]}">{label}</text>'
        )
        parts.append(
            f'<text x="{legend_x + 18}" y="{y + 14}" '
            f'font-family="var(--font-mono)" font-size="10" fill="{CHART_COLORS["text_muted"]}">{pct} ({value})</text>'
        )

    parts.append("</svg>")
    return "\n".join(parts)


def render_candlestick(chart: dict) -> str:
    """Render an OHLC candlestick chart from [{o, h, l, c}, ...] data."""
    data = chart.get("data", {})
    labels = data.get("labels", [])
    values = data.get("values", [])
    if not labels or not values:
        return ""
    if len(labels) != len(values):
        return ""

    w, h = 720, chart.get("height", 320)
    margin = {"top": 40, "right": 20, "bottom": 50, "left": 60}
    cw = w - margin["left"] - margin["right"]
    ch = h - margin["top"] - margin["bottom"]

    # Normalize short/long key names
    def _ohlc(v):
        return {
            "o": float(v.get("o", v.get("open", 0))),
            "h": float(v.get("h", v.get("high", 0))),
            "l": float(v.get("l", v.get("low", 0))),
            "c": float(v.get("c", v.get("close", 0))),
        }

    normalized = [_ohlc(v) for v in values]
    all_prices = [v["h"] for v in normalized] + [v["l"] for v in normalized]
    max_p = max(all_prices) * 1.05
    min_p = min(all_prices) * 0.95
    range_p = max_p - min_p if max_p != min_p else 1

    parts = [_svg_tag(w, h, chart.get("title", ""))]

    if chart.get("title"):
        parts.append(
            f'<text x="{margin["left"]}" y="24" font-family="var(--font-display)" '
            f'font-size="14" font-weight="600" fill="{CHART_COLORS["heading"]}">{chart["title"]}</text>'
        )

    # Gridlines
    for i in range(6):
        y = margin["top"] + ch - (ch * i / 5)
        val = min_p + range_p * i / 5
        parts.append(
            f'<line x1="{margin["left"]}" y1="{y}" x2="{w - margin["right"]}" '
            f'y2="{y}" stroke="{CHART_COLORS["grid"]}" stroke-width="0.5"/>'
        )
        parts.append(
            f'<text x="{margin["left"] - 8}" y="{y + 4}" text-anchor="end" '
            f'font-family="var(--font-mono)" font-size="10" fill="{CHART_COLORS["text_muted"]}">{val:.1f}</text>'
        )

    candle_w = max((cw / len(values)) * 0.5, 6)
    step = cw / len(values)

    for i, (label, v) in enumerate(zip(labels, normalized)):
        cx = margin["left"] + step * i + step / 2
        o, hi, lo, c = v["o"], v["h"], v["l"], v["c"]

        # Wick (high-low line)
        wy_top = margin["top"] + ch - ((hi - min_p) / range_p) * ch
        wy_bot = margin["top"] + ch - ((lo - min_p) / range_p) * ch
        parts.append(
            f'<line x1="{cx}" y1="{wy_top}" x2="{cx}" y2="{wy_bot}" '
            f'stroke="{CHART_COLORS["text"]}" stroke-width="1"/>'
        )

        # Body (open-close rect)
        body_top = margin["top"] + ch - ((max(o, c) - min_p) / range_p) * ch
        body_bot = margin["top"] + ch - ((min(o, c) - min_p) / range_p) * ch
        body_h = max(abs(body_bot - body_top), 0)
        color = CHART_COLORS["positive"] if c >= o else CHART_COLORS["negative"]
        parts.append(
            f'<rect x="{cx - candle_w / 2}" y="{body_top}" width="{candle_w}" '
            f'height="{body_h}" fill="{color}" rx="1"/>'
        )

        # X-axis label
        parts.append(
            f'<text x="{cx}" y="{margin["top"] + ch + 18}" text-anchor="middle" '
            f'font-family="var(--font-body)" font-size="11" fill="{CHART_COLORS["text_muted"]}">{label}</text>'
        )

    parts.append("</svg>")
    return "\n".join(parts)


def render_waterfall(chart: dict) -> str:
    """Render a waterfall/bridge chart from labels and values."""
    data = chart.get("data", {})
    labels = data.get("labels", [])
    values = data.get("values", [])
    if not labels or not values:
        return ""
    if len(labels) != len(values):
        return ""

    w, h = 720, chart.get("height", 300)
    margin = {"top": 40, "right": 20, "bottom": 50, "left": 60}
    cw = w - margin["left"] - margin["right"]
    ch = h - margin["top"] - margin["bottom"]

    running = 0
    bases = []
    for v in values:
        bases.append(running if v >= 0 else running + v)
        running += v

    all_y = [b for b in bases] + [b + v for b, v in zip(bases, values)]
    max_y = max(all_y) * 1.1 if all_y else 1
    min_y = min(0, min(all_y) * 0.9) if all_y else 0
    range_y = max_y - min_y if max_y != min_y else 1

    parts = [_svg_tag(w, h, chart.get("title", ""))]

    if chart.get("title"):
        parts.append(
            f'<text x="{margin["left"]}" y="24" font-family="var(--font-display)" '
            f'font-size="14" font-weight="600" fill="{CHART_COLORS["heading"]}">{chart["title"]}</text>'
        )

    # Baseline
    bl_y = margin["top"] + ch - ((0 - min_y) / range_y) * ch
    parts.append(
        f'<line x1="{margin["left"]}" y1="{bl_y}" x2="{w - margin["right"]}" '
        f'y2="{bl_y}" stroke="{CHART_COLORS["neutral"]}" stroke-width="1"/>'
    )

    # Gridlines
    for i in range(6):
        y = margin["top"] + ch - (ch * i / 5)
        val = min_y + range_y * i / 5
        parts.append(
            f'<line x1="{margin["left"]}" y1="{y}" x2="{w - margin["right"]}" '
            f'y2="{y}" stroke="{CHART_COLORS["grid"]}" stroke-width="0.5"/>'
        )
        parts.append(
            f'<text x="{margin["left"] - 8}" y="{y + 4}" text-anchor="end" '
            f'font-family="var(--font-mono)" font-size="10" fill="{CHART_COLORS["text_muted"]}">{val:.0f}</text>'
        )

    bar_w = (cw / len(values)) * 0.55
    gap = (cw / len(values)) * 0.45

    for i, (label, v) in enumerate(zip(labels, values)):
        x = margin["left"] + gap / 2 + i * (bar_w + gap)
        base = bases[i]
        b_top = margin["top"] + ch - ((base + v - min_y) / range_y) * ch
        b_bot = margin["top"] + ch - ((base - min_y) / range_y) * ch
        bar_h = abs(b_bot - b_top)

        is_total = label.lower() in ("total", "总计", "合计")
        is_subtotal = label.lower() in ("subtotal", "小计")
        if is_total or is_subtotal:
            color = CHART_COLORS["accent"]
        elif v >= 0:
            color = CHART_COLORS["primary"]
        else:
            color = CHART_COLORS["negative"]

        rect_y = b_top if v >= 0 else b_bot
        parts.append(
            f'<rect x="{x}" y="{rect_y}" width="{bar_w}" height="{max(bar_h, 1)}" '
            f'fill="{color}" rx="2"/>'
        )

        # Connector line from previous bar
        if i > 0:
            prev_x = margin["left"] + gap / 2 + (i - 1) * (bar_w + gap) + bar_w
            prev_top = margin["top"] + ch - ((bases[i - 1] + values[i - 1] - min_y) / range_y) * ch
            parts.append(
                f'<line x1="{prev_x}" y1="{prev_top}" x2="{x}" y2="{rect_y}" '
                f'stroke="{CHART_COLORS["grid"]}" stroke-width="1" stroke-dasharray="4,4"/>'
            )

        # Value label
        lx = x + bar_w / 2
        ly = (rect_y - 8) if v >= 0 else (rect_y + bar_h + 16)
        parts.append(
            f'<text x="{lx}" y="{ly}" text-anchor="middle" '
            f'font-family="var(--font-mono)" font-size="10" fill="{CHART_COLORS["text"]}">{v:+.0f}</text>'
        )

        # X-axis label
        parts.append(
            f'<text x="{lx}" y="{margin["top"] + ch + 18}" text-anchor="middle" '
            f'font-family="var(--font-body)" font-size="11" fill="{CHART_COLORS["text_muted"]}">{label}</text>'
        )

    parts.append("</svg>")
    return "\n".join(parts)


def _validate_chart(chart: dict) -> tuple[list, list] | None:
    """Validate chart data and return (labels, values) or None if invalid."""
    data = chart.get("data", {})
    labels = data.get("labels", [])
    values = data.get("values", [])
    if not labels or not values:
        return None
    if len(labels) != len(values):
        return None
    return labels, values


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
    elif chart_type == "candlestick":
        return render_candlestick(chart_data)
    elif chart_type == "waterfall":
        return render_waterfall(chart_data)
    return f"<!-- unsupported chart type: {chart_type} -->"
