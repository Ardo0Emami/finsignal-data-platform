from __future__ import annotations

from typing import Any

from app.services.asset_read_service import AssetReadService


class AskService:
    def __init__(self, asset_read_service: AssetReadService) -> None:
        self._asset_read_service = asset_read_service

    def answer(self, symbol: str, question: str) -> dict[str, Any] | None:
        snapshot = self._asset_read_service.get_snapshot(symbol)
        regime = self._asset_read_service.get_regime(symbol)
        signals = self._asset_read_service.get_signals(symbol)

        if snapshot is None and regime is None and not signals:
            return None

        latest_signal = signals[0] if signals else None
        normalized_symbol = symbol.upper()

        signal_label = latest_signal.get("signal_label") if latest_signal else "unknown"
        signal_explanation = latest_signal.get("signal_explanation") if latest_signal else None
        regime_label = regime.get("regime_label") if regime else "unknown"
        regime_explanation = regime.get("regime_explanation") if regime else None

        answer_parts = [
            f"{normalized_symbol} is currently classified as '{signal_label}'",
            f"under the '{regime_label}' regime.",
        ]

        if signal_explanation:
            answer_parts.append(f"Signal reason: {signal_explanation}")

        if regime_explanation:
            answer_parts.append(f"Regime reason: {regime_explanation}")

        evidence = []

        if latest_signal:
            evidence.append(
                {
                    "price_date": str(latest_signal["price_date"]),
                    "signal_code": latest_signal["signal_code"],
                    "signal_label": latest_signal["signal_label"],
                    "signal_explanation": latest_signal["signal_explanation"],
                    "regime_label": latest_signal["regime_label"],
                }
            )

        if regime:
            evidence.append(
                {
                    "price_date": str(regime["price_date"]),
                    "close_price": float(regime["close_price"]),
                    "regime_label": regime["regime_label"],
                    "regime_explanation": regime["regime_explanation"],
                }
            )

        if snapshot:
            evidence.append(
                {
                    "price_date": str(snapshot["price_date"]),
                    "close_price": float(snapshot["close_price"]),
                }
            )

        return {
            "symbol": normalized_symbol,
            "question": question,
            "answer": " ".join(answer_parts),
            "evidence": evidence,
        }
