---
name: build-situation
description: >-
  Builds Mind the School Situation definitions from a narrative prompt or design
  document, or shows a short syntax guide for creating situations. Generates
  code in game/scripts/situations/situations.rpy inside label load_situations.
  Use when the user asks to create, design, implement, or extend a Situation,
  situation bar, thresholds, passive options, injected events, situation teasers,
  or asks how situation syntax works, how to write a Situation, or for a syntax
  reference / Anleitung.
---

# Build Situation

Zwei Modi — zuerst erkennen, was der User will:

| Modus | Wann | Output |
|-------|------|--------|
| **Syntax-Anleitung** | User fragt nach Syntax, Struktur, „wie schreibt man…“, Cheatsheet, Anleitung — **ohne** konkreten Situations-Prompt | Kurze Syntax-Referenz (siehe unten). **Kein Code schreiben**, es sei denn explizit gewünscht. |
| **Situation bauen** | User liefert Prompt, Design-Doc oder konkrete Situation | Tabelle + `load_situations`-Code (Standard-Workflow) |

Default bei Implementierung: `game/scripts/situations/situations.rpy`, inside `label load_situations`, as a new `situation_manager.load_situation(...)` call — unless the user specifies another file or location.

## Syntax-Anleitung (Kurzreferenz)

Bei reiner Syntax-Frage diese Anleitung zeigen (ggf. auf Deutsch, wenn User Deutsch schreibt). Kompakt halten — kein vollständiger Design-Workflow.

### Gerüst in `label load_situations`

Nutze die **Definition-Helper** (weniger Boilerplate, kein `direction=1` / leeres `threshold_hint` von Hand):

```python
$ register_situations(
    Situation("<key>", "<Name>", "<Beschreibung>",
        Bar("main",
            BlockingThreshold(-5, "<approach>", "<reached>", PlaceholderCondition()),
            AutoThreshold(10, "<approach>"),
            limits=(-30, 60),
            stat_weights={HAPPINESS: 0.5, EDUCATION: 0.2},
        ),
        PassiveOption("stable_key", "Spieler-Beschreibung", DummyEffect()),
        SituationPool("building_action_event", bar_min, bar_max),
        thumbnail="images/...",
    ).add_effect("positive_resolution", DummyEffect())
     .add_effect("negative_resolution", DummyEffect()),
)
```

**Helper:** `AutoThreshold` · `BlockingThreshold` · `Bar` · `PassiveOption` · `SituationPool` · `register_situations`

`Bar(key, ...)` — erster Parameter ist der Balken-Key (`"main"` für Standard-Situationen; bei PTA mehrere Keys möglich, z.B. `"teachers"`, `"parents"`, `"students"`).

Low-level (weiterhin gültig): `SituationThreshold(...)` · `SituationBar(...)` · `situation_manager.load_situation(...)`

### SituationThreshold (Low-level)

```python
SituationThreshold(balkenwert, approach_hint, threshold_hint, direction, *conditions_oder_effects)
```

| Typ | `threshold_hint` | Extra | `direction` |
|-----|------------------|-------|-------------|
| Auto-fire | `""` | optional `Effect`s | `1` (aufwärts) / `-1` (abwärts) |
| Blocking | Konkreter Task-Hinweis | min. 1 `Condition` | `1` für Gates beim Fortschritt nach oben |

```python
# Blocking
SituationThreshold(20, "Eltern müssen mitziehen.", "PTA-Abstimmung planen.", 1, PlaceholderCondition()),
# Auto-fire
SituationThreshold(35, "Der Umbau kann beginnen.", "", 1),
```

- `approach_hint` — vage Richtung, solange Balken unter der Schwelle
- `threshold_hint` — konkretes *Was* (nur bei Blocking relevant)

### SituationPassive

```python
SituationPassive("stable_key", "Spieler-Beschreibung", DummyEffect()),
```

Tutorial-Situationen: weglassen.

### SituationEventPools

```python
SituationEventPools("<building>_<action>_<event>", bar_min, bar_max),
```

Pool aktiv solange `bar_min <= balkenwert <= bar_max`.

### Stat-Gewichte & Resolutions

```python
# Am SituationBar (nicht Situation!):
.add_stat_weight(HAPPINESS, 0.5)

# Am Situation:
.add_effect("positive_resolution", DummyEffect())
.add_effect("negative_resolution", DummyEffect())
```

### Wichtige Regeln

- **`__init__` darf nichts returnen** — nur Chain-Methoden (`add_*`, `set_*`) returnen `self`
- `bar.value` **nicht** im Template setzen (Runtime-State überlebt Reload)
- `add_stat_weight` / `Bar(..., stat_weights=...)` am Bar, nicht an `Situation`
- Blocking braucht `Condition`; WIP: `PlaceholderCondition()`
- Konstanten: `HAPPINESS`, `EDUCATION`, `REPUTATION`, … aus `consts.rpy`

Mehr Details: [reference.md](reference.md) · Beispiel: [examples.md](examples.md)

---

## Situation bauen (voller Workflow)

Create or extend a **Situation** from a user prompt.

## Before coding

1. Read `game/scripts/situations/situations.rpy` (classes + existing situations).
2. Read `game/scripts/situations/situation_system_concept.md` for design intent.
3. Skim an existing building's `EventStorage` targets if injected events are needed (`game/scripts/buildings/*.rpy`).

If the prompt is incomplete, infer sensible defaults and state assumptions briefly. Ask only when a missing choice blocks implementation (e.g. tutorial vs. full situation, PTA subtype).

## Workflow

```
- [ ] 1. Parse prompt → structured design
- [ ] 2. Draft thresholds + hints
- [ ] 3. Draft passives, event pools, stat weights, resolutions
- [ ] 4. Write load_situations entry
- [ ] 5. Run checklist (below)
```

### Step 1 — Parse the prompt

Extract or infer:

| Field | Notes |
|-------|-------|
| `key` | snake_case, unique (`cafeteria_crisis`) |
| `name` | Journal title (English unless user wants German) |
| `description` | 1–3 sentences, protagonist-facing context |
| Start value | Often negative (`-10`); set via bar after creation if needed |
| Limits | `set_limits(negative_resolution, positive_resolution)` |
| Thresholds | Value, type (blocking / auto-fire), narrative beat |
| Passives | 0 (tutorial) or 3 strategies |
| Injected events | Building, action, bar range |
| Stat weights | Only stats that narratively matter; use `HAPPINESS`, `EDUCATION`, etc. from `consts.rpy` |
| Resolutions | `positive_resolution` / `negative_resolution` effects |
| Trigger | Event or condition that starts the situation (note separately if not in `load_situations`) |
| Teasers | Optional `SituationTeaser` entries (class exists; wire when `Situation` supports them) |

### Step 2 — Thresholds and hints

**Constructor:** `SituationThreshold(value, approach_hint, threshold_hint, direction, *conditions_or_effects)`

| Type | `threshold_hint` | Extra args | `direction` |
|------|------------------|------------|-------------|
| **Auto-fire** | `""` | Optional `Effect`s | `1` (up) or `-1` (down) |
| **Blocking** | Concrete task hint (`reached_hint`) | At least one `Condition` | `1` for gates on upward progress; `-1` for negative escalation |

**Hint rules** (from concept doc):
- `approach_hint`: vague direction, protagonist journal voice, no exact steps
- `threshold_hint` (reached): concrete *what*, player discovers *where/how*
- German or English — match the user's prompt language

**Ordering:** Threshold values define narrative order. Blocking gates must sit before auto-fire beats they should precede.

**Placeholders:** Use `PlaceholderCondition()` only until real conditions exist. Replace with `EventSeenCondition`, `ProgressCondition`, `BuildingCondition`, etc.

### Step 3 — Passives, pools, weights

**Passives:** `SituationPassive(key, description, *effects)` — use stable snake_case keys (`leave_adelaide`), not `"Option A"`. Tutorial situations: omit passives.

**Event pools:** `SituationEventPools(key, min, max)` — bar range when the pool is active.
- Prefer keys: `{building}_{action}_{event}` (e.g. `cafeteria_look_around_delivery`)
- One pool per building+action combination; duplicate ranges if the same event appears in multiple buildings
- Cross-check building actions exist (`patrol`, `work`, `look_around`, …)

**Stat weights:** Chain via `Bar(..., stat_weights={...})` or on `SituationBar`:
```python
Bar("main",
    AutoThreshold(10, "..."),
    limits=(-30, 60),
    stat_weights={HAPPINESS: 0.5, EDUCATION: 0.2},
)
```

**Resolutions:** Chain on `Situation`:
```python
.add_effect("positive_resolution", DummyEffect())
.add_effect("negative_resolution", DummyEffect())
```
Replace `DummyEffect()` with real effects when available.

### Step 4 — Write code

Add inside `label load_situations` in `game/scripts/situations/situations.rpy`:

```python
$ situation_manager.load_situation(
    Situation("<key>", "<Name>", "<Description>",
        Bar("main",
            SituationThreshold(...),
            # ... more thresholds
            limits=(<neg>, <pos>),
            stat_weights={HAPPINESS: <weight>},
        ),
        # SituationPassive(...) — if not tutorial
        SituationEventPools("<pool_key>", <min>, <max>),
    )
    .add_effect("positive_resolution", DummyEffect())
    .add_effect("negative_resolution", DummyEffect())
)
```

**Rules:**
- One `load_situation` call per situation; do not replace existing situations unless asked
- Keep `set_current_mod('base')` and manager init as-is
- Do not set `bar.value` in the template — runtime progress persists across reloads; `update_data` must not reset it
- Do not add `@property` on `key`/`name` fields that are set in `__init__`
- Blocking conditions belong in `SituationThreshold`, not as separate elements on `Situation`

### Step 5 — Checklist

- [ ] `key` is unique among loaded situations
- [ ] `set_limits` matches planned negative/positive resolution values
- [ ] Every blocking threshold has a non-empty `threshold_hint` and a `Condition`
- [ ] Every auto-fire threshold has `threshold_hint=""` (unless deliberately different)
- [ ] `-5`-style early gates use `direction=1` when the player progresses upward from a negative start
- [ ] `add_stat_weight` is on `SituationBar`, not `Situation`
- [ ] Event pool min/max align with narrative phases (construction, operation, resolution)
- [ ] Passive keys are descriptive and stable
- [ ] Hints match prompt language and tone
- [ ] No duplicate `load_situation` keys on reload

## Prompt → deliverables

When the user provides a design doc, produce:

1. **Summary table** — thresholds with approach/reached hints (blocking only for reached)
2. **Event pool table** — key, building/action, min, max
3. **Code** — `load_situations` entry

If the user only wants hints or pools, still follow the same hint/pool rules; only skip code when they say so.

## Common conditions

| Goal | Condition |
|------|-----------|
| Event was seen | `EventSeenCondition("event_key")` |
| Building unlocked | `BuildingCondition("cafeteria")` |
| Progress step | `ProgressCondition("unlock_cafeteria", "2")` |
| Placeholder / WIP | `PlaceholderCondition()` |

Grep `game/scripts/conditions.rpy` for more. Read `.cursor/rules/conditions.mdc` when composing complex logic.

## Pitfalls (system constraints)

- `get_next_threshold` iterates `self.thresholds.values()` — never iterate the dict directly
- `SituationThreshold.key` is a **property**, not a method — use `threshold.key`, not `threshold.key()`
- `add_threshold` must set `threshold.bar = self` before indexing by `threshold.key`
- `SituationBar.update_data` must **not** copy `value` from the template
- `SituationThreshold.update_data` must **not** copy `reached`
- `SituationTeaser.update_data` must preserve `active` and `values`

## Additional resources

- Full API and reload semantics: [reference.md](reference.md)
- Worked example (Cafeteria Crisis): [examples.md](examples.md)
- Design philosophy: `game/scripts/situations/situation_system_concept.md`
