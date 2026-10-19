"""Tests for the version handling in upload_assets.py. Run: python -m unittest tools/test_upload_assets.py

Needs boto3 and python-dotenv (requirements.txt), like the uploader itself.
"""

import io
import json
import pathlib
import sys
import unittest
from unittest import mock

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import upload_assets  # noqa: E402
from botocore.exceptions import ClientError  # noqa: E402
from upload_assets import next_patch_version, parse_version, remote_version_or_none, with_env_value  # noqa: E402


class FakeClient:
    def __init__(self, version=None, error_code=None):
        self.version = version
        self.error_code = error_code

    def get_object(self, Bucket, Key):
        if self.error_code:
            raise ClientError({"Error": {"Code": self.error_code}}, "GetObject")
        return {"Body": io.BytesIO(json.dumps({"version": self.version}).encode())}


class VersionTest(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(parse_version("1.0.2"), (1, 0, 2))
        self.assertEqual(parse_version(" 10.4 "), (10, 4))

    def test_parse_rejects_non_numbers(self):
        with self.assertRaises(SystemExit):
            parse_version("1.0.2-beta")

    def test_counts_up_from_the_higher_version(self):
        self.assertEqual(next_patch_version("1.0.2", "1.0.2"), "1.0.3")
        self.assertEqual(next_patch_version("1.0.2", "1.0.0"), "1.0.3")   # stale .env
        self.assertEqual(next_patch_version("1.0.2", "1.1.0"), "1.1.1")   # .env set ahead by hand
        self.assertEqual(next_patch_version("1.0.9", "1.0.10"), "1.0.11")  # numeric, not text order

    def test_first_upload_counts_from_env(self):
        self.assertEqual(next_patch_version(None, "1.0.0"), "1.0.1")

    def test_nothing_to_count_from(self):
        with self.assertRaises(SystemExit):
            next_patch_version(None, None)

    def test_remote_version(self):
        self.assertEqual(remote_version_or_none(FakeClient("1.0.2"), "b"), "1.0.2")
        self.assertIsNone(remote_version_or_none(FakeClient(error_code="NoSuchKey"), "b"))
        with self.assertRaises(SystemExit):
            remote_version_or_none(FakeClient(error_code="AccessDenied"), "b")


class EnvTest(unittest.TestCase):
    def test_replaces_only_the_version_line(self):
        text = "R2_BUCKET_NAME=game-assets\nASSET_VERSION=1.0.2\n# comment\nR2_PUBLIC_URL=https://x\n"
        self.assertEqual(
            with_env_value(text, "ASSET_VERSION", "1.0.3"),
            "R2_BUCKET_NAME=game-assets\nASSET_VERSION=1.0.3\n# comment\nR2_PUBLIC_URL=https://x\n",
        )

    def test_handles_spaces_and_crlf(self):
        self.assertEqual(with_env_value("A=1\r\nASSET_VERSION = 1.0.2\r\n", "ASSET_VERSION", "1.0.3"),
                         "A=1\nASSET_VERSION=1.0.3\n")

    def test_appends_when_missing(self):
        self.assertEqual(with_env_value("A=1\n", "ASSET_VERSION", "1.0.0"), "A=1\nASSET_VERSION=1.0.0\n")


class MainFlowTest(unittest.TestCase):
    """--next-version with --bump-version: new number from the live one, saved only after the bump."""

    def run_main(self, argv, bump_side_effect=None):
        config = {"R2_BUCKET_NAME": "b", "R2_PUBLIC_URL": "https://x", "ASSET_VERSION": "1.0.2"}
        calls = self.calls = []
        with mock.patch.object(sys, "argv", ["upload_assets.py", *argv]), \
             mock.patch.object(upload_assets, "load_config", return_value=config), \
             mock.patch.object(upload_assets, "create_r2_client", return_value=FakeClient("1.0.2")), \
             mock.patch.object(upload_assets, "bump_cloud_version",
                               side_effect=bump_side_effect or (lambda c, b, v, u: calls.append(("bump", v)))), \
             mock.patch.object(upload_assets, "save_env_version", side_effect=lambda v: calls.append(("env", v))), \
             mock.patch.object(upload_assets, "announce_asset_release",
                               side_effect=lambda v, n: calls.append(("changelog", v, n))), \
             mock.patch("builtins.print"):
            upload_assets.main()
        return calls

    def test_bump_to_next_version(self):
        calls = self.run_main(["--next-version", "--bump-version", "--note", "renamed"])
        self.assertEqual(calls, [("bump", "1.0.3"), ("env", "1.0.3"), ("changelog", "1.0.3", "renamed")])

    def test_failed_bump_leaves_env_alone(self):
        def refuse(*_):
            raise SystemExit(1)
        with self.assertRaises(SystemExit):
            self.run_main(["--next-version", "--bump-version"], bump_side_effect=refuse)
        self.assertEqual(self.calls, [])  # no .env write, no changelog entry

    def test_plain_bump_keeps_env_version(self):
        calls = self.run_main(["--bump-version"])
        self.assertEqual(calls, [("bump", "1.0.2"), ("changelog", "1.0.2", None)])

    def test_next_version_refuses_reuse_archive(self):
        with self.assertRaises(SystemExit):
            self.run_main(["--next-version", "--reuse-archive"])


if __name__ == "__main__":
    unittest.main()
