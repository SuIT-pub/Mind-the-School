> **Audience:** Developers writing *Mind the School* content who need to **show a
> picture** — a scene frame in an event, a thumbnail in a screen, a building sprite,
> a paperdoll layer, a journal icon. This page is the map of how a path string becomes
> a file on disk.
>
> **Scope:** The image system (`images.rpy`): patterns, placeholder substitution,
> alternative fallbacks, PNG/WebP compatibility, mod-path prefixing, and which helper
> to call from events, screens and classes. Layered talking sprites are covered in
> [Paperdoll](Paperdoll); event wiring that *uses* patterns is in [Events](Events).

---

## Quick start

Inside an event, declare a pattern and show it:

```python
# at Event construction (init, after set_current_mod)
Pattern("main", "images/events/cafeteria/snack_chat/<topic> <step>.webp")

# in the scene label
$ image = convert_pattern("main", **kwargs)
$ image.show(0)
"Dialogue over frame 0."
$ image.show(1)
```

Write **plain** paths (`images/…`). Never prefix `mods/MyMod/` yourself — the mod
context does that. End the pattern in `.png` or `.webp`; the other extension is found
automatically if that is what exists on disk.

---

## Contents

1. [What the image system is](#1-what-the-image-system-is)
2. [Path anatomy](#2-path-anatomy)
3. [PNG / WebP compatibility](#3-png--webp-compatibility)
4. [Mod paths](#4-mod-paths)
5. [How a path is resolved](#5-how-a-path-is-resolved)
6. [Built-in placeholders](#6-built-in-placeholders)
7. [Alternatives and the `$` wildcard](#7-alternatives-and-the--wildcard)
8. [Nude levels](#8-nude-levels)
9. [Events](#9-events)
10. [Screens](#10-screens)
11. [Classes and other systems](#11-classes-and-other-systems)
12. [Background images](#12-background-images)
13. [Overwriting event images](#13-overwriting-event-images)
14. [Videos](#14-videos)
15. [Conventions](#15-conventions)
16. [Troubleshooting](#16-troubleshooting)
17. [Reference](#17-reference)

---

## 1. What the image system is

Almost every picture in the game starts as a **path string** with optional
`<placeholders>`:

```text
images/events/cafeteria/snack_chat/<topic> <step>.webp
```

At display time the system:

1. prefixes the **mod folder** if the object was built under a mod,
2. replaces every `<key>` with a runtime value (selector, level, step, …),
3. optionally tries **`$` wildcards** for keys listed as alternatives,
4. picks the **best available level** when `<level>` is in the path,
5. accepts **`.png` or `.webp`** regardless of which extension the pattern wrote,
6. shows the file that actually exists (or logs an error and shows nothing).

The engine does not care whether the caller is an event, a screen or a paperdoll
layer. Those just pick a different entry point into the same pipeline.

---

## 2. Path anatomy

A path is a string. Tokens in `<angle brackets>` are placeholders; everything else is
literal, including spaces.

| Piece | Example | Meaning |
|-------|---------|---------|
| Folder | `images/events/cafeteria/snack_chat/` | relative to `game/` (or the mod root — [§4](#4-mod-paths)) |
| Name tokens | `<topic> <step>` | filled from kwargs / selectors |
| Wildcard | `$` | "this dimension does not apply" — a real character in the filename |
| Extension | `.webp` or `.png` | preferred format; the other is tried automatically |

Typical filenames on disk:

```text
images/events/cafeteria/snack_chat/muffin 0.webp
images/events/cafeteria/snack_chat/muffin 1.webp
images/paperdoll/Emiko/bottom/Emiko $ 1 uniform 6 $.png
```

`$` is **not** a placeholder. It is the character the game writes into the filename
when an alternative key is allowed to fall back ([§7](#7-alternatives-and-the--wildcard)).

---

## 3. PNG / WebP compatibility

Patterns still name **one** extension. Resolution always tries that one first, then
the other:

| Pattern says | File on disk | Result |
|--------------|--------------|--------|
| `….png` | `….png` | `….png` |
| `….png` | `….webp` | `….webp` |
| `….webp` | `….webp` | `….webp` |
| `….webp` | `….png` | `….png` |
| `….png` | both | `….png` (the pattern wins) |

So you can keep writing `.png` in paperdoll patterns and ship WebP assets, or mix
formats in one folder. The returned / displayed path is the file that **exists**.

This is implemented once, in `find_loadable_image`, and used by:

- `refine_image` / `refine_image_with_alternatives` / `refine_image_with_variant`
- `find_available_images` / `check_image`
- `get_image` / `get_available_level` / `get_image_max_value*`
- `Image_Series` (step/variant probing and display)
- `show_ready_image` and the nude-toggle screens
- paperdoll layer and background resolution

You do **not** write extension fallbacks yourself. Do not call `renpy.loadable` on a
pattern path and then `add` that same string — if the file is the other format, the
check would pass (via `check_image`) but the original string would not load. Resolve
first, display the resolved path:

```python
$ path = find_loadable_image(some_path)
if path:
    add path
```

---

## 4. Mod paths

`set_current_mod('mymod_key')` at the top of an init / loader block does two things
(see [Modding](Modding)): it gates registration on the mod being enabled, and it
**redirects assets**.

While that context is active, constructing any of these prepends
`get_mod_path(active_mod_key)` (e.g. `mods/MyMod/`) to the path you wrote:

| Object | When the prefix is applied |
|--------|----------------------------|
| `Pattern` | constructor — stored on `_pattern` |
| `Person` | constructor — `self.basePath`; paperdoll patterns and portraits use it |
| `Building` | constructor — `self.image` |
| `Situation` / threshold / teaser | constructor — `thumbnail` / `image` |
| `Pictogram` | constructor — `icon` |
| `ItemData` | constructor — `self.image` |
| `BGImage` inside `BGStorage` | `set_path_prefix(...)` when the storage is built |

Write **plain** paths, the same as the base game:

```python
set_current_mod('mymod_key')
Pattern("main", "images/mymod_scene <step>.webp")
# file lives at game/mods/MyMod/images/mymod_scene 0.webp
```

Never write `mods/MyMod/images/…` yourself — that would double the prefix.

The base game does the same with `set_current_mod('base')`. For the base game the
prefix is empty, so `images/…` stays `images/…`.

PNG/WebP swapping runs **after** the prefix is in place, so a mod file
`mods/MyMod/images/foo.webp` is found from a pattern that says `images/foo.png`.

`Pattern.get_path()` prepends `get_mod_path(active_mod_key)` **again** at call time.
The constructor already stored a prefixed `_pattern`, so this is a no-op when the
current prefix is empty (typical once inits have finished with `'base'`). Do not "fix"
missing mod images by baking `mods/…` into the pattern string.

---

## 5. How a path is resolved

Two families of helpers, depending on whether you have **one** path or a list of
fallbacks.

### Single path — `refine_image` / `get_image`

```text
pattern + kwargs
    → replace <school_level> / <teacher_level> / … from the live stats
    → get_available_level for <level> (nearest existing level, png or webp)
    → replace every remaining <key> from kwargs
    → apply_available_image_extension  (png ↔ webp if the path has no leftover <…>)
```

`refine_image(path, **kwargs)` returns that string. Paths that still contain
`<placeholders>` (e.g. `<step>`, `<nude>`) keep the original extension so later
probing can fill them in.

`get_image(path, **kwargs)` does the same substitution, then:

- if there is no `<nude>`, returns `(0, loadable_path)` or `(-1, original)` on miss,
- if there is `<nude>`, returns `(max_nude_level, template)` where the template still
  holds `<nude>` but already has the extension of the file that exists.

### Several candidates — `refine_image_with_alternatives` + `find_available_images`

Used when some keys are allowed to fall back to `$`:

```text
pattern + alt_keys + kwargs
    → one candidate per combination of alt_keys replaced by $
    → same level / kwarg fill as refine_image
    → sort: fewer $ first (more specific wins)
    → apply_available_image_extension on complete paths
    → find_available_images: first candidate that loadable (png or webp)
```

Paperdoll layers and `Image_Series` both use this. You almost never call it by hand
from an event label.

### Display — `show_ready_image`

The low-level show label. If the path still contains `<nude>`, it opens the nude
toggle UI. Otherwise it resolves png/webp and `scene` / `show`s the **resolved** path.

`SCENE` (default) replaces the background; `SHOW` adds it as `general_image`.

---

## 6. Built-in placeholders

These keys are filled even if you did not pass them in kwargs:

| Placeholder | Filled from |
|-------------|-------------|
| `<school_level>` | school character's level |
| `<teacher_level>` | teacher character's level |
| `<parent_level>` | parent character's level |
| `<secretary_level>` | secretary character's level |
| `<level>` | nearest **existing** file at or below the requested level, else the next one up |
| `<variant>` | random `1…max` among files that exist (`get_image` / `refine_image_with_variant`) |
| `<nude>` | not replaced with a single value — see [§8](#8-nude-levels) |
| `<step>` | the frame index, filled by `Image_Series.show(n)` |
| `<loli>` / `<loli_content>` | content-filter values, injected if missing |

Any other `<key>` comes from **kwargs**: event selectors ([Selectors](Selectors)),
values you pass into `refine_image`, paperdoll `PDAImage` keys, a building's
`state=`, and so on.

`<level>` is special: the system does not require a file for every level. It walks
down from the requested level, then up, and rewrites the path to the closest file
that exists (png or webp).

---

## 7. Alternatives and the `$` wildcard

Some dimensions are optional on disk. A paperdoll body might have a per-level file
*or* a generic `$` file. You list those keys as **alternatives**; the resolver
generates every combination, most specific first:

```python
Pattern("main", "images/scene/<char> <outfit> <level>.webp", "level", "outfit")
```

Candidates, in order (requested `char=emiko`, `outfit=uniform`, `level=6`):

1. `images/scene/emiko uniform 6.webp`
2. `images/scene/emiko uniform $.webp`     (`level` → `$`)
3. `images/scene/emiko $ 6.webp`           (`outfit` → `$`)
4. `images/scene/emiko $ $.webp`           (both)

The first that exists (as `.webp` or `.png`) wins.

Paperdoll character layers use `alt_keys = ["level", "mouth", "state", "char_var"]`.
Event patterns pass alternative keys as extra constructor args:
`Pattern("main", path, "level", "variant")`.

`$` must appear in the **filename** on disk for a fallback to work. A missing
specific file with no `$` sibling is a miss, not a silent skip of that token.

---

## 8. Nude levels

A path containing `<nude>` is a **template**, not a final file. Files are numbered:

```text
images/events/foo/foo 1 0.webp    # clothed
images/events/foo/foo 1 1.webp    # nude 1
images/events/foo/foo 1 2.webp    # nude 2
```

`get_image` reports the highest available nude index (capped by `nude_vision`) and
leaves `<nude>` in the returned template. `show_ready_image` then opens the
eye-icon UI so the player can step between versions.

In an event you usually do not handle this yourself: `image.show(step)` detects
`<nude>` and routes to that UI. For a one-off path:

```python
$ nude, path = get_image("images/events/foo/foo <step> <nude>.webp", step=1)
# nude == 2, path still contains <nude>, extension already matches the files
call show_image_with_nude_var(path, nude)
```

---

## 9. Events

This is the common author path. Full event wiring is in [Events §9](Events#9-images-patterns-steps--image_series); this section is which **image** helper to pick.

### Declare

```python
Pattern("main", "images/events/…/<topic> <step>.webp")
Pattern("card", "images/events/…/card <girls> <step>.webp", "girls")  # girls may fall back to $
```

Several named patterns per event (`"main"`, `"bg"`, `"card"`, …). They are attached
to the event and show up in the label as `kwargs["image_patterns"]`.

### Show a stepped scene (the usual case)

```python
$ image = convert_pattern("main", **kwargs)
$ image.show(0)          # SCENE, random variant if the pattern has <variant>
$ image.show(1)
$ image.show(2, SHOW)    # overlay instead of replacing the scene
```

`$ image.show(n)` (`Image_Series.show`) also `paperdoll_manager.clear()`s when a
manager exists — paperdolls and their backdrop go away with the still. No extra
`clear_display()`. (`call show_image` / `show_pattern` do **not** do this.)

`convert_pattern_with_data("card", {"girls": "emiko"}, **kwargs)` builds a series
with one key forced — useful when a second pattern must show a specific character.

`call Image_Series.show_image(image, 0, 1, 2)` plays several steps on click with no
dialogue between them.

`image[step]` (getitem) returns a **concrete loadable path** or `None` — handy as a
paperdoll background: `paperdoll_manager.set_background(image[2], blur=True)`.

### Show a single static image

```python
$ show_pattern("main", **kwargs)
```

Or, without a named pattern:

```python
call show_image("images/background/school building/<level> 0 1.webp")
```

`show_image` runs `refine_image` then `show_ready_image`. Prefer `convert_pattern` /
`show_pattern` when the path lives on the event so mods can overwrite it
([§13](#13-overwriting-event-images)).

### Black / hide

```python
$ image.show_black()
$ image.hide()
```

---

## 10. Screens

Screens do not have event kwargs. You typically have a **concrete path** (maybe with
one or two placeholders) and need to put it in an `add` / `imagebutton`.

| Need | Call |
|------|------|
| "Does this file exist, png or webp?" | `find_loadable_image(path)` → the real path, or `""` |
| Boolean only | `check_image(path)` (same fallback; still prefer displaying the resolved path) |
| Fill `<state>` / `<level>` / a few keys | `refine_image(path, state="idle", level=3)` |
| Fill keys **and** `$` fallbacks | `refine_image_with_alternatives(path, ["level"], level=3)` then `find_available_images(...)` |

```python
# building sprite on the map — the Building already stored a prefixed pattern
$ idle = find_loadable_image(building.get_image("idle"))
if idle:
    add idle:
        xpos building.x_pos ypos building.y_pos

# journal thumbnail that may still contain <level>
$ thumb = find_loadable_image(refine_image(obj.thumbnail, **kwargs))
if thumb == "":
    $ thumb = "images/journal/empty_image.webp"
add thumb
```

**Do not** `add path` after a successful `renpy.loadable(path)` check unless `path`
is already the resolved file. `find_loadable_image` is the check **and** the path
to display.

---

## 11. Classes and other systems

When you store an image on a class, capture the mod prefix **in the constructor**
(while `set_current_mod` is set) and resolve at use time.

### Pattern to follow

```python
def __init__(self, image: str, ...):
    self.image = get_mod_path(active_mod_key) + image if image else image

def get_image(self, state="idle"):
    return refine_image(self.image, state=state)
    # refine_image already swaps png/webp on the filled path
```

That is what `Building`, `Pictogram`, `ItemData`, teasers and situation thumbnails
do. Callers that put the result on screen should still run `find_loadable_image` if
they need a miss → fallback image.

### What to call from where

| System | Store | Resolve / show |
|--------|-------|----------------|
| **Event** | `Pattern("main", "images/…")` on the `Event` | `convert_pattern` / `show_pattern` in the label |
| **Paperdoll** | `Person.register_paperdoll()` (patterns include `basePath`) | `PDAImage` + `.display()` — [Paperdoll](Paperdoll) |
| **Person portraits** | `basePath` + `images/characters/<name>/level_N.webp` | `person.get_portraits()` / `get_thumbnail()` already resolve png/webp |
| **Building map sprite** | `Building(..., "images/map/foo_<state>.webp")` | `building.get_image("idle")` then `find_loadable_image` in the screen |
| **Situation thumbnail / teaser photo** | constructor path | `situation.get_current_thumbnail()` / teaser `_resolve_image` (uses `get_image`) |
| **Pictogram icon** | constructor path | `pictogram.get_icon(**kwargs)` → `refine_image` |
| **Inventory item** | constructor path | `item.get_image()` → `find_loadable_image` |
| **Idle location BG** | `BGStorage` + `BGImage`s | `call show_idle_image(bg_images)` |

### Paperdoll

Character paperdolls are two layers whose patterns end in `.png`. Resolution is the
same pipeline (`refine_image_with_alternatives` → `find_available_images`). See
[Paperdoll](Paperdoll) for registration, actions and backgrounds. A paperdoll
background accepts a pattern, a concrete path, or `image[step]` from an
`Image_Series`.

---

## 12. Background images

Location idle art uses `BGImage` / `BGStorage`, not event `Pattern`s.

```python
BGStorage(
    "images/background/school building/1 0 1.webp",          # fallback
    BGImage("images/background/school building/<level> 0 1.webp", 1,
        TimeCondition(daytime="d")),
)
```

`BGStorage` stamps the current mod prefix onto each `BGImage`. `call show_idle_image(storage)`
picks the highest-priority image whose conditions pass, then shows it (with nude
toggle if the path has `<nude>`).

For a one-off backdrop behind a paperdoll, prefer
`paperdoll_manager.set_background(...)` rather than `BGStorage`.

---

## 13. Overwriting event images

A mod can replace one named pattern on an existing event without forking the label:

```python
init 1 python:
    set_current_mod('mymod_key')
    overwrite_event_image(
        "snack_chat",
        "main",
        Pattern("main", "images/snack_chat_alt/<topic> <step>.webp"))
```

The new `Pattern` is prefixed into the mod folder. The scene label keeps calling
`convert_pattern("main", **kwargs)` and now loads your files. No-ops while the mod
is disabled.

---

## 14. Videos

A video is the animated twin of a stepped `.webp` frame. The `Movie` image **name**
must be `anim_` + the resolved webp basename, spaces → underscores. Details and the
`image.show_video(step, pause)` call live in [Events §10](Events#10-videos).

`show_video` derives that name from the resolved image path after png/webp
resolution, using the stem (so `foo 1 0.webp` and `foo 1 0.png` yield the same
`anim_foo_1_0`).

---

## 15. Conventions

- **Write `images/…`, never `mods/MyMod/…`.** Prefixing is the constructor's job.
- **`set_current_mod` before you construct** anything that stores a path.
- **One extension in the pattern is enough.** Ship png, webp, or a mix; do not
  duplicate patterns per format.
- **Prefer `Pattern` on the event** over a hardcoded path in the label, so mods can
  overwrite it.
- **`$` on disk** for every alternative key you list, or that fallback will never hit.
- **Resolve, then display.** `find_loadable_image(path)` (or `refine_image` /
  `convert_pattern`) first; `add` / `scene` the returned string.
- **Do not call `renpy.loadable` on pattern paths** in new code. Use
  `find_loadable_image` / `check_image`.
- **`<level>` does not need a file per level.** The resolver walks to the nearest
  existing file.
- **Paperdoll patterns stay `.png`** by convention; WebP assets still resolve.

---

## 16. Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Image missing, log shows `.png` | No png *and* no webp at that stem | Check folder, tokens, and `$` fallbacks. |
| Literal `<key>` in the log path | Kwarg / selector never set | Add the selector or pass the key into `refine_image` / `PDAImage`. |
| Mod images not found | `set_current_mod` missing, or you wrote `mods/…` yourself | Set the context first; use plain `images/…`. |
| Wrong event art after adding a mod | `overwrite_event_image` not used, or wrong event/pattern key | Match the event key and pattern name (`"main"`). |
| Step 0 works, later steps empty | Gap in `<step>` numbering, or only png probed in old code | Number steps densely from `step_start`; current probing sees both extensions. |
| Variant never appears | No `1…n` files, or `<variant>` not in the pattern | Add `foo 0 1.webp`, `foo 0 2.webp`, … |
| Nude toggle missing | Path has no `<nude>`, or only level `0` exists | Name files `… 0`, `… 1`, … and keep `<nude>` in the pattern. |
| Screen shows nothing / error on `add` | Displayed the pattern string after a png/webp miss | `path = find_loadable_image(...)`; `add path` only when non-empty. |
| Paperdoll layer blank | Specific file missing and no `$` sibling for an `alt_key` | Add the file or a `$` fallback; check pose/outfit are exact (not alt keys). |

---

## 17. Reference

### Author-facing (events)

`Pattern(key, path, *alternative_keys)` · `show_pattern(key, **kwargs)` ·
`convert_pattern(key, **kwargs)` → `Image_Series` ·
`convert_pattern_with_data(key, data, **kwargs)` ·
`image.show(step, display_type=SCENE, variant=-1)` ·
`image.show_video(step, pause=False, variant=-1)` ·
`image[step]` → concrete path · `image.show_black()` / `image.hide()` ·
`call Image_Series.show_image(image, *steps)` ·
`overwrite_event_image(event_key, pattern_key, Pattern(...))`.

### Author-facing (screens / classes)

`refine_image(path, **kwargs)` · `refine_image_with_alternatives(path, alt_keys, **kwargs)` ·
`find_loadable_image(path)` · `find_available_images(paths)` · `check_image(path)` ·
`get_image(path, **kwargs)` → `(nude, path)` ·
`call show_image(path, display_type=SCENE, **kwargs)` ·
`get_mod_path(key)` / `get_current_mod_path()`.

### Internals (you rarely call these)

`apply_available_image_extension` · `image_extension_candidates` ·
`replace_image_extension` · `get_available_level` · `get_image_max_value` /
`get_image_max_value_with_alternatives` · `show_ready_image`.

### Display types

`SCENE` — replace the background (`scene`). `SHOW` — overlay as `general_image`.

### Related pages

- [Events](Events) — when to put a `Pattern` on an event, stepped scenes, videos
- [Selectors](Selectors) — the values that fill `<key>`
- [Paperdoll](Paperdoll) — layered sprites on top of this resolver
- [Modding](Modding) — `set_current_mod`, folder layout, asset redirection

### Related files

- `game/scripts/images.rpy` — `Pattern`, `Image_Series`, refine/loadable helpers, show labels
- `game/scripts/helper.rpy` — `get_mod_path`, `set_current_mod`
- `game/scripts/paperdoll.rpy` — layer/background resolution on top of this system
- `game/scripts/character.rpy` — `Person` `basePath`, `register_paperdoll`, portraits
- `game/scripts/event.rpy` — attaches `Pattern`s as `image_patterns` / `frag_image_patterns`
