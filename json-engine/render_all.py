#!/usr/bin/env python3
"""Batch render all sample JSON files to HTML using the momo_paper engine."""

import sys
from pathlib import Path

from momo_paper.engine import render_to_file, get_template_dir

SCRIPT_DIR = Path(__file__).parent
EXAMPLES_DIR = SCRIPT_DIR / "momo_paper" / "examples"
OUTPUT_DIR = SCRIPT_DIR / "output"

SAMPLES = [
    ("sample-equity-report.json",    "equity-report-zh.html"),
    ("sample-one-pager.json",        "one-pager-zh.html"),
    ("sample-long-doc.json",         "long-doc-zh.html"),
    ("sample-letter.json",           "letter-zh.html"),
    ("sample-portfolio.json",        "portfolio-zh.html"),
    ("sample-resume.json",           "resume-zh.html"),
    ("sample-changelog.json",        "changelog-zh.html"),
    ("sample-process-flow.json",     "process-flow-zh.html"),
    ("sample-timeline.json",         "timeline-zh.html"),
    ("sample-faq-page.json",         "faq-page-zh.html"),
    ("sample-case-study.json",       "case-study-zh.html"),
    ("sample-research-summary.json", "research-summary-zh.html"),
    ("sample-stats-report.json",     "stats-report-zh.html"),
    ("sample-infographic.json",      "infographic-zh.html"),
]

OUTPUT_DIR.mkdir(exist_ok=True)
templates = get_template_dir()
success = 0
failed = 0

for data_file, output_file in SAMPLES:
    data_path = EXAMPLES_DIR / data_file

    if not data_path.exists():
        print(f"SKIP (not found): {data_file}")
        failed += 1
        continue

    try:
        out = render_to_file(str(data_path), str(OUTPUT_DIR / output_file), templates)
        print(f"OK: {data_file} -> {output_file}")
        success += 1
    except Exception as e:
        print(f"FAIL: {data_file} — {e}")
        failed += 1

print(f"\nDone: {success} succeeded, {failed} failed")
sys.exit(0 if failed == 0 else 1)
