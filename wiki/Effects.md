> **Audience:** Developers comfortable with Python/Ren'Py who need to *change* game
> state from *Mind the School* content — events, situation resolutions, unlockable
> unlocks, PTA votes. This guide covers the `Effect` base contract, how effects are
> applied and reverted, the shared `Option` system, and the full catalog.
>
> **Scope:** The ordinary `Effect` system (`effects.rpy`). These are the "what
> happens" counterpart to [Conditions](Conditions) (the "when").
> The situation-internal `SituationEffect` types (the description layer used by
> passives/measures) are a **separate** hierarchy — see the Situations guide — but
> they can wrap any ordinary `Effect` via `SituationEffectGeneral`.

---

## Quick start

An Effect is a small object that mutates game state when `apply()`-ed. You build
one and hand it to whatever system runs it (an event's effect list, a resolution, an
unlockable unlock):

```python
# When this fires: +500 money, mark a flag, open a building.
MoneyEffect("reward_money", 500, "ADD")
ValueEffect("cafeteria_opened", True)
BuildingOpenEffect("cafeteria")
```

- `effect.apply(**kwargs)` runs it; `effect.revert(**kwargs)` undoes it (if the
  effect supports revert).
- A group runs via `EffectStorage(*effects).apply(**kwargs)`.
- Character-scoped effects (`StatEffect`, `LevelEffect`) need a `char_obj` in the
  kwargs; without one they no-op.

---

## Contents

1. [What is an Effect?](#1-what-is-an-effect)
2. [The base contract](#2-the-base-contract)
3. [apply / revert semantics](#3-apply--revert-semantics)
4. [EffectStorage](#4-effectstorage)
5. [Options](#5-options)
6. [The effect catalog](#6-the-effect-catalog)
7. [Effects vs. SituationEffects](#7-effects-vs-situationeffects)
8. [Common patterns](#8-common-patterns)
9. [Conventions](#9-conventions)
10. [Troubleshooting](#10-troubleshooting)
11. [Reference tables](#11-reference-tables)

---

## 1. What is an Effect?

An **Effect** performs a state change: adjust a stat, move money, set a flag, open a
building, unlock content, fire another event. Effects are the actions that run when
a gate passes — an event completes, a situation resolves, a vote succeeds.

Like conditions, effects are **declarative and reusable**. You compose the existing
types; you rarely subclass. Everything is coupled through keys, so a mod's effect
can act on base state and vice versa.

---

## 2. The base contract

Every effect subclasses `Effect(name, *options)`:

- **`name`** — a stable identifier. For modifier-style effects it is the modifier
  key (identity in the modifier system), so it must be **unique** where that
  matters. For plain effects it's mostly a label.
- **`apply(**kwargs)`** (abstract) — perform the change. Receives the runtime
  context (`char_obj`, event data, …).
- **`revert(**kwargs)`** — undo the change. **Default is a no-op** (many effects are
  one-way). Effects that support undo override it.
- **`options`** (`OptionSet`) — trailing `*options` that tweak behavior
  (`EffectNoRevert`, `MoneyEscrow`).

`**kwargs` carry context. The most important is **`char_obj`**: character-scoped
effects read it (defaulting to nothing → no-op if absent). Most non-character
effects (`MoneyEffect`, `ValueEffect`, `BuildingOpenEffect`, …) ignore it and work
standalone.

---

## 3. apply / revert semantics

Whether `revert` actually undoes depends on the effect. Three groups:

- **Symmetric (inverse) revert:** `StatEffect`, `MoneyEffect` — `apply` adds/sets,
  `revert` applies the inverse. Correct even if the effect object is fresh, because
  it's pure arithmetic. `revert` respects the `EffectNoRevert` option (skips undo).
- **Stored-previous revert:** `ValueEffect`, `ProgressEffect`,
  `UnlockableUnlockEffect` — `apply` remembers the prior value and `revert` restores
  it. A genuine undo, but it needs the *same* instance that applied it.
- **No revert:** the default (`revert` does nothing) — `NotificationEffect`,
  `EventEffect`, `DummyEffect`, most one-way actions. `BuildingOpenEffect` /
  `BuildingCloseEffect` do revert (they add/remove a collection key).

> This is the same "stop vs. undo" distinction as the situation `SituationEffect`
> types. When an effect is wrapped in a situation passive/measure via
> `SituationEffectGeneral`, the wrapper's `revert` flag decides whether `revert` is
> even called — and if the wrapped effect is a no-revert or modifier-style effect,
> "undo" means whatever that effect does. When in doubt, design one-way.

`mode` on value effects: **`"ADD"`** (add the value) or **`"SET"`** (set to the
value). `SET`'s revert is best-effort — prefer `ADD` when you need clean undo.

---

## 4. EffectStorage

`EffectStorage(*effects)` holds an ordered effect list and forwards `apply` /
`revert` to each in turn. Resolutions and other multi-effect hosts use it. You
mostly pass a plain list/varargs of effects to a system and it wraps them; construct
`EffectStorage` directly only when writing such a host.

---

## 5. Options

Trailing `*options` (from `option.rpy`) tweak an effect — see the
[Options](Options) guide for the full shared catalog. The
effect-relevant ones:

| Option | Effect |
|--------|--------|
| `EffectNoRevertOption()` (`"EffectNoRevert"`) | `revert` becomes a no-op — the change is permanent even inside a reverting host |
| `MoneyEscrowOption(stash_key)` | a `MoneyEffect` ADD cost consumes a reserved PTA-vote stash instead of charging again (auto-attached by the Unlockable machinery — you rarely add it by hand) |

Other options are condition- or event-specific — see the
[Options](Options) guide. Options are passed after the
constructor's own args: `MoneyEffect("cost", -1500, "ADD", EffectNoRevertOption())`.

---

## 6. The effect catalog

`blocking`/`mode` defaults noted; `*options` always accepted last.

### Stats, level & money

| Constructor | Does |
|-------------|------|
| `StatEffect(name, stat, value, mode="ADD", *options)` | change a **character** stat (`char_obj` from kwargs); reverts by inverse. *No-op without a `char_obj`.* |
| `LevelEffect(name, value, mode="ADD", char_obj=None, *options)` | change a character/school level; `char_obj` may be a key, else taken from kwargs |
| `MoneyEffect(name, value, mode="ADD", *options)` | change money; reverts by inverse; honors `MoneyEscrow` |

> There is **no** dedicated effect for *school* stats — `StatEffect` is
> character-scoped. Drive school stats via `ModifierEffect` or the `change_stat`
> path (see the Modifiers guide).

### Progress, values & data

| Constructor | Does |
|-------------|------|
| `ProgressEffect(key, value=1, *options)` | set an event-series progress step (stores previous → reverts) |
| `ValueEffect(key, value, *options)` | set a registered value / flag (stores previous → reverts) |
| `ChangeKwargsEffect(key, value)` | inject/overwrite a kwarg for the rest of the current event flow |
| `SetProficiencyEffect(subject, *, level=0, xp=0)` | set a teaching proficiency |

### Modifiers

| Constructor | Does |
|-------------|------|
| `ModifierEffect(key, stat, mod_obj, collection="default", *options)` | register a `Modifier_Obj` on a stat (or a `situation:<k>:<bar>` key) in a modifier collection; `revert` removes it. The low-level engine behind stat/bar drift — see the Modifiers guide |

### Map / buildings

| Constructor | Does |
|-------------|------|
| `BuildingOpenEffect(building_key, is_open=True, *options)` | open (or with `is_open=False`, close) a map location; reverts |
| `BuildingCloseEffect(building_key, is_close=True, *options)` | close (or reopen) a map location; reverts |
| `BlockBuildingEffect(name, building_name, is_blocking=True, *options)` | block/unblock a building; reverts |

### Events

| Constructor | Does |
|-------------|------|
| `EventEffect(event, *options)` | queue/run an event (`Event` / `EventStorage` / key) |
| `EventSelectEffect(event, *options)` | present a selection among events (`Event`/key/list) |

### Unlockables & PTA

| Constructor | Does |
|-------------|------|
| `UnlockableUnlockEffect(unlockable_situation_key, group_key=None, group_index=-1, *options)` | mark an unlockable unlocked (+ group level); reverts. Injected by the Unlockable machinery — you don't add it yourself |
| `ScheduleVoteEffect(situation_key, *options)` | put an item on the PTA schedule; reverts |

### Quests (legacy path)

| Constructor | Does |
|-------------|------|
| `QuestCompleteEffect(quest_type, key)` · `QuestVisibleEffect(...)` · `QuestInvisibleEffect(...)` · `QuestActivateEffect(key)` | drive the legacy quest system (Situations/Unlockables replaced quests for new content) |

### UI & placeholders

| Constructor | Does |
|-------------|------|
| `NotificationEffect(message)` | show a player notification |
| `DummyEffect(*options)` | no-op placeholder — satisfies "needs at least one effect" self-tests (resolutions) while you have no real effect yet |

> **Legacy (deprecated, save-compat no-ops):** `RuleEffect`, `ClubEffect`,
> `BuildingEffect`. Use `UnlockableUnlockEffect` (auto-injected) /
> `BuildingOpenEffect` instead.

---

## 7. Effects vs. SituationEffects

Two similarly-named hierarchies — don't confuse them:

- **`Effect`** (this guide) — the general action system. Used by event effect lists,
  resolution `EffectStorage`, unlockable unlock effects.
- **`SituationEffect`** (Situations guide) — a *description-carrying* wrapper used by
  situation **passives/measures**, because a plain `Effect` can't describe itself in
  player-facing text. There are a few native ones (set-gamedata, stat/bar modifier,
  cancel), plus **`SituationEffectGeneral(key, effects, descriptions, revert=True)`**
  which **bridges** any ordinary `Effect`s into a passive/measure.

Rule of thumb: writing an **event / resolution / unlock**? Use ordinary `Effect`s.
Writing a **passive / measure**? Use `SituationEffect`s, wrapping ordinary effects
with `SituationEffectGeneral` when you need one that has no native equivalent.

---

## 8. Common patterns

**Reward on event end:** a list of effects on the event — `MoneyEffect`,
`StatEffect`, `ValueEffect`.

**Unlock consequences:** put real effects on the unlockable so a won vote *does*
something — e.g. `BuildingOpenEffect("cafeteria")` for a building, `ValueEffect`/
`SetProficiencyEffect`/`LevelEffect` for a rule.

**One-way cost:** `MoneyEffect("cost", -500, "ADD", EffectNoRevertOption())` — money
spent, never refunded on revert.

**Placeholder while authoring:** `DummyEffect()` in a resolution until the real
effect exists (every resolution needs ≥ 1 effect).

**School-stat change over time:** a `ModifierEffect` with a rhythm collection, or —
inside a situation — `SituationEffectBarChangeModifier` / `SituationEffectRegularStatChange`.

---

## 9. Conventions

- **Compose, don't subclass.** Only write a new `Effect` for a genuinely new kind of
  action (implement `apply`, and `revert` if it can be undone).
- **Give modifier-style effects stable, unique `name`s** — the name is the modifier
  key; a collision silently overwrites.
- **Design revert deliberately.** Decide up front whether an effect is undoable;
  use `EffectNoRevertOption` for permanent changes inside reverting hosts, and
  prefer `ADD` over `SET` when you need clean undo.
- **Character vs. school.** `StatEffect`/`LevelEffect` need a `char_obj`; for school
  stats use the modifier path.
- **Prefer the modern effects** (`UnlockableUnlockEffect` is auto-injected;
  `BuildingOpenEffect`) over the deprecated `RuleEffect`/`ClubEffect`/`BuildingEffect`.
- **Replace `DummyEffect()`** with real effects before shipping.

---

## 10. Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Stat/level effect does nothing | No `char_obj` in the kwargs (character-scoped) | Ensure the host passes a `char_obj`, or use a school-stat modifier path. |
| Revert doesn't undo the change | The effect is a no-op-revert type, or has `EffectNoRevert`, or a *fresh* instance reverted a stored-previous effect | Use a symmetric (`ADD`) effect, keep the same instance, or accept it's one-way by design. |
| Money charged twice on a vote | Missing/incorrect `MoneyEscrow` pairing | Let the Unlockable machinery inject escrow (match `MoneyCondition` ↔ negative `MoneyEffect` by amount). |
| Two modifier effects clash | Same `name` (= modifier key) | Give each a unique name. |
| School stat won't move via `StatEffect` | It's character-scoped | Use `ModifierEffect` / the situation bar-change effects instead. |
| Resolution rejected by self-test | Resolution has no effect | Add at least one effect (`DummyEffect()` at worst). |

---

## 11. Reference tables

### Base contract
`Effect(name, *options)` · abstract `apply(**kwargs)` · `revert(**kwargs)`
(default no-op) · `options` (`EffectNoRevert`, `MoneyEscrow`).

### EffectStorage
`EffectStorage(*effects)` · `apply` / `revert` forward to each in order.

### Modes
`"ADD"` (add value; clean inverse revert) · `"SET"` (set value; best-effort revert).

### Revert behavior by effect
- Inverse: `StatEffect`, `MoneyEffect`
- Stored-previous: `ValueEffect`, `ProgressEffect`, `UnlockableUnlockEffect`
- Add/remove: `BuildingOpenEffect`, `BuildingCloseEffect`, `BlockBuildingEffect`, `ModifierEffect`
- No-op: most others (`NotificationEffect`, `EventEffect`, `DummyEffect`, …)

### Related files
- `game/scripts/effects.rpy` — all effect classes + `EffectStorage`
- `game/scripts/option.rpy` — the `Option` / `OptionSet` system
- [Conditions](Conditions) — the gating counterpart
- `game/scripts/modifier.rpy` — `Modifier_Obj` behind `ModifierEffect`
- [Building Situations](Building-Situations) — `SituationEffect` + `SituationEffectGeneral`
