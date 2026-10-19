"""Tests for modding_changelog_hook.py. Run: python -m unittest tools/test_modding_changelog_hook.py"""

import json
import pathlib
import sys
import unittest
from unittest import mock

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import modding_changelog_hook  # noqa: E402
from modding_changelog_hook import needs_reminder, run  # noqa: E402


class NeedsReminderTest(unittest.TestCase):
    def test_code_change_without_entry(self):
        self.assertTrue(needs_reminder(["game/scripts/event.rpy"]))
        self.assertTrue(needs_reminder(["wiki/Events.md"]))
        self.assertTrue(needs_reminder(["game/mods/TestModA/names.csv"]))

    def test_entry_in_same_commit_silences(self):
        self.assertFalse(needs_reminder(["game/scripts/event.rpy", "modding-changelog.json"]))

    def test_developer_wiki_and_asset_tools_count(self):
        self.assertTrue(needs_reminder(["wiki/Paperdoll.md"]))
        self.assertTrue(needs_reminder(["wiki/School-Levels.md"]))
        self.assertTrue(needs_reminder(["tools/upload_assets.py"]))

    def test_player_wiki_pages_stay_quiet(self):
        for page in ("Player-Guide.md", "Walkthrough-Unlocks.md", "Lore.md", "Roadmap.md", "Home.md",
                     "_Sidebar.md", "scripts/sync-wiki.ps1"):
            self.assertFalse(needs_reminder([f"wiki/{page}"]), page)

    def test_content_only_paths_stay_quiet(self):
        self.assertFalse(needs_reminder(["wiki/characters/Lily-Anderson/Lily-Anderson.md"]))
        self.assertFalse(needs_reminder(["game/images/bg.webp", "devstatus.json", "tools/x.py"]))
        self.assertFalse(needs_reminder([]))


class RunTest(unittest.TestCase):
    def payload(self, command):
        return json.dumps({"tool_input": {"command": command}, "cwd": "."})

    def test_ignores_non_commit_commands(self):
        self.assertEqual(run(self.payload("git status")), "")

    def test_reminds_after_relevant_commit(self):
        with mock.patch.object(modding_changelog_hook, "changed_paths", return_value=["game/scripts/menu.rpy"]):
            out = json.loads(run(self.payload('git commit -m "x"')))
        self.assertIn("update-modding-changelog", out["hookSpecificOutput"]["additionalContext"])

    def test_quiet_after_irrelevant_commit(self):
        with mock.patch.object(modding_changelog_hook, "changed_paths", return_value=["devstatus.json"]):
            self.assertEqual(run(self.payload("git commit -m x")), "")

    def test_broken_payload_is_silent(self):
        self.assertEqual(run("not json"), "")


if __name__ == "__main__":
    unittest.main()
