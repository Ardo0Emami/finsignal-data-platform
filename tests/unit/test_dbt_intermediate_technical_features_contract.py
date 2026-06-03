from __future__ import annotations

from pathlib import Path


def test_technical_features_model_uses_returns_model() -> None:
    model = Path(
        "dbt/models/intermediate/int_market_technical_features.sql"
    ).read_text(encoding="utf-8")

    assert "{{ ref('int_market_price_returns') }}" in model
    assert "close_price_3d_moving_avg" in model
    assert "daily_return_3d_volatility" in model
    assert "close_vs_3d_moving_avg" in model


def test_technical_features_model_uses_rolling_windows_by_symbol() -> None:
    model = Path(
        "dbt/models/intermediate/int_market_technical_features.sql"
    ).read_text(encoding="utf-8")

    assert "partition by provider_name, dataset_name, symbol" in model
    assert "order by price_timestamp" in model
    assert "rows between 2 preceding and current row" in model


def test_technical_features_model_preserves_lineage() -> None:
    model = Path(
        "dbt/models/intermediate/int_market_technical_features.sql"
    ).read_text(encoding="utf-8")

    assert "ingestion_run_id" in model
    assert "raw_path" in model
    assert "ingested_at" in model
