import unittest
from pathlib import Path

from momo_dsl.errors import DslError
from momo_dsl.parser import BlockNode, MarkdownNode, parse_file, parse_text
from momo_dsl.schema import validate_document


VALID = """---
document_type: landing
locale: zh-CN
title: Test Page
---

## Intro

:::hero
title: Hello
primary_cta:
  label: Start
  href: /start
:::
"""


class ParserTests(unittest.TestCase):
    def test_parses_frontmatter_markdown_and_block(self):
        doc = parse_text(VALID)
        self.assertEqual(doc.meta["document_type"], "landing")
        self.assertIsInstance(doc.nodes[0], MarkdownNode)
        self.assertIsInstance(doc.nodes[1], BlockNode)
        self.assertEqual(doc.nodes[1].name, "hero")
        self.assertEqual(doc.nodes[1].props["primary_cta"]["label"], "Start")

    def test_parses_nested_list_items(self):
        doc = parse_text("""---
document_type: landing
locale: en
title: Test
---

:::feature-grid
items:
  - title: One
    desc: First
  - title: Two
    desc: Second
:::
""")
        block = doc.nodes[0]
        self.assertIsInstance(block, BlockNode)
        self.assertEqual(block.props["items"][1]["desc"], "Second")

    def test_parses_reference_example_tags(self):
        root = Path(__file__).resolve().parents[1]
        doc = parse_file(root / "examples" / "reference.md")
        tags = [node.name for node in doc.nodes if isinstance(node, BlockNode)]
        for expected in [
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
            self.assertIn(expected, tags)

    def test_parses_scalar_types(self):
        doc = parse_text("""---
document_type: landing
locale: en
title: Scalars
featured: true
count: 3
ratio: 1.5
empty: null
---

:::section
active: false
count: 10
ratio: 2.25
empty: ~
quoted: "A quoted value"
:::
""")
        self.assertEqual(doc.meta["featured"], True)
        self.assertEqual(doc.meta["count"], 3)
        self.assertEqual(doc.meta["ratio"], 1.5)
        self.assertIsNone(doc.meta["empty"])
        block = doc.nodes[0]
        self.assertIsInstance(block, BlockNode)
        self.assertEqual(block.props["active"], False)
        self.assertEqual(block.props["quoted"], "A quoted value")

    def test_accepts_custom_tags(self):
        doc = parse_text("""---
document_type: landing
locale: en
title: Custom
---

:::pricing-note
title: Pricing note
items:
  - Free tier
  - Pro tier
:::
""")
        block = doc.nodes[0]
        self.assertIsInstance(block, BlockNode)
        self.assertEqual(block.name, "pricing-note")
        self.assertEqual(block.props["items"], ["Free tier", "Pro tier"])

    def test_rejects_missing_frontmatter(self):
        with self.assertRaises(DslError):
            parse_text("# No frontmatter")

    def test_rejects_unclosed_block(self):
        with self.assertRaisesRegex(DslError, "unclosed"):
            parse_text("""---
document_type: landing
locale: en
title: Test
---

:::hero
title: Hello
""")

    def test_rejects_invalid_tag(self):
        with self.assertRaisesRegex(DslError, "invalid block tag"):
            parse_text("""---
document_type: landing
locale: en
title: Test
---

:::Hero
title: Hello
:::
""")

    def test_rejects_underscore_tag(self):
        with self.assertRaisesRegex(DslError, "invalid block tag"):
            parse_text("""---
document_type: landing
locale: en
title: Test
---

:::feature_grid
title: Hello
:::
""")

    def test_rejects_tab_indentation(self):
        with self.assertRaisesRegex(DslError, "tabs"):
            parse_text("""---
document_type: landing
locale: en
title: Test
---

:::section
button:
\tlabel: Start
:::
""")

    def test_reports_dashboard_document_type_as_semantic_error(self):
        doc = parse_text("""---
document_type: dashboard
locale: en
title: Test
---
""")
        report = validate_document(doc)
        self.assertIn("invalid_document_type", [error.code for error in report.errors])

    def test_reports_missing_locale_as_semantic_error(self):
        doc = parse_text("""---
document_type: landing
title: Test
---
""")
        report = validate_document(doc)
        self.assertIn("missing_field", [error.code for error in report.errors])


if __name__ == "__main__":
    unittest.main()
