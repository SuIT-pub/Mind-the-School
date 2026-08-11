# Situation / Unlockable API Reference

> Low-level cheat-sheet. For the full, self-contained references see
> `wiki/Building-Situations.md` (Situations) and
> `wiki/Building-Unlockables.md` (Unlockables).

## Class hierarchy

```
SituationManager.load_situation(Situation)
  Situation
    SituationBar ("main")
      SituationThreshold × N
      stat_weights
    SituationPassive × 0–3
    SituationEventPools × N
    effects["positive_resolution" | "negative_resolution"]
```

## SituationThreshold

```python
SituationThreshold(
    threshold: int,        # bar position
    approach_hint: str,    # shown while approaching
    threshold_hint: str,   # reached_hint for blocking; "" for auto-fire
    direction: int = 1,    # 1 = triggers on upward cross; -1 = downward
    *elements: Condition | Effect
)
```

Runtime state (persist across reload): `reached`, pending state in `situation_manager.threshold_checks`.

Template state (updated on reload): `threshold`, hints, `direction`, `blocking`, `effects`.

## SituationBar / Bar helper

```python
# Helper (preferred in load_situations):
Bar("main", *thresholds, limits=(-100, 100), stat_weights=None)

# Low-level:
SituationBar("main", *thresholds)
  .set_limits(min, max)
  .add_stat_weight(HAPPINESS, 0.5)
```

Runtime state: `value` (never overwrite in `update_data`).

Default: `value=0`, `min=-100`, `max=100` until `set_limits`.

## SituationPassive

```python
SituationPassive("stable_key", "Player-facing description", *effects)
```

Keyed by `name` in `situation.passives`. Effects run/revert when switching active passive.

## SituationEventPools

```python
SituationEventPools("pool_key", bar_min, bar_max)
```

Active while `bar_min <= bar.value <= bar_max`. Keys should map to building event registration (convention: `{building}_{action}_{slug}`).

## Situation

```python
Situation("key", "Name", "Description", *elements)
  .add_effect("positive_resolution", SomeEffect())
  .add_effect("negative_resolution", SomeEffect())
```

Runtime state: `pause_until` (do not reset from template in `update_data`).

## Unlockable (subclass of Situation)

```python
Unlockable(
    type_key,                 # "rule" / "club" / "building"
    key,                      # stable key within the type; situation key = type_key:key
    name,                     # display name / group-member label
    inject_default_measure,   # True → inject the free "Persuade" measure
    *elements,                # visibility Conditions, unlock Effects (or a PositiveResolution),
                              #   SituationDescription, custom Bars/measures, Teasers, Picto,
                              #   UnlockableScheduleVoteConditions(...)
    thumbnail=None,
    group_index=-1,           # chain level (-1 = standalone)
    inject_default_cancel=True,
)
```

Registered via `register_unlockables(...)` in `label load_unlockables`
(`game/scripts/journal/unlockables.rpy`). Auto-injects: three faction bars
(`Students`/`Parents`/`Teachers`), Schedule Vote + Cancel (+ optional Persuade),
and the `vote_passed` / `PositiveResolution` unlock resolutions carrying
`UnlockableUnlockEffect` + your unlock effects.

Key details (full: unlockables author guide):
- **Visibility** = bare `Condition`s (when listed); *not* vote gates.
- **Unlock effects** = bare `Effect`s or a `PositiveResolution`; run on a won vote.
  Building → add `BuildingOpenEffect("<key>")` (unlock ≠ map-open).
- **Money cost** = `UnlockableScheduleVoteConditions(MoneyCondition("N+"))` +
  `MoneyEffect("<name>", -N, "ADD")`, paired by absolute value (self-test 800–803).
- **Upgrade chain** = one Unlockable per level, consecutive `group_index`.
- Runtime checks: `is_unlockable_unlocked(key, index=-1)` / `UnlockableCondition(key, index=-1)`.

## load_situations pattern

```python
label load_situations:
    $ set_current_mod('base')

    if not situation_manager:
        $ situation_manager = SituationManager()

    $ situation_manager.load_situation(
        Situation(...)
    )
    # additional load_situation calls for other situations
```

Called from `game/script.rpy` on start and after load. Reload path: existing situation → `update_data(template)`; new key → store template instance.

## Building actions (injected events)

| Building | Common actions |
|----------|----------------|
| `cafeteria` | `look_around`, `order_food`, `eat_alone`, `search` |
| `courtyard` | `patrol`, `search` |
| `school_building` | `patrol`, `check_class`, `teach_class`, `search` |
| `office_building` | `work`, … |

Always verify targets in the building's `.rpy` file before naming pools.

## Stat constants (`game/scripts/consts.rpy`)

`HAPPINESS`, `EDUCATION`, `CHARM`, `REPUTATION`, `INHIBITION`, `CORRUPTION`, `MONEY`

Weights are floats; `0` means ignore. A negative weight inverts direction; invert
behavior is situation-specific (see the author's guide, "Stat coupling in depth").

## Hint authoring guide

| Bar phase | approach_hint tone | reached_hint tone |
|-----------|-------------------|-------------------|
| Early / negative | Problem awareness, vague lead | — |
| Blocking gate | Build anticipation | Specific action |
| Mid progression | Momentum, who's involved | — |
| Pre-resolution | Almost there | — |

Protagonist journal voice. No UI meta ("trigger event X").

## Event pool range guide

| Narrative phase | Typical range anchor |
|-----------------|---------------------|
| Problem visible | from `start_value` |
| Character involved | from first character threshold |
| Post-construction | from construction threshold |
| Operational crises | construction → before resolution |
| Resolution | stop pools below `positive_resolution` |

Negative-path events can extend pools toward `negative_resolution` when tone should escalate.
