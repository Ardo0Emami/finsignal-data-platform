from __future__ import annotations

from app.core.config import Settings

REQUIRED_SETTINGS = [
    "snowflake_account",
    "snowflake_user",
    "snowflake_password",
    "snowflake_warehouse",
]


def check_snowflake_ready(settings: Settings | None = None) -> dict[str, object]:
    settings = settings or Settings()

    missing = [
        field_name
        for field_name in REQUIRED_SETTINGS
        if not getattr(settings, field_name)
    ]

    return {
        "ready": not missing,
        "missing_settings": missing,
        "database": settings.snowflake_database,
        "schema": settings.snowflake_schema,
        "warehouse": settings.snowflake_warehouse,
    }


def main() -> None:
    result = check_snowflake_ready()
    print(result)

    if not result["ready"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
