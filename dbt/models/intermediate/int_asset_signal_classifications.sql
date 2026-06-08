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

    case
        when close_vs_3d_moving_avg > 0 and daily_return > 0
            then 'bullish_momentum'
        when close_vs_3d_moving_avg < 0 and daily_return < 0
            then 'bearish_momentum'
        else 'neutral'
    end as regime_label,

    case
        when close_vs_3d_moving_avg > 0 and daily_return > 0
            then 'Price is above its 3-day moving average and daily return is positive.'
        when close_vs_3d_moving_avg < 0 and daily_return < 0
            then 'Price is below its 3-day moving average and daily return is negative.'
        else 'Momentum signals are mixed or insufficient.'
    end as regime_explanation,

    case
        when close_vs_3d_moving_avg > 0 and daily_return > 0
            then 'buy_watch'
        when close_vs_3d_moving_avg < 0 and daily_return < 0
            then 'risk_off'
        else 'hold_neutral'
    end as signal_label,

    case
        when close_vs_3d_moving_avg > 0 and daily_return > 0
            then 'Asset shows positive momentum versus its short-term trend.'
        when close_vs_3d_moving_avg < 0 and daily_return < 0
            then 'Asset shows negative momentum versus its short-term trend.'
        else 'Asset does not show a strong directional momentum signal.'
    end as signal_explanation,

    adjusted_close_price,
    volume,
    raw_path,
    ingestion_run_id,
    ingested_at
from {{ ref('int_market_technical_features') }}
