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
    
    def parse_situation_journal_display(display: str):
        """
        Split a situations journal display into situation key and optional tab.

        Situation keys may contain colons (e.g. unlockable keys ``rule:level:3``).
        Tabs are only the known suffixes ``passives`` and ``notes``, or a trailing
        colon for the overview tab.

        Args:
            display (str): Journal display value.

        Returns:
            tuple[str, str]: (situation_key, situation_tab).
        """
        if display is None or display == "":
            return ("", "")
        if display.endswith(":"):
            return (display[:-1], "")
        for tab in ("passives", "notes"):
            suffix = ":" + tab
            if display.endswith(suffix):
                return (display[:-len(suffix)], tab)
        return (display, "")

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
        call screen journal_inventory(display, 2) with dissolveM
    elif page == 3:
        call screen journal_overview(display, char) with dissolveM
    elif page == 4:
        call screen journal_unlockables(display) with dissolveM
    elif page == 5:
        call screen journal_cheats(display, char) with dissolveM
    elif page == 6:
        call screen journal_credits(display) with dissolveM
    elif page == 7:
        call screen journal_gallery(display) with dissolveM
    elif page == 8:
        call screen journal_situations(display) with dissolveM
    elif page == 9:
        call screen journal_character(display) with dissolveM
    elif page == 10:
        call screen journal_inventory(display, 10) with dissolveM

label close_journal ():
    # """
    # A label used to close the journal screen
    # """

    hide screen journal
    jump map_entry

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
style journal_note_timestamp:
    color "#555555"
    size 14
    italic True
style journal_note_type:
    size 14
    bold True
style journal_note_interpretation:
    color "#444444"
    size 15
    italic True

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

style buttons_idle_small:
    color "#000"
    hover_color gui.hover_color
    size 20

style buttons_inactive take buttons_idle:
    color gui.button_text_insensitive_color
    size 30

style buttons_inactive_small take buttons_idle_small:
    color gui.button_text_insensitive_color
    size 20

style buttons_selected take buttons_idle:
    color gui.hover_muted_color

style buttons_selected_small take buttons_idle_small:
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

screen journal_log_json_entry(entry):
    # """
    # Renders a JSON log entry header plus expandable flat tree rows.
    # """

    $ log_line = format_game_log_entry(entry)
    $ root_path = "logjson." + str(entry.get("id", 0))
    $ root_data = entry.get("data")
    $ marker = "▼" if is_log_json_expanded(root_path) else "▶"
    $ summary = escape_renpy_log_text(format_log_json_summary(root_data))
    $ root_label = marker + " " + summary

    text log_line:
        style "journal_text"
        size 14
        xmaximum 520

    textbutton root_label:
        text_style "buttons_idle"
        text_size 13
        xmaximum 520
        action Function(toggle_log_json_node, root_path)

    if is_log_json_expanded(root_path):
        $ json_rows = get_log_json_tree_rows(root_data, root_path, 1)
        for row in json_rows:
            $ indent = min(row["depth"], 8) * 12
            $ key_text = escape_renpy_log_text(str(row["key"])) if row["key"] is not None else ""
            $ value_text = escape_renpy_log_text(row["summary"])
            if row["is_branch"]:
                $ row_marker = "▼" if row["expanded"] else "▶"
                $ branch_label = row_marker + " " + key_text + ": " + value_text
                hbox:
                    null width indent
                    textbutton branch_label:
                        text_style "buttons_idle"
                        text_size 13
                        xmaximum 520 - indent
                        action Function(toggle_log_json_node, row["path"])
            else:
                if row["key"] is not None:
                    $ leaf_label = key_text + ": " + value_text
                else:
                    $ leaf_label = value_text
                hbox:
                    null width indent
                    text leaf_label:
                        style "journal_text"
                        size 13
                        xmaximum 520 - indent

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
        elif page == 10:
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
            if page != 2 and page != 10:
                key "K_3" action [With(dissolveM), Call("open_journal", 2, "")]
                key "K_KP3" action [With(dissolveM), Call("open_journal", 2, "")]
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
        if page != 2 and page != 10:
            $ text = ("Inventory" + key_text).replace("x", "3")
            hotspot (144, 617, 168, 88) action  [With(dissolveM), Call("open_journal", 2, "")] tooltip text
        if page != 4:
            $ text = ("Unlockables" + key_text).replace("x", "5")
            hotspot (144, 830, 168, 88) action [With(dissolveM), Call("open_journal", 4, "")] tooltip text
        if page != 6:
            $ text = ("Credits" + key_text).replace("x", "6")
            hotspot (1500, 246, 179, 87) action [With(dissolveM), Call("open_journal", 6, "")] tooltip text
        if page != 7:
            $ text = ("Replay" + key_text).replace("x", "7")
            hotspot (1493, 356, 185, 87) action [With(dissolveM), Call("open_journal", 7, "")] tooltip text
        if page != 8:
            $ text = ("Situations" + key_text).replace("x", "2")
            hotspot (154, 358, 166, 93) action [With(dissolveM), Call("open_journal", 8, "")] tooltip text
        
    
    # if page == 1 or (page == 5 and display == 'stats'):
    #     if char == "school":
    #         if has_keyboard():
    #             key "K_TAB" action [With(dissolveM), Call("open_journal", page, display, "teacher")]
    #         image "journal/journal/school_hover.webp":
    #             xpos 365
    #             ypos 74
    #         text "School":
    #             xalign 0.225 yalign 0.1
    #             size 20
    #             color "#fff"
    #     else:
    #         imagebutton:
    #             idle "journal/journal/school_idle.webp"
    #             hover "journal/journal/school_hover.webp"
    #             xpos 365
    #             ypos 74
    #             tooltip "School"
    #             action [With(dissolveM), Call("open_journal", page, display, "school")]
    #     if char == "teacher":
    #         if has_keyboard():
    #             key "K_TAB" action [With(dissolveM), Call("open_journal", page, display, "parent")]
    #         image "journal/journal/teacher_hover.webp":
    #             xpos 541
    #             ypos 75
    #         text "Teacher":
    #             xalign 0.3225 yalign 0.1
    #             size 20
    #             color "#fff"
    #     else:
    #         imagebutton:
    #             idle "journal/journal/teacher_idle.webp"
    #             hover "journal/journal/teacher_hover.webp"
    #             xpos 541
    #             ypos 75
    #             tooltip "Teacher"
    #             action [With(dissolveM), Call("open_journal", page, display, "teacher")]
    #     if char == "parent":
    #         if has_keyboard():
    #             key "K_TAB" action [With(dissolveM), Call("open_journal", page, display, "school")]
    #         image "journal/journal/parent_hover.webp":
    #             xpos 718
    #             ypos 76
    #         text "Parents":
    #             xalign 0.415 yalign 0.1
    #             size 20
    #             color "#fff"
    #     else:
    #         imagebutton:
    #             idle "journal/journal/parent_idle.webp"
    #             hover "journal/journal/parent_hover.webp"
    #             xpos 718
    #             ypos 76
    #             tooltip "Parents"
    #             action [With(dissolveM), Call("open_journal", page, display, "parent")]

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

    
    if has_keyboard():  
        if page != 2 and page != 10:
            key "K_0" action [With(dissolveM), Call("open_journal", 2, "")]
            key "K_KP0" action [With(dissolveM), Call("open_journal", 2, "")]
    if page != 2 and page != 10:
        $ text = ("Inventory" + key_text).replace("x", "0")
        imagebutton:
            idle "journal/journal/top_tag_1_idle.webp"
            hover "journal/journal/top_tag_1_hover.webp"
            xpos 365
            ypos 74
            tooltip text
            action [With(dissolveM), Call("open_journal", 2, display)]
    else:
        image "journal/journal/top_tag_1_hover.webp":
            xpos 365
            ypos 74
        text "Inventory":
            xalign 0.225 yalign 0.1
            size 20
            color "#fff"

    $ text = ("Close Journal" + key_text).replace("x", "ESC")

    imagebutton:
        idle "journal/journal/close_idle.webp"
        hover "journal/journal/close_hover.webp"
        tooltip text
        xpos 1509
        ypos 836
        action [With(dissolveM), Jump("map_entry")]

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

    $ active_obj_list_conditions_list = active_obj.get_list_conditions_list(cond_type = action_text, char_obj = get_school())

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

    $ resolved_j_image = find_loadable_image(j_image)
    if resolved_j_image == "":
        $ j_image = "images/journal/empty_image.webp"
        if wide:
            $ j_image = "images/journal/empty_image_wide.webp"
        $ full_image = None
    else:
        $ j_image = resolved_j_image

    $ width = height
    if wide:
        $ width = int(height / 9 * 16)

    $ resolved_full_image = find_loadable_image(full_image) if full_image != None else ""
    if resolved_full_image != "":
        button:
            xpos x_pos ypos y_pos
            add j_image: 
                xsize width
                ysize height
            action [With(dissolveM), Call("call_max_image_from_journal", resolved_full_image, page, display)]
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
        $ stat_text += f" ({char})"
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
    null height 10

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
    button:
        xpos -6 ypos -6
        xsize 1920 ysize 1080
        add "[image_path]":
            xpos 0 ypos 0
            xsize 1920 ysize 1080
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

    $ modifier_weekly = get_modifier_lists('money', 'payroll_weekly')
    $ modifier_monthly = get_modifier_lists('money', 'payroll_monthly')

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

screen journal_tab_selection(page, display, selection, endpoint_label, *options, **kwargs):
    # """
    # A screen used to display the tab selection for the journal

    # ### Parameters:
    # 1. page: int
    #     - The page number to display.
    # 2. display: str
    #     - The display type for the journal page.
    # 3. selection: str
    #     - The currently selected tab.
    # 4. endpoint_label: str
    #     - The label of the endpoint to call when a tab is selected.
    # 5. *options: List[str]
    #     - The list of options to display in the tab selection.
    # 6. **kwargs: Dict[str, Any]
    #     - Additional keyword arguments to pass to the frame.
    #     - possible kwargs:
    #         - size: Tuple[int, int, int, int] (default: (989, 200, 500, 250))
    #             - The size of the tab selection.
    # """

    $ (xpos, ypos, width, height) = get_kwargs('size', (989, 200, 500, 250), **kwargs)

    frame:
        background Solid("#0000")
        area (xpos, ypos, width, height)
        viewport id "Tab_Selection":
            mousewheel True
            draggable "touch"

            hbox:
                for tab in options:
                    if tab != selection:
                        textbutton tab:
                            text_style "buttons_idle"
                            action Call(endpoint_label, tab, page, display)
                    else:
                        textbutton tab:
                            text_style "buttons_active"
                            action NullAction()
                    null width 5

        bar value XScrollValue("Tab_Selection"):
            unscrollable "hide"
            yalign 1

# endregion
##############################

########################
# region Main Journals #
########################

# Unlockables (4)
screen journal_unlockables(display):
    # """
    # Journal page for unlockables: filtered list on the left, detail on the right.

    # ### Parameters:
    # 1. display: str
    #     - Unlockable selection as ``key`` or ``key:view_index``.
    # """

    tag interaction_overlay
    modal True

    use school_overview_map
    use school_overview_stats

    image "journal/journal/background.webp"

    key "K_ESCAPE" action [With(dissolveM), Jump("map_entry")]

    use journal_page_selector(4, display)

    text "Unlockables":
        xalign 0.25
        yalign 0.2
        size 60
        color "#000"

    python:
        type_filter = get_setting("journal_unlockables_type_filter")
        if type_filter is None:
            type_filter = ""
            set_setting("journal_unlockables_type_filter", "")

    $ type_keys = unlockable_manager.get_type_keys()
    $ incomplete_list, completed_list = unlockable_manager.get_list_entries(type_filter)
    $ unlockable_key, view_index = unlockable_manager.parse_display(display)
    $ list_display = unlockable_key

    if display == "" or unlockable_manager.resolve_display(display) is None:
        $ display = ""
        $ list_display = ""
        if len(incomplete_list) != 0:
            $ display = incomplete_list[0][1]
            $ list_display = display
        elif len(completed_list) != 0:
            $ display = completed_list[0][1]
            $ list_display = display
        $ unlockable_key, view_index = unlockable_manager.parse_display(display)

    # type_key filter
    frame:
        background Solid("#0000")
        area (330, 250, 560, 45)

        hbox:
            spacing 12
            $ all_style = "buttons_selected" if type_filter == "" else "buttons_idle"
            textbutton "All":
                text_style all_style
                action [Function(set_setting, "journal_unlockables_type_filter", ""), With(dissolveM), Call("open_journal", 4, display)]
            for type_key in type_keys:
                $ type_title = get_translation(type_key)
                $ type_style = "buttons_selected" if type_filter == type_key else "buttons_idle"
                textbutton "[type_title]":
                    text_style type_style
                    action [Function(set_setting, "journal_unlockables_type_filter", type_key), With(dissolveM), Call("open_journal", 4, display)]

    # left lists
    frame:
        background Solid("#00000000")
        area (330, 300, 560, 600)

        viewport id "UnlockablesList":
            mousewheel True
            draggable "touch"

            vbox:
                use journal_foldable_list("Incomplete", 4, list_display, incomplete_list, "journal_setting_4_incomplete")
                null height 20
                use journal_foldable_list("Completed", 4, list_display, completed_list, "journal_setting_4_completed", "buttons_active")

        vbar value YScrollValue("UnlockablesList"):
            unscrollable "hide"
            xalign 1.0

    if display != "":
        $ active_unlockable = unlockable_manager.resolve_display(display)
        if active_unlockable is not None:
            $ unlockable_key = active_unlockable.unlockable_key
            $ navigable_indices = unlockable_manager.get_navigable_indices(unlockable_key)
            $ current_index = active_unlockable.group_index

            # group prev / next
            if len(navigable_indices) > 1 and current_index in navigable_indices:
                $ nav_pos = navigable_indices.index(current_index)
                if nav_pos > 0:
                    $ prev_display = unlockable_manager.build_display(unlockable_key, navigable_indices[nav_pos - 1])
                    textbutton "<":
                        xpos 960
                        ypos 175
                        text_style "buttons_idle"
                        action [With(dissolveM), Call("open_journal", 4, prev_display)]
                if nav_pos < len(navigable_indices) - 1:
                    $ next_display = unlockable_manager.build_display(unlockable_key, navigable_indices[nav_pos + 1])
                    textbutton ">":
                        xpos 1420
                        ypos 175
                        text_style "buttons_idle"
                        action [With(dissolveM), Call("open_journal", 4, next_display)]

                text "[current_index]":
                    xpos 1180
                    ypos 180
                    size 24
                    color "#000"

            $ unlockable_thumbnail = active_unlockable.get_current_thumbnail()
            if unlockable_thumbnail is None:
                $ unlockable_thumbnail = "images/journal/empty_image.webp"

            use journal_image(4, display, unlockable_thumbnail, unlockable_thumbnail, x_pos = 985, y_pos = 220, height = 280, wide = True)

            $ unlockable_descriptions = active_unlockable.get_descriptions()
            $ pictogram_data = active_unlockable.get_pictogram_data()
            $ pictogram_list = list(pictogram_data.values())
            $ pictogram_count = len(pictogram_list)
            $ pictogram_max_cols = 5
            python:
                # Even row sizes with max 5 cols: prefer fewer rows (9 → 5+4, not 3+3+3).
                pictogram_row_slices = []
                if pictogram_count > 0:
                    row_count = (pictogram_count + pictogram_max_cols - 1) // pictogram_max_cols
                    base_size = pictogram_count // row_count
                    extra = pictogram_count % row_count
                    offset = 0
                    for row_i in range(row_count):
                        size = base_size + (1 if row_i < extra else 0)
                        pictogram_row_slices.append(pictogram_list[offset:offset + size])
                        offset += size

            # Pictograms under the image, description below — shared scroll viewport
            frame:
                background Solid("#0000")
                area (985, 510, 500, 280)
                viewport id "UnlockableDetail":
                    mousewheel True
                    draggable "touch"
                    vbox:
                        spacing 8
                        if pictogram_count > 0:
                            vbox:
                                spacing 4
                                xfill True
                                for pic_row in pictogram_row_slices:
                                    hbox:
                                        xalign 0.5
                                        spacing 4
                                        for pic_entry in pic_row:
                                            $ pic_icon = pic_entry.get("icon")
                                            $ pic_icon = find_loadable_image(pic_icon) if pic_icon is not None else ""
                                            $ pic_label = pic_entry.get("label") or ""
                                            $ pic_tooltip = pic_entry.get("tooltip") or pic_label
                                            button:
                                                xsize 92
                                                ysize 72
                                                action NullAction()
                                                tooltip pic_tooltip
                                                vbox:
                                                    xalign 0.5
                                                    spacing 2
                                                    if pic_icon:
                                                        add pic_icon:
                                                            xsize 48
                                                            ysize 48
                                                            xalign 0.5
                                                    else:
                                                        null height 48
                                                    if pic_label != "":
                                                        text pic_label:
                                                            size 12
                                                            color "#000"
                                                            xalign 0.5
                                                            textalign 0.5
                                                            xmaximum 90
                            null height 12

                        for desc in unlockable_descriptions:
                            textbutton desc:
                                text_style "journal_desc"
                                yalign 0.5
                                action NullAction()

                vbar value YScrollValue("UnlockableDetail"):
                    unscrollable "hide"
                    xalign 1.04
            frame:
                background Solid("#0000")
                area (985, 800, 500, 120)
                viewport id "UnlockableVoteResolutionDetail":
                    mousewheel True
                    draggable "touch"
                    for resolution_key, resolution in active_unlockable.resolutions.items():
                        if resolution_key== "vote_passed":
                            vbox:
                                spacing 2
                                text "When Passed following Effects will Occur":
                                    yalign 0.1
                                    color "#000"
                                    size 14
                                for effect in resolution.effects.effects:
                                    text f"{effect.__str__()}":
                                        size 12
                                        color "#000"
                vbar value YScrollValue("UnlockableVoteResolutionDetail"):
                    unscrollable "hide"
                    xalign 1.04

            $ unlockable_status = active_unlockable.status
            if unlockable_status == "inactive":
                textbutton "Start Introducing":
                    xpos 985
                    yalign 0.9
                    text_style "buttons_idle"
                    action Call("start_unlockable_situation", display)
            elif unlockable_status == "active":
                textbutton "View Situation":
                    xpos 985
                    yalign 0.83
                    text_style "buttons_idle"
                    action [With(dissolveM), Call("open_journal", 8, active_unlockable.key)]
            else:
                textbutton "(Completed) View Situation":
                    xpos 985
                    yalign 0.83
                    text_style "buttons_idle"
                    action [With(dissolveM), Call("open_journal", 8, active_unlockable.key)]

    $ tooltip = GetTooltip()
    if tooltip:
        nearrect:
            focus "tooltip"
            prefer_top True

            frame:
                xalign 0.5
                text tooltip

# School Overview (1)
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

    key "K_ESCAPE" action [With(dissolveM), Jump("map_entry")]

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
    if pta_proposal is not None and not isinstance(pta_proposal, Unlockable):
        $ clean_legacy_vote_proposal()
        $ pta_proposal = None

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
                if isinstance(pta_proposal, Unlockable):
                    $ pta_type = pta_proposal.type_key.capitalize()
                    $ pta_title = "\"" + pta_proposal.get_title() + "\""
                    if pta_proposal.group_index != -1:
                        $ pta_display = unlockable_manager.build_display(pta_proposal.unlockable_key, pta_proposal.group_index)
                    else:
                        $ pta_display = pta_proposal.unlockable_key
                    text "[pta_type] scheduled for pta-meeting:" style "journal_text" size 27
                    textbutton "[pta_title]":
                        text_style "journal_pta_overview"
                        action [With(dissolveM), Call("open_journal", 4, pta_display)]

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

# Cheats (5)
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

    key "K_ESCAPE" action [With(dissolveM), Jump("map_entry")]

    use journal_page_selector(5, display, char)

    text "Cheats":
        xalign 0.72 yalign 0.11
        size 20
        color "#000"

    $ options = {
        "general": "General",
        "events": "Events",
        "situations": "Situations",
        "unlockables": "Unlockables",
        "items": "Items",
        "debug": "Debug",
        "logs": "Logs",
        "stats": "Stats",
        "buildings": "Buildings",
        "mods": "Mods",
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
                    
                    
            vbar value YScrollValue("CheatStatList"):
                unscrollable "hide"
                xalign 1.0
    elif display == "events":
        frame:
            background Solid("#0000")
            area (950, 200, 560, 690)

            viewport id "CheatEventList":
                mousewheel True
                draggable "touch"
                vbox:
                    text "Start any registered event directly via its Event.call().\nFilter by replay category. Starting an event closes the journal.\nProceed on your own risk.":
                        color "#000000"
                        size 18

                    null height 15

                    hbox:
                        button:
                            text "Category" xalign 0.0 style "journal_text"
                            xsize 180
                        button:
                            text "[event_cheat_category]" xalign 1.0 style "buttons_idle"
                            action [With(dissolveM), Call("cycle_event_cheat_filter", 5, display)]
                            xsize 320

                    null height 10
                    image "journal/journal/left_list_separator.webp"
                    null height 10

                    $ cheat_events = get_filtered_cheat_events(event_cheat_category)
                    if len(cheat_events) == 0:
                        text "No events registered." style "journal_text" size 18
                    else:
                        for cheat_event in cheat_events:
                            $ cheat_event_id = cheat_event.event_id
                            $ cheat_event_name = cheat_event.get_name()
                            $ cheat_event_cat = getattr(cheat_event, "replay_category", "Misc")
                            button:
                                xfill True
                                action [With(dissolveM), Call("call_event_cheat", cheat_event_id)]
                                hbox:
                                    spacing 10
                                    text cheat_event_name:
                                        style "buttons_idle"
                                        size 20
                                        xsize 360
                                    text ("{color=#777777}" + cheat_event_cat + "{/color}"):
                                        size 16
                                        yalign 0.5
                            null height 4

            vbar value YScrollValue("CheatEventList"):
                unscrollable "hide"
                xalign 1.0
    elif display == "situations":
        frame:
            background Solid("#0000")
            area (950, 200, 560, 690)

            viewport id "CheatSituationList":
                mousewheel True
                draggable "touch"
                vbox:
                    text "Activate a situation, or activate all/individual teasers within it.\nExpand a situation to reach its single teasers.\nProceed on your own risk.":
                        color "#000000"
                        size 18

                    null height 15

                    $ cheat_situations = get_cheat_situation_list()
                    if len(cheat_situations) == 0:
                        text "No situations registered." style "journal_text" size 18
                    else:
                        for cheat_situation in cheat_situations:
                            $ sit_key = cheat_situation.key
                            $ sit_expanded = is_situation_cheat_expanded(sit_key)
                            $ sit_marker = "▼" if sit_expanded else "▶"
                            $ sit_state = cheat_situation.visibility_state
                            hbox:
                                spacing 8
                                textbutton sit_marker:
                                    text_style "buttons_idle"
                                    text_size 20
                                    action Function(toggle_situation_cheat_expand, sit_key)
                                text (cheat_situation.name + " {color=#777777}(" + sit_state + "){/color}"):
                                    style "journal_text"
                                    size 20
                                    yalign 0.5
                                    xsize 320
                            hbox:
                                null width 40
                                spacing 10
                                button:
                                    text "Activate" style "buttons_idle" size 18
                                    action [With(dissolveM), Call("activate_situation_cheat", sit_key)]
                                    sensitive cheat_situation.state != "active"
                                button:
                                    text "All Teasers" style "buttons_idle" size 18
                                    action [With(dissolveM), Call("activate_situation_teasers_cheat", sit_key)]
                            if sit_expanded:
                                if len(cheat_situation.teasers) == 0:
                                    hbox:
                                        null width 60
                                        text "No teasers." style "journal_text" size 16
                                else:
                                    for teaser_key in cheat_situation.teasers.keys():
                                        $ cheat_teaser = cheat_situation.teasers[teaser_key]
                                        $ teaser_active = cheat_teaser.active
                                        hbox:
                                            null width 60
                                            spacing 10
                                            if teaser_active:
                                                text ("{color=#00a000}✓{/color} " + teaser_key):
                                                    style "journal_text"
                                                    size 16
                                                    xsize 300
                                                    yalign 0.5
                                            else:
                                                text teaser_key:
                                                    style "journal_text"
                                                    size 16
                                                    xsize 300
                                                    yalign 0.5
                                            button:
                                                text "Activate" style "buttons_idle" size 16
                                                action [With(dissolveM), Call("activate_teaser_cheat", sit_key, teaser_key)]
                                                sensitive not teaser_active
                            null height 12

            vbar value YScrollValue("CheatSituationList"):
                unscrollable "hide"
                xalign 1.0
    elif display == "unlockables":
        frame:
            background Solid("#0000")
            area (950, 200, 560, 690)

            viewport id "CheatUnlockableList":
                mousewheel True
                draggable "touch"
                vbox:
                    text "Force the visibility of an unlockable on or off.\nVisible ON overrides the derived condition state (override_visible).\nProceed on your own risk.":
                        color "#000000"
                        size 18

                    null height 15

                    $ cheat_unlockables = get_cheat_unlockable_list()
                    if len(cheat_unlockables) == 0:
                        text "No unlockables registered." style "journal_text" size 18
                    else:
                        for cheat_unlockable in cheat_unlockables:
                            $ unlock_display = get_unlockable_cheat_display(cheat_unlockable)
                            $ unlock_override = getattr(cheat_unlockable, "override_visible", False)
                            $ unlock_name = cheat_unlockable.name
                            if cheat_unlockable.group_index != -1:
                                $ unlock_name = unlock_name + " (" + str(cheat_unlockable.group_index) + ")"
                            hbox:
                                spacing 8
                                text unlock_name:
                                    style "journal_text"
                                    size 18
                                    xsize 300
                                    yalign 0.5
                                if unlock_override:
                                    text "{color=#00a000}VISIBLE{/color}":
                                        size 18
                                        xsize 90
                                        yalign 0.5
                                    button:
                                        text "HIDE" xalign 0.5 style "buttons_idle" size 18
                                        action [With(dissolveM), Call("toggle_unlockable_visibility_cheat", unlock_display)]
                                        xsize 110
                                else:
                                    text "{color=#a00000}AUTO{/color}":
                                        size 18
                                        xsize 90
                                        yalign 0.5
                                    button:
                                        text "SHOW" xalign 0.5 style "buttons_idle" size 18
                                        action [With(dissolveM), Call("toggle_unlockable_visibility_cheat", unlock_display)]
                                        xsize 110
                            null height 8

            vbar value YScrollValue("CheatUnlockableList"):
                unscrollable "hide"
                xalign 1.0
    elif display == "items":
        frame:
            background Solid("#0000")
            area (950, 200, 560, 690)

            viewport id "CheatItemList":
                mousewheel True
                draggable "touch"
                vbox:
                    text "Add any registered item to your inventory.\nLeft-click ADD for +1, right-click for +10.\nProceed on your own risk.":
                        color "#000000"
                        size 18

                    null height 12

                    hbox:
                        button:
                            text "Add all items (1x each)" xalign 0.0 style "journal_text" size 20
                            action [With(dissolveM), Call("give_every_item", 5, "items")]

                    null height 10
                    image "journal/journal/left_list_separator.webp"
                    null height 10

                    $ cheat_items = get_cheat_item_list()
                    if len(cheat_items) == 0:
                        text "No items registered." style "journal_text" size 18
                    else:
                        for cheat_item in cheat_items:
                            $ cheat_item_key = cheat_item.key
                            $ cheat_item_count = inventory_manager.get_item_count(cheat_item_key)
                            hbox:
                                spacing 10
                                text (cheat_item.get_name() + " {color=#777777}(x" + str(cheat_item_count) + "){/color}"):
                                    style "journal_text"
                                    size 18
                                    xsize 360
                                    yalign 0.5
                                button:
                                    text "ADD" xalign 0.5 style "buttons_idle" size 18
                                    action [With(dissolveM), Call("add_item_cheat", cheat_item_key, 1)]
                                    alternate [With(dissolveM), Call("add_item_cheat", cheat_item_key, 10)]
                                    xsize 110
                            null height 8

            vbar value YScrollValue("CheatItemList"):
                unscrollable "hide"
                xalign 1.0
    elif display == "debug":
        frame:
            background Solid("#0000")
            area (950, 200, 560, 690)

            viewport id "CheatDebugList":
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
                    

                    input:
                        value VariableInputValue("game_data_input")

                    if game_data_old != game_data_input:
                        $ display_game_data_journal(game_data_input)

                    $ game_data_text = "Game Data: " + str(game_data_output)
                    $ progress_text = "Progress: " + str(progress_output)
                    button:
                        text game_data_text xalign 0.0 style "journal_text"
                    button:
                        text progress_text xalign 0.0 style "journal_text"

                    null height 10

                    button:
                        text "Run Test-Label" style "buttons_idle"
                        action Call("test_label")

                    null height 10

                    button:
                        text "Show Paperdoll-Test" style "buttons_idle"
                        action Call("show_paperdoll_test")

                    null height 10

                    button:
                        text "Give every Item" style "buttons_idle"
                        action Call("give_every_item", 5, display)

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
                
                    
            vbar value YScrollValue("CheatDebugList"):
                unscrollable "hide"
                xalign 1.0
    elif display == "logs":
        frame:
            background Solid("#0000")
            area (950, 200, 560, 690)

            viewport id "CheatLogList":
                mousewheel True
                draggable "touch"
                vbox:
                    text "Session logs from log / log_val / log_json / log_separator.\nFilter by type, category and origin. Cleared on restart.":
                        color "#000000"
                        size 18

                    null height 15

                    hbox:
                        button:
                            text "Type" xalign 0.0 style "journal_text"
                            xsize 180
                        button:
                            text "[log_filter_type]" xalign 1.0 style "buttons_idle"
                            action [With(dissolveM), Call("cycle_log_filter", "type", 5, display)]
                            xsize 320
                    null height 5
                    hbox:
                        button:
                            text "Category" xalign 0.0 style "journal_text"
                            xsize 180
                        button:
                            text "[log_filter_category]" xalign 1.0 style "buttons_idle"
                            action [With(dissolveM), Call("cycle_log_filter", "category", 5, display)]
                            xsize 320
                    null height 5
                    hbox:
                        button:
                            text "Origin" xalign 0.0 style "journal_text"
                            xsize 180
                        button:
                            text "[log_filter_origin]" xalign 1.0 style "buttons_idle"
                            action [With(dissolveM), Call("cycle_log_filter", "origin", 5, display)]
                            xsize 320

                    null height 10
                    hbox:
                        button:
                            text "Clear Logs" xalign 0.0 style "journal_text"
                            xsize 250
                        button:
                            text "{color=#a00000}CLEAR NOW{/color}" xalign 1.0
                            action [With(dissolveM), Call("clear_logs_cheat", 5, display)]
                            xsize 250

                    null height 15
                    image "journal/journal/left_list_separator.webp"
                    null height 10

                    $ filtered_logs = get_filtered_game_logs(log_filter_type, log_filter_category, log_filter_origin)
                    if len(filtered_logs) == 0:
                        text "No log entries." style "journal_text" size 18
                    else:
                        for log_entry in filtered_logs:
                            if log_entry.get("is_json"):
                                use journal_log_json_entry(log_entry)
                            else:
                                $ log_line = format_game_log_entry(log_entry)
                                text log_line:
                                    style "journal_text"
                                    size 14
                                    xmaximum 520
                            null height 6

            vbar value YScrollValue("CheatLogList"):
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
                    use journal_cheats_stat(MONEY, "school")
                    # LEVEL
                    use journal_cheats_stat(LEVEL, "school")
                    use journal_cheats_stat(LEVEL, "parent")
                    use journal_cheats_stat(LEVEL, "teacher")
                    use journal_cheats_stat(LEVEL, "secretary")
                    # CORRUPTION
                    use journal_cheats_stat(CORRUPTION, "school")
                    # INHIBITION
                    use journal_cheats_stat(INHIBITION, "school")
                    # HAPPINESS
                    use journal_cheats_stat(HAPPINESS, "school")
                    # EDUCATION
                    use journal_cheats_stat(EDUCATION, "school")
                    # CHARM
                    use journal_cheats_stat(CHARM, "school")
                    # REPUTATION
                    use journal_cheats_stat(REPUTATION, "school")
                    
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
    elif display == "buildings":
        frame:
            background Solid("#0000")
            area (950, 200, 560, 690)

            viewport id "CheatBuildingList":
                mousewheel True
                draggable "touch"
                vbox:
                    text "Force the open/closed state of registered buildings.\nOPEN clears all close-reasons; CLOSE keeps the building shut.\nProceed on your own risk.":
                        color "#000000"
                        size 20

                    null height 20

                    if building_manager is None or len(building_manager.get_buildings()) == 0:
                        text "No buildings registered." style "journal_text" size 20
                    else:
                        for building in sorted(building_manager.get_buildings(), key = lambda b: b.get_name()):
                            $ b_key = building.key
                            $ b_open = building.is_open()
                            hbox:
                                spacing 5
                                text building.get_name():
                                    style "journal_text"
                                    xsize 200
                                    yalign 0.5
                                if b_open:
                                    text "{color=#00a000}OPEN{/color}":
                                        size 20
                                        xsize 90
                                        yalign 0.5
                                    button:
                                        text "CLOSE" xalign 0.5 style "buttons_idle"
                                        action [With(dissolveM), Call("set_building_state_cheat", 5, display, b_key, "closed")]
                                        xsize 110
                                        sensitive b_open
                                else:
                                    text "{color=#a00000}CLOSED{/color}":
                                        size 20
                                        xsize 90
                                        yalign 0.5
                                    button:
                                        text "OPEN" xalign 0.5 style "buttons_idle"
                                        action [With(dissolveM), Call("set_building_state_cheat", 5, display, b_key, "open")]
                                        xsize 110
                                        sensitive not b_open
                                
                            null height 8

            vbar value YScrollValue("CheatBuildingList"):
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

# Gallery (7)
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

    key "K_ESCAPE" action [With(dissolveM), Jump("map_entry")]

    use journal_page_selector(7, display)

    text "Gallery":
        xalign 0.25 yalign 0.2
        size 60
        color "#000"

    # separate location and event in display (schema: location.event)
    $ split_display = [display, "", "value_mode", ""]
    if '.' in display:
        $ split_display = display.split('.')
    
    

    $ category = split_display[0]
    $ event = split_display[1] if len(split_display) > 1 else ""

    

    # value_mode, fragment_mode, fragment_selection_mode
    $ display_mode = split_display[2] if len(split_display) > 2 else "value_mode"
    $ fragment_selection_index = int(split_display[3]) if len(split_display) > 3 and is_integer(split_display[3]) else 0
    $ fragment_selection_fragment = split_display[4] if len(split_display) > 4 else ""

    python:
        if get_event_from_register(fragment_selection_fragment) != None:
            event_obj = get_event_from_register(event)
            persistent.gallery[event_obj.get_location()][event]['options']['frag_order'][fragment_selection_index] = fragment_selection_fragment

    $ category_collection = persistent.gallery
    if get_setting("show_gallery_category") == "Categories":
        $ category_collection = {cat: cat_coll for cat, cat_coll in event_replay_categories.items() if len([e for e in cat_coll if e in persistent.gallery[get_event_from_register(e).get_location()].keys()])}

    if category != "" and category not in category_collection.keys():
        $ location = ""
        $ event = ""
    elif event != "" and (event not in category_collection[category] or (get_setting("show_gallery_category") == "Locations" and event not in category_collection[category].keys())):
        $ event = ""    

    # if no location is defined 
    if category == "": 
        
        python:
            show_gallery_category = get_setting("show_gallery_category")
            if show_gallery_category == None:
                show_gallery_category = "Locations"
                set_setting("show_gallery_category", "Locations")

        use journal_tab_selection(7, display, show_gallery_category, "journal_gallery_switch_category", "Locations", "Categories", size = (350, 275, 500, 100))

        # parse all available location keys to their corresponding buildings
        # $ location_list = [get_building(location_name) for location_name in persistent.gallery.keys() if get_building(location_name) != None]

        # # map all the buildings with their corresponding names into a dict
        # $ location_dict = {building.get_name(): building.get_title() for building in location_list}
        $ exclude_keys = ['FragStorage', 'fragment']
        $ category_dict = {key: get_translation(key) for key in category_collection.keys() if key not in exclude_keys}

        # add the miscellaneous location separately as there is no corresponding building
        # miscellaneous represents all events that are not bound to a location
        # if 'misc' in persistent.gallery.keys():
        #     $ location_dict['misc'] = "Miscellaneous"

        

        # check if there is any event that can be replayed
        # if yes, display a list with all locations where events are available
        # if no be sad and show that
        if len(category_dict) != 0:
            
            

            use journal_simple_list(7, category, category_dict, "buttons_idle", pos_x = 350, pos_y = 350, width = 500, sort = True)
            text "Please select an option.":
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
        
    elif category != "": # if an option is defined
        

        $ category_title = "Miscellaneous"

        if get_setting("show_gallery_category") == "Locations":
            $ category_title = get_location_title(category)
        else:
            $ category_title = get_translation(category)
        
        # display a button that deletes all persistent data for all events registered in that location
        if debug_mode:
            textbutton "{color=#a00000}Reset Category{/color}":
                text_style "journal_text"
                xpos 350
                ypos 260
                action [With(dissolveM), Call('reset_event_gallery', category, "")]

        # return button for returning to location overview
        textbutton "← [category_title]":
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
    if category != "":
        $ event_collection = []
        if get_setting("show_gallery_category") == "Locations":
            $ event_collection = persistent.gallery[category].keys()
        else:
            $ event_collection = event_replay_categories[category]

        if display_mode != "fragment_selection_mode":
            $ event_list = [get_event_from_register(event_name) for event_name in event_collection if get_event_from_register(event_name) != None and renpy.has_label(get_event_from_register(event_name).get_event_label()) and event_name in persistent.gallery[get_event_from_register(event_name).get_location()].keys()]
            $ event_dict = {f"{category}.{event_obj.get_event()}": get_translation(event_obj.get_event()) for event_obj in event_list}
            use journal_simple_list(7, display, event_dict, "buttons_idle", pos_x = 400, pos_y = 350, width = 450, sort = True)
        else: 
            $ location = get_event_from_register(event).get_location()
            $ event_frag_storage = persistent.gallery[location][event]['options']['Frag_Storage'][fragment_selection_index]
            $ base_event_data = persistent.gallery[location][event]['options']['last_data']
            $ event_list = [get_event_from_register(event_name) for event_name in persistent.gallery["FragStorage"][event_frag_storage]['values'].keys() if get_event_from_register(event_name) != None and get_event_from_register(event_name).is_available(in_journal_gallery = True, **base_event_data)]
            $ event_dict = {'.'.join([category, event, "fragment_selection_mode", str(fragment_selection_index), event_obj.get_event()]): get_translation(event_obj.get_event()) for event_obj in event_list}
            use journal_simple_list(7, display, event_dict, "buttons_idle", pos_x = 450, pos_y = 400, width = 450, height = 550, sort = True)
        
    # if an event is selected, display event information on right side
    if event != "":
        

        $ event_obj = get_event_from_register(event)
        $ location = event_obj.get_location()
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
        $ event_thumb = find_loadable_image(event_obj.get_thumbnail())
        if event_thumb != "":
            $ thumbnail = im.Scale(event_thumb, 500, 281)

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
                        action [With(dissolveM), Call("open_journal", 7, '.'.join([category, event, "fragment_mode"]))]
                else:
                    
                    textbutton "Values":
                        text_style "buttons_idle"
                        xpos 989
                        ypos 560
                        action [With(dissolveM), Call("open_journal", 7, '.'.join([category, event, "value_mode"]))]
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

# Credits (6)
image pBannerI = im.Scale("images/journal/journal/patreon banner idle.webp", 500, 262)
image pBannerH = im.Scale("images/journal/journal/patreon banner hover.webp", 500, 262)
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

    key "K_ESCAPE" action [With(dissolveM), Jump("map_entry")]

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

                        text f"{len(teacher_members)} patreons":
                            size 20
                            color "#676767"

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

                        text f"{len(student_members)} patreons":
                            size 20
                            color "#676767"

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

transform journal_note_tilt(angle=0):
    rotate angle
    # Nominal size stays frame_w/h; cell metrics reserve space for the tilt.
    rotate_pad False

screen journal_situation_note_polaroid(metrics, image_path):
    $ frame_w = metrics["frame_w"]
    $ frame_h = metrics["frame_h"]
    $ cell_w = metrics["cell_w"]
    $ cell_h = metrics["cell_h"]
    $ place_x = metrics["place_x"]
    $ place_y = metrics["place_y"]
    $ photo_w = metrics["photo_w"]
    $ photo_h = metrics["photo_h"]
    $ rotation = metrics["rotation"]

    fixed:
        xsize cell_w
        ysize cell_h

        fixed at journal_note_tilt(rotation):
            xpos place_x
            ypos place_y
            xsize frame_w
            ysize frame_h

            add Solid("#00000028"):
                xsize frame_w
                ysize frame_h
                xpos 2
                ypos 3

            add Solid("#f7f3e8"):
                xsize frame_w
                ysize frame_h

            add image_path:
                xsize photo_w
                ysize photo_h
                xpos 8
                ypos 8

            add Solid("#d4c4a8"):
                xsize 44
                ysize 11
                xalign 0.5
                ypos 0

screen journal_situation_note(teaser, width=480):
    $ stamp = teaser.get_timestamp_text()
    $ type_label, type_color = teaser.get_note_type_display()
    $ layout_id = getattr(teaser, "layout_id", None) or "text_full"
    $ has_photo = teaser.has_photo()
    $ interpretation = getattr(teaser, "interpretation_text", None)
    $ metrics = teaser.get_polaroid_metrics() if has_photo else None
    $ gap = 16
    $ text_side_w = max(120, width - metrics["cell_w"] - gap) if metrics else width

    vbox:
        xsize width
        spacing 6

        hbox:
            spacing 8
            if type_label is not None:
                text "● [type_label]":
                    style "journal_note_type"
                    color type_color
            if stamp:
                text stamp style "journal_note_timestamp"

        if has_photo and layout_id in ("photo_left", "text_aside"):
            $ side_text_offset = 12 if layout_id == "text_aside" else 0
            hbox:
                spacing gap
                use journal_situation_note_polaroid(metrics, teaser.image_path)
                vbox:
                    xsize text_side_w
                    xoffset side_text_offset
                    yalign 0.0
                    text teaser.text style "journal_desc"
                    if interpretation:
                        null height 4
                        text "— [interpretation]":
                            style "journal_note_interpretation"

        elif has_photo and layout_id == "photo_right":
            hbox:
                spacing gap
                vbox:
                    xsize text_side_w
                    yalign 0.0
                    text teaser.text style "journal_desc"
                    if interpretation:
                        null height 4
                        text "— [interpretation]":
                            style "journal_note_interpretation"
                use journal_situation_note_polaroid(metrics, teaser.image_path)

        elif has_photo and layout_id in ("photo_top", "text_full"):
            vbox:
                xsize width
                hbox:
                    xalign 0.5
                    use journal_situation_note_polaroid(metrics, teaser.image_path)
                null height 8
                text teaser.text style "journal_desc"
                if interpretation:
                    null height 4
                    text "— [interpretation]":
                        style "journal_note_interpretation"

        elif layout_id == "text_aside":
            vbox:
                xsize width - 18
                xoffset 12
                text teaser.text style "journal_desc"
                if interpretation:
                    null height 4
                    text "— [interpretation]":
                        style "journal_note_interpretation"

        else:
            vbox:
                xsize width
                text teaser.text style "journal_desc"
                if interpretation:
                    null height 4
                    text "— [interpretation]":
                        style "journal_note_interpretation"

        null height 16

screen journal_situation_gate(xpos, height, color="#1a1a1a", gate_width=12):
    # """
    # Gate-style marker on a situation bar (two pillars + lintels).

    # ### Parameters:
    # 1. xpos: int
    #     - Horizontal center of the gate on the bar.
    # 2. height: int
    #     - Track height; gate extends slightly above/below.
    # 3. color: str (default: \"#1a1a1a\")
    #     - Gate fill color.
    # 4. gate_width: int (default: 12)
    #     - Total width of the gate opening.
    # """

    fixed:
        xpos xpos
        xanchor 0.5
        yalign 0.5
        xsize gate_width
        ysize height + 16

        add Solid(color):
            xsize 3
            ysize height + 16
            xpos 0

        add Solid(color):
            xsize 3
            ysize height + 16
            xpos gate_width - 3

        add Solid(color):
            xsize gate_width
            ysize 3
            ypos 0

        add Solid(color):
            xsize gate_width
            ysize 3
            yalign 1.0

screen journal_situation_bar(situation, width=480, height=28):
    # """
    # Non-interactive combined situation progress bar with a red→green track,
    # a handle for the current combined value, and gate markers for the nearest
    # projected thresholds above and below.

    # ### Parameters:
    # 1. situation: Situation
    #     - The situation whose combined bar to display.
    # 2. width: int (default: 480)
    #     - Track width in pixels.
    # 3. height: int (default: 28)
    #     - Track height in pixels.
    # """

    $ bar_min = situation.get_combined_bar_min()
    $ bar_max = situation.get_combined_bar_max()
    $ bar_value = situation.get_combined_bar_value()
    $ span = float(bar_max - bar_min) or 1.0
    $ t = clamp_value((bar_value - bar_min) / span, 0.0, 1.0)
    $ handle_x = int(t * width)
    $ value_label = situation.get_combined_bar_value_mood()
    $ label_space = 20

    $ next_above = situation.get_closest_next_blocking_threshold(bar_value, 1.0)
    $ next_below = situation.get_closest_next_blocking_threshold(bar_value, -1.0)
    $ next_above_pos = situation.get_combined_threshold_value(next_above) if next_above is not None else None
    $ next_below_pos = situation.get_combined_threshold_value(next_below) if next_below is not None else None

    fixed:
        xsize width
        ysize height + 16 + label_space

        $ text_margin = 40  # how close to edge before shifting text anchor
        $ margin_left = text_margin
        $ margin_right = width - text_margin
        if handle_x < margin_left:
            $ label_x = margin_left
            $ label_anchor = 0.0
        elif handle_x > margin_right:
            $ label_x = margin_right
            $ label_anchor = 1.0
        else:
            $ label_x = handle_x
            $ label_anchor = 0.5

        text value_label:
            style "journal_desc_small"
            xpos label_x
            xanchor label_anchor
            ypos 0
            textalign 0.5
       

        fixed:
            ypos label_space
            xsize width
            ysize height + 16

            add HGradient("#c62828", "#2e7d32"):
                ysize height
                yalign 0.5
                xsize width

            if bar_min < 0 < bar_max:
                $ zero_t = clamp_value((0 - bar_min) / span, 0.0, 1.0)
                add Solid("#00000040"):
                    xsize 2
                    ysize height
                    xpos int(zero_t * width)
                    xanchor 0.5
                    yalign 0.5

            if next_below is not None and next_below_pos + next_below.visible_range > bar_value:
                $ tb = clamp_value((next_below_pos - bar_min) / span, 0.0, 1.0)
                use journal_situation_gate(int(tb * width), height, "#7f1d1d")

            if next_above is not None and next_above_pos - next_above.visible_range < bar_value:
                if next_above is not next_below:
                    $ ta = clamp_value((next_above_pos - bar_min) / span, 0.0, 1.0)
                    use journal_situation_gate(int(ta * width), height, "#14532d")

                if next_above is next_below:
                    $ ta = clamp_value((next_above_pos - bar_min) / span, 0.0, 1.0)
                    use journal_situation_gate(int(ta * width), height, "#1a1a1a")

            add Solid("#ffffff"):
                xsize 10
                ysize height + 10
                xpos handle_x
                xanchor 0.5
                yalign 0.5

            add Solid("#111111"):
                xsize 6
                ysize height + 6
                xpos handle_x
                xanchor 0.5
                yalign 0.5

screen journal_situation_tabs(situation_key, tab):

    if tab == "":
        if has_keyboard():
            key "K_TAB" action [With(dissolveM), Call("open_journal", 8, f"{situation_key}:")]
        image "journal/journal/top_tag_4_hover.webp":
            xpos 940
            ypos 75
        text "Overview":
            xpos 980
            ypos 105
            size 20
            color "#fff"
    else:
        imagebutton:
            idle "journal/journal/top_tag_4_idle.webp"
            hover "journal/journal/top_tag_4_hover.webp"
            xpos 940
            ypos 75
            tooltip "Overview"
            action [With(dissolveM), Call("open_journal", 8, f"{situation_key}:")]

    if tab == "passives":
        if has_keyboard():
            key "K_TAB" action [With(dissolveM), Call("open_journal", 8, f"{situation_key}:passives")]
        image "journal/journal/top_tag_5_hover.webp":
            xpos 1114
            ypos 75
        text "Measures":
            xpos 1154
            ypos 108
            size 20
            color "#000"
    else:
        imagebutton:
            idle "journal/journal/top_tag_5_idle.webp"
            hover "journal/journal/top_tag_5_hover.webp"
            xpos 1114
            ypos 75
            tooltip "Measures"
            action [With(dissolveM), Call("open_journal", 8, f"{situation_key}:passives")]

    if tab == "notes":
        if has_keyboard():
            key "K_TAB" action [With(dissolveM), Call("open_journal", 8, f"{situation_key}:notes")]
        image "journal/journal/top_tag_6_hover.webp":
            xpos 1290
            ypos 75
        text "Notes":
            xpos 1350
            ypos 109
            size 20
            color "#fff"
    else:
        imagebutton:
            idle "journal/journal/top_tag_6_idle.webp"
            hover "journal/journal/top_tag_6_hover.webp"
            xpos 1290
            ypos 75
            tooltip "Notes"
            action [With(dissolveM), Call("open_journal", 8, f"{situation_key}:notes")]

# Situations (8)
screen journal_situations(display):
    tag interaction_overlay
    modal True

    use school_overview_map
    use school_overview_stats

    image "journal/journal/background.webp"

    key "K_ESCAPE" action [With(dissolveM), Jump("map_entry")]

    use journal_page_selector(8, display, char)

    text "Situations":
        xalign 0.25
        yalign 0.2
        size 60
        color "#000"

    python:
        show_completed = get_setting("journal_situations_show_completed")

        if show_completed == None:
            show_completed = False
            set_setting("journal_situations_show_completed", False)

        show_normal = get_setting("journal_situations_show_normal")

        if show_normal == None:
            show_normal = True
            set_setting("journal_situations_show_normal", True)

    $ situation_key, situation_tab = parse_situation_journal_display(display)

    frame:
        # background Solid("#00000090")
        background Solid("#00000000")
        area (330, 300, 560, 600)

        viewport id "SituationsList":
            mousewheel True
            draggable "touch"

            vbox:
                if situation_manager is not None and situation_manager.is_resolution_breather_active():
                    $ breather_days = situation_manager.get_resolution_breather_display_days()
                    text "The pressure eases for a moment. The remaining situations hold steady.":
                        color "#000"
                        size 18
                        italic True
                    text "Still [breather_days] day(s) of calm.":
                        color "#000"
                        size 16
                        italic True
                    null height 12

                $ situations_list = situation_manager.get_visible_situations()
                $ teaser_titles = situation_manager.get_visible_teaser_titles(*situations_list, tab = situation_tab)
                use journal_foldable_list("Active", 8, display, teaser_titles, "journal_situations_show_normal")

                $ completed_situations = situation_manager.get_completed_situations()
                $ teaser_titles = situation_manager.get_visible_teaser_titles(*completed_situations, tab = situation_tab)
                use journal_foldable_list("Completed", 8, display, teaser_titles, "journal_situations_show_completed")


        vbar value YScrollValue("SituationsList"):
            unscrollable "hide"
            xalign 1.04

    if display != "":

        $ situation = situation_manager.get_situation(situation_key)
        if situation is None:
            $ display = ""
        else:
            $ situation_thumbnail = situation.get_current_thumbnail()
            $ situation_full_image = None
            if situation_thumbnail:
                $ thumb_stem = situation_thumbnail.rsplit('.', 1)[0]
                $ situation_full_image = find_loadable_image(thumb_stem + '_full.webp') or find_loadable_image(thumb_stem + '_full.png') or None

        if situation is not None and situation.visibility_state == "teaser_active":
            frame:
                # background Solid("#00000090")
                background Solid("#00000000")
                area (960, 200, 500, 780)

                viewport id "SituationTeaserDetail":
                    mousewheel True
                    draggable "touch"

                    vbox:
                        for teaser in situation.get_active_teasers():
                            use journal_situation_note(teaser, 480)

                vbar value YScrollValue("SituationTeaserDetail"):
                    unscrollable "hide"
                    xalign 1.04

        elif situation is not None:
            $ combined_bar_value = situation.get_combined_bar_value()
            $ combined_bar_tendency = situation.get_combined_bar_tendency()

            use journal_situation_tabs(situation_key, situation_tab)

            # use journal_image(8, display, situation_thumbnail, situation_thumbnail.replace('.webp', '_full.webp'), x_pos = 960, y_pos = 180, height = 280, wide = True)

            frame:
                # background Solid("#00000090")
                background Solid("#00000000")
                area (960, 180, 500, 800)

                viewport id "SituationDetail":
                    mousewheel True
                    draggable "touch"

                    vbox:                        
                        if situation_tab == "":
                            button:
                                add situation_thumbnail xsize 497 ysize 279
                                action [With(dissolveM), Call("call_max_image_from_journal", situation_thumbnail, 8, display)]

                            null height 10

                            for description in situation.get_descriptions():
                                text description style "journal_desc"

                            null height 5
                            image "journal/journal/left_list_separator.webp"
                            null height 5

                            use journal_situation_bar(situation)

                            null height 10

                            $ threshold_hints = situation.get_hints()
                            for i, hint in enumerate(threshold_hints):
                                $ text_str = f"{i}. {hint}"
                                text text_str style "journal_desc"
                                null height 10
                        elif situation_tab == "passives":
                            $ passives = situation.get_passives("passive")
                            if len(passives) > 0:
                                text "Passives" style "journal_desc"
                                image "journal/journal/left_list_separator.webp"

                                null height 10

                                if situation.active_passive is not None:
                                    $ active_passive = situation.get_passive(situation.active_passive)
                                    if active_passive is not None:
                                        $ passive_description, effects_descriptions = active_passive.get_full_description()
                                        text "Current active:" style "journal_desc"
                                        null height 5
                                        text passive_description style "journal_desc"
                                        null height 10
                                        for effect_description in effects_descriptions:
                                            text effect_description style "journal_desc_small"
                                            null height 10
                                else:
                                    text "No passive active" style "journal_desc"
                                    
                                null height 10

                                for i, passive in enumerate(passives):
                                    $ passive_name = f"{i}. {get_translation(passive.name)}"
                                    $ passive_description = f"    {passive.get_effects_description()}"

                                    $ button_style = "buttons_idle_small"
                                    if situation.active_passive == passive.name:
                                        $ button_style = "buttons_selected_small"

                                    button:
                                        action Call("activate_passive", display, situation, passive)
                                        text passive_name style button_style
                                    text passive_description style "journal_desc_small"
                                    null height 10
                                null height 10

                            $ measures = situation.get_passives("measure")
                            if len(measures) > 0:
                                text "Measures" style "journal_desc"
                                image "journal/journal/left_list_separator.webp"

                                null height 10

                                if situation.active_measure is not None:
                                    $ active_measure = situation.get_measure()
                                    if active_measure is not None:
                                        $ measure_description, measure_effects = active_measure.get_full_description()
                                        text "Current active:" style "journal_desc"
                                        null height 5
                                        text measure_description style "journal_desc"
                                        null height 10
                                        for effect_description in measure_effects:
                                            text effect_description style "journal_desc_small"
                                            null height 10
                                else:
                                    text "No measure active" style "journal_desc"

                                null height 10

                                for i, measure in enumerate(measures):
                                    $ measure_name = f"{i}. {get_translation(measure.name)}"
                                    $ measure_description = f"    {measure.get_effects_description()}"
                                    $ measure_available = measure.check_available()

                                    $ button_style = "buttons_idle_small"
                                    if situation.active_measure == measure.name:
                                        $ button_style = "buttons_selected_small"
                                    elif not measure_available:
                                        $ button_style = "buttons_inactive_small"

                                    button:
                                        action Call("activate_measure", display, situation, measure)
                                        sensitive measure_available
                                        text measure_name style button_style
                                    text measure_description style "journal_desc_small"
                                    null height 10
                        elif situation_tab == "notes":
                            for teaser in situation.get_active_teasers():
                                use journal_situation_note(teaser, 480)



                vbar value YScrollValue("SituationDetail"):
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

label activate_passive(display, situation, passive):
    $ situation.set_passive(passive.name)
    call open_journal(8, display)

label activate_measure(display, situation, measure):
    $ situation.set_measure(measure.name)
    call open_journal(8, display)

# Goals (8) - DEPRECATED
screen journal_goals(display):
    tag interaction_overlay
    modal True

    use school_overview_map
    use school_overview_stats

    image "journal/journal/background.webp"

    key "K_ESCAPE" action [With(dissolveM), Jump("map_entry")]

    use journal_page_selector(8, display, char)

    text "Goals": 
        xalign 0.25 
        yalign 0.2
        size 60
        color "#000"

    if not get_setting("journal_quest_hinting_active"):
        button:
            xalign 0.45
            yalign 0.15
            image "images/icons/info.webp"
            action Call("start_quest_hinting", display)
            tooltip "Activate Quest hints"

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
                $ categories = list(quest_manager.category_quest.keys())
                $ categories.sort(key=lambda x: get_translation(x))

                for category in categories:
                    $ quests_list = [quest for quest in quest_manager.category_quest[category].keys() if quest_manager.category_quest[category][quest].visible and (show_completed or not quest_manager.category_quest[category][quest].complete)]
                    $ quest_list = [(get_translation(quest) if not quest_manager.category_quest[category][quest].complete else set_text_color(get_translation(quest), "#00a000"), f"{category}-?-{quest}") for quest in quests_list]
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
        $ quest = quest_manager.get_quest(quest_key)
        if quest is None:
            text "Quest system archived.":
                xpos 989 ypos 200 size 30 color "#000" xmaximum 500
        else:

            $ quest_descriptions = quest.description

            use journal_image(8, display, quest.thumbnail, quest.thumbnail.replace('.webp', '_full.webp'), y_pos = 200, height = 280, wide = True)

            frame:
                # background Solid("#00000090")
                background Solid("#00000000")
                area (960, 480, 500, 500)
            
                viewport id "ProgressList":
                    mousewheel True
                    draggable "touch"

                    vbox:
                        null height 10 

                        for description in quest_descriptions:
                            text description style "journal_desc"

                        null height 20

                        for i, goal in enumerate(quest.get_active_goals().values()):
                            $ goal_finished = "☐"
                            if goal.complete:
                                $ goal_finished = "☑"
                        
                            $ goal_text = f"{goal_finished}  {i + 1}. {goal.name}"

                            python:
                                display_goal = get_setting(f"show_goal_{goal.key}")

                                if display_goal == None:
                                    display_goal = True
                                    set_setting(f"show_goal_{goal.key}", True)

                                arrow = "▲  " if display_goal else "▼  "

                                goal_text = arrow + goal_text

                            button:
                                text goal_text: 
                                    style "journal_desc"
                                action Function(set_setting, f"show_goal_{goal.key}", not display_goal)

                            if display_goal:
                                $ goal_descriptions = goal.description

                                for goal_desc in goal_descriptions:
                                    $ goal_desc_text = "  {i}" + goal_desc + "{/i}"
                                    text goal_desc_text style "journal_desc"

                                    for task in goal.tasks.values():
                                        use journal_display_task(task, gap = 8)


                        if quest.complete:
                            null height 30

                            $ final_text = quest.finished_description

                            for final_description in final_text:
                                text final_description style "journal_text"

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

# Character (9)
screen journal_character(display):

    tag interaction_overlay
    modal True

    use school_overview_map
    use school_overview_stats

    image "journal/journal/background.webp"

    use journal_page_selector(9, display, char)

    key "K_ESCAPE" action [With(dissolveM), Jump("map_entry")]

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

# Inventory (2 / 10)
screen journal_inventory(display, page = 10):
    
    tag interaction_overlay
    modal True

    use school_overview_map
    use school_overview_stats

    image "journal/journal/background.webp"

    use journal_page_selector(page, display, char)

    key "K_ESCAPE" action [With(dissolveM), Jump("map_entry")]

    $ inventory_items = inventory_manager.get_inventory()

    # left side
    frame:
        background Solid("#0000")
        area (350, 200, 500, 750)

        $ grid_rows = (len(inventory_items) + 3) // 4

        viewport id "journal_inventory_left":
            mousewheel True
            draggable "touch"
            grid 4 grid_rows:
                spacing 4
                for item in inventory_items:
                    $ item_image = item.data().get_image()
                    if display == item.key:
                        button:
                            xsize 100
                            ysize 100
                            background Solid("#0001")
                            add item_image:
                                xalign 0.5
                                yalign 0.5
                                xsize 90
                                ysize 90
                    else:
                        button:
                            xsize 100
                            ysize 100
                            action Call("open_journal", page, f"{item.key}")
                            add item_image:
                                xalign 0.5
                                yalign 0.5
                                xsize 90
                                ysize 90

            vbar value YScrollValue("journal_inventory_left"):
                unscrollable "hide"
                xalign 1.035

    if display != "" and not inventory_manager.has_item_data(display):
        $ display = ""

    if display != "":
        $ item_obj = inventory_manager.get_item(display)
        $ item_image = item_obj.data().get_image()
        $ item_name = item_obj.data().get_name()
        $ item_description = item_obj.data().get_description()
        $ item_amount = item_obj.amount

        # right side
        frame:
            background Solid("#0000")
            area (960, 200, 500, 700)

            viewport id "journal_inventory_right":
                mousewheel True
                draggable "touch"

                vbox:
                    text item_name:
                        style "journal_text"

                    add item_image:
                        xsize 500
                        ysize 500

                    text "Amount: {amount}".format(amount=item_amount):
                        style "journal_desc"

                    for description in item_description:
                        text description:
                            style "journal_desc"

            vbar value YScrollValue("journal_inventory_right"):
                unscrollable "hide"
                xalign 1.035

    
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

##################
# region Credits #

screen journal_display_text_list(text_list, text_style="journal_desc", gap = 0):
    $ text_gap = " " * gap
    if isinstance(text_list, list):
        for text_content in text_list:
            $ text_con = text_gap + text_content
            text text_con style text_style
    else:
        $ text_con = text_gap + text_list
        text text_con style text_style

screen journal_display_task(task, gap = 0):
    if (isinstance(task, TaskGroup) or isinstance(task, TaskOptionalGroup)):
        $ task_group_description_list = task.description
        use journal_display_text_list(task_group_description_list, "journal_desc", gap - 2)

        for group_task in task.tasks.values():
            $ text_list = group_task.display()
            use journal_display_text_list(text_list, "journal_desc_small", gap + 4)
    else:
        $ text_list = task.display()
        use journal_display_text_list(text_list, "journal_desc_small", gap)

# endregion
##################

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

label journal_gallery_switch_category(category, page, display):
    # """
    # Switches the category of the gallery display

    # ### Parameters:
    # 1. category: str
    #     - the category to be switched to
    # 2. page: int
    #     - the page to be opened after the category switch
    # 3. display: str
    #     - the display information for the page
    # """

    $ set_setting("show_gallery_category", category)
    call open_journal(page, display) from journal_gallery_switch_category_1

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

init python:
    game_data_input = ""
    game_data_old = ""
    game_data_output = "N/A"
    progress_output = "N/A"
    def display_game_data_journal(new_input: str):
        global game_data_output
        global game_data_input
        global game_data_old
        
        game_data_input = new_input
        game_data_old = game_data_input

        game_data_output = get_game_data(new_input)

        if game_data_output == None:
            game_data_output = "N/A"

        global progress_output
        progress_output = get_progress(new_input)

        if progress_output == None:
            progress_output = "N/A"

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

label cycle_log_filter(filter_key, page, display):
    # """
    # Cycles a session log filter and reopens the journal logs page.

    # ### Parameters:
    # 1. filter_key: str
    #     - One of "type", "category", or "origin".
    # 2. page: int
    #     - The journal page to reopen.
    # 3. display: str
    #     - The journal display to reopen.
    # """

    $ cycle_log_filter_value(filter_key)
    call open_journal(page, display) from cycle_log_filter_1

label clear_logs_cheat(page, display):
    # """
    # Clears stored session logs and reopens the journal logs page.

    # ### Parameters:
    # 1. page: int
    #     - The journal page to reopen.
    # 2. display: str
    #     - The journal display to reopen.
    # """

    $ clear_game_logs()
    $ renpy.notify("Logs cleared!")
    call open_journal(page, display) from clear_logs_cheat_1

label set_building_state_cheat(page, display, building_key, state):
    # """
    # Forces a registered building's open/closed state from the cheat page.
    #
    # ### Parameters:
    # 1. page: int
    #     - The journal page to reopen.
    # 2. display: str
    #     - The journal display to reopen.
    # 3. building_key: str
    #     - The building to change.
    # 4. state: str
    #     - "open" clears every close-reason and adds a cheat open-reason so the
    #       building opens; "closed" adds a cheat close-reason so it stays shut.
    # """

    if state == "open":
        $ set_game_data(building_key + ":closed", [])
        $ add_building_collection_key(building_key, "open", "cheat")
    elif state == "closed":
        $ remove_building_collection_key(building_key, "open", "cheat")
        $ add_building_collection_key(building_key, "closed", "cheat")

    $ renpy.notify("Building updated!")
    call open_journal(page, display) from set_building_state_cheat_1

label cycle_event_cheat_filter(page, display):
    # """
    # Cycles the event cheat category filter and reopens the journal events page.
    #
    # ### Parameters:
    # 1. page: int
    #     - The journal page to reopen.
    # 2. display: str
    #     - The journal display to reopen.
    # """

    $ cycle_event_cheat_category()
    call open_journal(page, display) from cycle_event_cheat_filter_1

label call_event_cheat(event_id):
    # """
    # Starts a registered event directly from the cheat page via Event.call().
    #
    # ### Parameters:
    # 1. event_id: str
    #     - The event_id of the registered event to start.
    # """

    $ cheat_event = event_register.get(event_id, None)
    if cheat_event is None:
        $ renpy.notify("Event not found: " + str(event_id))
        call open_journal(5, "events") from call_event_cheat_1
        return

    $ hide_all()
    $ cheat_event.call(cheat_event_return = True)
    jump map_entry

label activate_situation_cheat(situation_key):
    # """
    # Activates a situation directly from the cheat page.
    #
    # ### Parameters:
    # 1. situation_key: str
    #     - The key of the situation to activate.
    # """

    $ cheat_situation = situation_manager.get_situation(situation_key) if situation_manager is not None else None
    if cheat_situation is not None and cheat_situation.state != "active":
        $ cheat_situation.activate()
        $ renpy.notify("Situation activated!")
    call open_journal(5, "situations") from activate_situation_cheat_1

label activate_situation_teasers_cheat(situation_key):
    # """
    # Activates all teasers of a situation directly from the cheat page.
    #
    # ### Parameters:
    # 1. situation_key: str
    #     - The key of the situation whose teasers are activated.
    # """

    $ cheat_situation = situation_manager.get_situation(situation_key) if situation_manager is not None else None
    if cheat_situation is not None:
        python:
            for cheat_teaser in cheat_situation.teasers.values():
                cheat_teaser.activate()
        $ renpy.notify("Teasers activated!")
    call open_journal(5, "situations") from activate_situation_teasers_cheat_1

label activate_teaser_cheat(situation_key, teaser_key):
    # """
    # Activates a single teaser of a situation directly from the cheat page.
    #
    # ### Parameters:
    # 1. situation_key: str
    #     - The key of the situation the teaser belongs to.
    # 2. teaser_key: str
    #     - The key of the teaser to activate.
    # """

    $ activate_situation_teaser(situation_key, teaser_key)
    $ renpy.notify("Teaser activated!")
    call open_journal(5, "situations") from activate_teaser_cheat_1

label toggle_unlockable_visibility_cheat(unlock_display):
    # """
    # Toggles the visibility override of an unlockable from the cheat page.
    #
    # ### Parameters:
    # 1. unlock_display: str
    #     - Unlockable selection as ``key`` or ``key:group_index``.
    # """

    $ cheat_unlockable = unlockable_manager.resolve_display(unlock_display) if unlockable_manager is not None else None
    if cheat_unlockable is not None:
        $ cheat_unlockable.override_visible = not getattr(cheat_unlockable, "override_visible", False)
    call open_journal(5, "unlockables") from toggle_unlockable_visibility_cheat_1

label add_item_cheat(item_key, amount = 1):
    # """
    # Adds an item to the inventory from the cheat page.
    #
    # ### Parameters:
    # 1. item_key: str
    #     - The key of the item to add.
    # 2. amount: int (default: 1)
    #     - The amount to add.
    # """

    if inventory_manager is not None and inventory_manager.has_item_data(item_key):
        $ inventory_manager.add_item(Item(item_key, amount))
    call open_journal(5, "items") from add_item_cheat_1

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

label start_unlockable_situation(display):
    # """
    # Activates the situation for an unlockable and reopens the unlockables journal page.

    # ### Parameters:
    # 1. display: str
    #     - Unlockable selection as ``key`` or ``key:view_index``.
    # """

    $ unlockable = unlockable_manager.resolve_display(display)
    if unlockable is not None and unlockable.status == "inactive":
        $ unlockable.activate()
    call open_journal(4, display) from start_unlockable_situation_1

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

label give_every_item(page, display):
    python:
        for item in inventory_manager.item_data.keys():
            inventory_manager.add_item(Item(item, 1))
    call open_journal(page, display) from give_every_item_1

# endregion
########################

# endregion
##########################