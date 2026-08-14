# Wiki source

This folder **is** the GitHub Wiki. Every `*.md` file at the top level becomes a wiki
page (the filename, with hyphens shown as spaces, is the page title). `_Sidebar.md`
and `_Footer.md` are the wiki's navigation chrome. These files are the single source
of truth — edit them here and publish with the sync script.

> `README.md` (this file) and the `scripts/` folder are **not** published to the
> wiki — the sync only copies top-level pages.

## Structure

| Page | Section |
|------|---------|
| `Home.md` | landing page |
| `_Sidebar.md` / `_Footer.md` | navigation chrome |
| `Player-Guide.md`, `Player-Walkthroughs.md` | 🎮 players (placeholders for now) |
| `Cheat-Menu.md` | 🎛️ tools |
| `Developer-Guide.md` | 🛠️ developer section landing |
| `Modding.md` | 🛠️ modding quick-start |
| `Building-Situations.md`, `Building-Unlockables.md` | 🛠️ content guides |
| `Events.md`, `Conditions.md`, `Selectors.md`, `Effects.md`, `Modifiers.md`, `Options.md`, `Paperdoll.md` | 🛠️ system guides |

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
4. Commits and pushes.

Pushing needs the same GitHub credentials you use for the main repo. The wiki must
already exist (create one page in the repo's *Wiki* tab once, then the `.wiki.git`
repo is available).

## Adding a page

1. Create `My-Page.md` in this folder (hyphens for spaces, no `# H1`).
2. Add a link to it in `_Sidebar.md` (and wherever else it belongs).
3. Run the sync.
