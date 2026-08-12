> **Audience:** Developers comfortable with Python/Ren'Py who need to gate content
> in *Mind the School* — events, situations, unlockables, effects, votes. This guide
> explains what a Condition is, the base contract, how to combine conditions, the
> shared `Option` system, and the full catalog of condition types.
>
> **Scope:** Conditions only. They are the shared gating primitive used by nearly
> every other system (events, situations, unlockables, selectors, PTA). Those
> systems have their own guides; this one is the reference for the conditions
> themselves.

---

## Quick start

A Condition answers one yes/no question about the game state. You build one and
hand it to whatever system does the gating (an event, a situation threshold, an
unlockable's visibility, …):

```python
# "school level ≥ 2 AND at least $1500 AND the intro event was seen"
AND(
    LevelCondition("2"),
    MoneyCondition("1500+"),
    EventSeenCondition(True, "intro_done"),
)
```

- A bare condition is checked with `condition.is_fulfilled(**kwargs)`.
- A group is checked with `ConditionStorage(*conditions).is_fulfilled(**kwargs)`
  (**all** must pass) — most systems wrap your conditions in a storage for you.
- Combine with `AND` / `OR` / `NOR` / `NOT` / `XOR`.
- While work is in progress, use `PlaceholderCondition()` (never fulfilled).

---

## Contents

1. [What is a Condition?](#1-what-is-a-condition)
2. [The base contract](#2-the-base-contract)
3. [ConditionStorage](#3-conditionstorage)
4. [Logic combinators](#4-logic-combinators)
5. [Options](#5-options)
6. [The condition catalog](#6-the-condition-catalog)
7. [Common patterns](#7-common-patterns)
8. [Conventions](#8-conventions)
9. [Troubleshooting](#9-troubleshooting)
10. [Reference tables](#10-reference-tables)

---

## 1. What is a Condition?

A **Condition** is a small object that evaluates the game state and returns
`True`/`False`. It is the universal gating primitive: events use conditions to
decide when they can fire, situation thresholds use them as gate conditions, teasers
use them as unlock triggers, unlockables use them for visibility, PTA votes use them
for cost gates, and so on.

Conditions are **declarative and reusable**. You never subclass to gate ordinary
content — you compose the existing types. Because everything is coupled only through
keys and conditions, a mod can gate on base content and vice versa.

---

## 2. The base contract

Every condition subclasses `Condition(*options)`:

- **`check_condition(**kwargs) -> bool`** (abstract) — the actual test. Subclasses
  implement this.
- **`is_fulfilled(**kwargs) -> bool`** — the public entry point. It wraps
  `check_condition` with universal short-circuits: it returns **`True`** in replay
  mode / journal gallery (`in_replay`, `check_in_replay`, `in_journal_gallery`), and
  **`True`** if the condition carries the `Optional` option. Otherwise it delegates
  to `check_condition`. **Call `is_fulfilled`, not `check_condition`.**
- **`get_name() -> str`** (abstract) — a human-readable identifier, used in logs and
  default description text.
- **`type`** (property, on many subclasses) — a string tag (`"stat"`, `"money"`,
  `"timer"`, …) used by `find_by_type` to pull specific conditions back out of a
  storage.

`**kwargs` carry the evaluation context — most importantly `char_obj` (the character
or school the condition applies to; defaults to the school), plus event/selector
data. Conditions read what they need and ignore the rest.

Display hooks (mostly for the journal): `display_in_list` / `display_in_desc` flags
(default `False`; set `True` by display-worthy subclasses like `StatCondition`),
`to_list_text` / `to_desc_text`, and `get_diff` / `calculate_probability` (how close
to fulfilled — feeds vote probability and sorting).

> **Note:** "Blocking" is **not** a Condition concept. The old blocking attribute that
> once controlled journal display was removed — a condition's own visibility is driven
> by `display_in_list` / `display_in_desc` (above). Situation *blocking thresholds* are
> an unrelated, threshold-level mechanic and live in the [Situations](Building-Situations)
> guide, not here.

---

## 3. ConditionStorage

`ConditionStorage(*conditions)` is the container systems use to hold a set of
conditions. Key behavior:

- **`is_fulfilled(**kwargs)`** — **AND** semantics: `True` only if **every** member
  is fulfilled. (An empty storage is `True`.)
- **`add_conditions(*conditions)` / `add_condition(c)` / `add_storage(other)`** —
  build it up incrementally; duplicates (same object) are skipped.
- **`find_by_type(type)`** — returns all members whose `type` matches (recursing
  into combinators). This is how systems extract, e.g., the `TimerCondition` or
  `MoneyCondition` out of a mixed list.
- Sorts members into `list_conditions` / `desc_conditions` for the journal, and
  tracks whether a `LockCondition` is present (`is_locked`).

You rarely construct a storage yourself for gating — you pass a list of conditions
to a system and it wraps them. You *do* use `ConditionStorage` when writing a system
that gates on author-supplied conditions.

---

## 4. Logic combinators

Conditions compose. Each combinator is itself a `Condition`, so it nests anywhere a
condition is accepted:

| Combinator | Fulfilled when |
|-----------|----------------|
| `AND(*conditions)` | **all** are fulfilled |
| `OR(*conditions)` | **at least one** is fulfilled |
| `NOR(*conditions)` | **none** are fulfilled |
| `NOT(condition)` | the single inner condition is **not** fulfilled |
| `XOR(*conditions)` | an **odd** number are fulfilled (exclusive) |

```python
OR(
    AND(LevelCondition("3"), EventSeenCondition(True, "sb_event_3")),
    MoneyCondition("5000+"),
)
```

Note: a bare `ConditionStorage` / a plain condition list is already an implicit
`AND`. Use the explicit `AND(...)` only when you need it *inside* an `OR`/`NOT`/etc.

---

## 5. Options

Both conditions and effects accept trailing `*options` (from `option.rpy`). An
`Option` tweaks how the host is evaluated or displayed — see the
[Options](Options) guide for the full shared catalog. The
condition-relevant ones:

| Option | Effect on a condition |
|--------|-----------------------|
| `OptionalOption()` (`"Optional"`) | `is_fulfilled` always returns `True` — a soft, non-gating marker |
| `ShowBlockedOption()` | let the host show even while blocked (host-interpreted) |
| `NoHighlightOption()` / `ForceHighlightOption()` | control map/journal highlighting of the host |
| `PriorityOption(priority)` | tag the host with a priority bucket (events) |
| `NoOverrideOption()` | opt out of override/latch key rewriting (e.g. resolution latches) |

Other options are event- or effect-specific (`FragmentRepeatOption`,
`EffectNoRevertOption`, `MoneyEscrowOption`, …) — see the
[Options](Options) guide. Options are passed positionally after
the constructor's own args: `StatCondition(OptionalOption(), corruption=20)`.

---

## 6. The condition catalog

All constructors below are `Condition` subclasses. `*options` is always accepted
last.

### Stats, levels & proficiency

| Constructor | Checks |
|-------------|--------|
| `StatCondition(*options, char_obj=None, **stats)` | each `stat=threshold` kwarg is met on `char_obj` (default school), e.g. `StatCondition(corruption=20, happiness=50)` |
| `StatLimitCondition(stat, char_obj=None, *options)` | the stat is at its current level cap |
| `LevelCondition(value, *options, char_obj=None)` | character/school level meets `value` (e.g. `"2"`, `"2+"`) |
| `ProficiencyCondition(proficiency, *options, xp=-1, level=-1)` | a proficiency's xp/level threshold |
| `MaxLevelEventCondition(value, *options)` | max-level event progress |

### Money & items

| Constructor | Checks |
|-------------|--------|
| `MoneyCondition(value, *options)` | available money meets `value` (number = minimum; string like `"1500+"` / `">=1000"`) |
| `ItemCondition(item_key, amount=1, *options)` | at least `amount` of an inventory item |
| `DeliveryCondition(*options)` | a delivery is available |

### Game data, values & comparisons

| Constructor | Checks |
|-------------|--------|
| `GameDataCondition(key, value, *options)` | a GameData entry equals `value` |
| `BoolCondition(value, *options)` | a constant `True`/`False` (useful as a fixed gate) |
| `ValueCondition(key, value, *options)` | a registered value equals `value` |
| `NumValueCondition(key, value, *options)` | a numeric value meets `value` (accepts a `Selector`) |
| `NumCompareCondition(key, value, operation, *options)` | numeric compare (`operation` ∈ `>`, `<`, `>=`, …) |
| `CompareCondition(key, value, *options)` | generic equality compare (accepts a `Selector`) |
| `KeyCompareCondition(key_1, key_2, operation, *options)` | compare two keys against each other |
| `ProgressCondition(key, value="", *options)` | an event-series progress step |

### Time & timers

| Constructor | Checks |
|-------------|--------|
| `TimeCondition(*options, **when)` | calendar match via `day` / `week` / `month` / `year` / `daytime` / `weekday` / `date`; each defaults to `"x"` (any); `condition` = `"+"`/`"-"`/`""` for ≥ / ≤ / = |
| `TimerCondition(id, *options, **span)` | a named countdown timer (set elsewhere) has elapsed by `day=` / `daytime=` / … — also the standard **duration / cooldown / grace** primitive for situations |
| `DaytimeChangedCondition(*options)` | the daytime segment just changed |

### Counters & latches

| Constructor | Checks |
|-------------|--------|
| `ManualCounterCondition(counter_key, max=1, *options)` | a manually-incremented counter is below `max` (hard quota; used by measures) |
| `CounterCondition(counter_key, condition, max=1, *options)` | counts edges of `condition` up to `max` |
| `LatchCounterCondition(counter_key, max=1, *options)` | a latch that fires after `max` falling edges (grace counts) |
| `ManualCondition(is_fulfilled, *options)` | a fixed boolean you set at construction |

### Events, story & replay

| Constructor | Checks |
|-------------|--------|
| `EventSeenCondition(seen=False, event_name="", *options)` | whether `event_name` has been seen matches `seen` |
| `IntroCondition(is_intro=True, *options)` | whether the intro is (not) running |
| `TutorialCondition(*options)` | tutorial state |
| `CheckReplay(condition, *options)` | wraps a condition so it also evaluates in replay |
| `RandomCondition(threshold, limit=100, *options)` | a random roll below `threshold` out of `limit` (probabilistic gate) |

### Situations, unlockables & PTA

| Constructor | Checks |
|-------------|--------|
| `SituationPoolCondition(situation_key, pool_key, *options)` | a situation's event pool is active (bar in range) |
| `ThresholdReachedCondition(situation_key, threshold_key, *options)` | a situation threshold has been reached |
| `UnlockableCondition(unlockable_key, group_index=-1, *options)` | an unlockable (optionally a group level) is unlocked |
| `BuildingCondition(key, *options)` | a map building is currently open |
| `HasAnythingInCollectionGameDataCondition(collection_key, *options)` | a GameData collection is non-empty (backs building open/closed) |
| `VoteProposalFreeCondition(*options)` | no PTA proposal is currently scheduled (gate for Schedule Vote) |
| `JournalVoteCondition(journal_obj, *options)` / `JournalNRVoteCondition(*options)` | PTA vote journal state |

### Gating helpers

| Constructor | Purpose |
|-------------|---------|
| `PlaceholderCondition(*options)` | never fulfilled — WIP marker until a real condition exists |
| `LockCondition(*options)` | marks the host as hard-locked (`ConditionStorage.is_locked`) |

> **Deprecated (as of 0.2.3 — replaced by the Unlockables system, kept only for save
> compatibility):** `RuleCondition(value, …)`, `ClubCondition(value, …)`,
> `BuildingLevelCondition(name, level, …)` and `PTAOverride(char, accept, …)`. The
> rule/club conditions are effectively always-false stubs. **Use `UnlockableCondition`
> instead** (and `BuildingCondition` for building state).

---

## 7. Common patterns

**Gate on multiple stats:** one `StatCondition` takes several stat kwargs (implicit
AND across them):
```python
StatCondition(corruption=30, inhibition=20)
```

**Probabilistic appearance:** `RandomCondition(35)` ≈ a 35 % chance gate — often
combined with hard requirements via `AND`.

**Duration / cooldown / grace (situations):** `TimerCondition("my_id", daytime=3)`.
The situation/measure machinery starts and reads the timer; you just declare it.

**"Not yet done":** `NOT(EventSeenCondition(True, "some_event"))`, or simply
`EventSeenCondition(False, "some_event")`.

**Mixed AND/OR:** compose explicitly:
```python
AND(LevelCondition("3"), OR(MoneyCondition("2000+"), UnlockableCondition("grant")))
```

**WIP gate:** `PlaceholderCondition()` — the host stays uncompletable until you
replace it. (Some hosts self-test that they carry ≥ 1 condition — e.g. situation
gate thresholds and teasers; a placeholder satisfies "has a condition" but never
fires, so the gate can never pass until you replace it.)

---

## 8. Conventions

- **Compose, don't subclass.** Gate ordinary content with the existing types +
  combinators. Only write a new `Condition` subclass for a genuinely new *kind* of
  check (then implement `check_condition` + `get_name`, and add a `type` if it
  should be `find_by_type`-discoverable).
- **Call `is_fulfilled`, never `check_condition`.** Only `is_fulfilled` honors
  replay/gallery/`Optional`.
- **Keys are identity.** Condition arguments reference keys (`event_name`,
  `situation_key`, GameData `key`, unlockable key). Use the real, stable keys; a
  typo silently makes the gate unsatisfiable.
- **Prefer `UnlockableCondition` / `BuildingCondition`** over the legacy
  `RuleCondition` / `ClubCondition`.
- **Placeholders are temporary.** Replace every `PlaceholderCondition()` before
  shipping — grep for them.

---

## 9. Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Gate never passes | Wrong/typo'd key, or a `PlaceholderCondition()` still in place | Verify the key exists; replace placeholders. |
| Gate passes when it shouldn't | You're in replay/gallery (`is_fulfilled` returns `True` there), or an `Optional` option is attached | Expected in replay; drop `Optional` if you meant a hard gate. |
| Stat gate ignored for a character | `char_obj` mismatch — a condition bound to one character returns `True` for others | Pass the intended `char_obj`, or leave it unbound to use the context/school. |
| `find_by_type` returns nothing | The condition type has no `type` tag, or the tag string differs | Check the subclass's `type` property; combinators recurse, plain lists don't. |
| Timer/counter never elapses | Nobody sets/increments it — `TimerCondition`/`ManualCounterCondition` only *read* state | Ensure the owning system (measure, situation) starts the timer / increments the counter. |

---

## 10. Reference tables

### Base contract
`Condition(*options)` · abstract `check_condition` + `get_name` ·
public `is_fulfilled` · `type` → `find_by_type` ·
`display_in_list` / `display_in_desc` + `to_list_text` / `to_desc_text`.

### ConditionStorage
`is_fulfilled` = AND · `add_conditions` /
`add_condition` / `add_storage` · `find_by_type` · `get_conditions`.

### Combinators
`AND` · `OR` · `NOR` · `NOT(single)` · `XOR` (odd count).

### Comparison operators (Num/Key compare)
`>` · `<` · `>=` · `<=` · `==` (and the string-suffix form on `MoneyCondition` /
`LevelCondition`, e.g. `"1500+"`).

### Time / timer keys
`day` · `week` · `month` · `year` · `daytime` · `weekday` · `date` · `condition`
(`+`/`-`/``) for `TimeCondition`; span keys `day=` / `daytime=` / … for
`TimerCondition`.

### Related files
- `game/scripts/conditions.rpy` — all condition classes + `ConditionStorage`
- `game/scripts/option.rpy` — the `Option` / `OptionSet` system
- `game/scripts/selector.rpy` — `Selector`s (some conditions accept one as `value`)
- `game/scripts/effects.rpy` — the counterpart: `Effect`s (what happens when a gate passes)
