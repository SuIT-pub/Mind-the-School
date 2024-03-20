######################
# ----- SCREENS -----#
######################

screen show_building_hovered (building):
    use school_overview_images

    if building == "School Building" or building == "x":
        add "background/bg school school building hover.webp":
            xpos 1171 ypos 262
    if building == "School Dormitory" or building == "x":
        add "background/bg school school dormitory hover.webp":
            xpos 1257 ypos 613
    if building == "Labs" or building == "x":
        add "background/bg school labs hover.webp":
            xpos 644 ypos 356
    if building == "Sports Field" or building == "x":
        add "background/bg school sports field hover.webp":
            xpos 203 ypos -11
    if building == "Tennis Court" or building == "x":
        add "background/bg school tennis court hover.webp":
            xpos 558 ypos 90
    if building == "Gym" or building == "x":
        add "background/bg school gym hover.webp":
            xpos 462 ypos 5
    if building == "Pool" or building == "x":
        add "background/bg school pool hover.webp":
            xpos 297 ypos 61
    if building == "Cafeteria" or building == "x":
        add "background/bg school cafeteria hover.webp":
            xpos 229 ypos 460
    if building == "Kiosk" or building == "x":
        add "background/bg school kiosk hover.webp":
            xpos 485 ypos 661
    if building == "Courtyard" or building == "x":
        add "background/bg school courtyard hover.webp":
            xpos 604 ypos 228
    if building == "Office Building" or building == "x":
        add "background/bg school office building hover.webp":
            xpos 42 ypos 127
    if building == "Bath" or building == "x":
        add "background/bg school bath hover.webp":
            xpos 557 ypos 319

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