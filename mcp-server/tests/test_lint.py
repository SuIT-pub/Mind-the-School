"""Tests for mts_mcp.lint. Run: python -m unittest discover mcp-server/tests"""

import pathlib
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))

from mts_mcp.lint import LintRun, format_lint_run, parse_lint_report, read_sdk_path  # noqa: E402

REPORT = """\

Ren'Py 8.1.3.23091805 lint report, generated at: Mon Oct 19 10:23:19 2026

game/scripts/buildings/cafeteria.rpy:215 Could not evaluate 'adelaide' in the who part of a say statement.
Perhaps you forgot to define a character?

game/scripts/buildings/cafeteria.rpy:221 Could not evaluate 'adelaide' in the who part of a say statement.

game/scripts/events/new_management.rpy:88 Could not evaluate 'emkio' in the who part of a say statement.

game/scripts/journal/journal.rpy:12 The image tag 'bg_missing' is not the prefix of a declared image, nor is it a known attribute.

Statistics:
The game contains 3,687 dialogue blocks.

game/scripts/fake.rpy:1 this looks like an issue but sits in the statistics tail
"""


class ParseLintReportTest(unittest.TestCase):
    def test_folds_say_who_noise_into_counts(self):
        report = parse_lint_report(REPORT)
        self.assertEqual(report.say_who_counts, {"adelaide": 2, "emkio": 1})

    def test_keeps_real_issues_with_file_and_line(self):
        report = parse_lint_report(REPORT)
        self.assertEqual(len(report.issues), 1)
        issue = report.issues[0]
        self.assertEqual(issue.file, "game/scripts/journal/journal.rpy")
        self.assertEqual(issue.line, 12)
        self.assertIn("bg_missing", issue.text)

    def test_ignores_header_and_statistics_tail(self):
        report = parse_lint_report(REPORT)
        self.assertEqual(report.other_blocks, [])
        self.assertNotIn("fake.rpy", "".join(i.file for i in report.issues))

    def test_strips_bom_before_header(self):
        report = parse_lint_report("﻿" + REPORT.lstrip("\n"))
        self.assertEqual(report.other_blocks, [])

    def test_handles_crlf_reports(self):
        report = parse_lint_report(REPORT.replace("\n", "\r\n"))
        self.assertEqual(len(report.issues), 1)
        self.assertEqual(report.say_who_counts, {"adelaide": 2, "emkio": 1})
        self.assertNotIn("\r", report.issues[0].text)

    def test_empty_report(self):
        report = parse_lint_report("")
        self.assertEqual((report.issues, report.other_blocks, sum(report.say_who_counts.values())), ([], [], 0))


class FormatLintRunTest(unittest.TestCase):
    def _run(self, **overrides):
        values = dict(report=parse_lint_report(REPORT), parse_errors=None, duration_seconds=16.4, stdout="")
        values.update(overrides)
        return LintRun(**values)

    def test_parse_errors_win_over_report(self):
        text = format_lint_run(self._run(parse_errors='File "game/x.rpy", line 3: EOL while scanning'))
        self.assertIn("PARSE-FEHLER", text)
        self.assertNotIn("bg_missing", text)

    def test_path_filter_matches_backslash_paths(self):
        self.assertIn("1 echte Befunde", format_lint_run(self._run(), path_filter="scripts\\journal"))
        self.assertIn("0 echte Befunde", format_lint_run(self._run(), path_filter="cafeteria"))

    def test_say_names_rarest_first(self):
        text = format_lint_run(self._run(), show_say_names=True)
        self.assertLess(text.index("- emkio: 1"), text.index("- adelaide: 2"))

    def test_say_names_hidden_by_default(self):
        self.assertNotIn("- emkio", format_lint_run(self._run()))

    def test_truncates_beyond_max_issues(self):
        many = "\n\n".join(f"game/a.rpy:{n} broken thing" for n in range(3))
        text = format_lint_run(self._run(report=parse_lint_report(many)), max_issues=1)
        self.assertIn("- game/a.rpy:0 broken thing", text)
        self.assertNotIn("game/a.rpy:1 ", text)
        self.assertIn("2 weitere abgeschnitten", text)

    def test_missing_report_shows_stdout(self):
        text = format_lint_run(self._run(report=None, stdout="Traceback: boom"))
        self.assertIn("Traceback: boom", text)


class ReadSdkPathTest(unittest.TestCase):
    def test_reads_utf16_le_without_bom(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            (root / ".renpy-sdk").write_bytes("M:\\RenPy\r\n".encode("utf-16-le"))
            self.assertEqual(read_sdk_path(root, pathlib.Path("X:/fallback")), pathlib.Path("M:/RenPy"))

    def test_reads_utf8(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            (root / ".renpy-sdk").write_text("D:/SDK/renpy-8.1.3\n", encoding="utf-8")
            self.assertEqual(read_sdk_path(root, pathlib.Path("X:/fallback")), pathlib.Path("D:/SDK/renpy-8.1.3"))

    def test_falls_back_when_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(read_sdk_path(pathlib.Path(tmp), pathlib.Path("X:/fallback")), pathlib.Path("X:/fallback"))


if __name__ == "__main__":
    unittest.main()
