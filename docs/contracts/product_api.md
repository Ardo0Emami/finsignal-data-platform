# Product API Contract

FinSignal exposes product-facing API endpoints over curated Snowflake marts.

The API does not query raw files directly. It reads from the modeled `MARTS` schema so that users receive governed, tested, and explainable outputs.

## Endpoints

### `GET /health`

Returns service health.

Example response:

    {
      "status": "ok",
      "service": "finsignal-api"
    }

### `GET /api/v1/assets/{symbol}/snapshot`

Returns the latest modeled snapshot for an asset.

Backed by:

    MARTS.MART_CURRENT_ASSET_SNAPSHOT

Key response fields:

- `symbol`
- `price_date`
- `price_timestamp`
- `close_price`
- `ingestion_run_id`
- `raw_path`

### `GET /api/v1/assets/{symbol}/regime`

Returns the latest explainable market regime for an asset.

Backed by:

    MARTS.MART_ASSET_REGIME

Key response fields:

- `symbol`
- `price_date`
- `price_timestamp`
- `close_price`
- `regime_label`
- `regime_explanation`
- `ingestion_run_id`
- `raw_path`

### `GET /api/v1/assets/{symbol}/signals`

Returns modeled signal rows for an asset.

Backed by:

    MARTS.MART_ASSET_SIGNAL

Key response fields:

- `symbol`
- `price_date`
- `signal_code`
- `signal_version`
- `signal_label`
- `signal_explanation`
- `regime_label`
- `ingestion_run_id`
- `raw_path`

### `POST /api/v1/ask`

Returns a governed explanation for a user question about an asset signal or regime.

This endpoint is evidence-based. It does not generate a free-form answer from ungoverned context. The answer is built from modeled mart outputs such as:

- latest signal
- latest regime
- latest snapshot
- signal explanation
- regime explanation

Example request:

    {
      "symbol": "QQQ",
      "question": "Why is QQQ buy_watch?"
    }

Example response shape:

    {
      "symbol": "QQQ",
      "question": "Why is QQQ buy_watch?",
      "answer": "...",
      "evidence": [
        {
          "price_date": "2026-05-22",
          "signal_code": "momentum_regime_v1",
          "signal_label": "buy_watch",
          "signal_explanation": "...",
          "regime_label": "bullish_momentum"
        }
      ]
    }

## Error behavior

If no modeled context exists for a symbol, the API returns `404`.

Examples:

- no current snapshot found
- no signal found
- no regime found
- no signal or regime context found for `/ask`

## Contract principle

The API is a product layer over governed marts, not a replacement for the data warehouse. Raw lineage remains available through `ingestion_run_id` and `raw_path`.
