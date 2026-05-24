from ingestion.providers.static_sample import StaticSampleProvider


def test_fetch_daily_prices_returns_records_for_symbol() -> None:
    provider = StaticSampleProvider("data_samples/market_prices_sample.json")

    records = provider.fetch_daily_prices("BTCUSD")

    assert len(records) == 3
    assert records[0].symbol == "BTCUSD"
    assert records[0].provider_name == "static_sample"
    assert records[-1].close_price == 69950.0


def test_fetch_latest_price_returns_most_recent_record() -> None:
    provider = StaticSampleProvider("data_samples/market_prices_sample.json")

    latest = provider.fetch_latest_price("QQQ")

    assert latest.symbol == "QQQ"
    assert latest.price_timestamp == "2026-05-22T00:00:00Z"
    assert latest.close_price == 453.1
