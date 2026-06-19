from __future__ import annotations

from pathlib import Path


def test_reviewer_validation_checklist_documents_safe_local_checks() -> None:
    content = Path("docs/operations/reviewer_validation_checklist.md").read_text(
        encoding="utf-8"
    )

    assert "python -m ruff check ." in content
    assert "python -m pytest" in content
    assert "python -m pytest tests/unit/api" in content
    assert "python -m pytest tests/unit/docs" in content


def test_reviewer_validation_checklist_documents_api_smoke_tests() -> None:
    content = Path("docs/operations/reviewer_validation_checklist.md").read_text(
        encoding="utf-8"
    )

    assert "uvicorn app.main:app --reload --port 8000" in content
    assert "curl http://127.0.0.1:8000/health" in content
    assert "curl -X POST http://127.0.0.1:8000/api/v1/ask" in content


def test_reviewer_validation_checklist_documents_aws_boundary() -> None:
    content = Path("docs/operations/reviewer_validation_checklist.md").read_text(
        encoding="utf-8"
    )

    assert "Do not run the following unless intentionally activating AWS resources" in content
    assert "terraform apply" in content
    assert "terraform plan" in content


def test_reviewer_validation_checklist_documents_expected_path() -> None:
    content = Path("docs/operations/reviewer_validation_checklist.md").read_text(
        encoding="utf-8"
    )

    assert "docs/positioning/reviewer_summary.md" in content
    assert "docs/positioning/project_status.md" in content
    assert "docs/architecture/platform_flow_diagram.md" in content
