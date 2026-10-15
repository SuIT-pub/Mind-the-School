"""
Pencil doodles for the journal margins (game/gui/journal/doodles/).

Every doodle is drawn stroke by stroke like the other hand-made marks (build_ui.py):
dabs of graphite with varying pressure and a slight tremor, so no two look stamped.
Lettering is limited to single short words on purpose; it is drawn from the Hershey
simplex stroke font, every glyph with its own size, tilt and wobble.

Where each doodle sits on which page is decided in Ren'Py (JOURNAL_DOODLES in
journal_book.rpy); this script only draws them, each cropped to its own size.

It also draws the runtime lettering kit (doodles/glyphs/: every character in a few
variants + metrics.json) and pointing arrows (doodles/arrows/), both in white so
Ren'Py can tint them; journal_doodles.rpy composes pencil notes from them.

Run:  python tools/journal_assets/build_doodles.py
"""
import json
import math
import random
import string
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sources import GUI_OUT, HERSHEY_SIMPLEX, ensure_sources, save_webp  # noqa: E402

OUT = GUI_OUT / "doodles"
SS = 3
PENCIL = (78, 72, 66)
RED_PENCIL = (150, 46, 40)


def load_jhf(path):
    """Hershey .jhf: 5-char glyph id, 3-char vertex count, then coordinate pairs
    offset by 'R'; the first pair is the glyph's left/right extent, ' R' lifts the pen."""
    glyphs, buf = [], ""
    for line in path.read_text(encoding="latin-1").splitlines():
        buf += line
        if len(buf) - 8 >= int(buf[5:8]) * 2:
            glyphs.append(buf)
            buf = ""
    font = {}
    for i, g in enumerate(glyphs):
        data = g[8:8 + int(g[5:8]) * 2]
        left, right = ord(data[0]) - 82, ord(data[1]) - 82
        strokes, cur = [], []
        for k in range(2, len(data), 2):
            pair = data[k:k + 2]
            if pair == " R":
                if cur:
                    strokes.append(cur)
                cur = []
            else:
                cur.append((ord(pair[0]) - 82, ord(pair[1]) - 82))
        if cur:
            strokes.append(cur)
        font[chr(32 + i)] = (left, right, strokes)
    return font


class Sheet:
    def __init__(self, w, h, seed):
        self.w, self.h = w, h
        self.rng = random.Random(seed)
        self.img = Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.img)

    def stroke(self, pts, width=1.6, color=PENCIL, alpha=205, jitter=0.3):
        """A polyline laid down as overlapping dabs; pressure eases in and out."""
        rng = self.rng
        pts = np.array(pts, np.float32)
        if len(pts) < 2:
            pts = np.vstack([pts, pts + 0.3])
        dense = []
        for a, b in zip(pts[:-1], pts[1:]):
            n = max(2, int(math.hypot(*(b - a)) * 2.2))
            dense.extend(a + (b - a) * i / n for i in range(n))
        dense.append(pts[-1])
        ph = rng.random() * 6.28
        m = len(dense)
        for i, (x, y) in enumerate(dense):
            t = i / max(1, m - 1)
            press = 0.55 + 0.45 * math.sin(math.pi * min(1, t * 1.15 + 0.05))
            j = jitter * math.sin(i * 0.9 + ph)
            r = width / 2 * SS * (0.8 + 0.3 * press)
            cx, cy = (x + j * 0.3) * SS, (y + j) * SS
            a = int(alpha * (0.55 + 0.45 * press) * (0.85 + 0.15 * rng.random()))
            self.d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=color + (a,))

    def write(self, font, text, x, y, size, color=PENCIL, slant=0.3, width=1.6, loose=1.2):
        """Short word in quick slanted print; y is the baseline-ish top of capitals."""
        rng = self.rng
        scale = size / 21.0
        cx = x
        for ch in text:
            if ch not in font:
                cx += size * 0.5
                continue
            left, right, strokes = font[ch]
            gs = scale * rng.uniform(0.88, 1.1) ** loose
            sl = slant + rng.uniform(-0.08, 0.08) * loose
            base = rng.uniform(-1.0, 1.0) * loose
            for st in strokes:
                ph = rng.random() * 6.28
                pts = []
                for k, (px, py) in enumerate(st):
                    nx = math.sin(k * 0.7 + ph) * 0.45 * loose
                    ny = math.cos(k * 0.55 + ph) * 0.45 * loose
                    pts.append((cx + (px - left) * gs + py * gs * sl * -1 + nx, y + py * gs + ny + base))
                self.stroke(pts, width, color, jitter=0.3)
            cx += (right - left) * gs * rng.uniform(0.92, 1.04) ** loose
        return cx

    def save(self, name, tilt=0.0):
        img = self.img.resize((self.w, self.h), Image.LANCZOS)
        if tilt:
            img = img.rotate(tilt, resample=Image.BICUBIC, expand=True)
        bbox = img.getbbox()
        if bbox:
            pad = 3
            img = img.crop((max(0, bbox[0] - pad), max(0, bbox[1] - pad),
                            min(img.width, bbox[2] + pad), min(img.height, bbox[3] + pad)))
        save_webp(img, OUT / f"{name}.webp", lossless=True)


# ---------------------------------------------------------------- drawings

def star(name, r, color, seed, tilt):
    s = Sheet(int(r * 2.6), int(r * 2.6), seed)
    c = r * 1.3
    pts = []
    for k in range(6):
        a = -math.pi / 2 + k * 4 * math.pi / 5 + s.rng.uniform(-0.05, 0.05)
        rr = r * s.rng.uniform(0.92, 1.06)
        pts.append((c + math.cos(a) * rr, c + math.sin(a) * rr))
    s.stroke(pts, 1.7, color)
    s.save(name, tilt)


def stars_trio(seed):
    s = Sheet(110, 70, seed)
    for cx, cy, r in ((24, 44, 15), (62, 22, 10), (90, 48, 8)):
        pts = []
        for k in range(6):
            a = -math.pi / 2 + k * 4 * math.pi / 5 + s.rng.uniform(-0.06, 0.06)
            pts.append((cx + math.cos(a) * r, cy + math.sin(a) * r))
        s.stroke(pts, 1.5, PENCIL)
    s.save("stars_trio", -6)


def spiral(seed):
    s = Sheet(80, 80, seed)
    pts = [(40 + math.cos(t) * 30 * i / 160, 40 + math.sin(t) * 27 * i / 160)
           for i, t in ((i, i / 160 * 4.2 * math.pi) for i in range(160))]
    s.stroke(pts, 1.4, PENCIL, alpha=185)
    s.save("spiral", 0)


def heart(name, size, color, seed, tilt, filled_hatch=False):
    s = Sheet(int(size * 2.6), int(size * 2.4), seed)
    cx, cy = size * 1.3, size * 1.15
    pts = []
    for i in range(90):
        t = i / 90 * 2 * math.pi
        x = 16 * math.sin(t) ** 3
        y = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
        pts.append((cx + x * size / 16, cy + y * size / 16))
    s.stroke(pts, 1.7, color)
    if filled_hatch:
        for k in range(-6, 7):
            x0 = cx + k * size / 7
            s.stroke([(x0 - size * 0.35, cy + size * 0.4), (x0 + size * 0.35, cy - size * 0.5)], 1.0, color, alpha=120)
    s.save(name, tilt)


def cube(seed):
    s = Sheet(90, 90, seed)
    x, y, size = 14, 12, 44
    o = size * 0.45
    rng = s.rng
    P = lambda a, b: (x + a + rng.uniform(-0.8, 0.8), y + b + rng.uniform(-0.8, 0.8))
    s.stroke([P(0, o), P(size, o), P(size, size + o), P(0, size + o), P(0, o)], 1.4)
    s.stroke([P(o, 0), P(size + o, 0), P(size + o, size), P(o, size), P(o, 0)], 1.2, alpha=150)
    for a, b in (((0, o), (o, 0)), ((size, o), (size + o, 0)), ((size, size + o), (size + o, size)), ((0, size + o), (o, size))):
        s.stroke([P(*a), P(*b)], 1.2)
    for k in range(7):
        t = k / 7
        s.stroke([P(size + 2, o + t * size + 4), P(size + o - 2, t * size + 2)], 1.0, alpha=130)
    s.save("cube", 4)


def flask(seed):
    s = Sheet(70, 80, seed)
    x, y = 14, 12
    s.stroke([(x + 14, y), (x + 14, y + 22), (x, y + 50), (x + 2, y + 54), (x + 40, y + 54),
              (x + 42, y + 50), (x + 28, y + 22), (x + 28, y)], 1.5)
    s.stroke([(x + 11, y), (x + 31, y)], 1.5)
    s.stroke([(x + 6, y + 40), (x + 36, y + 40)], 1.1, alpha=150)
    for bx, by, br in ((x + 18, y + 46, 2.5), (x + 25, y + 33, 1.8), (x + 21, y + 14, 1.4), (x + 17, y + 2, 1.1)):
        s.stroke([(bx + math.cos(t) * br, by + math.sin(t) * br) for t in np.linspace(0, 6.4, 14)], 1.0, alpha=160)
    s.save("flask", -5)


def tally(seed, n=13):
    s = Sheet(140, 40, seed)
    x, y = 6, 6
    for i in range(n):
        g, k = divmod(i, 5)
        if k == 4:
            s.stroke([(x + g * 34 - 4, y + 22), (x + g * 34 + 26, y + 2)], 1.5)
        else:
            xx = x + g * 34 + k * 6
            s.stroke([(xx, y), (xx + 1, y + 24)], 1.5)
    s.save("tally", -2)


def tictactoe(seed):
    s = Sheet(90, 90, seed)
    o = 12
    for k in (1, 2):
        s.stroke([(o + k * 22, o - 2), (o + k * 22 + 1, o + 66)], 1.4)
        s.stroke([(o - 2, o + k * 22), (o + 66, o + k * 22 + 1)], 1.4)
    def X(cx, cy):
        s.stroke([(cx - 6, cy - 6), (cx + 6, cy + 6)], 1.5)
        s.stroke([(cx + 6, cy - 6), (cx - 6, cy + 6)], 1.5)
    def O(cx, cy):
        s.stroke([(cx + math.cos(t) * 7, cy + math.sin(t) * 7) for t in np.linspace(0.3, 6.6, 20)], 1.5)
    c = lambda i: o + 11 + i * 22
    X(c(0), c(0)); O(c(1), c(0)); X(c(1), c(1)); O(c(2), c(1)); X(c(2), c(2))
    s.stroke([(c(0) - 9, c(0) - 9), (c(2) + 9, c(2) + 9)], 1.8, RED_PENCIL)
    s.save("tictactoe", 3)


def paper_plane(seed):
    s = Sheet(100, 70, seed)
    s.stroke([(8, 34), (88, 10), (40, 56), (8, 34)], 1.5)
    s.stroke([(88, 10), (34, 40), (40, 56)], 1.3)
    # dashed flight path
    for k in range(5):
        x0 = 6 - k * 12
        s.stroke([(x0 + 60, 62 + k * 0.5), (x0 + 66, 62 + k * 0.4)], 1.2, alpha=150)
    s.save("paper_plane", -4)


def sun(seed):
    s = Sheet(80, 80, seed)
    s.stroke([(40 + math.cos(t) * 13, 40 + math.sin(t) * 13) for t in np.linspace(0.2, 6.6, 26)], 1.5)
    for k in range(10):
        a = k / 10 * 2 * math.pi + s.rng.uniform(-0.08, 0.08)
        s.stroke([(40 + math.cos(a) * 19, 40 + math.sin(a) * 19), (40 + math.cos(a) * 29, 40 + math.sin(a) * 29)], 1.4)
    s.save("sun", 0)


def smiley(seed):
    s = Sheet(60, 60, seed)
    s.stroke([(30 + math.cos(t) * 20, 30 + math.sin(t) * 19) for t in np.linspace(-1.4, 4.95, 30)], 1.5)
    s.stroke([(23, 24), (23, 26)], 2.0)
    s.stroke([(37, 24), (37, 26)], 2.0)
    s.stroke([(20 + i * 1.0, 35 + math.sin(i / 20 * math.pi) * 6) for i in range(21)], 1.5)
    s.save("smiley", 6)


def lightning(seed):
    s = Sheet(50, 80, seed)
    s.stroke([(30, 6), (14, 38), (26, 38), (16, 72), (38, 30), (25, 30), (34, 6), (30, 6)], 1.5)
    s.save("lightning", 0)


def arrow_curve(seed):
    s = Sheet(150, 70, seed)
    x0, y0, x1, y1 = 8, 58, 136, 14
    cx, cy = 60, 8
    pts = [((1 - t) ** 2 * x0 + 2 * (1 - t) * t * cx + t * t * x1,
            (1 - t) ** 2 * y0 + 2 * (1 - t) * t * cy + t * t * y1) for t in np.linspace(0, 1, 40)]
    s.stroke(pts, 1.6, RED_PENCIL)
    ang = math.atan2(y1 - pts[-4][1], x1 - pts[-4][0])
    for da in (2.6, -2.6):
        s.stroke([(x1, y1), (x1 + math.cos(ang + da) * 11, y1 + math.sin(ang + da) * 11)], 1.6, RED_PENCIL)
    s.save("arrow_curve", 0)


def coffee_ring(seed):
    size = 160
    rng = np.random.default_rng(seed)
    Y, X = np.mgrid[0:size, 0:size].astype(np.float32)
    ang = np.arctan2(Y - size / 2, X - size / 2)
    # the cup sat slightly tilted: thicker on one side, fading out on the other
    wob = 1 + 0.025 * np.sin(ang * 3 + 1) + 0.015 * np.sin(ang * 7)
    r = np.hypot(X - size / 2, Y - size / 2) / (size * 0.40) / wob
    noise = np.asarray(Image.fromarray((rng.random((size // 5, size // 5)) * 255).astype(np.uint8))
                       .resize((size, size), Image.BICUBIC), np.float32) / 255
    thick = 0.03 + 0.02 * (0.5 + 0.5 * np.sin(ang + 0.8))
    fade = np.clip(0.35 + 0.65 * (0.5 + 0.5 * np.cos(ang - 2.4)) + 0.2 * (noise - 0.5), 0, 1)
    ring = np.exp(-((r - 1) / thick) ** 2) * 0.55 * fade + np.clip(1 - r, 0, 1) * 0.045 * noise
    ring += np.exp(-(((X - size * 0.86) / 4) ** 2 + ((Y - size * 0.7) / 3.5) ** 2)) * 0.4
    img = np.zeros((size, size, 4), np.uint8)
    img[..., :3] = (122, 80, 40)
    img[..., 3] = np.clip(ring * 255, 0, 255).astype(np.uint8)
    save_webp(Image.fromarray(img, "RGBA"), OUT / "coffee_ring.webp", lossless=True)


# ---------------------------------------------------------------- short words

def word(name, font, text, size, color, seed, tilt, underline=0, circle=False, extra=None):
    s = Sheet(int(size * len(text) * 0.9) + 60, int(size * 2.6) + 30, seed)
    x0, y0 = 16, 16
    x1 = s.write(font, text, x0, y0, size, color)
    if underline:
        for k in range(underline):
            yy = y0 + size * 1.25 + k * 5
            s.stroke([(x0 - 2, yy + s.rng.uniform(-1, 1)), (x1 + 2, yy + s.rng.uniform(-1.5, 0.5))], 1.4, color)
    if circle:
        cx, cy = (x0 + x1) / 2, y0 + size * 0.55
        rx, ry = (x1 - x0) / 2 + 12, size * 0.95
        s.stroke([(cx + math.cos(t) * rx * (1 + 0.05 * i / 100), cy + math.sin(t) * ry * (1 + 0.06 * i / 100))
                  for i, t in ((i, i / 100 * 2.3 * math.pi - 0.6) for i in range(100))], 1.6, RED_PENCIL, alpha=190)
    if extra:
        extra(s, x1, y0)
    s.save(name, tilt)


# ---------------------------------------------------------------- runtime lettering

GLYPH_CHARS = (string.ascii_letters + string.digits + ".,!?'-:;&()/+=#%*\"")
GLYPH_VARIANTS = 3
GLYPH_CAP = 22          # cap height the glyphs are drawn at; Ren'Py zooms from there
GLYPH_H = 46            # every glyph image has the same height: rows line up
GLYPH_ORIGIN_X = 9      # pen position inside the image (room for the slant)
WHITE = (255, 255, 255)


def glyphs(font):
    """
    Every character in GLYPH_VARIANTS hand-drawn variants, in white so Ren'Py can
    tint them (pencil grey, red pencil). journal_doodles.rpy composes words from
    them at runtime; metrics.json holds each character's advance.
    """

    scale = GLYPH_CAP / 21.0
    # Hershey y runs about -16..16 with the baseline at 9
    to_y = lambda hy: 5 + (hy + 16) * scale
    metrics = {"cap": GLYPH_CAP, "height": GLYPH_H, "origin_x": GLYPH_ORIGIN_X,
               "baseline": round(to_y(9), 1), "advance": {}}
    out = OUT / "glyphs"
    for ch in " " + GLYPH_CHARS:
        left, right, strokes = font[ch]
        advance = (right - left) * scale
        metrics["advance"][str(ord(ch))] = round(advance, 1)
        if ch == " ":
            continue
        for v in range(GLYPH_VARIANTS):
            s = Sheet(int(advance) + GLYPH_ORIGIN_X * 2 + 6, GLYPH_H, 1000 + ord(ch) * 7 + v)
            rng = s.rng
            gs = rng.uniform(0.94, 1.06)
            slant = 0.3 + rng.uniform(-0.07, 0.07)
            for st in strokes:
                ph = rng.random() * 6.28
                pts = []
                for k, (px, py) in enumerate(st):
                    nx = math.sin(k * 0.7 + ph) * 0.5
                    ny = math.cos(k * 0.55 + ph) * 0.5
                    x = GLYPH_ORIGIN_X + (px - left) * scale * gs - (py - 9) * scale * slant + nx
                    pts.append((x, to_y(9) + (py - 9) * scale * gs + ny))
                s.stroke(pts, 1.7, WHITE, alpha=225, jitter=0.3)
            img = s.img.resize((s.w, s.h), Image.LANCZOS)
            save_webp(img, out / f"{ord(ch)}_{v}.webp", lossless=True)
    (out / "metrics.json").write_text(json.dumps(metrics, indent=1), encoding="utf-8")


def arrows():
    """
    Short curved pencil arrows (white, tinted in Ren'Py) for notes that point at
    something: right / left and the four diagonals, two variants each.
    """

    for v in range(2):
        s = Sheet(110, 60, 2000 + v)
        x0, y0, x1, y1 = 8, 34 + v * 4, 96, 30
        cx, cy = 50, 12 + v * 10
        pts = [((1 - t) ** 2 * x0 + 2 * (1 - t) * t * cx + t * t * x1,
                (1 - t) ** 2 * y0 + 2 * (1 - t) * t * cy + t * t * y1) for t in np.linspace(0, 1, 36)]
        s.stroke(pts, 1.7, WHITE, alpha=225)
        ang = math.atan2(y1 - pts[-5][1], x1 - pts[-5][0])
        for da in (2.6, -2.6):
            s.stroke([(x1, y1), (x1 + math.cos(ang + da) * 11, y1 + math.sin(ang + da) * 11)], 1.7, WHITE, alpha=225)
        right = s.img.resize((s.w, s.h), Image.LANCZOS)
        turns = {
            "right": right,
            "left": right.transpose(Image.FLIP_LEFT_RIGHT),
            "down_right": right.rotate(-35, resample=Image.BICUBIC, expand=True),
            "up_right": right.rotate(35, resample=Image.BICUBIC, expand=True),
        }
        turns["down_left"] = turns["down_right"].transpose(Image.FLIP_LEFT_RIGHT)
        turns["up_left"] = turns["up_right"].transpose(Image.FLIP_LEFT_RIGHT)
        for name, img in turns.items():
            save_webp(img.crop(img.getbbox()), OUT / "arrows" / f"{name}_{v}.webp", lossless=True)


def build():
    font = load_jhf(HERSHEY_SIMPLEX)
    glyphs(font)
    arrows()
    coffee_ring(3)
    star("star", 16, PENCIL, 11, 8)
    star("star_red", 12, RED_PENCIL, 12, -10)
    stars_trio(13)
    spiral(14)
    heart("heart_red", 18, RED_PENCIL, 15, -8)
    heart("heart_hatched", 14, RED_PENCIL, 16, 10, filled_hatch=True)
    cube(17)
    flask(18)
    tally(19)
    tictactoe(20)
    paper_plane(21)
    sun(22)
    smiley(23)
    lightning(24)
    arrow_curve(25)
    word("word_wow", font, "wow!", 22, RED_PENCIL, 30, -6, underline=2)
    word("word_qqq", font, "???", 22, PENCIL, 31, 4)
    word("word_excl", font, "!!", 24, RED_PENCIL, 32, 6)
    word("word_shh", font, "shh!", 20, RED_PENCIL, 33, -5, underline=1)
    word("word_ok", font, "ok", 20, PENCIL, 34, -3, circle=True)
    word("word_coffee", font, "coffee", 19, PENCIL, 35, -4, underline=1)
    word("word_fri", font, "Fri!", 20, RED_PENCIL, 36, 5, underline=2)


if __name__ == "__main__":
    ensure_sources()
    build()
