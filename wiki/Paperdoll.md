> **Audience:** Developers writing *Mind the School* scenes who need a **layered,
> live sprite on screen** — a character built from a body + head that changes pose,
> outfit, mood and mouth mid-conversation, moves, zooms, blurs, shakes, flips or
> desaturates, sitting over a (blurred) background.
>
> **Scope:** The paperdoll system (`paperdoll.rpy`). It is the compositor the game
> uses for talking characters, driven by the `Person.register_paperdoll()` /
> `Person.display()` helpers in `character.rpy`. But the engine itself knows nothing
> about characters: it stacks **any** set of pattern-resolved image layers. Give it
> sprites and it will render anything — props, machines, multi-part scenery.

---

## Quick start

Inside an event, hand a character off from a static scene image to a live paperdoll:

```python
$ emiko.register_paperdoll()                                   # build the layered object
$ paperdoll_manager.set_background(
    "images/background/office building/secretary 6 1 0.webp",
    blur = True)                                               # blurred backdrop behind her
$ emiko.display(                                               # first frame + how she enters
    PDAImage(pose = "1", outfit = "uniform", level = 6, mood = "neutral", mouth = "closed"),
    PDAPreset("upper_body", duration = 0.0),
    PDAPreset("outside",    duration = 0.0))
$ emiko.display(PDAPreset("upper_body_center", duration = 0.4))   # slide her in
$ emiko.display(PDAImage(mood = "suspicious", mouth = "open"))    # change expression
emiko.say "Oh. You noticed."
$ emiko.display(PDAImage(mood = "neutral", mouth = "closed"))
...
$ emiko.clear_display()                                       # tear the paperdoll down
```

The three moving parts:

- **`paperdoll_manager`** — the global compositor. Holds the registered objects and
  the background. Auto-created by `begin_event` in normal events (you rarely touch
  its lifecycle yourself).
- **A paperdoll object** — a named stack of **layers**, each layer a *pattern* that
  resolves to an image from the current `values` (`pose`, `outfit`, `mood`, …).
- **Actions (`PDA…`)** — the verbs you pass to `.display()`: change the image, move,
  blur, pause, shake, flip, desaturate, or expand a preset.

---

## Contents

1. [What the paperdoll system is](#1-what-the-paperdoll-system-is)
2. [Manager lifecycle](#2-manager-lifecycle)
3. [Layers & pattern resolution](#3-layers--pattern-resolution)
4. [Registering an object](#4-registering-an-object)
5. [Values & the config model](#5-values--the-config-model)
6. [Displaying: the action pipeline](#6-displaying-the-action-pipeline)
7. [The action catalog](#7-the-action-catalog)
8. [Presets](#8-presets)
9. [Backgrounds](#9-backgrounds)
10. [display_size & high-resolution assets](#10-display_size--high-resolution-assets)
11. [Overrides: per-layer conditional nudges](#11-overrides-per-layer-conditional-nudges)
12. [Beyond characters: displaying anything](#12-beyond-characters-displaying-anything)
13. [The in-game paperdoll editor](#13-the-in-game-paperdoll-editor)
14. [Conventions](#14-conventions)
15. [Troubleshooting](#15-troubleshooting)
16. [Reference tables](#16-reference-tables)

---

## 1. What the paperdoll system is

A **paperdoll** is a picture assembled from stacked image **layers** and shown as a
single, animatable actor. Each layer is drawn from a *pattern* — a path with
`<placeholders>` — that is filled in from the object's current **values** and
resolved to a concrete file at display time.

For a character the stack is two layers:

1. **bottom** — the body: `… <char_var> <pose> <outfit> <level> <state>.png`
2. **top** — the head: `… <char_var> <pose> <mood> <mouth>.png`

Changing `outfit` re-resolves only what the pattern references; changing `mood` or
`mouth` swaps the head without touching the body. Because both layers share the same
position/zoom/blur transforms, they move as one figure.

The engine is deliberately generic. It has no concept of "character", "mood" or
"outfit" — those are just keys in the pattern. A paperdoll can have **one layer or
many**, and its patterns can point at anything. See
[§12](#12-beyond-characters-displaying-anything).

---

## 2. Manager lifecycle

The compositor is a single global, `paperdoll_manager` (a `PaperdollManager`).

- **`init_paperdoll_manager()`** — creates a fresh manager.
- **`unload_paperdoll_manager()`** — clears every object + background, then drops it.

**In events you normally do neither.** `begin_event` calls
`init_paperdoll_manager()` at scene start and `unload_paperdoll_manager()` at
teardown (`event.rpy`), so inside an event the manager already exists. Your job is
just to register objects, display them, and `clear_display()` when the conversation
ends. You only init/unload the manager by hand outside the event flow (the debug
editor does exactly that — see [§13](#13-the-in-game-paperdoll-editor)).

Manager surface you use directly:

| Method | Purpose |
|--------|---------|
| `register_obj(key, *patterns, **kwargs)` | register a paperdoll object under `key` |
| `get_obj(key)` | fetch the `Paperdoll_Obj` |
| `display(key, *actions)` | run the action pipeline for that object |
| `set_background(pattern, …)` | set/replace the backdrop |
| `set_background_split(left, right, …)` | split backdrop (left half + right half) |
| `hide_background()` | drop the backdrop |
| `clear()` | hide all objects **and** the background |

---

## 3. Layers & pattern resolution

Each layer's pattern is resolved the same way image paths are resolved everywhere in
the game (see [Selectors §7](Selectors) and `images.rpy`):

1. Every `<key>` in the pattern is replaced with the object's matching **value**.
2. `refine_image_with_alternatives(pattern, alt_keys, **values)` generates the path
   **plus fallbacks**: for each key listed in `alt_keys`, a variant is produced where
   that key is replaced by the wildcard `#` (so a missing per-level/mouth/state file
   can fall back to a generic one).
3. `find_available_images(...)` walks the candidates in priority order and returns
   the **first one that actually exists** (`renpy.loadable`). If none exist, the
   layer resolves to `""` and shows nothing.

So `alt_keys` decides *which* values are allowed to be "smoothed over" by a wildcard
when a specific asset is missing — you list the fine-grained keys (level, mouth,
state, variant) and keep the structural ones (pose, outfit) exact.

Resolution is **lazy and cached per layer**: `display_paperdoll_image` only resolves
a layer whose `image[index]` is still `""`. `PDAImage` changes the values and forces
re-resolution; pure movement/blur/flip actions reuse the already-resolved image.

---

## 4. Registering an object

### Characters (the common path)

`Person.register_paperdoll(*overrides, **kwargs)` (in `character.rpy`) is the wrapper
you use 99% of the time. It registers a two-layer object under the person's name with
the body/head patterns and sensible default values:

```python
$ emiko.register_paperdoll()                     # defaults: pose 1, uniform, level 1,
                                                 # mood happy, mouth closed, char_var 1
$ luna.register_paperdoll(level = 10, mood = "happy", mouth = "closed")   # override defaults
```

Defaults it seeds: `alt_keys = ["level", "mouth", "state", "char_var"]`,
`mood="happy"`, `pose=1`, `outfit="uniform"`, `level=1`, `mouth="closed"`,
`state=""`, `blur=0.0`, `char_var=1`, and `display_size=(600, 1080)`. Any
`PaperdollOverride`s declared on the person ([§11](#11-overrides-per-layer-conditional-nudges))
are merged in automatically.

### The general form

Under the hood that calls the manager directly. This is also how you'd register a
**non-character** paperdoll:

```python
paperdoll_manager.register_obj(
    key,                       # unique name; also the show tag prefix
    pattern_layer0,            # one pattern string per layer, bottom → top
    pattern_layer1,
    ...,
    alt_keys = [...],          # keys allowed to fall back to the `#` wildcard
    display_size = (w, h),     # logical on-screen size (see §10); omit for native px
    display_sizes = [...],     # per-layer size overrides (optional)
    overrides = [...],         # list[PaperdollOverride] (optional)
    config = {...},            # initial alignX/alignY/rotation/zoom/blur/bw (optional)
    **initial_values,          # the values that fill the <keys> in the patterns
)
```

Layer order **is** draw order: pattern 0 is drawn first (bottom), later patterns on
top.

---

## 5. Values & the config model

Two distinct dictionaries drive a paperdoll:

**Values** — fill the `<keys>` in the patterns (`pose`, `outfit`, `mood`, `mouth`,
`level`, `state`, `char_var`, `blur`, …). Set at registration, updated by
`PDAImage`. This is *what image* each layer shows.

**Config** — the transform state, shared by all layers. This is *where/how* the stack
is drawn:

| Config key | Meaning | Default |
|------------|---------|---------|
| `alignX` | horizontal alignment (Ren'Py `xalign`; can exceed 0–1 to go off-frame) | `-0.5` |
| `alignY` | vertical position (`ypos`) | `0.0` |
| `zoom` | scale multiplier (on top of the display-size base scale) | `1.0` |
| `rotation` | rotation | `0.0` |
| `blur` | gaussian blur radius | `0.0` |
| `bw` | grayscale when `True` | `False` |

Each layer additionally has a **config override** (`config_override[index]`) — a
small per-layer delta added on top of the shared config. `get_config(key, index)`
returns `config[key] + config_override[index][key]`. The shared config is what your
actions move; the override is where [PaperdollOverride](#11-overrides-per-layer-conditional-nudges)
nudges an individual layer (e.g. shifting only the body for a bulky outfit).

---

## 6. Displaying: the action pipeline

`.display(*actions)` (→ `paperdoll_manager.display` → the `display_paperdoll_image`
label) does two things:

1. **Ensures every layer is shown.** Any layer still unresolved (`image == ""`) is
   resolved now and shown with the current position, blur and bw transforms.
2. **Runs the actions in order.** `run_paperdoll_actions` pops each action and calls
   the label `paperdoll_action_<key>` (e.g. `paperdoll_action_move`). A `PDAPreset`
   is expanded first and its actions run recursively.

Each `.display()` call is one step. A conversation is a **sequence** of `.display()`
calls interleaved with dialogue — change the expression, say a line, change it again:

```python
$ emiko.display(PDAImage(mood = "happy", mouth = "open"))
emiko.say "Gladly."
$ emiko.display(PDAImage(mood = "happy", mouth = "closed"))
```

Motion (`PDAMove`, `PDABlur`, `PDABw`) with a `duration > 0` animates; the transition
is scaled by the player's transition-speed preference automatically. Call
`clear_display()` (→ `paperdoll_manager.clear()`) to hide the object and background
when the paperdoll segment ends.

---

## 7. The action catalog

All actions are `PDAction` subclasses; pass any number to a single `.display()`.

| Action | Constructor | Effect |
|--------|-------------|--------|
| **Image** | `PDAImage(**values)` | merge new values, re-resolve every layer (change pose/outfit/mood/mouth/…) |
| **Move** | `PDAMove(alignX=-100, alignY=-100, zoom=-100, duration=0.0)` | reposition/scale; omitted args keep the current value (sentinel `< -10`); `duration` eases |
| **Blur** | `PDABlur(blur, duration=0.0)` | set blur radius, optionally eased |
| **Bw** | `PDABw(bw=True, duration=0.0)` | toggle grayscale (saturation), optionally eased |
| **Flip** | `PDAFlip(flip=False)` | mirror horizontally (`xzoom`) — `True` faces the other way |
| **Shake** | `PDAShake(duration=1.0, max_distance=15)` | deterministic shake; all layers share one seed so they shake together |
| **Pause** | `PDAPause(duration=0.0, transition=True)` | wait; `transition` scales the wait by transition-speed preference |
| **Preset** | `PDAPreset(preset, **overrides)` | expand a named preset into its actions (see §8) |

Notes:

- **`PDAMove` sentinels.** Leaving an argument at its default (a large negative
  number) means "keep current"; only the values you pass change. That's why
  `PDAMove(alignX = 0.68, duration = 0.4)` slides horizontally without altering zoom.
- **`PDAImage` is the only value-changing action.** Move/blur/flip/bw operate on the
  *already resolved* images and don't re-read the filesystem.
- **Order matters.** Actions in one `.display()` apply left-to-right; e.g. an image
  swap followed by a move.

---

## 8. Presets

A **preset** is a reusable named list of actions — the standard framings, so scenes
don't hand-tune the same `alignX`/`zoom` over and over.

```python
register_preset("upper_body", PDAMove(alignY = -0.1, zoom = 3.0))
register_preset("upper_body_center", PDAPreset("upper_body"), PDAMove(alignX = 0.5))
```

Use them via `PDAPreset("name", **overrides)`. Overrides are applied to every action
in the preset that supports them (so `PDAPreset("upper_body", duration = 0.4)` adds a
0.4s ease to the preset's move). Presets can reference other presets, as
`upper_body_center` does.

Built-in presets (`paperdoll.rpy`):

| Preset | What it frames |
|--------|----------------|
| `outside` | push the figure off-frame to the left (`alignX = -1.5`) |
| `close_body` / `_center` / `_right` / `_left` | mid/close body framing, positioned |
| `upper_body` / `_center` / `_right` / `_left` | tight upper-body framing, positioned |

Registry API: `register_preset(key, *actions)`, `get_preset(key)`,
`get_preset_with_overrides(key, **kwargs)`, `clear_presets()`.

---

## 9. Backgrounds

The manager owns one backdrop, drawn behind all paperdoll objects.

```python
$ paperdoll_manager.set_background("images/background/office building/secretary 6 1 0.webp", blur = True)
```

### What a background source can be

`set_background` (and each side of `set_background_split`) accepts **any** of these
for its source argument — all resolved by `_resolve_background_path`:

| Source form | Example | How it resolves |
|-------------|---------|-----------------|
| **Pattern string** | `"images/background/school building/<level> 0 1.webp"` | `<key>`/alt-key resolution like a layer (`refine_image_with_alternatives` → `find_available_images`) |
| **Concrete path** | `"images/background/office building/secretary 6 1 0.webp"` | returned as-is if `renpy.loadable` |
| **`Image_Series` step** | `image_series[step]` | `Image_Series.__getitem__` yields a concrete loadable path (or `None`); the path is used directly |
| **Event path with `<nude>`** | a raw `get_image` result still holding `<nude>` | resolved via `get_image`, preferring the clothed level `0`, else the highest available nude level |
| **`None` / `""`** | `set_background(None)` | resolves to no background (empty) |

The order matters: a **loadable concrete path wins immediately**, so an
`Image_Series[step]` (which already returns a resolved file) is taken verbatim; only
an unresolved pattern goes through `<key>` substitution. A non-string source logs a
`paperdoll` error and yields no background.

```python
# Drive the backdrop from an image series (e.g. the current scene's step)
$ image = Image_Series("images/events/intro/intro <step>.webp")
$ paperdoll_manager.set_background(image[2], blur = True)
```

### The functions

- **`set_background(pattern=None, blur=False, blur_duration=0.0, bw=False, alt_keys=[], **kwargs)`**
  — resolve `pattern` (any source form above) and show it. `blur=True` maps to radius
  `10.0`, `False` to `0.0`, or pass a float for a custom radius; `blur_duration` eases
  the blur in. `bw=True` desaturates it.
- **`set_background_split(pattern_left=None, pattern_right=None, blur=False, blur_duration=0.0, separator_width=8, bw_left=False, bw_right=False, alt_keys=[], **kwargs)`**
  — composes the **left half** of one source and the **right half** of another (each
  source is any of the forms above) with a white divider strip, for two-location /
  two-character framings. If only one side resolves, it falls back to showing that
  side full-frame.
- **`hide_background()`** — remove it.

The blurred background is the standard "hand off from scene image to conversation"
move: show the establishing scene, then blur its location behind the paperdoll so the
character reads as the subject.

---

## 10. display_size & high-resolution assets

Source sprites are often authored much larger than their intended on-screen size.
`display_size = (width, height)` declares the **logical** size a layer should occupy;
the engine computes a **base scale** = `logical_height / native_height` per layer
(cached) and folds it into the effective zoom. So `zoom = 1.0` means "the intended
on-screen size", and your `PDAMove`/preset zooms are multipliers on top of that —
independent of the raw pixel dimensions of the art.

- `display_size` applies to all layers; `display_sizes = [...]` overrides it
  per-layer (pass `None` in a slot to keep native sizing for that layer).
- Character paperdolls use `display_size = (600, 1080)`.
- Omit both to draw layers at native pixel size (base scale `1.0`).

This is what lets you drop in a 4K sprite and a 1K sprite side by side and have them
render at consistent, art-directed sizes.

---

## 11. Overrides: per-layer conditional nudges

A `PaperdollOverride` adjusts a **single layer's** position/rotation/blur/zoom, but
**only when its conditions match the current values**. Use it when one asset variant
needs a small correction the others don't — e.g. a bulky outfit whose body layer
needs to shift a few thousandths.

```python
PaperdollOverride(
    1,                               # layer index this applies to (here: the body)
    {"outfit": "bunny"},             # active only while values["outfit"] == "bunny"
    x_override = -0.0014,
    y_override = -0.026132,
    # rot_override, blur_override, zoom_override also available
)
```

- The condition dict is matched against the object's current values (equality, or
  membership via `check_in_value`); a non-match contributes zero.
- All matching overrides for a layer are **summed** into that layer's
  `config_override`, which is then added on top of the shared config.
- Overrides are passed at registration (`overrides=[...]`), and a `Person` can carry
  a permanent `paperdollOverrides` list that `register_paperdoll` merges in
  automatically.

Overrides are recomputed on every re-resolution, so they track value changes as the
conversation swaps outfits/poses.

---

## 12. Beyond characters: displaying anything

Nothing in the engine is character-specific. A paperdoll object is just *N pattern
layers + values + a transform*, so you can register one to display **any** stacked
imagery — a machine that gains parts, a signboard whose text layer changes, a
creature assembled from body/wings/overlay — as long as you supply the sprites.

To do so, skip `Person.register_paperdoll` and call the manager directly:

```python
paperdoll_manager.register_obj(
    "reactor",
    "images/props/reactor/core <power> <state>.png",     # layer 0
    "images/props/reactor/shield <shield>.png",          # layer 1
    "images/props/reactor/sparks <power>.png",           # layer 2 (top)
    alt_keys   = ["state", "shield"],                     # allow these to wildcard-fallback
    display_size = (400, 700),
    power = "1", state = "idle", shield = "up",
)
paperdoll_manager.display("reactor",
    PDAMove(alignX = 0.5, alignY = 0.1, zoom = 1.2, duration = 0.5))
paperdoll_manager.display("reactor", PDAImage(power = "3", state = "active"))
paperdoll_manager.display("reactor", PDAShake(duration = 0.6, max_distance = 20))
```

Everything else — presets, backgrounds, blur, bw, flip, overrides, per-layer
`display_sizes` — works identically. The character wrapper is simply the most-used
preset of this general capability.

The only requirements are: a **unique key**, **one pattern per layer**, and matching
**values** so each pattern resolves to a file that exists (or is covered by an
`alt_keys` fallback).

---

## 13. The in-game paperdoll editor

`show_paperdoll_test` (debug menu, `debug.rpy`) is a live editor for **finding the
right config values** for an asset set. It manages its own manager (it calls
`init_paperdoll_manager` / `unload_paperdoll_manager` around the session), lets you
pick a character and cycle `char_var` / `pose` / `outfit` / `level` / `state` /
`mood` / `mouth` (discovered by scanning the actual files on disk), and exposes live
`alignX` / `alignY` / `rotation` / `zoom` / `blur` / `flip` sliders plus the presets.

Use it to dial in the position/zoom for a new pose or outfit, then copy those numbers
into your event's `PDAMove`/preset or into a `PaperdollOverride`. It is a tuning tool,
not something shipped in a scene.

---

## 14. Conventions

- **Register → display → clear.** Always `clear_display()` (or `paperdoll_manager.clear()`)
  when the paperdoll segment ends, so the figure and background don't leak into the
  next beat. Every branch in the New Management events does this.
- **Blur the background, don't remove it.** The house look is a blurred location
  behind the character; use `set_background(..., blur=True)`.
- **Don't reach for paperdolls by default — that's an authorial call, not a rule.**
  Technically you can use paperdolls however you like: begin an event with them, run a
  whole event on them, mix them freely with scene images. But they aren't a substitute
  for art. Interesting, spicy or atmosphere-carrying beats want a properly rendered
  image; the paperdoll shines for lightweight, talky moments where a live, reactive
  figure beats a static shot. Deciding when a scene deserves real art vs. a paperdoll
  is the author's editorial judgement — the caution is only against using paperdolls
  *inflationarily*, for everything.
- **Change images with `PDAImage`, move with the others.** Don't re-register an object
  to change a mood; that's what `PDAImage` is for. Re-registration is for a genuinely
  new object.
- **Let `alt_keys` absorb missing variants.** List the fine-grained keys (level,
  mouth, state, variant) so a missing specific asset falls back to a generic one
  instead of vanishing.
- **Tune with the editor, ship the numbers.** Find `alignX`/`zoom` in
  `show_paperdoll_test`, then hard-code them — don't guess.
- **Normalize sizes with `display_size`.** Declare the intended on-screen size so
  `zoom = 1.0` is meaningful regardless of the source resolution.

---

## 15. Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Nothing appears | No layer resolved to an existing file | Check the pattern's `<keys>` match your values and the file exists; add `alt_keys` for the missing dimension. |
| Only one layer shows | The other layer's pattern resolves to `""` | Verify that layer's file for the current values; check the `#` fallback path. |
| Figure is the wrong size | `display_size` missing or wrong | Set `display_size` to the intended on-screen size; then use `zoom` as a multiplier. |
| Position/zoom won't change | Passing sentinels or wrong action | `PDAMove` keeps any arg you omit; pass the ones you want changed. Only `PDAMove`/presets move. |
| Expression won't update | Not using `PDAImage` | Change `mood`/`mouth` via `PDAImage`; move/blur don't re-resolve images. |
| Two layers drift apart on shake | (shouldn't happen) all layers share the shake seed | Confirm you're on `PDAShake` (seeded by the object key), not per-layer motion. |
| One outfit sits a few pixels off | Needs a per-layer correction | Add a `PaperdollOverride` on that layer gated on the outfit value. |
| Paperdoll persists into the next scene | Missing teardown | Call `clear_display()` / `paperdoll_manager.clear()` at the end of the segment. |
| `paperdoll_manager is None` outside an event | No manager (event flow creates it) | Call `init_paperdoll_manager()` yourself (as the debug editor does). |

---

## 16. Reference tables

### Manager (`PaperdollManager`)
`register_obj(key, *patterns, **kwargs)` · `get_obj(key)` · `display(key, *actions)` ·
`set_background(pattern=None, blur, blur_duration, bw, alt_keys, **kwargs)` ·
`set_background_split(left=None, right=None, blur, blur_duration, separator_width, bw_left, bw_right, alt_keys, **kwargs)` ·
`hide_background()` · `clear()`. Background source = pattern string · concrete/loadable
path · `Image_Series[step]` · `<nude>` event path · `None`. Globals:
`init_paperdoll_manager()` / `unload_paperdoll_manager()`.

### Object (`Paperdoll_Obj`)
Constructed as `(key, *patterns, **kwargs)`. kwargs: `overrides`, `alt_keys`,
`config`, `display_size`, `display_sizes`, plus initial values. Config keys:
`alignX -0.5`, `alignY 0.0`, `rotation 0.0`, `zoom 1.0`, `blur 0.0`, `bw False`.
`get_config(key, index)` = shared config + layer override.

### Actions
`PDAImage(**values)` · `PDAMove(alignX, alignY, zoom, duration)` ·
`PDABlur(blur, duration)` · `PDABw(bw, duration)` · `PDAFlip(flip)` ·
`PDAShake(duration, max_distance)` · `PDAPause(duration, transition)` ·
`PDAPreset(preset, **overrides)`. Each runs via label `paperdoll_action_<key>`.

### Presets
`register_preset(key, *actions)` · `get_preset(key)` ·
`get_preset_with_overrides(key, **kwargs)` · `clear_presets()`. Built-ins:
`outside`, `close_body(_center/_right/_left)`, `upper_body(_center/_right/_left)`.

### Character helper (`character.rpy`)
`person.register_paperdoll(*overrides, **kwargs)` (2 layers, `display_size=(600,1080)`,
`alt_keys=["level","mouth","state","char_var"]`) · `person.display(*actions)` ·
`person.clear_display()` · `PaperdollOverride(index, conditions, x_override,
y_override, rot_override, blur_override, zoom_override)`.

### Related files
- `game/scripts/paperdoll.rpy` — manager, object, actions, presets, transforms, labels
- `game/scripts/character.rpy` — `register_paperdoll` / `display` / `clear_display`, `PaperdollOverride` usage
- `game/scripts/images.rpy` — `refine_image_with_alternatives` / `find_available_images` (`<key>` + `#` resolution); `Image_Series` (background `image[step]` source)
- `game/scripts/event.rpy` — creates/unloads the manager around each event
- `game/scripts/debug.rpy` — `show_paperdoll_test`, the in-game editor
- `game/scripts/events/new_management.rpy` — worked examples (register → display → clear)
- [Selectors](Selectors) — how `<key>` values are produced and substituted into paths
