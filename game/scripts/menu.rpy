init python:
    from typing import Tuple, Union, List

    def call_custom_menu(with_leave: bool = True, *elements: Tuple[str, str | Effect | List[Effect]] | Tuple[str, str | Effect | List[Effect], bool], **kwargs) -> None:
        """
        Calls a custom menu with the given elements and the given text and person.

        ### Parameters
        1. with_leave : bool, (default True)
            - Whether or not to display a leave button.
        2. *elements : Tuple[str, str | Effect | List[Effect]] | Tuple[str, str | Effect | List[Effect], bool]
            - The elements to display in the menu. Each element is a tuple of the form (title, event_label, active), (title, effect, active) or (title, effect_list, active). The active parameter is optional and defaults to True.

        """
        filtered_elements = [tupleEl for tupleEl in elements if len(tupleEl) == 2 or tupleEl[2]]
        renpy.call("call_menu", None, None, with_leave, *filtered_elements, **kwargs)

    def call_custom_menu_with_text(text: str, person: Person, with_leave: bool = True, *elements: Tuple[str, str | Effect | List[Effect]] | Tuple[str, str | Effect | List[Effect], bool], **kwargs) -> None:
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


        filtered_elements = [tupleEl for tupleEl in elements if len(tupleEl) == 2 or tupleEl[2]]
        renpy.call("call_menu", text, person, with_leave, *filtered_elements, **kwargs)

    def clean_events_for_menu(events: Dict[str, EventStorage], **kwargs) -> List[Tuple[str, EventEffect]]:
        """
        Cleans a list of events for use in a menu.
        It takes each EventStorage in events and checks if it has any applicable events. If it does, it adds it to the output list.
        The elements in the output list are tuples of the form (title, EventEffect).

        ### Parameters
        1. events : Dict[str, EventStorage]
            - The events to filter and refine for use in the menu.

        ### Returns
        1. List[Tuple[str, EventEffect]]
            - The list of events that have applicable events and their effects.
        """

        output = []
        used = []

        # remove events that have no applicable events
        for key in events.keys():
            if (events[key].count_available_events(**kwargs) > 0 and key not in used):
                output.append((events[key].get_title(), EventEffect(events[key])))
                used.append(key)

        return output
        

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
    # 4. *elements : Tuple[str, str | Effect | List[Effect]] | Tuple[str, str | Effect | List[Effect], bool]
    #     - The elements to display in the menu. 
    #     - Each element is a tuple of the form (title, event_label, active), (title, effect, active) or (title, effect_list, active). 
    #     - The active parameter is optional and defaults to True.
    # """

    if not with_leave and len(elements) == 1:
        $ title, effects, _active = None, None, None
        if len(elements[0]) == 2:
            $ title, effects = elements[0]
        else:
            $ title, effects, _active = elements[0]
        $ renpy.call("call_element", effects, **kwargs)

    if text != None and person != None:
        $ person ("[text]", interact=False)
    else:
        subtitles_Empty "" (interact=False)

    while (True):
        call screen custom_menu_choice(1, 7, list(elements), with_leave, **kwargs)

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

    $ event_list = clean_events_for_menu(events, **kwargs)

    if len(event_list) == 0:
        call call_event(fallback, **kwargs) from call_event_menu_1
        jump map_overview

    call call_menu (text, person, True, *event_list, **kwargs) from call_event_menu_2

    jump new_daytime

# calls the effect of a selected choice
label call_element(effects, **kwargs):
    # """
    # Calls the effect of a selected choice in the menu.

    # ### Parameters
    # 1. effects : str | Effect | List[Effect]
    #     - The effect to call.
    #     - if effects is a string, it is interpreted as an event label.
    # """

    hide screen custom_menu_choice
    hide screen image_with_nude_var

    if isinstance(effects, str):
        $ renpy.call(effects, **kwargs)

    $ call_effects(effects, **kwargs)

# closes the current menu
label close_menu():
    # """
    # Closes the current menu.
    # """
    hide screen custom_menu_choice
    hide screen image_with_nude_var
    jump map_overview

style menu_text:
    color "#fff"
    textalign 0.5
    size 30
style menu_text_left take menu_text:
    textalign 0.0
style menu_text_right take menu_text:
    textalign 1.0

screen custom_menu_choice(page, page_limit, elements, with_leave = True, **kwargs):
    # """
    # Displays a menu with the given elements.

    # ### Parameters
    # 1. page : int
    #     - The page to display.
    # 2. page_limit : int
    #     - The maximum amount of elements to display per page.
    # 3. elements : List[Tuple[str, str | Effect | List[Effect]] | Tuple[str, str | Effect | List[Effect], bool]]
    #     - The elements to display in the menu. 
    #     - Each element is a tuple of the form (title, event_label, active), (title, effect, active) or (title, effect_list, active). 
    #     - The active parameter is optional and defaults to True.
    # 4. with_leave : bool, (default True)
    #     - Whether or not to display a leave button.
    # 5. **kwargs
    #     - Any additional keyword arguments are passed to the effects of the selected element.
    # """

    tag menu_choice

    $ element_count = len(elements)

    frame:
        background "#ffffff00"
        area(367, 0, 1185, 800)

        vbox:
            xalign 0.5 
            yalign 0.5

            # get max amount of pages needed to display all elements
            $ max_pages = element_count // page_limit + 1
            if element_count % page_limit == 0:
                $ max_pages = element_count // page_limit
                
            $ start = (page - 1) * page_limit
            $ end = page * page_limit

            $ count = 1
            # display all elements for current page
            for i in range(start, end):
                # display empty space if last page and no elements are remaining
                if i >= element_count and max_pages != 1:
                    null height 78
                # display element
                elif i < element_count:
                    $ title, effects, _active = None, None, None
                    if len(elements[i]) == 2:
                        $ title, effects = elements[i]
                    else:
                        $ title, effects, _active = elements[i]
                    $ title_text = "[title]"
                    if has_keyboard() and count < 10:
                        if show_shortcut():
                            $ title_text = "[title] [[[count]]"
                        key ("K_" + str(count)) action Call("call_element", effects, **kwargs)
                        key ("K_KP" + str(count)) action Call("call_element", effects, **kwargs)
                    button:
                        background "gui/button/choice_idle_background.png"
                        hover_background "gui/button/choice_hover_background.png"
                        text title_text style "menu_text":
                            xalign 0.5
                            yalign 0.5
                        xsize 1185
                        xalign 0.5
                        action Call("call_element", effects, **kwargs)
                        
                    null height 30
                $ count += 1
                
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
                            background "gui/button/choice_idle_background_250px.png"
                            hover_background "gui/button/choice_hover_background_250px.png"
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
                    key "K_ESCAPE" action Jump("close_menu")
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
                        action Jump("close_menu")
    