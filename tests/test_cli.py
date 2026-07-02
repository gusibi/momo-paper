import json
import unittest
from pathlib import Path
import tempfile

from momo_dsl.cli import main


class CliTests(unittest.TestCase):
    def setUp(self):
        try:
            self.tmp_dir = tempfile.TemporaryDirectory()
        except (FileNotFoundError, PermissionError) as exc:
            self.skipTest(f"no writable temp directory: {exc}")
        self.tmp = Path(self.tmp_dir.name)

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_validate_and_render(self):
        source = self.tmp / "page.md"
        output = self.tmp / "out" / "page.html"
        source.write_text("""---
document_type: landing
locale: en
title: CLI Test
---

:::hero
title: Hello
:::
""", encoding="utf-8")

        self.assertEqual(main(["validate", str(source)]), 0)
        self.assertEqual(main(["render", str(source), "-o", str(output)]), 0)
        self.assertTrue(output.exists())
        html = output.read_text(encoding="utf-8")
        self.assertIn("CLI Test", html)
        self.assertIn("<style>", html)
        self.assertFalse((output.parent / "momo-paper.css").exists())

    def test_render_with_custom_css_file(self):
        source = self.tmp / "page.md"
        css = self.tmp / "theme.css"
        output = self.tmp / "out" / "page.html"
        source.write_text("""---
document_type: landing
locale: en
title: CLI Test
---
""", encoding="utf-8")
        css.write_text(".page { color: red; }\n", encoding="utf-8")

        self.assertEqual(main(["render", str(source), "-o", str(output), "--css", str(css)]), 0)
        self.assertIn(".page { color: red; }", output.read_text(encoding="utf-8"))

    def test_validate_returns_error(self):
        source = self.tmp / "bad.md"
        source.write_text("no frontmatter", encoding="utf-8")
        self.assertEqual(main(["validate", str(source)]), 1)

    def test_validate_json_ok(self):
        source = self.tmp / "page.md"
        source.write_text(
            "---\ndocument_type: landing\nlocale: en\ntitle: T\n---\n\n:::hero\ntitle: Hi\n:::\n",
            encoding="utf-8",
        )
        rc, out, _ = self._capture(["validate", str(source), "--json"])
        self.assertEqual(rc, 0)
        self.assertEqual(json.loads(out), {"ok": True, "errors": []})

    def test_validate_json_error_payload(self):
        source = self.tmp / "bad.md"
        source.write_text("no frontmatter", encoding="utf-8")
        rc, out, _ = self._capture(["validate", str(source), "--json"])
        self.assertEqual(rc, 1)
        payload = json.loads(out)
        self.assertFalse(payload["ok"])
        self.assertEqual(len(payload["errors"]), 1)
        err = payload["errors"][0]
        self.assertIn("message", err)
        self.assertEqual(err["line"], 1)
        self.assertIsNone(err["block"])

    def test_bench_text_and_json(self):
        source = self.tmp / "page.md"
        source.write_text(
            "---\ndocument_type: landing\nlocale: en\ntitle: T\n---\n\n:::hero\ntitle: Hi\n:::\n",
            encoding="utf-8",
        )
        self.assertEqual(main(["bench", str(source)]), 0)
        rc, out, _ = self._capture(["bench", str(source), "--json"])
        self.assertEqual(rc, 0)
        payload = json.loads(out)
        for key in ("dsl_tokens", "html_tokens", "saved_percent", "tokenizer"):
            self.assertIn(key, payload)
        self.assertGreater(payload["html_tokens"], payload["dsl_tokens"])
        self.assertGreater(payload["saved_percent"], 0)

    def test_render_pdf(self):
        try:
            import playwright  # noqa: F401
        except ImportError:
            self.skipTest("playwright not installed")
        source = self.tmp / "page.md"
        output = self.tmp / "out.pdf"
        source.write_text(
            "---\ndocument_type: landing\nlocale: en\ntitle: T\n---\n\n:::hero\ntitle: Hi\n:::\n",
            encoding="utf-8",
        )
        self.assertEqual(main(["render", str(source), "-o", str(output), "--format", "pdf"]), 0)
        self.assertTrue(output.exists())
        self.assertTrue(output.read_bytes()[:5].startswith(b"%PDF"))

    @staticmethod
    def _capture(argv):
        import io
        from contextlib import redirect_stdout

        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = main(argv)
        return rc, buf.getvalue(), None


if __name__ == "__main__":
    unittest.main()
