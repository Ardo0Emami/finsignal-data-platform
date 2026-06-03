with returns as (

    select
        provider_name,
        dataset_name,
        symbol,
        price_timestamp,
        price_date,
        close_price,
        previous_close_price,
        daily_return,
        adjusted_close_price,
        volume,
        raw_path,
        ingestion_run_id,
        ingested_at
    from {{ ref('int_market_price_returns') }}

),

features as (

    select
        *,
        avg(close_price) over (
            partition by provider_name, dataset_name, symbol
            order by price_timestamp
            rows between 2 preceding and current row
        ) as close_price_3d_moving_avg,

        stddev_samp(daily_return) over (
            partition by provider_name, dataset_name, symbol
            order by price_timestamp
            rows between 2 preceding and current row
        ) as daily_return_3d_volatility

    from returns

)

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
    case
        when close_price_3d_moving_avg is null then null
        when close_price_3d_moving_avg = 0 then null
        else close_price / close_price_3d_moving_avg - 1
    end as close_vs_3d_moving_avg,
    adjusted_close_price,
    volume,
    raw_path,
    ingestion_run_id,
    ingested_at
from features
