import pytest

from app.core.config import Settings
from scripts.ingestion.run_market_ingestion import parse_asset_symbols


def test_parse_asset_symbols_defaults_to_btc_and_qqq() -> None:
    settings = Settings()

    symbols = parse_asset_symbols(settings)

    assert symbols == ["BTCUSD", "QQQ"]


def test_parse_asset_symbols_trims_and_uppercases_values() -> None:
    settings = Settings(asset_symbols=" btcusd, qqq , spy ")

    symbols = parse_asset_symbols(settings)

    assert symbols == ["BTCUSD", "QQQ", "SPY"]


def test_parse_asset_symbols_rejects_empty_list() -> None:
    settings = Settings(asset_symbols=" , , ")

    with pytest.raises(ValueError, match="FINSIGNAL_ASSET_SYMBOLS"):
        parse_asset_symbols(settings)
