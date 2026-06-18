from __future__ import annotations

from pathlib import Path


def test_spark_feature_job_reads_and_writes_parquet() -> None:
    script = Path("spark/jobs/build_asset_feature_parquet.py").read_text(
        encoding="utf-8"
    )

    assert "spark.read.parquet" in script
    assert '.write.mode("overwrite").parquet' in script
    assert "data/staged/market_prices" in script
    assert "data/features/asset_features" in script


def test_spark_feature_job_calculates_expected_features() -> None:
    script = Path("spark/jobs/build_asset_feature_parquet.py").read_text(
        encoding="utf-8"
    )

    assert "previous_close_price" in script
    assert "daily_return" in script
    assert "close_price_3d_moving_avg" in script
    assert "daily_return_3d_volatility" in script
    assert "close_vs_3d_moving_avg" in script
    assert "lag(" in script
    assert "avg(" in script
    assert "stddev_samp(" in script


def test_spark_feature_job_partitions_windows_by_asset_grain() -> None:
    script = Path("spark/jobs/build_asset_feature_parquet.py").read_text(
        encoding="utf-8"
    )

    assert '"provider_name"' in script
    assert '"dataset_name"' in script
    assert '"symbol"' in script
    assert 'orderBy("price_timestamp")' in script
    assert "rowsBetween(-2, 0)" in script
