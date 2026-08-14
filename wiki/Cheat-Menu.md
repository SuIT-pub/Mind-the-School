The Cheat Menu is a built‑in developer/testing console that lives inside the
in‑game Journal. It lets you jump events, activate situations, force unlockables,
hand yourself items, edit stats and time, and inspect the save. It is equally
useful for players who want to experiment and for developers testing content — so
it sits in its own section, between the player and developer guides.

> ⚠️ **Read the [Dangers](#-dangers--read-this-first) section before using it.**
> Cheats write directly to your live save. Used carelessly they can desync or
> soft‑lock a playthrough. **Keep a separate backup save.**

## Enabling the Cheat Menu

The menu is provided by the **CheatMod**. Once the CheatMod is active, on the next
load its start method sets `cheat_mode = True`, and:

- a **Cheats** button appears in the Journal (bottom‑right), and
- pressing **`8`** in the Journal opens the Cheats page directly.

If you don't see the button, the CheatMod isn't active. Activating/deactivating
mods is part of the mod system (see the [Mods](#mods) tab once cheats are on).

The Cheats page is Journal page **5**. It is organised into tabs, listed down the
left‑hand side. Pick a tab to switch views.

## 🔴 Dangers — read this first

Cheating bypasses the game's normal pacing and gating. The most important risks:

- **Everything is written to the live save.** There is no undo. Before a cheat
  session, save to a **separate slot** you can return to.
- **You can desync systems.** Situations, unlockables, modifiers, time‑gates and
  event pools are designed to change together in a specific order. Forcing one
  piece (a stat, a situation, the clock) out of order can leave the save in a
  state the normal flow never produces.
- **You can soft‑lock progression.** Extreme stat/level values or a rewound clock
  can push a situation past a threshold it can't recover from, or hide content
  whose trigger conditions can no longer be met.
- **Cheat‑started content still counts.** Jumping an event runs its real body: it
  applies stat/flag changes and registers the event as *seen* and into the
  Gallery. It is not a "preview".
- **Some actions are destructive.** *Reset Gallery* wipes gallery unlocks; forcing
  a building state and deactivating a mod leave lasting marks on the save.

Rule of thumb: treat the Cheat Menu as a workshop, not a shortcut. If something
looks wrong afterwards, reload your backup rather than trying to cheat your way
back out.

## The tabs

### General

Time and event‑flow controls.

- **Select Events** — toggles *event selection mode*. While on, arriving at a
  location lets you **pick which available event fires** instead of the game
  choosing one at random — handy for reaching a specific scene.
- **Time — Freeze/Unfreeze** — stops (or resumes) the automatic advance of the
  daytime.
- **Set daytime to** — jump straight to Morning, Early Noon, Noon, Early
  Afternoon, Afternoon, Evening or Night.
- **Advance/rewind date** — click **Day / Month / Year** to move forward,
  right‑click to move back.

> Danger: time is a primary driver of situations and event availability. Jumping
> the clock — **especially rewinding** — can desync time‑gated content.

### Events

Browse and start any registered event directly.

- **Category filter** — cycle the button to filter the list by replay category.
- **List** — every registered event (fragments excluded), each showing its name
  and category. Click a row to run it.

Clicking an event calls it through the normal `Event.call()`, so the event plays
its full body. It is started **out of its usual trigger context**, so selectors
and values it would normally receive may be missing — dialogue text or images can
render with placeholder/wildcard values. When the event ends it returns to this
cheat page instead of advancing the daytime or running situation threshold checks.

> Danger: the event's effects (stat changes, flags, seen/Gallery registration)
> **do** apply. Missing context can also surface as `"… could not be found!"`
> image warnings.

### Situations

Drive the [situation](Building-Situations) system by hand.

- **Activate** — activates the situation (sets it active and starts its bars /
  passives). Disabled once it is already active.
- **All Teasers** — activates every teaser inside the situation at once.
- **Expand (▶ / ▼)** — unfold a situation to see its teasers; each can be
  activated individually. A ✓ marks teasers that are already active.

> Danger: activating a situation out of its intended order can conflict with the
> pacing its thresholds/resolutions expect. Teasers activated here have **no event
> context**, so text with `{placeholders}` may show unfilled.

### Unlockables

Force the visibility of any [unlockable](Building-Unlockables).

- Each unlockable shows its name (and group index) and a state: **VISIBLE**
  (override on) or **AUTO** (normal, condition‑derived).
- The button toggles the override: **SHOW** forces it visible; **HIDE** returns it
  to automatic.

The override makes even a gated group member — one whose predecessor isn't
unlocked yet — appear in the Unlockables journal and become navigable.

> Note: this only changes **visibility**. It does **not** unlock the item, start
> its situation, or grant its rewards. It's mainly for previewing hidden/WIP
> entries.

### Items

Add anything to your inventory.

- **Add all items (1× each)** — grants one of every registered item.
- **Per item** — left‑click **ADD** for +1, right‑click for +10. Each row shows
  the item's current count.

> Danger: you can push an item above its intended `max_possession`, which shop
> logic doesn't expect.

### Debug

Developer inspection and one‑off tools.

- **Debug — Activate/Deactivate** — toggles debug mode (developer overlays/tools).
- **Game Data inspector** — type a key to read its stored `Game Data` and
  `Progress` values.
- **Run Test‑Label** — runs the developer scratch label.
- **Show Paperdoll‑Test** — opens the [paperdoll](Paperdoll) preview/editor.
- **Give every Item** — same as the Items tab's bulk grant.
- **Reset Gallery** — **wipes all gallery unlocks.**
- **Dump Gallery Data** — prints gallery state to the log.

> Danger: **Reset Gallery is destructive and irreversible** for that save.

### Logs

The session log viewer (see also the log helpers used across the codebase).

- **Filters** — cycle **Type / Category / Origin** to narrow the entries.
- **Clear Logs** — empties the current session log.
- The list shows recent log entries (including expandable JSON entries).

This tab is read‑only apart from *Clear Logs*, which only affects the in‑memory
session log — it is the safest tab.

### Stats

Edit the core stats. One row per stat with `Min / −N / −1 / value / +1 / +N / Max`
controls (Money uses ±100 / ±1000 instead of Min/Max):

- **Money**
- **Level** — School, Parent, Teacher, Secretary
- **Corruption, Inhibition, Happiness, Education, Charm, Reputation** (School)

> Danger: **Level** gates content and feeds situation thresholds; the school stats
> feed situation bars and resolutions. Extreme or jumpy values are the easiest way
> to break progression or trip a threshold you can't undo.

### Buildings

Force the open/closed state of any registered building.

- **OPEN** clears every close‑reason and adds a cheat open‑reason.
- **CLOSE** adds a cheat close‑reason so the building stays shut.

> Danger: the cheat reason **persists** and overrides the building's normal
> open/close logic until you toggle it back.

### Mods

Activate or deactivate registered mods.

- Lists available mods with an **ACTIVATE / DEACTIVATE** button.
- Changes take effect only after the game is **refreshed**, and this works in
  **developer mode** only.

> Danger: deactivating a mod mid‑save **orphans** its situations, events and
> unlockables (they're invalidated, and their save state is kept for a possible
> return). Only turn mods off if you understand that trade‑off.

## Best practices

- **Back up first.** Save to a slot you don't cheat in.
- **Change one thing at a time** and check the result before the next cheat.
- **Prefer the intended lever.** e.g. to see an unlockable, use *Unlockables →
  SHOW* rather than editing the stats that gate it.
- **Watch the Logs tab** — cheat‑induced problems (missing images, invalid states)
  usually announce themselves there first.

## Related files

- `game/mods/CheatMod/cheat_mod.rpy` — registers the CheatMod and sets `cheat_mode`
- `game/scripts/journal/journal.rpy` — the `journal_cheats` screen (all tabs) and
  the cheat action labels
- `game/scripts/debug.rpy` — cheat helpers (event/situation/unlockable/item lists,
  log filters, paperdoll test)
- `game/scripts/values.rpy` — `cheat_mode`, `event_selection_mode` and related flags
