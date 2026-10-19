---
name: update-modding-changelog
description: Use when a change affects what modders build on — registration functions, class/function signatures, condition/selector/effect/option behaviour, label or key names, asset naming tokens, save compatibility, the mod loader or names files — or deprecates/removes something, when the modding-changelog hook reminds you after a commit, or when asked what changed for modders. Keeps modding-changelog.json (posted to the Discord modding channel) current.
---

# Update modding-changelog.json

`modding-changelog.json` in the repo root is a running history of changes that matter to people
who write mods for *Mind the School*. **Modders read this.** Unlike `devstatus.json`, it is
technical: name the functions, classes, parameters and wiki pages.

When you push, the `Post modding changelog` GitHub Action posts every entry that wasn't posted
yet to the Discord modding channel — one message per entry, oldest first. It never edits or
deletes a message. Posted ids are recorded on the `devstatus` branch, so an entry is posted once
even if several branches carry it.

## When to add an entry

Ask: **could a mod break, behave differently, or do something new because of this change?**
If you think modders should know, add it.

| Change | Type |
|---|---|
| Something a mod used stops working or needs a change (renamed/removed function, parameter, label, key, asset token, changed default, save break) | `breaking` |
| Same API, different behaviour or a new recommended way | `changed` |
| New API a mod can use (function, class, parameter, hook, register function) | `added` |
| Still works, but will go away; say what to use instead | `deprecated` |
| Gone (after a deprecation, or a dead legacy stub) | `removed` |
| A bug fix in engine/API code that mods may have worked around | `fixed` |
| Docs corrected in a way that changes how to use something | `docs` |
| A new asset pack was published (`upload_assets.py`) | `assets` |

Not for: story content, dialogue, art, balancing, player-only UI, refactors that keep the API, tooling
that only the core team runs. One entry per idea; a big commit can produce several entries.

### Developer wiki changes

The developer pages of the wiki (Events, Conditions, Selectors, Effects, Options, Modifiers, Maps,
Modding, Paperdoll, Images, Dialogue, Building-Situations, Building-Unlockables, Items-and-Inventory,
Journal-Alerts, Value-Ranges, School-Levels, Cheat-Menu, Developer-Guide, …) are what modders code
against. When a page gains a new section, documents behaviour that wasn't written down, or corrects
something that was wrong, add a `docs` entry with the page (and anchor) in `wiki`. Typo fixes and
rewording don't count. Player pages (Player-Guide, Walkthrough-*, Home), Lore, Roadmap, character
pages and the wiki's own scripts never need an entry.

### Asset packs

Asset packs are published locally and never show up in a commit, so `tools/upload_assets.py` writes
the entry itself after every successful upload or `--bump-version`: id `asset-pack-<version>`, type
`assets`, the game version from `devstatus.json`'s `targetVersion`. A pack only reaches downloaders
under a new version number: use `--next-version` (or the VS Code task "Assets: Upload as new
version"), which counts the version up and saves it to `.env`. Pass `--note "…"` to say what
changed in the pack (renamed tokens, new sprite sets, removed files); without it the entry only says
that a new pack is online. The uploader prints a reminder to commit and push `modding-changelog.json`.
If an upload ran without writing the entry (older script, error), add it by hand with
`record_asset_release()` from `tools/modding_changelog_assets.py`.

## Automatic reminder

A PostToolUse hook (`tools/modding_changelog_hook.py`, wired in `.claude/settings.json`) runs after
every `git commit`. When the commit touched `game/scripts/`, `game/mods/`, a developer wiki page or
the asset tools (`tools/upload_assets.py`, `tools/download_assets.py`) but not `modding-changelog.json`,
it reminds you to use this skill. Decide then
with the table above; most content commits need nothing.

## Schema (schemaVersion 1)

```json
{
  "schemaVersion": 1,
  "entries": [
    {
      "id": "event-title",
      "date": "2026-10-17",
      "version": "0.2.2",
      "type": "added",
      "title": "Events can carry their own title (title=)",
      "details": "`Event`, `EventComposite`, … take `title=\"…\"`. …",
      "wiki": "Events"
    }
  ]
}
```

Rules (the validator enforces all of them):
- `entries`: **newest first**. Keep the whole history; nothing is trimmed.
- `id`: kebab-case, unique, never changed or reused once pushed (it is how the poster knows an
  entry was already posted).
- `date`: `YYYY-MM-DD`, the day the change was committed.
- `version`: the release the change ships in. While a version is in progress that is the version
  being worked on (`targetVersion` in `devstatus.json`), not the last release.
- `type`: one of `breaking`, `changed`, `added`, `deprecated`, `removed`, `fixed`, `docs`, `assets`.
- `title`: at most 120 characters. `details`: at most 1500 characters, Discord markdown allowed.
- `wiki`: optional page name on the GitHub wiki, optionally with an anchor: `"Events"` or
  `"Events#event-flags"`. It becomes a link in the post.

## Writing rules

- **Say what a modder has to do.** "Update `mood = \"suprised\"` to `\"surprised\"`", not "renamed a token".
- Show the old and the new form for `breaking`, `changed`, `deprecated`, `removed`.
- Code in backticks, real names from the code. Check the signature in `game/scripts/` before writing it.
- No spoilers from `wiki/Lore.md` / `wiki/Roadmap.md`, nothing explicit: the channel is public.
- Don't edit a posted entry to correct it — Discord won't change. Add a new entry
  (`fixed`/`docs`) that corrects it, and only fix typos in place.

## Steps

1. Read `modding-changelog.json`.
2. Add the entry at the **top** of `entries`.
3. Run `python tools/validate_modding_changelog.py` — it must print `modding-changelog.json: OK`.
4. Commit it on its own: `Update modding changelog: <what changed>`.
5. Optional preview: `python tools/post_modding_changelog_discord.py modding-changelog.json --dry-run`
   prints the messages that would be posted.
