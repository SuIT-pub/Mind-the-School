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

    $ acknowledge_journal_alerts(page, display)

    # map_entry shows the full map HUD as its own zorder-80 screen, which would sit on top
    # of the book; journal_backdrop draws a reduced HUD instead. map_entry shows it again on close.
    hide screen school_overview_stats

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
    elif page == 11:
        call screen journal_menu(display) with dissolveM
    elif page == 12:
        call screen journal_collectibles(display) with dissolveM

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

screen journal_page_selector(page, display, char = "school", sub_entries = None):
    # """
    # Draws the journal book and its ribbon navigation for the given page.
    # Kept under its old name so every journal screen picks up the book.

    # ### Parameters:
    # 1. page: int
    #     - The page number to display.
    # 2. display: str
    #     - The display type for the journal page.
    # 3. char: str (default: "school")
    #     - unused, kept for the existing callers
    # 4. sub_entries: List[Tuple[str, bool, Action]] (default: None)
    #     - sub-page bookmarks along the top edge
    # """

    use journal_book(page, display, sub_entries)

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
        xysize (1920, 1080)
        background Solid("#0b0806")
        add Transform(image_path, fit = "contain", xysize = (1840, 1040)) align (0.5, 0.5)
        action [With(dissolveM), Call("open_journal", journal, display)]
    key "K_ESCAPE" action [With(dissolveM), Call("open_journal", journal, display)]

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

# Unlockables (4): journal_unlockables.rpy

# School Overview (1): journal_overview.rpy

# Cheats (5): journal_cheats.rpy

# Gallery (7): journal_gallery.rpy

# Credits (6): journal_credits.rpy

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

screen journal_situation_gate(xpos, height, color="#1a1a1a", gate_width=12, overhang=8):
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
    # 5. overhang: int (default: 8)
    #     - Extra pixels the gate extends above and below the track.
    # """

    $ gate_height = height + overhang * 2

    fixed:
        xpos xpos
        xanchor 0.5
        yalign 0.5
        xsize gate_width
        ysize gate_height

        add Solid(color):
            xsize 3
            ysize gate_height
            xpos 0

        add Solid(color):
            xsize 3
            ysize gate_height
            xpos gate_width - 3

        add Solid(color):
            xsize gate_width
            ysize 3
            ypos 0

        add Solid(color):
            xsize gate_width
            ysize 3
            yalign 1.0

screen journal_situation_bar(situation, width=480, height=28, show_label=True, gate_width=12, overhang=8):
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
    # 4. show_label: bool (default: True)
    #     - Whether to render the mood label above the track.
    # 5. gate_width: int (default: 12)
    #     - Total width of each gate opening.
    # 6. overhang: int (default: 8)
    #     - Extra pixels the gates extend above and below the track.
    # """

    $ bar_min = situation.get_combined_bar_min()
    $ bar_max = situation.get_combined_bar_max()
    $ bar_value = situation.get_combined_bar_value()
    $ span = float(bar_max - bar_min) or 1.0
    $ t = clamp_value((bar_value - bar_min) / span, 0.0, 1.0)
    $ handle_x = int(t * width)
    $ value_label = situation.get_combined_bar_value_mood()
    $ label_space = 20 if show_label else 0
    $ track_extra = overhang * 2
    $ handle_outer = max(6, int(round(height * 10 / 28.0)))
    $ handle_inner = max(4, int(round(height * 6 / 28.0)))

    $ next_above = situation.get_closest_next_blocking_threshold(bar_value, 1.0)
    $ next_below = situation.get_closest_next_blocking_threshold(bar_value, -1.0)
    $ next_above_pos = situation.get_combined_threshold_value(next_above) if next_above is not None else None
    $ next_below_pos = situation.get_combined_threshold_value(next_below) if next_below is not None else None

    fixed:
        xsize width
        ysize height + track_extra + label_space

        if show_label:
            $ text_margin = 40
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
            ysize height + track_extra

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
                use journal_situation_gate(int(tb * width), height, "#7f1d1d", gate_width, overhang)

            if next_above is not None and next_above_pos - next_above.visible_range < bar_value:
                if next_above is not next_below:
                    $ ta = clamp_value((next_above_pos - bar_min) / span, 0.0, 1.0)
                    use journal_situation_gate(int(ta * width), height, "#14532d", gate_width, overhang)

                if next_above is next_below:
                    $ ta = clamp_value((next_above_pos - bar_min) / span, 0.0, 1.0)
                    use journal_situation_gate(int(ta * width), height, "#1a1a1a", gate_width, overhang)

            add Solid("#ffffff"):
                xsize handle_outer
                ysize height + handle_outer
                xpos handle_x
                xanchor 0.5
                yalign 0.5

            add Solid("#111111"):
                xsize handle_inner
                ysize height + handle_inner
                xpos handle_x
                xanchor 0.5
                yalign 0.5

# Situations (8): journal_situations.rpy

label activate_passive(display, situation, passive):
    $ situation.set_passive(passive.name)
    # Events queued by the passive/measure effects play now, then back to the journal.
    call drain_situation_events from _call_drain_situation_events_activate_passive
    call open_journal(8, display)

label activate_measure(display, situation, measure):
    $ situation.set_measure(measure.name)
    call drain_situation_events from _call_drain_situation_events_activate_measure
    call open_journal(8, display)

# Goals (8) - DEPRECATED
screen journal_goals(display):
    tag interaction_overlay
    modal True


    use journal_backdrop

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


    use journal_tooltip

# Character (9): journal_characters.rpy

# Inventory (2 / 10): journal_inventory.rpy

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

label deactivate_situation_cheat(situation_key):
    # """
    # Deactivates an active situation directly from the cheat page, returning it
    # to `inactive` so it can be activated again.
    #
    # ### Parameters:
    # 1. situation_key: str
    #     - The key of the situation to deactivate.
    # """

    $ cheat_situation = situation_manager.get_situation(situation_key) if situation_manager is not None else None
    if cheat_situation is not None and cheat_situation.state == "active":
        $ cheat_situation.deactivate()
        $ renpy.notify("Situation deactivated!")
    call open_journal(5, "situations") from deactivate_situation_cheat_1

label toggle_pause_situation_cheat(situation_key):
    # """
    # Pauses an active situation from the cheat page, or drops the manual pause.
    # A flag pause is left alone; it ends when the event flag matches again.
    #
    # ### Parameters:
    # 1. situation_key: str
    #     - The key of the situation to pause or resume.
    # """

    $ cheat_situation = situation_manager.get_situation(situation_key) if situation_manager is not None else None
    if cheat_situation is not None and "manual" in cheat_situation.get_pause_reasons():
        $ cheat_situation.resume()
        if cheat_situation.is_paused():
            $ renpy.notify("Manual pause removed, still paused by the event flag.")
        else:
            $ renpy.notify("Situation resumed!")
    elif cheat_situation is not None and cheat_situation.state == "active":
        $ cheat_situation.pause()
        $ renpy.notify("Situation paused!")
    call open_journal(5, "situations") from toggle_pause_situation_cheat_1

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