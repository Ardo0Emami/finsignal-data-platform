from __future__ import annotations

from pathlib import Path


def test_product_api_contract_documents_core_endpoints() -> None:
    content = Path("docs/contracts/product_api.md").read_text(encoding="utf-8")

    assert "GET /api/v1/assets/{symbol}/snapshot" in content
    assert "GET /api/v1/assets/{symbol}/regime" in content
    assert "GET /api/v1/assets/{symbol}/signals" in content
    assert "POST /api/v1/ask" in content


def test_product_api_contract_documents_mart_dependencies() -> None:
    content = Path("docs/contracts/product_api.md").read_text(encoding="utf-8")

    assert "MARTS.MART_CURRENT_ASSET_SNAPSHOT" in content
    assert "MARTS.MART_ASSET_REGIME" in content
    assert "MARTS.MART_ASSET_SIGNAL" in content


def test_product_api_contract_documents_governed_ask_behavior() -> None:
    content = Path("docs/contracts/product_api.md").read_text(encoding="utf-8")

    assert "evidence-based" in content
    assert "does not generate a free-form answer" in content
    assert "signal explanation" in content
    assert "regime explanation" in content


def test_product_api_runbook_documents_local_smoke_test() -> None:
    content = Path("docs/operations/product_api_runbook.md").read_text(encoding="utf-8")

    assert "uvicorn app.main:app --reload --port 8000" in content
    assert "curl http://127.0.0.1:8000/health" in content
    assert "curl -X POST http://127.0.0.1:8000/api/v1/ask" in content
    assert "source .env" in content
