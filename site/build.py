#!/usr/bin/env python3
"""Build the Momo Paper static product site.

Renders each JSON data file through the momo-paper engine, then injects
shared site navigation and footer into the rendered HTML output.
"""

import shutil
import sys
from pathlib import Path

# Make the engine importable without pip install
ENGINE_DIR = Path(__file__).resolve().parent.parent / "scripts" / "json-engine"
sys.path.insert(0, str(ENGINE_DIR))

from momo_paper.engine import render  # noqa: E402

SITE_DIR = Path(__file__).resolve().parent
DATA_DIR = SITE_DIR / "data"
OUTPUT_DIR = SITE_DIR / "output"

SITE_TEMPLATES = SITE_DIR / "templates"

PAGES = [
    # (data_file, url_path, page_id, template_file or None)
    ("index.json", "index.html", "index", "landing.html.j2"),
    ("guide.json", "guide/index.html", "guide", None),
    ("types.json", "types/index.html", "types", None),
    ("charts.json", "charts/index.html", "charts", None),
    ("faq.json", "faq/index.html", "faq", None),
]


def load_nav(page_id: str) -> str:
    raw = (SITE_DIR / "nav.html").read_text(encoding="utf-8")
    for _, _, p, _ in PAGES:
        raw = raw.replace(f"__active_{p}__", "active" if p == page_id else "")
    return raw


def load_footer() -> str:
    return (SITE_DIR / "footer.html").read_text(encoding="utf-8")


def build():
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir()

    for data_file, url_path, page_id, template_file in PAGES:
        data_path = DATA_DIR / data_file
        if not data_path.exists():
            print(f"  SKIP: {data_file} not found")
            continue

        kwargs = {}
        if template_file:
            kwargs["template_dir"] = str(SITE_TEMPLATES)
            kwargs["template_file"] = template_file
        html = render(str(data_path), **kwargs)

        html = html.replace("<body>", "<body>\n" + load_nav(page_id), 1)
        html = html.replace("</body>", load_footer() + "\n</body>", 1)

        out_path = OUTPUT_DIR / url_path
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(html, encoding="utf-8")
        print(f"  OK: {data_file} -> {url_path}")

    print(f"\nBuilt {len(PAGES)} pages to {OUTPUT_DIR.resolve()}")


if __name__ == "__main__":
    build()
