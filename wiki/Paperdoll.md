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
# no teardown: the next image.show(...) or end_event already paperdoll_manager.clear()s
```

More copy-paste recipes (two people, flip/walk-off, temp presets, split backdrop, …)
are in [§8 Worked examples](#8-worked-examples).

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
8. [Worked examples](#8-worked-examples)
9. [Presets](#9-presets)
10. [Backgrounds](#10-backgrounds)
11. [display_size & high-resolution assets](#11-display_size--high-resolution-assets)
12. [Overrides: per-layer conditional nudges](#12-overrides-per-layer-conditional-nudges)
13. [Beyond characters: displaying anything](#13-beyond-characters-displaying-anything)
14. [Paperdoll editors (tuning tools)](#14-paperdoll-editors-tuning-tools)
15. [Conventions](#15-conventions)
16. [Troubleshooting](#16-troubleshooting)
17. [Reference tables](#17-reference-tables)

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
[§13](#13-beyond-characters-displaying-anything).

---

## 2. Manager lifecycle

The compositor is a single global, `paperdoll_manager` (a `PaperdollManager`).

- **`init_paperdoll_manager()`** — creates a fresh manager.
- **`unload_paperdoll_manager()`** — clears every object + background, then drops it.

**In events you normally do neither.** `begin_event` calls
`init_paperdoll_manager()` and `end_event` calls `unload_paperdoll_manager()`
(`event.rpy`), so the manager already exists inside a scene and is gone afterwards.
`$ image.show(n)` (`Image_Series.show`) also runs `paperdoll_manager.clear()` before
it puts up the still. Cutting to a scene image or ending the event is therefore
**self-cleaning** — you do not need a trailing `clear_display()`.

Call `Person.clear_display()` / `paperdoll_manager.clear()` only **on demand**: a
blank beat before something that does *not* auto-clear (`call show_image`, a custom
`renpy.show`, an empty pause). It hides **every** object plus the backdrop, not one
character. You only init/unload the manager by hand outside the event flow (the
debug editor does exactly that — see [§14](#14-paperdoll-editors-tuning-tools)).

Manager surface you use directly:

| Method | Purpose |
|--------|---------|
| `register_obj(key, *patterns, **kwargs)` | register a paperdoll object under `key` |
| `get_obj(key)` | fetch the `Paperdoll_Obj` |
| `display(key, *actions)` | run the action pipeline for that object |
| `set_background(pattern, …)` | set/replace the backdrop (`zorder -100`) |
| `set_background_split(left, right, …)` | split backdrop (left half + right half) |
| `hide_background()` | drop the backdrop |
| `clear()` | hide all objects **and** the background |

---

## 3. Layers & pattern resolution

Each layer's pattern is resolved the same way image paths are resolved everywhere in
the game (see [Images](Images) and [Selectors §7](Selectors)):

1. Every `<key>` in the pattern is replaced with the object's matching **value**.
2. `refine_image_with_alternatives(pattern, alt_keys, **values)` generates the path
   **plus fallbacks**: for each key listed in `alt_keys`, a variant is produced where
   that key is replaced by the wildcard `$` (so a missing per-level/mouth/state file
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
`PaperdollOverride`s and `PaperdollPreset`s declared on the person
([§12](#12-overrides-per-layer-conditional-nudges), [§9](#9-presets)) are merged in
automatically.

### The general form

Under the hood that calls the manager directly. This is also how you'd register a
**non-character** paperdoll:

```python
paperdoll_manager.register_obj(
    key,                       # unique name; also the show tag prefix
    pattern_layer0,            # one pattern string per layer, bottom → top
    pattern_layer1,
    ...,
    alt_keys = [...],          # keys allowed to fall back to the `$` wildcard
    display_size = (w, h),     # logical on-screen size (see §11); omit for native px
    display_sizes = [...],     # per-layer size overrides (optional)
    overrides = [...],         # list[PaperdollOverride] (optional)
    presets = [...],           # list[PaperdollPreset] → temp "{key}:{preset}" (optional)
    parent = "aona",           # parent object key; must already be registered (optional)
    local = {"alignX": 0.08},  # relative transform when parented (optional)
    space = "screen",          # "screen" offsets, or "parent" = 0–1 on parent box
    behind = False,            # True → zorder -1 (still above the background)
    config = {...},            # initial alignX/alignY/rotation/zoom/blur/bw (optional)
    **initial_values,          # the values that fill the <keys> in the patterns
)
```

Layer order **is** draw order: pattern 0 is drawn first (bottom), later patterns on
top.

### Parenting

A paperdoll can take another registered object as `parent`. The child keeps its own
values, presets, and tags; only its **transform** follows the parent.

- `config` is always **world** space (what the show transforms read).
- When parented, `PDAMove` / `PDAFlip` write `local` (relative to the parent), then
  compose into `config`.
- `space` chooses how `local.alignX` / `alignY` are interpreted:
  - `"screen"` (default) — screen-unit offsets added to the parent (`alignX`
    flips with parent facing). `0.0` = same position as the parent, not
    “left of the sprite”.
  - `"parent"` — `0–1` on the parent's `display_size` box (`0` left/top, `0.5`
    centre, `1` right/bottom). X mirrors around the box centre when the parent
    flips. Needs a parent `display_size` (characters already have `(600, 1080)`).
- Compose folds the **full ancestor chain** (nested parents are allowed:
  `mug` → `hand` → `aona`).
- Move / flip / shake on a parent fan out to the whole subtree with the same
  duration. Register ancestors first; cycles are rejected with a log error.

See [§8 Parenting a prop](#parenting-a-prop) for a recipe.

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
| `alignX` | horizontal alignment: `0.0` left edge at the left of the screen, `1.0` right edge at the right, at any zoom. Values outside 0–1 continue off that edge. Zoom grows around this point. | `-0.5` |
| `alignY` | vertical position (`ypos`) | `0.0` |
| `zoom` | scale multiplier (on top of the display-size base scale) | `1.0` |
| `rotation` | rotation | `0.0` |
| `blur` | gaussian blur radius | `0.0` |
| `bw` | grayscale when `True` | `False` |
| `flip` | horizontal mirror (`xzoom`; `1.0` unflipped, `-1.0` mirrored) | `1.0` |

Each layer additionally has a **config override** (`config_override[index]`) — a
small per-layer delta added on top of the shared config. `get_config(key, index)`
returns `config[key] + config_override[index][key]`. The shared config is what your
actions move; the override is where [PaperdollOverride](#12-overrides-per-layer-conditional-nudges)
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

Motion (`PDAMove`, `PDABlur`, `PDABw`, `PDAFlip`) with a `duration > 0` animates; the transition
is scaled by the player's transition-speed preference automatically. Duration does **not**
block the pipeline — follow a timed action with `PDAPause` of the same length if the next
action would replace the transform. Teardown is automatic: `$ image.show(…)` and
`end_event` both `paperdoll_manager.clear()`. Use `clear_display()` only for a
mid-scene blank that those two will not cover.

---

## 7. The action catalog

All actions are `PDAction` subclasses; pass any number to a single `.display()`.

| Action | Constructor | Effect |
|--------|-------------|--------|
| **Image** | `PDAImage(**values)` | merge new values, re-resolve every layer (change pose/outfit/mood/mouth/…) |
| **Move** | `PDAMove(alignX=-100, alignY=-100, zoom=-100, duration=0.0)` | reposition/scale; omitted args keep the current value (sentinel `< -10`); `duration` eases |
| **Blur** | `PDABlur(blur, duration=0.0)` | set blur radius, optionally eased |
| **Bw** | `PDABw(bw=True, duration=0.0)` | toggle grayscale (saturation), optionally eased |
| **Flip** | `PDAFlip(flip=False, duration=0.0)` | mirror horizontally (`xzoom`); `duration` eases, `0.0` snaps |
| **Shake** | `PDAShake(duration=1.0, max_distance=15)` | deterministic shake; all layers share one seed so they shake together |
| **Pause** | `PDAPause(duration=0.0, transition=True)` | wait; `transition` scales the wait by transition-speed preference |
| **Preset** | `PDAPreset(preset, **overrides)` | expand a named preset into its actions (see [§9](#9-presets)) |

Notes:

- **`PDAMove` sentinels.** Leaving an argument at its default (a large negative
  number) means "keep current"; only the values you pass change. That's why
  `PDAMove(alignX = 0.68, duration = 0.4)` slides horizontally without altering zoom.
- **Delta strings.** Any numeric action field accepts `"+0.5"` / `"-0.1"` (string
  must start with `+` or `-`). At apply time that delta is added to the current
  value — e.g. `PDAMove(alignX = "+0.1")` nudges right from wherever they are;
  `PDABlur("+5")` adds to the current blur. Plain `"0.5"` (no sign) is absolute.
  Preset overrides resolve duration/max_distance deltas against the action's prior
  number immediately (`PDAPreset("x", duration = "+0.4")`).
- **`alignX` is zoom-independent.** `0.0` is always left-aligned, `1.0` always
  right-aligned; extra zoom grows around that point. `< 0` / `> 1` continue linearly
  off that screen edge (same as `xalign` at zoom 1.0).
- **Zoom and position ease together.** `alignX`, `alignY` and `zoom` interpolate in
  the same move — `PDAMove(zoom = 2.0, alignX = 1.0, alignY = -0.1, duration = 1.0)`
  is one ease, not two sequential actions.
- **Sequential timed actions need a pause.** `duration` only drives the ATL ease;
  the next action in the same `.display()` starts immediately and replaces the
  transform. Chain with `PDAPause` of the same length:
  `PDAFlip(True, duration = 1.0), PDAPause(1.0), PDAMove(alignX = 1.0, duration = 1.0), PDAPause(1.0)`.
- **Flip is stored.** `PDAFlip` writes `config["flip"]` (`1.0` / `-1.0`), so later
  moves and image swaps keep the facing. `duration = 0.0` (the default) snaps as before.
  The ease pivots around the **sprite's horizontal center**, not the `xalign` point —
  otherwise a right-aligned figure would swing off-frame as `xzoom` passes through 0.
- **`PDAImage` is the only value-changing action.** Move/blur/flip/bw operate on the
  *already resolved* images and don't re-read the filesystem.
- **Order matters.** Actions in one `.display()` apply left-to-right; e.g. an image
  swap followed by a move.

---

## 8. Worked examples

Copy-paste recipes. Each assumes `begin_event` already created `paperdoll_manager`.
You do **not** need a trailing `clear_display()`: `$ image.show(n)` and `end_event`
already `paperdoll_manager.clear()`. `Person.clear_display()` is the same call —
it hides **every** object plus the backdrop — so use it only for a mid-scene blank
that those two will not cover, and never once per character.

| I want to… | Jump |
|------------|------|
| Hand off a still to a talking sprite | [Scene image → talking figure](#scene-image--talking-figure) |
| Open/close the mouth around dialogue | [Expression while they talk](#expression-while-they-talk) |
| Two characters, one each side | [Two people, left and right](#two-people-left-and-right) |
| Enter from off-screen / leave | [Slide in from off-screen](#slide-in-from-off-screen) |
| Zoom and slide in one ease | [Zoom and slide in one move](#zoom-and-slide-in-one-move) |
| Flip, then walk off, then return | [Timed sequence](#timed-sequence-turn-then-walk-off-then-come-back) |
| Repeat a framing only in this event | [Scene-local presets](#scene-local-presets) |
| Character-specific framing / pose pack | [Object presets](#object-presets-on-a-character) |
| Prop that follows a character | [Parenting a prop](#parenting-a-prop) |
| Nested parents (`mug` → `hand` → character) | [Nested parenting](#nested-parenting) |
| Two locations on one screen | [Split backdrop](#split-backdrop-two-locations) |
| Shake / blur / grayscale | [Emphasis](#emphasis-shake-blur-grayscale) |
| Hide one person, keep the other | [Hide one person](#hide-one-person-keep-the-other) |
| Change location behind them | [Change the backdrop](#change-the-backdrop-mid-scene) |
| Swap outfit or nude level | [Outfit or level swap](#outfit-or-level-swap) |
| Stack something that isn't a character | [Non-character stack](#non-character-stack) |

### Scene image → talking figure

The house hand-off: show the establishing shot, then blur that location behind a live
sprite. `lab_intro` does this with an `Image_Series` step as the backdrop.

```python
$ image = Image_Series("images/events/lab_intro/lab_intro <step>.webp")
$ image.show(2)
headmaster "How do you feel?"

$ image.hide()
$ secretary.register_paperdoll()
$ paperdoll_manager.set_background(image[2], blur = True)
$ secretary.display(
    PDAImage(pose = "21", mood = "neutral", mouth = "open"),
    PDAPreset("close_body_center", duration = 0.0))
secretary "Hmm. A little warmer."
$ secretary.display(PDAImage(mood = "happy", mouth = "closed"))
...
$ image.show(3)    # still; also paperdoll_manager.clear()
```

`set_background(image[step], blur = True)` takes the already-resolved series path; see
[§10](#10-backgrounds).

### Expression while they talk

`PDAImage` is the only action that re-resolves files. Change `mouth` (and `mood`)
around each line; leave pose/outfit/zoom alone so the figure doesn't jump.

```python
$ emiko.display(PDAImage(mood = "happy", mouth = "open"))
emiko.say "Gladly."
$ emiko.display(PDAImage(mood = "happy", mouth = "closed"))
```

A pose swap is the same call — current `alignX` / `zoom` / `flip` stay in config:

```python
$ aona.display(PDAImage(pose = "23", mood = "happy", mouth = "closed"))
```

### Two people, left and right

`alignX` is zoom-independent: `0.0` left edge, `1.0` right edge, at any zoom. Built-in
`close_body_left` / `_right` already encode that.

```python
$ aona.register_paperdoll()
$ ikushi.register_paperdoll()
$ paperdoll_manager.set_background(image[1], blur = True)

$ aona.display(
    PDAImage(pose = "7", outfit = "uniform", level = 1, mood = "suspicious", mouth = "closed"),
    PDAPreset("close_body_left", duration = 0.0))
$ ikushi.display(
    PDAImage(pose = "7", mood = "suprised", mouth = "open"),
    PDAFlip(True),
    PDAPreset("close_body_right", duration = 0.0))

aona.say "Trust me."
$ aona.display(PDAImage(mouth = "closed"))
$ ikushi.display(PDAImage(mood = "sad", mouth = "open"))
ikushi.say "...if you say so."
# next image.show(...) or end_event clears both figures and the backdrop
```

`PDAFlip(True)` is stored on the object, so later `PDAImage` / `PDAMove` keep the
facing. Nudge further inward with a second move if the preset sits too tight on the
edge: `PDAPreset("close_body_right"), PDAMove(alignX = 0.85)`.

### Slide in from off-screen

Park them in `outside` (`alignX = -1.5`) at duration 0, then ease a positioned preset:

```python
$ emiko.display(
    PDAImage(pose = "1", outfit = "uniform", level = 6, mood = "neutral", mouth = "closed"),
    PDAPreset("upper_body", duration = 0.0),
    PDAPreset("outside",    duration = 0.0))
$ emiko.display(PDAPreset("upper_body_center", duration = 0.4))
```

Same idea to leave: ease `outside` (or `alignX = 2.5` off the right) and **pause** so
the ease can finish before the next show replaces it.

```python
$ secretary.display(
    PDAImage(mood = "happy", mouth = "closed"),
    PDAPreset("outside", duration = 1.0),
    PDAPause(duration = 1.0))
```

### Zoom and slide in one move

`alignX`, `alignY` and `zoom` ease together in a single `PDAMove`. Do **not** split
them into two `PDAMove`s unless you want two sequential steps (and then you still
need a `PDAPause` between them).

```python
$ ikushi.display(
    PDAImage(pose = "1", mood = "neutral", mouth = "closed"),
    PDAFlip(True),
    PDAMove(zoom = 2.0, alignX = 1.0, alignY = -0.1, duration = 1.0))
```

`0.0` / `1.0` stay left / right at zoom 2 or 3 — you no longer compensate with `1.3`
or `6.0`. Values `< 0` / `> 1` continue off that edge.

### Timed sequence: turn, then walk off, then come back

`duration` only drives the ATL ease. The next action in the same `.display()` starts
immediately and **replaces** the transform. Chain with `PDAPause` of the same length.
Flip eases around the sprite's horizontal centre.

```python
$ ikushi.display(
    PDAFlip(False, duration = 0.5),
    PDAPause(0.5),
    PDAMove(alignX = 2.5, duration = 1.0),
    PDAPause(1.0))
# she is off-frame; Aona can react
$ aona.display(PDAImage(pose = "23", mood = "happy", mouth = "closed"))
# return, still flipped from config — set facing again if she turned
$ ikushi.display(
    PDAFlip(True),
    PDAImage(mood = "sad"),
    PDAMove(alignX = 1.0, duration = 1.0),
    PDAPause(1.0))
```

Two `.display()` calls with dialogue between them also wait — you only need
`PDAPause` when nothing else holds the beat.

### Scene-local presets

`register_temp_preset` is the same as `register_preset` but is discarded when the
manager unloads (`end_event`). Use it for framings you will repeat in **this** event
and don't want in the global table. You cannot overwrite a permanent name.

```python
$ register_temp_preset("cbl", PDAMove(alignX = 0.0, alignY = -0.1, zoom = 2.0))
$ register_temp_preset("cbr", PDAMove(alignX = 1.0, alignY = -0.1, zoom = 2.0))
$ aona.display(PDAImage(pose = "7", mood = "suspicious"), PDAPreset("cbl", duration = 0.0))
$ ikushi.display(PDAImage(pose = "7", mood = "suprised"), PDAFlip(True), PDAPreset("cbr"))
```

### Split backdrop (two locations)

Left half of one source, right half of another, white divider. Each side accepts the
same sources as `set_background` (path, pattern, `image[step]`, …).

```python
$ paperdoll_manager.set_background_split(
    "images/background/school building/1 0 1.webp",
    "images/background/office building/secretary 6 1 0.webp",
    blur = True)
$ emiko.display(PDAImage(...), PDAPreset("close_body_left"))
$ luna.display(PDAImage(...), PDAPreset("close_body_right"))
```

### Emphasis: shake, blur, grayscale

```python
$ emiko.display(PDAShake(duration = 0.6, max_distance = 20))
$ emiko.display(PDABlur(10.0, duration = 0.4), PDAPause(0.4))
$ emiko.display(PDABw(True, duration = 0.5), PDAPause(0.5))   # flashback / memory
$ emiko.display(PDABw(False, duration = 0.5), PDAPause(0.5))  # restore colour
```

Shake uses one seed per object so body and head move together. Blur/bw, like move,
need a pause if the next action would replace the transform.

### Hide one person, keep the other

`Person.clear_display()` is `paperdoll_manager.clear()`: it hides **everyone** and
the backdrop. To drop only one figure mid-scene, hide that object's layers and
leave the other registered:

```python
$ paperdoll_manager.get_obj(ikushi.name).hide_all_images()
# Aona stays; Ikushi is gone. Bring her back with a normal display:
$ ikushi.display(
    PDAImage(mood = "sad", mouth = "open"),
    PDAFlip(True),
    PDAPreset("close_body_right", duration = 0.0))
```

Walking her off-screen (`PDAMove(alignX = 2.5, duration = 1.0)` + `PDAPause`) is
the animated version of the same idea.

### Change the backdrop mid-scene

`set_background` replaces the manager's one backdrop; figures already on screen
stay. Same source forms as the first call (path, pattern, `image[step]`, …).

```python
$ paperdoll_manager.set_background(image[5], blur = True)   # new location, still blurred
$ paperdoll_manager.hide_background()                       # figures only, no backdrop
```

To *cut* to a full-screen still, just `$ image.show(n)` — `Image_Series.show`
already `paperdoll_manager.clear()`s. No extra hide.

### Outfit or level swap

Same action as a mood change — `PDAImage` re-resolves layers whose patterns use
those keys. Framing (`alignX` / `zoom` / `flip`) is unchanged.

```python
$ emiko.display(PDAImage(outfit = "casual", level = 1, mouth = "closed"))
$ emiko.display(PDAImage(level = 3))    # nude-level step; body layer only
```

If a bulky outfit sits a few pixels off, that is a [PaperdollOverride](#12-overrides-per-layer-conditional-nudges),
not a new `PDAMove`.

### Object presets on a character

Declare named action packs on the `Person` (or pass `presets=` to `register_obj`).
On register they become temp keys `"{name}:{key}"`. Bare preset names must not
contain `:` — that character is the cross-object scope separator.

```python
# on the Person definition:
paperdollPresets = [
    PaperdollPreset(
        "intro",
        PDAImage(pose = "12", mood = "neutral", mouth = "closed"),
        PDAMove(alignX = 0.85, alignY = -0.1, zoom = 2.0),
    ),
]

$ aona.register_paperdoll()
$ aona.display(PDAPreset("intro"), PDAImage(mouth = "open"))
# another object can borrow it:
$ emiko.display(PDAPreset("aona:intro"))
```

Lookup order for `PDAPreset(arg)` while displaying `obj`: try `"{obj.key}:{arg}"`,
then `arg` as-is. See [§9](#9-presets).

### Parenting a prop

Register the parent first, then the child with `parent=` and a `local` offset.
Moves and flips on the parent ease the child with them.

**Screen offsets** (`space="screen"`, default) — `local.alignX` is added in screen
units:

```python
$ paperdoll_manager.register_obj(
    "mug",
    "images/props/mug/mug <state>.png",
    parent = aona.name,
    local = {"alignX": 0.08, "alignY": 0.02, "zoom": 0.4},
    state = "full",
)
```

**Parent box** (`space="parent"`) — `local.alignX/Y` are 0–1 on the parent's
`display_size` box (`0.5` = centre of Aona's 600×1080 box):

```python
$ aona.register_paperdoll()
$ paperdoll_manager.register_obj(
    "mug",
    "images/props/mug/mug <state>.png",
    parent = aona.name,
    space = "parent",
    local = {"alignX": 0.72, "alignY": 0.45, "zoom": 0.35},
    state = "full",
)
$ aona.display(PDAImage(pose = "7"), PDAPreset("close_body_right"))
$ paperdoll_manager.display("mug", PDAImage(state = "full"))
$ aona.display(PDAMove(alignX = 0.5, duration = 0.5), PDAPause(0.5))
# mug stays on that point of her box while she moves / flips
```

### Nested parenting

```python
$ aona.register_paperdoll()
$ paperdoll_manager.register_obj("hand", "...", parent = aona.name, local = {"alignX": 0.1})
$ paperdoll_manager.register_obj("mug", "...", parent = "hand", local = {"alignX": 0.02, "zoom": 0.5})
```

A move on `aona` updates `hand` and `mug`. A move on `hand` only changes `hand.local`
(relative to Aona) and re-composes `mug`.

### Non-character stack

Skip `Person.register_paperdoll` and register patterns yourself — [§13](#13-beyond-characters-displaying-anything).

---

## 9. Presets

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

| Preset | Framing |
|--------|---------|
| `outside` | `alignX = -1.5` — off the left edge |
| `close_body` | `alignY = -0.1`, `zoom = 2.0` (no X yet) |
| `close_body_center` | close_body + `alignX = 0.5` |
| `close_body_right` | close_body + `alignX = 1.0` |
| `close_body_left` | close_body + `alignX = 0.0` |
| `upper_body` | `alignY = -0.1`, `zoom = 3.0` |
| `upper_body_center` | upper_body + `alignX = 0.5` |
| `upper_body_right` | upper_body + `alignX = 1.0` |
| `upper_body_left` | upper_body + `alignX = 0.0` |

`_left` / `_right` use `0.0` / `1.0` so they stay on the correct edge at any zoom.
Add `duration` via override: `PDAPreset("close_body_right", duration = 0.4)`.

**Temporary presets.** `register_temp_preset(key, *actions)` is the same lookup
(`PDAPreset("key")`) but is wiped when the manager unloads. Permanent names cannot
be overwritten. See [§8 Scene-local presets](#scene-local-presets).

**Object presets.** A third scope lives on the paperdoll object / `Person`:

```python
PaperdollPreset("intro", PDAImage(pose = "12"), PDAMove(alignX = 0.85, zoom = 2.0))
```

`register_obj(..., presets=[...])` (and `Person.paperdollPresets` via
`register_paperdoll`) stores each as a **temp** key `"{object_key}:{preset_key}"`.
Preset keys must not contain `:`.

When `PDAPreset(arg)` expands during `.display()` on object `obj`:

1. look up `"{obj.key}:{arg}"` (e.g. `aona:intro`, or `emiko:aona:intro` when the
   argument is already scoped)
2. if missing, look up `arg` as-is (global / temp / already-scoped `aona:intro`)

So `PDAPreset("intro")` on Aona hits `aona:intro`; `PDAPreset("aona:intro")` on Emiko
misses `emiko:aona:intro` and finds `aona:intro`. Nested `PDAPreset("close_body")`
inside an object preset uses the same rule — an object can locally sharpen a built-in.

Expand **deep-copies** the action list before applying `**overrides`, so
`PDAPreset("intro", duration = 0.4)` does not mutate the stored preset.

Registry API: `register_preset(key, *actions)`, `register_temp_preset(key, *actions)`,
`get_preset(key, paperdoll_obj=None)`,
`get_preset_with_overrides(key, paperdoll_obj=None, **kwargs)`,
`clear_temp_presets()`, `clear_presets()`.

---

## 10. Backgrounds

The manager owns one backdrop, drawn **behind** all paperdoll objects
(`zorder = -100`; figures use `0`, or `-1` when `behind=True`). Order of
`set_background` vs `.display()` does not matter — a late background cannot cover
a figure.

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

## 11. display_size & high-resolution assets

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

## 12. Overrides: per-layer conditional nudges

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

## 13. Beyond characters: displaying anything

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

## 14. Paperdoll editors (tuning tools)

Two companion tools let you assemble a paperdoll and read off what it takes — one
inside the game, one on the desktop. Neither ships in a scene; both exist to find the
right combination/numbers, which you then hard-code into your event.

### In-game editor — `show_paperdoll_test`

`show_paperdoll_test` (debug menu, `debug.rpy`) is a live editor for **finding the
right config values** for an asset set. It manages its own manager (it calls
`init_paperdoll_manager` / `unload_paperdoll_manager` around the session), lets you
pick a character and cycle `char_var` / `pose` / `outfit` / `level` / `state` /
`mood` / `mouth` (discovered by scanning the actual files on disk), and exposes live
`alignX` / `alignY` / `rotation` / `zoom` / `blur` / `flip` sliders plus the presets.

Use it to dial in the position/zoom for a new pose or outfit, then copy those numbers
into your event's `PDAMove`/preset or into a `PaperdollOverride`. It is a tuning tool,
not something shipped in a scene.

### Standalone viewer — `tools/paperdoll_viewer.py`

A self-contained desktop app (Tkinter + Pillow) that reproduces the *combination* side
of the editor **outside Ren'Py**. It scans `game/images/paperdoll` directly and lets
you cascade character / `char_var` / `pose` / `outfit` / `level` / `state` / `mood` /
`mouth` — offering only combinations that actually resolve to a file, exactly like the
in-game selector — and previews the composed body + head live in a large,
portrait-oriented panel. It can swap the backdrop (checkerboard / dark / light / green)
and export the composited PNG.

**Copy-ready `PDAImage(...)`.** Each field has a checkbox, and a *Copy PDAImage*
button puts a ready-to-paste call on the clipboard containing exactly the checked
fields — e.g. `PDAImage(pose = "1", outfit = "uniform", level = 6, mood = "neutral",
mouth = "open")`. Defaults mirror the house style (pose/outfit/level/mood/mouth on,
`char_var`/`state` off); tick those extra boxes only when a scene needs them. So you
dial in the look and paste the exact line into your event — no transcribing values by
hand.

Why it exists alongside the in-game editor: while **writing an event you can keep the
game paused on that beat** to watch your scene edits, and compose/preview the
paperdoll's pose/outfit/mood in the external window **at the same time** — no jumping
back and forth between the running event and `show_paperdoll_test`. Settle on the
pose / outfit / mood / mouth combination you want here, copy the `PDAImage(...)`, and
paste it straight into your event.

Run it with Python 3.9+ (needs `pillow` — `pip install pillow`):

```
python tools/paperdoll_viewer.py
```

or double-click `tools/Paperdoll Viewer.bat` on Windows. It auto-detects the
`game/images/paperdoll` folder relative to the repo (pass `--root <path>` to point it
elsewhere) and reads the assets **read-only** — it never modifies game files.

Division of labour: the standalone viewer nails the **image combination** (which
pose/outfit/mood/mouth), while the in-game editor is still where you tune the
**transform** (`alignX` / `zoom` / `blur` / … over the live background).

---

## 15. Conventions

- **Teardown is automatic.** `$ image.show(n)` and `end_event` both
  `paperdoll_manager.clear()`. Reach for `clear_display()` only when you need a
  blank *before* something that does not auto-clear. It is not a per-character
  hide (`get_obj(name).hide_all_images()` is).
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
- **`PDAImage` keeps the current transform.** A pose/mood swap does not reset
  `alignX` / `zoom` / `flip`. Pass a `PDAMove` only when you actually want to reframe.
- **Normalize sizes with `display_size`.** Declare the intended on-screen size so
  `zoom = 1.0` is meaningful regardless of the source resolution.

---

## 16. Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Nothing appears | No layer resolved to an existing file | Check the pattern's `<keys>` match your values and the file exists; add `alt_keys` for the missing dimension. |
| Only one layer shows | The other layer's pattern resolves to `""` | Verify that layer's file for the current values; check the `$` fallback path. |
| Figure is the wrong size | `display_size` missing or wrong | Set `display_size` to the intended on-screen size; then use `zoom` as a multiplier. |
| `PDAImage` (pose swap) suddenly huge | Unrelated — current `zoom` is kept from the last `PDAMove`/preset | Pass `PDAMove(zoom = …)` only if you want a new scale; don't re-register. |
| Position/zoom won't change | Passing sentinels or wrong action | `PDAMove` keeps any arg you omit; pass the ones you want changed. Only `PDAMove`/presets move. |
| Right-align needs `alignX = 1.3` at zoom 2 | Old compensation; `alignX` is zoom-independent | Use `0.0` left / `1.0` right at any zoom (`close_body_left` / `_right`). |
| Timed move/flip is skipped | Next action in the same `.display()` replaced the transform | Insert `PDAPause` of the same length; see [§8](#8-worked-examples). |
| Flip swings off-frame while easing | Flip must pivot on the sprite centre (engine does this) | Don't animate `xzoom` yourself; use `PDAFlip(..., duration = …)`. |
| Expression won't update | Not using `PDAImage` | Change `mood`/`mouth` via `PDAImage`; move/blur don't re-resolve images. |
| Two layers drift apart on shake | (shouldn't happen) all layers share the shake seed | Confirm you're on `PDAShake` (seeded by the object key), not per-layer motion. |
| One outfit sits a few pixels off | Needs a per-layer correction | Add a `PaperdollOverride` on that layer gated on the outfit value. |
| `PDAPreset("intro")` does nothing | Object preset not registered / wrong key | Ensure `PaperdollPreset` is on the Person or `presets=`; bare keys have no `:`. |
| Child prop does not follow | Not parented, or never shown | `register_obj(..., parent=...)`; `.display` the child once so layers resolve. |
| Parenting fails silently | Parent missing or cycle | Register ancestors first; check the `paperdoll` log for cycle / missing parent. |
| Background covers the figure | (fixed) late `set_background` used to win z-order | Background is `zorder -100`; figures stay above. |
| Paperdoll persists into the next still | The still was not `Image_Series.show` | `$ image.show(n)` clears; `call show_image` / a raw `renpy.show` does not — then `clear_display()` first. `end_event` always unloads. |
| `paperdoll_manager is None` outside an event | No manager (event flow creates it) | Call `init_paperdoll_manager()` yourself (as the debug editor does). |

---

## 17. Reference tables

### Manager (`PaperdollManager`)
`register_obj(key, *patterns, **kwargs)` · `get_obj(key)` · `display(key, *actions)` ·
`set_background(pattern=None, blur, blur_duration, bw, alt_keys, **kwargs)` ·
`set_background_split(left=None, right=None, blur, blur_duration, separator_width, bw_left, bw_right, alt_keys, **kwargs)` ·
`hide_background()` · `clear()`. Per object: `get_obj(key).hide_all_images()` hides
that stack only (`clear()` hides every object plus the background). Background source = pattern string · concrete/loadable
path · `Image_Series[step]` · `<nude>` event path · `None`. Globals:
`init_paperdoll_manager()` / `unload_paperdoll_manager()`.

### Object (`Paperdoll_Obj`)
Constructed as `(key, *patterns, **kwargs)`. kwargs: `overrides`, `presets`,
`parent`, `local`, `space` (`"screen"`|`"parent"`), `behind`, `alt_keys`, `config`,
`display_size`, `display_sizes`, plus initial values. Config (world): `alignX -0.5`,
`alignY 0.0`, `rotation 0.0`, `zoom 1.0`, `blur 0.0`, `bw False`, `flip 1.0`.
When parented, `local` holds the relative transform; `config` is composed along the
ancestor chain (`space="parent"` maps local align onto the parent's display box).
`get_config(key, index)` = shared config + layer override. Show zorder: `0`, or
`-1` if `behind=True` (background is `-100`).

### Actions
`PDAImage(**values)` · `PDAMove(alignX, alignY, zoom, duration)` ·
`PDABlur(blur, duration)` · `PDABw(bw, duration)` · `PDAFlip(flip, duration)` ·
`PDAShake(duration, max_distance)` · `PDAPause(duration, transition)` ·
`PDAPreset(preset, **overrides)`. Each runs via label `paperdoll_action_<key>`.
Move/flip/shake fan out to parented descendants.

### Presets
`register_preset(key, *actions)` · `register_temp_preset(key, *actions)` ·
`get_preset(key, paperdoll_obj=None)` ·
`get_preset_with_overrides(key, paperdoll_obj=None, **kwargs)` ·
`clear_temp_presets()` · `clear_presets()`. Built-ins:
`outside`, `close_body(_center/_right/_left)`, `upper_body(_center/_right/_left)`.
Object presets: `PaperdollPreset(key, *actions)` → temp `"{obj}:{key}"`; lookup
prefers scoped then bare (copy-on-expand).

### Character helper (`character.rpy`)
`person.register_paperdoll(*overrides, **kwargs)` (2 layers, `display_size=(600,1080)`,
`alt_keys=["level","mouth","state","char_var"]`, merges `paperdollOverrides` +
`paperdollPresets`) · `person.display(*actions)` ·
`person.clear_display()` · `PaperdollOverride(...)` · `PaperdollPreset(key, *actions)`.

### Related files
- `game/scripts/paperdoll.rpy` — manager, object, actions, presets, transforms, labels
- `game/scripts/character.rpy` — `register_paperdoll` / `display` / `clear_display`, `PaperdollOverride` / `PaperdollPreset`
- `game/scripts/images.rpy` — `refine_image_with_alternatives` / `find_available_images` (`<key>` + `$` resolution); `Image_Series` (background `image[step]` source)
- [Images](Images) — full path-resolution guide (PNG/WebP, mod prefixes, which helper to call)
- `game/scripts/event.rpy` — creates/unloads the manager around each event
- `game/scripts/debug.rpy` — `show_paperdoll_test`, the in-game editor
- `tools/paperdoll_viewer.py` — standalone desktop paperdoll viewer (out-of-game combination/preview; `Paperdoll Viewer.bat` launcher)
- `game/scripts/events/new_management.rpy` — worked examples (register → display → clear)
- [Selectors](Selectors) — how `<key>` values are produced and substituted into paths
