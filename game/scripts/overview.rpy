init -1 python:
    def hide_all():
        """
        hides all screens
        """

        for s in renpy.display.screen.screens_by_name:
            renpy.hide_screen(s)

    OVERVIEW_STAT_ORDER = (
        HAPPINESS, CHARM, EDUCATION, MONEY, CORRUPTION, INHIBITION, REPUTATION
    )

    def get_overview_stat_change_value(stat: str):
        """
        Returns the numeric change of a school stat since the last reset.

        ### Parameters:
        1. stat: str
            - The stat key to read.

        ### Returns:
        1. num
            - The change value. 0 if the stat cannot be resolved.
        """

        if stat == MONEY:
            return money.get_changed_value()

        stat_obj = get_school().get_stat_obj(stat)
        if stat_obj is None:
            return 0
        return stat_obj.get_changed_value()

    def get_overview_stat_change_color(stat: str, change) -> str:
        """
        Returns the HUD colour for a stat change.

        Increase is green and decrease is red. Inhibition is inverted.

        ### Parameters:
        1. stat: str
            - The stat key.
        2. change: num
            - The numeric change since the last reset.

        ### Returns:
        1. str
            - A hex colour string.
        """

        if change == 0:
            return "#ffffff"

        increased = change > 0
        beneficial = (not increased) if stat == INHIBITION else increased
        return "#00a000" if beneficial else "#a00000"

    OVERVIEW_TENDENCY_ARROWS_POS = (">", "≫", "⋙")
    OVERVIEW_TENDENCY_ARROWS_NEG = ("<", "≪", "⋘")

    def get_overview_active_situations():
        """
        Returns active situations for the map HUD list.

        Returns:
            list: Active Situation objects. Empty if the manager is missing.
        """

        if situation_manager is None:
            return []
        return situation_manager.get_active_situations()

    def get_overview_situation_tendency(situation):
        """
        Map HUD tendency glyph, side and colour from combined-bar movement.

        Strength is 1..3 from |tendency| relative to the combined bar span.
        Positive movement places the glyph on the right, negative on the left.

        Args:
            situation: Situation whose combined bar to read.

        Returns:
            tuple: (glyph, side, color). side is 1 (right), -1 (left), or 0.
        """

        raw = situation.get_combined_bar_tendency_value()
        span = float(situation.get_combined_bar_max() - situation.get_combined_bar_min()) or 1.0
        ratio = abs(raw) / span
        if raw == 0:
            return "", 0, "#ffffff"
        if ratio < (1.0 / 24.0):
            level = 1
        elif ratio < (1.0 / 10.0):
            level = 2
        else:
            level = 3
        if raw > 0:
            return OVERVIEW_TENDENCY_ARROWS_POS[level - 1], 1, "#4cc94c"
        return OVERVIEW_TENDENCY_ARROWS_NEG[level - 1], -1, "#e06060"

default persistent.overview_stats_expanded = True
default persistent.overview_situations_expanded = True

define OVERVIEW_COMPACT_BAR_WIDTH = 460
define OVERVIEW_STAT_ICON_ZOOM = 0.52
define OVERVIEW_STAT_TEXT_SIZE = 21
define OVERVIEW_TIME_TEXT_SIZE = 20
define OVERVIEW_SITUATION_LIST_MAX_HEIGHT = 224
define OVERVIEW_SITUATION_ROW_HEIGHT = 64
define OVERVIEW_SITUATION_ARROW_WIDTH = 28
define OVERVIEW_SITUATION_SCROLL_WIDTH = 12
define OVERVIEW_SPLIT_BAR_HEIGHT = 46

#######################
# region Styles ----- #
#######################

style stat_overview:
    outlines [(2, "222222", 1, 1)]
    color "#ffffff"
    size 16

style stat_value:
    outlines [(2, "222222", 1, 1)]
    color "#ffffff"
    size 16

style overview_hud_bar:
    background Solid("#111111cc")
    padding (8, 6, 10, 6)

style overview_hud_bar_soft is overview_hud_bar:
    background Solid("#11111177")

style overview_hud_button is default:
    hover_background Solid("#ffffff18")
    padding (4, 2)

style overview_situation_row is overview_hud_button:
    background Solid("#11111199")
    hover_background Solid("#222222bb")
    padding (6, 4, 6, 4)

style overview_vscrollbar is vscrollbar:
    xsize 12
    unscrollable "hide"

style overview_hud_button_text is stat_overview:
    size 21

style overview_split_button is overview_hud_button:
    background Solid("#00000000")
    hover_background Solid("#ffffff22")
    padding (8, 0)
    yminimum OVERVIEW_SPLIT_BAR_HEIGHT

style overview_toggle_button is overview_hud_button:
    xminimum 29
    yminimum 29

style overview_toggle_button_text is stat_overview:
    size 21
    xalign 0.5
    yalign 0.5

transform overview_icon_tint(tint_color):
    matrixcolor TintMatrix(tint_color)

# endregion
#######################

###########################
# region Map Screen ----- #
###########################

screen school_overview():
    use school_overview_map
    use school_overview_stats
    use school_overview_buttons

###################################
# display the school map with stats
screen school_overview_map ():
    # """
    # Displays the school map
    # """

    add "background/school_map.webp"

##############################
# display the stats on the map
screen overview_stat_entry(stat, compact, interactive):
    $ title = Stat_Data[stat].get_title()
    $ change = get_overview_stat_change_value(stat)
    $ icon_path = get_stat_icon_path(stat, size=ICON_SMALL)
    $ stat_action = Call("open_journal", 1, stat) if interactive else NullAction()

    if compact:
        $ change_color = get_overview_stat_change_color(stat, change)
        $ change_arrow = "▲" if change > 0 else "▼"
        button:
            style "overview_hud_button"
            tooltip title + " " + get_school_stat_value(stat)
            action stat_action
            hbox:
                spacing 2
                yalign 0.5
                add icon_path:
                    yalign 0.5
                    zoom OVERVIEW_STAT_ICON_ZOOM
                    at overview_icon_tint(change_color)
                text change_arrow:
                    style "stat_overview"
                    color change_color
                    size 18
                    yalign 0.5
    else:
        $ change_text = get_school_stat_change(stat).replace("{size=15}", "{size=20}")
        button:
            style "overview_hud_button"
            tooltip title
            action stat_action
            hbox:
                spacing 3
                yalign 0.5
                add icon_path:
                    yalign 0.5
                    zoom OVERVIEW_STAT_ICON_ZOOM
                text get_school_stat_value(stat):
                    style "stat_value"
                    size OVERVIEW_STAT_TEXT_SIZE
                    yalign 0.5
                if change_text:
                    text change_text:
                        style "stat_overview"
                        yalign 0.5

screen overview_situation_entry(situation, interactive, row_width):
    $ glyph, side, arrow_color = get_overview_situation_tendency(situation)
    $ sit_action = Call("open_journal", 8, situation.key) if interactive else NullAction()
    $ bar_width = row_width - 12 - (OVERVIEW_SITUATION_ARROW_WIDTH * 2) - 8

    button:
        style "overview_situation_row"
        tooltip situation.name
        action sit_action
        xsize row_width

        vbox:
            spacing 2

            text situation.name:
                style "stat_overview"
                size 13
                xmaximum row_width - 12

            hbox:
                spacing 4
                yalign 0.5

                fixed:
                    xsize OVERVIEW_SITUATION_ARROW_WIDTH
                    ysize 22
                    if side < 0:
                        text glyph:
                            style "stat_overview"
                            color arrow_color
                            size 16
                            xalign 1.0
                            yalign 0.5

                use journal_situation_bar(situation, bar_width, 12, False, 8, 4)

                fixed:
                    xsize OVERVIEW_SITUATION_ARROW_WIDTH
                    ysize 22
                    if side > 0:
                        text glyph:
                            style "stat_overview"
                            color arrow_color
                            size 16
                            xalign 0.0
                            yalign 0.5

screen overview_situation_list(situations, interactive, row_width):
    vbox:
        xsize row_width
        spacing 0

        for i, situation in enumerate(situations):
            if i > 0:
                add Solid("#ffffff40"):
                    xsize row_width
                    ysize 1
                null height 4
            use overview_situation_entry(situation, interactive, row_width)
            null height 4

screen school_overview_stats (interactive = True):
    # """
    # Displays the stats and time bars on the map.
    # """

    zorder 80

    $ expanded = persistent.overview_stats_expanded
    $ can_skip = interactive and time.compare_today(10, 1, 2023) != -1

    $ daytimestr = time.get_daytime_name()
    $ daystr = time.get_weekday()
    $ monthstr = time.get_month_name()
    $ datestr = str(time.day) + " " + monthstr + " " + str(time.year)
    $ daytime_color = "#ffffff"
    if time.check_daytime("n"):
        $ daytime_color = "#6d78ff"
    elif time.check_weekday("d") and time.check_daytime("c"):
        $ daytime_color = "#e06060"
    elif time.check_weekday("d") and time.check_daytime("f"):
        $ daytime_color = "#4cc94c"
    elif time.check_weekday("w"):
        $ daytime_color = "#d4893a"

    $ skip_time_text = "Skip Time"
    $ skip_day_text = "Skip to next day"
    if has_keyboard() and show_shortcut():
        $ skip_time_text = skip_time_text + " [[Z]"
        $ skip_day_text = skip_day_text + " [[U]"

    if can_skip:
        if has_keyboard():
            key "K_z" action Call("skip_time")
            key "K_u" action Call("new_day")

    vbox:
        xalign 1.0
        yalign 0.0
        xoffset -8
        yoffset 6
        spacing 4

        frame:
            style "overview_hud_bar"
            if not expanded:
                xsize OVERVIEW_COMPACT_BAR_WIDTH

            hbox:
                spacing 8
                yalign 0.5

                textbutton ("▶" if expanded else "◀"):
                    style "overview_toggle_button"
                    tooltip ("Collapse stats" if expanded else "Expand stats")
                    action ToggleField(persistent, "overview_stats_expanded")
                    yalign 0.5

                hbox:
                    spacing 8
                    yalign 0.5

                    for stat in OVERVIEW_STAT_ORDER:
                        if expanded:
                            use overview_stat_entry(stat, False, interactive)
                        elif get_overview_stat_change_value(stat) != 0:
                            use overview_stat_entry(stat, True, interactive)

        frame:
            style "overview_hud_bar"
            xsize OVERVIEW_COMPACT_BAR_WIDTH
            xalign 1.0

            fixed:
                xsize OVERVIEW_COMPACT_BAR_WIDTH - 18
                ysize 32

                hbox:
                    xalign 0.0
                    yalign 0.5
                    spacing 10

                    button:
                        style "overview_hud_button"
                        tooltip (skip_day_text if can_skip else datestr)
                        action (Call("new_day") if can_skip else NullAction())
                        text datestr:
                            style "stat_overview"
                            size OVERVIEW_TIME_TEXT_SIZE

                    text daystr:
                        style "stat_overview"
                        size OVERVIEW_TIME_TEXT_SIZE
                        yalign 0.5

                button:
                    style "overview_hud_button"
                    xalign 1.0
                    yalign 0.5
                    tooltip (skip_time_text if can_skip else daytimestr)
                    action (Call("skip_time") if can_skip else NullAction())
                    text daytimestr:
                        style "stat_overview"
                        size OVERVIEW_TIME_TEXT_SIZE
                        color daytime_color

        $ overview_situations = get_overview_active_situations()
        $ split_w = OVERVIEW_COMPACT_BAR_WIDTH // 2
        $ journal_action = Call("start_journal") if interactive else NullAction()
        $ journal_tip = "Open Journal"
        $ journal_icon = get_journal_map_icon()
        if has_keyboard() and show_shortcut():
            $ journal_tip = journal_tip + " [[J]"

        frame:
            background Solid("#11111177")
            padding (0, 0, 0, 0)
            xsize OVERVIEW_COMPACT_BAR_WIDTH
            ysize OVERVIEW_SPLIT_BAR_HEIGHT
            xalign 1.0

            hbox:
                spacing 0
                xfill True
                yfill True

                button:
                    style "overview_split_button"
                    xsize split_w
                    yfill True
                    tooltip ("Collapse situations" if persistent.overview_situations_expanded else "Expand situations")
                    action ToggleField(persistent, "overview_situations_expanded")

                    hbox:
                        spacing 6
                        yalign 0.5
                        xoffset 8

                        text ("▼" if persistent.overview_situations_expanded else "▶"):
                            style "stat_overview"
                            size OVERVIEW_TIME_TEXT_SIZE
                            yalign 0.5

                        text "Situations":
                            style "stat_overview"
                            size OVERVIEW_TIME_TEXT_SIZE
                            yalign 0.5

                        if not persistent.overview_situations_expanded:
                            text ("(" + str(len(overview_situations)) + ")"):
                                style "stat_overview"
                                size OVERVIEW_TIME_TEXT_SIZE
                                yalign 0.5

                add Solid("#ffffff50"):
                    xsize 1
                    ysize OVERVIEW_SPLIT_BAR_HEIGHT - 12
                    yalign 0.5

                button:
                    style "overview_split_button"
                    xsize split_w
                    yfill True
                    tooltip journal_tip
                    action journal_action

                    hbox:
                        spacing 6
                        xalign 0.5
                        yalign 0.5

                        add journal_icon:
                            yalign 0.5
                            zoom 0.18

                        text "Journal":
                            style "stat_overview"
                            size OVERVIEW_TIME_TEXT_SIZE
                            yalign 0.5

        if persistent.overview_situations_expanded and overview_situations:
            $ sit_count = len(overview_situations)
            $ sit_content_h = sit_count * OVERVIEW_SITUATION_ROW_HEIGHT
            $ needs_scroll = sit_content_h > OVERVIEW_SITUATION_LIST_MAX_HEIGHT
            $ sit_view_h = OVERVIEW_SITUATION_LIST_MAX_HEIGHT if needs_scroll else sit_content_h
            $ sit_row_w = OVERVIEW_COMPACT_BAR_WIDTH - (OVERVIEW_SITUATION_SCROLL_WIDTH if needs_scroll else 0)

            frame:
                background Solid("#00000000")
                padding (0, 0, 0, 0)
                xsize OVERVIEW_COMPACT_BAR_WIDTH
                xalign 1.0

                if needs_scroll:
                    side "c r":
                        xsize OVERVIEW_COMPACT_BAR_WIDTH
                        ysize sit_view_h

                        viewport id "OverviewSituationsList":
                            mousewheel True
                            draggable "touch"

                            use overview_situation_list(overview_situations, interactive, sit_row_w)

                        vbar:
                            style "overview_vscrollbar"
                            value YScrollValue("OverviewSituationsList")
                            unscrollable "hide"
                            xsize OVERVIEW_SITUATION_SCROLL_WIDTH
                            ysize sit_view_h
                else:
                    use overview_situation_list(overview_situations, interactive, sit_row_w)

    $ tooltip = GetTooltip()

    if tooltip:
        nearrect:
            focus "tooltip"
            prefer_top True

            frame:
                xalign 0.5
                text tooltip

##################################
# display all buildings on the map
screen school_overview_images ():
    # """
    # Displays all buildings on the map
    # """

    add "background/school_map.webp"

    $ map_buildings = building_manager.get_buildings()
    for building in map_buildings:
        if building.is_open():
            $ idle_image = find_loadable_image(building.get_image("idle"))
            if idle_image:
                add idle_image:
                    xpos building.x_pos ypos building.y_pos
        else:
            $ empty_image = find_loadable_image(building.get_image("empty"))
            if empty_image:
                add empty_image:
                    xpos building.x_pos ypos building.y_pos

############################################################################
# display clickable buttons for the buildings leading to building distributor
screen school_overview_buttons (with_available_Events = False):
    # """
    # Displays clickable buttons for the buildings leading to building distributor
    # """

    tag interaction_overlay
    # modal True
    
    $ map_buildings = building_manager.get_buildings()
    for building in map_buildings:
        if building.is_open():
            if has_keyboard() and building.has_shortcut():
                for shortcut in building.get_renpy_keys():
                    key shortcut action Call("building", building.key)
            $ image_text = find_loadable_image(building.get_image("idle"))
            if get_available_event(building.key):
                $ image_text = find_loadable_image(building.get_image("available")) or image_text
            if with_available_Events and get_available_highlight(building.key):
                $ image_text = find_loadable_image(building.get_image("red")) or image_text
            if image_text:
                imagebutton:
                    idle image_text
                    hover find_loadable_image(building.get_image("white")) or image_text
                    tooltip building.get_name(with_shortcut = True)
                    focus_mask True
                    xpos building.x_pos ypos building.y_pos
                    action Call("building", building.key)
        else:
            # Mods may supply an "empty" sprite for buildings not on the base map.
            # Native buildings are already baked into the map art and have no empty image —
            # skip the button entirely so there is nothing to select.
            $ empty_image = find_loadable_image(building.get_image("empty"))
            if empty_image:
                imagebutton:
                    idle empty_image
                    insensitive empty_image
                    focus_mask True
                    xpos building.x_pos ypos building.y_pos
                    action NullAction()
                    sensitive False

    key "K_j" action Call("start_journal")

    $ tooltip = GetTooltip()

    if tooltip:
        nearrect:
            focus "tooltip"
            prefer_top True

            frame:
                xalign 0.5
                text tooltip

# endregion
###########################

###############################
# region Map Overview Entries #
###############################

# goes to map overview while moving the time forward
label set_day_and_time(day, month, year, daytime):
    # """
    # sets the day and time and then goes to map overview

    # # Parameters:
    # 1. day: int
    #     - the day of the month
    # 2. month: int
    #     - the month of the year
    # 3. year: int
    #     - the year
    # 4. daytime: str
    #     - the daytime
    # """

    $ time.set_time(day = day, month = month, year = year, daytime = daytime)

    $ hide_all()

    call screen black_screen_text (f"{time.get_weekday()}, {time.day} {time.get_month_name()} {time.year}")
    
    call time_event_check from set_day_2

    jump map_overview

label set_day(day, month, year):
    # """
    # sets the day and then goes to map overview

    # # Parameters:
    # 1. day: int
    #     - the day of the month
    # 2. month: int
    #     - the month of the year
    # 3. year: int
    #     - the year
    # """

    $ time.set_time(day = day, month = month, year = year)

    $ hide_all()

    call screen black_screen_text (f"{time.get_weekday()}, {time.day} {time.get_month_name()} {time.year}")
    
    call time_event_check from set_day_3

    jump map_overview

label new_day ():
    # """
    # progresses the day and then goes to map overview
    # """

    if not time_freeze:
        $ time.progress_day()

    $ hide_all()

    call screen black_screen_text (f"{time.get_weekday()}, {time.day} {time.get_month_name()} {time.year}")
    $ renpy.force_autosave()
    
    call time_event_check from new_day_2

    $ quest_manager.check_task_type("daytime_change")
    $ quest_manager.check_task_type("day_change")

    jump map_overview

label new_daytime ():
    # """
    # progresses the daytime and then goes to map overview
    # """

    $ hide_all()

    if not time_freeze and time.progress_time():
        call screen black_screen_text (f"{time.get_weekday()}, {time.day} {time.get_month_name()} {time.year}")
        $ renpy.force_autosave()

    call time_event_check from new_daytime_2

    $ quest_manager.check_task_type("daytime_change")

    jump map_overview

label after_load_entry():

    $ clean_legacy_vote_proposal()

    call time_event_check from call_after_load_entry_1

    jump map_entry

label map_entry():

    # stop sound fadeout 1.0

    jump map_overview

# shows the map overview and then waits for input
label map_overview ():
    if len(headmaster_proficiencies.keys()) < 2 and (IntroCondition(False)).is_fulfilled():
        if persistent.tutorial:
            subtitles "Tutorials are currently deactivated. To enable them, go to the settings."
        else:
            subtitles "Tutorials are currently activated. To deactivate them, go to the settings."
        call check_missing_proficiencies from map_overview_6
    
    # $ _skipping = False
    $ image_code = get_random_int(0, 1000000)
    # $ renpy.pause(0)
    call empty_label from map_overview_1
    call empty_label from map_overview_2
    call empty_label from map_overview_3
    call empty_label from map_overview_4
    call empty_label from map_overview_5
    
    $ hide_all()

    $ reroll_selectors()

    # $ check_old_versions()

    $ is_in_replay = False

    $ renpy.choice_for_skipping()

    $ call_notify()

    $ quest_manager.check_all()
    $ quest_manager.update_complete_all()

    $ situation_manager.check_all_thresholds()
    $ situation_manager.check_passives()
    $ situation_manager.check_resolutions()

    if not debug_mode:
        # keep only the last 100 entries in the return stack
        $ renpy.set_return_stack(renpy.get_return_stack()[-100:])

    show school_map
    # show screen school_overview_map
    show screen school_overview_stats 

    $ log_separator()

    $ update_available_highlights()

    $ update_available_events()

    $ renpy.block_rollback()

    if time.get_daytime() < 7:
        $ play_sound(audio.forest_ambience, True, 0.8, 1.0)
    else:
        $ play_sound(audio.night_ambience, True, 0.8, 1.0)

    call screen school_overview_buttons (True)
    # call screen school_overview with dissolveM

    $ renpy.pause(hard = True)

# endregion
###############################

###############################
# region Map Overview targets #
###############################

label building(name=""):
    $ reset_stats()
    $ _skipping = True

    $ notify_messages = []

    hide screen school_overview_map
    hide screen school_overview_stats
    hide screen school_overview_buttons

    $ hide_all()

    # $ image_code = name + str(time.get_daytime_name()) + str(time.get_day()) + str(time.get_month_name()) + str(time.year)

    call expression name from building_1

    call map_entry from building_2

label skip_time ():
    $ reset_stats()

    call new_daytime from skip_time_1

label empty_label ():
    return

# endregion
###############################