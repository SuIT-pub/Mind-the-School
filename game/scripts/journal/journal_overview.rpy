##############################################################################
# Journal page 1: School Overview
#
# Left page: everything at a glance (budget, school stats, subject levels),
#            never behind an extra click.
# Right page: the detail of whatever is selected on the left.
##############################################################################

# TEMP (2026-10-15): fills the Overview with dummy entries so the page scrolling
# fallback can be tested. Must be False (or removed) before release.
define JOURNAL_OVERFLOW_TEST = False

init python:
    JOURNAL_OVERFLOW_DUMMY_PAYROLL = {
        "day": [("Vending machines", 20), ("Lost & found sales", 5), ("Library fines", 3)],
        "week": [("Janitor", -80), ("Gardener", -60), ("Bus service", -120), ("Pool chemicals", -40),
                ("Club grants", -90), ("Parents' donations", 150), ("Laundry service", -35)],
        "month": [("Electricity", -300), ("Water", -120), ("Insurance", -200), ("Sponsor: local bakery", 250),
                ("Equipment leasing", -180), ("Internet", -60)],
    }
    JOURNAL_OVERFLOW_DUMMY_SUBJECTS = {
        "Biology": 2, "Chemistry": 1, "Art": 3, "Music": 1, "Literature": 2, "Geography": 1,
        "Computer Science": 1, "Home Economics": 2, "Drama": 1, "Philosophy": 1,
    }

    JOURNAL_OVERFLOW_DUMMY_TEXT = ("\n\nDummy paragraph to test scrolling: this text only exists while "
        "JOURNAL_OVERFLOW_TEST is on, so the right page runs past its bottom edge.") * 6

    JOURNAL_PAYROLL_CADENCES = (
        ("day", "daily"),
        ("week", "payroll_weekly"),
        ("month", "payroll_monthly"),
    )

    def journal_payroll() -> Dict[str, List[Tuple[str, int]]]:
        """
        Collects the recurring money changes per cadence.

        ### Returns:
        1. Dict[str, List[Tuple[str, int]]]
            - cadence ("day", "week", "month") -> [(entry name, amount)]
            - only cadences that actually have non-zero entries are included,
                so the journal never shows empty columns
        """

        payroll = {}
        for cadence, collection in JOURNAL_PAYROLL_CADENCES:
            totals = {}
            for modifier in get_modifier_lists(MONEY, collection).values():
                # multipliers have no fixed amount to put in a ledger
                if modifier is None or modifier.get_mod_type() != "+":
                    continue
                name = modifier.get_name()
                totals[name] = totals.get(name, 0) + modifier.get_value()
            entries = [(name, int(value)) for name, value in totals.items() if value != 0]
            if JOURNAL_OVERFLOW_TEST:
                entries += JOURNAL_OVERFLOW_DUMMY_PAYROLL.get(cadence, [])
            if entries:
                payroll[cadence] = entries
        return payroll

    def journal_signed(value: num) -> str:
        if value > 0:
            return "+" + "{:,}".format(value)
        if value < 0:
            return "−" + "{:,}".format(-value)
        return "0"

    def journal_signed_color(value: num) -> str:
        if value > 0:
            return JR_GREEN
        if value < 0:
            return JR_ACCENT
        return JR_PRINT

    def journal_date_line() -> str:
        return "{} {} {} {} — {}".format(
            time.get_weekday()[:3], time.day, time.get_month_name()[:3], time.year,
            time.get_daytime_name()).upper()

    def journal_is_placeholder_image(path) -> bool:
        return path is None or find_loadable_image(path) == "" or "empty_image" in path

    # Screens are re-evaluated on every hover/tooltip change. Building fresh
    # Transforms of the 1080x1920 renders each time (and asking for their size)
    # made photo-heavy pages sluggish, so sizes and finished crops are cached.
    # functools caches live outside the store: nothing here ends up in saves.
    import functools

    @functools.lru_cache(maxsize = 512)
    def journal_image_size(path: str):
        return renpy.image_size(path)

    @functools.lru_cache(maxsize = 256)
    def _journal_cover_file(path: str, width: int, height: int):
        image_w, image_h = journal_image_size(path)
        if image_w * height > image_h * width:
            crop_w, crop_h = int(image_h * width / height), image_h
        else:
            crop_w, crop_h = image_w, int(image_w * height / width)
        crop = ((image_w - crop_w) // 2, (image_h - crop_h) // 2, crop_w, crop_h)
        return Transform(path, crop = crop, fit = "fill", xysize = (width, height))

    def journal_cover(image, width: int, height: int):
        """
        Fills exactly width x height: an image file is centre-cropped to the
        box's aspect first. (fit "cover" alone only scales, the overflow
        would spill over the photo border.) Displayables are expected to
        have the right aspect already and are just scaled.
        """

        if not isinstance(image, str) or not renpy.loadable(image):
            return Transform(image, fit = "fill", xysize = (width, height))
        return _journal_cover_file(image, int(width), int(height))

screen journal_overview(display, char = "school"):
    # """
    # This screen is used to display the school overview.

    # ### Parameters:
    # 1. display: str
    #     - The selected entry ("money", "level" or a stat key).
    # 2. char: str (default: "school")
    #     - The character to display the overview for.
    # """

    tag interaction_overlay
    modal True

    use journal_backdrop

    key "K_ESCAPE" action [With(dissolveM), Jump("map_entry")]

    use journal_page_selector(1, display, char)

    $ object_overview = {
        'school': get_school(),
        'teacher': get_character('teacher', charList['staff']),
        'parent': get_character('parent', charList)
    }
    $ school_object = object_overview[char]

    $ pta_proposal = get_game_data('voteProposal')
    if pta_proposal is not None and not isinstance(pta_proposal, Unlockable):
        $ clean_legacy_vote_proposal()
        $ pta_proposal = None

    if display == "":
        $ display = "money"

    $ payroll = journal_payroll()

    use journal_overview_summary(display, char, school_object, payroll, pta_proposal)

    if display == "money":
        use journal_overview_money(payroll)
    else:
        $ active_stat_obj = None
        if display == "level":
            $ active_stat_obj = school_object.get_level_obj()
        elif school_object.check_stat_exists(display):
            $ active_stat_obj = school_object.get_stat_obj(display)
        if active_stat_obj is not None:
            use journal_overview_stat(display, active_stat_obj, school_object)

    use journal_tooltip

screen journal_overview_entry(key, label, icon, selected, action):
    # """
    # A clickable entry label with its stat icon (pencil underline on hover,
    # marker swipe when selected).
    # """

    button:
        style "jr_entry_button"
        yalign 0.5
        selected selected
        action action
        hbox:
            spacing 10
            add Transform(icon, xysize = (26, 26), alpha = 0.85) yalign 0.5
            text label style "jr_entry_button_text"

screen journal_overview_summary(display, char, school_object, payroll, pta_proposal):

    use jr_page("journal_overview_left", JR_LEFT_X, JR_LEFT_W):
        vbox:
            xsize JR_LEFT_W

            text "School Overview" style "jr_title"
            null height 4
            use jr_double_rule(JR_LEFT_W)
            null height 10
            text journal_date_line() style "jr_typed_small"

            if isinstance(pta_proposal, Unlockable):
                if pta_proposal.group_index != -1:
                    $ pta_display = unlockable_manager.build_display(pta_proposal.unlockable_key, pta_proposal.group_index)
                else:
                    $ pta_display = pta_proposal.unlockable_key
                null height 6
                textbutton "PTA meeting — {} “{}”".format(pta_proposal.type_key.capitalize(), pta_proposal.get_title()):
                    style "jr_entry_button"
                    text_style "jr_small"
                    text_color JR_ACCENT
                    action [With(dissolveM), Call("open_journal", 4, pta_display)]

            # ---- budget
            null height 22
            use jr_rubric("Budget", JR_LEFT_W)
            null height 4
            fixed:
                xsize JR_LEFT_W
                ysize 38
                use journal_overview_entry("money", "Funds available", get_stat_icon_path(MONEY, size = ICON_SMALL, white = False),
                    (display == "money"), [With(dissolveM), Call("open_journal", 1, "money", char)])
                text money.display_stat() style "jr_value" xalign 1.0 yalign 0.5

            if payroll:
                hbox:
                    xoffset 42
                    spacing 26
                    for cadence, collection in JOURNAL_PAYROLL_CADENCES:
                        if cadence in payroll:
                            $ net = sum(value for _, value in payroll[cadence])
                            hbox:
                                spacing 8
                                text "per " + cadence style "jr_small"
                                text journal_signed(net) style "jr_small" font JR_FONT_BOLD color journal_signed_color(net)

            # ---- school
            null height 20
            use jr_rubric("The School", JR_LEFT_W)
            null height 4

            $ level_obj = school_object.get_level_obj()
            fixed:
                xsize JR_LEFT_W
                ysize 42
                use journal_overview_entry("level", "Level", get_stat_icon_path("level", size = ICON_SMALL, white = False),
                    (display == "level"), [With(dissolveM), Call("open_journal", 1, "level", char)])
                fixed:
                    xpos 230
                    use jr_level_boxes(school_object.get_level())
                text level_obj.display_stat() style "jr_value" xalign 1.0 yalign 0.5

            for stat_key in school_object.get_stats().keys():
                $ stat_obj = school_object.get_stat_obj(stat_key)
                $ stat_title = Stat_Data[stat_obj.get_name()].get_title()
                fixed:
                    xsize JR_LEFT_W
                    ysize 42
                    use journal_overview_entry(stat_key, stat_title, get_stat_icon_path(stat_key, size = ICON_SMALL, white = False),
                        (display == stat_key), [With(dissolveM), Call("open_journal", 1, stat_obj.get_name(), char)])
                    fixed:
                        xpos 230
                        use jr_value_bar(stat_obj.get_value(), Stat_Data[stat_obj.get_name()].get_max_limit())
                    text stat_obj.display_stat() style "jr_value" xalign 1.0 yalign 0.5

            # ---- subjects: two columns; the whole column scrolls if this ever gets too long
            $ subject_levels = get_headmaster_proficiency_levels()
            if JOURNAL_OVERFLOW_TEST:
                $ subject_levels = dict(subject_levels, **JOURNAL_OVERFLOW_DUMMY_SUBJECTS)
            if subject_levels:
                null height 20
                use jr_rubric("Subject Proficiency", JR_LEFT_W)
                null height 6
                $ subject_keys = list(subject_levels.keys())
                $ cell_w = (JR_LEFT_W - 30) // 2
                $ subject_rows = (len(subject_keys) + 1) // 2
                grid 2 subject_rows:
                    xspacing 30
                    yspacing 4
                    for subject in subject_keys:
                        $ subject_name = get_translation(subject)
                        $ subject_level = "Lv. {}".format(subject_levels[subject])
                        fixed:
                            xysize (cell_w, 32)
                            use jr_leader(journal_text_width(subject_name, size = 22),
                                cell_w - journal_text_width(subject_level, style = "jr_value", size = 22))
                            text subject_name style "jr_text" size 22 yalign 0.5
                            text subject_level style "jr_value" size 22 xalign 1.0 yalign 0.5
                    # keep the grid full; an odd count would leave the last row short
                    if len(subject_keys) % 2:
                        null

screen journal_overview_detail_header(title, icon, value_text, value_color = JR_PRINT):
    fixed:
        xsize JR_RIGHT_W
        ysize 66
        hbox:
            spacing 14
            yalign 1.0
            if icon:
                add Transform(icon, xysize = (40, 40), alpha = 0.9) yalign 0.6
            text title style "jr_title"
        text value_text style "jr_title" font JR_FONT_BOLD size 50 color value_color xalign 1.0 yalign 1.0
    null height 4
    use jr_double_rule(JR_RIGHT_W)

screen journal_overview_stat(stat_key, stat_obj, school_object):
    # """
    # Right page: one stat (or the school level) in detail.
    # """

    $ is_level = stat_key == "level"
    $ title = "Level" if is_level else Stat_Data[stat_obj.get_name()].get_title()
    $ stage = stat_obj.get_level()
    $ level_text = stat_obj.get_description()
    $ about_text = stat_obj.get_stat_description(char_obj = school_object).strip()
    if JOURNAL_OVERFLOW_TEST:
        $ about_text += JOURNAL_OVERFLOW_DUMMY_TEXT
    $ image_path = stat_obj.get_image()
    $ has_photo = not journal_is_placeholder_image(image_path)

    use jr_page("journal_overview_stat", JR_RIGHT_X, JR_RIGHT_W):
        vbox:
            xsize JR_RIGHT_W

            use journal_overview_detail_header(title,
                get_stat_icon_path(stat_key, size = ICON_SMALL, white = False),
                stat_obj.get_display_value(), JR_ACCENT)

            null height 22
            hbox:
                spacing 24
                vbox:
                    xsize (JR_RIGHT_W - 270 if has_photo else JR_RIGHT_W)
                    if not is_level:
                        use jr_rubric("Stage {} of 10".format(stage), 250)
                        null height 8
                        use jr_level_boxes(stage)
                        null height 22
                    use jr_rubric("Secretary's note", 250 if has_photo else JR_RIGHT_W)
                    null height 6
                    text level_text style "jr_typed"
                if has_photo:
                    use journal_polaroid(image_path, 236, 300, -3)

            if about_text:
                null height 24
                use jr_rubric("About this value", JR_RIGHT_W)
                null height 6
                text about_text style "jr_body"

screen journal_polaroid(image_path, width, height, angle, backdrop = None):
    # """
    # A photo glued into the journal: white border, slight tilt, soft shadow.
    # backdrop goes behind cut-out renders (transparent background).
    # """

    fixed at Transform(rotate = angle, rotate_pad = False):
        xysize (width, height)
        add Solid("#00000030") pos (4, 6) xysize (width, height)
        add Solid("#faf7f0") xysize (width, height)
        if backdrop:
            add journal_cover(backdrop, width - 24, height - 70) pos (12, 12)
        add journal_cover(image_path, width - 24, height - 70) pos (12, 12)

screen journal_overview_money(payroll):
    # """
    # Right page: the budget as a ledger. One column per cadence that actually
    # has entries; income and expenses grouped, net double-underlined.
    # """

    $ cadences = [cadence for cadence, _ in JOURNAL_PAYROLL_CADENCES if cadence in payroll]
    $ col_w = 112
    $ name_w = JR_RIGHT_W - col_w * len(cadences)

    python:
        ledger = {}
        for cadence in cadences:
            for name, value in payroll[cadence]:
                ledger.setdefault(name, {})[cadence] = value
        income = [(name, values) for name, values in ledger.items() if sum(values.values()) > 0]
        expenses = [(name, values) for name, values in ledger.items() if sum(values.values()) <= 0]
        reserved_total = sum(reserved_money.values()) if reserved_money else 0
        money_about = Stat_Data[MONEY].get_stat_description().strip()

    use jr_page("journal_overview_ledger", JR_RIGHT_X, JR_RIGHT_W):
        vbox:
            xsize JR_RIGHT_W

            use journal_overview_detail_header("Budget",
                get_stat_icon_path(MONEY, size = ICON_SMALL, white = False),
                money.get_display_value())

            null height 22
            if cadences:
                use jr_rubric("Recurring", JR_RIGHT_W)
                null height 4
                # Text ignores xsize, so every row is a fixed box and each
                # figure is right-anchored at the end of its column.
                $ table_w = JR_RIGHT_W
                $ col_end = {cadence: name_w + (i + 1) * col_w for i, cadence in enumerate(cadences)}
                fixed:
                    xysize (table_w, 22)
                    for cadence in cadences:
                        text ("per " + cadence).upper() style "jr_small" size 15 font JR_FONT_BOLD xpos col_end[cadence] xanchor 1.0 yalign 1.0
                for group_title, entries in (("Income", income), ("Expenses", expenses)):
                    if entries:
                        null height 6
                        text group_title style "jr_text" size 21 font JR_FONT_BOLD
                        for name, values in entries:
                            # helper.rpy shadows min() with a *values-only version, so unpack the list
                            $ first_figure = min(*[col_end[c] - journal_text_width(journal_signed(values[c]), font = JR_FONT_SEMIBOLD, size = 22) for c in values])
                            fixed:
                                xysize (table_w, 32)
                                use jr_leader(16 + journal_text_width(name, size = 22), first_figure)
                                text name style "jr_text" size 22 xpos 16 yalign 0.5
                                for cadence in cadences:
                                    if cadence in values:
                                        text journal_signed(values[cadence]) style "jr_text" size 22 font JR_FONT_SEMIBOLD color journal_signed_color(values[cadence]) xpos col_end[cadence] xanchor 1.0 yalign 0.5
                null height 8
                add Solid(JR_PRINT + "c8") xysize (col_w * len(cadences), 1) xpos name_w
                null height 4
                fixed:
                    xysize (table_w, 34)
                    text "Net" style "jr_text" size 23 font JR_FONT_BOLD yalign 0.5
                    for cadence in cadences:
                        $ net = sum(value for _, value in payroll[cadence])
                        text journal_signed(net) style "jr_text" size 23 font JR_FONT_BOLD color journal_signed_color(net) xpos col_end[cadence] xanchor 1.0 yalign 0.5
                null height 4
                fixed:
                    xpos name_w
                    fit_first True
                    use jr_double_rule(col_w * len(cadences))
            else:
                use jr_rubric("Recurring", JR_RIGHT_W)
                null height 6
                text "No regular income or expenses." style "jr_small"

            if reserved_total:
                null height 26
                use jr_rubric("Reserved", JR_RIGHT_W)
                null height 6
                fixed:
                    xsize JR_RIGHT_W
                    ysize 32
                    $ reserved_text = "{:,}".format(reserved_total)
                    use jr_leader(16 + journal_text_width("Held back for pending plans", size = 22),
                        JR_RIGHT_W - journal_text_width(reserved_text, font = JR_FONT_SEMIBOLD, size = 22))
                    text "Held back for pending plans" style "jr_text" size 22 xoffset 16 yalign 0.5
                    text reserved_text style "jr_text" size 22 font JR_FONT_SEMIBOLD xalign 1.0 yalign 0.5

            if money_about:
                null height 26
                use jr_rubric("About this value", JR_RIGHT_W)
                null height 6
                text money_about style "jr_body"
