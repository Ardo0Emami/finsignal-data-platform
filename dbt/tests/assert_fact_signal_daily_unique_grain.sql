select
    symbol,
    price_date,
    signal_code,
    signal_version,
    count(*) as row_count
from {{ ref('fact_signal_daily') }}
group by
    symbol,
    price_date,
    signal_code,
    signal_version
having count(*) > 1
