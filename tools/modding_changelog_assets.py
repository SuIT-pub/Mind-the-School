"""Record a published asset pack in modding-changelog.json.

upload_assets.py calls record_asset_release() after a successful upload or
version bump. Asset packs are built and published locally, never through a
commit, so no commit hook can notice them; the uploader writes the entry itself
and the next push posts it to the Discord modding channel.
"""

import json
from datetime import date
from pathlib import Path

from validate_modding_changelog import validate

REPO_ROOT = Path(__file__).resolve().parent.parent
CHANGELOG = REPO_ROOT / "modding-changelog.json"
DEVSTATUS = REPO_ROOT / "devstatus.json"

DEFAULT_DETAILS = (
    "A new asset pack is online. Run `tools/Download Assets.bat` "
    "(or `python tools/download_assets.py`) to update `game/images` before testing your mod "
    "against the current scripts."
)


def entry_id(asset_version):
    return "asset-pack-" + "".join(c if c.isalnum() else "-" for c in asset_version.lower()).strip("-")


def game_version():
    """The game version being worked toward, from devstatus.json; "unknown" if unreadable."""
    try:
        return json.loads(DEVSTATUS.read_text(encoding="utf-8"))["targetVersion"]
    except (OSError, ValueError, KeyError):
        return "unknown"


def build_entry(asset_version, note=None, today=None, version=None):
    details = DEFAULT_DETAILS
    if note:
        details = note.strip() + "\n\n" + DEFAULT_DETAILS
    return {
        "id": entry_id(asset_version),
        "date": (today or date.today()).isoformat(),
        "version": version or game_version(),
        "type": "assets",
        "title": f"Asset pack {asset_version} is out",
        "details": details,
    }


def record_asset_release(asset_version, note=None, path=CHANGELOG, today=None, version=None):
    """Prepend an asset entry to the changelog. Returns a one-line status for the console."""
    doc = json.loads(path.read_text(encoding="utf-8"))
    entry = build_entry(asset_version, note, today, version)
    if any(existing.get("id") == entry["id"] for existing in doc["entries"]):
        return f"modding-changelog.json already has {entry['id']}; left unchanged."

    doc["entries"].insert(0, entry)
    problems = validate(doc)
    if problems:
        return "modding-changelog.json NOT updated, the entry would be invalid:\n  " + "\n  ".join(problems)

    path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return (f"Added {entry['id']} to modding-changelog.json. "
            "Commit and push it to announce the pack in the Discord modding channel.")
