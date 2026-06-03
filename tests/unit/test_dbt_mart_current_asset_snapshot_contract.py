from __future__ import annotations

from pathlib import Path


def test_current_asset_snapshot_uses_technical_features_model() -> None:
    model = Path("dbt/models/marts/mart_current_asset_snapshot.sql").read_text(
        encoding="utf-8"
    )

    assert "{{ ref('int_market_technical_features') }}" in model
    assert "row_number() over" in model
    assert "partition by symbol" in model
    assert "order by price_timestamp desc, ingested_at desc" in model
    assert "where row_number = 1" in model


def test_current_asset_snapshot_exposes_latest_feature_columns() -> None:
    model = Path("dbt/models/marts/mart_current_asset_snapshot.sql").read_text(
        encoding="utf-8"
    )

    assert "daily_return" in model
    assert "close_price_3d_moving_avg" in model
    assert "daily_return_3d_volatility" in model
    assert "close_vs_3d_moving_avg" in model
    assert "ingestion_run_id" in model
    assert "raw_path" in model


def test_current_asset_snapshot_contract_requires_unique_symbol() -> None:
    contract = Path("dbt/models/marts/mart_current_asset_snapshot.yml").read_text(
        encoding="utf-8"
    )

    assert "mart_current_asset_snapshot" in contract
    assert "Latest analytics-ready market snapshot per asset" in contract
    assert "- unique" in contract
