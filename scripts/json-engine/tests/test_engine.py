"""Tests for momo_paper.engine."""

import json

import pytest

from momo_paper.engine import (
    DEFAULT_TEMPLATE_MAP,
    get_template_dir,
    list_types,
    load_json,
    render,
    render_to_file,
    resolve_template,
)


class TestListTypes:
    def test_returns_sorted_list(self):
        types = list_types()
        assert isinstance(types, list)
        assert len(types) == 15
        assert types == sorted(types)

    def test_contains_expected_types(self):
        types = list_types()
        assert "equity_report" in types
        assert "one_pager" in types
        assert "resume" in types
        assert "infographic" in types


class TestResolveTemplate:
    def test_resolves_known_type(self):
        tpl = resolve_template("one_pager", get_template_dir())
        assert tpl == "one-pager.html.j2"

    def test_resolves_with_explicit_override(self):
        tpl = resolve_template("one_pager", get_template_dir(), "custom.html.j2")
        assert tpl == "custom.html.j2"

    def test_raises_on_unknown_type(self):
        with pytest.raises(ValueError, match="No default template"):
            resolve_template("nonexistent", get_template_dir())

    def test_all_map_entries_have_templates(self):
        template_dir = get_template_dir()
        for doc_type, filename in DEFAULT_TEMPLATE_MAP.items():
            assert (template_dir / filename).exists(), f"Missing: {filename}"


class TestLoadJSON:
    def test_loads_from_dict(self, sample_data):
        result = load_json(sample_data)
        assert result == sample_data

    def test_loads_from_file(self, temp_json_file, sample_data):
        result = load_json(str(temp_json_file))
        assert result["document_type"] == sample_data["document_type"]

    def test_loads_from_stdin(self, temp_json_file, sample_data):
        import sys
        from io import StringIO

        old_stdin = sys.stdin
        try:
            sys.stdin = StringIO(json.dumps(sample_data))
            result = load_json("-")
            assert result["document_type"] == sample_data["document_type"]
        finally:
            sys.stdin = old_stdin

    def test_raises_on_missing_file(self):
        with pytest.raises(FileNotFoundError):
            load_json("/nonexistent/path.json")

    def test_raises_on_non_dict_root(self, temp_dir):
        p = temp_dir / "array.json"
        p.write_text("[]")
        with pytest.raises(ValueError, match="must be an object"):
            load_json(str(p))

    def test_raises_on_missing_required_fields(self, temp_dir):
        p = temp_dir / "incomplete.json"
        p.write_text('{"document_type": "one_pager"}')
        with pytest.raises(ValueError, match="Missing required fields"):
            load_json(str(p))


class TestRender:
    def test_renders_valid_data(self, sample_data):
        html = render(sample_data)
        assert "<!DOCTYPE html>" in html
        assert "Test Title" in html
        assert 'lang="zh-CN"' in html

    def test_renders_equity_report(self, equity_data):
        html = render(equity_data)
        assert "<!DOCTYPE html>" in html
        assert "Test Equity Report" in html

    def test_renders_from_file(self, temp_json_file):
        html = render(str(temp_json_file))
        assert "Test Title" in html

    def test_renders_with_custom_template_dir(self, sample_data):
        template_dir = get_template_dir()
        html = render(sample_data, template_dir=template_dir)
        assert "<!DOCTYPE html>" in html

    def test_chart_filter_renders_chart(self, equity_data):
        html = render(equity_data)
        assert "<svg" in html

    def test_raises_on_bad_type(self, sample_data):
        sample_data["document_type"] = "unknown"
        with pytest.raises(ValueError, match="No default template"):
            render(sample_data)


class TestRenderToFile:
    def test_writes_html_file(self, sample_data, temp_dir):
        out = temp_dir / "output.html"
        result = render_to_file(sample_data, str(out))
        assert result == out
        assert out.exists()
        content = out.read_text(encoding="utf-8")
        assert "Test Title" in content


class TestSlides:
    def test_renders_slides(self, slides_data):
        html = render(slides_data)
        assert "<!DOCTYPE html>" in html
        assert "Test Deck" in html
        assert "slide-cover" in html
        assert "slide" in html

    def test_slides_pagination_included(self, slides_data):
        html = render(slides_data)
        assert "1 / 3" in html
        assert "3 / 3" in html

    def test_load_json_requires_slides_field(self, temp_dir):
        p = temp_dir / "bad-slides.json"
        p.write_text('{"document_type": "slides", "locale": "zh-CN", "meta": {"title": "T"}}')
        with pytest.raises(ValueError, match="slides"):
            load_json(str(p))

    def test_load_json_with_slides(self, slides_data):
        result = load_json(slides_data)
        assert result["slides"] == slides_data["slides"]

    def test_slides_in_default_map(self):
        assert "slides" in DEFAULT_TEMPLATE_MAP
        assert DEFAULT_TEMPLATE_MAP["slides"] == "slides.html.j2"


class TestGetTemplateDir:
    def test_returns_existing_path(self):
        d = get_template_dir()
        assert d.exists()
        assert (d / "_base.html.j2").exists()
