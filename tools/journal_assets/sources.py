"""
Source files for the journal asset generators.

Nothing here is committed: the textures and the icon font are downloaded on first
use into .cache/ (gitignored). All sources are licensed for use in a commercial
adult game without restrictions:

  fabric_leather_02   Poly Haven          CC0
  Paper001            ambientCG           CC0
  Material Symbols    Google              Apache 2.0  (ribbon icons)
  Crimson Pro         Fonthausen          OFL         (ribbon labels; shipped in game/fonts)
  Hershey fonts       Dr. A. V. Hershey   free use with acknowledgement (doodle lettering;
                      (format: James Hurt) the acknowledgement ships in game/gui/journal/NOTICE.txt)
"""
import io
import urllib.request
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
CACHE = HERE / ".cache"
GUI_OUT = REPO / "game" / "gui" / "journal"
GAME_FONTS = REPO / "game" / "fonts"

LEATHER = CACHE / "fabric_leather_02_diff_2k.jpg"
PAPER = CACHE / "Paper001_2K-JPG_Color.jpg"
ICON_FONT = CACHE / "MaterialSymbolsRounded.ttf"
HERSHEY_SIMPLEX = CACHE / "hershey" / "futural.jhf"

_URLS = {
    LEATHER: "https://dl.polyhaven.org/file/ph-assets/Textures/jpg/2k/fabric_leather_02/fabric_leather_02_diff_2k.jpg",
    ICON_FONT: "https://raw.githubusercontent.com/google/material-design-icons/master/variablefont/"
               "MaterialSymbolsRounded%5BFILL%2CGRAD%2Copsz%2Cwght%5D.ttf",
    HERSHEY_SIMPLEX: "https://raw.githubusercontent.com/kamalmostafa/hershey-fonts/master/hershey-fonts/futural.jhf",
}
_PAPER_ZIP = "https://ambientcg.com/get?file=Paper001_2K-JPG.zip"


def _fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "mts-journal-assets"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        return resp.read()


def ensure_sources():
    CACHE.mkdir(exist_ok=True)
    for path, url in _URLS.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            print(f"downloading {path.name}")
            path.write_bytes(_fetch(url))
    if not PAPER.exists():
        print("downloading Paper001")
        with zipfile.ZipFile(io.BytesIO(_fetch(_PAPER_ZIP))) as z:
            PAPER.write_bytes(z.read(PAPER.name))
    GUI_OUT.mkdir(parents=True, exist_ok=True)


def save_webp(img, path, lossless=False):
    path.parent.mkdir(parents=True, exist_ok=True)
    if lossless:
        img.save(path, "WEBP", lossless=True, quality=100, method=6)
    else:
        # alpha stays lossless; colour at q92 keeps the leather grain without banding
        img.save(path, "WEBP", quality=92, alpha_quality=100, method=6)
