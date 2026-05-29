from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class IngestionAuditEvent(BaseModel):
    run_id: str
    provider_name: str
    dataset_name: str
    symbol: str
    status: Literal["started", "succeeded", "failed"]
    started_at: datetime
    completed_at: datetime | None = None
    records_extracted: int = 0
    records_written: int = 0
    raw_path: str | None = None
    error_message: str | None = None
