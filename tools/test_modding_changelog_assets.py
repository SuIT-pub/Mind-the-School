"""Tests for modding_changelog_assets.py. Run: python -m unittest tools/test_modding_changelog_assets.py"""

import copy
import json
import pathlib
import sys
import tempfile
import unittest
from datetime import date

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from modding_changelog_assets import build_entry, entry_id, record_asset_release  # noqa: E402
from test_validate_modding_changelog import VALID  # noqa: E402
from validate_modding_changelog import validate  # noqa: E402

TODAY = date(2026, 10, 19)


class AssetEntryTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = pathlib.Path(self.tmp.name, "modding-changelog.json")
        self.path.write_text(json.dumps(VALID), encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def entries(self):
        return json.loads(self.path.read_text(encoding="utf-8"))["entries"]

    def test_entry_id_is_kebab_case(self):
        self.assertEqual(entry_id("1.0.2"), "asset-pack-1-0-2")
        self.assertEqual(entry_id("2.0.0-RC1"), "asset-pack-2-0-0-rc1")

    def test_prepends_valid_entry(self):
        status = record_asset_release("1.0.2", path=self.path, today=TODAY, version="0.2.2")
        self.assertIn("Added asset-pack-1-0-2", status)
        first = self.entries()[0]
        self.assertEqual((first["id"], first["type"], first["date"]), ("asset-pack-1-0-2", "assets", "2026-10-19"))
        self.assertEqual(validate(json.loads(self.path.read_text(encoding="utf-8"))), [])

    def test_note_leads_the_details(self):
        record_asset_release("1.0.2", "Mood token renamed.", path=self.path, today=TODAY, version="0.2.2")
        self.assertTrue(self.entries()[0]["details"].startswith("Mood token renamed."))
        self.assertIn("Download Assets", self.entries()[0]["details"])

    def test_same_version_twice_is_left_alone(self):
        record_asset_release("1.0.2", path=self.path, today=TODAY, version="0.2.2")
        status = record_asset_release("1.0.2", path=self.path, today=TODAY, version="0.2.2")
        self.assertIn("already has", status)
        self.assertEqual(sum(e["id"] == "asset-pack-1-0-2" for e in self.entries()), 1)

    def test_invalid_result_is_not_written(self):
        before = self.path.read_text(encoding="utf-8")
        status = record_asset_release("1.0.2", "x" * 2000, path=self.path, today=TODAY, version="0.2.2")
        self.assertIn("NOT updated", status)
        self.assertEqual(self.path.read_text(encoding="utf-8"), before)

    def test_build_entry_falls_back_to_devstatus_version(self):
        self.assertIsInstance(build_entry("1.0.2", today=TODAY)["version"], str)


if __name__ == "__main__":
    unittest.main()
