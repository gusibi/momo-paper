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
import sys
from pathlib import Path

try:
    from jinja2 import Environment, FileSystemLoader, select_autoescape
except ImportError:
    print("Error: jinja2 is required. Install with: pip install jinja2")
    sys.exit(1)

from momo_paper.charts import render as render_chart
from momo_paper.engine import DEFAULT_TEMPLATE_MAP, resolve_template, load_json, get_template_dir


def render(data: dict, template_path: str, template_dir: Path) -> str:
    env = Environment(
        loader=FileSystemLoader(str(template_dir)),
        autoescape=select_autoescape(["html", "xml"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.filters["render_chart"] = render_chart
    template = env.get_template(template_path)
    return template.render(**data)


def main():
    parser = argparse.ArgumentParser(description="Momo Paper JSON Rendering Engine")
    parser.add_argument("--data", "-d", required=True, help="Path to JSON data file")
    parser.add_argument("--template", "-t", help="Explicit template file (overrides document_type mapping)")
    parser.add_argument("--output", "-o", required=True, help="Output HTML file path")
    parser.add_argument("--template-dir", default=None, help="Directory containing Jinja2 templates (defaults to package templates)")
    args = parser.parse_args()

    data_source = args.data
    output_path = Path(args.output)
    template_dir = Path(args.template_dir) if args.template_dir else get_template_dir()

    if data_source != "-" and not Path(data_source).exists():
        print(f"Error: Data file not found: {data_source}")
        sys.exit(1)

    try:
        data = load_json(data_source)
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
