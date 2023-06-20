style menu_text:
    color "#fff"
    textalign 0.5
    size 30

style menu_text_left take menu_text:
    textalign 0.0

style menu_text_right take menu_text:
    textalign 1.0

init python:
    def clean_events_for_menu(events, titles, *key_excludes):
        print("Clean events")
        event_keys = list(events.keys())

        # remove events that should be excluded
        for key in key_excludes:
            if key in event_keys:
                event_keys.remove(key)

        # remove events that have no applicable events
        for key in events.keys():
            if (key not in titles or get_events_area_count(key, events) == 0) and key in event_keys:
                event_keys.remove(key)

        return event_keys
        

label call_event_menu(text, page, page_limit, events, titles, *key_excludes, person = character.subtitles):

    python:
        print("call menu")

    $ event_keys = clean_events_for_menu(events, titles, key_excludes)

    python:
        print(event_keys)

    if len(event_keys) == 0:
        call call_fallback_from_menu(events["fallback"])
        jump map_overview

    show screen menu_event_choice(page, page_limit, event_keys, titles)

    while True:
        person "[text]"

    

screen menu_event_choice(page, page_limit, event_keys, titles):
    tag menu_choice

    frame:
        background "#ffffff00"
        area(367, 0, 1185, 800)

        vbox:
            xalign 0.5 
            yalign 0.5

            # get max amount of pages needed to display all elements
            $ max_pages = len(event_keys) // page_limit + 1
            if len(event_keys) % page_limit == 0:
                $ max_pages = len(event_keys) // page_limit
                
            $ start = (page - 1) * page_limit
            $ end = page * page_limit

            python:
                print("\n\n\n----------")
                print(event_keys)
            # display all elements for current page
            for i in range(start, end):
                python:
                    print("pos:" + str(i) + " length:" + str(len(event_keys)))
                # display empty space if last page and no elements are remaining
                if i >= len(event_keys) and max_pages != 1:
                    null height 78
                # display element
                elif i < len(event_keys):
                    $ key = event_keys[i]
                    button:
                        background "gui/button/choice_idle_background.png"
                        hover_background "gui/button/choice_hover_background.png"
                        text titles[key] style "menu_text":
                            xalign 0.5
                            yalign 0.5
                        xsize 1185
                        action Call("call_event_from_menu", key, events)
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
                            action Show("menu_event_choice", None, page - 1, page_limit, event_keys, titles)
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
                    if end < len(event_keys):
                        button:
                            background "gui/button/choice_idle_background_250px.png"
                            hover_background "gui/button/choice_hover_background_250px.png"
                            text "Next >>  " style "menu_text_right":
                                xalign 0.5
                                yalign 0.0
                            xsize 250
                            ysize 52
                            action Show("menu_event_choice", None, page + 1, page_limit, event_keys, titles)
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
            
label call_event_from_menu(key, events):
    hide screen menu_event_choice

    call event_check_area(key, events)

label call_fallback_from_menu(key):
    hide screen menu_event_choice

    call expression key