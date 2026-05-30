from __future__ import annotations

from datetime import datetime, timedelta

from airflow.decorators import dag, task

DEFAULT_ARGS = {
    "owner": "finsignal",
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
}


@dag(
    dag_id="market_daily_ingestion",
    start_date=datetime(2026, 5, 1),
    schedule="0 1 * * *",
    catchup=False,
    default_args=DEFAULT_ARGS,
    tags=["finsignal", "market-data", "ingestion"],
)
def market_daily_ingestion_dag() -> None:
    @task
    def run_daily_market_ingestion() -> list[dict[str, object]]:
        from app.core.config import Settings
        from scripts.ingestion.run_market_ingestion import (
            build_ingestion_service,
            parse_asset_symbols,
        )

        settings = Settings()
        service = build_ingestion_service(settings)
        symbols = parse_asset_symbols(settings)

        results = service.run_for_symbols(symbols)

        return [
            {
                "symbol": result.symbol,
                "status": result.status,
                "records_extracted": result.records_extracted,
                "records_written": result.records_written,
                "raw_path": result.raw_path,
                "audit_path": result.audit_path,
                "error_message": result.error_message,
            }
            for result in results
        ]

    run_daily_market_ingestion()


market_daily_ingestion_dag()
