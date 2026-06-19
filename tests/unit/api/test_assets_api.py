from __future__ import annotations

from typing import Any

from fastapi.testclient import TestClient

from app.api.dependencies import get_asset_read_service
from app.main import app


class FakeAssetReadService:
    def get_snapshot(self, symbol: str) -> dict[str, Any] | None:
        if symbol.upper() == "MISSING":
            return None

        return {
            "symbol": symbol.upper(),
            "price_date": "2026-06-01",
            "price_timestamp": "2026-06-01T00:00:00Z",
            "close_price": 123.45,
            "ingestion_run_id": "run-123",
            "raw_path": "s3://example/raw/path/data.json",
        }

    def get_signals(self, symbol: str) -> list[dict[str, Any]]:
        if symbol.upper() == "MISSING":
            return []

        return [
            {
                "symbol": symbol.upper(),
                "price_date": "2026-06-01",
                "signal_code": "MOMENTUM_SIGNAL",
                "signal_version": 1,
                "signal_label": "buy_watch",
                "signal_explanation": "Recent return and trend indicators are positive.",
                "regime_label": "bullish_momentum",
                "ingestion_run_id": "run-123",
                "raw_path": "s3://example/raw/path/data.json",
            }
        ]

    def get_regime(self, symbol: str) -> dict[str, Any] | None:
        if symbol.upper() == "MISSING":
            return None

        return {
            "symbol": symbol.upper(),
            "price_date": "2026-06-01",
            "price_timestamp": "2026-06-01T00:00:00Z",
            "close_price": 123.45,
            "regime_label": "bullish_momentum",
            "regime_explanation": "The asset is trading with positive momentum.",
            "ingestion_run_id": "run-123",
            "raw_path": "s3://example/raw/path/data.json",
        }


def override_asset_read_service() -> FakeAssetReadService:
    return FakeAssetReadService()


def test_health_endpoint_returns_status() -> None:
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "finsignal-api"}


def test_asset_snapshot_endpoint_returns_latest_snapshot() -> None:
    app.dependency_overrides[get_asset_read_service] = override_asset_read_service
    client = TestClient(app)

    try:
        response = client.get("/api/v1/assets/qqq/snapshot")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["symbol"] == "QQQ"
    assert response.json()["close_price"] == 123.45


def test_asset_signals_endpoint_returns_signal_rows() -> None:
    app.dependency_overrides[get_asset_read_service] = override_asset_read_service
    client = TestClient(app)

    try:
        response = client.get("/api/v1/assets/qqq/signals")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()[0]["signal_label"] == "buy_watch"
    assert response.json()[0]["regime_label"] == "bullish_momentum"


def test_asset_regime_endpoint_returns_latest_regime() -> None:
    app.dependency_overrides[get_asset_read_service] = override_asset_read_service
    client = TestClient(app)

    try:
        response = client.get("/api/v1/assets/qqq/regime")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["regime_label"] == "bullish_momentum"


def test_asset_snapshot_endpoint_returns_404_when_missing() -> None:
    app.dependency_overrides[get_asset_read_service] = override_asset_read_service
    client = TestClient(app)

    try:
        response = client.get("/api/v1/assets/missing/snapshot")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 404
