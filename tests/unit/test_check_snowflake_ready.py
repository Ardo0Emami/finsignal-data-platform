from __future__ import annotations

from app.core.config import Settings
from scripts.snowflake.check_snowflake_ready import check_snowflake_ready


def test_check_snowflake_ready_reports_missing_settings() -> None:
    result = check_snowflake_ready(
        Settings(
            snowflake_account=None,
            snowflake_user=None,
            snowflake_password=None,
            snowflake_warehouse=None,
        )
    )

    assert result["ready"] is False
    assert result["missing_settings"] == [
        "snowflake_account",
        "snowflake_user",
        "snowflake_password",
        "snowflake_warehouse",
    ]


def test_check_snowflake_ready_reports_ready_when_required_settings_exist() -> None:
    result = check_snowflake_ready(
        Settings(
            snowflake_account="example.ca-central-1.aws",
            snowflake_user="FINSIGNAL_USER",
            snowflake_password="secret",
            snowflake_warehouse="FINSIGNAL_DEV_WH",
        )
    )

    assert result["ready"] is True
    assert result["missing_settings"] == []
    assert result["database"] == "FINSIGNAL_DW"
    assert result["schema"] == "RAW"
    assert result["warehouse"] == "FINSIGNAL_DEV_WH"
