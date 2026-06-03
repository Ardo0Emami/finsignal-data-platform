from __future__ import annotations

from pathlib import Path


def test_asset_regime_mart_uses_current_asset_snapshot() -> None:
    model = Path("dbt/models/marts/mart_asset_regime.sql").read_text(
        encoding="utf-8"
    )

    assert "{{ ref('mart_current_asset_snapshot') }}" in model
    assert "regime_label" in model
    assert "regime_explanation" in model
    assert "bullish_momentum" in model
    assert "bearish_momentum" in model
    assert "neutral" in model


def test_asset_regime_mart_uses_explainable_rule_features() -> None:
    model = Path("dbt/models/marts/mart_asset_regime.sql").read_text(
        encoding="utf-8"
    )

    assert "close_vs_3d_moving_avg > 0" in model
    assert "daily_return > 0" in model
    assert "close_vs_3d_moving_avg < 0" in model
    assert "daily_return < 0" in model
    assert "Price is above its 3-day moving average" in model
    assert "Price is below its 3-day moving average" in model


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
