from __future__ import annotations

from pathlib import Path
from typing import Any

from scripts.snowflake.apply_schema import apply_schema, split_sql_statements


class FakeCursor:
    def __init__(self) -> None:
        self.executed_statements: list[str] = []
        self.closed = False

    def execute(self, command: str) -> None:
        self.executed_statements.append(command)

    def close(self) -> None:
        self.closed = True


class FakeConnection:
    def __init__(self) -> None:
        self.cursor_instance = FakeCursor()
        self.committed = False
        self.closed = False

    def cursor(self) -> FakeCursor:
        return self.cursor_instance

    def commit(self) -> None:
        self.committed = True

    def close(self) -> None:
        self.closed = True


def test_split_sql_statements_ignores_empty_statements() -> None:
    sql = """
    CREATE DATABASE IF NOT EXISTS FINSIGNAL_DW;

    CREATE SCHEMA IF NOT EXISTS FINSIGNAL_DW.RAW;

    ;
    """

    statements = split_sql_statements(sql)

    assert statements == [
        "CREATE DATABASE IF NOT EXISTS FINSIGNAL_DW",
        "CREATE SCHEMA IF NOT EXISTS FINSIGNAL_DW.RAW",
    ]


def test_apply_schema_executes_sql_scripts_in_order(tmp_path: Path) -> None:
    first_script = tmp_path / "001.sql"
    second_script = tmp_path / "002.sql"

    first_script.write_text(
        """
        CREATE DATABASE IF NOT EXISTS FINSIGNAL_DW;
        CREATE SCHEMA IF NOT EXISTS FINSIGNAL_DW.RAW;
        """,
        encoding="utf-8",
    )

    second_script.write_text(
        """
        CREATE TABLE IF NOT EXISTS FINSIGNAL_DW.RAW.RAW_MARKET_PRICES (
            symbol STRING
        );
        """,
        encoding="utf-8",
    )

    connection = FakeConnection()

    statement_count = apply_schema(
        connection=connection,
        script_paths=[first_script, second_script],
    )

    assert statement_count == 3
    assert connection.committed is True
    assert connection.cursor_instance.closed is True
    assert connection.cursor_instance.executed_statements == [
        "CREATE DATABASE IF NOT EXISTS FINSIGNAL_DW",
        "CREATE SCHEMA IF NOT EXISTS FINSIGNAL_DW.RAW",
        (
            "CREATE TABLE IF NOT EXISTS FINSIGNAL_DW.RAW.RAW_MARKET_PRICES "
            "(\n            symbol STRING\n        )"
        ),
    ]


def test_apply_schema_closes_cursor_when_execution_fails(tmp_path: Path) -> None:
    script = tmp_path / "001.sql"
    script.write_text("CREATE DATABASE broken;", encoding="utf-8")

    class FailingCursor(FakeCursor):
        def execute(self, command: str) -> Any:
            raise RuntimeError("snowflake failed")

    class FailingConnection(FakeConnection):
        def __init__(self) -> None:
            self.cursor_instance = FailingCursor()
            self.committed = False
            self.closed = False

    connection = FailingConnection()

    try:
        apply_schema(connection=connection, script_paths=[script])
    except RuntimeError as error:
        assert str(error) == "snowflake failed"

    assert connection.committed is False
    assert connection.cursor_instance.closed is True
