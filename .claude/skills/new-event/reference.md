# Event author reference

Condensed from the wiki and checked against the code (2026-10-19). When something here
and the wiki disagree, the code wins. Look it up in `game/scripts/`.

## Contents
1. Classes & storages
2. Conditions
3. Selectors
4. Options
5. Patterns, images, video
6. Paperdoll in a scene
7. Dialogue & speakers
8. Decision menu
9. Consequences: stats, situations, progress, flags, modifiers, effects
10. begin_event / end_event
11. Pools by building
12. Cast keys
13. Situation wiring

---

## 1. Classes & storages

| Constructor | Use |
|---|---|
| `Event(select_type, event, *conds_selectors_options_patterns, thumbnail="", register_self=True, override_location=None, title=None)` | the plain event |
| `EventComposite(select_type, event, [FragmentStorage, ...], *conditions, thumbnail="", title=None)` | intro + shuffled fragments (`call composite_event_runner(**kwargs)`) |
| `EventFragment(select_type, event, *conditions, thumbnail="", title=None)` | a fragment; lives in a `FragmentStorage`, never in a location pool, no auto flag condition |
| `EventSelect(select_type, event, text, {"key": EventStorage, ...}, *conditions, thumbnail="", override_menu_exit="map_entry", fallback=None, person=None, title=None)` | a routing menu into other pools; label is `select_event_runner`, so you write no scene label |
| `EventStorage(name, location, *options, fallback=None, fallback_text="There is nothing to do here.")` | a pool |
| `FragmentStorage(name, *options)` | fragment pool, with `FragmentRepeatOption(number_or_selector, repeatable)` |

Select type: **`EVENT_BLOCKING`** (1) is a story beat (the first available one runs, nothing else). **`EVENT_ALWAYS`** (2) means every available one runs, one after another. **`EVENT_RANDOM`** (3) means one is picked at random (ambient default; no map highlight unless `ForceHighlightOption()`).

## 2. Conditions

All must pass. Combine with `AND(...)`, `OR(...)`, `NOT(...)`. Number arguments take value ranges: `"2"`, `"2+"`, `"3-7"`, `"4-"`, `"1,3,5"`.

| Constructor | Gate |
|---|---|
| `TimeCondition(day=, week=, month=, year=, daytime=, weekday=, date=, condition="+"/"-"/"")` | calendar. daytime: `1` Morning · `2` Early Noon · `3` Noon · `4` Early Afternoon · `5` Afternoon · `6` Evening · `7` Night; `c` class (2,4,5) · `f` free (1,3,6) · `d` day (1–6) · `n` night (7). weekday: `1`–`7`, `d` workday, `w` weekend |
| `LevelCondition(value, char_obj="school")` | school level (or another character's level). Pass the character as **`char_obj=`**, because a 2nd positional argument is an option |
| `StatCondition(char_obj=None, **stats)` | `StatCondition(corruption=20, happiness=50)` minimums |
| `ProgressCondition(key, value="")` | event-series step |
| `EventSeenCondition(seen, "event_name")` | seen / not seen |
| `GameDataCondition(key, value)` | a GameData flag equals value |
| `FlagCondition(flag_key, exclusive=True)` | event-phase flag (see below) |
| `SituationPoolCondition(situation_key, pool_key)` | situation active **and** bar inside that `SituationPool` band |
| `ThresholdReachedCondition(situation_key, threshold_key)` | a situation threshold was reached |
| `UnlockableCondition(key, group_index=-1)` | an unlockable is unlocked (replaces rule/club conditions) |
| `BuildingCondition(key)` | a map building is open |
| `ItemCondition(item_key, amount=1)` · `MoneyCondition(int)` | inventory / money (plain int, no ranges) |
| `TimerCondition(id, day=, daytime=...)` | a named timer has elapsed (cooldowns) |
| `RandomCondition(threshold, limit=100)` | random roll |
| `NumCompareCondition(key, value, ">")` · `ValueCondition` · `CompareCondition` · `KeyCompareCondition` | value compares |
| `ProficiencyCondition(subject, xp=, level=)` | teaching proficiency |
| `CheckReplay(condition)` | make a condition also evaluate in replay (normally conditions pass in replay) |
| `PlaceholderCondition()` | never true, a WIP marker |

**Flags:** an event without a `FlagCondition` gets `FlagCondition(None)` and runs only while no flag is set.

| Event has … | no flag | flag `camp` | other flag |
|---|---|---|---|
| nothing | ✅ | ❌ | ❌ |
| `FlagCondition("camp", exclusive=False)` | ✅ | ✅ | ❌ |
| `FlagCondition("camp")` | ❌ | ✅ | ❌ |
| `FlagCondition("x")` | ✅ | ✅ | ✅ |

Situation pool events without their own flag condition get `SituationFlagCondition` instead. Events called directly by `EventEffect("<label>")` skip all conditions.

## 3. Selectors

Each selector rolls a value into `kwargs["values"]` under its key. A `<key>` in a pattern fills from it, and the label reads it with a getter.

| Constructor | Value |
|---|---|
| `RandomListSelector(key, *values)` | random pick; weighted with `(0.7, "a")` tuples; values may be selectors |
| `IterativeListSelector(key, *values, options=[FragmentRerollOption()])` | next in order (re-rolls per fragment with that option) |
| `RandomValueSelector(key, min, max)` | random int |
| `StatSelector(key, STAT, "school", [low, high])` | a stat; read with `get_stat_value(key, [low, high], **kwargs)` |
| `LevelSelector(key, "school")` | a level; read with `get_level(key, **kwargs)`. `<school_level>` works in paths without a selector |
| `SituationBarSelector("situation:<sit>:<bar>", "<sit>", "<bar>")` | a situation bar; read with `get_bar_value("<sit>", "<bar>", 0, **kwargs)`. The key **must** be that composite string |
| `GameDataSelector(key, "gamedata_key", alt)` | a GameData flag (cross-event memory) |
| `ProgressSelector(key, progress_key)` | progress step |
| `ConditionSelector(key, Condition, true_value, false_value)` | branch a value on a condition |
| `ValueSelector(key, value)` · `KwargsSelector(**kv)` · `DictSelector` · `KwargsValueSelector` · `NumClampSelector` | fixed and derived values |
| `CharacterSelector(key, "school")` · `TimeSelector(key, "daytime")` | references |
| `ModifierSelector(key, Modifier_Obj(...), STAT, collection="default")` | a lasting modifier, activated in the label by `load_modifier(key, **kwargs)` |

Getters (they register the value for replay, so always go through them): `get_value(key, alt, **kwargs)` · `get_value_ng` (does not register) · `get_stat_value` · `get_bar_value` · `get_level` · `get_person_value(key, **kwargs)` (→ `Person`) · `get_person_char(key, **kwargs)` (→ `Character`) · `get_kwargs(key, alt, **kwargs)` (raw kwarg).

## 4. Options

`ReplayCategoryOption("cat")` groups the event in the gallery · `ForceHighlightOption()` / `NoHighlightOption()` control the map highlight · `PriorityOption(n)` (selection order, not the select type) · `ShowBlockedOption()` · `EventSeenDebuffOption(0.25)` (on an `EventStorage`) lowers the chance of seen events · `FragmentRepeatOption(n, repeatable)` · `FragmentRerollOption()` (on selectors) · `OptionalOption()` (on a condition: it never blocks).

## 5. Patterns, images, video

- `Pattern("main", "images/events/<area>/<event>/<event> <key> <school_level> <step>.webp", "alt_key", ...)`. Alt keys fall back to a `$` file when a specific variant is missing. Built-in keys: `<step>`, `<school_level>`, `<parent_level>`, `<variant>`, `<nude>`.
- Path convention: `images/events/<area>/<event_name>/<event_name> <tokens>.webp`. Backgrounds live in `images/background/<location>/...`.
- `$ show_pattern("main", **kwargs)` shows one static image. If the file does not exist yet, it shows nothing, so put a fallback background first.
- `$ image = convert_pattern("main", **kwargs)` builds an `Image_Series`. Then `image.show(step)`, `image[step]` (the resolved path, e.g. as a paperdoll background), and `convert_pattern("main", {"girls": "lin_kato"}, **kwargs)` to override a key.
- `call Image_Series.show_image(image, 0, 1, 2)` plays steps one per click.
- Video: `image.show_video(step, pause=True)`. Needs `image anim_<webp basename with spaces→_> = Movie(play="<...>.webm", start_image="<...>.webp", loop=True)` for every step × level that has a clip (see `templates/video_snippet.rpy`).

## 6. Paperdoll in a scene

```python
$ emiko.register_paperdoll()                                   # once per person per scene
$ paperdoll_manager.set_background(image[1], blur = True, **kwargs)   # or a background path
$ emiko.display(PDAImage(pose = "10", outfit = "uniform", level = 5, mood = "neutral", mouth = "open"),
    PDAPreset("close_body_center", duration = 0.4))
$ emiko.display(PDAImage(mood = "happy", mouth = "closed"))    # expression change
$ emiko.display(PDAMove(alignX = -0.2, duration = 1.0))        # make room for a menu
$ emiko.clear_display()                                        # optional; image.show / end_event clear anyway
```

- Values: `pose` (1–39, see LO's pose reference), `outfit` (`uniform` is the one in use), `level` (should match the school level; Emiko starts at 5), `mood` (in use: `neutral`, `happy`, `sad`, `shining`, `surprised`, `suspicious`, `pout`, `angry`), `mouth` (`open`/`closed`), `look` (`follow`/`avert`), `extra1`/`extra2`.
- Presets: `outside`, `close_body[_center|_left|_right]`, `upper_body[_center|_left|_right]`. Bare strings work without overrides.
- Actions: `PDAImage`, `PDAMove(alignX, alignY, zoom, duration)`, `PDAFlip(bool, duration)`, `PDAPause(s)`, `PDABlur`, `PDABw`, `PDAColor`, `PDAShake`, `PDAPreset`. Timed actions in sequence need a `PDAPause` between them.
- Two people: register both, put one at `_left` and one at `_right`. A slide-in from off-screen is `register_paperdoll(config={"alignX": 2.5})` and then a preset with a `duration`.
- Paperdoll is the default visual. Real renders are for payoff moments.

## 7. Dialogue & speakers

- `headmaster "..."`, `headmaster.think "..."`, `headmaster.shout/.whisper`; `emiko "..."` / `emiko.say/.think/...`. Both are bound by `begin_event`.
- Others: `$ miwa = Person["miwa_igarashi"]`, then `miwa.say` / `.think` / `.whisper` / `.shout`, and `"[miwa.get_full_name()]"` in text.
- Selector-picked person: `$ girl = get_person_value("girl_name", **kwargs)`, then `girl.say "..."`.
- Narration: `subtitles "..."` (also `character.subtitles` as a menu speaker). Dev notes: `character.dev`.
- Text tags: `{i}…{/i}`, `{b}…{/b}`; interpolate with `[var]`.

## 8. Decision menu

```python
$ high_charm = get_stat_value("charm", [20, 100], **kwargs) >= 20
$ call_custom_menu_with_text("What do you do?", character.subtitles, False,
    MenuElement("fix",       "Fix it",             EventEffect("my_event.fix")),
    MenuElement("charm_fix", "Charm your way out", EventEffect("my_event.charm_fix"), high_charm),
    MenuElement("leave",     "Leave it",           EventEffect("my_event.leave")),
    menu_anchor = MENU_ANCHOR_MIDDLE_RIGHT,
**kwargs)

label .fix (**kwargs):
    ...
    $ end_event(END_NEW_DAYTIME, **kwargs)
```

- Python function, so it's `$ call_custom_menu_with_text(text, speaker, with_leave, *elements, menu_anchor=..., **kwargs)`, or `$ call_custom_menu(with_leave, *elements, **kwargs)` without a prompt.
- `MenuElement(key, title, *effects_or_conditions_or_bool)`. The key is recorded for replay, so keep it stable (bump `begin_event(version=...)` if you change it). Gate with a bool or any `Condition`.
- Branch targets: use the full label `"<event>.<branch>"`, as the live code does.
- At least one element must always be available. If every element is gated out, the player gets a dev error and lands on the map.
- Anchors: default `MENU_ANCHOR_DIALOG` (right-aligned on top of the dialogue box), or `MENU_ANCHOR_{TOP,MIDDLE,BOTTOM}_{LEFT,CENTER,RIGHT}`. Move the paperdoll aside so the menu doesn't cover her.
- `with_leave=False` with a single element skips the menu and runs that element directly.
- Never use a raw Ren'Py `menu:`, because it does not replay.

## 9. Consequences

| What | How |
|---|---|
| School stats | `call change_stats_with_modifier(happiness=SMALL, inhibition=DEC_TINY) from _<event>_<n>`; optional first arg = modifier collection (`'pe'`, `'cafeteria'`, …). Amounts: `TINY` `SMALL` `MEDIUM` `LARGE`, `DEC_*` |
| Direct stat (rare, story) | `$ change_stat("charm", 5)` |
| Situation bar | `$ situation_manager.apply_progress_change("situation:<sit>:<bar>", n)` (no-op unless active). Stat changes also drift bars through `stat_weights` |
| Suppress that drift | `$ situation_manager.block_progress(situations=["<sit>"])`; `end_event` clears all blocks |
| Before activation | `$ situation_manager.shift_start_value("<sit>", "main", "+", -10)` |
| Activate a situation | `$ situation_manager.get_situation("<sit>").activate()` (usually at the end of the story event that introduces it) |
| Storyline progress | `$ start_progress("key")` · `$ set_progress("key", n)` → `ProgressCondition` / `ProgressSelector` |
| Cross-event memory | `$ set_game_data("nm_door_claimed", 1)` → `GameDataSelector` / `GameDataCondition` |
| Lasting modifier | `ModifierSelector` on the event + `$ load_modifier("key", **kwargs)` in the label (orphan-safe) |
| School level change | `$ school.set_level(n)` in story labels, or `LevelEffect` |
| Effects in menus or code | `EventEffect`, `ValueEffect`, `ProgressEffect`, `MoneyEffect`, `StatEffect` (character-scoped), `BuildingOpenEffect`, `NotificationEffect`, … |
| Journal attention | `$ raise_journal_alert("<topic>", key)` (situations and unlockables already do this themselves) |

Teasers, Emiko gifts and collectibles are pull-based. They watch `EventSeenCondition` themselves, so the event doesn't need to do anything for them.

## 10. begin_event / end_event

- `$ begin_event(version="1", **kwargs)`. Call it first. It hides screens, clears the layer (including the map image), stops sound, blocks rollback, marks the event seen, starts the gallery, initialises the paperdoll manager, and binds every registered person under its speaker name (`aona_komuro` → `aona`). Bump `version` when a read value is dropped, a value's options/range change, or a `MenuElement` key changes; added or reordered values reset the replay data by themselves.
- `$ end_event(type, **kwargs)`:
  - `"new_daytime"`: advances time (default for actions that cost time)
  - `"map_entry"` (or anything unknown): back to the map, no time passes
  - `"new_day"`: jumps to the next day
  - `"none"`: returns to the caller. **Follow it with `return`.** Use it for threshold/resolution/measure scenes and chained prio-2 time checks
  - `"custom"`: calls the label in value `return_label`
- `end_event` also ticks situations (thresholds, passives, teasers, resolutions), drains queued situation events, unloads the paperdolls, and in replay returns to the journal.

## 11. Pools by building

From `game/scripts/buildings/*.rpy`. **Re-read the file before wiring**, because pools change.

| Building | General pool | Action pools |
|---|---|---|
| cafeteria | `cafeteria_general_event` | `cafeteria_events[...]`: `look_around`, `order_food`, `eat_alone`, `search` |
| courtyard | `courtyard_general_event` | `courtyard_events[...]`: `patrol`, `search` |
| gym | `gym_general_event` | `gym_events[...]`: `enter_changing`, `go_students`, `check_pe`, `teach_pe`, `patrol`, `search` |
| kiosk | `kiosk_general_event` | `kiosk_events[...]`: `get_snack`, `search` |
| labs | `labs_general_event` | `labs_events[...]`: `look_around` |
| office building | `office_building_general_event` | `office_building_events[...]`: `look_around`, `work`, `learn`, `call_secretary`, `schedule_meeting`, `computer`, `search`; `office_building_work_event[...]`: `counselling`, `money`, `education`, `reputation`, `lab`; `office_building_computer_event["shopping"]`; `office_building_lab_events[...]`: `research`, `produce`; `office_building_subject_learn_events[...]`: `math`, `history`, `pe`, `sex_ed`; `office_building_call_secretary_events[...]`: `naughty_sandbox`, `talk` |
| school building | `sb_general_event` | `sb_events[...]`: `check_class`, `teach_class`, `patrol`, `search`; `sb_teach_events[...]`: `math`, `history`, `sex_ed` |
| school dormitory | `sd_general_event` | `sd_events[...]`: `peek_students`, `look_around`, `search` |
| bath / beach / sports field / staff lodges / swimming pool | `<name>_general_event` | (general pool only) |
| misc | `time_check_events` (daily_check.rpy), `sandbox_check_events` (event.rpy), `journal_events` (journal.rpy) | situation misc storages, e.g. `nm_threshold_events`, `nm_resolution_events` |

## 12. Cast keys (`Person["key"]`)

Students (class 3A): `aona_komuro`, `easkey_tanaka`, `elsie_johnson`, `gloria_goto`, `luna_clark`, `seraphina_clark`, `hatano_miwa`, `ikushi_ito`, `ishimaru_maki`, `kokoro_nakamura`, `lin_kato`, `miwa_igarashi`, `sakura_mori`, `soyoon_yamamoto`, `yuriko_oshima`.
Parents: `adelaide_hall`, `nubia_davis`, `yuki_yamamoto`.
Staff: `chloe_garcia`, `emiko_langley` (bound as `emiko`), `finola_ryan`, `lily_anderson`, `yulan_chen`, `zoe_parker`, `linh_nguyen` (a hospital nurse early on, the school nurse only later).
Player: `headmaster` (bound by `begin_event`).
Fallback roles for selectors: `default_school`, `default_parent`, `default_teacher`, `default_secretary`.

All of them are adults. The only man in the world is the Headmaster.

## 13. Situation wiring

```python
# on the Situation (situations.rpy)
SituationPool("my_band", -10, 15),                          # pool window on the bar
AutoThreshold("Hint text.", EventEffect("my_thresh_scene"), main=-12, direction=-1),
PositiveResolution("ALL", ValueEffect("my_sit_resolved", "positive"), EventEffect("my_sit_positive_resolve")),
NegativeResolution("ANY", ValueEffect("my_sit_resolved", "negative"), EventEffect("my_sit_negative_resolve"), grace_count=1),

# the pool event (building pool)
Event(EVENT_RANDOM, "my_band_scene", SituationPoolCondition("my_sit", "my_band"), ...)

# the threshold / resolution scenes (misc storage, only fired by EventEffect)
my_sit_scene_events = EventStorage("my_sit_scenes", "misc")
my_sit_scene_events.add_event(
    Event(EVENT_ALWAYS, "my_thresh_scene", override_location="misc"),
    Event(EVENT_ALWAYS, "my_sit_positive_resolve", Pattern("main", "..."), override_location="misc"))
```

Situation scenes end with `$ end_event(END_NONE, **kwargs)` followed by `return`. Every resolution needs at least one effect (`DummyEffect()` as a placeholder). Hint text and teasers are written as the headmaster's case notes. Full model: `wiki/Building-Situations.md`.
