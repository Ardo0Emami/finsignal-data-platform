select
    symbol,
    signal_date,
    signal_code,
    signal_version,
    count(*) as row_count
from {{ ref('fact_backtest_result') }}
group by
    symbol,
    signal_date,
    signal_code,
    signal_version
having count(*) > 1
