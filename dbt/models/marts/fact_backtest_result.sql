with signals as (

    select
        symbol,
        price_date,
        price_timestamp,
        signal_code,
        signal_version,
        signal_label,
        regime_label,
        close_price as signal_close_price,
        ingestion_run_id,
        raw_path,
        ingested_at
    from {{ ref('fact_signal_daily') }}

),

prices as (

    select
        symbol,
        price_date,
        close_price
    from {{ ref('mart_asset_daily_returns') }}

),

backtest as (

    select
        signals.symbol,
        signals.price_date as signal_date,
        signals.price_timestamp,
        signals.signal_code,
        signals.signal_version,
        signals.signal_label,
        signals.regime_label,
        signals.signal_close_price,

        price_1d.close_price as close_price_1d,
        case
            when price_1d.close_price is null then null
            when signals.signal_close_price = 0 then null
            else (price_1d.close_price - signals.signal_close_price) / signals.signal_close_price
        end as forward_return_1d,

        price_3d.close_price as close_price_3d,
        case
            when price_3d.close_price is null then null
            when signals.signal_close_price = 0 then null
            else (price_3d.close_price - signals.signal_close_price) / signals.signal_close_price
        end as forward_return_3d,

        price_7d.close_price as close_price_7d,
        case
            when price_7d.close_price is null then null
            when signals.signal_close_price = 0 then null
            else (price_7d.close_price - signals.signal_close_price) / signals.signal_close_price
        end as forward_return_7d,

        signals.ingestion_run_id,
        signals.raw_path,
        signals.ingested_at

    from signals

    left join prices as price_1d
        on signals.symbol = price_1d.symbol
        and price_1d.price_date = dateadd(day, 1, signals.price_date)

    left join prices as price_3d
        on signals.symbol = price_3d.symbol
        and price_3d.price_date = dateadd(day, 3, signals.price_date)

    left join prices as price_7d
        on signals.symbol = price_7d.symbol
        and price_7d.price_date = dateadd(day, 7, signals.price_date)

)

select
    symbol,
    signal_date,
    price_timestamp,
    signal_code,
    signal_version,
    signal_label,
    regime_label,
    signal_close_price,
    close_price_1d,
    forward_return_1d,
    close_price_3d,
    forward_return_3d,
    close_price_7d,
    forward_return_7d,
    ingestion_run_id,
    raw_path,
    ingested_at
from backtest
