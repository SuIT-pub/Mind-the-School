##############################################################################
# Journal: Credits (page 6)
#
# Left page: thanks to the patrons and how to support the game. The patron
# list itself is a folded sheet tucked into the page: it unfolds over the
# whole book into as many panels as the list needs, so it can grow without
# ever being squeezed into a page column.
# Right page: who made the game and what it is made with (the About
# screen's credits plus the journal binder's own sources).
#
# display = "" or "patrons" (opens with the sheet unfolded)
##############################################################################

init python:
    JOURNAL_FOLDOUT_PANEL_W = 420
    JOURNAL_FOLDOUT_PANEL_H = 880
    JOURNAL_FOLDOUT_ROW_H = 30
    # rows a panel holds below its padding; the first panel also carries the heading
    JOURNAL_FOLDOUT_ROWS = 26
    JOURNAL_FOLDOUT_FIRST_ROWS = 20

    JOURNAL_CREDIT_TIERS = [("Teacher", "Teacher tier"), ("Student", "Student tier")]

    # (what, credit, link) — the same credits as the About screen in the game menu
    JOURNAL_GAME_ASSET_CREDITS = [
        ("Game artwork", "© 2023 SuIT-JI · CC BY 4.0", "https://creativecommons.org/licenses/by/4.0/"),
        ("External link icon", "Icons8", "https://icons8.com/icon/82787/externer-link"),
        ("Icons", "Game-icons.net", "https://game-icons.net/"),
        ("Notepad vectors", "Lovepik.com", "https://lovepik.com/images/png-notepad.html"),
        ("Journal & menu icons", "Flaticon", "https://www.flaticon.com/"),
        # per-file sources and licences of the ambience loops: game/audio/ambience/CREDITS.txt
        ("Crowd ambience", "joedeshon · CC BY 4.0", "https://freesound.org/people/joedeshon/sounds/119412/"),
        ("Ambience", "Freesound · CC0", "https://freesound.org/"),
        # per-track titles and licences (CC BY / CC BY-SA 4.0): game/audio/music/CREDITS.txt
        ("Music", "Purrple Cat · CC BY / BY-SA 4.0", "https://freemusicarchive.org/music/purrple-cat/"),
        # per-file sources and edits of the interface sounds: game/audio/ui/CREDITS.txt
        ("Journal sound", "Sabacky · CC BY 4.0", "https://freesound.org/people/Sabacky/sounds/774136/"),
        ("Photo sound", "egomassive, F4ngy · CC BY 3.0", "https://freesound.org/people/egomassive/sounds/536784/"),
        ("Level-up bowl", "Valerie-Vivegnis · CC BY 4.0", "https://freesound.org/people/Valerie-Vivegnis/sounds/864397/"),
        ("Interface sounds", "Freesound · CC0", "https://freesound.org/"),
    ]

    # (what, credit, link) for everything the journal binder is built from
    JOURNAL_ASSET_CREDITS = [
        ("Leather", "Poly Haven · CC0", "https://polyhaven.com/a/fabric_leather_02"),
        ("Paper", "ambientCG · CC0", "https://ambientcg.com/view?id=Paper001"),
        ("Icons", "Material Symbols · Apache 2.0", "https://fonts.google.com/icons"),
        ("Typeface", "Crimson Pro · OFL", "https://github.com/Fonthausen/CrimsonPro"),
        ("Typewriter", "Special Elite · Apache 2.0", "https://fonts.google.com/specimen/Special+Elite"),
        # the Hershey licence asks for this acknowledgement (full text in gui/journal/NOTICE.txt)
        ("Doodle lettering", "Hershey fonts · Dr. A. V. Hershey", "https://en.wikipedia.org/wiki/Hershey_fonts"),
    ]

    def journal_patron_entry(line: str):
        """
        One members.csv line -> (shown name, italic, faded). Patrons can ask
        to stay anonymous (*blacklisted*) or to appear under an alias.
        """

        name = line.split(';')[0].strip()
        if name == '*blacklisted*':
            return ("Anonymous", True, True)
        italic = name.startswith('*alias*')
        if italic:
            name = name[len('*alias*'):]
        # names are shown as they are: no text tags, no [interpolation]
        return (name.replace("{", "{{").replace("[", "[["), italic, False)

    def journal_patron_tiers():
        """
        [(tier title, [entries])] for every tier with patrons, plus the
        "last updated" line (or the reason the list is missing).
        """

        tiers = []
        updated = ""
        for tier_key, tier_title in JOURNAL_CREDIT_TIERS:
            members, updated = get_members(tier_key)
            if members:
                tiers.append((tier_title, [journal_patron_entry(member) for member in members]))
        return tiers, updated

    def journal_foldout_panels(tiers):
        """
        Flows the tiers into panels: a heading takes two rows, a name one.
        A heading never ends a panel on its own.
        """

        panels = [[]]
        capacity = JOURNAL_FOLDOUT_FIRST_ROWS
        used = 0

        def place(item, rows):
            nonlocal capacity, used
            if used + rows > capacity:
                panels.append([])
                capacity = JOURNAL_FOLDOUT_ROWS
                used = 0
            panels[-1].append(item)
            used += rows

        for tier_title, entries in tiers:
            place(("heading", "{} · {}".format(tier_title, len(entries))), 2)
            for entry in entries:
                place(("name", entry), 1)
        return panels

transform jr_unfold(delay):
    # each panel swings open from its left fold, one after the other
    xzoom 0.0 alpha 0.0
    pause delay
    easein 0.22 xzoom 1.0 alpha 1.0

screen journal_credits(display):
    # """
    # Credits page (in game). The pages themselves are journal_credits_pages,
    # shared with the title screen's journal (journal_title).
    # """

    tag interaction_overlay
    modal True

    default unfolded = (display == "patrons")

    use journal_backdrop

    if not unfolded:
        key "K_ESCAPE" action journal_close_action()

    use journal_page_selector(6, display)

    use journal_credits_pages(display)

    use journal_tooltip

    if unfolded:
        $ tiers, updated = journal_patron_tiers()
        if sum(len(entries) for _, entries in tiers):
            use journal_patron_foldout(tiers, updated)
        key "K_ESCAPE" action SetScreenVariable("unfolded", False)

screen journal_credits_pages(display):
    # """
    # Both credits pages: thanks and the folded patron list on the left, what
    # the game and the journal are made with on the right. The fold-out itself
    # is drawn by the screen that uses this (it needs `unfolded`).
    # """

    $ tiers, updated = journal_patron_tiers()
    $ patron_count = sum(len(entries) for _, entries in tiers)

    use jr_page("journal_credits_thanks", JR_LEFT_X, JR_LEFT_W):
        vbox:
            xsize JR_LEFT_W

            fixed:
                xysize (JR_LEFT_W, 66)
                text "Credits" style "jr_title" yalign 1.0
                text "{} · v{}".format(config.name, config.version):
                    style "jr_typed_small"
                    xalign 1.0
                    yalign 1.0
                    yoffset -8
            null height 4
            use jr_double_rule(JR_LEFT_W)

            null height 22
            use jr_rubric("Our patrons", JR_LEFT_W)
            null height 6
            text "Thank you to everyone who supports Mind the School on Patreon." style "jr_body"

            null height 20
            hbox:
                spacing 30

                button:
                    xysize (176, 236)
                    background None
                    padding (0, 0, 0, 0)
                    sensitive (patron_count > 0)
                    action SetScreenVariable("unfolded", True)
                    tooltip "Unfold the patron list"
                    use journal_folded_sheet(patron_count)

                vbox:
                    xsize JR_LEFT_W - 206
                    yalign 0.5
                    for tier_title, entries in tiers:
                        $ count_text = str(len(entries))
                        fixed:
                            xysize (JR_LEFT_W - 206, 32)
                            use jr_leader(journal_text_width(tier_title, size = 22),
                                JR_LEFT_W - 206 - journal_text_width(count_text, style = "jr_value", size = 22))
                            text tier_title style "jr_text" size 22 yalign 0.5
                            text count_text style "jr_value" size 22 xalign 1.0 yalign 0.5
                    null height 8
                    text updated style "jr_typed_small"
                    if patron_count:
                        null height 14
                        textbutton "Unfold the list ›":
                            style "jr_entry_button"
                            text_style "jr_value"
                            text_size 22
                            text_color JR_ACCENT
                            action SetScreenVariable("unfolded", True)

            null height 26
            use jr_rubric("Support the game", JR_LEFT_W)
            null height 14
            hbox:
                spacing 26
                button:
                    # fixed size: the tilted polaroid's bounding box is wider than its frame
                    xysize (260, 206)
                    background None
                    padding (0, 0, 0, 0)
                    tooltip "Open Patreon"
                    action Call("open_patreon_link")
                    # the banner is 500x262; the photo area keeps that shape
                    use journal_polaroid("images/journal/journal/patreon banner idle.webp", 260, 206, 2)
                vbox:
                    xsize JR_LEFT_W - 286
                    text "New versions are made possible by patrons. If you enjoy the game, joining them helps the next update along." style "jr_body"
                    null height 10
                    textbutton "Visit the Patreon page ›":
                        style "jr_entry_button"
                        text_style "jr_value"
                        text_size 22
                        text_color JR_ACCENT
                        action Call("open_patreon_link")

    use jr_page("journal_credits_made_with", JR_RIGHT_X, JR_RIGHT_W):
        vbox:
            xsize JR_RIGHT_W

            text "Made with" style "jr_title"
            null height 4
            use jr_double_rule(JR_RIGHT_W)

            null height 14
            use jr_rubric("The game", JR_RIGHT_W)
            null height 4
            use journal_credit_row("A game by", "Su.iT")
            use journal_credit_row("Patreon", "patreon page", patreon)
            use journal_credit_row("Discord", "community server", discord)

            null height 14
            use jr_rubric("Engine", JR_RIGHT_W)
            null height 4
            use journal_credit_row("Ren'Py", renpy.version_only, "https://www.renpy.org/")
            if renpy.license:
                null height 6
                text renpy.license style "jr_small"

            null height 14
            use jr_rubric("Assets", JR_RIGHT_W)
            null height 4
            for what, credit, url in JOURNAL_GAME_ASSET_CREDITS:
                use journal_credit_row(what, credit, url)

            null height 14
            use jr_rubric("This journal", JR_RIGHT_W)
            null height 4
            for what, credit, url in JOURNAL_ASSET_CREDITS:
                use journal_credit_row(what, credit, url)


screen journal_credit_row(label, value, url = None):
    # """
    # A credit as a ledger line; with a url the credit opens it in the browser.
    # """

    # a link button carries the entry padding (6 left, 8 right) around its text
    $ value_w = journal_text_width(value, style = "jr_value", size = 21) + (14 if url else 0)
    fixed:
        xysize (JR_RIGHT_W, 32)
        use jr_leader(journal_text_width(label, size = 21), JR_RIGHT_W - value_w)
        text label style "jr_text" size 21 yalign 0.5
        if url:
            textbutton value:
                style "jr_entry_button"
                text_style "jr_value"
                text_size 21
                text_color JR_ACCENT
                xalign 1.0
                yalign 0.5
                tooltip url
                action OpenURL(url)
        else:
            text value style "jr_value" size 21 xalign 1.0 yalign 0.5

screen journal_folded_sheet(patron_count):
    # """
    # The patron list folded into a small packet, tucked into the page.
    # """

    fixed at Transform(rotate = -3, rotate_pad = False):
        xysize (176, 236)
        for i in (2, 1, 0):
            # the folds underneath peek out a little at the right and bottom
            add Solid("#00000022") pos (i * 5 + 3, i * 4 + 4) xysize (160, 220)
            add Transform("gui/journal/ui/foldout_panel.webp", xysize = (160, 220)) pos (i * 5, i * 4)
        vbox:
            pos (18, 26)
            xsize 124
            spacing 6
            text "PATRONS" style "jr_rubric" size 16
            add Solid(JR_ACCENT + "90") xysize (124, 1)
            text ("1 name" if patron_count == 1 else "{} names".format(patron_count)) style "jr_typed" size 18
        text "unfold ›" style "jr_typed_small" pos (18, 186)

screen journal_patron_foldout(tiers, updated):
    # """
    # The unfolded patron sheet over the whole book. Panels open one after
    # the other; if there are ever more than fit the screen, the sheet
    # scrolls sideways.
    # """

    $ panels = journal_foldout_panels(tiers)
    $ sheet_w = len(panels) * (JOURNAL_FOLDOUT_PANEL_W + 6)
    $ view_w = min(sheet_w, 1840)
    $ pad = 36
    $ inner_w = JOURNAL_FOLDOUT_PANEL_W - pad * 2

    # click anywhere outside the sheet to fold it up again
    button:
        xysize (1920, 1080)
        background Solid("#140d08a0")
        action SetScreenVariable("unfolded", False)

    viewport:
        xsize view_w
        ysize JOURNAL_FOLDOUT_PANEL_H + 10
        xalign 0.5
        ypos 96
        mousewheel "horizontal"
        draggable True

        hbox:
            spacing 0
            for index, panel in enumerate(panels):
                # the outer box keeps its width while the panel inside swings open,
                # so the hbox doesn't slide the other panels around
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
                                text "Our patrons" style "jr_title" size 46
                                null height 2
                                use jr_double_rule(inner_w)
                                null height 8
                                text updated style "jr_typed_small"
                                null height 18

                            for kind, item in panel:
                                if kind == "heading":
                                    null height 14
                                    use jr_rubric(item, inner_w)
                                    null height 18
                                else:
                                    $ name, italic, faded = item
                                    text name:
                                        style "jr_text"
                                        size 22
                                        ysize JOURNAL_FOLDOUT_ROW_H
                                        if italic:
                                            font "fonts/CrimsonPro-Italic.ttf"
                                        if faded:
                                            color JR_PENCIL

                        if index == len(panels) - 1:
                            textbutton "Fold it up ›":
                                style "jr_entry_button"
                                text_style "jr_value"
                                text_size 21
                                text_color JR_ACCENT
                                xalign 1.0
                                yalign 1.0
                                xoffset -pad
                                yoffset -pad + 10
                                action SetScreenVariable("unfolded", False)
