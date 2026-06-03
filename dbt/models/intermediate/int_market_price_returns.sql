with market_prices as (

    select
        provider_name,
        dataset_name,
        symbol,
        price_timestamp,
        price_date,
        close_price,
        adjusted_close_price,
        volume,
        raw_path,
        ingestion_run_id,
        ingested_at
    from {{ ref('stg_market_prices') }}

),

with_previous_price as (

    select
        *,
        lag(close_price) over (
            partition by provider_name, dataset_name, symbol
            order by price_timestamp
        ) as previous_close_price
    from market_prices

)

select
    provider_name,
    dataset_name,
    symbol,
    price_timestamp,
    price_date,
    close_price,
    previous_close_price,
    case
        when previous_close_price is null then null
        when previous_close_price = 0 then null
        else (close_price - previous_close_price) / previous_close_price
    end as daily_return,
    adjusted_close_price,
    volume,
    raw_path,
    ingestion_run_id,
    ingested_at
from with_previous_price
