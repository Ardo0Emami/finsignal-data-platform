from __future__ import annotations

from pathlib import Path


def test_cost_discipline_doc_documents_no_implicit_cloud_creation() -> None:
    content = Path("docs/operations/cost_discipline.md").read_text(encoding="utf-8")

    assert "No implicit cloud creation" in content
    assert "terraform plan" in content
    assert "terraform apply" in content


def test_cost_discipline_doc_documents_cost_generating_boundaries() -> None:
    content = Path("docs/operations/cost_discipline.md").read_text(encoding="utf-8")

    assert "AWS Kinesis streams" in content
    assert "AWS Lambda executions" in content
    assert "Snowflake warehouse runtime" in content
    assert "long-running Spark jobs" in content


def test_cost_discipline_doc_documents_streaming_apply_boundary() -> None:
    content = Path("docs/operations/cost_discipline.md").read_text(encoding="utf-8")

    assert "event-ingestion layer" in content
    assert "implementation-ready" in content
    assert "not applied by default" in content


def test_cost_discipline_doc_documents_cleanup_checklist() -> None:
    content = Path("docs/operations/cost_discipline.md").read_text(encoding="utf-8")

    assert "Cleanup checklist" in content
    assert "Suspend unused Snowflake warehouses" in content
    assert "Destroy temporary Terraform-managed resources" in content
