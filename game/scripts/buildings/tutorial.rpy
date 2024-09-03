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
    $ map_example = {
        "school_building": "normal", 
        "school_dormitory": "normal",
        "gym": "normal",
        "kiosk": "normal",
        "courtyard": "normal",
        "office_building": "normal",
    }

    show screen show_building_buttons(map_example) with dissolveM
    secretary "This is the school campus. Quite big, isn't it?"

    if (count_locked_buildings() > 0):
        secretary "Unfortunately there are some buildings that have been taken out of service and became quite derelict."
        secretary "Funny, these buildings are greyed out... just like in a game."

    show screen show_building_buttons("school_building", show_type = "white") with dissolveM
    secretary "This is the School Building. Here the students from age 18 to 22 attend their classes and clubs."

    show screen show_building_buttons("school_dormitory", show_type = "white") with dissolveM
    secretary "This is the School Dormitory where the High School students live."

    show screen show_building_buttons("labs", show_type = "white") with dissolveM
    secretary "This is the Labs Building containing classrooms specialized for biology, chemistry etc."
    if not is_building_unlocked("labs"):
        secretary "This building is currently not in use and needs some renovation."

    show screen show_building_buttons("sports_field", show_type = "white") with dissolveM
    if is_building_unlocked("sports_field"):
        secretary "This is the Sports Field. Here our students can work to improve their physical abilities."
        secretary "I have to say, the students get way more charming when they are fit."
    else:
        secretary "This is, or rather was our Sports Field. Currently it's just a big overgrown field. Unusable for sport activities."

    show screen show_building_buttons("beach", show_type = "white") with dissolveM
    if is_building_unlocked("beach"):
        secretary "This is the Beach. The perfect place to relax and have fun."
    else:
        secretary "This is our beach. Unfortunately the former headmaster closed it down to save some money on maintenance."

    show screen show_building_buttons("gym", show_type = "white") with dissolveM
    secretary "This is the Gym Hall. Sport classes take place here."
    if not is_building_unlocked("sports_field"):
        secretary "Normally those classes would switch between the gym and the field outside. But you've seen the state of that."
    else:
        secretary "Those classes switch between the gym and the field outside."
    secretary "The weekly assemblies also take place in here every monday."

    show screen show_building_buttons("swimming_pool", show_type = "white") with dissolveM
    secretary "This is the our Swimming Pool. The best place to cool off on hot days. Especially because we don't really get winter in this part of the world."
    if not is_building_unlocked("pool"):
        secretary "But even this Facility couldn't survive the mishaps of the former Headmaster."
        secretary "I hope you can bring this back into operation rather quick. I really enjoy going for a swim."

    show screen show_building_buttons("bath", show_type = "white") with dissolveM
    secretary "This is the public Onsen"
    if not is_building_unlocked("bath"):
        secretary "The former headmaster closed this building down to save some money."
    else:
        secretary "It's the perfect place to relax from the stress in the school. I love it here."

    show screen show_building_buttons("cafeteria", show_type = "white") with dissolveM
    secretary "The Cafeteria! The Place where the students get their food."
    if not is_building_unlocked("cafeteria"):
        secretary "Because this building is closed, unfortunately the students have to get their food from the kiosk next door."
    else:
        secretary "Here they get full meals, while for snacks they have to go to the Kiosk next door."

    show screen show_building_buttons("kiosk", show_type = "white") with dissolveM
    secretary "While I'm at it. This is the Kiosk. Here students get snacks and drinks and other cool stuff like magazines."

    show screen show_building_buttons("courtyard", show_type = "white") with dissolveM
    secretary "This large area is the courtyard. Here the students can relax and spend their free time on campus."
    secretary "It's quite large, isn't it? It has to be with three schools on campus."

    show screen show_building_buttons("staff_lodges", show_type = "white") with dissolveM
    secretary "This is the Staff Lodges. Here the teachers and other staff members live."
    if not is_building_unlocked("staff_lodges"):
        secretary "But it's currently closed. The teachers have to find their own place to stay."    

    show screen show_building_buttons("office_building", show_type = "white") with dissolveM
    secretary "And last but not least! The building we're in right now. The Office Building."
    secretary "Here is your office, from where you manage this school, your apartment, and the school council."

    $ hide_all()

    return

label map_tutorial (**kwargs):
    $ begin_event(**kwargs)

    $ red_example = {
        "school_building": "normal", 
        "school_dormitory": "normal",
        "labs": "normal",
        "sports_field": "normal",  
        "beach": "normal",
        "staff_lodges": "normal", 
        "gym": "normal",
        "swimming_pool": "normal",
        "cafeteria": "normal",
        "bath": "normal",
        "kiosk": "normal",
        "courtyard": "red",
        "office_building": "normal",
    }

    $ hide_all()

    show screen show_building_buttons ('x', 'stats', 'time', 'time_skip_idle', 'journal_idle', show_type = "normal")
    subtitles "Hello and welcome to the map tutorial."
    subtitles "You are now probably seeing the map for the first time."
    subtitles "This map is an overview over the entire school campus."
    subtitles "The map consists of basically 3 parts."
    subtitles "One part consists of all the locations you can visit on the campus. These locations are where the events and bulk of the gameplay happens."
    show screen show_building_buttons ('x', 'stats', 'time', 'time_skip_idle', 'journal_idle', show_type = "white")
    subtitles "These are all the buildings you can visit. A bit crowded I know but you'll figure it out eventually ;)"
    show screen show_building_buttons (red_example, 'stats', 'time', 'time_skip_idle', 'journal_idle', show_type = "normal")
    subtitles "If a location is marked red, it means that there is a 'special' or time/condition-locked event available."
    show screen show_building_buttons ('x', 'stats', 'time', 'time_skip_idle', 'journal_idle', show_type = "normal", frames = [(1270, 0, 650, 350)])
    subtitles "The second part is the data area. This area shows you the current stats of your school and the current time."
    subtitles "The stats show the current stats and also how the stats changed during your last interaction."
    subtitles "If a stat is marked yellow, it means that stat is currently capped and you can't increase it further until you progress the school level."
    subtitles "The stats are clickable and lead to the description for that stat in the journal."
    subtitles "The time is rather self explanatory. You have years, 12 months with 28 days each."
    subtitles "Additionally each day consists of 7 parts. Morning, Early Noon, Noon, Early Afternoon, Afternoon, Evening and Night."
    subtitles "In addition, there is also a display that shows the current timetable. Free-time, Class, Weekend and Night."
    show screen show_building_buttons ('x', 'stats', 'time', 'time_skip_idle', 'journal_idle', show_type = "normal", frames = [(1750, 370, 170, 350)])
    subtitles "The third part is the control area. Here you have two buttons."
    subtitles "One button forwards the time by one day segment."
    subtitles "And one opens the journal. Where you get all the information about your school, goals and where you also manage everything."
    subtitles "That's all for this tutorial. If you want to see me again, just look for me in the journal."

    $ start_progress('map_tutorial')

    $ end_event("map_overview", **kwargs)

label journal_tutorial (**kwargs):
    $ begin_event(**kwargs)

    $ image = convert_pattern("main", **kwargs)

    $ image.show(0)
    dev "Welcome. You just opened the Journal for the first time."
    dev "Or it's not your first time, then please bear with it for now :)."
    dev "This is the journal. Here you get all the necessary information you need to play the game."
    dev "It also is your main tool to manage your school."
    dev "So now let me show you everything."
    dev "We start with the Overview Page. This is the main page of the journal and opens by default when you open your journal."
    dev "If you are on another page you can simply click on the blue bookmark at the top left with the information symbol."
    dev "Here you can see the current state of your school, your money, your level, your stats and your proficiency."
    $ image.show(1)
    dev "On the left side at the top you can see the current stats of your school."
    dev "When clicking on a stat you'll see a detailed description of it on the right side of the journal."
    dev "The journal is pretty much always structured like that. On the left side is an overview and on the right side a detailed view of your selection."
    $ image.show(2)
    dev "Now we see that you Money Stat is selected, so you have a detailed overview over your account on the right side."
    dev "There is a short description and your income/costs are displayed."
    dev "The other stats look similar. If you need information, on what influence those stats have and how to improve them, you can find it here."
    $ image.show(3)
    dev "On the left side in the overview at the bottom are your proficiencies displayed."
    dev "These influence your teaching skills in the shown subjects and can give you a bonus on the stats when teaching a subject."
    $ image.show(4)
    dev "At the top of the journal you see three bookmarks. There you can switch between the school, teacher and parents as those three all have their own stats."
    $ image.show(5)
    dev "Now let's check out the other bookmarks."
    dev "The red bookmark at the top left leads to the goal page."
    $ image.show(6)
    dev "Here you see all the goals and tasks you need to do."
    dev "Currently there is now task system so it is a rough guideline on what to generally do in the game."
    dev "It also contains a link to the online wiki with more informations on the game. But be careful, there are spoilers on the wiki :)"
    $ image.show(7)
    dev "Now let's move to the next bookmark. This one leads to the rules page."
    $ image.show(8)
    dev "A school needs rules and policies to run smoothly."
    dev "Here you manage those. Careful, not all rules are visible from the beginning. Some only show up once you fulfilled certain conditions."
    $ image.show(9)
    dev "Now here again we have an overview on the left side."
    $ image.show(10)
    dev "And a more detailed description on the right."
    $ image.show(9)
    dev "But first on the left, we have two lists. One for the rules you need to unlock and one for the rules you already unlocked."
    dev "For a better overview you can hide or expand both lists by clicking on 'hide/show locked/unlocked rule'."
    $ image.show(10)
    dev "Now in the detailed view we have 4 main components."
    $ image.show(11)
    dev "The description. Here you get a short summary of the rule included with the conditions to unlock it."
    dev "Potential costs or benefits are also displayed here."
    $ image.show(12)
    dev "The condition list. This list is a shortened variant of the conditions displayed in the description."
    dev "Here you will only see Conditions based on your stats. Thats for a better overview since those are the most difficult to fulfill and thus will be checked more often."
    $ image.show(13)
    dev "Third, there is an image showing a preview, example or a visual representation of the rule."
    dev "You can also click on the image to get a fullscreen variant of it."
    $ image.show(14)
    dev "And the last component it the 'Vote to unlock'-Button. This one queues the rule in the PTA agenda."
    dev "You can only queue up one rule, building or club at a time. When you decide to instead select another rule for example, you can just queue it and it will replace the old one."
    dev "You'll also see what Agenda is planned in the Overview-Page."
    dev "The PTA will vote every friday morning on the agenda you queued up."
    dev "It also shows a probability on how likely it is that the PTA will vote for it, since you don't need to fully fulfill the conditions, but the more you fulfill the higher the probability."
    dev "Now let's move on."
    $ image.show(15)
    dev "Below the Rule-Bookmark, there is the Club-Bookmark."
    dev "Here it's pretty much the same. Only now you have an overview over all clubs in the school. The clubs provide after-school activities for the students."
    $ image.show(16)
    dev "Next is the Buildings-Page. Here we have a full overview over all the buildings and locations of the school."
    dev "Those can be renovated to make them accessible again or upgraded to increase possible benefits."
    $ image.show(17)
    dev "Now let's move to the bookmarks on the right side. At the top we have the credits page."
    dev "There, all my beloved patreons are listed and credited for their contribution to this project."
    $ image.show(18)
    dev "Below it we have the Replay-Bookmark."
    $ image.show(19)
    dev "Here is the full replay gallery of all the events you ever saw in the game. Either in this savegame or in others."
    dev "Again, on the left you have the overview. First you select a location and then the event."
    dev "On the right you'll again see a detailed view of the event."
    dev "Now this probably also needs a bit more of explanation. The replay gallery is a bit special."
    dev "The problem is, most events are highly variable and differ between two types. The normal one and the composite one."
    dev "Additionally, almost all events change themselves depending on multiple variables like level of the school, stats or just random values that are rolled when playing the event."
    dev "So the replay gallery tracks all of those values and also your decisions made in the event, to allow you to only replay the events with the variables you already saw."
    $ image.show(20)
    dev "The first example is a normal event. Those are rather straight forward. You select what values you want."
    $ image.show(21)
    dev "Press 'Start Replay'"
    $ image.show(20)
    dev "Careful, the values can change depending on the values you selected, so it is recommendable to work your way from left to right because the values are always influenced by their left neighbour."
    $ image.show(22)
    dev "Now the composite events get a bit more complex."
    dev "Composite Events are events that are randomly put together from multiple smaller events."
    dev "The Composite Event therefore defines a step-by-step order and each step has a set of small event fragments from which one is chosen to be used."
    dev "Those events allow longer events that can also be repeated without being always identical."
    $ image.show(23)
    dev "Now to configure the replay of a Composite Event you get an extra tab called 'Fragments'. Here it's right next to 'Values'."
    $ image.show(24)
    dev "When clicking on it, you'll get to the order of what fragments will be played."
    $ image.show(26)
    dev "By clicking on one fragments, the overview on the left page will be extended to show all the fragments that can be used for that step in the Composite Event."
    dev "If the Composite Event has values to select, then those can influence the fragments that are available."
    dev "Now we see 'Silent Work and Help' is selected. That one is rather boring so let's change it to 'Math Exercises'."
    $ image.show(27)
    dev "Much better. Ah see, the fragments can also have a value selection."
    $ image.show(28)
    dev "Now that we finished the configuration, we can start the replay. For that we first need to head back to the main event."
    dev "For that we either click on 'Return to Main Event' at the bottom right or on the Event name at the top left."
    $ image.show(29)
    dev "Now press 'Start Replay' and enjoy your math lessons."
    dev "After you finished the replay, which can be ended at all times either in the quickbar at the bottom of the screen or in the game menu when pressing escape, you'll return back on this page in the journal."
    $ image.show(30)
    dev "And after you're finished with everything in the journal, you can either press 'Escape' or click on the bottom right bookmark to close the journal."
    dev "That was all about the journal. Sorry if that was a bit long. There are just soooo many informations in the journal."
    dev "So if you need to see this tutorial again, just replay me in the gallery. :)"
    dev "See you later!"

    $ start_progress('journal_tutorial')

    $ end_event('none', **kwargs)

    call start_journal.after_check() from _call_start_journal_after_check

label action_tutorial (**kwargs):
    $ begin_event(**kwargs)

    $ log_val('kwargs', kwargs)

    $ return_label = get_kwargs('return_label', 'map_overview', **kwargs)

    $ image = convert_pattern("main", **kwargs)

    $ image.show(0)
    dev "Hello and welcome to yet another tutorial."
    dev "This time we talk about the activity selection."
    dev "Each time you enter a location, you'll get an overview over the available activities."
    dev "Those activities are the events you can play in the location at the current time under the current circumstances."
    dev "Meaning that some events are only available at certain times or when certain conditions are met."
    dev "After you select an activity, you'll play through a random event that is based on the selected activity."
    dev "When you're playing on Desktop and didn't deactivate the setting, you can also navigate through this menu via the keyboard."
    dev "The corresponding keys are displayed inside the brackets next to the activity name."

    dev "Sometimes activities are marked red. This means that there is some kind of a special event available."
    dev "Those events are usually time-locked or condition-locked and are often only available for a limited time."

    $ image.show(1)
    dev "Maybe you noticed the eye symbol in the top left corner of the screen."
    dev "This is a special extra for you peeps. Currently it's always usable but will be locked behind an item in the future."
    dev "This button is visible in all activity selection menus and in some events."

    dev "That's all from me again."
    dev "If you need my help again, you can replay this tutorial in the replay gallery."
    dev "Bye."

    $ start_progress('action_tutorial')

    $ end_event('none', **kwargs)

    call expression return_label from _call_expression

label sandbox_tutorial (**kwargs):
    $ begin_event(**kwargs)

    $ log_val('kwargs', kwargs)

    $ return_label = get_kwargs('return_label', 'map_overview', **kwargs)

    $ image = convert_pattern("main", **kwargs)

    $ image.show(0)
    dev "Hey hey. It's me again."
    dev "This time I want to introduce to you the Movie Sandbox."
    dev "The Movie Sandbox allows you to watch this event however you want."
    dev "You decide the location, the position, the clothing and the camera angle."
    dev "The usage is quite simple. All the buttons you need are those 5 at the right side of the screen."
    dev "Maybe also the Hide-Button in the quick menu at the bottom :D"
    dev "So let's start with the buttons."

    $ image.show(1)
    dev "The first button allows you to change the clothing of the character."
    dev "Some clothing is locked behind certain conditions and some are only available in certain locations."
    dev "But as long as the button is visible, you can change the clothing."

    $ image.show(2)
    dev "The second button allows you to change the position of the character."

    $ image.show(3)
    dev "The third button allows you to change the location."

    $ image.show(4)
    dev "And the fourth one switches between all available camera angles."

    dev "If any of these buttons are not visible, it means that there is no option to change to in the current configuration."

    $ image.show(5)
    dev "The last button in the bottom right corner ends the sandbox mode and returns you to the map."

    dev "That's pretty much everything. If you have any questions, just replay this tutorial in the replay gallery."
    dev "Then lot's of fun with the sandbox ;) Bye."

    $ start_progress('sandbox_tutorial')

    $ end_event('none', **kwargs)

    call expression return_label from _call_expression_1
#####################