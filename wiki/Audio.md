> **Audience:** Developers and modders who add sound to a location, a map or a scene.
>
> **Scope:** The audio channels and mixers, location/map **ambience** (`Ambience`,
> `AmbienceStorage`, `register_building_ambience`, `register_map_ambience`), how events
> treat ambience, one-shot effects (`play_sound`) and the player's sound settings.
> Music and scene sound (rhythm/voice layers) are planned and not built yet —
> see [§8](#8-planned).
>
> **Status:** §1–§7 built (2026-10-20, step 1 of the sound overhaul); §8 is planned.

---

## 1. Why this exists

Until now every sound in the game ran through one call, `play_sound(...)`, on Ren'Py's
`sound` channel, picked by a hand-written `if time.get_daytime() in [...]` at the top of
each building label. That had three costs:

- **One channel, one sound.** The `sound` channel plays one file at a time, so any
  door creak or click would have cut the room tone dead. Layering was impossible.
- **Scenes were silent.** `begin_event` stopped the channel, so the moment a scene
  started — the part of the game players actually look at — the campus went quiet.
- **It didn't scale.** Every building repeated the daytime ladder, mods couldn't add or
  override a location's sound, and a map always played forest/night
  ([Maps §10](Maps#10-known-gaps)).

The fix mirrors what `BGStorage` already does for backgrounds: a location declares its
ambience as a list of candidates gated by [Conditions](Conditions); the framework picks
the highest-priority one that fits and plays it.

---

## 2. Channels and mixers

Each mixer is one volume slider in the journal's settings page.

| Channel | Mixer | Loops | Used for |
|---|---|---|---|
| `ambience_a`, `ambience_b` | `ambience` | yes | room tone, chatter, weather. Two channels so a change of location **crossfades** instead of dipping to silence; code never addresses them directly |
| `sound` (Ren'Py default) | `sfx` ("Effects") | no | one-shots: UI, doors, props — `play_sound` |
| `music` (Ren'Py default) | `music` | yes | *planned, step 2* — `config.has_music` stays `False` until then |
| `scene_voice` (+ more scene channels) | `voice` ("Voices") | yes | *planned, step 4* — moans, breathing, cries in scenes. `config.has_voice` stays `False` until the first scene sound ships |

**Why scene voices don't use Ren'Py's `voice` channel:** that channel stops on every new
dialogue line (it is built for voiced dialogue). A moan loop under a scene has to run
across many lines, so it gets its own channels that only share the `voice` **mixer** —
one slider, separate playback.

Register channels only in `init` (Ren'Py refuses afterwards). A new mixer name creates
the mixer; its default volume is `1.0`.

---

## 3. Declaring ambience

### `Ambience(sound, priority, *conditions, volume=1.0)`

One candidate sound. Shaped like `BGImage`:

- `sound` — a file under `game/` (`"audio/empty-room.ogg"`) or an `audio.` name
  (`audio.empty_room`). Inside a mod, a relative path resolves into the mod's folder.
- `priority` — the highest usable priority wins; ties keep declaration order.
- `*conditions` — any [Conditions](Conditions); all must pass. Evaluated with no event
  kwargs, so use conditions that read global state: `TimeCondition`,
  `LevelCondition(..., char_obj="school")`, `FlagCondition`, situation conditions.
  Unlike event gates they are **checked for real during a replay** (`check_condition`,
  not `is_fulfilled`, which passes everything in replay) — otherwise every replay
  would hear the top-priority candidate. `Optional` conditions still pass.
- `volume` — `0.0`–`1.0`, multiplied with the player's ambience slider.

### `AmbienceStorage(fallback, *ambiences)`

`fallback` is an `Ambience`, or `None` for silence when nothing matches.
`add_ambience(*ambience)` appends candidates (mod-gated, like `BGStorage.add_image`).

### Registering

Register in an `init 1 python:` block (or later): the `audio.` names are `define`s,
which run at init 0, so an `init -1` block would not see them yet.

```python
init 1 python:
    set_current_mod('base')

    register_building_ambience("courtyard", AmbienceStorage(
        Ambience(audio.empty_room, volume = 0.5),                                   # fallback
        Ambience(audio.muffled_chatter, 1, TimeCondition(daytime = "3,6")),
        Ambience(audio.night_ambience, 1, TimeCondition(daytime = 7), volume = 0.8),
    ))

    register_map_ambience("school", AmbienceStorage(
        Ambience(audio.forest_ambience, volume = 0.8),
        Ambience(audio.night_ambience, 1, TimeCondition(daytime = 7), volume = 0.8),
    ))
```

The first argument of `AmbienceStorage` is always the fallback; its priority is
irrelevant, so leave it out.

A mod adds to a base location without replacing it:

```python
get_building_ambience("dormitory").add_ambience(
    Ambience("audio/dorm_party.ogg", 5, FlagCondition("dorm_party")))
```

**Level-aware sound** is just a condition. The dorm at level 1 is footsteps and a
distant hairdryer; from level 6 the same hallway carries what the school has become:

```python
Ambience("audio/dorm_late.ogg", 2, LevelCondition("6+", char_obj="school"), TimeCondition(daytime=7))
```

The registry is a plain `init` dictionary like `map_manager`, **not pickled into
saves** — changing a location's ambience in code takes effect in old saves.

---

## 4. When ambience plays

| Moment | What happens |
|---|---|
| `label map_entry` | the current map's ambience resolves and plays |
| `label building(name)` | before the building label runs, that building's ambience resolves and plays. Building labels no longer call `play_sound` themselves. A building **without** a registration plays its map's ambience (the beach under the forest) and the map becomes the current location |
| `begin_event` | ambience **ducks** to `AMBIENCE_EVENT_VOLUME` (0.35) over one second. The `sound` channel still stops, so an effect from the location never bleeds into the scene |
| `end_event` | ducking ends and the location's ambience **re-resolves** — if the scene changed the school level or set a flag, the room now sounds different |
| replay from the journal | the event's location ambience plays, ducked; it stops when the replay returns to the journal |

Playing the same file that is already playing never restarts it; only the volume glides
to the new value. A different file crossfades over `AMBIENCE_FADE` (1.5 s).

### Overriding inside a scene

```python
$ play_ambience(audio.night_ambience, volume=0.6)   # replaces the location's sound until end_event
$ stop_ambience(fadeout=2.0)                         # silence for a tense beat
```

An override plays **un-ducked** — the scene asked for it on purpose.

---

## 5. One-shot effects

`play_sound(sound, loop=False, volume=1.0, fadein=1.0)` keeps its signature and stays the
call for effects. Using it with `loop=True` for room tone still works but is
**deprecated**: it sits on the effects channel, gets cut by the next effect, and stops
when a scene starts.

---

## 6. Files

- **Format: `.ogg` (Vorbis).** MP3 encoders pad the start and end with silence, which
  becomes an audible gap every time a loop wraps. The seven existing ambience files move
  from `.mp3` to `.ogg`; the `audio.` names in `values.rpy` stay the same.
  Old saves still name the `.mp3` files on their channels: `config.audio_filename_callback`
  (`_ambience_mp3_to_ogg`) swaps a missing `.mp3` for its `.ogg`, and an after-load
  callback moves a pre-0.2.2 room-tone loop off the effects channel onto the ambience
  channels, so it doesn't play twice.
- Loops must be cut on a zero crossing at both ends. Test a new loop by letting it wrap
  three times with headphones on.
- Keep ambience quiet in the file itself (around −20 LUFS); the slider is for the
  player's taste, not for fixing a hot file.
- Licence: record the source and licence of every file in the journal credits. Several
  royalty-free libraries forbid adult or commercial use — check both.

---

## 7. Settings

The journal's **Speed & sound** page shows:

- **Ambience** — `Preference("mixer ambience volume")`
- **Effects** — `Preference("sound volume")`
- **Music** — once `config.has_music` is on (step 2)
- **Voices** — `Preference("voice volume")`, once `config.has_voice` is on (step 4).
  Kept separate from everything else on purpose: plenty of players want the room and the
  music but the moaning low or off
- **Sound in background** — toggles `Preference("audio when unfocused")` and
  `Preference("audio when minimized")` together
- **Mute everything** — `Preference("all mute")`, which covers every mixer including
  `ambience`

---

## 8. Planned

- **Music** (step 2): mood loops (`music="tender"` on an event), `config.has_music = True`.
- **UI effects** (step 3): journal page turns, collectible pickup, decision clicks.
- **Scene sound** (step 4): `SceneSound(rhythm=..., voice=...)` on `show_video` steps,
  voice profiles per character, on the `scene_*` channels and the `voice` mixer (§2).

---

## 9. API

**Classes** — `Ambience(sound, priority, *conditions, volume=1.0)` ·
`AmbienceStorage(fallback, *ambiences)` with `add_ambience(*ambience)`,
`resolve()` → `Ambience | None`.

**Registry** — `register_building_ambience(key, storage)` ·
`register_map_ambience(key, storage)` · `get_building_ambience(key)` ·
`get_map_ambience(key)`.

**Playback** — `play_location_ambience(kind, key, ducked=False)` · `play_ambience(sound, volume=1.0)` ·
`stop_ambience(fadeout=AMBIENCE_FADE)` · `duck_ambience()` / `unduck_ambience()` ·
`restore_location_ambience()`.

**Constants** — `AMBIENCE_EVENT_VOLUME = 0.35` · `AMBIENCE_FADE = 1.5` ·
`AMBIENCE_CHANNELS = ("ambience_a", "ambience_b")`.

**State** — `default ambience_state` (saved): the active channel, the playing sound and
its volume, whether it is ducked, and the current location `(kind, key)`.

**Mod overview** — a registration shows under *Ambience*; registering a key another
mod owns lists it under *Places with replaced ambience*, `add_ambience` on someone
else's place under *Existing places with new ambience*.

### Related files
- `game/scripts/audio.rpy` — channels, classes, registry, playback *(new)*
- `game/scripts/values.rpy` — `audio.` names
- `game/scripts/event.rpy` — `begin_event` / `end_event` ducking
- `game/scripts/overview.rpy` — `map_entry`, `label building`
- `game/scripts/journal/journal_menu.rpy` — sliders
