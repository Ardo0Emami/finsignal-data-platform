# Event Ingestion Runbook

## Purpose

The event ingestion path captures latest-price events and lands them in the raw data layer.

This path supports lightweight near-real-time ingestion without replacing the batch Airflow pipeline.

## Architecture

```text
Latest price payload
  -> Lambda latest-price handler
  -> Kinesis price-events stream
  -> S3 raw event landing
  -> Snowflake RAW_PRICE_EVENTS
```

## Components

### Lambda latest-price handler

Receives or builds latest-price payloads and converts them into standardized price events.

### Kinesis price-events stream

Acts as the streaming buffer between event producers and downstream consumers.

### S3 raw event landing

Stores raw event JSON files in partitioned paths so events remain traceable and replayable.

### Snowflake RAW_PRICE_EVENTS

Represents the warehouse raw table intended for querying landed price events.

## Operational Notes

- This path does not replace the batch Airflow ingestion pipeline.
- Batch ingestion remains the primary path for scheduled daily market data.
- Event ingestion supports lightweight near-real-time latest-price events.
- Raw event payloads should be preserved for lineage and debugging.
- Event IDs should be treated as unique identifiers for tracing.
- S3 paths should remain partitioned by event type, symbol, and ingestion date.
- Snowflake loading for RAW_PRICE_EVENTS should preserve raw event metadata.

## Validation Checklist

Before enabling real AWS execution, verify:

- Lambda package exists and contains the expected handler.
- Lambda environment variables are configured.
- Kinesis stream name matches the deployed stream.
- S3 raw bucket exists and is writable by the Lambda execution role.
- IAM permissions allow the required Lambda, Kinesis, S3, and CloudWatch Logs operations.
- Unit tests pass locally.
- Terraform module contract tests pass locally.
- No Terraform apply is run until resource wiring is reviewed.

## Recovery Notes

If event ingestion fails:

1. Check Lambda logs in CloudWatch.
2. Confirm required environment variables are present.
3. Verify Kinesis stream name and permissions.
4. Check whether raw event files were written to S3.
5. Validate event payload shape against the PriceEvent model.
6. Reprocess raw event files if needed after the root cause is fixed.
