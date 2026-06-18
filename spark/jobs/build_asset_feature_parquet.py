from __future__ import annotations

import argparse
import platform
from pathlib import Path

from pyspark.sql import SparkSession, Window
from pyspark.sql.functions import avg, col, lag, stddev_samp


def _is_windows() -> bool:
    return platform.system().lower() == "windows"


def build_asset_feature_parquet(
    *,
    input_path: Path,
    output_path: Path,
    app_name: str = "FinSignalAssetFeatureProcessing",
) -> Path:
    spark = (
        SparkSession.builder.appName(app_name)
        .master("local[*]")
        .config("spark.sql.session.timeZone", "UTC")
        .getOrCreate()
    )

    try:
        prices = spark.read.parquet(str(input_path))

        asset_window = Window.partitionBy(
            "provider_name",
            "dataset_name",
            "symbol",
        ).orderBy("price_timestamp")

        rolling_3_window = asset_window.rowsBetween(-2, 0)

        features = (
            prices.withColumn(
                "previous_close_price",
                lag("close_price").over(asset_window),
            )
            .withColumn(
                "daily_return",
                (col("close_price") - col("previous_close_price"))
                / col("previous_close_price"),
            )
            .withColumn(
                "close_price_3d_moving_avg",
                avg("close_price").over(rolling_3_window),
            )
            .withColumn(
                "daily_return_3d_volatility",
                stddev_samp("daily_return").over(rolling_3_window),
            )
            .withColumn(
                "close_vs_3d_moving_avg",
                (col("close_price") / col("close_price_3d_moving_avg")) - 1,
            )
        )

        if _is_windows():
            output_path.mkdir(parents=True, exist_ok=True)
            parquet_file = output_path / "asset_features.parquet"
            features.toPandas().to_parquet(parquet_file, index=False)
            return parquet_file

        features.write.mode("overwrite").parquet(str(output_path))
        return output_path
    finally:
        spark.stop()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build Parquet asset feature dataset using PySpark."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("data/staged/market_prices"),
        help="Input staged market price Parquet dataset.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/features/asset_features"),
        help="Output feature Parquet dataset.",
    )
    args = parser.parse_args()

    path = build_asset_feature_parquet(
        input_path=args.input,
        output_path=args.output,
    )

    print(path)


if __name__ == "__main__":
    main()
