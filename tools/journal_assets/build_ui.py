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
  dialog_band(_50)          leather dialogue box (100% / 50% textbox setting)
  dialog_name               anthracite ribbon name tag for the dialogue box (Frame)
  title_plaque              main menu logo: leather patch with an engraved brass plaque
  choice_slip               paper strip for one choice of a menu (Frame)
  sticker_blank             round paper sticker for the main menu's link icons
  leather_patch             stitched leather patch: map HUD straps, quick menu, skip indicator (tiled Frame)
  quick_<name>_<state>      quick menu icons blind-stamped into the patch (idle / hover / active)
  (render_template          tools/journal_assets/main_menu_render_template.png, not shipped)

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


def dialog_band():
    """
    The dialogue box: a band of the binder's leather (darker and warmer so
    cream text reads at full strength) with an ink edge and the binder's
    stitching along the top. Two strengths for the textbox transparency
    setting (100% / 50%); the 0% setting shows no box. Used as a Frame in
    Ren'Py, so the top (edge + seam) stays put when the box is taller.
    """

    from sources import LEATHER

    w, h = 1920, 278
    tex = Image.open(LEATHER).convert("L").resize((2048, 2048), Image.LANCZOS).crop((0, 600, w, 600 + h))
    lum = np.asarray(tex, np.float32)[..., None] / 255
    tint = np.array([0.42, 0.27, 0.17], np.float32)
    rgb = np.clip(tint * (0.55 + 0.9 * lum), 0, 1)
    rgb *= (0.82 + 0.18 * np.linspace(0, 1, h, dtype=np.float32))[:, None, None]
    for name, body_alpha, seam_alpha in (("dialog_band", 1.0, 1.0), ("dialog_band_50", 0.62, 0.85)):
        img = Image.fromarray((rgb * 255).astype(np.uint8), "RGB").convert("RGBA")
        img.putalpha(int(255 * body_alpha))
        top = Sheet(w, 24)
        top.line(0, 1.6, w, 1.4, 3.0, (30, 18, 10), 71, amp=0.3, alpha=int(250 * seam_alpha))
        x = 20
        k = 0
        while x < w - 20:
            top.line(x, 16, x + 14, 16.2, 1.8, (238, 222, 190), 80 + k, amp=0.2, alpha=int(220 * seam_alpha))
            x += 26
            k += 1
        img.alpha_composite(top.out(), (0, 0))
        save_webp(img, OUT / f"{name}.webp")


def dialog_name():
    """
    The speaker's name tag: a dark anthracite grosgrain ribbon with a notch at
    its end, stretched sideways as a Frame (left 16px / right 34px fixed).
    Anthracite carries every speaker colour, the headmaster's white included.
    """

    w, h = 200, 54
    img = Image.new("RGBA", (w * SS, (h + 8) * SS), (0, 0, 0, 0))
    poly = [(0, 0), (w, 0), (w - 18, h / 2), (w, h), (0, h)]
    sh = Image.new("L", img.size, 0)
    ImageDraw.Draw(sh).polygon([((x + 2) * SS, (y + 4) * SS) for x, y in poly], fill=130)
    shadow = Image.new("RGBA", img.size, (10, 6, 4, 0))
    shadow.putalpha(sh.filter(ImageFilter.GaussianBlur(2.5 * SS)))
    img.alpha_composite(shadow)
    body = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(body)
    d.polygon([(x * SS, y * SS) for x, y in poly], fill=(46, 40, 38, 255))
    for x in range(0, w * SS, 3 * SS):
        d.line((x, 2 * SS, x, (h - 2) * SS), fill=(255, 255, 255, 12), width=SS)
    d.line((0, 6 * SS, (w - 6) * SS, 6 * SS), fill=(255, 255, 255, 34), width=2 * SS)
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).polygon([(x * SS, y * SS) for x, y in poly], fill=255)
    body.putalpha(Image.fromarray(np.minimum(np.asarray(body.split()[3]), np.asarray(mask))))
    img.alpha_composite(body)
    s = Sheet(w, h + 8)
    for (x0, y0), (x1, y1) in zip(poly, poly[1:] + poly[:1]):
        s.line(x0, y0, x1, y1, 2.0, (20, 14, 10), int(x0 + y0 * 7), amp=0.3, alpha=240)
    img.alpha_composite(s.img)
    save_webp(img.resize((w, h + 8), Image.LANCZOS), OUT / "dialog_name.webp", lossless=True)


def choice_slip():
    """
    One choice of a menu: a strip of the journal's loose paper with a soft
    shadow, used as a Frame (12px borders keep the shadow and the torn edge).
    """

    from sources import PAPER

    w, h = 420, 76
    paper = Image.open(PAPER).convert("L").transpose(Image.ROTATE_90).crop((200, 300, 200 + w * 2, 300 + h * 2))
    paper = paper.resize((w, h), Image.LANCZOS)
    detail = np.asarray(paper, np.float32)
    detail -= np.asarray(paper.filter(ImageFilter.GaussianBlur(20)), np.float32)
    detail = (detail - detail.mean()) / (detail.std() + 1e-6)
    base = np.array([248, 242, 229], np.float32)
    rgb = np.clip(base[None, None, :] * (1.0 - 0.02 * detail[..., None]), 0, 255)
    body = Image.fromarray(rgb.astype(np.uint8), "RGB").convert("RGBA")
    # slightly uneven edges, like a strip torn off a pad
    mask = Image.new("L", (w * SS, h * SS), 0)
    rng = random.Random(77)
    pts = []
    for x in range(0, w + 1, 6):
        pts.append((x * SS, (5 + rng.uniform(-1.2, 1.2)) * SS))
    for x in range(w, -1, -6):
        pts.append((x * SS, (h - 9 + rng.uniform(-1.2, 1.2)) * SS))
    ImageDraw.Draw(mask).polygon(pts, fill=255)
    mask = mask.resize((w, h), Image.LANCZOS)
    body.putalpha(mask)
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    shadow = Image.new("RGBA", (w, h), (14, 8, 4, 0))
    shadow.putalpha(mask.filter(ImageFilter.GaussianBlur(3)).point(lambda v: int(v * 0.42)))
    out.alpha_composite(shadow, (3, 4))
    out.alpha_composite(body)
    save_webp(out, OUT / "choice_slip.webp")


def title_plaque():
    """
    Main-menu logo: a stitched leather patch with a screwed-on brushed brass
    plaque, "Mind the School" engraved. The version is left out on purpose:
    Ren'Py engraves it at runtime in the empty band under the title (x centre,
    y 122 in this image), so a release never needs a new image.
    """

    from sources import LEATHER
    from PIL import ImageChops, ImageFont
    from sources import GAME_FONTS

    w, h = 580, 190
    tex = Image.open(LEATHER).convert("L").resize((1400, 1400), Image.LANCZOS).crop((200, 300, 200 + w, 300 + h))
    lum = np.asarray(tex, np.float32)[..., None] / 255
    rgb = np.clip(np.array([0.36, 0.2, 0.12], np.float32) * (0.6 + 0.8 * lum), 0, 1)
    img = Image.fromarray((rgb * 255).astype(np.uint8), "RGB").convert("RGBA")
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, w - 1, h - 1), 18, fill=255)
    img.putalpha(mask)
    seam = Sheet(w, h)
    k = 0
    for x in range(26, w - 26, 18):
        for y in (12, h - 13):
            seam.line(x, y, x + 10, y + 0.2, 1.8, (228, 206, 160), 300 + k, amp=0.2, alpha=200)
            k += 1
    for y in range(26, h - 26, 18):
        for x in (12, w - 13):
            seam.line(x, y, x + 0.2, y + 10, 1.8, (228, 206, 160), 300 + k, amp=0.2, alpha=200)
            k += 1
    img.alpha_composite(seam.out())

    pw, ph = 470, 112
    px, py = (w - pw) // 2, 30
    rng = np.random.default_rng(9)
    Y = np.linspace(0, 1, ph, dtype=np.float32)[:, None]
    shade = np.clip(0.78 + 0.16 * np.cos((Y - 0.35) * 5.5) + rng.normal(0, 0.035, (1, pw)).repeat(ph, 0), 0, 1.1)
    metal = np.stack([shade * 0.93, shade * 0.74, shade * 0.38], -1)
    plaque = Image.fromarray((np.clip(metal, 0, 1) * 255).astype(np.uint8), "RGB").convert("RGBA")
    pm = Image.new("L", (pw, ph), 0)
    ImageDraw.Draw(pm).rounded_rectangle((0, 0, pw - 1, ph - 1), 10, fill=255)
    plaque.putalpha(pm)
    pd = ImageDraw.Draw(plaque)
    pd.rounded_rectangle((1, 1, pw - 2, ph - 2), 10, outline=(255, 236, 170, 200), width=2)
    pd.rounded_rectangle((4, 4, pw - 5, ph - 5), 8, outline=(110, 72, 24, 160), width=2)
    font = ImageFont.truetype(str(GAME_FONTS / "CrimsonPro-SemiBold.ttf"), 58)
    eng = Image.new("L", (pw, ph), 0)
    ImageDraw.Draw(eng).text((pw / 2, 46), "Mind the School", font=font, fill=255, anchor="mm")
    plaque.alpha_composite(Image.merge("RGBA", [Image.new("L", (pw, ph), 255)] * 3 + [ImageChops.offset(eng, 0, 2).point(lambda v: int(v * 0.45))]))
    plaque.alpha_composite(Image.merge("RGBA", [Image.new("L", (pw, ph), 70), Image.new("L", (pw, ph), 44),
                                                Image.new("L", (pw, ph), 14), eng.point(lambda v: int(v * 0.92))]))
    for sx, sy in ((14, 14), (pw - 15, 14), (14, ph - 15), (pw - 15, ph - 15)):
        pd.ellipse((sx - 6, sy - 6, sx + 6, sy + 6), fill=(150, 112, 50, 255), outline=(90, 60, 20, 255))
        pd.line((sx - 4, sy + 2, sx + 4, sy - 2), fill=(80, 52, 18, 255), width=2)
    sh = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
    sh.putalpha(pm.point(lambda v: int(v * 0.5)))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(4)), (px + 3, py + 5))
    img.alpha_composite(plaque, (px, py))
    small = ImageFont.truetype(str(GAME_FONTS / "CrimsonPro-Medium.ttf"), 18)
    ImageDraw.Draw(img).text((w / 2, h - 34), "est. 2023", font=small, fill=(228, 206, 160, 170), anchor="mm")

    pad = 24
    out = Image.new("RGBA", (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
    drop = Image.new("RGBA", (w, h), (12, 8, 4, 0))
    drop.putalpha(img.split()[3].point(lambda v: int(v * 110 / 255)))
    out.alpha_composite(drop.filter(ImageFilter.GaussianBlur(6)), (pad + 5, pad + 7))
    out.alpha_composite(img, (pad, pad))
    save_webp(out, OUT / "title_plaque.webp")


def sticker_blank():
    # round paper sticker for the main menu's link icons (Wiki, Discord, Patreon)
    w = h = 92
    img = Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0))
    sh = Image.new("L", img.size, 0)
    ImageDraw.Draw(sh).ellipse((8 * SS, 10 * SS, 88 * SS, 90 * SS), fill=150)
    shadow = Image.new("RGBA", img.size, (20, 12, 6, 0))
    shadow.putalpha(sh.filter(ImageFilter.GaussianBlur(3 * SS)))
    img.alpha_composite(shadow)
    ImageDraw.Draw(img).ellipse((4 * SS, 4 * SS, 84 * SS, 84 * SS), fill=(250, 244, 230, 255),
                                outline=(180, 168, 148, 255), width=SS)
    save_webp(img.resize((w, h), Image.LANCZOS), OUT / "sticker_blank.webp", lossless=True)


def render_template():
    """
    Guide for rendering main-menu backgrounds: 1920x1080, transparent, with the
    three zones the menu covers (book, notes, plaque) tinted. Lay it over the
    camera preview; keep the subject out of the tinted areas. Not shipped.
    """

    from PIL import ImageFont
    from sources import GAME_FONTS

    here = Path(__file__).resolve().parent
    w, h = 1920, 1080
    font = ImageFont.truetype(str(GAME_FONTS / "CrimsonPro-SemiBold.ttf"), 30)
    small = ImageFont.truetype(str(GAME_FONTS / "CrimsonPro-Regular.ttf"), 22)

    # 1) zones: keep the subject out of the red areas (positions as in journal_title.rpy)
    zones = [
        ((0, 0, 470, h), "MENU BOOK", "book page + 3 ribbons on its edge"),
        ((1140, 0, w, 315), "NOTES", "news slip, link stickers, changelog"),
        ((1290, 838, w, h), "LOGO", "brass plaque"),
    ]
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for (x0, y0, x1, y1), title, note in zones:
        d.rectangle((x0, y0, x1 - 1, y1 - 1), fill=(220, 40, 40, 60), outline=(255, 60, 60, 230), width=4)
        d.text((x0 + 18, y0 + 14), title, font=font, fill=(255, 255, 255, 240), stroke_width=2, stroke_fill=(0, 0, 0, 200))
        d.text((x0 + 18, y0 + 50), note, font=small, fill=(255, 255, 255, 220), stroke_width=2, stroke_fill=(0, 0, 0, 200))
    # the chalkboard-style safe area: the middle stays free for the subject
    d.text((w / 2, h - 30), "subject area: everything outside the red zones", font=small, fill=(255, 255, 255, 200),
           anchor="mm", stroke_width=2, stroke_fill=(0, 0, 0, 200))
    img.save(here / "main_menu_render_template.png")

    # 2) ghost: the real menu pieces at their exact positions, half transparent
    gui = OUT.parent
    ghost = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    book = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    book.alpha_composite(Image.open(gui / "book_cover.webp").convert("RGBA"))
    for name, y in (("title_anim_pause", 752), ("title_bg_next", 842), ("title_bg_grid", 932)):
        book.alpha_composite(Image.open(gui / "ribbons" / f"{name}_idle.webp").convert("RGBA"), (1620 - 14, y - 44))
    book.alpha_composite(Image.open(gui / "book_pages.webp").convert("RGBA"))
    ghost.alpha_composite(book.crop((1290, 0, w, h)), (0, 10))
    note = Image.open(OUT / "foldout_panel.webp").convert("RGBA").resize((480, 120))
    ghost.alpha_composite(note, (1150, 22))
    for i in range(3):
        ghost.alpha_composite(Image.open(OUT / "sticker_blank.webp").convert("RGBA"), (1652 + i * 86, 18))
    packet = Image.open(OUT / "foldout_panel.webp").convert("RGBA").resize((170, 140))
    for i in (2, 1, 0):
        ghost.alpha_composite(packet, (1660 + i * 6, 130 + i * 5))
    ghost.alpha_composite(Image.open(OUT / "title_plaque.webp").convert("RGBA"), (1290, 838))
    alpha = ghost.split()[3].point(lambda v: int(v * 0.55))
    ghost.putalpha(alpha)
    ghost.save(here / "main_menu_render_ghost.png")

    # 3) the same two guides for a 3440x1440 studio viewport: the 16:9 frame
    # scaled to the full height and centred, the parts the game never shows dimmed
    for name, guide in (("template", img), ("ghost", ghost)):
        monitor_overlay(guide, 3440, 1440).save(here / f"main_menu_render_{name}_3440x1440.png")


def monitor_overlay(guide, screen_w, screen_h):
    """
    Fits a 16:9 render guide to a wider monitor so it can sit over a fullscreen
    camera preview: scaled to the screen height, centred, with the side strips
    outside the game frame darkened and the frame edge drawn in.
    """

    frame_w = round(screen_h * guide.width / guide.height)
    left = (screen_w - frame_w) // 2
    out = Image.new("RGBA", (screen_w, screen_h), (0, 0, 0, 0))
    d = ImageDraw.Draw(out)
    d.rectangle((0, 0, left - 1, screen_h - 1), fill=(0, 0, 0, 150))
    d.rectangle((left + frame_w, 0, screen_w - 1, screen_h - 1), fill=(0, 0, 0, 150))
    out.alpha_composite(guide.resize((frame_w, screen_h), Image.LANCZOS), (left, 0))
    d.line((left - 2, 0, left - 2, screen_h), fill=(255, 255, 255, 200), width=3)
    d.line((left + frame_w + 1, 0, left + frame_w + 1, screen_h), fill=(255, 255, 255, 200), width=3)
    return out


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


def leather_patch():
    """
    A stitched patch of the binder's leather with rounded corners: the map
    HUD straps and the quick menu in the corner of the dialogue box. Used as a
    tiled Frame (20px borders); the middle is a whole number of stitch periods
    (12px) both ways, so the stitching stays even at any size.
    """

    from sources import LEATHER

    w, h, r, period = 640, 196, 12, 12
    tex = Image.open(LEATHER).convert("L").resize((2048, 2048), Image.LANCZOS).crop((300, 900, 300 + w, 900 + h))
    lum = np.asarray(tex, np.float32)[..., None] / 255
    tint = np.array([0.36, 0.23, 0.15], np.float32)
    rgb = np.clip(tint * (0.55 + 0.9 * lum), 0, 1)
    body = Image.fromarray((rgb * 255).astype(np.uint8), "RGB").convert("RGBA")

    mask = Image.new("L", (w * SS, h * SS), 0)
    ImageDraw.Draw(mask).rounded_rectangle((3 * SS, 2 * SS, (w - 4) * SS, (h - 6) * SS), r * SS, fill=255)
    mask = mask.resize((w, h), Image.LANCZOS)
    body.putalpha(mask)

    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    shadow = Image.new("RGBA", (w, h), (10, 6, 3, 0))
    shadow.putalpha(mask.filter(ImageFilter.GaussianBlur(3)).point(lambda v: int(v * 0.55)))
    out.alpha_composite(shadow, (1, 3))
    out.alpha_composite(body)

    s = Sheet(w, h)
    s.d.rounded_rectangle((3 * SS, 2 * SS, (w - 4) * SS, (h - 6) * SS), r * SS, outline=(24, 14, 8, 235), width=2 * SS)
    # stitches 9px inside the edge; they start at the 20px border so the tiled middle repeats cleanly
    inset, k = 9.5, 0
    for x in range(20, w - 20, period):
        s.line(x + 2, inset, x + 9, inset + 0.1, 1.6, (232, 214, 180), 300 + k, amp=0.15, alpha=200)
        s.line(x + 2, h - 6 - inset, x + 9, h - 6 - inset + 0.1, 1.6, (232, 214, 180), 500 + k, amp=0.15, alpha=200)
        k += 1
    for y in range(20, h - 20, period):
        s.line(inset + 1.5, y + 2, inset + 1.6, y + 9, 1.6, (232, 214, 180), 700 + k, amp=0.15, alpha=200)
        s.line(w - 4 - inset - 1, y + 2, w - 4 - inset - 0.9, y + 9, 1.6, (232, 214, 180), 900 + k, amp=0.15, alpha=200)
        k += 1
    out.alpha_composite(s.out())
    save_webp(out, OUT / "leather_patch.webp")


QUICK_ICONS = {
    "back": 0xe166,      # undo
    "history": 0xe889,   # history
    "skip": 0xe01f,      # fast_forward
    "auto": 0xe1c4,      # play_circle
    "save": 0xe161,      # save
    "qsave": 0xe598,     # bookmark_add
    "qload": 0xe866,     # bookmark
    "prefs": 0xe8b8,     # settings
    "hide": 0xe8f5,      # visibility_off
    "menu": 0xea19,      # menu_book
    "end": 0xef71,       # stop_circle
}


SCENE_ICONS = {
    "scene_clothing": 0xf19e,  # checkroom
    "scene_position": 0xe92c,  # accessibility_new
    "scene_location": 0xe55f,  # place
    "scene_variant": 0xe043,   # shuffle
    "scene_finish": 0xe153,    # flag
    "scene_return": 0xe5c4,    # arrow_back
    "scene_stop": 0xe9ba,      # logout
}
QUICK_ICONS.update(SCENE_ICONS)


def calendar_sheet():
    """
    The date card between days: one sheet of a tear-off desk calendar, a
    deep red header band (month and year are set on it at runtime), cream
    paper below with the perforation along the top edge, two binder rings.
    """

    from sources import PAPER

    w, h, head = 440, 520, 96
    paper = Image.open(PAPER).convert("L").transpose(Image.ROTATE_90).crop((150, 200, 150 + w * 2, 200 + h * 2))
    paper = paper.resize((w, h), Image.LANCZOS)
    detail = np.asarray(paper, np.float32)
    detail -= np.asarray(paper.filter(ImageFilter.GaussianBlur(20)), np.float32)
    detail = (detail - detail.mean()) / (detail.std() + 1e-6)
    base = np.array([249, 244, 231], np.float32)
    rgb = np.clip(base[None, None, :] * (1.0 - 0.022 * detail[..., None]), 0, 255)
    red = np.array([128, 34, 30], np.float32)
    rgb[:head] = np.clip(red[None, None, :] * (1.0 - 0.05 * detail[:head, :, None]), 0, 255)
    body = Image.fromarray(rgb.astype(np.uint8), "RGB").convert("RGBA")

    # perforation: tiny holes just under the header, the edge the sheet was torn along
    d = ImageDraw.Draw(body)
    for x in range(10, w - 6, 9):
        d.ellipse((x, head + 5, x + 3, head + 8), fill=(196, 184, 160, 255))
    d.line((0, head, w, head), fill=(80, 20, 16, 255), width=2)

    mask = Image.new("L", (w * SS, h * SS), 0)
    rng = random.Random(23)
    pts = [(0, 0), (w * SS, 0)]
    # the bottom edge is slightly ragged: the next sheet was torn off below it
    for x in range(w, -1, -5):
        pts.append((x * SS, (h - 4 + rng.uniform(-2.2, 2.2)) * SS))
    ImageDraw.Draw(mask).polygon(pts, fill=255)
    mask = mask.resize((w, h), Image.LANCZOS)
    body.putalpha(mask)

    pad = 30
    out = Image.new("RGBA", (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
    shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    shadow.putalpha(mask.point(lambda v: int(v * 0.6)))
    out.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(9)), (pad + 6, pad + 10))
    out.alpha_composite(body, (pad, pad))

    # two binder rings through the header
    s = Sheet(w + pad * 2, h + pad * 2)
    for cx in (pad + w * 0.3, pad + w * 0.7):
        s.d.ellipse(((cx - 9) * SS, (pad + 22) * SS, (cx + 9) * SS, (pad + 34) * SS), fill=(26, 10, 8, 255))
        s.d.arc(((cx - 11) * SS, (pad - 22) * SS, (cx + 11) * SS, (pad + 32) * SS), 180, 360,
                fill=(170, 166, 158, 255), width=5 * SS)
        s.d.arc(((cx - 10) * SS, (pad - 21) * SS, (cx + 10) * SS, (pad + 31) * SS), 200, 300,
                fill=(236, 234, 226, 255), width=2 * SS)
    out.alpha_composite(s.out())
    save_webp(out, OUT / "calendar_sheet.webp")


def quick_icons():
    """
    Quick menu icons, blind-stamped into the leather patch: cream with a dark
    lower-right edge (idle), brass (hover), brass and filled (active, e.g.
    auto-forward running). Material Symbols, like the ribbons.
    """

    from PIL import ImageFont
    from sources import ICON_FONT

    size = 48
    for name, cp in QUICK_ICONS.items():
        for state, colour, fill in (("idle", (236, 222, 194), 0), ("hover", (228, 190, 112), 0),
                                    ("active", (228, 190, 112), 1)):
            font = ImageFont.truetype(str(ICON_FONT), 38 * SS)
            font.set_variation_by_axes([fill, 0, 40, 500])
            glyph = Image.new("L", (size * SS, size * SS), 0)
            gd = ImageDraw.Draw(glyph)
            bb = gd.textbbox((0, 0), chr(cp), font=font)
            gd.text(((size * SS - bb[0] - bb[2]) / 2, (size * SS - bb[1] - bb[3]) / 2), chr(cp), font=font, fill=255)
            glyph = glyph.resize((size, size), Image.LANCZOS)
            img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
            dark = Image.new("RGBA", (size, size), (12, 6, 2, 0))
            dark.putalpha(glyph.point(lambda v: int(v * 0.8)))
            img.alpha_composite(dark, (1, 1))
            face = Image.new("RGBA", (size, size), colour + (0,))
            face.putalpha(glyph.point(lambda v: int(v * (0.88 if state == "idle" else 1.0))))
            img.alpha_composite(face)
            save_webp(img, OUT / f"quick_{name}_{state}.webp", lossless=True)


# collectible polaroids lying in the locations: (style, shape, frame colour, extra)
COLLECTIBLE_POLAROIDS = [
    ("classic_white", "classic", (247, 245, 238), None),
    ("classic_cream", "classic", (236, 225, 199), None),
    ("classic_faded", "classic", (222, 207, 170), "faded"),
    ("classic_black", "classic", (40, 38, 36), None),
    ("instax_mint", "instax", (178, 222, 205), None),
    ("instax_pink", "instax", (238, 194, 204), None),
    ("instax_sky", "instax", (186, 211, 235), None),
    ("taped", "classic", (247, 245, 238), "tape"),
    ("dog_eared", "classic", (247, 245, 238), "corner"),
]


def collectible_polaroids():
    """
    Small polaroids for the collectibles hidden on location backgrounds
    (gui/journal/collectibles/polaroid_<style>.webp). Kept small and muted so
    they are easy to miss; the photo area is a generic glossy print, never the
    collectible itself. A 6px pad around the frame holds the soft shadow.
    """

    pad = 6
    shapes = {
        # frame size, photo box (x0, y0, x1, y1)
        "classic": ((58, 70), (5, 5, 53, 53)),
        "instax": ((48, 76), (4, 6, 44, 60)),
    }
    out = GUI_OUT / "collectibles"
    for style, shape, frame, extra in COLLECTIBLE_POLAROIDS:
        (fw, fh), (px0, py0, px1, py1) = shapes[shape]
        w, h = fw + pad * 2, fh + pad * 2
        img = Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0))

        shadow = Image.new("L", img.size, 0)
        ImageDraw.Draw(shadow).rectangle(((pad + 1) * SS, (pad + 2) * SS, (pad + fw + 1) * SS, (pad + fh + 2) * SS), fill=110)
        shadow_img = Image.new("RGBA", img.size, (20, 14, 8, 0))
        shadow_img.putalpha(shadow.filter(ImageFilter.GaussianBlur(2.2 * SS)))
        img.alpha_composite(shadow_img)

        d = ImageDraw.Draw(img)
        d.rectangle((pad * SS, pad * SS, (pad + fw) * SS - 1, (pad + fh) * SS - 1), fill=frame + (255,))

        # the print: dusk-blue into warm light with grain and a diagonal gloss
        pw, ph = (px1 - px0) * SS, (py1 - py0) * SS
        yy, xx = np.mgrid[0:ph, 0:pw]
        t = (yy / ph * 0.7 + xx / pw * 0.3)
        top, bottom = np.array([58, 70, 92]), np.array([176, 136, 92])
        if extra == "faded":
            top, bottom = np.array([120, 118, 112]), np.array([196, 172, 132])
        rgb = top * (1 - t[..., None]) + bottom * t[..., None]
        rng = np.random.default_rng(len(style))
        rgb += rng.normal(0, 6, rgb.shape)
        gloss = np.clip(1 - np.abs((xx / pw - yy / ph * 0.8) - 0.25) * 6, 0, 1) * 26
        rgb += gloss[..., None]
        photo = Image.fromarray(np.clip(rgb, 0, 255).astype("uint8"), "RGB").convert("RGBA")
        img.alpha_composite(photo, ((pad + px0) * SS, (pad + py0) * SS))

        if extra == "tape":
            tape = Image.new("RGBA", (26 * SS, 9 * SS), (236, 228, 196, 150))
            tape = tape.rotate(-8, expand=True, resample=Image.BICUBIC)
            img.alpha_composite(tape, ((pad + fw // 2 - 14) * SS, (pad - 4) * SS))
        if extra == "corner":
            c = 11
            x1, y1 = (pad + fw) * SS, (pad + fh) * SS
            # cut the corner away and lay the folded flap over it
            d.polygon([(x1 - c * SS, y1), (x1, y1 - c * SS), (x1, y1), (x1 - c * SS, y1)], fill=(0, 0, 0, 0))
            img.putpixel((0, 0), (0, 0, 0, 0))
            mask = Image.new("L", img.size, 255)
            ImageDraw.Draw(mask).polygon([(x1 - c * SS, y1), (x1, y1 - c * SS), (x1 + SS, y1 + SS)], fill=0)
            img.putalpha(Image.fromarray(np.minimum(np.asarray(img.split()[3]), np.asarray(mask))))
            d = ImageDraw.Draw(img)
            d.polygon([(x1 - c * SS, y1), (x1, y1 - c * SS), (x1 - c * SS, y1 - c * SS)], fill=tuple(int(v * 0.86) for v in frame) + (255,))

        save_webp(img.resize((w, h), Image.LANCZOS), out / f"polaroid_{style}.webp", lossless=True)


if __name__ == "__main__":
    ensure_sources()
    collectible_polaroids()
    leather_patch()
    quick_icons()
    calendar_sheet()
    choice_slip()
    title_plaque()
    sticker_blank()
    render_template()
    dialog_band()
    dialog_name()
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
