from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_asset_read_service
from app.schemas.ask import AskRequest, AskResponse
from app.services.ask_service import AskService
from app.services.asset_read_service import AssetReadService

router = APIRouter(prefix="/api/v1", tags=["ask"])

AssetReadServiceDep = Annotated[AssetReadService, Depends(get_asset_read_service)]


@router.post("/ask", response_model=AskResponse, response_model_exclude_none=True)
def ask_signal_question(
    request: AskRequest,
    asset_read_service: AssetReadServiceDep,
) -> dict[str, object]:
    ask_service = AskService(asset_read_service)
    answer = ask_service.answer(symbol=request.symbol, question=request.question)

    if answer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No signal or regime context found for symbol '{request.symbol}'.",
        )

    return answer
