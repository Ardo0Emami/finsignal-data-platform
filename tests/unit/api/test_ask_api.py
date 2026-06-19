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
                "signal_code": "momentum_regime_v1",
                "signal_version": 1,
                "signal_label": "buy_watch",
                "signal_explanation": "Asset shows positive momentum versus its short-term trend.",
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


def test_ask_endpoint_returns_governed_signal_explanation() -> None:
    app.dependency_overrides[get_asset_read_service] = override_asset_read_service
    client = TestClient(app)

    try:
        response = client.post(
            "/api/v1/ask",
            json={"symbol": "qqq", "question": "Why is QQQ buy_watch?"},
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200

    payload = response.json()
    assert payload["symbol"] == "QQQ"
    assert "buy_watch" in payload["answer"]
    assert "bullish_momentum" in payload["answer"]
    assert payload["evidence"]


def test_ask_endpoint_returns_404_when_symbol_has_no_context() -> None:
    app.dependency_overrides[get_asset_read_service] = override_asset_read_service
    client = TestClient(app)

    try:
        response = client.post(
            "/api/v1/ask",
            json={"symbol": "missing", "question": "Why?"},
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 404
