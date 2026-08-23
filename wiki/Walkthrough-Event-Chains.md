[Home](Home) › [Walkthroughs](Player-Walkthroughs) › Story chains

The scripted routes. Each section lists **when**, **where**, and **what happens**,
then the next trigger. Choices that change later scenes are called out.

<a id="first-week"></a>
## First week

The game opens on a short inspection of the campus. On **2–4 January 2023**,
walk into each building at least once. The first visit plays a one-shot intro
instead of the regular pool:

| Building | What you see |
|----------|----------------|
| Courtyard | Students hanging around; first impression of the yard |
| Gym | P.E. in progress |
| Kiosk | The snack bar the school currently lives on |
| Office | Emiko and the empty headmaster's desk |
| School building | Classes in session |
| Dormitory | Students in their rooms |

On the morning of **day 5** the **first PTA meeting** fires on its own. After
that, an **epilogue** at early noon wraps the week. You do not need to hunt
these — they are time-check events.

Until this week is over, many sandbox events stay locked behind the intro flag.

<a id="first-potion"></a>
## First potion

On **9 January** the leftover potion from the opening is still in the students'
systems. Visit the same buildings again (courtyard, gym, office, school,
dormitory). The scenes are more uninhibited than usual — underwear in the yard,
groggy classes, Emiko covering for you.

A second time-check later that day confirms you have seen the potion round. On
the morning of **day 10** a **final epilogue** closes the intro.

After this, memories of the potion week go fuzzy. That is the start of
**New Management**.

<a id="new-management"></a>
## New Management

This is a **Situation** (journal bar), not a numbered event chain. After the
potion week the campus is deciding whether you are actually the headmaster.
Teachers stay cautious, students test the rules, parents watch.

The bar **drifts down on its own** if you do nothing. Patrol, look around, hold
counselling, check classes, and work the office to push it up. Injected scenes
change as the bar moves — empty nameplate, Emiko on the private line, Aona
mistaking you for the janitor, Miwa's memory gaps, rumours at the kiosk, and
eventually a proper welcome.

Journal **Guided tips** (a passive) adds extra hints in some of those scenes.
Thresholds fire short reaction events on their own when the bar crosses them
(Emiko's pink slips, a district letter, a thaw from Yulan, Adelaide dropping
the word "new").

Stay out of the deep negative. A district letter at the bottom of the bar is
the game telling you the school is about to stop recognising you.

<a id="first-class"></a>
## First class with 3A

**When:** weekdays, class time.
**Where:** School building → **Teach Class**.

You introduce yourself, Finola Ryan introduces the class, and 3A introduce
themselves. This sets `first_class` to done. Several later chains — including
Aona's sports bra — will not start until this has played.

<a id="aonas-sports-bra"></a>
## Aona's sports bra

Aona cannot run P.E. comfortably. You take her into town for a sports bra.
That shopping trip is also the gate for the sex-ed chain.

### Prerequisites

- First class with 3A finished
- At least **$200** (not $500 — that figure was from the old wiki)
- School level 1–3 (P.E. teaching only exists in that range)

### 1. Running — Gym → Teach P.E. (weekdays, class time)

P.E. is a composite lesson (intro, entrance, warm-up, main, end). Keep teaching
until the **running** main fragment comes up. Aona complains that her chest
hurts; she has no sports bra and cannot afford one in her size. You offer to
write it off and take her to the city after school.

### 2. Bra shopping — evening, automatic

Once the running scene has finished, the shopping trip fires at **evening** on
its own (time-check, not a map click).

You wait while Aona picks, or you pick a bra yourself. If you pick, you can
ask her to try it, peek, wait, and — if inhibition is still high enough —
**swap** her choice for the skimpier one. Buying always costs **$200**.

The game remembers whether she left with a normal bra, a skimpy bra she agreed
to, or a skimpy bra you swapped in.

### 3. Changing-room gossip — next Teach P.E.

Miwa asks about the trip. The tone depends on the bra:

- **Normal bra** — they are happy; tiny inhibition drop
- **Skimpy, with permission** — Miwa thinks it looks good
- **Skimpy, swapped** — Aona tells Miwa the headmaster bought the wrong one;
  bigger inhibition drop, small happiness hit

### 4. Running, take two — Teach P.E. again

The class runs laps. If you swapped the bra, Aona calls you on it after class;
you can talk her into keeping it. The chain is done after this fragment.

<a id="first-time-naughty"></a>
## First time naughty

Not a named chain in the old wiki so much as a gate. Sex ed will not start
until **Emiko is at secretary level 6**. The story way to get there is this
scene.

**When:** weekdays, daytime.
**Where:** Office → **Work** → **Hold counselling sessions**.

1. Play the normal counselling scene at least **three** times (Yuriko, Elsie,
   or Easkey).
2. The next counselling pull can be **First time naughty**: Yuriko is waiting,
   then Emiko takes over. Inhibition and corruption swing hard; Emiko's level
   goes **5 → 6**.

After this, Office → **Call secretary** → **Naughty time** is a sandbox (desk /
floor variants, several outfits). It is optional. The chain only needed the
level-up.

The temporary **Level 3** journal unlock also sets Emiko to level 7, which
skips this gate. That is a debug-style shortcut, not the intended route.

<a id="sex-ed-introduction"></a>
## Sex ed introduction

You float theoretical sex education with Emiko, win over the teachers, present
to the PTA, vote it in, then teach the first class.

### Prerequisites

- Aona's shopping trip finished
- Emiko at secretary **level 6+**
- Sex-ed progress not already started

### 1. Ask Emiko — Office → Call secretary

**When:** **Monday**, daytime.

You float the idea. She likes it but wants the staff on board first, and
suggests preparing teaching material. A two-day timer starts.

### 2. How to approach the teachers — Office → Work

**When:** weekdays, daytime, **at least two days** after step 1.

You decide to sell it through their own subjects and ask Emiko to schedule a
staff meeting for the next morning (or Monday, if it is already late in the
week).

### 3. Teachers' opinions — automatic, morning, Mon–Thu

Finola, Chloe, Lily, Yulan, and Zoe hear the pitch. They are sceptical but you
get enough room to prepare a proper presentation.

### 4. Preparing the presentation — Office → Work (daytime)

You put the slides together. Next step unlocks **Schedule meeting**.

### 5. Presenting sex ed — Office → Schedule meeting

**When:** weekdays, **free time**.

You present to staff. Progress moves to the PTA discussion pool.

### 6. PTA discussion

At the next PTA, a dedicated discussion fragment plays. Parents (including
Yuki, Nubia, Adelaide) and student-rep Yuriko push back; you keep it theoretical
and careful. The rule **Theoretical Sex Education** is added to the journal.

### 7. PTA vote

Schedule the vote from the journal and win enough faction support. A dedicated
vote scene plays. If it passes, an assembly is queued.

### 8. Announcing sex ed — automatic, **Friday evening**

School assembly. The rule is public.

### 9. Weekend mini-events (any of these, high priority)

Until Monday morning, these replace the usual weekend pulls:

| Where | Who | What |
|-------|-----|------|
| Courtyard (any action) | students | Discussing the new material |
| Dormitory | Gloria Goto, Miwa Igarashi | Studying the pamphlet in a dorm room |
| Dormitory | Luna Clark, Seraphina Clark | Already modifying their uniforms |

### 10. First day after — automatic, **Monday morning**

Campus reaction. Small inhibition drop, happiness up.

### 11. First sex ed class — automatic, **Monday early noon**

Finola teaches 3A. Education up, inhibition down, corruption and happiness up.
The chain is done; **Teach Class → Sex Ed** becomes a regular composite lesson.

<a id="new-yoga-outfit"></a>
## New yoga outfit

Zoe adds yoga to P.E. The class needs outfits. You volunteer students, try
samples, bring in Linh for measurements, announce a "health checkup", then
hand out the new kit.

### Prerequisites

- School **level 2 or 3**
- 50% chance when the fragment is rolled — keep attending PTAs

### 1. Zoe's announcement — PTA discussion

Zoe tells the meeting she is adding yoga. Progress starts.

### 2. Checking yoga class — Gym → **Check P.E.** (weekdays, class time)

First look at 3A in yoga with Zoe. Charm and education up.

### 3. Checking again — same action

A second visit. Same stats. Starts a **4-day** timer.

### 4. Dressing volunteers — School building → **Check Classes**

**When:** weekdays, class time, **4 days** after step 3.

Luna, Elsie, and Hatano volunteer to try sample outfits. Inhibition dips.

### 5. Trying on outfits — Office, **evening**, weekdays

The volunteers try the samples in the office. Inhibition / corruption / charm.

### 6. Where to get the measurements? — Office (daytime)

You need proper sizing. Progress, then a **4-day** wait.

### 7. Zoe found someone — School building (daytime), 4 days later

Zoe has asked **Linh Nguyen** (the nurse) to help.

### 8. Announcing general health care — automatic, **Monday early noon**

You announce a "general health checkup" to 3A so the measurements look official.

### 9. Great health checkup day — automatic, **Tuesday noon**

Linh measures the class. Inhibition down, education up. Another **4-day** timer.

### 10. Distributing the outfits — Gym → **Check P.E.**, 4 days later

Zoe hands out the new yoga kit. Charm and education up, inhibition down.

After this, **Yoga Class** (Gym → Check P.E., school level 2+) becomes a
regular event.

<a id="truth-or-dare"></a>
## Truth or dare

A night-time glimpse of a topless student on the courtyard leads to a private
game in the dorms.

### Prerequisites

- School **level 2 or 3**
- Chain not already started

### 1. What do I spot there in the dark? — Courtyard → **Patrol**, **night**

You see a girl running without a top. Corruption up, inhibition down. The
chain starts.

### 2. When do the girls meet? — School building → **Patrol** (weekdays, class time)

Miwa Igarashi and Lin Kato talk about a recurring night-time get-together.
Happiness up.

### 3. Where do the girls meet? — same action, next time it pulls

Ikushi Ito and Lin Kato. The meeting place is the dorms. Happiness up.

### 4. Snooping on the girls — Dormitory → **Peek at Students**, weekdays **night**

A composite **truth or dare** with Ikushi, Lin, Miwa, and Ishimaru Maki. Two
to six random truth/dare fragments play, then an end card. Fragments are
level-gated (some only at 2–4 or 2–5, a few up to 10).

This is a peek, not a participation scene. After it finishes, the chain is
done.

<a id="lab-intro"></a>
## Lab intro

New relative to the old wiki. At school **level 2** you start rebuilding a
makeshift lab from scavenged gear. Later steps (full potion production) are
still incomplete in the code — steps 1–6 below are what currently fires.

**When:** weekdays, daytime, unless noted.

1. **Office → Work → Lab** — you decide to use the last notes and check the
   old lab building.
2. **Labs → Look around** — the building is wrecked; you need furniture and
   tools from around campus.
3. **Search** the campus (highlights while this step is active):

   | Location | Action | What you are looking for |
   |----------|--------|---------------------------|
   | Gym | Search | Mortar and pestle |
   | Cafeteria | Search | Mortar, distilled water |
   | Dormitory | Search | Mortar, distilled water |
   | Kiosk | Search | Glassware |
   | Courtyard | Patrol | Gas burner (if you do not have it yet) |
   | Courtyard | Search | leftover lab junk |
   | School building | Search | Office supplies |
   | Office | Search | Office supplies |

   Keep searching until you have **office supplies, glassware, gas burner,
   distilled water, mortar and pestle, utensils, chemicals, and furniture**.
4. **Office → Work → Lab** again — you set the makeshift lab up.
5. **Office → Lab → Research** — first look at recreating the base potion.
6. Further produce/research beats exist; some later labels are still commented
   out. Treat anything after the first test potion as WIP.
