"""Converts the PNGs written by the in-game `wiki_screenshots` label to WebP.

Run after `jump wiki_screenshots`:  python wiki/scripts/compress-screenshots.py
"""
import pathlib

from PIL import Image

folder = pathlib.Path(__file__).resolve().parent.parent / "screenshots"
for png in sorted(folder.glob("*.png")):
    webp = png.with_suffix(".webp")
    Image.open(png).convert("RGB").save(webp, "WEBP", quality=85, method=6)
    png.unlink()
    print(f"{png.name} -> {webp.name} ({webp.stat().st_size // 1024} KB)")
