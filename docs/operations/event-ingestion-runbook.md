# Event Ingestion Runbook

## Purpose

The event ingestion path captures latest-price events and lands them in the raw data layer.

This path supports lightweight near-real-time ingestion without replacing the batch Airflow pipeline.

Batch ingestion remains the primary path for scheduled daily market data. Event ingestion exists for latest-price snapshots and event-style processing.

## Architecture

```text
Latest price payload
  -> Lambda latest-price handler
  -> Kinesis price-events stream
  -> S3 raw event landing
  -> Snowflake RAW_PRICE_EVENTS
```

## Components

| Component | Responsibility |
|---|---|
| `ingestion/lambda_handlers/latest_price_ingestion.py` | Lambda-style entrypoint for latest-price events |
| `ingestion/streaming/models.py` | Price event and raw event row contracts |
| `ingestion/streaming/kinesis_producer.py` | Publishes price events to Kinesis |
| `ingestion/streaming/s3_event_writer.py` | Writes raw event JSON to S3-style partitioned paths |
| `ingestion/streaming/kinesis_consumer.py` | Reads Kinesis records and writes events to S3 |
| `scripts/snowflake/create_sample_price_event_file.py` | Creates local sample price event files |
| `scripts/snowflake/load_raw_price_events.py` | Loads raw event JSON files into Snowflake |
| `scripts/lambda_tools/package_latest_price_ingestion.py` | Builds the Lambda deployment package |
| `infra/terraform/modules/kinesis` | Defines the Kinesis price event stream |
| `infra/terraform/modules/lambda_ingestion` | Defines the latest-price Lambda function |
| `infra/terraform/modules/iam` | Grants S3, Kinesis, and CloudWatch Logs access |

## Raw Event Contract

Each latest-price event must include:

```text
event_id
event_type
provider_name
symbol
price_timestamp
close_price
ingested_at
raw_event
```

The raw warehouse target is:

```text
FINSIGNAL_DW.RAW.RAW_PRICE_EVENTS
```

## Raw Landing Path

Raw event files use partitioned paths:

```text
events/event_type=PRICE_TICK/symbol=<SYMBOL>/ingestion_date=<DATE>/event_id=<EVENT_ID>.json
```

This keeps events traceable, replayable, and easy to inspect.

## Local Validation

Run Python validation:

```bash
python -m ruff check .
python -m pytest
```

Build the Lambda package:

```bash
python -m scripts.lambda_tools.package_latest_price_ingestion \
  --output build/lambda/latest_price_ingestion.zip
```

Create a local sample event:

```bash
mkdir -p .local/price_events

python -m scripts.snowflake.create_sample_price_event_file \
  --output .local/price_events/sample_btc_event.json \
  --symbol BTCUSD \
  --close-price 70123.45 \
  --provider-name static_sample
```

Load the local event into Snowflake RAW:

```bash
set -a
source .env
set +a

python -m scripts.snowflake.load_raw_price_events \
  .local/price_events/sample_btc_event.json
```

Inspect recent raw price events:

```sql
SELECT
    event_id,
    event_type,
    provider_name,
    symbol,
    price_timestamp,
    close_price,
    raw_path,
    ingested_at
FROM FINSIGNAL_DW.RAW.RAW_PRICE_EVENTS
ORDER BY ingested_at DESC
LIMIT 5;
```

## Terraform Validation

Build the Lambda package first because the Terraform environment expects the zip path to exist before apply.

```bash
python -m scripts.lambda_tools.package_latest_price_ingestion \
  --output build/lambda/latest_price_ingestion.zip

cd infra/terraform/envs/dev

terraform init
terraform fmt -check -recursive ../..
terraform validate
```

## AWS Deployment Notes

Do not run `terraform apply` until resource wiring, cost, and teardown are reviewed.

If applying in dev:

```bash
cd infra/terraform/envs/dev
terraform plan
terraform apply
```

After validation, destroy resources when they are no longer needed:

```bash
terraform destroy
```

## Cost Guardrails

- Kinesis uses one provisioned shard in dev.
- Lambda is event-driven and does not run continuously.
- Snowflake warehouse must remain auto-suspended.
- Local Airflow remains the default orchestrator in development.
- Do not enable always-on infrastructure without documenting why.
- Do not run Terraform apply casually during local development.

## Validation Checklist

Before enabling real AWS execution, verify:

- Lambda package exists and contains the expected handler.
- Lambda environment variables are configured.
- Kinesis stream name matches the deployed stream.
- S3 raw bucket exists and is writable by the Lambda execution role.
- IAM permissions allow Lambda, Kinesis, S3, and CloudWatch Logs operations.
- Unit tests pass locally.
- Terraform module contract tests pass locally.
- Terraform validate succeeds.
- No Terraform apply is run until resource wiring and teardown are reviewed.

## Recovery Notes

If event ingestion fails:

1. Check Lambda logs in CloudWatch.
2. Confirm required environment variables are present.
3. Verify Kinesis stream name and permissions.
4. Check whether raw event files were written to S3.
5. Validate event payload shape against the `PriceEvent` model.
6. Reprocess raw event files after the root cause is fixed.

## Done Criteria

Phase 5 is considered complete when:

```text
A latest-price event can be created.
The event can be published through the event-ingestion abstraction.
The event can land as raw JSON.
The event can be loaded into FINSIGNAL_DW.RAW.RAW_PRICE_EVENTS.
Terraform defines the AWS Kinesis/Lambda/IAM path.
The Lambda package can be built.
The runbook explains local validation, Terraform validation, cost guardrails, and recovery.
```

## Public Explanation

FinSignal supports both batch and event-style ingestion.

Batch ingestion handles scheduled historical and daily market data.

Event ingestion handles lightweight latest-price snapshots through a Lambda and Kinesis path, preserving raw event payloads and loading them into Snowflake for downstream analytics.