with source_rows as (

    select
        provider_name,
        dataset_name,
        upper(symbol) as symbol,
        price_timestamp,
        open_price,
        high_price,
        low_price,
        close_price,
        adjusted_close_price,
        volume,
        raw_path,
        ingestion_run_id,
        ingested_at,
        raw_record
    from {{ source('raw', 'raw_market_prices') }}

),

deduplicated as (

    select
        *,
        row_number() over (
            partition by provider_name, dataset_name, symbol, price_timestamp
            order by ingested_at desc, ingestion_run_id desc
        ) as row_number
    from source_rows

)

select
    provider_name,
    dataset_name,
    symbol,
    price_timestamp,
    cast(price_timestamp as date) as price_date,
    open_price,
    high_price,
    low_price,
    close_price,
    adjusted_close_price,
    volume,
    raw_path,
    ingestion_run_id,
    ingested_at,
    raw_record
from deduplicated
where row_number = 1
