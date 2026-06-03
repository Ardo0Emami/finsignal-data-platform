with features as (

    select
        provider_name,
        dataset_name,
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
        ingestion_run_id,
        raw_path,
        ingested_at
    from {{ ref('int_market_technical_features') }}

),

signal_definitions as (

    select
        signal_code,
        signal_version,
        signal_name,
        signal_description
    from {{ ref('signal_definitions') }}
    where is_active = true
      and signal_code = 'momentum_regime_v1'

),

classified as (

    select
        features.*,
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
        end as regime_explanation
    from features

),

signals as (

    select
        classified.*,
        signal_definitions.signal_code,
        signal_definitions.signal_version,
        signal_definitions.signal_name,
        signal_definitions.signal_description,

        case
            when classified.regime_label = 'bullish_momentum' then 'buy_watch'
            when classified.regime_label = 'bearish_momentum' then 'risk_off'
            else 'hold_neutral'
        end as signal_label,

        case
            when classified.regime_label = 'bullish_momentum'
                then 'Asset shows positive momentum versus its short-term trend.'
            when classified.regime_label = 'bearish_momentum'
                then 'Asset shows negative momentum versus its short-term trend.'
            else 'Asset does not show a strong directional momentum signal.'
        end as signal_explanation
    from classified
    cross join signal_definitions

)

select
    symbol,
    price_date,
    price_timestamp,
    signal_code,
    signal_version,
    signal_name,
    signal_label,
    signal_explanation,
    signal_description,
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
from signals
