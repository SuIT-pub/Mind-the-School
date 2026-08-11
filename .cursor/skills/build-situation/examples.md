# Examples

- [Situation — Cafeteria Crisis](#situation--cafeteria-crisis)
- [Unlockable — a rule and a building chain](#unlockable--a-rule-and-a-building-chain)

---

# Situation — Cafeteria Crisis

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
| `cafeteria_look_around_delivery` | 35–54 | After construction |
| `courtyard_patrol_complaints` | -10–54 | Whole arc; tone varies |
| `cafeteria_look_around_adelaide` | 10–48 | After Adelaide intro |
| `office_building_work_teacher_feedback` | -5–54 | After room identified |

## Code shape

```python
$ register_situations(
    Situation("cafeteria_crisis", "Cafeteria Crisis",
        "The school doesn't have a proper cafeteria...",
        Bar("main",
            limits=(-30, 60),
            stat_weights={HAPPINESS: 0.5, EDUCATION: 0.2, REPUTATION: 0.2},
        ),
        BlockingThreshold("<approach>", "<reached>", PlaceholderCondition(), main=-5),
        AutoThreshold("<approach>", main=10),
        PassiveOption("leave_adelaide", "Leave Adelaide alone", DummyEffect()),
        PassiveOption("hire_staff", "Hire additional staff", DummyEffect()),
        PassiveOption("train_adelaide", "Train Adelaide personally", DummyEffect()),
        SituationPool("cafeteria_look_around_delivery", 35, 54),
        SituationPool("courtyard_patrol_complaints", -10, 54),
        SituationPool("school_building_patrol_complaints", -10, 54),
        SituationPool("cafeteria_look_around_adelaide", 10, 48),
        SituationPool("office_building_work_adelaide", 10, 48),
        SituationPool("office_building_work_teacher_feedback", -5, 54),
        PositiveResolution("ALL", DummyEffect()),
        NegativeResolution("ANY", DummyEffect()),
    ),
)
```

## Prompt fragment → output

**User prompt:**
> Level 1 Situation: Gym renovation. Start -15. Teachers skeptical (+15 blocking vote), construction at +30, opening at +55. Two passives: cheap repair vs proper renovation. Happiness and reputation matter.

**Agent output:**
1. Table with thresholds + hints
2. Pool ranges for `gym` / `patrol` and `office_building` / `work`
3. New `Situation(...)` block appended in `load_situations`

---

# Unlockable — a rule and a building chain

Reference: `game/scripts/journal/unlockables.rpy` (`label load_unlockables`). An
Unlockable is a Situation with the PTA-vote layer injected — you author visibility
and unlock effects; bars/vote/cancel/resolutions come for free.

## Standalone rule

| Field | Value |
|-------|-------|
| type_key / key | `rule` / `dress_code` |
| Visibility | school level ≥ 2 |
| Unlock effect | sets `dress_code_active` |
| Bars | injected three factions |

```python
$ register_unlockables(
    Unlockable("rule", "dress_code", "Dress Code", True,   # inject_default_measure
        SituationDescription([
            "Introduce a school-wide dress code.",
            "The PTA must approve it before it takes effect.",
        ]),
        LevelCondition("2", True),                          # visibility (when listed)
        SituationEffectSetGameData("dress_code_active", True, "Dress code in force"),
        thumbnail="images/journal/rules/dress_code.webp",
    ),
)
```

## Building upgrade chain (with a money cost)

Each level is its own `Unlockable` sharing the `key`, with consecutive
`group_index`. The level-2 vote costs $1500 (escrow pair). Unlock opens the map
location explicitly via `BuildingOpenEffect`.

```python
$ register_unlockables(
    Unlockable("building", "cafeteria", "Cafeteria I", True,
        SituationDescription(["Open a basic cafeteria."]),
        BuildingCondition("school_ground"),                 # visibility
        BuildingOpenEffect("cafeteria"),                    # unlock → open map location
        thumbnail="images/journal/buildings/cafeteria_1.webp",
        group_index=1,
    ),
    Unlockable("building", "cafeteria", "Cafeteria II", True,
        SituationDescription(["Expand the cafeteria. Costs $1500."]),
        UnlockableScheduleVoteConditions(MoneyCondition("1500+")),  # escrow amount
        MoneyEffect("cafeteria_2_cost", -1500, "ADD"),             # matching cost
        thumbnail="images/journal/buildings/cafeteria_2.webp",
        group_index=2,
    ),
)
```

The auto-inserted prerequisite gates Cafeteria II behind Cafeteria I; the
`MoneyCondition`/`MoneyEffect` pair (equal absolute value) satisfies self-test
800–803.

## Prompt fragment → output

**User prompt:**
> Unlockable club: a chess club. Visible once the school ground is unlocked. No cost.
> When the vote passes, mark the club as open.

**Agent output (after brainstorming type/visibility/unlock effect in plan mode):**
1. Type table: `club` / `chess_club`, standalone, injected faction bars
2. Visibility (`BuildingCondition("school_ground")`) + unlock effect (`SetGameData`)
3. New `Unlockable(...)` block appended in `load_unlockables`
