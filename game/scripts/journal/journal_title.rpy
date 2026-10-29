##############################################################################
# Main menu (title screen) in the journal's look.
#
# The journal peeks in from the left edge: its outer page lists the menu,
# two ribbons on its edge switch the background animation / image. Patreon
# polaroids (journal_news.rpy) and link stickers sit top right, the changelog is a folded sheet that opens
# like the patron list, the logo is a brass plaque on leather bottom right.
# Load / Settings / Mods / Credits slide the journal open (journal_title):
# the same pages as the in-game game menu, with only the ribbons that make
# sense before a game runs.
#
# Zones the background renders must keep free: tools/journal_assets/
# main_menu_render_template.png (book strip left, notes top right, plaque).
##############################################################################

init python:
    # the book image is 1920 wide; shifted this far left only its outer page shows
    JOURNAL_TITLE_BOOK_X = -1290
    JOURNAL_TITLE_TABS = [("load", "Load"), ("settings", "Settings"), ("mods", "Mods"), ("backgrounds", "Backgrounds")]

    def journal_title_mode() -> bool:
        """
        True on the title screen and the pages opened from it: no game runs.
        """

        return bool(main_menu)

    def journal_changelog_panels():
        """
        Flows CHANGELOG into fold-out panels by an estimate of the rows each
        line wraps into (Crimson Pro 20px is about 9.5px per character).
        """

        row_chars = {0: 36, 1: 33}
        panels = [[]]
        capacity = JOURNAL_FOLDOUT_FIRST_ROWS + 4
        used = 0

        def place(item, rows):
            nonlocal capacity, used
            if used + rows > capacity and panels[-1]:
                panels.append([])
                capacity = JOURNAL_FOLDOUT_ROWS + 3
                used = 0
            panels[-1].append(item)
            used += rows

        for title, sections in CHANGELOG:
            place(("version", title), 3)
            for heading, lines in sections:
                if heading:
                    place(("section", heading), 2)
                for line in lines:
                    text, level = (line if isinstance(line, tuple) else (line, 0))
                    place(("line", text, level), max(1, -(-len(text) // row_chars.get(level, 33))))
        place(("footer", CHANGELOG_FOOTER), 3)
        return panels

default journal_title_slide = False

transform jr_title_book_in:
    # the peeking book slides open into the middle of the screen
    xoffset JOURNAL_TITLE_BOOK_X
    easein 0.4 xoffset 0

style jr_title_entry is jr_entry_button
style jr_title_entry_text is jr_entry_button_text:
    font JR_FONT_MEDIUM
    size 40
    insensitive_color JR_PENCIL + "80"

##################
# region Title

screen main_menu():

    ## replaces any other menu screen
    tag menu

    default changelog_open = False

    add gui.main_menu_background

    # ---- the journal, peeking in from the left
    fixed:
        xpos JOURNAL_TITLE_BOOK_X
        ypos 10
        xysize (1920, 1080)

        add "gui/journal/book_cover.webp"

        # background controls as ribbons low on the page edge: still/animated, next, picker
        $ animated = bool(persistent.title_bg_animate)
        imagebutton:
            idle "gui/journal/ribbons/title_{}_idle.webp".format("anim_pause" if animated else "anim_play")
            pos (1620 - 14, 752 - 44)
            focus_mask True
            at jr_ribbon_slide(10)
            tooltip ("Still image" if animated else "Animated background")
            action Function(toggle_animation)
        imagebutton:
            idle "gui/journal/ribbons/title_bg_next_idle.webp"
            pos (1620 - 14, 842 - 44)
            focus_mask True
            at jr_ribbon_slide(10)
            tooltip "Next background"
            action Function(switch_background)
        imagebutton:
            idle "gui/journal/ribbons/title_bg_grid_idle.webp"
            pos (1620 - 14, 932 - 44)
            focus_mask True
            at jr_ribbon_slide(10)
            tooltip "Choose a background"
            action [SetVariable("journal_title_slide", True), ShowMenu("journal_title", "backgrounds")]

        add "gui/journal/book_pages.webp"

        vbox:
            pos (1372, 200)
            xsize 250
            spacing 2

            hbox:
                spacing 10
                text "MAIN MENU" style "jr_rubric" yalign 0.5
                add Solid(JR_ACCENT + "90") xysize (110, 1) yalign 0.6
            text "v[config.version]" style "jr_typed_small"
            null height 30

            if refresh_game:
                text "Mods changed — please restart the game.":
                    style "jr_typed"
                    size 17
                    color JR_ACCENT
                    xsize 250
                null height 14

            $ newest = renpy.newest_slot()
            textbutton "Continue":
                style "jr_title_entry"
                sensitive (newest is not None and not refresh_game)
                tooltip "Load the most recent save"
                action FileLoad(newest, slot = True)
            textbutton "New Game":
                style "jr_title_entry"
                sensitive (not refresh_game)
                action Start()
            textbutton "Load":
                style "jr_title_entry"
                sensitive (not refresh_game)
                action [SetVariable("journal_title_slide", True), ShowMenu("journal_title", "load")]
            textbutton "Settings":
                style "jr_title_entry"
                action [SetVariable("journal_title_slide", True), ShowMenu("journal_title", "settings")]
            textbutton "Mods":
                style "jr_title_entry"
                action [SetVariable("journal_title_slide", True), ShowMenu("journal_title", "mods")]
            if renpy.variant("pc"):
                null height 26
                textbutton "Quit":
                    style "jr_title_entry"
                    text_color JR_ACCENT
                    action Quit(confirm = False)

    # ---- link stickers
    hbox:
        pos (1652, 18)
        spacing -6
        for icon, icon_size, label, target in (("gui/wiki.png", (50, 50), "Wiki", "open_wiki_link_from_menu"),
                ("gui/discord.png", (58, 44), "Discord", "open_discord_link_from_menu"),
                ("gui/patreon.png", (48, 48), "Patreon", "open_patreon_link_from_menu")):
            button:
                xysize (92, 92)
                padding (0, 0, 0, 0)
                background None
                tooltip label
                action Call(target)
                add "gui/journal/ui/sticker_blank.webp"
                add Transform(icon, fit = "contain", xysize = icon_size) pos (44, 44) anchor (0.5, 0.5)

    # ---- changelog, a folded sheet
    button:
        pos (1660, 130)
        xysize (190, 170)
        padding (0, 0, 0, 0)
        background None
        tooltip "Unfold the changelog"
        action SetScreenVariable("changelog_open", True)
        fixed at Transform(rotate = 3, rotate_pad = False):
            xysize (190, 170)
            for i in (2, 1, 0):
                add Solid("#00000026") pos (i * 6 + 4, i * 5 + 5) xysize (170, 140)
                add Transform("gui/journal/ui/foldout_panel.webp", xysize = (170, 140)) pos (i * 6, i * 5)
            vbox:
                pos (18, 18)
                spacing 4
                text "WHAT'S NEW" style "jr_rubric" size 15
                text "in v[config.version]" style "jr_typed" size 19
            text "unfold ›" style "jr_typed_small" pos (18, 108)

    # ---- the logo: brass plaque on leather, version engraved at runtime
    fixed:
        pos (1290, 838)
        xysize (628, 238)
        add "gui/journal/ui/title_plaque.webp"
        # engraving: a light lip under dark letters, like the title on the plaque
        text "v[config.version]" font JR_FONT_MEDIUM size 22 color "#ffffff70" pos (314, 148) anchor (0.5, 0.5)
        text "v[config.version]" font JR_FONT_MEDIUM size 22 color "#462c0eeb" pos (314, 146) anchor (0.5, 0.5)

    # ---- Patreon polaroids top right, the developer's note on the plaque
    use news_board

    use journal_tooltip

    if changelog_open:
        use journal_changelog_foldout()
        key "K_ESCAPE" action SetScreenVariable("changelog_open", False)

screen journal_changelog_foldout():
    # """
    # The changelog unfolded over the title screen, panel by panel.
    # """

    $ panels = journal_changelog_panels()
    $ sheet_w = len(panels) * (JOURNAL_FOLDOUT_PANEL_W + 6)
    $ view_w = min(sheet_w, 1840)
    $ pad = 36
    $ inner_w = JOURNAL_FOLDOUT_PANEL_W - pad * 2

    button:
        xysize (1920, 1080)
        background Solid("#140d08a0")
        action SetScreenVariable("changelog_open", False)

    viewport:
        xsize view_w
        ysize JOURNAL_FOLDOUT_PANEL_H + 10
        xalign 0.5
        ypos 96
        mousewheel "horizontal"
        draggable True

        hbox:
            for index, panel in enumerate(panels):
                fixed:
                    xysize (JOURNAL_FOLDOUT_PANEL_W + 6, JOURNAL_FOLDOUT_PANEL_H + 8)
                    fixed at jr_unfold(index * 0.09):
                        xysize (JOURNAL_FOLDOUT_PANEL_W, JOURNAL_FOLDOUT_PANEL_H)
                        add Solid("#00000033") pos (3, 5) xysize (JOURNAL_FOLDOUT_PANEL_W, JOURNAL_FOLDOUT_PANEL_H)
                        add "gui/journal/ui/foldout_panel.webp"

                        vbox:
                            pos (pad, pad)
                            xsize inner_w

                            if index == 0:
                                text "What's new" style "jr_title" size 46
                                null height 2
                                use jr_double_rule(inner_w)
                                null height 12

                            for item in panel:
                                if item[0] == "version":
                                    null height 10
                                    text item[1] style "jr_text" size 26 font JR_FONT_BOLD
                                    null height 6
                                elif item[0] == "section":
                                    null height 6
                                    use jr_rubric(item[1], inner_w)
                                    null height 4
                                elif item[0] == "line":
                                    hbox:
                                        xoffset (24 if item[2] else 0)
                                        spacing 8
                                        text ("–" if item[2] else "•") style "jr_text" size 20 color JR_PENCIL
                                        text item[1] style "jr_text" size 20 xsize (inner_w - 20 - (24 if item[2] else 0))
                                else:
                                    null height 14
                                    text item[1] style "jr_small" size 19

                        if index == len(panels) - 1:
                            textbutton "Fold it up ›":
                                style "jr_cheat_link"
                                xalign 1.0
                                yalign 1.0
                                xoffset -pad
                                yoffset -pad + 10
                                action SetScreenVariable("changelog_open", False)

# endregion
##################

#######################
# region Title journal

screen journal_title(tab = "load"):
    # """
    # The journal opened from the title screen: Load / Settings / Mods as
    # sub pages of the menu ribbon, plus Credits. Close returns to the title.
    # """

    tag menu

    default selected_mod = None
    default picked_background = None
    default unfolded = False
    $ slide = journal_title_slide
    on "show" action SetVariable("journal_title_slide", False)
    on "replace" action SetVariable("journal_title_slide", False)

    use journal_backdrop

    key "K_ESCAPE" action journal_close_action()

    fixed:
        if slide:
            at jr_title_book_in

        if tab == "credits":
            use journal_page_selector(6, "")
            use journal_credits_pages("")
        else:
            $ sub_entries = [(label, (key == tab), ShowMenu("journal_title", key)) for key, label in JOURNAL_TITLE_TABS]
            use journal_page_selector(11, tab, sub_entries = sub_entries)
            if tab == "settings":
                use journal_menu_settings()
            elif tab == "mods":
                use journal_menu_mods(selected_mod)
            elif tab == "backgrounds":
                use journal_menu_backgrounds(picked_background)
            else:
                use journal_menu_files("load")

    use journal_tooltip

    if tab == "credits" and unfolded:
        $ tiers, updated = journal_patron_tiers()
        use journal_patron_foldout(tiers, updated)
        key "K_ESCAPE" action SetScreenVariable("unfolded", False)

screen journal_menu_mods(selected_mod = None):
    # """
    # Mods: the available mods on the left, the picked one on the right.
    # Switching a mod needs a restart (refresh_game, like the old manager).
    # """

    $ mods = [(key, mod) for key, mod in persistent.modList.items() if mod['available']]
    $ picked = selected_mod if selected_mod in persistent.modList else (mods[0][0] if mods else None)

    use jr_page("journal_menu_mods_list", JR_LEFT_X, JR_LEFT_W):
        vbox:
            xsize JR_LEFT_W
            text "Mods" style "jr_title"
            null height 4
            use jr_double_rule(JR_LEFT_W)
            null height 10
            text "Switching a mod on or off needs a restart of the game. Only install mods you trust: mods can contain code, and their makers are responsible for it." style "jr_small"
            if refresh_game:
                null height 10
                text "Mods changed — please restart the game." style "jr_typed" size 17 color JR_ACCENT

            null height 24
            use jr_rubric("Installed", JR_LEFT_W)
            null height 4
            for mod_key, mod in mods:
                fixed:
                    xysize (JR_LEFT_W, 40)
                    button:
                        style "jr_entry_button"
                        yalign 0.5
                        selected (mod_key == picked)
                        action SetScreenVariable("selected_mod", mod_key)
                        hbox:
                            spacing 12
                            add ("gui/journal/ui/box_full.webp" if mod['active'] else "gui/journal/ui/box_empty.webp") yalign 0.5
                            text mod['name'] style "jr_entry_button_text" size 24
                    text ("on" if mod['active'] else "off") style "jr_text" size 20 font "fonts/CrimsonPro-Italic.ttf" color (JR_GREEN if mod['active'] else JR_PENCIL) xalign 1.0 yalign 0.5

            use journal_menu_leave_links

    if picked is not None:
        $ mod = persistent.modList[picked]
        use jr_page("journal_menu_mods_detail", JR_RIGHT_X, JR_RIGHT_W):
            vbox:
                xsize JR_RIGHT_W
                text mod['name'] style "jr_title" size 44
                null height 4
                use jr_double_rule(JR_RIGHT_W)
                null height 10
                text "by {} · version {}".format(mod['author'], mod['version']) style "jr_typed_small"

                $ summary = get_mod_content_summary(picked)

                null height 20
                use jr_rubric("What it adds", JR_RIGHT_W)
                null height 4
                for label, value in summary["content"]:
                    use journal_credit_row(label, value)
                if not summary["content"]:
                    text "Nothing yet." style "jr_small"
                if summary["note"]:
                    null height 6
                    text summary["note"] style "jr_small"

                if summary["changes"]:
                    null height 20
                    use jr_rubric("What it changes", JR_RIGHT_W)
                    null height 4
                    for label, value in summary["changes"]:
                        use journal_credit_row(label, value)
                if summary["conflicts"]:
                    null height 6
                    text "Changes the same things as: {}".format(", ".join(summary["conflicts"])) style "jr_small" color JR_ACCENT

                # its kinks, settable here too (also before switching it on);
                # a kink shared with other mods has one setting for all of them
                $ mod_kinks = get_mod_kinks(picked)
                if mod_kinks:
                    null height 20
                    use jr_rubric("Kinks", JR_RIGHT_W)
                    null height 4
                    use kink_setting_rows(mod_kinks, JR_RIGHT_W)

                null height 20
                use jr_rubric("Description", JR_RIGHT_W)
                null height 6
                text mod['description'] style "jr_body"

                null height 24
                if mod['key'] == "base":
                    text "The base game is always on." style "jr_small"
                elif mod['active']:
                    textbutton "Switch it off ›":
                        style "jr_cheat_link"
                        action [Function(deactivate_mod, mod['key']), SetVariable("refresh_game", True)]
                else:
                    textbutton "Switch it on ›":
                        style "jr_cheat_link"
                        action [Function(activate_mod, mod['key']), SetVariable("refresh_game", True)]

# endregion
#######################

screen journal_menu_backgrounds(picked_background = None):
    # """
    # Background picker: sets, single images and videos from gui/bg/ on the
    # left, the picked one's images as a grid on the right. A set plays as
    # an animation; a clicked image becomes the still background.
    # """

    python:
        title_background_display(0, 0)  # makes sure the remembered choices exist
        entries = title_bg_entries
        current = title_bg_entry(picked_background) or title_bg_entry(persistent.title_bg_anim) or (entries[0] if entries else None)

    use jr_page("journal_menu_bg_list", JR_LEFT_X, JR_LEFT_W):
        vbox:
            xsize JR_LEFT_W
            text "Backgrounds" style "jr_title"
            null height 4
            use jr_double_rule(JR_LEFT_W)
            null height 20
            use jr_setting_choices("Animation", [("on", Function(title_bg_play, persistent.title_bg_anim)), ("off", Function(title_bg_pick_still, persistent.title_bg_still))])
            # slideshow tempo for image sets (videos keep their own speed)
            fixed:
                xysize (JR_LEFT_W, 40)
                text "Slideshow speed" style "jr_text" size 22 yalign 0.5
                bar:
                    value FieldValue(persistent, "title_bg_speed", 1.0, max_is_zero = False, step = 0.05)
                    style "jr_slider"
                    xalign 1.0

            null height 18
            use jr_rubric("Sets and videos", JR_LEFT_W)
            null height 4
            for entry in entries:
                $ playing = (persistent.title_bg_animate and entry.key == persistent.title_bg_anim) or (not persistent.title_bg_animate and persistent.title_bg_still in entry.frames)
                fixed:
                    xysize (JR_LEFT_W, 40)
                    button:
                        style "jr_entry_button"
                        yalign 0.5
                        selected (current is not None and entry.key == current.key)
                        action SetScreenVariable("picked_background", entry.key)
                        text entry.label style "jr_entry_button_text" size 24
                    hbox:
                        xalign 1.0
                        yalign 0.5
                        spacing 12
                        if playing:
                            text "on screen" style "jr_text" size 19 font "fonts/CrimsonPro-Italic.ttf" color JR_GREEN yalign 0.5
                        text ("video" if entry.kind == "video" else "{} images".format(len(entry.frames)) if entry.kind == "set" else "image"):
                            style "jr_small"
                            size 18
                            yalign 0.5

            use journal_menu_leave_links

    if current is not None:
        $ cols = 3
        $ gap = 14
        $ cell_w = (JR_RIGHT_W - gap * (cols - 1)) // cols
        $ cell_h = int(cell_w * 9 / 16)
        use jr_page("journal_menu_bg_frames", JR_RIGHT_X, JR_RIGHT_W):
            vbox:
                xsize JR_RIGHT_W
                text current.label style "jr_title" size 44
                null height 4
                use jr_double_rule(JR_RIGHT_W)
                null height 12

                if current.animated:
                    textbutton ("Play this video ›" if current.kind == "video" else "Play as animation ›"):
                        style "jr_cheat_link"
                        action Function(title_bg_play, current.key)
                    null height 12

                if current.kind == "video":
                    text "A video plays as it is; pick one of the images for a still background." style "jr_small"
                else:
                    text "Click an image to keep it as a still background." style "jr_small"
                    null height 10
                    $ rows = (len(current.frames) + cols - 1) // cols
                    grid cols rows:
                        xspacing gap
                        yspacing gap
                        for frame_path in current.frames:
                            $ chosen = (not persistent.title_bg_animate and persistent.title_bg_still == frame_path)
                            button:
                                xysize (cell_w, cell_h)
                                padding (0, 0, 0, 0)
                                background (Solid(JR_ACCENT) if chosen else Solid("#faf7f0"))
                                action Function(title_bg_pick_still, frame_path)
                                add journal_cover(frame_path, cell_w - 8, cell_h - 8) pos (4, 4)
                        for _ in range(rows * cols - len(current.frames)):
                            null
