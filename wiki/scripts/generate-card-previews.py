#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Write wiki display copies of HS2 / StudioNeoV2 character-card PNGs.

Each card is a PNG plus extra binary after IEND. The wiki pages show a sibling
``*.preview.png`` (image payload only) so browsers do not download the trailer.
The original file is never modified.

Usage:
    python wiki/scripts/generate-card-previews.py wiki/.wiki-repo/characters
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
PREVIEW_SUFFIX = ".preview.png"


def png_up_to_iend(data: bytes) -> bytes | None:
    """Return bytes through the IEND chunk, or None if the file is not a PNG.

    Args:
        data: Raw file bytes, possibly with a trailer after IEND.

    Returns:
        The well-formed PNG payload, or None when the signature or chunks
        are invalid.
    """
    if not data.startswith(PNG_SIGNATURE):
        return None
    pos = 8
    while pos + 12 <= len(data):
        length = int.from_bytes(data[pos : pos + 4], "big")
        chunk_type = data[pos + 4 : pos + 8]
        chunk_end = pos + 12 + length
        if chunk_end > len(data):
            return None
        if chunk_type == b"IEND":
            return data[:chunk_end]
        pos = chunk_end
    return None


def preview_path_for(card: Path) -> Path:
    """Return the sibling preview path for a card PNG.

    Args:
        card: Path to the original ``.png`` card.

    Returns:
        ``<stem>.preview.png`` next to ``card``.
    """
    return card.with_name(card.stem + PREVIEW_SUFFIX)


def generate_previews(root: Path) -> tuple[int, int, int]:
    """Write ``*.preview.png`` siblings for every card under ``root``.

    Args:
        root: Characters directory to walk.

    Returns:
        A tuple of (written, unchanged, skipped) counts.
    """
    written = unchanged = skipped = 0
    for path in sorted(root.rglob("*.png")):
        if path.name.endswith(PREVIEW_SUFFIX):
            continue
        data = path.read_bytes()
        payload = png_up_to_iend(data)
        if payload is None:
            print(f"skip (not a PNG): {path}", file=sys.stderr)
            skipped += 1
            continue
        dest = preview_path_for(path)
        if dest.exists() and dest.read_bytes() == payload:
            unchanged += 1
            continue
        dest.write_bytes(payload)
        written += 1
    return written, unchanged, skipped


def main(argv: list[str] | None = None) -> int:
    """Generate preview PNGs for a characters tree.

    Args:
        argv: Optional argument list; defaults to ``sys.argv[1:]``.

    Returns:
        Process exit code.
    """
    parser = argparse.ArgumentParser(
        description="Write *.preview.png siblings (PNG payload only) for character cards."
    )
    parser.add_argument(
        "characters_dir",
        type=Path,
        help="Path to the characters/ directory to process",
    )
    args = parser.parse_args(argv)
    root = args.characters_dir.resolve()
    if not root.is_dir():
        print(f"not a directory: {root}", file=sys.stderr)
        return 1
    written, unchanged, skipped = generate_previews(root)
    print(
        f"Card previews: {written} written, {unchanged} already current, {skipped} skipped"
    )
    return 1 if skipped else 0


if __name__ == "__main__":
    sys.exit(main())
