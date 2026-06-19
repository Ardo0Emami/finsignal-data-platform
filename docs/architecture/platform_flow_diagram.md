# FinSignal Platform Flow Diagram

This diagram shows the main FinSignal data flow from ingestion to product-facing explanations.

```mermaid
flowchart TD
    A[Market Data Providers] --> B[Batch Ingestion Services]
    B --> C[Raw Partitioned Storage]
    C --> D[Snowflake RAW Schema]
    B --> E[Snowflake AUDIT Schema]

    D --> F[dbt STAGING Models]
    F --> G[dbt INTERMEDIATE Models]
    G --> H[dbt MARTS Models]

    H --> I[Current Asset Snapshot]
    H --> J[Asset Signals]
    H --> K[Asset Regimes]
    H --> L[Backtest Results]

    F --> M[PySpark Parquet Export]
    M --> N[PySpark Feature Output]

    I --> O[FastAPI Product API]
    J --> O
    K --> O
    L --> O

    O --> P[Read Endpoints]
    O --> Q[Governed Ask Endpoint]

    Q --> R[Evidence-Based Explanation]
```

## Layer summary

| Layer | Responsibility |
| --- | --- |
| Providers | Source market data records |
| Batch ingestion | Fetch, validate, and write raw data with lineage |
| Raw storage | Preserve source-aligned files |
| Snowflake RAW | Store queryable raw records |
| Snowflake AUDIT | Store ingestion and quality metadata |
| dbt STAGING | Clean and type source-aligned data |
| dbt INTERMEDIATE | Build reusable features and classifications |
| dbt MARTS | Publish product-ready facts, signals, regimes, and backtests |
| PySpark | Generate file-oriented feature outputs over Parquet |
| FastAPI | Expose governed product endpoints |
| `/api/v1/ask` | Explain signals and regimes using modeled evidence |

## Event-ingestion side path

The event-ingestion layer is implemented as a deployment-ready side path:

```mermaid
flowchart LR
    A[Latest Price Event] --> B[Lambda Ingestion Handler]
    B --> C[Kinesis Price Event Stream]
    C --> D[Kinesis Consumer]
    D --> E[S3 Event Landing]
    E --> F[Snowflake RAW_PRICE_EVENTS]
```

AWS activation is intentionally separate from source implementation so cost-generating resources are only created through explicit operator action.
