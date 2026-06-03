with features as (

    select
        provider_name,
        dataset_name,
        symbol,
        price_timestamp,
        price_date,
        close_price,
        previous_close_price,
        daily_return,
        close_price_3d_moving_avg,
        daily_return_3d_volatility,
        close_vs_3d_moving_avg,
        adjusted_close_price,
        volume,
        ingestion_run_id,
        raw_path,
        ingested_at
    from {{ ref('int_market_technical_features') }}

),

ranked as (

    select
        *,
        row_number() over (
            partition by symbol
            order by price_timestamp desc, ingested_at desc
        ) as row_number
    from features

)

select
    symbol,
    price_date,
    price_timestamp,
    close_price,
    previous_close_price,
    daily_return,
    close_price_3d_moving_avg,
    daily_return_3d_volatility,
    close_vs_3d_moving_avg,
    adjusted_close_price,
    volume,
    provider_name,
    dataset_name,
    ingestion_run_id,
    raw_path,
    ingested_at
from ranked
where row_number = 1
