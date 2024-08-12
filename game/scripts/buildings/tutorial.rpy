######################
# ----- SCREENS -----#
######################

screen show_building_button(building, display, show_type, x, y):
    if display == building or display == "x" or building in display or (isinstance(display, dict) and building in display.keys()):
        if isinstance(display, dict):
            $ show_type = display[building]
        $ image_text = f"background/{building}.webp"
        if show_type == "red":
            $ image_text = f"background/{building}_red.webp"
        elif show_type == "white":
            $ image_text = f"background/{building}_white.webp"
        add image_text:
            xpos x ypos y

screen show_rectangle(xpos, ypos, width, height):
    frame:
        area(xpos, ypos, width, height)


screen show_building_buttons (building, *additions, show_type = "normal", frames = []):
    # """
    # Shows a mockup map of the school with buttons for each building.

    # # Parameters:
    # 1. building: str | List[str] | Dict[str, str]
    #     - The building to highlight.
    #     - If a list is passed, all buildings in the list will be highlighted.
    #     - If a dictionary is passed, the keys are the buildings to highlight and the values are the show_type for each building.
    # 2. *additions: str
    #     - Additional elements to show.
    #     - "stats": Show the stats on the right side.
    #     - "time": Show the time on the top right.
    #     - "time_skip_idle": Show the time skip button in idle state.
    #     - "time_skip_hover": Show the time skip button in hover state.
    #     - "journal_idle": Show the journal button in idle state.
    #     - "journal_hover": Show the journal button in hover state.
    # 3. show_type: str (default: "normal")
    #     - The type of button to show.
    #     - "normal": The default button.
    #     - "red": A red button.
    #     - "white": A white button.
    # 4. frames: List[Tuple[int, int, int, int]]
    #     - A list of rectangles to show on the map.
    #     - Each tuple is a rectangle with the format (xpos, ypos, width, height).
    # """
    # use school_overview_images

    add "background/school_map.webp"

    use show_building_button("school_building",  building, show_type,  563, 620)
    use show_building_button("school_dormitory", building, show_type, 1202, 410)
    use show_building_button("labs",             building, show_type,  722, 176)
    use show_building_button("sports_field",     building, show_type,  241, 130)
    use show_building_button("beach",            building, show_type,  952, 728)
    use show_building_button("staff_lodges",     building, show_type,  -19, 624)
    use show_building_button("gym",              building, show_type,  140, 289)
    use show_building_button("swimming_pool",    building, show_type,  354, 348)
    use show_building_button("cafeteria",        building, show_type,  825, 473)
    use show_building_button("bath",             building, show_type,  441, -19)
    use show_building_button("kiosk",            building, show_type,  269, 510)
    use show_building_button("courtyard",        building, show_type,  452, 490)
    use show_building_button("office_building",  building, show_type,  976,  70)

    for rect in frames:
        use show_rectangle(*rect)

    if "stats" in additions:
        grid 4 2:
            xalign 1.0 yalign 0.0
            spacing 2
            hbox:
                textbutton get_stat_icon('happiness'):
                    text_style "stat_overview"
                    action NullAction()
                null width 1
                textbutton get_school_stat_value(HAPPINESS) + "\n" + get_school_stat_change(HAPPINESS):
                    text_style "stat_value"
                    action NullAction()
            hbox:
                textbutton get_stat_icon('charm'):
                    text_style "stat_overview"
                    action NullAction()
                null width 1
                textbutton get_school_stat_value(CHARM) + "\n" + get_school_stat_change(CHARM):
                    text_style "stat_value"
                    action NullAction()
            hbox:
                textbutton get_stat_icon('education'):
                    text_style "stat_overview"
                    action NullAction()
                null width 1
                textbutton get_school_stat_value(EDUCATION) + "\n" + get_school_stat_change(EDUCATION):
                    text_style "stat_value"
                    action NullAction()
            hbox:
                textbutton get_stat_icon('money'):
                    text_style "stat_overview"
                    action NullAction()
                null width 1
                textbutton get_school_stat_value(MONEY) + "\n" + get_school_stat_change(MONEY):
                    text_style "stat_value"
                    action NullAction()

            null
            hbox:
                textbutton get_stat_icon('corruption'):
                    text_style "stat_overview"
                    action NullAction()
                null width 1
                textbutton get_school_stat_value(CORRUPTION) + "\n" + get_school_stat_change(CORRUPTION):
                    text_style "stat_value"
                    action NullAction()
            hbox:
                textbutton get_stat_icon('inhibition'):
                    text_style "stat_overview"
                    action NullAction()
                null width 1
                textbutton get_school_stat_value(INHIBITION) + "\n" + get_school_stat_change(INHIBITION):
                    text_style "stat_value"
                    action NullAction()
            hbox:
                textbutton get_stat_icon('reputation'):
                    text_style "stat_overview"
                    action NullAction()
                null width 1
                textbutton get_school_stat_value(REPUTATION) + "\n" + get_school_stat_change(REPUTATION):
                    text_style "stat_value"
                    action NullAction()

    if "time" in additions:
        vbox:
            xalign 1.0 ypos 150

            $ daytimestr = time.get_daytime_name()
            $ daystr = time.get_weekday()
            $ monthstr = time.get_month_name()
            $ daysegment = ""
            if time.check_daytime("n"):
                $ daysegment = "{color=#1b26c0}Night{/color}"
            elif time.check_weekday("d") and time.check_daytime("c"):
                $ daysegment = "{color=#ab0000}Class{/color}"
            elif time.check_weekday("d") and time.check_daytime("f"):
                $ daysegment = "{color=#0eab00}Free-Time{/color}"
            elif time.check_weekday("w"):
                $ daysegment = "{color=#ba6413}Weekend{/color}"

            text "[time.day] [monthstr] [time.year]":
                xalign 1.0
                size 30
                style "stat_overview"
            text "[daystr]":
                xalign 1.0
                size 35
                style "stat_overview"
            text "[daytimestr]":
                xalign 1.0
                size 30
                style "stat_overview"
            text "[daysegment]":
                xalign 1.0
                size 30
                style "stat_overview"

    if "time_skip_idle" in additions:
        add "icons/time skip idle.webp" xalign 0.995 yalign 0.4
    if "time_skip_hover" in additions:
        add "icons/time skip hover.webp" xalign 0.995 yalign 0.4
    
    if "journal_idle" in additions:
        add "icons/journal_icon_idle.webp" xalign 1.0 yalign 0.6
    if "journal_hover" in additions:
        add "icons/journal_icon_hover.webp" xalign 1.0 yalign 0.6

screen show_building_idle (building):
    use school_overview_images

    if building == "School Building" or building == "x":
        add "background/bg school school building idle.webp":
            xpos 1171 ypos 262
    if building == "School Dormitory" or building == "x":
        add "background/bg school school dormitory idle.webp":
            xpos 1257 ypos 613
    if building == "Labs" or building == "x":
        add "background/bg school labs idle.webp":
            xpos 644 ypos 356
    if building == "Sports Field" or building == "x":
        add "background/bg school sports field idle.webp":
            xpos 203 ypos -11
    if building == "Tennis Court" or building == "x":
        add "background/bg school tennis court idle.webp":
            xpos 558 ypos 90
    if building == "Gym" or building == "x":
        add "background/bg school gym idle.webp":
            xpos 462 ypos 5
    if building == "Pool" or building == "x":
        add "background/bg school pool idle.webp":
            xpos 297 ypos 61
    if building == "Cafeteria" or building == "x":
        add "background/bg school cafeteria idle.webp":
            xpos 229 ypos 460
    if building == "Kiosk" or building == "x":
        add "background/bg school kiosk idle.webp":
            xpos 485 ypos 661
    if building == "Courtyard" or building == "x":
        add "background/bg school courtyard idle.webp":
            xpos 604 ypos 228
    if building == "Office Building" or building == "x":
        add "background/bg school office building idle.webp":
            xpos 42 ypos 127
    if building == "Bath" or building == "x":
        add "background/bg school bath idle.webp":
            xpos 557 ypos 319

######################

#####################
# ----- LABEL ----- #
#####################

label tutorial_menu ():

    call show_image("images/events/intro/tutorial_event_1.webp") from _tutorial_menu_2
    menu:
        secretary "Do you have any questions?"

        "Show me the campus":
            call tutorial_map from tutorial_menu_1
        "That's all":
            return

    jump tutorial_menu

label tutorial_map ():
    show screen school_overview_images with dissolveM
    secretary "This is the school campus. Quite big, isn't it?"

    if (count_locked_buildings() > 0):
        secretary "Unfortunately there are some buildings that have been taken out of service and became quite derelict."
        secretary "Funny, these buildings are greyed out... just like in a game."

    show screen show_building_hovered("School Building") with dissolveM
    secretary "This is the School Building. Here the students from age 18 to 22 attend their classes and clubs."

    show screen show_building_hovered("School Dormitory") with dissolveM
    secretary "This is the School Dormitory where the High School students live."

    show screen show_building_hovered("Labs") with dissolveM
    secretary "This is the Labs Building containing classrooms specialized for biology, chemistry etc."
    if not is_building_unlocked("labs"):
        secretary "This building is currently not in use and needs some renovation."

    show screen show_building_hovered("Sports Field") with dissolveM
    if is_building_unlocked("sports_field"):
        secretary "This is the Sports Field. Here our students can work to improve their physical abilities."
        secretary "I have to say, the students get way more charming when they are fit."
    else:
        secretary "This is, or rather was our Sports Field. Currently it's just a big overgrown field. Unusable for sport activities."

    show screen show_building_hovered("Tennis Court") with dissolveM
    if is_building_unlocked("tennis_court"):
        secretary "Ah our Tennis Court! Ah good place for students to become fit and get their mind off studying."
    else:
        secretary "Our would be Tennis Court. Currently in very bad shape and definitely not usable."

    show screen show_building_hovered("Gym") with dissolveM
    secretary "This is the Gym Hall. Sport classes take place here."
    if not is_building_unlocked("sports_field"):
        secretary "Normally those classes would switch between the gym and the field outside. But you've seen the state of that."
    else:
        secretary "Those classes switch between the gym and the field outside."
    secretary "The weekly assemblies also take place in here every monday."

    show screen show_building_hovered("Pool") with dissolveM
    secretary "This is the our Swimming Pool. The best place to cool off on hot days. Especially because we don't really get winter in this part of the world."
    if not is_building_unlocked("pool"):
        secretary "But even this Facility couldn't survive the mishaps of the former Headmaster."
        secretary "I hope you can bring this back into operation rather quick. I really enjoy going for a swim."

    show screen show_building_hovered("Bath") with dissolveM
    secretary "This is the public Onsen"
    if not is_building_unlocked("bath"):
        secretary "The former headmaster closed this building down to save some money."
    else:
        secretary "It's the perfect place to relax from the stress in the school. I love it here."

    show screen show_building_hovered("Cafeteria") with dissolveM
    secretary "The Cafeteria! The Place where the students get their food."
    if not is_building_unlocked("cafeteria"):
        secretary "Because this building is closed, unfortunately the students have to get their food from the kiosk next door."
    else:
        secretary "Here they get full meals, while for snacks they have to go to the Kiosk next door."

    show screen show_building_hovered("Kiosk") with dissolveM
    secretary "While I'm at it. This is the Kiosk. Here students get snacks and drinks and other cool stuff like magazines."

    show screen show_building_hovered("Courtyard") with dissolveM
    secretary "This large area is the courtyard. Here the students can relax and spend their free time on campus."
    secretary "It's quite large, isn't it? It has to be with three schools on campus."

    show screen show_building_hovered("Office Building") with dissolveM
    secretary "And last but not least! The building we're in right now. The Office Building."
    secretary "Here is your office, from where you manage this school, your apartment, and the school council."

    hide screen show_building
    hide screen school_overview_images
    hide screen school_overview_map
    hide screen show_building_hovered

    $ hide_all()

    return

#####################