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
        # Keep DAG logic thin. Reusable ingestion workflow lives outside Airflow.
        from scripts.ingestion.run_market_ingestion import run_full_pipeline

        return run_full_pipeline()

    run_daily_market_ingestion()


market_daily_ingestion_dag()
