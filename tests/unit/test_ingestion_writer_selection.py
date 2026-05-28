import pytest

from app.core.config import Settings
from ingestion.writers.local_writer import LocalRawWriter
from ingestion.writers.s3_writer import S3RawWriter
from scripts.local.run_local_market_ingestion import build_writer


def test_build_writer_defaults_to_local() -> None:
    settings = Settings(raw_writer="local")

    writer = build_writer(settings)

    assert isinstance(writer, LocalRawWriter)


def test_build_writer_uses_local_when_configured() -> None:
    settings = Settings(raw_writer="local", local_raw_base_path="data")

    writer = build_writer(settings)

    assert isinstance(writer, LocalRawWriter)


def test_build_writer_uses_s3_when_bucket_is_configured() -> None:
    settings = Settings(raw_writer="s3", raw_bucket="finsignal-dev-raw")

    writer = build_writer(settings)

    assert isinstance(writer, S3RawWriter)
    assert writer.bucket_name == "finsignal-dev-raw"


def test_build_writer_rejects_s3_without_bucket() -> None:
    settings = Settings(raw_writer="s3", raw_bucket=None)

    with pytest.raises(ValueError, match="FINSIGNAL_RAW_BUCKET must be set"):
        build_writer(settings)


def test_build_writer_rejects_unknown_writer() -> None:
    settings = Settings(raw_writer="unknown")

    with pytest.raises(ValueError, match="Unsupported FINSIGNAL_RAW_WRITER"):
        build_writer(settings)
