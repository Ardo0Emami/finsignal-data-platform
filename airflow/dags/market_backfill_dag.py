from __future__ import annotations

from datetime import datetime, timedelta

from airflow.decorators import dag, task

DEFAULT_ARGS = {
    "owner": "finsignal",
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}


@dag(
    dag_id="market_backfill",
    start_date=datetime(2026, 5, 1),
    schedule=None,
    catchup=False,
    default_args=DEFAULT_ARGS,
    tags=["finsignal", "market-data", "backfill"],
)
def market_backfill_dag() -> None:
    @task
    def run_market_backfill() -> list[dict[str, object]]:
        from scripts.ingestion.run_market_ingestion import run_full_pipeline

        return run_full_pipeline()

    run_market_backfill()


market_backfill_dag()
