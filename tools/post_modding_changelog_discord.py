"""Post new modding-changelog.json entries to the Discord modding channel through a webhook.

Each entry is posted once, as its own message (one embed), oldest first so the
channel reads in order. Nothing is ever edited or deleted: the channel is the
history. Correcting a posted entry means adding a new one.

Which ids were already posted lives in modding-discord.json on the `devstatus`
branch, next to devstatus.json and discord.json. That makes the posts
branch-independent: an entry pushed from a feature branch and later merged into
master is still posted only once.

Usage (GitHub Actions, see .github/workflows/post-modding-changelog.yml):
    python tools/post_modding_changelog_discord.py modding-changelog.json
    python tools/post_modding_changelog_discord.py modding-changelog.json --dry-run

The webhook URL comes from the DISCORD_MODDING_WEBHOOK environment variable.
Without it the script does nothing, so forks and local runs stay quiet.
"""

import json
import os
import pathlib
import sys

from post_devstatus_discord import NO_MENTIONS, PrintingWebhook, Webhook
from publish_devstatus import TARGET_BRANCH, _git, tree_with
from validate_modding_changelog import validate

WEBHOOK_ENV = "DISCORD_MODDING_WEBHOOK"
STATE_FILE = "modding-discord.json"
WIKI_URL = "https://github.com/SuIT-pub/Mind-the-School/wiki/"
FOOTER = "Mind the School · Modding changelog"

# (label, colour) per entry type. Breaking is red so it can't be skimmed past.
TYPE_STYLE = {
    "breaking": ("⚠️ Breaking change", 0xC0392B),
    "changed": ("🔧 Changed", 0xE67E22),
    "added": ("✨ Added", 0x2E8B57),
    "deprecated": ("🕰️ Deprecated", 0xD4AC0D),
    "removed": ("🗑️ Removed", 0x7F8C8D),
    "fixed": ("🩹 Fixed", 0x2980B9),
    "docs": ("📘 Docs", 0x5D6D7E),
    "assets": ("📦 Asset pack", 0x8B5A2B),
}


def wiki_link(page):
    return WIKI_URL + page


def build_message(entry):
    label, color = TYPE_STYLE[entry["type"]]
    description = entry["details"]
    if entry.get("wiki"):
        page = entry["wiki"].split("#", 1)[0].replace("-", " ")
        description += f"\n\n📖 Wiki: [{page}]({wiki_link(entry['wiki'])})"
    # An entry has a day, not a time. As an embed timestamp the day became midnight UTC,
    # which Discord shows in each reader's zone (02:00 in Germany), so the date goes in the footer.
    embed = {
        "author": {"name": f"{label} · {entry['version']}"},
        "title": entry["title"],
        "description": description,
        "color": color,
        "footer": {"text": f"{FOOTER} · {entry['date']}"},
    }
    if entry.get("wiki"):
        embed["url"] = wiki_link(entry["wiki"])
    return {"embeds": [embed], "allowed_mentions": NO_MENTIONS}


def pending_entries(document, posted_ids):
    """Entries not posted yet, oldest first (the file lists newest first)."""
    posted = set(posted_ids)
    return [entry for entry in reversed(document["entries"]) if entry["id"] not in posted]


def post_pending(document, state, webhook):
    """Post every pending entry. Returns (new state, ids posted now).

    If Discord fails midway, the error is raised with the state of what did get
    posted attached (`error.state`), so the caller can still record it and the
    next run doesn't post those entries twice.
    """
    posted_ids = list(state.get("postedIds", []))
    new_ids = []
    for entry in pending_entries(document, posted_ids):
        try:
            webhook.post(build_message(entry))
        except Exception as error:
            error.state = {"postedIds": posted_ids}
            error.posted_now = new_ids
            raise
        posted_ids.append(entry["id"])
        new_ids.append(entry["id"])
    return {"postedIds": posted_ids}, new_ids


# ---------------------------------------------------------------- state on the devstatus branch

def load_state(repo):
    """(state, devstatus branch commit) — an empty state when nothing was posted yet."""
    if _git(repo, "fetch", "-q", "origin", TARGET_BRANCH, check=False).returncode != 0:
        return {}, None
    head = _git(repo, "rev-parse", "FETCH_HEAD").stdout.strip()
    shown = _git(repo, "show", f"{head}:{STATE_FILE}", check=False)
    if shown.returncode != 0:
        return {}, head
    try:
        return json.loads(shown.stdout), head
    except json.JSONDecodeError:
        return {}, head


def save_state(repo, state, parent, new_ids):
    text = json.dumps(state, indent=2, ensure_ascii=False) + "\n"
    blob = _git(repo, "hash-object", "-w", "--stdin", input_text=text).stdout.strip()
    tree = tree_with(repo, parent, STATE_FILE, blob)
    parent_args = ["-p", parent] if parent else []
    message = f"Record modding changelog posts: {', '.join(new_ids)}"
    commit = _git(repo, "commit-tree", tree, *parent_args, "-m", message).stdout.strip()
    pushed = _git(repo, "push", "-q", "origin", f"{commit}:refs/heads/{TARGET_BRANCH}", check=False)
    if pushed.returncode != 0:
        raise RuntimeError(
            f"Discord is updated, but {STATE_FILE} could not be saved to the {TARGET_BRANCH} branch:\n"
            f"{pushed.stderr.strip()}\nThe next run will post these entries again: {', '.join(new_ids)}"
        )


def main(argv):
    # Windows consoles default to cp1252, which cannot print the type emoji.
    sys.stdout.reconfigure(encoding="utf-8")
    dry_run = "--dry-run" in argv[1:]
    paths = [arg for arg in argv[1:] if arg != "--dry-run"]
    if len(paths) != 1:
        print("usage: post_modding_changelog_discord.py <modding-changelog.json> [--dry-run]")
        return 2

    path = pathlib.Path(paths[0])
    document = json.loads(path.read_text(encoding="utf-8"))
    problems = validate(document)
    if problems:
        print("modding-changelog.json is invalid:\n" + "\n".join(problems))
        return 1

    url = os.environ.get(WEBHOOK_ENV, "").strip()
    if not url and not dry_run:
        print(f"{WEBHOOK_ENV} is not set; Discord left alone.")
        return 0

    repo = path.resolve().parent
    state, parent = load_state(repo)

    if dry_run:
        _, new_ids = post_pending(document, state, PrintingWebhook())
        print(f"dry run: would post {len(new_ids)} entr{'y' if len(new_ids) == 1 else 'ies'}, nothing sent")
        return 0

    try:
        new_state, new_ids = post_pending(document, state, Webhook(url))
    except Exception as error:
        if getattr(error, "posted_now", None):
            save_state(repo, error.state, parent, error.posted_now)
        raise

    if not new_ids:
        print("skipped: every entry is already in the Discord channel")
        return 0
    save_state(repo, new_state, parent, new_ids)
    print(f"posted: {', '.join(new_ids)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
