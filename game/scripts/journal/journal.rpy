init python:
    def get_journal_type(page: int) -> str:
        page -= 1
        types = ["overview", "rules", "clubs", "buildings", "cheats", "credits"]
        if page < 0 or page > 4:
            return ""
        return types[page]
    def get_obj_type(page: int) -> str:
        page -= 2
        types = ["rule", "club", "building"]
        if page < 0 or page > 2:
            return ""
        return types[page]
    def get_journal_map(page: int) -> Dict[str, Journal_Obj]:
        page -= 2
        types = [rules, clubs, buildings]
        if page < 0 or page > 2:
            return []
        return types[page]

############################
# Journal Intro
############################

label start_journal ():
    call open_journal (1, "") from start_journal_1

label open_journal(page, display):
    if page == 1:
        call screen journal_overview(display) with dissolveM
    elif page == 2:
        call screen journal_page(2, display) with dissolveM
    elif page == 3:
        call screen journal_page(3, display) with dissolveM
    elif page == 4:
        call screen journal_page(4, display) with dissolveM
    elif page == 5:
        call screen journal_cheats(display) with dissolveM
    elif page == 6:
        call screen journal_credits(display) with dissolveM

label close_journal ():
    hide screen journal
    jump map_overview

############################
# Journal Styles
############################

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

style journal_pta_overview take buttons_idle:
    size 25

############################
# Journal Sub-screens
############################

screen journal_obj_list(page, display, journal_map):
    $ journal_type = get_obj_type(page)
    $ locked_list = get_visible_locked_objs_by_school(journal_map)
    $ unlocked_list = get_visible_unlocked_objs_by_school(journal_map)
    $ obj_list = locked_list + unlocked_list
    $ adj = ui.adjustment()

    python:
        adj.value = 0

        if display in obj_list:
            current_selected = obj_list.index(display)
            adj.range = len(obj_list)
            adj.value = (current_selected - 5) * len(obj_list) * 2.5

    frame:
        # background Solid("#00000090")
        background Solid("#00000000")
        area (330, 300, 560, 600)

        viewport id "[journal_type]List": 
            yadjustment adj
            mousewheel True
            draggable "touch"

            vbox:
                
                $ journal_settings = get_game_data("journal_setting_" + str(page) + "_locked " + journal_type)
                use journal_foldable_list((journal_settings == None or journal_settings), "locked " + journal_type, page, display, locked_list)
                
                null height 20

                $ journal_settings = get_game_data("journal_setting_" + str(page) + "_unlocked " + journal_type)
                use journal_foldable_list((journal_settings == None or journal_settings), "unlocked " + journal_type, page, display, unlocked_list, "buttons_active")

        vbar value YScrollValue("[journal_type]List"):
            unscrollable "hide"
            xalign 1.0

screen journal_foldable_list(is_showing, text, page, display, obj_list, default_style = "buttons_idle"):
    $ journal_map = get_journal_map(page)
    if is_showing:
        textbutton "hide [text]":
            text_style "buttons_idle"
            yalign 0.5
            action [With(dissolveM), Call("set_journal_setting", page, display, text, False)]
        image "journal/journal/left_list_separator.webp"
        for obj_name in obj_list:
            $ obj = get_journal_obj(journal_map, obj_name)
            if obj is not None:
                $ obj_title = obj.get_title()
                $ button_style = default_style
                if obj_name == display:
                    $ button_style = "buttons_selected"
                textbutton obj_title:
                    text_style button_style
                    action [With(dissolveM), Call("open_journal", page, obj_name)]
    else:
        textbutton "show [text]":
            text_style "buttons_inactive"
            yalign 0.5
            action [With(dissolveM), Call("set_journal_setting", page, display, text, True)]
        image "journal/journal/left_list_separator.webp"

screen journal_simple_list(page, display, display_list, default_style = "buttons_idle"):
    frame:
        background Solid("#0000")
        area (330, 300, 560, 600)

        viewport id "SimpleList":
            mousewheel True
            draggable "touch"

            vbox:
                for elem in display_list.keys():
                    $ elem_image = None
                    $ elem_text = display_list[elem]
                    if isinstance(elem_text, list):
                        $ elem_image = elem_text[1]
                        $ elem_text = elem_text[0]
                    $ button_style = default_style
                    if elem == display:
                        $ button_style = "buttons_selected"
                    textbutton elem_text:
                        text_style button_style
                        action [With(dissolveM), Call("open_journal", page, elem)]
                

        vbar value YScrollValue("SimpleList"):
            unscrollable "hide"
            xalign 1.0

screen journal_page_selector(page, display):
    imagemap:
        idle "journal/journal/[page]_idle.webp"
        hover "journal/journal/[page]_hover.webp"

        if page != 1:
            hotspot (144, 250, 168, 88) action [With(dissolveM), Call("open_journal", 1, "")] tooltip "School Overview"
        if page < 2:
            hotspot (1522, 617, 168, 88) action [With(dissolveM), Call("open_journal", 2, "")] tooltip "Rules"
        if page > 2:
            hotspot (144, 617, 168, 88) action  [With(dissolveM), Call("open_journal", 2, "")] tooltip "Rules"
        if page < 3:
            hotspot (1522, 722, 168, 88) action [With(dissolveM), Call("open_journal", 3, "")] tooltip "Clubs"
        if page > 3:
            hotspot (144, 722, 168, 88) action [With(dissolveM), Call("open_journal", 3, "")] tooltip "Clubs"
        if page < 4:
            hotspot (1522, 830, 168, 88) action [With(dissolveM), Call("open_journal", 4, "")] tooltip "Buildings"
        if page > 4:
            hotspot (144, 830, 168, 88) action [With(dissolveM), Call("open_journal", 4, "")] tooltip "Buildings"

    if cheat_mode and page != 5:
        imagebutton:
            idle "journal/journal/cheat_tag_idle.webp"
            hover "journal/journal/cheat_tag_hover.webp"
            tooltip "Cheats"
            xpos 1268
            ypos 70
            action [With(dissolveM), Call("open_journal", 5, "", school)]

    if page != 6:
        imagebutton:
            idle "journal/journal/credit_tag_idle.webp"
            hover "journal/journal/credit_tag_hover.webp"
            tooltip "Credits"
            xpos 338
            ypos 953
            action [With(dissolveM), Call("open_journal", 6, "", school)]
    
screen journal_desc(page, display, active_obj):
    $ active_obj_desc = active_obj.get_description_str()

    $ action_text = "unlock"
    if active_obj.get_type() == "building" and active_obj.is_unlocked()  and active_obj.has_higher_level():
        $ action_text = "upgrade"

    $ active_obj_desc_conditions_desc = active_obj.get_desc_conditions_desc(cond_type = action_text, char_obj = get_school(), blocking = True)
        
    frame:
        background Solid("#0000")
        area (989, 200, 500, 250)
        viewport id "RuleDesc":
            mousewheel True
            draggable "touch"

            vbox:
                text active_obj_desc style "journal_desc"

                if len(active_obj_desc_conditions_desc) != 0:
                    null height 40
                    text "{u}To unlock you need:{/u}" style "journal_desc"
                    for desc in active_obj_desc_conditions_desc:
                        textbutton desc:
                            text_style "journal_desc"
                            yalign 0.5
                            action NullAction()
    
        vbar value YScrollValue("RuleDesc"):
            unscrollable "hide"
            xalign 1.03

screen journal_list_conditions(page, active_obj):
    $ action_text = "unlock"
    if active_obj.get_type() == "building" and active_obj.is_unlocked() and active_obj.has_higher_level():
        $ action_text = "upgrade"

    $ active_obj_list_conditions_list = active_obj.get_list_conditions_list(cond_type = action_text, char_obj = get_school(), blocking = True)

    frame:
        background Solid("#0000")
        area (1350, 474, 150, 328)

        viewport id "ObjCond":
            mousewheel True
            draggable "touch"

            vbox:
                for (image_text, text_text, text_title) in active_obj_list_conditions_list:
                    hbox:
                        textbutton image_text:
                            tooltip text_title
                            action NullAction()
                        textbutton text_text:
                            text_style "condition_text"
                            yalign 0.5
                            tooltip text_title
                            action NullAction()
                            
        vbar value YScrollValue("ObjCond"):
            unscrollable "hide"
            xalign 1
        bar value XScrollValue("ObjCond"):
            unscrollable "hide"
            ypos 328

screen journal_vote_button(page, display, active_obj):
    $ obj_type = get_obj_type(page)
    if (not active_obj.is_unlocked() or 
        (obj_type == 'building' and active_obj.can_be_upgraded())
    ):
        $ voteProposal = get_game_data("voteProposal")
        if voteProposal == None or voteProposal._journal_obj.get_name() != display:
            $ condition_storage = active_obj.get_condition_storage()
            $ action_text = "unlock"
            $ probability = 0
            if obj_type == 'building' and active_obj.can_be_upgraded():
                $ condition_storage = active_obj.get_update_conditions(active_obj.get_level())
                $ action_text = "upgrade"
            if obj_type == 'building':
                $ probability = calculateProbabilitySum(condition_storage)
            else:
                $ probability = calculateProbabilitySum(
                    condition_storage, 
                    get_character("teacher", charList["staff"]),
                    get_school(),
                    get_character("parents", charList)
                )
            $ locked_text = ""
            $ probability_text = str(clamp_value(round(probability, 2))) + "%"
            if condition_storage.get_is_locked():
                $ probability_text = "Locked"
            if probability > 0:
                textbutton "Vote for [action_text] ([probability_text])":
                    xpos 985 yalign 0.83
                    text_style "buttons_idle"
                    action Call("add_" + obj_type + "_to_proposal", display)
            else:
                textbutton "Vote for [action_text] ([probability_text])":
                    xpos 985 yalign 0.83
                    text_style "buttons_inactive"
        else:
            text "Already scheduled!":
                xpos 985 yalign 0.83
                color "#f00"
    else:
        text "Already unlocked!":
            xpos 985 yalign 0.83
            color "#008800"
            size 30

screen journal_image(page, display, active_obj):
    $ active_obj_image = active_obj.get_image()
    $ active_obj_full_image = active_obj.get_full_image()

    if active_obj_full_image != None:
        button:
            xpos 985 yalign 0.65
            image "[active_obj_image]"
            action [With(dissolveM), Call("call_max_image_from_journal", active_obj_full_image, page, display)]
    else:
        image "[active_obj_image]": 
            xpos 985 yalign 0.65

screen journal_cheats_stat(stat):
    $ stat_name = str(stat)
    $ stat_text = stat_name.capitalize()
    $ stat_value = 0

    if stat == MONEY:
        $ stat_value = money.get_display_value()
    elif stat == LEVEL:
        $ stat_value = get_level_from_char(get_school())
    else:
        $ stat_value = get_school().get_display_value(stat)

    hbox:
        text "{image=icons/stat_[stat_name]_icon.webp}"
        text " [stat_text]" style "journal_text" yalign 0.5
    hbox:
        if stat != MONEY:
            textbutton "Min" action Call("modify_stat", stat, -100) text_style "buttons_idle"
            null width 20

        if stat == MONEY:
            textbutton "1000" action Call("modify_stat", stat, -1000) text_style "buttons_idle"
            null width 30
        elif stat == LEVEL:
            textbutton "5" action Call("modify_stat", stat, -5) text_style "buttons_idle"
            null width 40
        else:
            textbutton "10" action Call("modify_stat", stat, -10) text_style "buttons_idle"
            null width 20

        if stat == MONEY:
            textbutton "-" action Call("modify_stat", stat, -100) text_style "buttons_idle"
            null width 65
        else:
            textbutton "-" action Call("modify_stat", stat, -1) text_style "buttons_idle"
            null width 15

        button:
            text "[stat_value]" xalign 0.5 style "journal_text"
            xsize 100

        if stat == MONEY:
            null width 65
            textbutton "+" action Call("modify_stat", stat, 100) text_style "buttons_idle"
        else:
            null width 15
            textbutton "+" action Call("modify_stat", stat, 1) text_style "buttons_idle"

        if stat == MONEY:
            null width 30
            textbutton "1000" action Call("modify_stat", stat, 1000) text_style "buttons_idle"
        elif stat == LEVEL:
            null width 40
            textbutton "5" action Call("modify_stat", stat, 5) text_style "buttons_idle"
        else:
            null width 20
            textbutton "10" action Call("modify_stat", stat, 10) text_style "buttons_idle"

        if stat != MONEY:
            null width 30
            textbutton "Max" action Call("modify_stat", stat, 100) text_style "buttons_idle"
    null height 30

screen max_image_from_journal(image_path):
    tag interaction_overlay
    modal True
    image "[image_path]"
    button:
        xpos 0 ypos 0
        xsize 1902 ysize 1080
        action [With(dissolveM), Call("open_journal", journal, display)]

############################
# Main Journals
############################

# Object Pages
screen journal_page(page, display):
    tag interaction_overlay
    modal True
    
    use school_overview_map
    use school_overview_stats

    key "K_ESCAPE" action [With(dissolveM), Jump("map_overview")]

    use journal_page_selector(page, display)

    $ page_title = get_obj_type(page).capitalize()

    text page_title: 
        xalign 0.25 
        yalign 0.2
        size 60
        color "#000"

    $ journal_type = get_journal_type(page)
    $ journal_map = get_journal_map(page)
    $ active_obj = get_journal_obj(journal_map, display)

    use journal_obj_list(page, display, journal_map)

    if display != "" and not active_obj.is_visible):
        $ display = ""

    if display != "":
        use journal_image(page, display, active_obj)

        use journal_desc(page, display, active_obj)

        use journal_list_conditions(page, active_obj)

        use journal_vote_button(page, display, active_obj)

    textbutton "Close":
        xalign 0.75
        yalign 0.87
        action [With(dissolveM), Jump("map_overview")]

    $ tooltip = GetTooltip()
    if tooltip:
        nearrect:
            focus "tooltip"
            prefer_top True

            frame:
                xalign 0.5
                text tooltip

# School Overview
screen journal_overview(display):
    tag interaction_overlay
    modal True

    use school_overview_map
    use school_overview_stats

    key "K_ESCAPE" action [With(dissolveM), Jump("map_overview")]

    use journal_page_selector(1, display)

    text "School Overview": 
        xalign 0.25 
        yalign 0.2
        size 60
        color "#000"

    $ school_object = get_school()
    $ school_stats = school_object.get_stats()

    $ pta_proposal = get_game_data('voteProposal')

    frame:
        # background Solid("#00000090")
        background Solid("#00000000")
        area (350, 300, 500, 650)

        viewport id "Overview":
            mousewheel True
            draggable "touch"

            vbox:
                if pta_proposal != None:
                    $ pta_type = pta_proposal._journal_obj.get_type().capitalize()
                    text "[pta_type] scheduled for pta-meeting:" style "journal_text" size 27
                    $ pta_title = "\"" + pta_proposal._journal_obj.get_title() + "\""
                    $ pta_name = pta_proposal._journal_obj.get_name()
                    $ pta_page = 2
                    if pta_type == "Club":
                        $ pta_page = 3
                    elif pta_type == "Building":
                        $ pta_page = 4
                    textbutton "[pta_title]":
                        text_style "journal_pta_overview"
                        action [With(dissolveM), Call("open_journal", pta_page, pta_name)]

                    null height 20

                hbox:
                    $ button_style = "buttons_idle"
                    if "money" == display:
                        $ button_style = "buttons_selected"
                    $ money_text = money.display_stat()

                    text "{image=icons/stat_money_icon.webp}"
                    textbutton "  Money:":
                        yalign 0.5 
                        text_style button_style
                        action [With(dissolveM), Call("open_journal", 1, "money")]
                    text "[money_text]" style "journal_text" yalign 0.5

                null height 20

                text "[school_object.title]" style "journal_text" size 40

                null height 20

                hbox:
                    $ button_style = "buttons_idle"
                    if "level" == display:
                        $ button_style = "buttons_selected"
                    $ level_text = school_object.level.display_stat()

                    text "{image=icons/stat_level_icon.webp}"
                    textbutton "  Level:":
                        yalign 0.5 
                        text_style button_style
                        action [With(dissolveM), Call("open_journal", 1, "level")]
                    text "[level_text]" style "journal_text" yalign 0.5

                null height 20

                for stat_key in school_stats.keys():
                    $ stat_obj = school_object.get_stat_obj(stat_key)
                    $ stat_icon = stat_obj.image_path
                    $ stat_value = stat_obj.display_stat()
                    $ stat_title = Stat_Data[stat_obj.get_name()].get_title()
                    $ button_style = "buttons_idle"
                    if stat_key == display:
                        $ button_style = "buttons_selected"
                    hbox:
                        text "{image=[stat_icon]}"
                        textbutton "  [stat_title]:":
                            yalign 0.5 
                            text_style button_style
                            action [With(dissolveM), Call("open_journal", 1, stat_obj.get_name())]
                        text " [stat_value]" style "journal_text" yalign 0.5

        vbar value YScrollValue("Overview"):
            unscrollable "hide"
            xalign 1.0

    if display != "":
        $ active_stat_obj = None
        if school_object.check_stat_exists(display):
            $ active_stat_obj = school_object.get_stat_obj(display)
        if display == "money":
            $ active_stat_obj = money
        if display == "level":
            $ active_stat_obj = school_object.get_level()

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
        action [With(dissolveM), Jump("map_overview")]

    $ tooltip = GetTooltip()
    if tooltip:
        nearrect:
            focus "tooltip"
            prefer_top True

            frame:
                xalign 0.5
                text tooltip

# Cheats
screen journal_cheats(display):
    tag interaction_overlay
    modal True

    use school_overview_map
    use school_overview_stats

    key "K_ESCAPE" action [With(dissolveM), Jump("map_overview")]

    use journal_page_selector(5, display)

    text "Cheats":
        xalign 0.72 yalign 0.11
        size 20
        color "#000"

    $ options = {
        "general": "General",
        "stats": "Stats",
        "rules": "Rules",
        "clubs": "Clubs",
        "buildings": "Buildings",
    }

    if display == "":
        $ display = "general"

    use journal_simple_list(5, display, options)

    $ active_school = get_school()

    if display == "general":
        frame:
            background Solid("#0000")
            area (950, 200, 560, 690)

            viewport id "CheatStatList":
                mousewheel True
                draggable "touch"
                vbox:
                    text "Changing game values can lead to unintended behaviour or a broken game save.\nProceed on your own risk.":
                        color "#000000"
                        size 20

                    null height 20

                    # TIME
                    hbox:
                        button:
                            text "Time" xalign 0.0 style "journal_text"
                            xsize 250

                        $ time_freeze_text = "{color=#00ff00}FREEZE{/color}"
                        if time_freeze:
                            $ time_freeze_text = "{color=#ff0000}UNFREEZE{/color}"
                        button:
                            text time_freeze_text xalign 1.0
                            action [With(dissolveM), Call("switch_time_freeze", 5, display)]
                            xsize 250
                    null height 10
                    text "Set daytime to:" style "journal_text" size 20
                    hbox:
                        button:
                            text "Morning" style "buttons_idle"
                            action Call("set_time_cheat", 5, display, daytime = 1)
                        text "    " style "journal_text"
                        button:
                            text "Early Noon" style "buttons_idle"
                            action Call("set_time_cheat", 5, display, daytime = 2)
                        text "    " style "journal_text"
                        button:
                            text "Noon" style "buttons_idle"
                            action Call("set_time_cheat", 5, display, daytime = 3)
                    hbox:
                        button:
                            text "Early Afternoon" style "buttons_idle"
                            action Call("set_time_cheat", 5, display, daytime = 4)
                        text "    " style "journal_text"
                        button:
                            text "Afternoon" style "buttons_idle"
                            action Call("set_time_cheat", 5, display, daytime = 5)
                    hbox:
                        button:
                            text "Evening" style "buttons_idle"
                            action Call("set_time_cheat", 5, display, daytime = 6)
                        text "    " style "journal_text"
                        button:
                            text "Night" style "buttons_idle"
                            action Call("set_time_cheat", 5, display, daytime = 7)
                    null height 10
                    text "Left-click to fast forward; Right click to rewind" style "journal_text" size 20
                    hbox:
                        $ day = time.day
                        $ month = time.get_month_name()
                        $ year = time.year
                        button:
                            text "[day]" style "buttons_idle"
                            action Call("change_time_cheat", 5, display, day = 1)
                            alternate Call("change_time_cheat", 5, display, day = -1)
                        text "    " style "journal_text"
                        button:
                            text "[month]" style "buttons_idle"
                            action Call("change_time_cheat", 5, display, month = 1)
                            alternate Call("change_time_cheat", 5, display, month = -1)
                        text "    " style "journal_text"
                        button:
                            text "[year]" style "buttons_idle"
                            action Call("change_time_cheat", 5, display, year = 1)
                            alternate Call("change_time_cheat", 5, display, year = -1)
                
                    
            vbar value YScrollValue("CheatStatList"):
                unscrollable "hide"
                xalign 1.0
    elif display == "stats":
        frame:
            background Solid("#0000")
            area (950, 200, 560, 690)

            viewport id "CheatStatList":
                mousewheel True
                draggable "touch"
                vbox:
                    text "Changing stats can lead to unintended behaviour or a broken game save.\nProceed on your own risk.":
                        color "#000000"
                        size 20
                    # MONEY
                    use journal_cheats_stat(MONEY)
                    # LEVEL
                    use journal_cheats_stat(LEVEL)
                    # CORRUPTION
                    use journal_cheats_stat(CORRUPTION)
                    # INHIBITION
                    use journal_cheats_stat(INHIBITION)
                    # HAPPINESS
                    use journal_cheats_stat(HAPPINESS)
                    # EDUCATION
                    use journal_cheats_stat(EDUCATION)
                    # CHARM
                    use journal_cheats_stat(CHARM)
                    # REPUTATION
                    use journal_cheats_stat(REPUTATION)
                    
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
                            if rule.is_unlocked():
                                $ rule_unlock_text = "{color=#00ff00}LOCK{/color}"
                            button:
                                text rule_name:
                                    style "buttons_idle"
                                action [With(dissolveM), Call("open_journal", 5, display + ":" + rule.get_name())]
                            hbox:
                                null width 100
                                button:
                                    text rule_unlock_text
                                    action [With(dissolveM), Call("switch_rule", rule.get_name())]
                            null height 10
                        

                vbar value YScrollValue("CheatRuleList"):
                    unscrollable "hide"
                    xalign 1.0
        else:
            $ active_rule = get_rule(rule_keywords[1])
            $ active_rule_name = active_rule.get_name()
            $ active_rule_title = active_rule.get_title()
            $ active_rule_desc = active_rule.get_description_str()
            $ active_rule_image = active_rule.get_image()
            $ active_rule_full_image = active_rule.get_full_image()

            if active_rule_full_image != None:
                button:
                    xalign 0.63 yalign 0.65
                    image "[active_rule_image]"
                    action [With(dissolveM), Call("call_max_image_from_journal", active_rule_full_image, 5, display)]
            else:
                image "[active_rule_image]": 
                    xalign 0.629 yalign 0.647
        
            $ active_rule_desc_conditions_desc = active_rule.get_desc_conditions_desc(char_obj = get_school())
        
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

                        if len(active_rule_desc_conditions_desc) != 0:
                            null height 40
                            text "{u}To unlock you need:{/u}" style "journal_desc"
                            for desc in active_rule_desc_conditions_desc:
                                textbutton desc:
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
                                $ texts = condition.to_list_text(char_obj = get_school())
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
                action [With(dissolveM), Call("open_journal", 5, "rules")]
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
                            if club.is_unlocked():
                                $ club_unlock_text = "{color=#00ff00}LOCK{/color}"
                            button:
                                text club_name:
                                    style "buttons_idle"
                                action [With(dissolveM), Call("open_journal", 5, display + ":" + club.get_name())]
                            hbox:
                                null width 100
                                button:
                                    text club_unlock_text
                                    action [With(dissolveM), Call("switch_club", club.get_name())]
                            null height 10
                        

                vbar value YScrollValue("CheatClubList"):
                    unscrollable "hide"
                    xalign 1.0
        else:
            $ active_club = get_club(club_keywords[1])
            $ active_club_name = active_club.get_name()
            $ active_club_title = active_club.get_title()
            $ active_club_desc = active_club.get_description_str()
            $ active_club_desc_conditions_desc = active_club.get_desc_conditions_desc(char_obj = get_school())
            $ active_club_image = active_club.get_image()
            $ active_club_full_image = active_club.get_full_image()

            if active_club_full_image != None:
                button:
                    xalign 0.63 yalign 0.65
                    image "[active_club_image]"
                    action [With(dissolveM), Call("call_max_image_from_journal", active_club_full_image, 5, display)]
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

                        if len(active_club_desc_conditions_desc) != 0:
                            null height 40
                            text "{u}To unlock you need:{/u}" style "journal_desc"
                            for desc in active_club_desc_conditions_desc:
                                textbutton desc:
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
                                $ texts = condition.to_list_text(char_obj = get_school())
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
                action [With(dissolveM), Call("open_journal", 5, "clubs")]
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
                            if building.is_unlocked("x"):
                                $ building_unlock_text = "{color=#00ff00}LOCK{/color}"
                            button:
                                text building_name:
                                    style "buttons_idle"
                                action [With(dissolveM), Call("open_journal", 5, display + ":" + building.get_name())]
                            hbox:
                                null width 100
                                button:
                                    text building_unlock_text
                                    action [With(dissolveM), Call("switch_building", building.get_name(), -1000)]
                                if building.is_unlocked("x"):
                                    null width 100
                                    button:
                                        text "-":
                                            style "buttons_idle"
                                        action [With(dissolveM), Call("switch_building", building.get_name(), -1)]
                                    null width 20
                                    button:
                                        text "[building_level]":
                                            style "buttons_idle"
                                        action Null()
                                    null width 10
                                    button:
                                        text "+":
                                            style "buttons_idle"
                                        action [With(dissolveM), Call("switch_building", building.get_name(), 1)]
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
                    action Call("call_max_image_from_journal", active_building_full_image, 4, display)
            else:
                image "[active_building_image]": 
                    xalign 0.629 yalign 0.647
        
            $ active_building_desc_conditions_desc = active_building.get_desc_conditions_desc(char_obj = get_school())
        
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

                        if len(active_building_desc_conditions_desc) != 0:
                            null height 40
                            text "{u}To unlock you need:{/u}" style "journal_desc"
                            for desc in active_building_desc_conditions_desc:
                                textbutton desc:
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
                                $ texts = condition.to_list_text(char_obj = get_school())
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
                action [With(dissolveM), Call("open_journal", 5, "buildings")]

    text "Cheats": 
        xalign 0.25 
        yalign 0.2
        size 60
        color "#000"

    textbutton "Close":
        xalign 0.75
        yalign 0.87
        action [With(dissolveM), Jump("map_overview")]

    $ tooltip = GetTooltip()
    if tooltip:
        nearrect:
            focus "tooltip"
            prefer_top True

            frame:
                xalign 0.5
                text tooltip

screen journal_credits(display):
    tag interaction_overlay
    modal True

    use school_overview_map
    use school_overview_stats

    key "K_ESCAPE" action [With(dissolveM), Jump("map_overview")]

    use journal_page_selector(6, display)

    text "Credits":
        xalign 0.21 yalign 0.95
        size 20
        color "#000"

    $ student_members = get_members("Student")
    $ teacher_members = get_members("Teacher")

    # left side
    frame:
        # background Solid("#00000090")
        background Solid("#00000000")
        area (350, 200, 500, 750)

        vbox:
            text "Thanks to all patrons!":
                    size 40
                    color "#000000"
            null height 20
            hbox:
                viewport id "credits teachers list":
                    mousewheel True
                    draggable "touch"

                    vbox:
                        text "Teacher Tier ($5)":
                            size 35
                            color "#491616"

                        null height 20

                        for member in teacher_members:
                            $ data = member.split(',')
                            if data[0] == '*blacklisted*':
                                text "{i}Anonymous{/i}":
                                    color "#00000060"
                                    size 25
                            elif data[0].startswith('*alias*'):
                                $ alias = data[0][7:]
                                text "{i}[alias]{/i}":
                                    color "#000000"
                                    size 25
                            else:
                                text "[data[0]]":
                                    color "#000000"
                                    size 25
                        
                vbar value YScrollValue("credits teachers list"):
                    unscrollable "hide"
                    xalign 1.0

    # right side
    frame:
        # background Solid("#00000090")
        background Solid("#00000000")
        area (960, 200, 500, 700)

        vbox:
            text "Consider supporting the game:":
                    size 30
                    color "#000000"
            imagebutton:
                idle "journal/journal/patreon banner idle.webp"
                hover "journal/journal/patreon banner hover.webp"
                action Call("open_patreon_link", school)
            null height 20
            hbox:
                viewport id "credits students list":
                    mousewheel True
                    draggable "touch"

                    vbox:
                        text "Student Tier ($1)":
                            size 35
                            color "#16491c"

                        null height 20

                        for member in student_members:
                            $ data = member.split(',')
                            if data[0] == '*blacklisted*':
                                text "{i}Anonymous{/i}":
                                    color "#00000060"
                                    size 25
                            elif data[0].startswith('*alias*'):
                                $ alias = data[0][7:]
                                text "{i}[alias]{/i}":
                                    color "#000000"
                                    size 25
                            else:
                                text "[data[0]]":
                                    color "#000000"
                                    size 25
                        
                vbar value YScrollValue("credits students list"):
                    unscrollable "hide"
                    xalign 1.0

    textbutton "Close":
        xalign 0.75
        yalign 0.87
        action [With(dissolveM), Jump("map_overview")]

    $ tooltip = GetTooltip()
    if tooltip:
        nearrect:
            focus "tooltip"
            prefer_top True

            frame:
                xalign 0.5
                text tooltip

############################
# Journal Methods
############################

label set_time_cheat(page, display, **kwargs):
    $ time.set_time(**kwargs)

    call open_journal(page, display) from set_time_cheat_1

label change_time_cheat(page, display, **kwargs):
    $ time.add_time(**kwargs)

    call open_journal(page, display) from change_time_cheat_1

label switch_time_freeze(page, display, value = None):
    if time_freeze == None:
        $ time_freeze = True
    elif value == None:
        $ time_freeze = value
    else:
        $ time_freeze = not time_freeze
    call open_journal(page, display) from switch_time_freeze_1

label open_patreon_link():
    $ renpy.run(OpenURL(patreon))
    call open_journal(6, "") from open_patreon_link_1

label set_journal_setting(page, display, setting, value):
    $ set_game_data("journal_setting_" + str(page) + "_" + setting, value)
    call open_journal(page, display) from set_journal_setting_1

label call_max_image_from_journal(image_path, journal, display):
    hide screen school_overview_buttons
    call screen max_image_from_journal(image_path) with dissolveM

label switch_rule(rule_name):
    $ rule = get_rule(rule_name)
    $ rule.unlock(not rule.is_unlocked())
    call open_journal(5, "rules") from switch_rule_1

label switch_club(club_name):
    $ club = get_club(club_name)
    $ club.unlock(not club.is_unlocked())
    call open_journal(5, "clubs") from switch_club_1

label switch_building(building_name, level_delta):
    $ building = get_building(building_name)

    if level_delta == -1000:
        $ building.unlock(not building.is_unlocked("x"))
    else:
        $ building.set_level(building.get_level() + level_delta)
    call open_journal(5, "buildings") from switch_building_1

label modify_stat(stat, amount):
    $ school_obj = get_school()
    if stat == "money":
        $ money.change_value(amount)
    elif stat == "level":
        $ school_obj.set_level(school_obj.get_level() + amount)
    else:
        $ school_obj.change_stat(stat, amount)
    call open_journal(5, "stats") from modify_stat_1

label add_to_proposal(data, page, display, action = "unlock"):
    $ proposal = PTAProposal(data, display)
    $ set_game_data("voteProposal", proposal)
    call open_journal(page, display) from add_to_proposal_1

label add_rule_to_proposal(rule_name):
    $ rule = get_rule(rule_name)
    $ voteProposal = get_game_data("voteProposal")
    if voteProposal != None:
        $ title = "the " + voteProposal._journal_obj.get_type() + " \"" + voteProposal._journal_obj.get_title() + "\""
        $ rule_title = rule.get_title()
        if rule == None:
            return
        call screen confirm("You already scheduled [title] for voting.\n\nDo you wanna schedule the rule \"[rule_title]\" instead?",
            Call("add_to_proposal", rule, 2, rule_name),
            Call("open_journal", 2, rule_name))

    call add_to_proposal(rule, 2, rule_name) from add_rule_to_proposal_2

label add_club_to_proposal(club_name):
    $ club = get_club(club_name)
    $ voteProposal = get_game_data("voteProposal")
    if voteProposal != None:
        $ title = "the " + voteProposal._journal_obj.get_type() + " \"" + voteProposal._journal_obj.get_title() + "\""
        $ club_title = club.get_title()
        if club == None:
            return
        call screen confirm("You already scheduled [title] for voting.\n\nDo you wanna schedule the club \"[club_title]\" instead?",
            Call("add_to_proposal", club, 3, club_name),
            Call("open_journal", 3, club_name))

    call add_to_proposal(club, 3, club_name) from add_club_to_proposal_2

label add_building_to_proposal(building_name):
    $ building = get_building(building_name)
    $ voteProposal = get_game_data("voteProposal")
    if voteProposal != None:
        $ title = "the " + voteProposal._journal_obj.get_type() + " \"" + voteProposal._journal_obj.get_title() + "\""
        $ building_title = building.get_title()
        if building == None:
            return
        call screen confirm("You already scheduled [title] for voting.\n\nDo you wanna schedule the building \"[building_title]\" instead?",
            Call("add_to_proposal", building, 4, building_name),
            Call("open_journal", 4, building_name))

    $ action = "unlock"
    if building.is_unlocked("x"):
        $ action = "upgrade"

    call add_to_proposal(building, 4, building_name, action) from add_building_to_proposal_2