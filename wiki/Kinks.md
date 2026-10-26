> **Audience:** Developers and modders writing *Mind the School* content that not
> every player wants to see, and who need to gate it on the player's choice.
>
> **Scope:** The kink system (`kinks.rpy`): registering kinks, gating events and
> in-scene branches on them, how the event flow asks the player, replays and the
> gallery, and the family relations (`character.rpy`, `selector.rpy`) that pairings
> are built on.

---

## Quick start

```python
# 1) Register the kink with your mod (very early, like the mod itself).
init -97 python:
    register_mod("mymod_key", "My Mod", "1", "MyMod",
        description = "Adds a sisters scene.",
        kinks = [Kink("incest_sisters", "Sisters", "Scenes between two sisters.")],
    )

# 2) Gate the event on it.
init 1 python:
    set_current_mod('mymod_key')
    mymod_sisters = Event(3, "mymod_sisters", KinkCondition("incest_sisters"),
        Pattern("main", "images/mymod_sisters <step>.webp"))
    cafeteria_events["order_food"].add_event(mymod_sisters)
```

```renpy
# 3) Or branch inside any scene.
if kink_check("incest_sisters"):
    # the extra beat
```

The player never sees content with a kink they turned off. A kink they haven't decided
on yet is asked about right before the content starts.

---

## Contents

1. [What the player decides](#1-what-the-player-decides)
2. [Registering kinks](#2-registering-kinks)
3. [Gating content](#3-gating-content)
4. [How the event flow asks](#4-how-the-event-flow-asks)
5. [Composites and fragments](#5-composites-and-fragments)
6. [Replays and the gallery](#6-replays-and-the-gallery)
7. [Family relations](#7-family-relations)
8. [Conventions](#8-conventions)
9. [Reference](#9-reference)

---

## 1. What the player decides

Every kink has one **setting**, shared by all saves (`persistent.kink_settings`):

| Setting | Effect |
|---------|--------|
| `yes` | content with the kink runs |
| `no` | content with the kink never runs |
| `neutral` (default) | the player is asked right before such content starts |

The prompt (Emiko on the left, her question in the dialogue box, a card with the
kinks) offers four answers per kink:

| Button | Setting afterwards | This session |
|--------|-------------------|--------------|
| Yes | `yes` | allowed |
| No | `no` | not allowed |
| Yes, for now | stays `neutral` | allowed |
| No, for now | stays `neutral` | not allowed |

"For now" answers live in `renpy.session`: they are not saved, not rolled back, and
only cleared when the game is restarted. The player sets kinks in the journal's
**Settings** (section "Content preferences", all known kinks) and on the **mod page**
(section "Kinks", that mod's kinks, also while the mod is off). Changing a setting
there clears its "for now" answer.

A new kink — from a mod or an update — starts on `neutral`, so players are asked the
first time they meet it.

---

## 2. Registering kinks

```python
Kink(key, title, description = "")
```

- `key` — the identity. Compared case-insensitively (`"NTR"` == `"ntr"`).
- `title` — short name for buttons and lists.
- `description` — one or two neutral, non-explicit sentences (the settings page is
  visible to anyone looking over the player's shoulder).

Mods pass their kinks to `register_mod(..., kinks = [...])`. The base game lists its
own in `base_kinks` (`kinks.rpy`).

**Several sources, one kink.** Two mods (or a mod and the base game) registering the
same key share **one** kink with **one** setting. The title and description come from
the base game if it registers the key, otherwise from the first active mod in load
order. A different text for an existing key keeps the first one and logs a warning
(category `kinks`), so align your wording with the mod that was there first.

**Known kinks.** A kink counts as known while at least one source that registered it
is active. Content gated on a kink nobody active knows is **not allowed**.

---

## 3. Gating content

### `KinkCondition(*keys)`

```python
Event(3, "mymod_scene", KinkCondition("incest_sisters", "incest_mother_daughter"), ...)
```

- Fulfilled while **none** of the keys is disallowed: `yes`, `neutral` and a "yes, for
  now" all pass. So an event with an open kink still counts as available (menus and
  highlights show it); the player is asked when it is about to run (§4).
- Works on every event kind — `Event`, `EventComposite`, `EventFragment`,
  `EventSelect` — because conditions attach to all of them.
- Unlike other conditions it **also applies in replays** (§6).
- Never shown in journal requirement lists.
- Attach it at the top level of the event. Inside `OR(...)` it is still collected
  for the prompt, so the player may be asked about a kink the event wouldn't need.

### `kink_check(*keys) -> bool`

For a short branch inside a scene. It does two things, in this order:

1. **It opens the kink prompt** (the same screen as before an event: Emiko, her
   question, the four answers per kink) for every key that is still **open** —
   set to `neutral` and not answered "for now" this session. Keys that are open get
   asked together in one prompt. The scene waits there until the player has answered
   all of them; there is no way to cancel. Keys already set to `yes` / `no`, or
   answered "for now", don't trigger the prompt.
2. **It returns the result:** `True` only if every key is allowed after that,
   `False` as soon as one is not.

```renpy
if kink_check("incest_sisters"):
    # the extra beat
else:
    # the version without it
```

So the first time a player meets the branch with the kink on `neutral`, the scene
pauses for the prompt in the middle of the dialogue; afterwards (or with the kink
already decided) the check is silent. Write the line before the check so a prompt
there doesn't cut a sentence in half. If you need the answer twice in one scene, call
`kink_check` again — it won't ask a second time.

### `ask_kinks(*keys)` and the `kink_prompt` screen

`$ ask_kinks("incest_sisters")` is step 1 of `kink_check` on its own: it shows the
prompt for the open keys (nothing at all when none is open) and returns nothing — for
a scene that wants to settle its kinks up front and check them later with
`get_kink_state(key)` or `kink_check`. `call screen kink_prompt([keys])`
is the screen itself (Emiko, the question line and the card); it stores the answers
and returns them, but also asks about keys that are already decided.

All three must run in script (a `$` line or an `if` in a label), never in screen code.

---

## 4. How the event flow asks

`call_available_event` settles each event's kinks right before calling it:

1. The open kinks of the event (for a composite: of the composite and every fragment
   it could roll) are asked about in **one** prompt.
2. If the answers allow it, the event runs.
3. If not, the event is skipped. The rest of a priority-2 group still runs. When the
   whole pick was turned down — a single priority-1 or -3 event, or every event of a
   priority-2 group — the storage **picks again without the declined events**, falling
   through priority 1 → 2 → 3 like the first pick.
4. If nothing is left: a storage with its own fallback uses it (a building's entry
   storage, whose fallback is the action menu); otherwise the player returns to the
   menu they picked from, **without a daytime change** and without the default
   "There is nothing to do here." The event menu is rebuilt, so a choice whose events
   are now blocked disappears. `EventSelect` menus skip their exit (`override_menu_exit`)
   in this case.

`Event.call()` settles kinks too, so every other way of starting an event —
`EventEffect`, situation events, `call_event` — asks as well; a "no" there means the
event simply doesn't run.

---

## 5. Composites and fragments

- **Availability:** a composite is unavailable when kinks leave one of its fragment
  storages without a single event that would otherwise be available. Storages that
  are empty for other reasons keep the old behaviour (an error in the log when the
  composite runs). Composites without kinked fragments behave exactly as before.
- **One prompt before the start:** `EventComposite.get_kinks()` returns the composite's
  own kinks plus those of every fragment that could be rolled, so all of them are
  settled before the composite's label runs. Fragment selection then only skips
  disallowed fragments.
- **Fragments end through `end_event`.** A fragment label is entered via `call_event`,
  which returns to the *same* statement; a plain `return` re-runs the fragment forever.
  Always finish with `$ end_event(...)` — it hands over to the next fragment or ends the
  composite.

---

## 6. Replays and the gallery

- Replays read the **current** settings, never what was recorded with the gallery
  entry. Before a replay starts, open kinks are asked about; a blocked kink sends the
  player back to the scene's page.
- A replay counts the event's own kinks and, for a composite, those of the fragments
  picked for that replay (`get_replay_kinks`).
- **Gallery switch** "Turned-off content: marked / hidden"
  (`persistent.gallery_hide_blocked_kinks`, default *marked*):
  - *marked* — the scene stays listed; its page shows "Replay not available — it
    contains content you turned off: …" with the kinks comma-separated, and no replay
    button.
  - *hidden* — scenes with a blocked kink of their own disappear; so do composites
    with a fragment slot that has no seen fragment left without a blocked kink. Slots
    holding a blocked fragment move on to the first allowed one.

---

## 7. Family relations

Pairings that a kink is about (sisters, mother and daughter) are built on the family
relations of the people involved.

```python
Person("yuki_yamamoto", "Yuki", "Yamamoto", parent_char, [...],
    relations = {"mother_of": ["soyoon_yamamoto"]})
Person("soyoon_yamamoto", "Soyoon", "Yamamoto", school_char, [...],
    relations = {"daughter_of": ["yuki_yamamoto"]})
```

Relation types and their other side (`RELATION_INVERSES`): `mother_of` ↔ `daughter_of`,
`sister_of` ↔ `sister_of`, `grandmother_of` ↔ `granddaughter_of`, `aunt_of` ↔
`niece_of`, `cousin_of` ↔ `cousin_of`. Mods add types with
`register_relation_type(relation, inverse)` (symmetric: the same name twice).

| Function | Answers |
|----------|---------|
| `get_relations(person)` | relation → person keys, from both sides |
| `get_relation(person, other)` | what `person` is to `other`, or `None` |
| `are_related(person, other, relation = None)` | whether they are family (or exactly `relation`) |
| `get_related_persons(person, relation = None)` | keys of her relatives (or only those she is `relation` to) |

All take person keys or `Person` objects. A side that is missing is filled in from
`RELATION_INVERSES` (and an unknown type logs a warning, category `relations`).

A mod adds ties to people that already exist with
`add_person_relations(person, **relations)`, in its start loader (after the base
persons are loaded); nothing happens while the mod is off:

```python
label load_mymod:
    $ set_current_mod('mymod_key')
    $ add_person_relations("luna_clark", sister_of = ["seraphina_clark"])
    $ add_person_relations("seraphina_clark", sister_of = ["luna_clark"])
    return
```

`RelationSelector(key, of, relation = None, *options, alt = None)` rolls a relative of
another person — see [Selectors](Selectors):

```python
SelectorSet(
    RandomListSelector("girl", "luna_clark", "soyoon_yamamoto"),
    RelationSelector("relative", "girl"),        # Seraphina or Yuki
)
```

`relation` is what `of`'s person is to the one picked: `"sister_of"` picks her
sister, `"mother_of"` her daughter, `"daughter_of"` her mother.

---

## 8. Conventions

- **Never soft-lock progress.** Story-critical events, and every fragment storage of a
  story composite, need a path without the kink. Blocking a kink must never stop the
  story.
- **Neutral, non-explicit descriptions.** Kink titles and descriptions appear on the
  settings page and in the prompt.
- **Enter relations on both people.** The mirror is a safety net (a mod person related
  to a base one), not the way to write base content.
- **Reuse keys.** If another mod or the base game already has a kink for the same
  content, register the same key so players decide once.
- **Kink versions of base scenes from a mod** go through `replace_event` /
  `set_event_label` ([Modding](Modding#replacing-and-changing-base-events)). A replaced
  event that needs a kink no longer runs for players who turned it off, so add a
  version without it if the scene matters.
- **Fragments end with `end_event`**, never `return` (§5).

---

## 9. Reference

| API | Where |
|-----|-------|
| `Kink(key, title, description)` · `register_kinks(source_key, kinks)` · `register_mod(..., kinks=[...])` | `kinks.rpy`, `helper.rpy` |
| `get_kink(key)` · `get_known_kinks()` · `get_mod_kinks(mod_key)` | `kinks.rpy` |
| `get_kink_setting(key)` · `set_kink_setting(key, setting)` · `SetKinkSetting(key, setting)` (screen action) | `kinks.rpy` |
| `get_kink_session_answer(key)` · `set_kink_session_answer(key, allowed)` | `kinks.rpy` |
| `get_kink_state(key)` → `True` / `False` / `None` (open) · `get_open_kinks(keys)` | `kinks.rpy` |
| `KinkCondition(*keys)` | `conditions.rpy` |
| `kink_check(*keys)` · `ask_kinks(*keys)` · screen `kink_prompt(keys, show_host=True)` | `kinks.rpy` |
| `Event.get_kinks()` · `Event.kinks_allow()` · `settle_event_kinks(event)` | `event.rpy`, `kinks.rpy` |
| `get_available_events(..., exclude=())` | `event.rpy` |
| `get_replay_kinks(event, fragments)` · `get_blocked_kinks(keys)` · `get_kink_titles(keys)` | `kinks.rpy` |
| `Person(..., relations={...})` · `add_person_relations` · `get_relations` · `get_relation` · `are_related` · `get_related_persons` · `register_relation_type` | `character.rpy` |
| `RelationSelector(key, of, relation=None, *options, alt=None)` | `selector.rpy` |

### Related pages

- [Events](Events) — storages, priorities, composites and fragments
- [Conditions](Conditions) · [Selectors](Selectors)
- [Modding](Modding) — `register_mod`
