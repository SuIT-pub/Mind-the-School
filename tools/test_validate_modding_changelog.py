"""Tests for validate_modding_changelog.py. Run: python -m unittest tools/test_validate_modding_changelog.py"""

import copy
import json
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from validate_modding_changelog import MAX_DETAILS, validate  # noqa: E402

REPO_FILE = pathlib.Path(__file__).resolve().parent.parent / "modding-changelog.json"

VALID = {
    "schemaVersion": 1,
    "entries": [
        {"id": "event-title", "date": "2026-10-17", "version": "0.2.2", "type": "added",
         "title": "Events can carry their own title", "details": "`Event(..., title=\"…\")`.", "wiki": "Events"},
        {"id": "event-flags", "date": "2026-10-06", "version": "0.2.2", "type": "breaking",
         "title": "Event flags", "details": "Use `FlagCondition`.", "wiki": "Events#event-flags"},
        {"id": "map-registry", "date": "2026-10-06", "version": "0.2.2", "type": "added",
         "title": "Map registry", "details": "Same day as the entry above is fine."},
    ],
}


def with_entry(**changes):
    doc = copy.deepcopy(VALID)
    doc["entries"][0].update(changes)
    return doc


class ValidateTest(unittest.TestCase):
    def test_valid_document(self):
        self.assertEqual(validate(VALID), [])

    def test_repo_file_is_valid(self):
        self.assertEqual(validate(json.loads(REPO_FILE.read_text(encoding="utf-8"))), [])

    def test_empty_history_is_valid(self):
        self.assertEqual(validate({"schemaVersion": 1, "entries": []}), [])

    def test_rejects_wrong_schema_and_missing_entries(self):
        self.assertIn("schemaVersion: must be 1", validate({"schemaVersion": True, "entries": []}))
        self.assertIn("entries: missing or not a list", validate({"schemaVersion": 1}))

    def test_rejects_unknown_type(self):
        self.assertTrue(any("type" in p for p in validate(with_entry(type="feature"))))

    def test_rejects_bad_ids(self):
        self.assertTrue(any("kebab-case" in p for p in validate(with_entry(id="Event_Title"))))
        doc = copy.deepcopy(VALID)
        doc["entries"][1]["id"] = "event-title"
        self.assertTrue(any("duplicate" in p for p in validate(doc)))

    def test_rejects_bad_dates(self):
        self.assertTrue(any("YYYY-MM-DD" in p for p in validate(with_entry(date="17.10.2026"))))
        self.assertTrue(any("real date" in p for p in validate(with_entry(date="2026-02-30"))))

    def test_requires_newest_first(self):
        doc = copy.deepcopy(VALID)
        doc["entries"].reverse()
        self.assertTrue(any("newest first" in p for p in validate(doc)))

    def test_rejects_long_or_empty_text(self):
        self.assertTrue(any("details" in p for p in validate(with_entry(details="x" * (MAX_DETAILS + 1)))))
        self.assertTrue(any("title" in p for p in validate(with_entry(title="  "))))

    def test_wiki_must_be_a_page_name(self):
        self.assertTrue(any("wiki" in p for p in validate(with_entry(wiki="https://github.com/x"))))
        self.assertEqual(validate(with_entry(wiki="Building-Situations#situation-flags")), [])

    def test_version_required(self):
        doc = copy.deepcopy(VALID)
        del doc["entries"][0]["version"]
        self.assertTrue(any("version" in p for p in validate(doc)))


if __name__ == "__main__":
    unittest.main()
