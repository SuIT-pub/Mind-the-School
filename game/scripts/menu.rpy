init python:
    from typing import Tuple, Union, List

    ###############################
    # region Menu Data Refinement #
    ###############################

    class MenuElement:
        def __init__(self, key: str, title: str, *data: Effect | Condition | bool, active: bool = True, overwrite_position: Tuple[int, int] = None):
            self.key = key
            self.title = title
            self.active = active
            self.overwrite_position = overwrite_position

            self.effects = []
            self.conditions = []

            for item in data:
                if isinstance(item, Effect):
                    self.effects.append(item)
                elif isinstance(item, Condition):
                    self.conditions.append(item)
                elif isinstance(item, bool):
                    self.conditions.append(BoolCondition(item))

        def add_effect(self, effect: Effect):
            self.effects.append(effect)

        def add_condition(self, condition: str):
            self.conditions.append(condition)

        def set_title(self, title: str):
            self.title = title

        def set_effects(self, effects: List[Effect]):
            self.effects = effects

        def set_conditions(self, conditions: List[str]):
            self.conditions = conditions

        def get_key(self) -> str:
            return self.key

        def get_title(self) -> str:
            return self.title

        def get_effects(self) -> List[Effect]:
            return self.effects 

        def get_conditions(self) -> List[str]:
            return self.conditions

        def check_conditions(self, **kwargs) -> bool:
            return all(condition.is_fulfilled(**kwargs) for condition in self.conditions)
            
        def check_for_label_existence(self) -> bool:
            return all(check_for_label_existence(effect.event) for effect in self.effects if isinstance(effect, EventEffect))

        def set_active(self, active: bool):
            self.active = active

        def get_active(self) -> bool:
            return self.active

        def has_overwrite_position(self) -> bool:
            return self.overwrite_position != None

        def get_overwrite_position(self) -> Tuple[int, int]:
            return self.overwrite_position

    def check_for_label_existence(label: str) -> bool:
        """
        Checks if a label exists in the script.

        ### Parameters
        1. label : str
            - The label to check for.

        ### Returns
        1. bool
            - True if the label exists, False otherwise.
        """

        label_exists = renpy.has_label(label)
        if not label_exists:
            log(f"Label '{label}' does not exist.", log_type="error", category="menu")
        return label_exists            

    def clean_events_for_menu(events: Dict[str, EventStorage], **kwargs) -> Tuple[List[MenuElement], List[str], List[str]]:
        """
        Cleans a list of events for use in a menu.
        It takes each EventStorage in events and checks if it has any applicable events. If it does, it adds it to the output list.
        The elements in the output list are tuples of the form (title, EventEffect).

        ### Parameters
        1. events : Dict[str, EventStorage]
            - The events to filter and refine for use in the menu.

        ### Returns
        1. Tuple[List[MenuElement], List[str], List[str]]
            - The list of events that have applicable events and their effects.
        """

        output = []
        used = []

        high_prio_events = []

        blocked_events = []

        # remove events that have no applicable events
        for key in events.keys():
            storage = events[key]
            amount, prio = storage.count_available_events_and_highlight(**kwargs)
            title = get_event_menu_title(storage.get_location(), storage.get_name())
            if (amount > 0 and key not in used):
                if event_selection_mode:
                    effect = EventSelectEffect(storage)
                else:
                    effect = EventEffect(storage)

                # mark effect as high priority
                if prio:
                    high_prio_events.append(title)

                modified_title = title

                # if the event has a proficiency modifier, show it in the title
                if get_kwargs('show_proficiency_modifier', False, **kwargs):
                    modifier = get_headmaster_proficiency_multiplier(storage.get_name())
                    if modifier > 0 and modifier < 1:
                        modified_title = title + " (x{color=#a00000}" + f'{modifier:.1f}' + "{/color})"
                    elif modifier >= 1:
                        modified_title = title + " (x{color=#00a000}" + f'{modifier:.1f}' + "{/color})"

                output.append(MenuElement(title, modified_title, effect))
                used.append(key)
            elif get_kwargs('show_blocked_events', False, **kwargs) or storage.check_for_option('ShowBlocked'):
                output.append(MenuElement(title, title, EventEffect(title)))
                used.append(key)
                blocked_events.append(title)

        return output, high_prio_events, blocked_events

    # endregion
    ###############################

    ############################
    # region Call Menu Methods #
    ############################

    MENU_ANCHOR_TOP_LEFT = "top_left"
    MENU_ANCHOR_TOP_CENTER = "top_center"
    MENU_ANCHOR_TOP_RIGHT = "top_right"
    MENU_ANCHOR_MIDDLE_LEFT = "middle_left"
    MENU_ANCHOR_MIDDLE_CENTER = "middle_center"
    MENU_ANCHOR_MIDDLE_RIGHT = "middle_right"
    MENU_ANCHOR_BOTTOM_LEFT = "bottom_left"
    MENU_ANCHOR_BOTTOM_CENTER = "bottom_center"
    MENU_ANCHOR_BOTTOM_RIGHT = "bottom_right"
    # default: the choices stack right-aligned on top of the dialogue box
    MENU_ANCHOR_DIALOG = "dialog"

    MENU_ANCHOR_ALIGNS = {
        MENU_ANCHOR_TOP_LEFT: (0.0, 0.0),
        MENU_ANCHOR_TOP_CENTER: (0.5, 0.0),
        MENU_ANCHOR_TOP_RIGHT: (1.0, 0.0),
        MENU_ANCHOR_MIDDLE_LEFT: (0.0, 0.5),
        MENU_ANCHOR_MIDDLE_CENTER: (0.5, 0.5),
        MENU_ANCHOR_MIDDLE_RIGHT: (1.0, 0.5),
        MENU_ANCHOR_BOTTOM_LEFT: (0.0, 1.0),
        MENU_ANCHOR_BOTTOM_CENTER: (0.5, 1.0),
        MENU_ANCHOR_BOTTOM_RIGHT: (1.0, 1.0),
        MENU_ANCHOR_DIALOG: (1.0, 1.0),
    }

    MENU_WIDTH = 1185
    MENU_SCREEN_WIDTH = 1920
    MENU_SCREEN_HEIGHT = 1080
    MENU_DIALOG_RESERVED_HEIGHT = 280

    def get_menu_anchor_align(menu_anchor: str) -> Tuple[float, float]:
        """
        Resolves a nine-point menu anchor to (xalign, yalign).

        ### Parameters
        1. menu_anchor : str
            - One of: top_left, top_center, top_right, middle_left, middle_center,
                middle_right, bottom_left, bottom_center, bottom_right.

        ### Returns
        1. Tuple[float, float]
            - The xalign and yalign values for the menu vbox.
        """

        aligns = MENU_ANCHOR_ALIGNS.get(menu_anchor)
        if aligns is None:
            log(f"Unknown menu_anchor '{menu_anchor}', falling back to middle_center.", log_type="warning", category="menu")
            return MENU_ANCHOR_ALIGNS[MENU_ANCHOR_MIDDLE_CENTER]
        return aligns

    def get_menu_usable_height(has_dialog: bool) -> int:
        """
        Returns the vertical area the menu may occupy.

        Middle and bottom anchors use this height, so they sit above an open
        dialogue box and drop to the full screen when no dialogue is shown.
        Top anchors stay at the top of the screen in both cases.

        ### Parameters
        1. has_dialog : bool
            - True when a dialogue textbox is currently open.

        ### Returns
        1. int
            - Usable menu height in pixels.
        """

        if has_dialog:
            return MENU_SCREEN_HEIGHT - MENU_DIALOG_RESERVED_HEIGHT
        return MENU_SCREEN_HEIGHT

    def apply_menu_anchor(default_anchor: str, **kwargs) -> dict:
        """
        Stores the menu anchor in kwargs so every menu entry point can forward it.

        ### Parameters
        1. default_anchor : str
            - Nine-point anchor used by custom_menu_choice when kwargs has none.
        2. **kwargs
            - Existing menu kwargs. An explicit menu_anchor key wins over the parameter.

        ### Returns
        1. dict
            - kwargs with menu_anchor set.
        """

        kwargs['menu_anchor'] = get_kwargs('menu_anchor', default_anchor, **kwargs)
        return kwargs

    def call_custom_menu(with_leave: bool = True, *elements: MenuElement, menu_anchor: str = MENU_ANCHOR_DIALOG, **kwargs) -> None:
        """
        Calls a custom menu with the given elements and the given text and person.

        ### Parameters
        1. with_leave : bool, (default True)
            - Whether or not to display a leave button.
        2. *elements : MenuElement
            - The elements to display in the menu.
        3. menu_anchor : str, (default dialog)
            - "dialog" stacks the choices right-aligned on top of the dialogue box.
                Otherwise a nine-point anchor: top_left, top_center, top_right,
                middle_left, middle_center, middle_right, bottom_left, bottom_center,
                bottom_right. Middle and bottom shift up when dialogue is open.
        """

        kwargs = apply_menu_anchor(menu_anchor, **kwargs)

        in_event = get_kwargs('in_event', False, **kwargs)
        in_replay = get_kwargs('in_replay', False, **kwargs)
        no_gallery = get_kwargs("no_gallery", False, **kwargs)

        if not no_gallery and in_event:
            kwargs['is_decision_call'] = True

        disabled_elements = [element for element in elements if not element.check_for_label_existence()]

        if in_event and in_replay:
            made_decisions = get_kwargs('made_decisions', [], **kwargs)
            decision_data = get_kwargs('decision_data', {}, **kwargs)
            possible_decisions = get_decision_possibilities(decision_data, made_decisions)
            elements = [element for element in elements if element.get_key() in possible_decisions and not element.get_key() in disabled_elements]

        filtered_elements = [element for element in elements if element.check_conditions(**kwargs)]

        if len(filtered_elements) == 0:
            character.dev ("Oops something went wrong here. There seems to be nothing to choose from. Sry about that. I'll send you back to the map.")
            # character.dev (f"Error Code: [101]{kwargs['event_name']}:{';'.join([tag.split('.')[1] for tag in made_decisions])}")
            renpy.jump("map_entry")

        renpy.force_autosave(True)

        renpy.call("call_menu", None, None, with_leave, *filtered_elements, **kwargs)

    def call_custom_menu_with_text(text: str, person: Character = character.subtitles, with_leave: bool = True, *elements: MenuElement, menu_anchor: str = MENU_ANCHOR_DIALOG, **kwargs) -> None:
        """
        Calls a custom menu with the given elements and the given text and person.

        ### Parameters
        1. text : str
            - The text to display below the menu.
        2. person : Person
            - The person to display saying the text.
        3. with_leave : bool, (default True)
            - Whether or not to display a leave button.
        4. *elements : Tuple[str, str | Effect | List[Effect]] | Tuple[str, str | Effect | List[Effect], bool]
            - The elements to display in the menu. Each element is a tuple of the form (title, event_label, active), (title, effect, active) or (title, effect_list, active). The active parameter is optional and defaults to True.
        5. menu_anchor : str, (default dialog)
            - "dialog" stacks the choices right-aligned on top of the dialogue box.
                Otherwise a nine-point anchor: top_left, top_center, top_right,
                middle_left, middle_center, middle_right, bottom_left, bottom_center,
                bottom_right. Middle and bottom shift up when dialogue is open.

        """
        kwargs = apply_menu_anchor(menu_anchor, **kwargs)

        in_event = get_kwargs('in_event', False, **kwargs)
        in_replay = get_kwargs('in_replay', False, **kwargs)
        no_gallery = get_kwargs("no_gallery", False, **kwargs)

        if not no_gallery and in_event:
            kwargs['is_decision_call'] = True

        disabled_elements = [element for element in elements if not element.check_for_label_existence()]

        if in_event and in_replay and not no_gallery:
            made_decisions = get_kwargs('made_decisions', [], **kwargs)
            decision_data = get_kwargs('decision_data', {}, **kwargs)
            possible_decisions = get_decision_possibilities(decision_data, made_decisions)
            elements = [element for element in elements if element.get_key() in possible_decisions and not element.get_key() in disabled_elements]

        filtered_elements = [element for element in elements if element.check_conditions(**kwargs)]

        if len(filtered_elements) == 0:
            character.dev ("Oops something went wrong here. There seems to be nothing to choose from. Sry about that. I'll send you back to the map.")
            # character.dev (f"Error Code: [101]{kwargs['event_name']}:{';'.join([tag.split('.')[1] for tag in made_decisions])}")
            renpy.jump("map_entry")

        renpy.force_autosave(True)

        renpy.call("call_menu", text, person, with_leave, *filtered_elements, **kwargs)

    # endregion
    ############################

    

###########################
# region Call Menu Labels #
###########################

# calls a menu with the given elements
label call_menu(text, person, with_leave = True, *elements, **kwargs):
    # """
    # Calls a menu with the given elements and the given text and person.

    # ### Parameters
    # 1. text : str
    #     - The text to display below the menu.
    # 2. person : Person
    #     - The person to display saying the text.
    # 3. with_leave : bool, (default True)
    #     - Whether or not to display a leave button.
    # 4. *elements : MenuElement
    #     - The elements to display in the menu. 
    #     - Each element is a tuple of the form (title, event_label, active), (title, effect, active) or (title, effect_list, active). 
    #     - The active parameter is optional and defaults to True.
    # 5. menu_anchor : str, via kwargs (default middle_center)
    #     - Nine-point anchor forwarded to custom_menu_choice.
    # """

    if not with_leave and len(elements) == 1:
        $ renpy.call("call_element", elements[0].get_key(), elements[0].get_effects(), **kwargs)

    $ kwargs = apply_menu_anchor(MENU_ANCHOR_DIALOG, **kwargs)
    $ kwargs['has_dialog'] = text != None
    # the choices sit on top of the box, whose height follows the question's length
    $ kwargs['dialog_height'] = journal_dialog_box_height(text) if text != None else gui.textbox_height

    $ p_text = Character(kind = person, retain = False)

    if text != None and person != None:
        p_text "[text]" (interact = False)
    elif text != None:
        subtitles "[text]" (interact = False)
    else:
        subtitles_Empty "" (interact = False)

    while (True):
        if text == None:
            call screen custom_menu_choice(1, 7, list(elements), with_leave, **kwargs)
        else:
            show screen custom_menu_choice(1, 7, list(elements), with_leave, **kwargs)
        $ renpy.pause(hard = True)

# calls a menu specialized in use for events
label call_event_menu(text, events, fallback, person = character.subtitles, menu_anchor = "dialog", **kwargs):
    # """
    # Refines a list of events and calls a menu with the given elements and the given text and person.

    # ### Parameters
    # 1. text : str
    #     - The text to display below the menu.
    # 2. events : Dict[str, EventStorage]
    #     - The events to filter and refine for use in the menu.
    # 3. fallback : str
    #     - The event to call if no events are available.
    # 4. person : Person, (default character.subtitles)
    #     - The person to display saying the text.
    # 5. menu_anchor : str, (default middle_center)
    #     - Nine-point anchor forwarded to custom_menu_choice.
    # """

    $ kwargs = apply_menu_anchor(menu_anchor, **kwargs)

    $ renpy.block_rollback()

    $ bg_image = get_kwargs('bg_image', None, **kwargs)
    call show_idle_image(bg_image, **kwargs) from call_event_menu_3
    # polaroids to find on the background; begin_event and the map hide them again.
    # Hidden first so the new show puts it above the background screen just shown.
    hide screen collectible_spots
    show screen collectible_spots

    $ renpy.choice_for_skipping()

    $ kwargs['school_obj'] = get_character_by_key('school')
    $ kwargs['parent_obj'] = get_character_by_key('parent')
    $ kwargs['teacher_obj'] = get_character_by_key('teacher')
    $ kwargs['secretary_obj'] = get_character_by_key('secretary')

    $ event_list, high_prio, blocked_elements = clean_events_for_menu(events, **kwargs)

    if len(event_list) == 0:
        call call_event(fallback, **kwargs) from call_event_menu_1
        jump map_entry

    $ kwargs['marked'] = high_prio
    $ kwargs['blocked'] = blocked_elements

    call call_menu (text, person, True, *event_list, **kwargs) from call_event_menu_2

    jump new_daytime

# endregion
###########################

###########################
# region CUSTOM MENU BEEF #
###########################

style menu_text:
    color "#fff"
    textalign 0.5
    size 30
style blocked_menu_text take menu_text:
    color "#aaa"
style menu_text_left take menu_text:
    textalign 0.0
style menu_text_right take menu_text:
    textalign 1.0

# the Menu itself
screen custom_menu_choice(page, page_limit, elements, with_leave = True, **kwargs):
    # """
    # Displays a menu with the given elements.

    # ### Parameters
    # 1. page : int
    #     - The page to display.
    # 2. page_limit : int
    #     - The maximum amount of elements to display per page.
    # 3. elements : List[MenuElement]
    #     - The elements to display in the menu. 
    # 4. with_leave : bool, (default True)
    #     - Whether or not to display a leave button.
    # 5. **kwargs
    #     - Any additional keyword arguments are passed to the effects of the selected element.
    #     - menu_anchor : str, (default middle_center)
    #         Nine-point anchor: top_left, top_center, top_right, middle_left,
    #         middle_center, middle_right, bottom_left, bottom_center, bottom_right.
    #     - has_dialog : bool
    #         When True, middle and bottom anchors sit above the dialogue box.
    # """

    tag menu_choice

    python:
        renpy.choice_for_skipping()

        element_count = len(elements)

        overwrite_position = any(element.has_overwrite_position() for element in elements)

        marked_elements = get_kwargs('marked', [], **kwargs)

        blocked_elements = get_kwargs('blocked', [], **kwargs)

        menu_anchor = get_kwargs('menu_anchor', MENU_ANCHOR_DIALOG, **kwargs)
        has_dialog = get_kwargs('has_dialog', False, **kwargs)
        menu_xalign, menu_yalign = get_menu_anchor_align(menu_anchor)
        menu_height = get_menu_usable_height(has_dialog)

        kwargs.pop('menu_selection', None)

        # (active, title, title_text, effects, raw_title, position)
        buttons = []

        # get max amount of pages needed to display all elements
        max_pages = element_count // page_limit + 1
        if element_count % page_limit == 0:
            max_pages = element_count // page_limit
            
        start = (page - 1) * page_limit
        end = page * page_limit

        count = 1
        # display all elements for current page
        i = start
        while i < end:
            # display empty space if last page and no elements are remaining
            if i >= element_count:
                if overwrite_position:
                    break
                if max_pages != 1:
                    buttons.append(("inactive", -1, "", "", [], "", None))
            elif i < element_count:
                key = elements[i].get_key()
                title = elements[i].get_title()
                effects = elements[i].get_effects()
                active = elements[i].get_active()
                position = elements[i].get_overwrite_position()
                raw_title = str(effects)
                title_text = "[title]"
                number = -1
                if has_keyboard() and count < 10:
                    if show_shortcut():
                        title_text = title + " [[" + str(count) + "]"
                    if key not in blocked_elements:
                        number = count

                if key in marked_elements:
                    title_text = "{color=#a00000}●{/color}  " + title_text + "  {color=#a00000}●{/color}"

                if key in blocked_elements:
                    buttons.append(("inactive", number, title, title_text, effects, raw_title, position))
                else:
                    buttons.append(("active", number, title, title_text, effects, raw_title, position))
            count += 1
            i += 1

    # Each choice is a paper strip (gui/journal/ui/choice_slip.webp). Without an
    # explicit anchor ("dialog") the strips stack right-aligned on top of the
    # dialogue box, next to the line that asks the question; the nine classic
    # anchors still place the stack anywhere else.
    $ dialog_anchor = menu_anchor == MENU_ANCHOR_DIALOG
    $ slip_xalign = 1.0 if dialog_anchor else menu_xalign

    if overwrite_position:
        for button in buttons:
            $ active, number, title, title_text, effects, raw_title, position = button
            if number != -1:
                key ("K_" + str(number)) action Call("call_element", title, effects, menu_selection = raw_title, **kwargs)
                key ("K_KP" + str(number)) action Call("call_element", title, effects, menu_selection = raw_title, **kwargs)
            if active != "empty" and position is not None:
                fixed:
                    pos (position[0], position[1])
                    fit_first True
                    use jr_choice_slip(title, number, (active == "active"), (title_text.startswith("{color=#a00000}")),
                        Call("call_element", title, effects, menu_selection = raw_title, **kwargs))
        if with_leave:
            if has_keyboard():
                key "K_ESCAPE" action Call("close_menu", **kwargs)
            fixed:
                pos (1880, 1040 - quick_menu_reserved_height())
                anchor (1.0, 1.0)
                fit_first True
                use jr_choice_leave(Call("close_menu", **kwargs))
    else:
        if dialog_anchor:
            # right edge 40px in, bottom just above the dialogue box, or without one
            # above the quick menu patch in the bottom right corner
            $ dialog_height = get_kwargs('dialog_height', gui.textbox_height, **kwargs)
            $ stack_area = (0, 0, MENU_SCREEN_WIDTH - 40, (MENU_SCREEN_HEIGHT - dialog_height - 6) if has_dialog else (MENU_SCREEN_HEIGHT - max(40, quick_menu_reserved_height() + 10)))
        else:
            $ stack_area = (40, 30, MENU_SCREEN_WIDTH - 80, menu_height - 60)
            if menu_xalign == 1.0 and menu_yalign == 1.0 and not has_dialog:
                $ stack_area = (40, 30, MENU_SCREEN_WIDTH - 80, menu_height - 30 - max(30, quick_menu_reserved_height()))

        frame:
            background None
            area stack_area

            vbox:
                xalign (1.0 if dialog_anchor else menu_xalign)
                yalign (1.0 if dialog_anchor else menu_yalign)
                spacing 4

                for index, button in enumerate(buttons):
                    $ active, number, title, title_text, effects, raw_title, position = button

                    if number != -1:
                        key ("K_" + str(number)) action Call("call_element", title, effects, menu_selection = raw_title, **kwargs)
                        key ("K_KP" + str(number)) action Call("call_element", title, effects, menu_selection = raw_title, **kwargs)

                    if active == "empty" or (title == "" and number == -1):
                        null height 60
                    else:
                        # a little stagger so the stack looks hand-placed, not printed
                        $ stagger = [0, 16, 6, 22, 2, 14, 8][index % 7]
                        fixed:
                            fit_first True
                            xalign slip_xalign
                            xoffset (-stagger if slip_xalign == 1.0 else stagger if slip_xalign == 0.0 else 0)
                            use jr_choice_slip(title, number, (active == "active"), (title_text.startswith("{color=#a00000}")),
                                Call("call_element", title, effects, menu_selection = raw_title, **kwargs))

                # pages, when there are more choices than fit
                if max_pages != 1:
                    null height 6
                    hbox:
                        xalign slip_xalign
                        spacing 8
                        $ prev_key = "  ," if has_keyboard() and show_shortcut() else ""
                        $ next_key = "  ." if has_keyboard() and show_shortcut() else ""
                        if start != 0:
                            if has_keyboard():
                                key "K_COMMA" action Show("custom_menu_choice", None, page - 1, page_limit, elements, with_leave, **kwargs)
                            textbutton "‹ previous[prev_key]":
                                style "jr_choice_slip"
                                text_style "jr_choice_small"
                                action Show("custom_menu_choice", None, page - 1, page_limit, elements, with_leave, **kwargs)
                        text "[page] / [max_pages]" style "jr_choice_small" color "#f2e6cc" outlines [(2, "#140d08", 0, 0)] yalign 0.5
                        if end < element_count:
                            if has_keyboard():
                                key "K_PERIOD" action Show("custom_menu_choice", None, page + 1, page_limit, elements, with_leave, **kwargs)
                            textbutton "next ›[next_key]":
                                style "jr_choice_slip"
                                text_style "jr_choice_small"
                                action Show("custom_menu_choice", None, page + 1, page_limit, elements, with_leave, **kwargs)

                # with the dialogue box open, Leave is a small link inside the box instead
                if with_leave and not (dialog_anchor and has_dialog):
                    null height 6
                    fixed:
                        fit_first True
                        xalign slip_xalign
                        use jr_choice_leave(Call("close_menu", **kwargs))

        if with_leave:
            if has_keyboard():
                key "K_ESCAPE" action Call("close_menu", **kwargs)
            if dialog_anchor and has_dialog:
                $ leave_key = "   esc" if has_keyboard() and show_shortcut() else ""
                textbutton "Leave ›[leave_key]":
                    style "jr_entry_button"
                    text_style "jr_value"
                    text_size 26
                    text_color "#eedebe"
                    text_hover_color "#ffffff"
                    pos (1880, MENU_SCREEN_HEIGHT - get_kwargs('dialog_height', gui.textbox_height, **kwargs) + 22)
                    xanchor 1.0
                    action Call("close_menu", **kwargs)

screen jr_choice_slip(title, number, active, marked, action):
    # """
    # One choice on its paper strip: the shortcut digit, the text (marker
    # swipe on hover), a red asterisk for the important ones, struck through
    # when it can't be picked right now.
    # """

    button:
        style "jr_choice_slip"
        sensitive active
        action action
        hbox:
            spacing 12
            if number != -1 and has_keyboard() and show_shortcut():
                text str(number) style "jr_choice_number" yalign 0.5
            frame:
                style "jr_choice_label"
                yalign 0.5
                if active:
                    text "[title]" style "jr_choice_text"
                else:
                    text "{s}[title]{/s}" style "jr_choice_text"
            if marked:
                text "*" style "jr_choice_text" font JR_FONT_BOLD size 40 color JR_ACCENT yalign 0.3

screen jr_choice_leave(action):
    $ leave_key = "   esc" if has_keyboard() and show_shortcut() else ""
    textbutton "Leave ›[leave_key]":
        style "jr_choice_slip"
        text_style "jr_choice_text"
        text_color JR_ACCENT
        action action

style jr_choice_slip:
    background Frame("gui/journal/ui/choice_slip.webp", 14, 12, 14, 14)
    padding (26, 12, 32, 18)
    xminimum 300
    xmaximum 980

style jr_choice_slip:
    variant "touch"
    padding (30, 18, 36, 24)

style jr_choice_label:
    background None
    hover_background Frame("gui/journal/ui/highlight.webp", 12, 0, 12, 0)
    padding (8, 0, 10, 0)

style jr_choice_text is jr_text:
    font JR_FONT_MEDIUM
    size 30
    hover_color "#000"
    insensitive_color JR_PENCIL

style jr_choice_small is jr_choice_text:
    size 22

style jr_choice_number is jr_typed:
    size 20
    color JR_PENCIL

# calls the effect of a selected choice
label call_element(key, effects, **kwargs):
    # """
    # Calls the effect of a selected choice in the menu.

    # ### Parameters
    # 1. effects : str | Effect | List[Effect]
    #     - The effect to call.
    #     - if effects is a string, it is interpreted as an event label.
    # """

    hide screen custom_menu_choice
    hide screen image_with_nude_var

    $ in_event = get_kwargs('in_event', False, **kwargs)
    $ in_replay = get_kwargs('in_replay', False, **kwargs)
    $ no_gallery = get_kwargs("no_gallery", False, **kwargs)

    if not no_gallery and in_event:
        if not in_replay:
            $ register_decision(key)
        else:
            if 'made_decisions' not in kwargs.keys():
                $ kwargs['made_decisions'] = [key]
            else:
                $ kwargs['made_decisions'].append(key)

    if isinstance(effects, str):
        $ renpy.call(effects, **kwargs)

    if isinstance(effects, Effect):
        $ kwargs = call_effects(effects, **kwargs)

    if isinstance(effects, List) and all(isinstance(effect, Effect) for effect in effects):
        $ i = 0
        while (i < len(effects)):
            $ kwargs = call_effects(effects[i], **kwargs)
            $ i += 1

    $ override = get_kwargs('override_menu_exit', None, **kwargs)
    if override != None:
        if isinstance(override, str):
            $ renpy.call(override)
        elif isinstance(override, Event):
            $ renpy.call(override.get_event())

    $ override_kwargs = get_kwargs('override_menu_exit_with_kwargs', None, **kwargs)
    if override_kwargs != None:
        if isinstance(override_kwargs, str):
            $ renpy.call(override_kwargs, **kwargs)
        elif isinstance(override_kwargs, Event):
            $ override_kwargs.call(**kwargs)
        elif isinstance(override_kwargs, Effect):
            $ override_kwargs.apply(**kwargs)

    return

# closes the current menu
label close_menu(**kwargs):
    # """
    # Closes the current menu.
    # """
    hide screen custom_menu_choice
    hide screen image_with_nude_var

    $ override = get_kwargs('override_menu_exit', None, **kwargs)
    if override != None:
        if isinstance(override, str):
            $ renpy.call(override)
        elif isinstance(override, Event):
            $ renpy.call(override.get_event())
    $ override_kwargs = get_kwargs('override_menu_exit_with_kwargs', None, **kwargs)
    if override_kwargs != None:
        if isinstance(override_kwargs, str):
            $ renpy.call(override_kwargs, **kwargs)
        elif isinstance(override_kwargs, Event):
            $ override_kwargs.call(**kwargs)
        elif isinstance(override_kwargs, Effect):
            $ override_kwargs.apply(**kwargs)
    jump map_entry

# endregion
###########################