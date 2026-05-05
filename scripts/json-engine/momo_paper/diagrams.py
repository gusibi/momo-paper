"""SVG diagram primitives rendering: flowchart, architecture, swimlane, timeline, tree, etc.
Supports structured JSON to SVG conversion using design tokens.
"""

from typing import Any, List, Dict

DIAGRAM_COLORS = {
    "primary_bg": "var(--accent-glow)",
    "primary_stroke": "var(--accent)",
    "secondary_bg": "var(--bg-secondary)",
    "secondary_stroke": "var(--border)",
    "tertiary_bg": "var(--bg-tertiary)",
    "accent_bg": "rgba(212, 120, 90, 0.12)",
    "accent_stroke": "var(--accent-2)",
    "paper_bg": "var(--bg-elevated)",
    "text": "var(--text-primary)",
    "text_muted": "var(--text-secondary)",
    "font_mono": "var(--font-mono)",
    "font_body": "var(--font-body)",
    "success": "var(--green)",
    "danger": "var(--red)",
    "warning": "var(--orange)",
}

def _svg_tag(width: int, height: int, title: str = "", viewbox: str = None) -> str:
    t = f' aria-label="{title}"' if title else ""
    vb = viewbox if viewbox else f"0 0 {width} {height}"
    return (
        f'<svg width="100%" viewBox="{vb}" '
        f'xmlns="http://www.w3.org/2000/svg"{t} '
        f'style="font-family: var(--font-body);">'
    )

def render_element(el: dict) -> str:
    """Render a generic SVG element from dict."""
    etype = el.get("type", "rect")
    style = el.get("style", "primary")
    
    bg = DIAGRAM_COLORS.get(f"{style}_bg", DIAGRAM_COLORS["primary_bg"])
    stroke = DIAGRAM_COLORS.get(f"{style}_stroke", DIAGRAM_COLORS["primary_stroke"])
    
    # Handle semantic status colors
    if style in ["success", "danger", "warning"]:
        stroke = f"var(--{style})"
        bg = f"var(--{style}-glow, rgba(120, 120, 120, 0.1))"

    parts = []
    opacity = el.get("opacity", 1.0)
    sw = el.get("stroke_width", 1.5)
    
    if etype == "rect":
        x, y, w, h = el.get("x", 0), el.get("y", 0), el.get("w", 120), el.get("h", 60)
        rx = el.get("rx", 8)
        parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{bg}" fill-opacity="{opacity}" stroke="{stroke}" stroke-width="{sw}"/>')
        if el.get("label"):
            parts.append(f'<text x="{x + w/2}" y="{y + h/2 + 5}" text-anchor="middle" font-size="{el.get("font_size", 13)}" font-weight="500" fill="{DIAGRAM_COLORS["text"]}">{el["label"]}</text>')

    elif etype == "capsule":
        x, y, w, h = el.get("x", 0), el.get("y", 0), el.get("w", 100), el.get("h", 40)
        parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2}" fill="{bg}" fill-opacity="{opacity}" stroke="{stroke}" stroke-width="{sw}"/>')
        if el.get("label"):
            parts.append(f'<text x="{x + w/2}" y="{y + h/2 + 5}" text-anchor="middle" font-size="12" font-weight="600" fill="{DIAGRAM_COLORS["text"]}">{el["label"]}</text>')

    elif etype == "diamond":
        x, y, w, h = el.get("x", 0), el.get("y", 0), el.get("w", 100), el.get("h", 80)
        pts = f"{x+w/2},{y} {x+w},{y+h/2} {x+w/2},{y+h} {x},{y+h/2}"
        parts.append(f'<polygon points="{pts}" fill="{bg}" fill-opacity="{opacity}" stroke="{stroke}" stroke-width="{sw}"/>')
        if el.get("label"):
            parts.append(f'<text x="{x + w/2}" y="{y + h/2 + 5}" text-anchor="middle" font-size="12" font-weight="600" fill="{DIAGRAM_COLORS["text"]}">{el["label"]}</text>')

    elif etype == "circle":
        cx, cy, r = el.get("cx", 0), el.get("cy", 0), el.get("r", 30)
        parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{bg}" fill-opacity="{opacity}" stroke="{stroke}" stroke-width="{sw}"/>')
        if el.get("label"):
            parts.append(f'<text x="{cx}" y="{cy + 5}" text-anchor="middle" font-size="13" font-weight="500" fill="{DIAGRAM_COLORS["text"]}">{el["label"]}</text>')

    elif etype == "line":
        x1, y1, x2, y2 = el.get("x1", 0), el.get("y1", 0), el.get("x2", 0), el.get("y2", 0)
        marker = ' marker-end="url(#arrowhead)"' if el.get("arrow") else ""
        dash = f' stroke-dasharray="{el["dash"]}"' if el.get("dash") else ""
        parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}"{marker}{dash}/>')
        if el.get("label"):
            lx, ly = (x1 + x2) / 2, (y1 + y2) / 2
            parts.append(f'<text x="{lx}" y="{ly - 8}" text-anchor="middle" font-size="11" fill="{DIAGRAM_COLORS["text_muted"]}" font-family="{DIAGRAM_COLORS["font_mono"]}">{el["label"]}</text>')

    elif etype == "path":
        parts.append(f'<path d="{el.get("d", "")}" fill="{el.get("fill", "none")}" fill-opacity="{opacity}" stroke="{stroke}" stroke-width="{sw}"/>')

    elif etype == "polyline":
        parts.append(f'<polyline points="{el.get("points", "")}" fill="none" stroke="{stroke}" stroke-width="{el.get("stroke_width", 2)}"/>')

    elif etype == "text":
        tx, ty = el.get("x", 0), el.get("y", 0)
        anchor = el.get("anchor", "start")
        parts.append(f'<text x="{tx}" y="{ty}" text-anchor="{anchor}" font-size="{el.get("font_size", 12)}" font-weight="{el.get("font_weight", "normal")}" fill="{DIAGRAM_COLORS.get(el.get("color", "text"), DIAGRAM_COLORS["text"])}" font-family="{DIAGRAM_COLORS.get("font_" + el.get("font", "body"))}">{el.get("label", "")}</text>')

    return "\n".join(parts)

def render(diagram_data: dict) -> str:
    """Render a full diagram from structured JSON."""
    if not diagram_data or not isinstance(diagram_data, dict):
        return ""
        
    w = diagram_data.get("width", 800)
    h = diagram_data.get("height", 400)
    vb = diagram_data.get("viewBox")
    title = diagram_data.get("title", "")
    elements = diagram_data.get("elements", [])
    
    parts = [_svg_tag(w, h, title, vb)]
    parts.append("""<defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orientation="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="var(--accent)" />
    </marker>
  </defs>""")
    
    for el in elements:
        parts.append(render_element(el))
        
    parts.append("</svg>")
    return "\n".join(parts)
