python:
    from typing import Tuple, Union, List

    def call_custom_menu(elements: List[Tuple[str, Union[Effect, List[Effect]]]]):
        renpy.call_screen("custom_menu_choice", 1, 7, elements)

label call_element(effects, school = "x"):
    hide screen custom_menu_choice
    hide screen image_with_nude_var
    hide None
    $ call_effects(school, effects)

label close_menu():
    hide screen custom_menu_choice
    hide screen image_with_nude_var
    hide None
    jump map_overview

screen custom_menu_choice(page, page_limit, elements, school = "x"):
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

            # display all elements for current page
            for i in range(start, end):
                # display empty space if last page and no elements are remaining
                if i >= element_count and max_pages != 1:
                    null height 78
                # display element
                elif i < element_count:
                    $ title, effects = elements[i]
                    button:
                        background "gui/button/choice_idle_background.png"
                        hover_background "gui/button/choice_hover_background.png"
                        text title style "menu_text":
                            xalign 0.5
                            yalign 0.5
                        xsize 1185
                        action Call("call_element", effects, school)
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
                        button:
                            background "gui/button/choice_idle_background_250px.png"
                            hover_background "gui/button/choice_hover_background_250px.png"
                            text "  << Prev" style "menu_text_left":
                                xalign 0.5
                                yalign 0.0
                            xsize 250
                            ysize 52
                            action Show("custom_menu_choice", None, page - 1, page_limit, elements, school)
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
                        button:
                            background "gui/button/choice_idle_background_250px.png"
                            hover_background "gui/button/choice_hover_background_250px.png"
                            text "Next >>  " style "menu_text_right":
                                xalign 0.5
                                yalign 0.0
                            xsize 250
                            ysize 52
                            action Show("custom_menu_choice", None, page + 1, page_limit, elements, school)
                    else:
                        null width 250 height 52

            null height 30

            button:
                background "gui/button/choice_idle_background.png"
                hover_background "gui/button/choice_hover_background.png"
                text "Leave" style "menu_text":
                    xalign 0.5
                    yalign 0.5
                xsize 1185
                action Jump("close_menu")
    