from __future__ import annotations

from pathlib import Path


def test_project_status_documents_all_phases() -> None:
    content = Path("docs/positioning/project_status.md").read_text(encoding="utf-8")

    for phase_number in range(1, 11):
        assert f"Phase {phase_number}" in content


def test_project_status_is_honest_about_event_ingestion_boundary() -> None:
    content = Path("docs/positioning/project_status.md").read_text(encoding="utf-8")

    assert "Implementation-ready; not AWS-applied by default" in content
    assert "AWS infrastructure is intentionally not applied by default" in content
    assert "avoids accidental cost creation" in content


def test_project_status_documents_product_api_endpoints() -> None:
    content = Path("docs/positioning/project_status.md").read_text(encoding="utf-8")

    assert "GET /api/v1/assets/{symbol}/snapshot" in content
    assert "GET /api/v1/assets/{symbol}/regime" in content
    assert "GET /api/v1/assets/{symbol}/signals" in content
    assert "POST /api/v1/ask" in content


def test_project_status_documents_current_honest_positioning() -> None:
    content = Path("docs/positioning/project_status.md").read_text(encoding="utf-8")

    assert "end-to-end data engineering platform" in content
    assert "cloud activation is intentionally separated" in content
    assert "cost-generating actions explicit" in content
