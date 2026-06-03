from __future__ import annotations

from pathlib import Path


def test_dbt_project_defines_expected_project_shape() -> None:
    project = Path("dbt/dbt_project.yml").read_text(encoding="utf-8")

    assert "name: finsignal" in project
    assert "profile: finsignal" in project
    assert "+schema: STAGING" in project
    assert "+schema: MARTS" in project


def test_dbt_profiles_example_uses_finsignal_environment_variables() -> None:
    profile = Path("dbt/profiles.yml.example").read_text(encoding="utf-8")

    assert "FINSIGNAL_SNOWFLAKE_ACCOUNT" in profile
    assert "FINSIGNAL_SNOWFLAKE_USER" in profile
    assert "FINSIGNAL_SNOWFLAKE_PASSWORD" in profile
    assert "FINSIGNAL_SNOWFLAKE_AUTHENTICATOR" in profile
    assert "FINSIGNAL_DEV_WH" in profile
    assert "FINSIGNAL_DW" in profile


def test_dbt_source_defines_raw_market_prices_source() -> None:
    source = Path("dbt/models/staging/sources.yml").read_text(encoding="utf-8")

    assert "name: raw" in source
    assert "schema: RAW" in source
    assert "identifier: RAW_MARKET_PRICES" in source
    assert "ingestion_run_id" in source
    assert "raw_path" in source


def test_stg_market_prices_model_preserves_lineage_and_deduplicates() -> None:
    model = Path("dbt/models/staging/stg_market_prices.sql").read_text(
        encoding="utf-8"
    )

    assert "{{ source('raw', 'raw_market_prices') }}" in model
    assert "row_number() over" in model
    assert "partition by provider_name, dataset_name, symbol, price_timestamp" in model
    assert "order by ingested_at desc, ingestion_run_id desc" in model
    assert "where row_number = 1" in model
    assert "raw_path" in model
    assert "ingestion_run_id" in model
