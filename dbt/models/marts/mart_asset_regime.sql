with current_snapshot as (

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
    from {{ ref('mart_current_asset_snapshot') }}

),

classified as (

    select
        *,
        case
            when close_vs_3d_moving_avg > 0 and daily_return > 0
                then 'bullish_momentum'
            when close_vs_3d_moving_avg < 0 and daily_return < 0
                then 'bearish_momentum'
            else 'neutral'
        end as regime_label,

        case
            when close_vs_3d_moving_avg > 0 and daily_return > 0
                then 'Price is above its 3-day moving average and latest daily return is positive.'
            when close_vs_3d_moving_avg < 0 and daily_return < 0
                then 'Price is below its 3-day moving average and latest daily return is negative.'
            else 'Momentum signals are mixed or insufficient.'
        end as regime_explanation

    from current_snapshot

)

select
    symbol,
    price_date,
    price_timestamp,
    regime_label,
    regime_explanation,
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
from classified
