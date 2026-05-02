#!/usr/bin/env python3
"""Batch render all sample JSON files to HTML."""

import json
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR / "data"
OUTPUT_DIR = SCRIPT_DIR / "output"
RENDER_PY = SCRIPT_DIR / "render.py"

SAMPLES = [
    ("sample-equity-report.json", "equity-report-zh.html"),
    ("sample-one-pager.json", "one-pager-zh.html"),
    ("sample-long-doc.json", "long-doc-zh.html"),
    ("sample-letter.json", "letter-zh.html"),
    ("sample-portfolio.json", "portfolio-zh.html"),
    ("sample-resume.json", "resume-zh.html"),
    ("sample-changelog.json", "changelog-zh.html"),
    ("sample-process-flow.json", "process-flow-zh.html"),
    ("sample-timeline.json", "timeline-zh.html"),
    ("sample-faq-page.json", "faq-page-zh.html"),
    ("sample-case-study.json", "case-study-zh.html"),
    ("sample-research-summary.json", "research-summary-zh.html"),
    ("sample-stats-report.json", "stats-report-zh.html"),
    ("sample-infographic.json", "infographic-zh.html"),
]

OUTPUT_DIR.mkdir(exist_ok=True)

success = 0
failed = 0

for data_file, output_file in SAMPLES:
    data_path = DATA_DIR / data_file
    output_path = OUTPUT_DIR / output_file

    if not data_path.exists():
        print(f"SKIP (not found): {data_file}")
        failed += 1
        continue

    result = subprocess.run(
        [
            sys.executable, str(RENDER_PY),
            "--data", str(data_path),
            "--output", str(output_path),
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode == 0:
        print(f"OK: {data_file} -> {output_file}")
        success += 1
    else:
        print(f"FAIL: {data_file}")
        print(result.stderr)
        failed += 1

print(f"\nDone: {success} succeeded, {failed} failed")
