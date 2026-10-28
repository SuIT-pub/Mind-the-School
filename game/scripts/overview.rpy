init -1 python:
    def hide_all():
        """
        hides all screens
        """

        for s in renpy.display.screen.screens_by_name:
            # notifications shown right away stay up across scene changes
            if s == "notify_container":
                continue
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
            return OVERVIEW_CREAM

        increased = change > 0
        beneficial = (not increased) if stat == INHIBITION else increased
        return OVERVIEW_GOOD if beneficial else OVERVIEW_BAD

    def get_overview_stat_change_text(stat: str) -> str:
        """
        The stat's change since the last reset as HUD text: the shared
        display string, recoloured for the dark leather strap.

        ### Parameters:
        1. stat: str
            - The stat key.

        ### Returns:
        1. str
            - Text with Ren'Py text tags, empty when nothing changed.
        """

        change_text = get_school_stat_change(stat)
        return (change_text.replace("{size=15}", "")
                .replace("{/size}", "")
                .replace("#00a000", OVERVIEW_GOOD)
                .replace("#a00000", OVERVIEW_BAD))

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

        if situation.is_paused():
            return "", 0, JR_PRINT
        raw = situation.get_combined_bar_tendency_value()
        span = float(situation.get_combined_bar_max() - situation.get_combined_bar_min()) or 1.0
        ratio = abs(raw) / span
        if raw == 0:
            return "", 0, JR_PRINT
        if ratio < (1.0 / 24.0):
            level = 1
        elif ratio < (1.0 / 10.0):
            level = 2
        else:
            level = 3
        if raw > 0:
            return OVERVIEW_TENDENCY_ARROWS_POS[level - 1], 1, JR_GREEN
        return OVERVIEW_TENDENCY_ARROWS_NEG[level - 1], -1, JR_ACCENT

default persistent.overview_stats_expanded = True
default persistent.overview_situations_expanded = True

define OVERVIEW_COMPACT_BAR_WIDTH = 460
define OVERVIEW_STAT_ICON_ZOOM = 0.52
define OVERVIEW_SITUATION_LIST_MAX_HEIGHT = 244
define OVERVIEW_SITUATION_ROW_HEIGHT = 80
define OVERVIEW_SITUATION_ROW_SPACING = 0
define OVERVIEW_SITUATION_ARROW_WIDTH = 24
define OVERVIEW_SITUATION_SCROLL_WIDTH = 12
define OVERVIEW_SPLIT_BAR_HEIGHT = 54

# text on the leather straps: the dialogue box's cream, lighter green/red than
# on paper so a change still reads against the dark leather
define OVERVIEW_CREAM = "#f4ead6"
define OVERVIEW_GOOD = "#a6d98e"
define OVERVIEW_BAD = "#f2907c"

#######################
# region Styles ----- #
#######################

# The map HUD in the journal's materials: stitched leather straps
# (gui/journal/ui/leather_patch) for stats and navigation, the date and the
# situations on the paper slips of the choice menus.
style overview_strap is empty:
    background Frame("gui/journal/ui/leather_patch.webp", 20, 20, tile = True)
    padding (16, 9, 20, 15)

style overview_strap_text is default:
    font "fonts/CrimsonPro-SemiBold.ttf"
    size 21
    color OVERVIEW_CREAM
    outlines [(1, "#1a0e0670", 0, 1)]

style overview_strap_value is overview_strap_text:
    size 23

style overview_hud_button is empty:
    padding (3, 0)
    hover_background Solid("#e4be7020")

style overview_toggle_button is overview_hud_button:
    xminimum 22
    yminimum 30

style overview_toggle_button_text is overview_strap_text:
    size 30
    xalign 0.5
    yalign 0.5
    hover_color "#e4be70"

style overview_split_button is empty:
    padding (12, 0)
    hover_background Solid("#e4be7020")

style overview_date_slip is empty:
    background Frame("gui/journal/ui/choice_slip.webp", 12, 12)
    padding (18, 9, 20, 17)

style overview_slip_button is empty:
    padding (2, 0)

style overview_date_text is default:
    font "fonts/SpecialElite-Regular.ttf"
    size 19
    color JR_TYPED
    hover_color JR_ACCENT

style overview_daytime_text is default:
    font "fonts/CrimsonPro-SemiBold.ttf"
    size 22

style overview_situation_row is empty:
    background Frame("gui/journal/ui/choice_slip.webp", 12, 12)
    hover_background Frame(Transform("gui/journal/ui/choice_slip.webp", matrixcolor = TintMatrix("#fff0c8")), 12, 12)
    padding (16, 8, 18, 16)

style overview_slip_text is default:
    font "fonts/CrimsonPro-SemiBold.ttf"
    size 19
    color JR_PRINT

style overview_slip_glyph is default:
    font "DejaVuSans.ttf"
    size 16
    yalign 0.5

style overview_vscrollbar is jr_vscrollbar:
    xsize OVERVIEW_SITUATION_SCROLL_WIDTH

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

    add map_manager.get_current_map().get_map_path()

##############################
# display the stats on the map
screen overview_stat_entry(stat, compact, interactive):
    $ title = Stat_Data[stat].get_title()
    $ change = get_overview_stat_change_value(stat)
    $ icon_path = get_stat_icon_path(stat, size=ICON_SMALL)
    $ stat_action = [UISound("journal_open"), Call("open_journal", 1, stat)] if interactive else NullAction()

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
                    style "overview_strap_text"
                    font "DejaVuSans.ttf"
                    color change_color
                    size 15
                    yalign 0.5
    else:
        $ change_text = get_overview_stat_change_text(stat)
        button:
            style "overview_hud_button"
            tooltip title
            action stat_action
            hbox:
                spacing 4
                yalign 0.5
                add icon_path:
                    yalign 0.5
                    zoom OVERVIEW_STAT_ICON_ZOOM
                    at overview_icon_tint(OVERVIEW_CREAM)
                text get_school_stat_value(stat):
                    style "overview_strap_value"
                    yalign 0.5
                if change_text:
                    text change_text:
                        style "overview_strap_text"
                        size 17
                        yalign 0.5

screen overview_situation_entry(situation, interactive, row_width):
    $ glyph, side, arrow_color = get_overview_situation_tendency(situation)
    $ sit_action = [UISound("journal_open"), Call("open_journal", 8, situation.key)] if interactive else NullAction()
    $ inner_width = row_width - 34
    $ bar_width = inner_width - (OVERVIEW_SITUATION_ARROW_WIDTH * 2) - 8

    button:
        style "overview_situation_row"
        tooltip situation.name
        action sit_action
        xsize row_width

        vbox:
            spacing 2

            hbox:
                xsize inner_width
                text situation.name:
                    style "overview_slip_text"
                    xmaximum inner_width - 120
                if situation.is_paused():
                    text "paused":
                        style "overview_slip_text"
                        font "fonts/CrimsonPro-Italic.ttf"
                        color JR_PENCIL
                        xalign 1.0
                else:
                    text situation.get_combined_bar_value_mood():
                        style "overview_slip_text"
                        font "fonts/CrimsonPro-Italic.ttf"
                        color journal_mood_ink(situation)
                        xalign 1.0

            hbox:
                spacing 4

                fixed:
                    xsize OVERVIEW_SITUATION_ARROW_WIDTH
                    ysize 28
                    if side < 0:
                        text glyph:
                            style "overview_slip_glyph"
                            color arrow_color
                            xalign 1.0

                use jr_situation_bar(situation, bar_width, True)

                fixed:
                    xsize OVERVIEW_SITUATION_ARROW_WIDTH
                    ysize 28
                    if side > 0:
                        text glyph:
                            style "overview_slip_glyph"
                            color arrow_color
                            xalign 0.0

screen overview_situation_list(situations, interactive, row_width):
    vbox:
        xsize row_width
        spacing OVERVIEW_SITUATION_ROW_SPACING

        for situation in situations:
            use overview_situation_entry(situation, interactive, row_width)

screen school_overview_stats (interactive = True, show_navigation = True, show_tooltip = True):
    # """
    # Displays the stats and time on the map, in the journal's materials: the
    # stats and the navigation on stitched leather straps, the date on a paper
    # slip, the running situations on slips below.

    # ### Parameters:
    # 1. interactive: bool (default True)
    #     - whether the stat entries and time buttons react to clicks
    # 2. show_navigation: bool (default True)
    #     - whether the Situations / Journal bar (and the situation list) is shown;
    #       the open journal hides it because it would overlap the book
    # 3. show_tooltip: bool (default True)
    #     - whether this screen draws its own tooltip; off when embedded in a
    #       screen that already shows tooltips (the journal), or both would appear
    # """

    zorder 80

    $ expanded = persistent.overview_stats_expanded
    $ can_skip = interactive and time.compare_today(10, 1, 2023) != -1

    $ daytimestr = time.get_daytime_name()
    $ datestr = time.get_weekday() + ", " + str(time.day) + " " + time.get_month_name() + " " + str(time.year)
    # stamp ink by kind of time slot: night, class, free time, weekend
    $ daytime_color = JR_PRINT
    if time.check_daytime("n"):
        $ daytime_color = "#2e3f86"
    elif time.check_weekday("d") and time.check_daytime("c"):
        $ daytime_color = JR_ACCENT
    elif time.check_weekday("d") and time.check_daytime("f"):
        $ daytime_color = JR_GREEN
    elif time.check_weekday("w"):
        $ daytime_color = "#9a5a16"

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
        xoffset -10
        yoffset 8
        spacing 2

        frame:
            style "overview_strap"
            xalign 1.0
            if not expanded:
                xminimum OVERVIEW_COMPACT_BAR_WIDTH

            hbox:
                spacing 10
                yalign 0.5

                textbutton ("›" if expanded else "‹"):
                    style "overview_toggle_button"
                    tooltip ("Collapse stats" if expanded else "Expand stats")
                    action ToggleField(persistent, "overview_stats_expanded")
                    yalign 0.5

                hbox:
                    spacing 10
                    yalign 0.5

                    for stat in OVERVIEW_STAT_ORDER:
                        if expanded:
                            use overview_stat_entry(stat, False, interactive)
                        elif get_overview_stat_change_value(stat) != 0:
                            use overview_stat_entry(stat, True, interactive)

        # the date, typed on a slip tucked under the strap
        frame:
            style "overview_date_slip"
            xsize OVERVIEW_COMPACT_BAR_WIDTH
            xalign 1.0

            hbox:
                xfill True

                button:
                    style "overview_slip_button"
                    yalign 0.5
                    tooltip (skip_day_text if can_skip else datestr)
                    action (Call("new_day") if can_skip else NullAction())
                    text datestr style "overview_date_text"

                button:
                    style "overview_slip_button"
                    xalign 1.0
                    yalign 0.5
                    tooltip (skip_time_text if can_skip else daytimestr)
                    action (Call("skip_time") if can_skip else NullAction())
                    text daytimestr:
                        style "overview_daytime_text"
                        color daytime_color

        if show_navigation:
            $ overview_situations = get_overview_active_situations()
            $ split_w = (OVERVIEW_COMPACT_BAR_WIDTH - 36) // 2
            $ journal_action = Call("start_journal") if interactive else NullAction()
            $ journal_tip = "Open Journal"
            $ journal_icon = get_journal_map_icon()
            if has_keyboard() and show_shortcut():
                $ journal_tip = journal_tip + " [[J]"

            frame:
                style "overview_strap"
                xsize OVERVIEW_COMPACT_BAR_WIDTH
                ysize OVERVIEW_SPLIT_BAR_HEIGHT
                xalign 1.0

                hbox:
                    spacing 0
                    yfill True

                    button:
                        style "overview_split_button"
                        xsize split_w
                        yfill True
                        tooltip ("Collapse situations" if persistent.overview_situations_expanded else "Expand situations")
                        action ToggleField(persistent, "overview_situations_expanded")

                        hbox:
                            spacing 8
                            yalign 0.5

                            text ("▾" if persistent.overview_situations_expanded else "▸"):
                                style "overview_strap_text"
                                font "DejaVuSans.ttf"
                                size 16
                                yalign 0.5

                            text "Situations":
                                style "overview_strap_text"
                                yalign 0.5

                            if not persistent.overview_situations_expanded:
                                text ("(" + str(len(overview_situations)) + ")"):
                                    style "overview_strap_text"
                                    color OVERVIEW_CREAM + "aa"
                                    yalign 0.5

                    # a short stitched seam between the two halves
                    vbox:
                        yalign 0.5
                        spacing 4
                        for i in range(3):
                            add Solid(OVERVIEW_CREAM + "80") xysize (2, 6)

                    button:
                        style "overview_split_button"
                        xsize split_w
                        yfill True
                        tooltip journal_tip
                        action journal_action

                        hbox:
                            spacing 8
                            xalign 0.5
                            yalign 0.5

                            add journal_icon:
                                yalign 0.5
                                zoom 0.16

                            text "Journal":
                                style "overview_strap_text"
                                yalign 0.5

            if persistent.overview_situations_expanded and overview_situations:
                $ sit_count = len(overview_situations)
                $ sit_content_h = sit_count * (OVERVIEW_SITUATION_ROW_HEIGHT + OVERVIEW_SITUATION_ROW_SPACING)
                $ needs_scroll = sit_content_h > OVERVIEW_SITUATION_LIST_MAX_HEIGHT
                $ sit_view_h = OVERVIEW_SITUATION_LIST_MAX_HEIGHT if needs_scroll else sit_content_h
                $ sit_row_w = OVERVIEW_COMPACT_BAR_WIDTH - (OVERVIEW_SITUATION_SCROLL_WIDTH if needs_scroll else 0)

                null height 2

                frame:
                    background None
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

    $ tooltip = GetTooltip() if show_tooltip else None

    if tooltip:
        nearrect:
            focus "tooltip"
            prefer_top True

            frame:
                style "jr_tooltip_frame"
                xalign 0.5
                text tooltip style "jr_tooltip_text"

##################################
# display all buildings on the map
screen school_overview_images ():
    # """
    # Displays all buildings on the map
    # """

    add map_manager.get_current_map().get_map_path()

    $ map_buildings = map_manager.get_current_map().get_buildings()
    for building in map_buildings:
        if building.is_open():
            $ idle_image = find_loadable_image(building.get_image("idle"))
            if idle_image:
                add idle_image:
                    xpos building.x_pos ypos building.y_pos
        else:
            $ empty_image = building.get_map_empty_image()
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
    
    $ map_buildings = map_manager.get_current_map().get_buildings()
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
            $ empty_image = building.get_map_empty_image()
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
                style "jr_tooltip_frame"
                xalign 0.5
                text tooltip style "jr_tooltip_text"

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
    
    # time_event_check updates the intro flag first
    call time_event_check from new_day_2

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

    jump map_overview

label map_entry():

    # stop sound fadeout 1.0

    jump map_overview

# shows the map overview and then waits for input
label map_overview ():
    if len(headmaster_proficiencies.keys()) < 2 and (FlagCondition(None)).is_fulfilled():
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

    $ situation_manager.check_all_thresholds()
    $ situation_manager.check_passives()
    $ situation_manager.check_resolutions()
    call drain_situation_events from _call_drain_situation_events_map_entry

    if not debug_mode:
        # keep only the last 100 entries in the return stack
        $ renpy.set_return_stack(renpy.get_return_stack()[-100:])

    show expression map_manager.get_current_map().get_map_path() as map_image
    # show screen school_overview_map
    show screen school_overview_stats 

    $ log_separator()

    $ update_available_highlights()

    $ update_available_events()

    $ renpy.block_rollback()

    $ play_location_ambience("map", map_manager.get_current_map().key)
    $ play_map_music(map_manager.get_current_map().key)
    # the journal icon just lit up: a pencil scribble, once, not on every return
    if journal_alert_manager.take_announcement():
        $ play_ui_sound("journal_entry")

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

    # before the building label, so its general-check event already ducks the right room
    $ play_location_ambience("building", name)

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