from __future__ import annotations

from pathlib import Path


def test_asset_regime_mart_uses_centralized_signal_classifications() -> None:
    model = Path("dbt/models/marts/mart_asset_regime.sql").read_text(
        encoding="utf-8"
    )

    assert "{{ ref('int_asset_signal_classifications') }}" in model
    assert "regime_label" in model
    assert "regime_explanation" in model
    assert "qualify row_number() over" in model
    assert "partition by symbol" in model
    assert "order by price_timestamp desc, ingested_at desc" in model


def test_asset_regime_mart_does_not_duplicate_classification_rules() -> None:
    model = Path("dbt/models/marts/mart_asset_regime.sql").read_text(
        encoding="utf-8"
    )

    assert "bullish_momentum" not in model
    assert "bearish_momentum" not in model
    assert "close_vs_3d_moving_avg > 0" not in model
    assert "daily_return > 0" not in model


def test_asset_regime_contract_defines_allowed_regime_labels() -> None:
    contract = Path("dbt/models/marts/mart_asset_regime.yml").read_text(
        encoding="utf-8"
    )

    assert "mart_asset_regime" in contract
    assert "Current explainable market regime classification per asset" in contract
    assert "accepted_values" in contract
    assert "bullish_momentum" in contract
    assert "bearish_momentum" in contract
    assert "neutral" in contract
    assert "regime_explanation" in contract
