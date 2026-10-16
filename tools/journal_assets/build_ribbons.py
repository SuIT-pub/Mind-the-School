"""
Ribbon bookmarks for the journal navigation (game/gui/journal/ribbons/).

Three groups:
  side ribbons  left = content pages, right = meta pages; icon baked in,
                exported pointing left (<key>_<state>_l) and right (<key>_<state>_r)
  sub ribbons   top edge, sub pages of the current section; exported BLANK
                (sub_<key>_<state>) because their label is set by Ren'Py
  stubs         the end of every ribbon glued onto the page, drawn ABOVE the page
                layer (stub_<key>_<state>_l/_r, stub_sub_<key>_<state>)

Each sprite has PAD px of transparent margin for its shadow. The ribbon root is
meant to sit ~30px under the page layer (book_pages.webp), which supplies the
tuck shadow. Placement maths lives in journal_book.rpy.

Run:  python tools/journal_assets/build_ribbons.py
"""
import math
import random
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sources import GUI_OUT, ICON_FONT, ensure_sources, save_webp  # noqa: E402

OUT = GUI_OUT / "ribbons"
SS = 3
PAD = 14
INK = (43, 26, 18)
THREAD = (240, 228, 204)

# side ribbons: width across, idle/active length (root to tip, incl. the tucked part)
SIDE_THICK, SIDE_IDLE, SIDE_ACTIVE = 60, 112, 146
# sub ribbons: width across, idle/active length
SUB_THICK, SUB_IDLE, SUB_ACTIVE = 118, 84, 104
# glued-down ends on the page. Side: 12px over the page-stack edge (x 268-280 /
# 1640-1652) + 28px on the paper. Top: 4px over the edge line at y 150 + 16px, short
# so they end above the page titles. Placement in journal_book.rpy.
STUB_SIDE, STUB_SUB = 40, 20

ICONS = {
    "overview": 0xe871,      # dashboard
    "characters": 0xf233,    # groups
    "unlockables": 0xe898,   # lock_open
    "situations": 0xf1bb,    # pending_actions
    "inventory": 0xe1a1,     # inventory_2
    "collectibles": 0xe411,  # photo_album
    "gallery": 0xe404,       # movie
    "credits": 0xe87e,       # favorite
    "cheats": 0xeb40,        # casino
    "menu": 0xe8b8,          # settings
    "exit": 0xe5cd,          # close
}

# muted fabric colours; the meta group is neutral on purpose so it reads as "system"
COLORS = {
    "overview": (128, 34, 44),       # bordeaux
    "characters": (40, 62, 104),     # navy
    "unlockables": (46, 92, 64),     # fir green
    "situations": (176, 128, 40),    # ochre
    "inventory": (96, 52, 92),       # plum
    "collectibles": (44, 110, 116),  # petrol
    "gallery": (70, 70, 74),         # anthracite
    "credits": (128, 108, 92),       # taupe
    "cheats": (78, 92, 104),         # slate
    "menu": (104, 96, 84),           # warm grey
    "exit": (150, 44, 36),           # signal red
}


def smooth_noise(n, rng, octaves=((9, 1.0), (3, 0.5))):
    t = np.arange(n, dtype=np.float32) / max(1, n) * 2 * math.pi
    out = np.zeros(n, np.float32)
    for waves, amp in octaves:
        k = rng.randint(1, waves)
        out += amp * np.sin(k * t + rng.random() * 6.283)
    return out / max(1e-6, np.abs(out).max())


def densify(poly, step):
    pts = []
    for a, b in zip(poly, poly[1:] + poly[:1]):
        n = max(1, int(math.hypot(b[0] - a[0], b[1] - a[1]) / step))
        for i in range(n):
            pts.append((a[0] + (b[0] - a[0]) * i / n, a[1] + (b[1] - a[1]) * i / n))
    return np.array(pts, np.float32)


def wobble(pts, amp, seed):
    rng = random.Random(seed)
    d = np.roll(pts, -1, axis=0) - np.roll(pts, 1, axis=0)
    nrm = np.stack([d[:, 1], -d[:, 0]], 1)
    nrm /= np.linalg.norm(nrm, axis=1, keepdims=True) + 1e-6
    return pts + nrm * (smooth_noise(len(pts), rng) * amp)[:, None]


def _over(dst, rgb, a):
    a = np.clip(a, 0, 1)[..., None]
    da = dst[..., 3:4]
    oa = a + da * (1 - a)
    dst[..., :3] = (rgb * a + dst[..., :3] * da * (1 - a)) / np.maximum(oa, 1e-6)
    dst[..., 3:4] = oa


def ribbon(length, thick, color, seed, icon=None, notch=None, upright_after_flip=False):
    """
    Ribbon pointing LEFT, root at the right edge. Returns a 1x RGBA image with PAD margin.
    upright_after_flip: draw the icon mirrored, so it reads the right way round once the
    ribbon is flipped to point right (arrows and play symbols are not symmetric).
    """
    w, h = (length + PAD * 2) * SS, (thick + PAD * 2) * SS
    x0, y0 = PAD * SS, PAD * SS
    x1, y1 = x0 + length * SS, y0 + thick * SS
    notch = (thick * 0.36 if notch is None else notch) * SS
    poly = [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0 + notch, (y0 + y1) / 2)]
    pts = wobble(densify(poly, SS), 0.5 * SS, seed)

    mask_img = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask_img).polygon([tuple(p) for p in pts], fill=255)
    mask = np.asarray(mask_img, np.float32) / 255

    Y = np.arange(h, dtype=np.float32)[:, None].repeat(w, 1)
    X = np.arange(w, dtype=np.float32)[None, :].repeat(h, 0)
    c = np.array(color, np.float32) / 255

    # cel bands across the width: lit top edge, body, shaded underside
    tv = np.clip((Y - y0) / (y1 - y0), 0, 1)
    band = np.where(tv < 0.18, 1.22, np.where(tv < 0.80, 1.0, 0.78)).astype(np.float32)
    band = np.asarray(Image.fromarray((band / 1.3 * 255).astype(np.uint8)).filter(
        ImageFilter.GaussianBlur(0.8 * SS)), np.float32) / 255 * 1.3
    # grosgrain: fine ribs running across the ribbon
    rng = np.random.default_rng(seed)
    ribs = 0.94 + 0.06 * np.sin(X / (1.6 * SS) * math.pi) + rng.normal(0, 0.025, (h, w))
    rgb = np.clip(c[None, None, :] * band[..., None] * ribs[..., None], 0, 1)
    # only a hint of darkening towards the root: the glued stub on the page covers
    # the tuck, a strong falloff would show as a dark band next to it
    root = np.clip(1 - (x1 - X) / (40 * SS), 0, 1) ** 1.6
    rgb *= (1 - 0.1 * root)[..., None]

    # ink outline on every side except the root, which hides under the page
    stroke = Image.new("L", (w, h), 0)
    dr = ImageDraw.Draw(stroke)
    var = smooth_noise(len(pts), random.Random(seed + 7))
    for i, (x, y) in enumerate(pts):
        if x > x1 - 2 * SS:
            continue
        r = 1.15 * SS * (0.85 + 0.25 * var[i])
        dr.ellipse((x - r, y - r, x + r, y + r), fill=255)
    stroke = np.asarray(stroke, np.float32) / 255

    content = Image.new("L", (w, h), 0)
    if icon is not None:
        cd = ImageDraw.Draw(content)
        font = ImageFont.truetype(str(ICON_FONT), int(min(30, thick * 0.6) * SS))
        font.set_variation_by_axes([1, 0, 24, 500])
        ch = chr(icon)
        bb = cd.textbbox((0, 0), ch, font=font)
        # centre in the visible part: between the notch and the page edge (~36px from the root)
        cx = x0 + notch + (x1 - 36 * SS - x0 - notch) * 0.5
        cd.text((cx - (bb[0] + bb[2]) / 2, (y0 + y1) / 2 - (bb[1] + bb[3]) / 2), ch, font=font, fill=255)
        if upright_after_flip:
            # mirror the glyph around its own centre, not the whole ribbon
            gx0, gx1 = int(cx - (bb[2] - bb[0]) / 2) - 2 * SS, int(cx + (bb[2] - bb[0]) / 2) + 2 * SS
            glyph = content.crop((gx0, 0, gx1, h)).transpose(Image.FLIP_LEFT_RIGHT)
            content.paste(glyph, (gx0, 0))
    content = np.asarray(content, np.float32) / 255

    out = np.zeros((h, w, 4), np.float32)
    shadow = np.asarray(Image.fromarray((mask * 255).astype(np.uint8)).filter(
        ImageFilter.GaussianBlur(3 * SS)), np.float32) / 255
    shadow = np.roll(np.roll(shadow, 3 * SS, 0), 2 * SS, 1)
    _over(out, np.zeros(3, np.float32), shadow * 0.45)
    _over(out, rgb, mask)
    emboss = np.roll(np.roll(content, SS, 0), SS, 1) * (1 - content)
    _over(out, c * 0.45, emboss * mask * 0.9)
    _over(out, np.array(THREAD, np.float32) / 255, content * mask)
    _over(out, np.array(INK, np.float32) / 255, stroke)

    img = Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8), "RGBA")
    return img.resize((w // SS, h // SS), Image.LANCZOS)


def stub(length, thick, color, seed):
    """
    The glued-down end of a ribbon, lying on the page: it wraps over the page
    edge on the LEFT side of the image and ends in a straight cut on the right.
    Returns a 1x RGBA image with PAD margin and no shadow (added after the
    sprite is turned, so the shadow always falls down-right).
    """

    w, h = (length + PAD * 2) * SS, (thick + PAD * 2) * SS
    x0, y0 = PAD * SS, PAD * SS
    x1, y1 = x0 + length * SS, y0 + thick * SS
    poly = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    pts = wobble(densify(poly, SS), 0.45 * SS, seed)

    mask_img = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask_img).polygon([tuple(p) for p in pts], fill=255)
    mask = np.asarray(mask_img, np.float32) / 255

    Y = np.arange(h, dtype=np.float32)[:, None].repeat(w, 1)
    X = np.arange(w, dtype=np.float32)[None, :].repeat(h, 0)
    c = np.array(color, np.float32) / 255

    # same cel bands and grosgrain as the ribbon itself, so the two read as one strip
    tv = np.clip((Y - y0) / (y1 - y0), 0, 1)
    band = np.where(tv < 0.18, 1.22, np.where(tv < 0.80, 1.0, 0.78)).astype(np.float32)
    band = np.asarray(Image.fromarray((band / 1.3 * 255).astype(np.uint8)).filter(
        ImageFilter.GaussianBlur(0.8 * SS)), np.float32) / 255 * 1.3
    rng = np.random.default_rng(seed)
    ribs = 0.94 + 0.06 * np.sin(X / (1.6 * SS) * math.pi) + rng.normal(0, 0.025, (h, w))
    rgb = np.clip(c[None, None, :] * band[..., None] * ribs[..., None], 0, 1)
    # where it bends over the page edge the fabric turns away from the light
    bend = np.clip(1 - (X - x0) / (10 * SS), 0, 1) ** 1.5
    rgb *= (1 - 0.28 * bend)[..., None]
    # glue soaked into the fabric just before the cut: a darker, slightly blotchy band
    glue = np.clip(1 - np.abs(X - (x1 - 4 * SS)) / (3.5 * SS), 0, 1)
    glue *= 0.75 + 0.25 * np.sin(Y / (5 * SS) + seed)
    rgb *= (1 - 0.22 * glue)[..., None]

    # ink outline along both long sides and the cut; the edge side wraps out of view
    stroke = Image.new("L", (w, h), 0)
    dr = ImageDraw.Draw(stroke)
    var = smooth_noise(len(pts), random.Random(seed + 7))
    for i, (x, y) in enumerate(pts):
        if x < x0 + 2 * SS:
            continue
        r = 1.1 * SS * (0.85 + 0.25 * var[i])
        dr.ellipse((x - r, y - r, x + r, y + r), fill=255)
    stroke = np.asarray(stroke, np.float32) / 255

    out = np.zeros((h, w, 4), np.float32)
    _over(out, rgb, mask)
    _over(out, np.array(INK, np.float32) / 255, stroke)
    img = Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8), "RGBA")
    return img.resize((w // SS, h // SS), Image.LANCZOS)


def with_flat_shadow(img):
    # glued flat onto the paper: a short, tight shadow, not the hanging ribbon's soft one
    alpha = img.split()[3]
    shadow = Image.new("RGBA", img.size, (30, 18, 10, 0))
    shadow.putalpha(alpha.filter(ImageFilter.GaussianBlur(1.6)).point(lambda v: int(v * 0.45)))
    out = Image.new("RGBA", img.size, (0, 0, 0, 0))
    out.alpha_composite(shadow, (2, 2))
    out.alpha_composite(img)
    return out


def title_ribbons():
    """
    Main menu: background controls as ribbons on the right edge of the peeking book
    (title_<name>.webp, pointing right, icon upright).
    """

    for name, icon, color in (("anim_pause", 0xe034, (78, 92, 104)), ("anim_play", 0xe037, (78, 92, 104)),
                              ("bg_next", 0xe044, (104, 96, 84)), ("bg_grid", 0xe9b0, (96, 52, 92))):
        for state, length in (("idle", SIDE_IDLE), ("active", SIDE_ACTIVE)):
            c = color if state == "active" else tuple(int(v * 0.86) for v in color)
            img = ribbon(length, SIDE_THICK, c, 1300 + icon % 97, icon=icon, upright_after_flip=True)
            save_webp(img.transpose(Image.FLIP_LEFT_RIGHT), OUT / f"title_{name}_{state}.webp", lossless=True)


def build():
    for i, (key, col) in enumerate(COLORS.items()):
        for state in ("idle", "active"):
            c = col if state == "active" else tuple(int(v * 0.86) for v in col)
            piece = stub(STUB_SIDE, SIDE_THICK, c, 500 + i)
            save_webp(with_flat_shadow(piece), OUT / f"stub_{key}_{state}_l.webp", lossless=True)
            save_webp(with_flat_shadow(piece.transpose(Image.FLIP_LEFT_RIGHT)), OUT / f"stub_{key}_{state}_r.webp", lossless=True)
            piece = stub(STUB_SUB, SUB_THICK, c, 700 + i)
            save_webp(with_flat_shadow(piece.transpose(Image.ROTATE_270)), OUT / f"stub_sub_{key}_{state}.webp", lossless=True)

    for i, (key, col) in enumerate(COLORS.items()):
        for state, length in (("idle", SIDE_IDLE), ("active", SIDE_ACTIVE)):
            c = col if state == "active" else tuple(int(v * 0.86) for v in col)
            img = ribbon(length, SIDE_THICK, c, 100 + i, icon=ICONS[key])
            save_webp(img, OUT / f"{key}_{state}_l.webp", lossless=True)
            save_webp(img.transpose(Image.FLIP_LEFT_RIGHT), OUT / f"{key}_{state}_r.webp", lossless=True)

        for state, length in (("idle", SUB_IDLE), ("active", SUB_ACTIVE)):
            c = col if state == "active" else tuple(int(v * 0.86) for v in col)
            img = ribbon(length, SUB_THICK, c, 300 + i, notch=0)
            # rotate so the free end points up and the root sits at the bottom
            save_webp(img.transpose(Image.ROTATE_270), OUT / f"sub_{key}_{state}.webp", lossless=True)


if __name__ == "__main__":
    ensure_sources()
    build()
    title_ribbons()
