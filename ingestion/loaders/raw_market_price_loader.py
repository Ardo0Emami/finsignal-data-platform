from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class RawMarketPriceRow:
    provider_name: str
    dataset_name: str
    symbol: str
    price_timestamp: str
    open_price: float | None
    high_price: float | None
    low_price: float | None
    close_price: float
    adjusted_close_price: float | None
    volume: float | None
    raw_path: str
    ingestion_run_id: str
    ingested_at: str
    raw_record: dict[str, Any]


def load_raw_market_price_rows_from_file(raw_file_path: str | Path) -> list[RawMarketPriceRow]:
    raw_file = Path(raw_file_path)
    payload = json.loads(raw_file.read_text(encoding="utf-8"))

    provider_name = _required_string(payload, "provider")
    dataset_name = _required_string(payload, "dataset")
    symbol = _required_string(payload, "symbol")
    ingestion_run_id = _required_string(payload, "ingestion_run_id")
    ingested_at = _required_string(payload, "ingested_at")

    records = payload.get("records")
    if not isinstance(records, list):
        raise ValueError("Raw market price payload must contain a records list.")

    rows: list[RawMarketPriceRow] = []

    for record in records:
        if not isinstance(record, dict):
            raise ValueError("Each raw market price record must be an object.")

        rows.append(
            RawMarketPriceRow(
                provider_name=provider_name,
                dataset_name=dataset_name,
                symbol=symbol,
                price_timestamp=_required_string(record, "price_timestamp"),
                open_price=_optional_float(record, "open_price"),
                high_price=_optional_float(record, "high_price"),
                low_price=_optional_float(record, "low_price"),
                close_price=_required_float(record, "close_price"),
                adjusted_close_price=_optional_float(record, "adjusted_close_price"),
                volume=_optional_float(record, "volume"),
                raw_path=str(raw_file),
                ingestion_run_id=ingestion_run_id,
                ingested_at=ingested_at,
                raw_record=_raw_record(record),
            )
        )

    return rows


def _raw_record(record: dict[str, Any]) -> dict[str, Any]:
    raw_record = record.get("raw_record")

    if isinstance(raw_record, dict):
        return raw_record

    return record


def _required_string(payload: dict[str, Any], key: str) -> str:
    value = payload.get(key)

    if not isinstance(value, str) or not value:
        raise ValueError(f"Missing required string field: {key}")

    return value


def _required_float(payload: dict[str, Any], key: str) -> float:
    value = payload.get(key)

    if value is None:
        raise ValueError(f"Missing required numeric field: {key}")

    if not isinstance(value, int | float):
        raise ValueError(f"Field must be numeric: {key}")

    return float(value)


def _optional_float(payload: dict[str, Any], key: str) -> float | None:
    value = payload.get(key)

    if value is None:
        return None

    if not isinstance(value, int | float):
        raise ValueError(f"Field must be numeric when provided: {key}")

    return float(value)
