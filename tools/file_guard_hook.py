"""Claude Code hook: guard files Claude must not write, and check names files after edits.

Wired up in .claude/settings.json on Edit|Write:

- `pre`  (PreToolUse): denies writes to compiled Ren'Py files (*.rpyc — Ren'Py
  regenerates them, so a hand edit is lost on the next start) and to secrets
  (.env, *.keystore). .env.example stays writable.
- `post` (PostToolUse): after translations.csv or a mod's names.csv changed, runs
  tools/validate_names.py and feeds any error back to Claude.

Ordinary files produce no output. The hook never fails a tool call by crashing:
an unexpected error ends silently.
"""

import json
import os
import subprocess
import sys
from pathlib import PurePath

NAMES_FILES = ("translations.csv", "names.csv")


def blocked_reason(path):
    """Why Claude may not write `path`, or None when it may."""
    name = PurePath(path.replace("\\", "/")).name.lower()
    if name.endswith(".rpyc"):
        return (f"{name} is compiled by Ren'Py from its .rpy and is overwritten on the next start. "
                "Edit the .rpy instead.")
    if name == ".env":
        return ".env holds local secrets (API keys, webhook URLs). Ask LO to change it by hand."
    if name.endswith(".keystore"):
        return f"{name} is an Android signing keystore. Never write it."
    return None


def is_names_file(path):
    return PurePath(path.replace("\\", "/")).name.lower() in NAMES_FILES


def target_path(payload):
    tool_input = payload.get("tool_input") or {}
    return tool_input.get("file_path") or tool_input.get("path") or ""


def run_pre(payload):
    reason = blocked_reason(target_path(payload))
    if reason is None:
        return None
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }


def run_post(payload, project_dir):
    if not is_names_file(target_path(payload)):
        return None
    script = os.path.join(project_dir, "tools", "validate_names.py")
    result = subprocess.run(
        [sys.executable, script],
        capture_output=True, text=True, timeout=60, cwd=project_dir,
    )
    if result.returncode == 0:
        return None
    output = (result.stdout + result.stderr).strip()
    return {
        "decision": "block",
        "reason": "tools/validate_names.py failed after this edit. Fix the names file:\n" + output,
    }


def main(argv):
    mode = argv[0] if argv else ""
    try:
        payload = json.load(sys.stdin)
        project_dir = os.environ.get("CLAUDE_PROJECT_DIR") or payload.get("cwd") or os.getcwd()
        response = run_pre(payload) if mode == "pre" else run_post(payload, project_dir) if mode == "post" else None
    except Exception:
        return 0
    if response is not None:
        print(json.dumps(response))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
