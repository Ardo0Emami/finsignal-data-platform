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
from {{ ref('int_asset_signal_classifications') }}
qualify row_number() over (
    partition by symbol
    order by price_timestamp desc, ingested_at desc
) = 1
