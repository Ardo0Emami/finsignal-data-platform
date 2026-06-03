from __future__ import annotations

from pathlib import Path


def test_dbt_project_defines_seed_path_and_seed_schema() -> None:
    project = Path("dbt/dbt_project.yml").read_text(encoding="utf-8")

    assert "seed-paths:" in project
    assert "- seeds" in project
    assert "seeds:" in project
    assert "+schema: MARTS" in project


def test_signal_definitions_seed_is_versioned() -> None:
    seed = Path("dbt/seeds/signal_definitions.csv").read_text(encoding="utf-8")

    assert "signal_code" in seed
    assert "signal_version" in seed
    assert "momentum_regime_v1" in seed
    assert "true" in seed


def test_asset_signal_mart_uses_regime_and_signal_definition_seed() -> None:
    model = Path("dbt/models/marts/mart_asset_signal.sql").read_text(
        encoding="utf-8"
    )

    assert "{{ ref('mart_asset_regime') }}" in model
    assert "{{ ref('signal_definitions') }}" in model
    assert "signal_code = 'momentum_regime_v1'" in model
    assert "signal_version" in model
    assert "signal_label" in model
    assert "signal_explanation" in model


def test_asset_signal_mart_defines_expected_signal_labels() -> None:
    model = Path("dbt/models/marts/mart_asset_signal.sql").read_text(
        encoding="utf-8"
    )

    assert "buy_watch" in model
    assert "risk_off" in model
    assert "hold_neutral" in model

    contract = Path("dbt/models/marts/mart_asset_signal.yml").read_text(
        encoding="utf-8"
    )

    assert "accepted_values" in contract
    assert "buy_watch" in contract
    assert "risk_off" in contract
    assert "hold_neutral" in contract
