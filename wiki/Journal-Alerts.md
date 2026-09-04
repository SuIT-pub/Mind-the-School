> **Audience:** Developers adding journal attention (the map highlight, later
> bookmark pips, per-row markers) when something new appears in the journal.
>
> **Scope:** The journal alert registry (`journal_alerts.rpy`). It is **not** the
> map's building-event highlight (`ForceHighlight` / `get_available_highlight`).
> Situations and Unlockables already raise alerts; other journal surfaces plug in
> through the same topics.

---

## Quick start

Raise a flag when something the player has not seen yet appears. The map journal
button swaps to `icons/journal_icon_highlight.webp` until they open that row.

```python
# something new on the Situations page, for this situation key
$ raise_journal_alert("situations", "cafeteria_crisis")

# later, from any other system:
$ raise_journal_alert("gallery", event_key)
```

Clearing is automatic: `label open_journal` calls `acknowledge_journal_alerts(page, display)`.
Opening the cafeteria situation (`open_journal(8, "cafeteria_crisis")`) drops that
item. Opening the journal overview (page 1) does **not**.

Check from screens:

```python
if journal_has_alert():
    # map icon is already swapped by get_journal_map_icon()
if journal_has_alert("situations"):
    # e.g. a pip on the Situations bookmark
if journal_has_alert("situations", "cafeteria_crisis"):
    # e.g. a marker on that list row
```

---

## Contents

1. [What an alert is](#1-what-an-alert-is)
2. [Topics vs. items](#2-topics-vs-items)
3. [When flags raise and clear](#3-when-flags-raise-and-clear)
4. [Registering a new topic](#4-registering-a-new-topic)
5. [Built-in sources](#5-built-in-sources)
6. [Map icon](#6-map-icon)
7. [API](#7-api)
8. [Conventions](#8-conventions)

---

## 1. What an alert is

A **journal alert** is a pending reminder that a journal surface has something
new. It is stored on `journal_alert_manager` (save-backed) as:

```text
topic key  →  list of item ids
```

Topics themselves (`situations`, `unlockables`, …) are registered at init and
are **not** saved. Pending item ids **are** saved.

The map button is a single OR across every topic: if any list is non-empty, the
highlight icon shows. Later UI (bookmarks, list rows) can OR a smaller slice via
`journal_has_alert(topic)` / `journal_has_alert(topic, item)`.

---

## 2. Topics vs. items

| Piece | Role | Example |
|-------|------|---------|
| **Topic** | One journal surface | `"situations"` → page 8 |
| **Item** | One row on that surface | `"cafeteria_crisis"` |
| **Topic-level ping** | Item id `""` | “something happened on this page” with no row |

Named items stay pending until **that row** is opened. A topic-level `""` ping
clears when the player opens that topic's primary page (even with an empty
display), and also when they open any specific item on that topic.

Opening a list without selecting a row does **not** clear named items. The player
has to open the new situation / unlockable / future row.

---

## 3. When flags raise and clear

**Raise** by calling `raise_journal_alert(topic, item)` from gameplay code.
Re-raising the same topic+item is a no-op (the id is already in the list).

**Clear** happens in `label open_journal` via `acknowledge_journal_alerts(page, display)`:

- Primary page + empty display → drop the topic-level `""` ping. If the topic
  was registered with `clear_on_page=True`, drop the whole topic.
- Primary page + a display value → drop that item (after `extract_item`) and `""`.
- `extra_item_pages` + a display value → same item clear (so an Unlockable opened
  from the Situations page still counts as seen).

Manual clear: `clear_journal_alert(topic, item)` or `clear_journal_alert(topic)`
for the whole topic.

---

## 4. Registering a new topic

Register at init, next to the built-in topics in `journal_alerts.rpy` (or from a
mod `init python` block):

```python
register_journal_alert_topic(
    "gallery",
    page=7,
    extract_item=None,          # display string is the item id
    extra_item_pages=(),        # other pages that can open this row
    clear_on_page=False,        # empty page 7 does not wipe named items
)
```

Then raise from the system that produces the news:

```python
raise_journal_alert("gallery", event_key)
```

`extract_item` maps the `open_journal` `display` string onto the item id you
raised. Situations use `parse_situation_journal_display` so
`"cafeteria_crisis:notes"` still matches `"cafeteria_crisis"`.

Override `Situation.get_journal_alert_topic()` (Unlockable already does) if a
subclass should ping a different topic than `"situations"`.

---

## 5. Built-in sources

These call `notify_situation_journal_alert(situation)` which reads
`situation.get_journal_alert_topic()`:

| Event | Topic | Item |
|-------|-------|------|
| A Chronicle teaser unlocks | `situations` or `unlockables` | situation key |
| `Situation.activate()` (first time) | same | situation key |
| `Situation.complete()` (first time) | same | situation key |

`Unlockable` returns topic `"unlockables"` (journal page 4, with page 8 as an
extra item page). Plain Situations return `"situations"` (page 8). Cancel does
**not** raise. Reload / `update_data` does **not** re-raise — only live
transitions.

---

## 6. Map icon

`school_overview_stats` uses `get_journal_map_icon()`:

| State | Image (`game/images/icons/`) |
|-------|------------------------------|
| No pending alerts | `journal_icon_idle.webp` |
| Any pending alert | `journal_icon_highlight.webp` |

Hover is still the surrounding button, not a separate highlight asset. The
tutorial mockup (`journal_idle`) does not go through this helper.

This is independent of building-event highlights on the map.

---

## 7. API

| Call | What it does |
|------|----------------|
| `register_journal_alert_topic(key, page, extra_item_pages=(), extract_item=None, clear_on_page=False)` | Declare a surface. Init only. |
| `raise_journal_alert(topic, item="")` | Mark unseen. |
| `clear_journal_alert(topic, item=None)` | Drop one item, or the whole topic if `item` is None. |
| `journal_has_alert(topic=None, item=None)` | Query. Any / one topic / one item. |
| `get_journal_map_icon()` | Idle or highlight path for the map button. |
| `notify_situation_journal_alert(situation)` | Raise using `get_journal_alert_topic()`. |
| `acknowledge_journal_alerts(page, display="")` | Called from `open_journal`. |

Store object: `default journal_alert_manager = JournalAlertManager()`.

---

## 8. Conventions

- Raise from the **transition**, not from the template definition, and not from
  `update_data` / after-load sync.
- Item ids should be the same strings `open_journal` uses as `display` (or what
  `extract_item` peels out of it).
- Do not stuff unrelated news into `"situations"` — register a topic.
- Map highlight is the coarse OR. Prefer `journal_has_alert(topic, item)` for
  finer UI so one unseen teaser does not paint every bookmark.

**Related files:**

- `game/scripts/journal/journal_alerts.rpy` — registry, manager, helpers
- `game/scripts/journal/journal.rpy` — `open_journal` acknowledges
- `game/scripts/overview.rpy` — map icon
- `game/scripts/situations/situations.rpy` — teaser / activate / complete
- `game/scripts/journal/unlockables.rpy` — topic override
