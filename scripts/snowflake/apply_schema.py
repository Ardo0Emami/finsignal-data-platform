from __future__ import annotations

from pathlib import Path
from typing import Protocol

from app.core.config import Settings
from ingestion.loaders.snowflake_market_price_loader import create_snowflake_connection

DEFAULT_SCHEMA_SCRIPT_PATHS = [
    Path("scripts/snowflake/001_create_database.sql"),
    Path("scripts/snowflake/002_create_raw_tables.sql"),
    Path("scripts/snowflake/003_create_audit_tables.sql"),
]


class SqlCursor(Protocol):
    def execute(self, command: str) -> object:
        ...

    def close(self) -> None:
        ...


class SqlConnection(Protocol):
    def cursor(self) -> SqlCursor:
        ...

    def commit(self) -> None:
        ...

    def close(self) -> None:
        ...


def split_sql_statements(sql: str) -> list[str]:
    statements = []

    for statement in sql.split(";"):
        cleaned_statement = statement.strip()

        if cleaned_statement:
            statements.append(cleaned_statement)

    return statements


def apply_schema(
    connection: SqlConnection,
    script_paths: list[Path] | None = None,
) -> int:
    paths = script_paths or DEFAULT_SCHEMA_SCRIPT_PATHS
    cursor = connection.cursor()
    statement_count = 0

    try:
        for path in paths:
            sql = path.read_text(encoding="utf-8")
            statements = split_sql_statements(sql)

            for statement in statements:
                cursor.execute(statement)
                statement_count += 1

        connection.commit()
        return statement_count
    finally:
        cursor.close()


def main() -> None:
    settings = Settings()
    connection = create_snowflake_connection(settings)

    try:
        statement_count = apply_schema(connection)
        print({"status": "succeeded", "statements_executed": statement_count})
    finally:
        connection.close()


if __name__ == "__main__":
    main()
