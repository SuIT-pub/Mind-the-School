> **Audience:** Developers and modders who add sound to a location, a map or a scene.
>
> **Scope:** The audio channels and mixers, location/map **ambience** (`Ambience`,
> `AmbienceStorage`, `register_building_ambience`, `register_map_ambience`), how events
> treat ambience, one-shot effects (`play_sound`), **music** (`MusicTrack`,
> `register_map_music`, `register_music_pool`, `play_music`, `stop_music`) and the
> player's sound settings. Scene sound (rhythm/voice layers) is planned — see
> [§9](#9-planned).
>
> **Status:** §1–§7 built 2026-10-20 (step 1), §8 music built 2026-10-21 (step 2);
> §9 is planned.

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
| `music` (Ren'Py default) | `music` | no — the playlist advances itself (§8) | map tracks, the bed under scenes, mood pools, the main menu |
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
        Ambience(audio.empty_room, volume = 0.6),                                   # fallback
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
- **Level every file to −27 LUFS integrated** (ITU-R BS.1770), true peak at or below
  −1 dBTP. All base ambience files sit there (±0.1 LU, 2026-10-20). −27 rather than
  louder because room tones with sharp transients (`forest-ambience`, `empty-room`)
  would clip above it, and future music needs room on top.
- `volume` then states **intent only**, never compensates a badly levelled file:

  | Tier | `volume` | In game | Used for |
  |---|---|---|---|
  | busy | `1.0` | −27 LUFS | chatter, an active gym, a full cafeteria |
  | outdoors | `0.8` | −29 LUFS | the courtyard at night |
  | map | `0.6` | −31 LUFS | map day/night: outdoors at 75 %, so the map stays calm |
  | quiet room | `0.6` | −31 LUFS | `empty_room`, an empty cafeteria |

  A new file that needs `volume = 0.1` to fit is a file that needs re-levelling.
- Licence: record the source and licence of every file in the journal credits. Several
  royalty-free libraries forbid adult or commercial use — check both.

---

## 7. Settings

The journal's **Speed & sound** page shows:

- **Ambience** — `Preference("mixer ambience volume")`
- **Effects** — `Preference("sound volume")`
- **Music** — `Preference("music volume")`
- **Voices** — `Preference("voice volume")`, once `config.has_voice` is on (step 4).
  Kept separate from everything else on purpose: plenty of players want the room and the
  music but the moaning low or off
- **Sound in background** — toggles `Preference("audio when unfocused")` and
  `Preference("audio when minimized")` together
- **Mute everything** — `Preference("all mute")`, which covers every mixer including
  `ambience`

---

## 8. Music

Music works by contrast: it means something when it starts because it is not
always there. The rules below keep it from becoming wallpaper.

| Where | What plays |
|---|---|
| Main menu | `register_menu_music(track)`, looped (`label before_main_menu`) |
| Map | the map's track **once** (at `MUSIC_MAP_VOLUME` = 0.75 → −22.5 LUFS) when a new daytime begins, then only ambience. Coming back within the same daytime: ambience only. A track that covers several daytimes in a row (noon → afternoon) starts once, not at every step |
| Building menus | whatever is playing keeps playing; they have no music of their own |
| Events | `begin_event` starts the **bed** pool unless it already plays; a scene changes mood with `play_music(pool)` or goes quiet with `stop_music()` |
| Journal | whatever is playing keeps playing; a replay's bed stops when it returns to the journal |

### Tracks

```python
MusicTrack(sound, priority=0, *conditions, loudness=None, end=None, volume=1.0)
```

- `loudness` — the file's integrated loudness in LUFS. Commercial and CC tracks are
  mastered anywhere from −10 to −17 LUFS; the track is turned down to
  `MUSIC_REFERENCE_LUFS` (−20) so all of them play equally loud. Measure it, don't
  guess: an unmeasured track plays at full file level and will jump out.
- `end` — stop at this second (Ren'Py's `<to …>`), e.g. to skip 8 s of trailing
  silence. Never cut or re-level the file itself: most tracks are CC BY-SA, and an
  edited file would be an adaptation. Converting to Ogg is a format change and fine.
- Conditions pick a map's track like ambience (honest in replays).

### Registering

```python
init 1 python:
    set_current_mod('base')

    register_map_music("school", MusicStorage(None,     # None: no music when nothing fits
        MusicTrack("audio/music/look-on-the-bright-side.ogg", 1, TimeCondition(daytime = "1,2"), loudness = -12.1),
        MusicTrack("audio/music/coffee-jelly.ogg", 1, TimeCondition(daytime = "3,4,5"), loudness = -11.0),
    ))

    register_music_pool("bed",
        MusicTrack("audio/music/brain-fog.ogg", loudness = -14.5, end = 135.3),
        MusicTrack("audio/music/im-lost-but-thats-ok.ogg", loudness = -14.2, end = 156.3),
    )
```

The base game's music lives in `game/scripts/music.rpy`. Pools today: **`bed`**
(under every scene, at `MUSIC_BED_VOLUME` = 0.5 → −26 LUFS) and **`cozy`** (tea,
blanket, a quiet evening). A mod adds to a pool with `add_to_music_pool("bed", ...)`.

### In a scene

```python
$ begin_event(**kwargs)          # the bed starts (or keeps playing)
...
$ play_music("cozy")             # fades over to the cozy pool
...
$ stop_music(fadeout = 3.0)      # deliberate silence: only the room tone is left
```

Silence is the strongest tool here — take the music away when a character says
something unexpected or right before a decision. A silence survives decision
re-entry; a new fragment starts the bed again.

### How the playlist works

Ren'Py's own looping gives every queued file the volume of the last one, so pools
are advanced by `_music_tick` (`config.periodic_callbacks`, main thread): one track
at a time, each with its own `relative_volume`, in a shuffled order that never
repeats a track back to back. `music_state` (saved) holds the pool, the order and
the last map daytime; after a load the next track starts at once.

### Files and credits

`game/audio/music/*.ogg`, converted from the downloaded MP3s (masters outside the
repo in `M:\MTS Project\audio-masters\music`). Every track is listed with title,
source and licence in `game/audio/music/CREDITS.txt`; the journal's credits page
links the artist. Only CC0, CC BY or CC BY-SA — never NC (the game is commercial)
or ND.

---

## 9. Planned

- **UI effects** (step 3): journal page turns, collectible pickup, decision clicks.
- **Scene sound** (step 4): `SceneSound(rhythm=..., voice=...)` on `show_video` steps,
  voice profiles per character, on the `scene_*` channels and the `voice` mixer (§2).

---

## 10. API

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

**Music** — `MusicTrack(...)` · `MusicStorage(fallback, *tracks)` ·
`register_map_music(key, storage)` · `register_music_pool(key, *tracks)` ·
`add_to_music_pool(key, *tracks)` · `register_menu_music(track)` ·
`play_music(pool, volume=None)` · `stop_music(fadeout=MUSIC_FADE)` ·
`play_map_music(key)` (map_entry) · `start_event_music(**kwargs)` (begin_event) ·
constants `MUSIC_REFERENCE_LUFS = -20` · `MUSIC_MAP_VOLUME = 0.75` · `MUSIC_BED_VOLUME = 0.5` · `MUSIC_FADE = 2.0`.

**Mod overview** — a registration shows under *Ambience*; registering a key another
mod owns lists it under *Places with replaced ambience*, `add_ambience` on someone
else's place under *Existing places with new ambience*.

### Related files
- `game/scripts/audio.rpy` — channels, classes, registry, playback, music playlist
- `game/scripts/music.rpy` — the base game's map tracks, pools and menu music
- `game/audio/music/CREDITS.txt` — titles, sources and licences of every track
- `game/scripts/values.rpy` — `audio.` names
- `game/scripts/event.rpy` — `begin_event` / `end_event` ducking
- `game/scripts/overview.rpy` — `map_entry`, `label building`
- `game/scripts/journal/journal_menu.rpy` — sliders
