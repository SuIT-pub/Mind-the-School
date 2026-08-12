> **Audience:** Developers who need to bend how stats change in *Mind the School* —
> scale incoming changes, add recurring drift, or (via situations) move a bar over
> time. This guide covers `Modifier_Obj`, the operator set, modifier collections and
> rhythms, and the range-based operators.
>
> **Scope:** The modifier engine (`modifier.rpy`). You usually touch it *indirectly*
> — through a `ModifierEffect` ([Effects](Effects)) or the
> situation `SituationEffectStatChangeModifier` / `SituationEffectBarChangeModifier`
> / `SituationEffectRegularStatChange` types (Situations guide). This guide explains
> what those are driving underneath.

---

## Quick start

A modifier is an operator + value registered on a stat inside a named collection.
The **collection** decides *when* it acts:

```python
# +2 Happiness every in-game day (recurring drift), via a ModifierEffect:
ModifierEffect("morale_boost", HAPPINESS, Modifier_Obj("morale_boost", "+", 2), "daily")

# Scale all incoming Corruption changes by 1.5x while active (transform-on-change):
ModifierEffect("corruption_amp", CORRUPTION, Modifier_Obj("corruption_amp", "*", 1.5), "default")
```

- **`default`** collection → transforms stat *changes* as they happen.
- **rhythm** collections (`daytime_change`, `daily`, `weekly`, `monthly`, `yearly`)
  → apply a recurring change once per that period.
- Operators: `+`, `*`, `value_percent`, `range_percent`, `gated_percent`
  (`%` = legacy alias of `value_percent`).

---

## Contents

1. [What is a Modifier?](#1-what-is-a-modifier)
2. [Operators](#2-operators)
3. [Collections & rhythms](#3-collections--rhythms)
4. [How modifiers are applied](#4-how-modifiers-are-applied)
5. [Registering modifiers](#5-registering-modifiers)
6. [Situation bars as modifier targets](#6-situation-bars-as-modifier-targets)
7. [Conventions](#7-conventions)
8. [Troubleshooting](#8-troubleshooting)
9. [Reference tables](#9-reference-tables)

---

## 1. What is a Modifier?

A **`Modifier_Obj(name, mod_type, value)`** is a tiny rule that alters a numeric
change:

- **`name`** — the modifier's key/identity within its collection. Registering
  another modifier with the same name on the same stat/collection **overwrites** it.
- **`mod_type`** — the operator (see below).
- **`value`** — the operand.

Modifiers live in **collections**: a two-level map `collection → stat → {name:
Modifier_Obj}`. They never change a stat by themselves — they are consulted when the
stat system computes a change, and they add their contribution.

The target can be a **school stat** (`HAPPINESS`, `CORRUPTION`, …) or a **situation
bar** via the pseudo-stat key `situation:<situation_key>:<bar_key>` (see §6).

---

## 2. Operators

`Modifier_Obj.calculate_change(base_value, range_stat)` evaluates the operator
against the value being changed. `base_value` is the incoming change (or `0` for a
recurring rhythm tick). `range_stat` is the stat/bar whose range the percent
operators measure against (defaults to the target itself).

| Operator | Contribution | At `base = 0` (rhythm tick) |
|----------|--------------|------------------------------|
| `+` | `value` (flat) | contributes `value` |
| `*` | `value × base` | fizzles (0) |
| `value_percent` (`%`) | `base/100 × value` — a percent of the current change/value | fizzles |
| `range_percent` | `value/100 × full_range` — a percent of the target's whole min→max range | **contributes** |
| `gated_percent` | `value/100 × gated_range` — a percent of the range up to the current cap | **contributes** |

`%` is normalized to `value_percent` automatically (legacy alias). The range
operators resolve against `range_stat` → the target's own range if not overridden,
so `range_percent` on `HAPPINESS` uses the Happiness range, and on a situation bar
uses that bar's `limits`.

> **Consequence for recurring modifiers:** on a per-tick rhythm (base `0`), only
> `+`, `range_percent`, and `gated_percent` do anything — `*` and `value_percent`
> need a non-zero base and are meant for the transform-on-change (`default`) role.

---

## 3. Collections & rhythms

The collection a modifier lives in decides *when* it fires:

| Collection | Role |
|-----------|------|
| `default` | consulted whenever that stat undergoes a change — **transforms the change** (scale it, add to it) |
| `daytime_change` | applied once at each daytime-segment change |
| `daily` / `weekly` / `monthly` / `yearly` | applied once per that calendar period |
| `payroll_weekly` / `payroll_monthly` / `payroll_yearly` | payroll income buckets (money) |

The rhythm collections are the **recurring stat change** mechanism: a `+` modifier in
`daily` drifts the stat by `value` every day for as long as it's registered.

---

## 4. How modifiers are applied

- **On a stat change** (`change_stat_with_modifier(stat, value, collection)` /
  `change_stats_with_modifier(collection, **kwargs)`): the modifiers in `collection`
  for that stat transform the incoming `value` (via `apply_stat_modifier` →
  `get_total_stat_modifier_change`), then the stat is changed by the result.
- **On a time tick** (`change_stats_via_modifier(collection)`, called from the daily
  checks for each rhythm): every stat in that collection is changed with `base = 0`,
  i.e. each modifier contributes its recurring amount.

You don't call these yourself in ordinary content — the stat system and the daily
checks do. What you control is **which modifiers exist in which collection**.

---

## 5. Registering modifiers

Three ways, from lowest- to highest-level:

**a) Directly** (rare, for systems code):
```python
set_modifier("morale_boost", Modifier_Obj("morale_boost", "+", 2), stat=HAPPINESS, collection="daily")
remove_modifier("morale_boost", HAPPINESS, "daily")
```

**b) As an `Effect`** — `ModifierEffect(key, stat, mod_obj, collection="default")`.
Its `apply` registers the modifier, its `revert` removes it. Use this in event /
resolution effect lists. (See the Effects guide.)

**c) As a `SituationEffect`** (inside a situation passive/measure) — the recommended
path when working on a situation:
- `SituationEffectStatChangeModifier(stat, value, op)` — a `default`-collection stat
  modifier tied to the situation lifecycle.
- `SituationEffectRegularStatChange(stat, value, rhythm)` — a recurring rhythm stat
  change.
- `SituationEffectBarChangeModifier(bar, value, op, interval)` — recurring drift on
  one of the situation's own bars.

These register through the situation's lifecycle registry, so they are reverted /
hibernated correctly on passive switch, measure expiry, reload, and mod removal.

### Orphan risk: lifecycle vs. global registration

`set_modifier` and `ModifierEffect` register into the **global** modifier
collections, which have **no connection to any situation's lifecycle**. That is fine
in events / resolutions — an event is a one-shot, and a `ModifierEffect`'s own
`revert` removes the modifier again. Inside a **situation** passive/measure it is a
trap:

- If a modifier is registered outside the lifecycle registry and the situation is
  later torn down — passive switched, measure expired, save reloaded, or the owning
  **mod disabled** — nobody removes it. The modifier is **orphaned** and keeps
  affecting the stat/bar indefinitely, with no owner left to revert it.
- This is exactly why `SituationEffectGeneral` **rejects `ModifierEffect`** (it
  filters it out at construction and logs an error): wrapping one would smuggle a
  global registration past the lifecycle registry and reintroduce the orphan.

**Rule:** inside a situation, never register modifiers by hand or via `ModifierEffect`.
Use the lifecycle-tracked `SituationEffectStatChangeModifier` /
`SituationEffectBarChangeModifier` / `SituationEffectRegularStatChange` — they are
swept correctly on every teardown path. Reserve `set_modifier` / `ModifierEffect` for
non-situation contexts where you own the removal.

### Managed modifiers — orphan-safe registration outside situations

For that "own the removal" case there is a ready-made, orphan-safe path that reuses
the **same lifecycle registry** the situations ride on — no hand-wiring. Three calls:

| When | Call |
|------|------|
| **On activation** (once, when your mod turns the modifier on) | `track_managed_modifier(key, mod_obj, owner, *, category=None, stat="all", collection="default")` — applies the modifier *and* records an ownership entry. |
| **Every load wave, once per modifier** (from a `register_start_method` label — those run *inside* the check wave) | `keep_managed_modifier(key)` — KEEP-pings that one entry so it survives the sweep. |
| **On deactivation** (optional, deliberate off) | `remove_managed_modifier(key)` — removes it from the modifier system and drops the entry. |

> **Keep each modifier individually — never in bulk.** The sweep is only meaningful
> because every modifier must be *re-affirmed* each wave by the code path that still
> wants it. Ping the keys you still want, one by one; anything you don't re-ping
> (feature turned off, key retired, whole mod disabled) is swept. A blanket "keep all
> my entries" call would instead keep stale keys alive forever — reintroducing the
> exact orphans the registry exists to prevent.

```python
# once, when your mod activates the bonus:
track_managed_modifier(
    "mymod_happiness_boost",
    Modifier_Obj("mymod_happiness_boost", "+", 2),
    owner="mymod",
    stat=HAPPINESS, collection="daily",
)

# a label you register once — register_start_method("mymod_keep_alive").
# Re-affirm each modifier your mod still wants, guarded by your own logic:
label mymod_keep_alive:
    if mymod_bonus_active:
        $ keep_managed_modifier("mymod_happiness_boost")
    # not pinged when the bonus is off → swept at the next finalize_check
    return
```

Both the modifier (in `stat_modifier` game data) and its registry entry **persist
across saves**, so the wave hook only KEEP-pings — it never re-applies. Drop the reason
(or the whole mod) and the un-pinged modifiers are removed for you at the next
`finalize_check` sweep. That is the whole orphan guarantee — the identical machinery
the situation modifier effects use, exposed for mod/systems code.

> **Events have their own wrapper.** An event can install a lasting modifier without
> wiring any of this by hand: attach a `ModifierSelector` and call `load_modifier("key")`
> in its label. The event owns the modifier, and the event system re-affirms it each
> wave via `check_selectors` — same keep/sweep guarantee. See [Events](Events) §13 and
> [Selectors](Selectors).

> **Situation resolutions too.** A `ModifierEffect` placed in a resolution's effect list
> is registered on fire and re-affirmed each wave by the resolution's `update_data` — the
> same guarantee, surviving even after the Situation completes. See
> [Building Situations](Building-Situations) §14.

---

## 6. Situation bars as modifier targets

A situation bar is addressable as a pseudo-stat: `situation:<situation_key>:<bar_key>`.
The whole modifier machinery accepts this key, so a modifier (or a bar-change
effect) drifts the bar exactly like a stat. Two extras:

- **`ALL` fan-out:** `situation:<key>:ALL` applies to **every** bar of the situation
  (used by the Unlockable *Persuade* measure).
- **Range operators** resolve against the bar's `limits`, so `range_percent` on a
  bar means "x % of that bar's span".

See the Situations guide (§3, §13) for moving bars from events and the full picture.

---

## 7. Conventions

- **Unique names.** A modifier's `name` is its key in its collection; a duplicate
  silently overwrites. Namespace them (`mymod_...`, `<situation>:<bar>:...`).
- **Pick the collection by intent.** `default` = "reshape changes to this stat";
  a rhythm = "recurring drift". Don't put a `*`/`value_percent` modifier in a rhythm
  collection expecting per-tick effect — it fizzles at base 0.
- **Prefer the managed paths.** In a situation, use the `SituationEffect*` modifier
  types (lifecycle-tracked) over raw `set_modifier`; in events/resolutions use
  `ModifierEffect` (revertable). Raw `set_modifier` leaves you to manage removal.
- **Remember revert = "stop", not "undo".** Removing a rhythm modifier stops future
  ticks; it does not claw back the change already accumulated.
- **Use `range_percent`/`gated_percent` for zero-centered targets** (like a bar that
  starts at 0) — `*` and `value_percent` fizzle there.

---

## 8. Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Recurring modifier does nothing per tick | It uses `*` or `value_percent` (fizzles at base 0) | Use `+`, `range_percent`, or `gated_percent` for rhythm collections. |
| Modifier never stops | Registered via raw `set_modifier` and never removed | Use `ModifierEffect`/`SituationEffect*` (auto-revert), or call `remove_modifier`. |
| Two modifiers clash / one vanishes | Same `name` on the same stat+collection | Give unique names. |
| `range_percent` has no effect on a school stat | Range couldn't resolve | It defaults to the stat's own range; verify the stat/bar key is valid. |
| Bar modifier targets the wrong bar | Wrong `situation:<key>:<bar>` key, or you meant `ALL` | Check the key; use `:ALL` to hit every bar. |
| Ghost modifier after disabling a mod | Orphaned registration | Situation-owned modifiers are swept by the lifecycle registry; raw ones must be removed explicitly. |

---

## 9. Reference tables

### Modifier object
`Modifier_Obj(name, mod_type, value)` · `calculate_change(base_value, range_stat)` ·
`get_change()` (display string).

### Operators
`+` · `*` · `value_percent` (`%` legacy) · `range_percent` · `gated_percent`.
Range ops measure against `range_stat` (defaults to the target).

### Collections
`default` (transform-on-change) · `daytime_change` · `daily` · `weekly` · `monthly`
· `yearly` · `payroll_weekly` · `payroll_monthly` · `payroll_yearly`.

### Registration
`set_modifier(key, mod_obj, stat="all", collection)` / `remove_modifier(key, stat, collection)`
· `ModifierEffect(key, stat, mod_obj, collection)` · situation:
`SituationEffectStatChangeModifier` / `SituationEffectRegularStatChange` /
`SituationEffectBarChangeModifier`.

### Managed modifiers (orphan-safe, outside situations)
`track_managed_modifier(key, mod_obj, owner, *, category=None, stat="all", collection="default")`
(activate) · `keep_managed_modifier(key)` (per modifier, each load wave from a
`register_start_method` label) · `remove_managed_modifier(key)` (deactivate).

### Related files
- `game/scripts/modifier.rpy` — `Modifier_Obj`, collections, `set_modifier`, `change_stat*_modifier`
- `game/scripts/daily_check.rpy` — where rhythm collections are applied each tick
- `game/scripts/effects.rpy` — `ModifierEffect`
- [Building Situations](Building-Situations) — situation stat/bar modifier effects & bar targets
