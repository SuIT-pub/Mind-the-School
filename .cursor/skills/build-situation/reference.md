# Situation API Reference

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

Weights are floats; `0` means ignore. Invert behavior for stats is situation-specific (see concept doc).

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
