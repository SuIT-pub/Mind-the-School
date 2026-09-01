> **Audience:** Developers writing *Mind the School* events who need **dynamic
> values** — a random outfit variant, the acting character, a stat reading, a
> time-of-day — computed at runtime and woven into image paths, dialogue, effects
> and conditions.
>
> **Scope:** The selector system (`selector.rpy`). Selectors are an event-authoring
> tool: they produce values that land in the event's `kwargs`. They pair with
> [Events](Events) (which run them), and some
> [Conditions](Conditions) / [Effects](Effects)
> accept a `Selector` in place of a fixed value.

---

## Quick start

A Selector computes a value under a **key**; that key becomes a kwarg the rest of
the event can read:

```python
SelectorSet(
    CharacterSelector("char"),                      # pick the acting character → kwargs["char"]
    RandomValueSelector("variant", 1, 4),           # random 1..4 → kwargs["variant"]
    StatSelector("corr", CORRUPTION, "char", [0, 100]),  # a stat reading (+ "corr_range")
)
```

Downstream you reference those keys:

- in **image paths**: `"images/scene/<char>/pose_<variant>.webp"` (resolved by
  `refine_image`/`get_image`);
- in **Ren'Py text**: `"[char] looks away."`;
- as **values** passed into conditions/effects that accept a `Selector`.

---

## Contents

1. [What is a Selector?](#1-what-is-a-selector)
2. [The base contract](#2-the-base-contract)
3. [SelectorSet & how values reach kwargs](#3-selectorset--how-values-reach-kwargs)
4. [realtime vs. cached, and rerolling](#4-realtime-vs-cached-and-rerolling)
5. [Nesting selectors](#5-nesting-selectors)
6. [The selector catalog](#6-the-selector-catalog)
7. [Using selector values downstream](#7-using-selector-values-downstream)
8. [Conventions](#8-conventions)
9. [Troubleshooting](#9-troubleshooting)
10. [Reference tables](#10-reference-tables)

---

## 1. What is a Selector?

A **Selector** produces a value at runtime and stores it in the event `kwargs` under
a key. That is how an event stays generic: instead of hard-coding "Yuriko" or
"variant 2", you declare *how to pick* and let the selector roll it when the event
runs. The result flows into image resolution, dialogue interpolation, and any
condition/effect that reads the kwarg.

Selectors are almost always attached to events (via a `SelectorSet`). They are a
content-authoring convenience, not a gameplay system of their own.

---

## 2. The base contract

Every selector subclasses `Selector(realtime, key, *options)`:

- **`key`** — the kwarg name the value is stored under (`get_name()` returns it).
- **`roll(**kwargs) -> Any`** (abstract) — compute a fresh value.
- **`get_value(**kwargs)`** — return the value; rolls first if `realtime` or if no
  value is cached yet.
- **`update(**kwargs)`** — force a re-roll (caches the result).
- **`options`** — trailing `*options` (`OptionSet`); see the
  [Options](Options) guide (e.g. `FragmentReroll`).

You read values through `get_value` (or, in practice, through the `SelectorSet`);
never poke `_value` directly.

---

## 3. SelectorSet & how values reach kwargs

`SelectorSet(*selectors)` is the container an event holds. Its job is to turn the
selectors into kwargs:

- **`get_values(**kwargs) -> dict`** — merges every selector's `key: value` into
  `kwargs` and returns it (rolling once if not yet rolled). This is what feeds the
  event.
- **`roll_values(**kwargs)`** — re-rolls all selectors and re-merges.
- **`add_selector(*selectors)`** — extend the set.

Two selectors are merged specially:

- **`KwargsSelector`** contributes **multiple** keys at once (not one `key: value`).
- **`StatSelector`** contributes both `key` and `key + "_range"` (so downstream can
  scale against the stat's range).

---

## 4. realtime vs. cached, and rerolling

- **Cached** (`realtime=False`, the default for most) — the value is rolled once and
  stays fixed for the event, so an image path and the dialogue that reference the
  same key agree.
- **Realtime** (`realtime=True`) — re-rolled on every `get_value`. `StatSelector`
  defaults to realtime (a stat reading should be current); use realtime only when
  you truly want a fresh value each access.

`reroll_selectors()` re-rolls every selector queued in the global `rerollSelectors`
list — used to refresh values across a parenting/fragment boundary so a follow-up
scene can pick new values.

---

## 5. Nesting selectors

Selectors compose. Wherever a selector takes a value, that value may itself be a
`Selector`, and it gets rolled recursively:

- `RandomListSelector("x", "a", "b", AnotherSelector(...))` — if the nested selector
  is chosen, it rolls and its result is used.
- Many selectors accept `str | Selector` for their target (e.g. `StatSelector`'s
  `stat`/`char`, `LevelSelector`'s `char`) — so the character or stat to read can
  itself be selected dynamically.

This lets you build "pick a character, then read *that* character's stat" without
hard-coding the link.

---

## 6. The selector catalog

`realtime` defaults to `False` unless noted; `*options` accepted last.

### Random & lists

| Constructor | Produces |
|-------------|----------|
| `RandomListSelector(key, *values, realtime=False, alt=None, options=[])` | a random pick from `values` (nested selectors roll; `alt` if empty) |
| `IterativeListSelector(key, *values, realtime=False, options=[])` | the next value in order each roll |
| `RandomValueSelector(key, min_value, max_value, realtime=False, *options)` | a random integer in `[min, max]` |

### State readings

| Constructor | Produces |
|-------------|----------|
| `StatSelector(key, stat, char, stat_range, realtime=True, *options)` | a character's stat value (+ `key_range`); `stat`/`char` may be selectors |
| `LevelSelector(key, char, *options)` | a character's level (`"school"` → campus climate; see [School Levels](School-Levels)) |
| `CharacterSelector(key, char='school', *options)` | resolve a character reference |
| `TimeSelector(key, time_type, *options)` | a time component (`day`/`daytime`/…) |
| `BuildingLevelSelector(key, building, *options)` | a building's level |

### Data & values

| Constructor | Produces |
|-------------|----------|
| `ValueSelector(key, value, *options)` | a fixed value (wrap a constant as a selector) |
| `GameDataSelector(key, index, alt=None, *options)` | a GameData entry (`alt` fallback) |
| `DictSelector(key, index, dict, *options)` | a lookup into a provided dict |
| `KwargsValueSelector(key, kwargs_key, *options)` | copy another kwarg's value under `key` |
| `ProgressSelector(key, index, *options)` | an event-series progress value |
| `NumClampSelector(key, value, *options, min_value=-1, max_value=-1)` | clamp a number/selector into a range |

### Conditional & multi

| Constructor | Produces |
|-------------|----------|
| `ConditionSelector(key, condition, true_value, false_value, realtime=False, *options)` | `true_value` if the `Condition` holds, else `false_value` (either may be a selector) |
| `KwargsSelector(*options, **kwargs)` | injects several fixed `key=value` kwargs at once |

### Unlockables & PTA

| Constructor | Produces |
|-------------|----------|
| `BuildingUnlockedSelector(key, building, *options)` | whether a map building is unlocked |
| `PTAVoteSelector(key, condition_type='misc', *options)` | a PTA vote value by category |
| `PTAObjectSelector(key, *options)` | the current PTA object under vote |

> **Legacy:** `RuleUnlockedSelector` / `ClubUnlockedSelector` target the retired
> rules/clubs system. Prefer reading unlock state via an `UnlockableCondition`
> (or a `GameDataSelector` on the unlocked flag) instead.

### Modifiers (deferred activation)

| Constructor | Produces |
|-------------|----------|
| `ModifierSelector(key, modifier, stat, *options, collection="default")` | a `(modifier, stat, collection)` triple for **deferred** modifier activation — *not* an image/text value |

Unlike every selector above, a `ModifierSelector`'s value is never substituted into art
or dialogue. It carries a `Modifier_Obj` that the event **activates on demand** by
calling `load_modifier("key", **kwargs)` in its scene label. `load_modifier` applies the
modifier *and* registers it with the lifecycle registry, owned by the event — so it is
orphan-safe: kept alive while the event stays registered, swept if the event goes away.
Give each `ModifierSelector` on an event a **distinct key** (it becomes part of the
modifier's registry key `"<event>:<key>"`). Full flow: [Events](Events) §13 and
[Modifiers](Modifiers).

---

## 7. Using selector values downstream

Once a selector has put `key: value` into the kwargs:

- **Image paths** substitute `<key>` — `refine_image` / `get_image` replace every
  `<key>` with its kwarg value (this is how variants, characters and levels select
  the right art). `StatSelector`'s `key_range` is available for range-based art.
- **Dialogue** uses Ren'Py interpolation — `"[key]"`.
- **Conditions/effects** that accept `Union[..., Selector]` (e.g. `NumValueCondition`,
  `CompareCondition`, `NumClampSelector`) can be handed a selector directly, or read
  the resulting kwarg by key.

Because everything travels as kwargs, a selector defined once drives art, text and
logic consistently within the event.

---

## 8. Conventions

- **One key, one meaning.** A selector's `key` is a kwarg name; keep it descriptive
  and don't collide with kwargs the event system already sets (`char_obj`, event
  metadata, …).
- **Cache by default.** Leave `realtime=False` unless a value must be fresh on each
  read; otherwise the image and the dialogue referencing the same key can disagree.
- **Nest instead of duplicating.** "Read the selected character's stat" = pass the
  character selector into the stat selector, don't roll the character twice.
- **Prefer `UnlockableCondition`/GameData** over the legacy rule/club selectors.
- **`StatSelector` gives you a range too** (`key_range`) — use it for range-scaled
  art rather than hard-coding bounds.

---

## 9. Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Image/text shows a literal `<key>` / `[key]` | The selector isn't in the event's `SelectorSet`, or the key differs | Add the selector; match the key exactly. |
| Value changes mid-scene unexpectedly | The selector is `realtime` (re-rolls each access) | Set `realtime=False` to freeze it for the scene. |
| Same value every time you wanted variety | Cached and never re-rolled across the boundary | Use realtime, or rely on the reroll between parenting/fragments. |
| `StatSelector` "_range" missing | Reading the wrong key | It's `key + "_range"`; the `SelectorSet` adds it automatically. |
| Nested selector returns a `Selector` object | It wasn't rolled | Use the built-in nesting (list/target accepts `Selector`) so it rolls recursively; don't stuff a raw selector where a value is expected. |

---

## 10. Reference tables

### Base contract
`Selector(realtime, key, *options)` · abstract `roll(**kwargs)` · `get_value` (rolls
if realtime/uncached) · `update` (force re-roll) · `get_name` = key.

### SelectorSet
`SelectorSet(*selectors)` · `get_values(**kwargs)` → kwargs dict · `roll_values` ·
`add_selector`. Special: `KwargsSelector` (many keys), `StatSelector` (+`_range`).

### Downstream substitution
Image paths: `<key>` (via `refine_image`/`get_image`) · Text: `[key]` (Ren'Py) ·
Logic: pass a `Selector` where `Union[..., Selector]` is accepted.

### Related files
- `game/scripts/selector.rpy` — all selector classes + `SelectorSet`
- `game/scripts/event.rpy` — events that run selectors
- `game/scripts/images.rpy` — `refine_image` / `get_image` (`<key>` substitution)
- [Images](Images) — path resolution, PNG/WebP, mod prefixes
- [Conditions](Conditions) / [Effects](Effects) — consumers that accept a `Selector`
