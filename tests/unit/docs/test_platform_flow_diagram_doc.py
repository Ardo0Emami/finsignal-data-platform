from __future__ import annotations

from pathlib import Path


def test_platform_flow_diagram_contains_mermaid_diagram() -> None:
    content = Path("docs/architecture/platform_flow_diagram.md").read_text(encoding="utf-8")

    assert "```mermaid" in content
    assert "flowchart TD" in content
    assert "flowchart LR" in content


def test_platform_flow_diagram_documents_core_layers() -> None:
    content = Path("docs/architecture/platform_flow_diagram.md").read_text(encoding="utf-8")

    assert "Market Data Providers" in content
    assert "Batch Ingestion Services" in content
    assert "Snowflake RAW Schema" in content
    assert "dbt MARTS Models" in content
    assert "FastAPI Product API" in content


def test_platform_flow_diagram_documents_governed_ask_endpoint() -> None:
    content = Path("docs/architecture/platform_flow_diagram.md").read_text(encoding="utf-8")

    assert "Governed Ask Endpoint" in content
    assert "Evidence-Based Explanation" in content
    assert "`/api/v1/ask`" in content


def test_platform_flow_diagram_documents_event_ingestion_side_path() -> None:
    content = Path("docs/architecture/platform_flow_diagram.md").read_text(encoding="utf-8")

    assert "Lambda Ingestion Handler" in content
    assert "Kinesis Price Event Stream" in content
    assert "Snowflake RAW_PRICE_EVENTS" in content
    assert "cost-generating resources" in content
