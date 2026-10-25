##############################################################################
# Journal: Cheats (page 5, cheat mode only)
#
# Left page: the warning and the sections. Right page: the open section.
# Every control calls the same labels as before (switch_*, *_cheat,
# modify_stat, ...); only the look changed.
#
# display = section key ("" = general)
##############################################################################

init python:
    JOURNAL_CHEAT_SECTIONS = [
        ("general", "General"),
        ("stats", "Stats"),
        ("events", "Events"),
        ("situations", "Situations"),
        ("unlockables", "Unlockables"),
        ("items", "Items"),
        ("buildings", "Buildings"),
        ("mods", "Mods"),
        ("debug", "Debug"),
        ("logs", "Logs"),
    ]

    JOURNAL_CHEAT_DAYTIMES = [
        (1, "Morning"), (2, "Early Noon"), (3, "Noon"), (4, "Early Afternoon"),
        (5, "Afternoon"), (6, "Evening"), (7, "Night"),
    ]

style jr_cheat_link is jr_entry_button
style jr_cheat_link_text is jr_value:
    size 21
    color JR_ACCENT
    insensitive_color JR_PENCIL + "90"

screen journal_cheats(display, char = "school"):
    # """
    # Cheats page.
    # """

    tag interaction_overlay
    modal True

    $ section = display if display in [key for key, _ in JOURNAL_CHEAT_SECTIONS] else "general"
    $ section_title = dict(JOURNAL_CHEAT_SECTIONS)[section]

    use journal_backdrop

    key "K_ESCAPE" action journal_close_action()

    use journal_page_selector(5, display, char)

    use jr_page("journal_cheats_sections", JR_LEFT_X, JR_LEFT_W):
        vbox:
            xsize JR_LEFT_W

            text "Cheats" style "jr_title"
            null height 4
            use jr_double_rule(JR_LEFT_W)
            null height 12
            text "Changing game values can lead to unintended behaviour or a broken save. Most of this is meant for debugging during development — use it at your own risk.":
                style "jr_typed"
                size 18
                color JR_ACCENT

            null height 22
            use jr_rubric("Sections", JR_LEFT_W)
            null height 4
            for key, title in JOURNAL_CHEAT_SECTIONS:
                button:
                    style "jr_entry_button"
                    selected (key == section)
                    action [With(dissolveM), Call("open_journal", 5, key)]
                    text title style "jr_entry_button_text" size 24

    use jr_page("journal_cheats_" + section, JR_RIGHT_X, JR_RIGHT_W):
        vbox:
            xsize JR_RIGHT_W

            text section_title style "jr_title"
            null height 4
            use jr_double_rule(JR_RIGHT_W)
            null height 14

            if section == "general":
                use journal_cheats_general(section)
            elif section == "stats":
                use journal_cheats_stats(section)
            elif section == "events":
                use journal_cheats_events(section)
            elif section == "situations":
                use journal_cheats_situations()
            elif section == "unlockables":
                use journal_cheats_unlockables()
            elif section == "items":
                use journal_cheats_items()
            elif section == "buildings":
                use journal_cheats_buildings(section)
            elif section == "mods":
                use journal_cheats_mods()
            elif section == "debug":
                use journal_cheats_debug(section)
            elif section == "logs":
                use journal_cheats_logs(section)

    use journal_tooltip

##################
# region Parts  #

screen jr_cheat_note(note):
    text note style "jr_small"
    null height 14

screen jr_cheat_switch(label, on, action, on_text = "on", off_text = "off"):
    # """
    # A setting with its state in ink and a link that flips it.
    # """

    fixed:
        xysize (JR_RIGHT_W, 38)
        text label style "jr_text" size 22 yalign 0.5
        hbox:
            xalign 1.0
            yalign 0.5
            spacing 12
            text (on_text if on else off_text) style "jr_value" size 21 color (JR_GREEN if on else JR_PENCIL) yalign 0.5
            textbutton ("turn off" if on else "turn on"):
                style "jr_cheat_link"
                yalign 0.5
                action action

screen jr_cheat_action(label, link_text, action, sensitive = True):
    # """
    # A one-off action: what it does on the left, the link to run it on the right.
    # """

    $ link_w = journal_text_width(link_text, style = "jr_value", size = 21) + 14
    fixed:
        xysize (JR_RIGHT_W, 38)
        fixed:
            xysize (JR_RIGHT_W, 32)
            yalign 0.5
            use jr_leader(journal_text_width(label, size = 22), JR_RIGHT_W - link_w)
        text label style "jr_text" size 22 yalign 0.5
        textbutton link_text:
            style "jr_cheat_link"
            xalign 1.0
            yalign 0.5
            sensitive sensitive
            action action

# endregion
##################

#####################
# region Sections  #

screen journal_cheats_general(section):
    use jr_cheat_switch("Pick events manually", event_selection_mode,
        [With(dissolveM), Call("switch_event_select_mode", 5, section)])
    use jr_cheat_switch("Freeze time", time_freeze,
        [With(dissolveM), Call("switch_time_freeze", 5, section)], "frozen", "running")

    null height 18
    use jr_rubric("Set daytime", JR_RIGHT_W)
    null height 6
    hbox:
        box_wrap True
        xsize JR_RIGHT_W
        spacing 8
        for daytime, daytime_name in JOURNAL_CHEAT_DAYTIMES:
            textbutton daytime_name:
                style "jr_entry_button"
                text_style "jr_entry_button_text"
                text_size 21
                selected (time.get_daytime() == daytime)
                action Call("set_time_cheat", 5, section, daytime = daytime)

    null height 18
    use jr_rubric("Date", JR_RIGHT_W)
    null height 6
    text "Left-click moves forward, right-click moves back." style "jr_small"
    null height 4
    hbox:
        spacing 18
        for unit, unit_value in (("day", time.day), ("month", time.get_month_name()), ("year", time.year)):
            textbutton str(unit_value):
                style "jr_entry_button"
                text_style "jr_value"
                text_size 26
                tooltip "{} +1 / -1".format(unit.capitalize())
                action Call("change_time_cheat", 5, section, **{unit: 1})
                alternate Call("change_time_cheat", 5, section, **{unit: -1})

screen journal_cheats_stats(section):
    use jr_cheat_note("Changing stats can lead to unintended behaviour or a broken save.")
    use journal_cheats_stat(MONEY, "school")
    null height 6
    use jr_rubric("Levels", JR_RIGHT_W)
    for level_char in ("school", "parent", "teacher", "secretary"):
        use journal_cheats_stat(LEVEL, level_char)
    null height 6
    use jr_rubric("School stats", JR_RIGHT_W)
    for stat in (CORRUPTION, INHIBITION, HAPPINESS, EDUCATION, CHARM, REPUTATION):
        use journal_cheats_stat(stat, "school")

screen journal_cheats_stat(stat, char = "school"):
    # """
    # One stat with step buttons around its value: Min, a big and a small
    # step down, the value, the same steps up, Max. Money has no Min/Max.
    # """

    python:
        char_obj = get_character_by_key(char)
        if stat == MONEY:
            stat_label = "Money"
            stat_value = money.get_display_value()
            small, big = 100, 1000
        elif stat == LEVEL:
            stat_label = get_translation(char).capitalize()
            stat_value = get_level_for_char(char_obj)
            small, big = 1, 5
        else:
            stat_label = Stat_Data[stat].get_title()
            stat_value = char_obj.get_display_value(stat)
            small, big = 1, 10
        steps = []
        if stat != MONEY:
            steps.append(("min", -100))
        steps += [("−{}".format(big), -big), ("−{}".format(small) if small != 1 else "−", -small)]
        steps_up = [("+{}".format(small) if small != 1 else "+", small), ("+{}".format(big), big)]
        if stat != MONEY:
            steps_up.append(("max", 100))

    fixed:
        xysize (JR_RIGHT_W, 40)
        hbox:
            spacing 10
            yalign 0.5
            add Transform(get_stat_icon_path(stat if stat != LEVEL else "level", size = ICON_SMALL, white = False), xysize = (24, 24), alpha = 0.85) yalign 0.5
            text stat_label style "jr_text" size 22 yalign 0.5
        hbox:
            xalign 1.0
            yalign 0.5
            spacing 2
            for step_text, step in steps:
                textbutton step_text:
                    style "jr_entry_button"
                    text_style "jr_small"
                    text_color JR_PRINT
                    yalign 0.5
                    action Call("modify_stat", stat, step, char)
            text str(stat_value) style "jr_value" size 22 min_width 84 textalign 0.5 yalign 0.5
            for step_text, step in steps_up:
                textbutton step_text:
                    style "jr_entry_button"
                    text_style "jr_small"
                    text_color JR_PRINT
                    yalign 0.5
                    action Call("modify_stat", stat, step, char)

screen journal_cheats_events(section):
    $ can_start = not journal_in_game_menu()
    if can_start:
        use jr_cheat_note("Start any registered event directly. Starting one closes the journal.")
    else:
        use jr_cheat_note("Events can only be started from the map, not while one is running.")
    fixed:
        xysize (JR_RIGHT_W, 38)
        text "Replay category" style "jr_text" size 22 yalign 0.5
        textbutton str(event_cheat_category):
            style "jr_cheat_link"
            xalign 1.0
            yalign 0.5
            tooltip "Next category"
            action [With(dissolveM), Call("cycle_event_cheat_filter", 5, section)]
    null height 10

    $ cheat_events = get_filtered_cheat_events(event_cheat_category)
    if not cheat_events:
        text "No events registered." style "jr_small"
    for cheat_event in cheat_events:
        fixed:
            xysize (JR_RIGHT_W, 34)
            button:
                style "jr_entry_button"
                yalign 0.5
                sensitive can_start
                tooltip cheat_event.event_id
                action [With(dissolveM), Call("call_event_cheat", cheat_event.event_id)]
                text cheat_event.get_title(quiet = True) style "jr_entry_button_text" size 20
            text str(getattr(cheat_event, "replay_category", "Misc")) style "jr_small" size 17 xalign 1.0 yalign 0.5

screen journal_cheats_situations():
    use jr_cheat_note("Activate or deactivate situations and unlock their notes. Expand one to reach its single notes.")

    $ cheat_situations = get_cheat_situation_list()
    if not cheat_situations:
        text "No situations registered." style "jr_small"
    for cheat_situation in cheat_situations:
        $ sit_key = cheat_situation.key
        $ sit_expanded = is_situation_cheat_expanded(sit_key)
        $ sit_state = cheat_situation.visibility_state
        if cheat_situation.is_paused():
            $ sit_state += ", paused: " + "+".join(cheat_situation.get_pause_reasons())
        fixed:
            xysize (JR_RIGHT_W, 36)
            button:
                style "jr_entry_button"
                yalign 0.5
                tooltip ("Collapse" if sit_expanded else "Show its notes")
                action Function(toggle_situation_cheat_expand, sit_key)
                text cheat_situation.name style "jr_entry_button_text" size 22 font JR_FONT_SEMIBOLD
            text sit_state style "jr_small" size 17 xalign 1.0 yalign 0.5
        hbox:
            xoffset 18
            spacing 6
            textbutton "activate":
                style "jr_cheat_link"
                sensitive cheat_situation.state != "active"
                action [With(dissolveM), Call("activate_situation_cheat", sit_key)]
            textbutton "deactivate":
                style "jr_cheat_link"
                sensitive cheat_situation.state == "active"
                action [With(dissolveM), Call("deactivate_situation_cheat", sit_key)]
            textbutton ("resume" if "manual" in cheat_situation.get_pause_reasons() else "pause"):
                style "jr_cheat_link"
                sensitive cheat_situation.state == "active"
                action [With(dissolveM), Call("toggle_pause_situation_cheat", sit_key)]
            textbutton "all notes":
                style "jr_cheat_link"
                action [With(dissolveM), Call("activate_situation_teasers_cheat", sit_key)]
        if sit_expanded:
            if not cheat_situation.teasers:
                text "No notes." style "jr_small" xoffset 36
            for teaser_key, cheat_teaser in cheat_situation.teasers.items():
                fixed:
                    xysize (JR_RIGHT_W, 30)
                    hbox:
                        xoffset 36
                        spacing 10
                        yalign 0.5
                        add ("gui/journal/ui/box_full.webp" if cheat_teaser.active else "gui/journal/ui/box_empty.webp") yalign 0.5
                        text teaser_key style "jr_text" size 18 yalign 0.5
                    textbutton "activate":
                        style "jr_cheat_link"
                        text_size 18
                        xalign 1.0
                        yalign 0.5
                        sensitive not cheat_teaser.active
                        action [With(dissolveM), Call("activate_teaser_cheat", sit_key, teaser_key)]
        null height 12

screen journal_cheats_unlockables():
    use jr_cheat_note("Force an unlockable to be visible. \"auto\" leaves it to its own conditions.")

    $ cheat_unlockables = get_cheat_unlockable_list()
    if not cheat_unlockables:
        text "No unlockables registered." style "jr_small"
    for cheat_unlockable in cheat_unlockables:
        $ unlock_override = getattr(cheat_unlockable, "override_visible", False)
        $ unlock_name = cheat_unlockable.name + (" ({})".format(cheat_unlockable.group_index) if cheat_unlockable.group_index != -1 else "")
        use jr_cheat_switch(unlock_name, unlock_override,
            [With(dissolveM), Call("toggle_unlockable_visibility_cheat", get_unlockable_cheat_display(cheat_unlockable))],
            "visible", "auto")

screen journal_cheats_items():
    use jr_cheat_note("Add any registered item. Left-click adds one, right-click adds ten.")
    use jr_cheat_action("Every item once", "add all", [With(dissolveM), Call("give_every_item", 5, "items")])
    null height 10

    $ cheat_items = get_cheat_item_list()
    if not cheat_items:
        text "No items registered." style "jr_small"
    for cheat_item in cheat_items:
        $ item_count = "× {}".format(inventory_manager.get_item_count(cheat_item.key))
        fixed:
            xysize (JR_RIGHT_W, 36)
            text cheat_item.get_name() style "jr_text" size 22 yalign 0.5
            hbox:
                xalign 1.0
                yalign 0.5
                spacing 14
                text item_count style "jr_value" size 20 color JR_PENCIL yalign 0.5
                textbutton "add":
                    style "jr_cheat_link"
                    yalign 0.5
                    action [With(dissolveM), Call("add_item_cheat", cheat_item.key, 1)]
                    alternate [With(dissolveM), Call("add_item_cheat", cheat_item.key, 10)]

screen journal_cheats_buildings(section):
    use jr_cheat_note("Force buildings open or closed. Opening clears every close reason.")

    if building_manager is None or not building_manager.get_buildings():
        text "No buildings registered." style "jr_small"
    else:
        for building in sorted(building_manager.get_buildings(), key = lambda b: b.get_name()):
            $ b_open = building.is_open()
            fixed:
                xysize (JR_RIGHT_W, 38)
                text building.get_name() style "jr_text" size 22 yalign 0.5
                hbox:
                    xalign 1.0
                    yalign 0.5
                    spacing 12
                    text ("open" if b_open else "closed") style "jr_value" size 21 color (JR_GREEN if b_open else JR_ACCENT) yalign 0.5
                    textbutton ("close" if b_open else "open"):
                        style "jr_cheat_link"
                        yalign 0.5
                        action [With(dissolveM), Call("set_building_state_cheat", 5, section, building.key, ("closed" if b_open else "open"))]

screen journal_cheats_mods():
    use jr_cheat_note("After switching a mod the game has to be reloaded. Only works in developer mode.")

    for mod_key, mod in persistent.modList.items():
        if mod['available']:
            if mod['name'] == 'Base Mod':
                fixed:
                    xysize (JR_RIGHT_W, 38)
                    text mod['name'] style "jr_text" size 22 yalign 0.5
                    text "always on" style "jr_value" size 21 color JR_GREEN xalign 1.0 yalign 0.5
            else:
                use jr_cheat_switch(mod['name'], mod['active'],
                    [With(dissolveM), Call("switch_mod", mod_key, not mod['active'])], "active", "inactive")

screen journal_cheats_debug(section):
    use jr_cheat_switch("Debug mode", debug_mode, [With(dissolveM), Call("switch_debug_mode", 5, section)])

    null height 14
    use jr_rubric("Game data", JR_RIGHT_W)
    null height 6
    text "Type a game-data key to look it up:" style "jr_small"
    frame:
        xsize JR_RIGHT_W
        background Frame("gui/journal/ui/underline.webp", 10, 26, 10, 6)
        padding (6, 2, 6, 6)
        input:
            value VariableInputValue("game_data_input")
            style "jr_typed"
            size 20
    if game_data_old != game_data_input:
        $ display_game_data_journal(game_data_input)
    null height 6
    text "Value: " + str(game_data_output) style "jr_typed" size 18
    text "Progress: " + str(progress_output) style "jr_typed" size 18

    null height 14
    use jr_rubric("Tools", JR_RIGHT_W)
    null height 4
    # these leave the journal for the game; not from the game menu mid event
    $ can_leave = not journal_in_game_menu()
    use jr_cheat_action("Test label", "run", Call("test_label"), can_leave)
    use jr_cheat_action("Paperdoll test", "open", Call("show_paperdoll_test"), can_leave)
    use jr_cheat_action("Situation test lab", "open", Call("situation_test_lab"), can_leave)
    use jr_cheat_action("Every item once", "add all", Call("give_every_item", 5, section))

    null height 14
    use jr_rubric("Names", JR_RIGHT_W)
    null height 4
    use jr_cheat_switch("Log missing names", persistent.log_missing_names,
        [With(dissolveM), ToggleField(persistent, "log_missing_names")])
    $ can_validate = name_validator_available()
    use jr_cheat_action("Check names files", "run", Call("validate_names_cheat"), can_validate)
    use jr_cheat_action("…and list unnamed events", "run", Call("validate_names_cheat", list_events = True), can_validate)
    if not can_validate:
        text "tools/validate_names.py is missing (not part of builds)." style "jr_small"

    null height 14
    use jr_rubric("Gallery", JR_RIGHT_W)
    null height 4
    use jr_cheat_action("Gallery data to the log", "dump", [With(dissolveM), Call("dump_gallery_data", 5, section)])
    use jr_cheat_action("Delete all gallery data", "reset now", [With(dissolveM), Call("reset_gallery_cheat", 5, section)])

screen journal_cheats_logs(section):
    use jr_cheat_note("Session logs (log, log_val, log_json, log_separator). Cleared on restart.")

    for filter_key, filter_value in (("type", log_filter_type), ("category", log_filter_category), ("origin", log_filter_origin)):
        fixed:
            xysize (JR_RIGHT_W, 34)
            text filter_key.capitalize() style "jr_text" size 22 yalign 0.5
            textbutton str(filter_value):
                style "jr_cheat_link"
                xalign 1.0
                yalign 0.5
                tooltip "Next {}".format(filter_key)
                action [With(dissolveM), Call("cycle_log_filter", filter_key, 5, section)]
    use jr_cheat_action("All log entries", "clear now", [With(dissolveM), Call("clear_logs_cheat", 5, section)])

    null height 10
    add Solid(JR_PRINT + "40") xysize (JR_RIGHT_W, 1)
    null height 10

    $ filtered_logs = get_filtered_game_logs(log_filter_type, log_filter_category, log_filter_origin)
    if not filtered_logs:
        text "No log entries." style "jr_small"
    for log_entry in filtered_logs:
        if log_entry.get("is_json"):
            use journal_log_json_entry(log_entry)
        else:
            text format_game_log_entry(log_entry) style "jr_typed" size 14 xmaximum JR_RIGHT_W
        null height 6

# endregion
#####################
