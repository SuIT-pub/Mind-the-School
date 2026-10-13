"""Tests for devstatus_hook.py. Run: python -m unittest tools/test_devstatus_hook.py"""

import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from devstatus_hook import needs_reminder, run  # noqa: E402


class NeedsReminderTest(unittest.TestCase):
    def test_game_change_without_devstatus(self):
        self.assertTrue(needs_reminder(["game/script.rpy", "README.md"]))

    def test_wiki_change_without_devstatus(self):
        self.assertTrue(needs_reminder(["wiki/Lore.md"]))

    def test_devstatus_already_updated(self):
        self.assertFalse(needs_reminder(["game/script.rpy", "devstatus.json"]))

    def test_unrelated_change(self):
        self.assertFalse(needs_reminder(["tools/upload_assets.py", ".github/workflows/x.yml"]))

    def test_images_only_commit(self):
        # Asset dumps are not features; don't nag.
        self.assertFalse(needs_reminder(["game/images/events/a.webp", "game/images/events/b.webp"]))


class RunTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = pathlib.Path(self.tmp.name)
        git = ["git", "-C", str(self.repo)]
        subprocess.run([*git, "init", "-q"], check=True)
        subprocess.run([*git, "config", "user.email", "t@t"], check=True)
        subprocess.run([*git, "config", "user.name", "t"], check=True)
        (self.repo / "game").mkdir()
        (self.repo / "game" / "script.rpy").write_text("label start:\n", encoding="utf-8")
        subprocess.run([*git, "add", "."], check=True)
        subprocess.run([*git, "commit", "-q", "-m", "x"], check=True)

    def tearDown(self):
        self.tmp.cleanup()

    def payload(self, command, tool="Bash"):
        return json.dumps({"tool_name": tool, "tool_input": {"command": command}, "cwd": str(self.repo)})

    def test_commit_touching_game_gets_reminder(self):
        out = run(self.payload('git commit -m "feat: x"'))
        data = json.loads(out)
        self.assertEqual(data["hookSpecificOutput"]["hookEventName"], "PostToolUse")
        self.assertIn("update-devstatus", data["hookSpecificOutput"]["additionalContext"])

    def test_powershell_commit_also_counts(self):
        self.assertIn("update-devstatus", run(self.payload("git commit -m 'x'", tool="PowerShell")))

    def test_non_commit_command_is_silent(self):
        self.assertEqual(run(self.payload("git status")), "")

    def test_garbage_input_is_silent(self):
        self.assertEqual(run("not json"), "")


if __name__ == "__main__":
    unittest.main()
