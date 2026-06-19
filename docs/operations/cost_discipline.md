# Cost Discipline

FinSignal is designed to demonstrate production-style data engineering while keeping cloud spend explicit and controlled.

The project separates implementation from cloud activation. Infrastructure code, contracts, and runbooks can exist without automatically creating paid cloud resources.

## Principles

### 1. No implicit cloud creation

Code changes should not automatically create paid resources.

Terraform modules may be added and tested as source code, but resource creation requires an explicit operator action such as:

    terraform plan
    terraform apply

### 2. Prefer local validation first

Before activating cloud infrastructure, validate behavior locally where possible.

Examples:

- unit tests for ingestion services
- contract tests for Terraform modules
- local raw file writers
- local PySpark feature generation
- dbt compile before dbt run
- API tests with dependency overrides

### 3. Keep expensive runtime boundaries explicit

Cost-generating boundaries include:

- AWS Kinesis streams
- AWS Lambda executions at scale
- S3 storage growth
- Snowflake warehouse runtime
- dbt runs against Snowflake
- long-running Spark jobs

These steps should be documented and intentionally triggered.

### 4. Use Snowflake carefully

Snowflake usage should be controlled through:

- small development warehouse
- explicit warehouse start/stop awareness
- targeted dbt runs during development
- compile-only checks when possible
- limited sample data during early development

### 5. Keep streaming deployment separate

The event-ingestion layer includes Terraform modules for Kinesis, Lambda, IAM, and event landing. These are implementation-ready, but the AWS apply step is intentionally separate.

This allows the platform to demonstrate streaming architecture without accidentally creating recurring cloud costs.

## Current cost posture

The current project state uses:

- local unit tests
- local Airflow development
- local raw file generation
- Snowflake development runs
- local PySpark feature output
- FastAPI local smoke tests

AWS event infrastructure is implemented but not applied by default.

## Operator checklist before cloud activation

Before running a cost-generating command:

1. Confirm the target cloud account.
2. Confirm expected resources.
3. Run a plan or dry-run where possible.
4. Estimate whether resources have recurring cost.
5. Confirm cleanup steps.
6. Document the run result.

## Cleanup checklist

After experiments:

1. Stop unused services.
2. Suspend unused Snowflake warehouses.
3. Remove temporary S3 test data if appropriate.
4. Destroy temporary Terraform-managed resources if they are not needed.
5. Record what was created and removed.
