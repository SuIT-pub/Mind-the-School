> **Audience:** Developers who add items, hand them out from events, gate content on
> owning something, or sell things in the office-computer shop.
>
> **Scope:** The item system in `inventory.rpy`: item definitions (`ItemData` /
> `ShopItemData`), the save-backed `inventory_manager`, the shop → cart → delivery
> flow, the two item conditions, and the journal inventory page. Potions as a
> *gameplay driver* are lore, see [Lore](Lore); this page covers only the container
> they will live in.

---

## Quick start

Define the item once in a loader, then give, check and take it from events:

```python
# 1. define (inside label load_items, or your mod's loader)
$ load_item(ItemData(
    "lab_glassware",                     # key: stable, saved, never rename
    "Glassware",                         # display name
    [                                    # description: str or list of lines
        "Glassware that can be used to store liquids.",
        "",
        "Quest item: Headmaster's Lab Intro",
    ],
    "images/items/glassware.webp",       # icon (mod-prefixed, png/webp fallback)
))

# 2. give (inside an event)
$ inventory_manager.add_item("lab_glassware")            # +1, shows a notify toast
$ inventory_manager.add_item(Item("lab_glassware", 3))   # +3

# 3. gate on it
Event(2, "lab_intro_6", ItemCondition("lab_glassware"))
Event(2, "lab_intro_x", NOT(ItemCondition("lab_glassware")))

# 4. take it away
$ inventory_manager.remove_item("lab_chemicals", 1)      # -1
$ inventory_manager.remove_item("lab_chemicals")         # remove the whole stack
```

---

## Contents

1. [Two layers: definition vs. stack](#1-two-layers-definition-vs-stack)
2. [Defining items](#2-defining-items)
3. [Giving, checking, taking](#3-giving-checking-taking)
4. [Conditions](#4-conditions)
5. [The shop and deliveries](#5-the-shop-and-deliveries)
6. [The journal inventory page](#6-the-journal-inventory-page)
7. [Saves, reloads and mods](#7-saves-reloads-and-mods)
8. [Known gaps](#8-known-gaps)
9. [API](#9-api)
10. [Conventions](#10-conventions)

---

## 1. Two layers: definition vs. stack

| Layer | Class | Lives in | Saved? | Holds |
|-------|-------|----------|--------|-------|
| **Definition** | `ItemData` / `ShopItemData` | `inventory_manager.item_data` (+ `shop_item_data`) | rebuilt on every start / load | name, description, image, (price, limits) |
| **Stack** | `Item` | `inventory_manager.inventory` | **yes** | `key` + `amount` only |

An `Item` is just *"N of key X"*. Everything the player reads (name, text, icon) is
looked up from the definition by key at display time (`item.data()`,
`item.get_name()`, …). So you can rewrite an item's name, description or icon in
`load_items` and old saves pick the change up on the next load.

The **key** is the contract. It is what the save stores, what `ItemCondition`
checks and what the shop cart and delivery queue reference. Don't rename a
shipped key.

---

## 2. Defining items

Items are registered in `label load_items` (`inventory.rpy`), which runs in the
start / after-load wave (`script.rpy`). Each definition goes through `load_item(...)`.

### `ItemData(key, name, description, image)`

| Arg | Type | Notes |
|-----|------|-------|
| `key` | `str` | unique id, snake_case, prefixed by feature (`lab_…`) |
| `name` | `str` | shown in the journal, shop, notify toast |
| `description` | `str` or `list[str]` | a list renders one `text` per line; `""` gives a blank line |
| `image` | `str` | path relative to the mod root (`images/items/…`); see below |

**Image resolution.** The path is prefixed with the active mod's folder at
construction (`get_mod_path(active_mod_key) + image`). `get_image()` runs it
through `find_loadable_image`, so `.png` ↔ `.webp` both resolve. If nothing
loads, the item falls back to `images/journal/empty_image.webp` and doesn't crash.
Details: [Images](Images). Base-game icons live in `game/images/items/`.

**Description convention.** First line(s) = what the thing is. If it's tied to a
quest chain, add a blank line and `Quest item: <chain name>`, same as the lab items.

### `ShopItemData(key, name, description, image, price, max_possession=1, max_purchase=1)`

A `ShopItemData` is an `ItemData` that also shows up in the
[office computer shop](#5-the-shop-and-deliveries). `load_item` registers it in both
`item_data` and `shop_item_data`.

| Arg | Meaning |
|-----|---------|
| `price` | dollars per unit; `0` or less shows **Free** (green) and costs nothing |
| `max_possession` | the shop won't let the cart push `owned + in cart` past this |
| `max_purchase` | the shop won't let `bought + in cart` pass this (but see [Known gaps](#8-known-gaps)) |

Current example:

```python
$ load_item(ShopItemData(
    "lab_chemicals",
    "Chemicals",
    ["Chemicals that can be used to create potions.", "", "Quest item: Headmaster's Lab Intro"],
    "images/items/lab-chemicals.webp",
    150,
))
```

### Order inside `load_items`

```python
label load_items:
    $ set_current_mod('base')        # claim context: image prefix + gating
    python:
        global inventory_manager
        if inventory_manager is None:
            inventory_manager = InventoryManager()
        inventory_manager.init()     # wipes item_data / shop_item_data (NOT the inventory)
    $ load_item(...)                 # all definitions
    $ inventory_manager.check_missing_items()   # last: prune stacks with no definition
```

`check_missing_items()` **must** run after all definitions. It drops every stack
whose key has no `ItemData` anymore (see [§7](#7-saves-reloads-and-mods)).

---

## 3. Giving, checking, taking

All calls go through the global `inventory_manager`.

| Call | Effect |
|------|--------|
| `add_item("key")` | +1 of `key` |
| `add_item(Item("key", n))` | +n of `key` |
| `remove_item("key", n)` | −n; the stack is deleted when it reaches 0 |
| `remove_item("key")` | deletes the whole stack (`amount=-1`) |
| `has_item("key")` | `True` if any amount is owned |
| `get_item_count("key")` | owned amount, `0` if none |
| `get_item("key")` | the `Item` stack or `None` |

Behaviour worth knowing:

- **Replays are inert.** `add_item` and `remove_item` return immediately while
  `is_replay()` is true, so gallery replays never duplicate or eat items. You don't
  need to guard event code yourself.
- **`add_item` notifies.** Every call pushes `"Added Nx Name"` through
  `add_notify_message`. One call per pickup reads best; don't loop `add_item("x")`
  five times, give `Item("x", 5)`.
- **`add_item` doesn't check the key.** Giving an undefined key creates a stack
  whose `get_name()` fails, and the next load's `check_missing_items` deletes it.
  Define first.
- **`remove_item` with `0` or a negative other than `-1` does nothing.** Removing
  more than you own just deletes the stack (no negative counts).
- Plain `Item` objects stay in the save. There's no per-unit state; if you need
  "used / unused" or "brewed with X", make that a separate key.

### Typical event pattern

```python
label lab_intro_brew_test(**kwargs):
    $ begin_event(**kwargs)
    ...
    $ inventory_manager.remove_item("lab_chemicals", 1)
    $ inventory_manager.add_item("lab_test_potion")
    ...
    $ end_event("map_overview", **kwargs)
```

Pair it with conditions so the event only fires when the ingredients are there and
the result isn't already owned:

```python
Event(2, "lab_intro_brew_test",
    ItemCondition("lab_chemicals"),
    NOT(ItemCondition("lab_test_potion")),
)
```

---

## 4. Conditions

Both live in `conditions.rpy` and are listed in [Conditions](Conditions) under
*Money & items*.

| Constructor | True when |
|-------------|-----------|
| `ItemCondition(item_key, amount=1, *options)` | `get_item_count(item_key) >= amount` |
| `DeliveryCondition(*options)` | a delivery in `item_delivery` is due (date ≤ today) |

`ItemCondition` composes like any condition (`NOT(...)`, `OR(...)`, options such as
`OptionalOption()`). Its `to_desc_text` prints *"You have N Name(s)"* in green/red
for hint UIs. It reads the owned stack, so it only works when the player owns at
least one; see [Known gaps](#8-known-gaps).

---

## 5. The shop and deliveries

The player buys `ShopItemData` items on the **office computer** (office building →
computer → *Shopping*). Items aren't handed over at checkout; they ship.

```text
shop screen ──add to cart──▶ shopping_cart {key: n}
   │                              │
   └─ cart screen ── Checkout ────┘
         money −= products total          (shipping shown, not charged — see §8)
         item_delivery["D.M.YYYY" of today+3] += [key, key, …]
                                          │
   time_check_events: TimeCondition(weekday="1-4", daytime=1) + DeliveryCondition()
                                          ▼
   office_building_computer_shopping_delivery_event
         Emiko: "a package came for you."  → add_item(Item(key, 1)) per unit
         remove_old_deliveries()
```

| Piece | Where |
|-------|-------|
| entry event (`Event(3, "office_building_computer_shopping_event")` in `office_building_computer_event["shopping"]`) | `inventory.rpy` (registration), `office_building.rpy` (label; resets `shopping_cart = {}`) |
| `office_building_computer_shopping_screen` | product grid, 4 per row; Add to Cart / `− n +` / *Out of Stock* |
| `office_building_computer_shopping_cart_screen` | line items, subtotal, $5 shipping, total, Checkout (disabled if budget < total) |
| `office_building_computer_shopping_screen_checkout` | charges money, queues the delivery for **today + 3 days** |
| `office_building_computer_shopping_delivery_event` | priority 2 in `time_check_events`, morning of Mon–Thu (`weekday="1-4"`, `daytime=1`) |

**Stock rule (per card):** a product is buyable while
`owned + in_cart < max_possession` **and** `bought + in_cart < max_purchase`.
The grid always lists every shop item (`ignore_possession=True, ignore_purchase=True`)
and shows *Out of Stock* rather than hiding it.

**Delivery timing:** due is "date ≤ today", so a parcel landing on a weekend is
delivered the next Monday morning. Everything that's due arrives in one event.

Save-backed globals (`values.rpy`): `inventory_manager`, `shopping_cart`,
`item_delivery` (`{"D.M.YYYY": [key, …]}`).

### Adding a shop item

1. Add the `ShopItemData(...)` in `load_items` (or your mod loader).
2. Drop the icon at the given path (square; the grid shows it at 235×235, the
   journal at 500×500).
3. Gate whatever the item unlocks with `ItemCondition("your_key")`.

---

## 6. The journal inventory page

`screen journal_inventory(display, page)` in `journal.rpy`, opened via
`open_journal(2, …)` or `open_journal(10, …)` (both pages render the same screen).

- **Left:** a 4-column grid of every owned stack (`get_inventory()`), 90×90 icons,
  in insertion order. Clicking one reopens the page with `display = item key`.
- **Right:** the selected item's name, a 500×500 icon, `Amount: N`, then each
  description line.
- If `display` names a key that has no definition, the page resets to empty.

Cheat side: **Journal → Cheats → Items** lists every registered definition
(`get_cheat_item_list()` in `debug.rpy`) with ADD (+1 / right-click +10) and *Add all
items*. See [Cheat Menu](Cheat-Menu#items).

---

## 7. Saves, reloads and mods

- `inventory_manager` is a `default`, so the **stacks** persist. On every start and
  load `load_items` calls `init()`, which **rebuilds the definitions** from code.
  Editing an item's text or icon needs no migration.
- `check_missing_items()` then **deletes every stack whose key is no longer
  defined**. Removing a definition, renaming a key, or disabling the mod that defined
  it erases those items from the save the next time it loads. Re-enabling the mod
  does not bring them back.
- **Mods** define items with `load_item` inside their loader, after
  `set_current_mod('mymod_key')`. `load_item` is gated: a disabled mod's
  definitions are skipped (runtime `add_item` is deliberately **not** gated). Use a
  mod-prefixed key (`mymod_…`) so you don't collide with base items. See
  [Modding](Modding).

```python
init python:
    register_start_method("load_mymod")

label load_mymod:
    $ set_current_mod('mymod_key')
    $ load_item(ItemData("mymod_flask", "Flask", "A dented hip flask.", "images/items/flask.webp"))
    $ load_item(ShopItemData("mymod_tea", "Herbal Tea", "Calms the nerves.", "images/items/tea.webp", 12, max_possession=5, max_purchase=99))
```

> Danger: `start_methods` (mod loaders) run at the **end** of the start / after-load
> wave, after the base `load_items` has already called `check_missing_items()`. On
> every load the mod's definitions don't exist yet at prune time, so **owned mod
> items are wiped**. See [Known gaps](#8-known-gaps). Until that is fixed, don't
> rely on a mod item surviving a save/load.

---

## 8. Known gaps

Code-level facts that differ from what the shop UI suggests. Fix them in code
before relying on the feature, then update this section.

| Gap | Effect |
|-----|--------|
| `check_missing_items()` runs inside base `load_items`, before `start_methods` | mod-defined item stacks are deleted on every load (fix: prune once after the `start_methods` loop in `script.rpy`) |
| `ShopItemData.bought` is never incremented at checkout | `max_purchase` only limits a single cart, not lifetime purchases |
| `bought` lives on the definition, which is rebuilt each load | even once incremented, it would reset on load; it needs a save-backed counter |
| Shipping ($5) is shown in the total but checkout charges only the product sum | the Checkout button gates on the total including shipping, the charge omits it |
| `ItemCondition.to_desc_text` reads `get_item(key).amount` | raises when the player owns none (the `None` stack). `check_condition` itself is safe |
| Item stacks with an undefined key | `add_item` accepts them and the notify toast calls `get_name()` on a missing definition |

---

## 9. API

**Classes** — `Item(key, amount=1)`: `data()` · `get_name()` · `get_description()` ·
`get_image()`. `ItemData(key, name, description, image)`: `get_name()` ·
`get_description()` (always a list) · `get_image()`. `ShopItemData(…, price,
max_possession=1, max_purchase=1)`: `get_price()` · `get_max_possession()` ·
`get_max_purchase()` · `get_bought()`.

**`inventory_manager`** — `add_item(item|key)` · `remove_item(key, amount=-1)` ·
`has_item(key)` · `get_item(key)` · `get_item_count(key)` · `get_inventory()` ·
`has_item_data(key)` · `get_item_data(key)` · `get_all_shop_items(ignore_possession=False,
ignore_purchase=False)` · `init()` · `check_missing_items()`.

**Module functions** — `load_item(ItemData)` · `has_delivery_today()` ·
`get_delivery_today()` · `remove_old_deliveries()`.

**Conditions** — `ItemCondition(item_key, amount=1, *options)` ·
`DeliveryCondition(*options)`.

---

## 10. Conventions

- Keys are snake_case and feature-prefixed (`lab_…`, `mymod_…`). Never rename a
  shipped key; it silently deletes the item from every save.
- One definition per key. Put base items in `load_items`, mod items in the mod loader.
- Icons go in `images/items/`, kebab-case, square, WebP.
- Quest items end their description with `""` + `Quest item: <chain>`.
- Give items inside events between `begin_event` / `end_event`, and gate the event
  with `ItemCondition` / `NOT(ItemCondition(...))` so it can't double-award.
- Prefer a single `add_item(Item(key, n))` over repeated calls (one toast).

### Related files
- `game/scripts/inventory.rpy` — classes, `inventory_manager`, `load_item`, shop screens, checkout, delivery event, `label load_items`
- `game/scripts/conditions.rpy` — `ItemCondition`, `DeliveryCondition`
- `game/scripts/journal/journal.rpy` — `journal_inventory` screen, cheat Items tab, `add_item_cheat`, `give_every_item`
- `game/scripts/buildings/office_building.rpy` — `office_building_computer_shopping_event`
- `game/scripts/values.rpy` — `inventory_manager`, `shopping_cart`, `item_delivery` defaults
- `game/scripts/debug.rpy` — `get_cheat_item_list()`
- `game/script.rpy` — `call load_items` in the start / after-load wave
