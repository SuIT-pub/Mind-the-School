"""Claude Code hook: after a `git commit`, remind Claude to update devstatus.json.

Wired up in .claude/settings.json as a PostToolUse hook on Bash and PowerShell.
It reads the hook payload from stdin and, when the commit that just happened
changed game/ or wiki/ files but not devstatus.json, prints a JSON response
that tells Claude to run the update-devstatus skill. In every other case it
prints nothing, so ordinary commands stay quiet.

The hook never fails a tool call: any error ends silently.
"""

import json
import re
import subprocess
import sys

WATCHED = ("game/", "wiki/")
# Pure asset drops (new renders) are not features on the roadmap.
ASSET_ONLY = re.compile(r"^game/(images|audio|gui)/")
COMMIT = re.compile(r"\bgit\b[^|;&]*\bcommit\b")

REMINDER = (
    "You just committed changes to game/ or wiki/ without touching devstatus.json. "
    "devstatus.json feeds the public roadmap on mts-game.com. Use the update-devstatus skill now: "
    "if this commit starts, finishes or changes a player-visible feature, update devstatus.json "
    "(player voice, no spoilers, nothing explicit), run python tools/validate_devstatus.py and commit it. "
    "If the commit is only a fix or internal refactor that players wouldn't notice, leave it."
)


def needs_reminder(paths):
    """True when the changed paths contain feature work but no devstatus.json update."""
    if "devstatus.json" in paths:
        return False
    relevant = [p for p in paths if p.startswith(WATCHED)]
    return any(not ASSET_ONLY.match(p) for p in relevant)


def changed_paths(cwd):
    result = subprocess.run(
        ["git", "-C", cwd, "show", "--name-only", "--format=", "HEAD"],
        capture_output=True, text=True, timeout=10,
    )
    if result.returncode != 0:
        return []
    return [line.strip().replace("\\", "/") for line in result.stdout.splitlines() if line.strip()]


def run(stdin_text):
    try:
        payload = json.loads(stdin_text)
        command = str(payload.get("tool_input", {}).get("command", ""))
        if not COMMIT.search(command):
            return ""
        if not needs_reminder(changed_paths(payload.get("cwd") or ".")):
            return ""
    except Exception:  # a reminder hook must never break the session
        return ""

    return json.dumps({
        "hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": REMINDER},
    })


if __name__ == "__main__":
    sys.stdout.write(run(sys.stdin.read()))
