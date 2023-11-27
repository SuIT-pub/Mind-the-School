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

    def clean_events_for_menu(events: Dict[str, Event], **kwargs) -> List[Tuple[str, EventEffect]]:
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
    $ event_list = clean_events_for_menu(events, **kwargs)

    if len(event_list) == 0:
        call call_event(fallback, **kwargs) from call_event_menu_1
        jump map_overview

    call call_menu (text, person, True, *event_list, **kwargs) from call_event_menu_2

    jump new_daytime

# calls the effect of a selected choice
label call_element(effects, **kwargs):
    hide screen custom_menu_choice
    hide screen image_with_nude_var

    if isinstance(effects, str):
        $ renpy.call(effects, **kwargs)

    $ call_effects(effects, **kwargs)

# closes the current menu
label close_menu():
    hide screen custom_menu_choice
    hide screen image_with_nude_var
    jump map_overview

screen custom_menu_choice(page, page_limit, elements, with_leave = True, **kwargs):
    tag menu_choice

    $ element_count = len(elements)

    $ keyboard = (not renpy.android and not renpy.ios)

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
                    if keyboard and count < 10:
                        $ title_text = "[title] ([count])"
                        key str(count) action Call("call_element", effects, **kwargs)
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
                        key "," action Show("custom_menu_choice", None, page - 1, page_limit, elements, **kwargs)
                        button:
                            background "gui/button/choice_idle_background_250px.png"
                            hover_background "gui/button/choice_hover_background_250px.png"
                            text "  << Prev" style "menu_text_left":
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
                        key "." action Show("custom_menu_choice", None, page + 1, page_limit, elements, **kwargs)
                        button:
                            background "gui/button/choice_idle_background_250px.png"
                            hover_background "gui/button/choice_hover_background_250px.png"
                            text "Next >>  " style "menu_text_right":
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
                if keyboard:
                    $ l_text = " (⌫)"
                    key "K_BACKSPACE" action Jump("close_menu")
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
    