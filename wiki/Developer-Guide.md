# Developer & Modder Guide

Technical documentation for extending **Mind the School**. Everything here is
mod-capable: content is driven by keys, conditions, and effects, and mods register
through the same paths as the base game.

New to the project? Start with **[Modding — Quick Start](Modding)** — it walks you
from an empty folder to a working, enable-able mod, and points into the guides below.

## Getting the game assets

The Git repository contains **source code only**. Large game assets (~21 GB, mostly
under `game/images/`) are hosted separately on Cloudflare R2 and are **not** included
in Git. You need them to run the game or test mods against real art.

### Where to run the script

Run the commands from the **repository root** — the folder that contains both `game/`
and `tools/` (for example `Mind-the-School/`). Do **not** run them from inside
`game/` or `tools/`.

```bash
cd Mind-the-School          # repository root (has game/ and tools/)
pip install -r requirements.txt
python tools/download_assets.py
```

On Windows you can also double-click `tools/Download Assets.bat` (the batch file
switches into `tools/` itself; you do not need to open a terminal first).

The script installs images into `game/images/` and records the version in
`game/.asset-version`. No Cloudflare account or credentials are required. It
compares your local install with the remote version and only downloads when an
update is available. Run the same command again from the repository root whenever
a new asset version is published.

### Install modes

By default the downloader **merges** into `game/images/` (and `game/videos/` if
present). Local-only files are kept. Choose the behaviour with `--mode`:

| Mode | Flag | Behaviour |
|------|------|-----------|
| **Keep existing** (default) | `--mode keep-existing` | Local files win. Cloud files are added only when the path does not exist yet. Example: local `a`,`c` + cloud `a`,`b` → `a`,`b`,`c` (cloud `a` discarded). |
| **Overwrite existing** | `--mode overwrite-existing` | Cloud files overwrite matching local paths. Local-only files remain. Example: local `a`,`c` + cloud `a`,`b` → `a` (from cloud),`b`,`c`. |
| **Folder swap** | `--mode folder-swap` | Replace the whole folder with the archive contents (old behaviour). Local-only files are removed. Example: local `a`,`c` + cloud `a`,`b` → `a`,`b`. |

```bash
python tools/download_assets.py                              # keep-existing
python tools/download_assets.py --mode overwrite-existing
python tools/download_assets.py --mode folder-swap
```

On Windows, pass the flag through the batch file, e.g.
`tools\Download Assets.bat --mode overwrite-existing`.

### What the downloader does on failure

Expected problems print a short `ERROR:` message (no stack trace) and exit.

**Download resume:** If the transfer is interrupted (network drop, Ctrl+C, or a
hard kill that leaves `assets.zip.part` behind), run the same command again from
the repository root. The script continues with an HTTP Range request from the
bytes already on disk. Progress shows `Resuming assets.zip` with speed/ETA for
the remaining data. After the file is complete it still verifies the SHA-256
checksum before installing.

| Situation | Behaviour |
|-----------|-----------|
| No internet / connection dropped | Clear error; **`assets.zip.part` is kept** — run again to resume |
| Download cancelled (Ctrl+C) | **Partial download kept** — run again to resume |
| Hard kill / power loss | Leftover `.part` is reused on the next run (same as resume) |
| `version.json` or `assets.zip` missing (HTTP 404) | Clear error; no install |
| Access denied (HTTP 403) | Clear error (bucket public access / blocked request) |
| Not enough disk space | Clear error; **partial download kept** — free space, then resume |
| Server rejects resume (HTTP 416) | Partial file removed; next run starts clean |
| SHA-256 checksum mismatch | Archive is **not** installed; bad file removed; next run downloads fresh |
| Corrupt / invalid ZIP | Extraction aborted; temp files removed |
| Zip Slip / unsafe paths in the archive | Extraction aborted; temp files removed |
| Failure while swapping into `game/` (`folder-swap`) | Rollback to the previous `game/images/` when possible |
| Failure mid-merge (`keep-existing` / `overwrite-existing`) | Partial new files may remain; re-run with the same `--mode` to finish |

Existing installed assets under `game/images/` are only modified **after** a successful
download, checksum check, and extraction into a temp folder. `game/.asset-version` is
written only when installation finishes successfully.

Temporary paths the script may create:

- `assets.zip.part` — in-progress / resumable download (repository root)
- `assets.zip` — verified archive before install (repository root)
- `.temp_assets/` — extraction staging area (repository root)
- `game/images.old/` — brief backup during **folder-swap** only

### Cleaning leftovers manually

To discard a partial download and free disk space (instead of resuming), or to
clear leftovers after a failed install:

```bash
cd Mind-the-School
python tools/download_assets.py --cleanup
```

`--cleanup` deletes the temporary paths listed above. It does **not** remove an
already installed `game/images/` tree or `game/.asset-version`. After cleaning, run
`python tools/download_assets.py` again for a full download from the start.

## Content guides

- **[Building Situations](Building-Situations)** — a *Situation* is an ongoing
  problem or development the player influences through a bidirectional progress bar
  and narrative hints, ending in a positive or negative resolution. This is the
  system that replaced quests. Covers bars, thresholds, passives/measures, teasers,
  event pools, resolutions, effects, hot-reload, and the full mod workflow.
- **[Building Unlockables](Building-Unlockables)** — an *Unlockable* (rule, club, or
  building unlock) is a Situation with a PTA-vote layer pre-built on top. Covers the
  injected vote/cancel/persuade measures, faction bars, money escrow, upgrade
  chains, unlock effects, and pictograms. **Read the Situations guide first** — an
  Unlockable *is* a Situation.

## System guides

The building blocks the content systems are made of:

- **[Events](Events)** — the scenes players reach by exploring; location pools,
  priorities, scene labels, and how everything below plugs in.
- **[Conditions](Conditions)** — the universal gating primitive (when something is
  available), with the `AND`/`OR`/`NOT` combinators and the full catalog.
- **[Selectors](Selectors)** — dynamic values rolled at runtime into event kwargs
  (the acting character, a variant, a stat reading).
- **[Effects](Effects)** — the "what happens" actions (money, stats, unlocks,
  building open/close) and their apply/revert semantics.
- **[Modifiers](Modifiers)** — how stat changes are scaled and how recurring drift
  works; the engine behind stat/bar modifier effects.
- **[Options](Options)** — the shared trailing flags that fine-tune conditions,
  effects, selectors and events.
- **[Paperdoll](Paperdoll)** — the layered sprite compositor that puts a live,
  animatable character (body + head, changing pose/mood/mouth) on screen over a
  blurred background; general enough to display any stacked imagery.
- **[Images](Images)** — how a path string becomes a file: patterns, placeholders,
  `$` fallbacks, PNG/WebP, mod prefixes, and which helper to call from events,
  screens and classes.

## How the pieces fit together

- **Situations** are the core player-guidance system (the bar + hints).
- **Unlockables** build on Situations to gate permanent unlocks behind a PTA vote.
- **Pictograms** are descriptive preview marks on bars/unlockables.
- **Events** are injected into building pools while a Situation is active.

All four are registered inside the start/after-load *lifecycle wave*; mods queue
their loader with `register_start_method(...)`. Image paths (thumbnails, teaser
images, pictogram icons) are auto-redirected to the active mod's folder.

## About these pages

All wiki pages are maintained in the **`wiki/` folder of the main repository** and
published with a sync script. Edit them there — not directly on the wiki — and see
the repo's `wiki/README.md` for the workflow.
