from __future__ import annotations

from pathlib import Path


def test_fact_signal_daily_uses_classifications_and_signal_definitions() -> None:
    model = Path("dbt/models/marts/fact_signal_daily.sql").read_text(
        encoding="utf-8"
    )

    assert "{{ ref('int_asset_signal_classifications') }}" in model
    assert "{{ ref('signal_definitions') }}" in model
    assert "signal_code = 'momentum_regime_v1'" in model
    assert "signal_version" in model
    assert "signal_label" in model
    assert "signal_explanation" in model


def test_fact_signal_daily_does_not_duplicate_classification_rules() -> None:
    model = Path("dbt/models/marts/fact_signal_daily.sql").read_text(
        encoding="utf-8"
    )

    assert "bullish_momentum" not in model
    assert "bearish_momentum" not in model
    assert "then 'buy_watch'" not in model
    assert "then 'risk_off'" not in model
    assert "close_vs_3d_moving_avg > 0 and daily_return > 0" not in model


def test_fact_signal_daily_contract_documents_historical_grain() -> None:
    contract = Path("dbt/models/marts/fact_signal_daily.yml").read_text(
        encoding="utf-8"
    )

    assert "Historical daily signal fact table" in contract
    assert "symbol" in contract
    assert "price_date" in contract
    assert "signal_code" in contract
    assert "signal_version" in contract
    assert "accepted_values" in contract


def test_fact_signal_daily_has_singular_uniqueness_test() -> None:
    test_sql = Path("dbt/tests/assert_fact_signal_daily_unique_grain.sql").read_text(
        encoding="utf-8"
    )

    assert "{{ ref('fact_signal_daily') }}" in test_sql
    assert "symbol" in test_sql
    assert "price_date" in test_sql
    assert "signal_code" in test_sql
    assert "signal_version" in test_sql
    assert "having count(*) > 1" in test_sql
