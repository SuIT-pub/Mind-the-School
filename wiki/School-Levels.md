[Home](Home) › School Levels

> **Audience:** Anyone writing or drawing *Mind the School* content — event authors,
> paperdoll/outfit work, and players who want to know what a school level *feels*
> like. This page is the climate bible: dress, talk, and behaviour at each step
> from modest campus to joyful sexual paradise.
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
| 6 | Open Culture | Revealing, playful outfits everyday | Sex is ordinary, cheerful table-talk alongside class and gossip | Casual hookups in the open; nobody hides, everybody's welcome |
| 7 | Woven In | Barely-there sexy outfits the norm | Warm and easy — "want to?" gets a smile, then back to work | Sex threads through the day; approach anyone, and life still runs |
| 8 | Sexual Utopia | Barely-there fashion; nudity normal and freely chosen | Affectionate, articulate; pleasure and work in the same breath | Ambient public sex; easy abundance, everyone glad |
| 9 | Boundless Bliss | Sexier still; clothing is pure play | Loving, generous, still fully themselves | Endless shared pleasure; the community gives freely, joyfully |
| 10 | Sexual Paradise | Whatever feels sexiest — barely-there or bare, by choice | Perfectly articulate and loving; sex is woven into every topic | Sex, love and productive life are one seamless whole |

Levels **2–4** keep a **public veneer**. The jump at **5** is the campus going
open. **6–10** climb from open to fully woven-in: sex becomes ambient daily
texture — barely-there fashion and public play are the setting the scenes sit in
— while people stay warm, articulate, and **productive**. The top is a joyful
paradise where daily life and open sexuality flourish together.

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

### Level 6 — Open Culture

Sex is a welcome, ordinary part of campus life. Nobody hides it and nobody
polices it — but the school still runs, and everyone is glad it does.

- **Dress:** Revealing, playful outfits as everyday wear — sheer panels, high
  cuts, deliberately sexy rather than shocking.
- **Talk:** Sex is cheerful table-talk, folded in beside homework, gossip, and
  weekend plans. Casual, not clinical.
- **Behaviour:** Hookups happen in the open between classes; couples and groups
  form and drift apart easily. Everybody's welcome, and it's always a free yes.
- **Write:** Girls still go to class, still do the work — they just also flirt
  and fool around on the way. It's joyful and consensual, everyone in on it by
  choice. Let sex be one thread in the day; plenty of scenes can stay about
  class, friendship, or gossip.

### Level 7 — Woven In

Sex is fully threaded into the daily rhythm. You can walk up to anyone, say the
word, and get a warm yes — then both of you go back to what you were doing.

- **Dress:** Barely-there sexy outfits are the norm — the good stuff on show,
  covered just enough to keep it a look rather than nothing at all.
- **Talk:** Easy and affectionate. "Want to?" gets a smile, not a scandal, and
  afterward the conversation picks right back up — work, friends, the day.
- **Behaviour:** Encounters happen mid-day, between tasks, in the open, and then
  everyone carries on. All friends, all lovers, all still themselves.
- **Write:** The load-bearing idea: **life still runs**. The school functions,
  the work gets done, people stay warm and articulate — sex is easy background
  texture that everyone steps out of and gets on with the day. Each character
  keeps her own *voice* and her own place in the school.

### Level 8 — Sexual Utopia

Sexuality is the environment, and it's a happy one. No shame, no friction — just
abundance, affection, and a campus that still works because everyone wants it to.

- **Dress:** Barely-there fashion is the everyday look; nudity is completely
  normal and always a free choice. Clothing stays a playful, deliberately sexy
  pick.
- **Talk:** Warm, articulate, generous — pleasure and schoolwork in the same
  breath. People talk about sex the way they talk about lunch, and they talk
  about everything else with the same ease.
- **Behaviour:** Public sex is ambient — pairs and groups, out in the open, glad
  and unhurried — while classes, jobs, and friendships carry on around it.
- **Write:** A hallway still full of purpose *and* full of sex. Backgrounds keyed
  on `<school_level>` should read as barely-dressed, cheerful, and alive — bodies
  at ease, everyone glad to be there.

### Level 9 — Boundless Bliss

Pleasure has no ceiling and the whole community shares it. Generosity is total:
there is always more affection, more joy, more yes to give.

- **Dress:** Sexier still, and pure play — barely-there or bare, whatever feels
  best that day. Nobody's counting.
- **Talk:** Loving and open, still perfectly articulate. People are entirely
  themselves; the warmth is the point.
- **Behaviour:** Endless, freely shared pleasure — big, easy, communal — given
  and received with delight, always freely chosen. Everyone with everyone, all of
  it wanted.
- **Write:** This is abundance and ecstasy — the intensity lives in how much joy
  and affection there is to share. A named character can still say "not right
  now" to a *specific person*; it's a preference in the moment, and the warmth
  around her holds.

### Level 10 — Sexual Paradise

The completed paradise. Sex, love, and productive everyday life are one seamless
whole — and everything flourishes together.

- **Dress:** Whatever feels sexiest — barely-there or bare, always by free
  choice. Fashion is delight, never a rule in either direction.
- **Talk:** Perfectly articulate and loving. Sex is woven naturally into every
  topic — work, art, friendship — without ever crowding the rest out.
- **Behaviour:** Everyone loves everyone; everyone is desired and fulfilled. And
  the world still turns — school, craft, and community thrive right alongside the
  constant, joyful sex.
- **Write:** The end state is a functioning utopia: people are their fullest,
  warmest, most articulate selves *and* endlessly sexual. Write the joy at full
  volume — abundant, loving, alive — everyone fulfilled and the world thriving
  around them.

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

**Joy and function (levels 6–10).** The high end is a *paradise*. Sex is woven
into ordinary life, and life keeps happening: people study, work, make art, and
hold real conversations, with the sexy stuff running alongside — welcomed,
consensual, and easy to step into or out of. Keep everyone warm and articulate;
the higher the level, the more affection, generosity, and ease there is to write.

**Outfits.** Character wiki galleries are the visual spec: **Level 00** through
**Level 10**. When you add a new uniform or casual set, the step from N to N+1
should be readable as the row in [§4](#4-at-a-glance) — shorter, more skin, then
barely-there sexy fashion. Nudity is normal at the top, and the clothing that
*does* appear stays a deliberate, playful, sexy choice.

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
