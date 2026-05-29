import pytest

from app.core.config import Settings
from ingestion.providers.static_sample import StaticSampleProvider
from scripts.ingestion.run_market_ingestion import build_provider


def test_build_provider_uses_static_sample_by_default() -> None:
    settings = Settings(market_data_provider="static_sample")

    provider = build_provider(settings)

    assert isinstance(provider, StaticSampleProvider)
    assert provider.provider_name == "static_sample"


def test_build_provider_rejects_unknown_provider() -> None:
    settings = Settings(market_data_provider="unknown")

    with pytest.raises(ValueError, match="Unsupported FINSIGNAL_MARKET_DATA_PROVIDER"):
        build_provider(settings)
