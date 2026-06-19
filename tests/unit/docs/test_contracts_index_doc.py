from __future__ import annotations

from pathlib import Path


def test_contracts_index_documents_contract_groups() -> None:
    content = Path("docs/contracts/README.md").read_text(encoding="utf-8")

    assert "Raw contracts" in content
    assert "Audit contracts" in content
    assert "Mart contracts" in content
    assert "API contracts" in content


def test_contracts_index_references_existing_contract_files() -> None:
    content = Path("docs/contracts/README.md").read_text(encoding="utf-8")

    assert "raw_market_prices.md" in content
    assert "ingestion_runs.md" in content
    assert "fact_backtest_result.md" in content
    assert "product_api.md" in content


def test_contracts_index_documents_lineage_fields() -> None:
    content = Path("docs/contracts/README.md").read_text(encoding="utf-8")

    assert "ingestion_run_id" in content
    assert "raw_path" in content
    assert "lineage fields" in content


def test_contracts_index_documents_governed_api_behavior() -> None:
    content = Path("docs/contracts/README.md").read_text(encoding="utf-8")

    assert "governed mart outputs" in content
    assert "evidence-based explanations" in content
