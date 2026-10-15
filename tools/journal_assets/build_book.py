"""
Builds the journal book background (1920x1080 RGBA) from CC0 textures.

Style goal: cartoon silhouette (wobbly brush-pen ink outline, simple shapes)
filled with real photographed materials (leather, paper) and believable
construction (6-ring binder, page stacks, stitching, ribbon).

Output (game/gui/journal/) is split into two layers so the navigation ribbons
can sit between them and really come out from under the page stack:
  book_cover.webp  - drop shadow, leather cover, stitching, spine mechanism
  book_pages.webp  - page stacks, pages, rings, decorative ribbon
2x masters and a combined preview go to .cache/.

Run:  python tools/journal_assets/build_book.py

Everything is rendered at SS x resolution and downsampled for anti-aliasing.
"""
import math
import random
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sources import CACHE, GUI_OUT, LEATHER as LEATHER_TEX, PAPER as PAPER_TEX, ensure_sources, save_webp  # noqa: E402

OUT = CACHE

SS = 2
W, H = 1920 * SS, 1080 * SS

INK = np.array([43, 26, 18], np.float32) / 255
LEATHER = np.array([128, 70, 36], np.float32) / 255
PAPER = np.array([247, 240, 225], np.float32) / 255
THREAD = np.array([226, 200, 160], np.float32) / 255
RIBBON = np.array([138, 30, 38], np.float32) / 255
BLACK = np.zeros(3, np.float32)

# 1x layout -- journal_book.rpy uses the same page rectangles, keep them in sync
COVER = (228, 116, 1692, 1054)
LEFT_PAGE = (280, 150, 942, 1016)
RIGHT_PAGE = (978, 150, 1640, 1016)
GUTTER_X = 960
RING_YS = [236, 290, 344, 826, 880, 934]


def s(v):
    return v * SS


# ---------------------------------------------------------------- geometry

def rounded_rect_path(x0, y0, x1, y1, radii, step=1.0):
    """Closed outline, clockwise from top-left. radii = (tl, tr, br, bl) in canvas px."""
    tl, tr, br, bl = radii
    pts = []

    def arc(cx, cy, r, a0, a1):
        if r <= 0:
            pts.append((cx, cy))
            return
        n = max(2, int(abs(a1 - a0) * r / step))
        for i in range(n + 1):
            a = a0 + (a1 - a0) * i / n
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))

    def line(xa, ya, xb, yb):
        n = max(1, int(math.hypot(xb - xa, yb - ya) / step))
        for i in range(1, n):
            pts.append((xa + (xb - xa) * i / n, ya + (yb - ya) * i / n))

    arc(x0 + tl, y0 + tl, tl, math.pi, 1.5 * math.pi)
    line(x0 + tl, y0, x1 - tr, y0)
    arc(x1 - tr, y0 + tr, tr, 1.5 * math.pi, 2 * math.pi)
    line(x1, y0 + tr, x1, y1 - br)
    arc(x1 - br, y1 - br, br, 0, 0.5 * math.pi)
    line(x1 - br, y1, x0 + bl, y1)
    arc(x0 + bl, y1 - bl, bl, 0.5 * math.pi, math.pi)
    line(x0, y1 - bl, x0, y0 + tl)
    return np.array(pts, np.float32)


def smooth_noise(n, rng, octaves=((60, 1.0), (19, 0.35))):
    """1D periodic smooth noise of length n, built from random sine waves."""
    t = np.arange(n, dtype=np.float32) / n * 2 * math.pi
    out = np.zeros(n, np.float32)
    for waves, amp in octaves:
        for _ in range(3):
            k = rng.randint(max(1, waves // 2), waves)
            out += amp * np.sin(k * t + rng.random() * 6.283) / 3
    return out / max(1e-6, np.abs(out).max())


def wobble(pts, amp, seed):
    rng = random.Random(seed)
    d = np.roll(pts, -1, axis=0) - np.roll(pts, 1, axis=0)
    nrm = np.stack([d[:, 1], -d[:, 0]], 1)
    nrm /= np.linalg.norm(nrm, axis=1, keepdims=True) + 1e-6
    return pts + nrm * (smooth_noise(len(pts), rng) * amp)[:, None]


def poly_mask(pts):
    m = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m).polygon([tuple(p) for p in pts], fill=255)
    return np.asarray(m, np.float32) / 255


def stroke_mask(pts, width, seed):
    """Brush-pen stroke: stamped discs whose radius drifts smoothly along the path."""
    rng = random.Random(seed)
    m = Image.new("L", (W, H), 0)
    dr = ImageDraw.Draw(m)
    var = smooth_noise(len(pts), rng, ((25, 1.0), (7, 0.4)))
    for i, (x, y) in enumerate(pts):
        r = width / 2 * (0.82 + 0.28 * var[i])
        dr.ellipse((x - r, y - r, x + r, y + r), fill=255)
    return np.asarray(m, np.float32) / 255


def blur(a, radius):
    img = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))
    return np.asarray(img.filter(ImageFilter.GaussianBlur(radius)), np.float32) / 255


def blur_any(a, radius):
    lo, hi = float(a.min()), float(a.max())
    img = Image.fromarray(((a - lo) / (hi - lo + 1e-6) * 255).astype(np.uint8))
    return np.asarray(img.filter(ImageFilter.GaussianBlur(radius)), np.float32) / 255 * (hi - lo) + lo


def shift(a, dx, dy):
    out = np.zeros_like(a)
    dx, dy = int(dx), int(dy)
    ys = slice(max(0, dy), H + min(0, dy))
    yd = slice(max(0, -dy), H + min(0, -dy))
    xs = slice(max(0, dx), W + min(0, dx))
    xd = slice(max(0, -dx), W + min(0, -dx))
    out[ys, xs] = a[yd, xd]
    return out


# ---------------------------------------------------------------- materials

def load_lum(path, scale, x0, y0, rotate=False):
    """Texture detail placed once (no tiling, so no seams or mirror artefacts) at canvas pos x0,y0."""
    img = Image.open(path).convert("L")
    if rotate:
        img = img.transpose(Image.ROTATE_90)
    img = img.resize((int(img.width * scale), int(img.height * scale)), Image.LANCZOS)
    a = np.asarray(img, np.float32) / 255
    # remove low-frequency lighting so the photo only carries surface detail
    a = a - blur_any(a, 60 * SS)
    a /= a.std() + 1e-6
    out = np.zeros((H, W), np.float32)
    x0, y0 = int(x0), int(y0)
    h = min(a.shape[0], H - y0)
    w = min(a.shape[1], W - x0)
    out[y0:y0 + h, x0:x0 + w] = a[:h, :w]
    return out


def material(color, detail, strength):
    rgb = color[None, None, :] * (1 + strength * detail[..., None])
    return np.clip(rgb, 0, 1)


# ---------------------------------------------------------------- compositing

canvas = np.zeros((H, W, 4), np.float32)


def over(rgb, alpha):
    """Composite a colour layer (H,W,3 or 3,) with alpha (H,W) onto the canvas."""
    if rgb.ndim == 1:
        rgb = np.broadcast_to(rgb, (H, W, 3))
    a = np.clip(alpha, 0, 1)[..., None]
    ca = canvas[..., 3:4]
    out_a = a + ca * (1 - a)
    canvas[..., :3] = (rgb * a + canvas[..., :3] * ca * (1 - a)) / np.maximum(out_a, 1e-6)
    canvas[..., 3:4] = out_a


def shade(mask, amount, color=BLACK):
    """Darken (amount>0, towards color) or lighten (amount<0, towards white) inside mask."""
    m = np.clip(mask, 0, 1)[..., None]
    if amount >= 0:
        canvas[..., :3] = canvas[..., :3] * (1 - m * amount) + color * m * amount
    else:
        canvas[..., :3] = canvas[..., :3] + (1 - canvas[..., :3]) * m * (-amount)


def save_layer(name):
    img = Image.fromarray((np.clip(canvas, 0, 1) * 255).astype(np.uint8), "RGBA")
    img.save(OUT / f"{name}_2x.png")
    small = img.resize((1920, 1080), Image.LANCZOS)
    small.save(OUT / f"{name}.png")
    save_webp(small, GUI_OUT / f"{name}.webp")


# ---------------------------------------------------------------- build

def build():
    X = np.broadcast_to(np.arange(W, dtype=np.float32)[None, :], (H, W))
    Y = np.broadcast_to(np.arange(H, dtype=np.float32)[:, None], (H, W))

    leather_d = load_lum(LEATHER_TEX, 1.5, s(COVER[0]) - 20, s(COVER[1]) - 20)
    paper_tex = PAPER_TEX
    # one un-tiled photo per page (rotated: the scan is landscape); split at the spine
    left_half = (X < s(GUTTER_X)).astype(np.float32)
    paper_d = (load_lum(paper_tex, 1.18, s(LEFT_PAGE[0]) - s(20), s(LEFT_PAGE[1]) - s(150), True) * left_half
               + load_lum(paper_tex, 1.18, s(RIGHT_PAGE[0]) - s(30), s(RIGHT_PAGE[1]) - s(110), True) * (1 - left_half))

    # --- cover silhouette
    cx0, cy0, cx1, cy1 = (s(v) for v in COVER)
    cover_path = wobble(rounded_rect_path(cx0, cy0, cx1, cy1, (s(34),) * 4, step=SS), s(1.6), 11)
    cover = poly_mask(cover_path)

    # book drop shadow on the map
    over(BLACK, blur(shift(cover, s(10), s(16)), s(14)) * 0.55)

    over(material(LEATHER, leather_d, 0.24), cover)

    # cel-ish bevel: hard light band top-left, dark band bottom-right
    inner = poly_mask(wobble(rounded_rect_path(cx0 + s(9), cy0 + s(9), cx1 - s(9), cy1 - s(9),
                                               (s(26),) * 4, step=SS), s(1.2), 12))
    rim = np.clip(cover - blur(inner, s(1.5)), 0, 1)
    diag = ((X - cx0) / (cx1 - cx0) + (Y - cy0) / (cy1 - cy0)) / 2
    shade(rim * np.clip((0.55 - diag) * 4, 0, 1), -0.22)
    shade(rim * np.clip((diag - 0.45) * 4, 0, 1), 0.38, INK)
    # leather ages darker towards the edges
    shade(cover * (1 - blur(inner, s(30))), 0.18, INK)

    # stitching
    st = rounded_rect_path(cx0 + s(17), cy0 + s(17), cx1 - s(17), cy1 - s(17), (s(20),) * 4, step=SS)
    st = wobble(st, s(0.6), 13)
    stitch = Image.new("L", (W, H), 0)
    hole = Image.new("L", (W, H), 0)
    ds, dh = ImageDraw.Draw(stitch), ImageDraw.Draw(hole)
    dash, gap = s(10), s(6)
    seg = np.linalg.norm(np.diff(st, axis=0), axis=1)
    acc = np.concatenate([[0], np.cumsum(seg)])
    pos = 0.0
    while pos + dash < acc[-1]:
        i0, i1 = np.searchsorted(acc, pos), np.searchsorted(acc, pos + dash)
        a, b = st[min(i0, len(st) - 1)], st[min(i1, len(st) - 1)]
        ds.line([tuple(a), tuple(b)], fill=255, width=int(s(2.4)))
        for p in (a, b):
            r = s(1.6)
            dh.ellipse((p[0] - r, p[1] - r, p[0] + r, p[1] + r), fill=255)
        pos += dash + gap
    stitch = np.asarray(stitch, np.float32) / 255
    hole = np.asarray(hole, np.float32) / 255
    over(BLACK, shift(stitch, s(1), s(1.5)) * 0.45 * cover)
    over(INK, hole * 0.8 * cover)
    over(THREAD, stitch * cover)

    # --- spine: dark recess + ring mechanism plate
    gx = s(GUTTER_X)
    recess = poly_mask(rounded_rect_path(gx - s(30), cy0 + s(26), gx + s(30), cy1 - s(26), (s(8),) * 4, step=SS))
    shade(blur(recess, s(6)), 0.35, INK)

    plate_path = wobble(rounded_rect_path(gx - s(15), s(184), gx + s(15), s(986), (s(15),) * 4, step=SS), s(0.6), 21)
    plate = poly_mask(plate_path)
    over(BLACK, blur(shift(plate, s(3), s(5)), s(5)) * 0.45)
    t = np.clip((X - (gx - s(15))) / s(30), 0, 1)
    metal = np.stack([0.42 + 0.45 * np.clip(np.sin(t * math.pi), 0, 1) ** 0.6] * 3, -1) \
        * np.array([1.0, 0.98, 0.94], np.float32)
    over(metal, plate)
    over(INK, stroke_mask(plate_path, s(2.6), 22) * 0.95)

    # --- cover outline, then split: everything so far is the COVER layer.
    # Navigation ribbons are layered between cover and pages in Ren'Py, so they
    # really come out from under the page stack.
    over(INK, stroke_mask(cover_path, s(5.0), 99))
    save_layer("book_cover")
    canvas[...] = 0

    # --- page stacks + top pages
    for side, (px0, py0, px1, py1) in (("L", LEFT_PAGE), ("R", RIGHT_PAGE)):
        px0, py0, px1, py1 = (s(v) for v in (px0, py0, px1, py1))
        outer = -1 if side == "L" else 1
        radii = (s(16), 0, 0, s(16)) if side == "L" else (0, s(16), s(16), 0)

        # shadow of the whole block on the leather (and on ribbon roots below it)
        block = poly_mask(rounded_rect_path(px0 - s(8), py0, px1 + s(8), py1 + s(10), (s(16),) * 4, step=SS))
        over(BLACK, blur(shift(block, s(4), s(7)), s(8)) * 0.5)

        for k in (4, 3, 2, 1):
            dx, dy = outer * s(2.6) * k, s(2.4) * k
            sx0 = px0 + (dx if side == "L" else 0)
            sx1 = px1 + (dx if side == "R" else 0)
            sheet_path = wobble(rounded_rect_path(sx0, py0 + s(3) * k, sx1, py1 + dy, radii, step=SS), s(0.8), 30 + k)
            sheet = poly_mask(sheet_path)
            tone = PAPER * (0.95 - 0.02 * k)
            over(material(tone, paper_d, 0.02), sheet)
            over(INK, stroke_mask(sheet_path, s(1.4), 40 + k) * 0.32)

        page_path = wobble(rounded_rect_path(px0, py0, px1, py1, radii, step=SS), s(0.9), 50 if side == "L" else 51)
        page = poly_mask(page_path)
        over(material(PAPER, paper_d, 0.028), page)

        # gutter curvature shadow + soft outer falloff
        inner_x = px1 if side == "L" else px0
        dist_in = np.abs(X - inner_x)
        shade(page * np.clip(1 - dist_in / s(130), 0, 1) ** 1.6, 0.30, np.array([90, 62, 40], np.float32) / 255)
        shade(page * np.clip(1 - dist_in / s(22), 0, 1) ** 1.3, 0.30, INK)
        outer_x = px0 if side == "L" else px1
        dist_out = np.abs(X - outer_x)
        shade(page * np.clip(1 - dist_out / s(30), 0, 1) ** 2, 0.07, np.array([120, 90, 50], np.float32) / 255)
        dist_tb = np.minimum(np.abs(Y - py0), np.abs(Y - py1))
        shade(page * np.clip(1 - dist_tb / s(22), 0, 1) ** 2, 0.06, np.array([120, 90, 50], np.float32) / 255)

        # foxing at the two outer corners, irregular rather than a clean radial blob
        rng = np.random.default_rng(60 if side == "L" else 61)
        for cy in (py0, py1):
            spot = np.exp(-(((X - outer_x) / s(70)) ** 2 + ((Y - cy) / s(55)) ** 2))
            grain = blur(rng.random((H, W)).astype(np.float32), s(6))
            grain = (grain - grain.mean()) / (grain.std() + 1e-6)
            shade(page * spot * np.clip(0.6 + 0.5 * grain, 0, 1), 0.10, np.array([150, 105, 55], np.float32) / 255)

        over(INK, stroke_mask(page_path, s(2.2), 70 if side == "L" else 71) * 0.9)

    # --- punched holes + rings (ring arcs dive into the holes on both pages)
    hole_col = np.array([52, 34, 24], np.float32) / 255
    for i, ry in enumerate(RING_YS):
        ry = s(ry)
        for hx in (gx - s(30), gx + s(30)):
            hole_m = np.clip((1 - (((X - hx) / s(8)) ** 2 + ((Y - ry) / s(9.5)) ** 2)) * 8, 0, 1)
            over(hole_col, hole_m)
            over(INK, np.clip((1 - (((X - hx) / s(9.5)) ** 2 + ((Y - ry) / s(11)) ** 2)) * 8, 0, 1)
                 * (1 - hole_m) * 0.8)

        ring_path = wobble(rounded_rect_path(gx - s(31), ry - s(8), gx + s(31), ry + s(8), (s(8),) * 4, step=SS),
                           s(0.4), 80 + i)
        ring = poly_mask(ring_path)
        # the ring disappears into the holes: fade its ends into the hole colour
        ends = np.clip((np.abs(X - gx) - s(24)) / s(6), 0, 1)
        over(BLACK, blur(shift(ring * (1 - ends), s(3), s(6)), s(4)) * 0.45)
        tv = np.clip((Y - (ry - s(8))) / s(16), 0, 1)
        tone = np.where(tv < 0.28, 0.92, np.where(tv < 0.7, 0.66, 0.40)).astype(np.float32)
        tone = blur(tone, s(0.8))
        metal = np.stack([tone * 0.98, tone * 0.95, tone * 0.88], -1)
        over(metal, ring)
        shade(ring * ends, 0.75, hole_col)
        over(INK, stroke_mask(ring_path, s(2.4), 90 + i) * (1 - ends * 0.6))

    # --- decorative ribbon bookmark hanging out at the bottom
    rx0, rx1 = s(1004), s(1030)
    ry0, ry1 = s(990), s(1078)
    ribbon_pts = [(rx0, ry0), (rx1, ry0), (rx1 + s(2), ry1), (rx0 + s(13), ry1 - s(11)), (rx0 + s(2), ry1)]
    rp = []
    for a, b in zip(ribbon_pts, ribbon_pts[1:] + ribbon_pts[:1]):
        n = max(2, int(math.hypot(b[0] - a[0], b[1] - a[1]) / SS))
        for j in range(n):
            rp.append((a[0] + (b[0] - a[0]) * j / n, a[1] + (b[1] - a[1]) * j / n))
    rp = wobble(np.array(rp, np.float32), s(0.5), 95)
    ribbon = poly_mask(rp)
    over(BLACK, blur(shift(ribbon, s(3), s(4)), s(4)) * 0.45)
    tr = np.clip((X - rx0) / (rx1 - rx0), 0, 1)
    rib_rgb = RIBBON[None, None, :] * np.where(tr < 0.35, 1.18, np.where(tr < 0.8, 1.0, 0.78))[..., None]
    over(np.clip(rib_rgb, 0, 1), ribbon)
    # ribbon tucks under the page edge: page edge shadow over it
    shade(ribbon * np.clip(1 - (Y - s(1016)) / s(10), 0, 1) * (Y > s(1010)), 0.35, INK)
    over(INK, stroke_mask(rp, s(2.2), 96))

    save_layer("book_pages")

    # combined single image, handy for previews
    for suffix in ("", "_2x"):
        book = Image.open(OUT / f"book_cover{suffix}.png")
        book.alpha_composite(Image.open(OUT / f"book_pages{suffix}.png"))
        book.save(OUT / f"book{suffix}.png")
    return Image.open(OUT / "book.png")


def preview(book):
    bg_path = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    if bg_path and bg_path.exists():
        bg = Image.open(bg_path).convert("RGB").resize((1920, 1080), Image.LANCZOS)
        bg = bg.filter(ImageFilter.GaussianBlur(6))
        dark = Image.new("RGB", bg.size, (24, 18, 14))
        bg = Image.blend(bg, dark, 0.55)
    else:
        bg = Image.new("RGB", (1920, 1080), (40, 34, 30))
    bg = bg.convert("RGBA")
    bg.alpha_composite(book)
    bg.convert("RGB").save(OUT / "preview.png")


if __name__ == "__main__":
    ensure_sources()
    preview(build())
