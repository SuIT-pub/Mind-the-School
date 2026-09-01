---
name: build-situation
description: >-
  Designs and builds Mind the School Situations AND Unlockables (rules, clubs,
  building unlocks) from a narrative prompt or design idea. Brainstorms the design
  collaboratively with the user in planning mode first, then implements: Situations
  in game/scripts/situations/situations.rpy (label load_situations), Unlockables in
  game/scripts/journal/unlockables.rpy (label load_unlockables). Also shows a short
  syntax guide. Use when the user asks to create, design, implement, or extend a
  Situation or an Unlockable — bars, thresholds, passives/measures, injected events,
  teasers, PTA votes, unlock effects, upgrade chains — or asks how the syntax works.
---

# Build Situation / Unlockable

This skill covers **two closely related things**:

- **Situation** — an ongoing problem/development the player influences via a
  bidirectional bar and narrative hints, ending in a positive/negative resolution
  (e.g. *Cafeteria Crisis*, *Body Conflict*).
- **Unlockable** — a **subclass of Situation** that unlocks a **rule / club /
  building** through a **PTA vote**. The vote layer (Schedule Vote, faction bars,
  Cancel, unlock resolutions) is injected for you; you mostly author *visibility*
  and *what unlocking does*.

An Unlockable *is* a Situation, so everything about Situations applies to Unlockables
too. Read the guides before building:

- **`wiki/Building-Situations.md`** — the full Situation reference (self-contained:
  design + API + troubleshooting).
- **`wiki/Building-Unlockables.md`** — the Unlockable extension (what the class adds,
  PTA vote, money escrow, upgrade chains).

> The author guides live in the repo's `wiki/` folder (they are the GitHub Wiki
> source). Related system guides there: `wiki/Events.md`, `wiki/Conditions.md`,
> `wiki/Selectors.md`, `wiki/Effects.md`, `wiki/Modifiers.md`, `wiki/Options.md`,
> `wiki/School-Levels.md` (campus climate if the unlock changes school level).

## Modes — detect what the user wants

| Mode | When | What you do |
|------|------|-------------|
| **Syntax guide** | User asks about syntax/structure, "how do I write…", a cheatsheet — **without** a concrete build request | Show the [syntax guide](#syntax-guide-quick-reference). **No code, no plan mode.** |
| **Build** | User provides a prompt or wants a concrete Situation/Unlockable created or extended | Follow the [Brainstorm → Plan → Implement](#build-workflow-brainstorm--plan--implement) workflow below. |

---

## Build workflow: brainstorm → plan → implement

The build flow is **collaborative and plan-first**. Do **not** jump straight to
code — a Situation/Unlockable is a narrative + balancing design, and those decisions
are the user's. Brainstorm the design together in **planning mode**, converge on a
concrete plan, get approval, then implement.

### Phase 0 — Ground yourself (before talking design)

1. Read both author guides (above) if you haven't this session.
2. Read the target source for existing patterns and keys:
   - Situation → `game/scripts/situations/situations.rpy`
   - Unlockable → `game/scripts/journal/unlockables.rpy`
3. If injected events / PTA-discussion events are wanted, skim the relevant
   building's `EventStorage` targets (`game/scripts/buildings/*.rpy`).

### Phase 1 — Decide the type (Situation vs. Unlockable)

Usually clear from the prompt; if not, ask. Decision guide:

- The goal is to **permanently unlock a rule / club / building via a PTA vote**
  → **Unlockable** (`type_key` = `rule` / `club` / `building`).
- Building has **multiple levels/upgrades** → Unlockable **group chain**
  (`group_index` 1, 2, 3…).
- It's an **ongoing problem/arc** that resolves narratively (not a permanent
  unlock) → **Situation**.

### Phase 2 — Brainstorm the design **in planning mode**

Enter planning mode and shape the design **with** the user. Use `AskUserQuestion`
for focused choices; propose concrete options and a recommended default, but let the
user drive the narrative and balancing calls. Iterate until the design is settled.

Walk through the relevant checklist:

**Both types:**
- Narrative: what is the problem/goal, who is involved, what does success look like?
- Language: English or German (match the surrounding content / the user's prompt).
- Bars: single `main`, or multi-bar (PTA factions `teachers`/`parents`/`students`)?
- `limits`, and the start value (`start_base` / `start_modifiers`).
- Stat couplings (`stat_weights`) — only stats that narratively matter, kept small.
- Key beats → thresholds: which are **blocking gates** (must happen, need a
  condition) vs **auto-fire** (happen as a reaction to progress); their order.
- Injected events / pools (which building + action, which bar range)?
- Teasers — pre-activation "hunches" (pull architecture, unlocked by conditions)?
- What **activates** it (a story event, the journal button, a debug call)?

**Situation-specific:**
- Passives/measures (Layers 2 & 3), or none (tutorial)? Respect the net rule:
  wear + passive should not net clearly positive.
- Resolutions: positive/negative/deadline/condition, mode `ALL`/`ANY`, and the
  **real effects** each one fires.

**Unlockable-specific:**
- `type_key` (`rule` / `club` / `building`).
- Single unlockable or a **group chain** (`group_index` per level)?
- **Visibility conditions** — from when is it listed (these are *not* vote gates)?
- **Unlock effects** — what actually happens on a won vote (rule flag,
  `LevelEffect`, and for buildings a `BuildingOpenEffect` to open the map location —
  unlock ≠ map-open)?
- **Money cost?** → a `MoneyCondition` on Schedule Vote (via
  `UnlockableScheduleVoteConditions`) paired with a matching negative `MoneyEffect`.
- Injected measures: keep the free **Persuade** (`inject_default_measure=True`)?
  keep the free **Cancel** (`inject_default_cancel`), or a custom one?
- Custom bars, or the injected three factions? Preview `Picto(...)` marks?

### Phase 3 — Present the plan and get approval

Converge the brainstorm into a concrete plan, then present it (and exit plan mode
for approval). The plan should contain:

1. **Type & placement** — Situation or Unlockable; target file/label.
2. **Design tables** — thresholds (approach/reached hints), bars & stat weights,
   pools (key/building/action/range), resolutions/unlock effects; for Unlockables
   also visibility conditions, unlock effects, money pairing, group levels.
3. **Code shape** — the `Situation(...)` / `Unlockable(...)` block as it will be
   written.
4. **Open placeholders** — where `PlaceholderCondition()` / `DummyEffect()` stand in
   for content to be filled later, and the intended real values.

### Phase 4 — Implement + checklist

After approval, write the code (Phase 3 shape) into the correct label, then run the
[checklist](#implementation-checklist).

- **Situation** → inside `register_situations(...)` in `label load_situations`
  (`game/scripts/situations/situations.rpy`).
- **Unlockable** → inside `register_unlockables(...)` in `label load_unlockables`
  (`game/scripts/journal/unlockables.rpy`).

Rules:
- One entry per `Situation(...)` / `Unlockable(...)`; don't replace existing ones
  unless asked.
- Keep `set_current_mod(...)` and manager init as-is.
- **Never** set runtime state (`bar.value`, `threshold.reached`, `teaser.active`) in
  the template — `update_data` preserves save state; starting values go in
  `start_base` / `start_modifiers`.
- Blocking conditions belong **in** the threshold, not as separate `Situation`
  elements.

Tell the user how to test (from the guides' Quick start): reload, then activate via
the journal button or the Ren'Py console (`Shift+O`) —
`situation_manager.get_situation("<key>").activate()` or
`unlockable_manager.get_unlockable_by_key("<key>").activate()` — and check the
Journal log view (category filter `situation`) for self-test errors.

---

## Syntax guide (quick reference)

For a pure syntax question, show the relevant part (in the user's language). Keep it
compact — no plan mode, no full workflow.

### Situation skeleton (`label load_situations`)

```python
$ register_situations(
    Situation("<key>", "<Name>", "<Description>",
        Bar("main", limits=(-30, 60), stat_weights={HAPPINESS: 0.5, EDUCATION: 0.2}),
        BlockingThreshold("<approach>", "<reached>", PlaceholderCondition(), main=-5),
        AutoThreshold("<approach>", main=10),
        PassiveOption("stable_key", "Player-facing description", DummyEffect()),
        SituationPool("building_action_event", 10, 54),
        PositiveResolution("ALL", DummyEffect()),
        NegativeResolution("ANY", DummyEffect()),
        thumbnail="images/...",
    ),
)
```

**Helpers:** `Bar` · `AutoThreshold` · `BlockingThreshold` · `PassiveOption` ·
`MeasureOption` · `SituationPool` · `Teaser` · `Picto` · `PositiveResolution` ·
`NegativeResolution` · `DeadlineResolution` · `ConditionResolution` ·
`register_situations`

- Thresholds are **top-level elements** of `Situation(...)`, not nested in `Bar(...)`;
  bar association is via keyword bounds (`main=-5`, or `teachers=25, parents=30`).
- `AutoThreshold(approach_hint, *effects, direction=1, visible_range=100, **bounds)`
- `BlockingThreshold(approach_hint, threshold_hint, *conditions, direction=1, visible_range=100, **bounds)`
- `approach_hint` = vague direction while below; `threshold_hint` = concrete *what*
  (blocking only). Journal voice, never UI meta ("trigger event X").

### Unlockable skeleton (`label load_unlockables`)

```python
$ register_unlockables(
    Unlockable("rule", "<key>", "<Name>", True,          # inject_default_measure
        SituationDescription(["<line>", "<line>"]),
        LevelCondition("2", True),                        # visibility (when listed)
        SituationEffectSetGameData("<key>_active", True, "<desc>"),  # unlock effect
        thumbnail="images/...",
        # group_index=1,                                  # for building-upgrade chains
        # inject_default_cancel=False,                    # to supply a custom Cancel
    ),
)
```

`Unlockable(type_key, key, name, inject_default_measure, *elements, thumbnail=None,
group_index=-1, inject_default_cancel=True)`

Auto-injected: three faction bars (`Students`/`Parents`/`Teachers`), Schedule Vote,
Cancel, optional Persuade, and the unlock resolutions. You author: visibility
conditions, unlock effects, optional custom bars/measures/pictograms.

- **Money cost:** `UnlockableScheduleVoteConditions(MoneyCondition("1500+"))` +
  `MoneyEffect("<name>", -1500, "ADD")` (match by absolute value; escrow auto-attached).
- **Building unlock:** add `BuildingOpenEffect("<building_key>")` as an unlock effect
  (unlock ≠ map-open).
- **Upgrade chain:** one `Unlockable` per level with consecutive `group_index`.
- Runtime checks elsewhere: `is_unlockable_unlocked("<key>")` /
  `UnlockableCondition("<key>")`.

### Important rules (both)

- `__init__` must not `return` a value — chaining is via `add_*` / `set_*` methods.
- Do **not** set `bar.value` in the template (runtime state survives reload).
- `stat_weights` go on the `Bar`, not on `Situation`/`Unlockable`.
- Blocking thresholds need a `Condition`; WIP → `PlaceholderCondition()`.
- Every resolution needs ≥ 1 effect; WIP → `DummyEffect()`.
- Stat constants (`HAPPINESS`, `EDUCATION`, `REPUTATION`, …) from `consts.rpy`.

More details: [reference.md](reference.md) · Examples: [examples.md](examples.md)

---

## Implementation checklist

Situation **and** Unlockable:
- [ ] `key` unique among loaded situations/unlockables (Unlockable key is `type_key:key`).
- [ ] No runtime state in the template (`value`, `reached`, `active`).
- [ ] `stat_weights` on the Bar, not the Situation/Unlockable.
- [ ] Every blocking threshold has a non-empty `threshold_hint` **and** a `Condition`.
- [ ] Auto-fire beats use `AutoThreshold` (implicit empty `threshold_hint`).
- [ ] Every resolution has ≥ 1 effect (`DummyEffect()` at worst).
- [ ] Hints match the prompt's language and journal tone.
- [ ] Pool `min`/`max` align with narrative phases; referenced building actions exist.

Situation only:
- [ ] `limits` match the planned negative/positive resolution values.
- [ ] Passive keys are descriptive and stable; net rule respected (wear + passive ≤ 0).

Unlockable only:
- [ ] `type_key` is `rule` / `club` / `building` (or a deliberate new category).
- [ ] Visibility conditions are visibility-only (no legacy vote-scoring conditions).
- [ ] Real unlock effect present (not just the implicit flag); building → `BuildingOpenEffect`.
- [ ] Money `MoneyCondition` ↔ `MoneyEffect` paired by absolute value (self-test 800–803).
- [ ] Group `group_index` values consecutive, no gaps.

## Common conditions

| Goal | Condition |
|------|-----------|
| Event was seen | `EventSeenCondition("event_key")` |
| Building unlocked (map) | `BuildingCondition("cafeteria")` |
| Unlockable unlocked | `UnlockableCondition("dress_code")` |
| Progress step | `ProgressCondition("key", "2")` |
| School/char level | `LevelCondition("2", True)` |
| Money threshold (vote) | `MoneyCondition("1500+")` |
| Placeholder / WIP | `PlaceholderCondition()` |

Grep `game/scripts/conditions.rpy` for more. Read `.cursor/rules/conditions.mdc` for
complex logic.

## Pitfalls (system constraints)

- Threshold-search helpers iterate `self.thresholds.values()` — never the dict directly.
- `SituationThreshold.key` is a **property** — use `threshold.key`, not `threshold.key()`.
- `add_threshold` must set `threshold.situation = self` before indexing by `threshold.key`.
- `SituationBar.update_data` must **not** copy `value`; `SituationThreshold.update_data`
  must **not** copy `reached`; `SituationTeaser.update_data` must preserve `active`/`values`.
- Mod Situations/Unlockables must register **inside the load wave** (queue the label
  via `register_start_method`), not from the init path.
- Image paths (`thumbnail`, `Teaser(image=…)`, `Picto(...)` icon) are auto-prefixed
  with the current mod's path at construction — write plain paths relative to the
  mod root, never `mods/MyMod/...`. Set `set_current_mod` before building the object.

## Additional resources

- Situation author's guide (design + API + troubleshooting): `wiki/Building-Situations.md`
- Unlockable author's guide: `wiki/Building-Unlockables.md`
- API cheat-sheet: [reference.md](reference.md)
- Worked examples (Situation + Unlockable): [examples.md](examples.md)
