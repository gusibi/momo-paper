"""Command line interface for Momo Paper DSL."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from .errors import DslError, ValidationIssue
from .parser import parse_file
from .renderer import get_default_css_path, render_html
from .schema import describe_schema, list_schemas, validate_document


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


def _validation_issue_payload(issue: ValidationIssue) -> dict:
    return {
        "code": issue.code,
        "message": issue.message,
        "path": issue.path,
        "line": issue.line,
        "block": issue.block,
        "field": issue.field,
    }


def _print_issue(prefix: str, issue: ValidationIssue) -> None:
    parts: list[str] = []
    if issue.path:
        parts.append(issue.path)
    if issue.line is not None:
        parts.append(f"line {issue.line}")
    if issue.block:
        parts.append(f"block {issue.block}")
    if issue.field:
        parts.append(f"field {issue.field}")
    location = ": ".join(parts)
    detail = f"{location}: {issue.message}" if location else issue.message
    print(f"{prefix}: [{issue.code}] {detail}", file=sys.stderr)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="momo", description="Render Momo Paper Markdown DSL.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser("validate", help="Validate a Markdown DSL file.")
    validate_parser.add_argument("input")
    validate_parser.add_argument(
        "--json",
        action="store_true",
        dest="as_json",
        help="Emit machine-readable JSON: {ok, errors:[{message,line,block,path}]}",
    )
    validate_parser.add_argument(
        "--schema",
        default=None,
        help="Validate against a named formal schema instead of inferring it.",
    )

    render_parser = subparsers.add_parser("render", help="Render a Markdown DSL file to HTML or PDF.")
    render_parser.add_argument("input")
    render_parser.add_argument("-o", "--output", required=True)
    render_parser.add_argument(
        "--schema",
        default=None,
        help="Validate against a named formal schema before rendering.",
    )
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
    bench_parser.add_argument(
        "--baseline-html",
        default=None,
        help="Optional independently authored HTML baseline for an evidence-based token comparison.",
    )

    schema_parser = subparsers.add_parser("schema", help="List or describe formal document schemas.")
    schema_subparsers = schema_parser.add_subparsers(dest="schema_command", required=True)
    schema_list_parser = schema_subparsers.add_parser("list", help="List formal schemas.")
    schema_list_parser.add_argument("--json", action="store_true", dest="as_json")
    schema_describe_parser = schema_subparsers.add_parser(
        "describe", help="Describe one formal schema."
    )
    schema_describe_parser.add_argument("name")
    schema_describe_parser.add_argument("--json", action="store_true", dest="as_json")

    args = parser.parse_args(argv)

    if args.command == "validate":
        return _cmd_validate(args)
    if args.command == "render":
        return _cmd_render(args)
    if args.command == "bench":
        return _cmd_bench(args)
    if args.command == "schema":
        return _cmd_schema(args)
    return 1


def _cmd_validate(args) -> int:
    try:
        document = parse_file(args.input)
    except DslError as exc:
        if args.as_json:
            print(
                json.dumps(
                    {
                        "ok": False,
                        "schema": args.schema,
                        "mode": "strict" if args.schema else "free",
                        "candidates": [],
                        "errors": [_dsl_error_payload(exc)],
                        "warnings": [],
                    },
                    ensure_ascii=False,
                )
            )
        else:
            print(f"error: {exc}", file=sys.stderr)
        return 1

    report = validate_document(document, schema_name=args.schema)
    if args.as_json:
        print(
            json.dumps(
                {
                    "ok": report.ok,
                    "schema": report.schema,
                    "mode": report.mode,
                    "candidates": list(report.candidates),
                    "errors": [_validation_issue_payload(issue) for issue in report.errors],
                    "warnings": [_validation_issue_payload(issue) for issue in report.warnings],
                },
                ensure_ascii=False,
            )
        )
    else:
        for issue in report.errors:
            _print_issue("error", issue)
        for issue in report.warnings:
            _print_issue("warning", issue)
        if report.ok:
            schema_label = report.schema or "free mode"
            print(f"ok: {args.input} ({schema_label})")
    return 0 if report.ok else 1


def _cmd_schema(args) -> int:
    if args.schema_command == "list":
        summaries = list_schemas()
        if args.as_json:
            print(
                json.dumps(
                    [
                        {
                            "name": item.name,
                            "title": item.title,
                            "description": item.description,
                            "document_types": list(item.document_types),
                        }
                        for item in summaries
                    ],
                    ensure_ascii=False,
                )
            )
        else:
            for item in summaries:
                aliases = ", ".join(item.document_types)
                print(f"{item.name}\t{item.title}\t{aliases}")
        return 0

    try:
        schema = describe_schema(args.name)
    except KeyError:
        print(f"error: unknown schema: {args.name}", file=sys.stderr)
        return 1
    if args.as_json:
        print(json.dumps(schema, ensure_ascii=False))
    else:
        print(f"{schema['name']}: {schema.get('title', schema['name'])}")
        if schema.get("description"):
            print(schema["description"])
        print(f"document types: {', '.join(schema.get('document_types', []))}")
        required = schema.get("composition", {}).get("required_blocks", [])
        allowed = schema.get("composition", {}).get("allowed_blocks", [])
        print(f"required blocks: {', '.join(required) if required else '(none)'}")
        print(f"allowed blocks: {', '.join(allowed) if allowed else '(none)'}")
    return 0


def _cmd_render(args) -> int:
    try:
        document = parse_file(args.input)
    except DslError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    report = validate_document(document, schema_name=args.schema)
    for issue in report.errors:
        _print_issue("error", issue)
    for issue in report.warnings:
        _print_issue("warning", issue)
    if report.errors:
        return 1

    try:
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
    # The default comparison measures structural compression against this
    # renderer's markup. It is not an Agent-generated HTML baseline.
    saved_body = round((body_tokens - src_tokens) / body_tokens * 100, 1) if body_tokens else 0.0
    saved_total = round((html_tokens - src_tokens) / html_tokens * 100, 1) if html_tokens else 0.0
    baseline_tokens = None
    saved_vs_baseline = None
    if args.baseline_html:
        baseline_text = Path(args.baseline_html).read_text(encoding="utf-8")
        baseline_tokens, _ = _count_tokens(baseline_text)
        saved_vs_baseline = (
            round((baseline_tokens - src_tokens) / baseline_tokens * 100, 1)
            if baseline_tokens
            else 0.0
        )

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
                    "baseline_html_tokens": baseline_tokens,
                    "saved_vs_baseline_percent": saved_vs_baseline,
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
        print(f"Body reduction:     {saved_body}%  (DSL vs renderer-generated body markup)")
        print(f"  vs full HTML:     {saved_total}%  (DSL vs body + shared CSS)")
        if baseline_tokens is not None:
            print(f"Baseline HTML:      {baseline_tokens:>8,} tokens  (independently authored)")
            print(f"  vs baseline:      {saved_vs_baseline}%")
        print(f"HTML size:          {len(html):,} chars")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
