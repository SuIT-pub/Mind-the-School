"""Tests for publish_devstatus.py. Run: python -m unittest tools/test_publish_devstatus.py"""

import copy
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from publish_devstatus import publish, should_publish  # noqa: E402
from test_validate_devstatus import VALID  # noqa: E402


def doc(updated_at):
    d = copy.deepcopy(VALID)
    d["updatedAt"] = updated_at
    return d


class ShouldPublishTest(unittest.TestCase):
    def test_nothing_published_yet(self):
        self.assertTrue(should_publish(doc("2026-10-13T10:00:00Z"), None))

    def test_newer_wins(self):
        self.assertTrue(should_publish(doc("2026-10-13T10:00:00Z"), doc("2026-10-12T10:00:00Z")))

    def test_older_branch_does_not_overwrite(self):
        self.assertFalse(should_publish(doc("2026-10-01T10:00:00Z"), doc("2026-10-12T10:00:00Z")))

    def test_same_timestamp_is_skipped(self):
        self.assertFalse(should_publish(doc("2026-10-12T10:00:00Z"), doc("2026-10-12T10:00:00Z")))

    def test_timezones_are_compared_as_instants(self):
        self.assertTrue(should_publish(doc("2026-10-12T12:30:00+02:00"), doc("2026-10-12T10:00:00Z")))

    def test_broken_published_copy_is_replaced(self):
        self.assertTrue(should_publish(doc("2026-10-01T10:00:00Z"), {"garbage": True}))


class PublishTest(unittest.TestCase):
    """Runs publish() against a real local bare remote."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = pathlib.Path(self.tmp.name)
        self.remote = root / "remote.git"
        subprocess.run(["git", "init", "-q", "--bare", str(self.remote)], check=True)
        self.work = root / "work"
        subprocess.run(["git", "clone", "-q", str(self.remote), str(self.work)], check=True, capture_output=True)
        for key, value in (("user.email", "ci@test"), ("user.name", "ci")):
            subprocess.run(["git", "-C", str(self.work), "config", key, value], check=True)

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, document):
        path = self.work / "devstatus.json"
        path.write_text(json.dumps(document), encoding="utf-8")
        return path

    def published(self):
        out = subprocess.run(
            ["git", "-C", str(self.remote), "show", "devstatus:devstatus.json"],
            capture_output=True, text=True,
        )
        return json.loads(out.stdout) if out.returncode == 0 else None

    def test_first_publish_creates_branch_with_only_the_file(self):
        result = publish(self.write(doc("2026-10-13T10:00:00Z")), self.work, "feature/x")

        self.assertEqual(result, "published")
        self.assertEqual(self.published()["updatedAt"], "2026-10-13T10:00:00Z")
        files = subprocess.run(
            ["git", "-C", str(self.remote), "ls-tree", "--name-only", "devstatus"],
            capture_output=True, text=True, check=True,
        ).stdout.split()
        self.assertEqual(files, ["devstatus.json"])

    def test_newer_update_replaces_older(self):
        publish(self.write(doc("2026-10-12T10:00:00Z")), self.work, "a")
        result = publish(self.write(doc("2026-10-13T10:00:00Z")), self.work, "b")

        self.assertEqual(result, "published")
        self.assertEqual(self.published()["updatedAt"], "2026-10-13T10:00:00Z")

    def test_older_update_is_skipped(self):
        publish(self.write(doc("2026-10-13T10:00:00Z")), self.work, "a")
        result = publish(self.write(doc("2026-10-01T10:00:00Z")), self.work, "old-branch")

        self.assertEqual(result, "skipped")
        self.assertEqual(self.published()["updatedAt"], "2026-10-13T10:00:00Z")

    def test_rule_rejection_reports_git_message_without_retrying(self):
        # Simulate a repository ruleset: the remote refuses every push.
        hook = self.remote / "hooks" / "pre-receive"
        hook.write_bytes(b"#!/bin/sh\necho 'GH013: Repository rule violations found: cannot create ref' >&2\nexit 1\n")
        hook.chmod(0o755)

        with self.assertRaises(RuntimeError) as caught:
            publish(self.write(doc("2026-10-13T10:00:00Z")), self.work, "a")

        self.assertIn("GH013", str(caught.exception))
        self.assertIn("devstatus", str(caught.exception))

    def test_invalid_file_is_rejected(self):
        broken = doc("2026-10-13T10:00:00Z")
        broken["now"][0]["progress"] = 500

        with self.assertRaises(ValueError):
            publish(self.write(broken), self.work, "a")
        self.assertIsNone(self.published())


if __name__ == "__main__":
    unittest.main()
