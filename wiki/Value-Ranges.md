> **Audience:** Developers writing conditions, situations, events, or any content that
> gates on a number — a stat, a level, a day, a counter. Nearly every numeric argument
> in the game accepts a small pattern string (a **value range**, sometimes called the
> *number pattern*) instead of a bare number. This page is the reference for that
> grammar: the exact forms, how they match, the closeness score they produce, and the
> edge cases that will bite you.
>
> **Scope:** The shared value-range grammar parsed by `check_in_value` and
> `get_value_diff` (`game/scripts/helper.rpy`). This is **not** the `>` / `>=` operator
> argument that `NumCompareCondition` / `KeyCompareCondition` take — that is a separate
> mechanism, called out in [§6](#6-not-the-same-thing-comparison-operators).

---

## Quick start

Anywhere a check asks "is this number in range?", you pass a pattern instead of a plain
number. All five forms:

```python
LevelCondition("3")      # exactly 3
LevelCondition("3+")     # 3 or more   (minimum)
LevelCondition("3-")     # 3 or less   (maximum)
LevelCondition("3-5")    # 3, 4, or 5  (inclusive range)
LevelCondition("1,3,5")  # 1 or 3 or 5 (a list — OR)
```

The same strings work for stats, calendar fields, timers — every check that routes
through `check_in_value`:

```python
StatCondition(corruption="20+", happiness="40-60")
TimeCondition(weekday="1-5", daytime="2")   # any weekday, second daytime segment
```

Numbers are fine too — `LevelCondition(3)` means exactly `3`. The pattern only earns
its keep when you want *more than* / *less than* / *a range* / *a set*.

---

## Contents

1. [The five forms](#1-the-five-forms)
2. [How matching works](#2-how-matching-works)
3. [The closeness score (`get_value_diff`)](#3-the-closeness-score-get_value_diff)
4. [The `"x"` wildcard](#4-the-x-wildcard)
5. [Who uses this](#5-who-uses-this)
6. [NOT the same thing: comparison operators](#6-not-the-same-thing-comparison-operators)
7. [Edge cases & gotchas](#7-edge-cases--gotchas)
8. [Conventions](#8-conventions)
9. [Troubleshooting](#9-troubleshooting)
10. [Reference](#10-reference)

---

## 1. The five forms

A value range is a string. `check_in_value(pattern, value)` returns `True` when `value`
falls inside the range the pattern describes.

| Form | Written | Matches | Example → matches |
|------|---------|---------|-------------------|
| **Exact** | `"5"` | only that number | `"5"` → 5 |
| **Minimum** | `"5+"` | that number or higher | `"5+"` → 5, 6, 7, … |
| **Maximum** | `"5-"` | that number or lower | `"5-"` → 5, 4, 3, … 0 |
| **Range** | `"3-7"` | inclusive, both ends | `"3-7"` → 3, 4, 5, 6, 7 |
| **List** | `"1,3,5"` | any listed token | `"1,3,5"` → 1 or 3 or 5 |

The list separator is a comma and the semantics are **OR** — a value matches if it
satisfies **any** token. And the tokens can themselves be any of the other forms, so a
list is the general escape hatch:

```python
"1,5-8,20+"   # exactly 1, OR 3..8 wait — 5 through 8, OR 20 and up
```

Whitespace anywhere is ignored — `"1, 5 - 8, 20+"` parses identically. Write it however
reads best.

---

## 2. How matching works

`check_in_value(pattern, value)` (in `game/scripts/helper.rpy`) does this:

1. Strip **all** whitespace from the pattern.
2. Split on `,` into tokens. A value matches the whole pattern if it matches **any** one
   token (OR).
3. For each token, decide by shape:
   - contains `-` and **ends** with `-` → **maximum**: match if `value <= n`.
   - contains `-` (in the middle) → **range**: split on `-`, match if `value` is between
     the two ends (inclusive; the smaller of the two is the floor regardless of order).
   - ends with `+` → **minimum**: match if `value >= n`.
   - otherwise → **exact**: match if `n == value`.
4. If **no** token matched and the pattern held no digits at all, fall back to raw
   string equality (`str(pattern) == str(value)`).

That final fallback is why a non-numeric key only ever matches its exact self, and why
the `"x"` wildcard is **not** handled here (see [§4](#4-the-x-wildcard)) — `"x"` has no
digits, so it can only string-match the literal `"x"`, never a number.

---

## 3. The closeness score (`get_value_diff`)

Matching is yes/no. But the journal, vote probability, and event sorting also want to
know *how close* a value is to satisfying a range. That is `get_value_diff(pattern,
value)` — it returns a signed number:

- **Positive** — the value is inside the range, and the number is how much room it has
  (distance to the nearest edge).
- **Negative** — the value is outside, and the number is how far short it falls.
- Across a comma list, the token **closest to zero** wins (via `set_nearest`) — i.e. the
  least-unmet / most-comfortably-met token.

Worked, for `value = 3`:

| Pattern | `get_value_diff` | Reading |
|---------|------------------|---------|
| `"5"`   | `-2` | exact target, 2 away |
| `"5+"`  | `-2` | 2 below the minimum |
| `"2+"`  | `+1` | 1 above the minimum |
| `"5-"`  | `+2` | 2 under the ceiling |
| `"1-5"` | `+2` | inside, 2 above the floor |
| `"7-9"` | `-4` | 4 short of the floor |

One quirk worth internalizing: for an **exact** pattern the score is always `-abs(n -
value)` — so overshooting an exact target scores as negative as undershooting it. Exact
patterns have no "comfortable margin"; only `+` / `-` / range forms do. That's fine for
gating (matching is what gates), but it shapes how `get_diff` / `calculate_probability`
rank a near-miss.

---

## 4. The `"x"` wildcard

`"x"` means *don't check this field* — match anything. It is **not** part of the core
grammar; the calendar checks in `time.rpy` (`check_day`, `check_month`, `check_week`,
`check_year`, `check_daytime`, `check_weekday`) special-case it **before** calling
`check_in_value`:

```python
if value == "x":
    return True
return check_in_value(value, self.day)
```

So `"x"` works in `TimeCondition` / `TimerCondition` fields (all of which default to
`"x"` — that's why you only name the fields you care about). It does **not** work as a
wildcard for stats, levels, money, or anything else — pass `"x"` to a `StatCondition`
and it falls through to string equality and never matches.

---

## 5. Who uses this

The grammar is shared through a handful of thin wrappers that all delegate to
`check_in_value`:

| Wrapper | File | Feeds |
|---------|------|-------|
| `Stat.check_stat(value)` | `stats.rpy` | `StatCondition` |
| `Char.check_level(value)` | `character.rpy` | `LevelCondition` |
| `Time.check_day / _week / _month / _year / _daytime / _weekday` | `time.rpy` | `TimeCondition`, `TimerCondition` |
| direct `check_in_value` calls | `conditions.rpy`, `paperdoll.rpy` | misc. gates & layer resolution |

So any condition built on those (`StatCondition`, `LevelCondition`, `TimeCondition`,
`ProficiencyCondition`'s xp/level, …) accepts the full five-form pattern. See the
[Conditions](Conditions) guide for the condition catalog.

> **`MoneyCondition` is the odd one out.** It does **not** route through
> `check_in_value`; it compares `self.value <= money.get_value()` directly, so it wants a
> plain number (treated as a minimum). The `+` / `>=` strings its docstring hints at are
> not parsed there — pass an integer.

---

## 6. NOT the same thing: comparison operators

There is a second, unrelated numeric mechanism in the condition system, and it is easy
to confuse with value ranges:

```python
NumCompareCondition(key, value, ">=")   # operator is a SEPARATE argument
KeyCompareCondition(key_1, key_2, "<")
```

These take an explicit `operation` string (`>`, `<`, `>=`, `<=`, `==`) as its **own
parameter** and run it through `compare_to`. That is a different code path with a
different syntax. The value-range grammar on this page has no `>` / `>=` tokens — its
"greater/less" forms are the `+` and `-` suffixes. Don't write `">=3"` as a value range;
it has no digits-plus-operator parsing and will fall through to string equality.

| You want | Value range (this page) | Comparison operator (`NumCompare`) |
|----------|-------------------------|------------------------------------|
| 3 or more | `"3+"` | `NumCompareCondition(key, 3, ">=")` |
| 3 or less | `"3-"` | `NumCompareCondition(key, 3, "<=")` |
| exactly 3 | `"3"` | `NumCompareCondition(key, 3, "==")` |

Rule of thumb: if the number lives inside a stat/level/time check, it's a value range.
If it's a `NumCompare` / `KeyCompare`, the operator is a separate argument.

---

## 7. Edge cases & gotchas

- **Integers only.** Digits are extracted with `\d+`; the decimal point is not a digit.
  A token like `"1.5"` reads its digit runs `1` and `5`, concatenates them, and becomes
  **`15`** — silently. Never put decimals in a value range.
- **No negative numbers.** Everything is unsigned digit extraction, and `-` is the
  max/range marker. To say "at most 5" write **`"5-"`**, never `"-5"` — `"-5"` parses as
  a range, splits on `-` into `["", "5"]`, and `int("")` **crashes**.
- **`,` is OR, not a thousands separator.** `"1,000"` means "1 or 0 or 0", i.e. `1` or
  `0` — not one thousand.
- **`"x"` is time-only** (see [§4](#4-the-x-wildcard)).
- **Exact patterns have no margin** in `get_value_diff` — overshoot scores negative (see
  [§3](#3-the-closeness-score-get_value_diff)). Use `+` when you mean "at least".
- **Bare numbers are exact, not minimums.** `LevelCondition(3)` matches *only* level 3.
  If you mean "level 3 and up" — which is usually what a gate wants — write `"3+"`. This
  is the single most common mistake.

---

## 8. Conventions

- **Prefer `"n+"` for gates.** Content that unlocks at a level/stat almost always means
  "this much *or more*". A bare `"n"` locks it back up the moment the value moves past
  `n`. Reach for `+` unless you genuinely want an exact window.
- **Use ranges for windows, lists for scattered sets.** `"3-5"` for a contiguous band,
  `"1,4,9"` when the valid values don't line up.
- **Keep them strings.** Even where a bare int works, quoting (`"3"`) keeps the whole
  argument visually consistent with its `"+"` / `"-"` siblings and avoids the
  int-vs-pattern ambiguity when reviewing.
- **Don't reach for `>=` here.** That's `NumCompareCondition`'s job
  ([§6](#6-not-the-same-thing-comparison-operators)).

---

## 9. Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Gate opens at exactly N, then closes again | Bare/exact pattern (`"3"` or `3`) where you meant a minimum | Write `"3+"`. |
| `"-5"` crashes the check | `-5` parses as a range and splits into `["", "5"]` | Use `"5-"` for "at most 5". |
| A decimal threshold behaves wildly | `"1.5"` became `15` (dot stripped, digits joined) | Use integers only. |
| `"x"` never matches a stat/counter | `"x"` is a time-only wildcard; elsewhere it string-matches literally | Drop the field entirely, or use a real range. |
| `">=3"` never matches | Value ranges have no `>=` token; it fell through to string equality | Use `"3+"`, or switch to `NumCompareCondition(key, 3, ">=")`. |
| `"1,000"` matches level 0 or 1 | Comma is OR, not a digit group separator | Write the actual number, `"1000"`. |

---

## 10. Reference

### The five forms
`"5"` exact · `"5+"` minimum · `"5-"` maximum · `"3-7"` inclusive range · `"1,3,5"` list (OR). Whitespace ignored; integers only.

### Functions
- `check_in_value(pattern, value) -> bool` — does `value` fall in the range? (`helper.rpy`)
- `get_value_diff(pattern, value) -> num` — signed closeness: `+` inside (room), `−` outside (shortfall); nearest token wins across a list. (`helper.rpy`)
- `get_highest_value(pattern, max_value=INT64_MAX) -> int` — the top of the range (`INT64_MAX` if it's a `+` minimum, i.e. unbounded). (`helper.rpy`)
- `set_nearest(nearest, value)` — internal: keeps whichever is closer to zero. (`helper.rpy`)

### Wildcard
`"x"` = match-any, **time checks only** (`check_day` / `_week` / `_month` / `_year` / `_daytime` / `_weekday` in `time.rpy`).

### Not this grammar
`NumCompareCondition` / `KeyCompareCondition` take a separate `operation` argument (`>`, `<`, `>=`, `<=`, `==`) via `compare_to` — see [§6](#6-not-the-same-thing-comparison-operators). `MoneyCondition` compares directly and wants a plain integer.

### Related pages
- [Conditions](Conditions) — the condition catalog; most numeric conditions accept a value range.
- [Selectors](Selectors) — some conditions take a `Selector` where a value would go.
- [Modifiers](Modifiers) — numeric operators for *changing* values (a different system).
