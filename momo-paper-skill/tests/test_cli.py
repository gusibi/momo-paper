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


if __name__ == "__main__":
    unittest.main()
