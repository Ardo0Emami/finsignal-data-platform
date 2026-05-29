from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    raw_writer: str = "local"
    market_data_provider: str = "static_sample"
    raw_bucket: str | None = None
    sample_data_path: str = "data_samples/market_prices_sample.json"
    local_raw_base_path: str = "data"

    model_config = SettingsConfigDict(
        env_prefix="FINSIGNAL_",
        env_file=".env",
        extra="ignore",
    )
