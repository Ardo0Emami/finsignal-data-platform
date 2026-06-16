from __future__ import annotations

import zipfile

from scripts.lambda_tools.package_latest_price_ingestion import (
    build_latest_price_ingestion_package,
)


def test_build_latest_price_ingestion_package_contains_lambda_handler(tmp_path) -> None:
    output_path = tmp_path / "latest_price_ingestion.zip"

    package_path = build_latest_price_ingestion_package(output_path)

    assert package_path == output_path
    assert package_path.exists()

    with zipfile.ZipFile(package_path) as archive:
        names = set(archive.namelist())

    assert "ingestion/__init__.py" in names
    assert "ingestion/lambda_handlers/__init__.py" in names
    assert "ingestion/lambda_handlers/latest_price_ingestion.py" in names
    assert "ingestion/streaming/models.py" in names
    assert "ingestion/streaming/kinesis_producer.py" in names
    assert "ingestion/streaming/s3_event_writer.py" in names


def test_lambda_package_does_not_include_python_cache_files(tmp_path) -> None:
    output_path = tmp_path / "latest_price_ingestion.zip"

    build_latest_price_ingestion_package(output_path)

    with zipfile.ZipFile(output_path) as archive:
        names = set(archive.namelist())

    assert not any("__pycache__" in name for name in names)
    assert not any(name.endswith(".pyc") for name in names)
