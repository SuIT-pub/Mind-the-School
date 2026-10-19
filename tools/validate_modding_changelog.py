"""Validate modding-changelog.json, the history of changes modders need to know about.

Usage:
    python tools/validate_modding_changelog.py [path]     (default: modding-changelog.json)

Prints one problem per line, prefixed with its JSON path, and exits 1 if there
are any. post_modding_changelog_discord.py refuses an invalid file, so a broken
entry stops every new post until it is fixed.
"""

import json
import re
import sys
from datetime import date

TYPES = ("breaking", "changed", "added", "deprecated", "removed", "fixed", "docs")
MAX_TITLE = 120
MAX_DETAILS = 1500
MAX_VERSION = 20
KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
# A wiki page name, optionally with an anchor: "Events" or "Events#event-flags".
WIKI = re.compile(r"^[A-Za-z0-9-]+(#[a-z0-9-]+)?$")


def _text(entry, field, limit, path, errors):
    value = entry.get(field)
    if not isinstance(value, str) or value.strip() == "":
        errors.append(f"{path}.{field}: missing or not a string")
    elif len(value) > limit:
        errors.append(f"{path}.{field}: longer than {limit} characters")


def _validate_entry(entry, path):
    errors = []
    entry_id = entry.get("id")
    if not isinstance(entry_id, str):
        errors.append(f"{path}.id: missing or not a string")
    elif not KEBAB.match(entry_id):
        errors.append(f"{path}.id: must be kebab-case")

    entry_date = entry.get("date")
    if not isinstance(entry_date, str) or not DATE.match(entry_date):
        errors.append(f"{path}.date: must be a YYYY-MM-DD date")
    else:
        try:
            date.fromisoformat(entry_date)
        except ValueError:
            errors.append(f"{path}.date: not a real date")

    version = entry.get("version")
    if not isinstance(version, str) or version == "" or len(version) > MAX_VERSION:
        errors.append(f"{path}.version: must be a string of at most {MAX_VERSION} characters")

    if entry.get("type") not in TYPES:
        errors.append(f"{path}.type: must be one of {', '.join(TYPES)}")

    _text(entry, "title", MAX_TITLE, path, errors)
    _text(entry, "details", MAX_DETAILS, path, errors)

    if "wiki" in entry and (not isinstance(entry["wiki"], str) or not WIKI.match(entry["wiki"])):
        errors.append(f'{path}.wiki: must be a wiki page name like "Events" or "Events#event-flags"')
    return errors


def validate(doc):
    """Return a list of problems; an empty list means the document is valid."""
    if not isinstance(doc, dict):
        return ["(root): must be a JSON object"]

    errors = []
    if doc.get("schemaVersion") != 1 or isinstance(doc.get("schemaVersion"), bool):
        errors.append("schemaVersion: must be 1")

    entries = doc.get("entries")
    if not isinstance(entries, list):
        return errors + ["entries: missing or not a list"]

    seen = set()
    previous_date = None
    for index, entry in enumerate(entries):
        path = f"entries[{index}]"
        if not isinstance(entry, dict):
            errors.append(f"{path}: not an object")
            continue
        errors.extend(_validate_entry(entry, path))

        entry_id = entry.get("id")
        if isinstance(entry_id, str):
            if entry_id in seen:
                errors.append(f'{path}.id: duplicate id "{entry_id}"')
            seen.add(entry_id)

        entry_date = entry.get("date")
        if isinstance(entry_date, str) and DATE.match(entry_date):
            if previous_date is not None and entry_date > previous_date:
                errors.append(f"{path}.date: entries must be newest first ({entry_date} is after {previous_date})")
            previous_date = entry_date
    return errors


def main(argv):
    path = argv[1] if len(argv) > 1 else "modding-changelog.json"
    try:
        with open(path, encoding="utf-8") as handle:
            doc = json.load(handle)
    except (OSError, json.JSONDecodeError) as error:
        print(f"{path}: {error}")
        return 1

    problems = validate(doc)
    for problem in problems:
        print(problem)
    if not problems:
        print(f"{path}: OK")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
