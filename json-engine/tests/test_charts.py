"""Tests for momo_paper.charts."""

import pytest

from momo_paper.charts import (
    render,
    render_bar,
    render_line,
    render_donut,
    render_candlestick,
    render_waterfall,
    CHART_COLORS,
)


def _chart(type, labels, values, title="Test Chart", height=280):
    return {"type": type, "title": title, "height": height, "data": {"labels": labels, "values": values}}


class TestRenderBar:
    def test_renders_valid_bar(self):
        chart = _chart("bar", ["A", "B", "C"], [10, 20, 30])
        svg = render_bar(chart)
        assert "<svg" in svg
        assert "</svg>" in svg
        assert "Test Chart" in svg

    def test_includes_values(self):
        chart = _chart("bar", ["X"], [42])
        svg = render_bar(chart)
        assert "42" in svg

    def test_empty_data_returns_empty(self):
        assert render_bar({"data": {"labels": [], "values": []}}) == ""

    def test_mismatched_lengths_returns_empty(self):
        assert render_bar({"data": {"labels": ["A"], "values": [1, 2]}}) == ""


class TestRenderLine:
    def test_renders_valid_line(self):
        chart = _chart("line", ["Jan", "Feb", "Mar"], [10, 20, 15])
        svg = render_line(chart)
        assert "<svg" in svg
        assert "</svg>" in svg

    def test_empty_data_returns_empty(self):
        assert render_line({"data": {"labels": [], "values": []}}) == ""


class TestRenderDonut:
    def test_renders_valid_donut(self):
        chart = _chart("donut", ["A", "B"], [30, 70], height=320)
        svg = render_donut(chart)
        assert "<svg" in svg
        assert "</svg>" in svg
        assert "Total" in svg
        assert "100" in svg

    def test_zero_total_returns_empty(self):
        assert render_donut({"data": {"labels": ["A"], "values": [0]}}) == ""

    def test_empty_data_returns_empty(self):
        assert render_donut({"data": {"labels": [], "values": []}}) == ""


class TestRenderCandlestick:
    def test_renders_valid_candlestick(self):
        chart = {
            "type": "candlestick",
            "title": "OHLC",
            "height": 320,
            "data": {
                "labels": ["Mon", "Tue", "Wed"],
                "values": [
                    {"o": 100, "h": 105, "l": 98, "c": 103},
                    {"o": 103, "h": 108, "l": 101, "c": 105},
                    {"o": 105, "h": 106, "l": 95, "c": 97},
                ],
            },
        }
        svg = render_candlestick(chart)
        assert "<svg" in svg
        assert "</svg>" in svg
        assert "OHLC" in svg
        # Positive body uses positive color
        assert CHART_COLORS["positive"] in svg
        # Negative body (3rd candle: close < open) uses negative color
        assert CHART_COLORS["negative"] in svg

    def test_also_accepts_open_high_low_close_keys(self):
        chart = {
            "type": "candlestick",
            "data": {
                "labels": ["D1"],
                "values": [{"open": 50, "high": 55, "low": 48, "close": 52}],
            },
        }
        svg = render_candlestick(chart)
        assert "<svg" in svg

    def test_empty_data_returns_empty(self):
        assert render_candlestick({"data": {"labels": [], "values": []}}) == ""

    def test_mismatched_lengths_returns_empty(self):
        assert render_candlestick({"data": {"labels": ["A"], "values": []}}) == ""


class TestRenderWaterfall:
    def test_renders_valid_waterfall(self):
        chart = {
            "type": "waterfall",
            "title": "Revenue Bridge",
            "height": 300,
            "data": {
                "labels": ["Start", "Product A", "Product B", "Costs", "Total"],
                "values": [100, 30, 20, -15, 135],
            },
        }
        svg = render_waterfall(chart)
        assert "<svg" in svg
        assert "</svg>" in svg
        assert "Revenue Bridge" in svg

    def test_total_bar_uses_accent_color(self):
        chart = {
            "type": "waterfall",
            "data": {
                "labels": ["Start", "Total"],
                "values": [50, 50],
            },
        }
        svg = render_waterfall(chart)
        assert CHART_COLORS["accent"] in svg

    def test_negative_values_use_negative_color(self):
        chart = {
            "type": "waterfall",
            "data": {
                "labels": ["Start", "Expense"],
                "values": [100, -20],
            },
        }
        svg = render_waterfall(chart)
        assert CHART_COLORS["negative"] in svg

    def test_empty_data_returns_empty(self):
        assert render_waterfall({"data": {"labels": [], "values": []}}) == ""

    def test_mismatched_lengths_returns_empty(self):
        assert render_waterfall({"data": {"labels": ["A"], "values": []}}) == ""


class TestRenderDispatch:
    def test_renders_bar_via_dispatch(self):
        chart = _chart("bar", ["A"], [10])
        svg = render(chart)
        assert "<svg" in svg

    def test_renders_line_via_dispatch(self):
        chart = _chart("line", ["A", "B"], [10, 20])
        svg = render(chart)
        assert "<svg" in svg

    def test_renders_donut_via_dispatch(self):
        chart = _chart("donut", ["A", "B"], [10, 20], height=320)
        svg = render(chart)
        assert "<svg" in svg

    def test_renders_candlestick_via_dispatch(self):
        chart = {
            "type": "candlestick",
            "data": {
                "labels": ["A"],
                "values": [{"o": 10, "h": 12, "l": 8, "c": 11}],
            },
        }
        svg = render(chart)
        assert "<svg" in svg

    def test_renders_waterfall_via_dispatch(self):
        chart = _chart("waterfall", ["Start", "End"], [10, 10])
        svg = render(chart)
        assert "<svg" in svg

    def test_unsupported_type_returns_comment(self):
        svg = render({"type": "unknown", "data": {"labels": [], "values": []}})
        assert "unsupported chart type" in svg

    def test_empty_dict_returns_empty(self):
        assert render({}) == ""

    def test_none_returns_empty(self):
        assert render(None) == ""

    def test_non_dict_returns_empty(self):
        assert render("foo") == ""


class TestChartColors:
    def test_has_primary_color(self):
        assert "primary" in CHART_COLORS

    def test_categorical_has_six_colors(self):
        assert len(CHART_COLORS["categorical"]) >= 6
