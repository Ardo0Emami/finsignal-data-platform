from app.core.config import Settings


def test_settings_defaults_to_local_writer() -> None:
    settings = Settings()

    assert settings.raw_writer == "local"
    assert settings.raw_bucket is None
    assert settings.sample_data_path == "data_samples/market_prices_sample.json"
    assert settings.local_raw_base_path == "data"


def test_settings_can_be_configured_directly() -> None:
    settings = Settings(
        raw_writer="s3",
        raw_bucket="finsignal-dev-raw",
        sample_data_path="custom/sample.json",
        local_raw_base_path="custom-data",
    )

    assert settings.raw_writer == "s3"
    assert settings.raw_bucket == "finsignal-dev-raw"
    assert settings.sample_data_path == "custom/sample.json"
    assert settings.local_raw_base_path == "custom-data"
