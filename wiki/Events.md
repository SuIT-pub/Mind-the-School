> **Audience:** Developers writing *Mind the School* scenes — the events players reach
> by exploring buildings and through story triggers. This guide covers every event
> class, how events are defined and registered, and — in depth — how the **scene
> label** is written: reading selector values, showing images and videos, using
> characters, and the event **decision-menu** system used for branching and replay.
>
> **Scope:** The event system (`event.rpy`), its scene helpers (`images.rpy`,
> `menu.rpy`, `gallery.rpy`, `character.rpy`) and how content files wire it up. Events
> lean on: [Conditions](Conditions) (gates), [Selectors](Selectors) (dynamic values),
> [Effects](Effects) / [Modifiers](Modifiers) (consequences), [Options](Options)
> (flags), and [Building Situations](Building-Situations) (event pools).

---

## Quick start

An event is **two things that share a name**: a **definition** (`Event(...)`, holding
metadata) registered into a pool, and a **scene label** (`label <name>(**kwargs):`) —
the Ren'Py scene that plays.

```python
init 1 python:
    set_current_mod('base')
    my_event = Event(3, "cafeteria_snack_chat",             # priority 3, label name
        TimeCondition(daytime="d"),                         # gate: only at daytime "d"
        RandomListSelector("topic", "coffee", "tea"),       # dynamic value → <topic>
        Pattern("main", "images/events/cafeteria/snack_chat/<topic> <step>.webp"),
        thumbnail="images/events/cafeteria/snack_chat/coffee 1.webp")
    cafeteria_events["order_food"].add_event(my_event)      # into the pool

label cafeteria_snack_chat(**kwargs):
    $ begin_event(**kwargs)
    $ topic = get_value("topic", **kwargs)                  # read the rolled selector
    $ image = convert_pattern("main", **kwargs)             # build the stepped image
    $ image.show(0)
    "She sips her [topic]."
    $ image.show(1)
    call change_stats_with_modifier(happiness=SMALL) from _e1
    $ end_event("new_daytime", **kwargs)
```

Everything below expands each piece.

---

## Contents

1. [The event lifecycle](#1-the-event-lifecycle)
2. [The event classes](#2-the-event-classes)
3. [Storages & pools](#3-storages--pools)
4. [Defining an event](#4-defining-an-event)
5. [Priorities & availability](#5-priorities--availability)
6. [Registering & wiring into locations](#6-registering--wiring-into-locations)
7. [The scene label: begin_event / end_event](#7-the-scene-label-begin_event--end_event)
8. [Reading selector values in the label](#8-reading-selector-values-in-the-label)
9. [Images: patterns, steps & Image_Series](#9-images-patterns-steps--image_series)
10. [Videos](#10-videos)
11. [Characters & dialogue](#11-characters--dialogue)
12. [The decision-menu system](#12-the-decision-menu-system)
13. [Changing stats & progress](#13-changing-stats--progress)
14. [Composite events & fragments](#14-composite-events--fragments)
15. [Select events](#15-select-events)
16. [Gallery, seen-tracking & replay](#16-gallery-seen-tracking--replay)
17. [Modding events](#17-modding-events)
18. [Conventions](#18-conventions)
19. [Troubleshooting](#19-troubleshooting)
20. [Reference tables](#20-reference-tables)

---

## 1. The event lifecycle

1. **Definition** — an `Event(...)` object is built in an `init python` block and
   holds priority, gates (conditions), dynamic values (selectors), image patterns and
   a thumbnail. It registers itself into the global `event_register` and is added to a
   pool.
2. **Selection** — the player enters a location and picks an action. The location's
   `EventStorage` gathers **available** events (all conditions pass) and, by priority,
   selects what runs (see §5). If nothing is available, the pool's **fallback** runs.
3. **Call** — the selected event's `call()` merges its rolled selector values into
   `kwargs["values"]`, attaches its patterns as `kwargs["image_patterns"]`, sets
   `event_name`/`event_obj`, and `renpy.call`s the scene label.
4. **Scene** — the `label` runs: `begin_event`, then images/dialogue/menus/stat
   changes, then `end_event`, which returns to the map (or advances the day) and ticks
   the surrounding systems (situations, quests).

The definition and the label are joined only by the **event string = label name**.
`check_event()` validates that the label exists (`renpy.has_label`) and the priority
is 1–3; failures are logged (category `event`) and the event is marked invalid.

---

## 2. The event classes

All four subclass `Event`; the differences are how they select/run their content.

### `Event` — the plain event

```python
Event(select_type, event, *conditions_selectors_options_patterns,
      thumbnail="", register_self=True, override_intro=False, override_location=None)
```

- **`select_type`** — priority 1/2/3 (§5).
- **`event`** — the scene label name (string).
- **`*args`** — a **mixed list** sorted by type: `Condition` (gates), `Selector`
  (values), `Option` (flags), `Pattern` (images) — in any order (§4).
- **`thumbnail`** — journal/menu image (falls back to `journal/empty_image_wide.webp`).
- **`register_self`** — register into `event_register` (leave `True`; seen-tracking and
  replay need it).
- **`override_intro`** — skip the auto-added `IntroCondition(False)` (which otherwise
  hides the event during the intro).
- **`override_location`** — force the event's location tag.

### `EventComposite` — an event assembled from fragments

```python
EventComposite(priority, event, fragments: List[FragmentStorage], *conditions, thumbnail="")
```

A wrapper scene that plays a **sequence of fragments** pulled from the given
`FragmentStorage`s. Its own label runs an intro and then hands off to
`composite_event_runner`, which selects fragments (`select_fragments`) and plays them
in turn (`call_fragment`). Used for events with a repeating, shuffled middle (e.g.
*Truth or Dare*: a random number of truth/dare fragments, then an end fragment). See
§14.

### `EventFragment` — a reusable scene fragment

```python
EventFragment(select_type, event, *conditions, thumbnail="")
```

A scene that lives in a `FragmentStorage` (location `"fragment"`) and is pulled into a
composite. Authored like a normal event label; it does **not** register into a
location pool.

### `EventSelect` — a routing menu

```python
EventSelect(priority, event, text, event_list: Dict[str, EventStorage], *conditions,
            thumbnail="", override_menu_exit="map_entry", fallback=None, person=None)
```

Presents a menu (`text`, spoken by `person`) that routes to one of several
`EventStorage`s in `event_list`; its label is `select_event_runner`, which calls the
location action menu (`call_event_menu`) and, on exit, jumps to `override_menu_exit`.
Available only if at least one storage in `event_list` has an available event. See §15.

---

## 3. Storages & pools

### `EventStorage`

```python
EventStorage(name, location, *options, fallback=None, fallback_text="There is nothing to do here.")
```

A pool of events for a location. Holds three priority buckets internally. `fallback`
is the `Event` run when nothing is available; `fallback_text` is its "nothing to do"
line. `register_highlighting(*storages)` opts a pool into the map "available event"
highlight. `add_storage(dict, storage)` indexes a storage under its name in a dict.

A building typically builds a dict of per-action pools plus a "general" pool:

```python
cafeteria_events = {}
add_storage(cafeteria_events, EventStorage("look_around", "cafeteria", fallback_text="Nothing to see here."))
add_storage(cafeteria_events, EventStorage("order_food",  "cafeteria", fallback_text="I'm not hungry."))

cafeteria_general_event = EventStorage("cafeteria_general", "cafeteria",
    fallback=Event(2, "cafeteria.after_general_check"))
register_highlighting(cafeteria_general_event)
```

### `FragmentStorage`

```python
FragmentStorage(name, *options)          # location fixed to "fragment"
```

Holds `EventFragment`s for a composite. A `FragmentRepeatOption(number, repeatable)`
controls how many fragments the composite pulls from it and whether the same fragment
may repeat — `number` may be a `Selector` for a random count:

```python
truth_or_dare_storage = FragmentStorage("truth_or_dare",
    FragmentRepeatOption(RandomValueSelector("", 2, 6, True), False))   # 2–6, no repeats
```

---

## 4. Defining an event

After the label name, an event takes any mix of four element types (the constructor
sorts them):

- **Conditions** — gates; the event is available only when **all** pass (§5). Compose
  with `AND`/`OR`/`NOT` ([Conditions](Conditions)). An `IntroCondition(False)` is
  auto-added unless you pass your own `IntroCondition` or `override_intro=True`. A
  `LevelCondition` also registers the event under its max level for level-based
  bookkeeping.
- **Selectors** — dynamic values rolled when the event runs, exposed under their key
  ([Selectors](Selectors)). They can be weighted/conditional:
  `RandomListSelector('topic', (0.7, 'apron'), (0.2, 'breasts'), 'nude')`.
- **Options** — flags parsed specially: `PriorityOption(n)` sets priority,
  `ForceHighlightOption()` forces highlight eligibility, `ReplayCategoryOption(cat)`
  sets the gallery category, `EventSeenDebuffOption(x)` lowers re-selection weight once
  seen. Others are stored on the event ([Options](Options)).
- **Patterns** — named, mod-redirected image patterns (§9).

```python
truth_or_dare_event_1 = Event(3, "truth_or_dare_1",
    TimeCondition(daytime="n"),
    LevelCondition("2,3", char_obj="school"),
    NOT(ProgressCondition("truth_or_dare")),
    ReplayCategoryOption("truth_or_dare"),
    Pattern("main", base_path + "truth_or_dare_1/truth_or_dare_1 <school_level> <step>.webp"),
    thumbnail=base_path + "truth_or_dare_1/truth_or_dare_1 6 2.webp")
```

---

## 5. Priorities & availability

An event is **available** when every condition passes. Among available events in a
pool, `select_type` / priority decides what runs:

| Priority | Behavior |
|----------|----------|
| **1** | highest — the first available `1` runs and **blocks** all others (forced story beats) |
| **2** | all available `2`s run in sequence |
| **3** | one is chosen **at random** among available `3`s (the sandbox default) |

Most ambient events are `3`; a story interrupt is `1`. Highlighting: priority-3 events
don't light up the map unless they carry `ForceHighlightOption()`;
`is_highlighted()` combines availability, priority and the options'
`check_options(Highlight=True, …)`.

---

## 6. Registering & wiring into locations

Build events in an `init python` block (set the mod first), then add them to pools:

```python
init 1 python:
    set_current_mod('base')
    # … build event objects …
    cafeteria_events["order_food"].add_event(cafeteria_event_1, cafeteria_event_2)
    cafeteria_general_event.add_event(cafeteria_construction_event)
```

The location's entry label runs the pools — a "general" pass first, then the action
menu:

```python
label cafeteria():
    call call_available_event(cafeteria_general_event) from cafeteria_4
label .after_general_check(**kwargs):
    call call_event_menu("What to do at the Cafeteria?", cafeteria_events,
        default_fallback, character.subtitles, **kwargs) from _cafeteria_menu
```

`call_available_event(storage, priority=0, no_fallback=False, **kwargs)` runs the
available events of a storage; `call_event_menu(text, events, fallback, person,
**kwargs)` renders the per-action choice menu. `set_current_mod` before building
`Pattern`s redirects their paths into the active mod's folder (§17).

---

## 7. The scene label: begin_event / end_event

Every scene is a Ren'Py label named exactly like the event, bracketed by two calls:

```python
label truth_or_dare_2(**kwargs):
    $ begin_event(**kwargs)
    # … the scene …
    $ end_event("new_daytime", **kwargs)
```

- **`$ begin_event(version="1", **kwargs)`** — call it first (after any pre-scene
  choices). It hides prior images, stops sound, **blocks rollback** (locking in rolled
  selector values and choices), marks the event **seen** (`set_event_seen`), and starts
  a `Gallery_Manager` for replay (unless `no_gallery=True` in kwargs). Bump `version`
  when a scene's structure changes so stale replays are invalidated.
- **`$ end_event(return_type="new_daytime", **kwargs)`** — call it last. `"new_daytime"`
  advances to the next daytime segment; `"map_entry"` returns to the map; in replay it
  returns to the journal. It also ticks the situation manager (teasers, thresholds,
  passives, resolutions) and clears progress blocks.

Never hand-roll the seen/gallery/rollback hooks — always bracket with these.

Branches are `.`-prefixed sub-labels (`label .peek_1(**kwargs):`) reached from the
decision menu (§12) or `call`/`jump`. Each branch that is entered independently should
also `begin_event`/`end_event` if it is a distinct scene.

---

## 8. Reading selector values in the label

Selector values arrive in `kwargs["values"]`. **Read them through the gallery-aware
getters** so they are recorded for replay:

| Getter | Returns |
|--------|---------|
| `get_value(key, alt=None, **kwargs)` | the rolled selector value (and registers it for replay) |
| `get_value_ng(key, alt=None, **kwargs)` | same, **without** registering (transient) |
| `get_stat_value(key, ranges, alt=100, **kwargs)` | a stat-selector value normalized into `ranges` |
| `get_level(key, **kwargs)` | a character's level (replay-safe) |
| `get_kwargs(key, alt, **kwargs)` | a raw kwarg (not a selector value) |

```python
$ topic  = get_value("topic", **kwargs)
$ level  = get_stat_value("corr", [0, 40, 70, 100], **kwargs)
```

Prefer `get_value` over reaching into `kwargs["values"]` directly — the registration is
what makes the scene replayable. `<key>` placeholders in image paths are filled from
the same `values` automatically (§9), so you only call the getters for values you use
in Python/dialogue logic.

---

## 9. Images: patterns, steps & Image_Series

Images are declared as **patterns** on the event and shown from the label. The
resolver underneath (placeholders, `$` alternatives, PNG/WebP, mod prefixes) is
documented in [Images](Images). This section is the event-authoring surface.

### Patterns

`Pattern(key, path, *alternative_keys)` names an image pattern. `path` contains
`<placeholder>`s filled from selector values and built-in keys (`<step>`,
`<school_level>`, `<parent_level>`, `<variant>`, `<nude>`, and any selector key). An
event can hold several named patterns (`"main"`, `"base"`, `"card"`, …). Patterns are
**mod-redirected** (built while `set_current_mod` points at a mod).

### Showing a single image

```python
$ show_pattern("main", **kwargs)      # resolves & shows the pattern's image
```

Use this for a static scene image.

### Stepped scenes (Image_Series)

For a scene that advances through numbered frames, turn the pattern into an
`Image_Series` and drive its `<step>`:

```python
$ image = convert_pattern("main", **kwargs)     # -> Image_Series from the "main" pattern
$ image.show(0)                                  # show step 0
"Dialogue over frame 0."
$ image.show(1)                                  # advance to step 1
```

- `convert_pattern(pattern_key, **kwargs)` builds the series (its `<key>`s already
  filled from `values`).
- `image.show(step, display_type=SCENE, variant=-1)` shows a specific `<step>`.
- `convert_pattern_with_data(pattern_key, {"key": value}, **kwargs)` builds a series
  with an extra/overridden substitution (e.g. force `<girls>` to a specific character
  for one image).
- The `Image_Series.show_image(image, *steps)` label plays several steps in sequence
  (advancing on click) — handy for a short run of frames with no dialogue between.

`<step>` and `<nude>` are resolved by the image system; a `<nude>` image shows the
highest available nude level for the current state.

---

## 10. Videos

A video is the **animated version of a step**: same stepped `Pattern` as a static
scene (§9), but each frame also has a looping `Movie`, and you play it with
`image.show_video(...)` instead of `image.show(...)`. The image system finds the
`Movie` by a **name convention** derived from the step's `.webp` path, so you don't
reference it directly.

### 1. Same pattern as the static images

The event's pattern points at the `.webp` frames exactly as for a stepped scene:

```python
Pattern("main", "/images/events/teaching/pe/warm_up/warm_up_1/teaching_pe_warm_up_1 <school_level> <step>.webp")
```

### 2. Define a `Movie` image per frame — `anim_` + the webp basename

For every frame that has video, declare a `Movie` image whose **name is
`anim_` + the resolved `.webp` filename, spaces replaced by underscores**. That is
exactly the key `show_video` builds, so the names must line up:

```python
define anim_gtpewu1_path = "/images/events/teaching/pe/warm_up/warm_up_1/teaching_pe_warm_up_1 "
# webp ".../teaching_pe_warm_up_1 1 0.webp"  ->  image name "anim_teaching_pe_warm_up_1_1_0"
image anim_teaching_pe_warm_up_1_1_0 = Movie(play = anim_gtpewu1_path + "1 0.webm", start_image = anim_gtpewu1_path + "1 0.webp", loop = True)
image anim_teaching_pe_warm_up_1_1_1 = Movie(play = anim_gtpewu1_path + "1 1.webm", start_image = anim_gtpewu1_path + "1 1.webp", loop = True)
# … one per <school_level> × <step> (× variant) that has a clip …
```

- **`play`** — the `.webm`. **`start_image`** — the matching `.webp`, shown until the
  video is ready and as a fallback if it can't play (always ship it). **`loop=True`**
  keeps the clip running.
- The derived name is `video_prefix + basename(webp, no ext).replace(" ", "_")`, with
  `video_prefix` defaulting to `"anim_"` (overridable via a `video_prefix` kwarg). So
  the `Movie` image name must equal `anim_` + the same tokens the `<...>` placeholders
  resolve to.

### 3. Play it from the label with `show_video`

```python
label gym_teach_pe_warm_up_1(**kwargs):
    $ begin_event("2", **kwargs)
    $ image = convert_pattern("main", **kwargs)     # same Image_Series as for statics
    $ image.show_video(0, True)                      # play step 0's clip, wait for click
    $ image.show_video(1, True)
    $ image.show_video(2, True)
    headmaster "Alright, that's enough."
    call change_stats_with_modifier('pe', charm=SMALL, education=TINY) from _e_pe
    $ end_event('new_daytime', **kwargs)
```

`image.show_video(step, pause=False, variant=-1)`:

- resolves the step's `.webp` (from the pattern, `<school_level>`/`<step>`/… filled),
  derives the `anim_…` name, and shows that `Movie`;
- **`pause=True`** waits for a click before returning (so consecutive
  `show_video(0, True); show_video(1, True)` play one clip per click); `pause=False`
  shows and continues;
- **`variant=-1`** picks a random variant, like `image.show`.

Use `image.show(step)` for the static frame and `image.show_video(step, …)` for its
animated version — both come from the **same** `convert_pattern("main")` series, so a
scene can freely mix stills and clips.

---

## 11. Characters & dialogue

Dialogue uses Ren'Py `say` statements with a **Character** object.

### Fixed characters

Keep the **`Person` object** and speak through its speech-mode properties — you get
dialogue *and* access to the rest of the person (name, level, …) from one variable, no
second definition:

```python
$ miwa = Person["miwa_igarashi"]
miwa.say     "That was crazy..."
miwa.think   "...why did she do that?"
miwa.whisper "Don't tell anyone."
miwa.shout   "Watch out!"
"[miwa.get_full_name()] blushes."     # same object, other members
```

`Person["key"]` returns the `Person`; each property returns a fresh Ren'Py
`Character` in a speech mode, so a say statement can use it directly (Ren'Py evaluates
the who-expression, and dotted/subscript expressions are allowed — even
`Person["miwa_igarashi"].say "..."` works inline):

| Property | Mode |
|----------|------|
| `.say` | normal speech |
| `.think` | inner monologue — italic, parenthesized, suffix "(thinking)" |
| `.whisper` | italic, suffix "(whispering)" |
| `.shout` | bold, suffix "(shouting)" |

The older `$ miwa = Person["miwa_igarashi"].get_renpy_char(char_type="")` form still
works and returns the same `Character` (`char_type` ∈ `""` / `"thought"` / `"whisper"`
/ `"shout"`) — but the property form avoids the double `get_renpy_char()` definition
some events still carry. Each property access builds a new `Character`; that's cheap
and behaves identically (same name, `retain=False`).

Predefined narration characters are also available directly — e.g.
`headmaster_thought` (inner monologue), `character.subtitles` (neutral subtitle
voice), `character.dev` (developer notes).

### Selected characters

When a **selector** picked the character (its value is a character key), resolve it to
a speaking character:

```python
$ girl = get_person_char("girl_name", **kwargs)        # selector "girl_name" -> Character
girl "Fine, I'll do the dare."
```

- `get_person_char(key, alt=None, **kwargs)` → a Ren'Py `Character` for the selected
  key (handles the `school`/`parent`/`teacher`/`secretary` roles and falls back to a
  default view). Use it when you only need the speaking character.
- `get_person_value(key, alt=None, **kwargs)` → the resolved **`Person`** object — so
  you get the same speech-mode properties as a fixed character *and* the person's other
  members:
  ```python
  $ girl = get_person_value("girl_name", **kwargs)
  girl.say   "Fine, I'll do the dare."
  girl.think "...this is embarrassing."
  ```
- `get_person_char_with_key(group_key, name, char_type="")` → resolve a character from
  a collection group plus a name.

This is why an event stays generic: the selector chooses *who*, and
`get_person_value` / `get_person_char` turn that choice into the voice that speaks.

---

## 12. The decision-menu system

Player choices inside an event go through a **purpose-built decision menu**, not a
plain Ren'Py `menu:`. It records each choice into the gallery so the scene can be
**replayed** (and, in replay, only the originally-possible branches are offered).

### Building a decision menu

```python
label truth_or_dare_4_choice(**kwargs):
    call call_custom_menu_with_text(
        "Truth or Dare?", character.subtitles, True,
        MenuElement("truth", "Pick Truth", EventEffect(".truth_branch")),
        MenuElement("dare",  "Pick Dare",  EventEffect(".dare_branch")),
        MenuElement("peek",  "Keep watching", EventEffect(".peek"),
            StatCondition(corruption=20)),                 # gated choice
        **kwargs
    ) from _tod_choice
```

- **`call_custom_menu_with_text(text, person, with_leave, *MenuElement, **kwargs)`** —
  a decision menu with a prompt line. `call_custom_menu(with_leave, *elements,
  **kwargs)` is the same without prompt text. `with_leave` adds a "leave" option.
- **`MenuElement(key, title, *data, active=True, overwrite_position=None)`** — one
  choice. `key` is the **decision key** recorded for replay (keep it stable and
  unique within the menu). `title` is the displayed label. `*data` may include:
  - `Effect`s to run when chosen — most often `EventEffect("<label>")` to jump into a
    branch (a string label works too);
  - `Condition`s (or a bare `bool`) that gate whether the choice appears.

### What happens on choose

`call_element` registers the decision (`register_decision(key)` outside replay; appends
to `made_decisions` in replay), then runs the element's effects (a label is `call`ed, an
`Effect` is applied). So a choice both **branches** the scene and **records** itself.

### Replay behavior

In replay, the menu is filtered by `get_decision_possibilities(...)` to the decisions
that were actually recorded, so the gallery reproduces the original branch set. This is
why you must use the decision menu (not a raw `menu:`) for any in-event choice you want
in the gallery — and why decision `key`s must stay stable across versions (bump the
event `version` in `begin_event` if you restructure them).

---

## 13. Changing stats & progress

Change **school stats** through the modifier path so global modifiers apply:

```python
call change_stats_with_modifier(happiness=SMALL, inhibition=DEC_SMALL) from _e3
# with an explicit collection/context (e.g. a subject or location):
call change_stats_with_modifier('pe', happiness=MEDIUM, charm=SMALL) from _e4
```

- The optional first positional is the modifier **collection** (default `'default'`;
  e.g. `'pe'`, `'cafeteria'`) — it selects which `default`-collection modifiers reshape
  the change ([Modifiers](Modifiers)).
- Amounts are named constants — `TINY`, `SMALL`, `MEDIUM`, `LARGE` and their `DEC_`
  decrement forms (`DEC_TINY`, `DEC_SMALL`, …). Use these, not magic numbers.
- These changes also auto-drift active situations via their `stat_weights`, and a
  situation bar can be pushed directly with a `situation:<key>:<bar>` key
  ([Building Situations](Building-Situations) §13).

### Activating a lasting modifier (orphan-safe)

`change_stats_with_modifier` applies a **one-shot** change at event time. To install a
**lasting** modifier from an event — a drift/buff that stays registered after the scene
ends — attach a `ModifierSelector` ([Selectors](Selectors)) and activate it in the label:

```python
# in the definition:
Event(3, "cafeteria_regulars",
    ModifierSelector("regulars_bonus", Modifier_Obj("regulars_bonus", "+", 2),
                     HAPPINESS, collection="daily"),
    ...)

# in the scene label, where the modifier should take effect:
$ load_modifier("regulars_bonus", **kwargs)
```

`load_modifier` does two things: it **applies** the modifier and **registers** it with
the lifecycle registry, owned by this event (registry key `"<event>:<selector_key>"`).
You do **not** manage its removal:

- Every load wave the event system runs `check_selectors()` on each registered event,
  which KEEP-pings that event's `ModifierSelector` modifiers — so the modifier survives.
- If the event ever stops being registered (e.g. its mod is removed, so its definition
  never runs), nothing re-affirms the modifier and the next lifecycle sweep removes it —
  no orphan. This is the managed-modifier model in [Modifiers](Modifiers).
- `load_modifier` is a **no-op in replay** and when no `event_name` is in context.

Use this only for modifiers meant to outlive the event. For an immediate stat change,
stay with `change_stats_with_modifier`; for character-scoped or one-off effects use the
[Effects](Effects).

**Event-series progress** tracks multi-part storylines:

```python
$ start_progress("truth_or_dare")          # begin (progress 0/started)
$ set_progress("truth_or_dare", 2)         # set a step
```

Gate later events on it with `ProgressCondition("truth_or_dare", 2)` and read it with a
`ProgressSelector`.

For character stats or one-off actions, use the [Effects](Effects) (`StatEffect`,
`MoneyEffect`, …) rather than the school-stat modifier path.

---

## 14. Composite events & fragments

A composite is a scene whose middle is a **shuffled run of fragments**.

**Definition** — an `EventComposite` referencing one or more `FragmentStorage`s, each
filled with `EventFragment`s:

```python
truth_or_dare_storage     = FragmentStorage("truth_or_dare", FragmentRepeatOption(RandomValueSelector("", 2, 6, True), False))
truth_or_dare_end_storage = FragmentStorage("truth_or_dare_end")

truth_or_dare_4 = EventComposite(3, "truth_or_dare_4",
    [truth_or_dare_storage, truth_or_dare_end_storage],
    TimeCondition(weekday="d", daytime="n"),
    ProgressCondition("truth_or_dare", 3),
    IterativeListSelector("girls", "ikushi_ito", "lin_kato", "miwa_igarashi", options=[FragmentRerollOption()]),
    Pattern("base", base_path + "…/main <school_level> <step>.webp"),
    Pattern("card", base_path + "…/card <girls> <school_level> <step>.webp"))

truth_or_dare_storage.add_event(
    EventFragment(2, "truth_or_dare_truth_1", LevelCondition("2-10"), ReplayCategoryOption("truth_or_dare"),
        Pattern("main", base_path + "…/truth_1 <school_level> <step>.webp")),
    # … more truth/dare fragments …
)
truth_or_dare_end_storage.add_event(
    EventFragment(2, "truth_or_dare_end", ReplayCategoryOption("truth_or_dare"), Pattern("main", …)))
```

**Flow** — the composite's own label plays an intro, then hands off:

```python
label truth_or_dare_4(**kwargs):
    $ begin_event(**kwargs)
    $ image = convert_pattern("base", **kwargs)
    $ image.show(0)
    ishimaru "Okay, let's start! Pull a card."
    call composite_event_runner(**kwargs) from _tod4_run     # selects & plays fragments
```

`composite_event_runner` calls `select_fragments` (which honors each storage's
`FragmentRepeatOption` — count and repeatability) and plays the chosen fragments in
order via `call_fragment`, then `end_event`s. Each fragment is its own label
(`begin_event`/scene/`end_event`).

Notes:
- A `Selector` marked `FragmentRerollOption()` (like `girls`) is **re-rolled between
  fragments**, so each fragment can feature a different pick.
- Fragment patterns are exposed as `frag_image_patterns`; `convert_pattern`/
  `show_pattern` inside a fragment resolve against them.
- The composite's own patterns (`base`, `card`) remain available during its intro/outro.

---

## 15. Select events

`EventSelect` presents a menu that routes into other pools — use it when one map action
should offer a sub-choice of storages:

```python
peek_select = EventSelect(3, "dorm_peek_select", "Which room do you peek into?",
    { "left": dorm_left_events, "right": dorm_right_events },
    TimeCondition(daytime="n"),
    override_menu_exit="map_entry", person=character.subtitles)
```

Its label is `select_event_runner`, which renders `call_event_menu(text, event_list,
fallback, person, …)` and, after the chosen sub-event, jumps to `override_menu_exit`.
It is available only if some storage in `event_list` has an available event, and it
highlights if any of them have a highlightable event.

---

## 16. Gallery, seen-tracking & replay

`begin_event` records the event as **seen** and (outside replay) starts a
`Gallery_Manager` that captures the rolled values and decisions, so the scene can be
replayed from the journal gallery. Implications for authors:

- **Seen state** is queryable: `EventSeenCondition(True, "event_name")` /
  `get_event_seen(...)` — this is how later content reacts to what the player saw.
- **Read values via `get_value`** and **choose via the decision menu** — both register
  into the gallery; anything read/chosen another way won't replay correctly.
- **Conditions pass in replay** (the base `Condition.is_fulfilled` returns `True` when
  `in_replay`/gallery), so replays play straight through — don't rely on a gate to skip
  scene-critical code.
- **Version your scenes**: `begin_event(version="2", **kwargs)` invalidates stale
  galleries when you restructure a scene's steps or decisions.
- **`ReplayCategoryOption("category")`** groups a storyline's events/fragments together
  in the gallery (e.g. all *Truth or Dare* fragments under `"truth_or_dare"`).

---

## 17. Modding events

Events are fully moddable:

```python
init 1 python:
    set_current_mod('my_mod')            # redirect Pattern/thumbnail paths into the mod
    my_event = Event(3, "mymod_scene", TimeCondition(daytime="d"),
        Pattern("main", "images/events/mymod_scene/<step>.webp"),
        thumbnail="images/events/mymod_scene/1.webp")
    cafeteria_events["look_around"].add_event(my_event)     # extend a base pool …
```

- `set_current_mod(key)` at the top makes `Pattern`s and the thumbnail resolve into
  your mod folder — write **plain paths relative to your mod root**, never
  `mods/MyMod/...`.
- You can add events to **base pools** or your own, gate on base state, and be gated by
  it — coupling is only through keys, conditions and progress.
- The mod's event count is tracked (`change_mod_event_count`).

---

## 18. Conventions

- **Definition name = label name.** A mismatch means "available event, missing label" —
  `check_event` logs it and the event is invalidated.
- **Always bracket** scenes with `begin_event` / `end_event`; branches that are distinct
  scenes get their own pair.
- **Gate with conditions, vary with selectors.** Don't hard-code the time, character or
  variant — select them and reference `<key>` in the pattern.
- **Read values with `get_value`** (not raw `kwargs["values"]`) and **branch with the
  decision menu** (not a raw `menu:`) so scenes replay correctly.
- **Use the amount constants** and `change_stats_with_modifier` for stat changes; use
  progress for storyline gating.
- **Keep decision `key`s and selector keys stable**; bump the event `version` when you
  restructure steps/decisions.
- **Set the mod context** before building `Pattern`s so images redirect.
- **Ship a `start_image`** next to every `Movie`.
- **Priority intent:** `3` ambient, `2` always-run, `1` blocking interrupt.

---

## 19. Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| "Nothing to do here" when you expect an event | No event's conditions pass, or none registered in that pool | Check gates (time/level/progress); confirm `add_event` into the right pool. |
| Crash on firing | Label name ≠ `Event` string, or label missing | Make them identical; define the label (see the `event` log category). |
| Image shows a literal `<key>` | Selector missing/misnamed, or read outside the pattern | Add the selector; match the key; for logic use `get_value`. |
| Value differs between image and dialogue | Read via raw kwargs, or a `realtime` selector re-rolled | Read once with `get_value`; keep the selector cached (§8, [Selectors](Selectors)). |
| Choice missing in replay | A raw `menu:` was used, or the decision `key` changed | Use `call_custom_menu_with_text` + stable `MenuElement` keys; bump `version`. |
| Mod images not found | `set_current_mod` not set before the `Pattern` was built | Set the mod context at the top of the `init` block. |
| Composite plays nothing | Empty `FragmentStorage`, or no fragment's conditions pass | Add fragments; loosen their gates; check the `event` log. |
| Story event won't interrupt | It's priority 3 (random) not 1 (blocking) | Use `select_type=1`. |
| Situation event never appears | Missing/incorrect pool condition or bar out of range | Match the `SituationPoolCondition` and the `SituationPool` range ([Building Situations](Building-Situations)). |

---

## 20. Reference tables

### Classes
`Event(select_type, event, *conditions|selectors|options|patterns, thumbnail="", register_self=True, override_intro=False, override_location=None)` ·
`EventComposite(priority, event, fragments, *conditions, thumbnail="")` ·
`EventFragment(select_type, event, *conditions, thumbnail="")` ·
`EventSelect(priority, event, text, event_list, *conditions, thumbnail="", override_menu_exit="map_entry", fallback=None, person=None)` ·
`EventStorage(name, location, *options, fallback=None, fallback_text="…")` ·
`FragmentStorage(name, *options)`.

### Scene skeleton
`label <event>(**kwargs):` → `$ begin_event(**kwargs)` … `$ end_event("new_daytime", **kwargs)`.

### Value getters
`get_value(key, alt, **kwargs)` · `get_value_ng(...)` · `get_stat_value(key, ranges, alt, **kwargs)` ·
`get_level(key, **kwargs)` · `get_kwargs(key, alt, **kwargs)`.

### Images / video
`Pattern(key, path, *alt_keys)` · `show_pattern(key, **kwargs)` ·
`convert_pattern(key, **kwargs)` → `Image_Series` · `image.show(step, display_type, variant)` ·
`convert_pattern_with_data(key, data, **kwargs)` · `Image_Series.show_image(image, *steps)`.
Video: `image.show_video(step, pause=False, variant=-1)` with a
`Movie(play=<webm>, start_image=<webp>, loop=True)` image named `anim_` + the step's
webp basename (spaces → underscores).

### Characters
`Person["key"]` → `.say` / `.think` / `.whisper` / `.shout` (or `.get_renpy_char(char_type)`) ·
`get_person_value(key, alt, **kwargs)` → `Person` (same properties) ·
`get_person_char(key, alt, **kwargs)` → `Character` · `get_person_char_with_key(group, name, char_type)` ·
`headmaster_thought` · `character.subtitles` · `character.dev`.

### Decision menu
`call_custom_menu_with_text(text, person, with_leave, *MenuElement, **kwargs)` ·
`call_custom_menu(with_leave, *elements, **kwargs)` ·
`MenuElement(key, title, *effects|conditions|bool, active=True, overwrite_position=None)` ·
`register_decision(key)` (called for you by `call_element`).

### Stats / progress
`call change_stats_with_modifier('<collection>', stat=AMOUNT, …)` · amounts `TINY`/`SMALL`/`MEDIUM`/`LARGE` (+ `DEC_*`) ·
`start_progress(key)` / `set_progress(key, n)` · `ProgressCondition` / `ProgressSelector`.

### Runner labels
`call_event` · `call_available_event` · `call_event_menu` · `select_event_runner` ·
`composite_event_runner`.

### Related files
- `game/scripts/event.rpy` — event classes, storages, `begin_event`/`end_event`, runners
- `game/scripts/menu.rpy` — `MenuElement`, `call_custom_menu*`, `call_element` (decisions)
- `game/scripts/gallery.rpy` — `get_value`, `register_decision`, replay/gallery
- `game/scripts/images.rpy` — `Pattern`, `Image_Series`, `convert_pattern`, `show_pattern`
- `game/scripts/character.rpy` — `Person`, `get_person_char*`
- `game/scripts/buildings/*.rpy` — real pools & definitions (e.g. `cafeteria.rpy`)
- `game/scripts/events/*.rpy` — real scene labels (e.g. `truth_or_dare.rpy`, `teaching_lessons.rpy`)
- [Images](Images) · [Conditions](Conditions) · [Selectors](Selectors) · [Effects](Effects) · [Modifiers](Modifiers) · [Options](Options) · [Building Situations](Building-Situations)
