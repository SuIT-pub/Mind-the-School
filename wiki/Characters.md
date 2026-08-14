The cast of **Mind the School**, grouped as they are in the game. Each name
opens that character's page (description, portrait, and outfit cards).

> **Character cards (HS2 / StudioNeoV2).** The PNGs on character pages are not
> ordinary screenshots. They carry extra binary data after the image, and that
> payload is **keyed to the original filename**. Click a picture to open the
> raw file, then save it **under the same name** — do not rename, recompress, or
> re-export. Placeholders are in each folder until the real cards are dropped in;
> see [Adding images](#adding-images).

## Students (Class 3A)

- [Aona Komuro](Aona-Komuro)
- [Easkey Tanaka](Easkey-Tanaka) — with [Sakura Mori](Sakura-Mori)
- [Elsie Johnson](Elsie-Johnson) — with [Yuriko Oshima](Yuriko-Oshima)
- [Gloria Goto](Gloria-Goto)
- [Luna Clark](Luna-Clark) — twin of [Seraphina Clark](Seraphina-Clark)
- [Seraphina Clark](Seraphina-Clark) — twin of [Luna Clark](Luna-Clark)
- [Hatano Miwa](Hatano-Miwa)
- [Ikushi Ito](Ikushi-Ito)
- [Ishimaru Maki](Ishimaru-Maki)
- [Kokoro Nakamura](Kokoro-Nakamura)
- [Lin Kato](Lin-Kato)
- [Miwa Igarashi](Miwa-Igarashi)
- [Sakura Mori](Sakura-Mori) — with [Easkey Tanaka](Easkey-Tanaka)
- [Soyoon Yamamoto](Soyoon-Yamamoto) — daughter of [Yuki Yamamoto](Yuki-Yamamoto)
- [Yuriko Oshima](Yuriko-Oshima) — with [Elsie Johnson](Elsie-Johnson)

## Teachers

- [Chloe Garcia](Chloe-Garcia) — Art, Music
- [Finola Ryan](Finola-Ryan) — English, History
- [Lily Anderson](Lily-Anderson) — Math, Sciences
- [Yulan Chen](Yulan-Chen) — History, Politics
- [Zoe Parker](Zoe-Parker) — Physical Education, Health

## Administrative Staff

- [Emiko Langley](Emiko-Langley) — Secretary
- [Linh Nguyen](Linh-Nguyen) — Nurse

## Parents

- [Adelaide Hall](Adelaide-Hall) — Kitchen Mother
- [Nubia Davis](Nubia-Davis)
- [Yuki Yamamoto](Yuki-Yamamoto) — mother of [Soyoon Yamamoto](Soyoon-Yamamoto)

## Administration

- [Mark Benson](Headmaster) — Headmaster (player character)

## Adding images

Each character has a folder next to this page in the repo:

```
wiki/characters/<Name>/
  <Name>.md           ← this character's wiki page
  portrait.png        ← drop the main card here
  outfits/            ← drop outfit cards here
```

1. Copy the PNG **unchanged** into that folder (portrait) or into `outfits/`
   (outfit cards).
2. If the file is not named `portrait.png` or `outfit-1.png` / `outfit-2.png` /
   `outfit-3.png`, **keep the original name** and edit the two URLs on the
   character page so they match. Never rename the PNG to fit the placeholder.
3. Run the wiki sync. Do not upload through the GitHub Wiki web UI.

The download links point at
`https://raw.githubusercontent.com/wiki/SuIT-pub/Mind-the-School/…` so the file
you get is the git blob, not a preview transcode.
