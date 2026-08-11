# Legacy journal definitions archive

Copied from `rules.rpy`, `clubs.rpy`, `buildings.rpy`, and `journal_obj.rpy` before those implementations were retired.

These are **not loaded** by Ren'Py (``.txt``). Use them as source material when converting old rules, clubs, and buildings into ``Unlockable`` definitions.

- `rules_definitions.archive.txt` — old `Rule` class, helpers, `load_rules` definitions
- `clubs_definitions.archive.txt` — old `Club` class, helpers, `load_clubs` definitions
- `buildings_definitions.archive.txt` — former journal `Building` class, helpers, `load_buildings` definitions
- `journal_obj.archive.txt` — former `Journal_Obj` base class and map helpers

## Runtime

- `Journal_Obj` / `Rule` / `Club` are **save-unpickle stubs only** (like deprecated effects / `PTAProposal`).
- `clean_legacy_journal_objects()` clears `rules` / `clubs` / `buildings` on `after_load`.
- `RuleEffect` / `ClubEffect` / `BuildingEffect` are deprecated no-ops for save compatibility.
- Unlock checks use `is_unlockable_unlocked()` / `unlockable_manager`.
- Map buildings use `buildings/building.rpy` (`Building` / `BuildingManager` / collection key helpers).
