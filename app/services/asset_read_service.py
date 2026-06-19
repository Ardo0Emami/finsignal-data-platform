from __future__ import annotations

import os
from collections.abc import Callable
from typing import Any, Protocol

from snowflake.connector import connect
from snowflake.connector.connection import SnowflakeConnection


class AssetReadService(Protocol):
    def get_snapshot(self, symbol: str) -> dict[str, Any] | None:
        """Return the latest current-asset snapshot for a symbol."""

    def get_signals(self, symbol: str) -> list[dict[str, Any]]:
        """Return signal rows for a symbol."""

    def get_regime(self, symbol: str) -> dict[str, Any] | None:
        """Return the latest regime row for a symbol."""


def create_snowflake_connection() -> SnowflakeConnection:
    return connect(
        account=os.environ["FINSIGNAL_SNOWFLAKE_ACCOUNT"],
        user=os.environ["FINSIGNAL_SNOWFLAKE_USER"],
        password=os.environ["FINSIGNAL_SNOWFLAKE_PASSWORD"],
        role=os.environ["FINSIGNAL_SNOWFLAKE_ROLE"],
        warehouse=os.environ["FINSIGNAL_SNOWFLAKE_WAREHOUSE"],
        database=os.environ.get("FINSIGNAL_SNOWFLAKE_DATABASE", "FINSIGNAL_DW"),
    )


class SnowflakeAssetReadService:
    def __init__(
        self,
        connection_factory: Callable[[], SnowflakeConnection] = create_snowflake_connection,
    ) -> None:
        self._connection_factory = connection_factory

    def get_snapshot(self, symbol: str) -> dict[str, Any] | None:
        query = """
            select
                symbol,
                price_date,
                price_timestamp,
                close_price,
                ingestion_run_id,
                raw_path
            from MARTS.MART_CURRENT_ASSET_SNAPSHOT
            where upper(symbol) = upper(%s)
            qualify row_number() over (
                partition by symbol
                order by price_date desc, price_timestamp desc
            ) = 1
        """
        return self._fetch_one(query, (symbol,))

    def get_signals(self, symbol: str) -> list[dict[str, Any]]:
        query = """
            select
                symbol,
                price_date,
                signal_code,
                signal_version,
                signal_label,
                signal_explanation,
                regime_label,
                ingestion_run_id,
                raw_path
            from MARTS.MART_ASSET_SIGNAL
            where upper(symbol) = upper(%s)
            order by price_date desc, signal_code, signal_version
        """
        return self._fetch_all(query, (symbol,))

    def get_regime(self, symbol: str) -> dict[str, Any] | None:
        query = """
            select
                symbol,
                price_date,
                price_timestamp,
                close_price,
                regime_label,
                regime_explanation,
                ingestion_run_id,
                raw_path
            from MARTS.MART_ASSET_REGIME
            where upper(symbol) = upper(%s)
            qualify row_number() over (
                partition by symbol
                order by price_date desc, price_timestamp desc
            ) = 1
        """
        return self._fetch_one(query, (symbol,))

    def _fetch_one(self, query: str, params: tuple[Any, ...]) -> dict[str, Any] | None:
        rows = self._fetch_all(query, params)
        if not rows:
            return None
        return rows[0]

    def _fetch_all(self, query: str, params: tuple[Any, ...]) -> list[dict[str, Any]]:
        connection = self._connection_factory()

        try:
            cursor = connection.cursor()
            cursor.execute(query, params)

            column_names = [column[0].lower() for column in cursor.description]
            rows = cursor.fetchall()

            return [dict(zip(column_names, row, strict=True)) for row in rows]
        finally:
            connection.close()
