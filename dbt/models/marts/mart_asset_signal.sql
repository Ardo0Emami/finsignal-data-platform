with regimes as (

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
    from {{ ref('mart_asset_regime') }}

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

signals as (

    select
        regimes.*,
        signal_definitions.signal_code,
        signal_definitions.signal_version,
        signal_definitions.signal_name,
        signal_definitions.signal_description,
        case
            when regimes.regime_label = 'bullish_momentum' then 'buy_watch'
            when regimes.regime_label = 'bearish_momentum' then 'risk_off'
            else 'hold_neutral'
        end as signal_label,
        case
            when regimes.regime_label = 'bullish_momentum'
                then 'Asset shows positive momentum versus its short-term trend.'
            when regimes.regime_label = 'bearish_momentum'
                then 'Asset shows negative momentum versus its short-term trend.'
            else 'Asset does not show a strong directional momentum signal.'
        end as signal_explanation
    from regimes
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
