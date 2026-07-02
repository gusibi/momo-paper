"""Command line interface for Momo Paper DSL."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from .errors import DslError
from .parser import parse_file
from .renderer import get_default_css_path, render_html


def _count_tokens(text: str) -> tuple[int, str]:
    """Return (token_count, method_label).

    Prefers tiktoken cl100k_base when installed; falls back to a chars/4
    estimate so the command stays zero-dependency.
    """
    try:
        import tiktoken

        enc = tiktoken.get_encoding("cl100k_base")
        return len(enc.encode(text)), "tiktoken:cl100k_base"
    except Exception:
        return max(1, len(text) // 4), "chars/4-estimate"


def _dsl_error_payload(exc: DslError) -> dict:
    return {
        "message": exc.message,
        "path": exc.path,
        "line": exc.line,
        "block": exc.block,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="momo2", description="Render Momo Paper Markdown DSL.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser("validate", help="Validate a Markdown DSL file.")
    validate_parser.add_argument("input")
    validate_parser.add_argument(
        "--json",
        action="store_true",
        dest="as_json",
        help="Emit machine-readable JSON: {ok, errors:[{message,line,block,path}]}.",
    )

    render_parser = subparsers.add_parser("render", help="Render a Markdown DSL file to HTML or PDF.")
    render_parser.add_argument("input")
    render_parser.add_argument("-o", "--output", required=True)
    render_parser.add_argument(
        "--css",
        default=None,
        help="CSS file to inline into the HTML. Defaults to the bundled momo-paper.css.",
    )
    render_parser.add_argument(
        "--format",
        choices=("html", "pdf"),
        default="html",
        help="Output format. pdf requires the optional playwright dependency.",
    )

    bench_parser = subparsers.add_parser(
        "bench", help="Compare DSL token cost vs the rendered HTML output."
    )
    bench_parser.add_argument("input")
    bench_parser.add_argument(
        "--json",
        action="store_true",
        dest="as_json",
        help="Emit machine-readable JSON.",
    )
    bench_parser.add_argument(
        "--css",
        default=None,
        help="CSS file used when rendering. Defaults to the bundled momo-paper.css.",
    )

    args = parser.parse_args(argv)

    if args.command == "validate":
        return _cmd_validate(args)
    if args.command == "render":
        return _cmd_render(args)
    if args.command == "bench":
        return _cmd_bench(args)
    return 1


def _cmd_validate(args) -> int:
    try:
        parse_file(args.input)
    except DslError as exc:
        if args.as_json:
            print(json.dumps({"ok": False, "errors": [_dsl_error_payload(exc)]}, ensure_ascii=False))
        else:
            print(f"error: {exc}", file=sys.stderr)
        return 1
    if args.as_json:
        print(json.dumps({"ok": True, "errors": []}, ensure_ascii=False))
    else:
        print(f"ok: {args.input}")
    return 0


def _cmd_render(args) -> int:
    try:
        document = parse_file(args.input)
        css_path = Path(args.css) if args.css else get_default_css_path()
        css = css_path.read_text(encoding="utf-8")
        html = render_html(document, css=css)
    except DslError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    if args.format == "pdf":
        pdf_bytes = _render_pdf(html)
        output.write_bytes(pdf_bytes)
        print(f"rendered: {output}")
        return 0

    output.write_text(html, encoding="utf-8")
    print(f"rendered: {output}")
    return 0


def _render_pdf(html: str) -> bytes:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print(
            "error: PDF output requires the optional 'playwright' dependency.",
            file=sys.stderr,
        )
        print(
            "       Install it with:  pip install playwright && playwright install chromium",
            file=sys.stderr,
        )
        raise SystemExit(1)
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page()
        page.set_content(html, wait_until="load")
        pdf = page.pdf(print_background=True)
        browser.close()
        return pdf


def _cmd_bench(args) -> int:
    try:
        document = parse_file(args.input)
        css_path = Path(args.css) if args.css else get_default_css_path()
        css = css_path.read_text(encoding="utf-8")
        html = render_html(document, css=css)
    except DslError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    src_text = Path(args.input).read_text(encoding="utf-8")
    src_tokens, method = _count_tokens(src_text)
    html_tokens, _ = _count_tokens(html)
    css_tokens, _ = _count_tokens(css)
    body_tokens = max(0, html_tokens - css_tokens)
    # Headline saving is body-based: the theme CSS is shared/reused across
    # documents, so the per-document saving is DSL vs the HTML body the Agent
    # would otherwise hand-write. saved_vs_total includes the shared CSS.
    saved_body = round((body_tokens - src_tokens) / body_tokens * 100, 1) if body_tokens else 0.0
    saved_total = round((html_tokens - src_tokens) / html_tokens * 100, 1) if html_tokens else 0.0

    if args.as_json:
        print(
            json.dumps(
                {
                    "tokenizer": method,
                    "dsl_tokens": src_tokens,
                    "html_tokens": html_tokens,
                    "html_css_tokens": css_tokens,
                    "html_body_tokens": body_tokens,
                    "saved_percent": saved_body,
                    "saved_vs_total_percent": saved_total,
                    "html_chars": len(html),
                },
                ensure_ascii=False,
            )
        )
    else:
        print(f"tokenizer:          {method}")
        print(f"DSL source:         {src_tokens:>8,} tokens")
        print(f"Rendered HTML:      {html_tokens:>8,} tokens  (incl. inlined theme CSS)")
        print(f"  - theme CSS:      {css_tokens:>8,} tokens  (fixed, shared across docs)")
        print(f"  - body markup:    {body_tokens:>8,} tokens")
        print(f"Estimated saved:    {saved_body}%  (DSL vs HTML body — per-document saving)")
        print(f"  vs full HTML:     {saved_total}%  (DSL vs body + shared CSS)")
        print(f"HTML size:          {len(html):,} chars")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
