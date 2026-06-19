from __future__ import annotations

from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    symbol: str = Field(min_length=1)
    question: str = Field(min_length=1)


class AskEvidence(BaseModel):
    price_date: str
    close_price: float | None = None
    signal_code: str | None = None
    signal_label: str | None = None
    signal_explanation: str | None = None
    regime_label: str | None = None
    regime_explanation: str | None = None


class AskResponse(BaseModel):
    symbol: str
    question: str
    answer: str
    evidence: list[AskEvidence]
