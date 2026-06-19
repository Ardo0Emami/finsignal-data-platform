from __future__ import annotations

from pathlib import Path


def test_platform_architecture_documents_core_flow() -> None:
    content = Path("docs/architecture/platform_architecture.md").read_text(encoding="utf-8")

    assert "Market data providers" in content
    assert "Batch ingestion services" in content
    assert "Snowflake RAW / AUDIT" in content
    assert "dbt STAGING / INTERMEDIATE / MARTS" in content
    assert "Product API and governed explanations" in content


def test_platform_architecture_documents_snowflake_layers() -> None:
    content = Path("docs/architecture/platform_architecture.md").read_text(encoding="utf-8")

    assert "`RAW`" in content
    assert "`AUDIT`" in content
    assert "`STAGING`" in content
    assert "`INTERMEDIATE`" in content
    assert "`MARTS`" in content


def test_platform_architecture_documents_product_api_endpoints() -> None:
    content = Path("docs/architecture/platform_architecture.md").read_text(encoding="utf-8")

    assert "GET /api/v1/assets/{symbol}/snapshot" in content
    assert "GET /api/v1/assets/{symbol}/regime" in content
    assert "GET /api/v1/assets/{symbol}/signals" in content
    assert "POST /api/v1/ask" in content


def test_platform_architecture_documents_cost_control_boundary() -> None:
    content = Path("docs/architecture/platform_architecture.md").read_text(encoding="utf-8")

    assert "deployment-ready" in content
    assert "control cloud cost" in content
    assert "cloud-cost-generating steps are explicit" in content
