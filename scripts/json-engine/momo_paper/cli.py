"""CLI entry point for Momo Paper rendering engine."""

import json
import sys
from pathlib import Path

import click

from .charts import render as render_chart
from .engine import DEFAULT_TEMPLATE_MAP, render_to_file

DOC_TYPES_HELP = """Supported document types:

  equity_report    个股研报 / Equity Report
  one_pager        方案 / One-Pager
  long_doc         白皮书 / Long Document
  letter           信件 / Letter
  portfolio        作品集 / Portfolio
  resume           简历 / Resume
  changelog        更新日志 / Changelog
  process_flow     流程 / Process Flow
  timeline         时间线 / Timeline
  faq_page         常见问题 / FAQ Page
  case_study       案例拆解 / Case Study
  research_summary 研究摘要 / Research Summary
  stats_report     数据报告 / Stats Report
  infographic      信息图 / Infographic
  slides           幻灯片 / Slides
  landing          落地页 / Landing Page"""


@click.group()
@click.version_option(version="4.0.0", prog_name="momo-paper")
def cli():
    """Momo Paper — JSON-driven document rendering engine.

    Render structured JSON data into print-safe, design-token-aware HTML documents.
    """
    pass


@cli.command()
@click.option("--data", "-d", "data_source", required=True,
              help="Path to JSON data file (use '-' for stdin)")
@click.option("--output", "-o", required=True,
              help="Output HTML file path")
@click.option("--template", "-t", default=None,
              help="Explicit template file (auto-resolved from document_type if omitted)")
@click.option("--template-dir", default=None,
              help="Custom template directory (uses built-in templates if omitted)")
def render(data_source, output, template, template_dir):
    """Render a JSON data file to HTML.

    \b
    Examples:
      momo render -d data/report.json -o output/report.html
      momo render -d data/report.json -t my-template.html.j2 -o out.html
      cat report.json | momo render -d - -o out.html
    """
    td = Path(template_dir) if template_dir else None
    try:
        out = render_to_file(data_source, output, td, template)
        click.echo(f"✓ Rendered: {out}")
        click.echo(f"  output: {out.resolve()}")
    except FileNotFoundError as e:
        click.echo(f"✗ {e}", err=True)
        sys.exit(1)
    except ValueError as e:
        click.echo(f"✗ {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"✗ Rendering failed: {e}", err=True)
        sys.exit(1)


@cli.command()
def list():
    """List all supported document types."""
    click.echo(DOC_TYPES_HELP)
    click.echo("\nCharts: bar, line, donut, candlestick, waterfall")
    click.echo("Locales: zh-CN, en")


@cli.command()
@click.option("--type", "-t", "doc_type", required=True,
              help="Document type to generate template for")
@click.option("--locale", "-l", default="zh-CN",
              type=click.Choice(["zh-CN", "en"]),
              help="Locale for the template")
@click.option("--output", "-o", default=None,
              help="Output file (prints to stdout if omitted)")
def init(doc_type, locale, output):
    """Generate an empty JSON template for a document type.

    \b
    Examples:
      momo init -t equity_report -o my-report.json
      momo init -t one_pager -l en
    """
    if doc_type not in DEFAULT_TEMPLATE_MAP:
        click.echo(f"✗ Unknown document type: {doc_type}", err=True)
        click.echo("  Use 'momo list' to see supported types", err=True)
        sys.exit(1)

    if doc_type == "slides":
        template = {
            "document_type": doc_type,
            "locale": locale,
            "meta": {
                "title": "[Title]",
                "subtitle": "[Subtitle]",
                "eyebrow": f"Momo Paper / {doc_type} / {locale}",
                "date": "",
                "author": "",
            },
            "slides": [
                {"title": "[封面标题]", "point": "[一句话主结论]", "layout": "cover"},
                {"title": "[目录]", "point": "[章节结构]"},
                {"title": "[问题]", "point": "[核心观点]", "bullets": ["[要点 1]", "[要点 2]"]},
                {"title": "[结论]", "point": "[下一步行动]", "layout": "closing"},
            ],
        }
    elif doc_type == "landing":
        template = {
            "document_type": doc_type,
            "locale": locale,
            "meta": {
                "title": "[Site Title]",
            },
            "sections": {
                "hero": {
                    "badge": "[Badge]",
                    "headline": "[Headline]",
                    "description": "[Description]",
                    "cta_buttons": [
                        {"label": "[Primary CTA]", "url": "#", "style": "btn-primary"},
                        {"label": "[Secondary CTA]", "url": "#", "style": "btn-outline"}
                    ],
                    "pipeline": [
                        {"label": "[Step 1]", "desc": "[Description]"},
                        {"label": "[Step 2]", "desc": "[Description]"},
                        {"label": "[Step 3]", "desc": "[Description]"}
                    ]
                },
                "features": {
                    "label": "[Section Label]",
                    "heading": "[Features Heading]",
                    "description": "[Description]",
                    "cards": [
                        {"icon": "A", "icon_class": "docs", "title": "[Feature]", "description": "[Description]"}
                    ]
                },
                "bottom_cta": {
                    "heading": "[CTA Heading]",
                    "description": "[Description]",
                    "button_label": "[Button Label]",
                    "button_url": "#"
                }
            }
        }
    else:
        template = {
            "document_type": doc_type,
            "locale": locale,
            "meta": {
                "title": "[Title]",
                "subtitle": "[Subtitle]",
                "eyebrow": f"Momo Paper / {doc_type} / {locale}",
                "date": "",
                "author": "",
            },
            "sections": {},
        }

    result = json.dumps(template, ensure_ascii=False, indent=2)

    if output:
        Path(output).write_text(result + "\n", encoding="utf-8")
        click.echo(f"✓ Template written: {output}")
    else:
        click.echo(result)


@cli.command()
@click.option("--data", "-d", "data_source", required=True,
              help="Path to JSON data file (use '-' for stdin)")
@click.option("--output", "-o", default=None,
              help="Output SVG file (prints to stdout if omitted)")
@click.option("--key", "-k", default=None,
              help="Dot-separated key path to chart in JSON (e.g. 'sections.trends.chart')")
def chart(data_source, output, key):
    """Render only the chart from a JSON data file as standalone SVG.

    \b
    Examples:
      momo chart -d report.json -k sections.trends.chart -o chart.svg
      momo chart -d chart-data.json
    """
    if data_source == "-":
        data = json.load(sys.stdin)
    else:
        data = json.loads(Path(data_source).read_text(encoding="utf-8"))

    if key:
        for part in key.split("."):
            if isinstance(data, dict) and part in data:
                data = data[part]
            else:
                click.echo(f"✗ Key '{key}' not found in data", err=True)
                sys.exit(1)

    chart_data = data if isinstance(data, dict) else data.get("chart", {})
    svg = render_chart(chart_data)

    if not svg:
        click.echo("✗ No valid chart data found", err=True)
        sys.exit(1)

    if output:
        Path(output).write_text(svg, encoding="utf-8")
        click.echo(f"✓ Chart written: {output}")
    else:
        click.echo(svg)


def main():
    cli()


if __name__ == "__main__":
    main()
