"""Validate the display-name files (game/translations.csv and every mod's names files).

Usage:
    python tools/validate_names.py [--events] [game_dir]     (default: game)

Each file holds `key;Name` lines. The game reads them with parse_name_lines()
in game/scripts/helper.rpy; this script applies the same rules, so change
both together:
  - blank lines and lines starting with `#` are skipped
  - only the first `;` separates key and name, both are stripped

Errors (exit code 1), each prefixed with file and line:
  - a line without `;`, an empty key or an empty name
  - a key defined twice in the same file
  - a names file a mod lists that does not exist
  - get_translation("key") called with a literal key that no file defines

Notes (printed, never fail the run):
  - a mod key that replaces a base name (sometimes intended, e.g. Test Mod A)
  - with --events: registered event ids without a name. Many events never
    show their id anywhere, so this list is for spotting gaps, not a to-do.

Keys built at runtime (f-strings like `event_{location}_{option}`) can't be
checked statically; the game logs those misses in developer builds instead.
"""

import ast
import pathlib
import re
import sys

BASE_FILE = "translations.csv"
LITERAL_LOOKUP = re.compile(r"""(?<![\w.])get_translation\(\s*(["'])([^"'{}]+)\1\s*\)""")
EVENT_ID = re.compile(r"""\bEvent\(\s*\d+\s*,\s*(["'])([^"']+)\1""")


def parse_name_lines(text, source):
    """Return ((key, name, line) entries, errors) for one names file."""
    entries, errors, seen = [], [], {}
    for number, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        where = f"{source}:{number}"
        if ";" not in line:
            errors.append(f"{where}: no ';' between key and name: {line}")
            continue
        key, name = (part.strip() for part in line.split(";", 1))
        if not key:
            errors.append(f"{where}: empty key: {line}")
            continue
        if not name:
            errors.append(f"{where}: '{key}' has an empty name")
            continue
        if key in seen:
            errors.append(f"{where}: '{key}' already defined on line {seen[key]}")
            continue
        seen[key] = number
        entries.append((key, name, number))
    return entries, errors


def _call_source(text, start):
    """Return the source of the call whose '(' follows `start`, up to its matching ')'."""
    depth = 0
    for index in range(start, len(text)):
        if text[index] == "(":
            depth += 1
        elif text[index] == ")":
            depth -= 1
            if depth == 0:
                return text[start:index + 1]
    return None


def find_mod_name_files(game_dir):
    """Return (mod key, names file path) for every register_mod(...) that lists translations."""
    found = []
    for script in sorted((game_dir / "mods").glob("*/*.rpy")):
        text = script.read_text(encoding="utf-8")
        for match in re.finditer(r"\bregister_mod\s*\(", text):
            source = _call_source(text, match.end() - 1)
            if source is None:
                continue
            try:
                call = ast.parse("register_mod" + source.replace("\n", " "), mode="eval").body
                args = [ast.literal_eval(arg) for arg in call.args]
                kwargs = {kw.arg: kw.value for kw in call.keywords}
                files = ast.literal_eval(kwargs["translations"]) if "translations" in kwargs else []
            except (SyntaxError, ValueError):
                continue
            if isinstance(files, str):
                files = [files]
            if len(args) < 4:
                continue
            for file_name in files:
                found.append((args[0], game_dir / "mods" / args[3] / file_name))
    return found


def _scripts(game_dir):
    yield from (game_dir / "scripts").rglob("*.rpy")
    yield from (game_dir / "mods").rglob("*.rpy")


def validate(game_dir, list_events=False):
    """Return (errors, notes) for the names files under game_dir."""
    game_dir = pathlib.Path(game_dir)
    errors, notes = [], []

    sources = [("base", game_dir / BASE_FILE)] + find_mod_name_files(game_dir)
    names = {}   # key -> list of (mod key, "file:line")
    for mod_key, path in sources:
        label = path.relative_to(game_dir).as_posix()
        if not path.is_file():
            errors.append(f"{label}: listed by mod '{mod_key}' but the file does not exist")
            continue
        entries, file_errors = parse_name_lines(path.read_text(encoding="utf-8-sig"), label)
        errors.extend(file_errors)
        for key, _name, number in entries:
            names.setdefault(key, []).append((mod_key, f"{label}:{number}"))

    for key, definitions in sorted(names.items()):
        base = [where for mod_key, where in definitions if mod_key == "base"]
        mods = [(mod_key, where) for mod_key, where in definitions if mod_key != "base"]
        for mod_key, where in mods:
            if base:
                notes.append(f"{where}: mod '{mod_key}' replaces the base name '{key}' ({base[0]})")
        if not base and len({mod_key for mod_key, _ in mods}) > 1:
            # whichever mod loads last wins, and the player can't tell which that is
            places = ", ".join(f"{mod_key} ({where})" for mod_key, where in mods)
            notes.append(f"'{key}' is defined by several mods: {places}")

    event_ids = set()
    for script in sorted(_scripts(game_dir)):
        label = script.relative_to(game_dir).as_posix()
        text = script.read_text(encoding="utf-8")
        for match in LITERAL_LOOKUP.finditer(text):
            key = match.group(2)
            if key not in names:
                line = text.count("\n", 0, match.start()) + 1
                errors.append(f"{label}:{line}: get_translation('{key}') has no name in any names file")
        event_ids.update(match.group(2) for match in EVENT_ID.finditer(text))

    if list_events:
        for event_id in sorted(event_ids - set(names)):
            notes.append(f"event '{event_id}' has no name")

    return errors, notes


def main(argv):
    list_events = "--events" in argv
    rest = [arg for arg in argv if arg != "--events"]
    game_dir = pathlib.Path(rest[0]) if rest else pathlib.Path("game")
    errors, notes = validate(game_dir, list_events)
    for note in notes:
        print(f"note: {note}")
    for error in errors:
        print(f"error: {error}")
    if errors:
        print(f"names: {len(errors)} error(s)")
        return 1
    print("names: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
