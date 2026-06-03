from __future__ import annotations

from pathlib import Path


def test_daily_returns_mart_uses_intermediate_returns_model() -> None:
    model = Path("dbt/models/marts/mart_asset_daily_returns.sql").read_text(
        encoding="utf-8"
    )

    assert "{{ ref('int_market_price_returns') }}" in model
    assert "symbol" in model
    assert "price_date" in model
    assert "daily_return" in model
    assert "previous_close_price" in model
    assert "ingestion_run_id" in model
    assert "raw_path" in model


def test_daily_returns_mart_contract_defines_analytics_facing_table() -> None:
    contract = Path("dbt/models/marts/mart_asset_daily_returns.yml").read_text(
        encoding="utf-8"
    )

    assert "mart_asset_daily_returns" in contract
    assert "Analytics-facing daily asset return table" in contract
    assert "symbol" in contract
    assert "price_date" in contract
    assert "daily_return" in contract
