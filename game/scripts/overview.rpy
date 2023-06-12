######################
# Map overview methods
init python:
    import math

    # generates the stat-value text with change
    def display_stat(stat, school = "school_mean"):

        if stat != "money":
            return schools[school].display_stat(stat)

        text = str(money.get_value())
        changed_money = money.get_changed_value()

        if changed_money < 0:
            text += "{color=#ff0000}{size=15}([changed_money]){/size}{/color}"
        elif changed_money > 0:
            text += "{color=#00ff00}{size=15}(+[changed_money]){/size}{/color}"
        return text

    # changes the stat value
    def change_stat(stat, change, school):
        if stat == "money":
            change_val = math.ceil(change)
            money.set_value(math.ceil(money.get_value() + change_val))
            money.set_changed_value(change_val)
            return

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
screen school_overview_map:
    add "background/bg school overview idle.png"

##############################
# display the stats on the map
screen school_overview_stats:
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
        null
        null
        # text "Corruption" style "stat_name"
        # text "Inhibition" style "stat_name"
        text "Reputation" style "stat_name"
        
        null
        null
        null
        # text display_stat("corruption") style "stat_value"
        # text display_stat("inhibition") style "stat_value"
        text display_stat("reputation") style "stat_value"

    vbox:
        xalign 1.0 ypos 150

        $ daytimestr = daytime_name[game_daytime - 1]
        $ daystr = get_weekday(game_day)
        $ monthstr = month_name[game_month - 1]
        text "[game_day] [monthstr] [game_year]":
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
screen school_overview_images:
    add "background/bg school overview idle.png"

    add "background/bg school high school building idle.png":
        xpos 1171 ypos 262
    add "background/bg school high school dormitory idle.png":
        xpos 1257 ypos 613
    if loli_content >= 1:
        add "background/bg school middle school building idle.png":
            xpos 725 ypos 103
        add "background/bg school middle school dormitory idle.png":
            xpos 666 ypos 476
    if loli_content == 2:
        add "background/bg school elementary school building idle.png":
            xpos 826 ypos 178
        add "background/bg school elementary school dormitory idle.png":
            xpos 446 ypos 196
    if get_building("labs").isUnlocked():
        add "background/bg school labs idle.png":
            xpos 664 ypos 356
    if get_building("sports_field").isUnlocked():
        add "background/bg school sports field idle.png":
            xpos 203 ypos -11
    if get_building("tennis_court").isUnlocked():
        add "background/bg school tennis court idle.png":
            xpos 558 ypos 90
    add "background/bg school gym idle.png":
        xpos 462 ypos 5
    if get_building("swimming_pool").isUnlocked():
        add "background/bg school pool idle.png":
            xpos 297 ypos 61
    if get_building("cafeteria").isUnlocked():
        add "background/bg school cafeteria idle.png":
            xpos 229 ypos 460
    add "background/bg school kiosk idle.png":
        xpos 485 ypos 661
    add "background/bg school courtyard idle.png":
        xpos 604 ypos 228
    add "background/bg school office building idle.png":
        xpos 42 ypos 127

############################################################################
# display clickable buttons for the buildings leading to building distibutor
screen school_overview_buttons:
    
    imagebutton:
        auto "background/bg school high school building %s.png"
        hover "background/bg school high school building hover.png"
        tooltip "High School Building"
        focus_mask True
        xpos 1171 ypos 262
        action Call("building", "high_school_building")
    imagebutton:
        auto "background/bg school high school dormitory %s.png"
        tooltip "High School Dormitory"
        focus_mask True
        xpos 1257 ypos 613
        action Call("building", "high_school_dormitory")
    if loli_content >= 1:
        imagebutton:
            auto "background/bg school middle school building %s.png"
            tooltip "Middle School Building"
            focus_mask True
            xpos 725 ypos 103
            action Call("building", "middle_school_building")
        imagebutton:
            auto "background/bg school middle school dormitory %s.png"
            tooltip "Middle School Dormitory"
            focus_mask True
            xpos 666 ypos 476
            action Call("building", "middle_school_dormitory")
    if loli_content == 2:
        imagebutton:
            auto "background/bg school elementary school building %s.png"
            tooltip "Elementary School Building"
            focus_mask True
            xpos 826 ypos 178
            action Call("building", "elementary_school_building")
        imagebutton:
            auto "background/bg school elementary school dormitory %s.png"
            tooltip "Elementary School Dormitory"
            focus_mask True
            xpos 446 ypos 196
            action Call("building", "elementary_school_dormitory")
    if get_building("labs").isUnlocked():
        imagebutton:
            auto "background/bg school labs %s.png"
            tooltip "Labs"
            focus_mask True
            xpos 644 ypos 356
            action Call("building", "labs")
    if get_building("sports_field").isUnlocked():
        imagebutton:
            auto "background/bg school sports field %s.png"
            tooltip "Sports Field"
            focus_mask True
            xpos 203 ypos -11
            action Call("building", "sports_field")
    if get_building("tennis_court").isUnlocked():
        imagebutton:
            auto "background/bg school tennis court %s.png"
            tooltip "Tennis Court"
            focus_mask True
            xpos 558 ypos 90
            action Call("building", "tennis_court")
    imagebutton:
        auto "background/bg school gym %s.png"
        tooltip "Gym"
        focus_mask True
        xpos 462 ypos 5
        action Call("building", "gym")
    if get_building("swimming_pool").isUnlocked():
        imagebutton:
            auto "background/bg school pool %s.png"
            tooltip "Swimming Pool"
            focus_mask True
            xpos 297 ypos 61
            action Call("building", "swimming_pool")
    if get_building("cafeteria").isUnlocked():
        imagebutton:
            auto "background/bg school cafeteria %s.png"
            tooltip "Cafeteria"
            focus_mask True
            xpos 229 ypos 460
            action Call("building", "cafeteria")
    imagebutton:
        auto "background/bg school kiosk %s.png"
        tooltip "Kiosk"
        focus_mask True
        xpos 485 ypos 661
        action Call("building", "kiosk")
    imagebutton:
        auto "background/bg school courtyard %s.png"
        tooltip "Courtyard"
        focus_mask True
        xpos 604 ypos 228
        action Call("building", "courtyard")
    imagebutton:
        auto "background/bg school office building %s.png"
        tooltip "Office Building"
        focus_mask True
        xpos 42 ypos 127
        action Call("building", "office_building")
    
    imagebutton:
        auto "icons/time skip %s.png"
        tooltip "Skip Time"
        focus_mask None
        xalign 0.0 yalign 0.0
        action Call("new_daytime")
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

#########################
# ----- Map Logic ----- #
#########################

####################################################
# goes to map overview while moving the time forward
label new_daytime:
    $ game_daytime += 1

    if game_daytime == 8:
        jump new_day

    # show screen school_overview_map

    call time_event_check

    jump map_overview

label new_day:
    $ game_daytime = 1
    $ game_day += 1
    if game_day >= 29:
        $ game_day = 1
        $ game_month += 1
        if game_month >= 13:
            $ game_month = 1
            $ game_year += 1
            
    call time_event_check

    jump map_overview

#################################################
# shows the map overview and then waits for input
label map_overview:
    # $ _skipping = False
    call load_stats
    call load_rules
    call load_buildings
    call load_clubs
    
    show screen school_overview_map
    show screen school_overview_stats
    show screen school_overview_buttons

    Subtitles_Empty ""

    jump map_overview

#############################################################################
# building distributor. directs the building calls to the corresponding label
label building(name=""):
    $ reset_stats()
    $ _skipping = True

    hide screen school_overview_map
    hide screen school_overview_stats
    hide screen school_overview_buttons

    call expression name

    call map_overview