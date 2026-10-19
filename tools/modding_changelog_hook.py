"""Claude Code hook: after a `git commit`, remind Claude to consider modding-changelog.json.

Wired up in .claude/settings.json as a PostToolUse hook on Bash and PowerShell,
next to devstatus_hook.py. When the commit that just happened touched game code
or the wiki but not modding-changelog.json, it prints a JSON response telling
Claude to run the update-modding-changelog skill. Otherwise it prints nothing.

The hook never fails a tool call: any error ends silently.
"""

import json
import sys

from devstatus_hook import COMMIT, changed_paths

# Code and developer docs modders build on. The asset tools change how packs are named and fetched.
WATCHED = ("game/scripts/", "game/mods/", "wiki/", "tools/upload_assets.py", "tools/download_assets.py")
# Wiki pages for players, story content, and the wiki's own plumbing are not modding API.
IGNORED = (
    "wiki/characters/", "wiki/screenshots/", "wiki/scripts/", "wiki/.wiki-repo/",
    "wiki/Home.md", "wiki/_Sidebar.md", "wiki/_Footer.md", "wiki/README.md",
    "wiki/Player-", "wiki/Walkthrough-", "wiki/Lore.md", "wiki/Roadmap.md",
)
CHANGELOG = "modding-changelog.json"

REMINDER = (
    "You just committed changes to game code, the developer wiki or the asset tools without touching "
    "modding-changelog.json. That file feeds the Discord modding channel. Use the "
    "update-modding-changelog skill now: if this commit changes something a modder builds on "
    "(registration functions, class or function signatures, condition/selector/effect behaviour, label "
    "or key names, asset naming tokens, save compatibility, the mod loader, names files), deprecates or "
    "removes something, or changes the developer docs in a way that changes how to use an API (type "
    "docs), add an entry, validate it with python tools/validate_modding_changelog.py and commit it. "
    "If modders can't notice the change (content, dialogue, art, typo fixes, internal refactor with the "
    "same API), leave it."
)


def needs_reminder(paths):
    """True when the changed paths include code or developer docs modders use, but no changelog entry."""
    if CHANGELOG in paths:
        return False
    return any(p.startswith(WATCHED) and not p.startswith(IGNORED) for p in paths)


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
