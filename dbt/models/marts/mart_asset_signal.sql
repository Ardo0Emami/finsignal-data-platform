select
    classifications.symbol,
    classifications.price_date,
    classifications.price_timestamp,
    definitions.signal_code,
    definitions.signal_version,
    definitions.signal_name,
    classifications.signal_label,
    classifications.signal_explanation,
    definitions.signal_description,
    classifications.regime_label,
    classifications.regime_explanation,
    classifications.close_price,
    classifications.previous_close_price,
    classifications.daily_return,
    classifications.close_price_3d_moving_avg,
    classifications.daily_return_3d_volatility,
    classifications.close_vs_3d_moving_avg,
    classifications.adjusted_close_price,
    classifications.volume,
    classifications.provider_name,
    classifications.dataset_name,
    classifications.ingestion_run_id,
    classifications.raw_path,
    classifications.ingested_at
from {{ ref('int_asset_signal_classifications') }} as classifications
cross join {{ ref('signal_definitions') }} as definitions
where definitions.is_active = true
  and definitions.signal_code = 'momentum_regime_v1'
qualify row_number() over (
    partition by classifications.symbol
    order by classifications.price_timestamp desc, classifications.ingested_at desc
) = 1
