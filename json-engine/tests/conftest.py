"""Shared test fixtures for momo_paper tests."""

import json
import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def sample_data():
    """Minimal valid document data dict."""
    return {
        "document_type": "one_pager",
        "locale": "zh-CN",
        "meta": {
            "title": "Test Title",
            "subtitle": "Test Subtitle",
            "eyebrow": "Momo Paper / test",
            "date": "2025-01-01",
        },
        "sections": {},
    }


@pytest.fixture
def equity_data():
    """Sample equity report data with sections."""
    return {
        "document_type": "equity_report",
        "locale": "zh-CN",
        "meta": {
            "title": "Test Equity Report",
            "subtitle": "Test Ticker",
            "eyebrow": "Equity Research",
            "date": "2025-01-01",
        },
        "sections": {
            "thesis": {"body": "Test thesis"},
            "business_snapshot": {
                "cards": [
                    {"label": "Revenue", "value": "100B"},
                ]
            },
            "price_and_drivers": {
                "body": ["Price analysis."],
                "chart": {
                    "type": "line",
                    "title": "Price Trend",
                    "data": {
                        "labels": ["Jan", "Feb", "Mar"],
                        "values": [100, 120, 110],
                    },
                }
            },
        },
    }


@pytest.fixture
def temp_dir():
    """Create a temporary directory that is cleaned up after the test."""
    with tempfile.TemporaryDirectory() as d:
        yield Path(d)


@pytest.fixture
def temp_json_file(temp_dir, sample_data):
    """Write sample data to a temp JSON file, return its path."""
    p = temp_dir / "test.json"
    p.write_text(json.dumps(sample_data, ensure_ascii=False), encoding="utf-8")
    return p


@pytest.fixture
def temp_equity_json(temp_dir, equity_data):
    """Write equity data to a temp JSON file."""
    p = temp_dir / "equity.json"
    p.write_text(json.dumps(equity_data, ensure_ascii=False), encoding="utf-8")
    return p


@pytest.fixture
def slides_data():
    """Minimal valid slides data dict."""
    return {
        "document_type": "slides",
        "locale": "zh-CN",
        "meta": {
            "title": "Test Deck",
            "subtitle": "A test presentation",
            "eyebrow": "Momo Paper / slides",
            "date": "2025-01-01",
        },
        "slides": [
            {"title": "封面", "point": "主结论", "layout": "cover"},
            {"title": "问题", "point": "核心观点", "bullets": ["要点1", "要点2"]},
            {"title": "结论", "point": "下一步", "layout": "closing"},
        ],
    }


@pytest.fixture
def temp_slides_json(temp_dir, slides_data):
    """Write slides data to a temp JSON file."""
    p = temp_dir / "slides.json"
    p.write_text(json.dumps(slides_data, ensure_ascii=False), encoding="utf-8")
    return p
