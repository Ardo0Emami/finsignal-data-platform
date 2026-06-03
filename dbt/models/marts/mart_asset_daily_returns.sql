with returns as (

    select
        provider_name,
        dataset_name,
        symbol,
        price_date,
        price_timestamp,
        close_price,
        previous_close_price,
        daily_return,
        adjusted_close_price,
        volume,
        ingestion_run_id,
        raw_path,
        ingested_at
    from {{ ref('int_market_price_returns') }}

)

select
    symbol,
    price_date,
    price_timestamp,
    close_price,
    previous_close_price,
    daily_return,
    adjusted_close_price,
    volume,
    provider_name,
    dataset_name,
    ingestion_run_id,
    raw_path,
    ingested_at
from returns
