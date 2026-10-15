##############################################################################
# Journal: Unlockables (page 4)
#
# Top ribbons filter by type (only when there is more than one type), the
# left page lists what is still to win and what is already unlocked, the
# right page shows one unlockable (or one stage of a group).
#
# display = "<unlockable key>" or "<unlockable key>:<group index>"
##############################################################################

init python:
    def journal_unlockable_on_agenda(unlockable) -> bool:
        proposal = get_game_data('voteProposal')
        return isinstance(proposal, Unlockable) and proposal.key == unlockable.key

    def journal_unlockable_state(unlockable):
        """
        Short state word for the list and the facts box, with its ink.
        """

        if unlockable.is_unlocked():
            return ("unlocked", JR_GREEN)
        if journal_unlockable_on_agenda(unlockable):
            return ("on the PTA agenda", JR_ACCENT)
        if unlockable.status == "active":
            if unlockable.is_paused():
                return ("paused", JR_PENCIL)
            return ("in progress", JR_PRINT)
        return ("not started", JR_PENCIL)

    def journal_unlockable_has_alert(unlockable_key: str) -> bool:
        # alerts are raised per member (situation key "rule:level:3"), the list row is the group
        return any(journal_has_alert("unlockables", member.key)
            for member in unlockable_manager.get_unlockables_by_key(unlockable_key))

    def journal_split_warning(line: str):
        """
        Description lines wrapped in "!!! ... !!!" are warnings; returns
        (is_warning, text without the marks).
        """

        stripped = line.strip()
        if stripped.startswith("!!!") and stripped.endswith("!!!") and len(stripped) > 6:
            return True, stripped[3:-3].strip()
        return False, line

screen journal_unlockables(display):
    # """
    # Unlockables page.
    # """

    tag interaction_overlay
    modal True

    python:
        type_filter = get_setting("journal_unlockables_type_filter")
        if type_filter is None:
            type_filter = ""
            set_setting("journal_unlockables_type_filter", "")
        type_keys = unlockable_manager.get_type_keys()
        if type_filter and type_filter not in type_keys:
            type_filter = ""
        incomplete_list, completed_list = unlockable_manager.get_list_entries(type_filter)

        requested_display = display
        # nothing picked (or picked one vanished): open the first entry
        if display == "" or unlockable_manager.resolve_display(display) is None:
            first = (incomplete_list or completed_list or [("", "")])[0][1]
            display = first
        active_unlockable = unlockable_manager.resolve_display(display) if display else None
        list_key = active_unlockable.unlockable_key if active_unlockable is not None else ""

        sub_entries = None
        if len(type_keys) > 1:
            sub_entries = [("All", (type_filter == ""),
                [Function(set_setting, "journal_unlockables_type_filter", ""), With(dissolveM), Call("open_journal", 4, "")])]
            for type_key in type_keys:
                sub_entries.append((get_translation(type_key), (type_filter == type_key),
                    [Function(set_setting, "journal_unlockables_type_filter", type_key), With(dissolveM), Call("open_journal", 4, "")]))

    use journal_backdrop

    key "K_ESCAPE" action [With(dissolveM), Jump("map_entry")]

    use journal_page_selector(4, display, sub_entries = sub_entries)

    use journal_unlockable_list(incomplete_list, completed_list, list_key)

    if active_unlockable is not None:
        # an entry the page opened by itself counts as seen, like a clicked one
        if requested_display != display:
            on "show" action Function(acknowledge_journal_alerts, 4, display)
        use journal_unlockable_detail(active_unlockable, display)

    use journal_tooltip

screen journal_unlockable_list(incomplete_list, completed_list, list_key):
    # """
    # Left page: what is still to win, then what is already unlocked (foldable).
    # """

    $ show_completed = get_setting("journal_setting_4_completed")
    if show_completed is None:
        $ show_completed = True

    use jr_page("journal_unlockable_list", JR_LEFT_X, JR_LEFT_W):
        vbox:
            xsize JR_LEFT_W

            fixed:
                xysize (JR_LEFT_W, 66)
                text "Unlockables" style "jr_title" yalign 1.0
                text "{} of {} unlocked".format(len(completed_list), len(completed_list) + len(incomplete_list)):
                    style "jr_typed_small"
                    xalign 1.0
                    yalign 1.0
                    yoffset -8
            null height 4
            use jr_double_rule(JR_LEFT_W)

            null height 22
            use jr_rubric("To win over", JR_LEFT_W)
            null height 4
            if incomplete_list:
                for title, unlockable_key in incomplete_list:
                    use journal_unlockable_entry(title, unlockable_key, (unlockable_key == list_key))
            else:
                text "Nothing left to push for right now." style "jr_small"

            if completed_list:
                null height 22
                button:
                    xsize JR_LEFT_W
                    background None
                    padding (0, 0, 0, 0)
                    action [With(dissolveM), Function(set_setting, "journal_setting_4_completed", not show_completed)]
                    tooltip ("Hide unlocked" if show_completed else "Show unlocked")
                    use jr_rubric("Unlocked ({}) · {}".format(len(completed_list), "hide" if show_completed else "show"), JR_LEFT_W)
                if show_completed:
                    null height 4
                    for title, unlockable_key in completed_list:
                        use journal_unlockable_entry(title, unlockable_key, (unlockable_key == list_key))

screen journal_unlockable_entry(title, unlockable_key, selected):
    $ member = unlockable_manager.get_default_member(unlockable_key)
    $ state_text, state_ink = journal_unlockable_state(member)

    fixed:
        xysize (JR_LEFT_W, 40)
        button:
            style "jr_entry_button"
            yalign 0.5
            selected selected
            action [With(dissolveM), Call("open_journal", 4, unlockable_key)]
            hbox:
                spacing 8
                text title style "jr_entry_button_text" size 24 yalign 0.5
                if journal_unlockable_has_alert(unlockable_key):
                    use jr_new_mark(unlockable_key)
        text state_text style "jr_text" size 21 font "fonts/CrimsonPro-Italic.ttf" color state_ink xalign 1.0 yalign 0.5

screen journal_unlockable_detail(unlockable, display):
    # """
    # Right page: photo and state, what it takes (pictograms), the
    # description and the next step.
    # """

    python:
        unlockable_key = unlockable.unlockable_key
        members = unlockable_manager.get_unlockables_by_key(unlockable_key)
        navigable = unlockable_manager.get_navigable_indices(unlockable_key)
        current_index = unlockable.group_index
        nav_pos = navigable.index(current_index) if current_index in navigable else -1

        subtitle = get_translation(unlockable.type_key)
        member_indices = [member.group_index for member in members]
        if current_index != -1 and len(members) > 1 and current_index in member_indices:
            subtitle += " · stage {} of {}".format(member_indices.index(current_index) + 1, len(members))

        thumbnail = unlockable.get_current_thumbnail()
        has_photo = bool(thumbnail) and not journal_is_placeholder_image(thumbnail)
        state_text, state_ink = journal_unlockable_state(unlockable)
        facts = [("Status", state_text, state_ink)]
        if unlockable.status == "active" and not unlockable.is_unlocked():
            facts.append(("PTA support", "{}%".format(int(round(unlockable.get_vote_probability() * 100))), JR_PRINT))
        pictograms = list(unlockable.get_pictogram_data().values())
        photo_w = 300
        photo_h = 251
        facts_w = JR_RIGHT_W - photo_w - 24 if has_photo else JR_RIGHT_W

    use jr_page("journal_unlockable_detail", JR_RIGHT_X, JR_RIGHT_W):
        vbox:
            xsize JR_RIGHT_W

            text unlockable.get_title() style "jr_title"
            null height 4
            use jr_double_rule(JR_RIGHT_W)
            null height 6
            fixed:
                xysize (JR_RIGHT_W, 34)
                text subtitle style "jr_typed_small" yalign 0.5
                # step through the stages of a group (unlocked ones plus the next to win)
                if nav_pos != -1 and len(navigable) > 1:
                    hbox:
                        xalign 1.0
                        yalign 0.5
                        spacing 4
                        if nav_pos > 0:
                            textbutton "‹ previous":
                                style "jr_entry_button"
                                text_style "jr_small"
                                action [With(dissolveM), Call("open_journal", 4, unlockable_manager.build_display(unlockable_key, navigable[nav_pos - 1]))]
                        if nav_pos < len(navigable) - 1:
                            textbutton "next ›":
                                style "jr_entry_button"
                                text_style "jr_small"
                                action [With(dissolveM), Call("open_journal", 4, unlockable_manager.build_display(unlockable_key, navigable[nav_pos + 1]))]

            null height 16
            hbox:
                spacing 24
                if has_photo:
                    button:
                        # fixed size: the tilted polaroid's bounding box is wider than its frame
                        xysize (photo_w, photo_h)
                        padding (0, 0, 0, 0)
                        background None
                        tooltip "Enlarge"
                        action [With(dissolveM), Call("call_max_image_from_journal", thumbnail, 4, display)]
                        use journal_polaroid(thumbnail, photo_w, photo_h, -1.5)
                vbox:
                    xsize facts_w
                    use jr_rubric("On record", facts_w)
                    null height 4
                    for label, value, ink in facts:
                        if journal_text_width(label, size = 22) + journal_text_width(value, style = "jr_value", size = 22) + 40 > facts_w:
                            text label style "jr_text" size 22
                            text value style "jr_value" size 22 color ink xalign 1.0
                            null height 6
                        else:
                            fixed:
                                xysize (facts_w, 32)
                                use jr_leader(journal_text_width(label, size = 22),
                                    facts_w - journal_text_width(value, style = "jr_value", size = 22))
                                text label style "jr_text" size 22 yalign 0.5
                                text value style "jr_value" size 22 color ink xalign 1.0 yalign 0.5

                    null height 16
                    use journal_unlockable_action(unlockable, display)

            if pictograms:
                null height 22
                use jr_rubric("What it takes", JR_RIGHT_W)
                null height 8
                $ cell_w = JR_RIGHT_W // 5
                $ picto_rows = (len(pictograms) + 4) // 5
                grid 5 picto_rows:
                    for entry in pictograms:
                        $ icon = find_loadable_image(entry.get("icon")) if entry.get("icon") is not None else ""
                        $ label = entry.get("label") or ""
                        button:
                            xsize cell_w
                            background None
                            padding (0, 0, 0, 0)
                            action NullAction()
                            tooltip (entry.get("tooltip") or label)
                            vbox:
                                xalign 0.5
                                spacing 4
                                if icon:
                                    add Transform(icon, xysize = (42, 42), alpha = 0.78) xalign 0.5
                                else:
                                    null height 42
                                text label style "jr_small" size 17 color JR_PRINT xalign 0.5 textalign 0.5 xmaximum cell_w - 8
                    for _ in range(-len(pictograms) % 5):
                        null

            $ descriptions = unlockable.get_descriptions()
            if descriptions:
                null height 22
                use jr_rubric("Description", JR_RIGHT_W)
                null height 6
                for line in descriptions:
                    $ is_warning, line_text = journal_split_warning(line)
                    if is_warning:
                        text line_text style "jr_text" size 20 font JR_FONT_BOLD color JR_ACCENT
                    else:
                        text line_text style "jr_body"
                    null height 4

screen journal_unlockable_action(unlockable, display):
    # """
    # The next step for this unlockable, written like a task in the planner.
    # """

    if unlockable.status == "inactive":
        textbutton "Start introducing it ›":
            style "jr_entry_button"
            text_style "jr_value"
            text_size 22
            text_color JR_ACCENT
            action Call("start_unlockable_situation", display)
    else:
        textbutton "Open its situation ›":
            style "jr_entry_button"
            text_style "jr_value"
            text_size 22
            text_color JR_ACCENT
            action [With(dissolveM), Call("open_journal", 8, unlockable.key)]
