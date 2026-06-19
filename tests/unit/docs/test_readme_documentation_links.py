from __future__ import annotations

from pathlib import Path


def test_readme_links_core_project_documentation() -> None:
    content = Path("README.md").read_text(encoding="utf-8")

    assert "## Project Documentation" in content
    assert "docs/positioning/reviewer_summary.md" in content
    assert "docs/positioning/project_status.md" in content
    assert "docs/architecture/platform_architecture.md" in content
    assert "docs/architecture/platform_flow_diagram.md" in content
    assert "docs/contracts/README.md" in content
    assert "docs/operations/cost_discipline.md" in content


def test_readme_links_product_api_and_operations_docs() -> None:
    content = Path("README.md").read_text(encoding="utf-8")

    assert "docs/contracts/product_api.md" in content
    assert "docs/operations/product_api_runbook.md" in content
    assert "docs/operations/event-ingestion-runbook.md" in content
    assert "docs/operations/snowflake_trial_setup.md" in content
