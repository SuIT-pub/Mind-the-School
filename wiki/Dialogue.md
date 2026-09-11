> **Audience:** Developers writing *Mind the School* scenes who need someone to
> **speak** — a line of dialogue, an inner thought, a whisper or a shout — and want
> the name tag, colour, font and format to be right without hand-defining a Ren'Py
> `Character` per person.
>
> **Scope:** How a `Person` becomes a speaking voice (`character.rpy`), how the name
> tag is styled per role and per character, how the player-named **Headmaster** and
> **Emiko** fit in, and where names live. The on-screen *sprite* is a separate system —
> see [Paperdoll](Paperdoll). Picking *who* speaks from a selector is in
> [Events §11](Events#11-characters--dialogue) and [Selectors](Selectors).

---

## Quick start

Grab the `Person`, then talk through its speech modes:

```python
$ miwa = Person["miwa_igarashi"]
miwa "That was crazy..."           # bare call == normal speech
miwa.say     "That was crazy..."   # same thing, explicit
miwa.think   "...why did she do that?"
miwa.whisper "Don't tell anyone."
miwa.shout   "Watch out!"
"[miwa.get_full_name()] blushes."  # same object, other members
```

The player (Headmaster) and the secretary (Emiko) are ordinary `Person`s too, and
`begin_event` already binds them — inside any event you can just speak:

```python
$ begin_event(**kwargs)      # binds `headmaster` and `emiko` for you
emiko "Caught you glaring at it. Don't worry — everyone glares at it."
headmaster.think "That plaque again."
headmaster "Then let's stop waiting on it. Chase it today."
```

The three moving parts:

- **`Char`** — a *stat container* (level + corruption/inhibition/…). One per role/school.
- **`Person`** — the *actor*: name, description, portraits, paperdoll, and the speaking
  voice. It points at a `Char` for stats and for its styling category.
- **The speaking `Character`** — built on demand by `Person.get_renpy_char()`; you never
  define one per person unless you want to override its look.

---

## Contents

1. [Char vs. Person](#1-char-vs-person)
2. [Speaking as a fixed character](#2-speaking-as-a-fixed-character)
3. [Speaking as a selected character](#3-speaking-as-a-selected-character)
4. [The Headmaster & Emiko](#4-the-headmaster--emiko)
5. [Styling categories (the `kind`)](#5-styling-categories-the-kind)
6. [Per-character overrides (`styleOverrides`)](#6-per-character-overrides-styleoverrides)
7. [Names](#7-names)
8. [Registering a person](#8-registering-a-person)
9. [Conventions](#9-conventions)
10. [Troubleshooting](#10-troubleshooting)
11. [Reference tables](#11-reference-tables)

---

## 1. Char vs. Person

Two classes, two jobs — don't conflate them.

- **`Char`** holds the numbers: a `level` and a bag of `Stat` objects. The game runs on
  a small set of shared `Char`s — one per **role** (`school`, `parent`, `teacher`,
  `secretary`), reached with `get_character_by_key("...")`. Every student shares the one
  `school` char; every teacher shares the `teacher` char. That's why raising "the
  school's" inhibition moves the whole class at once.
- **`Person`** is the individual: `name` (the id), `first_name`/`last_name`, a
  `description`, `portraits`, paperdoll data, and `character` — the `Char` it draws stats
  and styling from. A `Person` is what speaks.

So many `Person`s can share one `Char`. The **Headmaster is the exception**: he is the
player, has *no* stat-`Char` (`character` is `None`), and is handled by name — see
[§4](#4-the-headmaster--emiko).

> `Person` objects live in `person_storage`, which is **per-save**, but `load_person`
> re-applies the code definition on every load. Treat a `Person` definition as
> **code-authoritative and save-agnostic**: name, description and styling come from the
> code each session; only genuinely per-save data (the Headmaster's chosen name, the
> `Char`'s stats) lives in the save. **Never bake per-save state into a `Person` def.**

---

## 2. Speaking as a fixed character

Keep the **`Person`** and speak through it — you get dialogue *and* the rest of the
person from one variable, no second definition:

```python
$ miwa = Person["miwa_igarashi"]
miwa         "Normal line."     # __call__ delegates to .say
miwa.say     "Normal line."
miwa.think   "Inner monologue."
miwa.whisper "Kept quiet."
miwa.shout   "Loud!"
```

`Person["key"]` returns the `Person` (via `__class_getitem__` → `find_person`). Each
speech-mode property returns a **fresh** Ren'Py `Character`, so a say statement can use
it directly — Ren'Py evaluates the who-expression, and dotted/subscript expressions are
allowed, so even `Person["miwa_igarashi"].say "..."` works inline. The bare
`person "..."` form works because `Person.__call__` forwards to `.say`.

| Property / form | Mode | What it adds on top of the category look |
|-----------------|------|------------------------------------------|
| `person "..."` / `.say` | normal speech | nothing |
| `.think` | inner monologue | italic, prefix `(  `, suffix `  )`, name suffix "(thinking)" |
| `.whisper` | whisper | italic, name suffix "(whispering)" |
| `.shout` | shout | bold, name suffix "(shouting)" |

Under the hood every one calls `get_renpy_char(char_type="")` (`char_type` ∈ `""` /
`"thought"` / `"whisper"` / `"shout"`). The old
`$ x = Person["key"].get_renpy_char(...)` form still works and returns the same
`Character`; the property/bare-call form just avoids carrying that extra line. Building a
new `Character` per access is cheap and behaves identically (same name, `retain=False`).

---

## 3. Speaking as a selected character

When a [selector](Selectors) picked *who* speaks (its value is a character key like
`"aona_komuro"` or a role like `"school"`), resolve it in the scene label:

```python
$ girl = get_person_value("girl_name", **kwargs)   # -> the Person
girl.say   "Fine, I'll do the dare."
girl.think "...this is embarrassing."
```

- `get_person_value(key, alt=None, **kwargs)` → the resolved **`Person`** (handles the
  `school`/`parent`/`teacher`/`secretary` roles and falls back to a neutral default
  view). Prefer this — you get the speech-mode properties *and* the person's other
  members.
- `get_person_char(key, alt=None, **kwargs)` → just a speaking `Character` for the
  selected key. Use it when you only need a voice.
- `get_person_char_with_key(group_key, name, char_type="")` → resolve a character from a
  storage group (`"class_3a"`, `"staff"`, `"parents"`) plus a name.

This is why an event stays generic: the selector chooses *who*, and these helpers turn
that choice into the voice that speaks.

---

## 4. The Headmaster & Emiko

Both are full `Person`s and speak through the same `.say`/`.think`/`.whisper`/`.shout`
API as everyone else. You don't bind them yourself: **`begin_event` binds `headmaster`
and `emiko`** at the start of every event (`event.rpy`), so inside the scene you can use
them straight away. (Outside an event — e.g. a screen or a debug label that never calls
`begin_event` — the static `character.headmaster` / `character.emiko` still catch a bare
say line; only the `Person`-object features like `emiko.register_paperdoll()` need a real
`begin_event` first.)

**The Headmaster is special** in two ways:

1. **No stat-`Char`.** He's the player; his `character` is `None`. His styling is keyed
   by `self.name == "headmaster"` → the `character.headmaster` look (see
   [§5](#5-styling-categories-the-kind)).
2. **A save-specific, player-chosen name.** His `Person` is defined *name-less*
   (`Person("headmaster", "", "", ...)`). `get_first_name` / `get_last_name` /
   `get_full_name` special-case him and read the live name from `get_name("headmaster")`
   (see [§7](#7-names)). This keeps the name **per-save** while the `Person` definition
   stays save-agnostic — the name is never baked into the def.

**Emiko** is a normal `Person` (`emiko_langley`) whose `Char` is the `secretary` role, so
she automatically picks up the `character.secretary` look. Write her lines as `emiko`
(the old `secretary "..."` speaker was retired in favour of the `Person`).

> Static safety nets `character.headmaster` and `character.emiko` exist in `values.rpy`
> so a bare `headmaster`/`emiko` say line can't crash even if a code path forgot the
> `$ ... = Person[...]` binding. The legacy `character.*_thought/_whisper/_shout`
> definitions still exist (referenced by version-compat fixups) but are **redundant for
> dialogue** — the char-type modes generate that formatting dynamically. Don't add new
> ones; use `.think`/`.whisper`/`.shout`.

---

## 5. Styling categories (the `kind`)

Every speaking `Character` starts from a **category** — a shared Ren'Py `Character`
defined in `values.rpy` that carries the name-tag colour, text colour and size for that
kind of speaker. `get_renpy_char` picks it:

| Test on the `Person` | Category (`kind`) | Name-tag colour |
|----------------------|-------------------|-----------------|
| `name == "headmaster"` | `character.headmaster` | white |
| `character` is the `school` char | `character.sgirl` | purple |
| `character` is the `parent` char | `character.parent` | lavender |
| `character` is the `teacher` char | `character.teacher` | teal |
| `character` is the `secretary` char | `character.secretary` | magenta |
| *(none of the above)* | `character.subtitles` | neutral / centered |

The category sets the **base**; the char-type mode (`.think`/`.whisper`/`.shout`) layers
its markers on top; a per-character override (next section) can override anything in
between.

---

## 6. Per-character overrides (`styleOverrides`)

A `Person` can override any part of its speaking look without touching the shared
category. Pass `styleOverrides` — a dict of **Ren'Py `Character` kwargs** — to the
`Person` definition:

```python
$ load_person("class_3a", Person("zoe_parker", "Zoe", "Parker", school_char, [ ... ],
    styleOverrides = {
        "who_color":  "#e67e22",              # name-tag colour
        "what_color": "#fbeee0",              # spoken-text colour
        "what_font":  "gui/font/handwritten.ttf",
        "what_size":  30,
        "what_italic": True,
    }))
```

**Layering** (last wins): category `kind` → this Person's `styleOverrides` → the
char-type markers. So an override changes the base for *all* of this person's modes,
while `.whisper`/`.shout`/`.think` still apply their own italic/bold/suffix on top.
Anything the override doesn't set falls through to the category.

```
character.sgirl (base)   who_color #8a2be2, what_color #fff, what_size 28
   ↓ styleOverrides       who_color #e67e22, what_size 30
   ↓ .whisper             + what_italic, + name suffix "(whispering)"
= final Character         who_color #e67e22, what_color #fff, what_size 30, italic, "(whispering)"
```

Common keys: `who_color`, `what_color`, `who_font`, `what_font`, `who_size`,
`what_size`, `who_bold`, `what_bold`, `who_italic`, `what_italic`, `what_prefix`,
`what_suffix`, `window_background`. (Any Character kwarg is accepted.)

`styleOverrides` is **code-level** — copied from the definition on every load, like the
rest of the `Person`. An empty/omitted dict means "use the category as-is". Old saves
without the field are backfilled to empty.

---

## 7. Names

A character's display name has two independent sources depending on whether it's
player-editable.

**Baked-in (most characters).** `first_name`/`last_name` are set in the `Person`
definition and shown via `get_first_name()` / `get_last_name()` / `get_full_name()`.
These are code-level, save-agnostic.

**Editable (the Headmaster).** His name is player-chosen and lives in the save:

- `set_name("headmaster", first, last)` writes `gameData["names"]["headmaster"]`.
- `get_name("headmaster")` → `(first, last)`, falling back to `default_names` if unset.
- `get_name_str("headmaster")` → a joined string.
- `default_names` (in `values.rpy`) holds the defaults for every editable key.

The Headmaster `Person`'s name getters read `get_name("headmaster")` live, so renaming
mid-game is reflected everywhere immediately.

**Interpolating a name into another line.** Other characters refer to the Headmaster
with Ren'Py text tags, mirrored into per-save store variables:

```python
sgirl "Hello Mr. [headmaster_last_name]."
emiko "Good morning, [headmaster_first_name]."
```

`headmaster_first_name` / `headmaster_last_name` are kept in sync with
`get_name("headmaster")` on load. Use the tags in dialogue **text**; use the `Person`
getters in Python.

---

## 8. Registering a person

Persons are created in the `load_characters` label with `load_person(group_key, Person(...))`:

```python
$ load_person("class_3a", Person(
    "aona_komuro",              # name / id (also the image folder)
    "Aona", "Komuro",           # first, last  ("" , "" for the Headmaster)
    school_char,                # the Char this Person draws stats & category from
    [ "• Height: 172.5 cm", ... ],   # description lines (see Characters page format)
    styleOverrides = { ... },   # optional, see §6
))
```

Storage groups: `"class_3a"` (students), `"staff"` (teachers, Emiko, Headmaster lives
under `"NoView"`), `"parents"`, and `"NoView"` (default/neutral views not shown in the
journal). `load_person` is gated on the active mod, so a disabled mod's persons aren't
registered; base loaders run under `set_current_mod("base")`.

Related: registering a **sprite** for the same person is a separate call —
`Person.register_paperdoll()` / `Person.display()`, documented in [Paperdoll](Paperdoll).

---

## 9. Conventions

- **`headmaster` and `emiko` are auto-bound by `begin_event`** — don't bind them
  yourself; just speak. For any *other* fixed character, bind it once near the top:
  `$ x = Person["key"]`, then speak.
- **Speak through the `Person`**, not a hand-defined `Character`. Reserve
  `values.rpy` `Character` definitions for the shared **categories** and the two static
  safety nets (`headmaster`, `emiko`).
- **Never bake per-save data into a `Person` def.** The Headmaster's name proves the
  pattern: the def is name-less, the name is resolved live from the save.
- **Style per character with `styleOverrides`**, not a new category, unless the whole
  role should change.
- Use `[headmaster_first_name]` / `[headmaster_last_name]` tags in dialogue text; use
  `get_name(...)` / the `Person` getters in Python.
- Retire old speaker aliases: write `emiko`, `headmaster.think` — not `secretary "..."`
  or `headmaster_thought "..."`.

---

## 10. Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `NameError: emiko is not defined` on a say line | the label never called `begin_event` (which binds `headmaster`/`emiko`) | call `$ begin_event(**kwargs)` first, or for a non-event context rely on the static `character.emiko` |
| `AttributeError: 'ADVCharacter' has no attribute 'register_paperdoll'` | using `emiko.register_paperdoll()` where `emiko` fell back to the static Character | that call needs the `Person` — make sure `begin_event` ran in this label |
| Headmaster's name shows literal `[headmaster_first_name]` | reading the raw def field instead of a getter/tag | use `get_full_name()` in Python or the `[...]` tag in dialogue text |
| A character speaks with the neutral/centered subtitle look | their `Person.character` matches no known role (`kind` fell through to `subtitles`) | check the `Char` passed to the `Person`; for the Headmaster the name must be exactly `"headmaster"` |
| `styleOverrides` seems ignored | key typo, or a char-type marker overrides it (e.g. `.whisper` forces italic) | verify the kwarg name; remember char-type markers win on their own keys |
| `AttributeError: ... has no attribute 'get_character'` | calling the old method name on a `Person` | the method is `get_renpy_char(char_type="")` |
| Lint prints `Could not evaluate '<name>' in the who part` | expected — lint can't run the per-event `$ x = Person[...]` binding | harmless; it's the same for every dynamically-bound speaker (`aona`, `miwa`, …) |

---

## 11. Reference tables

**Speech modes** (`get_renpy_char(char_type)`)

| `char_type` | Property | Formatting layered on the category |
|-------------|----------|------------------------------------|
| `""` | `.say` / `person "..."` | — |
| `"thought"` | `.think` | italic, `(  ` … `  )`, "(thinking)" |
| `"whisper"` | `.whisper` | italic, "(whispering)" |
| `"shout"` | `.shout` | bold, "(shouting)" |

**Person API (dialogue-relevant)**

| Member | Returns | Notes |
|--------|---------|-------|
| `Person["key"]` | `Person` | lookup across all storage groups |
| `person(...)` / `person.say` | `Character` | normal speech |
| `person.think` / `.whisper` / `.shout` | `Character` | speech modes |
| `person.get_renpy_char(char_type="")` | `Character` | the underlying builder |
| `person.get_first_name()` / `get_last_name()` / `get_full_name()` | `str` | Headmaster reads `get_name` live |

**Helpers**

| Function | Returns | Where |
|----------|---------|-------|
| `get_person(group_key, name)` | `Person` | `character.rpy` |
| `find_person(name)` | `Person` | `character.rpy` |
| `get_person_value(key, alt=None, **kwargs)` | `Person` | `gallery.rpy` (selector value) |
| `get_person_char(key, alt=None, **kwargs)` | `Character` | `gallery.rpy` |
| `get_person_char_with_key(group_key, name, char_type="")` | `Character` | `character.rpy` |
| `get_character_by_key(key)` | `Char` | `character.rpy` (role stat container) |
| `get_name(key)` / `set_name(key, first, last)` / `get_name_str(key)` | name | `helper.rpy` |

**Related files**

- `game/scripts/character.rpy` — `Char`, `Person`, `get_renpy_char`, `styleOverrides`,
  `load_person`, `load_characters`.
- `game/scripts/values.rpy` — category `Character`s, static safety nets, `default_names`.
- `game/scripts/helper.rpy` — `set_name` / `get_name` / `get_name_str`.
- `game/scripts/gallery.rpy` — `get_person_value` / `get_person_char`.

**See also:** [Events §11 Characters & dialogue](Events#11-characters--dialogue) ·
[Selectors](Selectors) · [Paperdoll](Paperdoll)
