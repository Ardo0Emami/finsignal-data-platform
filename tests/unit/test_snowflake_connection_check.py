from __future__ import annotations

from typing import Any

from scripts.snowflake.test_connection import check_snowflake_connection


class FakeCursor:
    def __init__(self) -> None:
        self.executed_command: str | None = None
        self.closed = False

    def execute(self, command: str) -> None:
        self.executed_command = command

    def fetchone(self) -> tuple[Any, ...]:
        return (
            "FINSIGNAL_ACCOUNT",
            "FINSIGNAL_USER",
            "FINSIGNAL_ROLE",
            "FINSIGNAL_DEV_WH",
            "FINSIGNAL_DW",
            "RAW",
        )

    def close(self) -> None:
        self.closed = True


class FakeConnection:
    def __init__(self) -> None:
        self.cursor_instance = FakeCursor()

    def cursor(self) -> FakeCursor:
        return self.cursor_instance

    def close(self) -> None:
        pass


def test_snowflake_connection_returns_current_context() -> None:
    connection = FakeConnection()

    result = check_snowflake_connection(connection)

    assert result == {
        "account": "FINSIGNAL_ACCOUNT",
        "user": "FINSIGNAL_USER",
        "role": "FINSIGNAL_ROLE",
        "warehouse": "FINSIGNAL_DEV_WH",
        "database": "FINSIGNAL_DW",
        "schema": "RAW",
    }
    assert "CURRENT_ACCOUNT()" in str(connection.cursor_instance.executed_command)
    assert connection.cursor_instance.closed is True
