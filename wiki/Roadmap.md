> [!WARNING]
> **Spoilers.** This page describes planned story beats for upcoming versions: new characters, level transitions and story events.

[Home](Home) › Roadmap

> **Audience:** The dev team and modders who want to know where *Mind the School*
> is heading after the lab intro: potions as gameplay, hypnosis, the beach camp,
> the new campus cast, and the engine systems all of that needs.
>
> **Scope:** Design direction only. **Nothing on this page is built yet.** Each
> section says what it is, why it exists and how it is meant to work. Lore that
> is already canon lives in [Lore](Lore); this page is the plan on top of it.
>
> **Status marks.** **[Decided]** — agreed design, build to it;
> **[Proposal]** — a suggestion from the design talks that isn't confirmed yet;
> **[Open]** — deliberately unresolved, needs a decision before it is written.

---

## Contents

1. [The big picture](#1-the-big-picture)
2. [Story timeline](#2-story-timeline)
3. [Potions — Type 1 (active)](#3-potions--type-1-active)
4. [Potions — Type 2 (passive)](#4-potions--type-2-passive)
5. [Orgazyme — the last 70 ml](#5-orgazyme--the-last-70-ml)
6. [The friend — the biochemist](#6-the-friend--the-biochemist)
7. [Hypnosis](#7-hypnosis)
8. [Level 3 → 4: the beach camp](#8-level-3--4-the-beach-camp)
9. [Engine: map registry](#9-engine-map-registry)
10. [Engine: event flags](#10-engine-event-flags)
11. [Engine: situation pause & the camp situation](#11-engine-situation-pause--the-camp-situation)
12. [Engine: kink menu](#12-engine-kink-menu)
13. [Build order](#13-build-order)
14. [Lore follow-ups](#14-lore-follow-ups)
15. [Open questions](#15-open-questions)

---

## 1. The big picture

The lab intro ends at **school level 3** with the Orgazyme catalyst almost gone
and Emiko's budget proposal for the old lab building on the desk. From there,
conditioning stops being a single story chain and becomes **gameplay**:

| Tool | What it does | Lore role |
|------|--------------|-----------|
| **Type 1 potions** (drink / inhale) | the player uses them at a location → a spicy event | the acute *dose*: strong, short, hazy memory, small residue |
| **Type 2 potions** | produced in the full lab, run in the background | the ambient serum the whole school marinates in |
| **Hypnosis** | rare, per-character, needs its own resource | the *mind* side: breaks social norms, not desire |
| **PTA votes** | open rules, buildings, the beach | the institutional rail |

[Lore §7](Lore#7-how-the-change-actually-works--the-two-rails) already says
*serum = slow chemical pressure, hypnosis = rare spotlight*. The roadmap turns
that into systems: **the serum works on the body and desire, hypnosis on the mind
and shame.** That split decides which tool drives which level step.

---

## 2. Story timeline

The chronological order the content is meant to play out in. Levels are the
campus climate from [School Levels](School-Levels).

| Phase | Story beat | Unlocks / changes |
|-------|------------|-------------------|
| **End of lab intro (L3)** | Party dose (Emiko) → level 3. 70 ml Orgazyme left. Emiko starts the budget proposal for the old lab building. | — (already written) |
| **Level 3** | **The friend arrives**: the biochemist behind the original energizer, now partially amnesiac and petite. Research for a **weaker substitute** starts in the storage-room lab. | Type 1 **drink** potions (random targets, bulk dilution). Friend joins the cast. |
| **Level 3** | **Linh comes on board** as school nurse, dosed with ~30 ml of the remaining Orgazyme so she catches up. | Infirmary as a dosing channel → **targeted** dosing becomes possible later. |
| **Level 3 → 4** | **PTA vote opens the beach.** | Beach as a destination. |
| **Level 3 → 4** | **The beach camp** (~2 weeks, spring–autumn). Heat builds; the first **inhale** preparation debuts at the campfire; parents join for one campfire evening. | Level 4 on resolution. Beach becomes a permanent location. |
| **Level 4 → 5 (latest)** | The remaining ~40 ml of Orgazyme goes to **one more new character**. | New cast member. |
| **Level 4 → 5** | **PTA vote: renovate the science building.** | Full lab → **Type 2** production; the hypnosis compound can be made on purpose. |
| **Level 4 → 5** | **First hypnosis** carries the level 4 → 5 transition (the public/private hinge). | Hypnosis as a tool. |
| **Level 4–5** | Per-character hypnosis chains. | Sandbox sex with *that* character early. |
| **Level 6+** | Open culture. | Sandbox sex with everyone, no hypnosis needed. Hypnosis stays for extreme special scenes. |

The order of the science-building vote versus the camp is flexible; the camp only
needs the beach vote and the inhale preparation.

---

## 3. Potions — Type 1 (active)

**[Decided]** The player uses a potion at a location and gets an event. Two forms:

| Form | Reach | Typical carrier |
|------|-------|-----------------|
| **Drink** | one person up to a small group | coffee pot, punch, a personal mug |
| **Inhale** | a whole room / class | campfire smoke, sauna steam, a closed classroom |

Type 1 potions always need a **rare or limited resource**, so each use is a
decision.

### Flow

**[Decided]**

```text
location action "Use potion"
  └─ EventSelect { "Drink": drink_storage, "Inhale": inhale_storage }
       ├─ EventComposite "potion_drink_<location>"    (ItemCondition: a drink potion)
       │     └─ FragmentStorage potion_drink_<location>_fragments
       └─ EventComposite "potion_inhale_<location>"   (ItemCondition: an inhale potion)
             └─ FragmentStorage potion_inhale_<location>_fragments
```

- One **fragment storage per location and form**. All potion events go into it;
  which potion, level, time or character a fragment needs is defined on the
  fragment itself, and the fragment selection filters on its own. A new potion =
  new fragments, no new wiring.
- `EventSelect` only offers options whose storage has an available event, so
  *Inhale* doesn't show up without an inhale potion.
- **New condition:** `EventComposite` only checks its own conditions, not
  whether any fragment fits. A condition along the lines of
  **"this FragmentStorage has at least N available fragments"** goes on the
  composite, so the menu entry only appears when something can play. Selectors
  are already rolled ahead for deterministic availability checks, so the
  fragment conditions see the same values they will run with.
- **[Proposal]** Remove the potion only after the fragment selection succeeded,
  and leave a small persistent **stat residue** on the affected characters, so a
  use is more than a scene ("the residue moves the level", [Lore §7](Lore#7-how-the-change-actually-works--the-two-rails)).

### Random first, targeted later

**[Decided]** Early on, who gets the dose is **random**; later the player can
**choose**. The in-fiction reason has two halves:

1. **Concentration (lab tech).** The makeshift-lab brew is high-volume, sweet and
   smells fruity. It only hides **diluted in bulk** (the staff-room coffee pot, a
   punch bowl, the water cooler), so whoever drinks from it gets it. Better
   equipment later makes a dose small and neutral enough for **one cup**.
2. **Access (who hands over the cup).** **Linh as school nurse** (vitamin shots,
   routine checks), personal mugs, Emiko handing out drinks.

**[Decided]** Targeting comes with a **generic character picker**: a portrait grid
of `Person`s filtered by a condition that writes the chosen key into a kwarg
(`target`). It's reusable for hypnosis, office invitations and sandbox scenes.

**[Proposal]** The picker only lists characters that have at least one available
fragment, so a pick never leads nowhere.

---

## 4. Potions — Type 2 (passive)

**[Decided]**

- Only possible with the **full lab** in the **science building**, which first
  has to be **renovated by PTA vote**. Emiko's budget proposal at the end of the
  lab intro is the hook.
- Runs in the background: a **weekly cost** (a `payroll_weekly` money modifier, so
  it shows up in the journal's money overview automatically) plus a constant
  **stat drift** through the [Modifiers](Modifiers) system.
- The friend ([§6](#6-the-friend--the-biochemist)) runs the production.

**[Proposal]**

- **Production lines** as slots; lab upgrades add slots.
- Every line needs a **delivery channel** into the school (cafeteria food, the
  water supply, the ventilation) that is unlocked by renovating that facility. Reform
  and corruption stay on one track: reopening the cafeteria is also the serum route.
- The existing per-level stat caps (e.g. corruption ≤ level × 10) mean passive
  drift **fills up** to the cap; the next level step still needs events or the PTA.
- Later: passive production slowly raises the inspector's **Scrutiny**
  ([Lore §9](Lore#9-the-opposition--the-regional-inspector)).

---

## 5. Orgazyme — the last 70 ml

**[Decided]**

- Orgazyme is **not** a reusable potion resource. It carried the level 2 → 3 jump,
  so spending it six more times at level 3 would ask where that strength went. The
  lab intro also established that it **can't be reconstructed**: the enzymes are
  long dead and the formula went under with Cumulus Laboratories (dissolved 1998).
- The last 70 ml (10 ml per head is the standard dose) is reserved for
  **newcomers who have to catch up** to the campus:
  - **~30 ml for Linh** at level 3. An outside nurse would be the first to notice
    the campus acting strangely, so bringing her on board is necessary, not a
    bonus. A newcomer starting from zero gets more than the standard dose.
  - **~40 ml for one more new character** by level 4–5 at the latest.
- This gives a story reason why only a few new characters join around level 3:
  as many as the Orgazyme can catch up.
- The **substitute** the friend develops is **weaker** at first, so finding it
  doesn't instantly jump the school to level 4.

**[Proposal]** Potency grows with the **recipe and lab tier**, not with a new
ingredient for every level.

---

## 6. The friend — the biochemist

**[Decided]**

- The "close friend, a biochemist" who supplied the original energizer
  (`first_week_epilogue` in `daily_check.rpy`) is a **woman**. The epilogue
  currently says "him" / "He", which needs changing.
- **Fully on board from the start.** She supplied the potions before and had to
  **go into hiding** after handing them over, so she already worked in that
  territory.
- A **chemistry accident** left her with **partial amnesia** and a **changed body:
  truly petite** (small frame, very small chest). The change is **purely physical**,
  with **no age regression**; she is clearly an adult woman with a career. She
  works on **reversing** it, which gives her her own goal next to the Headmaster's.
- She fills a real cast gap: the Clarks are short but busty and curvy, Miwa is the
  smallest but has a B cup, Linh is slim with a C cup.
- She joins at **level 3** to help with the research, and later runs **Type 2**
  production.
- She needs **no** Orgazyme dose: the accident was her exposure.
- **The serum itself doesn't change bodies.** Her change comes from the accident
  only, which deliberately leaves the door open for a **body-modification mod**.

**[Proposal]**

- The **amnesia sets the research pace**: her own work comes back in fragments,
  and each returned memory is a research step (substitute → inhale preparation →
  hypnosis compound → Type 2).
- Her **reversal research** is where by-products appear, including the hypnosis
  compound.

**[Open]** Who she had to hide from. Leave it unresolved, like the backers; with
the amnesia she may not know exactly herself anymore. A link to the backers is
possible but not canon.

---

## 7. Hypnosis

**[Decided]**

- **First use: the level 4 → 5 transition.** Level 5 is the public/private hinge;
  level 4 is the last level where "don't get caught" is the default tension. That
  barrier is social and psychological, which is hypnosis' job, not the serum's.
- Hypnosis needs its own **rare resource**: a **suggestibility compound**, found
  as a by-product of the potion research. In the makeshift lab it only appears
  rarely and in small amounts; the **full lab** can make it on purpose. That is the
  **brake on early sandbox scenes**, and it lifts later.
- **Hypnosis only works on characters who already carry serum residue.** The
  serum opens the body; only a primed mind takes suggestion.
- After level 5, hypnosis runs **alongside** Type 1 potions.
- **Sandbox sex:**
  - level 4–5: per-character hypnosis chains (several sessions); once a character
    is conditioned, sandbox with **her** opens early.
  - **level 6+:** sandbox with everyone, **no hypnosis needed** (level 6 = "always a
    free yes").
  - Hypnosis then remains for extreme special scenes.
- Kept **outside** the item potion flow, as story and special events, so it stays
  rare as [Lore §7](Lore#7-how-the-change-actually-works--the-two-rails) asks.

**[Open]** How the level 4 → 5 transition reaches the whole campus when hypnosis
works per person: a group session, or a few key figures who tip the public climate.

---

## 8. Level 3 → 4: the beach camp

**[Decided]**

- **Setting:** the school lies in the **subtropics** and has a beach that is
  currently **closed**. A **PTA vote** opens it.
- **Timing:** possible any time of year in principle, limited to **spring–autumn**.
- **Length:** about **two weeks** on the normal calendar, enough time for the whole
  event set. Camp phases map onto the existing daytimes; no separate time scale.
- **Content:** sports, games, campfire, bikinis, wet bodies from swimming, and
  **tents with no sound insulation**. **Everyone hears everything**, so they
  influence each other and push each other up. That is level 4 in a nutshell:
  everyone *thinks* they're behind a closed door.
- **Who's there:** students, **teachers** (supervision) and the Headmaster.
- **Built as** a large set of plain events, not one composite. During the camp the
  rest of the campus is **closed on the map**; a **special beach map** with its own
  buttons for the camp activities.
- **Camp heat:** a camp-only value the player works towards, run as a
  **camp situation** ([§11](#11-engine-situation-pause--the-camp-situation)).
- **Afterwards** the beach stays as a **permanent location** (`buildings/beach.rpy`
  already exists).

### Parents

**[Decided]** Parents do **not** come on the camp: staff is enough supervision,
and Adelaide's and Nubia's absent daughters would make it weird. To bring the
parents to level 4 they come for **one campfire evening**:

- A thank-you evening for the PTA that opened the beach, so Adelaide and Nubia are
  there as PTA members, not as mothers.
- Parents and students talk; the mothers are **encouraged by the students** to
  open up. The usual direction flips.
- The PTA lemonade before level 3 was Orgazyme, so a drink dose isn't an option
  here.

**[Proposal]**

- Place the evening on the **second weekend**, when the heat is already high.
- The school is remote, so the mothers **stay overnight** in their own tent: the
  thin walls work on them too, and the campfire smoke (the inhale preparation)
  reaches them like everyone else.
- One very subtle hint, at most, that Adelaide's and Nubia's daughters aren't here
  for a reason. Never explain it.

**[Proposal]** The **first inhale preparation** debuts at the campfire, so the new
form is introduced with exactly the kind of group scene it is made for.

**[Proposal]** The camp may go far as a state of exception, but **back on campus it
is level 4**: private, behind doors. "What happened at the camp stays at the camp."
Otherwise the campus effectively jumps to level 5 and the hypnosis transition loses
its weight.

**[Open]** Yuki and Soyoon are both there on the parents' evening. Whether mother
and daughter get closer that night is handled by the kink filter
([§12](#12-engine-kink-menu)); the scenes still need writing both ways.

---

## 9. Engine: map registry

**Built.** The map registry is in place: `Map` / `map_manager` (`maps.rpy`), the
current map in `gameData["current_map"]`, `set_current_map(key)` to switch, and the
map screens read everything from the current map. The map image is shown under the
tag `map_image`. Full guide: **[Maps](Maps)**.

Still open for the beach camp:

- **[Proposal]** Ambience per map (today `map_overview` always plays forest/night).
- Restricting which events run on a special map → the event flags ([§10](#10-engine-event-flags)).
- The camp state must survive save/load: since only `current_map` is saved and
  `map_overview` reads it, a reload already lands back on the active map.

-------|------|
| `overview.rpy`, `map_overview` | `show school_map`, `call screen school_overview_buttons(True)`, forest/night ambience |
| `overview.rpy`, `school_overview_map` / `school_overview_images` | `add "school_map"` |
| `daily_check.rpy` (around lines 160, 172) | `scene school_map` |
| `event.rpy` (`begin_event`), `paperdoll.rpy` | `renpy.hide("school_map")` |
| `tutorial.rpy` | `add "school_map"` |

**[Proposal]**

- Show every map under **one fixed tag** (`show expression img as map_bg`), so the
  hide calls in `event.rpy` / `paperdoll.rpy` never have to change again.
- A registry entry: key, background, button screen, ambience per daytime,
  optionally the stats screen.
- Highlights and available events are `building_manager`-based today; a map
  needs its own source.
- The camp state must survive save/load: `after_load` lands back on the active map.

---

## 10. Engine: event flags

**✅ Built**, documented in [Events §5](Events#event-flags). A global flag
(`current_flag` in GameData) decides which events may run, for the camp first.
Empty by default, which means every event may run.

| Event has … | flag empty | flag = `camp` | flag = other key |
|---|---|---|---|
| no FlagCondition (auto `FlagCondition(None)`) | ✅ | ❌ | ❌ |
| `FlagCondition("camp", exclusive=False)` | ✅ | ✅ | ❌ |
| `FlagCondition("camp", exclusive=True)` | ❌ | ✅ | ❌ |
| `FlagCondition("x")` (wildcard) | ✅ | ✅ | ✅ |

How it was built:

- Like the old `IntroCondition`, **every event carries a `FlagCondition`**. Without
  one (searched recursively with `find_by_type`), `Event.__init__` appends
  `FlagCondition(None)`. The check runs through the normal condition check.
- **Fragments are exempt**; `EventSelect` and its options are not.
- The flag **replaces `IntroCondition`**: intro events use `FlagCondition("intro")`,
  `update_intro_flag()` sets and clears `"intro"` by date (start, `after_load`,
  `new_day`). `override_intro` was removed.
- Side effect, as intended: the shop delivery has no FlagCondition, so it waits during
  the camp and arrives on the first morning after it.

**[Decided]**

- Situation threshold/resolve scenes are called directly by `EventEffect` and bypass
  the flag **on purpose**. They are held back either by the situation pause (§11) or
  by conditions on the threshold/resolution itself.
- The wildcard is `"x"`, the same wildcard the codebase already uses elsewhere.

---

## 11. Engine: situation pause & the camp situation

**✅ Pause built** (independent of the flags for now), documented in
[Building Situations §2](Building-Situations#pausing-a-situation). A paused
situation **stays registered and `active`**, but:

- its bars, thresholds and resolutions freeze,
- its modifiers hibernate,
- measure durations, cooldowns, grace timers and the deadline stop (timers move
  forward by the paused time on resume),
- its situation pools close; game-data effects stay set,
- events already queued for `drain_situation_events` still run.

**[Decided]** Next step: tie the pause to the flags with the same table as
`FlagCondition`, so situations without a matching flag pause automatically while a
flag is set.

That allows a **camp situation** that only runs during the camp:

| Situation part | In the camp |
|----------------|-------------|
| **Bar** | the camp **heat** |
| **Wear** | quiet phases cool it down |
| **Thresholds** | unlock hotter events on the beach map |
| **Measures** | player actions that stoke it (game night, a dare, the inhale preparation) |
| **Pools** | inject the camp events into the beach map's storages |
| **Resolution** | the last night → **level 4** (registered as an event, `begin_event` / `end_event('none')`, see [Building Situations](Building-Situations)) |

---

## 12. Engine: kink menu

**[Decided]** A generic kink menu, built **before** the camp is written. Mods
register their own kinks; the list extends automatically.

**First use:** **Yuki & Soyoon** (mother / daughter) and **Luna & Seraphina
Clark** (sisters) can get closer in the game. All of them are adults, and in the
all-female world the biological concern doesn't arise. Players who don't want it
never see it.

### Three states

**[Decided]**

| State | Effect |
|-------|--------|
| **Want** | events and scenes are shown |
| **Block** | events and scenes are not shown |
| **Neutral** | the player is asked before the scene; the answer can set the state |

### The prompt screen

**[Decided]**

```text
┌──────────────────────────────────────────────┐
│  This scene contains:                        │
│                                              │
│      [ Show ]            [ Don't show ]      │
│                                              │
│  ☐ Don't ask again this session              │
│  ──────────────────────────────────────────  │
│  Incest (mother/daughter)   [ ✓ | ? | ✕ ]    │
│  Exhibitionism              [ ✓ | ? | ✕ ]    │
└──────────────────────────────────────────────┘
```

- Two buttons: **show** or **don't show**.
- A checkbox **"don't ask again this session"**.
- Below: a toggle for **every affected kink**, so the preference can be set right
  there, or left as it is. Several kinks are handled cleanly in one prompt.

**[Proposal]**

- **Buttons = this time, toggles = from now on.** Toggle on ✕ but *Show* → seen
  one last time. Toggle on ✓ but *Don't show* → skipped now, shown later. No
  combination is a contradiction.
- The session checkbox covers the kinks left on "?". "This session" means
  program start to program end: kept outside `persistent`, the save and rollback.
- The screen appears only if at least one kink of the scene is on "?" and not yet
  answered this session. Escape / right-click = *Don't show*.
- Neutral counts as **available** in availability checks; the prompt comes
  **after selection, before `begin_event`**. *Don't show* re-selects another event
  or fragment, so the action never leads nowhere.
- Tagging via an `Option` (Options already filter availability), so it works on
  fragments too.
- One shared **`kink_check(key)`** for whole events and in-label branches.
- **Story-critical events need a path without the kink** (in-label branch), so
  blocking never soft-locks progress.
- A **relationship registry** (`mother_of`, `sister_of`) so randomly rolled
  pairings are filtered too, not only hand-tagged events.
- **Mod kinks start on neutral**, so the player is asked on the first encounter
  and no mod can show something unasked.
- Gallery: blocked scenes hidden, neutral ones prompt; replays never change the
  setting. Preferences live in `persistent`.

---

## 13. Build order

What has to exist before what. Engine first, then content.

| # | Step | Needed for | Depends on |
|---|------|------------|------------|
| 1 | **Event flags + FlagCondition** ✅ built ([Events §5](Events#event-flags)) | camp, situation pause | — |
| 2 | **Situation pause** ✅ built ([Building Situations](Building-Situations#pausing-a-situation)); tie to flags still open | camp situation | 1 |
| 3 | **Map registry** ✅ built ([Maps](Maps)) | beach map | — |
| 4 | **Kink menu** (registry, states, prompt screen, `kink_check`) | camp content with Yuki/Soyoon, Luna/Seraphina | — |
| 5 | **"N available fragments" condition** | Type 1 flow | — |
| 6 | **Type 1 drink flow** (`Use potion` → select → composite → fragments) | level 3 gameplay | 5 |
| 7 | **Friend** (character, intro chain, epilogue pronouns) + **substitute research** | Type 1 resource, inhale, hypnosis compound | — |
| 8 | **Linh onboarding** (Orgazyme ~30 ml) | infirmary, targeted dosing | — |
| 9 | **Character picker** (generic) | targeted dosing, hypnosis, sandbox | 8 for the lore |
| 10 | **Beach vote + camp** (beach map, camp situation, event set, parents' evening, inhale debut) | level 4 | 1–4, 7 |
| 11 | **Science building vote + full lab** → **Type 2** | passive serum, mass-produced hypnosis compound | 7 |
| 12 | **Hypnosis** (compound, per-character chains, level 4 → 5) | level 5, early sandbox | 7, 11 |
| 13 | **Sandbox sex** | levels 4–6+ | 9, 12 |

Steps 1–5 are independent of each other and can be built in parallel.

---

## 14. Lore follow-ups

Changes [Lore](Lore) needs once these decisions are final:

- **§2** setting: **subtropical** climate and the (closed) **beach**.
- **§7** serum: **the serum doesn't change bodies** (note for modders: body-mod mods
  are welcome to add that). Hypnosis' *how and when* is no longer fully open: level
  4 → 5, its own compound, needs serum residue.
- **§6** cast: the **friend** as **[Planned]**.
- `daily_check.rpy`, `first_week_epilogue`: the friend's pronouns "him" / "He" →
  "her" / "She".

---

## 15. Open questions

| Question | Section |
|----------|---------|
| Who the friend had to hide from | [§6](#6-the-friend--the-biochemist) |
| Who the second Orgazyme newcomer (~40 ml) is | [§5](#5-orgazyme--the-last-70-ml) |
| How hypnosis carries the level 4 → 5 transition campus-wide (group session vs. key figures) | [§7](#7-hypnosis) |
| Order of the science-building vote vs. the beach camp | [§2](#2-story-timeline) |
| Exact camp event set and heat thresholds | [§8](#8-level-3--4-the-beach-camp) |
| Yuki & Soyoon on the parents' evening: which scenes, in which variants | [§8](#8-level-3--4-the-beach-camp), [§12](#12-engine-kink-menu) |
| Production slots and delivery channels for Type 2 | [§4](#4-potions--type-2-passive) |

### Related pages

- [Lore](Lore) · [School Levels](School-Levels) · [Building Situations](Building-Situations) ·
  [Building Unlockables](Building-Unlockables) · [Events](Events) · [Options](Options) ·
  [Modifiers](Modifiers) · [Items & Inventory](Items-and-Inventory) · [Characters](Characters)
