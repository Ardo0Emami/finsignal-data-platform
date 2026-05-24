from fastapi import FastAPI

app = FastAPI(
    title="FinSignal Data Platform",
    description=(
        "Market intelligence data platform for regime detection, signal validation, "
        "backtesting, and explainable financial analytics."
    ),
    version="0.1.0",
)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "finsignal-api"}
