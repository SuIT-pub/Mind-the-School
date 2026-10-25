##############################################################################
# Journal: Situations (page 8)
#
# Left page: every open matter with its current mood, completed ones below.
# Right page: the selected situation; its top ribbons switch between the
# overview, the passives/measures the headmaster can set and the chronicle
# of notes.
#
# display = "<situation key>" + optional ":passives" / ":notes" / ":"
# (see parse_situation_journal_display in journal.rpy)
##############################################################################

init python:
    # muted ink versions of TEASER_NOTE_TYPES, which are tuned for the old white page
    JOURNAL_NOTE_TYPE_INK = {
        "observation": "#35557e",
        "suspicion": "#6a4a80",
        "insight": "#34603a",
        "setback": "#8a2622",
    }

    JOURNAL_SITUATION_TABS = [("", "Overview"), ("passives", "Measures"), ("notes", "Notes")]

    def journal_escape_text(value) -> str:
        # literal text inside a tagged string: no text tags, no [interpolation]
        return str(value).replace("{", "{{").replace("[", "[[")

    JOURNAL_NOTE_ITALIC = "fonts/CrimsonPro-Italic.ttf"

    # wrapped heights only change with the text, so screens re-evaluating every frame
    # don't lay the same paragraph out again
    journal_note_height_cache = {}

    def journal_note_text_height(note_text: str, width: int, italic: bool = False) -> int:
        """
        Height of a jr_body paragraph wrapped to width, as the note screen draws it.
        """
        key = (note_text, width, italic, renpy.variant("small"))
        if key not in journal_note_height_cache:
            font_kwargs = {"font": JOURNAL_NOTE_ITALIC} if italic else {}
            journal_note_height_cache[key] = Text(note_text, style="jr_body", **font_kwargs).size(width=width)[1]
        return journal_note_height_cache[key]

    def journal_note_interpretation_below(note_text: str, interpretation: str, column_w: int, photo_h: int, extra_h: int = 0) -> bool:
        """
        Whether a side-photo note should run its interpretation full width under the
        photo instead of down the narrow text column.

        It moves once it would hang below the photo, as long as the observation
        (plus extra_h, e.g. a doodle) already fills the photo's height to within two
        lines; a short observation keeps it beside the photo, where moving it would
        leave a hole next to the picture.
        """
        note_h = journal_note_text_height(note_text, column_w) + extra_h
        beside_h = note_h + 4 + journal_note_text_height("— " + interpretation, column_w, True)
        if beside_h <= photo_h:
            return False
        line_h = journal_note_text_height("X", column_w)
        return photo_h - note_h <= 2 * line_h

    def journal_mood_ink(situation) -> str:
        area = situation.get_combined_bar_value_area()
        if area < 0:
            return JR_ACCENT
        if area > 0:
            return JR_GREEN
        return JR_PENCIL

    def journal_situation_status(situation) -> str:
        if situation.state == "completed":
            return "Completed"
        if situation.is_paused():
            return "Paused"
        return "Active"

    def journal_situation_trend(situation) -> str:
        tendency = situation.get_combined_bar_tendency()
        if tendency > 0:
            return "improving"
        if tendency < 0:
            return "worsening"
        return "steady"

    def journal_situation_tabs(situation) -> List[str]:
        """
        Tabs that have something to show for this situation, in ribbon order.
        """

        tabs = [""]
        if situation.state != "completed" and (situation.get_passives("passive") or situation.get_passives("measure")):
            tabs.append("passives")
        if situation.get_active_teasers():
            tabs.append("notes")
        return tabs

    def journal_bar_x(value, bar_min, bar_max, width) -> int:
        """
        x of a bar value on the mood track (4px inside the pencil box on each side).
        """

        span = float(bar_max - bar_min) or 1.0
        return int(clamp_value((value - bar_min) / span, 0.0, 1.0) * (width - 8)) + 4

    def journal_situation_full_image(thumbnail):
        if not thumbnail:
            return None
        stem = thumbnail.rsplit('.', 1)[0]
        return find_loadable_image(stem + '_full.webp') or find_loadable_image(stem + '_full.png') or thumbnail

screen journal_situations(display):
    # """
    # Situations page.
    # """

    tag interaction_overlay
    modal True

    default zoomed_image = None

    python:
        situation_key, situation_tab = parse_situation_journal_display(display)
        visible_situations = situation_manager.get_visible_situations() if situation_manager is not None else []
        completed_situations = situation_manager.get_completed_situations() if situation_manager is not None else []

        # nothing picked yet: open the first matter instead of an empty right page
        situation = situation_manager.get_situation(situation_key) if situation_key and situation_manager is not None else None
        if situation is None and visible_situations:
            situation = visible_situations[0]
            situation_tab = ""
        teaser_only = situation is not None and situation.visibility_state == "teaser_active"

        sub_entries = None
        tabs = []
        if situation is not None and not teaser_only:
            tabs = journal_situation_tabs(situation)
            if situation_tab not in tabs:
                situation_tab = ""
            if len(tabs) > 1:
                sub_entries = [(label, (tab == situation_tab), [With(dissolveM), Call("open_journal", 8, "{}:{}".format(situation.key, tab))])
                    for tab, label in JOURNAL_SITUATION_TABS if tab in tabs]

    use journal_backdrop

    if zoomed_image is None:
        key "K_ESCAPE" action journal_close_action()

    use journal_page_selector(8, display, sub_entries = sub_entries)

    if len(tabs) > 1 and has_keyboard():
        $ next_tab = tabs[(tabs.index(situation_tab) + 1) % len(tabs)]
        key "K_TAB" action [With(dissolveM), Call("open_journal", 8, "{}:{}".format(situation.key, next_tab))]

    use journal_situation_list(situation, visible_situations, completed_situations)

    if situation is not None:
        # opened without a pick, the page shows the first matter: that counts as seen
        if not situation_key:
            on "show" action Function(acknowledge_journal_alerts, 8, situation.key)
        if teaser_only:
            use journal_situation_notes_page(situation, "Unclear matter", "Notes so far — nothing is certain yet.")
        elif situation_tab == "passives":
            use journal_situation_measures(situation, display)
        elif situation_tab == "notes":
            use journal_situation_notes_page(situation, situation.name, "Notes")
        else:
            use journal_situation_overview(situation, display)

    use journal_tooltip

    if zoomed_image is not None:
        use jr_zoom_overlay(zoomed_image)

screen journal_situation_list(selected, visible_situations, completed_situations):
    # """
    # Left page: open matters with their mood, completed ones (foldable) below.
    # """

    $ show_completed = get_setting("journal_situations_show_completed") or False
    $ open_situations = [situation for situation in visible_situations if situation.state != "completed"]

    use jr_page("journal_situation_list", JR_LEFT_X, JR_LEFT_W):
        vbox:
            xsize JR_LEFT_W

            fixed:
                xysize (JR_LEFT_W, 66)
                text "Situations" style "jr_title" yalign 1.0
                text ("1 open" if len(open_situations) == 1 else "{} open".format(len(open_situations))):
                    style "jr_typed_small"
                    xalign 1.0
                    yalign 1.0
                    yoffset -8
            null height 4
            use jr_double_rule(JR_LEFT_W)

            if situation_manager is not None and situation_manager.is_resolution_breather_active():
                $ breather_days = situation_manager.get_resolution_breather_display_days()
                null height 12
                text "The pressure eases for a moment. The remaining situations hold steady — {} more day{} of calm.".format(breather_days, "" if breather_days == 1 else "s"):
                    style "jr_body"
                    font "fonts/CrimsonPro-Italic.ttf"
                    color JR_PENCIL

            null height 22
            use jr_rubric("Open", JR_LEFT_W)
            null height 4
            if open_situations:
                for situation in open_situations:
                    use journal_situation_entry(situation, (situation is selected))
            else:
                text "Nothing needs my attention right now." style "jr_small"

            if completed_situations:
                null height 22
                button:
                    xsize JR_LEFT_W
                    background None
                    padding (0, 0, 0, 0)
                    action [With(dissolveM), Function(set_setting, "journal_situations_show_completed", not show_completed)]
                    tooltip ("Hide completed" if show_completed else "Show completed")
                    use jr_rubric("Completed ({}) · {}".format(len(completed_situations), "hide" if show_completed else "show"), JR_LEFT_W)
                if show_completed:
                    null height 4
                    for situation in completed_situations:
                        use journal_situation_entry(situation, (situation is selected))

screen journal_situation_entry(situation, selected):
    # """
    # One list row: name on the left, mood (or state) right-aligned.
    # """

    python:
        if situation.visibility_state == "teaser_active":
            entry_name = "Unclear matter"
            note_count = len(situation.get_active_teasers())
            entry_state = "1 note" if note_count == 1 else "{} notes".format(note_count)
            state_ink = JR_PENCIL
        elif situation.state == "completed":
            entry_name = situation.name
            entry_state = "closed"
            state_ink = JR_PENCIL
        elif situation.is_paused():
            entry_name = situation.name
            entry_state = "paused"
            state_ink = JR_PENCIL
        else:
            entry_name = situation.name
            entry_state = situation.get_combined_bar_value_mood()
            state_ink = journal_mood_ink(situation)

    fixed:
        xysize (JR_LEFT_W, 40)
        button:
            style "jr_entry_button"
            yalign 0.5
            selected selected
            action [With(dissolveM), Call("open_journal", 8, situation.key)]
            hbox:
                spacing 8
                text entry_name style "jr_entry_button_text" size 24 yalign 0.5
                if journal_has_alert(situation.get_journal_alert_topic(), situation.key):
                    use jr_new_mark(situation.key)
        text entry_state style "jr_text" size 21 font "fonts/CrimsonPro-Italic.ttf" color state_ink xalign 1.0 yalign 0.5

screen journal_situation_header(title, subtitle):
    text title style "jr_title"
    null height 4
    use jr_double_rule(JR_RIGHT_W)
    null height 10
    text subtitle style "jr_typed_small"

screen journal_situation_overview(situation, display):
    # """
    # Right page, first tab: photo, state, description, mood bar and what
    # the headmaster expects to happen next.
    # """

    python:
        thumbnail = situation.get_current_thumbnail()
        has_photo = bool(thumbnail) and not journal_is_placeholder_image(thumbnail)
        hints = situation.get_hints() if situation.state != "completed" else []
        facts = [("Status", journal_situation_status(situation), JR_PRINT)]
        # an unlockable's campaign: say what it belongs to and link back to its page
        unlockable_display = None
        if isinstance(situation, Unlockable):
            # the names list holds the plural tab label ("Rules"), so use the key itself
            facts.insert(0, ("Type", situation.type_key.capitalize(), JR_PRINT))
            if situation.group_index != -1:
                unlockable_display = unlockable_manager.build_display(situation.unlockable_key, situation.group_index)
            else:
                unlockable_display = situation.unlockable_key
        if situation.state != "completed":
            facts.append(("Mood", situation.get_combined_bar_value_mood(), journal_mood_ink(situation)))
            facts.append(("Trend", journal_situation_trend(situation), JR_PRINT))
        photo_w = 288
        facts_w = JR_RIGHT_W - photo_w - 26 if has_photo else JR_RIGHT_W

    use jr_page("journal_situation_overview", JR_RIGHT_X, JR_RIGHT_W):
        vbox:
            xsize JR_RIGHT_W

            use journal_situation_header(situation.name, "Situation report")

            null height 20
            hbox:
                spacing 26
                if has_photo:
                    button:
                        # fixed size: the tilted polaroid's bounding box is wider than its frame
                        xysize (photo_w, 224)
                        padding (0, 0, 0, 0)
                        background None
                        tooltip "Enlarge"
                        action SetScreenVariable("zoomed_image", journal_situation_full_image(thumbnail))
                        use journal_polaroid(thumbnail, photo_w, 224, -1.5)
                vbox:
                    xsize facts_w
                    use jr_rubric("On record", facts_w)
                    null height 4
                    for label, value, ink in facts:
                        fixed:
                            xysize (facts_w, 32)
                            use jr_leader(journal_text_width(label, size = 22),
                                facts_w - journal_text_width(value, style = "jr_value", size = 22))
                            text label style "jr_text" size 22 yalign 0.5
                            text value style "jr_value" size 22 color ink xalign 1.0 yalign 0.5
                    if situation.is_paused():
                        null height 10
                        text "Nothing changes until it continues." style "jr_small"
                    if unlockable_display is not None:
                        null height 12
                        textbutton "Open its {} ›".format(situation.type_key):
                            style "jr_entry_button"
                            text_style "jr_value"
                            text_size 22
                            text_color JR_ACCENT
                            action [With(dissolveM), Call("open_journal", 4, unlockable_display)]

            null height 22
            for description in situation.get_descriptions():
                text description style "jr_body"
                null height 6

            if situation.state != "completed":
                null height 18
                use jr_rubric("Mood", JR_RIGHT_W)
                null height 6
                use jr_situation_bar(situation, JR_RIGHT_W)

            if hints:
                null height 18
                use jr_rubric("What comes next", JR_RIGHT_W)
                null height 6
                for i, hint in enumerate(hints):
                    hbox:
                        spacing 10
                        text "{}.".format(i + 1) style "jr_value" size 23 color JR_ACCENT min_width 26
                        text hint style "jr_body" xsize JR_RIGHT_W - 36
                    null height 8

screen jr_situation_bar(situation, width, compact = False):
    # """
    # The situation's combined bar as a watercolour track: ink pointer for
    # the current value, posts for the nearest thresholds either side.
    # compact: the map HUD's slim version, without the mood word above it.
    # """

    python:
        bar_min = situation.get_combined_bar_min()
        bar_max = situation.get_combined_bar_max()
        bar_value = situation.get_combined_bar_value()
        handle_x = journal_bar_x(bar_value, bar_min, bar_max, width)
        mood = situation.get_combined_bar_value_mood()
        next_above = situation.get_closest_next_blocking_threshold(bar_value, 1.0)
        next_below = situation.get_closest_next_blocking_threshold(bar_value, -1.0)
        gates = []
        if next_below is not None:
            below_pos = situation.get_combined_threshold_value(next_below)
            if below_pos + next_below.visible_range > bar_value:
                gates.append((journal_bar_x(below_pos, bar_min, bar_max, width), JR_ACCENT if next_above is not next_below else JR_PRINT))
        if next_above is not None and next_above is not next_below:
            above_pos = situation.get_combined_threshold_value(next_above)
            if above_pos - next_above.visible_range < bar_value:
                gates.append((journal_bar_x(above_pos, bar_min, bar_max, width), JR_GREEN))
        # keep the mood word on the page when the pointer sits near either end
        label_x = min(max(handle_x, 60), width - 60)
        # (track y, track height, post y, post height, pointer y, total height)
        track_y, track_h, post_y, post_h, pointer_y, total_h = (12, 12, 6, 22, 0, 28) if compact else (44, 18, 38, 30, 29, 70)

    fixed:
        xysize (width, total_h)

        if not compact:
            text mood:
                style "jr_text"
                size 21
                font "fonts/CrimsonPro-Italic.ttf"
                color journal_mood_ink(situation)
                xpos label_x
                xanchor 0.5
                ypos 0

        add Transform("gui/journal/ui/mood_track.webp", xysize = (width, track_h)) ypos track_y

        if bar_min < 0 < bar_max:
            add Solid(JR_PRINT + "60") xpos journal_bar_x(0, bar_min, bar_max, width) xanchor 0.5 ypos track_y + 2 xysize (1, track_h - 4)

        for gate_x, ink in gates:
            # threshold post: a short double ink stroke reaching past the track
            add Solid(ink) xpos gate_x - 3 ypos post_y xysize (2, post_h)
            add Solid(ink) xpos gate_x + 2 ypos post_y xysize (2, post_h)

        add "gui/journal/ui/marker.webp" xpos handle_x xanchor 0.5 ypos pointer_y
        add Solid("#342820d0") xpos handle_x xanchor 0.5 ypos pointer_y + 13 xysize (2, track_h + 4)

screen journal_situation_measures(situation, display):
    # """
    # Right page, second tab: one passive can run at a time, measures are
    # one-off interventions with their own availability.
    # """

    $ passives = situation.get_passives("passive")
    $ measures = situation.get_passives("measure")
    $ paused = situation.is_paused()

    use jr_page("journal_situation_measures", JR_RIGHT_X, JR_RIGHT_W):
        vbox:
            xsize JR_RIGHT_W

            use journal_situation_header(situation.name, "Measures")

            if paused:
                null height 12
                text "The situation is paused — nothing can be changed until it continues." style "jr_small"

            if passives:
                null height 22
                use jr_rubric("Passives — one at a time", JR_RIGHT_W)
                null height 6
                for passive in passives:
                    $ is_active = situation.active_passive == passive.name
                    use journal_situation_option(get_translation(passive.name), passive.get_effects_description(True),
                        is_active, (not paused or is_active),
                        Call("activate_passive", display, situation, passive))

            if measures:
                null height 22
                use jr_rubric("Measures", JR_RIGHT_W)
                null height 6
                for measure in measures:
                    $ is_active = situation.active_measure == measure.name
                    use journal_situation_option(get_translation(measure.name), measure.get_effects_description(True),
                        is_active, (is_active or measure.check_available()),
                        Call("activate_measure", display, situation, measure))

screen journal_situation_option(title, effects, active, available, action):
    # """
    # A tick box with the option's name; its effects pencilled underneath.
    # """

    vbox:
        xsize JR_RIGHT_W
        button:
            style "jr_entry_button"
            selected active
            sensitive (available and not active)
            action action
            hbox:
                spacing 12
                add ("gui/journal/ui/box_full.webp" if active else "gui/journal/ui/box_empty.webp") yalign 0.5
                text title:
                    style "jr_entry_button_text"
                    size 24
                    if active:
                        font JR_FONT_BOLD
                    elif not available:
                        color JR_PENCIL + "a0"
        if active:
            text "in effect" style "jr_small" font "fonts/CrimsonPro-Italic.ttf" color JR_GREEN xpos 36
        for effect in effects:
            text effect style "jr_small" xpos 36 xsize JR_RIGHT_W - 36
        null height 12

screen journal_situation_notes_page(situation, title, subtitle):
    # """
    # Right page: the situation's chronicle notes, oldest first.
    # """

    use jr_page("journal_situation_notes", JR_RIGHT_X, JR_RIGHT_W):
        vbox:
            xsize JR_RIGHT_W

            use journal_situation_header(title, subtitle)
            null height 22
            for teaser in situation.get_active_teasers():
                use jr_situation_note(teaser, JR_RIGHT_W)

screen jr_situation_note(teaser, width):
    # """
    # One chronicle note: type and date, the observation, the headmaster's
    # reading of it; photo notes keep their frozen layout and tilt. An
    # optional pencil doodle (teaser.doodle) points at the photo, or back at
    # the text when there is none.
    # """

    python:
        stamp = teaser.get_timestamp_text()
        note_type = getattr(teaser, "note_type", None)
        type_label = teaser.get_note_type_display()[0]
        type_ink = JOURNAL_NOTE_TYPE_INK.get(note_type, JR_ACCENT)
        layout_id = getattr(teaser, "layout_id", None) or "text_full"
        has_photo = teaser.has_photo()
        interpretation = getattr(teaser, "interpretation_text", None)
        metrics = teaser.get_polaroid_metrics() if has_photo else None
        gap = 18
        side_w = max(160, width - metrics["cell_w"] - gap) if metrics else width
        doodle = getattr(teaser, "doodle", None)
        doodle_ink = getattr(teaser, "doodle_ink", None) or "pencil"
        doodle_seed = journal_note_seed(teaser.key, doodle)
        interpretation_below = False
        if has_photo and interpretation and layout_id in ("photo_left", "photo_right", "text_aside"):
            doodle_h = (journal_pencil_note(doodle, "left", doodle_ink, 22, doodle_seed)[2] + 4) if doodle else 0
            interpretation_below = journal_note_interpretation_below(teaser.text, interpretation, side_w, metrics["cell_h"], doodle_h)
        side_interpretation = None if interpretation_below else interpretation

    vbox:
        xsize width
        spacing 6

        # type and date in ONE text: segments of a text share a baseline whatever their
        # fonts' metrics are, which two boxes side by side in an hbox never do
        python:
            header_parts = []
            if type_label is not None:
                header_parts.append("{{font={}}}{{k=2.2}}{{color={}}}{}{{/color}}{{/k}}{{/font}}".format(
                    JR_FONT_BOLD, type_ink, journal_escape_text(type_label.upper())))
            if stamp:
                header_parts.append("{{font={}}}{{color={}}}{}{{/color}}{{/font}}".format(
                    JR_FONT_TYPED, JR_PENCIL, journal_escape_text(stamp)))
        if header_parts:
            text "   ".join(header_parts) style "jr_text" size 17

        if has_photo and layout_id in ("photo_left", "text_aside"):
            hbox:
                spacing gap
                use jr_teaser_photo(metrics, teaser.image_path)
                use jr_situation_note_text(teaser.text, side_interpretation, side_w, 0, doodle, "left", doodle_ink, doodle_seed)
        elif has_photo and layout_id == "photo_right":
            hbox:
                spacing gap
                use jr_situation_note_text(teaser.text, side_interpretation, side_w, 0, doodle, "right", doodle_ink, doodle_seed)
                use jr_teaser_photo(metrics, teaser.image_path)
        elif has_photo:
            # photo centred; the doodle takes the free space on one side, pointing at it
            $ photo_x = (width - metrics["cell_w"]) // 2
            fixed:
                xysize (width, metrics["cell_h"])
                fixed:
                    xpos photo_x
                    xysize (metrics["cell_w"], metrics["cell_h"])
                    use jr_teaser_photo(metrics, teaser.image_path)
                if doodle:
                    $ on_left = (getattr(teaser, "doodle_side", None) or "right") == "left"
                    $ note, note_w, note_h = journal_pencil_note(doodle, ("right" if on_left else "left"), doodle_ink, 22, doodle_seed)
                    # the space beside the photo is narrow; longer notes shrink to fit it
                    $ note_zoom = min(1.0, (photo_x - 8) / float(max(1, note_w)))
                    $ note_w = int(note_w * note_zoom)
                    add Transform(note, zoom = note_zoom):
                        xpos (max(0, photo_x - note_w - 4) if on_left else photo_x + metrics["cell_w"] + 4)
                        ypos int(metrics["cell_h"] * 0.32)
            use jr_situation_note_text(teaser.text, interpretation, width)
        else:
            use jr_situation_note_text(teaser.text, interpretation, width - (18 if layout_id == "text_aside" else 0), (18 if layout_id == "text_aside" else 0),
                doodle, "up_left", doodle_ink, doodle_seed)

        if interpretation_below:
            text "— " + interpretation style "jr_body" font JOURNAL_NOTE_ITALIC color JR_PENCIL

        null height 18

screen jr_situation_note_text(note_text, interpretation, width, indent = 0, doodle = None, arrow = None, ink = "pencil", seed = 0):
    vbox:
        xsize width
        xoffset indent
        text note_text style "jr_body"
        if interpretation:
            null height 4
            text "— " + interpretation style "jr_body" font JOURNAL_NOTE_ITALIC color JR_PENCIL
        if doodle:
            null height 4
            # beside a photo the note leans towards it; under plain text it sits on the right
            $ note, note_w, note_h = journal_pencil_note(doodle, arrow, ink, 22, seed)
            add note xalign (1.0 if arrow in ("right", "up_left") else 0.0)

screen jr_teaser_photo(metrics, image_path):
    # """
    # A teaser's polaroid; clicking it enlarges the photo (jr_zoom_overlay).
    # """

    button:
        xysize (metrics["cell_w"], metrics["cell_h"])
        padding (0, 0, 0, 0)
        background None
        tooltip "Enlarge"
        action SetScreenVariable("zoomed_image", journal_situation_full_image(image_path))
        use journal_situation_note_polaroid(metrics, image_path)
