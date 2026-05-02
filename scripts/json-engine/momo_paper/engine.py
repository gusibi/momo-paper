"""Core rendering engine: load JSON, resolve template, render HTML."""

import json
import sys
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from .charts import render as render_chart

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
    "slides": "slides.html.j2",
}


def get_template_dir() -> Path:
    """Get the templates directory packaged with momo_paper."""
    return Path(__file__).parent / "templates"


def list_types() -> list[str]:
    """List all supported document types."""
    return sorted(DEFAULT_TEMPLATE_MAP.keys())


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


def load_json(data_source: str | dict) -> dict:
    """Load JSON from file path or accept a dict directly."""
    if isinstance(data_source, dict):
        data = data_source
    elif data_source == "-":
        data = json.load(sys.stdin)
    else:
        path = Path(data_source)
        if not path.exists():
            raise FileNotFoundError(f"Data file not found: {path}")
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

    if not isinstance(data, dict):
        raise ValueError("JSON root must be an object")

    required = ["document_type", "locale", "meta"]
    missing = [k for k in required if k not in data]
    if missing:
        raise ValueError(f"Missing required fields: {missing}")

    doc_type = data.get("document_type", "")
    if doc_type == "slides":
        if "slides" not in data:
            raise ValueError("Missing required field: slides")
    else:
        if "sections" not in data:
            raise ValueError("Missing required field: sections")
    return data


def render(data_source: str | dict, template_dir: Path | None = None, template_file: str | None = None) -> str:
    """Render JSON data to HTML string.

    Args:
        data_source: Path to JSON file, '-' for stdin, or a dict
        template_dir: Templates directory (defaults to package templates)
        template_file: Explicit template name (auto-resolved by document_type if None)

    Returns:
        Rendered HTML string
    """
    data = load_json(data_source)

    if template_dir is None:
        template_dir = get_template_dir()

    template_name = resolve_template(data["document_type"], template_dir, template_file)

    env = Environment(
        loader=FileSystemLoader(str(template_dir)),
        autoescape=select_autoescape(["html", "xml"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.filters["render_chart"] = render_chart

    template = env.get_template(template_name)
    return template.render(**data)


def render_to_file(
    data_source: str | dict,
    output_path: str,
    template_dir: Path | None = None,
    template_file: str | None = None,
) -> Path:
    """Render JSON data to an HTML file.

    Returns:
        Path to the output file
    """
    html = render(data_source, template_dir, template_file)
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    return out
