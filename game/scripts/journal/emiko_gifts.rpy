##############################################################################
# Emiko's gifts
#
# Now and then Emiko slips a polaroid between the journal's pages: a non-canon
# extra (Patreon renders) with a typed note on its white bottom border. Once
# a gift's conditions hold, it arrives the next morning; while one is pending
# the red ribbon hangs out of the bottom of the book. Clicking the ribbon
# lets a polaroid corner slide out between the pages, clicking the corner
# pulls the photo out, and from then on it is kept in the Collectibles
# section ("From Emiko").
#
# Pending gifts belong to the save; received gifts belong to the player
# (persistent, like the replay gallery), so a gift is only ever pulled once.
# Gifts that come with an update reach existing saves the same way: the next
# morning on which their conditions hold.
#
# Register base gifts in label load_collectibles, mod gifts in a
# register_start_method loader, both with register_emiko_gifts(...).
##############################################################################

init -1 python:
    import math
    import random

    class EmikoGift:
        """
        A photo Emiko leaves in the journal.

        ### Parameters:
        1. key: str
            - Unique key; prefix mod gifts with the mod key. Never reuse a key:
                received keys are kept per player.
        2. image: str
            - The photo (16:9 fills the print); redirected into the current
                mod's folder.
        3. *conditions: Condition
            - It arrives the morning after all of them hold. Gate by progress
                so explicit shots don't arrive too early.
        4. note: str (default "")
            - Emiko's line on the polaroid's bottom border (typed, 2 short
                lines at most).
        5. title: str (default "")
            - Its name in the album.
        """

        def __init__(self, key: str, image: str, *conditions: Condition, note: str = "", title: str = ""):
            self.key = key
            self.image = get_mod_asset_path(image)
            self.conditions = ConditionStorage(*conditions)
            self.note = note
            self.title = title or "From Emiko"
            self.mod_key = active_mod_key

        def is_received(self) -> bool:
            return self.key in get_received_emiko_gifts()

    # filled by every start/after-load wave; definitions are never saved
    emiko_gift_register = {}

    def register_emiko_gifts(*gifts: EmikoGift):
        """
        Load or update gifts. Gated on the current mod being active.
        """

        for gift in gifts:
            record_mod_content("emiko_gift", gift.key)
        if not is_mod_active(active_mod_key):
            return
        for gift in gifts:
            emiko_gift_register[gift.key] = gift

    def get_received_emiko_gifts() -> List[str]:
        """
        Keys of the gifts this player has pulled out, oldest first.
        """

        return persistent.emiko_gifts_received or []

    def get_pending_emiko_gift() -> EmikoGift:
        """
        The gift waiting in the journal, or None. Several pending gifts come
        one at a time, in the order they arrived.
        """

        received = get_received_emiko_gifts()
        for key in get_game_data("emiko_gifts_pending", None) or []:
            if key in emiko_gift_register and key not in received:
                return emiko_gift_register[key]
        return None

    def deliver_emiko_gifts():
        """
        Morning check: every gift whose conditions hold now waits in the
        journal. Runs on each new day (check_new_day). Silent on purpose: the
        ribbon in the journal is the only sign that a gift is waiting.
        """

        received = get_received_emiko_gifts()
        pending = list(get_game_data("emiko_gifts_pending", None) or [])
        arrived = False
        for gift in emiko_gift_register.values():
            if gift.key in received or gift.key in pending:
                continue
            if gift.conditions.is_fulfilled():
                pending.append(gift.key)
                arrived = True
        if arrived:
            set_game_data("emiko_gifts_pending", pending)

    def receive_emiko_gift(key: str):
        """
        The gift is pulled out: kept for this player, gone from the pending
        queue of this save.
        """

        received = get_received_emiko_gifts()
        if key not in received:
            persistent.emiko_gifts_received = received + [key]
        set_game_data("emiko_gifts_pending", [pending for pending in (get_game_data("emiko_gifts_pending", None) or []) if pending != key])
        play_ui_sound("gift")
        show_notify_message("Kept in your collection", 12, "emiko|" + key)
        renpy.restart_interaction()

    def get_emiko_gifts_received_registered() -> List[EmikoGift]:
        """
        The received gifts that are still registered, oldest first (a gift
        from a switched-off mod stays received but isn't shown).
        """

        return [emiko_gift_register[key] for key in get_received_emiko_gifts() if key in emiko_gift_register]

    # the polaroid at full size: a 16:9 print, the note on the wide bottom border
    EMIKO_GIFT_SIZE = (768, 560)
    EMIKO_GIFT_PRINT = (24, 24, 720, 405)

    def emiko_gift_polaroid(gift: EmikoGift, show_note: bool = True):
        """
        The gift as a polaroid, EMIKO_GIFT_SIZE plus a 6px shadow.
        """

        width, height = EMIKO_GIFT_SIZE
        px, py, pw, ph = EMIKO_GIFT_PRINT
        children = [
            Transform(Solid("#00000038"), pos = (5, 7), xysize = (width, height)),
            Transform(Solid("#faf7f0"), xysize = (width, height)),
            Transform(journal_cover(gift.image, pw, ph), pos = (px, py)),
        ]
        if show_note and gift.note:
            # typed straight onto the strip, not handwritten (no handwriting fonts)
            border_top = py + ph
            children.append(Text(gift.note, style = "jr_typed", size = 24, text_align = 0.5, layout = "subtitle",
                xmaximum = width - 64, xpos = width // 2, xanchor = 0.5,
                ypos = border_top + (height - border_top) // 2, yanchor = 0.5))
        return Fixed(*children, xysize = (width + 6, height + 8))

    # Where the corner can slide out: the edge it crosses, the direction it
    # points to, and the stretch of that edge it may appear on. Only spots that
    # stay clear of the bookmarks (side ribbons end at ~790 left / ~590 right,
    # the exit ribbon starts at 856; the gift ribbon hangs at x 1004-1030).
    EMIKO_GIFT_EDGES = [
        # name, direction, edge point range ((x0, y0), (x1, y1))
        ("left", (-1, 0), ((280, 815), (280, 960))),
        ("right", (1, 0), ((1640, 625), (1640, 800))),
        ("bottom", (0, 1), ((400, 1016), (890, 1016))),
        ("bottom", (0, 1), ((1100, 1016), (1560, 1016))),
        # up out of the binding, between the two pages
        ("binding", (0, -1), ((960, 150), (960, 150))),
    ]
    # page rectangles of the book layer (build_book.py LEFT_PAGE / RIGHT_PAGE)
    EMIKO_GIFT_PAGES = ((280, 150, 942, 1016), (978, 150, 1640, 1016))
    # how far the tip sticks out past the page edge, and the corner's size
    EMIKO_GIFT_REACH = 58
    EMIKO_GIFT_PEEK_ZOOM = 0.36

    def emiko_gift_corners(center_x: float, center_y: float, angle: float) -> List[Tuple[float, float]]:
        """
        Corners of the peeking polaroid (Ren'Py rotates clockwise).
        """

        width = EMIKO_GIFT_SIZE[0] * EMIKO_GIFT_PEEK_ZOOM
        height = EMIKO_GIFT_SIZE[1] * EMIKO_GIFT_PEEK_ZOOM
        cos, sin = math.cos(math.radians(angle)), math.sin(math.radians(angle))
        return [(center_x + dx * cos - dy * sin, center_y + dx * sin + dy * cos)
            for dx, dy in ((-width / 2, -height / 2), (width / 2, -height / 2), (width / 2, height / 2), (-width / 2, height / 2))]

    def emiko_gift_pick_placement(sub_ribbon_count: int = 0) -> Dict[str, Any]:
        """
        A random spot for the corner. Only one corner may come out from
        under the pages: the other three have to stay hidden under the page
        the polaroid lies in (between both pages for the binding, which is
        skipped when sub-page bookmarks reach the middle of the top edge).
        """

        edges = [edge for edge in EMIKO_GIFT_EDGES if edge[0] != "binding" or sub_ribbon_count <= 3]
        for attempt in range(200):
            name, (ux, uy), ((x0, y0), (x1, y1)) = random.choice(edges)
            t = random.random()
            edge_x, edge_y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
            # any turn that brings a corner, not a flat side, out first
            angle = random.uniform(-180, 180)
            if not 20 <= abs(angle) % 90 <= 70:
                continue

            corners = emiko_gift_corners(0, 0, angle)
            # the corner furthest out (no max(key=...): helper.rpy shadows max in the store)
            tip_index = 0
            for index in range(1, 4):
                if corners[index][0] * ux + corners[index][1] * uy > corners[tip_index][0] * ux + corners[tip_index][1] * uy:
                    tip_index = index
            # a corner of the wide bottom border: mostly white shows, little of the photo
            if tip_index not in (2, 3):
                continue
            tip = corners[tip_index]
            center_x = edge_x + ux * EMIKO_GIFT_REACH - tip[0]
            center_y = edge_y + uy * EMIKO_GIFT_REACH - tip[1]

            if name == "binding":
                area = (EMIKO_GIFT_PAGES[0][0], EMIKO_GIFT_PAGES[0][1], EMIKO_GIFT_PAGES[1][2], EMIKO_GIFT_PAGES[0][3])
            else:
                area = EMIKO_GIFT_PAGES[0] if edge_x < 960 else EMIKO_GIFT_PAGES[1]
            inside = all(area[0] + 4 < x < area[2] - 4 and area[1] + 4 < y < area[3] - 4
                for x, y in emiko_gift_corners(center_x, center_y, angle)
                if abs(x - (edge_x + ux * EMIKO_GIFT_REACH)) > 1 or abs(y - (edge_y + uy * EMIKO_GIFT_REACH)) > 1)
            if inside:
                return {
                    "name": name,
                    "angle": angle,
                    "center": (int(center_x), int(center_y)),
                    # the part outside the page, where the corner can be clicked
                    "hit": (int(edge_x + ux * EMIKO_GIFT_REACH / 2), int(edge_y + uy * EMIKO_GIFT_REACH / 2)),
                    "slide": (ux, uy),
                }

        # practically never reached (every edge finds a spot within a few tries):
        # a known-good spot at the bottom of the left page
        return {"name": "bottom", "angle": -35.0, "center": (640, 912), "hit": (585, 1045), "slide": (0, 1)}

    # the corner currently out, or None; reset whenever a journal page opens
    emiko_gift_state = {"placement": None}

    def emiko_gift_in_journal() -> EmikoGift:
        """
        The pending gift if the journal is open as itself (not from the title
        screen, not as the game menu mid event, not in a replay).
        """

        if journal_title_mode() or journal_in_game_menu() or is_in_replay:
            return None
        return get_pending_emiko_gift()

    def emiko_gift_toggle_corner(sub_ribbon_count: int = 0):
        """
        Ribbon click: a corner slides out somewhere, or back in.
        """

        if emiko_gift_state["placement"] is None:
            emiko_gift_state["placement"] = emiko_gift_pick_placement(sub_ribbon_count)
        else:
            emiko_gift_state["placement"] = None

    def emiko_gift_pull(key: str):
        placement = emiko_gift_state["placement"]
        emiko_gift_state["placement"] = None
        renpy.show_screen("emiko_gift_reveal", key, placement["center"], placement["angle"])

    def emiko_gift_hit_mask(placement: Dict[str, Any]):
        """
        Focus mask of the corner button: a box around the part sticking out
        (the button itself covers the whole screen).
        """

        size = 104
        hx, hy = placement["hit"]
        return Fixed(Transform(Solid("#fff"), xysize = (size, size), pos = (hx - size // 2, hy - size // 2)), xysize = (1920, 1080))

# the ribbon drops a little on hover
transform emiko_gift_ribbon_hover:
    on idle:
        easein 0.15 yoffset 0
    on hover:
        easein 0.15 yoffset 8

# the corner slides out from between the pages ...
transform emiko_gift_slide_in(ux, uy):
    xoffset (-ux * 70) yoffset (-uy * 70)
    easein 0.5 xoffset 0 yoffset 0

# ... and a bit further on hover, as a hint that it can be pulled
transform emiko_gift_peek_hover(ux, uy):
    on idle:
        easein 0.18 xoffset 0 yoffset 0
    on hover:
        easein 0.18 xoffset (ux * 18) yoffset (uy * 18)

# pulled out: from the corner's spot to the middle of the screen, upright
transform emiko_gift_fly_out(start, angle):
    subpixel True
    anchor (0.5, 0.5)
    pos start rotate angle zoom EMIKO_GIFT_PEEK_ZOOM
    easein 0.6 pos (960, 520) rotate -2.5 zoom 1.0

transform emiko_gift_dim:
    alpha 0.0
    easein 0.4 alpha 1.0

transform emiko_gift_hint:
    alpha 0.0
    pause 0.8
    easein 0.4 alpha 1.0

#############################
# region Journal book ---- #
#############################

screen emiko_gift_corner(gift, placement):
    # """
    # The corner sliding out between the pages. Drawn UNDER the page layer
    # (journal_book), so the pages hide all but the part beyond their edge;
    # the button covers the screen but only takes focus around that part.
    # """

    $ ux, uy = placement["slide"]
    button:
        style "empty"
        xysize (1920, 1080)
        focus_mask emiko_gift_hit_mask(placement)
        action Function(emiko_gift_pull, gift.key)
        add Transform(emiko_gift_polaroid(gift, show_note = False), rotate = placement["angle"], zoom = EMIKO_GIFT_PEEK_ZOOM):
            pos placement["center"]
            anchor (0.5, 0.5)
            at emiko_gift_slide_in(ux, uy), emiko_gift_peek_hover(ux, uy)

screen emiko_gift_ribbon(action):
    # """
    # The red ribbon hanging out of the bottom of the book, drawn above the
    # page layer (its root lies on the paper). Only there while a gift waits.
    # """

    imagebutton:
        idle "gui/journal/book_ribbon.webp"
        focus_mask True
        at emiko_gift_ribbon_hover
        action action

screen emiko_gift_reveal(key, start, angle):
    # """
    # The pulled-out polaroid, big, with Emiko's note. A click (or ESC) keeps
    # it: it goes into the album and stops being pending.
    # """

    zorder 85
    modal True

    $ gift = emiko_gift_register.get(key)

    if gift is not None:
        add Solid("#0b0806d0") at emiko_gift_dim

        button:
            style "empty"
            xysize (1920, 1080)
            action [Function(receive_emiko_gift, key), Hide("emiko_gift_reveal", dissolveM)]
            add emiko_gift_polaroid(gift) at emiko_gift_fly_out(start, angle)

        text "Click to keep it" style "jr_typed_small" color "#e8dcc4" xalign 0.5 ypos 1030 at emiko_gift_hint

        key "K_ESCAPE" action [Function(receive_emiko_gift, key), Hide("emiko_gift_reveal", dissolveM)]

# endregion
#############################

########################
# region Album ------ #
########################

screen journal_emiko_gifts_album(picked):
    # """
    # Left page of the Collectibles section's "From Emiko" sub page: the
    # received gifts as small polaroids, oldest first.
    # """

    $ gifts = get_emiko_gifts_received_registered()

    use jr_page("journal_emiko_gifts_album", JR_LEFT_X, JR_LEFT_W):
        vbox:
            xsize JR_LEFT_W
            text "From Emiko" style "jr_title"
            null height 4
            use jr_double_rule(JR_LEFT_W)
            null height 8
            text ("1 photo so far" if len(gifts) == 1 else "{} photos so far".format(len(gifts))) style "jr_typed_small"
            null height 22
            vpgrid:
                cols 4
                xspacing 16
                yspacing 18
                for gift in gifts:
                    button:
                        style "empty"
                        xysize (126, 100)
                        action [With(dissolveM), Call("open_journal", 12, "emiko|" + gift.key)]
                        tooltip gift.title
                        at collectible_spot_hover
                        add Transform(emiko_gift_polaroid(gift, show_note = False), zoom = 0.155, rotate_pad = False,
                            rotate = (-2.0 if picked is not None and picked.key == gift.key else 1.5))

screen journal_emiko_gift_detail(picked):
    # """
    # Right page: the picked gift with its note, click to see the photo big.
    # """

    use jr_page("journal_emiko_gift_detail", JR_RIGHT_X, JR_RIGHT_W):
        vbox:
            xsize JR_RIGHT_W
            if picked is None:
                text "Nothing yet" style "jr_title"
                null height 4
                use jr_double_rule(JR_RIGHT_W)
            else:
                text picked.title style "jr_title"
                null height 4
                use jr_double_rule(JR_RIGHT_W)
                null height 30
                button:
                    style "empty"
                    xalign 0.5
                    action SetScreenVariable("zoomed_image", picked.image)
                    add Transform(emiko_gift_polaroid(picked), zoom = (JR_RIGHT_W - 24) / EMIKO_GIFT_SIZE[0], rotate = -1.5, rotate_pad = False)

# endregion
########################
