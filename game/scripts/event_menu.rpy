style menu_text:
    color "#fff"
    textalign 0.5
    size 30

style menu_text_left take menu_text:
    textalign 0.0

style menu_text_right take menu_text:
    textalign 1.0

init -1 python:
    def clean_events_for_menu(events, school = "x"):
        output = []
        used = []

        # remove events that have no applicable events
        for key in events.keys():
            if (events[key].count_available_events(school) > 0 and key not in used):
                output.append((events[key].get_title(), EventEffect(events[key])))
                used.append(key)

        return output
        

label call_event_menu(text, page, page_limit, events, fallback, person = character.subtitles, school = "x"):
    $ event_list = clean_events_for_menu(events, school)

    if len(event_list) == 0:
        call call_event(fallback) from call_event_menu_1
        jump map_overview

    show text "text"
    $ person ("[text]", interact=False)

    call screen custom_menu_choice(page, page_limit, event_list)

    jump new_daytime

label call_event(event_obj, priority = 0):
    hide screen menu_event_choice

    if isinstance(event_obj, EventStorage):
        $ event_obj.call_available_event()


    if isinstance(event_obj, Event):
        $ event_obj = event_obj.get_event()

    if isinstance(event_obj, str):
        call expression event_obj from call_event_1

    $ i = 0
    while(len(event_obj) > i):
        call expression event_obj[i] from call_event_2
        $ i += 1

    

screen menu_event_choice(page, page_limit, events):
    tag menu_choice

    $ event_count = len(events)

    frame:
        background "#ffffff00"
        area(367, 0, 1185, 800)

        vbox:
            xalign 0.5 
            yalign 0.5

            # get max amount of pages needed to display all elements
            $ max_pages = event_count // page_limit + 1
            if event_count % page_limit == 0:
                $ max_pages = event_count // page_limit
                
            $ start = (page - 1) * page_limit
            $ end = page * page_limit

            $ event_keys = list(events.keys())

            # display all elements for current page
            for i in range(start, end):
                # display empty space if last page and no elements are remaining
                if i >= event_count and max_pages != 1:
                    null height 78
                # display element
                elif i < event_count:
                    $ event = events[event_keys[i]]
                    button:
                        background "gui/button/choice_idle_background.png"
                        hover_background "gui/button/choice_hover_background.png"
                        text event.get_title() style "menu_text":
                            xalign 0.5
                            yalign 0.5
                        xsize 1185
                        action Call("call_event", event)
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
                            action Show("menu_event_choice", None, page - 1, page_limit, events)
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
                    if end < event_count:
                        button:
                            background "gui/button/choice_idle_background_250px.png"
                            hover_background "gui/button/choice_hover_background_250px.png"
                            text "Next >>  " style "menu_text_right":
                                xalign 0.5
                                yalign 0.0
                            xsize 250
                            ysize 52
                            action Show("menu_event_choice", None, page + 1, page_limit, events)
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
                action Jump("map_overview")
    