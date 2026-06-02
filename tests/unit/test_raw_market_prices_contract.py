from __future__ import annotations

from pathlib import Path


def test_raw_market_prices_contract_documents_grain_and_lineage() -> None:
    contract = Path("docs/contracts/raw_market_prices.md").read_text(
        encoding="utf-8"
    )

    assert "FINSIGNAL_DW.RAW.RAW_MARKET_PRICES" in contract
    assert "one provider" in contract
    assert "one dataset" in contract
    assert "one symbol" in contract
    assert "one price timestamp" in contract
    assert "one ingestion run" in contract
    assert "ingestion_run_id" in contract
    assert "raw_path" in contract
    assert "AUDIT.INGESTION_RUNS.run_id" in contract


def test_raw_market_prices_contract_documents_append_only_duplicate_policy() -> None:
    contract = Path("docs/contracts/raw_market_prices.md").read_text(
        encoding="utf-8"
    )

    assert "append-only" in contract
    assert "does not enforce uniqueness" in contract
    assert "deduplication belongs in the staging layer" in contract
    assert "latest ingested_at" in contract
