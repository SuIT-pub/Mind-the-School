> **Audience:** Developers who want to add content to *Mind the School* as a mod —
> events, situations, unlockables, pictograms, assets — without touching the base
> game. This is a **quick start**: follow it top to bottom and you end up with a
> working, enable-able mod.
>
> **Scope:** How a mod is structured, registered, activated, and how it hooks its
> content into the game. The *content* systems have their own guides —
> [Events](Events), [Building Situations](Building-Situations),
> [Building Unlockables](Building-Unlockables) — this page is the wrapper around them.

---

## Requirements

Set up a working copy of the game **before** you start modding:

1. **Ren'Py SDK** — install [Ren'Py 8.1.3](https://www.renpy.org/release/8.1.3) (the version the
   project is built against; a newer 8.1.x release may work, but use 8.1.3 if you hit
   compatibility issues).
2. **Game source** — clone from GitHub:
   ```bash
   git clone https://github.com/SuIT-pub/Mind-the-School.git
   cd Mind-the-School
   ```
   **`master`** always tracks the **latest released** version. For the current
   **in-development** tree, check out the version branch — at the moment
   `MTS-285/Version-0.2.2` (each upcoming release gets its own branch):
   ```bash
   git checkout MTS-285/Version-0.2.2
   ```
   Mod against `master` if you want to match what players have from the last release;
   use the version branch to test against upcoming content.
3. **Python 3.9+** — needed for the asset download tools (`pip install -r requirements.txt`).
4. **Game assets** — the repository contains source code only (~21 GB of images are hosted
   separately). From the **repository root** (the folder with `game/` and `tools/`, not
   from inside `game/`), download and install them:
   ```bash
   cd Mind-the-School          # repository root
   pip install -r requirements.txt
   python tools/download_assets.py
   ```
   Default install mode is **keep-existing** (local files stay; cloud only adds
   missing paths). See [Install modes](Developer-Guide#install-modes) for
   `overwrite-existing` and `folder-swap`.
   On Windows you can double-click `tools/Download Assets.bat` instead. See
   [Getting the game assets](Developer-Guide#getting-the-game-assets) for details
   (where to run the script, failure handling, resume, and `--cleanup`).
5. **Launch in Ren'Py** — add the cloned project in the Ren'Py launcher and run the game
   once to confirm scripts and assets load.

---

## Quick start (the whole path)

Complete the [requirements](#requirements) above, then:

1. **Make a folder** `game/mods/MyMod/` and a file `game/mods/MyMod/my_mod.rpy`.
   Ren'Py auto-loads every `.rpy` under `game/`, mods included — no manifest needed.
2. **Register the mod** very early so it appears in the in-game mod list:
   ```python
   init -97 python:
       register_mod("mymod_key", "My Mod", "1", "MyMod",
           description="Adds a small cafeteria scene.", author="YourName")
   ```
3. **Claim the mod context and add content** after the base pools exist:
   ```python
   init 1 python:
       set_current_mod('mymod_key')                 # redirects assets + gates registration
       my_event = Event(3, "mymod_scene", TimeCondition(daytime="d"),
           Pattern("main", "images/mymod_scene <step>.webp"))
       cafeteria_events["order_food"].add_event(my_event)
   ```
4. **Write the scene label** (`label mymod_scene(**kwargs): …`) — see [Events](Events).
5. **Put assets** under `game/mods/MyMod/images/…` (referenced as plain `images/…`).
6. **Enable & test:** launch → Journal → mod list → toggle **My Mod** on → **restart**
   → your content is now live.

The [complete example](#a-complete-mod) at the bottom is a copy-paste starting point.

---

## Contents

0. [Requirements](#requirements)
1. [How a mod plugs in](#1-how-a-mod-plugs-in)
2. [Folder layout](#2-folder-layout)
3. [Step 1 — register the mod](#3-step-1--register-the-mod)
4. [Step 2 — claim the mod context](#4-step-2--claim-the-mod-context)
5. [Step 3 — add content](#5-step-3--add-content)
6. [Step 4 — assets](#6-step-4--assets)
7. [Step 5 — enable & test](#7-step-5--enable--test)
8. [Why activation needs a restart](#8-why-activation-needs-a-restart)
9. [A complete mod](#9-a-complete-mod)
10. [Distribution](#10-distribution)
11. [Conventions & gotchas](#11-conventions--gotchas)
12. [Reference](#12-reference)

---

## 1. How a mod plugs in

A mod is just `.rpy` files under `game/mods/<YourMod>/` that Ren'Py loads like any
other script. Nothing is special about the code — a mod uses the **same** APIs as the
base game (`Event`, `Situation`, `register_situations`, …). Two thin wrappers make it
a *mod* rather than base content:

- **`register_mod(...)`** — announces the mod so it shows up in the player's mod list
  and gets a folder path for its assets.
- **`set_current_mod('key')`** — marks the following registrations as belonging to your
  mod. This does two things at once: it **redirects asset paths** into your mod folder,
  and it **gates registration on the mod being active** — `EventStorage.add_event`,
  an event's self-registration, `register_start_method`, and every content register
  function (`register_situations`, `register_unlockables`, `load_person`,
  `add_pictogram`, `load_item`, `register_buildings`) all quietly no-op while your mod
  is disabled. So you never write "if enabled" checks: claim the context and register
  normally.

Coupling to the base game is only through **keys, conditions and progress**, so your
mod can gate on base state and be gated by it, and add to base event pools or
situations without editing them.

---

## 2. Folder layout

```
game/mods/MyMod/
    my_mod.rpy              # your code (any name; multiple files allowed)
    images/
        mymod_scene 0.webp  # assets, referenced as "images/mymod_scene 0.webp"
        ...
```

`game/mods/*` is git-ignored in the base repo (except the bundled `CheatMod`), so your
mod lives self-contained in its own folder and ships separately (see §10).

---

## 3. Step 1 — register the mod

Call `register_mod` at a **very early init** (before content and before the mod-list
UI builds) — the bundled `CheatMod` uses `init -97`:

```python
init -97 python:
    register_mod(
        "mymod_key",      # unique key — your mod's identity everywhere (namespace it)
        "My Mod",         # display name shown in the mod list
        "1",              # version string
        "MyMod",          # folder name under mods/ (→ assets resolve to mods/MyMod/)
        description="Adds a small cafeteria scene.",
        author="YourName",
        # translations=["translations.csv"],   # optional
    )
```

`register_mod(key, name, version, path, **meta)` writes the mod into
`persistent.modList`. A mod is registered **inactive by default**, and **bumping the
`version` string resets it to inactive** (players re-enable after an update).

---

## 4. Step 2 — claim the mod context

At the top of every `init` block (and every loader label) that registers content, call:

```python
set_current_mod('mymod_key')
```

- **Asset redirection:** image paths captured after this (event `Pattern`s, situation
  `thumbnail`s, teaser `image`s, `Picto` icons, item images) are prefixed with your
  mod's path (`mods/MyMod/`). Write **plain paths relative to your mod root** —
  `Pattern("main", "images/foo <step>.webp")` — never `mods/MyMod/...`.
- **Active-state gating:** registration functions check `is_mod_active('mymod_key')`
  and no-op while your mod is off. That is why disabled mods inject nothing.

Base scripts do the same with `set_current_mod('base')`; you just use your own key.

---

## 5. Step 3 — add content

There are **two** registration paths, and which one you use depends only on whether
it's an event:

- **Events** register **at init** (build the `Event`, `add_event` into a pool).
- **Everything else** — situations, unlockables, characters, pictograms, items,
  buildings — registers through a **`register_start_method` loader label**.

Both auto-gate on the active mod, so you never write "if enabled" checks.

### Events (the init path)

Build after the base pools exist (`init 1` works — base buildings build at `init -1`),
then add to a pool:

```python
init 1 python:
    set_current_mod('mymod_key')
    my_event = Event(3, "mymod_scene",
        TimeCondition(daytime="d"),
        Pattern("main", "images/mymod_scene <step>.webp"))
    cafeteria_events["order_food"].add_event(my_event)     # no-op if the mod is off
```

…and write the scene label (`label mymod_scene(**kwargs): …`) — full scene grammar in
[Events](Events).

### Everything else (the `register_start_method` path)

Queue **one loader label** into the start/after-load wave, and register whatever you
like inside it after claiming the context. This one mechanism covers situations,
unlockables, characters, pictograms, items and buildings:

```python
init python:
    register_start_method("load_mymod")        # gated; runs in the start/after-load wave

label load_mymod:
    $ set_current_mod('mymod_key')             # claim context first (redirect + gating)

    # situations / unlockables
    $ register_situations( Situation("mymod_thing", …) )
    $ register_unlockables( Unlockable("rule", "mymod_rule", …) )

    # characters / persons
    $ load_person("mymod_class", Person("mymod_girl", "Mira", "Sato", school_char, […]))

    # pictograms
    $ load_pictograms( Pictogram("mymod_icon", "Label", "Tooltip", "images/icons/mymod.webp") )

    # items
    $ load_item( ItemData("mymod_item", "Name", "Desc", "images/mymod_item.png") )

    # map buildings
    $ register_buildings( Building("mymod_building", "images/mymod_building.webp", …) )
    return
```

Why a start-method label rather than a bare `init` block: it runs **inside the
lifecycle wave** (after the base loaders), so reloads, the lifecycle registry, and
orphan revival all work — see [Building Situations](Building-Situations) §8 and
[Building Unlockables](Building-Unlockables) §13. Every `register_*` / `load_*`
function above also self-gates on the active mod, so a disabled mod registers
nothing even if its label somehow runs.

### Extending base content

You can also add **teasers/pictograms to base situations**, **events to base pools**,
and gate base events on your progress — all without editing base files. Prefix your
keys (`mymod_…`) so they never collide.

---

## 6. Step 4 — assets

Put images under your mod folder and reference them by the **plain path** you'd write
relative to the mod root:

```
game/mods/MyMod/images/mymod_scene 0.webp
game/mods/MyMod/images/mymod_scene 1.webp
```

```python
Pattern("main", "images/mymod_scene <step>.webp")   # → mods/MyMod/images/mymod_scene <step>.webp
```

The redirect is baked in at construction (while `set_current_mod` points at your mod),
so it only works if the context is set **before** the object is built. Videos
(`Movie` images), thumbnails, teaser images and pictogram icons follow the same rule.

---

## 7. Step 5 — enable & test

1. Launch the game.
2. Open the **Journal → mod list** and toggle your mod **on**.
3. **Restart the game** (see §8 — content registers at startup based on the saved
   active state).
4. Trigger it — e.g. go to the cafeteria, pick the action your event is in, at the
   right time. Watch the log (category `event`) for a missing-label or bad-key error.

---

## 8. Why activation needs a restart

Content is registered during **init / the start wave**, and `set_current_mod` gates
that registration on `is_mod_active(...)`, which reads the **saved** `persistent.modList`
active flag. So the sequence is:

- First launch → your mod is registered but **inactive** → its `add_event` /
  `register_start_method` calls no-op → no content.
- You enable it in the mod list → the active flag is saved to `persistent`.
- **Restart** → init runs again, now `is_mod_active` is `True` → your content
  registers.

Toggling a mod therefore takes effect on the next start, not immediately — tell your
players to restart after enabling, and after a version bump (which re-disables it).

---

## 9. A complete mod

Drop this in `game/mods/SnackMod/snack_mod.rpy`, add the two images, enable **Snack
Mod**, restart, and visit the cafeteria's *order food* action at daytime `"d"`.

```python
## game/mods/SnackMod/snack_mod.rpy

# 1) Register the mod (very early).
init -97 python:
    register_mod(
        "snackmod_suit",                 # unique key
        "Snack Mod",                     # display name
        "1",                             # version
        "SnackMod",                      # folder under mods/  → assets at mods/SnackMod/
        description="Adds a small chat event to the cafeteria.",
        author="YourName",
    )

# 2) Claim the context and register content (after base pools exist).
init 1 python:
    set_current_mod('snackmod_suit')

    snackmod_chat = Event(3, "snackmod_snack_chat",
        TimeCondition(daytime="d"),
        RandomListSelector("snack", "muffin", "apple", "bento"),
        Pattern("main", "images/snack_chat <snack> <step>.webp"),
        thumbnail="images/snack_chat muffin 0.webp")

    cafeteria_events["order_food"].add_event(snackmod_chat)   # auto-gated on active state

# 3) The scene label.
label snackmod_snack_chat(**kwargs):
    $ begin_event(**kwargs)
    $ snack = get_value("snack", **kwargs)
    $ miwa  = Person["miwa_igarashi"]
    $ image = convert_pattern("main", **kwargs)
    $ image.show(0)
    miwa.say "Ooh, a [snack]! My favourite."
    $ image.show(1)
    miwa.think "...maybe I'll grab two."
    call change_stats_with_modifier(happiness=SMALL) from _snackmod_1
    $ end_event("new_daytime", **kwargs)
```

Assets (referenced as `images/…`, resolved to `mods/SnackMod/images/…`):

```
game/mods/SnackMod/images/snack_chat muffin 0.webp
game/mods/SnackMod/images/snack_chat muffin 1.webp
game/mods/SnackMod/images/snack_chat apple 0.webp
…
```

That's a complete, self-contained mod: one registered mod, one ambient cafeteria event
with a rolled `snack` value driving both the image and the dialogue, its own art, and
a small happiness reward — all gated on the mod being enabled.

---

## 10. Distribution

A mod is its `game/mods/<YourMod>/` folder. Ship that folder; players drop it into
their own `game/mods/`. Because `game/mods/*` is git-ignored in the base repo, your mod
stays independent of the base game's version control. Keep everything (code + assets)
under your one folder so it's a single unit to install and remove. Bump the `version`
in `register_mod` on updates (players re-enable afterward).

---

## 11. Conventions & gotchas

- **Namespace everything.** Prefix your mod key, event/situation/label keys and asset
  folders (`mymod_…`) so nothing collides with base or other mods.
- **`set_current_mod` first, always.** Every content `init` block and loader label must
  set it before building anything — otherwise assets don't redirect and registration
  may attach to the wrong (or no) mod.
- **Definition name = label name.** An `Event("mymod_scene", …)` needs a matching
  `label mymod_scene`. Missing/mismatched labels are logged under category `event`.
- **Register early, build late.** `register_mod` at `init -97`; events at `init 1`
  (after base pools); **everything else** (situations, unlockables, characters,
  pictograms, items, buildings) via a `register_start_method` loader label.
- **Restart after enabling** (and after a version bump) — see §8.
- **Don't edit base files.** Add to base pools / situations through keys and conditions
  instead; that keeps your mod portable and update-safe.
- **Avoid the deprecated temp-event classes** (`TempEventStorage` & friends) — they are
  highly unstable.

---

## 12. Reference

### Mod API
`register_mod(key, name, version, path, description=…, author=…, translations=[…])` ·
`set_current_mod(key)` · `is_mod_active(key)` · `get_mod_path(key)` /
`get_current_mod_path()` · `register_start_method(label)`.

### Init timing
`register_mod` → `init -97` (early) · **events** → `init 1` (after base pools, via
`add_event`) · **everything else** (situations, unlockables, characters, pictograms,
items, buildings) → a `register_start_method` loader label (lifecycle wave).

### Content register functions (all mod-gated)
`register_situations(...)` · `register_unlockables(...)` · `load_person(key, Person)` ·
`load_pictograms(...)` / `add_pictogram(...)` · `load_item(ItemData)` ·
`register_buildings(...)`. Events use `EventStorage.add_event(...)` at init instead.

### Related pages
- [Events](Events) — scene definitions & labels, `Pattern`s, decisions, characters
- [Images](Images) — path resolution, PNG/WebP, how `images/…` becomes `mods/MyMod/images/…`
- [Building Situations](Building-Situations) / [Building Unlockables](Building-Unlockables) — the `register_start_method` loader pattern
- [Selectors](Selectors) · [Conditions](Conditions) · [Effects](Effects) · [Modifiers](Modifiers) · [Options](Options)

### Related files
- `game/mods/CheatMod/cheat_mod.rpy` — the bundled reference mod
- `game/scripts/helper.rpy` — `register_mod`, `set_current_mod`, `is_mod_active`, `get_mod_path`
