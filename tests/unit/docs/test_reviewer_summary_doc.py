from __future__ import annotations

from pathlib import Path


def test_reviewer_summary_describes_end_to_end_platform() -> None:
    content = Path("docs/positioning/reviewer_summary.md").read_text(encoding="utf-8")

    assert "end-to-end data engineering" in content
    assert "ingestion" in content
    assert "Snowflake" in content
    assert "dbt" in content
    assert "FastAPI" in content


def test_reviewer_summary_documents_core_capabilities() -> None:
    content = Path("docs/positioning/reviewer_summary.md").read_text(encoding="utf-8")

    assert "Batch ingestion" in content
    assert "Warehouse loading" in content
    assert "Event ingestion" in content
    assert "PySpark feature processing" in content
    assert "Product API" in content


def test_reviewer_summary_documents_api_endpoints() -> None:
    content = Path("docs/positioning/reviewer_summary.md").read_text(encoding="utf-8")

    assert "GET /api/v1/assets/{symbol}/snapshot" in content
    assert "GET /api/v1/assets/{symbol}/regime" in content
    assert "GET /api/v1/assets/{symbol}/signals" in content
    assert "POST /api/v1/ask" in content


def test_reviewer_summary_is_honest_about_aws_activation_boundary() -> None:
    content = Path("docs/positioning/reviewer_summary.md").read_text(encoding="utf-8")

    assert "intentionally not cloud-applied by default" in content
    assert "AWS Lambda latest-price ingestion" in content
    assert "Kinesis price-event stream" in content
    assert "cost-generating actions explicit" in content
