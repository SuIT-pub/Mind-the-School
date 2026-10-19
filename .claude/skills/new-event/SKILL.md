---
name: new-event
description: Use when creating a new Mind the School event or scene (Ren'Py Event definition + scene label) — a building/pool event, a situation pool/threshold/resolution/measure scene, a time-triggered story beat, a composite with fragments, a select/routing event, or a journal/misc event. Covers definition, gating, selectors, wiring, the scene label (images, video, paperdoll, dialogue, decision menu, stats, situations, flags) and verification.
---

# New Event

An event is **two things sharing one name**: an `Event(...)` definition registered into a
pool, and a `label <name>(**kwargs):` scene. This skill walks every kind of event the game
has. The full API is in the wiki (`wiki/Events.md`, `Building-Situations.md`,
`Conditions.md`, `Selectors.md`, `Effects.md`, `Options.md`, `Paperdoll.md`,
`Dialogue.md`, `School-Levels.md`); `reference.md` next to this file condenses what an
event author needs, and `templates/` holds a copy-ready skeleton per kind.

## Workflow

### 1. Pin down the event (ask LO for whatever is missing)

Do not start writing until each of these has an answer. Ask in one batch, not one by one.

| Question | Why it matters |
|---|---|
| **Kind** — see the table in step 2 | decides template, pool, end type |
| **Where** — building + action pool (e.g. `cafeteria_events["order_food"]`), or situation/threshold/resolution, or time check | wiring |
| **When** — daytime/weekday, school level range, progress step, seen-prerequisites, flag phase (intro/camp) | conditions |
| **Who** — fixed Person(s) or a selector-picked girl | dialogue + `get_person_value` |
| **Priority** — 1 blocking story beat · 2 always-run · 3 random ambient | `select_type` |
| **Visuals** — existing render(s) / new render planned / paperdoll over a blurred background | patterns, thumbnail |
| **Branches** — player choices, gated choices | decision menu |
| **Consequences** — stats, situation bar, progress, GameData flags, modifier, unlock | effects in the label |
| **Ending** — next daytime, back to map, `none` (chained/threshold), new day | `end_event` type |
| **Title** — name shown in menus/gallery/cheat page | `title=` |

Project rule: rework/creation goes **one event at a time** — present the plan (summary +
definition sketch + scene beats) and wait for LO's OK before implementing.

### 2. Pick the kind → template

| Kind | Typical trigger | Template | Pool | End |
|---|---|---|---|---|
| **Building/pool event** | player picks a map action | `templates/pool_event.rpy` | `<building>_events["<action>"]` or `<building>_general_event` | `new_daytime` (or `map_entry` for "free" actions) |
| **Situation pool event** | pool event that only exists while a situation's bar is in a band | `templates/situation_pool_event.rpy` | building pool + `SituationPoolCondition` + `SituationPool(...)` on the situation | `new_daytime` |
| **Threshold / resolution / measure scene** | fired by `EventEffect` from a situation | `templates/situation_triggered_event.rpy` | a `"misc"` `EventStorage` with `override_location="misc"` | `none` + `return` |
| **Time-triggered story beat** | a date/daytime arrives | `templates/time_check_event.rpy` | `time_check_events` | prio 1 story: `new_daytime`; prio 2 chained checks: `none` + `return` |
| **Composite + fragments** | one action plays an intro + shuffled fragments | `templates/composite_event.rpy` | composite in a building pool, fragments in `FragmentStorage`s | composite runner ends it; each fragment `end_event` |
| **Select / routing event** | one action opens a sub-menu of pools | `templates/select_event.rpy` | building pool; routes into other `EventStorage`s | `select_event_runner` handles it |
| **Video scene** | any kind above with animated steps | `templates/video_snippet.rpy` (add to any template) | — | — |

Other pools exist for special cases: `journal_events` (journal open), `sandbox_check_events`,
`office_building_work_event[...]`, `office_building_lab_events[...]`,
`office_building_call_secretary_events[...]`, `office_building_subject_learn_events[...]`,
`sb_teach_events[...]`. Read the building file (`game/scripts/buildings/<building>.rpy`)
for the exact pool keys before wiring — never guess them.

### 3. Read before writing

- The building file that owns the pool, and one or two neighbouring events of the same kind
  (e.g. `game/scripts/events/new_management.rpy` is the reference build for situation pool
  events with selectors, gated choices, paperdoll and GameData flags).
- For situation work: the situation's definition in `game/scripts/situations/situations.rpy`
  and `wiki/Building-Situations.md` §4 (pools), §7 (wiring), §13 (progress), §14 (resolutions).
- `wiki/School-Levels.md` for the tone of the level range you gate on.

### 4. Write the definition

Inside `init 1 python:` with `set_current_mod('base')` first (or the mod key for mods):

```python
Event(3, "cafeteria_snack_chat",                      # priority, label name
    TimeCondition(weekday="d", daytime="f"),          # gates (all must pass)
    LevelCondition("2-4", char_obj="school"),
    RandomListSelector("topic", "coffee", "tea"),     # values → kwargs + <topic>
    Pattern("main", "images/events/cafeteria/cafeteria_snack_chat/cafeteria_snack_chat <topic> <school_level> <step>.webp"),
    thumbnail="images/events/cafeteria/cafeteria_snack_chat/cafeteria_snack_chat coffee 2 1.webp",
    title="Snack Chat")
```

Conditions, selectors, options and patterns can come in any order; the constructor sorts
them. Catalogs: `reference.md`.

### 5. Write the scene label

Skeleton (every label and every `.branch` sub-label takes `(**kwargs)`):

```python
label cafeteria_snack_chat(**kwargs):
    $ begin_event(**kwargs)                  # first line; binds headmaster + emiko
    $ topic = get_value("topic", **kwargs)   # read selectors through the getters
    $ image = convert_pattern("main", **kwargs)
    $ image.show(0)                          # an image before the first line of text
    subtitles "..."
    call change_stats_with_modifier(happiness=SMALL) from _cafeteria_snack_chat_1
    $ end_event("new_daytime", **kwargs)
```

Scene building blocks (details in `reference.md`):
images & steps · video · paperdoll (`register_paperdoll` / `set_background` / `display`) ·
dialogue (`headmaster`, `emiko`, `Person["key"].say/think/whisper/shout`,
`get_person_value`) · decision menu (`$ call_custom_menu_with_text(...)` + `MenuElement`) ·
stats (`change_stats_with_modifier`) · situation bar (`apply_progress_change`) ·
progress · GameData flags · lasting modifiers (`load_modifier`) · situation activation.

### 6. Wire it

- Pool event: `<pool>.add_event(event)` in the same init block.
- Situation pool: `SituationPoolCondition("<situation>", "<pool_key>")` on the event **and**
  `SituationPool("<pool_key>", min, max)` on the situation (create it if new).
- Threshold/resolution/measure: add the `Event(2, ..., override_location="misc")` to the
  situation's misc storage and put `EventEffect("<label>")` into the `AutoThreshold` /
  resolution / measure on the situation.
- Time beat: `time_check_events.add_event(event)` in `daily_check.rpy` (or the content file).
- Title: prefer `title=` on the Event. If `game/translations.csv` already has a line for the
  id, either keep using the CSV or delete that line — the CSV wins over `title=`.

### 7. Verify

1. **Lint** — call the `renpy_lint` MCP tool (mind-the-school server), ideally with
   `path_filter="<file or event prefix>"`. Zero real findings, and no parse errors. Use
   `show_say_names=True` and look for a misspelled speaker among the rare names.
2. **IDE diagnostics** — `mcp__ide__getDiagnostics` for the edited file. The VS Code
   "MTS Event Manager" extension flags `Pattern`s / `image.show(n)` steps with no matching
   image file. For art that doesn't exist yet that is expected; list those paths for LO
   instead of treating them as errors. (Its "Label not found in workspace" warning is
   unreliable for labels in the same new file — lint is authoritative for labels.)
3. **Names** — `python tools/validate_names.py` when you touched `title=` or `translations.csv`.
4. **Checklist** below, item by item.
5. Offer LO to test in-game via the cheat menu's events page (it lists events by title and
   returns there after `end_event`).
6. Lint recompiles `.rpyc` files; restore any `.rpyc` you didn't mean to change
   (`git checkout -- <file>.rpyc`) so the diff stays clean.
7. If the event is player-visible new content that belongs on the roadmap, update
   `devstatus.json` via the `update-devstatus` skill.

## Checklist (the mistakes that actually happen)

**Definition**
- [ ] Label name == event string, character for character. Priority is 1, 2 or 3.
- [ ] `set_current_mod(...)` runs before any `Pattern`/thumbnail is built.
- [ ] Time gates use the right codes: daytime `c` class (2,4,5) · `f` free (1,3,6) · `d` day (1–6) · `n` night (7); weekday `d` workday · `w` weekend. Use `OR(...)` for "free time on workdays OR daytime on weekends".
- [ ] Level gate matches the scene's tone (`LevelCondition("1-", char_obj="school")`, `"3+"`, `"2-4"`; the character goes in `char_obj=` — a second positional argument is treated as an *option*, not the character).
- [ ] Flag phase: no `FlagCondition` = only runs when no flag is set. Intro-only → `FlagCondition("intro")`; also during camp → `FlagCondition("camp", exclusive=False)`.
- [ ] Every selector key used in a pattern `<key>` or `get_value` exists on the event; for a missing art variant, list the key as a `Pattern` alt key so it falls back to `$`.
- [ ] `SituationBarSelector` key equals `"situation:<sit>:<bar>"` when the label uses `get_bar_value`.
- [ ] Thumbnail points at a real file.
- [ ] Added to the right pool (read the building file for the pool keys).

**Label**
- [ ] `label name(**kwargs):` — and `label .branch(**kwargs):` for every branch.
- [ ] `$ begin_event(**kwargs)` is the first statement; bump `version="2"` etc. when steps/decisions change in an existing event.
- [ ] No `$ headmaster = Person[...]` / `$ emiko = Person[...]` — `begin_event` binds both. Other people: `$ yulan = Person["yulan_chen"]` and speak via `.say/.think/.whisper/.shout`.
- [ ] No legacy speaker names (`miwa_shout`, `secretary`, `headmaster_thought`, `girl_char`, …) in new code.
- [ ] Selector values read via `get_value` / `get_stat_value` / `get_bar_value` / `get_level` — never `kwargs["values"]`.
- [ ] Something is on screen before the first line of text (`image.show`, `show_pattern`, or `paperdoll_manager.set_background`).
- [ ] Choices use `$ call_custom_menu_with_text(...)` (a Python function — `$`, not `call`) with stable `MenuElement` keys, full branch targets `EventEffect("<event>.<branch>")`, and **at least one ungated element** (an all-gated menu dumps the player to the map with a dev error). Never a raw `menu:`.
- [ ] Every branch ends with its own `end_event(...)`.
- [ ] `end_event("none", ...)` is followed by `return` (otherwise Ren'Py falls through into the next label).
- [ ] Every `call ... from _id` has a project-unique id (convention: `_<event>_<n>` or a short prefix like `_nm_go_np_fix`).
- [ ] Stat amounts use the constants (`TINY`/`SMALL`/`MEDIUM`/`LARGE`, `DEC_*`), never raw numbers in `change_stats_with_modifier`.
- [ ] Paperdolls: `register_paperdoll()` before `display()`; `level=` matches the scene's level; no manual teardown needed (`image.show` and `end_event` clear it).

**Content rules (project canon)**
- [ ] Every character is an adult; "student", "class", "dorm" are roles at an adult boarding school.
- [ ] Only women plus the male Headmaster exist; any hookup is girl/girl, never another man. The setting is never called a girls' school in-fiction.
- [ ] Behaviour, dress and atmosphere match the gated school level (no low-level shame in a high-level scene and vice versa).
- [ ] Cast availability: Linh is a hospital nurse early on (school nurse only later); the PTA government rep stays out of scenes.
- [ ] Dialogue sounds human — people over-talk, hedge, breathe; not one clipped epigram per line, and each character has her own voice.
- [ ] Paperdoll is the default visual; propose a render only for payoff moments.
