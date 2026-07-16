#############################
# region Lab Intro 1 Events #

init 2 python: 
    set_current_mod('base')
    office_building_work_event["lab"].add_event(
        Event(2, "lab_intro_1",
            TimeCondition(weekday = "d", daytime = "d"),
            LevelCondition("2"),
            ReplayCategoryOption("lab_intro"),
            Pattern("main", "images/events/lab_intro/lab_intro_1/lab_intro_1 <step>.webp"),
            NOT(ProgressCondition("lab_intro")),
            thumbnail = "images/events/lab_intro/lab_intro_1/lab_intro_1 0.webp"))

label lab_intro_1 (**kwargs):
    $ begin_event(**kwargs)

    $ image = convert_pattern("main", **kwargs)
    
    $ image.show(0)
    subtitles "The office smells like stale coffee and old paper. The overhead light buzzes faintly."
    headmaster_thought "Hmm, the progress I made is good, but it is just the beginning."
    headmaster_thought "It's probably getting harder from now on. I set a good basis, but there is still resistance in their minds..."

    $ image.show(1)
    headmaster_thought "Maybe it's time to start work on the potions."
    headmaster_thought "It's unfortunate that I can't reach my partner, he would be of immense help..."

    $ image.show(2)
    headmaster_thought "At least I have this one last potion. I have to be careful to not waste it."

    $ image.show(3)
    headmaster_thought "I also have a few notes about the potion, its effects and ingredients, but nothing very detailed unfortunately."
    headmaster_thought "I guess the first thing I should do is to set up a makeshift lab. I should check out the old lab building."

    $ image.show(4)
    headmaster_thought "Maybe there is some stuff I could still use."

    $ start_progress("lab_intro")

    $ end_event("new_daytime", **kwargs)

# endregion
#############################

#############################
# region Lab Intro 2 Events #
init 2 python: 
    set_current_mod('base')
    labs_events["look_around"].add_event(
        Event(2, "lab_intro_2",
            TimeCondition(weekday = "d", daytime = "d"),
            LevelCondition("2"),
            ProgressCondition("lab_intro", 1),
            ReplayCategoryOption("lab_intro"),
            Pattern("main", "images/events/lab/lab_intro_2/lab_intro_2 <step>.webp"),
            thumbnail = "images/events/lab/lab_intro_2/lab_intro_2 0.webp"))
    
    lab_intro_2_search_gym_storage = FragmentStorage("lab_intro_2_search_gym")
    lab_intro_2_search_gym_storage.add_event(
        EventFragment(3, "lab_intro_2_search_gym_1",
            NOT(ItemCondition("lab_mortar_and_pestle")),
            ReplayCategoryOption("lab_intro"),
            Pattern("main", "images/events/lab/lab_intro_2/lab_intro_2_gym_1.webp"),
            thumbnail = "images/events/lab/lab_intro_2/lab_intro_2_gym_1.webp"),
        EventFragment(3, "lab_intro_2_search_gym_2",
            ItemCondition("lab_distilled_water"),
            ReplayCategoryOption("lab_intro"),
            Pattern("main", "images/events/lab/lab_intro_2/lab_intro_2_gym_2.webp"),
            thumbnail = "images/events/lab/lab_intro_2/lab_intro_2_gym_2.webp"))
    gym_events["search"].add_event(
        EventComposite(3, "lab_intro_2_search_gym", [lab_intro_2_search_gym_storage],
            TimeCondition(weekday = "d", daytime = "d"),
            ProgressCondition("lab_intro", 2),
            ReplayCategoryOption("lab_intro"),
            Pattern("base", "images/events/lab/lab_intro_2/lab_intro_2_gym.webp"),
            thumbnail = "images/events/lab/lab_intro_2/lab_intro_2_gym.webp"))


    lab_intro_2_search_cafeteria_storage = FragmentStorage("lab_intro_2_search_cafeteria")
    lab_intro_2_search_cafeteria_storage.add_event(
        Event(3, "lab_intro_2_search_cafeteria_1",
            NOT(ItemCondition("lab_mortar_and_pestle")),
            ReplayCategoryOption("lab_intro"),
            Pattern("main", "images/events/lab/lab_intro_2/lab_intro_2_cafeteria_1.webp"),
            thumbnail = "images/events/lab/lab_intro_2/lab_intro_2_cafeteria_1.webp"),
        Event(3, "lab_intro_2_search_cafeteria_2",
            NOT(ItemCondition("lab_distilled_water")),
            ReplayCategoryOption("lab_intro"),
            Pattern("main", "images/events/lab/lab_intro_2/lab_intro_2_cafeteria_2.webp"),
            thumbnail = "images/events/lab/lab_intro_2/lab_intro_2_cafeteria_2.webp"),
        Event(3, "lab_intro_2_search_cafeteria_3",
            ItemCondition("lab_mortar_and_pestle"),
            ItemCondition("lab_distilled_water"),
            ReplayCategoryOption("lab_intro"),
            Pattern("main", "images/events/lab/lab_intro_2/lab_intro_2_cafeteria_3.webp"),
            thumbnail = "images/events/lab/lab_intro_2/lab_intro_2_cafeteria_3.webp"))
    cafeteria_events["search"].add_event(
        EventComposite(3, "lab_intro_2_search_cafeteria", [lab_intro_2_search_cafeteria_storage],
            TimeCondition(weekday = "d", daytime = "d"),
            ProgressCondition("lab_intro", 2),
            ReplayCategoryOption("lab_intro"),
            Pattern("base", "images/events/lab/lab_intro_2/lab_intro_2_cafeteria.webp"),
            thumbnail = "images/events/lab/lab_intro_2/lab_intro_2_cafeteria.webp"))

    lab_intro_2_search_dorm_storage = FragmentStorage("lab_intro_2_search_dorm")
    lab_intro_2_search_dorm_storage.add_event(
        Event(3, "lab_intro_2_search_dorm_1",
            NOT(ItemCondition("lab_mortar_and_pestle")),
            ReplayCategoryOption("lab_intro"),
            Pattern("main", "images/events/lab/lab_intro_2/lab_intro_2_dorm_1.webp"),
            thumbnail = "images/events/lab/lab_intro_2/lab_intro_2_dorm_1.webp"),
        Event(3, "lab_intro_2_search_dorm_2",
            NOT(ItemCondition("lab_distilled_water")),
            ReplayCategoryOption("lab_intro"),
            Pattern("main", "images/events/lab/lab_intro_2/lab_intro_2_dorm_2.webp"),
            thumbnail = "images/events/lab/lab_intro_2/lab_intro_2_dorm_2.webp"),
        Event(3, "lab_intro_2_search_dorm_3",
            ItemCondition("lab_mortar_and_pestle"),
            ItemCondition("lab_distilled_water"),
            ReplayCategoryOption("lab_intro"),
            Pattern("main", "images/events/lab/lab_intro_2/lab_intro_2_dorm_3.webp"),
            thumbnail = "images/events/lab/lab_intro_2/lab_intro_2_dorm_3.webp"))
    sd_events["search"].add_event(
        EventComposite(3, "lab_intro_2_search_dorm", [lab_intro_2_search_dorm_storage],
            TimeCondition(weekday = "d", daytime = "d"),
            ProgressCondition("lab_intro", 2),
            ReplayCategoryOption("lab_intro"),
            Pattern("base", "images/events/lab/lab_intro_2/lab_intro_2_dorm.webp"),
            thumbnail = "images/events/lab/lab_intro_2/lab_intro_2_dorm.webp"))

    lab_intro_2_search_kiosk_storage = FragmentStorage("lab_intro_2_search_kiosk")
    lab_intro_2_search_kiosk_storage.add_event(
        Event(3, "lab_intro_2_search_kiosk_1",
            NOT(ItemCondition("lab_glassware")),
            ReplayCategoryOption("lab_intro"),
            Pattern("main", "images/events/lab/lab_intro_2_search_kiosk/lab_intro_2_kiosk_1 <step>.webp"),
            thumbnail = "images/events/lab/lab_intro_2_search_kiosk/lab_intro_2_kiosk_1 4.webp"),
        Event(3, "lab_intro_2_search_kiosk_2",
            ItemCondition("lab_glassware"),
            ReplayCategoryOption("lab_intro"),
            Pattern("main", "images/events/lab/lab_intro_2_search_kiosk/lab_intro_2_kiosk_2.webp"),
            thumbnail = "images/events/lab/lab_intro_2_search_kiosk/lab_intro_2_kiosk_2.webp"))
    kiosk_events["search"].add_event(
        EventComposite(3, "lab_intro_2_search_kiosk", [lab_intro_2_search_kiosk_storage],
            TimeCondition(weekday = "d", daytime = "d"),
            ProgressCondition("lab_intro", 2),
            ReplayCategoryOption("lab_intro"),
            Pattern("base", "images/events/lab/lab_intro_2_search_kiosk/lab_intro_2_kiosk.webp"),
            thumbnail = "images/events/lab/lab_intro_2_search_kiosk/lab_intro_2_kiosk.webp"))

    courtyard_events["patrol"].add_event(
        Event(3, "lab_intro_2_patrol_courtyard",
            TimeCondition(weekday = "d", daytime = "d"),
            Pattern("main", "images/events/lab/lab_intro_2_patrol_courtyard/lab_intro_2_patrol_courtyard <school_level> <step>.webp"),
            ProgressCondition("lab_intro", 2),
            NOT(ItemCondition("lab_gas_burner")),
            ReplayCategoryOption("lab_intro"),
            thumbnail = "images/events/lab/lab_intro_2_patrol_courtyard/lab_intro_2_patrol_courtyard 1 0.webp"))
    courtyard_events["search"].add_event(
        Event(3, "lab_intro_2_search_courtyard",
            TimeCondition(weekday = "d", daytime = "d"),
            Pattern("main", "images/events/lab/lab_intro_2_search_courtyard/lab_intro_2_search_courtyard <school_level> <step>.webp"),
            ProgressCondition("lab_intro", 2),
            ReplayCategoryOption("lab_intro"),
            thumbnail = "images/events/lab/lab_intro_2_search_courtyard/lab_intro_2_search_courtyard 1 0.webp"))

    lab_intro_2_search_school_storage = FragmentStorage("lab_intro_2_search_school")
    lab_intro_2_search_school_storage.add_event(
        Event(3, "lab_intro_2_search_school_1",
            NOT(ItemCondition("lab_office_supplies")),
            ReplayCategoryOption("lab_intro"),
            Pattern("main", "images/events/lab_intro/lab_intro_2_school_2.webp"),
            thumbnail = "images/events/lab_intro/lab_intro_2_school_2.webp"),
        Event(3, "lab_intro_2_search_school_2",
            ItemCondition("lab_office_supplies"),
            ReplayCategoryOption("lab_intro"),
            Pattern("main", "images/events/lab_intro/lab_intro_2_school_1.webp"),
            thumbnail = "images/events/lab_intro/lab_intro_2_school_1.webp"))
    sb_events["search"].add_event(
        EventComposite(3, "lab_intro_2_search_school", [lab_intro_2_search_school_storage],
            TimeCondition(weekday = "d", daytime = "d"),
            ProgressCondition("lab_intro", 2),
            ReplayCategoryOption("lab_intro"),
            Pattern("main", "images/events/lab_intro/lab_intro_2_school.webp"),
            thumbnail = "images/events/lab_intro/lab_intro_2_school.webp"))

    lab_intro_2_search_office_storage = FragmentStorage("lab_intro_2_search_office")
    lab_intro_2_search_office_storage.add_event(
        Event(3, "lab_intro_2_search_office_1",
            NOT(ItemCondition("lab_office_supplies")),
            ReplayCategoryOption("lab_intro"),
            Pattern("main", "images/events/lab_intro_2/lab_intro_2_office_1.webp"),
            thumbnail = "images/events/lab_intro_2/lab_intro_2_office_1.webp"),
        Event(3, "lab_intro_2_search_office_2",
            ItemCondition("lab_office_supplies"),
            ReplayCategoryOption("lab_intro"),
            Pattern("main", "images/events/lab_intro_2/lab_intro_2_office_2.webp"),
            thumbnail = "images/events/lab_intro_2/lab_intro_2_office_2.webp"))
    office_building_events["search"].add_event(
        EventComposite(3, "lab_intro_2_search_office", [lab_intro_2_search_office_storage],
            TimeCondition(weekday = "d", daytime = "d"),
            ProgressCondition("lab_intro", 2),
            ReplayCategoryOption("lab_intro"),
            Pattern("main", "images/events/lab_intro_2/lab_intro_2_office.webp"),
            thumbnail = "images/events/lab_intro_2/lab_intro_2_office.webp"))

label lab_intro_2 (**kwargs):
    $ begin_event(**kwargs)

    # headmaster looks for some lab equipment in different storage rooms
    # headmaster finds a few tables, chairs, and some other equipment

    $ image = convert_pattern("main", **kwargs)
    
    $ image.show(0)
    subtitles "The smell hits first — mold and old solvent, something chemical that hasn't fully dissipated in thirty years."
    headmaster_thought "Hmm, everything is pretty run down."

    call Image_Series.show_image(image, 1, 2) from _call_lab_intro_show_image_1
    headmaster_thought "I don't think I can use any of this."

    # headmaster checks a few rooms

    $ image.show(3)
    headmaster_thought "Hey, what's that?"

    $ image.show(4)
    headmaster_thought "That table seems totally fine! That's perfect!"

    # headmaster calls secretary

    $ image.show(5)
    headmaster_thought "Time to get some help."

    $ image.show(6)
    headmaster "Hi Emiko. Yes, I am. I am in the old laboratory building. What I'm doing? I'm looking for some stuff for my potion lab."

    $ image.show(7)
    headmaster "Yes, I want to start. Yes, maybe you can have a few. Yes. Yes. No. Yes. Emiko... Yes. Yeah. I know."
    headmaster "Yes, Emiko... No. Emiko! Yes. Can you please come over? Yes I have a lab table and I need you to help me bring it over to the small storage room in the office."
    $ image.show(8)
    headmaster "Yes. No. No, now. Yes. On the second level. Yes. Yes you'll find me. Yes. Okay I'm gonna hang up now."
    headmaster "Yes. Yes. No. Yes. I'm gonna... Yes. Emiko. I'm... I'm gonna hang up now. See you... Yes. Yes. Bye!"
    $ image.show(9)
    headmaster "*phew*"

    $ inventory_manager.add_item("lab_furniture")

    $ set_progress("lab_intro", 2)
    $ end_event("new_daytime", **kwargs)

label lab_intro_2_search_gym (**kwargs):
    $ begin_event(**kwargs)

    $ show_pattern("base", **kwargs)
    headmaster_thought "Hmm, the gym should have anything useful."

    call composite_event_runner(**kwargs) from lab_intro_2_search_gym_composite_event_runner

label lab_intro_2_search_gym_1 (**kwargs):
    $ begin_event(**kwargs)

    # headmaster searches the gym for some equipment
    # headmaster finds a bra, but nothing useful for his lab

    $ show_pattern("main", **kwargs)
    headmaster_thought "Whose bra is this? And why is it in the equipment room?! Mhh, who cares."

    $ inventory_manager.add_item("generic_bra")

    $ end_event("new_daytime", **kwargs)

label lab_intro_2_search_gym_2 (**kwargs):
    $ begin_event(**kwargs)

    $ show_pattern("main", **kwargs)
    headmaster_thought "Nothing useful here."

    $ end_event("new_daytime", **kwargs)


label lab_intro_2_search_cafeteria (**kwargs):
    $ begin_event(**kwargs)

    $ show_pattern("base", **kwargs)
    headmaster_thought "Hmm, the cafeteria should have anything useful."

    call composite_event_runner(**kwargs) from lab_intro_2_search_cafeteria_composite_event_runner

label lab_intro_2_search_cafeteria_1 (**kwargs):
    $ begin_event(**kwargs)

    # headmaster searches the cafeteria for some equipment
    # headmaster finds a mortar and pestle

    $ show_pattern("main", **kwargs)
    headmaster_thought "Oh, look at that! That's a mortar and pestle! Perfect!"

    $ inventory_manager.add_item(Item("lab_mortar_and_pestle"))

    $ end_event("new_daytime", **kwargs)

label lab_intro_2_search_cafeteria_2 (**kwargs):
    $ begin_event(**kwargs)

    # headmaster searches the cafeteria for some equipment
    # headmaster finds some distilled water and some other liquids

    $ show_pattern("main", **kwargs)
    headmaster_thought "Ah, that's a nice looking bottle of distilled water. Perfect!"

    $ inventory_manager.add_item(Item("lab_distilled_water"))

    $ end_event("new_daytime", **kwargs)

label lab_intro_2_search_cafeteria_3 (**kwargs):
    $ begin_event(**kwargs)

    $ show_pattern("main", **kwargs)
    # headmaster searches the cafeteria for some equipment
    # headmaster doesn't find anything useful anymore

    headmaster_thought "Nothing useful here."

    $ end_event("new_daytime", **kwargs)


label lab_intro_2_search_dorm (**kwargs):
    $ begin_event(**kwargs)

    $ show_pattern("base", **kwargs)
    headmaster_thought "Let's see if the dorm has anything useful."

    call composite_event_runner(**kwargs) from lab_intro_2_search_dorm_composite_event_runner

label lab_intro_2_search_dorm_1 (**kwargs):
    $ begin_event(**kwargs)

    # headmaster searches the dorm for some equipment
    # headmaster finds a mortar and pestle

    $ show_pattern("main", **kwargs)
    headmaster_thought "Oh, look at that! That's a mortar and pestle! Perfect!"

    $ inventory_manager.add_item(Item("lab_mortar_and_pestle"))

    $ end_event("new_daytime", **kwargs)

label lab_intro_2_search_dorm_2 (**kwargs):
    $ begin_event(**kwargs)

    # headmaster searches the dorm for some equipment
    # headmaster finds some distilled water and some other liquids

    $ show_pattern("main", **kwargs)
    headmaster_thought "Ah, that's a nice looking bottle of distilled water. Perfect!"

    $ inventory_manager.add_item(Item("lab_distilled_water"))

    $ end_event("new_daytime", **kwargs)

label lab_intro_2_search_dorm_3 (**kwargs):
    $ begin_event(**kwargs)

    # headmaster searches the dorm for some equipment
    # headmaster doesn't find anything useful anymore

    $ show_pattern("main", **kwargs)
    headmaster_thought "Nothing useful here."

    $ end_event("new_daytime", **kwargs)


label lab_intro_2_search_kiosk (**kwargs):
    $ begin_event(**kwargs)

    $ show_pattern("base", **kwargs)
    headmaster_thought "Let's see if the kiosk has anything useful."

    call composite_event_runner(**kwargs) from lab_intro_2_search_kiosk_composite_event_runner

label lab_intro_2_search_kiosk_1 (**kwargs):
    $ begin_event(**kwargs)

    # headmaster looks for some equipment at the kiosk
    # headmaster finds some glassware and some utensils

    $ image = convert_pattern("main", **kwargs)

    $ image.show(0)
    headmaster_thought "Ahh, I could use this set of glassware."

    $ image.show(1)
    headmaster "Hello, I would like to buy this set."
    $ image.show(2)
    vendor "Sure, that's 100$"
    $ image.show(3)
    headmaster "Alright, here you go."
    $ image.show(4)
    vendor "Thank you very much!"

    $ inventory_manager.add_item(Item("lab_glassware"))

    $ end_event("new_daytime", **kwargs)

label lab_intro_2_search_kiosk_2 (**kwargs):
    $ begin_event(**kwargs)

    # headmaster looks for some equipment at the kiosk
    # headmaster doesn't find anything else useful at the kiosk

    $ show_pattern("main", **kwargs)
    headmaster_thought "Nothing useful here."

    $ end_event("new_daytime", **kwargs)


label lab_intro_2_patrol_courtyard (**kwargs):
    $ begin_event(**kwargs)

    $ hatano = Person["hatano_miwa"].get_renpy_char()
    $ kokoro = Person["kokoro_nakamura"].get_renpy_char()
    $ gloria = Person["gloria_goto"].get_renpy_char()

    # headmaster find students sitting in the courtyard playing with a gas burner acting like they are camping
    # headmaster reprimands them and confiscates the burner

    $ image = convert_pattern("main", **kwargs)

    call Image_Series.show_image(image, 0, 1, 2) from _call_show_image_lab_intro_2_patrol_courtyard_1
    headmaster "Hey, what are you doing? That's dangerous!"
    $ image.show(3)
    hatano "We're just camping!"
    $ image.show(4)
    headmaster "Camping? But you're just on the school grounds!"
    $ image.show(5)
    gloria "We're playing camping. We can't go camping anywhere else."
    $ image.show(6)
    headmaster "Okay, but I can't allow you to use a gas burner here without any supervision."
    $ image.show(7)
    gloria "But we want to make smores!"
    $ image.show(6)
    headmaster "I'm sorry, but I have to confiscate this gas burner."
    $ image.show(8)
    hatano "But Mr. [headmaster_last_name]!"
    $ image.show(9)
    headmaster "It's just not safe. If you want to go camping, then you should inquire about it with your teachers first."
    $ image.show(10)
    headmaster "Maybe they accept to go with you on a field trip."
    $ image.show(11)
    kokoro "Okay, we're sorry. We'll go back to class now."

    $ inventory_manager.add_item(Item("lab_gas_burner"))

    $ end_event("new_daytime", **kwargs)

label lab_intro_2_search_courtyard (**kwargs):
    $ begin_event(**kwargs)

    # headmaster looks for some equipment in the courtyard
    # of course there won't be anything useful in the courtyard

    $ image = convert_pattern("main", **kwargs)

    call Image_Series.show_image(image, 0, 1, 2) from _call_show_image_lab_intro_2_search_courtyard_1
    headmaster_thought "Nothing useful here."

    $ end_event("new_daytime", **kwargs)


label lab_intro_2_search_school (**kwargs):
    $ begin_event(**kwargs)

    $ show_pattern("base", **kwargs)
    headmaster_thought "Let's check the classrooms."

    call composite_event_runner(**kwargs) from lab_intro_2_search_school_composite_event_runner

label lab_intro_2_search_school_1 (**kwargs):
    $ begin_event(**kwargs)

    # headmaster looks for some equipment in the school
    # headmaster finds some labels and some small office supplies

    $ image = convert_pattern("main", **kwargs)

    headmaster_thought "Ah, a lot of office supplies here!"
    headmaster_thought "I could use this for my lab."

    $ inventory_manager.add_item(Item("lab_office_supplies"))

    $ end_event("new_daytime", **kwargs)

label lab_intro_2_search_school_2 (**kwargs):
    $ begin_event(**kwargs)

    # headmaster looks for some equipment in the school
    # headmaster doesn't find anything else useful in the school

    headmaster_thought "Nothing useful here."

    $ end_event("new_daytime", **kwargs)


label lab_intro_2_search_office (**kwargs):
    $ begin_event(**kwargs)

    headmaster_thought "Let's check the office."
    call composite_event_runner(**kwargs) from lab_intro_2_search_office_composite_event_runner

label lab_intro_2_search_office_1 (**kwargs):
    $ begin_event(**kwargs)

    # headmaster looks for some equipment in the office
    # headmaster finds a a label maker and some small office supplies

    headmaster_thought "Ah, a label maker! Perfect!"

    $ inventory_manager.add_item(Item("lab_office_supplies"))

    $ end_event("new_daytime", **kwargs)

label lab_intro_2_search_office_2 (**kwargs):
    $ begin_event(**kwargs)

    # headmaster looks for some equipment in the office
    # headmaster doesn't find anything else useful in the office
    
    headmaster_thought "Nothing useful here."

    $ end_event("new_daytime", **kwargs)

# endregion
#############################

#############################
# region Lab Intro 3 Events #

init 2 python: 
    set_current_mod('base')

    office_building_work_event["lab"].add_event(
        Event(2, "lab_intro_3",
            TimeCondition(weekday = "d", daytime = "d"),
            ProgressCondition("lab_intro", 2),
            LevelCondition("2"),
            ItemCondition("lab_office_supplies"),
            ItemCondition("lab_glassware"),
            ItemCondition("lab_gas_burner"),
            ItemCondition("lab_distilled_water"),
            ItemCondition("lab_mortar_and_pestle"),
            ItemCondition("lab_utensils"),
            ItemCondition("lab_chemicals"),
            ItemCondition("lab_furniture"),
            ReplayCategoryOption("lab_intro"),
            Pattern("main", "images/events/lab/lab_intro_3/lab_intro_3 <step>.webp"),
            thumbnail = "images/events/lab/lab_intro_3/lab_intro_3 6.webp"))

# all equipment needs to be found and purchased
label lab_intro_3 (**kwargs):
    $ begin_event(**kwargs)

    $ image = convert_pattern("main", **kwargs)

    # headmaster starts setting up a makeshift lab in the office

    $ image.show(0)
    headmaster_thought "Let's start setting up the lab."
    subtitles "The storage room smells like dust and old ink. The desk surface is gritty under his palms."
    headmaster_thought "I should start with recreating the base potion."

    # multiple shots of the headmaster setting up the lab 
    call Image_Series.show_image(image, 1, 2, 3, 4, 5) from _call_show_image_lab_intro_3_1
    headmaster_thought "Now I can start experimenting with the equipment."
    $ image.show(6)
    headmaster_thought "I should start with recreating the base potion."

    $ set_progress("lab_intro", 3)

    $ end_event("new_daytime", **kwargs)

# endregion
#############################

#############################
# region Lab Intro 4 Events #

init 2 python: 
    set_current_mod('base')

    office_building_lab_events["research"].add_event(
        Event(3, "lab_intro_4",
            TimeCondition(weekday = "d", daytime = "d"),
            LevelCondition("2"),
            ProgressCondition("lab_intro", 3),
            ReplayCategoryOption("lab_intro"),
            Pattern("main", "images/events/lab/lab_intro_4/lab_intro_4_<step>.webp"),
            thumbnail = "images/events/lab/lab_intro_4/lab_intro_4_0.webp"))

label lab_intro_4 (**kwargs):
    $ begin_event(**kwargs)

    $ image = convert_pattern("main", **kwargs)

    $ image.show(0)
    subtitles "The vial is warm from being in his pocket all morning. The liquid inside is amber — darker than expected, catching the desk lamp like old honey."

    headmaster_thought "Alright. Let's get to work."
    $ image.show(1)
    headmaster_thought "I should check my notes first..."
    $ image.show(2)
    headmaster_thought "Where is the notebook? I had it just before..."
    $ image.show(3)
    headmaster_thought "Damn. I must have left it somewhere."
    $ image.show(4)
    headmaster_thought "I'll have to manage without it for now. Let's start analyzing the potion."

    # shots of the headmaster analyzing the potion
    call Image_Series.show_image(image, 5, 6) from _call_show_image_lab_intro_4_1
    headmaster_thought "Okay, I think I have a good idea of what to do."
    call Image_Series.show_image(image, 7, 8, 9) from _call_show_image_lab_intro_4_2
    headmaster_thought "Now let's try to recreate the potion."

    call Image_Series.show_image(image, 10, 11) from _call_show_image_lab_intro_4_3
    subtitles "The smell is wrong at first — sharp, almost medicinal. He adjusts the ratio. Tries again."

    ## 3 hours later...
    $ image.show(12)
    headmaster_thought "Hmm, I could only make these vials. I need to figure out how to make more."
    headmaster_thought "I need to think about it a bit more. I should try it myself first — just in case there are any side effects."
    $ image.show(13)
    headmaster_thought "Okay, here goes nothing..."

    subtitles "It tastes like copper with something sweet fighting underneath — not pleasant, not chemical, just wrong in a way he can't name yet."
    $ image.show(14)
    headmaster_thought "Hmm, I definitely need to work on the taste..."
    $ image.show(15)
    headmaster_thought "No side effects so far. But it's too early to say."
    $ image.show(16)
    headmaster_thought "I'll stop here for today. Let's see what tomorrow brings."

    $ set_progress("lab_intro", 4)

    $ end_event("new_daytime", **kwargs)

# endregion
#############################

#############################
# region Lab Intro 5 Events #

init 2 python: 
    set_current_mod('base')

    time_check_events.add_event(
        Event(2, "lab_intro_5",
            TimeCondition(weekday = "d", daytime = 1),
            ProgressCondition("lab_intro", 4),
            ReplayCategoryOption("lab_intro"),
            Pattern("main", "images/events/lab/lab_intro_5/lab_intro_5 <step>.webp"),
            thumbnail = "images/events/lab/lab_intro_5/lab_intro_5 0.webp"),
    )

label lab_intro_5 (**kwargs):
    $ begin_event(**kwargs)

    subtitles "It's morning. The lab smell has seeped into his clothes overnight."
    headmaster_thought "I seem to be fine. I don't feel any effects yet."
    headmaster_thought "Though... I don't feel any effect at all."
    headmaster_thought "Maybe I'm just not susceptible to it. Nothing for me to be conditioned toward..."
    headmaster_thought "The formula targets inhibition. Suppressed desire. If those aren't present in the subject to begin with..."
    headmaster_thought "Maybe it only works on women."
    headmaster_thought "At any rate — no adverse effects. The formula is sound. Time to move forward."

    $ set_progress("lab_intro", 5)

    $ end_event("new_daytime", **kwargs)

# endregion
#############################

#############################
# region Lab Intro 6 Events #

init 2 python: 
    set_current_mod('base')

            # TimeCondition(weekday = "d", daytime = "d"),
            # ProgressCondition("lab_intro", 5),
    lab_intro_6_event = Event(3, "lab_intro_6",
            ReplayCategoryOption("lab_intro"),
            Pattern("main", "images/events/lab_intro/lab_intro_5/lab_intro_5 <step>.png"),
            thumbnail = "images/events/lab/lab_intro_6_secret/lab_intro_6_secretary_talk 0.webp")
    office_building_call_secretary_events["talk"].add_event(lab_intro_6_event)
    test_events.add_event(lab_intro_6_event)

label lab_intro_6 (**kwargs):
    $ begin_event(**kwargs)

    $ image = convert_pattern("main", **kwargs)

    $ secretary_person = Person["emiko_langley"]
    $ secretary_person.register_paperdoll()
    $ paperdoll_manager.set_background("images/background/office building/secretary 6 1 0.webp", blur = True)
    $ secretary_person.display(PDAImage(pose = "12", outfit = "uniform", level = 6, mood = "suprised", mouth = "open"),
        PDAPreset("upper_body", duration = 0.0),
        PDAPreset("outside", duration = 0.0)
    )

    headmaster "Emiko! Look, I tried to recreate the potion. Would you like to try it?"
    $ secretary_person.display(PDAPreset("upper_body_center", duration = 1.0))
    secretary "Hi"
    $ secretary_person.display(PDAImage(pose = "12", mood = "neutral", mouth = "closed"))
    headmaster "A potion prototype. I've already checked for unwanted side effects."
    $ secretary_person.display(PDAImage(pose = "19", mood = "happy", mouth = "open"))
    secretary "Sure, I'd like to try it."

    $ secretary_person.clear_display()

    $ image.show(0)
    headmaster "Great! Here you go."
    $ image.show(1)
    subtitles "The potion has a sweet, faintly floral smell. The kind of smell that sticks to the back of the throat."
    $ image.show(2)
    headmaster "How do you feel?"

    $ image.hide()
    $ paperdoll_manager.set_background("images/background/office building/secretary 6 1 0.webp", blur = True)
    $ secretary_person.display(PDAImage(pose = "21", mood = "neutral", mouth = "open"))
    secretary "Hmm. A little warmer. That's about it."
    $ secretary_person.display(PDAImage(pose = "10", mood = "neutral", mouth = "closed"))
    subtitles "Silence. Just the faint hum of the ventilation and the sound of his own breathing."
    $ secretary_person.display(PDAImage(pose = "10", mood = "happy", mouth = "closed"))
    headmaster "Oh well. Worth a try. I'll go wider — students next."
    $ secretary_person.display(PDAImage(pose = "10", mood = "happy", mouth = "open"))
    secretary "Good luck!"
    $ secretary_person.display(PDAImage(pose = "10", mood = "happy", mouth = "closed"),
        PDAPreset("outside", duration = 1.0), PDAPause(duration = 1.0))
    $ image.show(3)
    headmaster_thought "First I have to produce more."

    $ set_progress("lab_intro", 6)

    $ end_event("new_daytime", **kwargs)

# endregion
#############################

######################################
# region Lab Intro Production Events #

init 3 python: 
    set_current_mod('base')

    office_building_work_event["lab"].add_event(
        EventSelect(3, "lab_event_selection", "What do you want to do in the lab?", office_building_lab_events,
            TimeCondition(weekday = "d", daytime = "d"),
            ProgressCondition("lab_intro", "3+"),
            ReplayCategoryOption("lab_intro"),
            Pattern("main", "images/events/lab/lab_intro_3/lab_intro_3 <step>.webp")))

    office_building_lab_events["produce"].add_event(
        Event(3, "lab_intro_produce_test_potion",
            TimeCondition(weekday = "d", daytime = "d"),
            ProgressCondition("lab_intro", "6,7"),
            ItemCondition("lab_chemicals"),
            NOT(ItemCondition("lab_test_potion")),
            ReplayCategoryOption("lab_intro"),
            Pattern("main", "images/events/lab/lab_intro_produce_test_potion/lab_intro_produce_test_potion <step>.webp"),
            thumbnail = "images/events/lab/lab_intro_produce_test_potion/lab_intro_produce_test_potion 0.webp"),
        Event(3, "lab_intro_produce_test_potion_no_chemicals",
            TimeCondition(weekday = "d", daytime = "d"),
            ProgressCondition("lab_intro", "6,7"),
            NOT(ItemCondition("lab_chemicals")),
            NOT(ItemCondition("lab_test_potion")),
            ReplayCategoryOption("lab_intro"),
            Pattern("main", "images/events/lab/lab_intro_produce_test_potion_no_chemicals/lab_intro_produce_test_potion_no_chemicals <step>.webp"),
            thumbnail = "images/events/lab/lab_intro_produce_test_potion_no_chemicals/lab_intro_produce_test_potion_no_chemicals 0.webp"),
    )


label lab_intro_produce_test_potion (**kwargs):
    $ begin_event(**kwargs)

    # shots of headmaster producing more potions
    headmaster_thought "I definitely have to improve the process in the future."
    headmaster_thought "There is just too much chemicals wasted..."

    $ inventory_manager.remove_item("lab_chemicals", 1)
    $ inventory_manager.add_item("lab_test_potion")

    $ end_event("new_daytime", **kwargs)

label lab_intro_produce_test_potion_no_chemicals (**kwargs):
    $ begin_event(**kwargs)

    # shots of headmaster producing more potions
    headmaster_thought "I don't have any chemicals left. I first have to buy some more."

    $ end_event("new_daytime", **kwargs)

# endregion
######################################

# #############################
# # region Lab Intro 7 Events #

# init 2 python: 
#     set_current_mod('base')

#     sb_events["patrol"].add_event(
#         Event(3, "lab_intro_7",
#             TimeCondition(weekday = "d", daytime = "d"),
#             ProgressCondition("lab_intro", 6),
#             ItemCondition("lab_test_potion"),
#             ReplayCategoryOption("lab_intro"),
#             Pattern("main", "images/events/lab/lab_intro_7/lab_intro_7 <step>.webp"),
#             thumbnail = "images/events/lab/lab_intro_7/lab_intro_7 0.webp"),
#     )

# label lab_intro_7 (**kwargs):
#     $ begin_event(**kwargs)

#     $ sakura = Person["sakura_mori"].get_renpy_char()
#     $ easkey = Person["easkey_tanaka"].get_renpy_char()

#     headmaster "Ahh Ms. Mori. I accidentally bought two cans of soda. I only need one. Do you want one?"
#     sakura "Sure, that would be great. Thank you very much!"
#     headmaster "Here you go."

#     # Sakura drinks the potion
#     sakura "Mmm, it kinda tastes weird..."
#     headmaster "Oh, the can fell down earlier. Sorry, I guess some of the fizz got lost..."
#     sakura "It's okay, it still tastes good."
#     headmaster "Great! Then, I'll see you later!"
#     sakura "Thank you very much!"

#     # The headmaster goes around the corner and secretly checks on Sakura.
#     sakura "Oh my God! It's so warm! Don't you think so?"
#     easkey "What? I think it might be a little cold. What's wrong, Sakura?"
#     easkey "Don't you feel good?"
#     sakura "No, I'm fine. I feel pretty good actually, but it is sooo warm!"

#     # Sakura opens her blouse
#     sakura "Ahh! Much better!"
#     easkey "Sakura! What are you doing?!"
#     sakura "Huh? What? I'm just trying to cool off. It's so warm!"
#     easkey "But you can't just undress in public!"
#     sakura "What do you mean..."
#     sakura "Huh?! Why is my blouse open?!"
#     easkey "I... I don't know! You just opened it!"
#     sakura "What?! No! Help me close it!"

#     headmaster_thought "Hmm, that's interesting. It seems to work well for her."
#     headmaster_thought "I wonder why it had no effect on Emiko... Maybe she needs a higher dose due to the effect of the original potion..."
#     headmaster_thought "Hmm, but then she would've been more susceptible to this potion. Technically, these potions should enhance the effects..."
#     headmaster_thought "I should try it with other students to see if it works for them. Maybe I should also try a higher dose on Emiko."
    
#     headmaster_thought "Heat sensitivity. Loss of self-awareness. Inhibition down, memory gaps."
#     headmaster_thought "Short-lived. But it works."
    
#     # headmaster goes away

#     $ set_progress("lab_intro", 7)

#     $ end_event("new_daytime", **kwargs)

# # endregion
# #############################

# #############################
# # region Lab Intro 8 Events #

# init 2 python: 
#     set_current_mod('base')

#     office_building_events["look_around"].add_event(
#         Event(3, "lab_intro_8",
#             TimeCondition(weekday = "d", daytime = "f"),
#             ProgressCondition("lab_intro", 7),
#             ItemCondition("lab_test_potion"),
#             ReplayCategoryOption("lab_intro"),
#             Pattern("main", "images/events/lab/lab_intro_8/lab_intro_8 <step>.webp"),
#             thumbnail = "images/events/lab/lab_intro_8/lab_intro_8 0.webp"),
#     )

# label lab_intro_8 (**kwargs):
#     $ begin_event(**kwargs)

#     $ zoe = Person["zoe_parker"].get_renpy_char()
#     $ finola = Person["finola_ryan"].get_renpy_char()

#     headmaster_thought "Hmm, the teachers should be back in a few minutes. I could put the potion in their coffee."
#     # Headmaster Put's Potion in Coffee
#     headmaster_thought "Now to wait..."
#     # Teachers arrive
#     zoe "Good morning, [headmaster_first_name]!"
#     zoe "Can I help you with something?"
#     headmaster "Ah, Mrs. Parker. No thanks, I just thought I could work here. You know, get a little closer to the staff."
#     zoe "Ah, that's great! I'm going to get some coffee."
#     headmaster "You do that. I'll be here."
#     zoe "All right, see you later!"
#     # Zoe goes to the coffee machine
#     # Finola also gets some coffee.
#     # Both talk to each other while drinking
#     finola "Oh man, it's getting really warm in here."
#     zoe "Yes. I feel it too."
#     finola "I think... I'm beginning to feel something..."
#     zoe "Is everything okay?"
#     finola "Sorry, I think I need to go to the bathroom."
#     zoe "Oh, okay."
#     # Finola rushes off
#     zoe "Wow, it's getting really hot in here."
#     # zoe takes off jacket
#     # Finola comes back in different clothes
#     zoe "Finola! Are you all right?"
#     finola "Yeah, I'm fine. I just need to cool off a bit."
#     finola "Luckily I had some other clothes here. This is a little more comfortable."
#     zoe "Yes, I see. That top looks great on you. You should wear it more often!"
#     finola "I don't know, it shows a little too much..."
#     zoe "Oh, come on. You have an amazing body. You should show it off more!"
#     finola "Do you think so? I'm not sure..."
#     zoe "Of course I think so. You should be proud of your body. It's a gift from God."
#     finola "I'll think about it..."
#     zoe "Don't overthink it. Just do it. You'll feel great."

#     # A few moments pass

#     finola "Wait..." 
#     # Finola looks down at her outfit, confusion crossing her face
#     finola "Why did I... I need to change back. This is completely inappropriate for work."

#     zoe "I... yeah, sorry, I don't know why I was pushing that. That was weird of me."
#     # Zoe shakes her head slightly, looking uncomfortable

#     subtitles "The faculty lounge smells like burnt coffee and something sweeter underneath — faint, already fading."
#     headmaster_thought "Five minutes. Maybe less. They snap back every time."
#     headmaster_thought "I need a catalyst."

#     $ set_progress("lab_intro", 8)

#     $ end_event("new_daytime", **kwargs)

# # endregion
# #############################

# #############################
# # region Lab Intro 9 Events #

# init 2 python: 
#     set_current_mod('base')

#     office_building_events["patrol"].add_event(
#         Event(3, "lab_intro_9",
#             TimeCondition(weekday = "d", daytime = "f"),
#             ProgressCondition("lab_intro", 8),
#             ItemCondition("lab_test_potion"),
#             ReplayCategoryOption("lab_intro"),
#             Pattern("main", "images/events/lab/lab_intro_9/lab_intro_9 <step>.webp"),
#             thumbnail = "images/events/lab/lab_intro_9/lab_intro_9 0.webp"),
#     )

# # Chemical Mishap
# label lab_intro_9 (**kwargs):
#     $ begin_event(**kwargs)

#     $ ishimaru = Person["ishimaru_maki"].get_renpy_char()

#     headmaster_thought "I should test another dose on the students. See if the response varies by individual."
    
#     # headmaster bumps into student cleaning the hallway
#     headmaster "Oh—!"
    
#     # student's bucket tips, spilling cleaning solution across the floor
#     # headmaster's potion vial slips from his hand and shatters in the puddle
    
#     headmaster_thought "Damn it."
    
#     headmaster "My apologies, are you alright?"
#     ishimaru "I'm fine, Mr. [headmaster_last_name]! I'm so sorry, I'll clean this up right away."
#     headmaster "No harm done. Just watch for the glass shards."
    
#     headmaster_thought "There goes one dose. I'll have to synthesize more tonight."
    
#     # headmaster walks away
    
#     # vapor begins rising from the mixture where potion and cleaning chemicals merged
    
#     headmaster_thought "Huh... what's that smell?"
#     headmaster_thought "Actually... that smells really nice. Kinda sweet?"
    
#     # The classroom door down the hall is open
#     # Vapor drifts naturally toward the doorway where Luna, Lin, and Gloria are visible inside talking
    
#     $ set_progress("lab_intro", 9)

#     $ end_event("new_daytime", **kwargs)

# # endregion
# #############################

# ##############################
# # region Lab Intro 10 Events #

# init 2 python: 
#     set_current_mod('base')

#     office_building_events["look_around"].add_event(
#         Event(3, "lab_intro_10",
#             TimeCondition(weekday = "d", daytime = "f"),
#             ProgressCondition("lab_intro", 8),
#             ItemCondition("lab_test_potion"),
#             ReplayCategoryOption("lab_intro"),
#             Pattern("main", "images/events/lab/lab_intro_9/lab_intro_9 <step>.webp"),
#             thumbnail = "images/events/lab/lab_intro_9/lab_intro_9 0.webp"),
#     )

# # Investigation unlocks after Chemical Mishap
# label lab_intro_10 (**kwargs):
#     $ begin_event(**kwargs)

#     $ gloria = Person["gloria_goto"].get_renpy_char()
#     $ lin = Person["lin_kato"].get_renpy_char()
#     $ luna = Person["luna_clark"].get_renpy_char()
#     $ ishimaru = Person["ishimaru_maki"].get_renpy_char()

#     # IMAGE: School hallway, afternoon light through windows
#     # Headmaster walking back toward the area where spill occurred
#     # Slight mess from earlier still visible (wet patches, chemical residue)
#     # His expression curious, investigative
    
#     headmaster_thought "That smell from earlier. It's still lingering in this hallway."
#     headmaster_thought "I should check if there are any unexpected effects from the spill."
    
#     # IMAGE: Headmaster pausing outside classroom door (slightly ajar)
#     # Light spilling from inside, sound of girlish laughter
#     # His hand on doorframe, head tilted listening
    
#     headmaster_thought "That's odd. Class shouldn't be in session now."
    
#     # [Rest of the event continues as written...]
#     # IMAGE: Headmaster pushing door open slightly, peering inside
#     # View from his POV: three girls visible in the back corner
#     # Gloria and Lin sitting close together on desk, Luna in chair beside them
#     # All three with blouses partially unbuttoned, relaxed postures
    
#     headmaster "Girls? Is everything—"
    
#     # IMAGE: Girls turning toward him, bright smiles
#     # Gloria waving him in enthusiastically
#     # Lin leaning against Gloria's shoulder
#     # Luna's blouse hanging open loosely, revealing white lace bra
    
#     gloria "Mr. [headmaster_last_name]! Perfect timing, come sit with us!"
    
#     headmaster_thought "What in the world...?"
    
#     headmaster "Are you girls alright? You look..."
    
#     # IMAGE: Headmaster stepping into room
#     # Now visible: the room feels warmer than it should
#     # Afternoon sunlight streaming across desks
#     # The three girls flushed, eyes bright, hair slightly disheveled
    
#     lin "We're fantastic! Better than alright, honestly."
    
#     gloria "We were just comparing bras. Look how cute Lin's is!"
    
#     # IMAGE: Lin straightening up, pulling her blouse wider to display
#     # Navy blue bra with white trim detail visible
#     # Gloria's hand on Lin's shoulder, casual intimacy
#     # Luna watching with amused smile
    
#     lin "It's new! Got it last week. The white trim is adorable, right?"
    
#     headmaster "Yes, very... nice."
    
#     headmaster_thought "They're showing me their underwear like it's the most natural thing in the world. No hesitation, no embarrassment."
    
#     gloria "Now mine—tell me honestly, is the black too much? I thought it looked sophisticated."
    
#     # IMAGE: Gloria pulling her blouse fully open
#     # Sleek black satin bra clearly visible, more revealing cut than Lin's
#     # She's looking at headmaster expectantly
#     # Lin giggling beside her, Luna leaning forward with interest
    
#     headmaster "It's... elegant. Suits you."
    
#     gloria "Oh thank you! See, I told you guys it wasn't too grown-up."
    
#     luna "Okay, okay, your turn now Luna!"
    
#     # IMAGE: Luna shaking her head, but smiling
#     # Arms crossed loosely over chest
#     # Gloria and Lin both turning attention to her
    
#     luna "No way. Not in front of Mr. [headmaster_last_name]."
    
#     lin "Oh come on! We both showed ours!"
    
#     gloria "Don't be shy! We're all being open here."
    
#     luna "But I'm not wearing—"
    
#     lin "Exactly why you have to show! Come on, Luna!"
    
#     # IMAGE: Luna glancing at headmaster, then back at her friends
#     # Biting her lip, considering
#     # Her hands moving to the edges of her blouse
    
#     luna "Fine. But don't make it weird."
    
#     gloria "We won't!"
    
#     # IMAGE: Luna pulling her blouse fully open
#     # No bra underneath - bare breasts visible
#     # Pale skin, soft pink nipples
#     # Her expression a mix of defiance and nervousness
#     # Gloria and Lin's reactions: genuine surprise
    
#     gloria "WOAH!"
    
#     lin "Luna! You're not wearing anything?"
    
#     # IMAGE: Luna shrugging, leaving blouse open
#     # More confident now that the reveal is done
#     # Headmaster's face carefully neutral but eyes definitely looking
    
#     luna "Never do. Mum says bras aren't healthy, restrict circulation or something."
    
#     gloria "Huh. I never thought about that."
    
#     luna "Mr. [headmaster_last_name], you think they're nice?"
    
#     # IMAGE: Headmaster caught off-guard, eyes snapping up from her chest
#     # Luna looking at him directly, no shame
#     # Gloria and Lin watching his reaction with curiosity
    
#     headmaster "I—yes, they're lovely. But I should really be going now."
    
#     headmaster_thought "Christ. She's standing there topless asking my opinion like we're discussing the weather."
#     headmaster_thought "What happened here? This isn't normal teenage boundary-testing, this is something else entirely."
    
#     lin "Aww, already? We're having fun!"
    
#     # IMAGE: Headmaster backing toward door
#     # Girls still relaxed, Luna's blouse still open
#     # The afternoon light catches dust motes in the air
    
#     headmaster "I'll see you girls in class. Make sure to... button up before anyone else comes by."
    
#     gloria "Okay, okay. Bye Mr. [headmaster_last_name]!"
    
#     luna "Gloria, don't touch them!"
    
#     gloria "I just want to see if they feel different without a bra!"
    
#     # IMAGE: Headmaster in hallway outside classroom door
#     # Door closing behind him, muffled giggles audible
#     # Him running hand through hair, processing
#     # SMELL: faint sweet scent in the air, almost floral but with chemical edge
    
#     headmaster_thought "That smell. What is that?"
#     headmaster_thought "It's everywhere in there. Sweet, but not perfume. Something sharper underneath."
    
#     ishimaru "Mr. [headmaster_last_name]!"
    
#     # IMAGE: Ishimaru approaching from down the hall
#     # Carrying the broken vial pieces carefully in tissue
#     # Her shirt is off - wearing only skirt and white sports bra
#     # Skin slightly flushed, breathing a bit quick
    
#     headmaster "Ms. Maki! What happened to your top?"
    
#     # IMAGE: Ishimaru looking down at herself, then back up
#     # Casual shrug, no embarrassment
#     # Holding out the tissue with broken glass
    
#     ishimaru "Got it dirty while cleaning the spill. Easier to just take it off than walk around with stains."
    
#     ishimaru "I found this earlier. After we bumped into each other. Thought it might be yours."
    
#     # IMAGE: Headmaster taking the tissue, examining broken vial
#     # Ishimaru standing close, closer than normal professional distance
#     # Her hand lingering near his as she hands it over
    
#     headmaster "Yes, thank you. It... broke?"
    
#     ishimaru "It must've when it fell. I tried to clean it up but the liquid had already mixed with the cleaning solution."
    
#     headmaster_thought "The cleaning solution."
    
#     ishimaru "There was this really nice smell after. Kind of sweet? I've been smelling it all afternoon."
    
#     # IMAGE: Close-up of Ishimaru's face
#     # Pupils slightly dilated, small smile
#     # Leaning in subtly, head tilted
    
#     ishimaru "You smell nice too, Mr. [headmaster_last_name]. Is that cologne?"
    
#     headmaster "I... don't wear cologne."
    
#     # IMAGE: Ishimaru's hand reaching out, touching his forearm lightly
#     # Contact casual but lingering
#     # Her thumb brushing across his sleeve
    
#     ishimaru "Huh. Well, something smells really good."
    
#     headmaster "You can throw the glass away. I don't need it anymore."
    
#     ishimaru "Okay. See you later..."
    
#     # IMAGE: Ishimaru walking away
#     # Looking back over shoulder with smile
#     # Headmaster watching her go, tissue with broken vial in hand
    
#     headmaster_thought "The cleaning solution. The girls in the classroom. Ishimaru just now."
#     headmaster_thought "They all have that same look. That same lack of inhibition."
#     headmaster_thought "And that smell—it's the same one in the classroom. Stronger near where the spill happened."
#     headmaster_thought "Something in the cleaning chemicals reacted with the potion. Had to. But what?"
    
#     $ set_progress("lab_intro", 10)
    
#     $ end_event("new_daytime", **kwargs)

# # Analysis unlocks after Investigation
# label lab_intro_11 (**kwargs):
#     $ begin_event(**kwargs)

#     # IMAGE: Headmaster's office, late afternoon
#     # Papers spread across desk, him leaning back in chair
#     # Hand rubbing temples, thinking hard
#     # Window showing orange sunset light
    
#     headmaster_thought "The smell. The behavior. The timing. It all connects to that spill."
    
#     # IMAGE: Secretary entering office
#     # Knocking perfunctorily but already pushing door open
#     # Carrying folder, professional demeanor
#     # Headmaster looking up, expression shifting to eager
    
#     headmaster "Emiko! Perfect timing."
    
#     secretary "You look like you've had an eventful day."
    
#     # IMAGE: Headmaster gesturing to chair across from desk
#     # Secretary settling into it, crossing legs
#     # Setting folder aside, giving him full attention
    
#     headmaster "Eventful is one word for it. I think I've made a breakthrough."
    
#     secretary "Oh?"
    
#     secretary_thought "*He's practically vibrating with excitement. This should be good.*"
    
#     # IMAGE: Headmaster leaning forward, hands clasped on desk
#     # Animated expression, eyes bright
#     # Secretary maintaining polite interest
    
#     headmaster "Remember when I dropped that vial in the hallway? When I bumped into Ms. Maki?"
    
#     secretary "You mentioned it."
    
#     headmaster "I went back to investigate the area. Found three students in a classroom—blouses open, showing each other their bras like it was show-and-tell."
    
#     # IMAGE: Secretary's eyebrow raising slightly
#     # Leaning forward, interested but controlled
#     # Headmaster's hands gesturing as he talks
    
#     headmaster "One of them wasn't even wearing a bra. Just opened her shirt and asked my opinion on her breasts. Zero hesitation."
    
#     secretary "That's... significantly different from your earlier results."
    
#     # IMAGE: Headmaster nodding emphatically
#     # Standing now, starting to pace
#     # Secretary's eyes tracking him, calculating
    
#     headmaster "Exactly! The previous doses were short-lived. Minutes at most before the subjects snapped back."
#     headmaster "But these girls—they'd been like that for at least fifteen minutes by the time I found them. Possibly longer."
    
#     secretary "What about Ms. Maki?"
    
#     # IMAGE: Headmaster pausing mid-pace
#     # Turning to face secretary
#     # Slight flush on his cheeks remembering
    
#     headmaster "She was topless. Said she'd taken her shirt off while cleaning because it got dirty."
#     headmaster "Then she got very... close. Touching my arm, complimenting how I smell."
    
#     secretary "Flirting."
    
#     headmaster "Blatantly."
    
#     # IMAGE: Secretary's slight smile
#     # Fingers steepled, thinking
#     # Headmaster watching her, waiting for her input
    
#     secretary "So multiple subjects, stronger effects, longer duration. Something was different."
    
#     secretary_thought "*The catalyst worked even better than expected. But he doesn't know that's what it is yet.*"
    
#     # IMAGE: Headmaster moving back to desk
#     # Picking up the tissue with broken vial pieces
#     # Examining them in the fading light
    
#     headmaster "The smell. That's what was different."
    
#     secretary "Smell?"
    
#     headmaster "In the classroom, in the hallway near the spill—there was this scent. Sweet, almost floral, but with something chemical underneath."
#     headmaster "Both Ishimaru and the students mentioned it. Said it smelled good, appealing."
    
#     # IMAGE: Secretary standing, moving to window
#     # Looking out thoughtfully
#     # Headmaster still at desk, watching her
    
#     secretary "You think something reacted with your potion?"
    
#     headmaster "Has to be. The vial broke in the spill—Ishimaru said it mixed with the cleaning solution."
    
#     # IMAGE: Both in office, light nearly gone
#     # Headmaster looking thoughtful but troubled
#     # Secretary watching him, calculating
#     # Sense of conspiracy, shared purpose

#     headmaster "The implications are staggering. If I can isolate which compound created that reaction..."

#     secretary "You'd have a catalyst. Something to make the effects permanent instead of temporary."

#     headmaster "Exactly."

#     # IMAGE: Headmaster's excitement fading to frustration
#     # Slumping slightly in chair
#     # Secretary noticing the shift

#     headmaster "But I need to test it properly. Controlled experiments. And I've already used most of my supply on those early tests."

#     secretary "Hmm."

#     secretary_thought "*He doesn't realize it yet, but he's exactly where I need him. Desperate enough to push forward, limited enough to need my help.*"

#     # IMAGE: Secretary standing, gathering her folder
#     # Professional smile
#     # Headmaster looking drained but thoughtful

#     secretary "Let's call it a day. Sleep on it, come back fresh tomorrow."

#     headmaster "You're right. I need to think this through carefully."

#     secretary "Good idea. We'll figure something out."

#     # IMAGE: Secretary at door, looking back
#     # Professional demeanor maintained
#     # Headmaster already staring at the broken vial pieces again

#     secretary "This is important work. Don't lose sight of that."

#     headmaster "I won't."

#     secretary_thought "*Tomorrow I'll plant the seeds. Teachers first, then parents. Then he'll see what's really possible.*"

#     $ set_progress("lab_intro", 11)

#     $ end_event("new_daytime", **kwargs)

# # Frustration unlocks after Analysis and Secretary's Spin
# label lab_intro_12 (**kwargs):
#     $ begin_event(**kwargs)
    
#     # IMAGE: Headmaster's office converted to makeshift lab
#     # Late evening, desk lamp the only light
#     # Cleaning cart pulled into room, various bottles arranged
#     # Two vials of experimental potion, multiple small test tubes
#     # Notebook open with methodical notes
    
#     headmaster_thought "Systematic approach. Test each compound individually, document the reaction."
    
#     # IMAGE: Headmaster in safety goggles, gloves
#     # Pipetting tiny amount of potion into test tube
#     # First cleaning chemical bottle open beside him
#     # Concentrated expression, scientific precision
    
#     headmaster "Ammonia solution. Standard concentration."
    
#     # IMAGE: Adding single drop of ammonia to potion
#     # Watching carefully for reaction
#     # Liquid remains amber, no change
#     # His expression: focused disappointment
    
#     headmaster_thought "No visible reaction. No color change, no precipitation, no effervescence."
    
#     # IMAGE: Headmaster making note in notebook
#     # Crossing off "ammonia" from list
#     # Moving to next bottle on cart
#     # Test tube disposed in waste container
    
#     headmaster "Next. Industrial surfactant blend."
    
#     # IMAGE: Fresh test tube, new potion sample
#     # Adding drop of surfactant
#     # Liquid clouds slightly but settles back to amber
#     # Headmaster shaking head
    
#     headmaster_thought "Temporary emulsion, but no catalytic effect. Not this one either."
    
#     # IMAGE: Time passing montage
#     # Multiple test tubes used and discarded
#     # Cleaning bottles being tested one by one
#     # Headmaster's posture getting more tense
#     # Coffee mug emptied and refilled
#     # Night deepening outside window
    
#     headmaster "Chlorinated degreaser. Sodium hypochlorite solution. Quaternary ammonium compound."
    
#     # IMAGE: Notebook showing growing list of crossed-off chemicals
#     # Headmaster rubbing eyes, fatigue setting in
#     # Only a few bottles left untested
#     # One vial of potion nearly empty from all the tests
    
#     headmaster_thought "Seven compounds tested. Nothing. Maybe the reaction requires multiple chemicals working together?"
#     headmaster_thought "But that exponentially increases the complexity..."
    
#     # IMAGE: Headmaster picking up next bottle
#     # Large industrial bottle, 2.5 liter size
#     # Reading label carefully
#     # "Trichloroethylene - Industrial Solvent"
#     # Warning labels visible: flammable, ventilation required
    
#     headmaster "Trichloroethylene. That's... uncommon for standard cleaning."
#     headmaster "Must be for heavy degreasing. Probably left over from when they used this building for maintenance."
    
#     # IMAGE: Fresh test tube, careful potion measure
#     # Adding single drop of TCE
#     # Immediate reaction - liquid shimmers
    
#     headmaster "Wait—"
    
#     # IMAGE: Close-up of test tube
#     # Amber liquid becoming more vibrant, almost glowing
#     # Slight vapor rising with sweet chemical scent
#     # Color intensifying, becoming richer
    
#     headmaster "That's it. That's the reaction!"
    
#     # IMAGE: Headmaster's face lit by the glowing sample
#     # Excitement and triumph
#     # Leaning in close, examining the transformation
#     # The amber liquid now matching the intensity from the hallway spill
    
#     headmaster_thought "Trichloroethylene. That's the catalyst. That's what made the difference!"
    
#     # IMAGE: Headmaster frantically making notes
#     # Documenting the reaction in detail
#     # Checking the TCE bottle label again
#     # Adrenaline replacing fatigue
    
#     headmaster "The molecular structure must interact with the organic compounds in the base potion..."
#     headmaster "Creating a stable enhancement that prevents degradation of the active ingredients."
    
#     # IMAGE: Headmaster setting down the glowing test tube
#     # Picking up the large TCE bottle
#     # Reading the label - standard old hazard warnings
#     # His expression triumphant
    
#     headmaster "Trichloroethylene. Industrial degreaser."
    
#     # IMAGE: Headmaster checking the bottle's fill level
#     # Large industrial bottle, about half full
#     # Roughly 1.2 liters remaining
#     # Old, yellowed label, clearly vintage
    
#     headmaster "About a liter left. That's... actually a decent amount."
    
#     headmaster_thought "Enough for multiple applications. I can work with this."
#     headmaster_thought "But I should verify I can order more for future batches."
    
#     # IMAGE: Headmaster pulling out his phone
#     # Typing into search: "trichloroethylene purchase"
#     # Screen glow on his face in the dim office
#     # Expectant expression
    
#     # IMAGE: Close-up of phone screen
#     # Search results showing:
#     # "TCE phased out under EPA regulations"
#     # "Discontinued for commercial sale"
#     # "Restricted substance - industrial permits required"
    
#     headmaster_thought "What?"
    
#     # IMAGE: Headmaster's expression shifting from confusion to dismay
#     # Scrolling through results
#     # Multiple sites showing same message
#     # His triumph beginning to crumble
    
#     headmaster "Phased out. Environmental regulations... ozone depletion concerns."
    
#     # IMAGE: Headmaster clicking through to supplier website
#     # "This product requires industrial certification and bulk minimum orders"
#     # "$5000 minimum purchase - 200L drums only"
#     # "EPA permit documentation required"
    
#     headmaster "Five thousand dollars. Two hundred liters minimum."
#     headmaster "And environmental permits I don't have."
    
#     # IMAGE: Headmaster setting phone down
#     # Looking at the TCE bottle with new perspective
#     # What's there is all he'll ever have
#     # The glowing test tube representing both success and limitation
    
#     headmaster_thought "The school's bottle is ancient. From before the phaseout."
#     headmaster_thought "What I have here is irreplaceable. Once it's gone, it's gone forever."
    
#     # IMAGE: Headmaster calculating in his notebook
#     # Estimating catalyst ratios
#     # Looking at his two vials of base potion
#     # Doing the math
    
#     headmaster "A liter of catalyst. Maybe enough to enhance... twenty, thirty doses if I'm conservative with the ratio."
#     headmaster "But I only have two vials of base potion left. Barely enough for a handful of applications."
    
#     # IMAGE: Headmaster slumping in chair
#     # Head in hands
#     # The glowing test tube and TCE bottle on desk
#     # Victory feeling incomplete
    
#     headmaster_thought "I found the catalyst. I have enough of it for initial testing."
#     headmaster_thought "But I don't have enough base potion to use it on. And even if I synthesize more..."
    
#     # IMAGE: Headmaster's fist clenching on desk
#     # Jaw tight with frustration
#     # The perfect solution with imperfect resources
    
#     headmaster "Eventually this catalyst will run out. And I can't replace it."
#     headmaster "Every dose I make is one less I can ever make again."
    
#     # IMAGE: Headmaster standing, pacing
#     # Hands running through hair
#     # Office feeling claustrophobic despite the breakthrough
    
#     headmaster_thought "I need to be strategic. Can't waste this on random testing."
#     headmaster_thought "I need more base potion. I need better equipment to synthesize it."
#     headmaster_thought "And I need a plan for what to do with the limited catalyst I have."
    
#     # IMAGE: Headmaster looking at his two vials of base potion
#     # The large TCE bottle beside them
#     # Notebook showing the successful formula
#     # The weight of finite resources
    
#     headmaster "I could make a few enhanced doses with what I have. Test the formula properly."
#     headmaster "But then what? Wait weeks to synthesize more base potion in my closet setup?"
    
#     # IMAGE: Headmaster sitting back down heavily
#     # The glowing test tube still illuminating his notes
#     # Success achieved but path forward unclear
#     # Victory turned to strategic puzzle
    
#     headmaster_thought "I solved the mystery. I have the catalyst, at least for now."
#     headmaster_thought "But I'm still stuck. Limited materials, inadequate workspace, no replacement source."
#     headmaster_thought "I need help. I need a better plan."
    
#     # IMAGE: Office in darkness except for desk lamp
#     # Headmaster alone with his discovery
#     # Test tubes, bottles, notebooks surrounding him
#     # TCE bottle sitting there - precious and finite
    
#     headmaster "I have the answer. But I don't know what to do with it."
    
#     $ set_progress("lab_intro", 12)
    
#     $ end_event("new_daytime", **kwargs)

# # Strategic Planning unlocks after Frustration
# label lab_intro_13 (**kwargs):
#     $ begin_event(**kwargs)
    
#     # IMAGE: Headmaster's office, next morning
#     # Still looks like a lab - cleaning cart, test tubes
#     # Papers scattered, coffee mug refilled but untouched
#     # Headmaster at desk staring at the TCE bottle and his notes
#     # Morning light harsh through window
    
#     headmaster_thought "Twenty-four hours since I identified the catalyst. And I still don't know how to proceed."
    
#     # IMAGE: Door opening, secretary entering without knocking
#     # Folder under arm, professional demeanor
#     # Pausing when she sees the state of the office
#     # Headmaster looking up, exhausted
    
#     secretary "You look terrible."
#     headmaster "Good morning to you too."
    
#     # IMAGE: Secretary closing door, moving closer
#     # Taking in the makeshift lab setup
#     # Setting folder aside, giving him her attention
#     # Headmaster gesturing vaguely at the desk
    
#     secretary "I take it the testing didn't go well?"
#     headmaster "Actually, it went perfectly. That's the problem."
    
#     # IMAGE: Secretary settling into chair across from desk
#     # Crossing legs, focused on him
#     # Headmaster leaning back, rubbing face
#     # Sunlight cutting across the space between them
    
#     secretary "Explain."
    
#     headmaster "I found the catalyst. Trichloroethylene—an industrial solvent on the cleaning cart."
#     headmaster "The reaction was immediate, unmistakable. I documented everything."
    
#     secretary "That's excellent news."
    
#     # IMAGE: Headmaster picking up the large TCE bottle
#     # Showing it to her
#     # His expression frustrated despite the breakthrough
    
#     headmaster "This is all there is. The school's ancient bottle, maybe a liter left."
#     headmaster "And I can't get more. It's been phased out, requires industrial permits, minimum orders in the thousands of dollars."
    
#     # IMAGE: Secretary's eyebrows raising slightly
#     # Looking at the bottle, then back at him
#     # Processing the limitation
    
#     secretary "So you have the catalyst, but limited supply."
    
#     headmaster "Irreplaceable supply. Once this is gone, it's gone forever."
    
#     # IMAGE: Headmaster setting bottle down
#     # Gesturing to his two remaining vials of base potion
#     # Frustration evident in his movements
    
#     headmaster "And I barely have any base potion left. Maybe enough for six or seven doses total."
#     headmaster "I've spent all night trying to figure out how to synthesize more, find alternatives, optimize the process..."
    
#     secretary "And?"
    
#     headmaster "Every solution requires equipment I don't have, materials I can't source, or time I don't have."
    
#     # IMAGE: Secretary looking at him thoughtfully
#     # Slight tilt of her head
#     # Headmaster slumped in frustration
    
#     secretary "How many people work at this school?"
    
#     headmaster "What?"
    
#     secretary "Teachers. Staff. How many?"
    
#     # IMAGE: Headmaster looking confused by the question
#     # Secretary waiting patiently
#     # Him counting mentally
    
#     headmaster "Five teachers. You. Me. The cleaning staff, kitchen staff..."
    
#     secretary "And how many parents are on the PTA?"
    
#     headmaster "Three mothers. Plus the five teachers and myself, but..."
    
#     # IMAGE: Secretary's slight smile
#     # Leaning back, point made
#     # Headmaster processing
    
#     secretary "So you're sitting here panicking about supply when you need to dose maybe eight people total."
    
#     headmaster "Eight people won't change the entire school."
    
#     secretary "The teachers set classroom standards. The PTA mothers influence other parents."
#     secretary "That's not eight random people. That's everyone who actually matters for culture."
    
#     # IMAGE: Headmaster sitting up straighter
#     # Looking at the vials and catalyst with new perspective
#     # Secretary watching him arrive at the obvious conclusion
    
#     headmaster "You're saying I have enough."
    
#     secretary "I'm saying you have more than enough if you stop thinking about dosing students directly."
    
#     # IMAGE: Headmaster pulling over his notebook
#     # Starting to make notes
#     # Energy shifting from paralyzed to practical
    
#     headmaster "The five teachers. If they stop enforcing dress codes, relationship policies..."
    
#     secretary "Students notice immediately. They push boundaries, test limits."
    
#     headmaster "And the PTA mothers. If they stop objecting to relaxed standards..."
    
#     secretary "Other parents follow their lead. The institutional pressure disappears."
    
#     # IMAGE: Headmaster writing names
#     # Parker, Chen, Rodriguez, Thompson, Martinez
#     # The three PTA mothers
#     # Simple target list
    
#     headmaster "How do I dose them without being obvious?"
    
#     # IMAGE: Secretary considering
#     # Casual posture, matter-of-fact tone
    
#     secretary "The faculty lounge has coffee every morning. Everyone drinks from the same pot."
    
#     headmaster "Consistent small doses over several days."
    
#     secretary "Less noticeable than sudden changes. Looks like natural attitude shifts."
    
#     # IMAGE: Headmaster making more notes
#     # Distribution schedule, timing
#     # Secretary continuing
    
#     secretary "For the PTA mothers, there's a meeting next Wednesday. I handle refreshments."
    
#     headmaster "You'd help with that?"
    
#     # IMAGE: Secretary's direct look
#     # Simple, matter-of-fact
#     # No grand declarations
    
#     secretary "It's practical. I'm already setting up the refreshments anyway."
    
#     secretary_thought "*He still doesn't know about the students' project. Better to keep those tracks separate.*"
    
#     # IMAGE: Both at desk
#     # Notes spread between them
#     # TCE bottle and vials now manageable instead of impossible
    
#     headmaster "Faculty lounge starting tomorrow. Small doses in the coffee."
#     headmaster "PTA meeting Wednesday. Refreshments for the three mothers."
    
#     secretary "I'll make sure the faculty pot stays full. Monitor who drinks."
    
#     headmaster "And I'll prepare individual doses. Precise measurements."
    
#     # IMAGE: Secretary standing, picking up folder
#     # Professional demeanor
#     # Headmaster organizing his materials
    
#     secretary "This also buys time for the longer-term problem."
    
#     headmaster "The synthesis equipment. Proper lab space."
    
#     secretary "While you're handling this, I'll look into funding for the old lab building renovation."
#     secretary "Better equipment means more efficient production. Maybe alternative catalysts."
    
#     # IMAGE: Headmaster nodding
#     # Both short-term and long-term clear now
#     # No longer overwhelmed
    
#     headmaster "Use what I have on the people who matter. Build better capacity in parallel."
    
#     secretary "Exactly."
    
#     # IMAGE: Secretary at door
#     # Looking back briefly
#     # Headmaster already measuring out materials
    
#     secretary "You were overthinking it."
    
#     headmaster "Apparently."
    
#     secretary "It's a small school. Eight people. You have enough."
    
#     # IMAGE: Door closing, secretary gone
#     # Headmaster alone but refocused
#     # Office messy but purposeful now
#     # Target list simple and clear
    
#     headmaster_thought "Eight people. The five teachers, the three PTA mothers."
#     headmaster_thought "I was so focused on scarcity I forgot how small this operation actually is."
    
#     # IMAGE: Headmaster picking up potion vial
#     # Looking at it practically now
#     # TCE bottle beside it - limited but sufficient
    
#     headmaster "Teachers first. Then the mothers. That's all I need."
    
#     headmaster_thought "Emiko's right. I was overthinking it."
    
#     $ set_progress("lab_intro", 13)
    
#     $ end_event("new_daytime", **kwargs)

# # Morning Brew, unlocks after Strategic Planning and Brewing Session on Thursday
# label lab_intro_14 (**kwargs):
#     $ begin_event(**kwargs)
    
#     # IMAGE: Headmaster's office, very early morning
#     # Still dark outside, desk lamp only light
#     # Small vials arranged on desk with scientific precision
#     # Headmaster in careful concentration mode
#     # TCE bottle and base potion beside calibrated dropper
    
#     headmaster_thought "Five teachers. Need to calculate the concentration for the full urn."
    
#     # IMAGE: Headmaster measuring enhanced potion into small bottle
#     # Using dropper to add TCE catalyst
#     # Amber liquid glowing slightly when catalyst mixes
#     # His hands steady despite nerves
    
#     headmaster "Three drops base potion per serving. Twenty cup capacity..."
#     headmaster "Sixty drops total, plus catalyst at one-to-five ratio."
    
#     # IMAGE: Close-up of enhanced mixture in small dark bottle
#     # Richer amber color than base potion alone
#     # Faint sweet scent rising
#     # Headmaster sealing it carefully
    
#     headmaster_thought "This has to look natural. Just another morning."
    
#     # IMAGE: Headmaster pocketing the bottle
#     # Checking watch - 6:15 AM
#     # Gathering papers to use as cover
#     # Office door closing behind him
    
#     # IMAGE: School hallway, pre-dawn darkness
#     # Emergency lighting only, everything quiet
#     # Headmaster's footsteps echoing
#     # Walking toward faculty lounge with purpose
    
#     headmaster_thought "Staff don't usually arrive until seven. I have time."
    
#     # IMAGE: Faculty lounge door, headmaster entering
#     # Dark room, flipping light switch
#     # Fluorescent lights flickering on
#     # Empty space, coffee station visible on counter
    
#     # IMAGE: Coffee station setup
#     # Large institutional urn, 20-cup capacity
#     # Filters, coffee grounds in canister
#     # Headmaster moving to it with practiced casualness
    
#     headmaster_thought "Act normal. Just making coffee early. Nothing unusual."
    
#     # IMAGE: Headmaster filling urn with water
#     # Measuring coffee grounds
#     # Normal morning routine
#     # The small bottle still in his pocket
    
#     # IMAGE: Coffee beginning to brew
#     # Familiar percolating sound
#     # Rich coffee scent filling the room
#     # Headmaster waiting, checking watch nervously
    
#     headmaster_thought "Wait until it's finished brewing. The heat helps the compound distribute evenly."
    
#     # IMAGE: Headmaster at window, watching darkness fade
#     # Coffee urn bubbling in background
#     # Dawn light beginning to touch the sky
#     # His reflection tense in the glass
    
#     # IMAGE: Coffee urn finishing with final hiss
#     # Full pot of dark coffee
#     # Headmaster turning, moving back to it
#     # Pulling the small bottle from his pocket
    
#     headmaster_thought "Now. Before anyone arrives."
    
#     # IMAGE: Headmaster opening urn lid
#     # Steam rising, rich coffee aroma
#     # Pulling dropper from bottle
#     # Hand steady, professional precision
    
#     # IMAGE: Adding enhanced potion to coffee
#     # Amber drops falling into dark liquid
#     # Disappearing immediately, no color change visible
#     # Headmaster counting silently
    
#     headmaster_thought "Sixty drops. Precisely sixty."
    
#     # IMAGE: Stirring coffee with long spoon
#     # Mixing thoroughly
#     # The scent shifting subtly - coffee with something underneath
#     # Sweet, almost floral, barely noticeable
    
#     headmaster "There."
    
#     # IMAGE: Headmaster closing urn, replacing lid
#     # Pocketing the bottle and dropper
#     # Stepping back, examining his work
#     # Everything looks completely normal
    
#     headmaster_thought "No one will notice. Just coffee. Same as every morning."
    
#     # IMAGE: Headmaster arranging himself at nearby table
#     # Papers spread out like he's been here working
#     # Coffee mug for himself from separate personal thermos
#     # Relaxed posture, casual morning routine
    
#     # IMAGE: Clock on wall showing 6:47 AM
#     # Headmaster pretending to read through papers
#     # Pen in hand, making occasional marks
#     # Ears alert for approaching footsteps
    
#     # IMAGE: Door opening, first teacher arriving
#     # Zoe Parker, early as always
#     # Carrying bag and travel mug
#     # Headmaster looking up casually
    
#     headmaster "Morning, Zoe."
    
#     parker "Oh! You're here early."
    
#     # IMAGE: Parker moving to coffee station
#     # Blonde hair pulled back, professional attire
#     # Setting down her things
#     # Reaching for the urn
    
#     headmaster "Couldn't sleep. Figured I'd get some work done."
#     headmaster "Made coffee if you want some."
    
#     parker "You're a lifesaver."
    
#     # IMAGE: Parker pouring coffee into her mug
#     # Steam rising, dark liquid filling cup
#     # Headmaster watching peripherally, trying not to stare
#     # Her adding cream and sugar
    
#     parker "Smells good. Different somehow?"
    
#     # IMAGE: Headmaster's internal tension
#     # Maintaining casual expression
#     # Parker lifting mug to smell
    
#     headmaster "Same brand as always. Maybe fresher grounds?"
    
#     parker "Maybe."
    
#     # IMAGE: Parker taking first sip
#     # Headmaster holding his breath
#     # Her expression normal, satisfied
#     # Moving to sit at table with morning paper
    
#     parker "Mm. That hits the spot."
    
#     headmaster_thought "She doesn't notice anything unusual. Good."
    
#     # IMAGE: Door opening again, Yulan Chen arriving
#     # Black hair with blue ornamental piece
#     # Greeting Parker and headmaster
#     # Heading straight for coffee
    
#     chen "Morning. Oh good, coffee's ready."
    
#     # IMAGE: Chen pouring herself a large mug
#     # Adding just a splash of milk
#     # Drinking immediately despite the heat
    
#     chen "Ah. Needed this."
    
#     # IMAGE: Time passing - 7:05 AM
#     # Lily Anderson arriving
#     # Auburn wavy hair, professional but warm demeanor
#     # Followed shortly by Chloe Garcia
    
#     anderson "Is there any— oh perfect, thanks for making it."
    
#     garcia "You're here early today."
    
#     headmaster "Early meeting prep. Help yourselves."
    
#     # IMAGE: Both Anderson and Garcia at coffee station
#     # Pouring cups, adding their preferences
#     # Garcia with extensive tattoos visible on arms
#     # Anderson adjusting her hair while waiting
    
#     # IMAGE: All four teachers now in lounge
#     # Each with coffee from the urn
#     # Scattered at different tables, morning routines
#     # Parker reading paper, Chen checking phone, Anderson organizing materials
    
#     # IMAGE: Finola Ryan arriving last, 7:15 AM
#     # Red bob haircut, freckles visible
#     # Rushing in slightly flustered
#     # Immediately going for coffee
    
#     ryan "Sorry, overslept. Is there still—"
    
#     chen "Plenty left."
    
#     # IMAGE: Ryan pouring herself a cup
#     # Adding sugar, stirring
#     # All five teachers now present, all consuming the dosed coffee
#     # Headmaster's papers in front of him, pen moving but eyes tracking peripherally
    
#     headmaster_thought "All five. Every one of them drinking it."
    
#     # IMAGE: Faculty lounge in normal morning rhythm
#     # Coffee scent dominant but with that subtle sweet undertone
#     # Teachers talking about upcoming day, classes, students
#     # Headmaster appearing absorbed in his work
    
#     parker "Did anyone prep for the staff meeting Friday?"
    
#     chen "Not yet. What's on the agenda?"
    
#     anderson "Budget review, I think. And student discipline updates."
    
#     # IMAGE: Teachers refilling cups
#     # Parker getting second serving
#     # Chen topping off his mug
#     # The urn slowly emptying as morning progresses
    
#     headmaster_thought "They're drinking it naturally. No suspicion, no hesitation."
    
#     # IMAGE: Time showing 7:35 AM
#     # Teachers starting to show subtle changes
#     # Anderson standing, stretching
#     # Arms overhead, back arching
#     # Her blouse riding up, exposing bare midriff
    
#     anderson "God, I'm stiff this morning."

#     # IMAGE: Parker with red tracksuit jacket completely removed
#     # Draped over back of chair
#     # Sitting in just the yellow athletic swimsuit top and red tracksuit pants
#     # Form-fitting sleeveless top, bare shoulders and arms
#     # Blonde hair catching morning light
#     # Completely comfortable in minimal upper body coverage
#     # Legs crossed casually, relaxed posture
    
#     parker "This coffee hit different today. Feel really relaxed."
    
#     chen "Mm. Same actually."
    
#     # IMAGE: Chen and Ryan sitting close at same table
#     # Shoulders touching, comfortable proximity
#     # Chen's hand resting near Ryan's on the table
#     # Neither pulling away, natural intimacy
#     # Headmaster observing the casual physical closeness
    
#     ryan "Did you finish grading those essays?"
    
#     chen "Most of them. Want to compare notes during lunch?"
    
#     ryan "Sure, sounds good."
    
#     # IMAGE: Garcia adjusting her shirt
#     # Fabric clinging, outline visible
#     # Extensive tattoos on both arms fully visible
#     # She doesn't seem to notice or care about the exposure
#     # Everyone relaxed, guards slightly lowered
    
#     garcia "Is it warm in here or just me?"
    
#     anderson "Little warm, yeah."

#     # IMAGE: Finola setting her cup down abruptly
#     # Expression shifted — not just warm, something more urgent
#     # Hand pressed briefly to sternum, like checking her own heartbeat
    
#     ryan "Excuse me a second."
    
#     # IMAGE: Finola moving toward door
#     # Faster than casual, not quite a rush but close
#     # Other teachers barely register it, absorbed in conversation
    
#     headmaster_thought "That was off. Wrong tone entirely."
#     headmaster_thought "Too quick. Too sharp. If she's having an adverse reaction—"
    
#     # IMAGE: Headmaster setting down his papers
#     # Standing, moving toward door
#     # Keeping it casual, just stretching his legs apparently
    
#     # IMAGE: Hallway outside faculty lounge
#     # Empty, morning quiet
#     # Staff changing room door at the far end, sitting ajar
    
#     headmaster_thought "She wouldn't go to the bathroom. The changing room has lockers."
    
#     # IMAGE: Headmaster approaching the changing room door
#     # Crack of light visible through the gap
#     # Sound of movement inside — fabric, a soft exhale
    
#     headmaster "Ms. Ryan? Are you—"
    
#     # IMAGE: His hand pushing the door slightly open
#     # View through the gap: Finola at her locker
#     # Shirt already off, bare back to him
#     # Hands reaching behind her — bra clasp
    
#     headmaster_thought "Oh—"
    
#     # IMAGE: Finola turning at the sound of his voice
#     # Topless, one arm crossing her chest instinctively
#     # But the reaction is slow — a full beat late, like she had to remind herself to cover
#     # Her face: flushed, disoriented, not the sharp horror it should be
    
#     headmaster "I'm so sorry—I thought—I'll go—"
    
#     finola "I just—it was too tight. The shirt."
#     finola "I don't know why I—sorry, give me a minute."
    
#     # IMAGE: Headmaster pulling door shut
#     # Standing in hallway, processing
#     # The changing room quiet behind him
    
#     headmaster_thought "She stripped her top because the fabric felt restrictive. Same behavioral signature as Sakura in the courtyard."
#     headmaster_thought "But Sakura snapped back within minutes. Finola walked here deliberately. Found her locker. That's... more organized. More sustained."
#     headmaster_thought "And when I walked in—one second before she covered herself. One full second."
#     headmaster_thought "Normal Finola would've had something heavy airborne by now."
#     headmaster_thought "The formula is working. Faster than I expected."
    
#     # IMAGE: Finola emerging from changing room
#     # Different top now — athletic, fitted, more revealing than her usual work attire
#     # Expression back to professional, slightly embarrassed
#     # Not meeting his eyes
    
#     finola "Sorry about that. Don't know what came over me."
    
#     headmaster "No harm done. Feeling better?"
    
#     finola "Yeah. Much."
    
#     # IMAGE: Finola heading back toward the faculty lounge
#     # Headmaster watching her go
#     # The fitted top sitting very differently than her usual layers
#     # His expression: analytical satisfaction
    
#     headmaster_thought "Much better."

#     # Image: Headmaster walks back to the office

#     # IMAGE: Anderson checking time
#     # First period approaching
#     # Teachers beginning to gather their things
    
#     anderson "I should get to my classroom. First period starts in twenty."
    
#     garcia "Same. Thanks for the coffee."
    
#     # IMAGE: Teachers filing out one by one
#     # Each carrying their mug
#     # Some still half-full, taking it with them
#     # Headmaster remaining, watching them leave
    
#     parker "See you at lunch."
    
#     chen "Have a good morning."
    
#     # IMAGE: Headmaster alone in faculty lounge
#     # Nearly empty coffee urn
#     # His papers still spread but untouched
#     # Releasing held tension
    
#     headmaster_thought "Done. They all drank it. Every single one."
    
#     # IMAGE: Headmaster standing, moving to coffee urn
#     # Checking how much remains
#     # Maybe two cups worth left
#     # Pouring it out into sink
    
#     headmaster "Can't leave evidence."
    
#     # IMAGE: Headmaster rinsing urn
#     # Cleaning up
#     # Everything returning to normal state
#     # No trace of what happened
    
#     headmaster_thought "Now I wait. See if the effects manifest over the coming days."
#     headmaster_thought "Small doses. Consistent application. Cultural shift from the top."
    
#     # IMAGE: Headmaster gathering his papers
#     # Pocketing the small bottle
#     # Faculty lounge empty and clean
#     # Morning light fully illuminating the space now
    
#     headmaster_thought "The teachers are dosed. Next, the PTA mothers."
    
#     $ set_progress("lab_intro_faculty", 1)
    
#     $ end_event("new_daytime", **kwargs)

# # PTA Refreshments - Friday morning after Morning Brew
# label lab_intro_15 (**kwargs):
#     $ begin_event(**kwargs)
    
#     $ adelaide = get_person_char_with_key("parents", "adelaide_hall")
#     $ nubia = get_person_char_with_key("parents", "nubia_davis")
#     $ yuki = get_person_char_with_key("parents", "yuki_yamamoto")
#     $ yuriko = get_person_char_with_key("students", "yuriko_oshima")
    
#     $ parker = get_person_char_with_key("staff", "zoe_parker")
#     $ chen = get_person_char_with_key("staff", "yulan_chen")
#     $ anderson = get_person_char_with_key("staff", "lily_anderson")
#     $ garcia = get_person_char_with_key("staff", "chloe_garcia")
#     $ ryan = get_person_char_with_key("staff", "finola_ryan")
    
#     # IMAGE: Conference room, afternoon
#     # Large table with chairs arranged around it
#     # Headmaster setting up at head of table
#     # Pitcher of lemonade, plate of cookies on side table
#     # Afternoon sunlight through windows
    
#     headmaster_thought "PTA meeting in twenty minutes. The mothers usually arrive early."
    
#     # IMAGE: Headmaster at side table
#     # Small dark bottle in hand, hidden from view
#     # Pouring enhanced potion into lemonade pitcher
#     # Stirring carefully with long spoon
#     # Scent of lemon with subtle sweet undertone
    
#     headmaster_thought "Same ratio as the faculty coffee. Three mothers, five teachers, one student rep."
#     headmaster_thought "But the student won't drink. She never does at these meetings."
    
#     # IMAGE: Close-up of lemonade pitcher
#     # Clear yellow liquid, ice cubes floating
#     # No visible trace of the enhancement
#     # Condensation forming on glass surface
    
#     headmaster "Perfect."
    
#     # IMAGE: Headmaster arranging cups beside pitcher
#     # Setting out napkins, cookies on plate
#     # Everything looking professional, welcoming
#     # Pocketing the small bottle
    
#     # IMAGE: Door opening, three women entering
#     # Adelaide Hall leading - black hair, maroon form-fitting dress
#     # Nubia Davis behind her - white/silver hair, red cropped top and jeans
#     # Yuki Yamamoto following - black hair, black crop top and pants
#     # All carrying bags, talking amongst themselves
    
#     adelaide "Oh, we're early. Good."
    
#     headmaster "Mrs. Hall, Mrs. Davis, Mrs. Yamamoto. Right on time, actually."
    
#     # IMAGE: Three mothers settling around table
#     # Adelaide choosing seat near head of table
#     # Nubia and Yuki sitting together on opposite side
#     # Setting bags down, getting comfortable
    
#     nubia "The teachers aren't here yet?"
    
#     headmaster "They'll arrive at four. I appreciate you three coming early."
#     headmaster "I have some refreshments if you'd like. Lemonade and cookies."
    
#     # IMAGE: Headmaster gesturing to side table
#     # Pitcher glistening with condensation
#     # Mothers looking interested
#     # Yuki standing immediately
    
#     yuki "That sounds perfect. It's warm today."
    
#     adelaide "I'll take some. Thank you."
    
#     # IMAGE: Headmaster pouring lemonade into cups
#     # Handing first to Adelaide
#     # Then Nubia, then Yuki
#     # Each taking their cup with thanks
    
#     headmaster "Help yourselves to cookies as well."
    
#     # IMAGE: Three mothers with lemonade
#     # Adelaide taking first sip, nodding approval
#     # Nubia drinking deeper, appreciative
#     # Yuki holding hers, ice clinking softly
    
#     adelaide "This is good. Tart but not too sweet."
    
#     nubia "Mm. Refreshing."
    
#     # IMAGE: Mothers settling back into seats
#     # Adelaide crossing legs, leaning back slightly
#     # Nubia and Yuki talking quietly, sipping their drinks
#     # Headmaster taking seat at head of table with his own cup (from personal bottle)
    
#     headmaster "How have your daughters been doing this semester?"
    
#     # IMAGE: Adelaide setting her cup down
#     # Considering the question
#     # Nubia refilling her cup already, drinking more
    
#     adelaide "Mine's doing well. Busy, but her grades are solid."
    
#     yuki "Soyoon's been happy. More social than usual."
    
#     nubia "Same here. She seems more comfortable lately."
    
#     # IMAGE: Time showing 3:55 PM
#     # Mothers finishing their first cups
#     # Yuki getting up to refill
#     # Adelaide leaning forward, elbows on table, more relaxed posture
    
#     yuki "Anyone else want more?"
    
#     adelaide "Sure, I'll take another."
    
#     # IMAGE: Yuki refilling Adelaide's cup, then her own
#     # Nubia already on her second cup
#     # All three drinking the enhanced lemonade
#     # Conversation flowing easily
    
#     # IMAGE: Door opening, teachers arriving
#     # Parker, Chen, Anderson, Garcia, Ryan entering together
#     # Followed by Yuriko Oshima - dark wavy hair, white semi-transparent blouse showing red bra underneath, plaid skirt, red scarf
#     # Teachers greeting the mothers, taking seats
    
#     parker "Sorry if we're late."
    
#     headmaster "Right on time. We're just getting started."
    
#     # IMAGE: Teachers settling around table
#     # Yuriko taking seat across from the mothers
#     # Looking professional despite her revealing blouse
#     # Teachers noticing the refreshments
    
#     chen "Is there lemonade?"
    
#     headmaster "Help yourselves."
    
#     # IMAGE: Teachers getting drinks
#     # Parker and Chen pouring cups (undosed - this is fresh from fridge)
#     # Anderson and Garcia taking cookies
#     # Yuriko declining with small head shake
    
#     yuriko "I'm fine, thank you."
    
#     # IMAGE: Full table now
#     # Headmaster at head
#     # Three mothers on one side (Adelaide, Nubia, Yuki) - noticeably more relaxed
#     # Five teachers scattered around (Parker, Chen, Anderson, Garcia, Ryan)
#     # Yuriko across from mothers, student rep position
#     # Official meeting beginning
    
#     headmaster "Thank you all for coming. We have several items to discuss today."
#     headmaster "First, the budget review for next semester."
    
#     # IMAGE: Headmaster going through budget documents
#     # Normal discussion, everyone engaged
#     # Mothers occasionally sipping their lemonade
#     # Time passing, effects building
    
#     # IMAGE: Twenty minutes into meeting
#     # Adelaide with arm draped over back of her chair
#     # Maroon dress fabric clinging, showing her curves
#     # She's smiling more, contributing but not nitpicking
    
#     headmaster "The proposed allocation increases facility maintenance by eight percent."
    
#     adelaide "That seems reasonable. The building does need upkeep."
    
#     # IMAGE: Headmaster continuing through agenda
#     # Mothers listening, relaxed posture
#     # Nubia's bare midriff visible as she leans back
#     # Yuki's legs stretched out under table
    
#     headmaster "Next item—the spring fundraiser. The proposal is for a parent-student social event."
    
#     # IMAGE: Nubia leaning forward
#     # Red crop top, midriff bare, completely comfortable
#     # Nodding along
    
#     nubia "That sounds fun. The kids would enjoy that."
    
#     yuki "Agreed. When's it scheduled?"
    
#     headmaster "Third Saturday in May. Does that work for everyone?"
    
#     # IMAGE: Adelaide nodding casually
#     # Normally she'd be asking about budgets, supervision, liability
#     # Today just... agreeing
    
#     adelaide "Fine with me."
    
#     # IMAGE: Teachers watching mothers
#     # Parker and Chen exchanged glances
#     # Noticing how smoothly this is going
    
#     anderson "The teachers can help organize. We're happy to support it."
    
#     ryan "Absolutely."
    
#     # IMAGE: Yuriko watching the adults from across table
#     # Slightly surprised by how easily everyone's agreeing
#     # Taking notes dutifully as student rep
    
#     yuriko_thought "*Usually Mrs. Hall has a list of questions. Today everyone's just... nodding.*"
    
#     # IMAGE: Headmaster moving through agenda
#     # Cafeteria menu updates, parent-teacher conference scheduling
#     # Everything passing with unanimous approval
#     # No debate, no questioning
    
#     headmaster "The cafeteria wants to add a salad bar option. Slight cost increase."
    
#     yuki "Healthier options? Sounds good."
    
#     adelaide "I support that."
    
#     nubia "Makes sense to me."
    
#     # IMAGE: Meeting continuing smoothly
#     # Parent-teacher conference dates set
#     # Field trip permissions discussed
#     # Every item passing without debate
    
#     headmaster "That brings us to the final item—uniform policy clarification for warm weather."
    
#     adelaide "Oh, I think the current policy is fine. Students need flexibility."
    
#     # IMAGE: Meeting wrapping up
#     # Final agenda items covered
#     # Mothers getting more comfortable as time passes
#     # Adelaide with arms spread on chair backs, open posture
    
#     headmaster "Unless there's anything else to discuss, I think we're done."
    
#     adelaide "No, I think that covered everything. Very efficient."
    
#     # IMAGE: Everyone standing, gathering materials
#     # Mothers chatting with teachers casually
#     # More physical proximity than usual
    
#     adelaide "That was refreshing. Usually these run so long."
    
#     parker "Quick and productive. I appreciate that."
#     # IMAGE: Adelaide moving toward Chloe Garcia
#     # The usual social distance of a PTA meeting — nonexistent
#     # She's close, too close, looking at Garcia's forearm
    
#     adelaide "Are these new? I never noticed how detailed they are."
    
#     # IMAGE: Adelaide's fingers reaching out
#     # Touching Garcia's tattoo sleeve without asking
#     # Tracing the line of a floral design up toward the elbow
#     # Garcia going still — not uncomfortable, just surprised
    
#     garcia "Had most of them since before I started here."
    
#     adelaide "They're beautiful. This one especially."
    
#     # IMAGE: Adelaide's thumb pressing slightly into the ink
#     # The touch too slow, too interested for a school hallway conversation
#     # Garcia looking at Adelaide's face, recalibrating something
    
#     garcia_thought "*She's never once looked at my arms before. Three years and she always looked just past them.*"
    
#     # IMAGE: Yuriko nearby, notebook in hand
#     # Watching Adelaide and Garcia
#     # Trying to identify what feels wrong about the image
#     # Can't place it, notes it anyway
    
#     yuriko_thought "*Mrs. Hall is touching Ms. Garcia's arm. That's... fine. People do that.*"
#     yuriko_thought "*Why does it feel like I'm watching something I shouldn't be?*"
    
#     # IMAGE: Headmaster observing from across the room
#     # Cup in hand, expression neutral
#     # Eyes tracking Adelaide's fingers on Garcia's tattoo
    
#     headmaster_thought "Adelaide Hall. The first one to drain her cup, the first one to refill."
#     headmaster_thought "She arrived wound tight as a mainspring and now she's touching the art teacher's arm like they're old friends."
#     headmaster_thought "The dosing is holding. More than holding."

#     headmaster "Okay, that's enough for today. I wish you all a nice weekend."

#     $ set_progress("lab_intro_parents", 1)
    
#     $ end_event("new_daytime", **kwargs)
# # The Discovery unlocks after Chemical Mishap
# label lab_intro_16 (**kwargs):
#     $ begin_event(**kwargs)

#     $ luna = get_person_char_with_key("class_3a", "luna_clark")
#     $ ishimaru = get_person_char_with_key("class_3a", "ishimaru_maki")
#     $ lin = get_person_char_with_key("class_3a", "lin_kato")

#     # IMAGE: Exterior of abandoned lab building, overgrown, late afternoon light
#     # Three students approaching through the rusted gate
#     # Ishimaru leading, Lin slightly behind, Luna observing everything

#     subtitles "Meanwhile at the old abandoned lab building."

#     ishimaru "I can't believe they just left this place. Look at the size of it!"

#     luna "The equipment alone is worth thousands. Even secondhand."

#     lin "We're going to get in trouble."

#     ishimaru "We're already inside."

#     lin "...Fair."

#     # IMAGE: Interior hallway, dusty and dim
#     # Broken windows letting in shafts of light, cobwebs in corners
#     # Students walking single file through debris, Ishimaru first

#     # The interior smells like old paper and something chemical underneath — 
#     # faint, decades-stale, but still there. Footsteps echo on cracked linoleum.
#     # Old posters curl from the walls, their text faded to ghostly impressions.

#     ishimaru "Okay this is actually kind of creepy."

#     luna "Chemistry building. Pre-new-science-wing. Probably shut down mid-nineties."

#     lin "Please don't touch anything."

#     luna "I'm not touching anything."

#     lin "You're touching that beaker."

#     luna "I'm evaluating the beaker."

#     # IMAGE: Old classroom/lab space
#     # Dusty beakers and test tubes on shelves, ancient periodic table on wall
#     # Ishimaru holding a flask up to the light, Luna examining labels, Lin hanging back

#     # They spread out without deciding to. Glassware sits abandoned on every surface,
#     # a thin film of dust coating everything like ash.

#     ishimaru "Think any of this still works? These look ancient."

#     luna "Glassware, probably. Chemicals, no. Anything mechanical, unlikely."

#     lin "You sound like you're already planning to use it."

#     luna "I'm not planning anything yet."

#     # IMAGE: Lin drifting toward the back of the room
#     # Metal bookshelf leaning against the far wall, half in shadow
#     # Something catching her eye — a flash of color in the gap between shelf and brick

#     lin "Wait."

#     ishimaru "What?"

#     lin "There's something jammed back here."

#     # IMAGE: Close-up of Lin's hands pulling out a leather-bound notebook
#     # Worn cover, no title, pages clearly handwritten
#     # Surprisingly clean compared to everything else in the room

#     # The notebook comes free with a soft scrape.
#     # Lin holds it at arm's length for a second, like it might do something.

#     luna "Let me see."

#     ishimaru "What is it?!"

#     lin "A notebook. Hidden behind the shelf."

#     # IMAGE: Three students gathered around the open notebook
#     # Lin holding it, Ishimaru leaning over one shoulder, Luna over the other
#     # Pages covered in tight, precise handwriting — formulas, diagrams, margin notes

#     # Chemical formulas sprawl across diagrams in dark ink.
#     # Notes crowd the margins in a different hand: 'behavioral compounds,'
#     # 'dose-response curves,' 'inhibition reduction.'

#     ishimaru "Whoa. Is this someone's actual research?"

#     luna "Not student work. Look at the notation. Whoever wrote this knew exactly what they were doing."

#     lin "What's all this other stuff though. 'Subject responses.' 'Catalytic amplification.' That's not a chemistry class."

#     # IMAGE: Close-up of specific notebook page
#     # Formula visible, margin note: "requires catalyst for permanence"
#     # Another note: "psychological effects observed within 15 minutes"

#     lin "'Experimental compound — psychological effects observed within fifteen minutes.'"

#     ishimaru "Psychological effects?! Like what?!"

#     luna "It doesn't say. That's intentional — someone ran tests, documented outcomes, kept the methodology separate from the results. That's a research protocol. A real one."

#     ishimaru "That is genuinely insane."

#     lin "Okay can we please not be figuring out that someone was secretly dosing people in our school building."

#     ishimaru "We are literally figuring out that someone was secretly dosing people in our school building."

#     lin "I know. That's why I said please."

#     # IMAGE: Students' faces — Ishimaru excited, Lin unsettled, Luna thinking

#     luna "It's from before they shut this building down. Some old teacher, most likely."

#     ishimaru "But why hide it?"

#     luna "That's the interesting question."

#     lin "Because they did something they weren't supposed to and needed to make it disappear?"

#     luna "Better answer than I expected."

#     lin "Thanks. I think."

#     # A beat. All three looking at the notebook, then at each other.

#     luna "We need to actually understand what this is. Not guess — understand."

#     lin "How? This is way over our heads."

#     luna "Bring textbooks tomorrow. Cross-reference the formulas. Work through it properly."

#     ishimaru "Yes. Same time, and we don't tell anyone—"

#     lin "We're not telling anyone about this."

#     ishimaru "Obviously."

#     lin "I just needed to say it out loud."

#     # IMAGE: Students leaving the building
#     # Notebook tucked under Lin's arm, held close
#     # Afternoon sun lower now, long shadows across the overgrown path
#     # Ishimaru practically bouncing, Luna already composing something in her head
#     # Lin telling herself she just wants to understand it. That's all.

#     # They leave the way they came.
#     # The abandoned building settles back into silence behind them,
#     # dust already covering their footprints.

#     $ set_progress("lab_intro_discovery", 1)

#     $ end_event("new_daytime", **kwargs)


# # Secretary's Spin unlocks after The Discovery
# label lab_intro_17 (**kwargs):
#     $ begin_event(**kwargs)

#     $ luna = get_person_char_with_key("class_3a", "luna_clark")
#     $ ishimaru = get_person_char_with_key("class_3a", "ishimaru_maki")
#     $ lin = get_person_char_with_key("class_3a", "lin_kato")

#     # IMAGE: Interior of abandoned lab, same room as previous event
#     # Afternoon light through dusty windows
#     # All three gathered around the old lab table, notebook open between them
#     # Lin has a chemistry textbook open beside it, cross-referencing

#     luna "'Dosage control' maps to compound quantity per subject. 'Subject compliance' is the one that doesn't fit medical usage."

#     ishimaru "What do you mean?"

#     luna "In a research context, compliance implies the subjects weren't necessarily informed participants."

#     lin "Can we please not figure out that someone was running non-consensual experiments in our school."

#     ishimaru "We might literally be figuring out—"

#     lin "I know! I said please!"

#     luna "We don't have enough data to conclude that yet."

#     lin "The phrase 'subject compliance' is doing a lot of work in that sentence, Luna."

#     luna "...Fair."

#     # IMAGE: Doorway of the lab room
#     # Secretary's silhouette in the frame, backlit by hallway light
#     # Students haven't noticed her yet, still bent over the notebook

#     secretary_thought "*Perfect. That removes some work from me.*"

#     # IMAGE: Secretary stepping into the room
#     # Hand to chest, exaggerated surprise, warm smile
#     # Students looking up startled — Lin reflexively sliding the notebook 
#     # closer to herself

#     secretary "Oh my! I didn't expect to find anyone here."

#     ishimaru "Ms. [secretary_last_name]! We were just—"

#     lin "We weren't doing anything bad—"

#     luna "We found a research notebook hidden in the lab and we've been cross-referencing the methodology against our chemistry textbooks."

#     lin "...Or that. She said that."

#     secretary "Relax, I'm not going to report you for curiosity."

#     # IMAGE: Secretary moving closer, genuine-looking interest on her face
#     # Lin still protective of the notebook, hand resting on the cover

#     secretary "What did you find?"

#     ishimaru "A notebook. Hidden behind that shelf at the back."

#     lin "We think it might be from the old chemistry teacher. Before they shut this place down."

#     secretary "How intriguing! May I see?"

#     # IMAGE: Students exchanging glances
#     # Lin hesitating, then slowly sliding the notebook toward secretary
#     # Secretary reaching for it with careful, respectful hands

#     lin "Sure. We can't quite figure out what it's actually about."

#     # IMAGE: Secretary holding the notebook, reading
#     # Students watching her face for reaction
#     # Her expression shifting from curious to delighted — calculated performance

#     secretary_thought "*Behavioral compounds. Inhibition reduction. This is more detailed than I expected.*"
#     secretary_thought "*His work. How on earth did they find it.*"
#     secretary_thought "*I can use this.*"

#     # IMAGE: Secretary's face — warm, slightly mischievous smile

#     secretary "Oh, how sweet!"

#     ishimaru "What? What is it?"

#     secretary "This looks like a love potion recipe."

#     # IMAGE: Students' reactions
#     # Ishimaru's eyebrows shooting up, Lin looking skeptical
#     # Luna tilting her head slightly, recalibrating

#     ishimaru "Wait — seriously?!"

#     lin "That's not a real thing."

#     luna "She didn't say magic."

#     secretary "Exactly. Not magic — chemistry. Mood, perception, emotional receptivity. It's a chemical way of making people more... open to connection."

#     secretary "'Social bonding enhancement.' 'Inhibition reduction.' Whoever wrote this was quite the romantic."

#     # IMAGE: Secretary showing specific passages
#     # Finger deliberately highlighting the softer-sounding notes
#     # Carefully avoiding the clinical terms

#     luna "So it's pharmacology."

#     secretary "In the most charming possible application, yes."

#     ishimaru "Could we actually make it? Like, for real?"

#     lin "We are not making it."

#     ishimaru "I wasn't asking you."

#     # IMAGE: Secretary considering, tapping her chin — calculated pause

#     secretary "It would be quite advanced. But... educational. Chemistry in action. Practical application of theory."

#     luna "More rigorous than anything we do in actual class."

#     lin "You've already decided we're doing this."

#     luna "About two minutes ago."

#     lin "..."

#     secretary "I could help you gather what you need. I have access to the storage rooms, and the science department has some discretionary budget. This would be your project — I'd just be a facilitator."

#     ishimaru "Yes! Absolutely!"

#     lin "We'll be careful."

#     luna "I'll document everything properly."

#     lin "Of course you will."

#     # IMAGE: Secretary gesturing around the lab
#     # Students following her gaze, already looking at things differently
#     # Notebook back under Lin's arm

#     secretary "First — inventory what's still functional here. Glassware, heating elements, anything salvageable."

#     secretary "Then I'll see what I can pull from storage to fill the gaps."

#     lin "Thank you, Ms. [secretary_last_name]. This is... actually really cool of you."

#     secretary "Knowledge should be explored, not locked away. Now — let's see what we're working with."

#     # IMAGE: Secretary watching students start moving around the lab
#     # Her expression when they're not looking: satisfied, calculating
#     # Small smile at the corner of her mouth

#     secretary_thought "*They'll do the work. The headmaster handles the adults. This school transforms exactly as planned.*"
#     secretary_thought "*And they'll think it was their idea the whole time.*"

#     $ set_progress("lab_intro_discovery", 2)

#     $ end_event("new_daytime", **kwargs)


# # Gathering Ingredients unlocks after Secretary's Spin
# label lab_intro_18 (**kwargs):
#     $ begin_event(**kwargs)

#     $ luna = get_person_char_with_key("class_3a", "luna_clark")
#     $ ishimaru = get_person_char_with_key("class_3a", "ishimaru_maki")
#     $ lin = get_person_char_with_key("class_3a", "lin_kato")

#     # IMAGE: Abandoned lab interior, late afternoon light
#     # All three searching through cabinets and shelves
#     # Ishimaru on a chair reaching the high cabinets
#     # Lin examining glassware on the counter, checking each piece carefully
#     # Luna working through a lower shelf methodically, already keeping a list

#     ishimaru "Found a whole set of beakers up here! Different sizes!"

#     luna "Check the rims for chips before you add them to the pile. A cracked beaker can shatter under sustained heat."

#     ishimaru "They look fine."

#     luna "Check properly."

#     ishimaru "...They look fine upon closer inspection."

#     # IMAGE: Lin holding a graduated cylinder up to the light
#     # Turning it slowly, checking for damage
#     # Sunlight catching the measurement markings clearly

#     lin "This cylinder's perfect. No cracks, measurements still readable."

#     luna "That's our most important piece for accurate dosing."

#     lin "I still can't believe I just said 'accurate dosing' like it's something I say."

#     # IMAGE: Counter filling up with salvaged equipment
#     # Beakers, test tubes, flasks, stirring rods arranged in a growing pile
#     # Notebook open beside them for reference

#     luna "Glassware is covered. We're missing a heat source and the actual compounds."

#     ishimaru "Yeah, there's no way any chemicals are still here. They would've cleared those out decades ago."

#     # IMAGE: Luna pulling open a deep drawer
#     # Wrinkling her nose at the smell
#     # Reaching in carefully, testing what she finds

#     luna "This drawer smells like something died in it in 1994."

#     luna "But there's rubber tubing in here that might still flex. And glass stirring rods."

#     ishimaru "Glass doesn't expire, right?"

#     luna "Correct. Adding them to the list."

#     lin "You have a list?"

#     luna "I've had a list since yesterday."

#     lin "Of course you have."

#     # IMAGE: All three gathered around the counter
#     # Comparing their finds against the notebook
#     # Lin's finger tracing the equipment column

#     lin "So we have almost everything for glassware. Still missing a heat source and the actual ingredients."

#     ishimaru "Without those we can't do anything."

#     lin "Maybe Ms. [secretary_last_name] would know if the school has—"

#     # IMAGE: Doorway
#     # Secretary's silhouette appearing, carrying a cardboard box
#     # Afternoon light behind her — almost a halo effect
#     # Students turning, surprised

#     secretary "Ask me what?"

#     # IMAGE: Secretary setting the box down on the counter with a soft thunk
#     # Students moving toward it immediately

#     ishimaru "We found almost all the glassware but we're still missing—"

#     secretary "A heat source and the compounds. I figured as much."

#     # IMAGE: Secretary opening the box
#     # Contents visible: portable heating plate, new rubber tubing, clamps,
#     # safety goggles, multiple small bottles of chemicals — some still sealed

#     secretary "Portable heating plate from the old physics department. And the chemistry stockroom still had basic compounds that should cover most of your list."

#     ishimaru "Are you serious right now?!"

#     lin "This is professional grade. How did you even—"

#     secretary "I've been here a long time. You learn where everything's buried."

#     # IMAGE: Luna and Lin going through the chemical bottles
#     # Reading labels carefully, comparing to the notebook
#     # Ishimaru already inspecting the heating plate, turning it over

#     lin "Distilled water, ethanol, potassium hydroxide... this is almost everything."

#     secretary "Almost. You'll need a few organic compounds I couldn't source — nothing dangerous, just specialized. Available online, any chemistry supply shop."

#     luna "We can split the cost."

#     # IMAGE: Secretary pulling safety goggles and gloves from the bottom of the box
#     # Handing them out, expression shifting to something more serious

#     secretary "Chemical work requires proper equipment. Promise me you use these every time."

#     lin "We promise."

#     luna_thought "*She's handing us safety gear for a project she could have shut down in thirty seconds. She actually wants this to work.*"

#     # IMAGE: All four looking at the assembled counter
#     # Full lab setup — salvaged glassware, new equipment, chemicals, notebook
#     # Secretary slightly apart, students grouped together

#     ishimaru "We could actually start brewing soon. Like, really soon."

#     secretary "Once the last compounds arrive, yes. Follow the instructions precisely and you'll be fine."

#     lin "We'll be careful."

#     secretary "I know you will. Let me know when you're ready to brew — I'd like to be there for the first attempt."

#     ishimaru "Definitely. Thank you so much, Ms. [secretary_last_name]."

#     secretary "This is what education should be. Hands-on. Real. Goodnight."

#     # IMAGE: Secretary at the door, looking back briefly
#     # Satisfied, calculating expression once they're not watching
#     # Then she's gone

#     secretary_thought "*The formula is in their hands. The catalyst comes next.*"
#     secretary_thought "*And they'll think they built all of this themselves.*"

#     # IMAGE: Three students alone with the counter full of equipment
#     # Late afternoon light going golden through the dirty windows
#     # The notebook open in the center of it all

#     ishimaru "I can't believe she just gave us all of this."

#     lin "And she wants to be there when we actually brew it."

#     ishimaru "She believes in us."

#     luna "She believes in the project."

#     lin "That is the most Luna thing you have ever said."

#     luna "Thank you."

#     lin "It wasn't a compliment."

#     luna "I know. I took it as one anyway."

#     # IMAGE: Luna closing the notebook carefully
#     # All three looking at each other, then at the equipment

#     ishimaru "I'll handle the online order tonight. Split it three ways?"

#     lin "Deal."

#     luna "I'll have the methodology written up before the ingredients arrive. So we're not improvising when it actually matters."

#     ishimaru "This weekend is going to be incredible."

#     lin "We're brewing a love potion in an abandoned building with a school secretary as our supervisor."

#     lin "This is either the coolest thing I've ever done or we're getting expelled."

#     luna "Statistically, both can be true."

#     $ set_progress("lab_intro_discovery", 3)

#     $ end_event("new_daytime", **kwargs)

# # Brewing Session unlocks after Gathering Ingredients between Monday and Wednesday
# label lab_intro_19 (**kwargs):
#     $ begin_event(**kwargs)
    
#     # Get the same 3 students
#     $ student_1_name = get_values('student_1', 'random_student_1', **kwargs)
#     $ student_2_name = get_values('student_2', 'random_student_2', **kwargs)
#     $ student_3_name = get_values('student_3', 'random_student_3', **kwargs)
    
#     $ student_1 = Person[student_1_name].get_renpy_char()
#     $ student_2 = Person[student_2_name].get_renpy_char()
#     $ student_3 = Person[student_3_name].get_renpy_char()
    
#     # IMAGE: Abandoned lab, evening light through windows
#     # Lab setup on counter: heating plate, beakers, graduated cylinders, bottles of chemicals arranged neatly
#     # Students wearing safety goggles, standing around the setup nervously
#     # Secretary beside them, arms crossed, observing
#     # Notebook open on stand beside setup
    
#     student_2 "Okay. Everything's ready. All the ingredients are measured out."
    
#     student_1 "I've triple-checked the amounts against the notebook. They should be exact."
    
#     secretary "Good. Precision matters in chemistry. Small variations can change everything."
    
#     # IMAGE: Student 3 looking at heating plate controls
#     # Finger hovering over power button uncertainly
#     # Other two students watching, tense
#     # Secretary's hand resting lightly on counter edge, ready
    
#     student_3 "So... I just turn it on to medium heat like the notes say?"
    
#     secretary "Start lower. Let the temperature rise gradually. Sudden heat can cause unwanted reactions."
    
#     student_3 "Right. Gradual. Got it."
    
#     # IMAGE: Student 3 adjusting heat to low
#     # Students placing main beaker on the heating plate
#     # Secretary watching carefully, relaxed posture but attentive eyes
#     # First wisps of warmth beginning to rise from plate
    
#     student_1 "First ingredient is the distilled water base. Two hundred milliliters."
    
#     # IMAGE: Student 1 carefully pouring distilled water into beaker
#     # Measured precisely in graduated cylinder first
#     # Clear liquid flowing, catching light
#     # Other students watching the level, secretary nodding slightly
    
#     secretary "Perfect. Let that warm for about two minutes before adding anything else."
    
#     student_2 "The notebook doesn't specify a wait time between steps."
    
#     secretary "It doesn't need to. Anyone with chemistry experience knows you don't shock a mixture."
#     secretary "Think of it like cooking. You wouldn't dump cold ingredients into a hot pan all at once."
    
#     student_1 "That makes sense."
    
#     student_1_thought "*She makes everything sound so simple. Like it's just common sense.*"
    
#     # IMAGE: All four watching the water slowly heat
#     # Tiny bubbles beginning to form at bottom of beaker, not boiling yet
#     # Secretary checking her watch casually
#     # Students fidgeting slightly with nervous energy
    
#     secretary "Now. Next ingredient?"
    
#     student_2 "Ethanol. Fifty milliliters."
    
#     secretary "Add it slowly. Pour down the side of the beaker, not directly into the center."
    
#     # IMAGE: Student 2 tilting graduated cylinder
#     # Ethanol flowing down the inside wall of beaker
#     # Mixing with warm water, creating slight shimmer
#     # Secretary's slight nod of approval
    
#     student_2 "Like this?"
    
#     secretary "Exactly like that. Well done."
    
#     # IMAGE: Close-up of beaker contents
#     # Clear liquid, faint alcohol smell beginning to fill the air
#     # Students leaning in slightly, watching for changes
#     # Heat causing gentle circulation in the liquid
    
#     student_3 "It's not really doing anything yet."
    
#     secretary "Patience. The active compounds come next. Those will trigger the visible reactions."
    
#     student_1 "Okay, next is... potassium hydroxide. Ten grams."
    
#     # IMAGE: Student 1 carefully measuring white powder on small scale
#     # Secretary watching the scale reading over student's shoulder
#     # Precise measurement, concentration visible on student's face
    
#     secretary "Careful with that one. It's caustic. Avoid skin contact."
    
#     student_1 "The gloves are on, I'm good."
    
#     # IMAGE: Student 1 adding powder to beaker
#     # White granules hitting liquid, immediately beginning to dissolve
#     # Liquid starting to cloud slightly
#     # Students' faces lit by the heating plate's glow as evening deepens
    
#     student_3 "Oh! It's reacting!"
    
#     secretary "Watch the color. It should start turning cloudy, then progressively darker."
    
#     # IMAGE: Beaker contents shifting
#     # Clear liquid becoming milky white, then gradually taking on brownish tint
#     # Students leaning closer, fascinated
#     # Secretary's expression satisfied, measuring
    
#     student_2 "It's going brown. That's... kind of gross looking."
    
#     secretary "Murky brown is expected at this stage. Keep going."
    
#     secretary_thought "*Following the original formula perfectly. This will give them temporary effects - enough to feel successful, but nothing permanent. Not yet.*"
    
#     # IMAGE: Student checking notebook
#     # Reading next steps carefully
#     # Finger tracing down the handwritten instructions
#     # Other students waiting, watching the brown liquid slowly heat
    
#     student_1 "Next is the organic compound. The one we ordered online."
#     student_1 "Twenty-five milliliters. The notebook calls it... I can't even pronounce this."
    
#     secretary "Doesn't matter what it's called. What matters is the amount and timing."
    
#     # IMAGE: Student 2 holding small dark bottle
#     # Measuring out amber-colored liquid into graduated cylinder
#     # Viscous, slightly thicker than water
#     # Secretary watching the measurement carefully
    
#     secretary "Wait."
    
#     # IMAGE: Student 2 freezing, hand hovering over beaker
#     # Secretary leaning in, checking the temperature
#     # Hand held near beaker without touching, testing heat
    
#     secretary "The mixture needs to reach the right temperature first. Still too cool."
    
#     student_2 "How can you tell?"
    
#     secretary "Experience. Give it another minute, then increase to medium heat."
    
#     student_3 "The notebook doesn't mention specific temperatures."
    
#     secretary "The person who wrote this knew what they were doing. The steps imply the temperatures."
#     secretary "You learn to read between the lines."
    
#     secretary_thought "*He certainly did know what he was doing. Though his formula is incomplete without the catalyst.*"
    
#     # IMAGE: Student 3 adjusting heat to medium
#     # Liquid in beaker beginning to move more actively
#     # Not boiling, but definite circulation
#     # Murky brown color now fully established
    
#     secretary "Now. Add the organic compound."
    
#     # IMAGE: Student 2 pouring amber liquid into beaker
#     # Streams of viscous fluid mixing with brown mixture
#     # Immediate reaction - color darkening further, almost coffee-colored
#     # Students watching intently
    
#     student_1 "Whoa, it's getting darker."
    
#     secretary "Expected. Keep watching. The transformation takes about five minutes from this point."
    
#     # IMAGE: All four gathered close around the beaker
#     # Evening light nearly gone now, lab illuminated mostly by heating plate and whatever ambient light remains
#     # Shadows on faces, focused expressions
#     # Liquid slowly, almost imperceptibly beginning to change
    
#     student_3 "I don't see anything happening."
    
#     secretary "Look at the edges. Where it touches the glass."
    
#     # IMAGE: Close-up of beaker edge
#     # Thin line of liquid at glass contact point showing slight golden tint
#     # Different from the dark brown bulk
#     # Students noticing it, excitement building
    
#     student_2 "There! It's lighter there. Is that it?"
    
#     secretary "That's it. The reaction is starting. Now we wait."
    
#     # IMAGE: Wider shot, all watching
#     # Minutes passing, liquid gradually shifting
#     # Brown becoming less muddy, taking on warmer tones
#     # Students practically holding their breath
    
#     student_1 "It's definitely changing. The brown is getting... lighter? Warmer?"
    
#     secretary "Amber. It's becoming amber."
    
#     # IMAGE: Beaker contents transforming
#     # Murky brown clarifying, becoming translucent
#     # Golden-amber color spreading from edges inward
#     # Light from heating element shining through, creating warm glow
    
#     student_3 "Oh my god, it's actually working!"
    
#     # IMAGE: Complete transformation
#     # Liquid now clear, shimmering amber color
#     # Almost honey-like in appearance but fluid like water
#     # Light playing through it beautifully
#     # Students' faces amazed, lit by the golden glow
    
#     student_2 "It's beautiful!"
    
#     student_1 "We actually did it. We actually made it!"
    
#     # IMAGE: Students looking at each other, then at secretary
#     # Excited, almost bouncing with success
#     # Secretary smiling warmly, genuine-looking pride
    
#     secretary "You did. Well done. Very well done."
    
#     student_3 "I can't believe that worked!"
    
#     secretary "Why not? You followed the instructions precisely. Chemistry rewards precision."
    
#     # IMAGE: Secretary reaching over, turning off heating plate
#     # Beaker still glowing amber in the dimming evening
#     # Students watching as she handles it with practiced ease
    
#     secretary "Let it cool for a few minutes before handling. Still quite hot."
    
#     student_1 "So... does this mean it actually works? Like, as a love potion?"
    
#     # IMAGE: Secretary looking at the students thoughtfully
#     # Slight smile, encouraging but measured
#     # Students waiting for her assessment
    
#     secretary "The chemistry worked. Whether it has the psychological effects described in the notebook..."
#     secretary "That requires testing."
    
#     student_2 "Should we try it? Like, just a little bit to see?"
    
#     secretary "You could. Though I'd recommend a more controlled environment."
#     secretary "Perhaps with friends, in a social setting where you can observe the effects properly."
    
#     # IMAGE: Students exchanging glances
#     # Excitement building again
#     # Secretary watching them come to the conclusion themselves
    
#     student_3 "We could throw a party. This weekend."
    
#     student_1 "Here in the lab! Bring some people, music, make it a whole thing."
    
#     student_2 "And everyone tries the potion. See what happens."
    
#     # IMAGE: Secretary nodding approvingly
#     # Students getting more animated planning
#     # Amber potion cooling on the counter between them
    
#     secretary "That sounds like an excellent idea. Controlled testing in a safe, social environment."
#     secretary "Just keep the group small. Close friends you trust."
    
#     student_3 "Definitely. We don't want this getting out to everyone."
    
#     secretary "Wise. And I should probably be nearby during your... experiment. Just in case."
    
#     student_1 "Would you? That would be amazing."
    
#     # IMAGE: Secretary moving to cabinet, retrieving a clean bottle
#     # Returning to counter, students watching
#     # Preparing to transfer the cooled potion
    
#     secretary "Let's get this bottled properly. Glass container, sealed tight."
#     secretary "Store it somewhere cool and dark until your party."
    
#     # IMAGE: Secretary carefully pouring amber liquid from beaker into bottle
#     # Smooth, controlled pour
#     # Students watching the precious liquid transfer
#     # Glowing amber filling the bottle
    
#     student_2 "How long will it keep?"
    
#     secretary "The compounds should remain stable for several weeks. This weekend will be fine."
    
#     # IMAGE: Secretary sealing the bottle with stopper
#     # Holding it up to remaining light
#     # Amber liquid beautiful in the glass
#     # Students admiring their creation
    
#     secretary "There. Your first successful synthesis."
    
#     student_3 "This is so cool."
    
#     # IMAGE: Secretary handing bottle to Student 1
#     # The transfer careful, ceremonial almost
#     # Student 1 taking it with both hands, reverent
    
#     secretary "Keep it safe. And let me know when you're planning your party."
#     secretary "I'll make sure I'm available."
    
#     student_1 "We will. Thank you so much for all your help, Ms. [secretary_last_name]."
    
#     secretary "My pleasure. This is what education should be—hands-on, engaging, real."
    
#     secretary_thought "*And once they enhance this formula with the catalyst, they'll dose themselves and their friends with the perfected version. No coercion needed. They'll do it willingly.*"
    
#     # IMAGE: Secretary at door, preparing to leave
#     # Students gathered around their bottled potion
#     # Evening darkness outside windows
#     # Sense of accomplishment filling the space
    
#     secretary "Congratulations. You're real chemists now."
    
#     student_2 "Feels amazing."
    
#     secretary "It should. Goodnight, and be careful with that."
    
#     # IMAGE: Students alone with the amber potion in its bottle
#     # Evening darkness settling
#     # Their faces lit by whatever ambient light remains
#     # The bottle glowing faintly on the counter
    
#     student_3 "This weekend is going to be incredible."
    
#     student_1 "I know. I can't wait to see if it actually works."
    
#     student_2 "It will. It has to."
    
#     student_3_thought "*We made something real. Something that could actually change things.*"
    
#     $ set_progress("lab_intro_discovery", 4)
    
#     $ end_event("new_daytime", **kwargs)

# # Secretary Enhancement - After Strategic Planning and Brewing Session
# label lab_intro_20 (**kwargs):
#     $ begin_event(**kwargs)
    
#     $ student1_key = get_values('student1', 'gloria_goto', **kwargs)
#     $ student2_key = get_values('student2', 'lin_kato', **kwargs)
#     $ student3_key = get_values('student3', 'aona_komuro', **kwargs)
    
#     $ student1 = Person[student1_key].get_renpy_char()
#     $ student2 = Person[student2_key].get_renpy_char()
#     $ student3 = Person[student3_key].get_renpy_char()
    
#     # IMAGE: Abandoned lab, late afternoon
#     # Three students working at lab bench
#     # Their brewing equipment scattered around
#     # Bottles of completed weak potion visible
#     # Dust particles catching slanted sunlight through dirty windows
    
#     student1 "We should start bottling these for tomorrow night."
    
#     student2 "How many people are we expecting at the party?"
    
#     student3 "Maybe twenty? I invited everyone from our year."
    
#     # IMAGE: Secretary Emiko entering through lab door
#     # Long black hair, glasses, navy outfit
#     # Carrying small leather bag
#     # Students looking up, surprised but pleased
    
#     student1 "Oh! Miss Langley."
    
#     secretary "Good afternoon, ladies. How's the brewing going?"
    
#     # IMAGE: Students gathering around secretary
#     # Eager, trusting expressions
#     # Showing her their completed batch
#     # Bottles of amber liquid lined up
    
#     student2 "We finished it this morning. We were just about to portion it out."
    
#     student3 "Thank you so much for helping us. We never could've figured this out without you."
    
#     # IMAGE: Secretary examining the bottles
#     # Picking one up, holding to light
#     # Amber liquid clear and smooth
#     # Calculating expression behind warm smile
    
#     secretary "Beautiful work. The color is perfect, the clarity excellent."
    
#     student1 "Do you think it'll work? The love potion effect, I mean?"
    
#     # IMAGE: Secretary setting bottle down carefully
#     # Reaching into her bag
#     # Students watching curiously
    
#     secretary "That's actually why I'm here. I wanted to give you something before your party."
    
#     # IMAGE: Secretary pulling out small dark vial
#     # Maybe 30ml, amber glass
#     # Clear liquid inside
#     # Students leaning in with interest
    
#     student2 "What is it?"
    
#     secretary "A catalytic compound. We—I mean, I—identified it while researching alchemical formulations."
#     secretary "It significantly improves duration and stability of emotional enhancement potions."
    
#     # IMAGE: Students looking at vial with mixture of excitement and caution
#     # One student reaching for it hesitantly
#     # Secretary holding it up to light
    
#     student3 "Is it safe?"
    
#     # IMAGE: Secretary's expression warm, reassuring
#     # Glasses catching light
#     # Maternal, trustworthy posture
    
#     secretary "It's perfectly safe. It's just a stabilizer that makes the effects last longer and manifest more reliably."
#     secretary "Without it, your potion might work for an hour or two. With it, the effects will be much more... persistent."
    
#     student1 "That sounds amazing!"
    
#     student2 "How do we use it?"
    
#     # IMAGE: Secretary moving to lab bench
#     # Students following, clustering around
#     # She's setting vial down beside their bottles
#     # Professional, instructive posture
    
#     secretary "Just add a few drops to each dose before you serve it. Three drops per cup should be sufficient."
#     secretary "Mix it in well. The compound is water-soluble, so it'll integrate seamlessly."
    
#     # IMAGE: Students nodding, taking notes
#     # One student picking up vial carefully
#     # Examining it with academic interest
#     # Secretary watching them with subtle satisfaction
    
#     student3 "Three drops per cup. Got it."
    
#     student1 "You're sure this won't make anyone sick or anything?"
    
#     # IMAGE: Secretary shaking head, gentle smile
#     # Hand on student's shoulder reassuringly
#     # Warm afternoon light making the scene feel safe, mentorly
    
#     secretary "I promise. I've tested it myself."
#     secretary "Exactly what a love potion should do, just... better."
    
#     secretary_thought "*They have no idea they're about to dose themselves with the perfected formula.*"
#     secretary_thought "*Perfect little test subjects. Twenty students, all at once.*"
    
#     # IMAGE: Student holding vial up to light
#     # Clear liquid, unremarkable looking
#     # Other two students gathering their bottles
#     # Beginning to organize for dosing
    
#     student2 "This is incredible. Thank you so much, Miss Langley."
    
#     secretary "Of course. I want your experiment to succeed."
    
#     # IMAGE: Students working together
#     # Opening bottles, preparing to add catalyst
#     # Secretary watching from slight distance
#     # Satisfied, calculating expression when they're not looking
    
#     student3 "Should we test it on ourselves first? Before the party?"
    
#     # IMAGE: Secretary considering
#     # Tilting head thoughtfully
#     # Students waiting for guidance
    
#     secretary "That's wise. Scientific method requires testing."
#     secretary "Why don't you each take a dose tonight? See how you feel. If it works well, you'll know it's ready for the party."
    
#     student1 "Good idea. We can compare notes tomorrow morning."
    
#     # IMAGE: Students portioning out three cups
#         # Adding catalyst drops carefully—one, two, three per cup
#         # Clear liquid disappearing into amber potion
#         # Mixing with small stirrers

#         student2 "Does it change the taste?"

#         secretary "Not noticeably. Maybe slightly sweeter."

#         student3 "Should we dose the whole batch now? So it's ready for tomorrow?"

#         secretary "That's the sensible approach. Better than adding it cup by cup during the party."
#         secretary "Measure it out precisely — three drops per dose, multiply by however many servings you're making."

#         # IMAGE: Students calculating quietly
#         # Student 1 counting bottles, muttering numbers
#         # Student 3 uncapping the vial with careful fingers
#         # Secretary watching from slight distance, arms loosely crossed

#         student1 "Twenty guests, maybe a little extra buffer... so around seventy drops total."

#         secretary "That's right. Take your time. Precision matters more than speed here."

#         # IMAGE: Student 3 holding vial over the first bottle
#         # Tip of the dropper at the mouth of the bottle
#         # The other two watching without breathing
#         # Afternoon light through dirty windows going copper

#         # First drop falls

#         student3 "One."

#         # The liquid catches it without protest — a brief shimmer at the surface, then gone

#         student2 "Is it... doing something?"

#         student3 "Watch the color."

#         # IMAGE: Close-up of bottle
#         # The amber deepening almost imperceptibly
#         # Richer. More saturated. Like the difference between weak tea and steeped
#         # Student 2's face reflected in the glass, eyes wide

#         student1 "Oh."

#         secretary_thought "*There it is. The catalyst integrating perfectly.*"

#         # IMAGE: All three students now leaning over the bottles
#         # Student 3 moving methodically — drops counted under breath
#         # Student 1 transferring to next bottle as each is finished
#         # Student 2 recording counts on a scrap of paper
#         # The smell in the room shifting: old plaster and chemical residue, but warmer now, something floral underneath

#         secretary "Don't rush the last few. The ratio has to hold across the whole batch."

#         student3 "I know. I know."

#         # IMAGE: Student 3 sealing the final bottle
#         # Pressing the stopper in with her palm
#         # Slight exhale — held breath releasing
#         # The row of bottles on the bench, all the same deepened amber

#         student1 "That's everything."

#         student2 "Twenty-three doses. Plus the buffer."

#         # IMAGE: Three students looking at the bottles
#         # Then at each other
#         # Then at secretary

#         student3 "Thank you. Seriously. We couldn't have—"

#         secretary "You did the work. I just provided the tools."

#         # IMAGE: Secretary picking up her bag
#         # Moving toward the door
#         # Smooth, unhurried

#         secretary "Keep them sealed until tomorrow. Cool and dark."
#         secretary "And don't tell anyone what's actually in them before the party."

#         student1 "Obviously. It's our thing."

#         secretary "Good luck, ladies."

#         # IMAGE: Door closing behind her
#         # Students alone in the lab
#         # The smell of old chemicals and something sweet hanging in the cooling air
#         # Bottles in a neat row on the bench

#         # A beat of silence

#         student2 "Tomorrow."

#         student1 "Tomorrow."

#         # IMAGE: Student 3 picking up one of the bottles
#         # Holding it at eye level
#         # Amber liquid catching the last copper light through the window
#         # Her reflection fractured in the glass

#         student3_thought "*Twenty-three people. And none of them will know until it's already inside them.*"

#         # IMAGE: Secretary in the hallway outside
#         # Already several paces away, not looking back
#         # Bag over one shoulder, steps unhurried

#         secretary_thought "*He'll find out when the students hit Level 3 before he expects.*"
#         secretary_thought "*But by then the momentum will be irreversible.*"
#         secretary_thought "*The best experiments are the ones where the subjects never realize they're being studied.*"

#         # IMAGE: Student 3 setting the bottle back in the row
#         # Carefully. Like it might wake up
#         # The three of them standing there in the dimming light with what they've made

#         $ set_progress("lab_intro_discovery", 5)

#         $ end_event("new_daytime", **kwargs)

# # The Party - Friday night on the same day as the PTA Refreshments
# label lab_intro_21 (**kwargs):
#     $ begin_event(**kwargs)
    
#     $ student1_key = get_values('student1', 'gloria_goto', **kwargs)
#     $ student2_key = get_values('student2', 'lin_kato', **kwargs)
#     $ student3_key = get_values('student3', 'miwa_igarashi', **kwargs)
#     $ student4_key = get_values('student4', 'kokoro_nakamura', **kwargs)
    
#     $ student1 = Person[student1_key].get_renpy_char()
#     $ student2 = Person[student2_key].get_renpy_char()
#     $ student3 = Person[student3_key].get_renpy_char()
#     $ student4 = Person[student4_key].get_renpy_char()
    
#     subtitles "[Abandoned Lab, Friday Evening, 8:47 PM]"
    
#     # IMAGE: Abandoned lab transformed
#     # String lights hung haphazardly across ceiling
#     # Twenty students scattered throughout space
#     # Makeshift speaker playing pop music
#     # Dust particles dancing in colored light
#     # Table with plastic cups, bottles, snacks
    
#     # IMAGE: Three organizer students at drink table
#     # Pouring amber liquid from bottles into cups
#     # Adding catalyst drops—three per cup
#     # Mixing carefully with plastic stirrers
#     # Other students nearby, waiting for drinks
    
#     student1 "Three drops each, just like Miss Langley said."
    
#     student2 "Are we really doing this?"
    
#     student3 "Everyone here wants to try it. That's why they came."
    
#     # IMAGE: Organizers distributing cups
#     # Students accepting drinks eagerly
#     # Curiosity, excitement on faces
#     # Someone cranking up the music volume
    
#     subtitles "The scent in the air was complex: cheap perfume layered over old wood and plaster dust, mixed with the sweet amber smell of the enhanced potion. Bass thumped from the speaker, reverberating."
    
#     # IMAGE: Students drinking
#     # Lifting cups, toasting
#     # First sips, then deeper swallows
#     # Tasting, considering, drinking more
    
#     student4 "It's sweet. Tastes like honey and something floral."
    
#     subtitles "Yeah, it's really good!"
    
#     subtitles "Doesn't taste like alcohol at all!"
    
#     # IMAGE: Party in full swing
#     # Students dancing, talking, laughing
#     # Cups being refilled
#     # Fifteen minutes passing
#     # Energy shifting subtly
    
#     # IMAGE: One girl leaning against wall
#     # Flushed face, hand on chest
#     # Friend approaching, concern shifting to curiosity
    
#     subtitles "God, is it warm in here?"
    
#     subtitles "Yeah. Really warm. You okay?"
    
#     subtitles "I feel... good. Like, really good. Relaxed."
    
#     # IMAGE: Another student sitting on dusty workbench
#     # Legs swinging, uninhibited
#     # Skirt riding higher than usual
#     # Not adjusting it, not caring
    
#     student1_thought "*Why do I always worry so much about how I look? This feels better. Just... being.*"
    
#     # IMAGE: Two girls standing close
#     # Eye contact lingering
#     # One reaching up to tuck hair behind the other's ear
#     # Touch gentle, fingers trailing
    
#     subtitles "Your eyes are so pretty. I never noticed before."
    
#     subtitles "Really?"
    
#     subtitles "Really."
    
#     # IMAGE: The first kiss
#     # One girl leaning in
#     # The other meeting her halfway
#     # Lips touching, soft, experimental
#     # Both freezing for a moment
    
#     subtitles "Oh—"
    
#     # IMAGE: Kiss continuing
#     # Neither pulling away
#     # Deepening instead
#     # Hands finding waists
    
#     student2_thought "*This feels amazing. Why did I wait so long?*"
    
#     # IMAGE: Other students noticing
#     # Not shocked, just... interested
#     # Inhibitions visibly lowering across the room
#     # Music still playing, bass vibrating through floorboards
    
#     # IMAGE: Another pair in corner
#     # Already making out
#     # Hands in hair, bodies pressed close
#     # One girl's back against wall
    
#     subtitles "Mmnh—"
    
#     subtitles "Is this okay?"
    
#     subtitles "God, yes—"
    
#     # IMAGE: Student unbuttoning another's blouse
#     # Slow, deliberate
#     # White fabric parting, bra visible beneath
#     # The scent in the air shifting—sweat mixing with perfume and the sweet potion residue
    
#     student3_thought "*I've wanted to touch her like this for months. Months. And I was too scared to even try.*"
    
#     # IMAGE: More students pairing off
#     # Some still dancing, but closer now
#     # Hands on hips, on shoulders, on skin
#     # Clothes loosening across the room
    
#     # IMAGE: Girl pulling her uniform blouse over her head
#     # Tossing it aside casually
#     # Standing in just her bra and skirt
#     # Partner staring, hand reaching to touch bare stomach
    
#     subtitles "You're so soft..."
    
#     # IMAGE: Another student sliding down her skirt
#     # Kicking it away
#     # Dancing in just underwear and top
#     # Completely unselfconscious
    
#     student4_thought "*I feel beautiful. Powerful. Why did I ever think my body was something to hide?*"
    
#     # IMAGE: Makeout session intensifying
#     # Girl straddling another's lap on the dusty workbench
#     # Grinding slowly, deliberately
#     # Moans mixing with music
    
#     subtitles "Ahhh—fuck—"
    
#     subtitles "Don't stop—"
    
#     # IMAGE: Wide shot of lab
#     # Multiple pairs making out in different corners
#     # Clothes scattered on floor
#     # Some students still clothed, watching, considering
#     # Others half-naked, uninhibited
#     # Colored lights casting everything in dreamlike glow
    
#     subtitles "The air was thick—dust, sweat, the sweet chemical scent of residual potion clinging to every surface. Music pounded. Someone laughed, high and breathless. Someone else moaned. Fabric rustled."
    
#     # IMAGE: Two girls on floor
#     # One on top of the other
#     # Kissing deeply, hands wandering
#     # Skirts pushed up, visible skin
    
#     # IMAGE: Student watching from edge of room
#     # Flushed, breathing hard
#     # Hand sliding under her own shirt
#     # Touching herself through fabric
    
#     student1_thought "*I want to join them. I want to feel what they're feeling.*"
    
#     # IMAGE: Her approaching another girl
#     # Both reaching for each other simultaneously
#     # Kissing immediately, desperately
#     # Falling into it like they'd been waiting
    
#     # IMAGE: Time passing—10:30 PM now
#     # Party at peak intensity
#     # Most students partially undressed
#     # Bras visible, skirts bunched up, some topless
#     # Hands everywhere, mouths everywhere
    
#     # IMAGE: Girl with breasts fully exposed
#     # Nipples hard in cool air
#     # Partner's mouth on one, hand on the other
#     # Her head thrown back, eyes closed
    
#     subtitles "Oh god—yes—right there—"
    
#     # IMAGE: Wide shot again
#     # Twenty students, all affected
#     # Various stages of undress, various levels of intimacy
#     # No one judging, no one stopping
#     # Just exploration, pleasure, freedom
    
#     subtitles "The abandoned lab had become something else entirely. A space outside normal rules. The potion had done what it promised—stripped away fear, shame, hesitation. Left only want and the willingness to pursue it."
    
#     # IMAGE: Clock showing 11:15 PM
#     # Energy beginning to shift
#     # Some students separating, breathing hard
#     # Gathering scattered clothes
#     # Flushed faces, messy hair, satisfied expressions
    
#     student2 "I should... probably head back to the dorm."
    
#     student3 "Yeah. Me too."
    
#     # IMAGE: Students beginning to leave
#     # Putting on clothes haphazardly
#     # Buttons missed, skirts twisted
#     # Some leaving in pairs, hands clasped
    
#     subtitles "That was..."
    
#     subtitles "Yeah."
    
#     # IMAGE: Final student leaving lab
#     # Looking back at the space
#     # String lights still glowing
#     # Evidence of what happened scattered everywhere
    
#     student4_thought "*I'm not the same person who walked in here three hours ago.*"
#     student4_thought "*None of us are.*"
    
#     # IMAGE: Empty lab
#     # Lights still on, music still playing softly
#     # Clothes forgotten in corners
#     # The sweet scent of potion lingering
#     # Dust settling in colored light
    
#     $ set_progress("lab_intro_discovery", 5)
#     $ set_progress("school_level", 3)
    
#     $ end_event("new_daytime", **kwargs)

# # Saturday Morning after the PTA Refreshments and Party
# label lab_intro_22 (**kwargs):
#     $ begin_event(**kwargs)
    
#     $ student1_key = get_values('student1', 'lin_kato', **kwargs)
#     $ student2_key = get_values('student2', 'gloria_goto', **kwargs)
#     $ student3_key = get_values('student3', 'miwa_igarashi', **kwargs)
#     $ student4_key = get_values('student4', 'kokoro_nakamura', **kwargs)
    
#     $ student1 = Person[student1_key].get_renpy_char()
#     $ student2 = Person[student2_key].get_renpy_char()
#     $ student3 = Person[student3_key].get_renpy_char()
#     $ student4 = Person[student4_key].get_renpy_char()
    
#     subtitles "[Student Dorms, Saturday Morning, 9:23 AM]"
    
#     # IMAGE: Dorm room, morning light through curtains
#     # Student waking alone in bed
#     # Clothes from last night scattered on floor
#     # Smell of stale air and old perfume
    
#     subtitles "The potion's chemical warmth had faded overnight, leaving only memory and a quiet, persistent clarity."
    
#     # IMAGE: Student sitting up in bed
#     # Hand on chest, checking for the warmth
#     # It's gone—just normal heartbeat
#     # But the memory sharp
    
#     student1_thought "*It's gone. The glow, the heat. But I remember exactly how she tasted.*"
#     student1_thought "*That was real. I wanted it. I still want it.*"
    
#     # IMAGE: Shared bathroom, students brushing teeth
#     # Normal Saturday morning routine
#     # Sports bras, pajama pants, some topless
#     # But eye contact lingers now, awareness shifted
    
#     student2 "Morning."
    
#     student3 "Hey. How're you feeling?"
    
#     student2 "Normal. You?"
    
#     student3 "Yeah. Same."
    
#     # IMAGE: Two students at mirror
#     # One adjusting hair, the other washing face
#     # Glance meeting in reflection
#     # Small smile, then looking away
    
#     student3_thought "*I kissed her last night. Just... walked up and kissed her.*"
#     student3_thought "*The potion's gone but I'm not sorry.*"
    
#     # IMAGE: Back in dorm room
#     # Students getting dressed for the day
#     # Trying on clothes, normal weekend routine
#     # But choosing crop top instead of full shirt
    
#     student1 "What are you doing today?"
    
#     student4 "Breakfast, maybe study. You?"
    
#     student1 "Same."
    
#     # IMAGE: Student pulling on crop top
#     # Bare midriff showing
#     # Checking mirror, leaving it on instead of changing
#     # Small shift in choice
    
#     student4_thought "*Yesterday I would've picked something longer. Today this just... feels right.*"
    
#     # IMAGE: Common area, students gathering
#     # Sitting on couches, normal positions
#     # But closer than usual, touching casually
#     # Hand on knee, leaning into shoulder
    
#     student2 "So. Last night."
    
#     student3 "Yeah."
    
#     student2 "No regrets?"
    
#     student3 "None."
    
#     # IMAGE: Two students sitting together
#     # Legs touching, comfortable proximity
#     # Easy, not charged—just normalized
    
#     student4 "I kissed you."
    
#     subtitles "I remember."
    
#     student4 "...Can I do it again sometime?"
    
#     subtitles "Yeah. I'd like that."
    
#     # IMAGE: Students heading out of dorm
#     # Groups of two and three
#     # Crop tops, visible bra straps, shorter skirts
#     # Walking with shoulders back, confident stride
    
#     # IMAGE: Campus path, mid-morning
#     # Two students holding hands
#     # Not hiding it, just walking
#     # Others passing, not reacting
    
#     student1_thought "*The potion showed me what I wanted. Now I'm choosing to keep it.*"
    
#     # IMAGE: Final shot of dorm building
#     # Saturday morning quiet
#     # Students dispersing into weekend
#     # The chemical rush gone, the behavioral shift permanent
    
#     subtitles "The warmth had faded, but the comfort remained. What the potion revealed, they were choosing to keep."
    
#     $ end_event("new_daytime", **kwargs)

# # Saturday Evening after the PTA Refreshments and Party
# label lab_intro_23 (**kwargs):
#     $ begin_event(**kwargs)
    
#     $ student1_key = get_values('student1', 'lin_kato', **kwargs)
#     $ student2_key = get_values('student2', 'miwa_igarashi', **kwargs)
#     $ student3_key = get_values('student3', 'kokoro_nakamura', **kwargs)
#     $ student4_key = get_values('student4', 'gloria_goto', **kwargs)
    
#     $ student1 = Person[student1_key].get_renpy_char()
#     $ student2 = Person[student2_key].get_renpy_char()
#     $ student3 = Person[student3_key].get_renpy_char()
#     $ student4 = Person[student4_key].get_renpy_char()
    
#     subtitles "[Dorm Common Room, Saturday Evening, 7:34 PM]"
    
#     # IMAGE: Common room, evening light fading
#     # Twelve students scattered on couches and floor
#     # Pizza boxes open on coffee table
#     # Music playing from someone's phone, low volume
#     # Smell of pepperoni and cheap vanilla body spray
    
#     subtitles "Music drifted from a phone speaker, volume low enough for conversation."
    
#     # IMAGE: Students arranged casually
#     # Two on couch, one sitting in the other's lap
#     # Three on floor cushions, legs tangled together
#     # Others leaning against furniture, sitting close
#     # Visible bra straps through sheer tops, crop tops showing midriff
    
#     # IMAGE: Student sitting in another's lap
#     # Arms around waist, chin on shoulder
#     # Completely casual, just how they're sitting
#     # Neither thinking about it
    
#     student1 "Pass me a slice?"
    
#     subtitles "Which kind?"
    
#     student1 "Pepperoni."
    
#     # IMAGE: Student reaching across, handing pizza
#     # Hand lingering on the other's thigh afterward
#     # Natural placement, comfortable
    
#     student1_thought "*Her hand on my leg doesn't make me nervous. It makes me happy.*"
    
#     # IMAGE: Two students on floor
#     # One braiding the other's hair
#     # Fingers working through strands slowly
#     # The one being braided leaning back into touch
    
#     student2 "So who kissed who Friday night?"
    
#     subtitles "God, everyone kissed everyone."
    
#     student3 "I kissed Yuki. And Hana. And... I think Akari?"
    
#     subtitles "Definitely Akari. I saw that."
    
#     # IMAGE: Students laughing, easy and open
#     # No coded language, no euphemisms
#     # Talking about attraction like it's normal
    
#     student4 "I've been into Mei for weeks. Friday just finally gave me the excuse."
    
#     student2 "Are you two together now?"
    
#     student4 "Maybe? We're figuring it out."
    
#     # IMAGE: Two students sitting close on couch
#     # Shoulders touching, hands near each other on cushion
#     # One wearing white sheer top, red bra visible underneath
#     # The other in black crop top, bare midriff
    
#     student3_thought "*Friday was the potion. Tonight is just us. And it still feels right.*"
    
#     # IMAGE: Student leaning in to kiss another
#     # Quick, gentle press of lips
#     # Pulling back, continuing conversation
#     # Like it's punctuation, not disruption
    
#     student1 "You want to hang out tomorrow?"
    
#     subtitles "Yeah. Come to my room after breakfast?"
    
#     student1 "Okay."
    
#     # IMAGE: Group conversation continuing
#     # Pizza being eaten, drinks passed around
#     # Physical contact constant—hands on knees, heads on shoulders, fingers playing with hair
    
#     student2 "Friday was intense."
    
#     student4 "So intense."
    
#     student2 "But this... this just feels right."
    
#     # IMAGE: Two students making out on couch
#     # Not frenzied, just affectionate
#     # Hands in hair, gentle
#     # Others glancing, smiling, turning back to conversation
    
#     # IMAGE: Student adjusting another's necklace
#     # Fingers on collarbone, lingering
#     # Eye contact, small smile
    
#     subtitles "You look good today."
    
#     student3 "Thanks. So do you."
    
#     # IMAGE: Students starting to pair off
#     # Some clearly coupling, sitting closer
#     # Others still exploring, talking to multiple people
#     # Fluidity accepted, no judgment
    
#     student4_thought "*I like her. But I also like her. And maybe that's okay.*"
    
#     # IMAGE: Time passing—9:00 PM
#     # Students beginning to disperse
#     # Gathering phones, water bottles, shoes
#     # Making plans, confirming times
    
#     student1 "I'm heading back to my room."
    
#     student2 "Want company?"
    
#     student1 "Yeah. Come over."
    
#     # IMAGE: Two students leaving together
#     # Hands clasped, easy intimacy
#     # Others watching, accepting
    
#     student3 "See you guys tomorrow."
    
#     subtitles "Study session in the library at two?"
    
#     student3 "I'll be there."
    
#     # IMAGE: Common room emptying
#     # Students leaving in pairs and small groups
#     # Physical closeness visible—arms around waists, holding hands
#     # New patterns forming, normalizing
    
#     # IMAGE: Last few students cleaning up
#     # Closing pizza boxes, gathering trash
#     # Still touching casually—shoulder bumps, hands brushing
    
#     student4 "This weekend's been good."
    
#     subtitles "Really good."
    
#     student4 "Different. But good."
    
#     # IMAGE: Final students leaving
#     # Lights being turned off
#     # Music stopping
#     # Empty common room, smell of pizza lingering
    
#     subtitles "The chemistry was gone, but the permission remained. What started Friday was settling into something sustainable."
    
#     $ end_event("new_daytime", **kwargs)

# # Sunday Mini events after the PTA Refreshments and Party
# label lab_intro_24a (**kwargs):
#     $ begin_event(**kwargs)
    
#     subtitles "[Campus Gym, Sunday Morning, 11:15 AM]"
    
#     # IMAGE: Gym floor, students working out
#     # Four girls in just sports bras and athletic shorts
#     # No shirts, completely comfortable
#     # Sweat glistening, bodies on display without self-consciousness
    
#     subtitles "The gym smelled like rubber mats and sweat."
    
#     # IMAGE: Two students spotting each other on weights
#     # Close physical proximity, hands ready to assist
#     # Bodies confident, posture strong
    
#     student_thought "*A week ago I would've worn a loose shirt. Today this just feels normal.*"
    
#     # IMAGE: Student stretching on mat
#     # Sports bra, bare midriff, legs extended
#     # Another student watching, appreciative glance
#     # No shame in looking, no shame in being looked at
    
#     $ end_event("new_daytime", **kwargs)

# label lab_intro_24b (**kwargs):
#     $ begin_event(**kwargs)
    
#     subtitles "[Library Study Room, Sunday Afternoon, 2:20 PM]"
    
#     # IMAGE: Five students around table with textbooks
#     # Crop tops, visible bra straps, casual dress
#     # Legs touching under table, leaning on shoulders while reading
#     # Nobody adjusting clothes or creating distance
    
#     student1 "What did you get for question seven?"
    
#     student2 "Thirty-two. Wait, let me check—"
    
#     # IMAGE: Student leaning over another's shoulder to see paper
#     # Hand on back for balance, cheek close to cheek
#     # Physical contact unremarkable, just how they work now
    
#     student_thought "*Her hand on my back. Her hair smelling like coconut. This is just how we study now.*"
    
#     # IMAGE: Two students sharing textbook
#     # Shoulders pressed together, thighs touching
#     # One's hand resting on the other's knee while pointing at page
    
#     $ end_event("new_daytime", **kwargs)
    
# label lab_intro_24c (**kwargs):
#     $ begin_event(**kwargs)
    
#     subtitles "[Campus Courtyard, Sunday Afternoon, 4:10 PM]"
    
#     # IMAGE: Courtyard benches, students scattered
#     # Two girls kissing on bench, casual afternoon affection
#     # Others walking past, not staring
#     # Hand-holding pairs, sitting in laps
    
#     # IMAGE: Student sitting in another's lap
#     # Arms around waist, talking to third student
#     # Completely casual positioning
#     # No self-consciousness about observers
    
#     student_thought "*People can see us. And I don't care. Why would I care?*"
    
#     # IMAGE: Another pair holding hands while walking
#     # Fingers laced, swinging arms slightly
#     # Public display, completely normalized
    
#     $ end_event("new_daytime", **kwargs)

# label lab_intro_24d (**kwargs):
#     $ begin_event(**kwargs)
    
#     subtitles "[Dorm Hallway, Sunday Evening, 6:35 PM]"
    
#     # IMAGE: Dorm hallway, doors open
#     # Students visible inside rooms in underwear, sports bras
#     # Walking between rooms in minimal clothing
#     # Privacy boundaries relaxed
    
#     # IMAGE: Student in hallway wearing just panties and tank top
#     # Carrying towel to shower, completely casual
#     # Another student passing, both nodding hello
    
#     student_thought "*This is just who I am now. Who we are. And it's better.*"
    
#     $ end_event("new_daytime", **kwargs)

# label lab_intro_24e (**kwargs):
#     $ begin_event(**kwargs)
    
#     subtitles "[Dorm Room, Sunday Night, 9:20 PM]"
    
#     # IMAGE: Student choosing outfit for Monday
#     # Laying clothes on bed—crop top, shorter skirt
#     # Things that would've felt "too much" on Thursday
#     # Now just normal
    
#     student_thought "*This would've scared me last week. Now it's just Monday's outfit.*"
    
#     # IMAGE: Phone screen showing text messages
#     # Making plans, confirming times
#     # "lunch tomorrow?" "yeah see you then"
#     # New relationship dynamics settling
    
#     # IMAGE: Student getting into bed
#     # Lights off, phone on nightstand
#     # Monday classes tomorrow
#     # Everything changed, everything normal
    
#     subtitles "Sunday night settled quiet. New patterns accepted. The weekend had integrated what Friday revealed."
    
#     $ end_event("new_daytime", **kwargs)


# # First Monday after the PTA Refreshments and Party
# label lab_intro_25 (**kwargs):
    # $ begin_event(**kwargs)
    
    # subtitles "[School Campus, Monday Morning, 7:32 AM]"
    
    # # IMAGE: Headmaster arriving on campus
    # # Early morning light, students walking to classes
    # # Briefcase in hand, usual Monday routine
    # # Smell of dew on grass, fresh coffee from nearby café
    
    # headmaster_thought "First Monday after the PTA vote. Let's see if the changes are manifesting."
    
    # # IMAGE: Hallway entrance, students passing
    # # Headmaster's eyes tracking details immediately
    # # Two girls holding hands, walking close
    # # Another with visible red bra straps through white sheer blouse
    
    # headmaster_thought "Hand-holding. Public affection between students."
    
    # # IMAGE: Student in crop top and skirt
    # # Bare midriff visible, confident stride
    # # Walking past headmaster without adjusting clothes
    # # No self-consciousness
    
    # headmaster_thought "Crop tops. Visible skin. She's comfortable showing it."
    
    # # IMAGE: Two students by lockers
    # # Quick kiss before separating to classes
    # # Other students passing, not reacting
    # # Normalized behavior
    
    # headmaster_thought "Kissing in the hallway. Between girls. And no one's stopping them."
    
    # # IMAGE: Classroom glimpsed through open door
    # # Students settling in for first period
    # # Multiple visible bra straps, tied shirts, relaxed posture
    # # Teacher Lily Anderson at board, not addressing dress code
    
    # headmaster_thought "Anderson sees the violations and she's just... teaching."
    # headmaster_thought "The teachers are permissive. That's the formula working."
    
    # # IMAGE: Headmaster walking through main corridor
    # # Cataloging changes mentally
    # # Student sitting in another's lap on bench
    # # Group of three with arms around waists
    # # Confidence in every posture, every gesture
    
    # headmaster_thought "The teachers I understand. I dosed them Friday morning."
    # headmaster_thought "Their permissiveness makes sense—they're not enforcing boundaries, not correcting clothing."
    
    # # IMAGE: Headmaster stopping, staring
    # # Student walking past in tied shirt showing midriff
    # # Another with skirt shorter than regulation
    # # Third with completely visible black bra under sheer white top
    
    # headmaster_thought "But the students themselves..."
    # headmaster_thought "I didn't dose the students. I dosed the teachers and the parents to create permissive structures."
    # headmaster_thought "So why are the students choosing this? Why are they comfortable?"
    
    # # IMAGE: More students passing
    # # Casual physical contact, confident body language
    # # Visible undergarments, intentional skin exposure
    # # All voluntary, all comfortable
    
    # headmaster_thought "Something else happened. Something I didn't plan."
    
    # # IMAGE: Headmaster's office, 8:15 AM
    # # Him at desk, door open
    # # Secretary Emiko entering with morning reports
    # # Long black hair, glasses, navy outfit as always
    
    # secretary "Good morning."
    
    # headmaster "Morning. Close the door."
    
    # # IMAGE: Secretary closing door, turning
    # # Slight smile, knowing expression
    # # Moving to sit across from his desk
    
    # secretary "You've seen the students."
    
    # headmaster "I've seen the students."
    
    # # IMAGE: Headmaster leaning forward
    # # Hands clasped on desk
    # # Analytical, trying to piece it together
    
    # headmaster "The teachers are permissive. That's expected—I dosed them Friday morning."
    # headmaster "But the students are exhibiting the same comfort. Visible undergarments, physical affection, body confidence."
    # headmaster "I didn't dose the students. So what happened this weekend?"
    
    # # IMAGE: Secretary settling back in chair
    # # Calm, composed, not surprised by his question
    # # Fingers steepled, slight smile
    
    # secretary "I facilitated it."
    
    # # IMAGE: Headmaster's expression shifting
    # # Surprise, confusion, processing
    
    # headmaster "You what?"
    
    # secretary "Not directly. But I helped them along."
    
    # # IMAGE: Secretary leaning forward
    # # Explaining methodically
    # # Headmaster listening intently
    
    # secretary "Three weeks ago, a group of students found your notebook in the abandoned lab. The original weak formula."
    # secretary "I intercepted them. Spun it as a 'love potion' experiment. Offered to help them brew it."
    
    # headmaster "You helped students brew the potion."
    
    # secretary "The weak formula, initially. No catalyst. Just the base compound."
    
    # # IMAGE: Headmaster's hands spreading on desk
    # # Mind working through timeline
    
    # headmaster "But they wouldn't have had access to the catalyst. The trichloroethylene was—"
    
    # secretary "I gave it to them."
    
    # # IMAGE: Headmaster staring
    # # Secretary meeting his gaze steadily
    
    # secretary "Friday afternoon, after you'd already dosed the PTA mothers. I brought the catalyst to the lab."
    # secretary "Told them it was a stabilizer to make their potion last longer."
    # secretary "They added it to their batch. Threw a party Friday night in the abandoned lab."
    
    # # IMAGE: Secretary's slight smile
    # # Headmaster processing, calculating
    
    # secretary "Students dosed themselves with the enhanced formula Friday night."
    
    # headmaster "They dosed themselves."
    
    # secretary "They tested it on themselves. Experienced the peak effects. By Saturday morning, the chemical rush had faded..."
    # secretary "But the behavioral changes remained. They spent the weekend integrating. Today you're seeing the permanent baseline."
    
    # # IMAGE: Headmaster leaning back
    # # Running hand through hair
    # # Mix of emotions—surprise, concern, but also recognition
    
    # headmaster "You ran a parallel operation. Without telling me."
    
    # secretary "Yes."
    
    # headmaster "Why?"
    
    # # IMAGE: Secretary's expression shifting
    # # More serious, strategic
    
    # secretary "Because student culture shifts fastest. Peer influence is exponential."
    # secretary "You were focused on authority figures—teachers, parents—creating permissive structures from above."
    # secretary "I focused on the students themselves. Cultural change from within."
    
    # # IMAGE: Headmaster considering
    # # Analytical mind engaging
    
    # headmaster_thought "She's right. Student behavior drives peer pressure more than any policy change."
    # headmaster_thought "If the students are comfortable, they'll pull others along faster than teacher permission ever could."
    
    # headmaster "The timing was deliberate. You dosed them the same weekend I dosed the teachers and parents."
    
    # secretary "Convergence. All three populations moving together."
    # secretary "Teachers permissive, parents approving, students comfortable."
    # secretary "No resistance from any direction."
    
    # # IMAGE: Headmaster standing
    # # Moving to window, looking out at campus
    # # Students visible below, exhibiting new behaviors
    
    # headmaster "Show me. Walk me through what you're seeing."
    
    # # IMAGE: Hallway, headmaster and secretary walking together
    # # Students passing in both directions
    # # Secretary gesturing subtly
    
    # secretary "Visible undergarments. Bra straps through sheer tops, intentional exposure."
    # secretary "Crop tops, tied shirts—midriff showing is normalized now."
    # secretary "Physical affection. Hand-holding, casual touching, sitting in laps."
    
    # # IMAGE: Two students against lockers
    # # One adjusting the other's necklace
    # # Fingers on collarbone, intimate proximity
    # # Passing without self-consciousness
    
    # secretary "Confidence. Posture, eye contact, body language. They're comfortable in their bodies."
    
    # # IMAGE: Classroom door open
    # # Teacher Zoe Parker at front
    # # Students in various revealing outfits
    # # Parker teaching, not addressing dress code
    
    # headmaster "Parker's not correcting them."
    
    # secretary "Parker was dosed Friday morning. So were all the teachers."
    # secretary "They're permissive now. The dress code violations don't register as problems anymore."
    
    # # IMAGE: Courtyard visible through window
    # # Two students kissing on bench
    # # Others walking past, unbothered
    
    # secretary "Public displays of affection. Between girls. No one's stopping it because everyone's baseline shifted."
    
    # headmaster "Teachers dosed. Parents dosed. Students comfortable."
    
    # secretary "Exactly. Convergence."
    
    # # IMAGE: Returning to office
    # # Both sitting, headmaster at desk, secretary across
    # # Strategic discussion mode
    
    # headmaster "And the students who weren't at the party?"
    
    # secretary "Influenced by those who were. Peer pressure, social proof, visible comfort."
    # secretary "The culture is shifting. Some will follow faster than others."
    
    # # IMAGE: Headmaster's hands clasped, thinking
    # # Secretary waiting, confident in her assessment
    
    # headmaster "The teachers. How are they adapting?"
    
    # secretary "Permissive. Physical comfort increasing—they're not enforcing boundaries they used to enforce."
    # secretary "Give them time. The permanent changes will stabilize further."
    
    # headmaster "And the parents?"
    
    # secretary "Adelaide Hall, Nubia Davis, Yuki Yamamoto. All dosed Friday afternoon."
    # secretary "They approved the relaxed policies without objection. First visible effect."
    # secretary "Behavioral changes will continue to manifest."
    
    # # IMAGE: Headmaster looking at secretary
    # # New understanding of her role
    
    # headmaster "You've been operating independently."
    
    # secretary "Yes."
    
    # headmaster "Running your own strategy. Making decisions without consulting me."
    
    # secretary "Yes."
    
    # # IMAGE: Secretary meeting his gaze
    # # Unapologetic, calm
    
    # secretary "You needed plausible deniability. If this went wrong, you could claim ignorance of the student subplot."
    # secretary "But it didn't go wrong. It worked."
    
    # # IMAGE: Headmaster's slight smile
    # # Recognition, acceptance
    
    # headmaster "It did work. The convergence is visible everywhere."
    
    # secretary "Student culture is the accelerant. Authority structure is the framework. You built the framework."
    # secretary "I provided the accelerant."
    
    # # IMAGE: Both looking out window
    # # Campus visible, students moving between classes
    # # New behaviors everywhere—comfort, confidence, physical affection
    
    # headmaster "We need to maintain supply. The catalyst is limited."
    
    # secretary "I'm aware. We have enough for strategic dosing—key influencers, resistant individuals."
    # secretary "But the students self-replicated. They brewed it themselves."
    
    # headmaster "Can they do it again?"
    
    # secretary "If we provide catalyst, yes. The formula is in their hands now."
    
    # # IMAGE: Headmaster considering
    # # Secretary watching
    
    # headmaster "Let them. If they want to dose their friends, let them."
    # headmaster "Student-driven is more sustainable than top-down anyway."
    
    # secretary "Agreed."
    
    # # IMAGE: Secretary standing
    # # Preparing to leave
    # # Headmaster remaining seated
    
    # secretary "I should get back to my desk. Morning announcements need to go out."
    
    # headmaster "Emiko."
    
    # # IMAGE: Secretary pausing at door
    # # Looking back
    
    # headmaster "Good work."
    
    # secretary "Thank you."
    
    # # IMAGE: Secretary leaving, door closing
    # # Headmaster alone at desk
    # # Processing everything
    
    # headmaster_thought "Teachers. Parents. Students. All dosed in one weekend."
    # headmaster_thought "The experiment exceeded my control. But it's succeeding."
    
    # # IMAGE: Headmaster at window again
    # # Watching campus
    # # Students showing new behaviors, teachers permissive, boundaries shifted
    
    # headmaster_thought "I planned for gradual cultural shift. She created exponential momentum."
    # headmaster_thought "Teachers, parents, students—all moving together now."
    
    # # IMAGE: Close-up of headmaster's face
    # # Analytical satisfaction, strategic acceptance
    
    # headmaster_thought "Student comfort. Teacher permissiveness. Parent approval."
    # headmaster_thought "The culture is shifting faster than I projected."
    # headmaster_thought "And I'm no longer the only one building it."
    
    # headmaster_thought "She didn't go around me. She went ahead of me."
    # headmaster_thought "There's a difference."

    # # IMAGE: Campus from headmaster's window
    # # Students comfortable, confident, free
    # # New normal settling into place
    # # Everything changed, momentum building
    
    # headmaster_thought "The experiment continues. But it's not just mine anymore."
    
    # $ set_progress("lab_intro", 20)
    
    # $ end_event("new_daytime", **kwargs)