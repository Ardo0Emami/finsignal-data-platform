from __future__ import annotations

from app.services.asset_read_service import AssetReadService, SnowflakeAssetReadService


def get_asset_read_service() -> AssetReadService:
    return SnowflakeAssetReadService()
