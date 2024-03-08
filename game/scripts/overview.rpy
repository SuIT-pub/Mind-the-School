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

style stat_value:
    size 20

##########################
# ----- Map Screen ----- #
##########################

###################################
# display the school map with stats
screen school_overview_map ():
    # """
    # Displays the school map
    # """

    add "background/bg school overview idle.webp"

##############################
# display the stats on the map
screen school_overview_stats ():
    # """
    # Displays the stats on the map
    # """

    grid 4 2:
        xalign 1.0 yalign 0.0
        spacing 5
        hbox:
            textbutton get_stat_icon('happiness', True):
                tooltip "Happiness"
                action NullAction()
            null width 1
            textbutton get_school_stat_value(HAPPINESS) + "\n " + get_school_stat_change(HAPPINESS):
                tooltip "Happiness"
                text_style "stat_value"
                action NullAction()
        hbox:
            textbutton get_stat_icon('charm', True):
                tooltip "Charm"
                action NullAction()
            null width 1
            textbutton get_school_stat_value(CHARM) + "\n" + get_school_stat_change(CHARM):
                tooltip "Charm"
                text_style "stat_value"
                action NullAction()
        hbox:
            textbutton get_stat_icon('education', True):
                tooltip "Education"
                action NullAction()
            null width 1
            textbutton get_school_stat_value(EDUCATION) + "\n" + get_school_stat_change(EDUCATION):
                tooltip "Education"
                text_style "stat_value"
                action NullAction()
        hbox:
            textbutton get_stat_icon('money', True):
                tooltip "Money"
                action NullAction()
            null width 1
            textbutton get_school_stat_value(MONEY) + "\n" + get_school_stat_change(MONEY):
                tooltip "Money"
                text_style "stat_value"
                action NullAction()

        null
        hbox:
            textbutton get_stat_icon('corruption', True):
                tooltip "Corruption"
                action NullAction()
            null width 1
            textbutton get_school_stat_value(CORRUPTION) + "\n" + get_school_stat_change(CORRUPTION):
                tooltip "Corruption"
                text_style "stat_value"
                action NullAction()
        hbox:
            textbutton get_stat_icon('inhibition', True):
                tooltip "Inhibition"
                action NullAction()
            null width 1
            textbutton get_school_stat_value(INHIBITION) + "\n" + get_school_stat_change(INHIBITION):
                tooltip "Inhibition"
                text_style "stat_value"
                action NullAction()
        hbox:
            textbutton get_stat_icon('reputation', True):
                tooltip "Reputation"
                action NullAction()
            null width 1
            textbutton get_school_stat_value(REPUTATION) + "\n" + get_school_stat_change(REPUTATION):
                tooltip "Reputation"
                text_style "stat_value"
                action NullAction()

    vbox:
        xalign 1.0 ypos 150

        $ daytimestr = time.get_daytime_name()
        $ daystr = time.get_weekday()
        $ monthstr = time.get_month_name()
        text "[time.day] [monthstr] [time.year]":
            xalign 1.0
            size 30
        text "[daystr]":
            xalign 1.0
            size 35
        text "[daytimestr]":
            xalign 1.0
            size 30

        $ daysegment = ""
        if time.check_daytime("n"):
            $ daysegment = "{color=#1b26c0}Night{/color}"
        elif time.check_weekday("d") and time.check_daytime("c"):
            $ daysegment = "{color=#ab0000}Class{/color}"
        elif time.check_weekday("d") and time.check_daytime("f"):
            $ daysegment = "{color=#0eab00}Free-Time{/color}"
        elif time.check_weekday("w"):
            $ daysegment = "{color=#ba6413}Weekend{/color}"

        text "[daysegment]":
            xalign 1.0
            size 30

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

    add "background/bg school overview idle.webp"

    # High School Building
    if is_building_available("school_building"):
        add "background/bg school school building idle.webp":
            xpos 1171 ypos 262

    # High School Dormitory
    if is_building_available("school_dormitory"):
        add "background/bg school school dormitory idle.webp":
            xpos 1257 ypos 613

    # Labs
    if is_building_available("labs"):
        add "background/bg school labs idle.webp":
            xpos 664 ypos 356

    # Sports Field
    if is_building_available("sports_field"):
        add "background/bg school sports field idle.webp":
            xpos 203 ypos -11

    # Tennis Court
    if is_building_available("tennis_court"):
        add "background/bg school tennis court idle.webp":
            xpos 558 ypos 90

    # Gym
    if is_building_available("gym"):
        add "background/bg school gym idle.webp":
            xpos 462 ypos 5

    # Swimming Pool
    if is_building_available("swimming_pool"):
        add "background/bg school pool idle.webp":
            xpos 297 ypos 61

    # Cafeteria
    if is_building_available("cafeteria"):
        add "background/bg school cafeteria idle.webp":
            xpos 229 ypos 460

    # Bath
    if is_building_available("bath"):
        add "background/bg school bath idle.webp":
            xpos 540 ypos 319

    # Kiosk
    if is_building_available("kiosk"):
        add "background/bg school kiosk idle.webp":
            xpos 485 ypos 661

    # Courtyard
    if is_building_available("courtyard"):
        add "background/bg school courtyard idle.webp":
            xpos 604 ypos 228

    # Office Building
    if is_building_available("office_building"):
        add "background/bg school office building idle.webp":
            xpos 42 ypos 127

############################################################################
# display clickable buttons for the buildings leading to building distributor
screen school_overview_buttons ():
    # """
    # Displays clickable buttons for the buildings leading to building distributor
    # """

    # tag interaction_overlay
    # modal True
    
    # High School Building
    if is_building_available("school_building") or is_building_available("high_school_building"):
        $ sb_text = ""
        if has_keyboard():  
            if show_shortcut():
                $ sb_text = " [[1]"
            key "K_1" action Call("building", "school_building")
            key "K_KP1" action Call("building", "school_building")
        imagebutton:
            auto "background/bg school school building %s.webp"
            hover "background/bg school school building hover.webp"
            tooltip "School Building" + sb_text
            focus_mask True
            xpos 1171 ypos 262
            action Call("building", "school_building")

    # High School Dormitory
    if is_building_available("school_dormitory") or is_building_available("high_school_dormitory"):
        $ sd_text = ""
        if has_keyboard():
            if show_shortcut():
                $ sd_text = " [[2]"
            key "K_2" action Call("building", "school_dormitory")
            key "K_KP2" action Call("building", "school_dormitory")
        imagebutton:
            auto "background/bg school school dormitory %s.webp"
            tooltip "School Dormitory" + sd_text
            focus_mask True
            xpos 1257 ypos 613
            action Call("building", "school_dormitory")

    # if loli_content >= 1:
    #     # Middle School Building
    #     if is_building_available("middle_school_building"):
    #         imagebutton:
    #             auto "background/bg school middle school building %s.webp"
    #             tooltip "Middle School Building"
    #             focus_mask True
    #             xpos 725 ypos 103
    #             action Call("building", "middle_school_building")
        
    #     # Middle School Dormitory
    #     if is_building_available("middle_school_dormitory"):
    #         imagebutton:
    #             auto "background/bg school middle school dormitory %s.webp"
    #             tooltip "Middle School Dormitory"
    #             focus_mask True
    #             xpos 666 ypos 476
    #             action Call("building", "middle_school_dormitory")

    # if loli_content == 2:
    #     # Elementary School Building
    #     if is_building_available("elementary_school_building"):
    #         imagebutton:
    #             auto "background/bg school elementary school building %s.webp"
    #             tooltip "Elementary School Building"
    #             focus_mask True
    #             xpos 826 ypos 178
    #             action Call("building", "elementary_school_building")

    #     # Elementary School Dormitory
    #     if is_building_available("elementary_school_dormitory"):
    #         imagebutton:
    #             auto "background/bg school elementary school dormitory %s.webp"
    #             tooltip "Elementary School Dormitory"
    #             focus_mask True
    #             xpos 446 ypos 196
    #             action Call("building", "elementary_school_dormitory")

    # Labs
    if is_building_available("labs"):
        imagebutton:
            auto "background/bg school labs %s.webp"
            tooltip "Labs"
            focus_mask True
            xpos 644 ypos 356
            action Call("building", "labs")

    # Sports Field
    if is_building_available("sports_field"):
        imagebutton:
            auto "background/bg school sports field %s.webp"
            tooltip "Sports Field"
            focus_mask True
            xpos 203 ypos -11
            action Call("building", "sports_field")

    # Tennis Court
    if is_building_available("tennis_court"):
        imagebutton:
            auto "background/bg school tennis court %s.webp"
            tooltip "Tennis Court"
            focus_mask True
            xpos 558 ypos 90
            action Call("building", "tennis_court")

    # Gym
    if is_building_available("gym"):
        $ g_text = ""
        if has_keyboard():
            if show_shortcut():
                $ g_text = " [[6]"
            key "K_6" action Call("building", "gym")
            key "K_KP6" action Call("building", "gym")
        imagebutton:
            auto "background/bg school gym %s.webp"
            tooltip "Gym" + g_text
            focus_mask True
            xpos 462 ypos 5
            action Call("building", "gym")

    # Swimming Pool
    if is_building_available("swimming_pool"):
        imagebutton:
            auto "background/bg school pool %s.webp"
            tooltip "Swimming Pool"
            focus_mask True
            xpos 297 ypos 61
            action Call("building", "swimming_pool")

    # Cafeteria
    if is_building_available("cafeteria"):
        $ cf_text = ""
        if has_keyboard():
            if show_shortcut():
                $ cf_text = " [[7]"
            key "K_7" action Call("building", "cafeteria")
            key "K_KP7" action Call("building", "cafeteria")
        imagebutton:
            auto "background/bg school cafeteria %s.webp"
            tooltip "Cafeteria" + cf_text
            focus_mask True
            xpos 229 ypos 460
            action Call("building", "cafeteria")

    # Bath
    if is_building_available("bath"):
        imagebutton:
            auto "background/bg school bath %s.webp"
            tooltip "Bath"
            focus_mask True
            xpos 538 ypos 300
            action Call("building", "bath")

    # Kiosk
    if is_building_available("kiosk"):
        $ k_text = ""
        if has_keyboard():
            if show_shortcut():
                $ k_text = " [[5]"
            key "K_5" action Call("building", "kiosk")
            key "K_KP5" action Call("building", "kiosk")
        imagebutton:
            auto "background/bg school kiosk %s.webp"
            tooltip "Kiosk" + k_text
            focus_mask True
            xpos 485 ypos 661
            action Call("building", "kiosk")

    # Courtyard
    if is_building_available("courtyard"):
        $ c_text = ""
        if has_keyboard():
            if show_shortcut():
                $ c_text = " [[4]"
            key "K_4" action Call("building", "courtyard")
            key "K_KP4" action Call("building", "courtyard")
        imagebutton:
            auto "background/bg school courtyard %s.webp"
            tooltip "Courtyard" + c_text
            focus_mask True
            xpos 604 ypos 228
            action Call("building", "courtyard")

    # Office Building
    if is_building_available("office_building"):
        $ o_text = ""
        if has_keyboard():
            if show_shortcut():
                $ o_text = " [[3]"
            key "K_3" action Call("building", "office_building")
            key "K_KP3" action Call("building", "office_building")
        imagebutton:
            auto "background/bg school office building %s.webp"
            tooltip "Office Building" + o_text
            focus_mask True
            xpos 42 ypos 127
            action Call("building", "office_building")
    
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
            xalign 0.0 yalign 0.0
            action Call("skip_time")

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
            xalign 0.07 yalign 0.0
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
    # call load_stats from map_overview_1
    # call load_schools from map_overview_2
    # call load_rules from map_overview_3
    # call load_buildings from map_overview_4
    # call load_clubs from map_overview_5
    
    $ hide_all()

    $ reroll_selectors()

    # $ check_old_versions()

    $ is_in_replay = False

    $ renpy.choice_for_skipping()

    scene bg school overview idle
    # show screen school_overview_map
    show screen school_overview_stats

    $ renpy.block_rollback()

    call screen school_overview_buttons
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

    call expression name from building_1

    call map_overview from building_2

label skip_time ():
    $ reset_stats(get_school())
    $ reset_stats(get_character('parent', charList))
    $ reset_stats(get_character('teacher', charList['staff']))

    call new_daytime from skip_time_1