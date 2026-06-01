CREATE TABLE IF NOT EXISTS FINSIGNAL_DW.AUDIT.INGESTION_RUNS (
    run_id STRING NOT NULL,
    provider_name STRING NOT NULL,
    dataset_name STRING NOT NULL,
    symbol STRING NOT NULL,
    status STRING NOT NULL,
    started_at TIMESTAMP_NTZ NOT NULL,
    completed_at TIMESTAMP_NTZ,
    records_extracted INTEGER NOT NULL,
    records_written INTEGER NOT NULL,
    raw_path STRING,
    error_message STRING,
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

CREATE TABLE IF NOT EXISTS FINSIGNAL_DW.AUDIT.DATA_QUALITY_RESULTS (
    run_id STRING NOT NULL,
    check_name STRING NOT NULL,
    dataset_name STRING NOT NULL,
    status STRING NOT NULL,
    failed_row_count INTEGER NOT NULL,
    details VARIANT,
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);
