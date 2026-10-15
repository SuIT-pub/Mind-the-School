"""
Small hand-made UI pieces for the journal pages (game/gui/journal/ui/).

Every mark is drawn stroke by stroke with slightly varying pressure, so nothing
repeats like a font or a stock brush would.

  bar_full / bar_empty      pencil-hatched value bar + empty pencil box (bar left/right)
  box_full / box_empty      single level box, hatched or empty
  highlight                 chisel-tip marker swipe (used as a Frame, ends stay intact)
  underline                 pencil underline for hovered entries (Frame)
  scroll_thumb / scroll_track  graphite-stroke thumb on a dotted pencil guide line
  slip                      paper slip behind tooltips (Frame)
  leader                    one dot of a ledger leader line, tiled between label and figure
  backdrop                  warm vignette laid over the (blurred) map
  photo_backdrop            mottled studio backdrop behind the cut-out character photos
  mood_track / marker       watercolour situation-mood track in a pencil box + ink pointer
  foldout_panel             one creased panel of the fold-out patron sheet (Credits)
  alert_pin                 paper sticker with a red asterisk: "something new" on a ribbon

Run:  python tools/journal_assets/build_ui.py
"""
import math
import random
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sources import GUI_OUT, ensure_sources, save_webp  # noqa: E402

OUT = GUI_OUT / "ui"
SS = 4
PENCIL = (112, 106, 96)
HIGHLIGHT = (255, 214, 64)


class Sheet:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.img = Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.img)

    def line(self, x0, y0, x1, y1, width, color, seed, amp=0.4, alpha=235):
        rng = random.Random(seed)
        n = max(2, int(math.hypot(x1 - x0, y1 - y0) * 1.5))
        ph = [rng.random() * 6.28 for _ in range(3)]
        for i in range(n + 1):
            t = i / n
            off = amp * (math.sin(t * 7 + ph[0]) * 0.6 + math.sin(t * 19 + ph[1]) * 0.3)
            # pressure: a little lighter where the stroke starts and lifts off
            press = 0.75 + 0.25 * math.sin(math.pi * t)
            x = (x0 + (x1 - x0) * t) * SS
            y = (y0 + (y1 - y0) * t + off) * SS
            r = width / 2 * SS * (0.85 + 0.25 * math.sin(i * 0.3 + ph[2])) * press
            self.d.ellipse((x - r, y - r, x + r, y + r), fill=color + (int(alpha * press),))

    def box(self, x0, y0, x1, y1, seed):
        rng = random.Random(seed)
        # corners overshoot slightly, like a quickly drawn box
        o = 1.2
        self.line(x0 - o, y0, x1 + o * rng.random(), y0, 1.4, PENCIL, rng.randint(0, 10**6))
        self.line(x0, y1, x1 + o, y1, 1.4, PENCIL, rng.randint(0, 10**6))
        self.line(x0, y0 - o, x0, y1 + o * rng.random(), 1.4, PENCIL, rng.randint(0, 10**6))
        self.line(x1, y0, x1, y1 + o, 1.4, PENCIL, rng.randint(0, 10**6))

    def hatch(self, x0, y0, x1, y1, seed, step=6.5):
        rng = random.Random(seed)
        x = x0 + 1.5
        h = y1 - y0
        while x < x1 - 1:
            xe = min(x1 - 1, x + h * 0.6)
            ye = y1 - 1.5 - (xe - x) / 0.6
            self.line(x, y1 - 1.5, xe, ye, 1.9, PENCIL, rng.randint(0, 10**6), amp=0.25)
            x += step * rng.uniform(0.85, 1.15)

    def out(self):
        return self.img.resize((self.w, self.h), Image.LANCZOS)


def bars():
    for w, h, name in ((210, 18, "bar"), (150, 14, "bar_small")):
        full = Sheet(w, h)
        full.hatch(2, 2, w - 2, h - 2, 11)
        full.box(2, 2, w - 2, h - 2, 12)
        save_webp(full.out(), OUT / f"{name}_full.webp", lossless=True)
        empty = Sheet(w, h)
        empty.box(2, 2, w - 2, h - 2, 12)
        save_webp(empty.out(), OUT / f"{name}_empty.webp", lossless=True)


def boxes():
    full = Sheet(18, 20)
    full.hatch(2, 2, 16, 18, 21, step=4.5)
    full.box(2, 2, 16, 18, 22)
    save_webp(full.out(), OUT / "box_full.webp", lossless=True)
    empty = Sheet(18, 20)
    empty.box(2, 2, 16, 18, 22)
    save_webp(empty.out(), OUT / "box_empty.webp", lossless=True)


def highlight():
    w, h = 320, 34
    m = Image.new("L", (w * SS, h * SS), 0)
    d = ImageDraw.Draw(m)
    rng = random.Random(7)
    # chisel tip: slanted ends, edges that drift a little along the swipe
    top = [(x, 3 + rng.uniform(-0.8, 0.8)) for x in range(10, w - 4, 8)]
    bot = [(x, h - 3 + rng.uniform(-0.8, 0.8)) for x in range(w - 10, 4, -8)]
    pts = [(4, h - 4)] + [(8, 3)] + top + [(w - 2, 4)] + [(w - 6, h - 3)] + bot
    d.polygon([(x * SS, y * SS) for x, y in pts], fill=150)
    m = m.filter(ImageFilter.GaussianBlur(0.7 * SS))
    # ink pools slightly where the marker rests at both ends
    arr = np.asarray(m, np.float32)
    X = np.arange(w * SS, dtype=np.float32)[None, :]
    ends = np.exp(-((X - 10 * SS) / (8 * SS)) ** 2) + np.exp(-((X - (w - 8) * SS) / (8 * SS)) ** 2)
    arr = np.clip(arr * (1 + 0.25 * ends), 0, 255)
    img = Image.new("RGBA", m.size, HIGHLIGHT + (0,))
    img.putalpha(Image.fromarray(arr.astype(np.uint8)))
    save_webp(img.resize((w, h), Image.LANCZOS), OUT / "highlight.webp", lossless=True)


def underline():
    # line sits at the bottom of a row-high image so it works as a button Frame
    s = Sheet(320, 34)
    s.line(3, 31, 317, 30.5, 1.6, PENCIL, 31, amp=0.6, alpha=220)
    save_webp(s.out(), OUT / "underline.webp", lossless=True)


def scrollbar():
    # thumb: a firm graphite stroke with rounded ends (used as a Frame, ends stay intact)
    t = Sheet(10, 120)
    t.line(5, 5, 5.2, 115, 4.2, (70, 64, 56), 41, amp=0.35, alpha=245)
    t.line(5.4, 8, 5.5, 112, 1.4, (40, 36, 32), 43, amp=0.25, alpha=200)
    save_webp(t.out(), OUT / "scroll_thumb.webp", lossless=True)
    # track: one dot of a dotted pencil guide line, tiled vertically
    b = Sheet(10, 9)
    b.d.ellipse((4.1 * SS, 3.6 * SS, 5.9 * SS, 5.4 * SS), fill=PENCIL + (150,))
    save_webp(b.out(), OUT / "scroll_track.webp", lossless=True)


def slip():
    w, h = 220, 60
    img = Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0))
    sh = Image.new("L", img.size, 0)
    ImageDraw.Draw(sh).rectangle((4 * SS, 6 * SS, (w - 3) * SS, (h - 2) * SS), fill=120)
    sh = sh.filter(ImageFilter.GaussianBlur(3 * SS))
    shadow = Image.new("RGBA", img.size, (20, 12, 6, 0))
    shadow.putalpha(sh)
    img.alpha_composite(shadow)
    d = ImageDraw.Draw(img)
    d.rectangle((2 * SS, 2 * SS, (w - 6) * SS, (h - 7) * SS), fill=(250, 245, 232, 255),
                outline=(196, 186, 168, 255), width=SS)
    save_webp(img.resize((w, h), Image.LANCZOS), OUT / "slip.webp", lossless=True)


def leader():
    # one 7px cell of a 32px row; the dot sits on the baseline of 22px Crimson Pro
    w, h = 7, 32
    img = Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0))
    r = 0.95 * SS
    cx, cy = 3.5 * SS, 22.5 * SS
    ImageDraw.Draw(img).ellipse((cx - r, cy - r, cx + r, cy + r), fill=PENCIL + (190,))
    save_webp(img.resize((w, h), Image.LANCZOS), OUT / "leader.webp", lossless=True)


def backdrop():
    w, h = 1920, 1080
    Y, X = np.mgrid[0:h, 0:w].astype(np.float32)
    r = np.sqrt(((X - w / 2) / (w * 0.62)) ** 2 + ((Y - h / 2) / (h * 0.62)) ** 2)
    alpha = 0.50 + 0.30 * np.clip(r, 0, 1) ** 1.8
    img = np.zeros((h, w, 4), np.float32)
    img[..., :3] = np.array([24, 18, 14], np.float32) / 255
    img[..., 3] = alpha
    out = Image.fromarray((img * 255).astype(np.uint8), "RGBA")
    save_webp(out, OUT / "backdrop.webp")


def photo_backdrop():
    # mottled studio backdrop of a school photo day; the character renders are cut out
    w, h = 400, 400
    rng = np.random.default_rng(51)
    mottle = np.zeros((h, w), np.float32)
    for blur, weight in ((40, 1.0), (14, 0.45), (4, 0.15)):
        layer = Image.fromarray((rng.random((h, w)) * 255).astype(np.uint8))
        layer = np.asarray(layer.filter(ImageFilter.GaussianBlur(blur)), np.float32)
        layer = (layer - layer.mean()) / (layer.std() + 1e-6)
        mottle += layer * weight
    mottle /= np.abs(mottle).max()
    Y, X = np.mgrid[0:h, 0:w].astype(np.float32)
    # the flash leaves a lighter patch behind the head, upper centre
    light = np.exp(-(((X - w * 0.5) / (w * 0.42)) ** 2 + ((Y - h * 0.38) / (h * 0.45)) ** 2))
    dark = np.array([70, 86, 104], np.float32)
    bright = np.array([148, 162, 176], np.float32)
    t = np.clip(light * 0.85 + mottle * 0.12, 0, 1)[..., None]
    rgb = dark * (1 - t) + bright * t
    out = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8), "RGB")
    save_webp(out, OUT / "photo_backdrop.webp")


def mood_track():
    # situation mood: a watercolour wash from rust red to sage green inside a pencil box
    w, h = 552, 18
    rng = np.random.default_rng(61)
    X = np.linspace(0, 1, w * SS, dtype=np.float32)[None, :, None]
    red = np.array([176, 74, 58], np.float32)
    ochre = np.array([196, 160, 86], np.float32)
    green = np.array([92, 138, 78], np.float32)
    rgb = np.where(X < 0.5, red + (ochre - red) * (X / 0.5), ochre + (green - ochre) * ((X - 0.5) / 0.5))
    rgb = np.repeat(rgb, h * SS, axis=0)
    # pigment pools unevenly, like a quick brush stroke
    blot = Image.fromarray((rng.random((h * SS // 4, w * SS // 4)) * 255).astype(np.uint8))
    blot = blot.resize((w * SS, h * SS), Image.BICUBIC).filter(ImageFilter.GaussianBlur(3 * SS))
    blot = np.asarray(blot, np.float32) / 255
    alpha = np.clip(0.68 + (blot - 0.5) * 0.6, 0.4, 0.9)
    wash = np.dstack([rgb, alpha * 255]).astype(np.uint8)
    img = Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0))
    img.alpha_composite(Image.fromarray(wash, "RGBA").crop((3 * SS, 3 * SS, (w - 3) * SS, (h - 3) * SS)), (3 * SS, 3 * SS))
    box = Sheet(w, h)
    box.box(2, 2, w - 2, h - 2, 62)
    img.alpha_composite(box.img)
    save_webp(img.resize((w, h), Image.LANCZOS), OUT / "mood_track.webp", lossless=True)


def marker():
    # ink pointer above the mood track, drawn as a filled, slightly uneven triangle
    w, h = 18, 14
    img = Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0))
    pts = [(1.5, 1.8), (16.6, 1.2), (9.2, 12.8)]
    ImageDraw.Draw(img).polygon([(x * SS, y * SS) for x, y in pts], fill=(52, 40, 32, 240))
    save_webp(img.resize((w, h), Image.LANCZOS), OUT / "marker.webp", lossless=True)


def alert_pin():
    # "something new here": a small round paper sticker with a red pencil asterisk,
    # stuck onto a ribbon; readable on every ribbon colour
    w = h = 30
    img = Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0))
    sh = Image.new("L", img.size, 0)
    ImageDraw.Draw(sh).ellipse((4 * SS, 5 * SS, 27 * SS, 28 * SS), fill=150)
    sh = sh.filter(ImageFilter.GaussianBlur(1.6 * SS))
    shadow = Image.new("RGBA", img.size, (20, 12, 6, 0))
    shadow.putalpha(sh)
    img.alpha_composite(shadow)
    ImageDraw.Draw(img).ellipse((2 * SS, 2 * SS, 25 * SS, 25 * SS), fill=(250, 244, 230, 255),
                                outline=(170, 158, 140, 255), width=SS)
    s = Sheet(w, h)
    for k in range(3):
        a = math.pi / 2 + k * math.pi / 3 + 0.12
        cx, cy, r = 13.5, 13.5, 6.8
        s.line(cx - math.cos(a) * r, cy - math.sin(a) * r, cx + math.cos(a) * r, cy + math.sin(a) * r,
               2.1, (160, 40, 34), 900 + k, amp=0.25, alpha=245)
    img.alpha_composite(s.img)
    save_webp(img.resize((w, h), Image.LANCZOS), OUT / "alert_pin.webp", lossless=True)


def foldout_panel():
    # one panel of the folded patron sheet: lighter loose paper, a valley crease on the
    # left edge and a raised fold on the right, so neighbouring panels read as zigzag
    from sources import PAPER

    w, h = 420, 880
    # the texture is landscape (2048x1201): turn it upright and stay clear of its frayed edge
    paper = Image.open(PAPER).convert("L").transpose(Image.ROTATE_90)
    paper = paper.crop((120, 250, 120 + w * 2, 250 + h * 2)).resize((w, h), Image.LANCZOS)
    detail = np.asarray(paper, np.float32)
    # high-pass: keep the fibres, drop the photo's uneven lighting
    detail -= np.asarray(paper.filter(ImageFilter.GaussianBlur(24)), np.float32)
    detail = (detail - detail.mean()) / (detail.std() + 1e-6)
    X = np.arange(w, dtype=np.float32)[None, :]
    valley = np.exp(-X / 22.0) * 0.16
    ridge = np.exp(-(w - 1 - X) / 14.0) * 0.07
    shade = 1.0 - valley + ridge - 0.02 * detail
    base = np.array([247, 241, 228], np.float32)
    rgb = np.clip(base[None, None, :] * shade[..., None], 0, 255)
    save_webp(Image.fromarray(rgb.astype(np.uint8), "RGB"), OUT / "foldout_panel.webp")


if __name__ == "__main__":
    ensure_sources()
    alert_pin()
    foldout_panel()
    photo_backdrop()
    mood_track()
    marker()
    bars()
    boxes()
    highlight()
    underline()
    scrollbar()
    slip()
    leader()
    backdrop()
