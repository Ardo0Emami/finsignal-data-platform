from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_asset_read_service
from app.schemas.asset import AssetRegimeResponse, AssetSignalResponse, AssetSnapshotResponse
from app.services.asset_read_service import AssetReadService

router = APIRouter(prefix="/api/v1/assets", tags=["assets"])

AssetReadServiceDep = Annotated[AssetReadService, Depends(get_asset_read_service)]


@router.get("/{symbol}/snapshot", response_model=AssetSnapshotResponse)
def get_asset_snapshot(symbol: str, service: AssetReadServiceDep) -> dict[str, object]:
    snapshot = service.get_snapshot(symbol)

    if snapshot is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No snapshot found for symbol '{symbol}'.",
        )

    return snapshot


@router.get("/{symbol}/signals", response_model=list[AssetSignalResponse])
def get_asset_signals(symbol: str, service: AssetReadServiceDep) -> list[dict[str, object]]:
    signals = service.get_signals(symbol)

    if not signals:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No signals found for symbol '{symbol}'.",
        )

    return signals


@router.get("/{symbol}/regime", response_model=AssetRegimeResponse)
def get_asset_regime(symbol: str, service: AssetReadServiceDep) -> dict[str, object]:
    regime = service.get_regime(symbol)

    if regime is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No regime found for symbol '{symbol}'.",
        )

    return regime
