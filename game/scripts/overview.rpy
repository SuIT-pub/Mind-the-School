######################
# Map overview methods
init -1 python:
    import math

    # generates the stat-value text with change
    def display_stat(stat, school = "school_mean"):
        if stat != "money":
            return schools[school].display_stat(stat)
        else:
            return money.display_stat()

    # changes the stat value
    def change_stat(stat, change, school):
        if stat == "money":
            money.change_value(change)
        else:
            schools[school].change_stat(stat, change)

    def reset_stats(school = ""):
        money.reset_change()

        if school != "":
            schools[school].reset_changed_stats()

        for keys in schools.keys():
            schools[keys].reset_changed_stats()

######################
# ----- Styles ----- #
######################

style stat_name:
    size 20
style stat_value:
    size 25

##########################
# ----- Map Screen ----- #
##########################

###################################
# display the school map with stats
screen school_overview_map ():
    add "background/bg school overview idle.png"

##############################
# display the stats on the map
screen school_overview_stats ():
    grid 4 4:
        xalign 1.0 yalign 0.0
        spacing 5
        text "Happiness"      style "stat_name"
        text "Charm"          style "stat_name"
        text "Education     " style "stat_name"
        text "Money"          style "stat_name"

        text display_stat("happiness") style "stat_value"
        text display_stat("charm")     style "stat_value"
        text display_stat("education") style "stat_value"
        text display_stat("money")     style "stat_value"

        null
        text "-" style "stat_name"
        text "-" style "stat_name"
        text "Reputation" style "stat_name"
        
        null
        text display_stat("corruption") style "stat_value"
        text display_stat("inhibition") style "stat_value"
        text display_stat("reputation") style "stat_value"

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


##################################
# display all buildings on the map
screen school_overview_images ():
    add "background/bg school overview idle.png"

    # High School Building
    if is_building_available("high_school_building"):
        add "background/bg school high school building idle.png":
            xpos 1171 ypos 262

    # High School Dormitory
    if is_building_available("high_school_dormitory"):
        add "background/bg school high school dormitory idle.png":
            xpos 1257 ypos 613

    if loli_content >= 1:
        # Middle School Building
        if is_building_available("middle_school_building"):
            add "background/bg school middle school building idle.png":
                xpos 725 ypos 103

        # Middle School Dormitory
        if is_building_available("middle_school_dormitory"):
            add "background/bg school middle school dormitory idle.png":
                xpos 666 ypos 476

    if loli_content == 2:
        # Elementary School Building
        if is_building_available("elementary_school_building"):
            add "background/bg school elementary school building idle.png":
                xpos 826 ypos 178
        
        # Elementary School Dormitory
        if is_building_available("elementary_school_dormitory"):
            add "background/bg school elementary school dormitory idle.png":
                xpos 446 ypos 196

    # Labs
    if is_building_available("labs"):
        add "background/bg school labs idle.png":
            xpos 664 ypos 356

    # Sports Field
    if is_building_available("sports_field"):
        add "background/bg school sports field idle.png":
            xpos 203 ypos -11

    # Tennis Court
    if is_building_available("tennis_court"):
        add "background/bg school tennis court idle.png":
            xpos 558 ypos 90

    # Gym
    if is_building_available("gym"):
        add "background/bg school gym idle.png":
            xpos 462 ypos 5

    # Swimming Pool
    if is_building_available("swimming_pool"):
        add "background/bg school pool idle.png":
            xpos 297 ypos 61

    # Cafeteria
    if is_building_available("cafeteria"):
        add "background/bg school cafeteria idle.png":
            xpos 229 ypos 460

    # Bath
    if is_building_available("bath"):
        add "background/bg school bath idle.png":
            xpos 557 ypos 319

    # Kiosk
    if is_building_available("kiosk"):
        add "background/bg school kiosk idle.png":
            xpos 485 ypos 661

    # Courtyard
    if is_building_available("courtyard"):
        add "background/bg school courtyard idle.png":
            xpos 604 ypos 228

    # Office Building
    if is_building_available("office_building"):
        add "background/bg school office building idle.png":
            xpos 42 ypos 127

############################################################################
# display clickable buttons for the buildings leading to building distibutor
screen school_overview_buttons ():
    tag interaction_overlay
    modal True
    
    # High School Building
    if is_building_available("high_school_building"):
        imagebutton:
            auto "background/bg school high school building %s.png"
            hover "background/bg school high school building hover.png"
            tooltip "High School Building"
            focus_mask True
            xpos 1171 ypos 262
            action Call("building", "high_school_building")

    # High School Dormitory
    if is_building_available("high_school_dormitory"):
        imagebutton:
            auto "background/bg school high school dormitory %s.png"
            tooltip "High School Dormitory"
            focus_mask True
            xpos 1257 ypos 613
            action Call("building", "high_school_dormitory")

    if loli_content >= 1:
        # Middle School Building
        if is_building_available("middle_school_building"):
            imagebutton:
                auto "background/bg school middle school building %s.png"
                tooltip "Middle School Building"
                focus_mask True
                xpos 725 ypos 103
                action Call("building", "middle_school_building")
        
        # Middle School Dormitory
        if is_building_available("middle_school_dormitory"):
            imagebutton:
                auto "background/bg school middle school dormitory %s.png"
                tooltip "Middle School Dormitory"
                focus_mask True
                xpos 666 ypos 476
                action Call("building", "middle_school_dormitory")

    if loli_content == 2:
        # Elementary School Building
        if is_building_available("elementary_school_building"):
            imagebutton:
                auto "background/bg school elementary school building %s.png"
                tooltip "Elementary School Building"
                focus_mask True
                xpos 826 ypos 178
                action Call("building", "elementary_school_building")

        # Elementary School Dormitory
        if is_building_available("elementary_school_dormitory"):
            imagebutton:
                auto "background/bg school elementary school dormitory %s.png"
                tooltip "Elementary School Dormitory"
                focus_mask True
                xpos 446 ypos 196
                action Call("building", "elementary_school_dormitory")

    # Labs
    if is_building_available("labs"):
        imagebutton:
            auto "background/bg school labs %s.png"
            tooltip "Labs"
            focus_mask True
            xpos 644 ypos 356
            action Call("building", "labs")

    # Sports Field
    if is_building_available("sports_field"):
        imagebutton:
            auto "background/bg school sports field %s.png"
            tooltip "Sports Field"
            focus_mask True
            xpos 203 ypos -11
            action Call("building", "sports_field")

    # Tennis Court
    if is_building_available("tennis_court"):
        imagebutton:
            auto "background/bg school tennis court %s.png"
            tooltip "Tennis Court"
            focus_mask True
            xpos 558 ypos 90
            action Call("building", "tennis_court")

    # Gym
    if is_building_available("gym"):
        imagebutton:
            auto "background/bg school gym %s.png"
            tooltip "Gym"
            focus_mask True
            xpos 462 ypos 5
            action Call("building", "gym")

    # Swimming Pool
    if is_building_available("swimming_pool"):
        imagebutton:
            auto "background/bg school pool %s.png"
            tooltip "Swimming Pool"
            focus_mask True
            xpos 297 ypos 61
            action Call("building", "swimming_pool")

    # Cafeteria
    if is_building_available("cafeteria"):
        imagebutton:
            auto "background/bg school cafeteria %s.png"
            tooltip "Cafeteria"
            focus_mask True
            xpos 229 ypos 460
            action Call("building", "cafeteria")

    # Bath
    if is_building_available("bath"):
        imagebutton:
            auto "background/bg school bath %s.png"
            tooltip "Bath"
            focus_mask True
            xpos 557 ypos 319
            action Call("building", "bath")

    # Kiosk
    if is_building_available("kiosk"):
        imagebutton:
            auto "background/bg school kiosk %s.png"
            tooltip "Kiosk"
            focus_mask True
            xpos 485 ypos 661
            action Call("building", "kiosk")

    # Courtyard
    if is_building_available("courtyard"):
        imagebutton:
            auto "background/bg school courtyard %s.png"
            tooltip "Courtyard"
            focus_mask True
            xpos 604 ypos 228
            action Call("building", "courtyard")

    # Office Building
    if is_building_available("office_building"):
        imagebutton:
            auto "background/bg school office building %s.png"
            tooltip "Office Building"
            focus_mask True
            xpos 42 ypos 127
            action Call("building", "office_building")
    
    # Skip Daytime
    imagebutton:
        auto "icons/time skip %s.png"
        tooltip "Skip Time"
        focus_mask None
        xalign 0.0 yalign 0.0
        action Call("new_daytime")

    # Open Journal
    imagebutton:
        auto "icons/journal_icon_%s.png"
        tooltip "Open Journal"
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

screen black_screen_text(text_str):
    add "black"

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

####################################################
# goes to map overview while moving the time forward

label set_day(day, month, year):
    $ time.set_time(day, month, year)

    call screen black_screen_text (f"{time.get_weekday()}, {time.day} {time.get_month_name()} {time.year}")

    call time_event_check from _call_time_event_check_2

    jump map_overview

label new_day:
    $ time.progress_day()

    call screen black_screen_text (f"{time.get_weekday()}, {time.day} {time.get_month_name()} {time.year}")

    call time_event_check from _call_time_event_check

    jump map_overview

label new_daytime:
    if time.progress_time():
        call screen black_screen_text (f"{time.get_weekday()}, {time.day} {time.get_month_name()} {time.year}")
        
    call time_event_check from _call_time_event_check_1

    jump map_overview

#################################################
# shows the map overview and then waits for input
label map_overview:
    # $ _skipping = False
    call load_stats from _call_load_stats_1
    call load_schools from _call_load_schools_1
    call load_rules from _call_load_rules_1
    call load_buildings from _call_load_buildings_1
    call load_clubs from _call_load_clubs_1
    
    show screen school_overview_map
    show screen school_overview_stats
    show screen school_overview_buttons

    subtitles_Empty ""

    jump map_overview

#############################################################################
# building distributor. directs the building calls to the corresponding label
label building(name=""):
    $ reset_stats()
    $ _skipping = True

    hide screen school_overview_map
    hide screen school_overview_stats
    hide screen school_overview_buttons

    call expression name from _call_expression_1

    call map_overview from _call_map_overview