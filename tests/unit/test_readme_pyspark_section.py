from __future__ import annotations

from pathlib import Path


def test_readme_documents_pyspark_feature_processing_role() -> None:
    readme = Path("README.md").read_text(encoding="utf-8")

    assert "## PySpark Feature Processing" in readme
    assert "Spark does not replace Snowflake or dbt" in readme
    assert "file-based feature processing" in readme
    assert "staged Parquet datasets" in readme


def test_readme_documents_spark_jobs_and_local_commands() -> None:
    readme = Path("README.md").read_text(encoding="utf-8")

    assert "spark/jobs/export_market_prices_to_parquet.py" in readme
    assert "spark/jobs/build_asset_feature_parquet.py" in readme
    assert "python -m spark.jobs.export_market_prices_to_parquet" in readme
    assert "python -m spark.jobs.build_asset_feature_parquet" in readme
    assert "data/staged/market_prices" in readme
    assert "data/features/asset_features" in readme


def test_readme_documents_spark_features_lineage_and_cost_guardrail() -> None:
    readme = Path("README.md").read_text(encoding="utf-8")

    assert "previous_close_price" in readme
    assert "daily_return" in readme
    assert "close_price_3d_moving_avg" in readme
    assert "daily_return_3d_volatility" in readme
    assert "close_vs_3d_moving_avg" in readme
    assert "raw_path" in readme
    assert "ingestion_run_id" in readme
    assert "ingested_at" in readme
    assert "local[*]" in readme
    assert "does not create cloud compute cost" in readme
