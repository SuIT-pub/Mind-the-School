> **Audience:** Developers who are comfortable with Python/Ren'Py and already know
> the **Situation** system (see
> [Building Situations](Building-Situations)).
> This guide explains what Unlockables are, how they extend Situations, what the
> system injects for you, how to define them, and how to use them in a mod.
>
> **Scope:** This is exclusively about **Unlockables** (rules, clubs, building
> unlocks). An Unlockable **is** a Situation plus a PTA/vote layer and unlock
> semantics. Everything a Situation already does — bars, thresholds, passives,
> teasers, pools, resolutions, effects, thumbnails, hot-reload, self-test — is
> **inherited** and is **not** re-explained here. Read the Situation guide first;
> this document only covers what Unlockables *add*.
>
> This guide is both the **design rationale** and the **practical API/workflow**
> reference for Unlockables — it is intended to be self-contained. Preview
> pictograms are shared with the Situation system and documented in full in the
> Situation guide (§18); this document summarizes their Unlockable use.

---

## Contents

> **New here and just want to build one?** Read the Situation guide's Quick start
> first (an Unlockable *is* a Situation), then [Quick start — your first
> Unlockable](#quick-start--your-first-unlockable) below, then §1–§4 and §10–§12.
> [Troubleshooting](#troubleshooting) is at the end.

- [Quick start — your first Unlockable](#quick-start--your-first-unlockable)
1. [What is an Unlockable?](#1-what-is-an-unlockable)
2. [Unlockable vs. Situation — what the class adds](#2-unlockable-vs-situation--what-the-class-adds)
3. [Lifecycle of an Unlockable](#3-lifecycle-of-an-unlockable)
4. [The building blocks](#4-the-building-blocks)
5. [The PTA vote](#5-the-pta-vote)
6. [Money costs (escrow)](#6-money-costs-escrow)
7. [Groups & building-upgrade chains](#7-groups--building-upgrade-chains)
8. [Unlock effects & what unlocking means](#8-unlock-effects--what-unlocking-means)
9. [Preview pictograms](#9-preview-pictograms)
10. [The definition helper (author API)](#10-the-definition-helper-author-api)
11. [Full example](#11-full-example)
12. [Wiring Unlockables into the game](#12-wiring-unlockables-into-the-game)
13. [Implementing Unlockables in a mod](#13-implementing-unlockables-in-a-mod)
14. [Conventions (not enforced, but important)](#14-conventions-not-enforced-but-important)
- [Troubleshooting](#troubleshooting)
15. [Reference tables](#15-reference-tables)

---

## Quick start — your first Unlockable

An Unlockable is a Situation with the PTA-vote layer pre-built. So you author very
little: the constructor injects the bars, the vote, the cancel, and the resolutions
([§2](#2-unlockable-vs-situation--what-the-class-adds)).

### 1. Define the smallest possible Unlockable

You supply: a `type_key`, a `key`, a display `name`, the `inject_default_measure`
flag, your **visibility condition(s)**, and your **unlock effect**. Add it inside
`register_unlockables(...)` in `label load_unlockables` (base) — or your own mod
label ([§13](#13-implementing-unlockables-in-a-mod)):

```python
Unlockable("rule", "my_first_rule", "My First Rule", True,  # inject_default_measure
    SituationDescription(["A short description of the rule."]),
    LevelCondition("2", True),                               # when it becomes visible
    SituationEffectSetGameData("my_first_rule_active", True, "Rule in force"),  # unlock effect
),
```

The three faction bars (`Students`/`Parents`/`Teachers`), Schedule Vote, Cancel and
Persuade measures, and the unlock resolutions are all injected automatically.

### 2. Reload

`register_unlockables` runs on every load. Reload (or start a new game). It is now
registered and, once its visibility condition is met, **listed** in the journal —
but not yet started.

### 3. Introduce it, campaign, and vote

- Start it via the journal's **"Start Introducing"** button, or from the **Ren'Py
  console** (`Shift+O`): `unlockable_manager.get_unlockable_by_key("my_first_rule").activate()`.
- Raise faction support (events, the **Persuade** measure, stats), then use
  **Schedule Vote**. The vote resolves at the next Friday PTA meeting; success
  probability comes from the bar fills ([§5](#5-the-pta-vote)).

### 4. Verify

- Journal → Unlockables page (filtered by the `rule` tab): it should be listed,
  then show "View Situation" while running, then the unlocked status after a won
  vote.
- If it's missing or mis-behaving, open the Journal **log view**, category filter
  `situation` (Unlockables log under the same category), and check for self-test
  errors — including the money-escrow codes 800–803 ([§15](#15-reference-tables)).

### Where to go next

Read [§1](#1-what-is-an-unlockable)–[§4](#4-the-building-blocks) for the model, then
[§10](#10-the-definition-helper-author-api)–[§12](#12-wiring-unlockables-into-the-game)
for the full API and wiring. [§5](#5-the-pta-vote)–[§9](#9-preview-pictograms) cover
the vote, money costs, upgrade chains, unlock effects and pictograms;
[Troubleshooting](#troubleshooting) covers the usual snags.

---

## 1. What is an Unlockable?

An **Unlockable** represents something the player can permanently unlock at the
school — a **rule**, a **club**, or a **building** (upgrade). Examples: a dress
code, a sports club, opening the cafeteria building.

Every Unlockable is freed through **exactly one path**: a **PTA vote**. There is
no second unlock mechanism and no direct-unlock shortcut. Even a trivially-unlocked
Unlockable is built as a Situation whose vote is easy to win. This is the whole
point of the rebuild: the old three classes (`Rule`, `Club`, `Building`) collapsed
into **one** class, `Unlockable`, distinguished only by a `type_key` string.

Technically an `Unlockable` **is a `Situation`** (it subclasses it) and is stored
in the same `situation_manager`. On top of the Situation it adds:

- a **`type_key`** (the category: `rule` / `club` / `building` / …),
- a **visibility `ConditionStorage`** (when the Unlockable is listed in the journal),
- **unlock semantics** (the unlocked flag, and unlock effects that run on a won vote),
- an injected **PTA-vote layer**: a *Schedule Vote* measure, a *Cancel* measure,
  optional *Persuade* measure, three faction bars, and the resolutions that fire
  the unlock.

Because it is a Situation, the player interacts with it through the **same bar and
hint UI**. The bars here represent **PTA faction support** (Students / Parents /
Teachers), and their fill level drives the **probability** that the vote passes —
they are *not* an unlock gate by themselves.

---

## 2. Unlockable vs. Situation — what the class adds

When you construct an `Unlockable`, the constructor **rewrites your element list**
before handing it to `Situation.__init__`. Knowing exactly what it injects is the
key to authoring one correctly. Given your `*elements`, it:

1. **Sorts your elements by role:**
   - bare `Condition`s → the **visibility** `ConditionStorage` (not situation gates).
   - an `UnlockableScheduleVoteConditions(...)` wrapper → **extra gates** on the
     Schedule Vote measure.
   - bare `Effect`s **and** the effects inside any `PositiveResolution` you pass →
     collected as **unlock effects** (they run when the vote passes).
   - `SituationBar`s → kept as your own bars (suppresses the default bars).
   - everything else (thresholds, pools, teasers, `SituationDescription`,
     pictograms, measures, …) → passed through to the Situation unchanged.
2. **Injects the *Schedule Vote* measure** (always, at slot 0). Its gate is
   `VoteProposalFreeCondition()` plus whatever you supplied via
   `UnlockableScheduleVoteConditions`. Its instant effect puts this Unlockable on
   the PTA schedule for next Friday.
3. **Injects the *Cancel* measure** (unless `inject_default_cancel=False`) — a free
   `SituationEffectCancelSituation()`.
4. **Injects the unlock resolutions:** a `ConditionResolution("vote_passed", …)`
   gated on a won vote, and a `PositiveResolution("ALL", …)` also gated on a won
   vote. Both carry an `UnlockableUnlockEffect` **plus your unlock effects**.
5. **Injects the three default faction bars** (`Students`, `Parents`, `Teachers`,
   `limits=(0, 100)`, slow regular decrease) — **only if you passed no bars of
   your own.**
6. **Injects the *Persuade* measure** (only if `inject_default_measure=True`) — a
   day-cooldown measure that nudges **all** bars up by `range_percent`.

So the minimum you must actually author is: a `type_key`, a `key`, a display
`name`, the `inject_default_measure` flag, your **visibility conditions**, and your
**unlock effects** (what actually happens when it passes). Bars, vote, cancel and
resolutions come for free.

> **Consequence:** never pass a `NegativeResolution` expecting the Situation's
> usual negative end — an Unlockable does not "fail" on bar-min; it simply stays
> unwon until the player wins a vote or cancels. The only resolutions are the two
> injected vote-passed paths.

---

## 3. Lifecycle of an Unlockable

An Unlockable reuses the full Situation lifecycle (inactive → teaser → active →
completed/cancelled) and adds an unlock state on top. What the player sees is a
**three-phase context button** in the journal, driven by the Situation state:

| Phase | Situation state | Journal button |
|-------|-----------------|----------------|
| Not started yet | no active Situation (visibility conditions met) | **"Start Introducing"** → activates the Situation |
| Running | Situation `active` | **"View Situation"** → the Situation page |
| Unlocked | resolved (vote won) | unlocked status (link to the completed Situation) |

Note the Unlockable's `status` property maps the Situation's `teaser_active`
visibility back to `inactive` — a pre-activation teaser does not count as "running"
for the button.

### Visible vs. unlocked

- **Visible** (`is_visible()`): the visibility `ConditionStorage` is fulfilled.
  Visible = **listed and usable**; there is deliberately no separate "usable" gate.
- **Unlocked** (`is_unlocked()`): the game-data flag `{situation_key}_unlocked`
  exists — written by `UnlockableUnlockEffect` when the vote passes.

### The vote round

While active, the player raises faction support (events, Persuade, stats via
`stat_weights`) and then uses **Schedule Vote**. On the next Friday PTA meeting the
vote is rolled from the bar fills (see [§5](#5-the-pta-vote)). On success the unlock
resolutions fire; on failure the bars take a penalty and the player can try again.

### Hot reload & orphans

Because an Unlockable is a Situation registered through
`situation_manager.load_situation`, the **same reload and orphan rules apply**
verbatim — see *Hot reload* and *Missing definitions* in the Situation guide.
Register on every load; the definition is refreshed via `update_data`, the runtime
state (bar values, unlocked flag, which measures ran) is preserved. A missing
definition soft-invalidates; a returning one revives.

---

## 4. The building blocks

An Unlockable is authored as a small header plus the situation elements you choose
to add. The pieces unique to Unlockables:

### `type_key` (the category)

A plain string — `rule`, `club`, `building`, or any new category you invent. It
becomes the key prefix (`rule:dress_code`) and the journal filter tab. There is
**no registry** of categories: a new `type_key` string simply creates a new
category. `get_type_keys()` derives the tab list from whatever is registered.

### `key` and the situation key

The stable identity within its type. The full situation key is
`type_key:key` — or `type_key:key:group_index` for grouped Unlockables (see
[§7](#7-groups--building-upgrade-chains)). Like every Situation key, this is
**identity across saves** — never rename it.

### Visibility conditions (bare `Condition` elements)

Any `Condition` passed directly as an element goes into the visibility
`ConditionStorage`. These decide **when the Unlockable appears in the journal** —
nothing more. They do **not** block the vote and are **not** shown as vote
requirements.

> **Migration note:** old vote-scoring conditions (legacy `blocking=False` on
> conditions) must be **dropped**, not turned into visibility gates. Visibility
> answers "from when is this listed"; the vote's difficulty comes from the bars,
> not from conditions.

### Faction bars (the PTA)

If you pass no bars, three are injected: `Students`, `Parents`, `Teachers`,
`limits=(0, 100)`, with a slow regular decrease (return pressure). Each bar's fill
ratio is one faction's yes-probability at the vote. Pass your own `Bar(...)`
elements to override the whole set (e.g. different names, weights, `stat_weights`,
or a two-faction Unlockable). The moment you supply **one** bar, the defaults are
suppressed — you own the full bar set.

### The injected measures

- **Schedule Vote** — always present; the player's "call the vote" action.
- **Cancel** — free by default; set `inject_default_cancel=False` to supply your
  own (e.g. a Cancel with a reputation cost) as a `MeasureOption`/`SituationMeasure`
  element instead.
- **Persuade** — only with `inject_default_measure=True`; a simple day-cooldown push
  on all bars. For anything richer, leave it off and author your own measures.

### Unlock effects (bare `Effect` elements or a `PositiveResolution`)

What actually happens on a won vote. Provide them either as **bare `Effect`s** in
the element list, or grouped inside a `PositiveResolution("ALL", …effects…)` — both
are collected into the same unlock-effect set and attached to **both** injected
resolutions, alongside the automatic `UnlockableUnlockEffect`. See
[§8](#8-unlock-effects--what-unlocking-means).

### Description, thumbnail, teasers, thresholds, pools, pictograms

All inherited from Situation and passed straight through:
`SituationDescription([...])`, `thumbnail="images/..."`, `Teaser(...)`,
`AutoThreshold`/`BlockingThreshold`, `SituationPool(...)`, `Picto(...)`. Use them
exactly as in a Situation. Thresholds and pools are how you hang **PTA-discussion
events** on the bar (no special API — see [§12](#injected-pta-discussion-events)).

---

## 5. The PTA vote

The vote is the single unlock gate, and it is **probabilistic**, not a threshold.

### Scheduling

**Schedule Vote** does not roll immediately — it puts the Unlockable on the
schedule for the **next Friday PTA meeting** (`UnlockableScheduleVoteEffect` →
`ScheduleVoteEffect` → `voteProposal`). Its gate is always
`VoteProposalFreeCondition()` (only one proposal can be scheduled at a time); add
more gates with `UnlockableScheduleVoteConditions(cond, …)`.

### The roll

At the meeting, **one yes/no vote is rolled per bar** from that bar's fill ratio
(`bar.value / bar.max`, clamped to `[0, 1]`). So bars do **not** need to be at
100 % — a 70 %-filled bar means roughly a 70 % chance that faction votes yes. The
combined fill (`get_vote_probability()`) is the overall likelihood.

### Success and failure

- **Success** → the `vote_passed` resolution (and, if bars are also maxed, the
  `PositiveResolution`) fires: `UnlockableUnlockEffect` sets the unlocked flag and
  your unlock effects apply.
- **Failure** → `apply_vote_failure_penalty()` pushes **all** bars down (default
  `-15`). The player rebuilds support and can schedule again.

> **Design point:** the bars are the *campaign*, the vote is the *outcome*. Raising
> support improves your odds; it never guarantees the unlock. This keeps the same
> return-pressure feel as Situations — support decays, and a rushed vote can lose.

---

## 6. Money costs (escrow)

A vote can cost money (e.g. building a cafeteria). The cost is **escrowed** so it
is reserved when the vote is scheduled and only truly spent if the vote passes —
never double-charged, and refunded on failure or cancel.

You wire it as a **matched pair**:

1. A **`MoneyCondition`** on the Schedule Vote measure — supply it via
   `UnlockableScheduleVoteConditions(MoneyCondition("1500+"))`. This is the amount
   reserved.
2. A **cost `MoneyEffect`** among your unlock effects — an `ADD` effect with a
   **negative** value of the **same absolute amount**:
   `MoneyEffect("cafeteria_cost", -1500, "ADD")`.

The constructor auto-tags the cost effect with a `MoneyEscrowOption` so that, on a
won vote, it consumes the reserved stash instead of charging again. On
schedule the amount is set aside with `reserve_money`; on failure/cancel it is
returned with `release_money`.

The pairing is matched by **absolute value**, and the self-test enforces it
(codes 800–803, see [§15](#15-reference-tables)): every `MoneyCondition` needs a
cost `MoneyEffect` of equal magnitude carrying the escrow option, and vice versa.

---

## 7. Groups & building-upgrade chains

A **building upgrade** is not a special mechanism — it is a **chain of individual
Unlockables** sharing one `key`, each with a distinct `group_index` (the level).
This replaces the old `Building.upgrade` machinery.

```python
Unlockable("building", "cafeteria", "Cafeteria I", True, …, group_index=1),
Unlockable("building", "cafeteria", "Cafeteria II", True, …, group_index=2),
Unlockable("building", "cafeteria", "Cafeteria III", True, …, group_index=3),
```

The manager handles the chain for you:

- **One journal row per key.** The list shows the *default member* — the lowest
  index that isn't unlocked yet, or the highest if all are unlocked.
- **Consecutive levels required.** Indices may start anywhere but must have no
  gaps; a gap invalidates the whole group (`run_unlockables_test`). They need not
  start at 1.
- **Auto prerequisite.** `apply_group_chain_conditions()` inserts a
  `GameDataCondition("{key}_level", prev_index)` on each member so level *n*
  only becomes visible after level *n−1* is unlocked. Don't add this by hand.
- **Atomic upgrade.** When a level unlocks, `apply_group_upgrade_transition`
  **reverts the previous member's content effects** before applying the new
  level's — so upgrades replace rather than stack (see the revert semantics below).
- **Persistence.** `UnlockableUnlockEffect` writes `{situation_key}_unlocked` and
  the group's `{key}_level`.

A non-grouped Unlockable simply omits `group_index` (stays `-1`) and is a single
row.

> **Upgrade-revert vs. Situation revert:** the same rule from the Situation guide
> applies — reverting a modifier-based effect *stops the ongoing contribution*, it
> does not roll back accumulated value; only `SituationEffectSetGameData` /
> game-data-style effects truly restore. Design upgrade content effects with this
> in mind (a level-2 building effect should be the full state for level 2, since
> level 1's transient effects are pulled on transition).

---

## 8. Unlock effects & what unlocking means

Unlocking does exactly two guaranteed things: it sets `{situation_key}_unlocked`,
and (for groups) writes `{key}_level`. **Everything else is your unlock effects.**
A won vote applies whatever effects you passed — so *this* is where the rule/club/
building actually takes effect.

Common unlock effects:

| Effect | Use |
|--------|-----|
| `LevelEffect(name, value, "SET"/"ADD", char)` | raise a character/school level |
| `MoneyEffect(name, -cost, "ADD")` | the vote's escrowed money cost (see [§6](#6-money-costs-escrow)) |
| `BuildingOpenEffect(building_key)` | make a map location enterable |
| `BuildingCloseEffect(building_key)` | close a map location |
| `SituationEffectSetGameData(key, value, desc)` | set a flag other content reads |
| any `Effect` | whatever the unlock should do |

### Map access is orthogonal

Unlocking a building Unlockable does **not** automatically open its map location.
The two are deliberately separate systems — unlock state lives on the Unlockable,
map-open state lives on the `BuildingManager` (`{key}:open` / `{key}:closed`
collections). If you want the unlock to also open the door, add a
**`BuildingOpenEffect(building_key)`** to the unlock effects **explicitly**.

---

## 9. Preview pictograms

Pictograms are small **descriptive preview marks** on an Unlockable's bars or on
the Unlockable itself — "persuade the teachers", "win over the students". They
replace the old condition-icons next to the unlock image. They are **purely
descriptive**: they check nothing, gate nothing, unlock nothing.

Attach one inline with the `Picto(key)` vehicle, either on a bar or as a top-level
element:

```python
Bar("Students", Picto("students_support"), limits=(0, 100)),
# or at situation level:
Unlockable("rule", "dress_code", "Dress Code", True,
    Picto("factions_all"), …),
```

`Picto("key")` resolves a definition from the central pictogram registry (icon +
label + tooltip templates). A bar-bound pictogram may show that bar's live value in
its tooltip; a situation-bound one is identity-only and stays purely descriptive.
Missing/broken pictograms **soft-fail** (skipped at render, the Unlockable still
works). A mod can add pictograms to an existing Unlockable via
`situation_manager.add_pictogram(situation_key, picto_key, bar_key=…)`. Full
details — the reference-not-object model, the load-time key-completeness check, and
soft-fail behavior — are in the Situation guide, §18.

---

## 10. The definition helper (author API)

Unlockables are defined declaratively via the `Unlockable(...)` constructor and
registered with `register_unlockables(...)`.

```python
Unlockable(
    type_key,                 # category string: "rule" / "club" / "building" / …
    key,                      # stable key within the type
    name,                     # display name (also the group-member label)
    inject_default_measure,   # True → add the free "Persuade" measure
    *elements,                # conditions, effects, bars, description, teasers,
                              #   thresholds, pools, pictograms, custom measures,
                              #   optional PositiveResolution wrapping unlock effects,
                              #   optional UnlockableScheduleVoteConditions(...)
    thumbnail=None,           # journal image (inherited Situation thumbnail)
    group_index=-1,           # chain level; -1 = standalone
    inject_default_cancel=True,  # False → supply your own Cancel measure
)
```

Supporting helpers you will use inside `*elements`:

| Helper / class | Role |
|----------------|------|
| `UnlockableScheduleVoteConditions(*conditions)` | extra gates (incl. `MoneyCondition`) on Schedule Vote |
| `SituationDescription([lines…])` | the description block |
| `Bar(key, *pictos, limits=(0,100), stat_weights=…, …)` | custom faction/progress bar |
| `MeasureOption(...)` / `SituationMeasure(...)` | custom measures (e.g. a costed Cancel) |
| `Picto(key)` | preview pictogram reference |
| `LevelEffect` / `MoneyEffect` / `BuildingOpenEffect` / … | unlock effects |
| `register_unlockables(*unlockables)` | loads/updates templates (call in `label load_unlockables`) |

Runtime lookups (for events, tutorial, other content):

| Helper | Returns |
|--------|---------|
| `is_unlockable_unlocked(key, index=-1)` | bool — is it unlocked |
| `UnlockableCondition(key, index=-1)` | a `Condition` for the same check |
| `unlockable_manager.get_unlockable_by_key(key, index=-1)` | the `Unlockable` (default or specific member) |

> **Note on `key` in `is_unlockable_unlocked` / `UnlockableCondition`:** pass the
> **group key** (e.g. `"cafeteria"`), not the full `type_key:key` situation key.

---

## 11. Full example

A single rule with a money-free vote, custom visibility, and a concrete unlock
effect (abridged from `load_unlockables`):

```python
register_unlockables(
    Unlockable("rule", "dress_code", "Dress Code", True,   # inject_default_measure
        SituationDescription([
            "Introduce a school-wide dress code.",
            "The PTA must approve it before it takes effect.",
        ]),

        # --- Visibility: only listed once the school has reached level 2 ---
        LevelCondition("2", True),

        # --- Custom faction bars with preview pictograms (override defaults) ---
        Bar("Students", Picto("students_support"), limits=(0, 100),
            stat_weights={INHIBITION: 0.4}),
        Bar("Parents",  Picto("parents_support"),  limits=(0, 100),
            stat_weights={REPUTATION: 0.4}),
        Bar("Teachers", Picto("teachers_support"), limits=(0, 100),
            stat_weights={REPUTATION: 0.3}),

        # --- Unlock effect: what happens when the vote passes ---
        SituationEffectSetGameData("dress_code_active", True, "Dress code in force"),

        thumbnail="images/journal/rules/dress_code.webp",
    ),
)
```

A **building upgrade** with a money cost on level 2's vote:

```python
register_unlockables(
    Unlockable("building", "cafeteria", "Cafeteria I", True,
        SituationDescription(["Open a basic cafeteria."]),
        BuildingCondition("school_ground"),            # visibility
        BuildingOpenEffect("cafeteria"),               # unlock → open the map location
        thumbnail="images/journal/buildings/cafeteria_1.webp",
        group_index=1,
    ),
    Unlockable("building", "cafeteria", "Cafeteria II", True,
        SituationDescription(["Expand the cafeteria. Costs $1500."]),
        # money cost: MoneyCondition on the vote + matching negative MoneyEffect
        UnlockableScheduleVoteConditions(MoneyCondition("1500+")),
        MoneyEffect("cafeteria_2_cost", -1500, "ADD"),
        thumbnail="images/journal/buildings/cafeteria_2.webp",
        group_index=2,
    ),
)
```

The vote, cancel, faction bars (level 1 uses the injected defaults), unlock
resolutions, the `_unlocked`/`_level` persistence, and the level-2 prerequisite on
level 1 are all injected automatically.

---

## 12. Wiring Unlockables into the game

### Registering

Base Unlockables are registered in `label load_unlockables`, which is called in the
start sequence (and after every load). Wrap `set_current_mod('base')` and your
`register_unlockables(...)` call exactly as the base file does. `register_unlockables`
is idempotent and reload-safe (it delegates to `situation_manager.load_situation`).

### Activating (Start Introducing)

The journal's **"Start Introducing"** button activates the underlying Situation:

```python
$ unlockable_manager.get_unlockable_by_key("dress_code").activate()
```

From then on it behaves like an active Situation — bars move, the player campaigns,
schedules the vote.

### Gating other content on an unlock

Events, tutorial steps, and other Situations check the unlocked state:

```python
# as a plain check
if is_unlockable_unlocked("dress_code"):
    ...

# as a Condition (e.g. on an event or another situation element)
UnlockableCondition("cafeteria", 2)   # cafeteria at least level 2
```

<a id="injected-pta-discussion-events"></a>
### Injected PTA-discussion events

An event that should only appear while an Unlockable's campaign is in a certain bar
range is hung into a building pool exactly like a Situation event — declare a
`SituationPool(pool_key, min, max)` on the Unlockable and gate the event with the
matching pool/threshold conditions (`SituationPoolCondition`,
`ThresholdReachedCondition`). No Unlockable-specific API is needed; the Situation
pool mechanism already covers "PTA discussion at these bar levels".

---

## 13. Implementing Unlockables in a mod

Unlockables are fully mod-capable — nothing is hard-wired except through keys and
conditions. Because an Unlockable **is** a Situation, the mod rules from the
Situation guide apply unchanged; only the registration entry point differs.

### Path A — Register your own Unlockables

```python
init python:
    register_start_method("load_unlockables_mymod")   # queue into the lifecycle wave

label load_unlockables_mymod:
    $ set_current_mod('my_mod')

    $ register_unlockables(
        Unlockable("club", "mymod_chess_club", "Chess Club", True,
            SituationDescription(["Found a chess club."]),
            BuildingCondition("school_ground"),
            SituationEffectSetGameData("mymod_chess_club_active", True, "Chess club open"),
            thumbnail="images/journal/clubs/chess.webp",
        ),
    )
```

> **Register your label into `start_methods` — do not register from the init path.**
> Unlockables ride the **same lifecycle wave** as Situations (they register through
> `situation_manager.load_situation`). The same reasoning as in the Situation guide
> applies verbatim: queue your label with `register_start_method(...)` so it runs
> inside the `begin_check` → `finalize_check` window, after the base loaders.
> Registering at init time can leave modifiers/checks unswept. If your mod is
> missing, its Unlockables soft-invalidate (state kept) and revive when it returns.

> **Image paths auto-redirect to your mod folder.** As with Situations, the
> `thumbnail` (and any `Teaser(image=…)` / `Picto(...)`) captured while your
> `set_current_mod` is active is prefixed with your mod's path — so write plain
> paths relative to your mod root (`thumbnail="images/journal/clubs/chess.webp"`),
> never `mods/MyMod/...`. See the Situation guide, §8.

Prefix mod keys (`mymod_...`) and, if you invent a new `type_key`, remember it also
becomes a new journal filter tab automatically.

### Path B — Extend existing Unlockables

Because Unlockables are Situations, the Situation pull-architecture extension
points work too: add a **teaser** to an existing Unlockable
(`get_situation(...).add_teaser(...)`), add a **pictogram**
(`situation_manager.add_pictogram(...)`), or inject **PTA-discussion events** into
its pools — all without touching base code. Register permanent extensions through
the reload-safe load path (a runtime-only `add_teaser` can be synced away by a later
`register_unlockables` pass; see the Situation guide's Path B note).

### What a mod can contribute

- New Unlockables (any `type_key`, standalone or grouped chains).
- New **unlock effects** (reuse existing `Effect` types; custom subclasses possible).
- New **injected events** into building pools tied to an Unlockable's bar ranges.
- New **teasers / pictograms** on base Unlockables.

---

## 14. Conventions (not enforced, but important)

The Situation conventions all apply (stable keys, no runtime state in the template,
hint-text voice, self-test discipline). Additional Unlockable-specific rules:

### `type_key` is a category, not decoration
Pick from the established set (`rule`, `club`, `building`) unless you truly need a
new category — every distinct `type_key` becomes a journal filter tab. Keep it
lowercase and stable; it is part of the situation key.

### Visibility conditions are "from when listed", nothing else
Do not smuggle vote difficulty into them. The vote's difficulty is the bars. Old
vote-scoring conditions must be **removed**, not converted into visibility gates.
### Always supply real unlock effects
`UnlockableUnlockEffect` only sets a flag. If the unlock is supposed to *do*
something (open a building, set a rule flag, raise a level), that must be an
explicit unlock effect. A "building" Unlockable with no `BuildingOpenEffect` unlocks
a door that never opens.

### Pair every money cost
A `MoneyCondition` on the vote and its cost `MoneyEffect` must match by absolute
value, or the self-test (800–803) invalidates the Unlockable. Don't charge money
with a bare `MoneyEffect` and no escrow condition, and don't gate on money you never
actually spend.

### Groups: consecutive, no gaps, don't hand-wire the prerequisite
Give chain members consecutive `group_index` values and let
`apply_group_chain_conditions` insert the "previous level" prerequisite. A gap
invalidates the whole group. Design each level's content effects as the **full
state** for that level (upgrade transition reverts the previous level's transient
effects).

### Map-open is your responsibility
Unlock ≠ door open. Add `BuildingOpenEffect` / `BuildingCloseEffect` explicitly if
the unlock should change map access.

### Custom bars replace, not extend, the defaults
Passing one `Bar` suppresses all three injected faction bars. If you want the
standard three plus a fourth, you must declare all four yourself.

---

## Troubleshooting

Symptom-first list for Unlockables. The Situation guide's troubleshooting applies
too (an Unlockable is a Situation). When in doubt, **check the log** (Journal log
view, category `situation`).

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| **Not listed in the journal** | Visibility condition unmet. | Visibility = listed. Check your bare `Condition`s ([§4](#4-the-building-blocks)); they must be fulfilled to show. |
| | Rejected by the self-test. | Check the log; common Unlockable-specific codes are the money-escrow pair 800–803 ([§6](#6-money-costs-escrow)). |
| | Group has a gap in `group_index`. | Levels must be consecutive, no gaps — a gap invalidates the whole group ([§7](#7-groups--building-upgrade-chains)). |
| **The vote is scheduled but nothing happens** | The vote resolves at the **next Friday** PTA meeting, not immediately. | Advance to Friday; only one proposal can be scheduled at a time (`VoteProposalFreeCondition`). |
| **The vote keeps failing** | Faction bars are too low — success is probabilistic from bar fills. | Raise support (events, Persuade, `stat_weights`) before scheduling; each failure also applies a bar penalty ([§5](#5-the-pta-vote)). |
| **It "unlocks" but nothing visibly changes** | `UnlockableUnlockEffect` only sets a flag; you supplied no real unlock effect. | Add the actual effect (rule flag, `LevelEffect`, etc.) as a bare `Effect` or in a `PositiveResolution` ([§8](#8-unlock-effects--what-unlocking-means)). |
| **A building unlocked but its map location is still closed** | Unlock ≠ map-open; they are orthogonal. | Add `BuildingOpenEffect(building_key)` to the unlock effects ([§8](#map-access-is-orthogonal)). |
| **The next group level won't appear** | It requires the previous level to be unlocked first. | Expected — the auto-inserted prerequisite gates it until level *n−1* is unlocked ([§7](#7-groups--building-upgrade-chains)). |
| **Self-test 800–803 on load** | `MoneyCondition` on Schedule Vote and its cost `MoneyEffect` don't pair by absolute value. | Match the amounts exactly; the escrow option is auto-attached ([§6](#6-money-costs-escrow)). |

---

## 15. Reference tables

### The injected pieces (recap)

| Injected | When | Detail |
|----------|------|--------|
| Schedule Vote measure | always | gate `VoteProposalFreeCondition` + your `UnlockableScheduleVoteConditions` |
| Cancel measure | `inject_default_cancel=True` | free `SituationEffectCancelSituation` |
| `vote_passed` + `PositiveResolution` | always | carry `UnlockableUnlockEffect` + your unlock effects |
| 3 faction bars | only if you passed no bars | `Students`/`Parents`/`Teachers`, `(0,100)`, slow decrease |
| Persuade measure | `inject_default_measure=True` | day cooldown, `range_percent` push on all bars |

### Persistence keys

| Key | Written by | Meaning |
|-----|-----------|---------|
| `{type_key}:{key}_unlocked` (or `…:{group_index}_unlocked`) | `UnlockableUnlockEffect` | unlocked flag |
| `{key}_level` | `UnlockableUnlockEffect` (groups) | highest unlocked group level |
| `vote_{situation_key}_{effect_name}` | escrow | reserved money stash key |

### Established `type_key`s
`rule` · `club` · `building` (new categories: just use a new string)

### Unlockable-specific self-test codes
| Code | Meaning |
|------|---------|
| 800 | `MoneyCondition` value on Schedule Vote isn't a usable escrow amount |
| 801 | `MoneyCondition` has no matching cost `MoneyEffect` (equal absolute value) |
| 802 | matching `MoneyEffect` is missing its `MoneyEscrowOption` |
| 803 | cost `MoneyEffect` has no matching `MoneyCondition` on Schedule Vote |

(Group-consistency failures are reported separately by `run_unlockables_test` —
"Group X has non-consecutive levels" — and invalidate the group.) All inherited
Situation self-test codes (700–793) still apply.

### Runtime lookups
| Goal | Call |
|------|------|
| Is it unlocked (bool) | `is_unlockable_unlocked(key, index=-1)` |
| Unlocked as a condition | `UnlockableCondition(key, index=-1)` |
| Get the Unlockable | `unlockable_manager.get_unlockable_by_key(key, index=-1)` |
| Default (list) member | `unlockable_manager.get_default_member(key)` |
| All members of a group | `unlockable_manager.get_unlockables_by_key(key)` |

### Related files
- `game/scripts/journal/unlockables.rpy` — `Unlockable`, `UnlockableManager`, `register_unlockables`, `load_unlockables`
- [Building Situations](Building-Situations) — the Situation base (read first; pictograms in §18)
- `game/scripts/journal/pictograms.rpy` — pictogram registry
- `game/scripts/effects.rpy` — `UnlockableUnlockEffect`, `BuildingOpen/CloseEffect`, `LevelEffect`, `MoneyEffect`
- `game/scripts/conditions.rpy` — `UnlockableCondition`, `MoneyCondition`, `VoteProposalFreeCondition`
