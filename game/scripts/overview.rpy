init -1 python:
    def hide_all():
        """
        hides all screens
        """

        for s in renpy.display.screen.screens_by_name:
            renpy.hide_screen(s)

#######################
# region Styles ----- #
#######################

style stat_overview:
    outlines [(2, "222222", 1, 1)]

style stat_value take stat_overview:
    size 25

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
screen school_overview_stats ():
    # """
    # Displays the stats on the map
    # """

    grid 4 2:
        xalign 1.0 yalign 0.0
        spacing 2
        hbox:
            textbutton get_stat_icon('happiness'):
                tooltip "Happiness"
                text_style "stat_overview"
                action Call("open_journal", 1, HAPPINESS)
            null width 1
            textbutton get_school_stat_value(HAPPINESS) + "\n" + get_school_stat_change(HAPPINESS):
                tooltip "Happiness"
                text_style "stat_value"
                action Call("open_journal", 1, HAPPINESS)
        hbox:
            textbutton get_stat_icon('charm'):
                tooltip "Charm"
                text_style "stat_overview"
                action Call("open_journal", 1, CHARM)
            null width 1
            textbutton get_school_stat_value(CHARM) + "\n" + get_school_stat_change(CHARM):
                tooltip "Charm"
                text_style "stat_value"
                action Call("open_journal", 1, CHARM)
        hbox:
            textbutton get_stat_icon('education'):
                tooltip "Education"
                text_style "stat_overview"
                action Call("open_journal", 1, EDUCATION)
            null width 1
            textbutton get_school_stat_value(EDUCATION) + "\n" + get_school_stat_change(EDUCATION):
                tooltip "Education"
                text_style "stat_value"
                action Call("open_journal", 1, EDUCATION)
        hbox:
            textbutton get_stat_icon('money'):
                tooltip "Money"
                text_style "stat_overview"
                action Call("open_journal", 1, MONEY)
            null width 1
            textbutton get_school_stat_value(MONEY) + "\n" + get_school_stat_change(MONEY):
                tooltip "Money"
                text_style "stat_value"
                action Call("open_journal", 1, MONEY)

        null
        hbox:
            textbutton get_stat_icon('corruption'):
                tooltip "Corruption"
                text_style "stat_overview"
                action Call("open_journal", 1, CORRUPTION)
            null width 1
            textbutton get_school_stat_value(CORRUPTION) + "\n" + get_school_stat_change(CORRUPTION):
                tooltip "Corruption"
                text_style "stat_value"
                action Call("open_journal", 1, CORRUPTION)
        hbox:
            textbutton get_stat_icon('inhibition'):
                tooltip "Inhibition"
                text_style "stat_overview"
                action Call("open_journal", 1, INHIBITION)
            null width 1
            textbutton get_school_stat_value(INHIBITION) + "\n" + get_school_stat_change(INHIBITION):
                tooltip "Inhibition"
                text_style "stat_value"
                action Call("open_journal", 1, INHIBITION)
        hbox:
            textbutton get_stat_icon('reputation'):
                tooltip "Reputation"
                text_style "stat_overview"
                action Call("open_journal", 1, REPUTATION)
            null width 1
            textbutton get_school_stat_value(REPUTATION) + "\n" + get_school_stat_change(REPUTATION):
                tooltip "Reputation"
                text_style "stat_value"
                action Call("open_journal", 1, REPUTATION)

    if time.compare_today(10, 1, 2023) != -1:
        $ s_text = ""
        if has_keyboard():
            if show_shortcut():
                $ s_text = " [[Z]"
            key "K_z" action Call("skip_time")
        # Skip Daytime
        imagebutton:
            auto "icons/time skip %s.webp"
            tooltip "Skip Time" + s_text
            focus_mask None
            xalign 0.985 yalign 0.35
            action Call("skip_time")

        $ s_text = ""
        if has_keyboard():
            if show_shortcut():
                $ s_text = " [[U]"
            key "K_u" action Call("new_day")
        # Skip Daytime
        imagebutton:
            auto "icons/day skip %s.webp"
            tooltip "Skip to next day" + s_text
            focus_mask None
            xalign 0.995 yalign 0.49
            action Call("new_day")

    vbox:
        xalign 1.0 ypos 150

        $ daytimestr = time.get_daytime_name()
        $ daystr = time.get_weekday()
        $ monthstr = time.get_month_name()
        $ daysegment = ""
        if time.check_daytime("n"):
            $ daysegment = "{color=#1b26c0}Night{/color}"
        elif time.check_weekday("d") and time.check_daytime("c"):
            $ daysegment = "{color=#ab0000}Class{/color}"
        elif time.check_weekday("d") and time.check_daytime("f"):
            $ daysegment = "{color=#0eab00}Free-Time{/color}"
        elif time.check_weekday("w"):
            $ daysegment = "{color=#ba6413}Weekend{/color}"

        text "[time.day] [monthstr] [time.year]":
            xalign 1.0
            size 30
            style "stat_overview"
        text "[daystr]":
            xalign 1.0
            size 35
            style "stat_overview"
        text "[daytimestr]":
            xalign 1.0
            size 30
            style "stat_overview"
        text "[daysegment]":
            xalign 1.0
            size 30
            style "stat_overview"


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
            add building.get_image("idle"):
                xpos building.x_pos ypos building.y_pos
        else:
            $ empty_image = building.get_image("empty")
            if check_image(empty_image):
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
            $ image_text = building.get_image("idle")
            if get_available_event(building.key):
                $ image_text = building.get_image("available")
            if with_available_Events and get_available_highlight(building.key):
                $ image_text = building.get_image("red")
            imagebutton:
                idle image_text
                hover building.get_image("white")
                tooltip building.get_name(with_shortcut = True)
                focus_mask True
                xpos building.x_pos ypos building.y_pos
                action Call("building", building.key)
        else:
            # Mods may supply an "empty" sprite for buildings not on the base map.
            # Native buildings are already baked into the map art and have no empty image —
            # skip the button entirely so there is nothing to select.
            $ empty_image = building.get_image("empty")
            if check_image(empty_image):
                imagebutton:
                    idle empty_image
                    insensitive empty_image
                    focus_mask True
                    xpos building.x_pos ypos building.y_pos
                    action NullAction()
                    sensitive False

    $ j_text = ""
    if has_keyboard():
        if show_shortcut():
            $ j_text = " [[J]"
    key "K_j" action Call("start_journal")
    # Open Journal
    imagebutton:
        auto "icons/journal_icon_%s.webp"
        tooltip "Open Journal" + j_text
        focus_mask None
        xalign 1.0 yalign 0.65
        action Call("start_journal")

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