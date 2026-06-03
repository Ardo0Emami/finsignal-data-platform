from __future__ import annotations

from pathlib import Path


def test_fact_backtest_result_uses_signal_fact_and_daily_returns_mart() -> None:
    model = Path("dbt/models/marts/fact_backtest_result.sql").read_text(
        encoding="utf-8"
    )

    assert "{{ ref('fact_signal_daily') }}" in model
    assert "{{ ref('mart_asset_daily_returns') }}" in model
    assert "forward_return_1d" in model
    assert "forward_return_3d" in model
    assert "forward_return_7d" in model
    assert "dateadd(day, 1, signals.price_date)" in model


def test_fact_backtest_result_guards_against_zero_signal_price() -> None:
    model = Path("dbt/models/marts/fact_backtest_result.sql").read_text(
        encoding="utf-8"
    )

    assert "when signals.signal_close_price = 0 then null" in model


def test_fact_backtest_result_has_unique_grain_test() -> None:
    test_sql = Path("dbt/tests/assert_fact_backtest_result_unique_grain.sql").read_text(
        encoding="utf-8"
    )

    assert "{{ ref('fact_backtest_result') }}" in test_sql
    assert "symbol" in test_sql
    assert "signal_date" in test_sql
    assert "signal_code" in test_sql
    assert "signal_version" in test_sql
    assert "having count(*) > 1" in test_sql


def test_backtest_contract_documents_look_ahead_bias_rule() -> None:
    contract = Path("docs/contracts/fact_backtest_result.md").read_text(
        encoding="utf-8"
    )

    assert "Look-Ahead Bias Rule" in contract
    assert "only use data available at or before the signal timestamp" in contract
    assert "Forward return columns are evaluation outcomes" in contract
