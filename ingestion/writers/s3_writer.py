import hashlib
import json
from datetime import datetime, timezone
from uuid import uuid4

import boto3

from ingestion.writers.base import RawMarketDataWriter


class S3RawWriter(RawMarketDataWriter):
    def __init__(self, bucket_name: str):
        self.bucket_name = bucket_name
        self.client = boto3.client("s3")

    def write_market_prices(
        self,
        provider_name: str,
        dataset_name: str,
        symbol: str,
        records: list[dict],
    ) -> str:
        now = datetime.now(timezone.utc)
        run_id = str(uuid4())
        ingestion_date = now.date().isoformat()

        payload = {
            "provider": provider_name,
            "dataset": dataset_name,
            "symbol": symbol,
            "ingestion_run_id": run_id,
            "ingested_at": now.isoformat(),
            "records": records,
        }

        key_prefix = (
            f"raw/provider={provider_name}/dataset={dataset_name}/"
            f"symbol={symbol}/ingestion_date={ingestion_date}/"
            f"run_id={run_id}"
        )

        data_key = f"{key_prefix}/data.json"
        metadata_key = f"{key_prefix}/metadata.json"

        body = json.dumps(payload, indent=2, default=str).encode("utf-8")
        checksum = hashlib.sha256(body).hexdigest()

        self.client.put_object(
            Bucket=self.bucket_name,
            Key=data_key,
            Body=body,
            ContentType="application/json",
            Metadata={"sha256": checksum},
        )

        metadata = {
            "provider": provider_name,
            "dataset": dataset_name,
            "symbol": symbol,
            "record_count": len(records),
            "ingested_at": now.isoformat(),
            "schema_version": "1.0",
            "data_sha256": checksum,
            "data_path": f"s3://{self.bucket_name}/{data_key}",
        }

        self.client.put_object(
            Bucket=self.bucket_name,
            Key=metadata_key,
            Body=json.dumps(metadata, indent=2).encode("utf-8"),
            ContentType="application/json",
        )

        return f"s3://{self.bucket_name}/{data_key}"
