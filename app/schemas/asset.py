from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel


class AssetSnapshotResponse(BaseModel):
    symbol: str
    price_date: date
    price_timestamp: datetime
    close_price: float
    ingestion_run_id: str
    raw_path: str


class AssetSignalResponse(BaseModel):
    symbol: str
    price_date: date
    signal_code: str
    signal_version: int
    signal_label: str
    signal_explanation: str
    regime_label: str
    ingestion_run_id: str
    raw_path: str


class AssetRegimeResponse(BaseModel):
    symbol: str
    price_date: date
    price_timestamp: datetime
    close_price: float
    regime_label: str
    regime_explanation: str
    ingestion_run_id: str
    raw_path: str
