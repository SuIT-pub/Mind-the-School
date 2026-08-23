#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Download and install game assets from the public Cloudflare R2 distribution.

No authentication required. Checks the remote version against the locally
installed version and only downloads when an update is available.

Usage:
    python tools/download_assets.py
    python tools/download_assets.py --cleanup

Interrupted downloads leave ``assets.zip.part`` in place; the next run resumes
via an HTTP Range request.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
import time
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
USER_AGENT = "MTS-Asset-Downloader/1.0"

# Directories inside the archive that get swapped into game/ on install.
ASSET_DIRS = ("images", "videos")

# How downloaded files are merged into game/<dir>/.
INSTALL_MODE_KEEP = "keep-existing"
INSTALL_MODE_OVERWRITE = "overwrite-existing"
INSTALL_MODE_SWAP = "folder-swap"
INSTALL_MODES = (
    INSTALL_MODE_KEEP,
    INSTALL_MODE_OVERWRITE,
    INSTALL_MODE_SWAP,
)

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


def format_gb(num_bytes: int | float) -> str:
    """Format bytes as gigabytes with one decimal place."""
    return f"{num_bytes / (1024**3):.1f} GB"


def format_speed(bytes_per_sec: float) -> str:
    """Format a transfer rate, preferring MB/s or GB/s."""
    if bytes_per_sec >= 1024**3:
        return f"{bytes_per_sec / (1024**3):.2f} GB/s"
    return f"{bytes_per_sec / (1024**2):.1f} MB/s"


def format_duration(seconds: float) -> str:
    """Format a duration as h/m/s for ETA display."""
    if seconds <= 0 or seconds == float("inf"):
        return "--"
    total = int(seconds)
    hours, rem = divmod(total, 3600)
    minutes, secs = divmod(rem, 60)
    if hours:
        return f"{hours}h {minutes:02d}m"
    if minutes:
        return f"{minutes}m {secs:02d}s"
    return f"{secs}s"


class ProgressDisplay:
    """Single-line progress bar with speed and ETA (updates in place)."""

    def __init__(
        self,
        label: str,
        total_bytes: int,
        initial_bytes: int = 0,
    ) -> None:
        self.label = label
        self.total_bytes = max(total_bytes, 1)
        self.initial_bytes = max(initial_bytes, 0)
        self._started = time.monotonic()
        self._last_render = 0.0
        self._printed_label = False

    def update(self, current: int, force: bool = False) -> None:
        """Redraw the progress line for the given byte count."""
        now = time.monotonic()
        if not force and (now - self._last_render) < 0.25 and current < self.total_bytes:
            return
        self._last_render = now

        if not self._printed_label:
            sys.stdout.write(f"{self.label}\n")
            self._printed_label = True

        elapsed = max(now - self._started, 0.001)
        # Speed/ETA from this session only (important when resuming).
        session_bytes = max(current - self.initial_bytes, 0)
        speed = session_bytes / elapsed
        remaining = max(self.total_bytes - current, 0)
        eta = remaining / speed if speed > 0 else 0.0

        percent = min(100, int(current * 100 / self.total_bytes))
        filled = percent // 5
        bar = "#" * filled + "." * (20 - filled)
        line = (
            f"[{bar}] {percent:3d}%  "
            f"{format_gb(current)} / {format_gb(self.total_bytes)}  "
            f"{format_speed(speed)}  "
            f"ETA {format_duration(eta)}"
        )
        sys.stdout.write("\r" + line.ljust(max(len(line), 72)))
        sys.stdout.flush()

    def finish(self, current: int | None = None) -> None:
        """Force a final update and advance to the next line."""
        if current is not None:
            self.update(current, force=True)
        sys.stdout.write("\n")
        sys.stdout.flush()


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
        # Cloudflare R2's r2.dev endpoint rejects Python's default urllib User-Agent
        # with HTTP 403; always send an explicit UA.
        request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(request, timeout=60) as response:
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


def check_disk_space(required_bytes: int) -> None:
    """Ensure enough free disk space is available for the given byte budget."""
    usage = shutil.disk_usage(REPO_ROOT)
    if usage.free < required_bytes:
        raise UserError(
            f"Not enough disk space.\n"
            f"  Required: ~{format_gb(required_bytes)}\n"
            f"  Available: {format_gb(usage.free)}"
        )


def download_file(url: str, dest: Path, expected_size: int) -> None:
    """
    Stream-download a file to disk with progress display.

    Supports resume: an existing ``assets.zip.part`` smaller than ``expected_size``
    is continued via an HTTP Range request. Incomplete files are kept on network
    errors / cancel so the next run can continue.
    """
    existing = dest.stat().st_size if dest.is_file() else 0
    total = max(expected_size, 1)

    if existing > expected_size > 0:
        print(
            f"Partial file is larger than expected "
            f"({format_gb(existing)} > {format_gb(expected_size)}); starting over."
        )
        dest.unlink()
        existing = 0
    elif expected_size > 0 and existing == expected_size:
        print(f"Found complete partial download ({format_gb(existing)}); skipping transfer.")
        return
    elif existing > 0:
        print(f"Resuming download from {format_gb(existing)} / {format_gb(expected_size)}...")

    headers = {"User-Agent": USER_AGENT}
    if existing > 0:
        headers["Range"] = f"bytes={existing}-"

    downloaded = existing
    progress: ProgressDisplay | None = None

    try:
        request = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(request, timeout=60) as response:
            status = getattr(response, "status", None) or response.getcode()
            mode = "ab"

            if existing > 0 and status == 200:
                print("Server does not support resume; restarting download from the beginning.")
                existing = 0
                downloaded = 0
                mode = "wb"
            elif existing > 0 and status == 206:
                mode = "ab"
            elif existing > 0:
                raise UserError(
                    f"Unexpected HTTP status {status} when resuming download.\n"
                    "Run with --cleanup and try again."
                )
            else:
                mode = "wb"

            content_range = response.headers.get("Content-Range")
            content_length = response.headers.get("Content-Length")
            if content_range and "/" in content_range:
                total_token = content_range.rsplit("/", 1)[-1]
                if total_token.isdigit():
                    total = int(total_token)
            elif content_length:
                length = int(content_length)
                total = length if mode == "wb" else existing + length
            elif expected_size > 0:
                total = expected_size

            if expected_size > 0 and total > 0 and total != expected_size:
                print(
                    f"WARNING: remote size ({format_gb(total)}) differs from "
                    f"version.json ({format_gb(expected_size)})."
                )

            # Free space for the remaining download plus a full extract buffer.
            remaining = max(total - existing, 0)
            check_disk_space(remaining + total)

            label = (
                f"Resuming {ARCHIVE_NAME}"
                if existing > 0 and mode == "ab"
                else f"Downloading {ARCHIVE_NAME}"
            )
            progress = ProgressDisplay(label, total, initial_bytes=existing)

            with dest.open(mode) as handle:
                while True:
                    chunk = response.read(CHUNK_SIZE)
                    if not chunk:
                        break
                    handle.write(chunk)
                    downloaded += len(chunk)
                    progress.update(downloaded)

        if progress is not None:
            progress.finish(downloaded)
        else:
            sys.stdout.write("\n")
            sys.stdout.flush()

        if expected_size > 0 and downloaded != expected_size:
            raise UserError(
                f"Download size mismatch.\n"
                f"  expected: {expected_size} bytes\n"
                f"  actual:   {downloaded} bytes\n"
                "Run the script again to resume, or use --cleanup to start over."
            )

    except UserError:
        raise
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            raise UserError(f"Could not find {ARCHIVE_NAME} at {url} (HTTP 404).") from exc
        if exc.code == 403:
            raise UserError(f"Access denied when downloading {ARCHIVE_NAME} (HTTP 403).") from exc
        if exc.code == 416:
            # Invalid range — partial file is inconsistent; force a clean retry.
            if dest.is_file():
                dest.unlink()
            raise UserError(
                "Could not resume download (invalid byte range).\n"
                "The partial file was removed; run the script again to start over."
            ) from exc
        raise UserError(f"HTTP error {exc.code} while downloading {ARCHIVE_NAME}.") from exc
    except urllib.error.URLError as exc:
        raise UserError(
            "Download interrupted or connection failed.\n"
            "Your partial download was kept. Run the script again to resume."
        ) from exc
    except OSError as exc:
        if exc.errno == 28 or "No space" in str(exc):
            raise UserError(
                "Not enough disk space to complete the download.\n"
                "Free some space, then run the script again to resume."
            ) from exc
        raise UserError(f"Failed to write download file: {exc}") from exc


def compute_sha256(file_path: Path) -> str:
    """Compute SHA-256 hash of a file using chunked reads with progress."""
    digest = hashlib.sha256()
    total = file_path.stat().st_size
    processed = 0
    progress = ProgressDisplay("Verifying SHA-256 checksum...", max(total, 1))

    with file_path.open("rb") as handle:
        while chunk := handle.read(CHUNK_SIZE):
            digest.update(chunk)
            processed += len(chunk)
            progress.update(processed)

    progress.finish(processed)
    return digest.hexdigest()


def verify_checksum(file_path: Path, expected: str) -> None:
    """Verify the SHA-256 checksum of a downloaded file."""
    actual = compute_sha256(file_path)
    print(f"  expected: {expected}")
    print(f"  actual:   {actual}")
    if actual != expected:
        if file_path.is_file():
            file_path.unlink()
        raise UserError(
            "SHA-256 checksum mismatch.\n"
            "The downloaded archive may be corrupted and was removed.\n"
            "Run the script again to download a fresh copy."
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
    """Replace game/<asset_name>/ entirely with the extracted directory."""
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


def merge_asset_directory(asset_name: str, mode: str) -> tuple[int, int, int]:
    """
    Merge extracted files into game/<asset_name>/.

    Returns ``(added, skipped, overwritten)`` counts.
    """
    source_root = TEMP_EXTRACT_DIR / asset_name
    if not source_root.is_dir():
        return (0, 0, 0)

    target_root = GAME_DIR / asset_name
    target_root.mkdir(parents=True, exist_ok=True)

    added = 0
    skipped = 0
    overwritten = 0

    try:
        for source_file in source_root.rglob("*"):
            if not source_file.is_file():
                continue
            rel = source_file.relative_to(source_root)
            dest_file = target_root / rel
            dest_file.parent.mkdir(parents=True, exist_ok=True)

            if dest_file.exists():
                if mode == INSTALL_MODE_KEEP:
                    skipped += 1
                    continue
                # overwrite-existing
                shutil.copy2(source_file, dest_file)
                overwritten += 1
            else:
                shutil.copy2(source_file, dest_file)
                added += 1
    except OSError as exc:
        raise UserError(f"Failed to merge into {asset_name}/: {exc}") from exc

    return (added, skipped, overwritten)


def install_assets(version: str, mode: str) -> None:
    """Install extracted asset directories into game/ using the chosen merge mode."""
    print(f"Installing assets (mode: {mode})...")
    installed: list[str] = []
    total_added = 0
    total_skipped = 0
    total_overwritten = 0

    try:
        for asset_name in ASSET_DIRS:
            if not (TEMP_EXTRACT_DIR / asset_name).is_dir():
                continue
            if mode == INSTALL_MODE_SWAP:
                swap_asset_directory(asset_name)
                print(f"  Replaced game/{asset_name}/")
            else:
                added, skipped, overwritten = merge_asset_directory(asset_name, mode)
                total_added += added
                total_skipped += skipped
                total_overwritten += overwritten
                print(
                    f"  game/{asset_name}/: "
                    f"+{added} added, {skipped} kept local, {overwritten} overwritten"
                )
            installed.append(asset_name)
    except UserError:
        raise
    except Exception as exc:
        raise UserError(f"Installation failed: {exc}") from exc

    if not installed:
        raise UserError(
            "The archive did not contain any expected asset directories "
            f"({', '.join(ASSET_DIRS)})."
        )

    LOCAL_VERSION_FILE.write_text(version + "\n", encoding="utf-8")
    if mode == INSTALL_MODE_SWAP:
        print(f"Installed (folder swap): {', '.join(installed)}/")
    else:
        print(
            f"Installed (merge): {', '.join(installed)}/ — "
            f"+{total_added} added, {total_skipped} kept local, "
            f"{total_overwritten} overwritten"
        )


def cleanup_after_install(part_path: Path, archive_path: Path) -> None:
    """Remove temporary files after a successful install."""
    if part_path.is_file():
        part_path.unlink()
    if archive_path.is_file():
        archive_path.unlink()
    if TEMP_EXTRACT_DIR.exists():
        shutil.rmtree(TEMP_EXTRACT_DIR, ignore_errors=True)


def cleanup_on_failure(
    part_path: Path,
    archive_path: Path,
    *,
    keep_partial_download: bool = False,
) -> None:
    """
    Remove temp extract/archive artefacts after a failure.

    When ``keep_partial_download`` is True (network drop / Ctrl+C during transfer),
    ``assets.zip.part`` is kept so the next run can resume via HTTP Range.
    """
    if keep_partial_download and part_path.is_file():
        size = part_path.stat().st_size
        print(
            f"Partial download kept for resume: {part_path.name} "
            f"({format_gb(size)})."
        )
    elif part_path.is_file():
        part_path.unlink()
        print("Removed incomplete download.")

    if archive_path.is_file() and not keep_partial_download:
        archive_path.unlink()

    if TEMP_EXTRACT_DIR.exists():
        shutil.rmtree(TEMP_EXTRACT_DIR, ignore_errors=True)


def cleanup_leftovers() -> int:
    """
    Remove leftover download/install artefacts from failed or interrupted runs.

    Does not touch an installed ``game/images/`` tree or ``game/.asset-version``.
    Returns the number of paths removed.
    """
    removed = 0
    candidates: list[Path] = [
        REPO_ROOT / PART_FILE,
        ARCHIVE_PATH,
        TEMP_EXTRACT_DIR,
    ]
    for asset_name in ASSET_DIRS:
        candidates.append(GAME_DIR / f"{asset_name}.old")

    for path in candidates:
        if path.is_file():
            path.unlink()
            print(f"  Removed file: {path.relative_to(REPO_ROOT)}")
            removed += 1
        elif path.is_dir():
            shutil.rmtree(path)
            print(f"  Removed directory: {path.relative_to(REPO_ROOT)}")
            removed += 1

    return removed


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description=(
            "Download and install Mind the School game assets from the public "
            "Cloudflare R2 distribution."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Install modes (--mode):\n"
            f"  {INSTALL_MODE_KEEP}       Keep local files; only add missing ones from the cloud (default).\n"
            f"  {INSTALL_MODE_OVERWRITE}  Cloud files overwrite locals; local-only files remain.\n"
            f"  {INSTALL_MODE_SWAP}         Replace game/images/ (etc.) entirely with the archive."
        ),
    )
    parser.add_argument(
        "--cleanup",
        action="store_true",
        help=(
            "Remove leftover temporary files from failed or interrupted downloads "
            "(assets.zip.part, assets.zip, .temp_assets/, game/images.old/) "
            "and exit without downloading. Does not remove installed assets."
        ),
    )
    parser.add_argument(
        "--mode",
        choices=INSTALL_MODES,
        default=INSTALL_MODE_KEEP,
        help=(
            "How to merge downloaded files into game/ "
            f"(default: {INSTALL_MODE_KEEP})."
        ),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.cleanup:
        print("Cleaning leftover download/install files...")
        count = cleanup_leftovers()
        if count == 0:
            print("Nothing to clean.")
        else:
            print(f"Removed {count} leftover path(s).")
        return

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

    print(f"Install mode: {args.mode}")
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
        install_assets(remote_version, args.mode)
        cleanup_after_install(part_path, ARCHIVE_PATH)

        if local_version:
            print(f"\nAssets successfully updated from {local_version} to {remote_version}.")
        else:
            print(f"\nAssets successfully installed (version {remote_version}).")

        print_artwork_license_notice()

    except UserError as exc:
        # Network / disk errors during transfer keep the .part file for resume.
        keep_partial = "run the script again to resume" in str(exc).lower()
        cleanup_on_failure(
            part_path,
            ARCHIVE_PATH,
            keep_partial_download=keep_partial,
        )
        fail(str(exc))
    except KeyboardInterrupt:
        cleanup_on_failure(
            part_path,
            ARCHIVE_PATH,
            keep_partial_download=True,
        )
        fail(
            "Download cancelled.\n"
            "Your partial download was kept. Run the script again to resume."
        )
    except Exception as exc:
        cleanup_on_failure(part_path, ARCHIVE_PATH, keep_partial_download=False)
        fail(f"Unexpected error: {exc}")


if __name__ == "__main__":
    main()
