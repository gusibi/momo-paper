import unittest
from pathlib import Path

from momo_dsl.parser import parse_file, parse_text
from momo_dsl.schema import describe_schema, infer_schema, list_schemas, validate_document


class SchemaTests(unittest.TestCase):
    def test_lists_and_describes_flagship_schemas(self):
        names = [item.name for item in list_schemas()]
        self.assertEqual(names, ["deep-research", "landing-page", "research-summary"])
        schema = describe_schema("deep-research")
        self.assertIn("sources", schema["composition"]["required_blocks"])

    def test_infers_landing_alias(self):
        doc = parse_text("""---
document_type: landing
locale: en
title: Test
---

:::hero
title: Hello
:::
""")
        selected, candidates = infer_schema(doc)
        self.assertEqual(selected, "landing-page")
        self.assertEqual(candidates, ("landing-page",))

    def test_unknown_document_uses_free_mode(self):
        doc = parse_text("""---
document_type: custom-report
locale: en
title: Test
---

:::custom-block
anything: stays renderable
:::
""")
        report = validate_document(doc)
        self.assertTrue(report.ok)
        self.assertEqual(report.mode, "free")
        self.assertEqual(report.warnings[0].code, "schema_not_inferred")

    def test_collects_document_block_field_and_citation_errors(self):
        doc = parse_text("""---
document_type: research-summary
locale: en
title: Broken
extra: no
---

:::key-findings
items:
  - title: Finding
    body: Evidence
    citations:
      - missing-source
    unknown: no
:::

:::extra-block
value: no
:::
""", path="broken.md")
        report = validate_document(doc)
        codes = {error.code for error in report.errors}
        self.assertTrue(
            {"unknown_field", "unknown_block", "missing_block", "unresolved_citation"}.issubset(codes)
        )
        citation = next(error for error in report.errors if error.code == "unresolved_citation")
        self.assertEqual(citation.field, "items[0].citations[0]")
        self.assertEqual(citation.line, 13)

    def test_reports_duplicate_sources(self):
        doc = parse_text("""---
document_type: deep-research
locale: en
title: Duplicate Sources
---

:::research-header
topic: Test
:::
:::executive-summary
summary: Test
:::
:::key-findings
items:
  - title: Test
    body: Test
:::
:::methodology
summary: Test
methods:
  - Review
:::
:::sources
items:
  - id: same
    title: One
    url: one
  - id: same
    title: Two
    url: two
:::
""")
        report = validate_document(doc)
        self.assertIn("duplicate_source_id", [error.code for error in report.errors])

    def test_flagship_examples_validate_strictly(self):
        root = Path(__file__).resolve().parents[1]
        for name in ("landing-page.md", "research-summary.md", "deep-research.md"):
            with self.subTest(name=name):
                report = validate_document(parse_file(root / "examples" / name))
                self.assertTrue(report.ok, report.errors)
                self.assertEqual(report.mode, "strict")

    def test_legacy_landing_with_experimental_blocks_uses_free_mode(self):
        root = Path(__file__).resolve().parents[1]
        report = validate_document(parse_file(root / "examples" / "reference.md"))
        self.assertTrue(report.ok)
        self.assertEqual(report.mode, "free")

    def test_existing_equity_report_remains_free_mode(self):
        root = Path(__file__).resolve().parents[1]
        report = validate_document(parse_file(root / "examples" / "equity-report.md"))
        self.assertTrue(report.ok)
        self.assertEqual(report.mode, "free")
        self.assertEqual(report.warnings[0].code, "schema_not_inferred")

    def test_explicit_unknown_schema_is_an_error(self):
        doc = parse_text("""---
document_type: custom
locale: en
title: Test
---
""")
        report = validate_document(doc, schema_name="missing")
        self.assertFalse(report.ok)
        self.assertEqual(report.errors[0].code, "unknown_schema")


if __name__ == "__main__":
    unittest.main()
