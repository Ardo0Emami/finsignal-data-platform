CREATE TABLE IF NOT EXISTS FINSIGNAL_DW.RAW.RAW_MARKET_PRICES (
    provider_name STRING NOT NULL,
    dataset_name STRING NOT NULL,
    symbol STRING NOT NULL,
    price_timestamp TIMESTAMP_NTZ NOT NULL,
    open_price FLOAT,
    high_price FLOAT,
    low_price FLOAT,
    close_price FLOAT NOT NULL,
    adjusted_close_price FLOAT,
    volume FLOAT,
    raw_path STRING NOT NULL,
    ingestion_run_id STRING NOT NULL,
    ingested_at TIMESTAMP_NTZ NOT NULL,
    raw_record VARIANT NOT NULL
);

CREATE TABLE IF NOT EXISTS FINSIGNAL_DW.RAW.RAW_PRICE_EVENTS (
    event_id STRING NOT NULL,
    event_type STRING NOT NULL,
    provider_name STRING NOT NULL,
    symbol STRING NOT NULL,
    price_timestamp TIMESTAMP_NTZ NOT NULL,
    close_price FLOAT NOT NULL,
    raw_path STRING NOT NULL,
    ingested_at TIMESTAMP_NTZ NOT NULL,
    raw_event VARIANT NOT NULL
);
