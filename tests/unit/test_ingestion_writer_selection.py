import pytest

from ingestion.writers.local_writer import LocalRawWriter
from ingestion.writers.s3_writer import S3RawWriter
from scripts.local.run_local_market_ingestion import build_writer


def test_build_writer_defaults_to_local(monkeypatch) -> None:
    monkeypatch.delenv("FINSIGNAL_RAW_WRITER", raising=False)

    writer = build_writer()

    assert isinstance(writer, LocalRawWriter)


def test_build_writer_uses_local_when_configured(monkeypatch) -> None:
    monkeypatch.setenv("FINSIGNAL_RAW_WRITER", "local")

    writer = build_writer()

    assert isinstance(writer, LocalRawWriter)


def test_build_writer_uses_s3_when_bucket_is_configured(monkeypatch) -> None:
    monkeypatch.setenv("FINSIGNAL_RAW_WRITER", "s3")
    monkeypatch.setenv("FINSIGNAL_RAW_BUCKET", "finsignal-dev-raw")

    writer = build_writer()

    assert isinstance(writer, S3RawWriter)
    assert writer.bucket_name == "finsignal-dev-raw"


def test_build_writer_rejects_s3_without_bucket(monkeypatch) -> None:
    monkeypatch.setenv("FINSIGNAL_RAW_WRITER", "s3")
    monkeypatch.delenv("FINSIGNAL_RAW_BUCKET", raising=False)

    with pytest.raises(ValueError, match="FINSIGNAL_RAW_BUCKET must be set"):
        build_writer()


def test_build_writer_rejects_unknown_writer(monkeypatch) -> None:
    monkeypatch.setenv("FINSIGNAL_RAW_WRITER", "unknown")

    with pytest.raises(ValueError, match="Unsupported FINSIGNAL_RAW_WRITER"):
        build_writer()
