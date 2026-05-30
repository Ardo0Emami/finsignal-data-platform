import json
from pathlib import Path

from app.core.config import Settings


def find_audit_files(base_path: str) -> list[Path]:
    audit_root = Path(base_path) / "audit" / "ingestion_events"

    if not audit_root.exists():
        return []

    return sorted(
        audit_root.glob("dataset=*/symbol=*/*.json"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )


def load_audit_event(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def format_audit_summary(event: dict) -> str:
    status = event["status"]
    symbol = event["symbol"]
    provider = event["provider_name"]
    dataset = event["dataset_name"]
    records_written = event["records_written"]
    run_id = event["run_id"]
    error_message = event.get("error_message")

    if error_message:
        return (
            f"{status.upper()} | symbol={symbol} | provider={provider} | "
            f"dataset={dataset} | records_written={records_written} | "
            f"run_id={run_id} | error={error_message}"
        )

    return (
        f"{status.upper()} | symbol={symbol} | provider={provider} | "
        f"dataset={dataset} | records_written={records_written} | "
        f"run_id={run_id}"
    )


def main() -> None:
    settings = Settings()
    audit_files = find_audit_files(settings.local_raw_base_path)

    if not audit_files:
        print("No ingestion audit events found.")
        return

    for path in audit_files[:10]:
        event = load_audit_event(path)
        print(format_audit_summary(event))


if __name__ == "__main__":
    main()
