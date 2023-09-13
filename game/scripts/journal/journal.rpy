label start_journal:
    call open_journal (1, "", "high_school") from start_journal_1

label open_journal(page, display, school):
    if page == 1:
        call screen journal_1(display, school)
    elif page == 2:
        call screen journal_2(display, school)
    elif page == 3:
        call screen journal_3(display, school)
    elif page == 4:
        call screen journal_4(display, school)
    elif page == 5:
        call screen journal_5(display, school)

label close_journal:
    hide screen journal
    jump map_overview

style journal_desc:
    color "#000"
    size 20

style journal_text:
    color "#000"
    size 30

style journal_text_center take journal_text:
    textalign 0.5

style condition_text:
    size 30
style condition_desc:
    size 20

style buttons_idle:
    color "#000"
    hover_color gui.hover_color
    size 30

style buttons_inactive take buttons_idle:
    color gui.button_text_insensitive_color
    size 30

style buttons_selected take buttons_idle:
    color gui.hover_muted_color

style buttons_active take buttons_idle:
    color "#008800"

# School Overview
screen journal_1(display, school):
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
            hotspot (373, 80, 160, 67) action Call("open_journal", 1, display, "high_school") tooltip "High School"
        if school != "middle_school" and loli_content >= 1:
            hotspot (550, 80, 160, 67) action Call("open_journal", 1, display, "middle_school") tooltip "Middle School"
        if school != "elementary_school" and loli_content == 2:
            hotspot (725, 80, 160, 67) action Call("open_journal", 1, display, "elementary_school") tooltip "Elementary School"

    if cheat_mode:
        imagebutton:
            idle "journal/journal/cheat_tag_idle.png"
            hover "journal/journal/cheat_tag_hover.png"
            tooltip "Cheats"
            xpos 1268
            ypos 70
            action Call("open_journal", 5, "", school)
        
    if (school == "high_school" and loli_content >= 1):
        text "High School":
            xalign 0.22 yalign 0.1
            size 20
            color "#000"
    if (school == "middle_school" and loli_content >= 1):
        text "Middle School":
            xalign 0.315 yalign 0.1
            size 20
            color "#000"
    if (school == "elementary_school" and loli_content == 2):
        text "Elem. School":
            xalign 0.415 yalign 0.1
            size 20
            color "#000"

    text "School Overview": 
        xalign 0.25 
        yalign 0.2
        size 60
        color "#000"

    $ school_object = get_character(school, charList["schools"])
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
                    xalign 1.05

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
screen journal_2(display, school):
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
            hotspot (373, 80, 160, 67) action Call("open_journal", 2, display, "high_school") tooltip "High School"
        if school != "middle_school" and loli_content >= 1:
            hotspot (550, 80, 160, 67) action Call("open_journal", 2, display, "middle_school") tooltip "Middle School"
        if school != "elementary_school" and loli_content == 2:
            hotspot (725, 80, 160, 67) action Call("open_journal", 2, display, "elementary_school") tooltip "Elementary School"

    if cheat_mode:
        imagebutton:
            idle "journal/journal/cheat_tag_idle.png"
            hover "journal/journal/cheat_tag_hover.png"
            tooltip "Cheats"
            xpos 1268
            ypos 70
            action Call("open_journal", 5, "", school)
        
    if (school == "high_school" and loli_content >= 1):
        text "High School":
            xalign 0.22 yalign 0.1
            size 20
            color "#000"
    if (school == "middle_school" and loli_content >= 1):
        text "Middle School":
            xalign 0.315 yalign 0.1
            size 20
            color "#000"
    if (school == "elementary_school" and loli_content == 2):
        text "Elem. School":
            xalign 0.415 yalign 0.1
            size 20
            color "#000"

    text "Rules": 
        xalign 0.25 
        yalign 0.2
        size 60
        color "#000"

    $ rule_locked_list = get_visible_locked_rules_by_school(school)
    $ rule_unlocked_list = get_visible_unlocked_rules_by_school(school)
    $ rule_list = rule_locked_list + rule_unlocked_list
    $ rule_adj = ui.adjustment()
    python:
        rule_adj.value = 0

        if display in rule_list:
            current_selected = rule_list.index(display)
            rule_adj.range = len(rule_list)
            rule_adj.value = (current_selected - 5) * len(rule_list) * 2.5

    frame:
        # background Solid("#00000090")
        background Solid("#00000000")
        area (330, 300, 560, 600)

        viewport id "RuleList": 
            yadjustment rule_adj
            mousewheel True
            draggable "touch"

            vbox:
                $ journal_settings = get_game_data("journal_setting_2_show_locked")
                if journal_settings == None or journal_settings:
                    textbutton "hide locked rules":
                        text_style "buttons_idle"
                        yalign 0.5
                        action Call("set_journal_setting", 2, display, school, 'show_locked', False)
                    image "journal/journal/left_list_seperator.png"
                    for rule_name in rule_locked_list:
                        $ rule = get_rule(rule_name)
                        if rule is not None:
                            $ rule_title = rule.get_title()
                            $ button_style = "buttons_idle"
                            if rule_name == display:
                                $ button_style = "buttons_selected"
                            textbutton rule_title:
                                text_style button_style
                                action Call("open_journal", 2, rule_name, school)
                else:
                    textbutton "show locked rules":
                        text_style "buttons_inactive"
                        yalign 0.5
                        action Call("set_journal_setting", 2, display, school, 'show_locked', True)
                    image "journal/journal/left_list_seperator.png"

                null height 20

                $ journal_settings = get_game_data("journal_setting_2_show_unlocked")
                if journal_settings == None or journal_settings:
                    textbutton "hide unlocked rules":
                        text_style "buttons_idle"
                        yalign 0.5
                        action Call("set_journal_setting", 2, display, school, 'show_unlocked', False)
                    image "journal/journal/left_list_seperator.png"
                    for rule_name in rule_unlocked_list:
                        $ rule = get_rule(rule_name)
                        if rule is not None:
                            $ rule_title = rule.get_title()
                            $ button_style = "buttons_active"
                            if rule_name == display:
                                $ button_style = "buttons_selected"
                            textbutton rule_title:
                                text_style button_style
                                action Call("open_journal", 2, rule_name, school)
                else:
                    textbutton "show unlocked rules":
                        text_style "buttons_inactive"
                        yalign 0.5
                        action Call("set_journal_setting", 2, display, school, 'show_unlocked', True)
                    image "journal/journal/left_list_seperator.png"

        vbar value YScrollValue("RuleList"):
            unscrollable "hide"
            xalign 1.0

    if display != "" and not get_rule(display).is_visible(school):
        $ display = ""

    if display != "":
        $ active_rule = get_rule(display)
        $ active_rule_name = active_rule.get_name()
        $ active_rule_desc = active_rule.get_description_str()
        $ active_school = get_character(school, charList["schools"])

        $ active_rule_image = active_rule.get_image(school, active_school.get_level())
        $ active_rule_full_image = active_rule.get_full_image(school, active_school.get_level())


        if active_rule_full_image != None:
            button:
                xalign 0.63 yalign 0.65
                image "[active_rule_image]"
                action Call("call_max_image_from_journal", active_rule_full_image, 2, school, display)
        else:
            image "[active_rule_image]": 
                xalign 0.629 yalign 0.647
        
        $ active_rule_desc_conditions = active_rule.get_desc_conditions()
        
        frame:
            background Solid("#0000")
            area (989, 200, 500, 250)
            viewport id "RuleDesc":
                mousewheel True
                draggable "touch"

                vbox:
                    text active_rule_desc style "journal_desc"

                    if len(active_rule_desc_conditions) != 0:
                        null height 40
                        text "{u}To unlock you need:{/u}" style "journal_desc"
                        for condition in active_rule_desc_conditions:
                            $ texts = condition.to_desc_text(school)
                            textbutton texts:
                                text_style "journal_desc"
                                yalign 0.5
                                action NullAction()
        
            vbar value YScrollValue("RuleDesc"):
                unscrollable "hide"
                xalign 1.03

        frame:
            background Solid("#0000")
            area (1350, 474, 150, 328)

            viewport id "RuleCond":
                mousewheel True
                draggable "touch"

                vbox:
                    for condition in active_rule.get_list_conditions():
                        $ texts = condition.to_list_text(school)
                        hbox:
                            textbutton texts[0]:
                                tooltip condition.get_name()
                                action NullAction()
                            textbutton texts[1]:
                                text_style "condition_text"
                                yalign 0.5
                                tooltip condition.get_name()
                                action NullAction()
                                
            vbar value YScrollValue("RuleCond"):
                unscrollable "hide"
                xalign 1
            bar value XScrollValue("RuleCond"):
                unscrollable "hide"
                ypos 328

        # if not active_rule.is_unlocked(school):
        #     $ voteProposal = get_game_data("voteProposal")
        #     if voteProposal == None or voteProposal[3].get_name() != display:
        #         textbutton "Plan for vote":
        #             xalign 0.6 yalign 0.87
        #             text_style "buttons_idle"
        #             action Call("add_rule_to_proposal", display, school)
        #     else:
        #         text "Already queued!":
        #             xalign 0.6 yalign 0.87
        #             color "#f00"
        # else:
        #     text "Already unlocked!":
        #         xalign 0.6 yalign 0.87
        #         color "#008800"
        #         size 30

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
screen journal_3(display, school):
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
            hotspot (373, 80, 160, 67) action Call("open_journal", 3, display, "high_school") tooltip "High School"
        if school != "middle_school" and loli_content >= 1:
            hotspot (550, 80, 160, 67) action Call("open_journal", 3, display, "middle_school") tooltip "Middle School"
        if school != "elementary_school" and loli_content == 2:
            hotspot (725, 80, 160, 67) action Call("open_journal", 3, display, "elementary_school") tooltip "Elementary School"
    
    if cheat_mode:
        imagebutton:
            idle "journal/journal/cheat_tag_idle.png"
            hover "journal/journal/cheat_tag_hover.png"
            tooltip "Cheats"
            xpos 1268
            ypos 70
            action Call("open_journal", 5, "", school)
        
    if (school == "high_school" and loli_content >= 1):
        text "High School":
            xalign 0.22 yalign 0.1
            size 20
            color "#000"
    if (school == "middle_school" and loli_content >= 1):
        text "Middle School":
            xalign 0.315 yalign 0.1
            size 20
            color "#000"
    if (school == "elementary_school" and loli_content == 2):
        text "Elem. School":
            xalign 0.415 yalign 0.1
            size 20
            color "#000"

    $ club_locked_list = get_visible_locked_clubs_by_school(school)
    $ club_unlocked_list = get_visible_unlocked_clubs_by_school(school)
    $ club_list = club_locked_list + club_unlocked_list
    $ club_adj = ui.adjustment()
    python:
        club_adj.value = 0

        if display in club_list:
            current_selected = club_list.index(display)
            club_adj.range = len(club_list)
            club_adj.value = (current_selected - 5) * len(club_list) * 2.5

    frame:
        background Solid("#0000")
        area (330, 300, 560, 600)

        viewport id "ClubsList":
            yadjustment club_adj
            mousewheel True
            draggable "touch"

            vbox:
                $ journal_settings = get_game_data("journal_setting_3_show_locked")
                if journal_settings == None or journal_settings:
                    textbutton "hide locked clubs":
                        text_style "buttons_idle"
                        yalign 0.5
                        action Call("set_journal_setting", 3, display, school, 'show_locked', False)
                    image "journal/journal/left_list_seperator.png"
                    for club_name in club_locked_list:
                        $ club = get_club(club_name)
                        if club is not None:
                            $ club_title = club.get_title()
                            $ button_style = "buttons_idle"
                            if club_name == display:
                                $ button_style = "buttons_selected"
                            textbutton club_title:
                                text_style button_style
                                action Call("open_journal", 3, club_name, school)
                else:
                    textbutton "show locked clubs":
                        text_style "buttons_inactive"
                        yalign 0.5
                        action Call("set_journal_setting", 3, display, school, 'show_locked', True)
                    image "journal/journal/left_list_seperator.png"

                null height 20

                $ journal_settings = get_game_data("journal_setting_3_show_unlocked")
                if journal_settings == None or journal_settings:
                    textbutton "hide unlocked clubs":
                        text_style "buttons_idle"
                        yalign 0.5
                        action Call("set_journal_setting", 3, display, school, 'show_unlocked', False)
                    image "journal/journal/left_list_seperator.png"
                    for club_name in club_unlocked_list:
                        $ club = get_club(club_name)
                        if club is not None:
                            $ club_title = club.get_title()
                            $ button_style = "buttons_active"
                            if club_name == display:
                                $ button_style = "buttons_selected"
                            textbutton club_title:
                                text_style button_style
                                action Call("open_journal", 3, club_name, school)
                else:
                    textbutton "show unlocked clubs":
                        text_style "buttons_inactive"
                        yalign 0.5
                        action Call("set_journal_setting", 3, display, school, 'show_unlocked', True)
                    image "journal/journal/left_list_seperator.png"

        vbar value YScrollValue("ClubsList"):
            unscrollable "hide"
            xalign 1.0

    if display != "" and not get_club(display).is_visible(school):
        $ display = ""

    if display != "":
        $ active_club = get_club(display)
        $ active_club_name = active_club.get_name()
        $ active_club_desc = active_club.get_description_str()
        $ active_school = get_character(school, charList["schools"])

        $ active_club_image = active_club.get_image(school, active_school.get_level())
        $ active_club_full_image = active_club.get_full_image(school, active_school.get_level())

        if active_club_full_image != None:
            button:
                xalign 0.63 yalign 0.65
                image "[active_club_image]"
                action Call("call_max_image_from_journal", active_club_full_image, 3, school, display)
        else:
            image "[active_club_image]": 
                xalign 0.629 yalign 0.647
        
        $ active_club_desc_conditions = active_club.get_desc_conditions()
        
        frame:
            background Solid("#0000")
            area (989, 200, 500, 250)
            viewport id "ClubDesc":
                mousewheel True
                draggable "touch"

                vbox:
                    text active_club_desc style "journal_desc"

                    if len(active_club_desc_conditions) != 0:
                        null height 40
                        text "{u}To unlock you need:{/u}" style "journal_desc"
                        for condition in active_club_desc_conditions:
                            $ texts = condition.to_desc_text(school)
                            textbutton texts:
                                text_style "journal_desc"
                                yalign 0.5
                                action NullAction()
        
            vbar value YScrollValue("ClubDesc"):
                unscrollable "hide"
                xalign 1.0

        frame:
            background Solid("#0000")
            area (1350, 474, 150, 328)

            viewport id "ClubCond":
                mousewheel True
                draggable "touch"

                vbox:
                    for condition in active_club.get_list_conditions():
                        $ texts = condition.to_list_text(school)
                        hbox:
                            textbutton texts[0]:
                                tooltip condition.get_name()
                                action NullAction()
                            textbutton texts[1]:
                                text_style "condition_text"
                                yalign 0.5
                                tooltip condition.get_name()
                                action NullAction()
                                
            vbar value YScrollValue("ClubCond"):
                unscrollable "hide"
                xalign 1.0
            bar value XScrollValue("ClubCond"):
                unscrollable "hide"
                ypos 328

        # if not active_club.is_unlocked(school):
        #     $ voteProposal = get_game_data("voteProposal")
        #     if voteProposal == None or voteProposal[3].get_name() != display:
        #         textbutton "Plan for vote":
        #             xalign 0.6 yalign 0.87
        #             text_style "buttons_idle"
        #             action Call("add_club_to_proposal", display, school)
        #     else:
        #         text "Already queued!":
        #             xalign 0.6 yalign 0.87
        #             color "#f00"
        # else:
        #     text "Already unlocked!":
        #         xalign 0.6 yalign 0.87
        #         color "#008800"

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
screen journal_4(display, school):
    tag interaction_overlay
    modal True

    key "K_ESCAPE" action Jump("map_overview")

    imagemap:
        idle "journal/journal/high_school/4_0_idle.png"
        hover "journal/journal/high_school/4_0_hover.png"

        hotspot (144, 250, 168, 88) action Call("open_journal", 1, "", school) tooltip "School Overview"
        hotspot (144, 617, 168, 88) action Call("open_journal", 2, "", school) tooltip "Rules"
        hotspot (144, 722, 168, 88) action Call("open_journal", 3, "", school) tooltip "Clubs"
    
    if cheat_mode:
        imagebutton:
            idle "journal/journal/cheat_tag_idle.png"
            hover "journal/journal/cheat_tag_hover.png"
            tooltip "Cheats"
            xpos 1268
            ypos 70
            action Call("open_journal", 5, "", school)
    
    $ building_locked_list = get_visible_locked_buildings()
    $ building_unlocked_list = get_visible_unlocked_buildings()
    $ building_list = building_locked_list + building_unlocked_list
    $ building_adj = ui.adjustment()
    python:
        building_adj.value = 0

        if display in building_list:
            current_selected = building_list.index(display)
            building_adj.range = len(building_list)
            building_adj.value = (current_selected - 5) * len(building_list) * 2.5

    frame:
        background Solid("#0000")
        area (330, 300, 560, 600)

        viewport id "BuildingList":
            yadjustment building_adj
            mousewheel True
            draggable "touch"

            vbox:
                $ journal_settings = get_game_data("journal_setting_4_show_locked")
                if journal_settings == None or journal_settings:
                    textbutton "hide locked buildings":
                        text_style "buttons_idle"
                        yalign 0.5
                        action Call("set_journal_setting", 4, display, school, 'show_locked', False)
                    image "journal/journal/left_list_seperator.png"
                    for building_name in building_locked_list:
                        $ building = get_building(building_name)
                        if building is not None:
                            $ building_title = building.get_title()
                            $ button_style = "buttons_idle"
                            if building_name == display:
                                $ button_style = "buttons_selected"
                            textbutton building_title:
                                text_style button_style
                                action Call("open_journal", 4, building_name, school)
                else:
                    textbutton "show locked buildings":
                        text_style "buttons_inactive"
                        yalign 0.5
                        action Call("set_journal_setting", 4, display, school, 'show_locked', True)
                    image "journal/journal/left_list_seperator.png"

                null height 20

                $ journal_settings = get_game_data("journal_setting_4_show_unlocked")
                if journal_settings == None or journal_settings:
                    textbutton "hide unlocked buildings":
                        text_style "buttons_idle"
                        yalign 0.5
                        action Call("set_journal_setting", 4, display, school, 'show_unlocked', False)
                    image "journal/journal/left_list_seperator.png"
                    for building_name in building_unlocked_list:
                        $ building = get_building(building_name)
                        if building is not None:
                            $ building_title = building.get_title()
                            $ button_style = "buttons_active"
                            if building_name == display:
                                $ button_style = "buttons_selected"
                            textbutton building_title:
                                text_style button_style
                                action Call("open_journal", 4, building_name, school)
                else:
                    textbutton "show unlocked buildings":
                        text_style "buttons_inactive"
                        yalign 0.5
                        action Call("set_journal_setting", 4, display, school, 'show_unlocked', True)
                    image "journal/journal/left_list_seperator.png"

        vbar value YScrollValue("BuildingList"):
            unscrollable "hide"
            xalign 1.0

    if display != "" and not get_building(display).is_visible():
        $ display = ""

    if display != "":
        $ active_building = get_building(display)
        $ active_building_name = active_building.get_name()
        $ active_building_desc = active_building.get_description_str()

        $ active_building_image = active_building.get_image()
        $ active_building_full_image = active_building.get_full_image()

        if active_building_full_image != None:
            button:
                xalign 0.63 yalign 0.65
                image "[active_building_image]"
                action Call("call_max_image_from_journal", active_building_full_image, 4, school, display)
        else:
            image "[active_building_image]": 
                xalign 0.629 yalign 0.647
        
        $ cond_type = "unlock"

        if active_building.is_unlocked():
            $ cond_type = "upgrade"

        $ active_building_desc_conditions = active_building.get_desc_conditions(cond_type)
        
        frame:
            background Solid("#0000")
            area (989, 200, 500, 250)
            viewport id "BuildingDesc":
                mousewheel True
                draggable "touch"

                vbox:
                    text active_building_desc style "journal_desc"

                    if len(active_building_desc_conditions) != 0:
                        null height 40
                        text "{u}To [cond_type] you need:{/u}" style "journal_desc"
                        for condition in active_building_desc_conditions:
                            $ texts = condition.to_desc_text(school)
                            textbutton texts:
                                text_style "journal_desc"
                                yalign 0.5
                                action NullAction()
        
            vbar value YScrollValue("BuildingDesc"):
                unscrollable "hide"
                xalign 1.0

        frame:
            background Solid("#0000")
            area (1350, 474, 150, 328)

            viewport id "BuildingCond":
                mousewheel True
                draggable "touch"

                vbox:
                    for condition in active_building.get_list_conditions(cond_type):
                        $ texts = condition.to_list_text(school)
                        hbox:
                            textbutton texts[0]:
                                tooltip condition.get_name()
                                action NullAction()
                            textbutton texts[1]:
                                text_style "condition_text"
                                yalign 0.5
                                tooltip condition.get_name()
                                action NullAction()

            vbar value YScrollValue("BuildingCond"):
                unscrollable "hide"
                xalign 1.0
            bar value XScrollValue("BuildingCond"):
                unscrollable "hide"
                ypos 328

        # if not active_building.is_unlocked() or active_building.has_higher_level():
        #     $ voteProposal = get_game_data("voteProposal")
        #     if voteProposal == None or voteProposal[3].get_name() != display:
        #         textbutton "Vote for [cond_type]":
        #             xalign 0.6 yalign 0.87
        #             text_style "buttons_idle"
        #             action Call("add_building_to_proposal", display, school)
        #     else:
        #         text "Already queued!":
        #             xalign 0.6 yalign 0.87
        #             color "#ff0000"
        # else:
        #     text "Fully upgraded!":
        #         xalign 0.6 yalign 0.87
        #         color "#008800"

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

# Cheats
screen journal_5(display, school):
    tag interaction_overlay
    modal True

    key "K_ESCAPE" action Jump("map_overview")

    imagemap:
        if not display.startswith("building"):
            idle "journal/journal/[school]/5_[loli_content]_idle.png"
            hover "journal/journal/[school]/5_[loli_content]_hover.png"
        else:
            idle "journal/journal/high_school/5_0_idle.png"
            hover "journal/journal/high_school/5_0_hover.png"

        hotspot (144, 250, 168, 88) action Call("open_journal", 1, "", school) tooltip "School Overview"
        hotspot (144, 617, 168, 88) action Call("open_journal", 2, "", school) tooltip "Rules"
        hotspot (144, 722, 168, 88) action Call("open_journal", 3, "", school) tooltip "Clubs"
        hotspot (144, 830, 168, 88) action Call("open_journal", 4, "", school) tooltip "Buildings"

        if school != "high_school":
            hotspot (373, 80, 160, 67) action Call("open_journal", 5, display, "high_school") tooltip "High School"
        if school != "middle_school" and loli_content >= 1:
            hotspot (550, 80, 160, 67) action Call("open_journal", 5, display, "middle_school") tooltip "Middle School"
        if school != "elementary_school" and loli_content == 2:
            hotspot (725, 80, 160, 67) action Call("open_journal", 5, display, "elementary_school") tooltip "Elementary School"

    if not display.startswith("building"):
        if (school == "high_school" and loli_content >= 1):
            text "High School":
                xalign 0.22 yalign 0.1
                size 20
                color "#000"
        if (school == "middle_school" and loli_content >= 1):
            text "Middle School":
                xalign 0.315 yalign 0.1
                size 20
                color "#000"
        if (school == "elementary_school" and loli_content == 2):
            text "Elem. School":
                xalign 0.415 yalign 0.1
                size 20
                color "#000"


    text "Cheats":
        xalign 0.72 yalign 0.11
        size 20
        color "#000"

    frame:
        background Solid("#0000")
        area (330, 300, 560, 600)

        viewport id "CheatListLeft":
            mousewheel True
            draggable "touch"

            $ options = {
                "stats": "Stats",
                "rules": "Rules",
                "clubs": "Clubs",
                "buildings": "Buildings",
            }

            vbox:
                for option in options.keys():
                    $ option_text = options[option]
                    $ button_style = "buttons_idle"
                    if option == display:
                        $ button_style = "buttons_selected"
                    textbutton option_text:
                        text_style button_style
                        action Call("open_journal", 5, option, school)
                

        vbar value YScrollValue("CheatListLeft"):
            unscrollable "hide"
            xalign 1.0

    $ active_school = get_character(school, charList["schools"])

    if display == "stats":
        frame:
            background Solid("#0000")
            area (950, 200, 560, 690)

            $ money_val  = money.get_display_value()
            $ level  = active_school.get_level()
            $ corruption = active_school.get_display_value("corruption")
            $ inhibition = active_school.get_display_value("inhibition")
            $ happiness  = active_school.get_display_value("happiness")
            $ education  = active_school.get_display_value("education")
            $ charm      = active_school.get_display_value("charm")
            $ reputation = active_school.get_display_value("reputation")

            viewport id "CheatStatList":
                mousewheel True
                draggable "touch"
                vbox:
                    text "Changing stats can lead to unintended behaviour or a broken game save.\nProceed on your own risk.":
                        color "#000000"
                        size 20
                    # MONEY
                    hbox:
                        text "{image=icons/stat_money_icon.png}"
                        text " Money" style "journal_text" yalign 0.5
                    hbox:
                        textbutton "1000" action Call("modify_stat", "money", -1000, school) text_style "buttons_idle"
                        null width 30
                        textbutton "-" action Call("modify_stat", "money", -100, school) text_style "buttons_idle"
                        null width 40
                        button:
                            text "[money_val]" xalign 0.5 style "journal_text"
                            xsize 150
                        null width 40
                        textbutton "+" action Call("modify_stat", "money", 100, school) text_style "buttons_idle"
                        null width 30
                        textbutton "1000" action Call("modify_stat", "money", 1000, school) text_style "buttons_idle"
                    null height 30
                    # LEVEL
                    hbox:
                        text "{image=icons/stat_level_icon.png}"
                        text " Level" style "journal_text" yalign 0.5
                    hbox:
                        textbutton "Min" action Call("modify_stat", "level", -100, school) text_style "buttons_idle"
                        null width 30
                        textbutton "5" action Call("modify_stat", "level", -5, school) text_style "buttons_idle"
                        null width 30
                        textbutton "-" action Call("modify_stat", "level", -1, school) text_style "buttons_idle"
                        null width 20
                        button:
                            text "[level]" xalign 0.5 style "journal_text"
                            xsize 100
                        null width 20
                        textbutton "+" action Call("modify_stat", "level", 1, school) text_style "buttons_idle"
                        null width 30
                        textbutton "5" action Call("modify_stat", "level", 5, school) text_style "buttons_idle"
                        null width 30
                        textbutton "Max" action Call("modify_stat", "level", 100, school) text_style "buttons_idle"
                    null height 30
                    # CORRUPTION
                    hbox:
                        text "{image=icons/stat_corruption_icon.png}"
                        text " Corruption" style "journal_text" yalign 0.5
                    hbox:
                        textbutton "Min" action Call("modify_stat", "corruption", -100, school) text_style "buttons_idle"
                        null width 20
                        textbutton "10" action Call("modify_stat", "corruption", -10, school) text_style "buttons_idle"
                        null width 20
                        textbutton "-" action Call("modify_stat", "corruption", -1, school) text_style "buttons_idle"
                        null width 20
                        button:
                            text "[corruption]" xalign 0.5 style "journal_text"
                            xsize 100
                        null width 20
                        textbutton "+" action Call("modify_stat", "corruption", 1, school) text_style "buttons_idle"
                        null width 20
                        textbutton "10" action Call("modify_stat", "corruption", 10, school) text_style "buttons_idle"
                        null width 20
                        textbutton "Max" action Call("modify_stat", "corruption", 100, school) text_style "buttons_idle"
                    null height 30
                    # INHIBITION
                    hbox:
                        text "{image=icons/stat_inhibition_icon.png}"
                        text " Inhibition" style "journal_text" yalign 0.5
                    hbox:
                        textbutton "Min" action Call("modify_stat", "inhibition", -100, school) text_style "buttons_idle"
                        null width 20
                        textbutton "10" action Call("modify_stat", "inhibition", -10, school) text_style "buttons_idle"
                        null width 20
                        textbutton "-" action Call("modify_stat", "inhibition", -1, school) text_style "buttons_idle"
                        null width 20
                        button:
                            text "[inhibition]" xalign 0.5 style "journal_text"
                            xsize 100
                        null width 20
                        textbutton "+" action Call("modify_stat", "inhibition", 1, school) text_style "buttons_idle"
                        null width 20
                        textbutton "10" action Call("modify_stat", "inhibition", 10, school) text_style "buttons_idle"
                        null width 20
                        textbutton "Max" action Call("modify_stat", "inhibition", 100, school) text_style "buttons_idle"
                    null height 30
                    # HAPPINESS
                    hbox:
                        text "{image=icons/stat_happiness_icon.png}"
                        text " Happiness" style "journal_text" yalign 0.5
                    hbox:
                        textbutton "Min" action Call("modify_stat", "happiness", -100, school) text_style "buttons_idle"
                        null width 20
                        textbutton "10" action Call("modify_stat", "happiness", -10, school) text_style "buttons_idle"
                        null width 20
                        textbutton "-" action Call("modify_stat", "happiness", -1, school) text_style "buttons_idle"
                        null width 20
                        button:
                            text "[happiness]" xalign 0.5 style "journal_text"
                            xsize 100
                        null width 20
                        textbutton "+" action Call("modify_stat", "happiness", 1, school) text_style "buttons_idle"
                        null width 20
                        textbutton "10" action Call("modify_stat", "happiness", 10, school) text_style "buttons_idle"
                        null width 20
                        textbutton "Max" action Call("modify_stat", "happiness", 100, school) text_style "buttons_idle"
                    null height 30
                    # EDUCATION
                    hbox:
                        text "{image=icons/stat_education_icon.png}"
                        text " Education" style "journal_text" yalign 0.5
                    hbox:
                        textbutton "Min" action Call("modify_stat", "education", -100, school) text_style "buttons_idle"
                        null width 20
                        textbutton "10" action Call("modify_stat", "education", -10, school) text_style "buttons_idle"
                        null width 20
                        textbutton "-" action Call("modify_stat", "education", -1, school) text_style "buttons_idle"
                        null width 20
                        button:
                            text "[education]" xalign 0.5 style "journal_text"
                            xsize 100
                        null width 20
                        textbutton "+" action Call("modify_stat", "education", 1, school) text_style "buttons_idle"
                        null width 20
                        textbutton "10" action Call("modify_stat", "education", 10, school) text_style "buttons_idle"
                        null width 20
                        textbutton "Max" action Call("modify_stat", "education", 100, school) text_style "buttons_idle"
                    null height 30
                    # CHARM
                    hbox:
                        text "{image=icons/stat_charm_icon.png}"
                        text " Charm" style "journal_text" yalign 0.5
                    hbox:
                        textbutton "Min" action Call("modify_stat", "charm", -100, school) text_style "buttons_idle"
                        null width 20
                        textbutton "10" action Call("modify_stat", "charm", -10, school) text_style "buttons_idle"
                        null width 20
                        textbutton "-" action Call("modify_stat", "charm", -1, school) text_style "buttons_idle"
                        null width 20
                        button:
                            text "[charm]" xalign 0.5 style "journal_text"
                            xsize 100
                        null width 20
                        textbutton "+" action Call("modify_stat", "charm", 1, school) text_style "buttons_idle"
                        null width 20
                        textbutton "10" action Call("modify_stat", "charm", 10, school) text_style "buttons_idle"
                        null width 20
                        textbutton "Max" action Call("modify_stat", "charm", 100, school) text_style "buttons_idle"
                    null height 30
                    # REPUTATION
                    hbox:
                        text "{image=icons/stat_reputation_icon.png}"
                        text " Reputation" style "journal_text" yalign 0.5
                    hbox:
                        textbutton "Min" action Call("modify_stat", "reputation", -100, school) text_style "buttons_idle"
                        null width 20
                        textbutton "10" action Call("modify_stat", "reputation", -10, school) text_style "buttons_idle"
                        null width 20
                        textbutton "-" action Call("modify_stat", "reputation", -1, school) text_style "buttons_idle"
                        null width 20
                        button:
                            text "[reputation]" xalign 0.5 style "journal_text"
                            xsize 100
                        null width 20
                        textbutton "+" action Call("modify_stat", "reputation", 1, school) text_style "buttons_idle"
                        null width 20
                        textbutton "10" action Call("modify_stat", "reputation", 10, school) text_style "buttons_idle"
                        null width 20
                        textbutton "Max" action Call("modify_stat", "reputation", 100, school) text_style "buttons_idle"
                    null height 30
                    
            vbar value YScrollValue("CheatStatList"):
                unscrollable "hide"
                xalign 1.0
    elif display.startswith("rules"):
        $ rule_keywords = display.split(":")
        if len(rule_keywords) == 1:
            frame:
                background Solid("#0000")
                area (950, 200, 560, 690)

                viewport id "CheatRuleList":
                    mousewheel True
                    draggable "touch"

                    vbox:
                        text "Unlocking certain rules can lead to unintended behaviour or a broken game save.\nProceed on your own risk.":
                            color "#000000"
                            size 20

                        null height 20

                        for rule_key in rules.keys():
                            $ rule = get_rule(rule_key)
                            $ rule_name = rule.get_title()
                            $ rule_unlock_text = "{color=#ff0000}UNLOCK{/color}"
                            if rule.is_unlocked(school):
                                $ rule_unlock_text = "{color=#00ff00}LOCK{/color}"
                            button:
                                text rule_name:
                                    style "buttons_idle"
                                action Call("open_journal", 5, display + ":" + rule.get_name(), school)
                            hbox:
                                null width 100
                                button:
                                    text rule_unlock_text
                                    action Call("switch_rule", rule.get_name(), school)
                            null height 10
                        

                vbar value YScrollValue("CheatRuleList"):
                    unscrollable "hide"
                    xalign 1.0
        else:
            $ active_rule = get_rule(rule_keywords[1])
            $ active_rule_name = active_rule.get_name()
            $ active_rule_title = active_rule.get_title()
            $ active_rule_desc = active_rule.get_description_str()
            $ active_rule_image = active_rule.get_image(school, active_school.get_level())
            $ active_rule_full_image = active_rule.get_full_image(school, active_school.get_level())

            if active_rule_full_image != None:
                button:
                    xalign 0.63 yalign 0.65
                    image "[active_rule_image]"
                    action Call("call_max_image_from_journal", active_rule_full_image, 5, school, display)
            else:
                image "[active_rule_image]": 
                    xalign 0.629 yalign 0.647
        
            $ active_rule_desc_conditions = active_rule.get_desc_conditions()
        
            text active_rule_title:
                xpos 989
                ypos 200
                size 30
                xmaximum 500
                ymaximum 50
                color "#000"

            frame:
                background Solid("#00000000")
                area (989, 250, 500, 200)
                viewport id "CheatRuleDesc":
                    mousewheel True
                    draggable "touch"

                    vbox:
                        text active_rule_desc style "journal_desc"

                        if len(active_rule_desc_conditions) != 0:
                            null height 40
                            text "{u}To unlock you need:{/u}" style "journal_desc"
                            for condition in active_rule_desc_conditions:
                                $ texts = condition.to_desc_text(school)
                                textbutton texts:
                                    text_style "journal_desc"
                                    yalign 0.5
                                    action NullAction()
                
                vbar value YScrollValue("CheatRuleDesc"):
                    unscrollable "hide"
                    xalign 1.03

            frame:
                background Solid("#0000")
                area (1350, 474, 150, 328)

                viewport id "CheatRuleCond":
                    mousewheel True
                    draggable "touch"

                    vbox:
                        for condition in active_rule.get_list_conditions():
                            if not condition.is_set_blocking():
                                $ texts = condition.to_list_text(school)
                                hbox:
                                    textbutton texts[0]:
                                        tooltip condition.get_name()
                                        action NullAction()
                                    textbutton texts[1]:
                                        text_style "condition_text"
                                        yalign 0.5
                                        tooltip condition.get_name()
                                        action NullAction()
                                    
                vbar value YScrollValue("CheatRuleCond"):
                    unscrollable "hide"
                    xalign 1
                bar value XScrollValue("CheatRuleCond"):
                    unscrollable "hide"
                    ypos 328
            textbutton "Return":
                xalign 0.55 yalign 0.87
                text_style "buttons_idle"
                action Call("open_journal", 5, "rules", school)
    elif display.startswith("clubs"):
        $ club_keywords = display.split(":")
        if len(club_keywords) == 1:
            frame:
                background Solid("#0000")
                area (950, 200, 560, 690)

                viewport id "CheatClubList":
                    mousewheel True
                    draggable "touch"

                    vbox:
                        text "Unlocking certain clubs can lead to unintended behaviour or a broken game save.\nProceed on your own risk.":
                            color "#000000"
                            size 20
                        for club_key in clubs.keys():
                            $ club = get_club(club_key)
                            $ club_name = club.get_title()
                            $ club_unlock_text = "{color=#ff0000}UNLOCK{/color}"
                            if club.is_unlocked(school):
                                $ club_unlock_text = "{color=#00ff00}LOCK{/color}"
                            button:
                                text club_name:
                                    style "buttons_idle"
                                action Call("open_journal", 5, display + ":" + club.get_name(), school)
                            hbox:
                                null width 100
                                button:
                                    text club_unlock_text
                                    action Call("switch_club", club.get_name(), school)
                            null height 10
                        

                vbar value YScrollValue("CheatClubList"):
                    unscrollable "hide"
                    xalign 1.0
        else:
            $ active_club = get_club(club_keywords[1])
            $ active_club_name = active_club.get_name()
            $ active_club_title = active_club.get_title()
            $ active_club_desc = active_club.get_description_str()
            $ active_club_desc_conditions = active_club.get_desc_conditions()
            $ active_club_image = active_club.get_image(school, active_school.get_level())
            $ active_club_full_image = active_club.get_full_image(school, active_school.get_level())

            if active_club_full_image != None:
                button:
                    xalign 0.63 yalign 0.65
                    image "[active_club_image]"
                    action Call("call_max_image_from_journal", active_club_full_image, 5, school, display)
            else:
                image "[active_club_image]": 
                    xalign 0.629 yalign 0.647
            
            text active_club_title:
                xpos 989
                ypos 200
                xmaximum 500
                ymaximum 50
                color "#000"

            frame:
                background Solid("#00000000")
                area (989, 250, 500, 200)
                viewport id "CheatClubDesc":
                    mousewheel True
                    draggable "touch"

                    vbox:
                        text active_club_desc style "journal_desc"

                        if len(active_club_desc_conditions) != 0:
                            null height 40
                            text "{u}To unlock you need:{/u}" style "journal_desc"
                            for condition in active_club_desc_conditions:
                                $ texts = condition.to_desc_text(school)
                                textbutton texts:
                                    text_style "journal_desc"
                                    yalign 0.5
                                    action NullAction()
                
                vbar value YScrollValue("CheatClubDesc"):
                    unscrollable "hide"
                    xalign 1.03

            frame:
                background Solid("#0000")
                area (1350, 474, 150, 328)

                viewport id "CheatClubCond":
                    mousewheel True
                    draggable "touch"

                    vbox:
                        for condition in active_club.get_list_conditions():
                            if not condition.is_set_blocking():
                                $ texts = condition.to_list_text(school)
                                hbox:
                                    textbutton texts[0]:
                                        tooltip condition.get_name()
                                        action NullAction()
                                    textbutton texts[1]:
                                        text_style "condition_text"
                                        yalign 0.5
                                        tooltip condition.get_name()
                                        action NullAction()
                                    
                vbar value YScrollValue("CheatClubCond"):
                    unscrollable "hide"
                    xalign 1
                bar value XScrollValue("CheatClubCond"):
                    unscrollable "hide"
                    ypos 328
            textbutton "Return":
                xalign 0.55 yalign 0.87
                text_style "buttons_idle"
                action Call("open_journal", 5, "clubs", school)
    elif display.startswith("buildings"):
        $ building_keywords = display.split(":")
        if len(building_keywords) == 1:
            frame:
                background Solid("#0000")
                area (950, 200, 560, 690)

                viewport id "CheatBuildingList":
                    mousewheel True
                    draggable "touch"

                    vbox:
                        text "Unlocking certain buildings can lead to unintended behaviour or a broken game save.\nProceed on your own risk.":
                            color "#000000"
                            size 20
                        for building_key in buildings.keys():
                            $ building = get_building(building_key)
                            $ building_name = building.get_title()
                            $ building_level = building.get_level()
                            $ building_unlock_text = "{color=#ff0000}UNLOCK{/color}"
                            if building.is_unlocked():
                                $ building_unlock_text = "{color=#00ff00}LOCK{/color}"
                            button:
                                text building_name:
                                    style "buttons_idle"
                                action Call("open_journal", 5, display + ":" + building.get_name(), school)
                            hbox:
                                null width 100
                                button:
                                    text building_unlock_text
                                    action Call("switch_building", building.get_name(), school, -1000)
                                if building.is_unlocked():
                                    null width 100
                                    button:
                                        text "-":
                                            style "buttons_idle"
                                        action Call("switch_building", building.get_name(), school, -1)
                                    null width 20
                                    button:
                                        text "[building_level]":
                                            style "buttons_idle"
                                        action Null()
                                    null width 10
                                    button:
                                        text "+":
                                            style "buttons_idle"
                                        action Call("switch_building", building.get_name(), school, 1)
                            null height 10
                        

                vbar value YScrollValue("CheatBuildingList"):
                    unscrollable "hide"
                    xalign 1.0
        else:
            $ active_building = get_building(building_keywords[1])
            $ active_building_name = active_building.get_name()
            $ active_building_title = active_building.get_title()
            $ active_building_desc = active_building.get_description_str()
            
            $ active_building_image = active_building.get_image()
            $ active_building_full_image = active_building.get_full_image()

            if active_building_full_image != None:
                button:
                    xalign 0.63 yalign 0.65
                    image "[active_building_image]"
                    action Call("call_max_image_from_journal", active_building_full_image, 4, school, display)
            else:
                image "[active_building_image]": 
                    xalign 0.629 yalign 0.647
        
            $ active_building_desc_conditions = active_building.get_desc_conditions()
        
            text active_building_title:
                xpos 989
                ypos 200
                xmaximum 500
                ymaximum 50
                color "#000"

            frame:
                background Solid("#00000000")
                area (989, 250, 500, 200)
                viewport id "CheatBuildingDesc":
                    mousewheel True
                    draggable "touch"

                    vbox:
                        text active_building_desc style "journal_desc"

                        if len(active_building_desc_conditions) != 0:
                            null height 40
                            text "{u}To unlock you need:{/u}" style "journal_desc"
                            for condition in active_building_desc_conditions:
                                $ texts = condition.to_desc_text(school)
                                textbutton texts:
                                    text_style "journal_desc"
                                    yalign 0.5
                                    action NullAction()
                
                vbar value YScrollValue("CheatBuildingDesc"):
                    unscrollable "hide"
                    xalign 1.03

            frame:
                background Solid("#0000")
                area (1350, 474, 150, 328)

                viewport id "CheatBuildingCond":
                    mousewheel True
                    draggable "touch"

                    vbox:
                        for condition in active_building.get_list_conditions():
                            if not condition.is_set_blocking():
                                $ texts = condition.to_list_text(school)
                                hbox:
                                    textbutton texts[0]:
                                        tooltip condition.get_name()
                                        action NullAction()
                                    textbutton texts[1]:
                                        text_style "condition_text"
                                        yalign 0.5
                                        tooltip condition.get_name()
                                        action NullAction()
                                    
                vbar value YScrollValue("CheatBuildingCond"):
                    unscrollable "hide"
                    xalign 1
                bar value XScrollValue("CheatBuildingCond"):
                    unscrollable "hide"
                    ypos 328
            textbutton "Return":
                xalign 0.55 yalign 0.87
                text_style "buttons_idle"
                action Call("open_journal", 5, "buildings", school)

    text "Cheats": 
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


screen max_image_from_journal(image_path):
    tag interaction_overlay
    modal True
    image "[image_path]"
    button:
        xpos 0 ypos 0
        xsize 1902 ysize 1080
        action Call("open_journal", journal, display, school)

label set_journal_setting(page, display, school, setting, value):
    $ set_game_data("journal_setting_" + str(page) + "_" + setting, value)
    call open_journal(page, display, school) from set_journal_setting_1

label call_max_image_from_journal(image_path, journal, school, display):
    hide screen school_overview_buttons
    call screen max_image_from_journal(image_path)

label switch_rule(rule_name, school):
    $ rule = get_rule(rule_name)
    $ rule.unlock(school, not rule.is_unlocked(school))
    call screen journal_5("rules", school)

label switch_club(club_name, school):
    $ club = get_club(club_name)
    $ club.unlock(school, not club.is_unlocked(school))
    call screen journal_5("clubs", school)

label switch_building(building_name, school, level_delta):
    $ building = get_building(building_name)

    if level_delta == -1000:
        $ building.unlock(not building.is_unlocked())
    else:
        $ building.set_level(building.get_level() + level_delta)
    call screen journal_5("buildings", school)

label modify_stat(stat, amount, school):
    if stat == "money":
        $ money.change_value(amount)
    elif stat == "level":
        $ school_obj = get_character(school, charList["schools"])
        $ school_obj.set_level(school_obj.get_level() + amount)
    else:
        $ get_character(school, charList["schools"]).change_stat(stat, amount)
    call screen journal_5("stats", school)

label add_to_proposal(data, page, school, display, propType):
    $ set_game_data("voteProposal", [propType, display, school, data])
    call open_journal(page, display, school) from add_to_proposal_1

label add_rule_to_proposal(rule_name, school):
    $ rule = get_rule(rule_name)
    $ voteProposal = get_game_data("voteProposal")
    if voteProposal != None:
        $ title = "the " + voteProposal[3].get_type() + " \"" + voteProposal[3].get_title() + "\""
        $ rule_title = rule.get_title()
        if rule == None:
            return
        call screen confirm("You already queued [title] for voting.\n\nDo you wanna queue the rule \"[rule_title]\" instead?",
            Call("add_to_proposal", rule, 2, school, rule_name, "rule"),
            Call("open_journal", 2, rule_name, school))

    call add_to_proposal(rule, 2, school, rule_name, "rule") from add_rule_to_proposal_2

label add_club_to_proposal(club_name, school):
    $ club = get_club(club_name)
    $ voteProposal = get_game_data("voteProposal")
    if voteProposal != None:
        $ title = "the " + voteProposal[3].get_type() + " \"" + voteProposal[3].get_title() + "\""
        $ club_title = club.get_title()
        if club == None:
            return
        call screen confirm("You already queued [title] for voting.\n\nDo you wanna queue the club \"[club_title]\" instead?",
            Call("add_to_proposal", club, 3, school, club_name, "club"),
            Call("open_journal", 3, club_name, school))

    call add_to_proposal(club, 3, school, club_name, "club") from add_club_to_proposal_2

label add_building_to_proposal(building_name, school):
    $ building = get_building(building_name)
    $ voteProposal = get_game_data("voteProposal")
    if voteProposal != None:
        $ title = "the " + voteProposal[3].get_type() + " \"" + voteProposal[3].get_title() + "\""
        $ building_title = building.get_title()
        if building == None:
            return
        call screen confirm("You already queued [title] for voting.\n\nDo you wanna queue the building \"[building_title]\" instead?",
            Call("add_to_proposal", building, 4, school, building_name, "building"),
            Call("open_journal", 4, building_name, school))

    call add_to_proposal(building, 4, school, building_name, "building") from add_building_to_proposal_2