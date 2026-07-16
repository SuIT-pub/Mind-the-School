# Example: Cafeteria Crisis

Reference implementation in `game/scripts/situations/situations.rpy`.

## Design summary

| Field | Value |
|-------|-------|
| key | `cafeteria_crisis` |
| Start | `-10` (planned; set at activation) |
| Limits | `-30` / `+60` |
| Role | 2nd situation; introduces passives |

## Thresholds

| Value | Type | approach_hint (short) | reached_hint |
|-------|------|----------------------|--------------|
| -5 | Blocking | Campus eating space needed | Inspect empty kitchen building |
| +10 | Auto-fire | Someone from PTA may help | — |
| +20 | Blocking | PTA must agree | Plan PTA vote |
| +35 | Auto-fire | Construction can begin | — |
| +40 | Blocking | Adelaide needs support soon | Help with meal plan (office/cafeteria) |
| +50 | Auto-fire | First real lunch service | — |
| +60 | Auto-fire | Resolution — stable cafeteria | — |

## Event pools

| Key | Range | Phase |
|-----|-------|-------|
| `Lieferproblem` | 35–54 | After construction |
| `Schülerbeschwerden` | -10–54 | Whole arc; tone varies |
| `Adelaide überfordert` | 10–48 | After Adelaide intro |
| `Lehrer-Feedback` | -5–54 | After room identified |

## Code shape

```python
$ situation_manager.load_situation(
    Situation("cafeteria_crisis", "Cafeteria Crisis", "Die Schule hat keine richtige Mensa...",
        Bar("main",
            BlockingThreshold(-5, "<approach>", "<reached>", PlaceholderCondition()),
            AutoThreshold(10, "<approach>"),
            limits=(-30, 60),
            stat_weights={HAPPINESS: 0.5, EDUCATION: 0.2, REPUTATION: 0.2},
        ),
        SituationPassive("leave_adelaide", "Adelaide alleine lassen", DummyEffect()),
        SituationPassive("hire_staff", "Zusätzliches Personal einstellen", DummyEffect()),
        SituationPassive("train_adelaide", "Adelaide persönlich einarbeiten", DummyEffect()),
        SituationEventPools("cafeteria_look_around_delivery", 35, 54),
        SituationEventPools("courtyard_patrol_complaints", -10, 54),
        SituationEventPools("school_building_patrol_complaints", -10, 54),
        SituationEventPools("cafeteria_look_around_adelaide", 10, 48),
        SituationEventPools("office_building_work_adelaide", 10, 48),
        SituationEventPools("office_building_work_teacher_feedback", -5, 54),
    )
    .add_effect("positive_resolution", DummyEffect())
    .add_effect("negative_resolution", DummyEffect())
)
```

## Prompt fragment → output

**User prompt:**
> Level 1 Situation: Gym renovation. Start -15. Teachers skeptical (+15 blocking vote), construction at +30, opening at +55. Two passives: cheap repair vs proper renovation. Happiness and reputation matter.

**Agent output:**
1. Table with thresholds + hints
2. Pool ranges for `gym` / `patrol` and `office_building` / `work`
3. New `load_situation` block appended in `load_situations`
