from __future__ import annotations

import argparse
import shutil
import zipfile
from pathlib import Path

INCLUDED_PATHS = [
    Path("ingestion/lambda_handlers"),
    Path("ingestion/streaming"),
]

PACKAGE_ROOT_FILES = [
    Path("ingestion/__init__.py"),
]


def _copy_path(source: Path, destination_root: Path) -> None:
    destination = destination_root / source

    if source.is_dir():
        shutil.copytree(
            source,
            destination,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
        )
        return

    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def build_latest_price_ingestion_package(output_path: Path) -> Path:
    build_root = Path("build/lambda/package_latest_price_ingestion")

    if build_root.exists():
        shutil.rmtree(build_root)

    build_root.mkdir(parents=True, exist_ok=True)

    for path in PACKAGE_ROOT_FILES + INCLUDED_PATHS:
        if not path.exists():
            raise FileNotFoundError(f"Required Lambda package path is missing: {path}")

        _copy_path(path, build_root)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    if output_path.exists():
        output_path.unlink()

    with zipfile.ZipFile(output_path, mode="w", compression=zipfile.ZIP_DEFLATED) as archive:
        for file_path in sorted(build_root.rglob("*")):
            if file_path.is_file():
                archive.write(
                    file_path,
                    arcname=file_path.relative_to(build_root).as_posix(),
                )

    shutil.rmtree(build_root)

    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build the latest price ingestion Lambda deployment package."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("build/lambda/latest_price_ingestion.zip"),
        help="Output path for the Lambda zip package.",
    )
    args = parser.parse_args()

    package_path = build_latest_price_ingestion_package(args.output)
    print(package_path)


if __name__ == "__main__":
    main()
