init python:
    gallery_chooser = {}
    gallery_chooser_order = []
    old_event = ""
    
    def journal_add_to_gallery_chooser(value: Any, elem: Any, list_obj: List[Any], dict_obj: Dict[str, Any]) -> Tuple[List[Any], Dict[str, Any]]:
        if elem not in list_obj:
            list_obj.append(elem)
            dict_obj[elem] = value
        return list_obj, dict_obj

    def update_gallery_chooser(gallery_chooser_order: List[string], gallery_chooser: Dict[string, Any], gallery_dict: Dict[string, Any]) -> Dict[string, Any]:
        """
        A function used to update the gallery chooser based on the given order and dictionary

        ### Parameters:
        1. gallery_chooser_order: List[string]
            - The order of the gallery chooser.
        2. gallery_chooser: Dict[string, Any]
            - The gallery chooser to update.
        3. gallery_dict: Dict[string, Any]
            - The dictionary to update the gallery chooser with.

        ### Returns:
        1. Dict[string, Any]
            - The updated gallery chooser.
        """

        reset = False
        # iterates through the order to check if all values are still in scope and if not to replace them
        for topic in gallery_chooser_order:
            # if the value is not in the dictionary or reset is true, then reset the list from this point on
            if gallery_chooser["values"][topic] not in gallery_dict.keys() or reset:
                values = list(gallery_dict.keys())
                gallery_chooser["values"][topic] = None
                if len(values) != 0:
                    gallery_chooser["values"][topic] = values[0]
                reset = True
            gallery_dict = gallery_dict[gallery_chooser["values"][topic]]
        return gallery_chooser
    
    def get_journal_type(page: int) -> str:
        """
        A function used to get the journal type for the given page

        ### Parameters:
        1. page: int
            - The page number to get the journal type for.
            - 0: Overview
            - 1: Rules
            - 2: Clubs
            - 3: Buildings
            - 4: Cheats
            - 5: Credits
            - 6: Gallery

        ### Returns:
        1. str
            - The journal type for the given page.
        """

        page -= 1
        types = ["overview", "rules", "clubs", "buildings", "cheats", "credits"]
        if page < 0 or page > 4:
            return ""
        return types[page]
    
    def get_obj_type(page: int) -> str:
        """
        A function used to get the object type for the given page

        ### Parameters:
        1. page: int
            - The page number to get the object type for.
            - 0: Rules
            - 1: Clubs
            - 2: Buildings

        ### Returns:
        1. str
            - The object type for the given page.
        """

        page -= 2
        types = ["rule", "club", "building"]
        if page < 0 or page > 2:
            return ""
        return types[page]
    
    def get_journal_map(page: int) -> Dict[str, Journal_Obj]:
        """
        A function used to get the journal map for the given page

        ### Parameters:
        1. page: int
            - The page number to get the journal map for.
            - 0: Rules
            - 1: Clubs
            - 2: Buildings

        ### Returns:
        - Dict[str, Journal_Obj]
            - The journal map for the given page.
        """

        page -= 2
        types = [rules, clubs, buildings]
        if page < 0 or page > 2:
            return []
        return types[page]

#########################
# region Journal Events #

init -1 python:
    journal_events = EventStorage("journal_events", "misc", fallback = Event(2, "start_journal.after_check"))

# endregion
#########################

########################
# region Journal Entry #
########################

label start_journal ():
    # """
    # A label used to start the journal screen
    # """

    call call_available_event(journal_events) from start_journal_2

label .after_check (**kwargs):

    call open_journal (1, "") from start_journal_1


label open_journal(page, display, char = "school"):
    # """
    # A label used to open the journal screen

    # ### Parameters:
    # 1. page: int
    #     - The page number to display.
    # 2. display: str
    #     - The display type for the journal page.
    # 3. char: str (default: "school")
    #     - The character to display the journal for.
    # """

    if page == 1:
        call screen journal_overview(display, char) with dissolveM
    elif page == 2:
        call screen journal_page(2, display) with dissolveM
    elif page == 3:
        call screen journal_page(3, display) with dissolveM
    elif page == 4:
        call screen journal_page(4, display) with dissolveM
    elif page == 5:
        call screen journal_cheats(display, char) with dissolveM
    elif page == 6:
        call screen journal_credits(display) with dissolveM
    elif page == 7:
        call screen journal_gallery(display) with dissolveM
    elif page == 8:
        call screen journal_goals(display) with dissolveM
    elif page == 9:
        call screen journal_character(display) with dissolveM

label close_journal ():
    # """
    # A label used to close the journal screen
    # """

    hide screen journal
    jump map_overview

# endregion
########################

#########################
# region Journal Styles #
#########################

style journal_desc:
    color "#000"
    size 20
style journal_desc_small:
    color "#000"
    size 15

style journal_text:
    color "#000"
    size 30

style journal_text_small:
    color "#000"
    size 20

style journal_text_center take journal_text:
    textalign 0.5

style condition_text:
    size 20

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

# endregion
########################

##############################
# region Journal Sub-screens #
##############################

screen journal_obj_list(page, display, journal_map):
    # """
    # A screen used to display the list of objects in the journal

    # ### Parameters:
    # 1. page: int
    #     - The page number to display.
    # 2. display: str
    #     - The display type for the journal page.
    # 3. journal_map: Dict[str, Journal_Obj]
    #     - The map of objects to display in the journal.
    # """

    $ journal_type = get_obj_type(page)
    $ locked_list = get_visible_locked_objs(journal_map)
    $ unlocked_list = get_visible_unlocked_objs(journal_map)
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
                $ obj_list = [(get_journal_obj(journal_map, obj_name).get_title(), get_journal_obj(journal_map, obj_name).get_name()) for obj_name in locked_list]
                use journal_foldable_list("Locked " + get_translation(journal_type), page, display, obj_list, "journal_setting_" + str(page) + "_locked " + journal_type)
                
                null height 20

                $ obj_list2 = [(get_journal_obj(journal_map, obj_name).get_title(), get_journal_obj(journal_map, obj_name).get_name()) for obj_name in unlocked_list]
                use journal_foldable_list("Unlocked " + get_translation(journal_type), page, display, obj_list2, "journal_setting_" + str(page) + "_unlocked " + journal_type, "buttons_active")

        vbar value YScrollValue("[journal_type]List"):
            unscrollable "hide"
            xalign 1.0

screen journal_foldable_list(text, page, display, obj_list, setting_key, default_style = "buttons_idle"):
    # """
    # A screen used to display a foldable list of items in the journal

    # ### Parameters:
    # 1. text: str
    #     - The text to display for the list.
    # 2. page: int
    #     - The page number to display.
    # 3. display: str
    #     - The display type for the journal page.
    # 4. obj_list: List[(str, display)]
    #     - The list of items to display in the journal.
    # 5. setting_key
    #     - The key to use for the game data setting.
    # 6. default_style: str (default: "buttons_idle")
    #     - The default style for the buttons in the list.
    # """

    python:

        journal_settings = get_setting(setting_key)

        if journal_settings == None:
            journal_settings = True
            set_setting(setting_key, True)

    $ journal_map = get_journal_map(page)
    if journal_settings:
        textbutton "[text]":
            text_style "buttons_idle"
            yalign 0.5
            action [With(dissolveM), Function(set_setting, setting_key, False)]
        image "journal/journal/left_list_separator.webp"
        for (title, dest_display) in obj_list:
            $ button_style = default_style
            if dest_display == display:
                $ button_style = "buttons_selected"
            textbutton title:
                text_style button_style
                action [With(dissolveM), Call("open_journal", page, dest_display)]
    else:
        textbutton "[text]":
            text_style "buttons_inactive"
            yalign 0.5
            action [With(dissolveM), Function(set_setting, setting_key, True)]
        image "journal/journal/left_list_separator.webp"

screen journal_simple_list(page, display, display_list, default_style = "buttons_idle", **kwargs):
    # """
    # A screen used to display a simple list of items in the journal

    # ### Parameters:
    # 1. page: int
    #     - The page number to display.
    # 2. display: str
    #     - The display type for the journal page.
    # 3. display_list: Dict[str, str | List[str]]
    #     - The list of items to display in the journal.
    # 4. default_style: str (default: "buttons_idle")
    #     - The default style for the buttons in the list.
    # 5. **kwargs: Dict
    #     - Additional keyword arguments to pass to the screen.
    #     - possible kwargs:
    #         - pos_x: int (default: 330)
    #             - The x position of the list.
    #         - pos_y: int (default: 300)
    #             - The y position of the list.
    #         - width: int (default: 560)
    #             - The width of the list.
    #         - height: int (default: 600)
    #             - The height of the list.
    #         - sort: bool (default: False)
    #             - Whether to sort the list items.
    # """

    $ pos_x = get_kwargs('pos_x', 330, **kwargs)
    $ pos_y = get_kwargs('pos_y', 300, **kwargs)
    $ width = get_kwargs('width', 560, **kwargs)
    $ height = get_kwargs('height', 600, **kwargs)
    $ sort = get_kwargs('sort', False, **kwargs)
    frame:
        background Solid("#0000")
        area (pos_x, pos_y, width, height)

        viewport id "SimpleList":
            mousewheel True
            draggable "touch"

            vbox:
                $ elem_list = sorted(display_list.keys()) if sort else display_list.keys()
                for elem in elem_list:
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

screen journal_page_selector(page, display, char = "school"):
    # """
    # A screen used to display the page selector for the journal pages

    # ### Parameters:
    # 1. page: int
    #     - The page number to display.
    # 2. display: str
    #     - The display type for the journal page.
    # 3. char: str (default: "school")
    #     - The character to display the page selector for.
    # """

    imagemap:
        if page == 1:
            idle "journal/journal/1_idle.webp"
            hover "journal/journal/hover.webp"
        elif page == 2:
            idle "journal/journal/2_idle.webp"
            hover "journal/journal/hover.webp"
        elif page == 3:
            idle "journal/journal/3_idle.webp"
            hover "journal/journal/hover.webp"
        elif page == 4:
            idle "journal/journal/4_idle.webp"
            hover "journal/journal/hover.webp"
        elif page == 5:
            idle "journal/journal/idle.webp"
            hover "journal/journal/hover.webp"
        elif page == 6:
            idle "journal/journal/6_idle.webp"
            hover "journal/journal/hover.webp"
        elif page == 7:
            idle "journal/journal/7_idle.webp"
            hover "journal/journal/hover.webp"
        elif page == 8:
            idle "journal/journal/8_idle.webp"
            hover "journal/journal/hover.webp"
        elif page == 9:
            idle "journal/journal/idle.webp"
            hover "journal/journal/hover.webp"

        $ key_text = ""

        if has_keyboard():  
            if show_shortcut():
                $ key_text = " [[x]"
            if page != 1:
                key "K_1" action [With(dissolveM), Call("open_journal", 1, "")]
                key "K_KP1" action [With(dissolveM), Call("open_journal", 1, "")]
            if page != 8:
                key "K_2" action [With(dissolveM), Call("open_journal", 8, "")]
                key "K_KP2" action [With(dissolveM), Call("open_journal", 8, "")]
            if page != 2:
                key "K_3" action [With(dissolveM), Call("open_journal", 2, "")]
                key "K_KP3" action [With(dissolveM), Call("open_journal", 2, "")]
            if page != 3:
                key "K_4" action [With(dissolveM), Call("open_journal", 3, "")]
                key "K_KP4" action [With(dissolveM), Call("open_journal", 3, "")]
            if page != 4:
                key "K_5" action [With(dissolveM), Call("open_journal", 4, "")]
                key "K_KP5" action [With(dissolveM), Call("open_journal", 4, "")]
            if page != 6:
                key "K_6" action [With(dissolveM), Call("open_journal", 6, "")]
                key "K_KP6" action [With(dissolveM), Call("open_journal", 6, "")]
            if page != 7:
                key "K_7" action [With(dissolveM), Call("open_journal", 7, "")]
                key "K_KP7" action [With(dissolveM), Call("open_journal", 7, "")]

        if page != 1:
            $ text = ("School Overview" + key_text).replace("x", "1")
            hotspot (144, 250, 168, 88) action [With(dissolveM), Call("open_journal", 1, "")] tooltip text
        if page != 2:
            $ text = ("Rules" + key_text).replace("x", "3")
            hotspot (144, 617, 168, 88) action  [With(dissolveM), Call("open_journal", 2, "")] tooltip text
        if page != 3:
            $ text = ("Clubs" + key_text).replace("x", "4")
            hotspot (144, 722, 168, 88) action [With(dissolveM), Call("open_journal", 3, "")] tooltip text
        if page != 4:
            $ text = ("Buildings" + key_text).replace("x", "5")
            hotspot (144, 830, 168, 88) action [With(dissolveM), Call("open_journal", 4, "")] tooltip text
        if page != 6:
            $ text = ("Credits" + key_text).replace("x", "6")
            hotspot (1500, 246, 179, 87) action [With(dissolveM), Call("open_journal", 6, "")] tooltip text
        if page != 7:
            $ text = ("Replay" + key_text).replace("x", "7")
            hotspot (1493, 356, 185, 87) action [With(dissolveM), Call("open_journal", 7, "")] tooltip text
        if page != 8:
            $ text = ("Goals" + key_text).replace("x", "2")
            hotspot (154, 358, 166, 93) action [With(dissolveM), Call("open_journal", 8, "")] tooltip text
            
    if page == 1 or (page == 5 and display == 'stats'):
        if char == "school":
            if has_keyboard():
                key "K_TAB" action [With(dissolveM), Call("open_journal", page, display, "teacher")]
            image "journal/journal/school_hover.webp":
                xpos 365
                ypos 74
            text "School":
                xalign 0.225 yalign 0.1
                size 20
                color "#fff"
        else:
            imagebutton:
                idle "journal/journal/school_idle.webp"
                hover "journal/journal/school_hover.webp"
                xpos 365
                ypos 74
                tooltip "School"
                action [With(dissolveM), Call("open_journal", page, display, "school")]
        if char == "teacher":
            if has_keyboard():
                key "K_TAB" action [With(dissolveM), Call("open_journal", page, display, "parent")]
            image "journal/journal/teacher_hover.webp":
                xpos 541
                ypos 75
            text "Teacher":
                xalign 0.3225 yalign 0.1
                size 20
                color "#fff"
        else:
            imagebutton:
                idle "journal/journal/teacher_idle.webp"
                hover "journal/journal/teacher_hover.webp"
                xpos 541
                ypos 75
                tooltip "Teacher"
                action [With(dissolveM), Call("open_journal", page, display, "teacher")]
        if char == "parent":
            if has_keyboard():
                key "K_TAB" action [With(dissolveM), Call("open_journal", page, display, "school")]
            image "journal/journal/parent_hover.webp":
                xpos 718
                ypos 76
            text "Parents":
                xalign 0.415 yalign 0.1
                size 20
                color "#fff"
        else:
            imagebutton:
                idle "journal/journal/parent_idle.webp"
                hover "journal/journal/parent_hover.webp"
                xpos 718
                ypos 76
                tooltip "Parents"
                action [With(dissolveM), Call("open_journal", page, display, "parent")]

    if cheat_mode:
        if has_keyboard():  
            key "K_8" action [With(dissolveM), Call("open_journal", 5, "")]
            key "K_KP8" action [With(dissolveM), Call("open_journal", 5, "")]
        if page != 5:
            $ text = ("Cheats" + key_text).replace("x", "8")
            imagebutton:
                idle "journal/journal/cheat_idle.webp"
                hover "journal/journal/cheat_hover.webp"
                tooltip text
                xpos 1501
                ypos 715
                action [With(dissolveM), Call("open_journal", 5, "")]
        else:
            image "journal/journal/cheat_hover.webp":
                xpos 1501
                ypos 715

    
    if has_keyboard():  
        key "K_9" action [With(dissolveM), Call("open_journal", 9, "")]
        key "K_KP9" action [With(dissolveM), Call("open_journal", 9, "")]
    if page != 9:
        $ text = ("Characters" + key_text).replace("x", "9")
        imagebutton:
            idle "journal/journal/char_idle.webp"
            hover "journal/journal/char_hover.webp"
            tooltip text
            xpos 144
            ypos 456
            action [With(dissolveM), Call("open_journal", 9, "")]
    else:
        image "journal/journal/char_hover.webp":
            xpos 144
            ypos 456

    $ text = ("Close Journal" + key_text).replace("x", "ESC")

    imagebutton:
        idle "journal/journal/close_idle.webp"
        hover "journal/journal/close_hover.webp"
        tooltip text
        xpos 1509
        ypos 836
        action [With(dissolveM), Jump("map_overview")]

screen journal_desc(**kwargs):
    # """
    # A screen used to display the description of the active object in the journal

    # ### Parameters:
    # 1. page: int
    #     - The page number to display.
    # 2. display: str
    #     - The display type for the journal page.
    # 3. active_obj: Journal_Obj
    #     - The active object to display the description for.
    # 4. with_title: bool (default: False)
    #     - whether the description area should be moved down a bit to make space for the title
    # """

    $ top_description = get_kwargs('top_description', "", **kwargs)
    $ description = get_kwargs('description', "", **kwargs)
    $ description_list_title = get_kwargs('description_list_title', "", **kwargs)
    $ description_list = get_kwargs('description_list', [], **kwargs)

    $ (xpos, ypos, width, height) = get_kwargs('size', (989, 200, 500, 250), **kwargs)

    frame:
        background Solid("#0000")
        area (xpos, ypos, width, height)
        viewport id "RuleDesc":
            mousewheel True
            draggable "touch"

            vbox:
                if top_description != "":
                    text top_description style "journal_desc"
                    null height 40

                text description style "journal_desc"

                if len(description_list) != 0:
                    null height 40
                    if description_list_title != "":
                        text description_list_title style "journal_desc"
                    for desc in description_list:
                        textbutton desc:
                            text_style "journal_desc"
                            yalign 0.5
                            action NullAction()
    
        vbar value YScrollValue("RuleDesc"):
            unscrollable "hide"
            xalign 1.04

screen journal_list_conditions(page, active_obj):
    # """
    # A screen used to display the conditions for the active object in the journal as a compact icon list

    # ### Parameters:
    # 1. page: int
    #     - The page number to display.
    # 2. active_obj: Journal_Obj
    #     - The active object to display the conditions for.
    # """

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
                            text_style "condition_text"
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
    # """
    # A screen used to display the vote button for the journal page

    # ### Parameters:
    # 1. page: int
    #     - The page number to display.
    # 2. display: str
    #     - The display type for the journal page.
    # 3. active_obj: Journal_Obj
    #     - The active object to display the vote button for.
    # """

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
                $ condition_storage = active_obj.get_upgrade_conditions(active_obj.get_level())
                $ action_text = "upgrade"
            if obj_type == 'building':
                $ probability = calculateProbabilitySum(condition_storage)
            else:
                $ log_separator()
                $ probability = calculateProbabilitySum(
                    condition_storage
                )
            $ locked_text = ""
            $ probability_text = str(clamp_value(round(probability, 2))) + "%"
            if condition_storage.get_is_locked():
                $ probability_text = "Locked"
                textbutton "Vote not available in this version!":
                    xpos 985 yalign 0.83
                    text_style "buttons_inactive"
            else:
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
                color "#a00000"
    else:
        text "Already unlocked!":
            xpos 985 yalign 0.83
            color "#008800"
            size 30

screen journal_image(page, display, j_image, full_image, x_pos = 985, y_pos = 474, height = 350, wide = False):
    # """
    # A screen used to display the image of the active object in the journal

    # ### Parameters:
    # 1. page: int
    #     - The page number to display.
    # 2. display: str
    #     - The display type for the journal page.
    # 3. active_obj: Journal_Obj
    #     - The active object to display the image for.
    # """

    if not renpy.loadable(j_image):
        $ j_image = "images/journal/empty_image.webp"
        if wide:
            $ j_image = "images/journal/empty_image_wide.webp"
        $ full_image = None

    $ width = height
    if wide:
        $ width = int(height / 9 * 16)

    if full_image != None and renpy.loadable(full_image):
        button:
            xpos x_pos ypos y_pos
            add j_image: 
                xsize width
                ysize height
            action [With(dissolveM), Call("call_max_image_from_journal", full_image, page, display)]
    else:
        add j_image: 
            xsize width
            ysize height
            xpos x_pos ypos y_pos

screen journal_cheats_stat(stat, char = "school"):
    # """
    # A screen used to display the stat modification Row in the stat list on the cheat journal

    # ### Parameters:
    # 1. stat: str
    #     - the stat to be modified
    # 2. char: str (default: "school")
    #     - the character object for which to modify the stat
    # """

    $ stat_name = str(stat)
    $ stat_text = stat_name.capitalize()
    $ stat_value = 0

    $ char_obj = get_character_by_key(char)

    if stat == MONEY:
        $ stat_value = money.get_display_value()
    elif stat == LEVEL:
        $ stat_value = get_level_for_char(char_obj)
    else:
        $ stat_value = char_obj.get_display_value(stat)

    hbox:
        text get_stat_icon(stat_name, white = False)
        text " [stat_text]" style "journal_text" yalign 0.5
    hbox:
        if stat != MONEY:
            textbutton "Min" action Call("modify_stat", stat, -100, char) text_style "buttons_idle"
            null width 20

        if stat == MONEY:
            textbutton "1000" action Call("modify_stat", stat, -1000, char) text_style "buttons_idle"
            null width 30
        elif stat == LEVEL:
            textbutton "5" action Call("modify_stat", stat, -5, char) text_style "buttons_idle"
            null width 40
        else:
            textbutton "10" action Call("modify_stat", stat, -10, char) text_style "buttons_idle"
            null width 20

        if stat == MONEY:
            textbutton "-" action Call("modify_stat", stat, -100, char) text_style "buttons_idle"
            null width 65
        else:
            textbutton "-" action Call("modify_stat", stat, -1, char) text_style "buttons_idle"
            null width 15

        button:
            text "[stat_value]" xalign 0.5 style "journal_text"
            xsize 100

        if stat == MONEY:
            null width 65
            textbutton "+" action Call("modify_stat", stat, 100, char) text_style "buttons_idle"
        else:
            null width 15
            textbutton "+" action Call("modify_stat", stat, 1, char) text_style "buttons_idle"

        if stat == MONEY:
            null width 30
            textbutton "1000" action Call("modify_stat", stat, 1000, char) text_style "buttons_idle"
        elif stat == LEVEL:
            null width 40
            textbutton "5" action Call("modify_stat", stat, 5, char) text_style "buttons_idle"
        else:
            null width 20
            textbutton "10" action Call("modify_stat", stat, 10, char) text_style "buttons_idle"

        if stat != MONEY:
            null width 30
            textbutton "Max" action Call("modify_stat", stat, 100, char) text_style "buttons_idle"
    null height 30

screen max_image_from_journal(image_path, journal, display):
    # """
    # A screen solely used to display the max size variant of journal images and then return to the original journal page

    # ### Parameters:
    # 1. image_path: str
    #     - The path to the image to display.
    # 2. journal: int
    #     - The journal page to return to.
    # 3. display: str
    #     - The display type for the journal page.
    # """

    tag interaction_overlay
    modal True
    image "[image_path]"
    button:
        xpos 0 ypos 0
        xsize 1902 ysize 1080
        action [With(dissolveM), Call("open_journal", journal, display)]

screen journal_money_overview():
    # """
    # A screen used in the journal money overview to display the current budget and expenses of the school
    # """

    $ stat_obj = money
    $ stat_desc = Stat_Data[stat_obj.get_name()].description

    frame:
        background Solid("#0000")
        area (982, 175, 500, 300)
        viewport id "OverviewDesc":
            mousewheel True
            draggable "touch"

            text "[stat_desc]":
                color "#000"
                size 22
        
        vbar value YScrollValue("OverviewDesc"):
            unscrollable "hide"
            xalign 1.05

    $ modifier_weekly = get_modifier_lists('money', None, 'payroll_weekly')
    $ modifier_monthly = get_modifier_lists('money', None, 'payroll_monthly')

    $ (positive_income_list, negative_income_list, net_weekly, net_monthly) = sort_payroll_modifier(modifier_weekly, modifier_monthly)

    $ rows = len(positive_income_list) + len(negative_income_list) + 6

    $ weekly_net_color = "#00a000"
    $ monthly_net_color = "#00a000"

    if net_weekly < 0:
        $ weekly_net_color = "#a00000"
    elif net_weekly == 0:
        $ weekly_net_color = "#000"

    if net_monthly < 0:
        $ monthly_net_color = "#a00000"
    elif net_monthly == 0:
        $ monthly_net_color = "#000"

    frame:
        background Solid("#0000")
        area (989, 475, 510, 400)
        left_padding 0
        right_padding 0
        viewport id "MoneyOverview":
            mousewheel True
            draggable "touch"

            vbox:
                frame:
                    background Frame("gui/Payroll_Table_1.webp", left=1, top=1, tile = False)
                    left_padding 0
                    hbox:
                        button:
                            text "{b}Name{/b}" style "journal_text_small"
                            xsize 300
                        null width 5
                        button:
                            text "{b}Weekly{/b}" style "journal_text_small"
                            xsize 95
                        null width 2
                        button:
                            text "{b}Monthly{/b}" style "journal_text_small"
                            xsize 95
                        null width 3
                null height -2
                frame:
                    background Frame("gui/Payroll_Table_2.webp", left=1, top=1, tile = False)
                    left_padding 0
                    hbox:
                        button:
                            text "{b}Net Income{/b}" style "journal_text_small"
                            xsize 300
                        null width 5
                        button:
                            text "{b}{color=[weekly_net_color]}[net_weekly]{/color}{/b}":
                                style "journal_text_small"
                                xalign 1.0
                            xsize 95
                        null width 5
                        button:
                            text "{b}{color=[monthly_net_color]}[net_monthly]{/color}{/b}":
                                style "journal_text_small"
                                xalign 1.0
                            xsize 95

                null height 3

                $ table_variant = 1

                if len(positive_income_list) > 0:
                    for name, weekly, monthly in positive_income_list:
                        $ weekly_color = "#00a000"
                        $ monthly_color = "#00a000"

                        if weekly < 0:
                            $ weekly_color = "#a00000"
                        elif weekly == 0:
                            $ weekly_color = "#000"

                        if monthly < 0:
                            $ monthly_color = "#a00000"
                        elif monthly == 0:
                            $ monthly_color = "#000"
                        frame:
                            background Frame("gui/Payroll_Table_" + str(table_variant) + ".webp", left=1, top=1, tile = False)
                            left_padding 0
                            hbox:
                                button:
                                    text "[name]" style "journal_text_small"
                                    xsize 300
                                
                                if weekly == 0:
                                    null width 100
                                else:
                                    null width 5
                                    button:
                                        text "{color=[weekly_color]}[weekly]{/color}":
                                            style "journal_text_small"
                                            xalign 1.0
                                        xsize 95
                                if monthly == 0:
                                    null width 100
                                else:
                                    null width 5
                                    button:
                                        text "{color=[monthly_color]}[monthly]{/color}":
                                            style "journal_text_small"
                                            xalign 1.0
                                        xsize 95
                        $ table_variant = 3 - table_variant
                        null height -2
                    null height 5

                if len(negative_income_list) > 0:
                    for name, weekly, monthly in negative_income_list:
                        $ weekly_color = "#00a000"
                        $ monthly_color = "#00a000"
                        $ reserved_color = "#CCCC00"

                        if weekly < 0:
                            $ weekly_color = "#a00000"
                        elif weekly == 0:
                            $ weekly_color = "#000"

                        if monthly < 0:
                            $ monthly_color = "#a00000"
                        elif monthly == 0:
                            $ monthly_color = "#000"
                        frame:
                            background Frame("gui/Payroll_Table_" + str(table_variant) + ".webp", left=1, top=1, tile = False)
                            left_padding 0
                            hbox:
                                button:
                                    text "[name]" style "journal_text_small"
                                    xsize 300
                                
                                if weekly == 0:
                                    null width 100
                                else:
                                    null width 5
                                    button:
                                        text "{color=[weekly_color]}[weekly]{/color}":
                                            style "journal_text_small"
                                            xalign 1.0
                                        xsize 95
                                if monthly == 0:
                                    null width 100
                                else:
                                    null width 5
                                    button:
                                        text "{color=[monthly_color]}[monthly]{/color}":
                                            style "journal_text_small"
                                            xalign 1.0
                                        xsize 95
                        $ table_variant = 3 - table_variant
                        null height -2
                    null height 5

                frame:
                    background Frame("gui/Payroll_Table_" + str(table_variant) + ".webp", left=1, top=1, tile = False)
                    left_padding 0
                    hbox:
                        button:
                            text "{b}Net Income{/b}" style "journal_text_small"
                            xsize 300
                        null width 5
                        button:
                            text "{b}{color=[weekly_net_color]}[net_weekly]{/color}{/b}":
                                style "journal_text_small"
                                xalign 1.0
                            xsize 95
                        null width 5
                        button:
                            text "{b}{color=[monthly_net_color]}[net_monthly]{/color}{/b}":
                                style "journal_text_small"
                                xalign 1.0
                            xsize 95
                if reserved_money != None and len(reserved_money.keys()) != 0:
                    null height 5

                    $ reserved_total = sum(reserved_money.values())

                    frame:
                        background Frame("gui/Payroll_Table_3.webp", left=1, top=1, tile = False)
                        left_padding 0
                        hbox:
                            button:
                                text "{b}Reserved Money{/b}" style "journal_text_small"
                                xsize 300
                            null width 5
                            button:
                                text "{b}{color=[reserved_color]}[reserved_total]{/color}{/b}":
                                    style "journal_text_small"
                                    xalign 1.0
                                xsize 195

        vbar value YScrollValue("MoneyOverview"):
            unscrollable "hide"
            xalign 1.035

# endregion
##############################

########################
# region Main Journals #
########################

# Object Pages
screen journal_page(page, display):
    # """
    # This screen is used to display the journal pages for rules, clubs and buildings

    # ### Parameters:
    # 1. page: int
    #     - The page number to display.
    # 2. display: str
    #     - The display type for the journal page.
    # """

    use school_overview_map
    use school_overview_stats

    image "journal/journal/background.webp"

    key "K_ESCAPE" action [With(dissolveM), Jump("map_overview")]

    $ journal_type = get_journal_type(page)
    $ journal_map = get_journal_map(page)
    $ active_obj = get_journal_obj(journal_map, display)
    
    if display == "" or (display != "" and not active_obj.is_visible(char_obj = get_school())):
        $ display = ""
        $ locked_list = get_visible_locked_objs(journal_map)
        $ unlocked_list = get_visible_unlocked_objs(journal_map)

        if len(unlocked_list) != 0:
            $ display = unlocked_list[0]
        elif len(locked_list) != 0:
            $ display = locked_list[0]

        $ active_obj = get_journal_obj(journal_map, display)

    use journal_page_selector(page, display)

    $ page_title = get_translation(get_obj_type(page))

    text page_title: 
        xalign 0.25 
        yalign 0.2
        size 60
        color "#000"

    use journal_obj_list(page, display, journal_map)

    if display != "":
        
        $ image, variant = active_obj.get_image(variant = get_random_loli())
        $ full_image, variant = active_obj.get_full_image(variant = variant)

        use journal_image(page, display, image, full_image)

        $ descriptions = {}

        $ descriptions['description'] = active_obj.get_description_str()

        $ action_text = "unlock"
        $ obj_type = active_obj.get_type()
        if obj_type == "building" and active_obj.is_unlocked()  and active_obj.has_higher_level():
            $ action_text = "upgrade"

        $ descriptions['description_list'] = active_obj.get_desc_conditions_desc(cond_type = action_text, char_obj = get_school(), blocking = True)
        if len(descriptions['description_list']) != 0:
            $ descriptions['description_list_title'] = "{u}To unlock you need:{/u}"


        $ condition_storage = active_obj.get_condition_storage()
        if obj_type == 'building' and active_obj.can_be_upgraded(char_obj = get_school()):
            $ condition_storage = active_obj.get_upgrade_conditions(active_obj.get_level())
        
        if condition_storage.get_is_locked():
            $ descriptions['top_description'] = ("This object isn't currently implemented and only acts as a preview of what's to come.\n" +
                "All values and contents are subject to change.\n" +
                "----------------------------------------")

        use journal_desc(**descriptions)

        use journal_list_conditions(page, active_obj)

        use journal_vote_button(page, display, active_obj)

    $ tooltip = GetTooltip()
    if tooltip:
        nearrect:
            focus "tooltip"
            prefer_top True

            frame:
                xalign 0.5
                text tooltip

# School Overview
screen journal_overview(display, char = "school"):
    # """
    # This screen is used to display the school overview.

    # ### Parameters:
    # 1. display: str
    #     - The display type for the school overview.
    # 2. char: str (default: "school")
    #     - The character to display the overview for.
    # """

    tag interaction_overlay
    modal True

    use school_overview_map
    use school_overview_stats

    image "journal/journal/background.webp"

    key "K_ESCAPE" action [With(dissolveM), Jump("map_overview")]

    use journal_page_selector(1, display, char)

    text "School Overview": 
        xalign 0.25 
        yalign 0.2
        size 60
        color "#000"

    text "Click on any stat to get more information on it.":
        style "journal_text_small"
        xalign 0.25
        yalign 0.26

    $ object_overview = {
        'school': get_school(),
        'teacher': get_character('teacher', charList['staff']),
        'parent': get_character('parent', charList)
    }

    $ school_object = object_overview[char]
    $ school_stats = school_object.get_stats()

    $ pta_proposal = get_game_data('voteProposal')

    if display == "":
        $ display = "money"

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

                    text get_stat_icon("money", white = False)
                    textbutton "  Money:":
                        yalign 0.5 
                        text_style button_style
                        action [With(dissolveM), Call("open_journal", 1, "money", char)]
                    text "[money_text]" style "journal_text" yalign 0.5

                null height 20

                text "[school_object.title]" style "journal_text" size 40

                null height 20

                hbox:
                    $ button_style = "buttons_idle"
                    if "level" == display:
                        $ button_style = "buttons_selected"
                    $ level_text = school_object.level.display_stat()

                    text get_stat_icon("level", white = False)
                    textbutton "  Level:":
                        yalign 0.5 
                        text_style button_style
                        action [With(dissolveM), Call("open_journal", 1, "level", char)]
                    text "[level_text]" style "journal_text" yalign 0.5

                null height 20

                for stat_key in school_stats.keys():
                    $ stat_obj = school_object.get_stat_obj(stat_key)
                    $ stat_icon = stat_obj.get_image_path()
                    $ stat_value = stat_obj.display_stat()
                    $ stat_title = Stat_Data[stat_obj.get_name()].get_title()
                    $ button_style = "buttons_idle"
                    if stat_key == display:
                        $ button_style = "buttons_selected"
                    hbox:
                        text get_stat_icon(stat_key, white = False)
                        textbutton "  [stat_title]:":
                            yalign 0.5 
                            text_style button_style
                            action [With(dissolveM), Call("open_journal", 1, stat_obj.get_name(), char)]
                        text " [stat_value]" style "journal_text" yalign 0.5

                null height 20

                text "Subject Proficiency" style "journal_text" size 40

                null height 20

                $ subject_levels = get_headmaster_proficiency_levels()
                $ subject_xp = get_headmaster_proficiency_xps()

                for key in subject_levels.keys():
                    $ subject = get_translation(key)
                    $ level = subject_levels[key]
                    $ xp = subject_xp[key]
                    text "{b}[subject]{/b}:" style "journal_text" size 28
                    text "    Lvl. [level] {size=20}([xp] / 100){/size}" style "journal_text" yalign 0.5 size 25
                    null height 5

        vbar value YScrollValue("Overview"):
            unscrollable "hide"
            xalign 1.0

    if display != "":
        $ active_stat_obj = None
        if display == "level":
            $ active_stat_obj = school_object.get_level_obj()
        elif display == "money":
            $ active_stat_obj = money
        elif school_object.check_stat_exists(display):
            $ active_stat_obj = school_object.get_stat_obj(display)

        if display == "money":
            use journal_money_overview
        else:
            if active_stat_obj != None:
                $ active_desc = active_stat_obj.get_full_description(char_obj = school_object)
                $ active_image = active_stat_obj.get_image()

                image "[active_image]":
                    xalign 0.63 yalign 0.65
                
                frame:
                    background Solid("#0000")
                    area (989, 200, 500, 250)
                    viewport id "OverviewDesc":
                        mousewheel True
                        draggable "touch"

                        text "[active_desc]":
                            color "#000"
                            size 22
                    
                    vbar value YScrollValue("OverviewDesc"):
                        unscrollable "hide"
                        xalign 1.05

    $ tooltip = GetTooltip()
    if tooltip:
        nearrect:
            focus "tooltip"
            prefer_top True

            frame:
                xalign 0.5
                text tooltip

# Cheats
screen journal_cheats(display, char = "school"):
    # """
    # A screen to show cheats and debug options in journal

    # ### Paramters:
    # 1. display: str
    #     - The current display page
    # 2. char: str (default: "school")
    #     - The character to show cheats for
    # """

    tag interaction_overlay
    modal True

    use school_overview_map
    use school_overview_stats

    image "journal/journal/background.webp"

    key "K_ESCAPE" action [With(dissolveM), Jump("map_overview")]

    use journal_page_selector(5, display, char)

    text "Cheats":
        xalign 0.72 yalign 0.11
        size 20
        color "#000"

    $ options = {
        "general": "General",
        "stats": "Stats",
        "mods": "Mods",
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
                    text "Changing game values can lead to unintended behaviour or a broken game save.\nMost functions on this page are used for debugging during developement.\nProceed on your own risk.":
                        color "#000000"
                        size 20

                    null height 20

                    # DEBUG
                    hbox:
                        button:
                            text "DEBUG" xalign 0.0 style "journal_text"
                            xsize 250

                        $ debug_mode_text = "{color=#a00000}ACTIVATE{/color}"
                        if debug_mode:
                            $ debug_mode_text = "{color=#00a000}DEACTIVATE{/color}"
                        button:
                            text debug_mode_text xalign 1.0
                            action [With(dissolveM), Call("switch_debug_mode", 5, display)]
                            xsize 250
                    null height 10
                    # Event Selection
                    hbox:
                        button:
                            text "SELECT EVENTS" xalign 0.0 style "journal_text"
                            xsize 250

                        $ event_select_text = "{color=#a00000}ACTIVATE{/color}"
                        if event_selection_mode:
                            $ event_select_text = "{color=#00a000}DEACTIVATE{/color}"
                        button:
                            text event_select_text xalign 1.0
                            action [With(dissolveM), Call("switch_event_select_mode", 5, display)]
                            xsize 250
                    null height 10
                    # TIME
                    hbox:
                        button:
                            text "Time" xalign 0.0 style "journal_text"
                            xsize 250

                        $ time_freeze_text = "{color=#a00000}FREEZE{/color}"
                        if time_freeze:
                            $ time_freeze_text = "{color=#00a000}UNFREEZE{/color}"
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
                    null height 10
                    
                    text "Debug:" style "journal_text" size 20
                    button:
                        text "Run Test-Label" style "buttons_idle"
                        action Call("test_label")

                    null height 10
                    hbox:
                        button:
                            text "Reset Gallery" xalign 0.0 style "journal_text"
                            xsize 250

                        button:
                            text "{color=#a00000}RESET NOW{/color}" xalign 1.0
                            action [With(dissolveM), Call("reset_gallery_cheat", 5, display)]
                            xsize 250

                    null height 10
                    hbox:
                        button:
                            text "Dump Gallery Data" xalign 0.0 style "journal_text"
                            xsize 250

                        button:
                            text "{color=#a00000}PRINT{/color}" xalign 1.0
                            action [With(dissolveM), Call("dump_gallery_data", 5, display)]
                            xsize 250
                
                    
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
                    use journal_cheats_stat(MONEY, char)
                    # LEVEL
                    use journal_cheats_stat(LEVEL, char)
                    # CORRUPTION
                    use journal_cheats_stat(CORRUPTION, char)
                    # INHIBITION
                    use journal_cheats_stat(INHIBITION, char)
                    # HAPPINESS
                    use journal_cheats_stat(HAPPINESS, char)
                    # EDUCATION
                    use journal_cheats_stat(EDUCATION, char)
                    # CHARM
                    use journal_cheats_stat(CHARM, char)
                    # REPUTATION
                    use journal_cheats_stat(REPUTATION, char)
                    
            vbar value YScrollValue("CheatStatList"):
                unscrollable "hide"
                xalign 1.0
    elif display == "mods":
        frame:
            background Solid("#0000")
            area (950, 200, 560, 690)

            viewport id "CheatModList":
                mousewheel True
                draggable "touch"

                vbox:
                    text "After activating or deactivating mod, you have to refresh the game.\nWorks only in developer mode.":
                        color "#000000"
                        size 20

                    null height 20

                    for mod_key in persistent.modList.keys():
                        $ mod = persistent.modList[mod_key]
                        if not mod['available']:
                            continue

                        $ mod_name = mod['name']
                        $ mod_unlock_text = "{color=#a00000}ACTIVATE{/color}"
                        if mod['active']:
                            $ mod_unlock_text = "{color=#00a000}DEACTIVATE{/color}"
                        text mod_name:
                            style "buttons_idle"
                        if mod_name != 'Base Mod':
                            hbox:
                                null width 100
                                button:
                                    text mod_unlock_text
                                    action [With(dissolveM), Call("switch_mod", mod_key, not persistent.modList[mod_key]['active'])]
                        null height 10
                    

            vbar value YScrollValue("CheatModList"):
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
                            $ rule_unlock_text = "{color=#a00000}UNLOCK{/color}"
                            if rule.is_unlocked():
                                $ rule_unlock_text = "{color=#00a000}LOCK{/color}"
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

            # title
            $ active_rule_title = active_rule.get_title()
            text active_rule_title:
                xpos 989
                ypos 200
                size 30
                xmaximum 500
                ymaximum 50
                color "#000"

            # image
            $ active_rule_image, variation = active_rule.get_image()
            $ active_rule_full_image, variation = active_rule.get_full_image(variant = variation)
            use journal_image(5, display, active_rule_image, active_rule_full_image)

            # description
            $ descriptions = {
                'description': active_rule.get_description_str(),
                'description_list': active_rule.get_desc_conditions_desc(char_obj = get_school())
            }

            if len(descriptions['description_list']) != 0:
                $ descriptions['description_list_title'] = "{u}To unlock you need:{/u}"

            use journal_desc(size = (989, 250, 500, 200), **descriptions)

            use journal_list_conditions(page, active_rule)

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
                            $ club_unlock_text = "{color=#a00000}UNLOCK{/color}"
                            if club.is_unlocked():
                                $ club_unlock_text = "{color=#00a000}LOCK{/color}"
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

            # title
            $ active_club_title = active_club.get_title()
            text active_club_title:
                xpos 989
                ypos 200
                size 30
                xmaximum 500
                ymaximum 50
                color "#000"

            # image
            $ active_club_image, variation = active_club.get_image()
            $ active_club_full_image, variation = active_club.get_full_image(variant = variation)
            use journal_image(5, display, active_club_image, active_club_full_image)

            # description
            $ descriptions = {
                'description': active_club.get_description_str(),
                'description_list': active_club.get_desc_conditions_desc(char_obj = get_school())
            }

            if len(descriptions['description_list']) != 0:
                $ descriptions['description_list_title'] = "{u}To unlock you need:{/u}"

            use journal_desc(size = (989, 250, 500, 200), **descriptions)

            use journal_list_conditions(page, active_club)

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
                            $ building_unlock_text = "{color=#a00000}UNLOCK{/color}"
                            if building.is_unlocked():
                                $ building_unlock_text = "{color=#00a000}LOCK{/color}"
                            button:
                                text building_name:
                                    style "buttons_idle"
                                action [With(dissolveM), Call("open_journal", 5, display + ":" + building.get_name())]
                            hbox:
                                null width 100
                                button:
                                    text building_unlock_text
                                    action [With(dissolveM), Call("switch_building", building.get_name(), -1000)]
                                if building.is_unlocked():
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

            # title
            $ active_building_title = active_building.get_title()
            text active_building_title:
                xpos 989
                ypos 200
                size 30
                xmaximum 500
                ymaximum 50
                color "#000"

            # image
            $ active_building_image, variation = active_building.get_image()
            $ active_building_full_image, variation = active_building.get_full_image(variant = variation)
            use journal_image(5, display, active_building_image, active_building_full_image)

            # description
            $ descriptions = {
                'description': active_building.get_description_str(),
                'description_list': active_building.get_desc_conditions_desc(char_obj = get_school())
            }

            if len(descriptions['description_list']) != 0:
                $ descriptions['description_list_title'] = "{u}To unlock you need:{/u}"

            use journal_desc(size = (989, 250, 500, 200), **descriptions)

            use journal_list_conditions(page, active_building)

            textbutton "Return":
                xalign 0.55 yalign 0.87
                text_style "buttons_idle"
                action [With(dissolveM), Call("open_journal", 5, "buildings")]

    $ tooltip = GetTooltip()
    if tooltip:
        nearrect:
            focus "tooltip"
            prefer_top True

            frame:
                xalign 0.5
                text tooltip

# Gallery
screen journal_gallery(display):
    # """
    # Display the gallery of events and locations that the player has unlocked.

    # ### Parameters:
    # 1. display: str
    #     - The display parameter is used to determine which event or location is currently selected.
    # """

    tag interaction_overlay
    modal True

    use school_overview_map
    use school_overview_stats

    image "journal/journal/background.webp"

    key "K_ESCAPE" action [With(dissolveM), Jump("map_overview")]

    use journal_page_selector(7, display)

    text "Gallery":
        xalign 0.25 yalign 0.2
        size 60
        color "#000"

    # separate location and event in display (schema: location.event)
    $ split_display = [display, "", "value_mode", ""]
    if '.' in display:
        $ split_display = display.split('.')
    
    

    $ location = split_display[0]
    $ event = split_display[1] if len(split_display) > 1 else ""

    

    # value_mode, fragment_mode, fragment_selection_mode
    $ display_mode = split_display[2] if len(split_display) > 2 else "value_mode"
    $ fragment_selection_index = int(split_display[3]) if len(split_display) > 3 and is_integer(split_display[3]) else 0
    $ fragment_selection_fragment = split_display[4] if len(split_display) > 4 else ""

    python:
        if get_event_from_register(fragment_selection_fragment) != None:
            persistent.gallery[location][event]['options']['frag_order'][fragment_selection_index] = fragment_selection_fragment

    if location != "" and location not in persistent.gallery.keys():
        $ location = ""
        $ event = ""
    elif event != "" and event not in persistent.gallery[location].keys():
        $ event = ""    

    # if no location is defined 
    if location == "": 
        
        # parse all available location keys to their corresponding buildings
        # $ location_list = [get_building(location_name) for location_name in persistent.gallery.keys() if get_building(location_name) != None]

        # # map all the buildings with their corresponding names into a dict
        # $ location_dict = {building.get_name(): building.get_title() for building in location_list}
        $ exclude_keys = ['FragStorage', 'fragment']
        $ location_dict = {key: get_translation(key) for key in persistent.gallery.keys() if key not in exclude_keys}

        # add the miscellaneous location separately as there is no corresponding building
        # miscellaneous represents all events that are not bound to a location
        # if 'misc' in persistent.gallery.keys():
        #     $ location_dict['misc'] = "Miscellaneous"

        

        # check if there is any event that can be replayed
        # if yes, display a list with all locations where events are available
        # if no be sad and show that
        if len(location_dict) != 0:
            use journal_simple_list(7, location, location_dict, "buttons_idle", pos_x = 350, width = 500, sort = True)
            text "Please select a location.":
                xpos 989
                ypos 200
                size 30
                xmaximum 500
                ymaximum 50
                color "#000"
        else:
            text "No Events to replay :(":
                xpos 989
                ypos 200
                size 30
                xmaximum 500
                ymaximum 50
                color "#000"
        
    elif location != "": # if a location is defined
        

        $ location_title = "Miscellaneous"
        $ building = get_building(location)
        if building != None:
            $ location_title = building.get_title()
        
        # display a button that deletes all persistent data for all events registered in that location
        if debug_mode:
            textbutton "{color=#a00000}Reset Location{/color}":
                text_style "journal_text"
                xpos 350
                ypos 260
                action [With(dissolveM), Call('reset_event_gallery', location, "")]

        # return button for returning to location overview
        textbutton "← [location_title]":
            xpos 350 ypos 300
            text_style "buttons_idle"
            action [With(dissolveM), Call("open_journal", 7, "")]
        
        # if there is no event displayed, prompt the user to select one
        if event == "":
            text "Please select an event.":
                xpos 989
                ypos 200
                size 30
                xmaximum 500
                ymaximum 50
                color "#000"
        elif display_mode == "fragment_selection_mode":
            $ event_obj = get_event_from_register(event)
            $ event_title = get_translation(event_obj.get_id())
            # return button for returning to location overview
            textbutton "  ← [event_title]":
                xpos 350 ypos 350
                text_style "buttons_idle"
                action [With(dissolveM), Call("open_journal", 7, '.'.join([location, event, "fragment_mode"]))]
        
    # if location is selected, display a list of all possible events in that location
    if location != "":
        
        if display_mode != "fragment_selection_mode":
            $ event_list = [get_event_from_register(event_name) for event_name in persistent.gallery[location].keys() if get_event_from_register(event_name) != None and renpy.has_label(get_event_from_register(event_name).get_event_label())]
            $ event_dict = {f"{location}.{event_obj.get_event()}": get_translation(event_obj.get_event()) for event_obj in event_list}
            use journal_simple_list(7, display, event_dict, "buttons_idle", pos_x = 400, pos_y = 350, width = 450, sort = True)
        else: 
            $ event_frag_storage = persistent.gallery[location][event]['options']['Frag_Storage'][fragment_selection_index]
            $ base_event_data = persistent.gallery[location][event]['options']['last_data']
            $ event_list = [get_event_from_register(event_name) for event_name in persistent.gallery["FragStorage"][event_frag_storage]['values'].keys() if get_event_from_register(event_name) != None and get_event_from_register(event_name).is_available(in_journal_gallery = True, **base_event_data)]
            $ event_dict = {'.'.join([location, event, "fragment_selection_mode", str(fragment_selection_index), event_obj.get_event()]): get_translation(event_obj.get_event()) for event_obj in event_list}
            use journal_simple_list(7, display, event_dict, "buttons_idle", pos_x = 450, pos_y = 400, width = 450, height = 550, sort = True)
        
    # if an event is selected, display event information on right side
    if event != "":
        

        $ event_obj = get_event_from_register(event)
        $ top_border_offset = 0

        # display event title on top of page
        $ event_title = get_translation(event_obj.get_event())
        text event_title:
            xpos 989
            ypos 200
            size 30
            xmaximum 500
            ymaximum 50
            color "#000"
        
        # display event thumbnail if available
        $ thumbnail = Image("images/journal/empty_image_wide.webp")
        if renpy.loadable(event_obj.get_thumbnail()):
            $ thumbnail = im.Scale(event_obj.get_thumbnail(), 500, 281)

        image thumbnail:
            xpos 989 ypos 250

        $ has_option = False
        
        if event_obj.get_form() == "composite":            
            python:
                if 'frag_order' not in persistent.gallery[location][event]['options'].keys():
                    persistent.gallery[location][event]['options']['frag_order'] = []

                for i, frag_storage_name in enumerate(persistent.gallery[location][event]['options']['Frag_Storage']):
                    if i >= len(persistent.gallery[location][event]['options']['frag_order']):
                        frag_event = list(persistent.gallery["FragStorage"][frag_storage_name]['values'].keys())[0]
                        persistent.gallery[location][event]['options']['frag_order'].append(frag_event)
        
        if display_mode == "fragment_mode":
            
            frame:
                background Solid('#0000')
                area(989, 600, 500, 270)
                viewport id "GalleryFragmentSelectionOverview":
                        
                    vbox:
                        for i, frag_storage_name in enumerate(persistent.gallery[location][event]['options']['Frag_Storage']):
                            $ curr_fragment = persistent.gallery[location][event]['options']['frag_order'][i]
                            $ frag_title = str(i + 1) + ": " + get_event_menu_title('fragment', curr_fragment) + " →"
                            textbutton frag_title:
                                action [With(dissolveM), Call('open_journal', 7, '.'.join([location, event, "fragment_selection_mode", str(i), curr_fragment]))]
    
                vbar value YScrollValue("GalleryFragmentSelectionOverview"):
                    unscrollable "hide"
                    xalign 1.0
                    xoffset 15
        $ disable_play = False
        
        if display_mode == "value_mode" or display_mode == "fragment_selection_mode":
            
            # check if event has changed to trigger information reload
            $ base_gallery = persistent.gallery[location][event]
            $ display_event = event
            $ display_location = location
            if display_mode == "fragment_selection_mode":
                $ base_gallery = persistent.gallery['fragment'][fragment_selection_fragment]
                $ display_event = fragment_selection_fragment
                $ display_location = "fragment"

            if display_event != old_event:
                $ gallery_chooser = {"values": {}}
                $ gallery_chooser_order = []
                $ old_event = display_event
            
            # load existing data for user selection from last session
            if ('last_data' in base_gallery['options'].keys() and 
                'last_order' in base_gallery['options'].keys()
            ):
                $ gallery_chooser["values"] = base_gallery['options']['last_data']
                $ gallery_chooser_order = base_gallery['options']['last_order']
            
            # displays a button that deletes all persistent data for this specific event
            if debug_mode:
                textbutton "{color=#a00000}Reset Event{/color}":
                    text_style "journal_text"
                    xpos 1280
                    ypos 160
                    action [With(dissolveM), Call('reset_event_gallery', display_location, display_event)]
            
            # load all variables requested by the event
            $ variant_names = [topic for topic in base_gallery['order']]
            
            $ event_obj = get_event_from_register(display_event)
            
            # display value overview for all possible values in all needed variables
            frame:
                area(989, 600, 500, 250)
                background Solid('#0000')
                viewport id "GallerySelectionOverview":
                    mousewheel True
                    draggable "touch"
                    hbox:
                        
                        # get the entire value tree from persistent data for this event
                        $ gallery_dict = base_gallery['values']
                        # iterate over all variables to display a selection list for each variable
                        for variant_name in variant_names:
                            # get all possible values
                            $ values = list(gallery_dict.keys())
                            
                            # check if variable is new and add it to the data if missing
                            python:
                                if variant_name not in gallery_chooser_order:
                                    gallery_chooser_order.append(variant_name)
                                    gallery_chooser["values"][variant_name] = values[0]
                            
                            # get the currently selected value for the current variable
                            $ value = gallery_chooser["values"][variant_name]
                            
                            # if value is not in current variable set because of differing sets on this tree path, select first value in list
                            python:
                                if value not in values:
                                    gallery_chooser["values"][variant_name] = values[0]
                            
                            # get the gallery data tree starting from this variable so the next variable can work with that
                            $ gallery_dict = gallery_dict[gallery_chooser["values"][variant_name]]
                            
                            # checks if there is more than one selection possible and only then displays a value list,
                            # otherwise the only selection possible is selected by default and will not be displayed in the overview
                            if len(values) > 1:
                                
                                # get display title for variable
                                $ title = get_gallery_topic_title(display_location, display_event, variant_name) 
                                

                                # display list of values
                                frame:
                                    background Frame("gui/border.png", left=1, top=1, tile = True)
                                    vbox:
                                        
                                        text "[title]":
                                            bold True
                                            style "journal_text"
                                            size 30

                                        # filters all possible values that have been filtered in the loli filter as those can only be seen, selected or viewed if the appropriate loli setting is activated
                                        $ filtered_values = [value for value in values if variant_name + '.' + str(value) not in loli_filter[loli_content]]
                                        
                                        # checks if any values are left after filtering and disables the replay possibility if there is none as the events need a full set of values to work properly
                                        if len(filtered_values) == 0:
                                            
                                            python:
                                                if gallery_chooser["values"][variant_name] not in filtered_values:
                                                    gallery_chooser["values"][variant_name] = None
                                                    update_gallery_chooser(gallery_chooser_order, gallery_chooser, base_gallery['values'])
                                            $ disable_play = True
                                        else:
                                            
                                            # iterates through all possible values and displays them for the user to select
                                            for value in sorted(filtered_values):
                                                $ has_option = True
                                                $ value_text = get_gallery_value_title(variant_name, display_location, display_event, value)
                                                if value == gallery_chooser["values"][variant_name]:
                                                    textbutton "[value_text]":
                                                        text_style "buttons_selected"
                                                        action NullAction()
                                                else:
                                                    textbutton "[value_text]":
                                                        text_style "buttons_idle"
                                                        action [With(dissolveM), SetDict(gallery_chooser["values"], variant_name, value), SetVariable('gallery_chooser', update_gallery_chooser(gallery_chooser_order, gallery_chooser, base_gallery['values']))]
                        
                bar value XScrollValue("GallerySelectionOverview"):
                    unscrollable "hide"
                    yalign 1.0
                    yoffset 15
                vbar value YScrollValue("GallerySelectionOverview"):
                    unscrollable "hide"
                    xalign 1.0
                    xoffset 15
            
            # saves the current selection for this event in the persistent gallery data so the selection is maintained between sessions
            if not disable_play:
                $ base_gallery['options']['last_data'] = gallery_chooser["values"]
                $ base_gallery['options']['last_order'] = gallery_chooser_order
        
        if has_option and event_obj.get_form() != "composite":
            text "Variants":
                xpos 989
                ypos 560
                color "#000"
        elif event_obj.get_form() == "composite" and display_mode in ["value_mode", "fragment_mode"]:
            
            if display_mode == "value_mode" and not has_option:
                text "No values to choose :(":
                    style "buttons_inactive"
                    xpos 1000
                    ypos 650
                # action Call('open_journal', 7, '.'.join([location, event, "fragment_mode"]))
            
            $ top_border_offset = 50
            hbox:
                
                if display_mode == "value_mode":
                    
                    textbutton "Values":
                        text_style "buttons_selected"
                        xpos 989
                        ypos 560
                        action NullAction()

                    textbutton "Fragments":
                        text_style "buttons_idle"
                        xpos 1030
                        ypos 560
                        action [With(dissolveM), Call("open_journal", 7, '.'.join([location, event, "fragment_mode"]))]
                else:
                    
                    textbutton "Values":
                        text_style "buttons_idle"
                        xpos 989
                        ypos 560
                        action [With(dissolveM), Call("open_journal", 7, '.'.join([location, event, "value_mode"]))]
                    textbutton "Fragments":
                        text_style "buttons_selected"
                        xpos 1030
                        ypos 560
                        action NullAction()
        

        if display_mode == "value_mode" or display_mode == "fragment_mode":
            
            # displays the replay button if replay is possible
            if not disable_play:
                
                if event_obj.get_form() == "composite":
                    
                    button:
                        text "▶ Start Replay":
                            style "buttons_idle"
                            size 50
                        xpos 1000
                        ypos 880
                        action [Call('start_gallery_composite_replay', location, event, dict(gallery_chooser), list(persistent.gallery[location][event]['options']['frag_order']), display)]
                else:
                    
                    button:
                        text "▶ Start Replay":
                            style "buttons_idle"
                            size 50
                        xpos 1000
                        ypos 880
                        action [Call('start_gallery_replay', location, event, dict(gallery_chooser), display)]
            else:
                
                button:
                    text "Replay not available":
                        style "buttons_inactive"
                        size 30
                    xpos 1000
                    ypos 880
        else:
            button:
                text "← Return to Main Event":
                    style "buttons_idle"
                    size 40
                xpos 1000
                ypos 880
                action [With(dissolveM), Call("open_journal", 7, '.'.join([location, event, "fragment_mode"]))]
        
    $ tooltip = GetTooltip()
    if tooltip:
        nearrect:
            focus "tooltip"
            prefer_top True

            frame:
                xalign 0.5
                text tooltip


image pBannerI = im.Scale("images/journal/journal/patreon banner idle.webp", 500, 262)
image pBannerH = im.Scale("images/journal/journal/patreon banner hover.webp", 500, 262)
# Credits
screen journal_credits(display):
    # """
    # A screen used to display the credits in the journal

    # ### Parameters:
    # 1. display: str
    #     - the display to be opened after the credits have been closed
    # """

    tag interaction_overlay
    modal True

    use school_overview_map
    use school_overview_stats

    image "journal/journal/background.webp"

    key "K_ESCAPE" action [With(dissolveM), Jump("map_overview")]

    use journal_page_selector(6, display)

    $ (student_members, time_text) = get_members("Student")
    $ (teacher_members, time_text) = get_members("Teacher")

    # left side
    # displays all patrons with teacher tier subscription on Patreon
    frame:
        # background Solid("#00000090")
        background Solid("#00000000")
        area (350, 200, 500, 750)

        vbox:
            text "Thanks to all patrons!":
                    size 40
                    color "#000000"
            text time_text:
                size 20
                color "#8a8a8a"
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
                            $ data = member.split(';')
                            # shows 'Anonymous' if name has been blacklisted due to patrons wish
                            if data[0] == '*blacklisted*':
                                text "{i}Anonymous{/i}":
                                    color "#00000060"
                                    size 25

                            # displays an alias wished by the patron to keep his real name anonymous
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
    # displays all patrons with student tier subscription on Patreon
    frame:
        # background Solid("#00000090")
        background Solid("#00000000")
        area (960, 200, 500, 700)

        vbox:
            # small image with link to patreon page
            text "Consider supporting the game:":
                    size 30
                    color "#000000"
            imagebutton:
                idle "pBannerI"
                hover "pBannerH"
                action Call("open_patreon_link")
            null height 20

            # patrons overview of student tier patrons
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
                            $ data = member.split(';')
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

    $ tooltip = GetTooltip()
    if tooltip:
        nearrect:
            focus "tooltip"
            prefer_top True

            frame:
                xalign 0.5
                text tooltip

# Goals
screen journal_goals(display):
    tag interaction_overlay
    modal True

    use school_overview_map
    use school_overview_stats

    image "journal/journal/background.webp"

    key "K_ESCAPE" action [With(dissolveM), Jump("map_overview")]

    use journal_page_selector(8, display, char)

    text "Goals": 
        xalign 0.25 
        yalign 0.2
        size 60
        color "#000"

    python:
        show_note = get_setting("journal_goals_show_note_setting")
        note_tooltip = "Show quests as a hint"
        if show_note:
            note_tooltip = "Don't show quests as a hint"

    button:
        xalign 0.45
        yalign 0.15
        image "images/icons/info.webp"
        action Function(set_setting, "journal_goals_show_note_setting", not get_setting("journal_goals_show_note_setting"))
        tooltip note_tooltip

    python:

        show_completed = get_setting("journal_goals_show_completed")

        if show_completed == None:
            show_completed = False
            set_setting("journal_goals_show_completed", False)

    frame:
        # background Solid("#00000090")
        background Solid("#00000000")
        area (330, 300, 560, 600)

        viewport id "GoalList":
            mousewheel True
            draggable "touch"

            vbox:
                $ category_num = 0
                $ categories = list(quests.keys())
                $ categories.sort(key=lambda x: get_translation(x))

                for category in categories:
                    $ quests_list = [quest for quest in quests[category].keys() if (quests[category][quest].is_active() or (quests[category][quest].show_prematurely() and get_setting("journal_goals_show_note_setting"))) and (show_completed or not quests[category][quest].all_active_done())]
                    $ quest_list = [(get_translation(quest) if not quests[category][quest].all_active_done() else set_text_color(get_translation(quest), "#00a000"), f"{category}-?-{quest}") for quest in quests_list]
                    $ quest_list.sort(key=lambda x: x[0])
                    if len(quest_list) > 0:
                        $ category_num += 1
                        if display == "":
                            $ display = quest_list[0][1]
                        use journal_foldable_list(get_translation(category), 8, display, quest_list, f"quests_{category}_foldable_setting")

                if category_num == 0:
                    text "There are currently no quests :(" style "journal_text"

        vbar value YScrollValue("GoalList"):
            unscrollable "hide"
            xalign 1.04

    if show_completed:
        button:
            xalign 0.38
            yalign 0.25
            text "Hide Completed Quests":
                style "journal_desc"
            action [With(dissolveM), Function(set_setting, "journal_goals_show_completed", False)]
    else:
        button:
            xalign 0.38
            yalign 0.25
            text "Show Completed Quests":
                style "journal_desc"
            action [With(dissolveM), Function(set_setting, "journal_goals_show_completed", True)]

    if display != "":

        $ category, quest_key = display.split('-?-')
        $ quest = get_quest(category, quest_key)

        $ quest_description = quest.get_description()

        use journal_image(8, display, quest.get_thumbnail(), quest.get_thumbnail().replace('.webp', '_full.webp'), y_pos = 200, height = 280, wide = True)

        frame:
            # background Solid("#00000090")
            background Solid("#00000000")
            area (960, 480, 500, 500)
            
            viewport id "ProgressList":
                mousewheel True
                draggable "touch"

                vbox:
                    null height 10 
                    text quest_description style "journal_desc"

                    null height 20

                    for i, goal in quest.get_active_goals().items():
                        $ goal_finished = "☐"
                        if goal.is_completed():
                            $ goal_finished = "☑"
                        $ goal_text = f"{goal_finished}  {i}. {goal.get_description()}"

                        python:
                            display_goal = get_setting(f"show_goal_{goal.get_key()}")

                            if display_goal == None:
                                display_goal = True
                                set_setting(f"show_goal_{goal.get_key()}", True)

                            arrow = "▲  " if display_goal else "▼  "

                            goal_text = arrow + goal_text

                        button:
                            text goal_text: 
                                style "journal_desc"
                            action Function(set_setting, f"show_goal_{goal.get_key()}", not display_goal)

                        if display_goal:
                            $ progress_list = goal.get_progress()
                            if isinstance(progress_list, list):
                                for progress in progress_list:
                                    $ progress_text = f"    {progress}"
                                    text progress_text style "journal_desc_small"
                            else:
                                $ progress_text = f"    {progress_list}"
                                text progress_text style "journal_desc_small"

                    if quest.all_active_done():
                        null height 30

                        $ final_text = quest.get_finished_description()

                        text final_text style "journal_text"

            vbar value YScrollValue("ProgressList"):
                unscrollable "hide"
                xalign 1.04


    $ tooltip = GetTooltip()
    if tooltip:
        nearrect:
            focus "tooltip"
            prefer_top True

            frame:
                xalign 0.5
                text tooltip

screen journal_character(display):

    tag interaction_overlay
    modal True

    use school_overview_map
    use school_overview_stats

    image "journal/journal/background.webp"

    use journal_page_selector(9, display, char)

    key "K_ESCAPE" action [With(dissolveM), Jump("map_overview")]

    $ display_values = display.split(':')

    $ char_key = ""
    $ char_name = ""
    $ char_image = 0


    if len(display_values) >= 1:
        $ char_key = display_values[0]
    if len(display_values) >= 2:
        $ char_name = display_values[1]
    if len(display_values) >= 3:
        $ char_image = int(display_values[2])

    if char_name == "":
        # left side
        # displays all patrons with teacher tier subscription on Patreon
        frame:
            background Solid("#00000000")
            area (350, 200, 500, 750)

            vbox:
                text "Characters":
                    size 40
                    color "#000000"
                null height 20
                hbox:
                    viewport id "journal_character_keys":
                        mousewheel True
                        draggable "touch"

                        vbox:
                            for character_key in person_storage.keys():
                                if character_key == "NoView":
                                    continue
                                $ button_style = "buttons_idle"
                                if character_key == char_key:
                                    $ button_style = "buttons_selected"
                                $ key_title = get_translation(character_key)
                                textbutton key_title:
                                    text_style button_style
                                    action [With(dissolveM), Call("open_journal", 9, character_key)]
                    vbar value YScrollValue("journal_character_keys"):
                        unscrollable "hide"
                        xalign 1.0

        if char_key != "":
            frame:
                background Solid("#00000000")
                area (960, 200, 500, 700)

                viewport id "journal_character_values":
                    mousewheel True
                    draggable "touch"
                    $ grid_rows = int((len(person_storage[char_key].keys()) + 1) / 2)

                    grid 2 grid_rows:
                        spacing 4

                        for character_name in person_storage[char_key].keys():
                            $ name_title = get_translation(character_name)

                            button:
                                xsize 240
                                vbox:
                                    image person_storage[char_key][character_name].get_thumbnail():
                                        xsize 240
                                        ysize 427
                                    text name_title:
                                        xsize 240
                                        style "buttons_idle"
                                action [With(dissolveM), Call("open_journal", 9, f"{char_key}:{character_name}:-1")]
                vbar value YScrollValue("journal_character_values"):
                    unscrollable "hide"
                    xalign 1.05

    else:
        $ character = person_storage[char_key][char_name]
        $ character_images = character.get_portraits()
        $ character_images_length = len(character_images.keys())
        $ character_thumbnail = character.get_thumbnail()

        if char_image == -1:
            $ char_images_keys = character_images.keys()
            $ i = 0
            for key in char_images_keys:
                if character_images[key] == character_thumbnail:
                    $ char_image = i
                    break
                $ i += 1

        if char_image < 0:
            $ char_image = 0

        if char_image >= character_images_length:
            $ char_image = character_images_length - 1

        $ character_images_key = list(character_images.keys())[char_image]
        $ character_image = character_images[character_images_key]

        frame:
            background Solid("#00000000")
            area (350, 150, 500, 800)

            vbox:
                hbox:
                    xsize 500
                    textbutton "<- Return":
                        xalign 0.0
                        text_style "buttons_idle"
                        action [With(dissolveM), Call("open_journal", 9, f"{char_key}")]
                    
                    $ idle_image = "images/icons/favorite_disabled.webp"
                    $ hover_image = "images/icons/favorite_enabled.webp"
                    if character_image == character_thumbnail:
                        $ idle_image = "images/icons/favorite_enabled.webp"
                        $ hover_image = "images/icons/favorite_disabled.webp"

                    imagebutton:
                        idle idle_image
                        hover hover_image
                        xsize 50
                        ysize 50
                        xalign 1.0
                        action Function(character.set_thumbnail, character_image)

                hbox:
                    xsize 500
                    hbox:
                        xalign 0.5
                        if char_image != 0:
                            textbutton "<":
                                xsize 50
                                text_style "buttons_idle"
                                action [With(dissolveM), Call("open_journal", 9, f"{char_key}:{char_name}:{char_image - 1}")]
                        else:
                            null width 50
                        button:
                            xsize 300
                            text character_images_key:
                                xalign 0.5
                                style "journal_text"
                        if char_image < character_images_length - 1:
                            textbutton ">":
                                xsize 50
                                text_style "buttons_idle"
                                action [With(dissolveM), Call("open_journal", 9, f"{char_key}:{char_name}:{char_image + 1}")]
                        else:
                            null width 50

                null height 20

                image character_image:
                    xsize 393
                    ysize 700
                    xalign 0.5

        frame:
            background Solid("#00000000")
            area (960, 200, 500, 700)

            vbox:
                text get_translation(character.get_name()):
                    size 40
                    color "#000000"
                
                null height 20

                viewport id "journal_character_description":
                    mousewheel True
                    draggable "touch"

                    $ character_description = character.get_description_str()
                    text character_description:
                        style "journal_text"

                vbar value YScrollValue("journal_character_description"):
                    unscrollable "hide"
                    xalign 1.05

    $ tooltip = GetTooltip()
    if tooltip:
        nearrect:
            focus "tooltip"
            prefer_top True

            frame:
                xalign 0.5
                text tooltip

# endregion
########################

##########################
# region Journal Methods #
##########################

####################
# region Open Link #

label open_patreon_link():
    # """
    # Opens the patreon page in the default browser
    # """

    $ renpy.run(OpenURL(patreon))
    call open_journal(6, "") from open_patreon_link_1

label open_wiki_page():
    $ renpy.run(OpenURL(wiki))
    call open_journal(8, "") from open_wiki_page_1

# endregion
####################

##################
# region Gallery #

label reset_event_gallery(location, event):
    # """
    # Clears the persistent data for a specific event or location in persistent.gallery
    
    # ### Parameters:
    # 1. location: str
    #     - the location to be resetted
    # 2. event: str
    #     - the event to be resetted
    # """

    $ reset_gallery(location, event)

    if location not in persistent.gallery.keys():
        $ location = ""

    call open_journal(7, location) from reset_event_gallery_1

label dump_gallery_data(page, display):
    # """
    # Clears the persistent data for the entire gallery in persistent.gallery

    # ### Parameters:
    # 1. page: int
    #     - the page to be opened after the reset
    # 2. display: str
    #     - the display to be opened after the reset
    # """

    $ log_json("gallery_data", persistent.gallery)

    $ renpy.notify("Dumped gallery data!")

    call open_journal(page, display) from dump_gallery_data_1

label reset_gallery_cheat(page, display):
    # """
    # Clears the persistent data for the entire gallery in persistent.gallery

    # ### Parameters:
    # 1. page: int
    #     - the page to be opened after the reset
    # 2. display: str
    #     - the display to be opened after the reset
    # """

    $ reset_gallery()

    $ renpy.notify("Reset gallery!")

    call open_journal(page, display) from reset_gallery_cheat_1

label start_gallery_composite_replay(location, event, gallery_chooser, fragments, display):
    # """
    # Starts the replay of a specific event with the selected values

    # ### Parameters:
    # 1. location: str
    #     - the location of the event
    # 2. event: str
    #     - the event to be replayed
    # 3. gallery_chooser: dict
    #     - the selected values for the event
    # 4. display: str
    #     - the display to be opened after the replay
    # """

    # prepare data for the kwargs
    $ is_in_replay = True
    $ event_obj = get_event_from_register(event)

    $ gallery_chooser['in_replay'] = True
    $ gallery_chooser['journal_display'] = display
    $ gallery_chooser['in_event'] = True

    $ gallery_chooser['replay_frag_list'] = [get_event_from_register(event_name) for event_name in fragments if is_event_registered(event_name)]

    $ gallery_chooser['event_name'] = event
    $ gallery_chooser['event_obj'] = event_obj
    $ gallery_chooser['event_type'] = event_obj.event_type
    $ gallery_chooser['event_form'] = 'composite'
    $ gallery_chooser['image_patterns'] = event_obj.get_pattern()

    $ gallery_chooser['decision_data'] = persistent.gallery[location][event]['decisions']

    # $ i = 0
    # while i < len(gallery_chooser['frag_order']):
    #     $ frag_obj = gallery_chooser['frag_order'][i]
    #     $ j = 0
    #     $ last_data = get_last_data('fragment', frag_obj.get_id())
    #     $ data_keys = list(last_data.keys())
    #     while j < len(data_keys):
    #         $ data_key = data_keys[j]
    #         $ gallery_chooser[frag_obj.get_id() + '.' + data_key] = last_data[data_key]
    #         $ j += 1
    #     $ i += 1

    $ replay_data = gallery_chooser
    
    $ hide_all()

    # call event
    $ renpy.call("call_event", event_obj.get_event_label(), event_obj.priority, **gallery_chooser)

label start_gallery_replay(location, event, gallery_chooser, display):
    # """
    # Starts the replay of a specific event with the selected values

    # ### Parameters:
    # 1. location: str
    #     - the location of the event
    # 2. event: str
    #     - the event to be replayed
    # 3. gallery_chooser: dict
    #     - the selected values for the event
    # 4. display: str
    #     - the display to be opened after the replay
    # """

    # prepare data for the kwargs
    $ is_in_replay = True
    $ gallery_chooser['in_replay'] = True
    $ gallery_chooser['journal_display'] = display
    $ gallery_chooser['in_event'] = True
    $ gallery_chooser['event_name'] = event

    $ event_obj = get_event_from_register(event)

    $ gallery_chooser['image_patterns'] = event_obj.get_pattern()

    $ gallery_chooser['decision_data'] = persistent.gallery[location][event]['decisions']
    $ replay_data = gallery_chooser
    
    $ hide_all()

    # call event
    $ renpy.call(event, **gallery_chooser)

# endregion
##################

#########################
# region Journal Helper #

label set_journal_setting(page, display, setting, value):
    # """
    # Sets a specific setting in the journal

    # ### Parameters:
    # 1. page: int
    #     - the page to be opened after the time change
    # 2. display: str
    #     - the display to be opened after the time change
    # 3. setting: str
    #     - the setting to be set
    # 4. value: bool
    #     - the value to be set
    # """

    $ set_setting("journal_setting_" + str(page) + "_" + setting, value)
    call open_journal(page, display) from set_journal_setting_1

label call_max_image_from_journal(image_path, journal, display):
    # """
    # Calls the max_image screen with the given image path and opens the journal afterwards

    # ### Parameters:
    # 1. image_path: str
    #     - the path to the image to be displayed
    # 2. journal: int
    #     - the page to be opened after the image is displayed
    # 3. display: str
    #     - the display to be opened after the image is displayed
    # """

    hide screen school_overview_buttons
    call screen max_image_from_journal(image_path, journal, display) with dissolveM

label call_max_image_from_cheats(image_path, journal, display):
    # """
    # Calls the max_image screen with the given image path and opens the journal afterwards

    # ### Parameters:
    # 1. image_path: str
    #     - the path to the image to be displayed
    # 2. journal: int
    #     - the page to be opened after the image is displayed
    # 3. display: str
    #     - the display to be opened after the image is displayed
    # """

    hide screen school_overview_buttons
    call screen max_image_from_journal(image_path, journal, display) with dissolveM

# endregion
#########################

########################
# region Cheat Methods #

label switch_debug_mode(page, display, value = None):
    # """
    # Switches the debug mode on or off

    # ### Parameters:
    # 1. page: int
    #     - the page to be opened after the time change
    # 2. display: str
    #     - the display to be opened after the time change
    # 3. value: bool (default: None)
    #     - the value to be set
    #     - if value is None the debug mode is toggled
    # """

    if debug_mode == None:
        $ debug_mode = True
    elif value == None:
        $ debug_mode = value
    else:
        $ debug_mode = not debug_mode

    if debug_mode:
        $ renpy.notify("Debug mode activated!")
    else:
        $ renpy.notify("Debug mode deactivated!")
    call open_journal(page, display) from switch_debug_mode_1

label switch_event_select_mode(page, display, value = None):
    # """
    # Switches the debug mode on or off

    # ### Parameters:
    # 1. page: int
    #     - the page to be opened after the time change
    # 2. display: str
    #     - the display to be opened after the time change
    # 3. value: bool (default: None)
    #     - the value to be set
    #     - if value is None the debug mode is toggled
    # """

    if event_selection_mode == None:
        $ event_selection_mode = True
    elif value == None:
        $ event_selection_mode = value
    else:
        $ event_selection_mode = not event_selection_mode

    if event_selection_mode:
        $ renpy.notify("Event selection mode activated!")
    else:
        $ renpy.notify("Event selection mode deactivated!")
    call open_journal(page, display) from switch_event_select_mode_1

label switch_time_freeze(page, display, value = None):
    # """
    # Switches the time freeze on or off

    # ### Parameters:
    # 1. page: int
    #     - the page to be opened after the time change
    # 2. display: str
    #     - the display to be opened after the time change
    # 3. value: bool (default: None)
    #     - the value to be set
    #     - if value is None the time freeze is toggled
    # """

    if time_freeze == None:
        $ time_freeze = True
    elif value == None:
        $ time_freeze = value
    else:
        $ time_freeze = not time_freeze
    if time_freeze:
        $ renpy.notify("Time is now frozen!")
    else:
        $ renpy.notify("Time is not frozen anymore!")
    call open_journal(page, display) from switch_time_freeze_1

label set_time_cheat(page, display, **kwargs):
    # """
    # Sets the time to a specific date and time

    # ### Parameters:
    # 1. page: int
    #     - the page to be opened after the time change
    # 2. display: str
    #     - the display to be opened after the time change
    # 3. **kwargs: dict
    #     - the time to be set
    #     - day: int
    #         - the day to be set
    #     - month: int
    #         - the month to be set
    #     - year: int
    #         - the year to be set
    #     - daytime: int
    #         - the daytime to be set
    # """

    $ time.set_time(**kwargs)

    # checks if the time set is before the actual start if the game
    if time.compare_now(10, 1, 2023, 2) == -1:
        $ time.set_time(day = 10, month = 1, year = 2023, daytime = 2)

    call open_journal(page, display) from set_time_cheat_1

label change_time_cheat(page, display, **kwargs):
    # """
    # Adds a specific amount of time to the current time
    #
    # ### Parameters:
    # 1. page: int
    #     - the page to be opened after the time change
    # 2. display: str
    #     - the display to be opened after the time change
    # 3. **kwargs: dict
    #     - the time to be added
    #     - day: int
    #         - the days to be added
    #     - month: int
    #         - the months to be added
    #     - year: int
    #         - the years to be added
    #     - daytime: int
    #         - the daytime to be added
    # """

    $ time.add_time(**kwargs)

    # checks if the time set is before the actual start if the game
    if time.compare_today(10, 1, 2023) == -1:
        $ time.set_time(day = 10, month = 1, year = 2023, daytime = time.get_daytime())

    # checks if the time set is before the actual start if the game
    if time.compare_now(10, 1, 2023, 2) == -1:
        $ time.set_time(day = 10, month = 1, year = 2023, daytime = 2)

    call open_journal(page, display) from change_time_cheat_1

label switch_mod(mod_key, state):
    $ persistent.modList[mod_key]['active'] = state
    call open_journal(5, 'mods') from call_open_journal_switch_mod_1

label switch_rule(rule_name):
    # """
    # Switches the unlock state of a rule

    # ### Parameters:
    # 1. rule_name: str
    #     - the name of the rule to be switched
    # """

    $ rule = get_rule(rule_name)
    $ rule.unlock(not rule.is_unlocked())
    call open_journal(5, "rules") from switch_rule_1

label switch_club(club_name):
    # """
    # Switches the unlock state of a club

    # ### Parameters:
    # 1. club_name: str
    #     - the name of the club to be switched
    # """

    $ club = get_club(club_name)
    $ club.unlock(not club.is_unlocked())
    call open_journal(5, "clubs") from switch_club_1

label switch_building(building_name, level_delta = -1000):
    # """
    # Switches the unlock state of a building or upgrades it by a specific amount

    # ### Parameters:
    # 1. building_name: str
    #     - the name of the building to be switched
    # 2. level_delta: int (default: -1000)
    #     - the amount to be added to the level of the building
    #     - if level_delta is -1000 the building is unlocked or locked
    # """

    $ building = get_building(building_name)

    if level_delta == -1000:
        $ building.unlock(not building.is_unlocked())
    else:
        $ building.set_level(building.get_level() + level_delta)
    call open_journal(5, "buildings") from switch_building_1

label modify_stat(stat, amount, char = "school"):
    # """
    # Modifies a specific stat of a character

    # ### Parameters:
    # 1. stat: str
    #     - the stat to be modified
    # 2. amount: int
    #     - the amount to be added to the stat
    # 3. char: str
    #     - the character to be modified
    #     - only needed when stat is not money
    # """

    $ char_obj = get_character_by_key(char)
    if stat == "money":
        $ money.change_value(amount)
    elif stat == "level":
        $ char_obj.set_level(char_obj.get_level() + amount)
    else:
        $ char_obj.change_stat(stat, amount)
    call open_journal(5, "stats", char) from modify_stat_1

# endregion
########################

#########################
# region Propose Object #

label add_to_proposal(data, page, display, action = "unlock"):
    # """
    # Adds a specific object to the proposal for voting

    # ### Parameters:
    # 1. data: object
    #     - the object to be added to the proposal
    # 2. page: int
    #     - the page to be opened after the object is added to the proposal
    # 3. display: str
    #     - the display to be opened after the object is added to the proposal
    # 4. action: str (default: "unlock")
    #     - the action to be performed on the object
    #     - if action is "unlock" the object is added to the proposal for unlocking
    #     - if action is "upgrade" the object is added to the proposal for upgrading
    # """

    $ currentProposal = get_game_data("voteProposal")

    if currentProposal != None:
        $ vote_obj = currentProposal._journal_obj
        $ money_conditions = [condition for condition in vote_obj.get_conditions() if isinstance(condition, MoneyCondition)]
        python:
            for condition in money_conditions:
                release_money("vote_" + condition.get_name() + "_" + vote_obj.get_name())

    $ money_conditions = [condition for condition in data.get_conditions() if isinstance(condition, MoneyCondition)]
    python:
        for condition in money_conditions:
            reserve_money("vote_" + condition.get_name() + "_" + data.get_name(), condition.value)

    $ proposal = PTAProposal(data, action)
    $ set_game_data("voteProposal", proposal)
    $ update_quest("schedule_voting", proposal = proposal)
    call open_journal(page, display) from add_to_proposal_1

label add_rule_to_proposal(rule_name):
    # """
    # Adds a specific rule to the proposal for voting

    # ### Parameters:
    # 1. rule_name: str
    #     - the name of the rule to be added to the proposal
    # """

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
    # """
    # Adds a specific club to the proposal for voting

    # ### Parameters:
    # 1. club_name: str
    #     - the name of the club to be added to the proposal
    # """

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
    # """
    # Adds a specific building to the proposal for voting

    # ### Parameters:
    # 1. building_name: str
    #     - the name of the building to be added to the proposal
    # """

    $ building = get_building(building_name)

    $ action = "unlock"
    if building.is_unlocked():
        $ action = "upgrade"

    $ voteProposal = get_game_data("voteProposal")
    if voteProposal != None:
        $ title = "the " + voteProposal._journal_obj.get_type() + " \"" + voteProposal._journal_obj.get_title() + "\""
        $ building_title = building.get_title()
        if building == None:
            return
        call screen confirm("You already scheduled [title] for voting.\n\nDo you wanna schedule the building \"[building_title]\" instead?",
            Call("add_to_proposal", building, 4, building_name, action),
            Call("open_journal", 4, building_name))

    call add_to_proposal(building, 4, building_name, action) from add_building_to_proposal_2

# endregion
#########################

# endregion
##########################