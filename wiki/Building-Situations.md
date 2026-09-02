> **Audience:** Developers who are comfortable with Python/Ren'Py but do not know
> the *Mind the School* game system. This guide explains what Situations are, how
> they work, what they can do, how to define them, and how to use them in a mod.
>
> **Scope:** This is exclusively about **Situations**. *Unlockables* (rules,
> clubs, building unlocks — which technically build on the same Situation object
> but add a PTA/vote layer) are a separate extension with their own document
> ([Building Unlockables](Building-Unlockables)).
> They are mentioned briefly where needed for understanding, but never in detail.
>
> This guide is both the **design reference** and the **practical API/workflow**
> reference for the Situation system — it is intended to be self-contained.

---

## Contents

> **New here and just want to build one?** Start with
> [Quick start](#quick-start--your-first-situation) below, then read §1–§7. The
> deep-dive sections §10–§19 are reference — consult them when you need them, not
> up front. [Troubleshooting](#troubleshooting) is at the end.

- [Quick start — your first Situation](#quick-start--your-first-situation)
1. [What is a Situation?](#1-what-is-a-situation)
2. [Lifecycle of a Situation](#2-lifecycle-of-a-situation)
3. [How bars move](#3-how-bars-move)
4. [The building blocks](#4-the-building-blocks)
5. [The definition helpers (author API)](#5-the-definition-helpers-author-api)
6. [Full example](#6-full-example)
7. [Wiring Situations into the game](#7-wiring-situations-into-the-game)
8. [Implementing Situations in a mod](#8-implementing-situations-in-a-mod)
9. [Conventions (not enforced, but important)](#9-conventions-not-enforced-but-important)
10. [Multi-bar Situations & the combined bar](#10-multi-bar-situations--the-combined-bar)
11. [The hold system (hysteresis)](#11-the-hold-system-hysteresis)
12. [Hints in detail](#12-hints-in-detail)
13. [Controlling progress from events](#13-controlling-progress-from-events)
14. [Resolutions in detail](#14-resolutions-in-detail)
15. [Stacking & chaining](#15-stacking--chaining)
16. [Stat coupling in depth](#16-stat-coupling-in-depth)
17. [Custom effects & the lifecycle registry](#17-custom-effects--the-lifecycle-registry)
18. [Pictograms (preview marks)](#18-pictograms-preview-marks)
19. [Recurring mini-Situations (pattern)](#19-recurring-mini-situations-pattern)
- [Troubleshooting](#troubleshooting)
20. [Reference tables](#20-reference-tables)

---

## Quick start — your first Situation

If you read nothing else first, read this. It gets one working Situation into the
game; the rest of the guide explains everything it glosses over.

### 1. Define the smallest possible Situation

A valid Situation needs only **one bar** and **resolutions that each have at least
one effect**. Everything else (teasers, thresholds, passives, pools) is optional.
Add it inside the `register_situations(...)` call in `label load_situations`
(base game) — or in your own mod label (see [§8](#8-implementing-situations-in-a-mod)):

```python
Situation("my_first", "My First Situation",
    "A short description of the problem the player will work on.",

    Bar("main", limits=(-30, 60),
        stat_weights={HAPPINESS: 0.5}),          # so the bar reacts to play

    PositiveResolution("ALL", DummyEffect()),    # override the auto-added default
    NegativeResolution("ANY", DummyEffect()),    # + always add a negative one
),
```

That is a complete, self-test-passing Situation. `DummyEffect()` is a legal
placeholder while you have no real resolution effect yet.

### 2. Reload

`register_situations` runs on every load, so just reload the game (or start a new
game). Your template is now registered — but **not yet active**, and an inactive
Situation with no teasers is deliberately hidden ([§2](#2-lifecycle-of-a-situation)).

### 3. Activate it

Activation is normally done by a story event, but for testing use the **Ren'Py
console** (developer mode: press `Shift+O`) and run:

```python
situation_manager.get_situation("my_first").activate()
```

Now the start values are computed, the bar goes live, and it is fully playable.

### 4. Verify

- Open the in-game **Journal → Situations page**. Your Situation should appear
  under "Active" with its bar and (if you added thresholds) its hints.
- If it does **not** appear, it was almost certainly rejected by the self-test.
  Open the Journal's **log view** and set the category filter to `situation` — every
  self-test error is logged there with a code (see
  [Reference tables](#important-self-test-error-codes)). Fix, reload, retry.

### Where to go next

Read [§1](#1-what-is-a-situation)–[§7](#7-wiring-situations-into-the-game) in order
to understand what you just did and to add real content (thresholds, hints,
passives, measures, teasers, resolution effects). Sections
[§10](#10-multi-bar-situations--the-combined-bar)–[§19](#19-recurring-mini-situations-pattern)
are depth you can reach for later; [Troubleshooting](#troubleshooting) covers the
usual "why isn't it working" cases.

---

## 1. What is a Situation?

A **Situation** represents an ongoing problem or development at the school that
the player can actively influence — e.g. "Cafeteria Crisis" or "Body Conflict".
It replaces the classic quest system as the primary player-guidance system.

The key difference from a quest: the player does **not** work through a
checklist. Instead of goals and tasks, they see a **bidirectional progress bar**
and **narrative hint texts**. The bar can move in either direction — progress is
not guaranteed to be permanent. At the end there is a positive or negative
**resolution** with concrete consequences.

```
   negative (red)                 0                   positive (green)
   -100 ────────────────────────── │ ──────────────────────────── +100
                    ▲ current position (handle)
```

Important: the **exact numeric value is never shown to the player** — only the
position of the handle on the bar and the hint texts. As an author you still work
with concrete numbers.

Technically a Situation is a `Situation` object composed of several building
blocks (bars, thresholds, passives, teasers, …), registered and managed through a
central `situation_manager`.

---

## 2. Lifecycle of a Situation

A Situation moves through several states (`situation.state` /
`situation.visibility_state`):

| State | Meaning | Visible in the journal? |
|-------|---------|-------------------------|
| `inactive` | Registered, but neither active nor showing teasers | No |
| `teaser_active` | Not active yet, but at least one teaser has unlocked | Yes — as a censored title `???????`, teaser list only |
| `active` | Running; bar, thresholds, passives etc. are live | Yes — full view (Overview / Measures / Notes) |
| `completed` | Ended via a resolution | Yes (as completed) |
| `cancelled` | Aborted (e.g. via `SituationEffectCancelSituation`) | No |

### Flow

1. **Registration** — At game start (and on every reload) all Situations are
   loaded via `register_situations(...)` inside `label load_situations`. This is
   a pure **template definition**: structure, texts, bounds.
2. **Teaser phase (optional)** — Even before the Situation "properly" starts,
   teasers can unlock (see [§4](#teaser-the-headmasters-chronicle)). The player
   then sees `???????` with early observations.
3. **Activation** — An event (or debug call) invokes
   `situation_manager.get_situation("key").activate()`. Now each bar's start
   value is computed once (a snapshot), the base wear is activated, and the
   Situation is fully playable.
4. **Runtime** — The bar moves (see [§3](#3-how-bars-move)), thresholds fire, the
   player picks passives/measures, injected events appear in the buildings.
5. **Resolution** — As soon as a resolution condition is met, its effects fire and
   the Situation goes to `completed`.

### Hot reload (important to understand)

`register_situations` runs on **every** load — including loading a save. If a
Situation already exists in the `situation_manager`, it is not recreated; instead
`update_data()` is called: the **definition** (texts, bounds, effects) is
refreshed from the template, while the **runtime state** (current bar value, which
teasers are active, which thresholds were reached) is preserved.

From this follows the single most important authoring rule: **never set runtime
state in the template definition.** Concretely: never set `bar.value` in the
template, because `update_data` will (deliberately) not overwrite it on the next
reload and you would get inconsistencies. Define starting values via `start_base`
/ `start_modifiers` — not via `value`.

#### Missing definitions (orphans)

After all base and mod registrations finish, any Situation still in the save that
was **not** re-registered in this load wave is **soft-invalidated**: it stays in
the save with its runtime state, but is hidden from gameplay (`invalid=True`).
Pending threshold checks and modifiers for that Situation are hibernated via the
lifecycle registry. If the definition returns later (mod re-enabled, key
restored), `load_situation` revives it: `update_data` → uninvalidate → resume.

**`timed_release` timers:**

- **Normal reload** (definition still present): the running grace period is
  preserved — threshold checks are only re-announced to the lifecycle registry.
- **Orphan → revive** (definition was missing, then came back): the grace timer
  is started again with `set_timer(..., "now")` — the player gets the full grace
  period anew. That is intentional, not a bug.

---

## 3. How bars move

The bar is the heart of every Situation. Its value changes through four
mechanisms:

### a) Base wear (Layer 1)

Configured per bar via `regular_decrease_rate` + `regular_decrease_interval`.
While the Situation is active, this value drags the bar constantly in one
direction each interval (typically negative). This creates return pressure —
problems don't solve themselves. Rate `0` = no wear.

### b) Stat weights (`stat_weights`)

This is the coupling to the **global school stats** (Happiness, Education,
Corruption, Inhibition, Charm, Reputation, …). When such a stat changes in the
game, the change — multiplied by the weight — is transferred to the bar:

```python
Bar("main", stat_weights={HAPPINESS: 0.5, INHIBITION: -0.8})
```

If Happiness rises by 10, `main` moves by +5. If Inhibition drops by 10, `main`
moves by +8 (a negative weight inverts the direction). This lets the Situation
respond organically to whatever the player is already doing at the school.

> The implementation runs through
> `situation_manager.apply_progress_change_via_stats`, which is called
> automatically on every stat change across all active Situations. You don't have
> to wire anything up beyond the `stat_weights`.

### c) Passives & measures (Layers 2 & 3)

Player-chosen strategies that act on the bar via **bar-change modifiers**, either
slowly (passive) or strongly (measure). See
[§4](#passives--measures-the-strategy-layers).

### d) Direct change by events

An event can push a bar directly. The bar value is internally addressable as a
pseudo-stat with the key `situation:<situation_key>:<bar_key>`:

```python
# Move bar 'main' of situation 'cafeteria_crisis' by +8:
situation_manager.apply_progress_change("situation:cafeteria_crisis:main", 8)
```

> **The bar key is a first-class stat key — reuse your stat-change calls.** This key
> is not limited to `apply_progress_change`; it is recognized everywhere the
> **global** stat-change system takes a key and is routed to the bar automatically.
> So an event that already changes school stats can push a bar in the **same** call
> instead of adding a separate line:
>
> ```python
> # module-level change_stat routes a situation key straight to the bar:
> $ change_stat("situation:cafeteria_crisis:main", 8)
>
> # the modifier-based stat-change labels accept it too — range operators
> # (range_percent, value_percent, gated_percent) resolve against the bar's range:
> call change_stats_with_modifier(**{"situation:cafeteria_crisis:main": 8})
> ```
>
> A special bar key **`ALL`** fans a change out to **every** bar of the situation:
> `situation:cafeteria_crisis:ALL` (this is how the Unlockable *Persuade* measure
> nudges all three faction bars at once). Keys may contain colons — for an
> Unlockable the situation key is itself `rule:level:3`, and the **last** segment is
> always the bar key.
>
> Caveat: the character-scoped **`StatEffect`** does *not* route here — it targets a
> character's stat via `char_obj`. Use the module-level `change_stat` or the
> modifier stat-change labels for bar pushes.

Direct bar pushes (`apply_progress_change`, `change_stat("situation:…")`, and
the modifier stat-change labels) are a **no-op** while the Situation is not
`active`. Thresholds, resolutions, pools, and passives are likewise skipped until
activation. Only teasers evaluate in the inactive / teaser phase.

Before activation (e.g. when a pre-event should influence the starting value) use
`shift_start_value` instead (see [start-value calculation](#start-value-calculation)).

### Tendency & direction

Each bar remembers its last 5 changes and averages them into a `tendency`. This
direction decides whether the hint system shows hints "upward" or "downward". You
don't have to steer this as an author — but it explains why hints follow the
player's most recent direction of movement.

---

## 4. The building blocks

A `Situation` is assembled from building blocks, all passed as elements to the
constructor. Order doesn't matter — the constructor sorts them by type.

### Bar (`SituationBar`)

The progress bar. A Situation needs **at least one** bar. Multiple bars make a
**multi-bar Situation** (e.g. three stakeholder bars `teachers` / `parents` /
`students` for PTA-style Situations). The player only ever sees a single
**weighted combined bar** (`weight` per bar); the individual sub-values stay
hidden.

Properties:
- `limits=(min, max)` — value range, default `(-100, 100)`.
- `weight` — share of the combined bar (normalized internally to a sum of 1.0).
- `stat_weights` — coupling to school stats (see [§3b](#b-stat-weights-stat_weights)).
- `regular_decrease_rate` / `regular_decrease_interval` — base wear.
- `start_base` / `start_modifiers` — start-value calculation (see below).
- **Pictograms** — a bar can carry `Picto(...)` preview marks as leading elements
  (`Bar("main", Picto("teachers_support"), limits=…)`). They are purely descriptive
  and never gate anything. Note: they are **only rendered in the Unlockable journal
  view**, not the plain Situation view — see [§18](#18-pictograms-preview-marks).

#### Start-value calculation

Each bar's start value is computed **once, at activation** — a snapshot of the
world state. Formula: `start_base`, then modifiers in the fixed order
`*` → `value_percent` (`%`) → `range_percent` → `gated_percent` → `+`, then clamp to
`limits` (see [operators](#modifier-operators)).

```python
Bar("main",
    limits=(-50, 60),
    start_base=-20,                       # base: the problem starts at -20
    start_modifiers=[
        StartModifier("+", -5),           # flat -5
        StartModifier("+", 0.05, stat=HAPPINESS),  # + (Happiness × 0.05)
    ],
)
```

A `StartModifier` **with** `stat` reads the stat once at start (snapshot), one
**without** `stat` acts directly on the running start value. Note: on a
zero-centered bar (`start_base=0`), `*` and `value_percent` (`%`) fizzle — they
scale the base, which is 0. `range_percent` and `gated_percent`, however, scale the
bar's **range**, not the base, so they still contribute at base 0 — as do `+` and
stat contributions.

### Threshold (`SituationThreshold`)

A defined point on the bar where something happens. Two types:

- **Auto-fire** (`AutoThreshold`): when the bar reaches the value for the first
  time, the attached effects fire automatically. No `threshold_hint`. Use: moments
  that happen as a reaction to overall progress ("a teacher changes their mind").
- **Blocking** (`BlockingThreshold`): the bar cannot rise past this point until a
  `Condition` is met. Use: narratively critical beats that MUST happen in a
  certain order ("the PTA vote must take place"). Effectively a quest goal that
  doesn't feel like one.

Every threshold carries two hint texts:
- `approach_hint` — shown while the bar is **below** the threshold. Vague
  direction, no exact step. **Always required.**
- `threshold_hint` — shown when the threshold is **reached**. Concrete, what to
  do. **Blocking only**; empty (`""`) for auto-fire.

Other fields:
- `direction` — `1` (upward, "value ≥ bound") or `-1` (downward,
  "value ≤ bound"). Downward thresholds serve as escalation warnings on the
  negative side.
- `visible_range` — how close the bar must get before the threshold becomes
  visible.
- Bounds — set per bar via keyword: `main=20` or `teachers=25, parents=30`.
- `timed_release` — a `TimerCondition` gives the player a **grace period**: when
  the bar reaches a blocking threshold, they have the timer span to meet the
  condition before the effects fire automatically.

> **Multi-bar:** a threshold belongs to the Situation, not to a bar. It can set
> bounds for several bars (AND-linked: `teachers=40, parents=60` fires only once
> teacher ≥ 40 AND parent ≥ 60). Its displayed position on the combined bar is the
> weighted average and can drift; the **trigger logic**, however, checks the
> individual bounds — display and fulfillment are separate.

### Passives & measures (the strategy layers)

The **three-layer model**: wear (Layer 1, above) drags the bar back; **passives**
(Layer 2) and **measures** (Layer 3) are the player-chosen countermeasures.

- **Passive** (`PassiveOption`): permanent but **weak**. It only modulates — it
  dampens the wear or contributes a small amount of its own. A Situation starts
  **without** an active passive; the player picks one in the journal. There is
  exactly one slot (`active_passive`); re-selecting the same passive toggles it
  off again.
- **Measure** (`MeasureOption`): started by the player, **time-limited**,
  **limited availability**. The source of a strong push. It has an active duration
  (`TimerCondition`), optionally a cooldown and a hard quota
  (`ManualCounterCondition`). Two kinds of effect: **instant effects** (applied
  once on start, no revert) and **lasting effects** (active over the duration,
  then automatically reverted). One slot (`active_measure`), usable in parallel
  with the passive slot; no swap — the slot frees when the duration expires.
  **`duration=None`** is instant: instant effects fire, then the slot is freed
  immediately (a cooldown still starts on that deactivate). **Exception:**
  `open_ended=True` holds the slot until something else deactivates it — used by
  Unlockable **Schedule Vote**, which stays active until the Friday PTA vote
  resolves. Instant effects are **not** reverted on close, so the queued proposal
  survives.

> **Balance principle:** wear + passive should **not** net out clearly positive.
> Real positive progress comes only from active play (measures and events). This
> keeps the return pressure structurally intact. Tutorial Situations often have
> neither passives nor measures.

#### SituationEffects

Passives and measures act through `SituationEffect` objects. Available types:

| Effect | Behavior |
|--------|----------|
| `SituationEffectSetGameData(key, value, desc)` | Sets a GameData value (restored on revert). Also usable as a no-op placeholder. |
| `SituationEffectStatChangeModifier(stat, value, op)` | Modifies a school stat. `op` is the full modifier set (`+`, `*`, `value_percent`, `range_percent`, `gated_percent`; `%` = legacy `value_percent`; range ops resolve against the stat's own range — see [operators](#modifier-operators)). |
| `SituationEffectBarChangeModifier(bar, value, op, interval)` | Moves one of its own bars per interval (`daytime_change`, `daily`, …). `op` is the full modifier set (`+`, `*`, `value_percent`, `range_percent`, `gated_percent`; `%` = legacy `value_percent`). The standard tool for passive/measure drift. |
| `SituationEffectRegularStatChange(stat, value, rhythm)` | Recurring stat change per rhythm. |
| `SituationEffectCancelSituation()` | Aborts the Situation. |
| `SituationEffectGeneral(key, effects, descriptions, revert=True)` | **Bridge to any regular `Effect`.** Wraps a list of ordinary game effects (money, level, building open/close, …) behind the description layer — see below. |

Where no real effect exists yet, use `DummyEffect()` as a placeholder (needed
because the self-test requires at least one effect — see below).

#### `SituationEffectGeneral` — the bridge to all effects

The five types above are the only "native" SituationEffects. They exist because a
plain `Effect` cannot describe itself in player-facing terms — the SituationEffect
**is the description layer**. The price is that passives/measures could otherwise
only use those five (a passive silently **drops** any element that is not a
`SituationEffect`).

`SituationEffectGeneral` removes that limit. It wraps **any** ordinary `Effect`
objects and runs them through the same apply/revert lifecycle, while **you** supply
the text to show:

```python
PassiveOption("bribe_the_board", "Grease the right palms",
    SituationEffectGeneral(
        "board_bribe",                                      # stable key, unique in this option
        [MoneyEffect("board_bribe", -500, "ADD"),          # any regular effects
         ProgressEffect("board_favor", 1)],
        ["Money: -500", "The board owes you a favor"],      # author-written lines
        revert=False,                                       # never undo these
    ),
)
```

- **`key`** — a stable, author-chosen identity, **unique among the effects of this
  passive/measure**. This is what the reload sync matches on — the wrapped effect
  set is *not* enough, because two `SituationEffectGeneral` can wrap the same effect
  types and would otherwise collide. Use `snake_case`, and never rename it (same
  key-stability rule as everywhere else).
- **`effects`** — a list of regular `Effect` objects (not SituationEffects). They
  are `apply()`-ed when the passive/measure starts. **`ModifierEffect` is rejected:**
  it registers a persistent modifier via `set_modifier()` into the *global* modifier
  collections — outside the Situation lifecycle register — so routed through here it
  would escape lifecycle cleanup and **orphan** once the Situation is torn down. The
  constructor filters any `ModifierEffect` out and logs an error (category
  `situation`); if that empties the list, self-test **761** ("needs at least one
  effect") then fires. Need a lifecycle-tracked modifier? Use
  `SituationEffectStatChangeModifier` / `SituationEffectBarChangeModifier` /
  `SituationEffectRegularStatChange` instead.
- **`descriptions`** — a list of lines you write. They are shown **comma-joined** in
  the selection list and **one per row** in the detail view (that's why it's a list,
  not a single string). The engine cannot derive these from the effects, so this is
  on you — keep them accurate.
- **`revert`** — `True` (default): the wrapped effects are `revert()`-ed when the
  passive is switched off / the measure expires. `False`: revert is a no-op, so the
  effects are **never undone** — use this for one-way changes or costs that must not
  be refunded. (Instant measure effects are never reverted anyway, so `revert` only
  matters for passive and lasting-measure use.)

> Mind the [revert semantics](#what-revert-actually-reverts) below: reverting a
> wrapped effect does whatever **that effect's** own `revert()` does. A stateless
> effect (e.g. a stat add) undoes itself; a modifier-style one only stops. If in
> doubt, set `revert=False` and make the effect one-way by design.

#### What "revert" actually reverts

This is a common misunderstanding, so be precise about it. Passive and lasting
measure effects `apply()` when they start and `revert()` when they end (passive
switched off, measure duration expired). For the modifier-based effects —
`SituationEffectBarChangeModifier`, `SituationEffectStatChangeModifier`,
`SituationEffectRegularStatChange` — **revert removes the modifier from the
modifier system; it does not roll back the value the modifier already produced.**

Concretely: a `SituationEffectBarChangeModifier("main", 3, "+", "daytime_change")`
registers a modifier that adds +3 to the bar every daytime change. While it is
active, the bar climbs 3 per tick. On revert, that per-tick modifier is pulled out
of the system — so the bar simply **stops** gaining +3 per tick. The points it
already accumulated stay on the bar. Revert is "stop the ongoing effect", not
"undo the accumulated change".

The same holds for stat effects: reverting a `SituationEffectStatChangeModifier`
removes the modifier contributing to that stat, it does not subtract back the
change the player benefited from while it was running.

The one effect that behaves like a true undo is `SituationEffectSetGameData`: it
remembers the previous GameData value on `apply` and restores it on `revert` (or
removes the key if none existed). That is a genuine value restore, because it
writes a value directly rather than registering an ongoing modifier.

### Event pools (`SituationPool`)

Situations temporarily enlarge the buildings' event pools: while the Situation is
active and the bar is within the given range, additional events can appear in the
buildings. This fills the sandbox without permanently needing more events.

```python
SituationPool("cafeteria_look_around_delivery", 35, 54)  # active while 35 ≤ value ≤ 54
```

A pool is a "window" on the bar. Positive events in high ranges, negative
escalation events in low ranges — so good and bad players see different (not
fewer) events. The pool key references the concrete event definition; optionally a
pool can be bound to a specific bar.

### Teaser (the headmaster's chronicle)

A `Teaser` is an **observation** — narratively a case note by the headmaster (who
is a psychologist in the story). Teasers serve a dual role:

- **Before activation:** they appear under the censored title `???????` and give
  the player a hunch that something is brewing — without spelling it out. Detective
  feeling instead of a progress bar.
- **After activation:** the same list moves into the **Notes tab** and becomes an
  ongoing chronicle.

**Pull architecture:** teasers observe the game, not the other way around. An event
knows nothing about triggering a teaser — the teaser defines for itself, via
`Condition`s, when it unlocks:

```python
Teaser("miwa_crying",
    "Miwa stood crying in the hallway today. Wouldn't say why.",
    EventSeenCondition("sb_event_3"),
    interpretation="Classic avoidance behavior.",
    note_type="observation",
)
```

This makes the full condition toolkit (AND/OR/NOT, StatCondition, TimeCondition,
…) usable as unlock logic, and lets a mod add teasers to **existing** Situations
without touching their code.

Options: `interpretation` (reading line), `note_type` (`observation` /
`suspicion` / `insight` / `setback`, with color/label), `image` (instant photo, 4:3 ratio),
`layout` (layout variant, otherwise random). Once unlocked, a teaser stays
unlocked (the ink is dry).

### Resolutions

The end of a Situation. Every resolution has a `ConditionStorage` (optional grace
gates) and an `EffectStorage` (what happens when it fires). Types:

| Helper | Trigger | Special |
|--------|---------|---------|
| `PositiveResolution(mode, *elements, delta_lock=False)` | Bars at **max** (`ALL`/`ANY`) | `delta_lock`: discards negative deltas while reached |
| `NegativeResolution(mode, *elements, grace_count=None)` | Bars at **min** (`ALL`/`ANY`) | `grace_count`: latch — X times of grace, then immediate |
| `DeadlineResolution(deadline, *elements)` | `Time` deadline passed | no latch, no delta lock |
| `ConditionResolution(key, *elements)` | pure conditions met (bars ignored) | ignores bar fill/deadline |

`mode`: `ALL` = all bars must reach the end, `ANY` = one is enough. Positive is
usually `ALL`, negative usually `ANY`. Every resolution needs **at least one
effect** (otherwise self-test error 780) — use `DummyEffect()` as a placeholder.

> The `Situation` constructor automatically adds an empty
> `PositiveResolution("ALL")`. Since that fails the self-test without an effect,
> you must override it with your own `PositiveResolution("ALL", …effect…)` (same
> key `positive_resolution`) and, as a rule, add a `NegativeResolution`.

### Odds and ends

- `thumbnail="images/..."` — image in the journal (also possible per threshold).
- `SituationDescription(text, *conditions)` — conditional description text.
- `add_comments(...)` — comments (used e.g. for PTA vote context).
- `add_deadline(Time(...))` — deadline, usually paired with `DeadlineResolution`.

---

## 5. The definition helpers (author API)

Situations are defined **declaratively**. Instead of instantiating the classes
directly, use the **definition helpers** — they reduce boilerplate (no manual
`direction=1` or empty `threshold_hint`) and are the recommended style.

| Helper | Creates |
|--------|---------|
| `Situation(key, name, description, *elements, thumbnail=None)` | the Situation itself |
| `Bar(key, *pictos, weight=None, limits=(-100,100), stat_weights=None, regular_decrease_rate=0, regular_decrease_interval="daytime_change", start_base=0, start_modifiers=None)` | a bar (leading `Picto(...)` args attach preview marks — see [§18](#18-pictograms-preview-marks)) |
| `StartModifier(op, value, name=None, stat=None)` | a start-value modifier |
| `AutoThreshold(approach_hint, *effects, direction=1, visible_range=100, **bounds)` | auto-fire threshold |
| `BlockingThreshold(approach_hint, threshold_hint, *conditions, direction=1, visible_range=100, default_hold=-1, **bounds)` | blocking threshold (no hysteresis by default) |
| `PassiveOption(key, description, *effects)` | passive (Layer 2) |
| `MeasureOption(key, description, duration, *limits, instant=None, permanent=None, open_ended=False)` | measure (Layer 3) |
| `SituationPool(key, bar_min, bar_max)` | event pool |
| `Teaser(key, text, *conditions, interpretation=None, note_type=None, image=None, layout=None)` | teaser |
| `PositiveResolution` / `NegativeResolution` / `DeadlineResolution` / `ConditionResolution` | resolutions |
| `register_situations(*situations)` | loads/updates the templates |

> **Important — bounds via keywords:** for `AutoThreshold` / `BlockingThreshold`
> you give the bounds **as keyword arguments per bar**, not positionally:
> `AutoThreshold("...", main=10)` or
> `BlockingThreshold("...", "...", cond, teachers=25, parents=30)`.

> **Important — thresholds are top-level elements.** Even though a threshold
> logically belongs to a bar (via its bounds), it is passed **directly to
> `Situation(...)`**, not nested inside `Bar(...)`. The association happens solely
> through the bound keys.

---

## 6. Full example

Here is a real single-bar Situation (abridged from `load_situations`):

```python
Situation("cafeteria_crisis", "Cafeteria Crisis",
    "The school doesn't have a proper cafeteria. Adelaide Hall has agreed to "
    "help, but she has no experience managing a commercial kitchen.",

    # --- Teasers (chronicle / pre-activation) ---
    Teaser("kiosk_complaints",
        "There's a heated discussion about prices at the snack bar.",
        EventSeenCondition("kiosk_price_event"),
        interpretation="Money pressure shows first at the lunch counter.",
        note_type="observation"),

    # --- Bar ---
    Bar("main",
        limits=(-30, 60),
        stat_weights={HAPPINESS: 0.5, EDUCATION: 0.2, REPUTATION: 0.2},
        regular_decrease_rate=-0.5),

    # --- Thresholds (top-level, bound via kwarg 'main') ---
    BlockingThreshold(
        "The students need a permanent place to eat lunch.",      # approach
        "Inspect the vacant building next to the courtyard.",     # reached
        EventSeenCondition("inspect_kitchen"),
        main=-5),
    AutoThreshold(
        "If I push forward, someone from the PTA will reach out.",
        main=10, visible_range=10),
    BlockingThreshold(
        "A cafeteria isn't something I can do alone. The PTA must approve.",
        "Plan a PTA vote and gather support.",
        ProgressCondition("pta_cafeteria_vote", "1"),
        main=20, visible_range=10),
    AutoThreshold("With approval, the renovation can begin.", main=35),
    AutoThreshold("The cafeteria is up and running.", main=60),

    # --- Passives (Layer 2) ---
    PassiveOption("leave_adelaide", "Leave Adelaide alone",
        SituationEffectSetGameData("cc_leave_adelaide_noop", 0, "No-op")),
    PassiveOption("hire_staff", "Hire additional staff",
        SituationEffectBarChangeModifier("main", 0.3, "+", "daytime_change")),

    # --- Event pools (sandbox filling) ---
    SituationPool("cafeteria_look_around_delivery", 35, 54),
    SituationPool("kiosk_talk_complaints", -10, 54),

    # --- Resolutions ---
    PositiveResolution("ALL", DummyEffect()),
    NegativeResolution("ANY", DummyEffect()),

    thumbnail="images/journal/cafeteria.webp",
),
```

For a **multi-bar Situation** you simply define several bars with `weight` and
thresholds with multiple bound keys, plus optional measures:

```python
Bar("teachers", weight=0.4, limits=(-40, 60), stat_weights={REPUTATION: 0.4}),
Bar("parents",  weight=0.4, limits=(-40, 60), stat_weights={REPUTATION: 0.5}),
Bar("students", weight=0.2, limits=(-40, 60), stat_weights={HAPPINESS: 0.5}),

BlockingThreshold(
    "A PTA only works if staff and parents both commit.",
    "Schedule a PTA vote and secure teacher and parent support.",
    PlaceholderCondition(),
    teachers=25, parents=30, visible_range=15),

MeasureOption(
    "faculty_briefing",
    "Call a short faculty briefing. Steady teacher support for a few periods.",
    TimerCondition("fb_duration", daytime=3),        # active duration
    TimerCondition("fb_cooldown", daytime=2),        # cooldown
    ManualCounterCondition("fb_count", 3),           # at most 3x
    instant=[SituationEffectSetGameData("fb_ping", 1, "PTA on today's agenda")],
    permanent=[SituationEffectBarChangeModifier("teachers", 3, "+", "daytime_change")],
),
```

---

## 7. Wiring Situations into the game

The definition alone shows nothing yet. Four connection points:

### Activating

A Situation starts when an event (or a debug call) activates it:

```python
$ situation_manager.get_situation("cafeteria_crisis").activate()
```

This sets `state="active"`, computes the start values and activates the base
wear. Typically this call sits at the end of a story event that narratively
introduces the Situation.

### Moving the bar (events)

Inside a Situation event you move the bar directly:

```python
$ situation_manager.apply_progress_change("situation:cafeteria_crisis:main", 8)
```

Or — more commonly — **indirectly**: the event changes a school stat (Happiness,
Education, …) and the bar follows automatically via its `stat_weights`. Both are
valid; the direct variant is used for dedicated Situation events meant to act
specifically on this one Situation.

Before activation (pre-events that influence the start value):

```python
$ situation_manager.shift_start_value("cafeteria_crisis", "main", "+", -10)
```

### Check points (automatic)

The manager is ticked automatically in several places — on event end, on
daytime/day change, and in the map overview: `check_all_thresholds`,
`check_passives`, `check_resolutions`. You don't need to call these yourself; they
ensure that thresholds with a timer grace period, expiring measures, and
resolutions are checked in time.

### Injected events

An event that should only appear during a Situation is hung into a building pool
via the pool mechanism: the event carries a `ProgressPoolCondition` (or similar),
which checks `situation_manager.check_pool(situation_key, pool_key)`, and you
declare the matching `SituationPool(pool_key, min, max)` on the Situation. While
the Situation is active and the bar is in range, the event can fire.

---

## 8. Implementing Situations in a mod

Situations are fully mod-capable — nothing is hard-wired except through keys and
conditions. There are two paths, and you can combine them.

### Path A — Register your own Situations

In your mod file you register your Situations exactly like the base game, just
with your mod key instead of `'base'`:

```python
# Queue your registration label so it runs inside the lifecycle wave (see below).
init python:
    register_start_method("load_situations_mymod")

label load_situations_mymod:
    $ set_current_mod('my_mod')          # marks assets/IDs as belonging to your mod

    $ register_situations(
        Situation("mymod_library_crisis", "Library Crisis",
            "The old library is falling apart …",
            Bar("main", limits=(-30, 60), stat_weights={EDUCATION: 0.6}),
            AutoThreshold("Something must be done.", main=0),
            BlockingThreshold("The board must approve funding.",
                "Secure a budget vote.", PlaceholderCondition(), main=20),
            PositiveResolution("ALL", DummyEffect()),
            NegativeResolution("ANY", DummyEffect()),
        ),
    )
```

`set_current_mod(key)` tells the system that the following registrations (and
referenced assets/images) belong to your mod — mirroring the pattern used in all
base scripts (`set_current_mod('base')`). `register_situations` is idempotent and
reload-safe (see [hot reload](#hot-reload-important-to-understand)): you can
re-register the same Situation on every load; if it already exists, only the
definition is updated, the save state is preserved.

> **Image paths are auto-redirected to your mod folder.** While `set_current_mod`
> points at your mod, every image path captured at construction — a Situation
> `thumbnail`, a threshold `thumbnail`, a `Teaser(image=…)`, and a `Picto(...)`
> icon — is prefixed with your mod's path. So write **plain paths relative to your
> mod root** (`thumbnail="images/journal/my_thing.webp"`), exactly as the base game
> does; **do not** hand-write `mods/MyMod/...`. Base registrations (prefix `""`)
> are unaffected. The redirect is baked in at construction, so the mod context must
> be set (via your `set_current_mod` at the top of the load label) *before* the
> `Situation(...)` is built.

> **Register your label into `start_methods` — do not register Situations from the
> init path.** The lifecycle registry (which owns Situation modifiers and pending
> threshold checks) runs a wave: the `start` / after-load flow calls
> `lifecycle_registry.begin_check()`, then the base loaders (including
> `load_situations`), then all queued `start_methods`, then
> `situation_manager.reconcile_orphan_situations()`, and only afterward
> `lifecycle_registry.finalize_check()`. Orphan reconcile runs **before** the
> sweep so hibernated resources for missing definitions survive. Registering
> Situations at init time (outside that window) can leave modifiers/checks
> unswept or incorrectly swept.
>
> Queue your label with `register_start_method("load_situations_mymod")` from an
> `init` block (as above). It only registers the *label name*; the label itself
> runs during the start sequence, inside the `begin_check` → `finalize_check`
> window. If you instead register Situations directly at init time (outside that
> window), the wave that reconciles the registry has already been set up without
> your entries, and your modifiers may not register or update properly — hibernated
> or swept as ghosts. The `situation_manager` exists by then; it is created in the
> base `load_situations`, which runs before your `start_methods` label.
>
> If the mod is missing or deactivated, its Situations are soft-invalidated on
> load (state kept). When the mod returns and re-registers them, they revive
> automatically — see [Missing definitions](#missing-definitions-orphans).

### Path B — Extend existing Situations

Thanks to the pull architecture of teasers, you can add your own teasers to an
existing Situation **without touching base code** — e.g. a mod event as another
observation for "Cafeteria Crisis":

```python
$ situation_manager.get_situation("cafeteria_crisis").add_teaser(
    Teaser("mymod_extra_hint",
        "A supplier left a flyer — cheaper ingredients, if someone asks.",
        EventSeenCondition("mymod_supplier_event"),
        note_type="insight")
)
```

Conversely, a **base event can serve as a teaser for your mod Situation** — the
direction doesn't matter, because nothing is coupled except through keys and
conditions.

> Note that teasers added at runtime directly may be synced away on a subsequent
> `register_situations` pass of the base template (because `update_data` aligns
> the teaser list with the template). If you want a permanent extension, register
> it through the same reload-safe path that loads the base Situation.

### What a mod can contribute

- New Situations (with everything: bars, thresholds, passives, measures, teasers,
  pools).
- New **injected events** into existing or your own buildings (via pools).
- New **teasers** for base Situations.
- New **effects** in passives/measures (the `SituationEffect` types are reusable;
  custom subclasses are possible but rarely necessary).

---

## 9. Conventions (not enforced, but important)

These rules cannot (or will not) be enforced by the system — follow them anyway,
or you will break saves or the game feel.

### Stable, descriptive keys
The `key` of a Situation, bar, threshold bounds, passive, measure, teaser and pool
are **identity across saves**. Use `snake_case` and descriptive names
(`leave_adelaide`, not `option_a`). **Never rename a key afterward** — the save
references it; a renamed key effectively creates a new object and loses the old
progress. Prefix mod keys (`mymod_...`) to avoid collisions with the base game or
other mods.

### No runtime state in the template
**Never** set `bar.value`, `threshold.reached`, `teaser.active` etc. in the
definition. These fields belong to the save. `update_data` deliberately does not
overwrite them — so your template value would either be ignored or would destroy
running progress. Starting values belong in `start_base` / `start_modifiers`.

### Chain methods vs. `__init__`
The builder pattern relies on `add_*`/`set_*` methods explicitly returning `self`,
so calls can be chained (`bar.set_limits(...).add_stat_weight(...)`). If you write
your own building blocks, keep that.

The `__init__` method is different, and it's easy to phrase this wrong.
Constructing an object (`Bar(...)`, `SituationBar(...)`) naturally yields the new
instance — that's just how a constructor call works, nothing special to do. What
you must **not** do is put an explicit `return <value>` inside the `__init__`
method body: Python forbids a constructor from returning anything other than
`None` and will raise `TypeError` if you try. So `__init__` sets up the object and
returns nothing itself; chaining is provided by the separate `add_*`/`set_*`
methods, not by `__init__`.

### Hint-text voice
`approach_hint` is the **headmaster's diary voice** — vague, suggestive, never the
exact click path ("The teachers seem more open."). `threshold_hint` states the
concrete **what**, never the **where/how** ("Work on the curriculum draft in the
office." rather than "Go to the office, pick work, trigger event X."). The appeal
lies in the illusion of the player's own discovery.

### Net rule of the layers
Calibrate so that **wear + passive does not net out clearly positive**. Positive
progress should come from active play (measures, events). A passive that carries
the bar to the goal on its own turns the Situation into a set-and-forget and
devalues the whole system.

### Don't cross threshold order
The narrative order emerges from the bound values. Don't build blocking thresholds
whose bounds cross between bars (on bar X, A is before B, on bar Y after B) — that
can softlock each other. The self-test catches some of this (error 791), but don't
rely on it.

### Resolutions always with an effect
Every resolution needs at least one effect (self-test 780). Even the
automatically-added positive default resolution must be overridden with your own
(with an effect, `DummyEffect()` at worst), and add a negative one.

### Use teasers sparingly
Not every trigger needs a teaser. Rule of thumb: **at most two to five unsolved
`???????` teasers at once**, otherwise "mysterious" tips over into "messy". Every
teaser needs at least one condition (self-test 700), otherwise it would never or
immediately fire.

### Pool keys by scheme
Name pool keys by `{building}_{action}_{event}` (e.g.
`cafeteria_look_around_delivery`) and make sure the referenced action exists in
the building. Anchor `min`/`max` to the narrative phases (setup, operation,
resolution).

### Take the self-test seriously
`register_situations` calls `run_self_test()` per Situation. If it fails, the
Situation is **invalidated** (not loaded) and the errors land in the log (category
`situation`). Check the log after every change — an invalid Situation silently
disappears from the game.

---

## 10. Multi-bar Situations & the combined bar

A Situation with several bars (the PTA pattern: `teachers` / `parents` /
`students`) hides its sub-values entirely — the player only ever sees **one
combined bar**. Understanding how that combined bar and its thresholds are computed
is essential for authoring multi-bar Situations.

### Weights

Each bar's `weight` is its share of the combined bar. Weights are **normalized to
sum 1.0** at load — you can pass raw numbers (`0.4, 0.4, 0.2` or `2, 2, 1`), they
mean the same thing. If you give no weights, bars are distributed evenly (`1/n`).
Invalid weights (≤ 0 or unknown bar keys) are dropped with a non-blocking log and
the rest is re-normalized.

> `stat_weights` (stat coupling, [§16](#16-stat-coupling-in-depth)) is a **separate
> concept** — it is *not* the combined-bar weight. One decides stat influence, the
> other the share on the combined bar.

### The combined handle

```
combined_handle = Σ (weight_bar × value_bar)     over all bars
```

Always weighted; there is no unweighted variant. For a single-bar Situation the
combined handle equals that bar's value (projection = identity).

### Threshold projection (display) vs. fulfillment (trigger)

A multi-bar threshold sets bounds for one or more bars via keywords
(`teachers=40, parents=60`); bars it omits are **unbounded** for that threshold.
Two things must be kept apart:

**Projected position** (where the gate marker sits on the combined bar):

```
projected_position = Σ (weight_bar × reference_value_bar)   over all bars
  reference_value = bound          (for bounded bars)
                  = current value  (for unbounded bars)
```

So `projected − combined_handle = Σ weight_bar × (bound − value)` over the bounded
bars. Consequences:

- A bounded bar reaching its bound → its gap contribution vanishes.
- All bounded bars met → handle and marker coincide (gap 0).
- An **unbounded** bar moving → handle and marker shift by the same amount; the
  gap stays constant.
- A **bounded** bar moving toward its bound → the marker stays put (w.r.t. that
  bar), the handle closes in; the gap shrinks.

**Fulfillment** is checked **per bounded bar, AND-linked**, and ignores the
projection entirely:

- `teachers=40, parents=60` fires only once teacher ≥ 40 **AND** parent ≥ 60
  (direction `1`; direction `-1` uses ≤).
- teacher 80, parent 20 → the average of the bounds is "reached" but the parent
  bound is not → the threshold does **not** fire.

### Growth clamp

A blocking threshold caps **each of its bounded bars individually** at that bar's
bound until it is completed. Unbounded bars keep growing freely. Author rule: for
each bar, the bounds of consecutive blocking thresholds must be **monotonic** in the
growth direction — non-monotonic (crossing) bounds risk a softlock and trip the
load-time check (error 791; the offending threshold is skipped with a non-blocking
log, the rest of the Situation still loads).

### "Next" threshold, visibility, and static display

The *next* threshold in a direction is the un-reached one with the **smallest
distance on the combined bar** (`|projected − combined|`, directed). This resolves
the case where two bars suggest different next thresholds — the one nearer on the
combined bar wins, so journal markers, hints, and engine checks stay consistent. A
threshold's `visible_range` is likewise measured as the combined-bar gap, so
approaches via bounded and unbounded movement count consistently.

Bar values, projections, and visibility only update **at the time-segment change**
after an event ends (the game has 7 rotating time segments); nothing moves while the
journal is open. The display is static within a view — no smoothing needed.

---

## 11. The hold system (hysteresis)

When a blocking threshold with a timer grace period is cleared or times out, it
may enter a **hold** state that pins the bar at its bound and prevents an
immediate re-trigger. While held, the threshold is skipped in all threshold
searches and does not fire again. The hold releases only once the bar has clearly
moved `hold` points **beyond** the bound (direction-aware).

`default_hold` controls this:

- **`-1` (BlockingThreshold default)** — no hysteresis. The threshold is marked
  permanently `reached` and **cannot re-arm**. Use this for one-shot quest gates.
- **`0` or higher** — hysteresis zone of that size; after release the gate can
  trigger again if the bar returns to the bound.

Plain blocking thresholds without a timer already set `reached = True` on success
and never enter hold. You only need an explicit `default_hold=…` when a
`TimerCondition` is involved and you want reactivation hysteresis (e.g.
`default_hold=5`).

This hysteresis is deliberately **separate** from resolution grace
([§14](#14-resolutions-in-detail)): thresholds carry hint obligations and a
visible bar position; resolutions do not.

---

## 12. Hints in detail

The journal shows, instead of goals: the combined bar, a **list** of narrative hint
texts, and the active passive/measure. The hint list — not a single hint — matters
because several thresholds can be approached at once (on different bars, or an
auto-fire alongside a blocking gate).

- **Per relevant threshold:** if its bar value is reached, its `threshold_hint` is
  shown; otherwise its `approach_hint`. Empty hints are omitted.
- **Sorted** by the proximity of the projected threshold position to the combined
  value (closest first).
- **Cap:** at most `number_of_bars × 2` hints are active at once (per bar, one
  blocking gate plus a passing auto-fire); the Notes/Hints display scrolls, so
  there is no overflow.

### Direction via tendency

On a bidirectional bar the system must decide whether to show hints upward or
downward. Each bar averages its **last 5 changes** into a `tendency`; the combined
tendency returns `1` / `-1` / `0`. Hints follow that direction; a neutral tendency
defaults to upward (`1`). You don't steer this — it just makes hints follow the
player's recent direction of movement. (See [§9](#9-conventions-not-enforced-but-important)
for the hint-text voice rules.)

---

## 13. Controlling progress from events

An event has three distinct ways to affect a Situation's bar — pick by intent:

### a) Direct push (during runtime)

Move a bar directly through its pseudo-stat key:

```python
$ situation_manager.apply_progress_change("situation:cafeteria_crisis:main", 8)
```

`situation:<key>:<bar>` (or `situation:<key>` → bar `main`). This is the manual push
for dedicated Situation events. It is a **no-op** until the Situation is `active`.
The same key also works in the general stat-change
calls (`change_stat`, the modifier stat-change labels) and supports the `ALL` bar
key — so you can fold a bar push into an existing stat change instead of a separate
line; see the note in [§3d](#d-direct-change-by-events).

### b) Shift the start value (before activation)

For a pre-event that should influence where the bar starts:

```python
$ situation_manager.shift_start_value("cafeteria_crisis", "main", "+", -10)
```

`start_shifts` survive definition sync and are applied at activation alongside the
author's `start_modifiers`.

### c) The progress-blocker system

Every stat change auto-drifts all active Situations via their `stat_weights`
([§3b](#b-stat-weights-stat_weights)). Sometimes an event must **suppress** that
auto-drift — e.g. a Situation event that sets its own bar explicitly and doesn't
want the stat side effects doubled in. The manager keeps a rule set:

| Rule | Blocks |
|------|--------|
| `("situation", key)` | all auto-drift for one Situation (`"*"` = all) |
| `("stat", key)` | all auto-drift through one stat (`"*"` = all) |
| `("pair", situation, stat)` | only that Situation×stat combination (wildcards on both axes) |

API: `block_progress(situations=None, stats=None)` (only situations → situation
axis; only stats → stat axis; both → pair rules; `"all"` as wildcard),
`unblock_progress(...)` (mirror the block), `clear_progress_blocks()`. Typically you
`block_progress(...)` at the start of a Situation event and rely on
`clear_progress_blocks()` at `end_event` to reset everything.

---

## 14. Resolutions in detail

A resolution ends a Situation. It works in **two levels**:

1. **Reached** (`is_reached`): the intrinsic trigger — bars at min/max (per
   `ANY`/`ALL`) or a deadline passed.
2. **Fire** (`evaluate` → `fire`): only if reached **and** the gating conditions (if
   any) are met. No conditions → fires immediately on reaching.

Each resolution carries a `ConditionStorage` (optional gates) and an `EffectStorage`
(at least one effect — self-test 780). The `Situation` constructor auto-adds a
default `PositiveResolution("ALL")` and `NegativeResolution("ANY")`; override them
with your own (with effects).

### Grace period (gate conditions)

If a resolution has gate conditions, they act as a grace period:

- On entering "reached", every `TimerCondition` gate is started (`set_timer(id,
  "now")`).
- While reached, the gates are checked; all fulfilled → `fire()`.
- If the bar leaves the end before the gates pass, the checks stop and timers are
  removed — grace ends without firing.

### Type specifics

- **`PositiveResolution(mode, *elements, delta_lock=False)`** — bars at max.
  `delta_lock`: while positively reached, negative bar deltas are discarded (holds
  the win against slippage during grace).
- **`NegativeResolution(mode, *elements, grace_count=None)`** — bars at min.
  `grace_count`: a latch — the resolution supplies its own `LatchCounterCondition`
  (you give only the count); each time the bar reaches min and then leaves counts
  once, and when the latch is exhausted it fires immediately on the next reach.
- **`DeadlineResolution(deadline, *elements)`** — fires after the `Time` deadline,
  immediately or after its conditions; **no** latch, **no** delta lock.
- **`ConditionResolution(key, *elements)`** — pure conditions, bars ignored.

`mode` is `ALL` (all bars must reach the end) or `ANY` (one suffices); positive is
usually `ALL`, negative usually `ANY` (self-test 781/782). Resolutions are checked
on bar change, daytime/day change, map overview and event end; the first one to fire
wins.

### Lasting modifiers in a resolution (orphan-safe)

A resolution's effects fire once, but a `ModifierEffect` among them installs a
**persistent** modifier. Unlike `SituationEffectGeneral` (which *rejects* `ModifierEffect`),
a resolution's `EffectStorage` accepts a raw `ModifierEffect` — because the resolution
gives it the same lifecycle handling the managed-modifier path uses:

- **On fire**, each `ModifierEffect` is applied (by the effect) *and* its modifier is
  registered with the lifecycle registry under the effect's own modifier key.
- **Every load wave**, the resolution's `update_data` re-affirms (KEEP-pings) those
  modifiers — and a **completed** Situation still runs this as long as its template is
  registered, so the buff survives across saves.
- If the Situation (or its mod) goes away, nothing re-affirms the modifier and the next
  lifecycle sweep removes it — no orphan.

So a resolution may hand out a lasting stat/bar buff via `ModifierEffect` without you
managing its removal. Give the `ModifierEffect` a **unique key** (it *is* the modifier's
registry key). See [Modifiers](Modifiers) for the orphan model.

> **No level regression.** Situation consequences are stat changes, flags, and
> content access — never a level step-back.

---

## 15. Stacking & chaining

### Stacking

There is **no hard limit** on simultaneously active Situations. Unsolved ones pile
up and press on each other, which is the intended difficulty curve: more active
Situations mean more events competing for attention, more passive/measure costs
adding up, and negative drift in neglected Situations that can cascade. Design
safety valves keep this fair:

- **Stat floors** — Situation penalties alone cannot push a stat below a minimum.
- **Cascading resolution breather** — when one Situation resolves negatively,
  remaining active Situations pause **base wear only** (`regular_decrease`).
  Duration is `min(4, remaining active count)` after the failed Situation
  completes. Day-change checks the counter **before** decrementing, so N=1
  covers the current day plus the next full day. A second failure extends via
  `max(remaining, new)` — never stacks. Events, passives, measures, and
  stat-weights keep running. Shown on the Situations journal page above the list.
- **Story-driven pacing** — Situations are introduced by already-balanced story
  events, so a normal playthrough doesn't stack extremes.

### Chaining

Situations feed each other through **flags and start values**, not hard links:

- A resolution sets a flag (`SituationEffectSetGameData("body_conflict_resolved",
  "positive", …)`).
- A later Situation reads that flag — as an activation condition, or to bias its
  start via `start_modifiers` / a pre-activation `shift_start_value`.
- A positive earlier resolution can improve a later Situation's starting bar; a
  negative one can worsen it or add a blocking threshold.

Example: "Social Sorting" resolves positively → "Body Conflict" starts at `-5`
instead of `-20`, because the social groundwork is laid.

---

## 16. Stat coupling in depth

`stat_weights` couples a bar to the school stats so the Situation reacts to whatever
the player is already doing (see [§3b](#b-stat-weights-stat_weights)). Three rules
for using it well:

- **Keep the scaling small.** The conversion from stat change to bar movement must
  feel like background noise — a small Happiness boost should move the bar maybe
  `+0.5`…`+1`. It accumulates over many events but is never the main driver. The
  intended player feeling: "I taught and patrolled a lot this week and the Situation
  somehow improved, even though I did nothing specific for it." Real positive
  progress still comes from active play (measures, events).
- **Invert where it makes sense.** A negative weight flips direction — e.g. falling
  Inhibition *helping* a conflict defuse: `stat_weights={INHIBITION: -0.8}`.
- **Differentiate per bar in multi-bar Situations.** Education can weigh more on the
  `teachers` bar than on `parents`, etc., so different stats pull different factions.

Manual per-event Situation influence would be absurd across ~45+ regular events,
teaching subjects, office work and counseling — `stat_weights` is the mechanism that
lets all of that ambiently move the right Situations without hand-wiring each event.
When an event must opt out of this auto-drift, use the progress-blocker system
([§13c](#c-the-progress-blocker-system)).

---

## 17. Custom effects & the lifecycle registry

The built-in `SituationEffect` types ([§4](#situationeffects)) cover common cases,
and `SituationEffectGeneral` already bridges to **any** regular `Effect` — so before
subclassing, check whether wrapping existing effects with `SituationEffectGeneral`
does the job. When you do need bespoke behavior you can still subclass
`SituationEffect`. The ABC contract every effect
implements: `clone()`, `update_data(other)`, `apply(**kwargs)`, `revert(**kwargs)`,
`run_self_test()`, plus `local_key` (stable identity within its passive/measure,
without the Situation prefix) and the fully-qualified `key`
(`<situation>:passive:<name>:effect:<local_key>`). The `apply`/`revert` contract is
what lets passives toggle and measure durations expire cleanly — effects are
reverted before new ones take hold or the slot frees. Remember the revert semantics
from [§4](#what-revert-actually-reverts): modifier-based effects *stop*, they don't
roll back accumulated value; only game-data effects truly restore.

### Why the lifecycle registry exists

Situation modifiers live on in the **global** stat/modifier system even after their
origin Situation is gone (e.g. a disabled mod). A global `lifecycle_registry` tracks
ownership so orphaned modifiers can be swept:

| Level | Meaning | Example |
|-------|---------|---------|
| `owner` | system | `"situations"` |
| `category` | instance | `"cafeteria_crisis"` |
| `key` | resource | `"cafeteria_crisis:passive:…:effect:…"` |

**Ping states:** `KEEP` (hold / revive from hibernation), `HIBERNATE` (suspend,
keep metadata), `UPGRADE` (remove + recreate), `REMOVE` (final). A resource that
stays silent until the sweep is a ghost → removed.

**The wave barrier:** during the init/reload wave — `begin_check()` → systems load
(each `track`/`ping` marks its resources alive) → `finalize_check()` — ghosts (any
tracked resource **not** pinged this wave) are removed **only** in `finalize_check`,
so a missing or disabled system never blocks the sweep. This is exactly why mod
Situations must register inside the wave (see
[§8](#8-implementing-situations-in-a-mod)): `track_modifier` writes into this
registry (`owner="situations"`, `category=situation.key`) and marks the resource
pinged, and an invalid Situation (failed self-test) has its category hibernated
rather than lost.

---

## 18. Pictograms (preview marks)

Pictograms are small **descriptive preview marks** — "persuade the teachers", "raise
education". They are **purely descriptive**: they check nothing, gate nothing, unlock
nothing. They replace the old condition-icons.

> **In practice, pictograms are an Unlockables feature.** The data model lives on
> `Situation`/`Bar`, and `Unlockable` inherits it (`class Unlockable(Situation)`), so
> you *can* attach `Picto(...)` to any Situation or bar — but **only the Unlockable
> journal view renders them**. The plain Situation journal view has no pictogram
> display, so a `Picto(...)` on a non-Unlockable Situation is stored but never shown.
> See [Building Unlockables](Building-Unlockables) for where they actually appear.

**Reference, not object.** A pictogram *definition* (icon pattern + label + tooltip
templates) lives once in a central registry under a key. A bar or Situation stores
only the **key** — via the `Picto("key")` vehicle in its element list:

```python
Bar("teachers", Picto("teachers_support"), limits=(-40, 60)),
# or at situation level (identity-only, no bar value):
Situation("...", Picto("factions_all"), ...),
```

Resolution happens at display time: the key is looked up, the owner's local context
(a bar's key/value/name, or the Situation's identity) fills the templates, and a
fresh icon+label+tooltip is produced (so a live bar value in a tooltip is always
current). A **bar-bound** pictogram has access to `bar_value` and can show a live
value; a **situation-bound** one has only identity keys and stays purely
descriptive.

- **Self-declared needs / load check.** Each pictogram derives from its templates
  which context keys it needs (e.g. `<bar_value>`). At load the owner's offered keys
  are compared against the needed keys; a mismatch means the pictogram simply
  **isn't loaded**, with a concrete log entry ("expects `<x>`, owner offers …").
- **Soft-fail.** A missing or broken pictogram **never** invalidates the Situation —
  it is skipped at render, everything else keeps working. This is deliberate: a
  decorative mark is not worth failing a Situation over.
- **Mod / late attach.** Add a pictogram to an existing Situation/bar without
  touching its definition: `situation_manager.add_pictogram(situation_key, picto_key,
  bar_key=…)` (omit `bar_key` to attach at Situation level). The `add_pictogram` call
  must run after the target Situation is loaded.

---

## 19. Recurring mini-Situations (pattern)

Not every Situation is a long arc. A useful lightweight pattern (used e.g. for
potion/serum testing) is the **mini-Situation**: a short Situation opened on demand
that tracks a single quick outcome.

- **Short runtime** — a few events over a few days.
- **Small bar range** — e.g. `limits=(-30, 30)`.
- **No passives/measures** — too short to matter.
- **Parameters shape the bar** — a willing test subject → a narrower, lower-risk
  bar; a riskier setup → a wider bar with larger swings. Early attempts get wider
  bars (more uncertainty), later ones narrower (the character has learned).
- **Both resolutions carry meaning** — a negative resolution is a learning beat
  (the next attempt accounts for the mistake), a positive one unlocks the next
  stage.

Mechanically these are ordinary Situations — the pattern is just a calibration
recipe (short, narrow, passiveless) plus activating a fresh instance per occurrence.

---

## Troubleshooting

Symptom-first list of the mistakes newcomers actually hit. When in doubt, **check
the log** (Journal log view, category filter `situation`) — a rejected Situation
always logs why.

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| **It doesn't appear in the journal at all** | The self-test rejected it (invalidated, not loaded). | Check the log (category `situation`) for an error code ([table below](#important-self-test-error-codes)) and fix it. |
| | It was never registered. | Ensure it's inside a `register_situations(...)` call that actually runs — base `load_situations`, or a mod label queued via `register_start_method` ([§8](#8-implementing-situations-in-a-mod)). |
| | It's inactive and has no teasers. | Inactive teaser-less Situations are hidden by design ([§2](#2-lifecycle-of-a-situation)). Activate it, or give it a teaser. |
| **It shows as `???????` and never becomes the real title** | It's in `teaser_active` — teasers unlocked but the Situation was never activated. | Call `…activate()` (from the triggering event, or the console). |
| **The bar never moves** | No `stat_weights`, no events pushing it, and `regular_decrease_rate` is 0. | Add `stat_weights`, a wear rate, or move it from an event ([§3](#3-how-bars-move), [§13](#13-controlling-progress-from-events)). |
| **A threshold never fires** | Blocking condition unmet; or (multi-bar) not *all* bounds met; or it's on hold; or bounds cross. | Verify the condition; remember multi-bar bounds are AND-linked ([§10](#10-multi-bar-situations--the-combined-bar)); check for a softlock (error 791). |
| **A threshold event fires from a cheat-menu test / while the Situation is still inactive** | Direct `apply_progress_change` used to move bars and fire AutoThresholds regardless of state. | Bars, thresholds, pools, passives, and resolutions no-op until `activate()`. Use `shift_start_value` before activation, or activate first. |
| **It never resolves / never ends** | A resolution has no effect (rejected, 780); or bars can't reach their `limits`; or gate conditions are unmet. | Give every resolution an effect; check bar `limits` vs. the resolution mode; review gates ([§14](#14-resolutions-in-detail)). |
| **Edits to my template don't take effect / progress reset** | You set runtime state (`bar.value`, `reached`, …) in the template. `update_data` deliberately keeps save state and won't overwrite it — and template runtime state corrupts progress. | Set starting values via `start_base` / `start_modifiers`, never `value` ([§9](#9-conventions-not-enforced-but-important)). |
| **A passive/measure effect "won't undo"** | Revert stops an ongoing modifier; it does not roll back accumulated value. | Expected behavior — only `SituationEffectSetGameData` truly restores ([§4](#what-revert-actually-reverts)). |
| **A measure stays active forever** | `duration=None` without `open_ended` should auto-close after apply. | Instant is the default ([§4](#passives--measures-the-strategy-layers)). Use `open_ended=True` only when something else must close the slot (Unlockable Schedule Vote). |
| **Mod Situation vanishes after disabling/re-enabling the mod** | Orphan soft-invalidation. | Expected — it revives on re-registration; timers may restart ([§2](#missing-definitions-orphans)). |

---

## 20. Reference tables

### Intervals / rhythms
`daytime_change` · `daily` · `weekly` · `monthly` · `yearly`

### Modifier operators

The single percent operator was split and extended. `%` is kept as a **legacy alias
for `value_percent`** (normalized automatically).

| Operator | Change applied to the value | At `base = 0` |
|----------|-----------------------------|---------------|
| `+` | flat add: `+ value` | contributes |
| `*` | multiply: `value × base` | fizzles (0 × anything) |
| `value_percent` (`%`) | percent of the current value: `+ base/100 × value` | fizzles |
| `range_percent` | percent of the whole min→max range: `+ range/100 × value` | **contributes** |
| `gated_percent` | percent of the gated range (up to the current cap): `+ gated_range/100 × value` | **contributes** |

- All three modifier effects — **bar-change** (`SituationEffectBarChangeModifier`),
  **stat-change** (`SituationEffectStatChangeModifier`), and **start-value**
  (`StartModifier`) — accept the full set above.
- For `range_percent` / `gated_percent`, the range resolves against the target: a
  bar modifier uses that bar's range, a stat modifier uses that stat's own range.
- **Start-value application order:** `*` → `value_percent`/`%` → `range_percent` →
  `gated_percent` → `+`, then clamp to `limits`.

### Teaser `note_type`
`observation` (blue) · `suspicion` (purple) · `insight` (green) · `setback` (red)

### Teaser `layout`
Text: `text_full`, `text_aside` · Photo: `photo_left`, `photo_right`, `photo_top`
(only with `image`). If omitted: random on activation.

### Common conditions
| Goal | Condition |
|------|-----------|
| Event was seen | `EventSeenCondition("event_key")` |
| Building unlocked | `BuildingCondition("cafeteria")` |
| Progress step | `ProgressCondition("key", "2")` |
| Timer (duration/cooldown/grace) | `TimerCondition("id", daytime=3)` |
| Hard quota | `ManualCounterCondition("id", 3)` |
| Placeholder / WIP | `PlaceholderCondition()` |

More in `game/scripts/conditions.rpy`.

### Important self-test error codes
| Code | Meaning |
|------|---------|
| 700 | Teaser without a condition |
| 718/719 | Blocking threshold without `threshold_hint`+condition, or empty `approach_hint` |
| 730/731 · 740–744 · 750–752 | SituationEffect field errors (game-data / stat / bar / rhythm) |
| 760–764 | `SituationEffectGeneral`: invalid `key`, no effect, non-`Effect` item, bad/empty descriptions, non-bool `revert` |
| 780 | Resolution without an effect |
| 781/782 | Resolution mode not `ALL`/`ANY` |
| 784 | `NegativeResolution` `grace_count` invalid |
| 790 | Situation without a bar |
| 791 | Threshold bounds cross (softlock risk) |
| 792/793 | Situation key or name empty |

### Related files
- `game/scripts/situations/situations.rpy` — classes, helpers, `load_situations`
- `game/scripts/conditions.rpy` — condition toolkit
- `game/scripts/effects.rpy` — effect types
- `game/scripts/journal/pictograms.rpy` — pictogram registry ([§18](#18-pictograms-preview-marks))
- [Building Unlockables](Building-Unlockables) — the Unlockable extension
- `.cursor/skills/build-situation/` — skill/reference for building Situations
