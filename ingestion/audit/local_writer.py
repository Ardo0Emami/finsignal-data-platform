import json
from pathlib import Path

from ingestion.audit.models import IngestionAuditEvent


class LocalAuditWriter:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)

    def write_event(self, event: IngestionAuditEvent) -> str:
        output_dir = (
            self.base_path
            / "audit"
            / "ingestion_events"
            / f"dataset={event.dataset_name}"
            / f"symbol={event.symbol}"
        )

        output_dir.mkdir(parents=True, exist_ok=True)

        output_path = output_dir / f"{event.run_id}.json"

        output_path.write_text(
            json.dumps(event.model_dump(mode="json"), indent=2),
            encoding="utf-8",
        )

        return str(output_path)
