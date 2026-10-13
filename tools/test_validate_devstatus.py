"""Tests for validate_devstatus.py. Run: python -m unittest tools/test_validate_devstatus.py"""

import copy
import json
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from validate_devstatus import validate  # noqa: E402

VALID = {
    "schemaVersion": 1,
    "updatedAt": "2026-10-12T18:00:00Z",
    "currentVersion": "0.2.2",
    "targetVersion": "0.3.0",
    "now": [{"id": "lab-building", "title": "Lab building", "summary": "A real lab.", "progress": 40}],
    "next": [{"id": "beach-camp", "title": "Beach camp", "summary": "A school trip."}],
    "later": [{"id": "hypnosis", "title": "Hypnosis", "summary": "Rare."}],
    "done": [{"id": "map-registry", "title": "Maps", "summary": "Faster travel.", "doneIn": "0.2.2", "doneAt": "2026-10-01"}],
}


class ValidateDevstatusTest(unittest.TestCase):
    def doc(self):
        return copy.deepcopy(VALID)

    def test_valid_file_passes(self):
        self.assertEqual(validate(self.doc()), [])

    def test_repo_file_passes(self):
        path = pathlib.Path(__file__).resolve().parent.parent / "devstatus.json"
        self.assertEqual(validate(json.loads(path.read_text(encoding="utf-8"))), [])

    def test_long_title_fails(self):
        doc = self.doc()
        doc["next"][0]["title"] = "x" * 61
        self.assertIn("next[0].title: longer than 60 characters", validate(doc))

    def test_long_summary_fails(self):
        doc = self.doc()
        doc["now"][0]["summary"] = "x" * 161
        self.assertIn("now[0].summary: longer than 160 characters", validate(doc))

    def test_progress_out_of_range_fails(self):
        doc = self.doc()
        doc["now"][0]["progress"] = 120
        self.assertIn("now[0].progress: must be an integer from 0 to 100", validate(doc))

    def test_progress_bool_fails(self):
        doc = self.doc()
        doc["now"][0]["progress"] = True
        self.assertIn("now[0].progress: must be an integer from 0 to 100", validate(doc))

    def test_duplicate_id_fails(self):
        doc = self.doc()
        doc["next"].append(copy.deepcopy(doc["now"][0]))
        self.assertIn('next[1].id: duplicate id "lab-building"', validate(doc))

    def test_bad_id_fails(self):
        doc = self.doc()
        doc["now"][0]["id"] = "Lab Building"
        self.assertIn("now[0].id: must be kebab-case", validate(doc))

    def test_too_many_done_fails(self):
        doc = self.doc()
        for i in range(10):
            doc["done"].append({"id": f"item-{i}", "title": "x", "summary": "y", "doneIn": "0.1", "doneAt": "2026-01-01"})
        self.assertIn("done: more than 10 entries", validate(doc))

    def test_missing_list_fails(self):
        doc = self.doc()
        del doc["later"]
        self.assertIn("later: missing or not a list", validate(doc))

    def test_item_version_is_optional(self):
        doc = self.doc()
        doc["now"][0]["version"] = "0.2.2"
        self.assertEqual(validate(doc), [])

    def test_item_version_must_be_short_string(self):
        doc = self.doc()
        doc["next"][0]["version"] = 2
        doc["later"][0]["version"] = "x" * 21
        problems = validate(doc)
        self.assertIn("next[0].version: must be a string of at most 20 characters", problems)
        self.assertIn("later[0].version: must be a string of at most 20 characters", problems)

    def test_done_needs_date(self):
        doc = self.doc()
        doc["done"][0]["doneAt"] = "October"
        self.assertIn("done[0].doneAt: must be a YYYY-MM-DD date", validate(doc))


if __name__ == "__main__":
    unittest.main()
