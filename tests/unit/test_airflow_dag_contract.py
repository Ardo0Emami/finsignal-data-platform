from __future__ import annotations

from pathlib import Path


def test_market_daily_ingestion_dag_exists_and_uses_reusable_entrypoint() -> None:
    dag_path = Path("airflow/dags/market_daily_ingestion_dag.py")

    assert dag_path.exists()

    dag_source = dag_path.read_text(encoding="utf-8")

    assert 'dag_id="market_daily_ingestion"' in dag_source
    assert "from scripts.ingestion.run_market_ingestion import run_full_pipeline" in dag_source
    assert "return run_full_pipeline()" in dag_source
