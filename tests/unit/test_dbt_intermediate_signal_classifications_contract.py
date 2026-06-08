from __future__ import annotations

from pathlib import Path

MODEL_PATH = Path("dbt/models/intermediate/int_asset_signal_classifications.sql")
CONTRACT_PATH = Path("dbt/models/intermediate/int_asset_signal_classifications.yml")


def test_signal_classifications_uses_technical_features_model() -> None:
    model = MODEL_PATH.read_text(encoding="utf-8")

    assert "{{ ref('int_market_technical_features') }}" in model
    assert "regime_label" in model
    assert "regime_explanation" in model
    assert "signal_label" in model
    assert "signal_explanation" in model


def test_signal_classifications_centralizes_regime_and_signal_rules() -> None:
    model = MODEL_PATH.read_text(encoding="utf-8")

    assert "close_vs_3d_moving_avg > 0 and daily_return > 0" in model
    assert "close_vs_3d_moving_avg < 0 and daily_return < 0" in model
    assert "bullish_momentum" in model
    assert "bearish_momentum" in model
    assert "neutral" in model
    assert "buy_watch" in model
    assert "risk_off" in model
    assert "hold_neutral" in model


def test_signal_classifications_preserves_lineage() -> None:
    model = MODEL_PATH.read_text(encoding="utf-8")

    assert "raw_path" in model
    assert "ingestion_run_id" in model
    assert "ingested_at" in model


def test_signal_classifications_contract_defines_allowed_values() -> None:
    contract = CONTRACT_PATH.read_text(encoding="utf-8")

    assert "int_asset_signal_classifications" in contract
    assert "accepted_values" in contract
    assert "bullish_momentum" in contract
    assert "bearish_momentum" in contract
    assert "neutral" in contract
    assert "buy_watch" in contract
    assert "risk_off" in contract
    assert "hold_neutral" in contract
