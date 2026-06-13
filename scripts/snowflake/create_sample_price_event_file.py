from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

from ingestion.streaming.models import PriceEvent


def create_sample_price_event_file(
    *,
    output_path: Path,
    symbol: str,
    close_price: float,
    provider_name: str,
) -> Path:
    event = PriceEvent.latest_price(
        provider_name=provider_name,
        symbol=symbol,
        close_price=close_price,
        price_timestamp=datetime.now(timezone.utc),
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(event.model_dump_json(indent=2), encoding="utf-8")

    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a local sample price event file.")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--symbol", default="BTCUSD")
    parser.add_argument("--close-price", type=float, default=69000.0)
    parser.add_argument("--provider-name", default="static_sample")
    args = parser.parse_args()

    path = create_sample_price_event_file(
        output_path=args.output,
        symbol=args.symbol,
        close_price=args.close_price,
        provider_name=args.provider_name,
    )

    print(path)


if __name__ == "__main__":
    main()
