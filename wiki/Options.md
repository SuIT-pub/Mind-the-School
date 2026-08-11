> **Audience:** Developers who want to fine-tune how a condition, effect, selector or
> event behaves — make a gate soft, keep an effect from reverting, hide an event from
> the map highlight, tag a scene's replay category. This guide covers the `Option`
> contract and the full catalog.
>
> **Scope:** The shared `Option` system (`option.rpy`). Options are **trailing
> modifier flags** accepted by nearly every other primitive:
> [Conditions](Conditions),
> [Effects](Effects),
> [Selectors](Selectors), and
> [Events](Events) / `EventStorage`. Each host decides which
> options it reads — an option only does something where its host looks for it.

---

## Quick start

An Option is a small flag you append after a host's own constructor arguments. Same
object, different meaning per host:

```python
StatCondition(OptionalOption(), corruption=20)               # a soft, always-passing gate
MoneyEffect("cost", -500, "ADD", EffectNoRevertOption())     # spend that is never refunded
Event(3, "secret_scene", TimeCondition(daytime="d"), NoHighlightOption())  # runs, but no map hint
```

- Options are always **positional, after** the host's declared args.
- An option only matters **where its host checks for it** — attaching `EffectNoRevert`
  to a condition does nothing; attaching `Optional` to an effect does nothing.

---

## Contents

1. [What is an Option?](#1-what-is-an-option)
2. [The base contract](#2-the-base-contract)
3. [Three ways an option acts](#3-three-ways-an-option-acts)
4. [Where options attach](#4-where-options-attach)
5. [The option catalog](#5-the-option-catalog)
6. [Conventions](#6-conventions)
7. [Troubleshooting](#7-troubleshooting)
8. [Reference tables](#8-reference-tables)

---

## 1. What is an Option?

An **Option** is a named flag that modifies how its host is evaluated, displayed, or
reverted — without changing the host's core arguments. Options keep the common case
clean (no flag = default behavior) while allowing per-instance tweaks: "this gate is
optional", "don't undo this effect", "don't highlight this event".

Every host stores its options in an **`OptionSet`** and queries it. Because the same
`Option` classes are shared across conditions, effects, selectors and events, the
*meaning* of an option is defined by **which host reads it**, not by the option
itself.

---

## 2. The base contract

`Option(name)` is the base. Each option has:

- **`name`** — the string key the host looks up (`"Optional"`, `"EffectNoRevert"`,
  `"MoneyEscrow"`, …). Two options with the same name collide in an `OptionSet`.
- **`check_option(**kwargs) -> bool`** — a filter hook (default `True`). Used by
  hosts that *filter* by option (events).
- **`get_values() -> dict`** — data an option contributes (default `{}`). Used by
  options that carry a payload (`FragmentRepeat`, `MoneyEscrow`).

Hosts hold an **`OptionSet(*options)`**:

- **`has_option(name)`** — does this option exist? (behavior toggles)
- **`get_option(name)`** — fetch it (to read its payload)
- **`check_options(**kwargs)`** — `True` only if **all** options' `check_option` pass
- **`has_option_subclass(cls)`** — type-based lookup
- `empty_option_set` — the shared empty set.

---

## 3. Three ways an option acts

An option influences its host through one of three mechanisms — knowing which one
tells you *when* it matters:

**a) Behavior toggle (`has_option`).** The host checks for the option by name and
changes what it does. Examples: a condition returns `True` if it has `Optional`; an
effect skips `revert` if it has `EffectNoRevert`; a resolution condition opts out of
latch-key rewriting with `NoOverride`. These act at the moment the host runs.

**b) Availability filter (`check_option` / `check_options`).** The host asks every
option `check_option(**kwargs)` and is only available if all pass. Events use this
for map highlighting and priority buckets — the engine passes context kwargs
(`Highlight`, `ShowBlocked`, `Priority`) and options like `NoHighlight` / `ShowBlocked`
/ `Priority` answer against them.

**c) Value contribution (`get_values`).** The option carries data the host reads —
`MoneyEscrow` provides its `stash_key`, `FragmentRepeat` provides its repeat count.

---

## 4. Where options attach

Every primitive takes trailing `*options`:

| Host | Constructor tail | Reads (examples) |
|------|------------------|------------------|
| Condition | `Condition(*options)` | `Optional`, `NoOverride` |
| Effect | `Effect(name, *options)` | `EffectNoRevert`, `MoneyEscrow` |
| Selector | `Selector(realtime, key, *options)` | `FragmentReroll` |
| Event | `Event(select_type, event, *…|options, …)` | `NoHighlight`, `ForceHighlight`, `ShowBlocked`, `Priority`, `ReplayCategory`, `FragmentRepeat` |
| EventStorage | `EventStorage(name, location, *options, …)` | `EventSeenDebuff` |

An option attached to a host that doesn't read it is simply inert — no error, no
effect.

---

## 5. The option catalog

| Option | Host(s) | Effect |
|--------|---------|--------|
| `OptionalOption()` | Conditions | the condition's `is_fulfilled` always returns `True` — a soft, non-gating marker |
| `EffectNoRevertOption()` | Effects | `revert()` becomes a no-op — the change stays even inside a reverting host (permanent cost / one-way change) |
| `MoneyEscrowOption(stash_key)` | `MoneyEffect` | on apply, consume the reserved PTA-vote stash instead of charging again (auto-attached by the Unlockable machinery) |
| `NoOverrideOption()` | Conditions (in situation resolutions) | keep the condition's own latch/timer key — don't rewrite it to the resolution key |
| `NoHighlightOption()` | Events | exclude the event from the map "available event" highlight (still runnable) |
| `ForceHighlightOption()` | Events | force highlight eligibility even for a priority-3 event that normally wouldn't highlight |
| `ShowBlockedOption()` | Events / hosts | allow the host to be shown while blocked (gated by a `ShowBlocked` kwarg) |
| `PriorityOption(priority)` | Events | the event matches only when the passed `Priority` kwarg equals `priority` (priority-bucketed selection) |
| `EventSeenDebuffOption(debuff=0.25)` | `EventStorage` | lower the re-selection weight of already-seen events by `debuff` (favor fresh content) |
| `ReplayCategoryOption(category)` | Events / fragments | tag the scene into a replay/gallery category (e.g. `"truth_or_dare"`) |
| `FragmentRepeatOption(number, repeatable)` | Event fragments | how many times a fragment repeats and whether it may repeat (`number` may be a `Selector`) |
| `FragmentRerollOption()` | Selectors on fragments | re-roll this selector across fragment boundaries instead of keeping the cached value |

---

## 6. Conventions

- **Attach where it's read.** Check the catalog: put `Optional`/`NoOverride` on
  conditions, `EffectNoRevert`/`MoneyEscrow` on effects, highlight/priority/replay
  options on events. Misplaced options are silently inert.
- **Options are positional and last.** They come after the host's own arguments:
  `Condition(*options)`, `Effect(name, *options)`, etc.
- **Prefer the default.** No option = default behavior; only add one when you need
  the deviation. Don't sprinkle `Optional` to "be safe" — it turns a real gate off.
- **Let the machinery inject `MoneyEscrow`.** Pair a `MoneyCondition` with a negative
  `MoneyEffect` and let the Unlockable code attach the escrow; you rarely construct
  `MoneyEscrowOption` by hand.
- **Tag replayable scenes** with a consistent `ReplayCategoryOption(category)` across
  a storyline's fragments so they group in the gallery.

---

## 7. Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Option seems to do nothing | It's on a host that doesn't read it | Move it to the host that checks it (see §4/§5). |
| A gate never blocks | An `Optional` option is attached | Remove `Optional` if you meant a hard gate. |
| An effect won't undo | `EffectNoRevert` is attached (by design) | Remove it if the change should revert. |
| Event never highlights on the map | `NoHighlight`, or it's priority 3 without `ForceHighlight` | Drop `NoHighlight`, or add `ForceHighlightOption()`. |
| Money charged twice on a vote | `MoneyEscrow` missing/mismatched | Match `MoneyCondition` ↔ negative `MoneyEffect` by amount; let the Unlockable code inject escrow. |
| Two options ignored / one wins | Same `name` — they collide in the `OptionSet` | Don't attach two of the same option to one host. |

---

## 8. Reference tables

### Base contract
`Option(name)` · `check_option(**kwargs)` (filter, default `True`) ·
`get_values()` (payload, default `{}`). `OptionSet`: `has_option(name)` ·
`get_option(name)` · `check_options(**kwargs)` (all) · `has_option_subclass(cls)`.

### Mechanisms
Behavior toggle (`has_option`) · Availability filter (`check_option`) · Value
contribution (`get_values`).

### Quick index
Conditions: `Optional`, `NoOverride` · Effects: `EffectNoRevert`, `MoneyEscrow` ·
Selectors: `FragmentReroll` · Events: `NoHighlight`, `ForceHighlight`, `ShowBlocked`,
`Priority`, `ReplayCategory`, `FragmentRepeat` · EventStorage: `EventSeenDebuff`.

### Related files
- `game/scripts/option.rpy` — the `Option` / `OptionSet` classes
- [Conditions](Conditions) · [Effects](Effects) · [Selectors](Selectors) · [Events](Events) — the hosts
