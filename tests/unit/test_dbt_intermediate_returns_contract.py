from __future__ import annotations

from pathlib import Path


def test_dbt_project_defines_intermediate_schema() -> None:
    project = Path("dbt/dbt_project.yml").read_text(encoding="utf-8")

    assert "intermediate:" in project
    assert "+schema: INTERMEDIATE" in project


def test_intermediate_returns_model_uses_staging_model_and_lag() -> None:
    model = Path("dbt/models/intermediate/int_market_price_returns.sql").read_text(
        encoding="utf-8"
    )

    assert "{{ ref('stg_market_prices') }}" in model
    assert "lag(close_price) over" in model
    assert "partition by provider_name, dataset_name, symbol" in model
    assert "order by price_timestamp" in model
    assert "daily_return" in model
    assert "previous_close_price" in model
    assert "ingestion_run_id" in model
    assert "raw_path" in model


def test_intermediate_returns_model_guards_against_zero_previous_price() -> None:
    model = Path("dbt/models/intermediate/int_market_price_returns.sql").read_text(
        encoding="utf-8"
    )

    assert "when previous_close_price is null then null" in model
    assert "when previous_close_price = 0 then null" in model
