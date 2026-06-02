from __future__ import annotations

from pathlib import Path


def test_snowflake_trial_setup_runbook_documents_safe_validation_order() -> None:
    runbook = Path("docs/operations/snowflake_trial_setup.md").read_text(
        encoding="utf-8"
    )

    assert "python -m scripts.snowflake.check_snowflake_ready" in runbook
    assert "python -m scripts.snowflake.test_connection" in runbook
    assert "python -m scripts.snowflake.apply_schema" in runbook
    assert "python -m scripts.snowflake.load_raw_market_prices --limit 2" in runbook


def test_snowflake_trial_setup_runbook_documents_cost_safety() -> None:
    runbook = Path("docs/operations/snowflake_trial_setup.md").read_text(
        encoding="utf-8"
    )

    assert "FINSIGNAL_DEV_WH" in runbook
    assert "WAREHOUSE_SIZE = XSMALL" in runbook
    assert "AUTO_SUSPEND = 60" in runbook
    assert "ALTER WAREHOUSE FINSIGNAL_DEV_WH SUSPEND" in runbook
