from __future__ import annotations

from pathlib import Path


def test_ingestion_runs_contract_documents_grain_and_status_values() -> None:
    contract = Path("docs/contracts/ingestion_runs.md").read_text(
        encoding="utf-8"
    )

    assert "FINSIGNAL_DW.AUDIT.INGESTION_RUNS" in contract
    assert "one provider" in contract
    assert "one dataset" in contract
    assert "one symbol" in contract
    assert "one ingestion run" in contract
    assert "succeeded" in contract
    assert "failed" in contract


def test_ingestion_runs_contract_documents_relationship_to_raw_data() -> None:
    contract = Path("docs/contracts/ingestion_runs.md").read_text(
        encoding="utf-8"
    )

    assert "records_extracted > 0" in contract
    assert "records_written > 0" in contract
    assert "raw_path is not null" in contract
    assert "error_message is not null" in contract
