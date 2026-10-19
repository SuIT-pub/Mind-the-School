"""Tests for file_guard_hook.py. Run: python -m unittest tools/test_file_guard_hook.py"""

import pathlib
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from file_guard_hook import blocked_reason, is_names_file, run_post, run_pre  # noqa: E402


def payload(path):
    return {"tool_name": "Edit", "tool_input": {"file_path": path}}


class BlockedReasonTest(unittest.TestCase):
    def test_blocks_compiled_renpy(self):
        self.assertIn(".rpy", blocked_reason(r"M:\MTS Project\Mind the School\game\scripts\menu.rpyc"))

    def test_blocks_env_but_not_example(self):
        self.assertIsNotNone(blocked_reason("M:/proj/.env"))
        self.assertIsNone(blocked_reason("M:/proj/.env.example"))

    def test_blocks_keystores(self):
        self.assertIsNotNone(blocked_reason("android.keystore"))
        self.assertIsNotNone(blocked_reason("C:/x/bundle.KEYSTORE"))

    def test_allows_sources(self):
        for path in ("game/scripts/menu.rpy", "tools/x.py", "wiki/Events.md", "envy.txt"):
            self.assertIsNone(blocked_reason(path), path)


class RunPreTest(unittest.TestCase):
    def test_denies_with_reason(self):
        out = run_pre(payload("game/scripts/menu.rpyc"))["hookSpecificOutput"]
        self.assertEqual(out["permissionDecision"], "deny")
        self.assertEqual(out["hookEventName"], "PreToolUse")

    def test_silent_for_normal_file(self):
        self.assertIsNone(run_pre(payload("game/scripts/menu.rpy")))

    def test_silent_without_path(self):
        self.assertIsNone(run_pre({"tool_input": {}}))


class RunPostTest(unittest.TestCase):
    def test_names_file_detection(self):
        self.assertTrue(is_names_file(r"game\translations.csv"))
        self.assertTrue(is_names_file("game/mods/TestModA/names.csv"))
        self.assertFalse(is_names_file("game/other.csv"))

    def test_ignores_other_files(self):
        self.assertIsNone(run_post(payload("game/scripts/menu.rpy"), "unused"))

    def test_reports_failing_validator(self):
        with tempfile.TemporaryDirectory() as tmp:
            tools = pathlib.Path(tmp, "tools")
            tools.mkdir()
            (tools / "validate_names.py").write_text("print('error: boom'); raise SystemExit(1)\n")
            out = run_post(payload("game/translations.csv"), tmp)
        self.assertEqual(out["decision"], "block")
        self.assertIn("error: boom", out["reason"])

    def test_silent_when_validator_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            tools = pathlib.Path(tmp, "tools")
            tools.mkdir()
            (tools / "validate_names.py").write_text("print('names: OK')\n")
            self.assertIsNone(run_post(payload("game/translations.csv"), tmp))


if __name__ == "__main__":
    unittest.main()
