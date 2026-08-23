#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Upload local game assets to Cloudflare R2 for distribution.

Creates a ZIP archive from configured asset directories, computes a SHA-256
checksum, uploads to R2 via the S3-compatible API, and publishes version.json.

Requires a local .env file with R2 credentials (see .env.example).

Usage:
    python tools/upload_assets.py
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import threading
import zipfile
from pathlib import Path

import boto3
from botocore.config import Config
from botocore.exceptions import BotoCoreError, ClientError
from dotenv import load_dotenv
from boto3.s3.transfer import TransferConfig

REPO_ROOT = Path(__file__).resolve().parent.parent

ASSET_DIRECTORIES = [
    "game/images",
    "game/videos",  # optional: skipped if missing
]

ARCHIVE_NAME = "assets.zip"
VERSION_FILE = "version.json"
TEMP_OBJECT_KEY = "assets.zip.uploading"
LIVE_OBJECT_KEY = "assets.zip"

CHUNK_SIZE = 8 * 1024 * 1024  # 8 MiB for hashing
MULTIPART_THRESHOLD = 64 * 1024 * 1024  # 64 MiB
MULTIPART_CHUNK_SIZE = 64 * 1024 * 1024

REQUIRED_ENV_VARS = (
    "R2_ACCOUNT_ID",
    "R2_ACCESS_KEY_ID",
    "R2_SECRET_ACCESS_KEY",
    "R2_BUCKET_NAME",
    "R2_PUBLIC_URL",
    "ASSET_VERSION",
)


class ProgressCallback:
    """Thread-safe upload progress callback for boto3 transfer manager."""

    def __init__(self, label: str, total_bytes: int) -> None:
        self.label = label
        self.total_bytes = max(total_bytes, 1)
        self.seen = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount: int) -> None:
        with self._lock:
            self.seen += bytes_amount
            self._render()

    def _render(self) -> None:
        percent = min(100, int(self.seen * 100 / self.total_bytes))
        filled = percent // 5
        bar = "#" * filled + "." * (20 - filled)
        seen_gb = self.seen / (1024**3)
        total_gb = self.total_bytes / (1024**3)
        line = (
            f"\r{self.label}\n"
            f"[{bar}] {percent}%\n"
            f"{seen_gb:.1f} GB / {total_gb:.1f} GB"
        )
        sys.stdout.write(line)
        sys.stdout.flush()

    def finish(self) -> None:
        sys.stdout.write("\n")
        sys.stdout.flush()


def fail(message: str, code: int = 1) -> None:
    """Print an error message and exit."""
    print(f"ERROR: {message}", file=sys.stderr)
    sys.exit(code)


def load_config() -> dict[str, str]:
    """Load and validate required environment variables from .env."""
    env_path = REPO_ROOT / ".env"
    if not env_path.is_file():
        fail(
            "Missing .env file. Copy .env.example to .env and fill in your R2 credentials."
        )

    load_dotenv(env_path)

    config: dict[str, str] = {}
    missing: list[str] = []
    for key in REQUIRED_ENV_VARS:
        value = os.getenv(key, "").strip()
        if not value:
            missing.append(key)
        else:
            config[key] = value

    if missing:
        fail(
            "Missing required environment variables in .env:\n  "
            + "\n  ".join(missing)
        )

    return config


def create_r2_client(config: dict[str, str]):
    """Create a boto3 S3 client configured for Cloudflare R2."""
    endpoint = f"https://{config['R2_ACCOUNT_ID']}.r2.cloudflarestorage.com"
    return boto3.client(
        "s3",
        endpoint_url=endpoint,
        aws_access_key_id=config["R2_ACCESS_KEY_ID"],
        aws_secret_access_key=config["R2_SECRET_ACCESS_KEY"],
        region_name="auto",
        config=Config(signature_version="s3v4"),
    )


def iter_asset_files() -> list[tuple[Path, str]]:
    """
    Collect files to archive.

    Returns a list of (absolute_path, archive_name) tuples where archive_name
    is relative to the game/ directory (e.g. images/foo.png).
    """
    files: list[tuple[Path, str]] = []

    for rel_dir in ASSET_DIRECTORIES:
        source_dir = REPO_ROOT / rel_dir
        if not source_dir.is_dir():
            if rel_dir == "game/videos":
                continue
            fail(f"Asset directory not found: {rel_dir}")

        # Strip the "game/" prefix so archive paths are relative to game/
        game_prefix = Path("game")
        rel_dir_path = Path(rel_dir)
        if rel_dir_path.parts[:1] != ("game",):
            fail(f"Asset directory must be under game/: {rel_dir}")

        archive_prefix = Path(*rel_dir_path.parts[1:])

        for file_path in sorted(source_dir.rglob("*")):
            if file_path.is_file():
                rel_path = archive_prefix / file_path.relative_to(source_dir)
                files.append((file_path, rel_path.as_posix()))

    if not files:
        fail("No asset files found to archive.")

    return files


def create_archive(archive_path: Path, files: list[tuple[Path, str]]) -> None:
    """Create a ZIP archive with stored (uncompressed) entries and Zip64 support."""
    print(f"Creating archive: {archive_path.name}")
    print(f"  {len(files)} files from {len(ASSET_DIRECTORIES)} configured directories")

    with zipfile.ZipFile(
        archive_path,
        mode="w",
        compression=zipfile.ZIP_STORED,
        allowZip64=True,
    ) as zf:
        for index, (source, arcname) in enumerate(files, start=1):
            zf.write(source, arcname)
            if index % 500 == 0 or index == len(files):
                print(f"  Packed {index}/{len(files)} files...", end="\r", flush=True)

    print(f"\nArchive created ({archive_path.stat().st_size / (1024**3):.2f} GB)")


def compute_sha256(file_path: Path) -> str:
    """Compute SHA-256 hash of a file using chunked reads."""
    print("Computing SHA-256 checksum...")
    digest = hashlib.sha256()
    total = file_path.stat().st_size
    processed = 0

    with file_path.open("rb") as handle:
        while chunk := handle.read(CHUNK_SIZE):
            digest.update(chunk)
            processed += len(chunk)
            if total:
                percent = min(100, int(processed * 100 / total))
                print(f"  Hashing: {percent}%", end="\r", flush=True)

    print(f"  SHA-256: {digest.hexdigest()}")
    return digest.hexdigest()


def write_version_json(
    version_path: Path,
    version: str,
    filename: str,
    size: int,
    sha256: str,
) -> None:
    """Write version metadata to a local JSON file."""
    metadata = {
        "version": version,
        "filename": filename,
        "size": size,
        "sha256": sha256,
    }
    version_path.write_text(json.dumps(metadata, indent=4) + "\n", encoding="utf-8")


def upload_file(
    client,
    bucket: str,
    local_path: Path,
    object_key: str,
    cache_control: str,
) -> None:
    """Upload a local file to R2 with multipart support and progress display."""
    file_size = local_path.stat().st_size
    print(f"Uploading {object_key} ({file_size / (1024**3):.2f} GB)...")

    transfer_config = TransferConfig(
        multipart_threshold=MULTIPART_THRESHOLD,
        multipart_chunksize=MULTIPART_CHUNK_SIZE,
        max_concurrency=4,
        use_threads=True,
    )
    progress = ProgressCallback(f"Uploading {object_key}", file_size)

    try:
        client.upload_file(
            str(local_path),
            bucket,
            object_key,
            ExtraArgs={"CacheControl": cache_control},
            Config=transfer_config,
            Callback=progress,
        )
    except (BotoCoreError, ClientError) as exc:
        fail(f"Upload failed for {object_key}: {exc}")
    finally:
        progress.finish()


def copy_object(client, bucket: str, source_key: str, dest_key: str) -> None:
    """Copy an object within the same bucket (server-side)."""
    print(f"Publishing {dest_key}...")
    try:
        client.copy_object(
            Bucket=bucket,
            Key=dest_key,
            CopySource={"Bucket": bucket, "Key": source_key},
            CacheControl="no-cache, max-age=0",
            MetadataDirective="REPLACE",
        )
    except (BotoCoreError, ClientError) as exc:
        fail(f"Failed to publish {dest_key}: {exc}")


def delete_object(client, bucket: str, object_key: str) -> None:
    """Delete an object from the bucket, ignoring missing keys."""
    try:
        client.delete_object(Bucket=bucket, Key=object_key)
    except (BotoCoreError, ClientError) as exc:
        fail(f"Failed to delete {object_key}: {exc}")


def cleanup_local(*paths: Path) -> None:
    """Remove temporary local files created by this script."""
    for path in paths:
        if path.is_file():
            path.unlink()
            print(f"Removed local file: {path.name}")


def main() -> None:
    config = load_config()
    client = create_r2_client(config)
    bucket = config["R2_BUCKET_NAME"]
    version = config["ASSET_VERSION"]

    archive_path = REPO_ROOT / ARCHIVE_NAME
    version_path = REPO_ROOT / VERSION_FILE

    files = iter_asset_files()
    create_archive(archive_path, files)

    file_size = archive_path.stat().st_size
    sha256 = compute_sha256(archive_path)
    write_version_json(version_path, version, ARCHIVE_NAME, file_size, sha256)

    upload_file(
        client,
        bucket,
        archive_path,
        TEMP_OBJECT_KEY,
        cache_control="no-cache, max-age=0",
    )
    copy_object(client, bucket, TEMP_OBJECT_KEY, LIVE_OBJECT_KEY)
    upload_file(
        client,
        bucket,
        version_path,
        VERSION_FILE,
        cache_control="no-cache, max-age=0",
    )
    delete_object(client, bucket, TEMP_OBJECT_KEY)

    public_url = config["R2_PUBLIC_URL"].rstrip("/")
    print("\nUpload complete.")
    print(f"  Version:  {version}")
    print(f"  Size:     {file_size / (1024**3):.2f} GB")
    print(f"  SHA-256:  {sha256}")
    print(f"  Assets:   {public_url}/{LIVE_OBJECT_KEY}")
    print(f"  Metadata: {public_url}/{VERSION_FILE}")

    cleanup_local(archive_path, version_path)


if __name__ == "__main__":
    main()
