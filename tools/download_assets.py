#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Download and install game assets from the public Cloudflare R2 distribution.

No authentication required. Checks the remote version against the locally
installed version and only downloads when an update is available.

Usage:
    python tools/download_assets.py
"""

from __future__ import annotations

import hashlib
import json
import shutil
import sys
import urllib.error
import urllib.request
import zipfile
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
GAME_DIR = REPO_ROOT / "game"

# Set this to your public R2 URL after enabling public access on the bucket.
PUBLIC_ASSET_URL = "https://pub-9fd8bb5c68714747b644cf762a4320e0.r2.dev"

VERSION_FILE = "version.json"
ARCHIVE_NAME = "assets.zip"
PART_FILE = "assets.zip.part"
LOCAL_VERSION_FILE = GAME_DIR / ".asset-version"
TEMP_EXTRACT_DIR = REPO_ROOT / ".temp_assets"
ARCHIVE_PATH = REPO_ROOT / ARCHIVE_NAME

CHUNK_SIZE = 8 * 1024 * 1024  # 8 MiB

# Directories inside the archive that get swapped into game/ on install.
ASSET_DIRS = ("images", "videos")

LICENSE_FILE = REPO_ROOT / "LICENSE"

# Fallback if LICENSE cannot be read (CC BY 4.0 section from LICENSE).
ARTWORK_LICENSE_FALLBACK = """\
### Creative Commons Attribution 4.0 (CC BY 4.0)

Copyright (c) 2023 SuIT-JI

The artwork distributed with Mind the School (via the asset download and game
releases) is under the Creative Commons Attribution 4.0 (CC BY 4.0) license.

You should have received a copy of the license along with this
work. If not, see <https://creativecommons.org/licenses/by/4.0/>.\
"""


class UserError(Exception):
    """Expected error with a user-friendly message."""


def fail(message: str, code: int = 1) -> None:
    """Print an error message and exit."""
    print(f"ERROR: {message}", file=sys.stderr)
    sys.exit(code)


def read_artwork_license_text() -> str:
    """Return the CC BY 4.0 license text for downloaded artwork from LICENSE."""
    if LICENSE_FILE.is_file():
        content = LICENSE_FILE.read_text(encoding="utf-8")
        marker = "### Creative Commons Attribution 4.0"
        start = content.find(marker)
        if start != -1:
            end = content.find("Contact:", start)
            section = content[start:end].strip() if end != -1 else content[start:].strip()
            if section:
                return section
    return ARTWORK_LICENSE_FALLBACK


def print_artwork_license_notice() -> None:
    """Print the artwork license that applies to the downloaded game assets."""
    print("\n" + "=" * 72)
    print("Artwork license (downloaded game assets)")
    print("=" * 72)
    print(read_artwork_license_text())
    print("=" * 72 + "\n")


def format_gb(num_bytes: int) -> str:
    """Format bytes as gigabytes with one decimal place."""
    return f"{num_bytes / (1024**3):.1f} GB"


def validate_public_url() -> str:
    """Ensure PUBLIC_ASSET_URL has been configured."""
    url = PUBLIC_ASSET_URL.rstrip("/")
    if "xxxxxxxx" in url or not url.startswith("https://"):
        fail(
            "PUBLIC_ASSET_URL is not configured in tools/download_assets.py.\n"
            "Set it to your public R2 bucket URL (e.g. https://pub-xxxx.r2.dev)."
        )
    return url


def fetch_json(url: str) -> dict[str, Any]:
    """Fetch and parse a JSON document from a public URL."""
    try:
        with urllib.request.urlopen(url, timeout=60) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            raise UserError(f"Could not find {VERSION_FILE} at {url} (HTTP 404).") from exc
        if exc.code == 403:
            raise UserError(
                f"Access denied when fetching {VERSION_FILE} (HTTP 403).\n"
                "The bucket may not be configured for public access."
            ) from exc
        raise UserError(f"HTTP error {exc.code} while fetching {VERSION_FILE}.") from exc
    except urllib.error.URLError as exc:
        reason = exc.reason
        if isinstance(reason, OSError):
            raise UserError(
                "Could not connect to the asset server.\n"
                "Check your internet connection and try again."
            ) from exc
        raise UserError(f"Network error while fetching {VERSION_FILE}: {reason}") from exc
    except json.JSONDecodeError as exc:
        raise UserError(f"{VERSION_FILE} is not valid JSON.") from exc


def read_local_version() -> str | None:
    """Read the locally installed asset version, if any."""
    if LOCAL_VERSION_FILE.is_file():
        return LOCAL_VERSION_FILE.read_text(encoding="utf-8").strip() or None
    return None


def render_progress(label: str, downloaded: int, total: int) -> None:
    """Render a simple ASCII progress bar."""
    if total <= 0:
        total = max(downloaded, 1)
    percent = min(100, int(downloaded * 100 / total))
    filled = percent // 5
    bar = "#" * filled + "." * (20 - filled)
    sys.stdout.write(
        f"\r{label}\n"
        f"[{bar}] {percent}%\n"
        f"{format_gb(downloaded)} / {format_gb(total)}"
    )
    sys.stdout.flush()


def check_disk_space(required_bytes: int) -> None:
    """Ensure enough free disk space is available (archive + extract buffer)."""
    usage = shutil.disk_usage(REPO_ROOT)
    # Need space for the download and extraction (roughly 2x archive size).
    needed = required_bytes * 2
    if usage.free < needed:
        raise UserError(
            f"Not enough disk space.\n"
            f"  Required: ~{format_gb(needed)}\n"
            f"  Available: {format_gb(usage.free)}"
        )


def download_file(url: str, dest: Path, expected_size: int) -> None:
    """Stream-download a file to disk with progress display."""
    label = f"Downloading {ARCHIVE_NAME}"
    print(label)

    if dest.is_file():
        dest.unlink()

    downloaded = 0
    total = expected_size

    try:
        request = urllib.request.Request(url, headers={"User-Agent": "MTS-Asset-Downloader/1.0"})
        with urllib.request.urlopen(request, timeout=30) as response:
            content_length = response.headers.get("Content-Length")
            if content_length:
                total = int(content_length)

            check_disk_space(total)

            with dest.open("wb") as handle:
                while True:
                    chunk = response.read(CHUNK_SIZE)
                    if not chunk:
                        break
                    handle.write(chunk)
                    downloaded += len(chunk)
                    render_progress(label, downloaded, total)

        sys.stdout.write("\n")
        sys.stdout.flush()

    except urllib.error.HTTPError as exc:
        if dest.is_file():
            dest.unlink()
        if exc.code == 404:
            raise UserError(f"Could not find {ARCHIVE_NAME} at {url} (HTTP 404).") from exc
        if exc.code == 403:
            raise UserError(f"Access denied when downloading {ARCHIVE_NAME} (HTTP 403).") from exc
        raise UserError(f"HTTP error {exc.code} while downloading {ARCHIVE_NAME}.") from exc
    except urllib.error.URLError as exc:
        if dest.is_file():
            dest.unlink()
        raise UserError(
            "Download interrupted or connection failed.\n"
            "Check your internet connection and run the script again."
        ) from exc
    except OSError as exc:
        if dest.is_file():
            dest.unlink()
        if exc.errno == 28 or "No space" in str(exc):
            raise UserError("Not enough disk space to complete the download.") from exc
        raise UserError(f"Failed to write download file: {exc}") from exc


def compute_sha256(file_path: Path) -> str:
    """Compute SHA-256 hash of a file using chunked reads."""
    digest = hashlib.sha256()
    with file_path.open("rb") as handle:
        while chunk := handle.read(CHUNK_SIZE):
            digest.update(chunk)
    return digest.hexdigest()


def verify_checksum(file_path: Path, expected: str) -> None:
    """Verify the SHA-256 checksum of a downloaded file."""
    print("Verifying SHA-256 checksum...")
    actual = compute_sha256(file_path)
    print(f"  expected: {expected}")
    print(f"  actual:   {actual}")
    if actual != expected:
        raise UserError(
            "SHA-256 checksum mismatch.\n"
            "The downloaded archive may be corrupted."
        )


def safe_extract_path(base_dir: Path, member_name: str) -> Path:
    """
    Resolve a zip member path and ensure it stays within base_dir.

    Raises UserError if the path would escape the target directory (Zip Slip).
    """
    target = (base_dir / member_name).resolve()
    base_resolved = base_dir.resolve()
    try:
        target.relative_to(base_resolved)
    except ValueError as exc:
        raise UserError(
            f"Unsafe path in archive: {member_name}\n"
            "The archive may be corrupted or tampered with."
        ) from exc
    return target


def extract_archive(archive_path: Path, dest_dir: Path) -> None:
    """Extract archive contents into a temporary directory with Zip Slip protection."""
    print(f"Extracting to {dest_dir.name}/...")

    if dest_dir.exists():
        shutil.rmtree(dest_dir)
    dest_dir.mkdir(parents=True)

    try:
        with zipfile.ZipFile(archive_path, "r") as zf:
            members = zf.infolist()
            for index, member in enumerate(members, start=1):
                target = safe_extract_path(dest_dir, member.filename)
                if member.is_dir() or member.filename.endswith("/"):
                    target.mkdir(parents=True, exist_ok=True)
                else:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    with zf.open(member) as source, target.open("wb") as dest:
                        shutil.copyfileobj(source, dest)

                if index % 500 == 0 or index == len(members):
                    print(f"  Extracted {index}/{len(members)} entries...", end="\r", flush=True)

        print(f"\nExtraction complete ({len(members)} entries).")

    except zipfile.BadZipFile as exc:
        shutil.rmtree(dest_dir, ignore_errors=True)
        raise UserError("The downloaded archive is not a valid ZIP file.") from exc
    except OSError as exc:
        shutil.rmtree(dest_dir, ignore_errors=True)
        if exc.errno == 28 or "No space" in str(exc):
            raise UserError("Not enough disk space to extract the archive.") from exc
        raise UserError(f"Failed to extract archive: {exc}") from exc


def swap_asset_directory(asset_name: str) -> None:
    """Move an extracted asset directory into game/, keeping a rollback copy."""
    source = TEMP_EXTRACT_DIR / asset_name
    if not source.is_dir():
        return

    target = GAME_DIR / asset_name
    backup = GAME_DIR / f"{asset_name}.old"

    if backup.exists():
        shutil.rmtree(backup)

    if target.exists():
        target.rename(backup)

    try:
        shutil.move(str(source), str(target))
    except OSError as exc:
        if backup.exists() and not target.exists():
            backup.rename(target)
        raise UserError(f"Failed to install {asset_name}/: {exc}") from exc

    if backup.exists():
        shutil.rmtree(backup)


def install_assets(version: str) -> None:
    """Swap extracted asset directories into game/ and record the version."""
    print("Installing assets...")
    swapped: list[str] = []

    try:
        for asset_name in ASSET_DIRS:
            if (TEMP_EXTRACT_DIR / asset_name).is_dir():
                swap_asset_directory(asset_name)
                swapped.append(asset_name)
    except UserError:
        raise
    except Exception as exc:
        raise UserError(f"Installation failed: {exc}") from exc

    if not swapped:
        raise UserError(
            "The archive did not contain any expected asset directories "
            f"({', '.join(ASSET_DIRS)})."
        )

    LOCAL_VERSION_FILE.write_text(version + "\n", encoding="utf-8")
    print(f"Installed: {', '.join(swapped)}/")


def cleanup_after_install(part_path: Path, archive_path: Path) -> None:
    """Remove temporary files after a successful install."""
    if part_path.is_file():
        part_path.unlink()
    if archive_path.is_file():
        archive_path.unlink()
    if TEMP_EXTRACT_DIR.exists():
        shutil.rmtree(TEMP_EXTRACT_DIR, ignore_errors=True)


def cleanup_on_failure(part_path: Path, archive_path: Path) -> None:
    """Remove partial downloads and temp directories after a failure."""
    if part_path.is_file():
        part_path.unlink()
        print("Removed incomplete download.")
    if archive_path.is_file():
        archive_path.unlink()
    if TEMP_EXTRACT_DIR.exists():
        shutil.rmtree(TEMP_EXTRACT_DIR, ignore_errors=True)


def main() -> None:
    base_url = validate_public_url()
    version_url = f"{base_url}/{VERSION_FILE}"

    try:
        metadata = fetch_json(version_url)
    except UserError as exc:
        fail(str(exc))

    for key in ("version", "filename", "size", "sha256"):
        if key not in metadata:
            fail(f"{VERSION_FILE} is missing required field: {key}")

    remote_version = str(metadata["version"])
    filename = str(metadata["filename"])
    expected_size = int(metadata["size"])
    expected_sha256 = str(metadata["sha256"])

    local_version = read_local_version()

    if local_version == remote_version:
        print(f"Assets are already up to date ({remote_version}).")
        return

    if local_version:
        print(f"New asset version available: {remote_version}")
        print(f"Current version: {local_version}")
    else:
        print(f"Downloading asset version {remote_version}...")

    print("\nDownloading...")
    download_url = f"{base_url}/{filename}"
    part_path = REPO_ROOT / PART_FILE

    try:
        download_file(download_url, part_path, expected_size)
        verify_checksum(part_path, expected_sha256)

        # Rename .part to final archive name for extraction.
        if ARCHIVE_PATH.is_file():
            ARCHIVE_PATH.unlink()
        part_path.rename(ARCHIVE_PATH)

        extract_archive(ARCHIVE_PATH, TEMP_EXTRACT_DIR)
        install_assets(remote_version)
        cleanup_after_install(part_path, ARCHIVE_PATH)

        if local_version:
            print(f"\nAssets successfully updated from {local_version} to {remote_version}.")
        else:
            print(f"\nAssets successfully installed (version {remote_version}).")

        print_artwork_license_notice()

    except UserError as exc:
        cleanup_on_failure(part_path, ARCHIVE_PATH)
        fail(str(exc))
    except KeyboardInterrupt:
        cleanup_on_failure(part_path, ARCHIVE_PATH)
        fail("Download cancelled.")
    except Exception as exc:
        cleanup_on_failure(part_path, ARCHIVE_PATH)
        fail(f"Unexpected error: {exc}")


if __name__ == "__main__":
    main()
