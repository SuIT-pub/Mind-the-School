screen show_building (building):
    use school_overview_images

    if building == "High School Building":
        add "background/bg school high school building hover.png":
            xpos 1171 ypos 262
    if building == "High School Dormitory":
        add "background/bg school high school dormitory hover.png":
            xpos 1257 ypos 613
    if building == "Middle School Building":
        add "background/bg school middle school building hover.png":
            xpos 725 ypos 103
    if building == "Middle School Dormitory":
        add "background/bg school middle school dormitory hover.png":
            xpos 666 ypos 476
    if building == "Elementary School Building":
        add "background/bg school elementary school building hover.png":
            xpos 826 ypos 178
    if building == "Elementary School Dormitory":
        add "background/bg school elementary school dormitory hover.png":
            xpos 446 ypos 196
    if building == "Labs":
        add "background/bg school labs hover.png":
            xpos 644 ypos 356
    if building == "Sports Field":
        add "background/bg school sports field hover.png":
            xpos 203 ypos -11
    if building == "Tennis Court":
        add "background/bg school tennis court hover.png":
            xpos 558 ypos 90
    if building == "Gym":
        add "background/bg school gym hover.png":
            xpos 462 ypos 5
    if building == "Pool":
        add "background/bg school pool hover.png":
            xpos 297 ypos 61
    if building == "Cafeteria":
        add "background/bg school cafeteria hover.png":
            xpos 229 ypos 460
    if building == "Kiosk":
        add "background/bg school kiosk hover.png":
            xpos 485 ypos 661
    if building == "Courtyard":
        add "background/bg school courtyard hover.png":
            xpos 604 ypos 228
    if building == "Office Building":
        add "background/bg school office building hover.png":
            xpos 42 ypos 127

label tutorial_menu:

    scene office secretary 4 big smile

    menu:
        char_Secretary "Do you have any questions?"

        "Show me the campus":
            call tutorial_map
        "That's all":
            return

    jump tutorial_menu

label tutorial_map:
    show screen school_overview_images
    char_Secretary "This is the school campus. Quite big, isn't it?"

    if (False in unlocked_buildings.values()):
        char_Secretary "Unfortunately there are some buildings that have been taken out of service and became quite derelict."
        char_Secretary "Funny, these buildings are greyed out... just like in a game."

    show screen show_building("High School Building")
    char_Secretary "This is the High School Building. Here the students from age 18 to 22 attend their classes and clubs."

    show screen show_building("High School Dormitory")
    char_Secretary "This is the High School Dormitory where the High School students live."

    if loli_content >= 1:
        show screen show_building("Middle School Building")
        char_Secretary "This is the Middle School Building. Here the students from age 13 to 17 attend their classes and clubs."

        show screen show_building("Middle School Dormitory")
        char_Secretary "This is the Middle School Dormitory where the Middle School students live."

    if loli_content == 2:
        show screen show_building("Elementary School Building")
        char_Secretary "This is the Elementary School Building. Here the students from age 8 to 12 attend their classes and clubs."

        show screen show_building("Elementary School Dormitory")
        char_Secretary "This is the Elementary School Dormitory where the Elementary School students live."

    show screen show_building("Labs")
    char_Secretary "This is the Labs Building containing classrooms specialized for biology, chemistry etc."
    if not unlocked_buildings["labs"]:
        char_Secretary "This building is currently not in use and needs some renovation."

    show screen show_building("Sports Field")
    if unlocked_buildings["sports_field"]:
        char_Secretary "This is the Sports Field. Here our students can work to improve their physical abilities."
        char_Secretary "I have to say, the students get way more charming when they are fit."
    else:
        char_Secretary "This is, or rather was our Sports Field. Currently it's just a big overgrown field. Unusable for sport activities."

    show screen show_building("Tennis Court")
    if unlocked_buildings["tennis_court"]:
        char_Secretary "Ah our Tennis Court! Ah good place for students to become fit and get their mind off studying."
    else:
        char_Secretary "Our would be Tennis Court. Currently in very bad shape und definetly not usable."

    show screen show_building("Gym")
    char_Secretary "This is the Gym Hall. Sport classes take place here."
    if not unlocked_buildings["sports_field"]:
        char_Secretary "Normally those classes would switch between the gym and the field outside. But you've seen the state of that."
    else:
        char_Secretary "Those classes switch between the gym and the field outside."
    char_Secretary "The weekly assemblies also take place in here every monday."

    show screen show_building("Pool")
    char_Secretary "This is the our Swimming Pool. The best place to cool off on hot days. Especially because we don't relly get winter in this part of the world."
    if not unlocked_buildings["pool"]:
        char_Secretary "But even this Facility couldn't survive the mishaps of the former Principal."
        char_Secretary "I hope you can bring this back into operation rather quick. I really enjoy going for a swim."

    show screen show_building("Cafeteria")
    char_Secretary "The Cafeteria! The Place where the students get their food."
    if not unlocked_buildings["cafeteria"]:
        char_Secretary "Because this building is closed, unfortunately the students have to get their food from the kiosk next door."
    else:
        char_Secretary "Here they get full meals, while for snacks they have to go to the Kiosk next door."

    show screen show_building("Kiosk")
    char_Secretary "While I'm at it. This is the Kiosk. Here students get snacks and drink and other cool stuff like magazines."

    show screen show_building("Courtyard")
    char_Secretary "This large area is the courtyard. Here the students can relax and spend their free time on campus."
    char_Secretary "It's quite large, isn't it? It has to be with three schools on campus."

    show screen show_building("Office Building")
    char_Secretary "And last but not least! The building we're in right now. The Office Building."
    char_Secretary "Here is your office, from where you manage this school, your apartment, and the school council."

    hide screen show_building
    hide screen school_overview_images
    hide screen school_overview_map

    return