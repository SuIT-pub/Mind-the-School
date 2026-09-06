# Contributing to Mind the School

Thanks for wanting to help. This repo is the game's source and the source of the
developer wiki. You do **not** need to write code to contribute — ideas, bug reports,
and wiki pages all count.

The game is **18+**. Contributors must be adults. Treat other people in Issues,
Discussions, and PRs with the same respect you'd want in a small workshop, not a
comment section.

## Where things go

| What you have | Where it belongs |
|---|---|
| An idea, a design question, a "what if we…" | [Discussions](https://github.com/SuIT-pub/Mind-the-School/discussions) |
| Open-ended talk (lore, systems, player experience) | [Discussions](https://github.com/SuIT-pub/Mind-the-School/discussions) |
| A bug you can reproduce | [Issues](https://github.com/SuIT-pub/Mind-the-School/issues) |
| A concrete wiki gap or correction | [Issues](https://github.com/SuIT-pub/Mind-the-School/issues) |
| A specific, implementable task | [Issues](https://github.com/SuIT-pub/Mind-the-School/issues) |
| A finished change (code, wiki, docs) | A pull request |
| A standalone mod | Keep it in `game/mods/<YourMod>/` and [ship the folder](https://github.com/SuIT-pub/Mind-the-School/blob/master/wiki/Modding.md) — do not open a PR for it |
| Quick chat | [Discord](https://discord.suit-ji.com) |

**Discussions** are for thinking out loud. **Issues** are for work that should get
done. If you are not sure yet, start a Discussion. When the idea is sharp enough to
act on (a bug, a wiki page to write, a change with a clear shape), open an Issue and
link the Discussion.

Search existing Discussions and Issues before opening a new one.

## Reporting a bug

Use the **Bug report** issue template and include:

- Game version, or the git branch / commit if you run from source
- OS
- Steps to reproduce, and what you expected instead
- Whether any mods were enabled
- `traceback.txt` and/or `log.txt` from the game folder when Ren'Py throws

A short, reproducible report is more useful than a long one.

## Wiki

The GitHub Wiki is **authored in this repo**, in the `wiki/` folder — not in the
Wiki tab's web editor. Edit the markdown here and send a PR. Maintainers publish it
with the sync script (`wiki/README.md`).

If you want to **propose** a wiki expansion (new page, missing section, wrong API)
without writing it yourself, open an Issue and say which page and what is missing.

When you **write** the page:

1. Add `wiki/My-Page.md` (hyphens for spaces in the filename).
2. **No `# H1`** — GitHub uses the filename as the title.
3. Cross-page links look like `[Events](Events)`, not a `.md` path.
4. Link the page from `wiki/_Sidebar.md` (and `wiki/Home.md` if it belongs on the landing page).
5. Point "Related files" at the real `game/scripts/…` sources.

Do not upload character cards or other images through the GitHub Wiki UI. Honey Select
cards must be dropped into `wiki/characters/<Name>/` unchanged — never renamed,
recompressed, or opened-and-saved in an image editor. Details: `wiki/README.md`.

Developer system guides live next to this file in `wiki/` ([Events](wiki/Events.md),
[Building Situations](wiki/Building-Situations.md), [Modding](wiki/Modding.md), …).
Read the matching page before changing the system it documents.

## Development setup

You need this to run or test the game from source. Skip it if you are only editing
wiki markdown.

1. **Ren'Py 8.1.3** — [download](https://www.renpy.org/release/8.1.3). Newer 8.1.x may
   work; use 8.1.3 if something breaks.
2. **Clone** this repository.
3. **Python 3.9+**, then from the **repository root** (the folder that contains
   `game/` and `tools/`):

   ```bash
   pip install -r requirements.txt
   python tools/download_assets.py
   ```

   On Windows you can double-click `tools/Download Assets.bat` instead.

   The git tree is **source only**. Images (~21 GB) are downloaded separately. Default
   mode keeps local files and fills in missing ones. Full notes:
   [Developer Guide — Getting the game assets](wiki/Developer-Guide.md).

4. Add the project in the Ren'Py launcher and run it once.

**Branches:** `master` is the last **released** version. Active development lives on a
version branch named like `MTS-285/Version-0.2.2`. Check
[Modding — Quick Start](wiki/Modding.md) for the current one. Target your PR at that
branch unless you are fixing the last release, in which case use `master`.

## Pull requests

1. Fork (or branch, if you have write access).
2. Keep the PR focused — one problem or one wiki page family, not a mixed bag.
3. Match the style of the surrounding `.rpy` / markdown. Do not reformat files you
   did not need to change.
4. Test the path you touched in the running game when the change is playable.
5. Describe **why** the change exists and how you checked it. Link the Issue if there
   is one.
6. Do not commit secrets, downloaded assets, or generated junk (see below).

New game content that is meant to stay optional should be a **mod**, not a core PR.
See [Modding — Quick Start](wiki/Modding.md). `game/mods/*` is gitignored except for
the bundled CheatMod, so a personal mod will not show up in a PR anyway.

## Do not commit

These are ignored or must stay out of git:

- `game/images/`, `game/videos/`, `game/saves/`, `game/cache/`
- `.env` and Cloudflare / R2 credentials
- `assets.zip`, `assets.zip.part`, `.temp_assets/`
- `log.txt`, `traceback.txt`, `errors.txt`
- Personal mods under `game/mods/` (except changes to the bundled CheatMod)
- Wiki character-card PNGs (`wiki/characters/**/*.png` — maintainers handle those)

Do not drive-by-commit compiled `.rpyc` files unless they belong to the `.rpy` you
actually changed.

## License

- **Code and docs in this repository:** MIT (see `LICENSE`)
- **Artwork** (via the asset download and releases): CC BY 4.0

By opening a PR you offer the change under the same licenses.

## Questions

Unsure where a thought belongs? Open a Discussion. That is the right default.
Discord is fine for a quick ping; GitHub is what we can search six months later.
