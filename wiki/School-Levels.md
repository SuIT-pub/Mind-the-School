[Home](Home) › School Levels

> **Audience:** Anyone writing or drawing *Mind the School* content — event authors,
> paperdoll/outfit work, and players who want to know what a school level *feels*
> like. This page is the climate bible: dress, talk, and behaviour at each step
> from modest campus to sexual anarchy.
>
> **Scope:** The **school** character's level (`"school"`, 0–10) — the student-body
> / campus climate. Teacher, parent, and secretary have their own numeric levels;
> those tracks are noted below, but the named stages here describe **students**.
> Mechanical gating lives in [Conditions](Conditions) (`LevelCondition`); image
> tokens in [Images](Images); paperdoll `level=` in [Paperdoll](Paperdoll). How
> players currently *raise* the number is in
> [Walkthrough — Unlocks](Walkthrough-Unlocks#school-levels).

---

## Contents

1. [What a school level is](#1-what-a-school-level-is)
2. [Other level tracks](#2-other-level-tracks)
3. [How the number moves today](#3-how-the-number-moves-today)
4. [At a glance](#4-at-a-glance)
5. [The ten levels](#5-the-ten-levels)
6. [Writing and art](#6-writing-and-art)

---

## 1. What a school level is

The school is a `Char` keyed `"school"`. Its level is the campus climate: how
students dress, how they talk about sex, and what they will do in public versus
behind a door. `set_level` clamps the value to **0–10**.

In content:

| Use | How |
|-----|-----|
| Gate an event / fragment / unlockable | `LevelCondition("2")`, `"2+"`, `"1-3"`, `"4-"` — default `char_obj` is school; pass `char_obj="school"` when you want it explicit |
| Roll the number into kwargs / image paths | `LevelSelector("school_level", "school")` then `<school_level>` in the [Pattern](Images) |
| Read it in a scene label | `get_level("school_level", **kwargs)` (replay-safe) or `get_character_by_key("school").get_level()` |
| Change it | `LevelEffect("…", value, "SET"/"ADD", "school")` — or `school.set_level(n)` in a story label |
| Paperdoll / outfit cards | `PDAImage(outfit="uniform", level=N)` — student `N` should match school level. Character pages label the same scale as **Level 00–10** |

`<school_level>` in a path is filled from the school character, even if you never
declared a selector. Event stills, building backgrounds, and PTA art all key off it.

This page is **tone**, not a second rules engine. Stats (corruption, inhibition,
charm, …) still move independently. A high-corruption campus at level 1 is a
writing bug; a level-7 scene that talks like level 2 is the same bug the other way.

---

## 2. Other level tracks

Four characters carry a `level` stat. Only **school** is this bible.

| Key | What the number means | Typical relationship to school |
|-----|------------------------|--------------------------------|
| `school` | Student body / campus climate — **this page** | Canonical 1–10 named stages |
| `teacher` | Staff climate and teacher outfit/paperdoll level | Temporary level votes SET this to the same number as school |
| `parent` | Parent climate and parent outfit/paperdoll level | Same SET as school on those votes |
| `secretary` | [Emiko](Emiko-Langley)'s personal track | Starts at **5** on repaired saves; temporary votes jump her *ahead* of school (7 at school 3, then +1 per step) |

Individual students in Class 3A do **not** each store a level. Their uniform
cards and paperdoll `level=` follow the **school** number. A named girl can be
shy or bold *inside* that climate; she does not get her own 1–10 unlock.

**Level 0** is legal in the engine and shows up on outfit galleries as
**Level 00** (the most conservative card). Playable climate starts at **1**.
Treat 0 as uninitialized / pre-game, not a named stage.

Building levels (`BuildingLevelCondition`, `BuildingLevelSelector`) are a
different number — cafeteria construction, etc. Do not mix them with school
level.

---

## 3. How the number moves today

- New or repaired saves: if school (or parent / teacher) is 0, it is set to **1**.
  Secretary 0 becomes **5**.
- The **[sex-ed introduction](Walkthrough-Event-Chains#sex-ed-introduction)** sets
  school to **2**.
- **Levels 3–10** are a temporary journal Unlockable group (`"level"`). Each won
  vote **SET**s school, parent, and teacher to that step and bumps secretary. The
  journal warns you to **back up the save**. Not every event has art or variants
  at high levels. This will be replaced by real transition events.

See [Walkthrough — Unlocks](Walkthrough-Unlocks#school-levels) for the player
route. Cheat Menu → Stats can force the four tracks; that skips the vote and
desyncs easily.

---

## 4. At a glance

| Level | Name | Dress (public) | Talk | Sex |
|------:|------|----------------|------|-----|
| 1 | Pure and Innocent | Long skirts, covered shoulders, no cleavage or midriff | Sex is avoided or whispered behind a door | Physical boundaries, especially with males; masturbation / anal are foreign |
| 2 | Innocence Fading | Shorter skirts, lower-cut tops that *hint* at cleavage | Giggles, naive whispers, still a public veneer | Private curiosity; teasing among girls out of sight |
| 3 | Sexual Awareness | Skimpy sleepwear, more leg, midriffs at home | Own desires, still not graphic | Light groping under clothes at sleepovers / parties |
| 4 | Experimentation | Lingerie / revealing clothes at home; public still "normal" | Frank: technique, partners | Full nudity and oral under the covers; private only |
| 5 | Promiscuity | Cleavage, midriff, thighs on campus | Graphic, unfiltered (anal, threesomes, fetishes) | PDA: holding hands, kissing; sex is no longer a secret |
| 6 | Sexual Obsession | Barely-there clothing | Sex dominates school, social, family talk | New partners, group sex, fetish play as a lifestyle |
| 7 | Addiction | Little-to-no clothing in public | Everything is sex; schoolwork and relationships suffer | Rough / public / risk-seeking; thrill over consequence |
| 8 | Sexual Utopia | Nudity as the default, including when not having sex | No morality talk — only new ways to get off | Constant activity, orgies, public displays |
| 9 | Extreme Obsession | Same as 8; clothes are optional costume | Darker kinks, no regard for cost | BDSM, incest, bestiality; relationships are transactional |
| 10 | Sexual Anarchy | Nudity = identity; clothes have lost meaning | Primal; little language left | Anything, including acts that blur human / non-human |

Levels **2–4** keep a **public veneer**. The jump at **5** is the campus going
open. **8+** is a different game: nudity and public sex are the setting, not a
scene beat.

---

## 5. The ten levels

### Level 1 — Pure and Innocent

Students embody purity and modesty. Anything sexual or explicit makes them
deeply uncomfortable.

- **Dress:** Conservative. Long skirts, blouses that cover the shoulders, no
  cleavage, no midriffs.
- **Talk:** Sex is avoided, or handled tactfully behind a closed door.
- **Behaviour:** Strict boundaries around physical contact, especially with males.
  Topics like masturbation or anal play would be utterly foreign.
- **Write:** Blushes, subject-changes, "I don't want to talk about that." No
  knowing jokes. PE and changing-room scenes are about embarrassment, not heat.

### Level 2 — Innocence Fading

The discomfort is thinning. Curiosity happens in private; the public face is
still innocent.

- **Dress:** Shorter skirts, lower-cut tops that hint at cleavage without showing
  it.
- **Talk:** Whispered, often with giggles, still naive.
- **Behaviour:** Subtle flirting or teasing among themselves when nobody else is
  looking.
- **Write:** "Did you hear…?" energy. They do not have the vocabulary yet. Public
  scenes still punish overtness (reputation, teacher scolding). This is the
  first school level where a lot of story content unlocks (yoga outfits, truth
  or dare, lab intro).

### Level 3 — Sexual Awareness

They have the basics. Experimentation is small and still wrapped in propriety.

- **Dress:** Skimpy pajamas, midriffs, more leg — at home / sleepovers, not as a
  new uniform.
- **Talk:** Less guarded. They might name their own budding desires, still without
  explicit detail.
- **Behaviour:** Limited contact at sleepovers or parties: light groping under
  clothing.
- **Write:** First-time nerves, "is this allowed?", hands under a shirt, not
  under a skirt on the quad. Public dress is still a school, not a club.

### Level 4 — Experimentation

They are hunting new experiences in private and keeping an outward show of
normalcy.

- **Dress:** Lingerie or revealing clothes *for each other* at home. Campus
  uniform is provocatively interpreted but not abandoned.
- **Talk:** Frank. Masturbation technique, partner preferences.
- **Behaviour:** Full nudity and oral sex under the covers at sleepovers / parties.
- **Write:** The door is closed; the hallway is still "a school." Afterglow
  awkwardness, not public claiming. Last level where "don't get caught" is the
  default tension.

### Level 5 — Promiscuity

Sexuality is embraced. Social norms and repercussions barely slow them down.

- **Dress:** Revealing on campus: significant cleavage, midriffs, thighs.
- **Talk:** Graphic and unfiltered — anal play, threesomes, fetishes.
- **Behaviour:** Regular PDA (holding hands, kissing). Sex is a known fact of
  student life, not a rumour.
- **Write:** Teachers and parents are dealing with an open culture, not isolated
  incidents. Couples events stop being scandals. This is the public/private
  hinge — do not write level-4 secrecy here unless someone is specifically
  hiding from a *named* person.

### Level 6 — Sexual Obsession

Unrestrained lust. Lives organise around the next encounter, with little regard
for other people or consequences.

- **Dress:** Extremely revealing; essential parts barely covered.
- **Talk:** Sex dominates school, social events, and family conversation.
- **Behaviour:** New partners constantly, group sex, fetish experiments as
  routine.
- **Write:** Class time competes with hookups. A scene that never mentions sex
  should feel like an exception you chose on purpose.

### Level 7 — Addiction

The thrill and the release outrank everything else.

- **Dress:** Little-to-no clothing even in public.
- **Talk:** Sex consumes the day; schoolwork and relationships suffer out loud.
- **Behaviour:** Risky or dangerous acts for the high — rough sex, public sex,
  drugs during encounters.
- **Write:** Consequences exist and they do not care. A girl missing class
  because she is in a supply closet is climate, not a special event. Keep
  character *voice*; do not flatten everyone into the same addict.

### Level 8 — Sexual Utopia

Sexuality is the environment. No judgement, no outside consequences that
anyone respects.

- **Dress:** Clothing is gone. Nudity is the norm even when they are not having
  sex.
- **Talk:** Only new ways to satiate cravings. Morality / ethics talk is dead.
- **Behaviour:** Constant activity, group orgies, public displays as the
  background of the map.
- **Write:** A "fully clothed student in the hallway" needs a reason. Backgrounds
  keyed on `<school_level>` should look like this, not like a slightly dirtier
  level 5.

### Level 9 — Extreme Obsession

The fixation will pay any cost. Darker acts are on the table.

- **Dress:** Same as 8; clothes, when they appear, are costume or a scene prop.
- **Talk:** New boundaries, darker kinks, no regard for what it costs.
- **Behaviour:** Violent or disturbing sex — BDSM, incest, bestiality.
  Relationships are transactional: access to a body.
- **Write:** Consent-as-climate is gone; power and appetite run the scene. Named
  characters can still refuse *a specific person* — they do not refuse the
  culture. Do not pull punches if the event is gated 9+.

### Level 10 — Sexual Anarchy

No remaining social norm. Hedonism is the only motor.

- **Dress:** Nudity is identity. Clothes have lost meaning.
- **Talk:** Language thins toward grunts and moans; immediate desire only.
- **Behaviour:** Every imaginable act, including ones that blur human and
  non-human.
- **Write:** This is the end state. Scenes can be almost wordless. If you need
  long articulate dialogue, you are probably still at 8–9.

---

## 6. Writing and art

**Match three things:** the `LevelCondition` (who can see the event), the
`<school_level>` still (what they are wearing), and the dialogue (how they sound).
A level-1 gate with a level-6 still is a bug. A paperdoll `level=1` uniform in a
level-8 hallway is the same bug.

**Public vs private.** Levels 2–4: the interesting sex happens off the quad.
Level 5+ : the quad is fair game. If an event is available across a wide range
(`"2-10"`), branch the text and the images; do not write one scene and hope the
stills carry the difference.

**Named characters.** Personality survives the climate. Aona at 5 is still
Aona, dressed and talking like a level-5 campus. Read the
[character page](Characters) first, then apply this page on top.

**Outfits.** Character wiki galleries are the visual spec: **Level 00** through
**Level 10**. When you add a new uniform or casual set, the step from N to N+1
should be readable as the row in [§4](#4-at-a-glance) — shorter, more skin, then
less clothing, then none.

**Wide gates.** If art does not exist for high levels, say so in the event
(missing `<school_level>` files fall through `$` / nearest `<level>` — see
[Images](Images)). The temporary 3–10 unlocks already warn that not every event has
variants. Do not ship a 10-capable gate with only level-2 frames unless the
resolver has a real fallback.

**Conditions cheat-sheet**

```python
LevelCondition("1")                 # exactly 1
LevelCondition("2+")                # 2 and up
LevelCondition("1-3")               # 1, 2, or 3
LevelCondition("5-", char_obj="school")
LevelSelector("school_level", "school")
LevelEffect("set_school_level_4", 4, "SET", "school")
```

---

### Related files

- `game/scripts/character.rpy` — `Char.get_level` / `set_level` (clamp 0–10)
- `game/scripts/journal/unlockables.rpy` — temporary `"level"` group (3–10)
- `game/scripts/events/sex_ed_intro.rpy` — story set to school level 2
- `game/script.rpy` — save repair: 0 → 1 (secretary 0 → 5)
- [Events](Events) · [Conditions](Conditions) · [Selectors](Selectors) ·
  [Effects](Effects) · [Images](Images) · [Paperdoll](Paperdoll) ·
  [Characters](Characters) · [Walkthrough — Unlocks](Walkthrough-Unlocks#school-levels)
