from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    raw_writer: str = "local"
    market_data_provider: str = "static_sample"
    asset_symbols: str = "BTCUSD,QQQ"
    raw_bucket: str | None = None
    sample_data_path: str = "data_samples/market_prices_sample.json"
    local_raw_base_path: str = "data"

    snowflake_account: str | None = None
    snowflake_user: str | None = None
    snowflake_password: str | None = None
    snowflake_authenticator: str = "snowflake"
    snowflake_role: str | None = None
    snowflake_warehouse: str | None = None
    snowflake_database: str = "FINSIGNAL_DW"
    snowflake_schema: str = "RAW"

    model_config = SettingsConfigDict(
        env_prefix="FINSIGNAL_",
        env_file=".env",
        extra="ignore",
    )
