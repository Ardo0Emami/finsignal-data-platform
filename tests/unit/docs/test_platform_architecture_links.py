from __future__ import annotations

from pathlib import Path


def test_platform_architecture_links_flow_diagram() -> None:
    content = Path("docs/architecture/platform_architecture.md").read_text(encoding="utf-8")

    assert "## Architecture diagram" in content
    assert "docs/architecture/platform_flow_diagram.md" in content
