"""Validate devstatus.json, the file that feeds the roadmap on mts-game.com.

Usage:
    python tools/validate_devstatus.py [path]     (default: devstatus.json)

Prints one problem per line, prefixed with its JSON path, and exits 1 if
there are any. The website runs the same rules (src/Sources/DevStatusValidator.php
in the website repo); if the site finds the file invalid it keeps showing the
last valid version, so a broken file silently freezes the public roadmap.
Change both validators together.
"""

import json
import re
import sys
from datetime import datetime

LISTS = ("now", "next", "later", "done")
MAX_TITLE = 60
MAX_SUMMARY = 160
MAX_DONE = 10
MAX_VERSION = 20
MAX_GOAL = 240
KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _is_int(value):
    return isinstance(value, int) and not isinstance(value, bool)


def _validate_item(item, path, is_done):
    errors = []
    item_id = item.get("id")
    if not isinstance(item_id, str):
        errors.append(f"{path}.id: missing or not a string")
    elif not KEBAB.match(item_id):
        errors.append(f"{path}.id: must be kebab-case")

    for field, limit in (("title", MAX_TITLE), ("summary", MAX_SUMMARY)):
        value = item.get(field)
        if not isinstance(value, str) or value == "":
            errors.append(f"{path}.{field}: missing or not a string")
        elif len(value) > limit:
            errors.append(f"{path}.{field}: longer than {limit} characters")

    if "version" in item:
        version = item["version"]
        if not isinstance(version, str) or version == "" or len(version) > MAX_VERSION:
            errors.append(f"{path}.version: must be a string of at most {MAX_VERSION} characters")

    if "progress" in item:
        progress = item["progress"]
        if not _is_int(progress) or not 0 <= progress <= 100:
            errors.append(f"{path}.progress: must be an integer from 0 to 100")

    if is_done:
        if not isinstance(item.get("doneIn"), str):
            errors.append(f"{path}.doneIn: missing or not a string")
        done_at = item.get("doneAt")
        if not isinstance(done_at, str) or not DATE.match(done_at):
            errors.append(f"{path}.doneAt: must be a YYYY-MM-DD date")
    return errors


def validate(doc):
    """Return a list of problems; an empty list means the document is valid."""
    if not isinstance(doc, dict):
        return ["(root): must be a JSON object"]

    errors = []
    if doc.get("schemaVersion") != 1 or isinstance(doc.get("schemaVersion"), bool):
        errors.append("schemaVersion: must be 1")
    for key in ("updatedAt", "currentVersion", "targetVersion"):
        if not isinstance(doc.get(key), str) or doc.get(key) == "":
            errors.append(f"{key}: missing or not a string")
    if isinstance(doc.get("updatedAt"), str):
        try:
            datetime.fromisoformat(doc["updatedAt"].replace("Z", "+00:00"))
        except ValueError:
            errors.append("updatedAt: not a valid date")
    if "versionGoal" in doc:
        goal = doc["versionGoal"]
        if not isinstance(goal, str) or goal.strip() == "" or len(goal) > MAX_GOAL:
            errors.append(f"versionGoal: must be text of at most {MAX_GOAL} characters")

    seen = set()
    for name in LISTS:
        items = doc.get(name)
        if not isinstance(items, list):
            errors.append(f"{name}: missing or not a list")
            continue
        if name == "done" and len(items) > MAX_DONE:
            errors.append(f"done: more than {MAX_DONE} entries")
        for index, item in enumerate(items):
            path = f"{name}[{index}]"
            if not isinstance(item, dict):
                errors.append(f"{path}: not an object")
                continue
            errors.extend(_validate_item(item, path, name == "done"))
            item_id = item.get("id")
            if isinstance(item_id, str):
                if item_id in seen:
                    errors.append(f'{path}.id: duplicate id "{item_id}"')
                seen.add(item_id)
    return errors


def main(argv):
    path = argv[1] if len(argv) > 1 else "devstatus.json"
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
