"""Tests for validate_names.py. Run: python -m unittest tools/test_validate_names.py"""

import pathlib
import sys
import tempfile
import textwrap
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from validate_names import parse_name_lines, validate  # noqa: E402

REPO_GAME = pathlib.Path(__file__).resolve().parent.parent / "game"

MOD_SCRIPT = textwrap.dedent("""\
    init -97 python:
        register_mod(
            "demo",
            "Demo Mod",
            "1",
            "Demo",
            description = "A (test) mod.",
            translations = ["names.csv"],
        )
""")


class ParseNameLinesTest(unittest.TestCase):
    def test_skips_blank_and_comment_lines(self):
        entries, errors = parse_name_lines("# header\n\n  \nshower;Shower\n", "f.csv")
        self.assertEqual(entries, [("shower", "Shower", 4)])
        self.assertEqual(errors, [])

    def test_only_first_semicolon_splits(self):
        entries, _ = parse_name_lines("rule;Rules; for now\n", "f.csv")
        self.assertEqual(entries, [("rule", "Rules; for now", 1)])

    def test_strips_whitespace_and_carriage_returns(self):
        entries, _ = parse_name_lines(" gym ; Gym \r\n", "f.csv")
        self.assertEqual(entries, [("gym", "Gym", 1)])

    def test_line_without_semicolon_is_an_error(self):
        _, errors = parse_name_lines("shower Shower\n", "f.csv")
        self.assertEqual(errors, ["f.csv:1: no ';' between key and name: shower Shower"])

    def test_empty_key_and_empty_name_are_errors(self):
        _, errors = parse_name_lines(";Shower\ngym;\n", "f.csv")
        self.assertEqual(errors, ["f.csv:1: empty key: ;Shower", "f.csv:2: 'gym' has an empty name"])

    def test_duplicate_key_keeps_first(self):
        entries, errors = parse_name_lines("gym;Gym\ngym;Sports Hall\n", "f.csv")
        self.assertEqual(entries, [("gym", "Gym", 1)])
        self.assertEqual(errors, ["f.csv:2: 'gym' already defined on line 1"])


class ValidateTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.game = pathlib.Path(self.tmp.name)
        (self.game / "scripts").mkdir()
        (self.game / "mods" / "Demo").mkdir(parents=True)
        self.write("translations.csv", "gym;Gym\nmisc;Miscellaneous\n")
        self.write("mods/Demo/demo.rpy", MOD_SCRIPT)
        self.write("mods/Demo/names.csv", "demo_hut;Hut\n")

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, relative, text):
        (self.game / relative).write_text(text, encoding="utf-8")

    def test_clean_setup_passes(self):
        self.assertEqual(validate(self.game), ([], []))

    def test_bom_does_not_corrupt_first_key(self):
        (self.game / "translations.csv").write_bytes("﻿gym;Gym\n".encode("utf-8"))
        self.write("scripts/a.rpy", 'text get_translation("gym")\n')
        self.assertEqual(validate(self.game)[0], [])

    def test_mod_file_errors_carry_the_mod_path(self):
        self.write("mods/Demo/names.csv", "demo_hut Hut\n")
        self.assertEqual(validate(self.game)[0], ["mods/Demo/names.csv:1: no ';' between key and name: demo_hut Hut"])

    def test_missing_mod_file_is_an_error(self):
        (self.game / "mods/Demo/names.csv").unlink()
        self.assertEqual(validate(self.game)[0], ["mods/Demo/names.csv: listed by mod 'demo' but the file does not exist"])

    def test_mod_replacing_base_name_is_a_note(self):
        self.write("mods/Demo/names.csv", "misc;Other\n")
        errors, notes = validate(self.game)
        self.assertEqual(errors, [])
        self.assertEqual(notes, ["mods/Demo/names.csv:1: mod 'demo' replaces the base name 'misc' (translations.csv:2)"])

    def test_literal_lookup_without_name_is_an_error(self):
        self.write("scripts/a.rpy", 'x = get_translation("gym")\ny = get_translation(\'pool\')\n')
        self.assertEqual(validate(self.game)[0], ["scripts/a.rpy:2: get_translation('pool') has no name in any names file"])

    def test_runtime_built_keys_are_not_checked(self):
        self.write("scripts/a.rpy", 'x = get_translation(f"event_{location}")\ny = get_translation(key)\n')
        self.assertEqual(validate(self.game)[0], [])

    def test_events_listing_is_opt_in(self):
        self.write("scripts/a.rpy", 'Event(3, "gym_event_1", None)\nEvent(3, "gym", None)\n')
        self.assertEqual(validate(self.game)[1], [])
        self.assertEqual(validate(self.game, list_events=True)[1], ["event 'gym_event_1' has no name"])

    def test_events_with_title_argument_are_not_listed(self):
        self.write("scripts/a.rpy", textwrap.dedent("""\
            EventFragment(2, "tod_truth_1",
                TimeCondition(daytime = "c"),
                title = "Truth: first kiss")
            EventComposite(3, "tod", [], Pattern("main", "x.webp"), title = "Truth or Dare")
            EventSelect(1, "pick", "Where to?", {}, SomeOption(title = "inner"))
        """))
        self.assertEqual(validate(self.game, list_events=True)[1], ["event 'pick' has no name"])

    def test_title_hidden_by_own_names_file_is_an_error(self):
        self.write("translations.csv", "gym;Gym\nmisc;Miscellaneous\ngym_event_1;Old name\n")
        self.write("scripts/a.rpy", 'x = 1\nEvent(3, "gym_event_1", title = "New name")\n')
        self.assertEqual(validate(self.game)[0], [
            "scripts/a.rpy:2: title= of 'gym_event_1' never shows, translations.csv:3 names it "
            "and names files win; delete that line or the title"])

    def test_mod_renaming_a_titled_base_event_is_a_note(self):
        self.write("mods/Demo/names.csv", "gym_event_1;Mod name\n")
        self.write("scripts/a.rpy", 'Event(3, "gym_event_1", title = "Base name")\n')
        errors, notes = validate(self.game)
        self.assertEqual(errors, [])
        self.assertEqual(notes, ["mods/Demo/names.csv:1: renames 'gym_event_1', hiding its title= (scripts/a.rpy:1)"])

    def test_repo_names_pass(self):
        self.assertEqual(validate(REPO_GAME)[0], [])


if __name__ == "__main__":
    unittest.main()
