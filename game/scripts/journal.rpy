label start_journal:
    call open_journal (1, "", "high_school")

label open_journal (page, display, school):
    python:
        print("Open School: " + school)

    if page == 1:
        call screen journal_1(display, school)
    elif page == 2:
        call screen journal_2(display, school)
    elif page == 3:
        call screen journal_3(display, school)
    elif page == 4:
        call screen journal_4(display, school)

    Subtitles_Empty ""

    jump open_journal

label close_journal:
    hide screen journal
    jump map_overview

style journal_text:
    color "#000"
    size 30

style buttons_idle:
    color "#000"
    hover_color gui.hover_color
    size 30

style buttons_selected take buttons_idle:
    color gui.hover_muted_color

# School Overview
screen journal_1 (display, school):
    tag interaction_overlay
    modal True

    key "K_ESCAPE" action Jump("map_overview")

    imagemap:
        idle "journal/journal/[school]/1_[loli_content]_idle.png"
        hover "journal/journal/[school]/1_[loli_content]_hover.png"

        hotspot (1522, 617, 168, 88) action Call("open_journal", 2, "", school) tooltip "Rules"
        hotspot (1522, 722, 168, 88) action Call("open_journal", 3, "", school) tooltip "Clubs"
        hotspot (1522, 830, 168, 88) action Call("open_journal", 4, "", school) tooltip "Buildings"
        
        if school != "high_school":
            hotspot (373, 80, 160, 67) action Call("open_journal", 1, "", "high_school") tooltip "High School"
        if school != "middle_school" and loli_content >= 1:
            hotspot (550, 80, 160, 67) action Call("open_journal", 1, "", "middle_school") tooltip "Middle School"
        if school != "elementary_school" and loli_content == 2:
            hotspot (725, 80, 160, 67) action Call("open_journal", 1, "", "elementary_school") tooltip "Elementary School"

    if (school == "high_school"):
        text "High School":
            xalign 0.22 yalign 0.1
            size 20
            color "#000"
    if (school == "middle_school"):
        text "Middle School":
            xalign 0.315 yalign 0.1
            size 20
            color "#000"
    if (school == "elementary_school"):
        text "Elem. School":
            xalign 0.415 yalign 0.1
            size 20
            color "#000"

    text "School Overview": 
        xalign 0.25 
        yalign 0.2
        size 60
        color "#000"

    $ school_object = get_school(school)
    $ school_stats = school_object.get_stats()

    frame:
        # background Solid("#00000090")
        background Solid("#00000000")
        area (350, 300, 500, 600)

        viewport id "Overview":
            mousewheel True
            draggable "touch"

            vbox:
                hbox:
                    $ button_style = "buttons_idle"
                    if "money" == display:
                        $ button_style = "buttons_selected"
                    $ money_text = money.display_stat()

                    text "{image=icons/stat_money_icon.png}"
                    textbutton "  Money:":
                            yalign 0.5 
                            text_style button_style
                            action Call("open_journal", 1, "money", school)
                    text "[money_text]" style "journal_text" yalign 0.5

                null height 20

                text "[school_object.title]" style "journal_text" size 40

                null height 20

                hbox:
                    $ button_style = "buttons_idle"
                    if "level" == display:
                        $ button_style = "buttons_selected"
                    $ level_text = school_object.level.display_stat()

                    text "{image=icons/stat_level_icon.png}"
                    textbutton "  Level:":
                                yalign 0.5 
                                text_style button_style
                                action Call("open_journal", 1, "level", school)
                    text "[level_text]" style "journal_text" yalign 0.5

                null height 20

                for stat_key in school_object.get_stats().keys():
                    $ stat_obj = school_object.get_stat_obj(stat_key)
                    $ stat_icon = stat_obj.image_path
                    $ stat_value = stat_obj.display_stat()
                    $ stat_title = get_stat_data(stat_obj.name).title
                    $ button_style = "buttons_idle"
                    if stat_key == display:
                        $ button_style = "buttons_selected"
                    hbox:
                        text "{image=[stat_icon]}"
                        textbutton "  [stat_title]:":
                            yalign 0.5 
                            text_style button_style
                            action Call("open_journal", 1, stat_obj.name, school)
                        text " [stat_value]" style "journal_text" yalign 0.5

        vbar value YScrollValue("Overview"):
            unscrollable "hide"
            xalign 1.0

    if display != "":
        $ active_stat_obj = None
        if display in school_object.get_stats().keys():
            $ active_stat_obj = school_object.get_stat_obj(display)
        if display == "money":
            $ active_stat_obj = money
        if display == "level":
            $ active_stat_obj = school_object.level

        if active_stat_obj != None:
            $ active_desc = active_stat_obj.get_full_description()
            $ active_image = active_stat_obj.get_image()


            image "[active_image]":
                xalign 0.63 yalign 0.65
            
            frame:
                background Solid("#0000")
                area (989, 200, 500, 250)
                viewport id "OverviewDesc":
                    mousewheel True
                    draggable "touch"

                    text active_desc:
                        color "#000"
                        size 22
                
                vbar value YScrollValue("OverviewDesc"):
                    unscrollable "hide"
                    xalign 1.0

    textbutton "Close":
        xalign 0.75
        yalign 0.87
        action Jump("map_overview")

    $ tooltip = GetTooltip()
    if tooltip:
        nearrect:
            focus "tooltip"
            prefer_top True

            frame:
                xalign 0.5
                text tooltip
        

# Rules
screen journal_2 (display, school):
    tag interaction_overlay
    modal True
    
    key "K_ESCAPE" action Jump("map_overview")

    imagemap:
        idle "journal/journal/[school]/2_[loli_content]_idle.png"
        hover "journal/journal/[school]/2_[loli_content]_hover.png"

        hotspot (144, 250, 168, 88) action Call("open_journal", 1, "", school) tooltip "School Overview"
        hotspot (1522, 722, 168, 88) action Call("open_journal", 3, "", school) tooltip "Clubs"
        hotspot (1522, 830, 168, 88) action Call("open_journal", 4, "", school) tooltip "Buildings"
        
        if school != "high_school":
            hotspot (373, 80, 160, 67) action Call("open_journal", 2, "", "high_school") tooltip "High School"
        if school != "middle_school" and loli_content >= 1:
            hotspot (550, 80, 160, 67) action Call("open_journal", 2, "", "middle_school") tooltip "Middle School"
        if school != "elementary_school" and loli_content == 2:
            hotspot (725, 80, 160, 67) action Call("open_journal", 2, "", "elementary_school") tooltip "Elementary School"

    if (school == "high_school"):
        text "High School":
            xalign 0.22 yalign 0.1
            size 20
            color "#000"
    if (school == "middle_school"):
        text "Middle School":
            xalign 0.315 yalign 0.1
            size 20
            color "#000"
    if (school == "elementary_school"):
        text "Elem. School":
            xalign 0.415 yalign 0.1
            size 20
            color "#000"

    text "Rules": 
        xalign 0.25 
        yalign 0.2
        size 60
        color "#000"
    frame:
        # background Solid("#00000090")
        background Solid("#00000000")
        area (350, 300, 500, 600)

        viewport id "RuleList":
            mousewheel True
            draggable "touch"

            vbox:
                for rule_name in get_visible_rules_by_school(school):
                    $ rule = get_rule(rule_name)
                    if rule is not None:
                        $ rule_title = rule.title
                        $ button_style = "buttons_idle"
                        if rule_name == display:
                            $ button_style = "buttons_selected"
                        textbutton rule_title:
                            text_style button_style
                            action Call("open_journal", 2, rule_name, school)

        vbar value YScrollValue("RuleList"):
            unscrollable "hide"
            xalign 1.0

    if display != "":
        $ active_rule = get_rule(display)
        $ active_rule_name = active_rule.name
        $ active_rule_desc = active_rule.description
        $ active_rule_image = "journal/empty_image.png"
        if renpy.exists(active_rule.image_path):
            $ active_rule_image = active_rule.image_path

        image "[active_rule_image]":
            xalign 0.63 yalign 0.65
        
        frame:
            background Solid("#0000")
            area (989, 200, 500, 250)
            viewport id "RuleDesc":
                mousewheel True
                draggable "touch"

                text active_rule_desc:
                    color "#000"
                    size 22
            
            vbar value YScrollValue("RuleDesc"):
                unscrollable "hide"
                xalign 1.0

        frame:
            background Solid("#0000")
            area (1350, 474, 150, 350)

            viewport id "RuleCond":
                mousewheel True
                draggable "touch"

                vbox:
                    for condition in active_rule.unlock_conditions:
                        if "blocking" not in condition or not condition["blocking"]:
                            if condition["type"] == "level":
                                if active_rule.is_condition_fullfilled(school, condition):
                                    text "{image=icons/stat_level_icon.png} {color=#0f0}" + condition["value"] + "{/color}" size 30
                                else:
                                    text "{image=icons/stat_level_icon.png} {color=#f00}" + condition["value"] + "{/color}" size 30
                            elif condition["type"] == "stat":
                                $ stat_name = condition["stat"]
                                $ stat_icon = "icons/stat_" + stat_name + "_icon.png"
                                $ stat_value = condition["value"]
                                if active_rule.is_condition_fullfilled(school, condition):
                                    hbox:
                                        text "{image=[stat_icon]}"
                                        text " {color=#0f0}[stat_value]{/color}" size 30 yalign 0.5
                                else:
                                    hbox:
                                        text "{image=[stat_icon]}"
                                        text " {color=#f00}[stat_value]{/color}" size 30 yalign 0.5
                                

            vbar value YScrollValue("RuleCond"):
                unscrollable "hide"
                xalign 1.0

        textbutton "Plan for vote":
            xalign 0.576 yalign 0.87

    textbutton "Close":
        xalign 0.75
        yalign 0.87
        action Jump("map_overview")

    $ tooltip = GetTooltip()
    if tooltip:
        nearrect:
            focus "tooltip"
            prefer_top True

            frame:
                xalign 0.5
                text tooltip

# Clubs
screen journal_3 (display, school):
    tag interaction_overlay
    modal True

    key "K_ESCAPE" action Jump("map_overview")

    imagemap:
        idle "journal/journal/[school]/3_[loli_content]_idle.png"
        hover "journal/journal/[school]/3_[loli_content]_hover.png"

        hotspot (144, 250, 168, 88) action Call("open_journal", 1, "", school) tooltip "School Overview"
        hotspot (144, 617, 168, 88) action Call("open_journal", 2, "", school) tooltip "Rules"
        hotspot (1522, 830, 168, 88) action Call("open_journal", 4, "", school) tooltip "Buildings"

        if school != "high_school":
            hotspot (373, 80, 160, 67) action Call("open_journal", 3, "", "high_school") tooltip "High School"
        if school != "middle_school" and loli_content >= 1:
            hotspot (550, 80, 160, 67) action Call("open_journal", 3, "", "middle_school") tooltip "Middle School"
        if school != "elementary_school" and loli_content == 2:
            hotspot (725, 80, 160, 67) action Call("open_journal", 3, "", "elementary_school") tooltip "Elementary School"

    if (school == "high_school"):
        text "High School":
            xalign 0.22 yalign 0.1
            size 20
            color "#000"
    if (school == "middle_school"):
        text "Middle School":
            xalign 0.315 yalign 0.1
            size 20
            color "#000"
    if (school == "elementary_school"):
        text "Elem. School":
            xalign 0.415 yalign 0.1
            size 20
            color "#000"

    frame:
        background Solid("#0000")
        area (350, 300, 500, 600)

        viewport id "ClubsList":
            mousewheel True
            draggable "touch"

            vbox:
                for club in clubs.values():
                    if club is not None:
                        $ club_title = club.title
                        $ button_style = "buttons_idle"
                        if club.name == display:
                            $ button_style = "buttons_selected"
                        textbutton club_title:
                            text_style button_style
                            action Call("open_journal", 3, club.name, school)

        vbar value YScrollValue("ClubsList"):
            unscrollable "hide"
            xalign 1.0

    if display != "":
        $ active_club = get_club(display)
        $ active_club_name = active_club.name
        $ active_club_desc = active_club.description
        $ active_club_image = "journal/empty_image.png"
        if renpy.exists(active_club.image_path):
            $ active_club_image = active_club.image_path

        image "[active_club_image]":
            xalign 0.63 yalign 0.65
        
        frame:
            background Solid("#0000")
            area (989, 200, 500, 250)
            viewport id "ClubDesc":
                mousewheel True
                draggable "touch"

                text active_club_desc:
                    color "#000"
                    size 22
            
            vbar value YScrollValue("ClubDesc"):
                unscrollable "hide"
                xalign 1.0

        frame:
            background Solid("#0000")
            area (1350, 474, 150, 350)

            viewport id "ClubCond":
                mousewheel True
                draggable "touch"

                vbox:
                    for condition in active_club.unlock_conditions:
                        if "blocking" not in condition or not condition["blocking"]:
                            if condition["type"] == "stat":
                                $ stat_name = condition["stat"]
                                $ stat_icon = "icons/stat_" + stat_name + "_icon.png"
                                $ stat_value = condition["value"]
                                if active_club.is_condition_fullfilled(condition, school):
                                    hbox:
                                        text "{image=[stat_icon]}"
                                        text " {color=#0f0}[stat_value]{/color}" size 30 yalign 0.5
                                else:
                                    hbox:
                                        text "{image=[stat_icon]}"
                                        text " {color=#f00}[stat_value]{/color}" size 30 yalign 0.5
                                

            vbar value YScrollValue("ClubCond"):
                unscrollable "hide"
                xalign 1.0

    text "Clubs": 
        xalign 0.25 
        yalign 0.2
        size 60
        color "#000"

    textbutton "Close":
        xalign 0.75
        yalign 0.87
        action Jump("map_overview")

    $ tooltip = GetTooltip()
    if tooltip:
        nearrect:
            focus "tooltip"
            prefer_top True

            frame:
                xalign 0.5
                text tooltip

# Buildings
screen journal_4 (display, school):
    tag interaction_overlay
    modal True

    key "K_ESCAPE" action Jump("map_overview")

    imagemap:
        idle "journal/journal/high_school/4_0_idle.png"
        hover "journal/journal/high_school/4_0_hover.png"

        hotspot (144, 250, 168, 88) action Call("open_journal", 1, "", school) tooltip "School Overview"
        hotspot (144, 617, 168, 88) action Call("open_journal", 2, "", school) tooltip "Rules"
        hotspot (144, 722, 168, 88) action Call("open_journal", 3, "", school) tooltip "Clubs"

    frame:
        background Solid("#0000")
        area (350, 300, 500, 600)

        viewport id "BuildingList":
            mousewheel True
            draggable "touch"

            vbox:
                for building in buildings.values():
                    if building is not None:
                        $ building_title = building.title
                        $ button_style = "buttons_idle"
                        if building.name == display:
                            $ button_style = "buttons_selected"
                        textbutton building_title:
                            text_style button_style
                            action Call("open_journal", 4, building.name, school)

        vbar value YScrollValue("BuildingList"):
            unscrollable "hide"
            xalign 1.0

    if display != "":
        $ active_building = get_building(display)
        $ active_building_name = active_building.name
        $ active_building_desc = active_building.description
        $ active_building_image = "journal/empty_image.png"
        if renpy.exists(active_building.image_path):
            $ active_building_image = active_building.image_path

        image "[active_building_image]":
            xalign 0.63 yalign 0.65
        
        frame:
            background Solid("#0000")
            area (989, 200, 500, 250)
            viewport id "BuildingDesc":
                mousewheel True
                draggable "touch"

                text active_building_desc:
                    color "#000"
                    size 22
            
            vbar value YScrollValue("BuildingDesc"):
                unscrollable "hide"
                xalign 1.0

        frame:
            background Solid("#0000")
            area (1350, 474, 150, 350)

            viewport id "BuildingCond":
                mousewheel True
                draggable "touch"

                vbox:
                    for condition in active_building.unlock_conditions:
                        if "blocking" not in condition or not condition["blocking"]:
                            if condition["type"] == "stat":
                                $ stat_name = condition["stat"]
                                $ stat_icon = "icons/stat_" + stat_name + "_icon.png"
                                $ stat_value = condition["value"]
                                if active_building.is_condition_fullfilled(condition):
                                    hbox:
                                        text "{image=[stat_icon]}"
                                        text " {color=#0f0}[stat_value]{/color}" size 30 yalign 0.5
                                else:
                                    hbox:
                                        text "{image=[stat_icon]}"
                                        text " {color=#f00}[stat_value]{/color}" size 30 yalign 0.5
                                

            vbar value YScrollValue("BuildingCond"):
                unscrollable "hide"
                xalign 1.0

        textbutton "Plan for vote":
            xalign 0.576 yalign 0.87

    text "Buildings": 
        xalign 0.25 
        yalign 0.2
        size 60
        color "#000"

    textbutton "Close":
        xalign 0.75
        yalign 0.87
        action Jump("map_overview")

    $ tooltip = GetTooltip()
    if tooltip:
        nearrect:
            focus "tooltip"
            prefer_top True

            frame:
                xalign 0.5
                text tooltip

