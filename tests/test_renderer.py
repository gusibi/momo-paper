import unittest
from pathlib import Path

from momo_dsl.parser import parse_file, parse_text
from momo_dsl.renderer import get_default_css_path, render_html


class RendererTests(unittest.TestCase):
    def test_renders_generic_block_sections(self):
        doc = parse_text("""---
document_type: landing
locale: en
title: Render Test
description: Demo
---

## Intro

:::custom-block
title: Custom
items:
  - label: A
    value: 1
:::
""")
        html = render_html(doc)
        self.assertIn("<!DOCTYPE html>", html)
        self.assertIn("<style>", html)
        self.assertIn(".page { width: 100%; min-height: 100vh; }", html)
        self.assertIn('data-block="custom-block"', html)
        self.assertIn("Render Test", html)
        self.assertIn("<h2>Intro</h2>", html)
        self.assertIn("Custom", html)

    def test_renderer_uses_full_width_sections_not_page_card(self):
        doc = parse_text("""---
document_type: landing
locale: en
title: Layout Test
---

:::hero
title: Full width
:::
""")
        html = render_html(doc)
        self.assertIn('<div class="block-inner">', html)
        self.assertNotIn("width: min(1120px", html)
        self.assertNotIn("border-left:", html)

        css = get_default_css_path().read_text(encoding="utf-8")
        self.assertIn(".page { width: 100%; min-height: 100vh; }", css)
        self.assertIn(".block-inner", css)
        self.assertIn("font-size: clamp(34px, 5vw, 56px);", css)
        self.assertIn("font-size: clamp(36px, 6vw, 64px);", css)
        self.assertNotIn("border-left:", css)

    def test_can_inline_custom_css(self):
        doc = parse_text("""---
document_type: landing
locale: en
title: Custom CSS
---
""")
        html = render_html(doc, css=".page { color: red; }")
        self.assertIn("<style>\n.page { color: red; }\n  </style>", html)

    def test_renders_reference_example_tags(self):
        root = Path(__file__).resolve().parents[1]
        html = render_html(parse_file(root / "examples" / "reference.md"))
        for tag in [
            "hero",
            "section",
            "feature-grid",
            "timeline",
            "comparison",
            "stats",
            "cta",
            "faq",
            "custom-block",
            "logo-cloud",
            "pricing",
            "quote",
            "callout",
            "image-grid",
            "before-after",
            "steps",
            "card-grid",
            "two-columns",
            "three-columns",
            "table",
            "chart",
            "metric-card",
            "funnel",
            "diagram",
            "footer",
            "thesis-panel",
            "business-snapshot",
            "price-drivers",
            "candlestick-chart",
            "line-chart",
            "bar-chart",
            "donut-chart",
            "waterfall-chart",
            "valuation-table",
            "financial-table",
            "risk-matrix",
            "catalyst-timeline",
            "kpi-row",
            "recommendation",
            "footer-note",
        ]:
            self.assertIn(f'data-block="{tag}"', html)
        self.assertIn("<strong>bold</strong>", html)
        self.assertIn("<em>italic</em>", html)
        self.assertIn("<code>code</code>", html)
        self.assertIn('<a href="https://example.com">links</a>', html)


if __name__ == "__main__":
    unittest.main()
