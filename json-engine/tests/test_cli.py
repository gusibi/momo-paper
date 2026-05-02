"""Tests for momo_paper.cli."""

import json

import pytest
from click.testing import CliRunner

from momo_paper.cli import cli


@pytest.fixture
def runner():
    return CliRunner()


class TestListCommand:
    def test_list_output(self, runner):
        result = runner.invoke(cli, ["list"])
        assert result.exit_code == 0
        assert "one_pager" in result.output
        assert "equity_report" in result.output
        assert "bar, line, donut" in result.output


class TestInitCommand:
    def test_init_outputs_json(self, runner):
        result = runner.invoke(cli, ["init", "-t", "one_pager"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["document_type"] == "one_pager"
        assert data["locale"] == "zh-CN"
        assert "meta" in data
        assert "sections" in data

    def test_init_with_en_locale(self, runner):
        result = runner.invoke(cli, ["init", "-t", "resume", "-l", "en"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["locale"] == "en"

    def test_init_to_file(self, runner, tmp_path):
        out = tmp_path / "init.json"
        result = runner.invoke(cli, ["init", "-t", "letter", "-o", str(out)])
        assert result.exit_code == 0
        assert out.exists()
        data = json.loads(out.read_text(encoding="utf-8"))
        assert data["document_type"] == "letter"

    def test_init_unknown_type(self, runner):
        result = runner.invoke(cli, ["init", "-t", "bogus"])
        assert result.exit_code == 1
        assert "Unknown" in result.output


class TestRenderCommand:
    def test_render_basic(self, runner, temp_json_file, tmp_path):
        out = tmp_path / "out.html"
        result = runner.invoke(cli, ["render", "-d", str(temp_json_file), "-o", str(out)])
        assert result.exit_code == 0
        assert out.exists()
        content = out.read_text(encoding="utf-8")
        assert "Test Title" in content

    def test_render_missing_file(self, runner, tmp_path):
        out = tmp_path / "out.html"
        result = runner.invoke(cli, ["render", "-d", "/nonexistent.json", "-o", str(out)])
        assert result.exit_code == 1

    def test_render_with_explicit_template(self, runner, temp_equity_json, tmp_path):
        out = tmp_path / "out.html"
        result = runner.invoke(
            cli,
            ["render", "-d", str(temp_equity_json), "-t", "equity-report.html.j2", "-o", str(out)],
        )
        assert result.exit_code == 0

    def test_render_with_custom_template_dir(self, runner, temp_json_file, tmp_path):
        from momo_paper.engine import get_template_dir
        out = tmp_path / "out.html"
        result = runner.invoke(
            cli,
            ["render", "-d", str(temp_json_file), "--template-dir", str(get_template_dir()), "-o", str(out)],
        )
        assert result.exit_code == 0


class TestSlidesCommand:
    def test_init_slides(self, runner):
        result = runner.invoke(cli, ["init", "-t", "slides"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["document_type"] == "slides"
        assert "slides" in data
        assert isinstance(data["slides"], list)
        assert len(data["slides"]) == 4

    def test_render_slides(self, runner, temp_slides_json, tmp_path):
        out = tmp_path / "slides.html"
        result = runner.invoke(cli, ["render", "-d", str(temp_slides_json), "-o", str(out)])
        assert result.exit_code == 0
        content = out.read_text(encoding="utf-8")
        assert "Test Deck" in content
        assert "slide-cover" in content


class TestChartCommand:
    def test_chart_from_file(self, runner, temp_equity_json, tmp_path):
        out = tmp_path / "chart.svg"
        result = runner.invoke(
            cli, ["chart", "-d", str(temp_equity_json), "-k", "sections.price_and_drivers.chart", "-o", str(out)]
        )
        assert result.exit_code == 0
        assert out.exists()
        content = out.read_text(encoding="utf-8")
        assert "<svg" in content
        assert "Price Trend" in content

    def test_chart_stdout(self, runner, temp_equity_json):
        result = runner.invoke(
            cli, ["chart", "-d", str(temp_equity_json), "-k", "sections.price_and_drivers.chart"]
        )
        assert result.exit_code == 0
        assert "<svg" in result.output

    def test_chart_key_not_found(self, runner, temp_equity_json):
        result = runner.invoke(cli, ["chart", "-d", str(temp_equity_json), "-k", "sections.nonexistent"])
        assert result.exit_code == 1


class TestVersion:
    def test_version_output(self, runner):
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "4.0.0" in result.output
