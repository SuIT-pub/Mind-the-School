#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Replace the wiki's outfit cards with the ones from a Honey Select 2 folder.

The source is LO's HS2 coordinate folder (``UserData/coordinate/female/…``).
Every character folder in it whose name matches a wiki character (see
``FOLDER_ALIASES`` for spelling drift) replaces that character's
``wiki/characters/<Slug>/outfits/`` cards and the ``## Outfits`` section of the
page. Pages without a matching folder (the Headmaster's cards are male
coordinates and live elsewhere) are left alone.

Cards are named ``<First>_<Last>_<Category>[_<NN>]``, e.g.
``Adelaide_Hall_Cafeteria_04.png`` or ``Luna_Clark_Christmas.png``. Uniform
and cafeteria numbers are school levels; any other number is just a count.

Unrenamed ``HS2CoordeF_*`` cards are skipped, with one fallback: a level folder
(``Uniform``, ``Cafeteria``, …) that holds no renamed card at all takes its
level from the name stored inside the card ("Uniform 03", "Level 00 Var 1").
That keeps characters whose cards were never renamed on the page without
pulling in drafts that sit next to renamed cards. Every skipped card is
listed, so nothing disappears silently.

Files are copied byte-for-byte under their original names: the HS2 trailer
after the PNG payload must stay intact (see ``wiki/README.md``).

Usage:
    python wiki/scripts/import-outfit-cards.py "D:/Honey Select/UserData/coordinate/female/Mind the School"
    python wiki/scripts/import-outfit-cards.py <source> --dry-run
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote

WIKI_DIR = Path(__file__).resolve().parent.parent
CHARACTERS_DIR = WIKI_DIR / "characters"
RAW_BASE = "https://raw.githubusercontent.com/wiki/SuIT-pub/Mind-the-School/characters"
PREVIEW_SUFFIX = ".preview.png"
COLUMNS = 4
THUMB_WIDTH = 160

# HS2 folder name -> wiki slug, where the folder is spelled differently.
FOLDER_ALIASES = {
    "Seraphine Clark": "Seraphina-Clark",
}

# Card category -> (page section, whether the number is a school level).
# Staff keep their level outfits in "Normal" folders/cards.
CATEGORY_SECTIONS = {
    "uniform": ("Uniforms", True),
    "normal": ("Uniforms", True),
    "cafeteria": ("Cafeteria", True),
    "pajama": ("Pajamas", False),
    "bathwear": ("Bathwear", False),
    "casual": ("Casual", False),
    "party": ("Party", False),
}
OTHER_SECTION = "Other"
SECTION_ORDER = ["Uniforms", "Cafeteria", "Pajamas", "Bathwear", "Casual", "Party", OTHER_SECTION]

# First_Last_Category[_NN]; the name part is ignored (typos like "Fonola" exist).
NAMED_CARD = re.compile(r"^[^_]+_[^_]+_(?P<category>[A-Za-z]+)(?:_(?P<number>\d+))?$")
EMBEDDED_LEVEL = re.compile(r"(?:Level|Uniform|Cafeteria)\s*(?P<number>\d+)", re.IGNORECASE)

NAV_LINE = re.compile(r"^\| \[<kbd>", re.MULTILINE)


@dataclass(frozen=True)
class OutfitCard:
    """One coordinate card destined for a character page."""

    source: Path
    section: str
    label: str
    sort_key: tuple


def png_end(data: bytes) -> int | None:
    """Return the offset just past IEND, or None for a malformed PNG."""
    pos = 8
    while pos + 12 <= len(data):
        length = int.from_bytes(data[pos : pos + 4], "big")
        chunk_end = pos + 12 + length
        if data[pos + 4 : pos + 8] == b"IEND":
            return chunk_end
        pos = chunk_end
    return None


def read_dotnet_string(data: bytes, pos: int) -> tuple[str, int]:
    """Read a .NET BinaryWriter string (7-bit encoded length prefix)."""
    length = shift = 0
    while True:
        byte = data[pos]
        pos += 1
        length |= (byte & 0x7F) << shift
        shift += 7
        if byte < 0x80:
            break
    return data[pos : pos + length].decode("utf-8", "replace"), pos + length


def embedded_coordinate_name(path: Path) -> str:
    """Return the outfit name HS2 stored in the card, or '' if unreadable.

    Layout after IEND: int32 product number, header string, version string,
    int32 language, coordinate name string.
    """
    data = path.read_bytes()
    pos = png_end(data)
    if pos is None:
        return ""
    try:
        pos += 4
        _header, pos = read_dotnet_string(data, pos)
        _version, pos = read_dotnet_string(data, pos)
        pos += 4
        name, _ = read_dotnet_string(data, pos)
    except IndexError:
        return ""
    return name


def describe(category: str, number: str | None) -> tuple[str, str]:
    """Map a card category and number to (section, label)."""
    section, numbered_by_level = CATEGORY_SECTIONS.get(category.lower(), (OTHER_SECTION, False))
    if number is None:
        return section, category
    if numbered_by_level:
        return section, f"Level {int(number):02d}"
    return section, f"{category} {int(number):02d}"


def collect_cards(folder: Path) -> tuple[list[OutfitCard], list[str]]:
    """Return the cards for one character folder plus notes on skipped ones."""
    named: list[OutfitCard] = []
    unnamed: list[Path] = []
    for path in sorted(folder.rglob("*.png")):
        match = NAMED_CARD.match(path.stem)
        if match is None or path.stem.startswith("HS2Coorde"):
            unnamed.append(path)
            continue
        category, number = match["category"], match["number"]
        section, label = describe(category, number)
        named.append(OutfitCard(path, section, label, (category.lower(), int(number or 0))))

    named_sections = {card.section for card in named}
    cards = list(named)
    skipped: list[str] = []
    for path in unnamed:
        folder_category = path.parent.name.lower()
        section_info = CATEGORY_SECTIONS.get(folder_category)
        embedded = embedded_coordinate_name(path)
        level = EMBEDDED_LEVEL.search(embedded)
        if section_info and section_info[1] and section_info[0] not in named_sections and level:
            section, label = describe(path.parent.name, level["number"])
            cards.append(OutfitCard(path, section, label, (folder_category, int(level["number"]))))
            continue
        relative = path.relative_to(folder).as_posix()
        skipped.append(f"{relative} (card name: {embedded or '?'})")

    seen: dict[tuple[str, str], Path] = {}
    for card in cards:
        key = (card.section, card.label)
        if key in seen:
            raise SystemExit(
                f"Two cards would both show as '{card.label}' under {card.section}:\n"
                f"  {seen[key]}\n  {card.source}\nRename one of them in the HS2 folder."
            )
        seen[key] = card.source
    return cards, skipped


def find_character_folders(source: Path, slugs: set[str]) -> dict[str, Path]:
    """Map wiki slugs to the HS2 folder holding that character's cards."""
    found: dict[str, Path] = {}
    for folder in sorted(p for p in source.rglob("*") if p.is_dir()):
        slug = FOLDER_ALIASES.get(folder.name, folder.name.replace(" ", "-"))
        if slug not in slugs:
            continue
        if slug in found:
            raise SystemExit(f"Two HS2 folders match {slug}: {found[slug]} and {folder}")
        found[slug] = folder
    return found


def card_cell(slug: str, display_name: str, card: OutfitCard) -> str:
    """Render one linked thumbnail cell."""
    file_name = quote(card.source.name)
    preview_name = quote(card.source.stem + PREVIEW_SUFFIX)
    href = f"{RAW_BASE}/{slug}/outfits/{file_name}"
    src = f"{RAW_BASE}/{slug}/outfits/{preview_name}"
    return (
        f'<a href="{href}"><img src="{src}" alt="{display_name} — {card.label}" '
        f'width="{THUMB_WIDTH}"></a>'
    )


def render_outfits(slug: str, cards: list[OutfitCard]) -> str:
    """Render the full ``## Outfits`` section (without the nav line after it)."""
    display_name = slug.replace("-", " ")
    lines = ["## Outfits", "", "Click an image to open the original coordinate card.", ""]
    for section in SECTION_ORDER:
        in_section = sorted((c for c in cards if c.section == section), key=lambda c: c.sort_key)
        if not in_section:
            continue
        lines += [f"### {section}", ""]
        for start in range(0, len(in_section), COLUMNS):
            row = in_section[start : start + COLUMNS]
            lines.append("| " + " | ".join(c.label for c in row) + " |")
            lines.append("|" + ":---:|" * len(row))
            lines.append("| " + " | ".join(card_cell(slug, display_name, c) for c in row) + " |")
            lines.append("")
    return "\n".join(lines)


def replace_outfits_section(page: Path, new_section: str) -> None:
    """Swap the page's ``## Outfits`` block for ``new_section``.

    The block runs to the next ``## `` heading or the prev/next nav table,
    whichever comes first; a page without one gets the section before the nav.
    """
    text = page.read_text(encoding="utf-8")
    start = text.find("\n## Outfits\n")
    nav = NAV_LINE.search(text)
    if start == -1:
        if nav is None:
            raise SystemExit(f"{page.name}: no '## Outfits' heading and no nav table to insert before.")
        text = text[: nav.start()] + new_section + "\n" + text[nav.start() :]
    else:
        start += 1
        next_heading = text.find("\n## ", start + 1)
        ends = [pos + 1 for pos in (next_heading,) if pos != -1]
        nav_after = NAV_LINE.search(text, start)
        if nav_after:
            ends.append(nav_after.start())
        end = min(ends) if ends else len(text)
        text = text[:start] + new_section + "\n" + text[end:]
    page.write_text(text, encoding="utf-8", newline="\n")


def replace_cards(outfits_dir: Path, cards: list[OutfitCard]) -> None:
    """Delete the old cards (and their previews) and copy the new ones in."""
    outfits_dir.mkdir(exist_ok=True)
    for old in outfits_dir.glob("*.png"):
        old.unlink()
    for card in cards:
        # copyfile, not copy2/convert: the HS2 trailer must survive untouched.
        shutil.copyfile(card.source, outfits_dir / card.source.name)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("source", type=Path, help="HS2 coordinate folder with one subfolder per character")
    parser.add_argument("--dry-run", action="store_true", help="report what would change, write nothing")
    args = parser.parse_args(argv)
    sys.stdout.reconfigure(encoding="utf-8")

    source = args.source.resolve()
    if not source.is_dir():
        print(f"not a directory: {source}", file=sys.stderr)
        return 1

    slugs = {p.name for p in CHARACTERS_DIR.iterdir() if (p / f"{p.name}.md").is_file()}
    folders = find_character_folders(source, slugs)

    for slug in sorted(slugs - folders.keys()):
        print(f"{slug}: no HS2 folder, page left unchanged")

    for slug, folder in sorted(folders.items()):
        cards, skipped = collect_cards(folder)
        if not cards:
            print(f"{slug}: no usable cards in {folder}, page left unchanged")
            continue
        sections = {}
        for card in cards:
            sections[card.section] = sections.get(card.section, 0) + 1
        summary = ", ".join(f"{name} {sections[name]}" for name in SECTION_ORDER if name in sections)
        print(f"{slug}: {len(cards)} cards ({summary})")
        for note in skipped:
            print(f"    skipped {note}")
        if args.dry_run:
            continue
        character_dir = CHARACTERS_DIR / slug
        replace_cards(character_dir / "outfits", cards)
        replace_outfits_section(character_dir / f"{slug}.md", render_outfits(slug, cards))
    return 0


if __name__ == "__main__":
    sys.exit(main())
