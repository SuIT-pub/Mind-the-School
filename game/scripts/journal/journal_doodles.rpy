##############################################################################
# Pencil notes: short handwritten-looking words (with an optional arrow),
# composed at runtime from the glyph kit drawn by
# tools/journal_assets/build_doodles.py (doodles/glyphs, doodles/arrows).
#
# Every character exists in a few hand-drawn variants; a word picks variants,
# a small baseline wobble and spacing from a seed, so the same note always
# looks the same but no two words share their letters' shapes exactly.
# Meant for one to three words: longer text would show the shared shapes.
##############################################################################

init python:
    import json
    import zlib
    import functools

    JOURNAL_PENCIL_INKS = {
        "pencil": "#4e4842",
        "red": "#962e28",
    }
    JOURNAL_GLYPH_DIR = "gui/journal/doodles/glyphs/"
    JOURNAL_ARROW_DIR = "gui/journal/doodles/arrows/"
    JOURNAL_GLYPH_VARIANTS = 3
    JOURNAL_ARROW_VARIANTS = 2

    def _journal_glyph_metrics():
        try:
            with renpy.open_file(JOURNAL_GLYPH_DIR + "metrics.json") as f:
                return json.loads(f.read().decode("utf-8"))
        except Exception:
            return None

    journal_glyph_metrics = _journal_glyph_metrics()

    def journal_note_seed(*parts) -> int:
        # crc32, not hash(): str hashes change between runs, the note must not
        return zlib.crc32("|".join(str(p) for p in parts).encode("utf-8"))

    @functools.lru_cache(maxsize = 256)
    def journal_pencil_word(text: str, ink: str = "pencil", size: int = 22, seed: int = 0):
        """
        A word in pencil handwriting.

        ### Returns:
        1. Tuple[Displayable, int, int]
            - the word, its width and height in pixels
        """

        metrics = journal_glyph_metrics
        if not metrics:
            word = Text(text, style = "jr_text", size = size, color = JOURNAL_PENCIL_INKS.get(ink, ink))
            w, h = word.size()
            return word, int(w), int(h)

        zoom = size / float(metrics["cap"])
        tint = TintMatrix(JOURNAL_PENCIL_INKS.get(ink, ink))
        rng = renpy.random.Random(seed or journal_note_seed(text, ink))
        advance = metrics["advance"]
        space = advance["32"]
        origin = metrics["origin_x"] * zoom
        height = int(metrics["height"] * zoom)

        letters = []
        pen = 0.0
        for ch in text:
            code = str(ord(ch))
            if ch == " " or code not in advance:
                pen += space * zoom
                continue
            variant = rng.randrange(JOURNAL_GLYPH_VARIANTS)
            dy = rng.uniform(-1.4, 1.4) * zoom
            letters.append(Transform("{}{}_{}.webp".format(JOURNAL_GLYPH_DIR, code, variant),
                zoom = zoom, matrixcolor = tint, xpos = int(pen), ypos = int(dy)))
            pen += advance[code] * zoom * rng.uniform(0.94, 1.03)

        width = int(pen + origin * 2 + 6 * zoom)
        word = Fixed(*letters, xysize = (width, height))
        return word, width, height

    @functools.lru_cache(maxsize = 256)
    def journal_pencil_note(text: str, arrow: str = None, ink: str = "pencil", size: int = 22, seed: int = 0):
        """
        A pencil word with an arrow pointing at something next to it.

        arrow: None, "left", "right", "up_left", "up_right", "down_left",
        "down_right" — the direction the arrow points, seen from the word.

        ### Returns:
        1. Tuple[Displayable, int, int]
            - the note, its width and height
        """

        seed = seed or journal_note_seed(text, arrow, ink)
        word, ww, wh = journal_pencil_word(text, ink, size, seed)
        if not arrow:
            return word, ww, wh

        path = "{}{}_{}.webp".format(JOURNAL_ARROW_DIR, arrow, seed % JOURNAL_ARROW_VARIANTS)
        if not renpy.loadable(path):
            return word, ww, wh
        aw, ah = journal_image_size(path)
        tint = TintMatrix(JOURNAL_PENCIL_INKS.get(ink, ink))
        # the middle of the letters, where an arrow would naturally start from
        mid = int(wh * 0.55)

        if arrow == "left":
            positions = ((0, max(0, mid - ah // 2)), (aw - 4, max(0, ah // 2 - mid)))
        elif arrow == "right":
            positions = ((ww - 4, max(0, mid - ah // 2)), (0, max(0, ah // 2 - mid)))
        elif arrow == "down_left":
            positions = ((0, int(wh * 0.7)), (int(aw * 0.55), 0))
        elif arrow == "down_right":
            positions = ((max(0, ww - int(aw * 0.45)), int(wh * 0.7)), (0, 0))
        elif arrow == "up_left":
            positions = ((0, 0), (int(aw * 0.55), int(ah * 0.6)))
        else:  # up_right
            positions = ((max(0, ww - int(aw * 0.45)), 0), (0, int(ah * 0.6)))

        (ax, ay), (wx, wy) = positions
        note = Fixed(
            Transform(path, matrixcolor = tint, xpos = ax, ypos = ay),
            Transform(word, xpos = wx, ypos = wy),
            xysize = (max(ax + aw, wx + ww), max(ay + ah, wy + wh)))
        return note, max(ax + aw, wx + ww), max(ay + ah, wy + wh)

screen jr_pencil_note(text, arrow = None, ink = "pencil", size = 22, seed = 0):
    # """
    # A short pencil note, optionally with an arrow (see journal_pencil_note).
    # """

    $ note, note_w, note_h = journal_pencil_note(text, arrow, ink, size, seed)
    add note

screen jr_new_mark(seed_key = ""):
    # """
    # A red pencil "new" next to a journal entry with unseen changes.
    # """

    $ note, note_w, note_h = journal_pencil_note("new", None, "red", 17, journal_note_seed("new", seed_key))
    add note yalign 0.5 yoffset -2
