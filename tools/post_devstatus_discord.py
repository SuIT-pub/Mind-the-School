"""Mirror devstatus.json into a read-only Discord channel through a webhook.

The channel holds two messages from the webhook:
  1. the roadmap as one embed, edited in place on every update, and
  2. a short "Dev status updated" note underneath, posted fresh and the old one
     deleted each time. An edit notifies nobody; a new message marks the channel
     unread, and deleting the old note keeps the channel at exactly two messages.

The ids of both messages and the last document posted live in discord.json on
the `devstatus` branch, next to the published devstatus.json, so each run knows
which messages to touch and what changed since the last post.

Usage (GitHub Actions, see .github/workflows/publish-devstatus.yml):
    python tools/post_devstatus_discord.py devstatus.json
    python tools/post_devstatus_discord.py devstatus.json --dry-run   (print the messages, send nothing)

The webhook URL comes from the DISCORD_DEVSTATUS_WEBHOOK environment variable.
Without it the script does nothing, so forks and local runs stay quiet.
"""

import json
import os
import pathlib
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

from publish_devstatus import TARGET_BRANCH, _git, should_publish, tree_with
from validate_devstatus import validate

WEBHOOK_ENV = "DISCORD_DEVSTATUS_WEBHOOK"
STATE_FILE = "discord.json"
USER_AGENT = "DiscordBot (https://github.com/SuIT-pub/Mind-the-School, 1)"

EMBED_TITLE = "Mind the School · Dev Status"
EMBED_COLOR = 0x8B5A2B  # the journal's leather brown
DONE_SHOWN = 3
FIELD_LIMIT = 1024
EMBED_LIMIT = 6000
# Nobody gets pinged by accident if a title ever contains "@everyone".
NO_MENTIONS = {"parse": []}

SECTIONS = (
    ("now", "🔨 Working on now"),
    ("next", "⏭️ Up next"),
    ("later", "🗓️ Later"),
    ("done", "✅ Recently finished"),
)


# ---------------------------------------------------------------- formatting

def escape(text):
    """Keep roadmap text literal: a stray * or _ must not turn into Discord formatting."""
    return re.sub(r"([\\*_~`|>#\[\]])", r"\\\1", str(text))


def progress_bar(percent, width=10):
    filled = round(percent * width / 100)
    return f"`{'▰' * filled}{'▱' * (width - filled)}` {percent}%"


def item_text(item, section):
    head = f"**{escape(item['title'])}**"
    if section == "done":
        head += f" · {escape(item['doneIn'])}"
    elif item.get("version"):
        head += f" · {escape(item['version'])}"
    lines = [head, escape(item["summary"])]
    if section == "now" and "progress" in item:
        lines.append(progress_bar(item["progress"]))
    return "\n".join(lines)


def pack_fields(name, texts):
    """Embed fields holding `texts`, split into continuation fields when one would pass 1024 chars."""
    chunks, chunk = [], ""
    for text in texts:
        candidate = f"{chunk}\n\n{text}" if chunk else text
        if chunk and len(candidate) > FIELD_LIMIT:
            chunks.append(chunk)
            chunk = text
        else:
            chunk = candidate
    if chunk:
        chunks.append(chunk)
    # A zero-width space is the only "empty" name Discord accepts.
    return [{"name": name if i == 0 else "​", "value": value, "inline": False}
            for i, value in enumerate(chunks)]


def embed_size(embed):
    parts = [embed.get("title", ""), embed.get("description", ""), embed.get("footer", {}).get("text", "")]
    for field in embed["fields"]:
        parts += [field["name"], field["value"]]
    return sum(len(part) for part in parts)


def build_embed(document):
    description = f"**Working toward version {escape(document['targetVersion'])}**"
    if document.get("versionGoal"):
        description += "\n" + escape(document["versionGoal"])

    # A long roadmap first gives up finished items, which matter least to players.
    for done_shown in range(DONE_SHOWN, -1, -1):
        fields = []
        for section, name in SECTIONS:
            items = document[section][:done_shown] if section == "done" else document[section]
            if items:
                fields += pack_fields(name, [item_text(item, section) for item in items])
        embed = {
            "title": EMBED_TITLE,
            "description": description,
            "color": EMBED_COLOR,
            "fields": fields,
            "footer": {"text": f"Current version: {document['currentVersion']}"},
            "timestamp": document["updatedAt"],
        }
        if embed_size(embed) <= EMBED_LIMIT and len(fields) <= 25:
            return embed
    raise ValueError(
        "the roadmap no longer fits in one Discord embed (6000 characters, 25 fields); "
        "shorten the `later` list in devstatus.json"
    )


def describe_changes(old, new):
    """One line per change a player would care about, compared with the last posted document."""
    if not old:
        return ["📋 The dev status board is up."]

    lines = []
    if new["currentVersion"] != old.get("currentVersion"):
        lines.append(f"📦 Version {escape(new['currentVersion'])} is out.")
    if new["targetVersion"] != old.get("targetVersion"):
        lines.append(f"🎯 Now working toward version {escape(new['targetVersion'])}.")

    old_section = {item["id"]: section for section, _ in SECTIONS for item in old.get(section, [])}
    for item in new["done"]:
        if old_section.get(item["id"]) != "done":
            lines.append(f"✅ Finished: {escape(item['title'])}")
    for item in new["now"]:
        if old_section.get(item["id"]) != "now":
            lines.append(f"🔨 Started: {escape(item['title'])}")
    for section in ("next", "later"):
        for item in new[section]:
            if item["id"] not in old_section:
                lines.append(f"🆕 On the roadmap: {escape(item['title'])}")
    return lines or ["📝 Roadmap details updated."]


def build_note(document, previous):
    moment = datetime.fromisoformat(document["updatedAt"].replace("Z", "+00:00"))
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=timezone.utc)
    # <t:…:R> renders as "5 minutes ago" in each reader's own language and keeps counting.
    header = f"**Dev status updated** <t:{int(moment.timestamp())}:R>"
    return "\n".join([header, *describe_changes(previous, document)])


# ---------------------------------------------------------------- Discord

def _urllib_send(method, url, payload):
    """(status, parsed body) for one request; HTTP errors come back as statuses, not exceptions."""
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url, data=data, method=method,
        headers={"Content-Type": "application/json", "User-Agent": USER_AGENT},
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            status, body = response.status, response.read()
    except urllib.error.HTTPError as error:
        status, body = error.code, error.read()
    if not body:
        return status, None
    try:
        return status, json.loads(body)
    except json.JSONDecodeError:
        return status, body.decode("utf-8", "replace")


class Webhook:
    """The three webhook calls this script needs. Errors never echo the URL: it is the secret."""

    def __init__(self, url, send=_urllib_send, sleep=time.sleep):
        self.url = url.strip().split("?", 1)[0].rstrip("/")
        self.send = send
        self.sleep = sleep

    def _call(self, method, path, payload=None):
        for _ in range(3):
            status, body = self.send(method, self.url + path, payload)
            if status != 429:
                return status, body
            retry_after = body.get("retry_after", 1) if isinstance(body, dict) else 1
            self.sleep(float(retry_after))
        return status, body

    def post(self, payload):
        # wait=true makes Discord answer with the message, which carries the id we keep.
        status, body = self._call("POST", "?wait=true", payload)
        if status != 200:
            raise RuntimeError(f"Discord refused to post the message (HTTP {status}): {body}")
        return body["id"]

    def edit(self, message_id, payload):
        """True if edited, False if the message is gone (someone deleted it in Discord)."""
        status, body = self._call("PATCH", f"/messages/{message_id}", payload)
        if status == 404:
            return False
        if status != 200:
            raise RuntimeError(f"Discord refused to edit message {message_id} (HTTP {status}): {body}")
        return True

    def delete(self, message_id):
        status, body = self._call("DELETE", f"/messages/{message_id}")
        if status not in (204, 404):  # already gone is as good as deleted
            raise RuntimeError(f"Discord refused to delete message {message_id} (HTTP {status}): {body}")


class PrintingWebhook:
    """--dry-run stand-in: shows what would be sent."""

    def post(self, payload):
        print("POST", json.dumps(payload, indent=2, ensure_ascii=False))
        return "dry-run"

    def edit(self, message_id, payload):
        print(f"PATCH {message_id}", json.dumps(payload, indent=2, ensure_ascii=False))
        return True

    def delete(self, message_id):
        print(f"DELETE {message_id}")


def sync(document, state, webhook):
    """Bring the channel up to `document`. Returns the new state, or None if Discord is already current."""
    previous = state.get("posted")
    if previous and not should_publish(document, previous):
        return None

    roadmap = {"embeds": [build_embed(document)], "allowed_mentions": NO_MENTIONS}
    embed_id = state.get("embedMessageId")
    if not (embed_id and webhook.edit(embed_id, roadmap)):
        embed_id = webhook.post(roadmap)

    # Post before deleting: if Discord fails in between, the channel shows two notes, never none.
    note_id = webhook.post({"content": build_note(document, previous), "allowed_mentions": NO_MENTIONS})
    if state.get("noteMessageId"):
        webhook.delete(state["noteMessageId"])

    return {"embedMessageId": embed_id, "noteMessageId": note_id, "posted": document}


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


def save_state(repo, state, parent):
    text = json.dumps(state, indent=2, ensure_ascii=False) + "\n"
    blob = _git(repo, "hash-object", "-w", "--stdin", input_text=text).stdout.strip()
    tree = tree_with(repo, parent, STATE_FILE, blob)
    parent_args = ["-p", parent] if parent else []
    message = f"Record Discord dev status post ({state['posted']['updatedAt']})"
    commit = _git(repo, "commit-tree", tree, *parent_args, "-m", message).stdout.strip()
    pushed = _git(repo, "push", "-q", "origin", f"{commit}:refs/heads/{TARGET_BRANCH}", check=False)
    if pushed.returncode != 0:
        raise RuntimeError(
            f"Discord is updated, but {STATE_FILE} could not be saved to the {TARGET_BRANCH} branch:\n"
            f"{pushed.stderr.strip()}\nThe next run will post a second note; delete the older one by hand."
        )


def main(argv):
    # Windows consoles default to cp1252, which cannot print the section emoji.
    sys.stdout.reconfigure(encoding="utf-8")
    dry_run = "--dry-run" in argv[1:]
    paths = [arg for arg in argv[1:] if arg != "--dry-run"]
    if len(paths) != 1:
        print("usage: post_devstatus_discord.py <devstatus.json> [--dry-run]")
        return 2

    path = pathlib.Path(paths[0])
    document = json.loads(path.read_text(encoding="utf-8"))
    problems = validate(document)
    if problems:
        print("devstatus.json is invalid:\n" + "\n".join(problems))
        return 1

    url = os.environ.get(WEBHOOK_ENV, "").strip()
    if not url and not dry_run:
        print(f"{WEBHOOK_ENV} is not set; Discord left alone.")
        return 0

    repo = path.resolve().parent
    state, parent = load_state(repo)
    new_state = sync(document, state, PrintingWebhook() if dry_run else Webhook(url))
    if new_state is None:
        print("skipped: Discord already shows this dev status or a newer one")
    elif dry_run:
        print("dry run: nothing sent, nothing saved")
    else:
        save_state(repo, new_state, parent)
        print(f"posted: dev status {document['updatedAt']} to Discord")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
