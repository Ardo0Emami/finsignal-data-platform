from __future__ import annotations

from pathlib import Path


def test_dbt_uses_custom_schema_names_without_raw_prefix() -> None:
    macro = Path("dbt/macros/generate_schema_name.sql").read_text(encoding="utf-8")

    assert "macro generate_schema_name(custom_schema_name, node)" in macro
    assert "{{ custom_schema_name | trim }}" in macro
    assert "{{ default_schema }}" in macro


def test_dbt_project_declares_layer_schemas() -> None:
    project = Path("dbt/dbt_project.yml").read_text(encoding="utf-8")

    assert "+schema: STAGING" in project
    assert "+schema: INTERMEDIATE" in project
    assert "+schema: MARTS" in project


def test_dbt_profile_default_schema_remains_raw_for_sources() -> None:
    profile = Path("dbt/profiles.yml").read_text(encoding="utf-8")

    assert "FINSIGNAL_SNOWFLAKE_SCHEMA" in profile
    assert "'RAW'" in profile or '"RAW"' in profile
