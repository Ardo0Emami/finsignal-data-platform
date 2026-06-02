from __future__ import annotations

from pathlib import Path

from scripts.snowflake.apply_schema import DEFAULT_SCHEMA_SCRIPT_PATHS


def test_snowflake_warehouse_script_defines_cost_guardrails() -> None:
    sql = Path("scripts/snowflake/000_create_warehouse.sql").read_text(
        encoding="utf-8"
    )

    assert "CREATE WAREHOUSE IF NOT EXISTS FINSIGNAL_DEV_WH" in sql
    assert "WAREHOUSE_SIZE = XSMALL" in sql
    assert "AUTO_SUSPEND = 60" in sql
    assert "AUTO_RESUME = TRUE" in sql
    assert "INITIALLY_SUSPENDED = TRUE" in sql


def test_schema_apply_runs_warehouse_script_first() -> None:
    assert DEFAULT_SCHEMA_SCRIPT_PATHS[0] == Path(
        "scripts/snowflake/000_create_warehouse.sql"
    )


def test_readme_documents_snowflake_cost_guardrails() -> None:
    readme = Path("README.md").read_text(encoding="utf-8")

    assert "## Snowflake Cost Guardrails" in readme
    assert "FINSIGNAL_DEV_WH" in readme
    assert "AUTO_SUSPEND = 60" in readme
    assert "ALTER WAREHOUSE FINSIGNAL_DEV_WH SUSPEND" in readme
