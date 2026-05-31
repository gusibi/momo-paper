"""Command line interface for Momo Paper DSL."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from .errors import DslError
from .parser import parse_file
from .renderer import get_default_css_path, render_html


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="momo2", description="Render Momo Paper Markdown DSL.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser("validate", help="Validate a Markdown DSL file.")
    validate_parser.add_argument("input")

    render_parser = subparsers.add_parser("render", help="Render a Markdown DSL file to HTML.")
    render_parser.add_argument("input")
    render_parser.add_argument("-o", "--output", required=True)
    render_parser.add_argument(
        "--css",
        default=None,
        help="CSS file to inline into the HTML. Defaults to the bundled momo-paper.css.",
    )

    args = parser.parse_args(argv)

    try:
        document = parse_file(args.input)
        if args.command == "validate":
            print(f"ok: {args.input}")
            return 0
        css_path = Path(args.css) if args.css else get_default_css_path()
        css = css_path.read_text(encoding="utf-8")
        html = render_html(document, css=css)
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(html, encoding="utf-8")
        print(f"rendered: {output}")
        return 0
    except DslError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
