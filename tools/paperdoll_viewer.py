#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Standalone Paperdoll Viewer for *Mind the School*.

A self-contained Tkinter desktop tool that mirrors the in-game "Paperdoll Test"
debug screen, but runs completely independently of Ren'Py. It reads the real game
assets from ``game/images/paperdoll`` and lets you freely combine a character with
its variant, pose, outfit, level, state, mood and mouth, then previews the composed
paperdoll live.

How the game composes a paperdoll (replicated here)
---------------------------------------------------
Each character paperdoll is built from two stacked layers that share the same
1200x2160 canvas (see ``game/scripts/character.rpy`` -> ``register_paperdoll``):

    bottom :  <name>/bottom/<name> <char_var> <pose> <outfit> <level> <state>.png
    top    :  <name>/top/<name> <char_var> <pose> <mood> <mouth>.png

The ``bottom`` layer is the body incl. outfit and (progression) level; the ``top``
layer is the head/face incl. mood and mouth. ``$`` is the wildcard token the game
uses for a dimension that does not apply (e.g. ``char_var`` for most characters, or
``mouth`` for the ``pout`` / ``suprised`` moods). The trailing ``state`` token is
optional in some files.

The viewer discovers every available combination by scanning the files on disk and
only offers valid, resolvable selections (cascading, exactly like the debug screen).

Requirements
------------
    Python 3.9+      (tested on 3.13)
    Pillow           (pip install pillow)
    tkinter          (ships with the standard CPython installer on Windows)

Usage
-----
    python tools/paperdoll_viewer.py
    python tools/paperdoll_viewer.py --root "some/other/game/images/paperdoll"
"""

from __future__ import annotations

import argparse
import os
import sys
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

try:
    from PIL import Image, ImageTk
except ImportError:  # pragma: no cover - user guidance path
    sys.stderr.write(
        "\nThis tool needs the 'Pillow' package.\n"
        "Install it with:\n\n    pip install pillow\n\n"
    )
    raise SystemExit(1)

import tkinter as tk
from tkinter import ttk, filedialog, messagebox


# --------------------------------------------------------------------------- #
# Constants
# --------------------------------------------------------------------------- #

WILDCARD = "$"                 # token used in filenames for "not applicable"
CANVAS_W, CANVAS_H = 1200, 2160  # native paperdoll canvas (aspect used for fitting)
IMAGE_EXTS = (".png", ".webp")


# --------------------------------------------------------------------------- #
# Data model
# --------------------------------------------------------------------------- #


@dataclass
class BottomEntry:
    char_var: str
    pose: str
    outfit: str
    level: str
    state: str
    path: str


@dataclass
class TopEntry:
    char_var: str
    pose: str
    mood: str
    mouth: str
    path: str


@dataclass
class Character:
    name: str
    bottoms: List[BottomEntry] = field(default_factory=list)
    tops: List[TopEntry] = field(default_factory=list)


def _iter_images(folder: str):
    if not os.path.isdir(folder):
        return
    for fname in os.listdir(folder):
        stem, ext = os.path.splitext(fname)
        if ext.lower() in IMAGE_EXTS:
            yield fname, stem


def _rest_tokens(stem: str, name: str) -> Optional[List[str]]:
    """Return filename tokens after the leading character name, or None on mismatch."""
    prefix = name + " "
    if not stem.startswith(prefix):
        # Some assets may differ in case or spacing; be lenient by splitting.
        parts = stem.split(" ")
        if parts and parts[0] == name:
            return parts[1:]
        return None
    return stem[len(prefix):].split(" ")


def scan_character(root: str, name: str) -> Character:
    """Parse every bottom/top file for a character into structured entries."""
    char = Character(name=name)
    char_dir = os.path.join(root, name)

    # bottom: <char_var> <pose> <outfit> <level> [<state>...]
    bottom_dir = os.path.join(char_dir, "bottom")
    for fname, stem in _iter_images(bottom_dir):
        parts = _rest_tokens(stem, name)
        if parts is None or len(parts) < 4:
            continue
        state = " ".join(parts[4:]) if len(parts) > 4 else WILDCARD
        char.bottoms.append(
            BottomEntry(
                char_var=parts[0],
                pose=parts[1],
                outfit=parts[2],
                level=parts[3],
                state=state or WILDCARD,
                path=os.path.join(bottom_dir, fname),
            )
        )

    # top: <char_var> <pose> <mood> <mouth>
    top_dir = os.path.join(char_dir, "top")
    for fname, stem in _iter_images(top_dir):
        parts = _rest_tokens(stem, name)
        if parts is None or len(parts) < 4:
            continue
        char.tops.append(
            TopEntry(
                char_var=parts[0],
                pose=parts[1],
                mood=parts[2],
                mouth=parts[3],
                path=os.path.join(top_dir, fname),
            )
        )

    return char


def discover_characters(root: str) -> List[str]:
    if not os.path.isdir(root):
        return []
    names = []
    for entry in sorted(os.listdir(root)):
        full = os.path.join(root, entry)
        if os.path.isdir(full) and os.path.isdir(os.path.join(full, "bottom")):
            names.append(entry)
    return names


# --------------------------------------------------------------------------- #
# Sorting helpers
# --------------------------------------------------------------------------- #


def _num_key(value: str) -> Tuple[int, float, str]:
    """Sort numeric-ish tokens ascending, wildcard/non-numeric last, stable by text."""
    if value == WILDCARD:
        return (2, 0.0, value)
    try:
        return (0, float(value), value)
    except ValueError:
        return (1, 0.0, value)


def sorted_unique(values, numeric: bool = False) -> List[str]:
    uniq = list(dict.fromkeys(values))
    if numeric:
        uniq.sort(key=_num_key)
    else:
        uniq.sort(key=lambda v: (v == WILDCARD, v.lower()))
    return uniq


def pretty(value: str) -> str:
    return "— default —" if value == WILDCARD else value


# --------------------------------------------------------------------------- #
# Application
# --------------------------------------------------------------------------- #


class PaperdollViewer(tk.Tk):
    # Order matters: options cascade from top to bottom.
    BOTTOM_DIMS = ["char_var", "pose", "outfit", "level", "state"]
    TOP_DIMS = ["mood", "mouth"]

    DIM_LABELS = {
        "char_var": "Variant",
        "pose": "Pose",
        "outfit": "Outfit",
        "level": "Level",
        "state": "State",
        "mood": "Mood",
        "mouth": "Mouth",
    }
    NUMERIC_DIMS = {"char_var", "pose", "level"}

    BG_STYLES = ["Checkerboard", "Dark", "Light", "Green"]

    def __init__(self, root_dir: str):
        super().__init__()
        self.title("Mind the School — Paperdoll Viewer")
        self.minsize(360, 620)
        self.geometry("560x1000")  # portrait-first default

        self.root_dir = root_dir
        self.characters: Dict[str, Character] = {}
        self.char_names: List[str] = discover_characters(root_dir)
        self.active: Optional[Character] = None

        # Current selection per dimension.
        self.sel: Dict[str, str] = {}

        # Rendering state.
        self._composited: Optional[Image.Image] = None  # full-res RGBA
        self._tk_image = None                            # keep ref
        self._checker_cache: Dict[Tuple[int, int], Image.Image] = {}
        self._refreshing = False
        self._resize_job = None

        self._build_style()
        self._build_ui()

        if not self.char_names:
            self.after(100, self._prompt_for_root)
        else:
            self.character_var.set(self.char_names[0])
            self._load_character(self.char_names[0])

    # ------------------------------------------------------------------ UI --

    def _build_style(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        bg = "#1e1f24"
        panel = "#26272e"
        fg = "#e6e6ea"
        accent = "#4c8bf5"
        self.configure(bg=bg)
        self._c = dict(bg=bg, panel=panel, fg=fg, accent=accent)

        style.configure(".", background=bg, foreground=fg, fieldbackground=panel)
        style.configure("TFrame", background=bg)
        style.configure("Panel.TFrame", background=panel)
        style.configure("TLabel", background=bg, foreground=fg)
        style.configure("Head.TLabel", background=bg, foreground="#9aa0ac",
                        font=("Segoe UI", 8, "bold"))
        style.configure("Status.TLabel", background=panel, foreground="#9aa0ac",
                        font=("Consolas", 8))
        style.configure("TButton", background=panel, foreground=fg, borderwidth=0,
                        padding=2)
        style.map("TButton", background=[("active", accent)])
        style.configure("Field.TCheckbutton", background=panel, foreground="#9aa0ac",
                        font=("Segoe UI", 8, "bold"))
        style.map("Field.TCheckbutton",
                  background=[("active", panel)],
                  foreground=[("selected", fg), ("active", fg)])
        style.configure("TCombobox", padding=2)
        style.map("TCombobox", fieldbackground=[("readonly", panel)],
                  foreground=[("readonly", fg)], selectbackground=[("readonly", panel)],
                  selectforeground=[("readonly", fg)])

    def _build_ui(self):
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # --- Preview canvas (dominant, top) ---
        self.canvas = tk.Canvas(self, highlightthickness=0, bg="#111216", bd=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.canvas.bind("<Configure>", self._on_canvas_resize)

        # --- Control panel (bottom) ---
        panel = ttk.Frame(self, style="Panel.TFrame", padding=(10, 8))
        panel.grid(row=1, column=0, sticky="ew")
        panel.columnconfigure(0, weight=1)
        self._panel = panel

        # Character row
        char_row = ttk.Frame(panel, style="Panel.TFrame")
        char_row.grid(row=0, column=0, sticky="ew", pady=(0, 6))
        char_row.columnconfigure(1, weight=1)
        ttk.Label(char_row, text="Character", style="Head.TLabel").grid(
            row=0, column=0, columnspan=3, sticky="w")
        self.character_var = tk.StringVar()
        ttk.Button(char_row, text="◀", width=2,
                   command=lambda: self._step_character(-1)).grid(row=1, column=0)
        self.character_combo = ttk.Combobox(
            char_row, textvariable=self.character_var, values=self.char_names,
            state="readonly")
        self.character_combo.grid(row=1, column=1, sticky="ew", padx=4)
        self.character_combo.bind(
            "<<ComboboxSelected>>",
            lambda e: self._load_character(self.character_var.get()))
        ttk.Button(char_row, text="▶", width=2,
                   command=lambda: self._step_character(1)).grid(row=1, column=2)

        # Dimension comboboxes in a 2-column grid (portrait friendly)
        dims_frame = ttk.Frame(panel, style="Panel.TFrame")
        dims_frame.grid(row=1, column=0, sticky="ew")
        dims_frame.columnconfigure(0, weight=1)
        dims_frame.columnconfigure(1, weight=1)

        self.dim_vars: Dict[str, tk.StringVar] = {}
        self.dim_combos: Dict[str, ttk.Combobox] = {}
        # Whether each field is written into the generated PDAImage(...). The
        # checkbox doubles as the field label. Defaults mirror the house style:
        # events pass pose/outfit/level/mood/mouth; char_var/state are omitted.
        self.include_vars: Dict[str, tk.BooleanVar] = {}
        all_dims = self.BOTTOM_DIMS + self.TOP_DIMS
        for i, dim in enumerate(all_dims):
            cell = ttk.Frame(dims_frame, style="Panel.TFrame")
            cell.grid(row=i // 2, column=i % 2, sticky="ew", padx=3, pady=3)
            cell.columnconfigure(1, weight=1)
            inc = tk.BooleanVar(value=dim not in ("char_var", "state"))
            ttk.Checkbutton(cell, text=self.DIM_LABELS[dim], variable=inc,
                            style="Field.TCheckbutton",
                            command=self._update_code).grid(
                row=0, column=0, columnspan=3, sticky="w")
            var = tk.StringVar()
            combo = ttk.Combobox(cell, textvariable=var, state="readonly", width=6)
            combo.grid(row=1, column=1, sticky="ew", padx=2)
            ttk.Button(cell, text="◀", width=2,
                       command=lambda d=dim: self._step_dim(d, -1)).grid(row=1, column=0)
            ttk.Button(cell, text="▶", width=2,
                       command=lambda d=dim: self._step_dim(d, 1)).grid(row=1, column=2)
            combo.bind("<<ComboboxSelected>>",
                       lambda e, d=dim: self._on_dim_changed(d))
            self.dim_vars[dim] = var
            self.dim_combos[dim] = combo
            self.include_vars[dim] = inc

        # Options row: background style
        opts = ttk.Frame(panel, style="Panel.TFrame")
        opts.grid(row=2, column=0, sticky="ew", pady=(6, 2))
        opts.columnconfigure(1, weight=1)

        ttk.Label(opts, text="Backdrop", style="Head.TLabel").grid(row=0, column=0, sticky="w")
        self.bg_style_var = tk.StringVar(value=self.BG_STYLES[0])
        bg_combo = ttk.Combobox(opts, textvariable=self.bg_style_var, state="readonly",
                                width=12, values=self.BG_STYLES)
        bg_combo.grid(row=0, column=1, sticky="w", padx=4)
        bg_combo.bind("<<ComboboxSelected>>", lambda e: self._render_preview())

        # Code generator: live PDAImage(...) preview + copy button
        code = ttk.Frame(panel, style="Panel.TFrame")
        code.grid(row=3, column=0, sticky="ew", pady=(8, 2))
        code.columnconfigure(0, weight=1)
        self.code_var = tk.StringVar(value="")
        code_entry = ttk.Entry(code, textvariable=self.code_var, state="readonly",
                               font=("Consolas", 9))
        code_entry.grid(row=0, column=0, sticky="ew", padx=(0, 6))
        self.copy_btn = ttk.Button(code, text="Copy PDAImage", width=15,
                                   command=self._copy_code)
        self.copy_btn.grid(row=0, column=1)

        # Status / resolved filenames
        self.status_var = tk.StringVar(value="")
        status = ttk.Label(panel, textvariable=self.status_var, style="Status.TLabel",
                           anchor="w", justify="left")
        status.grid(row=4, column=0, sticky="ew", pady=(6, 0))

        # Menu (change asset root, save preview)
        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Set paperdoll folder…", command=self._prompt_for_root)
        filemenu.add_command(label="Save current preview…", command=self._save_preview)
        filemenu.add_separator()
        filemenu.add_command(label="Quit", command=self.destroy)
        menubar.add_cascade(label="File", menu=filemenu)
        self.config(menu=menubar)

    # -------------------------------------------------------------- loading --

    def _prompt_for_root(self):
        folder = filedialog.askdirectory(
            title="Select the 'images/paperdoll' folder",
            initialdir=self.root_dir if os.path.isdir(self.root_dir) else os.getcwd())
        if not folder:
            if not self.char_names:
                messagebox.showwarning(
                    "No characters",
                    "No paperdoll folder selected and none found. Closing.")
            return
        names = discover_characters(folder)
        if not names:
            messagebox.showerror(
                "Nothing found",
                "That folder has no character/bottom subfolders.")
            return
        self.root_dir = folder
        self.characters.clear()
        self.char_names = names
        self.character_combo.configure(values=self.char_names)
        self.character_var.set(self.char_names[0])
        self._load_character(self.char_names[0])

    def _load_character(self, name: str):
        if name not in self.characters:
            self.characters[name] = scan_character(self.root_dir, name)
        self.active = self.characters[name]

        # Reset selection; refresh() will clamp everything to valid values.
        self.sel = {d: None for d in self.BOTTOM_DIMS + self.TOP_DIMS}
        self.refresh()

    # ------------------------------------------------------- option cascade --

    def _bottom_options(self, dim: str) -> List[str]:
        """Valid values for a bottom dimension given the higher selections."""
        idx = self.BOTTOM_DIMS.index(dim)
        higher = self.BOTTOM_DIMS[:idx]
        vals = []
        for e in self.active.bottoms:
            if all(getattr(e, h) == self.sel.get(h) for h in higher):
                vals.append(getattr(e, dim))
        return sorted_unique(vals, numeric=dim in self.NUMERIC_DIMS)

    def _top_entries(self) -> List[TopEntry]:
        return self.active.tops

    def _top_options(self, dim: str) -> List[str]:
        """Valid mood/mouth values, constrained by char_var+pose (+mood for mouth)."""
        char_var = self.sel.get("char_var")
        pose = self.sel.get("pose")
        vals = []
        for e in self._top_entries():
            if e.char_var != char_var or e.pose != pose:
                continue
            if dim == "mouth" and e.mood != self.sel.get("mood"):
                continue
            vals.append(getattr(e, dim))
        return sorted_unique(vals, numeric=False)

    def _options_for(self, dim: str) -> List[str]:
        return self._top_options(dim) if dim in self.TOP_DIMS else self._bottom_options(dim)

    def refresh(self):
        """Recompute all cascading options, clamp selections, then render."""
        if self.active is None or self._refreshing:
            return
        self._refreshing = True
        try:
            for dim in self.BOTTOM_DIMS + self.TOP_DIMS:
                options = self._options_for(dim)
                combo = self.dim_combos[dim]
                if not options:
                    self.sel[dim] = None
                    combo.configure(values=[])
                    self.dim_vars[dim].set("")
                    continue
                if self.sel.get(dim) not in options:
                    self.sel[dim] = options[0]
                combo.configure(values=[pretty(o) for o in options])
                self.dim_vars[dim].set(pretty(self.sel[dim]))
                # stash raw options for step/lookup
                combo._raw_options = options  # type: ignore[attr-defined]
        finally:
            self._refreshing = False
        self._update_code()
        self._compose()

    def _on_dim_changed(self, dim: str):
        if self._refreshing:
            return
        combo = self.dim_combos[dim]
        raw = getattr(combo, "_raw_options", [])
        i = combo.current()
        if 0 <= i < len(raw):
            self.sel[dim] = raw[i]
        self.refresh()

    def _step_dim(self, dim: str, delta: int):
        combo = self.dim_combos[dim]
        raw = getattr(combo, "_raw_options", [])
        if not raw:
            return
        cur = self.sel.get(dim)
        idx = raw.index(cur) if cur in raw else 0
        self.sel[dim] = raw[(idx + delta) % len(raw)]
        self.refresh()

    def _step_character(self, delta: int):
        if not self.char_names:
            return
        cur = self.character_var.get()
        idx = self.char_names.index(cur) if cur in self.char_names else 0
        new = self.char_names[(idx + delta) % len(self.char_names)]
        self.character_var.set(new)
        self._load_character(new)

    # ------------------------------------------------------- code generator --

    # Field order in the emitted PDAImage(...) call.
    CODE_ORDER = ["char_var", "pose", "outfit", "level", "state", "mood", "mouth"]

    @staticmethod
    def _plain_int(value: str) -> bool:
        """True for a bare integer literal (no leading zero, so it's valid Python)."""
        return value.isdigit() and str(int(value)) == value

    def _format_kv(self, dim: str, value: str) -> str:
        """Format one 'key = value' pair matching the house style."""
        # level / char_var are ints in the game defaults; emit unquoted when clean.
        if dim in ("level", "char_var") and self._plain_int(value):
            return f"{dim} = {value}"
        return f'{dim} = "{value}"'

    def _pdaimage_string(self) -> str:
        parts = []
        for dim in self.CODE_ORDER:
            if not self.include_vars[dim].get():
                continue
            value = self.sel.get(dim)
            if value in (None, ""):
                continue
            parts.append(self._format_kv(dim, value))
        return "PDAImage(" + ", ".join(parts) + ")"

    def _update_code(self):
        if hasattr(self, "code_var"):
            self.code_var.set(self._pdaimage_string())

    def _copy_code(self):
        text = self._pdaimage_string()
        self.clipboard_clear()
        self.clipboard_append(text)
        self.update()  # keep the clipboard alive after the app exits
        # Brief visual confirmation on the button.
        self.copy_btn.configure(text="Copied ✓")
        self.after(1100, lambda: self.copy_btn.configure(text="Copy PDAImage"))

    # ----------------------------------------------------------- resolution --

    def _resolve_bottom(self) -> Optional[str]:
        for e in self.active.bottoms:
            if all(getattr(e, d) == self.sel.get(d) for d in self.BOTTOM_DIMS):
                return e.path
        return None

    def _resolve_top(self) -> Optional[str]:
        for e in self._top_entries():
            if (e.char_var == self.sel.get("char_var")
                    and e.pose == self.sel.get("pose")
                    and e.mood == self.sel.get("mood")
                    and e.mouth == self.sel.get("mouth")):
                return e.path
        return None

    def _compose(self):
        """Build the full-resolution composited RGBA image for the current selection."""
        bottom_path = self._resolve_bottom()
        top_path = self._resolve_top()

        base = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
        notes = []
        for label, path in (("body", bottom_path), ("head", top_path)):
            if not path:
                notes.append(f"{label}: (missing)")
                continue
            try:
                layer = Image.open(path).convert("RGBA")
                if layer.size != base.size:
                    # Different native size: align on shared canvas (top-centered).
                    canvas = Image.new("RGBA", base.size, (0, 0, 0, 0))
                    canvas.paste(layer, (0, 0))
                    layer = canvas
                base = Image.alpha_composite(base, layer)
                notes.append(f"{label}: {os.path.basename(path)}")
            except Exception as exc:  # pragma: no cover
                notes.append(f"{label}: ERROR {exc}")

        self._composited = base
        self.status_var.set("\n".join(notes) if notes else "no image")
        self._render_preview()

    # -------------------------------------------------------------- drawing --

    def _make_backdrop(self, size: Tuple[int, int]) -> Image.Image:
        style = self.bg_style_var.get()
        if style == "Dark":
            return Image.new("RGB", size, (17, 18, 22))
        if style == "Light":
            return Image.new("RGB", size, (235, 236, 240))
        if style == "Green":
            return Image.new("RGB", size, (0, 177, 64))
        # Checkerboard
        if size in self._checker_cache:
            return self._checker_cache[size].copy()
        tile = 16
        a, b = (60, 62, 70), (44, 46, 52)
        img = Image.new("RGB", size, a)
        px = img.load()
        for y in range(size[1]):
            row = (y // tile) & 1
            for x in range(size[0]):
                if ((x // tile) & 1) ^ row:
                    px[x, y] = b
        self._checker_cache[size] = img
        return img.copy()

    def _render_preview(self):
        if self._composited is None:
            return
        cw = self.canvas.winfo_width()
        ch = self.canvas.winfo_height()
        if cw < 10 or ch < 10:
            return

        # Fit the 1200x2160 image inside the canvas, preserving aspect.
        scale = min(cw / CANVAS_W, ch / CANVAS_H)
        tw = max(1, int(CANVAS_W * scale))
        th = max(1, int(CANVAS_H * scale))

        resample = Image.LANCZOS
        fg = self._composited.resize((tw, th), resample)

        backdrop = self._make_backdrop((cw, ch))
        ox = (cw - tw) // 2
        oy = (ch - th) // 2
        backdrop.paste(fg, (ox, oy), fg)

        self._tk_image = ImageTk.PhotoImage(backdrop)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=self._tk_image)

    def _on_canvas_resize(self, _evt=None):
        # Debounce heavy re-render during drag-resize.
        if self._resize_job is not None:
            self.after_cancel(self._resize_job)
        self._resize_job = self.after(60, self._render_preview)

    # ----------------------------------------------------------------- misc --

    def _save_preview(self):
        if self._composited is None:
            return
        path = filedialog.asksaveasfilename(
            title="Save composited paperdoll",
            defaultextension=".png",
            filetypes=[("PNG image", "*.png")])
        if path:
            self._composited.save(path)
            messagebox.showinfo("Saved", f"Saved to:\n{path}")


# --------------------------------------------------------------------------- #
# Entry point
# --------------------------------------------------------------------------- #


def default_root() -> str:
    """Locate game/images/paperdoll relative to this script, with fallbacks."""
    here = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(here, "..", "game", "images", "paperdoll"),
        os.path.join(here, "game", "images", "paperdoll"),
        os.path.join(os.getcwd(), "game", "images", "paperdoll"),
    ]
    for c in candidates:
        c = os.path.normpath(c)
        if os.path.isdir(c):
            return c
    return os.path.normpath(candidates[0])


def main(argv=None):
    parser = argparse.ArgumentParser(description="Standalone Mind the School paperdoll viewer.")
    parser.add_argument("--root", default=None,
                        help="Path to the images/paperdoll folder "
                             "(default: auto-detected relative to this script).")
    args = parser.parse_args(argv)

    root_dir = os.path.normpath(args.root) if args.root else default_root()
    app = PaperdollViewer(root_dir)
    app.mainloop()


if __name__ == "__main__":
    main()
