---
name: update-devstatus
description: Use when starting, finishing, pausing or reprioritising a feature, when a release or version bump happens, when the devstatus hook reminds you after a commit, or when asked what is being worked on — keeps devstatus.json (the public roadmap on mts-game.com) current.
---

# Update devstatus.json

`devstatus.json` in the repo root feeds the public roadmap on https://mts-game.com/roadmap and the
"What I'm working on" box on the home page. **Players read this.** Write for them, not for the dev team.

You can update it on any branch. When you push, the `Publish dev status` GitHub Action copies it
to the `devstatus` branch, which the site reads every 10 minutes. The newest `updatedAt` wins, so
always bump `updatedAt` — an unchanged timestamp is treated as "nothing new" and skipped.

## When to update

| Situation | Change |
|---|---|
| You start work on a feature | Add or move it to `now` |
| A feature is finished and merged | Move it from `now` to `done` with `doneIn` + `doneAt` |
| Plans change | Reorder or move items between `next` and `later` |
| Version bump in `game/options.rpy` (`config.version`) | Update `currentVersion`; set `targetVersion` to the version being worked toward |
| Progress on a long `now` item | Optionally set `progress` (0–100) |

Every change also sets `updatedAt` to the current UTC time (`2026-10-12T18:00:00Z` format).

## Automatic reminder

A PostToolUse hook (`tools/devstatus_hook.py`, wired in `.claude/settings.json`) runs after every
`git commit`. When the commit touched `game/` or `wiki/` (not just images, audio or GUI assets) but not
`devstatus.json`, it reminds you to use this skill. Decide then:

- The commit starts, finishes or changes something a **player would notice** → update the file.
- It is a bug fix, refactor, tooling or content cleanup players won't see → do nothing.

Don't update `devstatus.json` for every commit; the roadmap shows features, not a changelog.

## Schema (schemaVersion 1)

```json
{
  "schemaVersion": 1,
  "updatedAt": "2026-10-12T18:00:00Z",
  "currentVersion": "0.2.2",
  "targetVersion": "0.3.0",
  "now":   [{ "id": "lab-building", "title": "…", "summary": "…", "progress": 40 }],
  "next":  [{ "id": "…", "title": "…", "summary": "…" }],
  "later": [{ "id": "…", "title": "…", "summary": "…" }],
  "done":  [{ "id": "…", "title": "…", "summary": "…", "doneIn": "0.2.2", "doneAt": "2026-10-01" }]
}
```

Rules (the validator enforces all of them):
- `id`: kebab-case, unique across all four lists, never changes once published.
- `title`: at most 60 characters. `summary`: at most 160 characters.
- `progress`: optional, integer 0–100, only meaningful in `now`.
- `done`: newest first, **at most 10 entries** — drop the oldest when adding.
- `doneAt`: `YYYY-MM-DD`. `doneIn`: the version that shipped it.

## Writing rules

- **Player voice.** "Brew something in the lab and see what happens", not "Implement Type 1 drink flow".
  No ticket numbers (MTS-285), file names, class names or engine jargon.
- **No spoilers.** Nothing from `wiki/Lore.md` or `wiki/Roadmap.md` that the game hasn't revealed:
  no backers, no predecessor, no inspector, no names of future characters, no plot twists.
- **Nothing explicit.** The website is public and must stay non-pornographic. Describe features,
  never sex acts, body parts or kinks. "Content preferences" — not what the preferences are.
- One idea per item. If a summary needs "and also", it is probably two items.
- Don't promise dates.

## Steps

1. Read the current `devstatus.json`.
2. Apply the change from the table above. Keep `done` newest first and trimmed to 10.
3. Set `updatedAt`.
4. Run `python tools/validate_devstatus.py` — it must print `devstatus.json: OK`.
   If the validator fails, fix the file; an invalid file freezes the public roadmap.
5. Commit `devstatus.json` on its own: `Update dev status: <what changed>`.

## Examples

**Starting a feature** — the lab's potion flow begins:

```json
"now": [
  { "id": "usable-potions", "title": "Potions you can use",
    "summary": "Brew something in the lab, take it to a location on campus and see what happens.", "progress": 10 }
]
```
…and remove `usable-potions` from `next`.

**Finishing and releasing** — 0.2.2 ships on 2026-11-02:

```json
"currentVersion": "0.2.2",
"targetVersion": "0.3.0",
"done": [
  { "id": "version-0-2-2", "title": "Version 0.2.2",
    "summary": "Event flags, pausable situations and a new map system for places beyond the campus.",
    "doneIn": "0.2.2", "doneAt": "2026-11-02" },
  …older entries, at most 10 in total…
]
```
…and move the next item from `next` into `now`.
