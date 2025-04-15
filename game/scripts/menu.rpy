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
            log_error(102, f"Label '{label}' does not exist.")
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

    def call_custom_menu(with_leave: bool = True, *elements: MenuElement, **kwargs) -> None:
        """
        Calls a custom menu with the given elements and the given text and person.

        ### Parameters
        1. with_leave : bool, (default True)
            - Whether or not to display a leave button.
        2. *elements : MenuElement
            - The elements to display in the menu.
        """

        in_event = get_kwargs('in_event', False, **kwargs)
        in_replay = get_kwargs('in_replay', False, **kwargs)
        no_gallery = get_kwargs("no_gallery", False, **kwargs)

        log_val("elements", elements)

        if not no_gallery and in_event:
            kwargs['is_decision_call'] = True

        disabled_elements = [element for element in elements if not element.check_for_label_existence()]

        if in_event and in_replay:
            made_decisions = get_kwargs('made_decisions', [], **kwargs)
            decision_data = get_kwargs('decision_data', {}, **kwargs)
            possible_decisions = get_decision_possibilities(decision_data, made_decisions)
            elements = [element for elements in elements if element.get_key() in possible_decisions and not element.get_key() in disabled_elements]

        filtered_elements = [element for element in elements if element.check_conditions(**kwargs)]

        if len(filtered_elements) == 0:
            character.dev ("Oops something went wrong here. There seems to be nothing to choose from. Sry about that. I'll send you back to the map.")
            # character.dev (f"Error Code: [101]{kwargs['event_name']}:{';'.join([tag.split('.')[1] for tag in made_decisions])}")
            renpy.jump("map_overview")

        renpy.force_autosave(True)

        log_val("filtered_elements", filtered_elements)

        renpy.call("call_menu", None, None, with_leave, *filtered_elements, **kwargs)

    def call_custom_menu_with_text(text: str, person: Character = character.subtitles, with_leave: bool = True, *elements: MenuElement, **kwargs) -> None:
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

        """
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
            elements = [element for elements in elements if element.get_key() in possible_decisions and not element.get_key() in disabled_elements]

        filtered_elements = [element for element in elements if element.check_conditions(**kwargs)]

        if len(filtered_elements) == 0:
            character.dev ("Oops something went wrong here. There seems to be nothing to choose from. Sry about that. I'll send you back to the map.")
            # character.dev (f"Error Code: [101]{kwargs['event_name']}:{';'.join([tag.split('.')[1] for tag in made_decisions])}")
            renpy.jump("map_overview")

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
    # """

    if not with_leave and len(elements) == 1:
        $ renpy.call("call_element", elements[0].get_key(), elements[0].get_effects(), **kwargs)

    $ p_text = Character(kind = person, retain = False)

    if text != None and person != None:
        p_text "[text]" (interact = False)
    elif text != None:
        subtitles "[text]" (interact = False)

    while (True):
        show screen custom_menu_choice(1, 7, list(elements), with_leave, **kwargs)
        $ renpy.pause(hard = True)

# calls a menu specialized in use for events
label call_event_menu(text, events, fallback, person = character.subtitles, **kwargs):
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
    # """

    $ renpy.block_rollback()

    $ bg_image = get_kwargs('bg_image', None, **kwargs)
    call show_idle_image(bg_image, **kwargs) from call_event_menu_3

    $ renpy.choice_for_skipping()

    $ kwargs['school_obj'] = get_character_by_key('school')
    $ kwargs['parent_obj'] = get_character_by_key('parent')
    $ kwargs['teacher_obj'] = get_character_by_key('teacher')
    $ kwargs['secretary_obj'] = get_character_by_key('secretary')

    $ event_list, high_prio, blocked_elements = clean_events_for_menu(events, **kwargs)

    if len(event_list) == 0:
        call call_event(fallback, **kwargs) from call_event_menu_1
        jump map_overview

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
    # """

    tag menu_choice

    python:
        renpy.choice_for_skipping()

        element_count = len(elements)

        overwrite_position = any(element.has_overwrite_position() for element in elements)

        marked_elements = get_kwargs('marked', [], **kwargs)

        blocked_elements = get_kwargs('blocked', [], **kwargs)

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

    if overwrite_position:
        frame:
            background "#ffffff00"
            area(0, 0, 1920, 1080)
            $ lowest_y_pos = 0
            for button in buttons:
                $ active, number, title, title_text, effects, raw_title, position = button
                $ title_text = "     " + title_text + "     "
                $ x_pos = position[0]
                $ y_pos = position[1]

                if number != -1:
                    key ("K_" + str(number)) action Call("call_element", title, effects, menu_selection = raw_title, **kwargs)
                    key ("K_KP" + str(number)) action Call("call_element", title, effects, menu_selection = raw_title, **kwargs)

                if active == "empty":
                    null height 78
                elif active == "active":
                    button:
                        background Frame("gui/button/choice_idle_background.png", 1, 1, True)
                        hover_background Frame("gui/button/choice_hover_background.png", 1, 1, True)
                        text title_text style "menu_text":
                            xalign 0.5
                            yalign 0.5
                        xpos x_pos
                        ypos y_pos
                        action Call("call_element", title, effects, menu_selection = raw_title, **kwargs)
                else:
                    button:
                        background Frame("gui/button/choice_blocked_background.png", 1, 1, True)
                        text title_text style "blocked_menu_text":
                            xalign 0.5
                            yalign 0.5
                        xpos x_pos
                        ypos y_pos
                        action NullAction()
            if with_leave:
                $ l_text = ""
                if has_keyboard():
                    if show_shortcut():
                        $ l_text = " [Esc]"
                    key "K_ESCAPE" action Call("close_menu", **kwargs)
                hbox:
                    xsize 1920
                    button:
                        background "gui/button/choice_idle_background.png"
                        hover_background "gui/button/choice_hover_background.png"
                        text "Leave[l_text]" style "menu_text":
                            xalign 0.5
                            yalign 0.5
                        xsize 1185
                        xalign 0.5
                        yalign 0.0
                        action Call("close_menu", **kwargs)
    else:
        frame:
            background "#ffffff00"
            area(367, 0, 1185, 800)

            vbox:
                xalign 0.5 
                yalign 0.5

                for button in buttons:
                    $ active, number, title, title_text, effects, raw_title, position = button
                    
                    if number != -1:
                        key ("K_" + str(number)) action Call("call_element", title, effects, menu_selection = raw_title, **kwargs)
                        key ("K_KP" + str(number)) action Call("call_element", title, effects, menu_selection = raw_title, **kwargs)

                    if active == "empty":
                        null height 78
                    elif active == "active":
                        button:
                            background Frame("gui/button/choice_idle_background.png", 1, 1, True)
                            hover_background Frame("gui/button/choice_hover_background.png", 1, 1, True)
                            text title_text style "menu_text":
                                xalign 0.5
                                yalign 0.5
                            xsize 1185
                            xalign 0.5
                            action Call("call_element", title, effects, menu_selection = raw_title, **kwargs)
                    else:
                        button:
                            background Frame("gui/button/choice_blocked_background.png", 1, 1, True)
                            text title_text style "blocked_menu_text":
                                xalign 0.5
                                yalign 0.5
                            xsize 1185
                            xalign 0.5
                            action NullAction()
                    null height 30
                # display paginator if needed
                if max_pages != 1:
                    null height 30
                    hbox:
                        xsize 500
                        ysize 52
                        xalign 0.5

                        # go to previous page
                        if start != 0:
                            $ prev_text = ""
                            if has_keyboard():
                                if show_shortcut():
                                    $ prev_text = "[,]"
                                key "K_COMMA" action Show("custom_menu_choice", None, page - 1, page_limit, elements, **kwargs)
                            button:
                                background Frame("gui/button/choice_idle_background_250px.png")
                                hover_background Frame("gui/button/choice_hover_background_250px.png")
                                text "[prev_text]  << Prev" style "menu_text_left":
                                    xalign 0.5
                                    yalign 0.0
                                xsize 250
                                ysize 52
                                action Show("custom_menu_choice", None, page - 1, page_limit, elements, **kwargs)
                        else:
                            null width 250 height 52
                        
                        # display for current page
                        button:
                            background "gui/button/choice_idle_background_250px.png"
                            text "([page] / [max_pages])" style "menu_text":
                                xalign 0.5
                                yalign 0.0
                            xsize 250
                            ysize 52

                        # go to next page
                        if end < element_count:
                            $ next_text = ""
                            if has_keyboard():
                                if show_shortcut():
                                    $ next_text = "[.]"
                                key "K_PERIOD" action Show("custom_menu_choice", None, page + 1, page_limit, elements, **kwargs)
                            button:
                                background "gui/button/choice_idle_background_250px.png"
                                hover_background "gui/button/choice_hover_background_250px.png"
                                text "Next >>  [next_text]" style "menu_text_right":
                                    xalign 0.5
                                    yalign 0.0
                                xsize 250
                                ysize 52
                                action Show("custom_menu_choice", None, page + 1, page_limit, elements, **kwargs)
                        else:
                            null width 250 height 52
                
                null height 30

                if with_leave:
                    $ l_text = ""
                    if has_keyboard():
                        if show_shortcut():
                            $ l_text = " [Esc]"
                        key "K_ESCAPE" action Call("close_menu", **kwargs)
                    hbox:
                        xsize 1920
                        button:
                            background "gui/button/choice_idle_background.png"
                            hover_background "gui/button/choice_hover_background.png"
                            text "Leave[l_text]" style "menu_text":
                                xalign 0.5
                                yalign 0.5
                            xsize 1185
                            xalign 0.5
                            action Call("close_menu", **kwargs)

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
    jump map_overview

# endregion
###########################