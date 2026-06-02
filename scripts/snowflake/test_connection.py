from __future__ import annotations

from typing import Protocol

from app.core.config import Settings
from ingestion.loaders.snowflake_market_price_loader import create_snowflake_connection


class QueryCursor(Protocol):
    def execute(self, command: str) -> object:
        ...

    def fetchone(self) -> tuple[object, ...] | None:
        ...

    def close(self) -> None:
        ...


class QueryConnection(Protocol):
    def cursor(self) -> QueryCursor:
        ...

    def close(self) -> None:
        ...


def check_snowflake_connection(connection: QueryConnection) -> dict[str, object]:
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT
                CURRENT_ACCOUNT(),
                CURRENT_USER(),
                CURRENT_ROLE(),
                CURRENT_WAREHOUSE(),
                CURRENT_DATABASE(),
                CURRENT_SCHEMA()
            """
        )
        row = cursor.fetchone()

        if row is None:
            raise RuntimeError("Snowflake connection test returned no rows.")

        return {
            "account": row[0],
            "user": row[1],
            "role": row[2],
            "warehouse": row[3],
            "database": row[4],
            "schema": row[5],
        }

    finally:
        cursor.close()


def main() -> None:
    settings = Settings()
    connection = create_snowflake_connection(settings)

    try:
        result = check_snowflake_connection(connection)
        print({"status": "succeeded", **result})
    finally:
        connection.close()


if __name__ == "__main__":
    main()
