# Wiki source

This folder **is** the GitHub Wiki. Every top-level `*.md` file becomes a wiki page
(the filename, with hyphens shown as spaces, is the page title). Character pages are
authored under `characters/<Name>/` next to their images; the sync **promotes** each
`<Name>.md` to the wiki root so GitHub can open it (nested paths starting with
`characters/` collide with the Characters index). `_Sidebar.md` and `_Footer.md` are
the wiki's navigation chrome. These files are the single source of truth — edit them
here and publish with the sync script.

> `README.md` (this file) and the `scripts/` folder are **not** published to the
> wiki. The sync copies top-level pages **and** extra directories such as
> `characters/` (each character page lives with its card images).

## Structure

| Page | Section |
|------|---------|
| `Home.md` | landing page |
| `_Sidebar.md` / `_Footer.md` | navigation chrome |
| `Player-Guide.md` | 🎮 players (placeholder) |
| `Player-Walkthroughs.md`, `Walkthrough-Event-Chains.md`, `Walkthrough-Unlocks.md`, `Walkthrough-Locations.md` | 🎮 walkthroughs |
| `Characters.md` | 🎮 character index (groups → per-character pages) |
| `characters/<Name>/` | one folder per character (page + portrait + outfits) |
| `Cheat-Menu.md` | 🎛️ tools |
| `Developer-Guide.md` | 🛠️ developer section landing |
| `Modding.md` | 🛠️ modding quick-start |
| `School-Levels.md` | 🎮 / 🛠️ campus climate (levels 1–10) |
| `Building-Situations.md`, `Building-Unlockables.md` | 🛠️ content guides |
| `Events.md`, `Conditions.md`, `Selectors.md`, `Effects.md`, `Modifiers.md`, `Options.md`, `Paperdoll.md`, `Images.md`, `Journal-Alerts.md` | 🛠️ system guides |

All pages are **hand-authored here**. Wiki pages have no `# H1` (GitHub shows the page
title from the filename) and link to each other with `[Label](Page-Name)`; in-page
section links (`[text](#heading)`) work as on GitHub. "Related files" bullets point to
the actual source in `game/scripts/…` — those `.rpy` paths are the code the guide
documents.

## Publishing

`sync-wiki.ps1` (PowerShell, the repo's primary shell) publishes the folder. A
`sync-wiki.bat` wrapper sits next to it so you can **double-click it in the IDE /
Explorer**; it runs the `.ps1` and pauses so you can read the output.

```powershell
pwsh wiki/scripts/sync-wiki.ps1                       # auto commit message
pwsh wiki/scripts/sync-wiki.ps1 -Message "Update situation guide"
```

The sync script:

1. Derives the wiki remote from `origin` (`…/Mind-the-School.wiki.git`).
2. Clones/updates the wiki repo into `wiki/.wiki-repo/` (git-ignored).
3. Mirrors the top-level `*.md` pages (except `README.md`) into it — additions,
   changes, **and deletions**.
4. Mirrors extra directories such as `characters/` **byte-for-byte** (no image
   transcoding or renaming).
5. Promotes each `characters/<Name>/<Name>.md` to a top-level wiki page (GitHub
   Wiki cannot navigate nested `characters/…` paths — they resolve as the
   Characters index).
6. Commits and pushes.

Pushing needs the same GitHub credentials you use for the main repo. The wiki must
already exist (create one page in the repo's *Wiki* tab once, then the `.wiki.git`
repo is available).

## Adding a page

1. Create `My-Page.md` in this folder (hyphens for spaces, no `# H1`).
2. Add a link to it in `_Sidebar.md` (and wherever else it belongs).
3. Run the sync.

## Character pages and card images

Each character has a folder under `characters/` that holds the wiki page **and**
the image files. Edit the page there; the sync publishes it as a top-level wiki
page named `<Name>` (so `[Aona Komuro](Aona-Komuro)` works). Images stay in the
folder and are copied as-is.

```
characters/Aona-Komuro/
  Aona-Komuro.md      ← wiki page
  portrait.png        ← drop the main card here
  outfits/            ← drop outfit cards here
```

The PNGs are Honey Select 2 / StudioNeoV2 character cards: extra binary data sits
after the image payload and is **keyed to the original filename**. Rules:

- Drop files in as-is. **Never rename, recompress, re-export, or open-and-save**
  them in an image editor.
- If the card's filename is not `portrait.png` / `outfit-1.png`, keep that
  original name and change the links on the character page to match.
- Clicking a portrait or outfit on the wiki opens the **raw** file
  (`raw.githubusercontent.com/wiki/…`) so the download is the git blob, not a
  transcoded preview.
- Do not upload cards through the GitHub Wiki web UI — that can rename or
  recompress them. Always drop files into `wiki/characters/…` and run the sync.
