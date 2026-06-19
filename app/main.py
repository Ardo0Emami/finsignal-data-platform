from __future__ import annotations

from fastapi import FastAPI

from app.api.v1.assets import router as assets_router

app = FastAPI(
    title="FinSignal Data Platform",
    description=(
        "Market intelligence data platform for regime detection, signal validation, "
        "backtesting, and explainable financial analytics."
    ),
    version="0.1.0",
)

app.include_router(assets_router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "finsignal-api"}
