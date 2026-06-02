SELECT
    provider_name,
    dataset_name,
    symbol,
    COUNT(*) AS row_count,
    MIN(price_timestamp) AS min_price_timestamp,
    MAX(price_timestamp) AS max_price_timestamp
FROM FINSIGNAL_DW.RAW.RAW_MARKET_PRICES
GROUP BY
    provider_name,
    dataset_name,
    symbol
ORDER BY
    symbol;

SELECT
    ingestion_run_id,
    symbol,
    raw_path,
    COUNT(*) AS row_count
FROM FINSIGNAL_DW.RAW.RAW_MARKET_PRICES
GROUP BY
    ingestion_run_id,
    symbol,
    raw_path
ORDER BY
    symbol,
    ingestion_run_id;
