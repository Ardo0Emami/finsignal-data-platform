from ingestion.writers.base import RawMarketDataWriter
from ingestion.writers.local_writer import LocalRawWriter
from ingestion.writers.s3_writer import S3RawWriter


def test_local_writer_implements_raw_market_data_writer_contract() -> None:
    writer = LocalRawWriter("data")

    assert isinstance(writer, RawMarketDataWriter)


def test_s3_writer_implements_raw_market_data_writer_contract() -> None:
    writer = S3RawWriter("finsignal-dev-raw")

    assert isinstance(writer, RawMarketDataWriter)
