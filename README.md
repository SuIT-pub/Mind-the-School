<div align="center">
  <img src="https://iili.io/dHIFL3G.png" width="1600" height="180"/>
</div>

# Mind the School

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://github.com/SuIT-pub/Mind-the-School?tab=License-1-ov-file)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg?style=flat-square)](https://github.com/SuIT-pub/Mind-the-School?tab=License-1-ov-file)

[![Update Patreon Members](https://github.com/SuIT-pub/Mind-the-School/actions/workflows/update_members.yml/badge.svg?branch=master)](https://github.com/SuIT-pub/Mind-the-School/actions/workflows/update_members.yml)

[![GitHub Release](https://img.shields.io/github/v/release/SuIT-pub/Mind-the-School?style=flat-square&label=Release)](https://github.com/SuIT-pub/Mind-the-School/releases/latest)
[![Static Badge](https://img.shields.io/badge/-Wiki-grey?style=flat-square&logo=bookstack&logoColor=white)](https://wiki.suit-ji.com)
[![Static Badge](https://img.shields.io/badge/-Jira-blue?style=flat-square&logo=jirasoftware&logoColor=white)](https://suitpub.atlassian.net/jira/software/projects/MTS/boards/1)

[![Discord](https://img.shields.io/discord/1105841057016598569?logo=Discord&logoColor=white&style=flat-square&label=Discord&link=http%3A%2F%2Ftiny.cc%2Fmindtheschooldiscord)](https://discord.suit-ji.com)
[![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fwww.patreon.com%2Fapi%2Fuser%2F93190317&query=%24.included.0.attributes.patron_count&suffix=%20Patreons&style=flat-square&logo=Patreon&logoColor=white&label=Suit-JI&color=red)](https://patreon.suit-ji.com)
[![Static Badge](https://img.shields.io/badge/Itch.io-white?style=flat-square&logo=itchdotio&logoColor=white&labelColor=grey&color=red)](https://itch.suit-ji.com)

[![Made with Ren'Py](https://img.shields.io/badge/Made%20with-Ren'Py-red?style=flat-square)](https://www.renpy.org/)
[![Adult Content](https://img.shields.io/badge/Adult%20Content-18%2B-red?style=flat-square)]()
[![Development Status](https://img.shields.io/badge/Status-In%20Development-yellow?style=flat-square)]()

## About the Game

Mind the School is an adult visual novel where you take on the role of a new headmaster at a prestigious school that has fallen from grace. Armed with your unique theory of "intimate conditioning," your mission is to restore the school to its former glory while implementing your revolutionary educational approach.

### Key Features

- **School Management**: Manage various aspects of the school including facilities, staff, and student activities
- **Character Development**: Interact with students and staff, influencing their development through your choices
- **Multiple Locations**: Explore and manage different areas of the school including:
  - School Building
  - Dormitory
  - Labs
  - Sports Facilities
  - And more!
- **Quest System**: Complete various objectives and missions to progress through the story
- **Stats Management**: Monitor and influence various statistics including:
  - School Reputation
  - Student Happiness
  - Education Quality
  - Character Relationships
- **Time Management**: Make strategic decisions about how to spend your time each day
- **Consequences**: Your choices affect the school's development and characters' relationships

## Content Warning

This game contains adult content and themes. Players must be 18 years or older. The game includes:
- Mature themes and situations
- Sexual content
- Adult language
- Player choice-driven narrative

## Installation

### PC & Mac
1. Download the latest release from the [Releases Page](https://github.com/SuIT-pub/Mind-the-School/releases/)
2. Extract the .zip file
3. Run the executable file

### Android
1. Download the .apk file from the Releases page
2. Open the .apk file on your device
3. Follow the installation instructions on your device

## Modding
You want to create a mod using the game's inbuilt modding framework?
Check out my Quickstart Guide in the Wiki: [https://wiki.suit-ji.com/books/quickstart](https://wiki.suit-ji.com/books/quickstart)

## Game Assets

The game source code is distributed through this repository. Large game assets
(images, etc.) are hosted separately on Cloudflare R2 and are not included in Git.

### For mod developers

After cloning the repository, open a terminal in the **repository root** (the folder
that contains `game/` and `tools/`, not `game/` itself). Then install dependencies and
download the current assets:

```bash
cd Mind-the-School
pip install -r requirements.txt
python tools/download_assets.py
```

Or double-click `tools/Download Assets.bat` on Windows.

By default the install **merges** (`--mode keep-existing`): local files are kept,
and only missing paths are added from the cloud. Use
`--mode overwrite-existing` to let cloud files replace locals, or
`--mode folder-swap` to replace `game/images/` entirely.

The downloader automatically checks the installed asset version and only
downloads the assets when a newer version is available. No Cloudflare account or
credentials are required.

On network errors, cancel (Ctrl+C), or a hard kill that leaves `assets.zip.part`,
run the script again to **resume** the download (HTTP Range). A bad checksum
removes the bad file and forces a fresh download. To discard a partial download
instead of resuming:

```bash
python tools/download_assets.py --cleanup
```

See `wiki/Developer-Guide.md` (Getting the game assets) for the full failure /
resume / cleanup notes.

### For project maintainers

To publish a new asset version:

1. Copy `.env.example` to `.env` and fill in your R2 credentials.
2. Set `ASSET_VERSION` in `.env` to the new version number.
3. Run `python tools/upload_assets.py` (or `tools/Upload Assets.bat` on Windows).

The upload script creates `assets.zip` and `version.json` on R2, replacing the
previous version. Credentials must never be committed to Git.

Before the first upload, create an R2 bucket (Standard storage), enable public
access via an `*.r2.dev` URL, and set `PUBLIC_ASSET_URL` in
`tools/download_assets.py` to that URL.

## Development Status

The game is currently in active development. The current version includes:
- Complete introduction sequence
- First 10 days of gameplay
- Basic school management systems
- Core game mechanics
- Free roaming after day 10

## Community & Support

- Join our [Discord](https://discord.suit-ji.com) for discussions and updates
- Support development on [Patreon](https://patreon.suit-ji.com)
- Follow us on [Itch.io](https://itch.suit-ji.com)
- Check our [Wiki](https://wiki.suit-ji.com) for guides and information

## Legal

- Game code is licensed under the MIT License
- Creative assets are licensed under CC BY 4.0
- All characters and events in this game are entirely fictional
- Players must be 18 years or older
