import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from ingestion.writers.base import RawMarketDataWriter


class LocalRawWriter(RawMarketDataWriter):
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)

    def write_market_prices(
        self,
        provider_name: str,
        dataset_name: str,
        symbol: str,
        records: list[dict],
        run_id: str | None = None,
    ) -> str:
        now = datetime.now(timezone.utc)
        run_id = run_id or str(uuid4())
        ingestion_date = now.date().isoformat()

        payload = {
            "provider": provider_name,
            "dataset": dataset_name,
            "symbol": symbol,
            "ingestion_run_id": run_id,
            "ingested_at": now.isoformat(),
            "records": records,
        }

        output_dir = (
            self.base_path
            / "raw"
            / f"provider={provider_name}"
            / f"dataset={dataset_name}"
            / f"symbol={symbol}"
            / f"ingestion_date={ingestion_date}"
            / f"run_id={run_id}"
        )

        output_dir.mkdir(parents=True, exist_ok=True)

        data_path = output_dir / "data.json"
        metadata_path = output_dir / "metadata.json"

        body = json.dumps(payload, indent=2, default=str).encode("utf-8")
        checksum = hashlib.sha256(body).hexdigest()

        data_path.write_bytes(body)

        metadata = {
            "provider": provider_name,
            "dataset": dataset_name,
            "symbol": symbol,
            "record_count": len(records),
            "ingested_at": now.isoformat(),
            "schema_version": "1.0",
            "data_sha256": checksum,
            "data_path": str(data_path),
        }

        metadata_path.write_text(
            json.dumps(metadata, indent=2),
            encoding="utf-8",
        )

        return str(data_path)
