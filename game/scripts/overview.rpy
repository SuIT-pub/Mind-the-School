######################
# Map overview methods
init -1 python:
    def hide_all():
        """
        hides all screens
        """

        for s in renpy.display.screen.screens_by_name:
            renpy.hide_screen(s)

######################
# ----- Styles ----- #
######################

style stat_overview:
    outlines [(2, "222222", 1, 1)]

style stat_value take stat_overview:
    size 25



##########################
# ----- Map Screen ----- #
##########################

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
            xalign 1.0 yalign 0.32
            action Call("skip_time")

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

    # High School Building
    if is_building_available("school_building"):
        add "background/school_building.webp":
            xpos 563 ypos 620

    # High School Dormitory
    if is_building_available("school_dormitory"):
        add "background/school_dormitory.webp":
            xpos 1202 ypos 410

    # Labs
    if is_building_available("labs"):
        add "background/labs.webp":
            xpos 722 ypos 176

    # Sports Field
    if is_building_available("sports_field"):
        add "background/sports_field.webp":
            xpos 241 ypos 130

    # Beach
    if is_building_available("beach"):
        add "background/beach.webp":
            xpos 952 ypos 728

    # Gym
    if is_building_available("gym"):
        add "background/gym.webp":
            xpos 140 ypos 289

    # Swimming Pool
    if is_building_available("swimming_pool"):
        add "background/swimming_pool.webp":
            xpos 354 ypos 348

    # Cafeteria
    if is_building_available("cafeteria"):
        add "background/cafeteria.webp":
            xpos 825 ypos 473

    # Bath
    if is_building_available("bath"):
        add "background/bath.webp":
            xpos 441 ypos -19

    # Kiosk
    if is_building_available("kiosk"):
        add "background/kiosk.webp":
            xpos 269 ypos 510

    # Courtyard
    if is_building_available("courtyard"):
        add "background/courtyard.webp":
            xpos 452 ypos 490

    # Office Building
    if is_building_available("office_building"):
        add "background/office_building.webp":
            xpos 976 ypos 70

    # Staff Lodges
    if is_building_available("staff_lodges"):
        add "background/staff_lodges.webp":
            xpos -19 ypos 624

############################################################################
# display clickable buttons for the buildings leading to building distributor
screen school_overview_buttons (with_available_Events = False):
    # """
    # Displays clickable buttons for the buildings leading to building distributor
    # """

    tag interaction_overlay
    # modal True
    
    # High School Building
    if is_building_available("school_building") or is_building_available("high_school_building"):
        $ sb_text = ""
        if has_keyboard():  
            if show_shortcut():
                $ sb_text = " [[1]"
            key "K_1" action Call("building", "school_building")
            key "K_KP1" action Call("building", "school_building")
        $ image_text = "background/school_building.webp"
        if with_available_Events and overview_events_available['school_building']:
            $ image_text = "background/school_building_red.webp"
        imagebutton:
            idle image_text
            hover "background/school_building_white.webp"
            tooltip "School Building" + sb_text
            focus_mask True
            xpos 563 ypos 620
            action Call("building", "school_building")

    # High School Dormitory
    if is_building_available("school_dormitory") or is_building_available("high_school_dormitory"):
        $ sd_text = ""
        if has_keyboard():
            if show_shortcut():
                $ sd_text = " [[2]"
            key "K_2" action Call("building", "school_dormitory")
            key "K_KP2" action Call("building", "school_dormitory")
        $ image_text = "background/school_dormitory.webp"
        if with_available_Events and overview_events_available['school_dormitory']:
            $ image_text = "background/school_dormitory_red.webp"
        imagebutton:
            idle image_text
            hover "background/school_dormitory_white.webp"
            tooltip "School Dormitory" + sd_text
            focus_mask True
            xpos 1202 ypos 410
            action Call("building", "school_dormitory")

    # Labs
    if is_building_available("labs"):
        $ image_text = "background/labs.webp"
        if with_available_Events and overview_events_available['labs']:
            $ image_text = "background/labs_red.webp"
        imagebutton:
            idle image_text
            hover "background/labs_white.webp"
            tooltip "Labs"
            focus_mask True
            xpos 722 ypos 176
            action Call("building", "labs")

    # Sports Field
    if is_building_available("sports_field"):
        $ image_text = "background/sports_field.webp"
        if with_available_Events and overview_events_available['sports_field']:
            $ image_text = "background/sports_field_red.webp"
        imagebutton:
            idle image_text
            hover "background/sports_field_white.webp"
            tooltip "Sports Field"
            focus_mask True
            xpos 241 ypos 130
            action Call("building", "sports_field")

    # Beach
    if is_building_available("beach"):
        $ image_text = "background/beach.webp"
        if with_available_Events and overview_events_available['beach']:
            $ image_text = "background/beach_red.webp"
        imagebutton:
            idle image_text
            hover "background/beach_white.webp"
            tooltip "Beach"
            focus_mask True
            xpos 952 ypos 728
            action Call("building", "beach")

    # Staff Lodges
    if is_building_available("staff_lodges"):
        $ image_text = "background/staff_lodges.webp"
        if with_available_Events and overview_events_available['staff_lodges']:
            $ image_text = "background/staff_lodges_red.webp"
        imagebutton:
            idle image_text
            hover "background/staff_lodges_white.webp"
            tooltip "Staff Lodges"
            focus_mask True
            xpos -19 ypos 624
            action Call("building", "staff_lodges")

    # Gym
    if is_building_available("gym"):
        $ g_text = ""
        if has_keyboard():
            if show_shortcut():
                $ g_text = " [[6]"
            key "K_6" action Call("building", "gym")
            key "K_KP6" action Call("building", "gym")
        $ image_text = "background/gym.webp"
        if with_available_Events and overview_events_available['gym']:
            $ image_text = "background/gym_red.webp"
        imagebutton:
            idle image_text
            hover "background/gym_white.webp"
            tooltip "Gym" + g_text
            focus_mask True
            xpos 140 ypos 289
            action Call("building", "gym")

    # Swimming Pool
    if is_building_available("swimming_pool"):
        $ image_text = "background/swimming_pool.webp"
        if with_available_Events and overview_events_available['swimming_pool']:
            $ image_text = "background/swimming_pool_red.webp"
        imagebutton:
            idle image_text
            hover "background/swimming_pool_white.webp"
            tooltip "Swimming Pool"
            focus_mask True
            xpos 354 ypos 348
            action Call("building", "swimming_pool")

    # Cafeteria
    if is_building_available("cafeteria"):
        $ cf_text = ""
        if has_keyboard():
            if show_shortcut():
                $ cf_text = " [[7]"
            key "K_7" action Call("building", "cafeteria")
            key "K_KP7" action Call("building", "cafeteria")
        $ image_text = "background/cafeteria.webp"
        if with_available_Events and overview_events_available['cafeteria']:
            $ image_text = "background/cafeteria_red.webp"
        imagebutton:
            idle image_text
            hover "background/cafeteria_white.webp"
            tooltip "Cafeteria" + cf_text
            focus_mask True
            xpos 825 ypos 473
            action Call("building", "cafeteria")

    # Bath
    if is_building_available("bath"):
        $ image_text = "background/bath.webp"
        if with_available_Events and overview_events_available['bath']:
            $ image_text = "background/bath_red.webp"
        imagebutton:
            idle image_text
            hover "background/bath_white.webp"
            tooltip "Bath"
            focus_mask True
            xpos 441 ypos -19
            action Call("building", "bath")

    # Kiosk
    if is_building_available("kiosk"):
        $ k_text = ""
        if has_keyboard():
            if show_shortcut():
                $ k_text = " [[5]"
            key "K_5" action Call("building", "kiosk")
            key "K_KP5" action Call("building", "kiosk")
        $ image_text = "background/kiosk.webp"
        if with_available_Events and overview_events_available['kiosk']:
            $ image_text = "background/kiosk_red.webp"
        imagebutton:
            idle image_text
            hover "background/kiosk_white.webp"
            tooltip "Kiosk" + k_text
            focus_mask True
            xpos 269 ypos 510
            action Call("building", "kiosk")

    # Courtyard
    if is_building_available("courtyard"):
        $ c_text = ""
        if has_keyboard():
            if show_shortcut():
                $ c_text = " [[4]"
            key "K_4" action Call("building", "courtyard")
            key "K_KP4" action Call("building", "courtyard")
        $ image_text = "background/courtyard.webp"
        if with_available_Events and overview_events_available['courtyard']:
            $ image_text = "background/courtyard_red.webp"
        imagebutton:
            idle image_text
            hover "background/courtyard_white.webp"
            tooltip "Courtyard" + c_text
            focus_mask True
            xpos 452 ypos 490
            action Call("building", "courtyard")

    # Office Building
    if is_building_available("office_building"):
        $ o_text = ""
        if has_keyboard():
            if show_shortcut():
                $ o_text = " [[3]"
            key "K_3" action Call("building", "office_building")
            key "K_KP3" action Call("building", "office_building")
        $ image_text = "background/office_building.webp"
        if with_available_Events and overview_events_available['office_building']:
            $ image_text = "background/office_building_red.webp"
        imagebutton:
            idle image_text
            hover "background/office_building_white.webp"
            tooltip "Office Building" + o_text
            focus_mask True
            xpos 976 ypos 70
            action Call("building", "office_building")
    
    

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
            xalign 1.0 yalign 0.6
            action Call("start_journal")

    $ tooltip = GetTooltip()

    if tooltip:
        nearrect:
            focus "tooltip"
            prefer_top True

            frame:
                xalign 0.5
                text tooltip

screen black_error_screen_text(text_str):
    python:
        """
        Displays a black screen with red text
        Would be used for error messages

        # Parameters:
        1. text_str: str
            - the text to be displayed
        """

    add "black"
    zorder -1
    
    text text_str:
        xalign 0 yalign 0
        size 20
        color "#a00000"

screen black_screen_text(text_str):
    python:
        """
        Displays a black screen with white text

        # Parameters:
        1. text_str: str
            - the text to be displayed
        """

    add "black"
    
    key "K_SPACE" action Return()
    key "K_ESCAPE" action Return()
    key "K_KP_ENTER" action Return()
    key "K_SELECT" action Return()

    text text_str:
        xalign 0.5 yalign 0.5
        size 60

    button:
        xpos 0 ypos 0
        xsize 1920 ysize 1080
        action Return()
#########################
# ----- Map Logic ----- #
#########################


label say_with_image (image_series, step, text, person_name, person):
    # """
    # Prints a text with an image
    # Mainly used for the "random_say" method

    # ### Parameters:
    # 1. image_series: Image_Series
    #     - The image series to use
    # 2. step: int
    #     - The step of the image series to use
    # 3. text: str
    #     - The text to print
    # 4. person_name: str
    #     - The name of the person to print
    # 5. person: ADVCharacter
    #     - The character who says the text
    # """

    $ image_series.show(step)
    $ person(text, name = person_name)

    return

####################################################
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

screen school_overview():
    use school_overview_map
    use school_overview_stats
    use school_overview_buttons

#################################################
# shows the map overview and then waits for input
label map_overview ():
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

    show school_map
    # show screen school_overview_map
    show screen school_overview_stats

    $ overview_events_available = {
        'school_building': sb_events_available(),
        'school_dormitory': sd_events_available(),
        'labs': labs_events_available(),
        'sports_field': sports_field_events_available(),
        'gym': gym_events_available(),
        'swimming_pool': swimming_pool_events_available(),
        'cafeteria': cafeteria_events_available(),
        'bath': bath_events_available(),
        'kiosk': kiosk_events_available(),
        'courtyard': courtyard_events_available(),
        'office_building': office_building_events_available(),
        'beach': beach_events_available(),
        'staff_lodges': staff_lodges_events_available()
    }

    $ renpy.block_rollback()

    call screen school_overview_buttons (True)
    # call screen school_overview with dissolveM

    subtitles_Empty ""

#############################################################################
# building distributor. directs the building calls to the corresponding label
label building(name=""):
    $ reset_stats(get_school())
    $ reset_stats(get_character('parent', charList))
    $ reset_stats(get_character('teacher', charList['staff']))
    $ _skipping = True

    hide screen school_overview_map
    hide screen school_overview_stats
    hide screen school_overview_buttons

    $ hide_all()

    # $ image_code = name + str(time.get_daytime_name()) + str(time.get_day()) + str(time.get_month_name()) + str(time.year)

    call expression name from building_1

    call map_overview from building_2

label skip_time ():
    $ reset_stats(get_school())
    $ reset_stats(get_character('parent', charList))
    $ reset_stats(get_character('teacher', charList['staff']))

    call new_daytime from skip_time_1

label empty_label ():
    return