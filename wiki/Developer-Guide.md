# Developer & Modder Guide

Technical documentation for extending **Mind the School**. Everything here is
mod-capable: content is driven by keys, conditions, and effects, and mods register
through the same paths as the base game.

New to the project? Start with **[Modding — Quick Start](Modding)** — it walks you
from an empty folder to a working, enable-able mod, and points into the guides below.

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
