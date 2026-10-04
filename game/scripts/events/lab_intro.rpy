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
    headmaster.think "Hmm, the progress I made is good, but it is just the beginning."
    headmaster.think "It's probably getting harder from now on. I set a good basis, but there is still resistance in their minds..."

    $ image.show(1)
    headmaster.think "Maybe it's time to start work on the potions."
    headmaster.think "It's unfortunate that I can't reach my partner, he would be of immense help..."

    $ image.show(2)
    headmaster.think "At least I have this one last potion. I have to be careful to not waste it."

    $ image.show(3)
    headmaster.think "I also have a few notes about the potion, its effects and ingredients, but nothing very detailed unfortunately."
    headmaster.think "I guess the first thing I should do is to set up a makeshift lab. I should check out the old lab building."

    headmaster.think "Maybe there is some stuff I could still use."

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
            Pattern("main", "images/events/lab_intro/lab_intro_2/lab_intro_2 <step>.webp"),
            thumbnail = "images/events/lab_intro/lab_intro_2/lab_intro_2 0.webp"))
    
    lab_intro_2_search_gym_storage = FragmentStorage("lab_intro_2_search_gym")
    lab_intro_2_search_gym_storage.add_event(
        EventFragment(3, "lab_intro_2_search_gym_1",
            NOT(ItemCondition("lab_mortar_and_pestle")),
            ReplayCategoryOption("lab_intro"),
            Pattern("main", "images/events/lab_intro/lab_intro_2/lab_intro_2_gym 1.webp"),
            thumbnail = "images/events/lab_intro/lab_intro_2/lab_intro_2_gym 1.webp"),
        EventFragment(3, "lab_intro_2_search_gym_2",
            ItemCondition("lab_distilled_water"),
            ReplayCategoryOption("lab_intro"),
            Pattern("main", "images/events/lab_intro/lab_intro_2/lab_intro_2_gym 2.webp"),
            thumbnail = "images/events/lab_intro/lab_intro_2/lab_intro_2_gym 2.webp"))
    gym_events["search"].add_event(
        EventComposite(3, "lab_intro_2_search_gym", [lab_intro_2_search_gym_storage],
            TimeCondition(weekday = "d", daytime = "d"),
            ProgressCondition("lab_intro", 2),
            ReplayCategoryOption("lab_intro"),
            Pattern("base", "images/events/lab_intro/lab_intro_2/lab_intro_2_gym.webp"),
            thumbnail = "images/events/lab_intro/lab_intro_2/lab_intro_2_gym.webp"))


    lab_intro_2_search_cafeteria_storage = FragmentStorage("lab_intro_2_search_cafeteria")
    lab_intro_2_search_cafeteria_storage.add_event(
        Event(3, "lab_intro_2_search_cafeteria_1",
            NOT(ItemCondition("lab_mortar_and_pestle")),
            ReplayCategoryOption("lab_intro"),
            Pattern("main", "images/events/lab_intro/lab_intro_2/lab_intro_2_cafeteria 1.webp"),
            thumbnail = "images/events/lab_intro/lab_intro_2/lab_intro_2_cafeteria 1.webp"),
        Event(3, "lab_intro_2_search_cafeteria_2",
            NOT(ItemCondition("lab_distilled_water")),
            ReplayCategoryOption("lab_intro"),
            Pattern("main", "images/events/lab_intro/lab_intro_2/lab_intro_2_cafeteria 2.webp"),
            thumbnail = "images/events/lab_intro/lab_intro_2/lab_intro_2_cafeteria 2.webp"),
        Event(3, "lab_intro_2_search_cafeteria_3",
            ItemCondition("lab_mortar_and_pestle"),
            ItemCondition("lab_distilled_water"),
            ReplayCategoryOption("lab_intro"),
            Pattern("main", "images/events/lab_intro/lab_intro_2/lab_intro_2_cafeteria 3.webp"),
            thumbnail = "images/events/lab_intro/lab_intro_2/lab_intro_2_cafeteria 3.webp"))
    cafeteria_events["search"].add_event(
        EventComposite(3, "lab_intro_2_search_cafeteria", [lab_intro_2_search_cafeteria_storage],
            TimeCondition(weekday = "d", daytime = "d"),
            ProgressCondition("lab_intro", 2),
            ReplayCategoryOption("lab_intro"),
            Pattern("base", "images/events/lab_intro/lab_intro_2/lab_intro_2_cafeteria.webp"),
            thumbnail = "images/events/lab_intro/lab_intro_2/lab_intro_2_cafeteria.webp"))

    lab_intro_2_search_dorm_storage = FragmentStorage("lab_intro_2_search_dorm")
    lab_intro_2_search_dorm_storage.add_event(
        Event(3, "lab_intro_2_search_dorm_1",
            NOT(ItemCondition("lab_mortar_and_pestle")),
            ReplayCategoryOption("lab_intro"),
            Pattern("main", "images/events/lab_intro/lab_intro_2/lab_intro_2_dorm 1.webp"),
            thumbnail = "images/events/lab_intro/lab_intro_2/lab_intro_2_dorm 1.webp"),
        Event(3, "lab_intro_2_search_dorm_2",
            NOT(ItemCondition("lab_distilled_water")),
            ReplayCategoryOption("lab_intro"),
            Pattern("main", "images/events/lab_intro/lab_intro_2/lab_intro_2_dorm 2.webp"),
            thumbnail = "images/events/lab_intro/lab_intro_2/lab_intro_2_dorm 2.webp"),
        Event(3, "lab_intro_2_search_dorm_3",
            ItemCondition("lab_mortar_and_pestle"),
            ItemCondition("lab_distilled_water"),
            ReplayCategoryOption("lab_intro"),
            Pattern("main", "images/events/lab_intro/lab_intro_2/lab_intro_2_dorm 3.webp"),
            thumbnail = "images/events/lab_intro/lab_intro_2/lab_intro_2_dorm 3.webp"))
    sd_events["search"].add_event(
        EventComposite(3, "lab_intro_2_search_dorm", [lab_intro_2_search_dorm_storage],
            TimeCondition(weekday = "d", daytime = "d"),
            ProgressCondition("lab_intro", 2),
            ReplayCategoryOption("lab_intro"),
            Pattern("base", "images/events/lab_intro/lab_intro_2/lab_intro_2_dorm.webp"),
            thumbnail = "images/events/lab_intro/lab_intro_2/lab_intro_2_dorm.webp"))

    lab_intro_2_search_kiosk_storage = FragmentStorage("lab_intro_2_search_kiosk")
    lab_intro_2_search_kiosk_storage.add_event(
        Event(3, "lab_intro_2_search_kiosk_1",
            NOT(ItemCondition("lab_glassware")),
            ReplayCategoryOption("lab_intro"),
            Pattern("main", "images/events/lab_intro/lab_intro_2/lab_intro_2_kiosk_1 <step>.webp"),
            thumbnail = "images/events/lab_intro/lab_intro_2/lab_intro_2_kiosk_1 4.webp"),
        Event(3, "lab_intro_2_search_kiosk_2",
            ItemCondition("lab_glassware"),
            ReplayCategoryOption("lab_intro"),
            Pattern("main", "images/events/lab_intro/lab_intro_2/lab_intro_2_kiosk_2.webp"),
            thumbnail = "images/events/lab_intro/lab_intro_2/lab_intro_2_kiosk_2.webp"))
    kiosk_events["search"].add_event(
        EventComposite(3, "lab_intro_2_search_kiosk", [lab_intro_2_search_kiosk_storage],
            TimeCondition(weekday = "d", daytime = "d"),
            ProgressCondition("lab_intro", 2),
            ReplayCategoryOption("lab_intro"),
            Pattern("base", "images/events/lab_intro/lab_intro_2/lab_intro_2_kiosk.webp"),
            thumbnail = "images/events/lab_intro/lab_intro_2/lab_intro_2_kiosk.webp"))

    courtyard_events["patrol"].add_event(
        Event(3, "lab_intro_2_patrol_courtyard",
            TimeCondition(weekday = "d", daytime = "d"),
            Pattern("main", "images/events/lab_intro/lab_intro_2/lab_intro_2_patrol_courtyard <step>.webp"),
            ProgressCondition("lab_intro", 2),
            NOT(ItemCondition("lab_gas_burner")),
            ReplayCategoryOption("lab_intro"),
            thumbnail = "images/events/lab_intro/lab_intro_2/lab_intro_2_patrol_courtyard 0.webp"))
    courtyard_events["search"].add_event(
        Event(3, "lab_intro_2_search_courtyard",
            TimeCondition(weekday = "d", daytime = "d"),
            Pattern("main", "images/events/lab_intro/lab_intro_2/lab_intro_2_search_courtyard <step>.webp"),
            ProgressCondition("lab_intro", 2),
            ReplayCategoryOption("lab_intro"),
            thumbnail = "images/events/lab_intro/lab_intro_2/lab_intro_2_search_courtyard 0.webp"))

    lab_intro_2_search_school_storage = FragmentStorage("lab_intro_2_search_school")
    lab_intro_2_search_school_storage.add_event(
        Event(3, "lab_intro_2_search_school_1",
            NOT(ItemCondition("lab_office_supplies")),
            ReplayCategoryOption("lab_intro"),
            Pattern("main", "images/events/lab_intro/lab_intro_2/lab_intro_2_school 2.webp"),
            thumbnail = "images/events/lab_intro/lab_intro_2/lab_intro_2_school 2.webp"),
        Event(3, "lab_intro_2_search_school_2",
            ItemCondition("lab_office_supplies"),
            ReplayCategoryOption("lab_intro"),
            Pattern("main", "images/events/lab_intro/lab_intro_2/lab_intro_2_school 1.webp"),
            thumbnail = "images/events/lab_intro/lab_intro_2/lab_intro_2_school 1.webp"))
    sb_events["search"].add_event(
        EventComposite(3, "lab_intro_2_search_school", [lab_intro_2_search_school_storage],
            TimeCondition(weekday = "d", daytime = "d"),
            ProgressCondition("lab_intro", 2),
            ReplayCategoryOption("lab_intro"),
            Pattern("main", "images/events/lab_intro/lab_intro_2/lab_intro_2_school.webp"),
            thumbnail = "images/events/lab_intro/lab_intro_2/lab_intro_2_school.webp"))

    lab_intro_2_search_office_storage = FragmentStorage("lab_intro_2_search_office")
    lab_intro_2_search_office_storage.add_event(
        Event(3, "lab_intro_2_search_office_1",
            NOT(ItemCondition("lab_office_supplies")),
            ReplayCategoryOption("lab_intro"),
            Pattern("main", "images/events/lab_intro/lab_intro_2/lab_intro_2_office 1.webp"),
            thumbnail = "images/events/lab_intro/lab_intro_2/lab_intro_2_office 1.webp"),
        Event(3, "lab_intro_2_search_office_2",
            ItemCondition("lab_office_supplies"),
            ReplayCategoryOption("lab_intro"),
            Pattern("main", "images/events/lab_intro/lab_intro_2/lab_intro_2_office 2.webp"),
            thumbnail = "images/events/lab_intro/lab_intro_2/lab_intro_2_office 2.webp"))
    office_building_events["search"].add_event(
        EventComposite(3, "lab_intro_2_search_office", [lab_intro_2_search_office_storage],
            TimeCondition(weekday = "d", daytime = "d"),
            ProgressCondition("lab_intro", 2),
            ReplayCategoryOption("lab_intro"),
            Pattern("main", "images/events/lab_intro/lab_intro_2/lab_intro_2_office.webp"),
            thumbnail = "images/events/lab_intro/lab_intro_2/lab_intro_2_office.webp"))

label lab_intro_2 (**kwargs):
    $ begin_event(**kwargs)

    # headmaster looks for some lab equipment in different storage rooms
    # headmaster finds a few tables, chairs, and some other equipment

    $ image = convert_pattern("main", **kwargs)
    
    $ image.show(0)
    subtitles "The smell hits first — mold and old solvent, something chemical that hasn't fully dissipated in thirty years."
    headmaster.think "Hmm, everything is pretty run down."

    call Image_Series.show_image(image, 1, 2) from _call_lab_intro_show_image_1
    headmaster.think "I don't think I can use any of this."

    # headmaster checks a few rooms

    $ image.show(3)
    headmaster.think "Hey, what's that?"

    $ image.show(4)
    headmaster.think "That table seems totally fine! That's perfect!"

    # headmaster calls secretary

    $ image.show(5)
    headmaster.think "Time to get some help."

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
    headmaster.think "Hmm, the gym should have anything useful."

    call composite_event_runner(**kwargs) from lab_intro_2_search_gym_composite_event_runner

label lab_intro_2_search_gym_1 (**kwargs):
    $ begin_event(**kwargs)

    # headmaster searches the gym for some equipment
    # headmaster finds a bra, but nothing useful for his lab

    

    $ show_pattern("main", **kwargs)
    headmaster.think "Whose bra is this? And why is it in the equipment room?! Mhh, who cares."

    $ inventory_manager.add_item("generic_bra")

    $ end_event("new_daytime", **kwargs)

label lab_intro_2_search_gym_2 (**kwargs):
    $ begin_event(**kwargs)


    $ show_pattern("main", **kwargs)
    headmaster.think "Nothing useful here."

    $ end_event("new_daytime", **kwargs)


label lab_intro_2_search_cafeteria (**kwargs):
    $ begin_event(**kwargs)


    $ show_pattern("base", **kwargs)
    headmaster.think "Hmm, the cafeteria should have anything useful."

    call composite_event_runner(**kwargs) from lab_intro_2_search_cafeteria_composite_event_runner

label lab_intro_2_search_cafeteria_1 (**kwargs):
    $ begin_event(**kwargs)


    # headmaster searches the cafeteria for some equipment
    # headmaster finds a mortar and pestle

    $ show_pattern("main", **kwargs)
    headmaster.think "Oh, look at that! That's a mortar and pestle! Perfect!"

    $ inventory_manager.add_item(Item("lab_mortar_and_pestle"))

    $ end_event("new_daytime", **kwargs)

label lab_intro_2_search_cafeteria_2 (**kwargs):
    $ begin_event(**kwargs)


    # headmaster searches the cafeteria for some equipment
    # headmaster finds some distilled water and some other liquids

    $ show_pattern("main", **kwargs)
    headmaster.think "Ah, that's a nice looking bottle of distilled water. Perfect!"

    $ inventory_manager.add_item(Item("lab_distilled_water"))

    $ end_event("new_daytime", **kwargs)

label lab_intro_2_search_cafeteria_3 (**kwargs):
    $ begin_event(**kwargs)


    $ show_pattern("main", **kwargs)
    # headmaster searches the cafeteria for some equipment
    # headmaster doesn't find anything useful anymore


    headmaster.think "Nothing useful here."

    $ end_event("new_daytime", **kwargs)


label lab_intro_2_search_dorm (**kwargs):
    $ begin_event(**kwargs)


    $ show_pattern("base", **kwargs)
    headmaster.think "Let's see if the dorm has anything useful."

    call composite_event_runner(**kwargs) from lab_intro_2_search_dorm_composite_event_runner

label lab_intro_2_search_dorm_1 (**kwargs):
    $ begin_event(**kwargs)


    # headmaster searches the dorm for some equipment
    # headmaster finds a mortar and pestle

    $ show_pattern("main", **kwargs)
    headmaster.think "Oh, look at that! That's a mortar and pestle! Perfect!"

    $ inventory_manager.add_item(Item("lab_mortar_and_pestle"))

    $ end_event("new_daytime", **kwargs)

label lab_intro_2_search_dorm_2 (**kwargs):
    $ begin_event(**kwargs)


    # headmaster searches the dorm for some equipment
    # headmaster finds some distilled water and some other liquids

    $ show_pattern("main", **kwargs)
    headmaster.think "Ah, that's a nice looking bottle of distilled water. Perfect!"

    $ inventory_manager.add_item(Item("lab_distilled_water"))

    $ end_event("new_daytime", **kwargs)

label lab_intro_2_search_dorm_3 (**kwargs):
    $ begin_event(**kwargs)


    # headmaster searches the dorm for some equipment
    # headmaster doesn't find anything useful anymore

    $ show_pattern("main", **kwargs)
    headmaster.think "Nothing useful here."

    $ end_event("new_daytime", **kwargs)


label lab_intro_2_search_kiosk (**kwargs):
    $ begin_event(**kwargs)


    $ show_pattern("base", **kwargs)
    headmaster.think "Let's see if the kiosk has anything useful."

    call composite_event_runner(**kwargs) from lab_intro_2_search_kiosk_composite_event_runner

label lab_intro_2_search_kiosk_1 (**kwargs):
    $ begin_event(**kwargs)


    # headmaster looks for some equipment at the kiosk
    # headmaster finds some glassware and some utensils

    $ image = convert_pattern("main", **kwargs)

    $ image.show(0)
    headmaster.think "Ahh, I could use this set of glassware."

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
    headmaster.think "Nothing useful here."

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
    hatano "{i}They{/i} wanted to go camping. Don't look at me — I'm not the one who packed a gas burner into her bag."
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
    hatano "Ugh, {i}finally{/i}. Do you have any idea what twenty minutes in wet grass does to a skirt like this?"
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
    headmaster.think "Nothing useful here."

    $ end_event("new_daytime", **kwargs)


label lab_intro_2_search_school (**kwargs):
    $ begin_event(**kwargs)

    $ show_pattern("main", **kwargs)
    headmaster.think "Let's check the classrooms."

    call composite_event_runner(**kwargs) from lab_intro_2_search_school_composite_event_runner

label lab_intro_2_search_school_1 (**kwargs):
    $ begin_event(**kwargs)

    # headmaster looks for some equipment in the school
    # headmaster finds some labels and some small office supplies

    $ image = convert_pattern("main", **kwargs)

    headmaster.think "Ah, a lot of office supplies here!"
    headmaster.think "I could use this for my lab."

    $ inventory_manager.add_item(Item("lab_office_supplies"))

    $ end_event("new_daytime", **kwargs)

label lab_intro_2_search_school_2 (**kwargs):
    $ begin_event(**kwargs)

    # headmaster looks for some equipment in the school
    # headmaster doesn't find anything else useful in the school

    headmaster.think "Nothing useful here."

    $ end_event("new_daytime", **kwargs)


label lab_intro_2_search_office (**kwargs):
    $ begin_event(**kwargs)

    headmaster.think "Let's check the office."
    call composite_event_runner(**kwargs) from lab_intro_2_search_office_composite_event_runner

label lab_intro_2_search_office_1 (**kwargs):
    $ begin_event(**kwargs)

    # headmaster looks for some equipment in the office
    # headmaster finds a a label maker and some small office supplies

    headmaster.think "Ah, a label maker! Perfect!"

    $ inventory_manager.add_item(Item("lab_office_supplies"))

    $ end_event("new_daytime", **kwargs)

label lab_intro_2_search_office_2 (**kwargs):
    $ begin_event(**kwargs)

    # headmaster looks for some equipment in the office
    # headmaster doesn't find anything else useful in the office
    
    headmaster.think "Nothing useful here."

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
            Pattern("main", "images/events/lab_intro/lab_intro_3/lab_intro_3 <step>.webp"),
            thumbnail = "images/events/lab_intro/lab_intro_3/lab_intro_3 6.webp"))

# all equipment needs to be found and purchased
label lab_intro_3 (**kwargs):
    $ begin_event(**kwargs)

    $ image = convert_pattern("main", **kwargs)

    # headmaster starts setting up a makeshift lab in the office

    $ image.show(0)
    headmaster.think "Let's start setting up the lab."
    subtitles "The storage room smells like dust and old ink. The desk surface is gritty under his palms."
    headmaster.think "I should start with recreating the base potion."

    # multiple shots of the headmaster setting up the lab 
    call Image_Series.show_image(image, 1, 2, 3, 4, 5) from _call_show_image_lab_intro_3_1
    headmaster.think "Now I can start experimenting with the equipment."
    $ image.show(6)
    headmaster.think "I should start with recreating the base potion."

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
            Pattern("main", "images/events/lab_intro/lab_intro_4/lab_intro_4 <step>.webp"),
            thumbnail = "images/events/lab_intro/lab_intro_4/lab_intro_4 0.webp"))

label lab_intro_4 (**kwargs):
    $ begin_event(**kwargs)

    $ image = convert_pattern("main", **kwargs)

    $ image.show(0)
    subtitles "The vial is warm from being in his pocket all morning. The liquid inside is amber — darker than expected, catching the desk lamp like old honey."

    headmaster.think "Alright. Let's get to work."
    $ image.show(1)
    headmaster.think "I should check my notes first..."
    $ image.show(2)
    headmaster.think "Where is the notebook? I had it just before..."
    $ image.show(3)
    headmaster.think "Damn. I must have left it somewhere."
    $ image.show(4)
    headmaster.think "I'll have to manage without it for now. Let's start analyzing the potion."

    # shots of the headmaster analyzing the potion
    call Image_Series.show_image(image, 5, 6) from _call_show_image_lab_intro_4_1
    headmaster.think "Okay, I think I have a good idea of what to do."
    call Image_Series.show_image(image, 7, 8, 9) from _call_show_image_lab_intro_4_2
    headmaster.think "Now let's try to recreate the potion."

    call Image_Series.show_image(image, 10, 11) from _call_show_image_lab_intro_4_3
    subtitles "The smell is wrong at first — sharp, almost medicinal. He adjusts the ratio. Tries again."

    ## 3 hours later...
    $ image.show(12)
    headmaster.think "Hmm, I could only make these vials. I need to figure out how to make more."
    headmaster.think "I need to think about it a bit more. I should try it myself first — just in case there are any side effects."
    $ image.show(13)
    headmaster.think "Okay, here goes nothing..."

    subtitles "It tastes like copper with something sweet fighting underneath — not pleasant, not chemical, just wrong in a way he can't name yet."
    $ image.show(14)
    headmaster.think "Hmm, I definitely need to work on the taste..."
    $ image.show(15)
    headmaster.think "No side effects so far. But it's too early to say."
    $ image.show(16)
    headmaster.think "I'll stop here for today. Let's see what tomorrow brings."

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
            Pattern("main", "images/events/lab_intro/lab_intro_5/lab_intro_5 <step>.webp"),
            thumbnail = "images/events/lab_intro/lab_intro_5/lab_intro_5 0.webp"),
    )

label lab_intro_5 (**kwargs):
    $ begin_event(**kwargs)

    $ image.show(0)
    subtitles "It's morning. The lab smell has seeped into his clothes overnight."

    $ image.show(1)
    headmaster.think "I seem to be fine. I don't feel any effects yet."
    headmaster.think "Though... I don't feel any effect at all."

    $ image.show(2)
    headmaster.think "Maybe I'm just not susceptible to it. Nothing for me to be conditioned toward..."
    headmaster.think "The formula works on inhibition — on suppressed desire. If there's nothing there to suppress in the first place..."
    headmaster.think "Maybe it only works on women."

    $ image.show(3)
    headmaster.think "At any rate — no adverse effects. The formula is sound. Time to move forward."

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
            Pattern("main", "images/events/lab_intro/lab_intro_6/lab_intro_6 <step>.png"),
            thumbnail = "images/events/lab/lab_intro_6/lab_intro_6 0.webp")
    office_building_call_secretary_events["talk"].add_event(lab_intro_6_event)

label lab_intro_6 (**kwargs):
    $ begin_event(**kwargs)

    $ image = convert_pattern("main", **kwargs)

    $ secretary_person = Person["emiko_langley"]
    $ secretary_person.register_paperdoll()
    $ paperdoll_manager.set_background("images/background/office building/f.webp", blur = True)
    $ secretary_person.display(PDAImage(pose = "12", outfit = "uniform", level = 6, mood = "suprised", mouth = "open"),
        PDAPreset("upper_body", duration = 0.0),
        PDAPreset("outside", duration = 0.0)
    )

    headmaster "Emiko! There you are — I did it. I recreated it. The prototype's stable."
    $ secretary_person.display(PDAPreset("close_body_center", duration = 1.0))
    emiko "Hello to you too. That's the good kind of manic face, I hope."
    $ secretary_person.display(PDAImage(pose = "12", mood = "neutral", mouth = "closed"))
    headmaster "A prototype. I've already taken a dose myself — no ill effects. But before it goes anywhere near anyone else, I want a second reading. Would you?"
    $ secretary_person.display(PDAImage(pose = "19", mood = "happy", mouth = "open"))
    emiko "If you made it, I'll drink it. Hand it over."

    $ secretary_person.clear_display()

    $ image.show(0)
    headmaster "Great! Here you go."
    $ image.show(1)
    subtitles "The potion has a sweet, faintly floral smell. The kind of smell that sticks to the back of the throat."
    call Image_Series.show_image(image, 2, 3, 4, 5) from _call_show_image_lab_intro_6_1
    headmaster "How do you feel?"

    $ image.hide()
    $ paperdoll_manager.set_background("images/background/office building/secretary 6 1 0.webp", blur = True)
    $ secretary_person.display(PDAImage(pose = "21", mood = "neutral", mouth = "open"))
    emiko "Hmm... a little warmer, maybe? Honestly — barely anything at all."
    $ secretary_person.display(PDAImage(pose = "10", mood = "neutral", mouth = "closed"))
    subtitles "Silence. Just the faint hum of the ventilation and the sound of his own breathing."
    $ secretary_person.display(PDAImage(pose = "10", mood = "happy", mouth = "closed"))
    headmaster "Figures. After what the original did to you, there's not much left in you for a diluted batch to stir — so your reading tells me almost nothing about a fresh subject. I'll need a cleaner test."
    $ secretary_person.display(PDAImage(pose = "10", mood = "happy", mouth = "open"))
    emiko "Then be careful — with the dose, and with whoever you give it to. This is supposed to help them, remember."
    $ secretary_person.display(PDAImage(pose = "10", mood = "happy", mouth = "closed"),
        PDAPreset("outside", duration = 1.0), PDAPause(duration = 1.0))
    $ image.show(6)
    headmaster.think "She's right. Carefully, then. First — I need to produce more."

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
            Pattern("main", "images/events/lab_intro/lab_intro_3/lab_intro_3 <step>.webp")))

    office_building_lab_events["produce"].add_event(
        Event(3, "lab_intro_produce_test_potion",
            TimeCondition(weekday = "d", daytime = "d"),
            ProgressCondition("lab_intro", "6,7"),
            ItemCondition("lab_chemicals"),
            NOT(ItemCondition("lab_test_potion")),
            ReplayCategoryOption("lab_intro"),
            Pattern("main", "images/events/lab_intro/lab_intro_produce_test_potion/lab_intro_produce_test_potion <step>.webp"),
            thumbnail = "images/events/lab/lab_intro_produce_test_potion/lab_intro_produce_test_potion 0.webp"),
        Event(3, "lab_intro_produce_test_potion_no_chemicals",
            TimeCondition(weekday = "d", daytime = "d"),
            ProgressCondition("lab_intro", "6,7"),
            NOT(ItemCondition("lab_chemicals")),
            NOT(ItemCondition("lab_test_potion")),
            ReplayCategoryOption("lab_intro"),
            Pattern("main", "images/events/lab_intro/lab_intro_produce_test_potion/lab_intro_produce_test_potion <step>.webp"),
            thumbnail = "images/events/lab_intro/lab_intro_produce_test_potion/lab_intro_produce_test_potion 0.webp"),
    )


label lab_intro_produce_test_potion (**kwargs):
    $ begin_event(**kwargs)

    # shots of headmaster producing more potions
    headmaster.think "I definitely have to improve the process in the future."
    headmaster.think "There is just too much chemicals wasted..."

    $ inventory_manager.remove_item("lab_chemicals", 1)
    $ inventory_manager.add_item("lab_test_potion")

    $ end_event("new_daytime", **kwargs)

label lab_intro_produce_test_potion_no_chemicals (**kwargs):
    $ begin_event(**kwargs)

    # shots of headmaster producing more potions
    headmaster.think "I don't have any chemicals left. I first have to buy some more."

    $ end_event("new_daytime", **kwargs)

# endregion
######################################

# ###########################
# region Lab Intro 7 Events #

init 2 python: 
    set_current_mod('base')

    sb_events["patrol"].add_event(
        Event(3, "lab_intro_7",
            TimeCondition(weekday = "d", daytime = "d"),
            ProgressCondition("lab_intro", 6),
            ItemCondition("lab_test_potion"),
            ReplayCategoryOption("lab_intro"),
            Pattern("main", "images/events/lab_intro/lab_intro_7/lab_intro_7 <step>.webp"),
            thumbnail = "images/events/lab_intro/lab_intro_7/lab_intro_7 0.webp"),
    )

label lab_intro_7 (**kwargs):
    $ begin_event(**kwargs)

    $ sakura = Person["sakura_mori"]
    $ easkey = Person["easkey_tanaka"]

    $ image = convert_pattern("main", **kwargs)

    call Image_Series.show_image(image, 0, 1) from _call_show_image_lab_intro_7_1
    headmaster "Ahh Ms. Mori. I accidentally bought two cans of soda. I only need one. Do you want one?"
    $ image.show(2)
    sakura "Sure, that would be great. Thank you very much!"
    $ image.show(3)
    headmaster "Here you go."

    # Sakura drinks the potion
    call Image_Series.show_image(image, 4, 5) from _call_show_image_lab_intro_7_2
    sakura "Mmm, it kinda tastes weird..."
    $ image.show(6)
    headmaster "Oh, the can fell down earlier. Sorry, I guess some of the fizz got lost..."

    $ image.show(7)
    sakura "It's okay, it still tastes good."
    $ image.show(8)
    headmaster "Great! Then, I'll see you later!"
    $ image.show(9)
    sakura "Thank you very much!"

    # The headmaster goes around the corner and secretly checks on Sakura.
    call Image_Series.show_image(image, 10, 11, 12, 13) from _call_show_image_lab_intro_7_3
    sakura "Oh my God! It's so warm! Don't you think so?"
    $ image.show(14)
    easkey "What? I think it might be a little cold. What's wrong, Sakura?"
    $ image.show(15)
    easkey "Are you okay?"
    $ image.show(16)
    sakura "No, I'm fine. I feel pretty good actually, but it is sooo warm!"

    # Sakura opens her blouse
    $ image.show(17)
    sakura "Ahh! Much better!"
    $ image.show(18)
    easkey "Sakura! What are you doing?!"
    $ image.show(19)
    sakura "Huh? What? I'm just trying to cool off. It's so warm!"
    $ image.show(20)
    easkey "But you can't just undress in public!"
    $ image.show(21)
    sakura "What do you mean..."
    $ image.show(22)
    sakura "Huh?! Why is my blouse open?!"
    easkey "I... I don't know! You just opened it!"
    $ image.show(23)
    sakura "What?! No! Help me close it!"

    $ image.show(24)
    headmaster.think "Hmm, that's interesting. It seems to work well for her."
    $ image.show(25)
    headmaster.think "I wonder why it had no effect on Emiko... Maybe she needs a higher dose due to the effect of the original potion..."
    headmaster.think "Hmm, but then she would've been more susceptible to this potion. Technically, these potions should enhance the effects..."
    $ image.show(26)
    headmaster.think "I should try it with other students to see if it works for them. Maybe I should also try a higher dose on Emiko."
    
    $ image.show(27)
    headmaster.think "So that's the whole picture — the heat, the way she stopped watching herself, the inhibitions just dropping away. And afterward, gaps where the memory should be."
    headmaster.think "It doesn't hold long — a few minutes, maybe. But it works. It actually works."
    
    # headmaster goes away
    call Image_Series.show_image(image, 28, pause = True) from _call_show_image_lab_intro_7_4

    $ set_progress("lab_intro", 7)

    $ end_event("new_daytime", **kwargs)

# endregion
# ###########################

# ###########################
# region Lab Intro 8 Events #

init 2 python: 
    set_current_mod('base')

    office_building_events["look_around"].add_event(
        Event(3, "lab_intro_8",
            TimeCondition(weekday = "d", daytime = "f"),
            ProgressCondition("lab_intro", 7),
            ItemCondition("lab_test_potion"),
            ReplayCategoryOption("lab_intro"),
            Pattern("main", "images/events/lab_intro/lab_intro_8/lab_intro_8 <step>.webp"),
            thumbnail = "images/events/lab_intro/lab_intro_8/lab_intro_8 0.webp"),
    )

label lab_intro_8 (**kwargs):
    $ begin_event(**kwargs)

    $ zoe = Person["zoe_parker"]
    $ finola = Person["finola_ryan"]

    $ image = convert_pattern("main", **kwargs)

    call Image_Series.show_image(image, 0, 1, 2, 3) from _call_show_image_lab_intro_8_1
    headmaster.think "Hmm, the teachers should be back in a few minutes. I could put the potion in their coffee."

    # Headmaster Put's Potion in Coffee
    call Image_Series.show_image(image, 4, 5) from _call_show_image_lab_intro_8_2
    headmaster.think "Now to wait..."
    # Teachers arrive
    $ image.show(6)
    zoe "Good morning, [headmaster_first_name]!"
    zoe "Can I help you with something?"
    $ image.show(7)
    headmaster "Ah, Mrs. Parker. No thanks, I just thought I could work here. You know, get a little closer to the staff."
    $ image.show(8)
    zoe "Ah, that's great! I'm going to get some coffee."
    $ image.show(9)
    headmaster "You do that. I'll be here."
    zoe "All right, see you later!"
    
    # Zoe goes to the coffee machine
    # Finola also gets some coffee.
    call Image_Series.show_image(image, 10, 11, 12, 13) from _call_show_image_lab_intro_8_3
    # Both talk to each other while drinking
    finola "Oh man, it's getting really warm in here."
    $ image.show(14)
    zoe "Yes. I feel it too."
    $ image.show(15)
    finola "I think... I'm beginning to feel something..."
    $ image.show(16)
    zoe "Is everything okay?"
    $ image.show(17)
    finola "Sorry, I think I need to go to the bathroom."
    zoe "Oh, okay."
    # Finola rushes off
    $ image.show(18)
    zoe "Wow, it's getting really hot in here."
    # zoe takes off jacket
    # Finola comes back in different clothes
    call Image_Series.show_image(image, 19, 20) from _call_show_image_lab_intro_8_4
    zoe "Finola! Are you all right?"
    $ image.show(21)
    finola "Yeah, I'm fine. I just need to cool off a bit."
    $ image.show(22)
    finola "Luckily I had some other clothes here. This is a little more comfortable."
    $ image.show(23)
    zoe "Yes, I see. That top looks great on you. You should wear it more often!"
    $ image.show(24)
    finola "I don't know, it shows a little too much..."
    $ image.show(23)
    zoe "Oh, come on — you've got a lovely figure. There's no shame in letting it show a little."
    $ image.show(24)
    finola "Do you think so? I'm not sure..."
    $ image.show(23)
    zoe "Of course. You should feel good in your own skin — that's all I mean."
    $ image.show(24)
    finola "I'll think about it..."
    $ image.show(25)
    zoe "No pressure. I just think you deserve to feel comfortable."

    # A few moments pass
    $ image.show(26)
    finola "Wait..." 
    # Finola looks down at her outfit, confusion crossing her face
    $ image.show(27)
    finola "Why did I... I need to change back. This is completely inappropriate for work."

    subtitles "The faculty lounge smells like burnt coffee and something sweeter underneath — faint, already fading."
    headmaster.think "Five minutes. Maybe less. They snap back every time."
    headmaster.think "I need a catalyst."

    $ set_progress("lab_intro", 8)

    $ end_event("new_daytime", **kwargs)

# endregion
# ###########################

# ###########################
# region Lab Intro 9 Events #

init 2 python: 
    set_current_mod('base')

    office_building_events["look_around"].add_event(
        Event(3, "lab_intro_9",
            TimeCondition(weekday = "d", daytime = "f"),
            ProgressCondition("lab_intro", 8),
            ItemCondition("lab_test_potion"),
            ReplayCategoryOption("lab_intro"),
            Pattern("main", "images/events/lab_intro/lab_intro_9/lab_intro_9 <step>.webp"),
            thumbnail = "images/events/lab_intro/lab_intro_9/lab_intro_9 0.webp"),
    )

# Chemical Mishap
label lab_intro_9 (**kwargs):
    $ begin_event(**kwargs)

    $ ishimaru = Person["ishimaru_maki"]

    $ image = convert_pattern("main", **kwargs)

    $ image.show(0)
    headmaster.think "I should test another dose on the students. See if the response varies by individual."
    
    # headmaster bumps into student cleaning the hallway
    call Image_Series.show_image(image, 1, 2) from _call_show_image_lab_intro_9_1
    headmaster "Oh—!"
    
    # student's bucket tips, spilling cleaning solution across the floor
    # headmaster's potion vial slips from his hand and shatters in the puddle
    
    $ image.show(3)
    headmaster.think "Damn it."
    
    $ image.show(4)
    headmaster "My apologies, are you alright?"
    $ image.show(5)
    ishimaru "I'm fine, Mr. [headmaster_last_name]! I'm so sorry, I'll clean this up right away."
    $ image.show(6)
    headmaster "I'm sorry, I should have been more careful."
    
    $ image.show(7)
    headmaster.think "There goes one dose. I'll have to synthesize more tonight."
    
    # headmaster walks away
    
    # vapor begins rising from the mixture where potion and cleaning chemicals merged 
    
    $ image.show(8)
    headmaster.think "Huh... what's that smell?"
    headmaster.think "Actually... that smells really nice. Kinda sweet?"
    
    # The classroom door down the hall is open
    # Vapor drifts naturally toward the doorway where Luna, Lin, and Gloria are visible inside talking
    
    $ set_progress("lab_intro", 9)

    $ end_event("new_daytime", **kwargs)

# endregion
# ###########################

# ############################
# region Lab Intro 10 Events #

init 2 python: 
    set_current_mod('base')

    office_building_events["look_around"].add_event(
        Event(3, "lab_intro_10",
            TimeCondition(weekday = "d", daytime = "f"),
            ProgressCondition("lab_intro", 8),
            ItemCondition("lab_test_potion"),
            ReplayCategoryOption("lab_intro"),
            Pattern("main", "images/events/lab_intro/lab_intro_10/lab_intro_10 <step>.webp"),
            thumbnail = "images/events/lab_intro/lab_intro_10/lab_intro_10 0.webp"),
    )

# Investigation unlocks after Chemical Mishap
label lab_intro_10 (**kwargs):
    $ begin_event(**kwargs)

    $ gloria = Person["gloria_goto"]
    $ lin = Person["lin_kato"]
    $ luna = Person["luna_clark"]
    $ ishimaru = Person["ishimaru_maki"]

    $ image = convert_pattern("main", **kwargs) 

    call Image_Series.show_image(image, 0, 1) from _call_show_image_lab_intro_10_1
    headmaster.think "That smell from earlier. It's still lingering in this hallway."
    headmaster.think "I should check if there are any unexpected effects from the spill."
    
    $ image.show(2)
    headmaster.think "That's odd. Class shouldn't be in session now."
    
    $ image.show(3)
    headmaster "Girls? Is everything—"
    
    $ image.show(4)
    gloria "Mr. [headmaster_last_name]! Perfect timing, come sit with us!"
    headmaster.think "What in the world...?"
    
    $ image.show(5)
    headmaster "Are you girls alright? You look..."
    lin "We're fantastic! Better than alright, honestly."
    
    $ image.show(6)
    gloria "We were just comparing bras. Look how cute Lin's is!"
    
    $ image.show(7)
    lin "It's new! Got it last week. The white trim is adorable, right?"
    headmaster "Yes, very... nice."
    headmaster.think "They're showing me their underwear like it's the most natural thing in the world. No hesitation, no embarrassment."
    
    $ image.show(8)
    gloria "Now mine—tell me honestly, is the black too much? I thought it looked sophisticated."
    
    $ image.show(9)
    headmaster "It's... elegant. Suits you."
    
    $ image.show(10)
    gloria "Oh thank you! See, I told you guys it wasn't too grown-up."
    
    $ image.show(11)
    lin "Okay, okay, your turn now Luna!"
    
    $ image.show(12)
    luna "No way. Not in front of Mr. [headmaster_last_name]."
    
    $ image.show(13)
    lin "Oh come on! We both showed ours!"
    
    $ image.show(14)
    gloria "Don't be shy! We're all being open here."
    
    $ image.show(15)
    luna "But I'm not wearing—"
    
    $ image.show(16)
    lin "Come on, Luna!"
    
    $ image.show(17)
    luna "Fine. But don't make it weird."
    gloria "We won't!"
    
    call Image_Series.show_image(image, 18, 19) from _call_show_image_lab_intro_10_2
    gloria "WOAH!"
    lin "Luna! You're not wearing anything?"
    
    $ image.show(20)
    luna "I've never worn one. Mum says bras aren't healthy."
    
    $ image.show(21)
    gloria "Huh. Really?!"
    
    $ image.show(22)
    luna "Mr. [headmaster_last_name], you think they're nice?"
    
    $ image.show(23)
    headmaster "I—yes, they're lovely. But I should really be going now."
    headmaster.think "Christ. She's standing there topless asking my opinion like we're discussing the weather."
    headmaster.think "What happened in here? Girls test boundaries, sure, But not like this. This wasn't them. Something did this to them."
    lin "Aww, already? We're having fun!"
    
    $ image.show(24)
    headmaster "I'll see you girls in class. Make sure to... button up before anyone else comes by."
    gloria "Okay, okay. Bye Mr. [headmaster_last_name]!"
    luna "Gloria, don't touch them!"
    gloria "I just want to see if they feel different without a bra!"
    
    $ image.show(25)
    headmaster.think "That smell. What is that?"

    $ image.show(26)
    headmaster.think "It's everywhere in there. Sweet, but not perfume. Something sharper underneath."
    
    $ image.show(27)
    ishimaru "Mr. [headmaster_last_name]!"
    headmaster "Ms. Maki! What happened to your top?"
    
    $ image.show(28)
    ishimaru "Got it dirty while cleaning the spill. Easier to just take it off than walk around with stains."
    ishimaru "There was a broken vial. I picked it up,"
    
    $ image.show(29)
    headmaster "Yes, thank you. It... broke?"
    
    $ image.show(30)
    ishimaru "It must've when it fell. I tried to clean it up but the liquid had already mixed with the cleaning solution."
    headmaster.think "The cleaning solution."
    
    $ image.show(31)
    ishimaru "There was this really nice smell after. Kind of sweet? I've been smelling it all afternoon."
    
    $ image.show(32)
    ishimaru "You smell nice too, Mr. [headmaster_last_name]. Is that cologne?"
    
    $ image.show(33)
    headmaster "I... don't wear cologne."
    
    $ image.show(31)
    ishimaru "Huh. Well, something smells really good."
    
    $ image.show(34)
    headmaster "You can throw the glass away. I don't need it anymore."
    
    $ image.show(35)
    ishimaru "Okay. See you later..."
    
    $ image.show(36)
    headmaster.think "The cleaning solution. The girls in the classroom. Ishimaru just now."
    headmaster.think "They all have that same look. That same lack of inhibition."
    headmaster.think "And that smell—it's the same one in the classroom. Stronger near where the spill happened."
    headmaster.think "Something in those cleaning chemicals reacted with the potion — it has to be. But which one?"
    
    $ set_progress("lab_intro", 10)
    
    $ end_event("new_daytime", **kwargs)

# endregion
# ############################

##############################
# region Lab Intro 11 Events #

init 2 python:
    set_current_mod('base')

    # Analysis debrief — Headmaster calls Emiko in to talk it through. Pure
    # dialogue in the office, so it runs entirely on Emiko's paperdoll over the
    # blurred office background (f.webp — the empty plate of the secretary view,
    # no baked-in Emiko, so the overlaid paperdoll can't double her). No bespoke
    # CGs, hence no Pattern. Gated behind the Investigation (lab_intro 10).
    # Registered on the "call secretary → talk" action, same as lab_intro_6.
    lab_intro_11_event = Event(3, "lab_intro_11",
            TimeCondition(weekday = "d", daytime = "d"),
            ProgressCondition("lab_intro", 10),
            ReplayCategoryOption("lab_intro"),
            thumbnail = "images/background/office building/secretary 6 1 0.webp")
    office_building_call_secretary_events["talk"].add_event(lab_intro_11_event)

# Analysis unlocks after Investigation
label lab_intro_11 (**kwargs):
    $ begin_event(**kwargs)

    $ emiko.register_paperdoll()
    $ paperdoll_manager.set_background("images/background/office building/f.webp", blur = True)

    subtitles "Late afternoon. The sun has dropped far enough to come in sideways, laying a bar of orange across the desk and the papers scattered over it."
    subtitles "The office still smells faintly of the lab — that sweet, chemical undertone riding under the old-paper and cold-coffee of the room."
    headmaster.think "The smell. The behaviour. The timing. Every thread of it runs back to that spill in the hallway."

    # Emiko lets herself in after the token courtesy of a knock — folder under one
    # arm, already halfway through the door.
    $ emiko.display(PDAImage(pose = "10", outfit = "uniform", level = 6, mood = "neutral", mouth = "closed"),
        PDAPreset("close_body_center", duration = 0.0),
        PDAPreset("outside", duration = 0.0))
    subtitles "A single perfunctory knock, and the door's already opening. Emiko, folder tucked under one arm, catches the look on his face and stops just inside."

    headmaster "Emiko! Perfect timing."
    $ emiko.display(PDAImage(pose = "36", mood = "happy", mouth = "open"),
        PDAPreset("close_body_center", duration = 1))
    emiko.say "You've got the face of a man who's had an eventful day. Do I want the good version of that, or the version where I start rescheduling your evening?"

    $ emiko.display(PDAImage(mood = "neutral", mouth = "closed"))
    headmaster "Eventful is one word for it. I think I've made a breakthrough."
    $ emiko.display(PDAImage(pose = "19", mood = "suprised", mouth = "open"))
    emiko.say "Oh?"
    emiko.think "*He's practically vibrating. Whatever this is, he's been sitting on it since I passed his door this morning.*"

    $ emiko.display(PDAImage(pose = "7", mood = "happy", mouth = "closed"))
    headmaster "Remember the vial I dropped in the hallway? When I bumped into Ms. Maki?"
    $ emiko.display(PDAImage(mouth = "open"))
    emiko.say "You mentioned it. Broken glass and a bad morning, the way you told it."
    $ emiko.display(PDAImage(mouth = "closed"))
    headmaster "I went back to look the area over. Found three girls in a classroom — blouses open, showing each other their bras like it was show-and-tell."
    headmaster "One of them wasn't even wearing one. Just opened her shirt and asked my honest opinion. Though a bit hesitant, she still showed hers off."
    $ emiko.display(PDAImage(pose = "17", mood = "shining", mouth = "open"))
    emiko.say "That's a long way from your earlier results. The last batch barely got a giggle out of anyone before it wore off."

    $ emiko.display(PDAImage(mouth = "closed"))
    headmaster "Exactly. The early doses were nothing — minutes, and then they'd snap back, embarrassed, none the wiser."
    headmaster "These girls had been like that a quarter of an hour, maybe longer, by the time I walked in on them."
    $ emiko.display(PDAImage(pose = "2", mood = "happy", mouth = "open"))
    emiko.say "And Ms. Maki? She's the one you collided with when the vial went down."
    $ emiko.display(PDAImage(mouth = "closed"))

    subtitles "He pauses. A little colour comes up in his face before he answers."
    headmaster "Topless. Said she'd taken her top off cleaning because it got dirty — perfectly reasonable, the way she framed it."
    headmaster "Then she got close. Hand on my arm, telling me how good I smelled."
    $ emiko.display(PDAImage(pose = "27", mood = "shining", mouth = "open"))
    emiko.say "So — flirting."
    $ emiko.display(PDAImage(mouth = "closed"))
    headmaster "Blatantly. Without a shred of the woman who files my correspondence."

    $ emiko.display(PDAImage(pose = "7", mood = "neutral", mouth = "open", look = "avert"))
    emiko.say "Multiple subjects. Stronger. Longer. Something out in that hallway was different from anything you've ever cooked up in that closet you call a lab."
    emiko.think "*Whatever happened out there is leagues past the first batch. And look at him — colour in his face, up out of the chair. He hasn't been this alive in weeks. I'm not letting this fizzle out.*"

    $ emiko.display(PDAImage(mouth = "closed", look = "follow"))
    headmaster "The smell. That's what was different."
    $ emiko.display(PDAImage(mouth = "open"))
    emiko.say "The smell?"
    $ emiko.display(PDAImage(mouth = "closed"))
    headmaster "In the classroom, near the spill — sweet, almost floral, with something chemical underneath. Ishimaru noticed it. The girls noticed it. Every one of them said it smelled {i}good{/i}."

    # She drifts toward the window, thinking it through in the low light.
    $ emiko.display(PDAMove(alignX = "+0.5", duration = 1.0))
    subtitles "She crosses to the window, the low sun catching the side of her face, and turns it over for a moment before she speaks."
    $ emiko.display(PDAImage(mouth = "open", look = "avert"))
    emiko.say "You think something reacted with the potion."
    $ emiko.display(PDAImage(mouth = "closed"))
    headmaster "It has to be. The vial broke in the spill — Ishimaru said the liquid had already mixed into the cleaning solution before she got to it."

    headmaster "The implications are staggering. If I can isolate which compound triggered that reaction..."
    $ emiko.display(PDAImage(pose = "21", mood = "shining", mouth = "open", look = "follow"),
        PDAPreset("close_body_center", duration = 1))
    emiko.say "Then you'd have a catalyst. Something that makes it {i}hold{/i}... permanent, instead of a few borrowed minutes and a girl who wakes up mortified."
    $ emiko.display(PDAImage(pose = "7", mood = "neutral", mouth = "closed"))
    headmaster "Exactly."

    subtitles "The bar of light on the desk has narrowed to a thread. The excitement goes out of him a little, shoulders dropping."
    headmaster "But I have to test it properly. Controlled. Documented. And I've already burned through most of my supply on those early tosses of the dice."
    emiko.say "Mm."
    emiko.think "*He's been carrying every ounce of this alone, and it's starting to show around his eyes. He doesn't have to. Whatever he needs to keep going — more supply, more room, more hands — I'll put it in front of him before he thinks to ask.*"

    subtitles "She lifts the folder off the desk, the professional smile sliding back into place like a light switched on."
    $ emiko.display(PDAImage(pose = "6", mood = "shining", mouth = "open"))
    emiko.say "Call it a day. Sleep on it, come back at it fresh — you think better after actual sleep, whatever you like to tell yourself."
    $ emiko.display(PDAImage(mood = "happy", mouth = "closed"))
    headmaster "You're right. I need to think this through carefully."
    $ emiko.display(PDAImage(mood = "shining", mouth = "open"))
    emiko.say "We'll figure it out. We always do."

    $ emiko.display(PDAImage(mood = "neutral"))
    emiko.say "And [headmaster_first_name]... this is important work. Don't lose sight of that."
    $ emiko.display(PDAImage(mood = "happy", mouth = "closed"))
    headmaster "I won't."
    emiko.think "*He looks at this like he has to fix the whole school by himself. He doesn't. I'll help him see that tomorrow.*"

    $ emiko.display(PDAImage(pose = "39"),
        PDAMove(alignX = 1.5, duration = 1.0),
        PDAPause(duration = 1.0))

    headmaster.think "A catalyst. Permanent. She had the word out before I did — like she'd already run the whole board three moves ahead of me."

    $ set_progress("lab_intro", 11)

    $ end_event("new_daytime", **kwargs)

# endregion
##############################

##############################
# region Lab Intro 12 Events #

init 2 python:
    set_current_mod('base')

    # Frustration — Headmaster works late in the storage room lab, trying to
    # isolate the catalyst. Pure dialogue, so it runs entirely on Emiko's paperdoll
    # over the blurred lab background (lab_intro_3 6). No bespoke CGs, hence no
    # Pattern. Gated behind the Analysis (lab_intro 11). Registered on the "call
    # secretary → talk" action, same as lab_intro_6.
    lab_intro_12_event = Event(3, "lab_intro_12",
            TimeCondition(weekday = "d", daytime = "d"),
            ProgressCondition("lab_intro", 11),
            ReplayCategoryOption("lab_intro"),
            thumbnail = "images/events/lab_intro/lab_intro_3/lab_intro_3 6.png")
    office_building_call_secretary_events["talk"].add_event(lab_intro_12_event)

# Frustration unlocks after Analysis and Secretary's Spin
label lab_intro_12 (**kwargs):
    $ begin_event(**kwargs)

    # SCENE · lab_intro_12
    # Late evening in the storage-room lab next to the office. The janitor's
    # cleaning cart is wedged in between the shelves and the lab table, its
    # bottles lined up on the table. A rack of small test tubes, the base potion
    # in a stoppered flask, an open notebook with a column of chemical names.
    # He works in goggles and gloves.

    subtitles "The storage room is too small for the cleaning cart. He's had to wedge it in sideways between the shelving and the lab table, and now every bottle on it is lined up in a row under the bare bulb."
    subtitles "It smells like lemon floor cleaner, old dust, and the faint sweetness of the base potion cooling in its flask."

    headmaster.think "Right. One at a time. Everything on that cart, one drop each, and I write down every single result. Even the boring ones. {i}Especially{/i} the boring ones."

    # He pipettes a little base potion into a test tube, ammonia bottle open beside it.
    headmaster "Ammonia, household strength. One drop into two millilitres of base, and..."

    # Nothing happens. Amber stays amber.
    headmaster "...nothing. No colour shift, no precipitate, not even a polite fizz."
    headmaster.think "Rude. Okay. Crossed off."

    # Fresh tube, next bottle.
    headmaster "Industrial surfactant blend. Fatty alcohol ethoxylates, if the label's honest, which labels usually aren't..."

    # The sample clouds up, then slowly settles back to clear amber.
    headmaster "Oh, look at that, it's clouding— no. No, that's just micelles. It's making a little emulsion and giving up. Pretty. Useless."
    headmaster.think "Two down. How many bottles are on this thing? ...Don't count. Counting makes it worse."

    # Next bottle: sodium hypochlorite. He's warming up now, talking to the shelf.
    headmaster "Hypochlorite next. Now, hypochlorite's a strong oxidiser, so if the active fraction has anything electron-rich in it at all, and it must, given how fast it breaks down once it's out of the vial, then you'd expect either a colour loss or some kind of—"

    # TIME SKIP: two hours. Same spot, more tubes, cold coffee, notebook full of crossings-out.
    subtitles "Two hours later."

    headmaster "—which is why, honestly, you'd want to rule out the quaternary ammoniums as a class instead of one at a time, except of course I've now done them one at a time, so that's... that's thorough, at least. That's what that is."
    headmaster.think "...How long have I been explaining myself to a mop bucket?"

    subtitles "The coffee at his elbow has gone cold enough to grow a skin. The rack is full of used test tubes, every one of them the same unchanged amber."

    headmaster.think "Seven bottles. Seven for seven. Nothing."
    headmaster.think "Unless it's two of them together. Some combination..."
    headmaster.think "God, no. That's— what, twenty-one pairs? Before I even think about ratios. I'd be in here till Christmas."

    # Only a couple of bottles left. Behind the others, at the back of the cart's
    # bottom tray: a big 2.5 L jug with a faded label, ORGAZYME Bio-Enzymatic
    # Floor Concentrate, Cumulus Laboratories, "non-toxic · biodegradable".
    subtitles "At the very back of the bottom tray, behind the spray bottles, there's one he missed: a big white jug with a label faded almost to nothing."
    headmaster "{i}Orgazyme.{/i} Bio-enzymatic floor concentrate. Cumulus Laboratories."
    headmaster "...Orgazyme. From {i}Cumulus.{/i}"
    headmaster.think "Somebody in that marketing department had a very good year. Or got fired. Possibly both."
    headmaster "Non-toxic, biodegradable, 'powered by a proprietary living culture'. So it's basically fancy yoghurt for floors."

    subtitles "He unscrews the cap. The smell is nothing like the other bottles: warm and fruity, like overripe peaches, with something yeasty underneath."

    # One drop into a fresh sample.
    headmaster "One drop. Same as the others. And..."

    # The amber shimmers, deepens, turns vivid, almost lit from inside.
    headmaster "Wait— wait, wait, wait."
    headmaster "That's the colour. That's {i}exactly{/i} the colour from the hallway."

    subtitles "The sample isn't amber any more so much as honey held up to a lamp. A thin, sweet vapour curls off the top of the tube, and it's the same smell that hung in that corridor all afternoon."

    headmaster.think "Ha! Ha. Okay. Okay. Don't knock it over. Don't breathe on it. Don't do anything stupid."

    # Frantic notes. He's muttering while he writes.
    headmaster "It's the enzymes. Of course it's the enzymes. Some protease or other in there is latching onto the active fraction and— folding it. Locking it into a shape that doesn't fall apart."
    headmaster "So the stuff doesn't break down in minutes. It holds. That's why the girls in the hallway didn't snap back like the others did, that's why Ms. Maki was still— yes. {i}Yes.{/i}"
    headmaster.think "A catalyst. An actual, literal catalyst. Enzymes are catalysts. I'm allowed to call it that, it's {i}correct{/i}."

    # He picks up the jug and tilts it against the bulb to check the fill level.
    subtitles "He picks up the jug and tilts it against the light. It's barely a third full. Less, maybe."
    headmaster "Three hundred and fifty millilitres, give or take. That's... well. That's not nothing."
    headmaster.think "Plenty for testing. And when it runs low, I'll just order more. It's floor cleaner. Someone sells floor cleaner."

    # He pulls out his phone, still in one glove.
    subtitles "He tugs off one glove with his teeth and pulls out his phone."

    # Phone screen: Cumulus Laboratories, "dissolved 1998", no successor company;
    # an old forum thread: "anyone know what was in Orgazyme? nothing works like it".
    subtitles "Cumulus Laboratories: dissolved in 1998. No successor, no licence holder, nobody who bought the formula. The only thing still online is an old janitors' forum thread titled {i}anyone know what was actually in orgazyme??{/i}, forty replies long, and none of them know."
    headmaster.think "...Of course. Of course it is."

    # He sets the phone face-down next to the glowing test tube.
    headmaster "A proprietary culture. One strain, never published, and the company's been gone for twenty-odd years."
    headmaster "And I can't even grow more of it. After this long in the jug the culture's long dead. The enzymes still work, they just don't make any new ones."
    headmaster.think "The base potion I can make all week, as long as I keep buying chemicals. This I can't make at all."
    headmaster.think "Whatever's left in that jug is all there is. Anywhere."

    # Rough math in the notebook margin.
    headmaster "Say ten millilitres a dose, if the ratio holds, and I'm guessing at half of that ratio... thirty-five doses? Thirty, if I spill anything. I always spill something."
    headmaster.think "Thirty doses. For a whole school."

    # He sits down on an upturned mop bucket, back against the shelf.
    subtitles "He sits down on an upturned mop bucket, which creaks, and leans his head back against the shelving."
    headmaster.think "And every drop I put in a test tube tonight is a drop I never get back. Not ever."
    headmaster.think "I finally find the thing, and now I'm scared to use it. That's brilliant. That's a really great result."

    # Beat. Then he gets up and puts the jug away carefully.
    subtitles "After a while he gets up, screws the cap down as tight as it'll go, and puts the jug on the top shelf behind the paint tins, where nobody with a mop will ever find it."
    subtitles "Then, after a moment's thought, he tears a page out of the notebook, writes DO NOT TOUCH on it in capitals, and tapes it to the jug."

    headmaster.think "I need to think about what's actually worth spending it on. Properly. Not at eleven at night on a mop bucket."
    headmaster.think "...Emiko's going to have an opinion about this. She always has an opinion."

    # He switches off the bulb; the last sample still glows faintly on the table.
    subtitles "He switches off the bulb. On the lab table the last test tube keeps glowing faintly in the dark."

    $ set_progress("lab_intro", 12)

    $ end_event("new_daytime", **kwargs)

# endregion

##############################
# region Lab Intro 13 Events #

init 2 python:
    set_current_mod('base')

    # Strategic Planning — Headmaster and Emiko discuss the plan to fix the girls
    # in the classroom. Pure dialogue, so it runs entirely on Emiko's paperdoll
    # over the blurred lab background (lab_intro_3 6). No bespoke CGs, hence no
    # Pattern. Gated behind the Frustration (lab_intro 12). Registered on the "call
    # secretary → talk" action, same as lab_intro_6.
    lab_intro_13_event = Event(3, "lab_intro_13",
            TimeCondition(weekday = "d", daytime = "d"),
            ProgressCondition("lab_intro", 12),
            ReplayCategoryOption("lab_intro"),
            thumbnail = "images/events/lab_intro/lab_intro_3/lab_intro_3 6.png")
    office_building_call_secretary_events["talk"].add_event(lab_intro_13_event)

# Strategic Planning unlocks after Frustration
label lab_intro_13 (**kwargs):
    $ begin_event(**kwargs)

    # SCENE · lab_intro_13
    # The next morning in the storage-room lab. The headmaster fell asleep there
    # on the upturned mop bucket; cold coffee, notebook pages full of sums, the
    # Orgazyme jug on the top shelf with its taped-on DO NOT TOUCH note. Emiko
    # comes looking for him, and the whole planning talk happens in the cramped room.
    # Wired: blurred lab bg (lab_intro_3 6) + Emiko paperdoll.

    $ emiko.register_paperdoll()
    $ paperdoll_manager.set_background("images/events/lab_intro/lab_intro_3/lab_intro_3 6.png", blur = True)

    subtitles "Morning. Somewhere down the corridor a printer is grinding itself awake. In the storage room, the bulb has been on all night."
    subtitles "He wakes up on the mop bucket with his neck bent the wrong way, a pencil still in his hand, and the notebook in his lap covered in sums that all end in a circled, underlined {i}not enough{/i}."

    headmaster.think "...Ow. Okay. Didn't mean to do that."

    # The door opens; Emiko leans in, folder under one arm.
    $ emiko.display(PDAImage(pose = "25", outfit = "uniform", level = 6, mood = "suprised", mouth = "closed"),
        PDAPreset("close_body_center", duration = 0.0),
        PDAPreset("outside", duration = 0.0))
    $ emiko.display(PDAPreset("close_body_center", duration = 0.6))
    $ emiko.display(PDAImage(mood = "neutral", mouth = "open"))
    emiko "There you are. Your office is empty, your coat's on the chair, and your nine o'clock was twenty minutes ago."
    $ emiko.display(PDAImage(pose = "2", mood = "happy", mouth = "open"))
    emiko "I moved it, by the way. You're welcome."
    $ emiko.display(PDAImage(mouth = "closed"))
    headmaster "...What time is it?"
    $ emiko.display(PDAImage(pose = "9", mood = "shining", mouth = "open"))
    emiko "Late enough that you've got a mop bucket printed on the back of your trousers."
    $ emiko.display(PDAImage(pose = "34", mood = "neutral", mouth = "closed"))
    emiko.think "*He slept in here. On a bucket. And he's got that face on, the one where he's already decided it's hopeless and he's just waiting for the rest of the world to agree with him.*"

    # She spots the jug on the top shelf with the note taped to it.
    $ emiko.display(PDAImage(pose = "7", mood = "suspicious", mouth = "open", look = "avert"), "close_body_right")
    emiko "'Do not touch.' Is that one for the janitor or for you?"
    $ emiko.display(PDAImage(look = "follow", mouth = "closed"))
    headmaster "Bit of both, honestly."
    headmaster "I found it, Emiko. Whatever it was in that hallway, it's in that jug."
    $ emiko.display(PDAImage(pose = "19", mood = "suprised", mouth = "open"))
    emiko "That's floor cleaner."
    $ emiko.display(PDAImage(mood = "sad", mouth = "closed"))
    headmaster "It's an enzyme concentrate. And it's the catalyst. One drop and the sample went exactly the colour it was on the floor. It holds, it doesn't fall apart after five minutes, it's— it's the whole thing."

    $ emiko.display(PDAImage(pose = "17", mood = "neutral", mouth = "closed", look = "avert"))
    subtitles "She stretches up on her toes to read the label, and he watches her get to the name."
    $ emiko.display(PDAImage(mood = "shining", mouth = "open"))
    emiko "{i}Orgazyme.{/i}"
    emiko "...By {i}Cumulus Laboratories.{/i}"
    $ emiko.display(PDAImage(look = "follow", mouth = "closed"))
    headmaster "Don't."
    $ emiko.display(PDAImage(pose = "22", mood = "happy", mouth = "open"), "close_body_center")
    emiko "I didn't say a word. I said it with my face, that's different."

    # She looks back at him properly now; the teasing drops a notch.
    $ emiko.display(PDAImage(pose = "21", mood = "neutral", mouth = "open"))
    emiko "So why do you look like someone died? You found it."
    $ emiko.display(PDAImage(mouth = "closed"))
    headmaster "Because that's all of it. About a third of a litre. The company folded in '98, nobody ever published what was in the culture, and whatever's left in there is dead. The enzymes still work, but they don't make any more."
    $ emiko.display(PDAImage(pose = "7", mood = "suspicious", mouth = "closed"))
    headmaster "I spent half the night trying to stretch it. Lower ratios, a second extraction, cutting the base with... Every version either kills the effect or wastes more than it saves. Thirty doses, maybe. For a whole school full of girls."
    headmaster "I can't even get through one year group with that, let alone—"

    $ emiko.display(PDAImage(pose = "25", mood = "angry", mouth = "open"))
    emiko "You're doing sums for every girl on campus."
    $ emiko.display(PDAImage(mouth = "closed"))
    headmaster "Well— yes? That's rather the point."

    # She perches on the edge of the cleaning cart, folder on her knees.
    $ emiko.display(PDAMove(alignY = -0.18, zoom = 3, duration = 1))
    subtitles "She hitches herself up onto the edge of the cleaning cart, which rattles every bottle on it, and sets the folder on her knees."
    $ emiko.display(PDAImage(pose = "37", mood = "neutral", mouth = "open"))
    emiko "The girls don't make the rules here, [headmaster_first_name]. When Sakura's blouse came open the other day, Easkey panicked before Sakura did. And the second Sakura noticed, all either of them could think about was which teacher would hear about it."
    emiko "Five teachers keep the rules. Three mothers on the PTA make sure the teachers keep keeping them. That's eight people. You don't need a school's worth of doses. You need eight."
    $ emiko.display(PDAImage(mouth = "closed"))

    headmaster "Eight people won't change a whole school."
    $ emiko.display(PDAImage(pose = "27", mood = "shining", mouth = "open"),
        PDAPreset("close_body_center", duration = 1))
    emiko "Eight of the {i}right{/i} people will. If Ms. Parker stops sending girls back to change, and Mrs. Hall stops writing three-page letters every time she doesn't... how long do you honestly think the girls keep policing themselves?"
    $ emiko.display(PDAImage(mouth = "closed"))

    headmaster.think "...God. Those girls in the classroom didn't care what {i}I{/i} thought. They only cared once they pictured who might walk in next."
    headmaster.think "Take away who walks in next..."

    # He's doing sums again, but different ones; pencil back on the notebook.
    headmaster "Eight people. Small doses, repeated, three each over a week or so, that's... twenty-four. And I'd still have some left over."
    $ emiko.display(PDAImage(pose = "31", mood = "shining", mouth = "closed"))
    emiko "Look at you. Doing sums that actually help."
    $ emiko.display(PDAImage(mood = "happy", mouth = "closed"))

    headmaster "The teachers are the easy part. I've done the lounge coffee before."
    $ emiko.display(PDAImage(pose = "32", mood = "neutral", mouth = "open"))
    emiko "And it worked. For five minutes, and then Finola went and changed back into her cardigan."
    $ emiko.display(PDAImage(mouth = "closed"))
    headmaster "Five minutes {i}without{/i} this."
    subtitles "He points the pencil at the top shelf without looking up."

    headmaster "The mothers are the problem. I can hardly turn up on Adelaide Hall's doorstep with a thermos."
    $ emiko.display(PDAImage(pose = "37", mood = "shining", mouth = "open"))
    emiko "You won't have to. The PTA meets on Friday. And guess who does the refreshments."
    $ emiko.display(PDAImage(mouth = "closed"))
    headmaster "...You."
    $ emiko.display(PDAImage(pose = "26", mood = "happy", mouth = "open"))
    emiko "Me. Lemonade and whatever biscuits the kiosk hasn't sold. Nobody ever says no to the lemonade."
    $ emiko.display(PDAImage(mouth = "closed"))
    headmaster "You'd really do that?"
    $ emiko.display(PDAImage(pose = "1", mood = "neutral", mouth = "open", look = "avert"))
    emiko "I've poured that lemonade every other Friday for years. This time it's just... better lemonade."
    $ emiko.display(PDAImage(mouth = "closed"))
    emiko.think "*And he doesn't need to hear about the girls in the old lab building. Not yet. If their little project goes wrong, it's my name on it, not his. I'll carry that one.*"

    # She hops down off the cart; the bottles rattle again.
    $ emiko.display(PDAMove(alignX = "-0.2", duration = 0.6))
    $ emiko.display(PDAImage(pose = "5", mood = "shining", mouth = "open", look = "follow"))
    emiko "And while you're playing barista, I'll see what the budget says about the old lab building. You can't keep doing this in a broom cupboard."
    $ emiko.display(PDAImage(mouth = "closed"))
    headmaster "It's a storage room."
    $ emiko.display(PDAImage(mood = "happy", mouth = "open"))
    emiko "It's a broom cupboard with ambitions."

    $ emiko.display(PDAImage(pose = "11", mood = "neutral", mouth = "open"))
    emiko "Now go home, have a shower, and come back looking like a headmaster. I'll tell everyone you had the dentist."
    $ emiko.display(PDAImage(mouth = "closed"))
    headmaster "I don't have a—"
    $ emiko.display(PDAImage(pose = "2", mood = "shining", mouth = "open"))
    emiko "You do now."

    $ emiko.display(PDAImage(pose = "39", mouth = "closed"),
        PDAMove(alignX = 1.5, duration = 1.0),
        PDAPause(duration = 1.0))
    $ emiko.clear_display()

    # Alone. He takes the jug down from the shelf and looks at the note.
    subtitles "The door clicks shut behind her. He gets up, joints complaining, and lifts the jug down off the top shelf. The DO NOT TOUCH note is already curling at one corner."
    headmaster.think "Eight people. I was lying awake trying to work out how to fix every girl in this school one at a time. Idiot."
    headmaster.think "Teachers first. Then Friday."
    headmaster.think "...Shower first. {i}Then{/i} the teachers."

    $ set_progress("lab_intro", 13)

    $ end_event("new_daytime", **kwargs)

# Morning Brew, unlocks after Strategic Planning and Brewing Session on Thursday
label lab_intro_14 (**kwargs):
    $ begin_event(**kwargs)

    $ zoe = Person["zoe_parker"]
    $ yulan = Person["yulan_chen"]
    $ lily = Person["lily_anderson"]
    $ chloe = Person["chloe_garcia"]
    $ finola = Person["finola_ryan"]

    # SCENE · lab_intro_14
    # Before dawn the headmaster measures the first catalysed dose in the
    # storage-room lab and pockets it in a small dropper bottle. In the empty,
    # dark staff room he brews the big coffee urn and adds the drops. The five
    # teachers arrive one by one and all drink it. Within half an hour they're
    # warm and loose: Lily stretches, Zoe strips to her swimsuit top, Chloe rolls
    # up her sleeves, Yulan sits pressed up against Finola. Finola suddenly
    # leaves. He follows her to the staff changing room and walks in on her
    # completely naked at her locker; she covers herself a full second too late.
    # She comes back dressed, mortified, and remembers very little. The teachers
    # head off to class and he pours the rest of the coffee away.
    # Wired: blurred lab bg (lab_intro_3 6), dark staff room (c teacher),
    # daytime staff room (teacher 1 1 0), paperdolls for teachers who speak TO him.

    ########################################
    # Storage-room lab, before dawn

    $ paperdoll_manager.set_background("images/events/lab_intro/lab_intro_3/lab_intro_3 6.png", blur = True)

    subtitles "Ten to six. The corridor outside the storage room is still dark, and the bulb over the lab table is the only light on in the building."

    # He measures base potion into a small dark dropper bottle.
    headmaster "Five teachers, one dose each. Base potion first: the staff urn does twenty cups, so enough base for all of it, call it a bit extra in case somebody goes back for seconds..."
    headmaster "And Orgazyme, ten millilitres a head. Fifty. Not fifty-five. Don't get generous at six in the morning."

    subtitles "He measures it in the little graduated cylinder, right down to the line, and stands there holding it for a moment before he tips it in. He doesn't breathe out until the last of it has gone. The mixture goes from amber to that deep, lit-from-inside honey colour, and the fruity sweetness rises off it for a second before he gets the cap on."
    headmaster.think "Fifty out of three hundred and fifty. A seventh of everything I'll ever have, gone before anyone's even had breakfast."
    headmaster.think "...It's fine. This is what it's for. Stop looking at the jug."

    # Bottle into his jacket pocket; he grabs a stack of papers as cover.
    headmaster.think "Papers. Something to pretend to read. The budget draft, nobody ever asks about the budget draft."

    ########################################
    # Staff room, still dark

    $ paperdoll_manager.set_background("images/background/office building/c teacher.webp", blur = True)

    subtitles "The staff room is cold and blue in the half-light. Somebody has left a mug on the desk by the window with a teabag welded to the bottom of it."
    headmaster.think "Nobody's in before seven. Plenty of time. You're just a man making coffee. That's all this is."

    # He fills the big urn, measures the grounds, switches it on.
    subtitles "The urn takes forever. It ticks, and gurgles, and finally starts to hiss, and the room slowly fills up with the smell of cheap, strong coffee."

    # Waiting at the window, dawn coming up.
    headmaster.think "It's already bound. The enzymes did their work in the flask. The heat can't do anything to it now."
    headmaster.think "...Probably. Almost certainly. I really should have tested that."

    # The urn finishes. Lid up, steam, the dropper bottle.
    subtitles "When the urn clicks off he lifts the lid, and steam rolls up into his face. He tips the little bottle in all at once, stirs it with the long spoon, and watches the amber vanish into the black without a trace."
    headmaster "There."
    headmaster.think "Coffee. It's just coffee. It smells like coffee. Sit down."

    ########################################
    # Staff room, morning. Teachers arrive.

    $ paperdoll_manager.set_background("images/background/office building/teacher 1 1 0.webp", blur = True)

    subtitles "By quarter to seven there's grey daylight in the windows. He's at the long table with the budget draft spread out in front of him, and he has read the same line eleven times."

    # Zoe first, bag over her shoulder, travel mug in hand. Speaks to him.
    $ zoe.register_paperdoll()
    $ zoe.display(PDAImage(pose = "1", outfit = "uniform", level = 2, mood = "suprised", mouth = "open"),
        PDAPreset("upper_body", duration = 0.0),
        PDAPreset("outside", duration = 0.0))
    $ zoe.display(PDAPreset("upper_body_center", duration = 0.4))
    zoe "Oh! You're in before me? That never happens. Is everything okay? Nobody's— nothing's happened?"
    $ zoe.display(PDAImage(mouth = "closed"))
    headmaster "Nothing's happened. I couldn't sleep, so I thought I'd get some work done down here. There's coffee, if you want it."
    $ zoe.display(PDAImage(mood = "happy", mouth = "open"))
    zoe "You made coffee. In the staff room. Before seven."
    zoe "I'm going to pretend I'm not suspicious and just be grateful, okay? Thank you."
    $ zoe.display(PDAImage(mouth = "closed"))

    subtitles "She pours herself a mug, adds far too much milk, and takes a long swallow standing right there at the counter."
    $ zoe.display(PDAImage(mood = "happy", mouth = "open"))
    zoe "Oh, that's good. That's actually good. You're allowed to be in early more often."
    $ zoe.display(PDAImage(mouth = "closed"))
    headmaster.think "One."
    $ zoe.clear_display()

    # Yulan, precise, checks the clock before anything else.
    subtitles "Yulan Chen comes in two minutes later, glances at the urn, and then at the clock, in that order."
    yulan "It's six fifty-two. The machine's on a timer for seven fifteen."
    headmaster "I overrode it."
    yulan "...Hm."
    yulan "Well. I'm not going to file a complaint about it."
    subtitles "She takes it black, in the plain white mug she always uses, and drinks it hot enough that it must hurt."
    headmaster.think "Two."

    # Lily, exhausted, talking before she's through the door. Speaks to him.
    $ lily.register_paperdoll()
    $ lily.display(PDAImage(pose = "1", outfit = "uniform", level = 2, mood = "sad", mouth = "open"),
        PDAPreset("upper_body", duration = 0.0),
        PDAPreset("outside", duration = 0.0))
    $ lily.display(PDAPreset("upper_body_center", duration = 0.4))
    lily "Please tell me that's real coffee and not the smell of it coming off Yulan. I was up until past one with 3A's tests, and I swear half of them have invented a new kind of fraction—"
    $ lily.display(PDAImage(mouth = "closed"))
    headmaster "It's real. Help yourself."
    $ lily.display(PDAImage(mood = "happy", mouth = "open"))
    lily "Oh, bless you."

    subtitles "She pours, lifts the mug to her face, and stops with it just under her nose."
    $ lily.display(PDAImage(mood = "suspicious", mouth = "open"))
    lily "Is this a different brand? It's got a sort of... fruity note to it? Not bad. Just—"
    lily "Sorry. Science teacher. I smell everything, it's a curse. Ignore me."
    $ lily.display(PDAImage(mouth = "closed"))
    headmaster.think "Oh no. Of course it's the chemistry teacher. Of course it is."
    headmaster "Same tin as always. Maybe someone finally cleaned the machine."
    $ lily.display(PDAImage(mood = "suprised", mouth = "open"))
    lily "Someone {i}cleaned{/i} the machine? Okay, now I'm actually worried."
    $ lily.display(PDAImage(mood = "happy", mouth = "closed"))
    subtitles "She laughs, and drinks, and goes to collapse into the armchair by the radiator."
    headmaster.think "...Three. Breathe."
    $ lily.clear_display()

    # Chloe, sleeves down over her tattoos as usual. Speaks to him.
    $ chloe.register_paperdoll()
    $ chloe.display(PDAImage(pose = "1", outfit = "uniform", level = 2, mood = "neutral", mouth = "open"),
        PDAPreset("upper_body", duration = 0.0),
        PDAPreset("outside", duration = 0.0))
    $ chloe.display(PDAPreset("upper_body_center", duration = 0.4))
    chloe "Somebody made a full pot before seven. Who are you, and what have you done with our headmaster?"
    $ chloe.display(PDAImage(mouth = "closed"))
    headmaster "Early meeting prep. Help yourself."
    $ chloe.display(PDAImage(mood = "happy", mouth = "open"))
    chloe "'Meeting prep.' Sure. I'll take it, whatever it is."
    $ chloe.display(PDAImage(mouth = "closed"))
    headmaster.think "Four."
    $ chloe.clear_display()

    # Finola last, flustered, bag half open.
    subtitles "Finola Ryan arrives last, red bob still damp from the shower, with her bag half unzipped and a scarf she clearly grabbed on the way out the door."
    finola "Sorry, sorry, I overslept, I {i}never{/i} oversleep— is there any left?"
    yulan "Plenty. He's made enough for a regiment."
    subtitles "Finola pours a cup, stirs in two sugars, and sits down in the only free chair, which happens to be right next to Yulan."
    headmaster.think "Five. All five of them."

    ########################################
    # Overheard: the teachers talking among themselves (no paperdolls).

    subtitles "For a while it's just a normal staff-room morning. Mugs clinking, the radiator knocking, somebody's phone buzzing on the table."
    zoe "Did anybody actually read the agenda for Friday? Because I got as far as 'item one' and then I had to go and supervise the swimming."
    lily "It's the budget again. It's always the budget. And behaviour, apparently, because the council has decided we need a new form for it."
    chloe "Another form. Great. I'll colour it in."
    yulan "The existing form is fine. It's that nobody fills it in properly."
    lily "Can we please not talk about forms until I've had at least two of these?"

    headmaster.think "Normal. Completely normal. Maybe I got the ratio wrong. Maybe the heat did—"

    # Twenty minutes later. The shift starts.
    subtitles "Twenty minutes later, the conversation has got louder, and slower, and somehow warmer."

    # Lily stretches in the armchair; her blouse rides up over her stomach.
    subtitles "Lily stretches in the armchair, arms right up over her head, and her blouse comes untucked and rides up over a pale strip of stomach. She doesn't pull it down."
    lily "Mmh— God, sorry. I think I graded myself into a knot last night. Everything's so... loose now, though. Is that weird? That's weird."

    # Zoe peels off her red tracksuit jacket; yellow swimsuit top underneath.
    subtitles "Zoe has unzipped her tracksuit jacket all the way and shrugged it off onto the back of the chair. Underneath is the yellow swimsuit top she wears for the pool, and she's sitting there in it with her legs crossed as if that's what she always wears to the staff room."
    zoe "Is the heating on already? I'm roasting. Honestly, this coffee's doing something to me. I feel all... good-loose. Like after a really long swim."

    # Chloe rolls her sleeves right up; tattoo sleeves fully on show.
    subtitles "Chloe, who never shows her arms in front of colleagues, has rolled both her sleeves up past the elbow without seeming to notice. The ink runs all the way up: roses, a swallow, a line of sheet music."
    chloe "Oh, screw it. It's too warm for sleeves."

    # Yulan and Finola, shoulder to shoulder.
    subtitles "At the table, Yulan has ended up with her shoulder pressed against Finola's, and her hand resting on the table a few centimetres from Finola's own. Neither of them has moved away."
    yulan "Your hair's very red. In this light, I mean. I don't think I'd ever really noticed."
    finola "Oh— um. Thank you? It's just... hair."
    yulan "No, it's a good red. It's a very... committed red."

    headmaster.think "Oh. Oh, it's working. It's working faster than last time. {i}Much{/i} faster."
    headmaster.think "Don't stare. Read the budget. Turn a page. Any page."

    # Finola sets her cup down hard; one hand flat against her chest.
    subtitles "Finola puts her mug down harder than she means to. She presses one hand flat against her chest, like she's checking her own heartbeat, and stands up."
    finola "Excuse me a second."
    subtitles "She's out of the door before anyone can answer. It isn't quite running."

    zoe "Finn? You okay?"
    subtitles "Zoe half gets up out of her chair."
    headmaster.think "If Zoe goes after her, and it's bad, she'll know something's wrong. She'll want to know what everyone drank."
    headmaster "I'll check on her. I need to grab something from my office anyway."
    zoe "...Okay. Tell her to drink some water, she never drinks anything."

    ########################################
    # Corridor → staff changing room

    # IMAGE: empty corridor; the staff changing room door at the end, ajar.
    subtitles "The corridor's empty. At the far end, the staff changing room door is standing open about a hand's width."
    headmaster.think "Not the bathroom. The changing room. She went for her locker."
    headmaster.think "Last time she ran for it in a panic. This time she walked straight here like she knew exactly what she was doing..."

    subtitles "There's movement on the other side of the door: a soft rustle of fabric, a zip, a long exhale."
    headmaster "Ms. Ryan? Are you—"

    # IMAGE: through the gap, Finola at her locker, back to him, completely naked,
    # clothes in a heap on the bench and floor. Freckles down her back.
    subtitles "He pushes the door with two fingers, and it swings further than he means it to."
    subtitles "Finola is standing at her open locker with her back to him, and she isn't wearing anything at all. Her blouse, her skirt, her tights and her underwear are all in a heap on the bench, as though they'd been peeled off in one go. The freckles on her shoulders carry on down her back, all the way down."
    headmaster.think "Oh— oh God."

    # IMAGE: she turns at his voice; a full second passes before an arm crosses
    # her chest and a hand drops low. Face flushed, dazed, not horrified.
    subtitles "She turns around at the sound of his voice. For one long second she just looks at him, flushed and a bit dazed, completely bare, and it's only after that second that an arm comes up across her chest and her other hand drops to cover herself."
    $ set_game_data("seen_breasts_finola_ryan", True)
    $ set_game_data("seen_ass_finola_ryan", True)
    $ set_game_data("seen_pussy_finola_ryan", True)

    headmaster "I'm so sorry— I thought— I'll go. I'm going. I'm gone."
    finola "It was all too tight. Everything. The shirt, and then the— and then it was all of it, it was all just too {i}much{/i}, I couldn't—"
    finola "Sorry. I'm sorry. Give me a minute. Please."

    subtitles "He pulls the door shut and stands in the corridor with his hand still on the handle."
    finola.think "*He saw. He— did he see? He saw. I didn't even lock the door. I {i}always{/i} lock the door.*"

    headmaster.think "I just walked in on a colleague. Stark naked. At quarter to eight on a school morning."
    headmaster.think "...Last time she changed her top and was mortified inside five minutes. This time she took off everything, and when I walked in she just stood there."
    headmaster.think "A whole second before she even covered up. Normal Finola would've had something heavy airborne by now."

    # Finola comes out in the spare clothes from her locker: her level-3 outfit
    # (cropped yellow tank, lace bra edge showing, bare midriff, polka-dot belt,
    # ripped dark jeans, black lace-up boots). Speaks to him.
    subtitles "A few minutes later the door opens. Finola comes out dressed again, but not in what she arrived in. It's the spare clothes from her locker: a cropped yellow tank top that stops well above her navel, the lace edge of her bra showing at the neckline, ripped dark jeans and her black boots. The blouse is balled up in her hand."
    subtitles "She can't quite look at him."
    $ finola.register_paperdoll()
    $ finola.display(PDAImage(pose = "1", outfit = "uniform", level = 3, mood = "sad", mouth = "closed", look = "avert"),
        PDAPreset("upper_body", duration = 0.0),
        PDAPreset("outside", duration = 0.0))
    $ finola.display(PDAPreset("upper_body_center", duration = 0.4))
    $ finola.display(PDAImage(mouth = "open"))
    finola "I honestly don't know why I did that."
    finola "I remember being too hot, and then your voice, and... that's it, mostly. That's all I've got. I'm so sorry."
    $ finola.display(PDAImage(mouth = "closed"))
    finola.think "*I remember his voice. I remember the cold floor under my feet. I don't remember deciding to take everything off.*"
    headmaster "It's forgotten. Honestly. Are you feeling alright?"
    $ finola.display(PDAImage(mood = "neutral", mouth = "open"))
    finola "I... yes. Fine. Better, actually, which is somehow the worst part."
    finola "These were in my locker. For... I honestly don't know what for. I couldn't make myself put the blouse back on. It felt like— it just felt {i}wrong{/i} on me."
    $ finola.display(PDAImage(mouth = "closed"))
    headmaster.think "Last time she couldn't get back into her own clothes fast enough. 'Completely inappropriate for work.' Her words."
    headmaster.think "...She's not even reaching for the blouse."
    subtitles "She gives him a small, awful smile and goes back towards the staff room with the blouse still balled up in her fist, and her arms folded tight over her bare stomach."
    $ finola.clear_display()

    ########################################
    # Staff room, bell coming up

    subtitles "By the time he gets back, the teachers are gathering up bags and mugs. First period is ten minutes away."
    zoe "Is Finn alright?"
    headmaster "She's fine. Overheated, I think."
    zoe "Mm."
    subtitles "Zoe looks at him for a moment longer than she needs to, then shrugs her jacket back on over the swimsuit top and zips it right up."
    chloe "Thanks for the coffee, boss. Do it again sometime."
    lily "Please do it again. Every day. I'll pay you."
    yulan "Next time, leave the timer alone."

    subtitles "The door swings shut behind the last of them, and the room goes quiet except for the radiator."

    # He tips the last two cups' worth into the sink and rinses the urn.
    subtitles "There's maybe two cups left in the urn. He pours them down the sink, rinses the urn out twice, and puts it back exactly where it was, with the lid at the same slightly crooked angle."
    headmaster.think "Right. Now it wears off. Like it always does."
    headmaster.think "And tomorrow I find out whether anything stays behind."

    $ set_progress("lab_intro_faculty", 1)

    $ end_event("new_daytime", **kwargs)

# PTA Refreshments - Friday morning after Morning Brew
label lab_intro_15 (**kwargs):
    $ begin_event(**kwargs)

    $ adelaide = Person["adelaide_hall"]
    $ nubia = Person["nubia_davis"]
    $ yuki = Person["yuki_yamamoto"]
    $ yuriko = Person["yuriko_oshima"]

    $ zoe = Person["zoe_parker"]
    $ yulan = Person["yulan_chen"]
    $ lily = Person["lily_anderson"]
    $ chloe = Person["chloe_garcia"]
    $ finola = Person["finola_ryan"]

    # SCENE · lab_intro_15
    # Friday, the PTA meeting room. Emiko sets out two jugs of lemonade: the one
    # with lemon slices is dosed and meant for the three mothers, the plain one
    # is for everyone else (the teachers were dosed yesterday). Adelaide Hall
    # arrives with a tin of her own shortbread and seven printed pages of
    # objections to the summer uniform proposal; Nubia Davis and Yuki Yamamoto
    # come with her. All three drink. The teachers and Yuriko Oshima (student rep)
    # join; Yuriko drinks nothing. The agenda sails through, the mothers getting
    # chattier and giddier, and the uniform item passes in a unanimous show of
    # hands; Adelaide never uses her pages. Afterwards Adelaide traces Chloe
    # Garcia's tattoos, and Yuriko watches. Emiko clears up and mentions she has
    # plans tonight.
    # Wired: blurred PTA room bg (pta 6 2 0). No paperdolls: the room plate has
    # the cast baked in, and it's a group scene.

    $ paperdoll_manager.set_background("images/events/pta/regular meeting/pta 6 2 0.webp", blur = True)

    ########################################
    # Before the meeting: Emiko and the two jugs

    subtitles "The meeting room smells of furniture polish and the radiator that's been on since seven. On the side table Emiko has set out two glass jugs of lemonade, sweating in the warm air, and a stack of paper cups."
    subtitles "One jug has thin lemon slices floating in it. The other doesn't."

    headmaster "Which one's which?"
    emiko "Lemon slices for the mothers. Plain for everybody else."
    headmaster "Why lemon slices?"
    emiko "Because Adelaide Hall will tell me they look lovely, and pour herself a glass before she's even got her coat off."
    emiko "The teachers had theirs yesterday. No point wasting your precious floor cleaner on a second helping."
    headmaster.think "She's thought about this more than I have. Again."

    ########################################
    # The mothers arrive

    # IMAGE: the three mothers in the doorway. Adelaide in front with a biscuit
    # tin and a folder; Nubia and Yuki behind, mid-conversation.
    subtitles "They arrive together, ten minutes early, as always. Adelaide Hall leads, with a floral biscuit tin under one arm and a plastic folder held against her chest like a hymn book."
    adelaide "Good morning! I brought shortbread. The cafeteria had butter left over, and I couldn't bear to see it go to waste."
    headmaster "Mrs. Hall. Mrs. Davis, Mrs. Yamamoto. Thank you for coming early."
    nubia "She made us come early. She wanted to get the good chairs."
    adelaide "I wanted to get {i}settled{/i}, Nubia. There's a difference."

    subtitles "Adelaide sets the folder down on the table in front of her chair with great care. Through the plastic you can see the top page: SUMMER UNIFORM PROPOSAL — CONCERNS. It is stapled. There are a lot of pages."
    adelaide "I've put a few thoughts together on item five, headmaster. Nothing dramatic. I just think some of us have to be the grown-ups about hemlines."
    nubia "She has seven pages of thoughts."
    yuki "I only have one concern. But it's a big one."
    headmaster.think "Seven pages. Stapled. God help me."

    # Emiko offers the dosed jug.
    emiko "Lemonade, ladies? It's warm in here already."
    adelaide "Oh, the lemon slices, look. Emiko, that looks lovely."
    emiko.think "*Told him.*"

    subtitles "Adelaide takes the first cup, and sniffs it the way she'd sniff a pot of soup in her own kitchen, before she drinks."
    adelaide "Fresh lemons, not from concentrate. You spoil us. It's a touch sweet, but I'll forgive you."
    nubia "Beats the sludge you gave us last time. No offence."
    emiko "None taken. The last lot really was sludge."
    subtitles "Nubia drains half the cup in one go. Yuki holds hers in both hands for a while, then drinks it slowly, looking round the room over the rim."

    # Small talk while they settle.
    headmaster "How's Soyoon getting on, Mrs. Yamamoto?"
    yuki "Oh, you know Soyoon. Polite to everybody, friends with nobody."
    yuki "Although, she's been doing her homework in the common room with a group lately. A {i}group.{/i} I nearly fell over when she told me."
    headmaster "That's good to hear. And yours, Mrs. Hall? Mrs. Davis?"

    subtitles "There's a very small pause."
    adelaide "Oh, she's... doing well. Where she is."
    subtitles "Adelaide smooths the corner of her folder flat, although it was already flat."
    adelaide "Shortbread, anyone? I really did make far too much."
    nubia "Mine's fine."
    subtitles "Nubia says it into her cup, and drinks. Yuki glances from one of them to the other and says nothing at all."
    headmaster.think "That was a very quick change of subject. ...Not my business. Probably not my business."

    ########################################
    # Teachers and Yuriko arrive

    # IMAGE: the teachers coming in in a loose group, Yuriko Oshima at the back
    # with her student-rep notebook.
    subtitles "The teachers come in in a loose group just before the hour, with Yuriko Oshima trailing behind them clutching her student-rep notebook."
    zoe "Sorry, are we late? Lily couldn't find her keys."
    lily "They were in my hand. They were in my hand the whole time. Nobody tell anyone."

    subtitles "Emiko pours for them from the plain jug without being asked. Finola takes the chair at the far end of the table, as far from the headmaster as the room allows, and doesn't look up from her agenda."
    headmaster.think "...She remembers something, then. Not much. Enough."

    emiko "Yuriko? Lemonade?"
    yuriko "No, thank you."
    adelaide "It's lovely, dear. Fresh lemons."
    yuriko "I'm sure it is."
    subtitles "Yuriko sits down across from the mothers, opens her notebook to a clean page, and writes the date in the corner in small, very neat numbers."

    ########################################
    # The meeting

    headmaster "Thank you all for coming. We've got a full agenda, so let's make a start. Item one: the maintenance budget for next term."

    # IMAGE: twenty minutes in. Adelaide leaning back, one arm hooked over the
    # back of her chair; Nubia laughing; Yuki with her shoes slipped off.
    headmaster "The proposal increases facility maintenance by eight percent."
    subtitles "Adelaide has her pen in her hand. She always has her pen in her hand for the budget. Today she's using it to draw a little flower in the margin."
    adelaide "Eight? Honestly, the building's lovely, it deserves the attention. Give it ten."
    headmaster.think "...She fought me for forty minutes over three percent last time."

    headmaster "Item two. The spring fundraiser. The proposal is a parent-and-student social evening in the hall."
    nubia "A social! With music? Do schools still do those? I used to sneak out to those. I used to sneak {i}in{/i} to those, actually, I wasn't even at that school—"
    subtitles "She laughs so hard at herself that she has to put her cup down."
    nubia "Sorry. Sorry. Yes. Do it. The girls would love it."
    yuki "The third Saturday in May would be good. Soyoon has nothing on. Soyoon never has anything on."

    headmaster "Item three, the cafeteria salad bar. There's a slight cost increase."
    yuki "Oh, yes, please. Soyoon eats like a little bird, she'll tell me she hates salad and then she'll eat the whole bowl, she did it at my sister's, the entire bowl, and then she said it was too oily—"
    subtitles "Yuki has slipped her shoes off under the table somewhere around item two. She seems not to have noticed that she's still talking."
    adelaide "I support the salad bar. I'll run it myself."

    subtitles "Across the table, Zoe catches Yulan's eye. Yulan raises one eyebrow by about a millimetre. Neither of them says anything."
    yuriko.think "*Normally Mrs. Hall has a question about everything. Portion sizes. Supervision. Who's liable if someone chokes on a crouton. Today she's drawing flowers.*"

    # Item five: the uniform. The folder.
    headmaster "Which brings us to item five. The summer uniform proposal: lighter fabrics, and a relaxation of the rules on skirt length and blouses in warm weather."

    subtitles "Everyone looks at Adelaide's folder. Adelaide looks at it too. She picks it up, turns it over in her hands, reads the first line on the top page as if someone else had written it, and puts it down again, face-down."
    adelaide "You know, I was going to say a great deal about hemlines."
    adelaide "But it's {i}hot{/i}. Girls get hot. We were all girls once, weren't we? I remember sitting in a wool skirt in June thinking I'd actually die."
    nubia "Motion to just let them breathe."
    headmaster "...Then I suppose we should vote. All in favour?"

    # IMAGE: hands going up. All three mothers at once; the teachers after them.
    subtitles "Three hands go up at once. The teachers follow a beat later, one after another. Yulan's is last."
    yulan "Is this a formal vote? Then, yes. In favour."
    headmaster "Carried. Unanimously."
    subtitles "Yuriko's pen has stopped moving."
    yuriko.think "*She brought seven pages. I watched her staple them in the corridor.*"

    headmaster "Unless there's any other business... no? Then that's the fastest meeting we've ever had. Thank you, everyone."
    adelaide "Wasn't it lovely? Usually these go on {i}forever{/i}."

    ########################################
    # After the meeting: Adelaide and Chloe

    # IMAGE: people standing, gathering bags. Adelaide has drifted over to Chloe
    # Garcia and is standing much too close, looking at her bare forearm.
    subtitles "Chairs scrape. People gather up bags and papers and stand around in the loose, chatty way people do after a meeting that finished early. Adelaide has drifted over to Chloe Garcia, and is standing much closer than she needs to."
    adelaide "Are these new? I've never noticed how detailed they are."

    # IMAGE: Adelaide's fingertips tracing a rose up Chloe's forearm, unasked.
    subtitles "Before Chloe can answer, Adelaide's fingertips are on her arm, tracing the stem of a tattooed rose slowly up towards her elbow. Chloe goes very still."
    chloe "I've had most of them since before I started here."
    adelaide "They're beautiful. This one especially."
    subtitles "Adelaide's thumb presses into the ink a little. It's too slow, and far too interested, for a chat after a PTA meeting."
    chloe.think "*She's never once looked at my arms. Three years, and she's always looked just past them.*"

    yuriko.think "*Mrs. Hall is stroking Ms. Garcia's arm. In a PTA meeting. ...Adults are exhausting.*"
    yuriko.think "*It's fine. People touch each other all the time. So why does it feel like I've just walked in on something?*"

    headmaster.think "Adelaide Hall. First to finish her cup, first to go back for another."
    headmaster.think "She came in here wound up tight as a spring, with seven pages about hemlines. And now look at her."

    ########################################
    # Clearing up: Emiko

    subtitles "Twenty minutes later the room's empty except for the two of them and the smell of lemons. Emiko is emptying the jug with the lemon slices down the little sink in the corner."
    headmaster "That went... better than it had any right to."
    emiko "Seven pages. Face down. I'm going to have them framed."
    emiko "Oh, and I'm leaving early tonight, if that's alright. I've got plans."
    headmaster "Oh? Anything nice?"
    emiko "Something I've been working on for a while. It's a sort of... get-together."
    headmaster "Good for you. Honestly, you should go out more. You work too hard."
    emiko "...Yes. That's exactly what it is. Going out."
    emiko.think "*Bless him. He hasn't got the faintest idea.*"
    headmaster.think "Good for her. She deserves a night off."

    $ set_progress("lab_intro_parents", 1)

    $ end_event("new_daytime", **kwargs)

# The Discovery unlocks after Chemical Mishap
label lab_intro_16 (**kwargs):
    $ begin_event(**kwargs)

    $ gloria = Person["gloria_goto"]
    $ ishimaru = Person["ishimaru_maki"]
    $ lin = Person["lin_kato"]

    # SCENE · lab_intro_16
    # Late afternoon. Lin talks Gloria and Ishimaru into sneaking into the old,
    # abandoned lab building through the rusted gate. Inside: dusty corridor,
    # a derelict classroom lab full of old glassware and a faded periodic table.
    # Ishimaru knocks over a stand of test tubes; bending down to pick them up,
    # she spots a notebook that has slipped down behind a metal shelf. It's a
    # plain black hardcover notebook, clearly new, full of handwritten notes on
    # a potion: ingredients, effects on a "subject E.", open questions. The
    # three read it, get spooked, half-connect it to an afternoon last week none
    # of them remember properly, and agree to come back with textbooks.
    # (The notebook is the headmaster's, lost here in lab_intro_2. The girls
    # don't know that.) No headmaster present → overheard, no paperdolls.

    # IMAGE: exterior of the abandoned lab building, overgrown, late light;
    # the three girls at the rusted gate, Lin in front.
    subtitles "Behind the sports field, past the bins, the old lab building."
    subtitles "Nobody's used it in years. The windows on the ground floor are boarded, the gate's chained, and the chain has been hanging open for as long as anyone can remember."

    lin "Okay, so technically it's not breaking in if the chain's already broken. That's just... walking in."
    ishimaru "Is that how that works?"
    lin "That's exactly how that works. Come on, I want to see if it's haunted."
    gloria "It won't be haunted. But I would quite like to see the fume cupboards."
    lin "See? Gloria wants to see the fume cupboards. It's educational now. We're basically on a field trip."

    # IMAGE: interior corridor, dust, cobwebs, light through gaps in the boards.
    subtitles "Inside it smells like damp paper and something sharp and chemical underneath, faint, as if it's been soaking into the walls for thirty years. Their footsteps sound much too loud on the cracked lino."

    ishimaru "Okay, this is actually a bit creepy. Is it just me? It's a bit creepy."
    lin "It's not creepy, it's {i}atmospheric.{/i}"
    lin "...It's a bit creepy."
    gloria "The science wing must have moved when they built the new block. So everything in here is from before that. Nobody bothered to clear it out."

    # IMAGE: old classroom lab. Shelves of dusty beakers and test tubes, a faded
    # periodic table, benches with gas taps. Gloria reading bottle labels, Lin
    # peering into a cupboard, Ishimaru turning in a slow circle.
    subtitles "The old chemistry room is still full. Beakers and flasks stand in rows on the shelves under a grey skin of dust, as though the class just got up one day and never came back."

    gloria "Oh, these are good. Borosilicate. That's the proper stuff, you can heat it without it cracking. Half of this would still work if you washed it. Honestly, it's a waste, somebody should be using all of this, the school's buying new glassware every year and there's a whole room of it just sitting here—"
    lin "Gloria. Breathe."
    gloria "I'm breathing. I'm breathing and cataloguing."

    # Ishimaru backs into a stand of test tubes; they go over with a clatter.
    subtitles "Ishimaru takes a step back to look up at the periodic table and walks straight into a rack of test tubes. The whole thing goes over with a clatter that echoes all the way down the corridor."
    ishimaru "Oh— sorry! Sorry. Sorry, sorry, sorry—"
    lin "Who are you apologising to?"
    ishimaru "The... test tubes? I don't know! It's a reflex!"

    # IMAGE: Ishimaru crouching to gather the tubes, peering into the gap
    # between a metal shelf and the wall.
    subtitles "She crouches to scoop them up, and stops, with her cheek almost against the floor."
    ishimaru "Hang on. There's something down here. Behind the shelf."
    lin "If it's a rat I'm leaving. I'm serious. I'll leave you both here."
    ishimaru "It's not a rat, it's... it's a book, I think? Hang on, I can nearly—"

    # IMAGE: Ishimaru pulling a plain black hardcover notebook out of the gap.
    # It's the one clean thing in the room.
    subtitles "She wriggles her arm into the gap up to the shoulder and comes out with a notebook. Plain black hardcover, the elastic band still round it. It's the only thing in the entire room without dust on it."
    gloria "Let me see."
    lin "Why do you always get to see first?"
    gloria "Because I'll actually read it."

    # IMAGE: the three gathered around the open notebook on a bench.
    # Blue ballpoint, lists, arrows, crossed-out quantities.
    subtitles "Inside, page after page is covered in blue ballpoint. Lists of ingredients with quantities crossed out and rewritten. Arrows. Little diagrams of glassware. Question marks in the margins, a lot of them."

    gloria "Huh."
    lin "'Huh' what? Good huh or bad huh?"
    gloria "It's not old. Look at the ink, it hasn't faded at all. And the paper's new. This is the same kind of notebook they sell at the kiosk."
    gloria "Somebody was in here. Recently."
    ishimaru "Okay, I take it back, it's {i}really{/i} creepy now."

    lin "What even is it? Is it a recipe? It looks like a recipe."
    gloria "It's a formula. For... something you drink, I think. Listen:"
    gloria "'Subject E. Onset within fifteen minutes. Flushing, heat, marked drop in inhibition.' And then underneath: 'Fades too fast. Needs something to make it hold?'"
    ishimaru "Drop in {i}inhibition?{/i}"
    lin "Like... like being drunk?"
    gloria "Like being drunk without the drinking. Oh, this is fascinating. Who's subject E? And what does 'marked' mean, what's the scale, is there a scale, is it on the next page—"

    # A beat. Lin has gone quiet, reading over Gloria's shoulder.
    subtitles "Lin has gone quiet. She's reading the same line again, over Gloria's shoulder."
    lin "Fifteen minutes. Hot. And then you just... stop caring."
    lin "Hey. What were we doing last week? That afternoon, in that empty classroom by the admin corridor. You and me and Luna."
    gloria "We were..."
    subtitles "Gloria opens her mouth, and closes it again."
    gloria "We were talking. And then it was quarter past four and I didn't know where the time had gone."
    ishimaru "I got some weird cleaning stuff on my top that day. I remember taking it off. I don't really remember... after."
    subtitles "For a moment none of them says anything. Somewhere down the corridor a loose board creaks in the wind."

    lin "Okay, no. Nope. I'm not that kind of person, I don't do conspiracy theories. We were tired. It was a long day."
    lin "...It was a really weird day, though."

    gloria "We need to actually understand what this is. Properly. Not guess."
    lin "How? Half of this is words I've never seen in my life."
    gloria "Textbooks. Tomorrow, after last period. We go through it line by line and look up everything we don't know."
    ishimaru "Here? We're coming back {i}here?{/i}"
    gloria "It's got a whole room of free glassware, Ishimaru."
    ishimaru "...Okay, that's actually a good point."

    lin "And we don't tell anyone. Not Luna, not anyone. Not until we know what it is."
    ishimaru "Obviously."
    lin "I just wanted to say it out loud. So it's official."

    # IMAGE: the three leaving through the gate, Lin holding the notebook
    # against her chest; long shadows across the overgrown path.
    subtitles "They go out the way they came in. Lin carries the notebook, pressed flat against her chest with both arms, and doesn't let either of the others hold it all the way back."

    $ set_progress("lab_intro_discovery", 1)

    $ end_event("new_daytime", **kwargs)


# Secretary's Spin unlocks after The Discovery
label lab_intro_17 (**kwargs):
    $ begin_event(**kwargs)

    $ gloria = Person["gloria_goto"]
    $ ishimaru = Person["ishimaru_maki"]
    $ lin = Person["lin_kato"]

    # SCENE · lab_intro_17
    # The next afternoon in the old chemistry room. The three girls sit at a
    # bench with the notebook and a pile of borrowed textbooks. Emiko, who is
    # retracing the headmaster's steps from lab_intro_2 to find the notebook he
    # lost, hears them from the corridor and stops in the doorway. She
    # recognises his handwriting, and herself as "Subject E.". Instead of taking
    # it back she decides, on the spot, to let them have it: she reframes it
    # as a "love potion", offers supplies and supervision, and leaves the
    # notebook with them. No headmaster present → overheard, no paperdolls.

    # IMAGE: the three at the dusty bench; notebook open, textbooks stacked,
    # Gloria with a pencil behind her ear, Lin cross-legged on a stool,
    # Ishimaru sitting on the bench itself.
    subtitles "The next afternoon the old chemistry room has three schoolbags on the floor and a stack of borrowed textbooks on the bench, still in their plastic covers."

    gloria "Okay. 'Dosage per subject', that's just how much each person gets. Easy. 'Onset', that's how long before it starts working. Also easy."
    gloria "But look at how it's written. 'Subject E.' Just a letter. No consent form, no dates, no supervisor. A real trial has forms for everything. Forms for the forms."
    ishimaru "So... what does that mean?"
    gloria "It means whoever wrote this wasn't running it past anyone. And I don't know if subject E knew what she was drinking."
    lin "Right, okay, no. We're not doing this. I'm not that kind of person, I'm not sitting in a haunted building reading about someone secretly— you know. Doing stuff to people."
    lin "Can we please go back to the part where it's a recipe? I liked the part where it was a recipe."
    gloria "It's still a recipe. It's just a recipe with ethical questions."
    ishimaru "Gloria, you say that like it's a {i}good{/i} thing."

    # IMAGE: doorway. Emiko stands in it, tall, glasses, long black ponytail,
    # half in the corridor light; the girls haven't seen her yet.
    subtitles "None of them has noticed the figure in the doorway."
    emiko.think "*There it is. His notebook. He's turned his whole office upside down for that thing, and it's been sitting in the one building he swore he'd already searched.*"

    subtitles "Emiko knocks twice on the open door frame. All three of them jump. Ishimaru knocks a textbook off the bench."
    emiko "Well. I didn't expect to find a study group in here."
    ishimaru "Ms. Langley! Sorry! We weren't— sorry—"
    lin "We weren't doing anything bad. We're just— this is—"
    gloria "We found a research notebook hidden behind a shelf, and we've been cross-referencing it against the chemistry textbooks."
    lin "...Or that. She could have just said that."

    emiko "Relax. I'm not going to march you to the headmaster's office for being curious. I'd have to write a report, and I hate writing reports."
    emiko "What have you got there?"

    # IMAGE: Lin sliding the notebook across the bench, reluctantly.
    lin "We don't really know. Gloria thinks it's a formula."
    gloria "It {i}is{/i} a formula."
    subtitles "Lin hesitates for a second, then slides it across. Emiko picks it up in both hands, carefully, and turns the pages."

    # IMAGE: Emiko reading. Close on the page: blue ballpoint, "Subject E.".
    emiko.think "*His handwriting. All the little crossed-out numbers. That's the list he kept muttering over at his desk.*"
    emiko.think "*'Subject E. Onset within fifteen minutes. Flushing, heat, marked drop in inhibition.'*"
    emiko.think "*...That's me. That's the first night. He wrote it all down.*"
    subtitles "For just a moment the corner of her mouth goes soft. Then it's gone."

    ishimaru "Is it bad? It's bad, isn't it. You've got a face."
    emiko "I've always got a face."

    # She makes the decision. Her thoughts, then the spin.
    emiko.think "*He'd never let students anywhere near this. He's doing it all himself, from the top down, one careful teacher at a time, and it's wearing him thin.*"
    emiko.think "*And these three are going to try to brew it whether I'm here or not. Gloria's already halfway to a shopping list.*"
    emiko.think "*So, better with me than without me. And if it goes wrong, it's my name on it. Not his.*"

    emiko "Oh, this is sweet."
    lin "...Sweet?"
    emiko "It's a love potion."

    # IMAGE: the girls' faces. Ishimaru's eyebrows up; Lin sceptical;
    # Gloria tilting her head.
    ishimaru "Wait. Seriously? A real one?"
    lin "That's not a real thing. That's a thing from cartoons."
    gloria "She didn't say magic."
    emiko "Thank you, Gloria. Not magic. Chemistry. Things that change your mood, how warm you feel, how much you worry about what everyone else thinks. The kind of thing that makes people a little more... open to each other."
    emiko "Listen to this. 'Flushing, heat, marked drop in inhibition.' That's a blush, a warm face, and suddenly you're brave enough to say what you've been wanting to say. Whoever wrote this was a hopeless romantic."
    gloria "So it's pharmacology."
    emiko "In the most charming possible application, yes."

    # Lin brings up the afternoon they can't remember.
    lin "But the bit about subject E maybe not knowing. And... okay, this is going to sound stupid."
    lin "Last week the three of us had this afternoon where we just sort of... lost half an hour. We were all a bit weird. And then we find this, and it's all 'fifteen minutes' and 'heat', and—"
    subtitles "Emiko doesn't miss a beat."
    emiko "You three were giddy. It's spring. Half the school's giddy. I found two girls in the stationery cupboard last week giggling at a stapler."
    ishimaru "...At a {i}stapler?{/i}"
    emiko "I didn't ask. I've learned not to ask."
    subtitles "Lin laughs, a bit too loudly, and some of the tension goes out of her shoulders."
    emiko.think "*Good. Don't pull on that thread, sweetheart.*"

    # Gloria goes straight to the practical question.
    ishimaru "Could we actually make it, though? Like, for real?"
    gloria "Most of the ingredients are just... ingredients. It's the method that's vague. There are steps missing, temperatures missing, it never says how long anything sits. But the glassware's all here, and if we got the compounds, and did it really carefully—"
    lin "Hang on. You've already decided we're doing this."
    gloria "About two minutes ago. Possibly three."
    lin "..."
    lin "Okay, fine, I'm in. Obviously I'm in. I'm not letting you two blow yourselves up without me."

    subtitles "Emiko taps a finger on the cover of the notebook, as if she's thinking it over, though she's already thought it over."
    emiko "It would be quite advanced. But it's educational. Chemistry you can actually do something with. More than you'll get out of a worksheet."
    emiko "I could help you gather what you need. I've got keys to every storage room in this school, and the science budget has a little bit of money in it nobody ever remembers to spend."
    emiko "It's your project. I'd just be... a facilitator."
    ishimaru "Yes. Yes! Absolutely yes."
    gloria "I'll document everything. Properly."
    lin "Of course you will."

    # She hands the notebook back to Lin.
    subtitles "Emiko closes the notebook and holds it out to Lin, not Gloria."
    emiko "You found it, you keep it. Look after it."
    emiko "First job: go through this room and make a list of everything that still works. Glassware, burners, anything with a plug. Then I'll see what I can find to fill the gaps."
    lin "Thank you, Ms. Langley. Honestly. This is... actually really cool of you."
    emiko "Don't tell anyone I'm cool. I've got a reputation."

    # IMAGE: Emiko in the corridor outside, walking away. Behind her the girls
    # are already moving around the room, opening cupboards.
    subtitles "Out in the corridor, the three of them are already arguing behind her about who gets to open which cupboard."
    emiko.think "*He's going to be furious with me. Eventually.*"
    emiko.think "*But he's carrying the whole school on his own back, and he doesn't have to. Let them do this part. I'll keep an eye on them, and I'll keep him out of it.*"

    $ set_progress("lab_intro_discovery", 2)

    $ end_event("new_daytime", **kwargs)


# Gathering Ingredients unlocks after Secretary's Spin
label lab_intro_18 (**kwargs):
    $ begin_event(**kwargs)

    $ gloria = Person["gloria_goto"]
    $ ishimaru = Person["ishimaru_maki"]
    $ lin = Person["lin_kato"]

    # SCENE · lab_intro_18
    # A few days later, late afternoon in the old chemistry room. The three
    # girls go through every cupboard and shelf. Ishimaru stands on a wobbly
    # chair at the high cupboards, Lin checks glassware against the light,
    # Gloria works through the drawers with a list. The bench fills up with
    # beakers, flasks, a measuring cylinder, stirring rods, tubing. They're
    # missing a heat source and the chemicals. Emiko arrives with a cardboard
    # box: a hot plate, basic chemicals from the stockroom, goggles and gloves.
    # She makes them promise to wear the safety gear, and asks to be there for
    # the first brew. No headmaster present → overheard, no paperdolls.

    # IMAGE: the three searching the room. Ishimaru up on a chair at the high
    # cupboards, Lin holding a flask up to the window, Gloria kneeling at a
    # low drawer with a notebook of her own.
    subtitles "A few days later the old chemistry room has the windows propped open, and every cupboard door is standing wide."

    ishimaru "Found beakers! A whole set, up here, all different sizes! Hang on, I'll pass them down—"
    subtitles "The chair wobbles. Ishimaru grabs the cupboard door, and the cupboard door creaks in a way cupboard doors shouldn't."
    lin "Okay, maybe pass them down {i}slowly.{/i} Maybe pass them down one at a time, like a normal person, instead of doing a circus act."
    ishimaru "I'm fine! I'm totally fine. Sorry. I'm fine."
    gloria "Check the rims before you hand them over. If there's a chip, it can crack when it's heated, and then you've got boiling liquid all over your hands."
    ishimaru "They look fine."
    gloria "Look properly."
    subtitles "Ishimaru holds each one up in front of her nose and turns it round, very slowly, squinting."
    ishimaru "...They still look fine. But now I've looked {i}properly.{/i}"

    # IMAGE: Lin at the window with a graduated cylinder, sunlight through the
    # markings.
    lin "Ooh, this one's perfect. Not a scratch on it, and you can still read all the little lines."
    gloria "That's the measuring cylinder. That's the most important thing in this room, honestly. If we can't measure it properly, we can't dose it properly."
    lin "Right. 'Dose it properly.' Listen to me. I'm saying things like 'dose it properly' now. Last month I was watching videos of cats falling off sofas."
    gloria "You still watch videos of cats falling off sofas."
    lin "Yes, and I'll never stop. I contain multitudes."

    # IMAGE: Gloria at a deep drawer, recoiling slightly.
    subtitles "Gloria pulls open one of the deep drawers under the bench and leans back from it."
    gloria "This drawer smells like something died in it in 1994."
    gloria "But there's rubber tubing in here, and it still bends. And glass stirring rods. Glass doesn't go off. We can use all of this."
    subtitles "She writes it down. She's been writing everything down."
    lin "Hang on. Have you got an actual list?"
    gloria "I've had a list since the day we found the notebook. It's got sections."
    lin "Of course it's got sections."

    # IMAGE: the bench, now covered in salvaged glassware; the notebook open
    # beside it. The three of them standing round it.
    subtitles "By half past four the bench is covered: beakers, flasks, test tubes, the measuring cylinder standing on its own in the middle like a trophy."
    lin "So. Glassware? Done. Heat? Nothing. Actual ingredients? Nothing."
    ishimaru "There's no way anything in this building's still usable. They'd have cleared out the chemicals years ago. You can't just leave chemicals lying around."
    gloria "Somebody left a whole lab lying around."
    ishimaru "...Okay, yes, fair."
    lin "Maybe Ms. Langley knows if the school's got a—"

    # IMAGE: Emiko in the doorway, carrying a cardboard box against her hip.
    emiko "Knows if the school's got a what?"
    subtitles "Emiko comes in with a cardboard box on her hip, and sets it down on the one clear corner of the bench with a heavy, rattling thump."
    ishimaru "We found nearly all the glassware! But we haven't got anything to heat it with, or any of the actual—"
    emiko "A heat source and the chemicals. I did read your list, you know. Gloria left a copy on my desk."
    gloria "I thought you'd want to be informed."
    emiko "I did. It had a contents page."

    # IMAGE: the open box. A portable hot plate, new rubber tubing, clamps,
    # goggles, gloves, several small bottles of chemicals, some still sealed.
    subtitles "She pulls the flaps open. There's a portable hot plate on top, still with its old inventory sticker, then clamps and tubing, and underneath all of it a row of small brown bottles."
    emiko "The hot plate's from the old physics room. Nobody's touched it since before I started here, but I plugged it in this morning and it didn't catch fire, so that's promising."
    emiko "And the chemistry stockroom still had most of the basics."
    ishimaru "Are you {i}serious?{/i} Oh my God. Oh my God, thank you!"
    lin "This is proper stuff. Like, actual lab stuff. How did you even get all this?"
    emiko "I've got keys to every door in this school. You'd be amazed what's sitting in a cupboard with a label that just says 'MISC.'"

    # IMAGE: Gloria and Lin reading bottle labels against the notebook;
    # Ishimaru turning the hot plate over in her hands.
    gloria "Distilled water. Ethanol. Potassium hydroxide, that's the one the notebook underlines twice... This is almost all of it. This is nearly everything on the list."
    gloria "Almost everything. The organic compound on page four, the one with the name that goes on forever, that isn't here."
    emiko "No. That one's a bit specialised. Nothing dangerous, just not something a school keeps on a shelf. Any chemistry supplier online will have it."
    lin "We can split it. Three ways."
    ishimaru "Four ways if Ms. Langley wants in."
    emiko "Ms. Langley already bought a hot plate's worth of electricity. Three ways."

    # Emiko hands out goggles and gloves; the teasing drops away.
    subtitles "Emiko digs down to the bottom of the box and comes up with three pairs of safety goggles and a box of gloves. When she holds them out, she isn't smiling any more."
    emiko "These go on every single time. Every time, from the second you switch that plate on until it's cold again. I mean it."
    emiko "Potassium hydroxide will take the skin off your fingers. If one of you ends up in hospital with burnt hands, this whole thing ends that day, and I'm the one who has to explain it."
    lin "We promise. Honestly. Every time."
    emiko.think "*They're so eager it hurts. Please be careful, the three of you. I can't stand behind you every single minute.*"
    emiko.think "*...He's in that cupboard of his right now, probably, with his goggles pushed up on his head, making exactly the same face Gloria's making.*"

    lin.think "*She's handing us safety gear for a project she could've shut down in thirty seconds. She actually wants this to work. That's... kind of amazing, actually.*"

    ishimaru "So once the last bit arrives, we could actually start? Like, actually make it?"
    emiko "Once it arrives, yes. You follow the method exactly, you measure everything twice, and you'll be fine."
    emiko "And when you're ready to brew for the first time, you tell me first. I want to be there."
    ishimaru "Definitely! Thank you so much, Ms. Langley. Seriously."

    subtitles "Emiko picks up the empty box, tucks it under her arm, and stops at the door."
    emiko "Oh, and Ishimaru? Get down off chairs slowly. I heard that cupboard door all the way from the stairs."
    ishimaru "...Sorry."

    # IMAGE: Emiko leaving down the corridor; behind her the three girls
    # crowding round the box.
    emiko.think "*They'll do it properly. Gloria won't let them do it any other way.*"
    emiko.think "*And if they don't, I'll be there to catch it.*"

    # IMAGE: the three alone with the bench full of equipment, late light
    # going gold through the dirty windows.
    subtitles "When the sound of her footsteps has gone, the three of them just stand there for a moment, looking at the bench."
    ishimaru "She gave us a {i}hot plate.{/i} A school secretary gave us a hot plate and a box of chemicals. Is this real? This doesn't feel real."
    lin "And she wants to come and watch. Like it's our school play or something."
    ishimaru "She believes in us."
    gloria "She believes in the project."
    lin "Gloria, you are {i}so{/i} weird. That's such a Gloria thing to say. You know that, right?"
    gloria "I know. I've made my peace with it."

    ishimaru "I'll do the order tonight. Split three ways?"
    lin "Deal."
    gloria "I'll write the whole method out before it gets here. Step by step, with the temperatures filled in where the notebook doesn't say. So we're not making it up as we go along when it actually matters."

    lin "We're making a love potion. In an abandoned building. And the school secretary is our lab supervisor."
    lin "This is either the best thing I've ever done, or we're all getting expelled."
    ishimaru "Can it be both?"
    lin "It's probably going to be both."

    $ set_progress("lab_intro_discovery", 3)

    $ end_event("new_daytime", **kwargs)


# Brewing Session unlocks after Gathering Ingredients between Monday and Wednesday
label lab_intro_19 (**kwargs):
    $ begin_event(**kwargs)

    $ gloria = Person["gloria_goto"]
    $ ishimaru = Person["ishimaru_maki"]
    $ lin = Person["lin_kato"]

    # SCENE · lab_intro_19
    # Early evening in the old chemistry room. The online order has arrived.
    # The three girls, in goggles and gloves, brew the formula for the first
    # time on the hot plate, with Gloria's written-out method and the notebook
    # propped up beside it. Emiko watches, arms folded, and fills in the gaps
    # the notebook leaves out. The mixture goes cloudy, then muddy brown, then
    # clears into glowing amber. The girls decide to test it at a party in the
    # old lab that weekend, and want to invite everyone. Emiko bottles the
    # batch. No headmaster present → overheard, no paperdolls.

    # IMAGE: the bench set up for brewing. Hot plate, beakers, measuring
    # cylinder, small brown bottles in a row. The three girls in goggles;
    # Emiko a step back with her arms folded. Evening light through the windows.
    subtitles "The parcel came on Tuesday. By six o'clock on Wednesday the bench in the old chemistry room looks like an actual lab: hot plate in the middle, bottles lined up in the order they'll be used, Gloria's handwritten method taped to the wall at eye level."
    subtitles "All three of them are wearing their goggles. Nobody even had to be reminded."

    gloria "Right. Step one. Two hundred millilitres of distilled water, low heat."
    lin "Low heat. Okay. What's low? Is low one? Is it two? There's no numbers on this thing, it's just a picture of a little flame."
    emiko "Start at the smallest little flame. You can always go up. You can't un-boil something."
    ishimaru "'You can't un-boil something.' That's so wise. I'm writing that down."

    # IMAGE: Ishimaru carrying the measuring cylinder with both hands, very
    # slowly, tongue between her teeth.
    subtitles "Ishimaru carries the full measuring cylinder across the room with both hands, at roughly the speed of a glacier, and the other two watch her the whole way without breathing."
    ishimaru "I'm fine. I'm fine. I've got it. I've g— okay. Okay, I've got it."
    subtitles "The water goes into the beaker. All three of them breathe out at once."

    gloria "Next: ethanol, fifty millilitres. My method says add it immediately."
    emiko "Give the water two minutes first."
    gloria "The notebook doesn't say to wait."
    emiko "The notebook doesn't say a lot of things. You don't pour something cold into something warm all at once. And pour it down the side of the glass. Slowly."
    emiko.think "*I've watched him fuss over his flasks often enough. He never pours anything in cold, and he talks to every single drop.*"

    # IMAGE: Lin tilting the cylinder, ethanol running down the inside of the
    # beaker; a faint shimmer where it meets the water.
    lin "Down the side, down the side... is this slow enough? Tell me if it's too fast. Actually don't tell me, you'll make me jump."
    emiko "That's perfect."
    subtitles "A sharp, clean smell of alcohol rises off the beaker and mixes with the dust."

    # Potassium hydroxide.
    gloria "Potassium hydroxide. Ten grams. Gloves on."
    ishimaru "Gloves are on! Look. Gloves."
    emiko "Don't touch your face. Don't touch anything, actually, until that's in."
    subtitles "Gloria tips the white granules in off the paper. They hiss very faintly as they hit the liquid, and the whole beaker clouds over, milky, and then slowly starts to go brown."
    lin "Oh. Oh, that's... that's disgusting. It looks like pond water."
    gloria "It's supposed to look like pond water. It's in the notes. 'Muddy brown, don't panic.'"
    lin "It actually says 'don't panic'?"
    gloria "It actually says 'don't panic.' Underlined."
    emiko.think "*Of course he wrote that. That is exactly, precisely what he would write.*"

    # The last ingredient; Emiko stops them.
    gloria "Last one. The organic compound. Twenty-five millilitres, and I've written medium heat for this bit, so—"
    emiko "Wait."
    subtitles "Ishimaru freezes with the little bottle tilted over the beaker. Emiko holds her hand just above the glass, not touching it, for a few seconds."
    emiko "Still too cool. Another minute, then turn it up."
    gloria "How can you possibly tell that by just holding your hand there?"
    emiko "Experience."
    gloria "That's not an answer. That's a word."
    emiko "It's a very good word. Give it a minute."
    emiko.think "*'Needs something to make it hold?' Question mark. He wrote that and then lost the notebook before he ever found out.*"
    emiko.think "*So whatever they make tonight won't last. A few minutes of silliness. Nobody gets hurt by a few minutes of silliness.*"

    # Medium heat. The compound goes in; the mixture darkens further.
    subtitles "Lin turns the dial up. After a minute Emiko nods, and Ishimaru pours in the last compound, slowly, down the side. The mixture goes darker still, almost the colour of coffee."
    lin "Is it meant to get darker? It's getting darker. That feels like the wrong direction."
    emiko "Look at the edges. Where it touches the glass."

    # IMAGE: close on the beaker. A thin line of gold where the liquid meets
    # the glass, spreading inwards.
    subtitles "At first there's nothing. Then, right at the rim where the liquid touches the glass, there's a thin line that isn't brown any more. It's gold."
    ishimaru "There! There, look, it's changing, it's going— is that it? Is that it?"
    subtitles "The gold creeps inwards from the edges. The mud thins out and clears, the whole beaker brightening from the outside in, until there's nothing left in it but clear, shimmering amber, lit from underneath by the glow of the hot plate."
    subtitles "A sweet, faintly floral smell drifts up out of it and fills the room."
    lin "Oh my God. Oh my {i}God.{/i} We did it. We actually did it!"
    ishimaru "It's so pretty! It's like honey! It's like drinking-a-sunset honey!"
    gloria "It went exactly how the notes said. {i}Exactly.{/i} Every stage. Do you know how rare that is? Nothing ever goes exactly how the notes say, not in real labs, not ever—"
    lin "Gloria, you're allowed to just be happy."
    gloria "I am happy. This is what happy looks like on me."

    emiko "Well done. Honestly. Very well done, the three of you."
    subtitles "She reaches past them and switches off the hot plate."
    emiko "Leave it to cool before anybody touches it."

    # The party idea.
    ishimaru "So... does it actually work? Like, as a love potion? Like, for real?"
    emiko "The chemistry worked. Whether it does anything to people..."
    emiko "Well. That you'd have to find out."
    lin "We could try it. Just a tiny bit, just us?"
    emiko "You could. But three people staring at each other waiting to feel something won't tell you much. You'd want a proper crowd. Somewhere relaxed. See what happens when people are just being themselves."

    subtitles "The three of them look at each other."
    lin "A party. Here. This weekend."
    ishimaru "Yes! Fairy lights! Music! We can put the potion in a big bowl like a punch and call it something stupid!"
    gloria "Love Potion Number Nine."
    lin "That's already a song, Gloria."
    gloria "Then it's a reference. People like references."

    emiko "Keep it to your close friends, though. A small group."
    lin "It's a small school, Ms. Langley. Everybody's close friends with everybody. If we invite some people and not others, it'll be a whole thing, there'll be crying in the toilets on Monday."
    ishimaru "We should just invite everyone. Everyone! The whole school! Everybody!"
    subtitles "Emiko sighs, as if they've talked her into something."
    emiko "...Fine. Everyone. But you'll need a lot more than one beaker's worth."
    gloria "We'll scale it up. I'll redo the quantities tonight. We can do four batches before Friday if we come every day."
    emiko.think "*Everyone. The whole school, all at once.*"
    emiko.think "*...That's rather more than I'd dared to hope for.*"
    emiko "And I'll be around on the night. Nearby. Just in case."
    lin "Would you? Honestly, that'd make me feel way better."

    # IMAGE: Emiko pouring the cooled amber from the beaker into a stoppered
    # glass bottle; the girls watching.
    subtitles "When it's cool, Emiko pours it off into a clean glass bottle, holding it steady against the light, and presses the stopper in with her thumb."
    emiko "Somewhere cool and dark. Not in anybody's dorm room where a roommate can find it and drink it for a dare."
    ishimaru "How long does it keep?"
    emiko "Weeks, if you're careful with it. It'll be fine until the weekend."

    subtitles "She holds the bottle out to Lin, the same way she handed her the notebook."
    emiko "Your first proper synthesis. Congratulations. You're real chemists now, God help us all."
    lin "Thank you, Ms. Langley. Seriously. For all of it."
    emiko "Goodnight. And goggles on for the next four batches, all of you. I'll check."

    # IMAGE: the three alone with the bottle glowing on the bench in the
    # darkening room.
    subtitles "The door closes behind her. The room is almost dark now, and the bottle on the bench is the brightest thing in it."
    ishimaru "This weekend is going to be incredible."
    lin "I just want to know if it works. I really, really want to know if it works."
    gloria "It will. Everything else in that notebook has been right."

    $ set_progress("lab_intro_discovery", 4)

    $ end_event("new_daytime", **kwargs)


# Secretary Enhancement - Friday afternoon, after the PTA Refreshments and Brewing Session
label lab_intro_20 (**kwargs):
    $ begin_event(**kwargs)

    $ gloria = Person["gloria_goto"]
    $ ishimaru = Person["ishimaru_maki"]
    $ lin = Person["lin_kato"]

    # SCENE · lab_intro_20
    # Friday afternoon, a few hours after the PTA meeting and a few hours before
    # the party. In the old chemistry room the girls have four batches of the
    # weak potion bottled on the bench and are sorting out cups and fairy
    # lights. Emiko arrives with a small brown glass bottle: the catalyst,
    # secretly poured off from the headmaster's Orgazyme jug. She tells them
    # it's a stabiliser that makes the effect hold. They split the whole bottle
    # evenly between their bottles and watch the amber deepen. She tells them
    # to keep what's in it to themselves, and leaves. No headmaster present →
    # overheard, no paperdolls.

    # IMAGE: the old chemistry room, late afternoon. A row of stoppered bottles
    # of amber potion on the bench. A tangle of fairy lights, a stack of
    # plastic cups, a speaker. The three girls busy.
    subtitles "Friday, just after three. The bench in the old chemistry room has a row of eleven stoppered bottles on it, all the same pale amber, and next to them a stack of plastic cups, a speaker with a cracked grille, and a heap of fairy lights so tangled it's basically one object."

    lin "Okay, who packed the fairy lights? Because whoever packed them did it by throwing them into a bag and then fighting the bag."
    ishimaru "...That might have been me. Sorry. They were already like that! Mostly!"
    gloria "Four batches, eleven bottles. That's enough for everyone, plus about fifteen percent extra for people who go back for more."
    lin "People are going to go back for more of a drink called Love Potion Number Nine? Honestly?"
    gloria "People will drink anything if you put it in a bowl and give it a silly name. That's not a guess, that's just how parties work."

    # IMAGE: Emiko in the doorway, small leather bag over her shoulder.
    subtitles "Emiko comes in with her bag over her shoulder, still in her work clothes, and looks at the row of bottles for a long moment before she says anything."
    emiko "Eleven. You've been busy."
    ishimaru "Ms. Langley! We finished the last batch this morning. Before class. Well. Instead of the first bit of class. A little bit."
    emiko "I didn't hear that."

    emiko "Before tonight, though. I've brought you something."

    # IMAGE: Emiko taking a small brown glass bottle out of her bag. The liquid
    # inside is pale and slightly cloudy.
    subtitles "She takes a small brown glass bottle out of her bag and sets it down in front of the row. The liquid inside is pale and a little cloudy, and when she turns it, it moves slower than water."
    lin "What's that?"
    emiko "Your notebook keeps asking for something. 'Fades too fast. Needs something to make it hold?' You remember."
    gloria "Page six. Question mark."
    emiko "Well. I did some reading. This is something to make it hold."
    emiko "It's a stabiliser. Without it, whatever you've made lasts a few minutes and then it's gone, everyone giggles, and nobody's quite sure what happened. With it, it actually... takes."

    emiko.think "*Two hundred millilitres out of his jug. Most of what he had left.*"
    emiko.think "*I put it back exactly where it was, behind the paint tins, with DO NOT TOUCH facing out. He'll notice, eventually. He's going to be so angry.*"
    emiko.think "*...He'll understand. He will. Not tonight, but he will.*"

    ishimaru "Is it safe, though? Like, properly safe?"
    emiko "I've had some myself."
    subtitles "It's true, in its way. She doesn't say more than that."
    ishimaru "Oh. Okay. Okay, then that's fine."

    # How to use it. Kept vague: the whole bottle, split evenly.
    gloria "What's the ratio?"
    emiko "All of it, split evenly between every bottle. Exactly evenly. If one bottle gets more than the others, somebody's going to have a much stranger evening than everybody else."
    lin "How do we make it even? There's eleven."
    gloria "Measuring cylinder. Divide by eleven. I'll do it. Nobody else touch it."

    # IMAGE: Gloria at the measuring cylinder, Ishimaru unstoppering bottles in
    # a row, Lin writing each amount on a scrap of paper.
    subtitles "They set it up like a production line without anybody saying so. Ishimaru takes the stoppers out one at a time. Gloria measures. Lin writes each one down on the back of a flyer for the party."
    gloria "First one."
    subtitles "The pale liquid runs into the first bottle and vanishes. For a second nothing happens."
    ishimaru "Is it... doing anything? I can't tell if it's doing anything."
    lin "Watch the colour."

    # IMAGE: close on the first bottle. The pale amber deepening into a rich,
    # glowing honey colour. Lin's face reflected in the glass.
    subtitles "Slowly, the amber deepens. Pale tea turns to strong tea, then to honey, then to that rich, glowing gold that looks lit from inside even with the sun behind it. A sweet, fruity smell comes off the open neck of the bottle."
    lin "Oh."
    ishimaru "Oh, it's {i}gorgeous.{/i} It looks like it'd taste like... like the smell of a bakery."
    emiko "It doesn't. It tastes a bit sweet. That's all."

    emiko "Don't rush the last few. Every bottle the same."
    gloria "I know. I know. I'm not rushing. Ishimaru, stop breathing on the cylinder."
    ishimaru "I'm not breathing on it!"
    ishimaru "...I'll breathe somewhere else."

    # IMAGE: all eleven bottles now the same deep gold; Gloria pressing the
    # last stopper home.
    subtitles "When the last bottle's done, the whole row glows the same deep gold, and the empty brown bottle sits at the end of it like a full stop."
    gloria "Eleven. All even. I've checked it twice."
    lin "Of course you have."

    # Testing on themselves: Emiko says no.
    ishimaru "Should we try it first? Just a sip each, to see? Like a taste test?"
    emiko "No. You're hosting. Hosts stay clear-headed until the doors open. After that, have a cup like everybody else."
    lin "That's a very sensible rule. I don't like it, but it's very sensible."

    subtitles "Emiko puts the empty bottle back in her bag and picks up the bag."
    emiko "Keep them sealed until tonight. Somewhere cool."
    emiko "And that little bottle was never here. If anyone asks, it's your recipe, straight out of your notebook, start to finish."
    lin "It's our thing. Obviously."
    emiko "Good. Have a lovely party."

    # IMAGE: the door closing; the three girls alone with the glowing bottles.
    subtitles "The door closes behind her. For a moment none of them says anything. The speaker ticks as it warms up."

    lin "...Tonight."
    ishimaru "Tonight!"

    subtitles "Lin picks up one of the bottles and holds it up to the window. The light comes through it gold and warm, and her own face looks back at her from the curve of the glass, stretched and strange."
    lin.think "*Everybody thinks it's a joke. A silly drink in a bowl with a silly name.*"
    lin.think "*...It probably is a joke. Probably.*"
    subtitles "She puts the bottle back in the row very carefully, as if it might wake up."

    # IMAGE: Emiko in the corridor outside, walking away, bag over her shoulder.
    emiko.think "*Now I just have to be there. All night. Somewhere they won't notice me.*"
    emiko.think "*And first thing Monday, I tell him. ...Or maybe Tuesday.*"

    $ set_progress("lab_intro_discovery", 5)

    $ end_event("new_daytime", **kwargs)


# The Party - Friday night on the same day as the PTA Refreshments
label lab_intro_21 (**kwargs):
    $ begin_event(**kwargs)

    $ lin = Person["lin_kato"]
    $ gloria = Person["gloria_goto"]
    $ ishimaru = Person["ishimaru_maki"]
    $ aona = Person["aona_komuro"]
    $ miwa = Person["miwa_igarashi"]
    $ kokoro = Person["kokoro_nakamura"]
    $ sakura = Person["sakura_mori"]
    $ easkey = Person["easkey_tanaka"]
    $ soyoon = Person["soyoon_yamamoto"]
    $ hatano = Person["hatano_miwa"]
    $ seraphina = Person["seraphina_clark"]
    $ luna = Person["luna_clark"]
    $ ikushi = Person["ikushi_ito"]
    $ elsie = Person["elsie_johnson"]
    $ yuriko = Person["yuriko_oshima"]

    # SCENE · lab_intro_21
    # Friday night in the old chemistry room, turned into a party: fairy lights
    # strung across the ceiling, a speaker, a big bowl of "Love Potion Number
    # Nine" on the bench. The whole school comes. Everyone drinks, most of
    # them treating it as a joke. After about a quarter of an hour the effect
    # hits: heat, giggling, touching. It builds from dancing and a first kiss
    # to most of the room half-undressed and making out: Aona dancing topless
    # on a bench, Miwa and Kokoro, Sakura and Easkey, Soyoon and Hatano, Elsie
    # and Yuriko. The Clark twins slip away together into the side room
    # (implied only). Emiko watches unseen from the dark corridor. Around
    # eleven it ebbs; the girls drift back to the dorms confused and dishevelled.
    # Emiko gathers the empty bottles and takes the notebook out of Lin's bag.
    # No headmaster present → overheard, no paperdolls.

    ########################################
    # The party starts

    # IMAGE: the old chemistry room transformed. Fairy lights zigzagging under
    # the ceiling, the speaker on a stool, the big glass bowl of glowing gold
    # punch on the bench with a ladle and a stack of cups. Girls arriving.
    subtitles "Friday night. Behind the sports field, the old lab building has lights on for the first time in thirty years."
    subtitles "Inside, the fairy lights zigzag under the ceiling of the chemistry room, and somebody's speaker is thumping out something with a lot of bass. The whole place smells of dust, cheap body spray, crisps, and underneath it all something sweet and fruity coming off the big glass bowl on the bench."

    aona "Oh my God, this is {i}so{/i} much better than I thought it'd be. It's like a haunted house, but with snacks!"
    lin "Welcome, welcome, come in, mind the broken tile, everybody gets one cup of Love Potion Number Nine on the way in, that's the entry fee, those are the rules!"
    seraphina "Does it actually do anything?"
    lin "It absolutely does not. It's lemony. It's a joke, it's a whole bit, just go with it."
    seraphina "Boo. I wanted to fall in love."
    lin "Drink two, then."

    # IMAGE: Lin at the bowl ladling gold punch into cups; a queue of girls;
    # Gloria beside her with a clipboard.
    subtitles "Lin ladles it out as fast as the cups come. Gloria stands next to her with a clipboard, taking notes on everyone who drinks, which everyone assumes is part of the bit."
    gloria "Name, please. And roughly what time you're drinking it."
    ikushi "Why do you need my name?"
    gloria "Data."
    ikushi "...Fine. But you're not writing down anything else."
    subtitles "Ikushi drains her cup in one go, looks faintly surprised at herself, and holds it out for another."

    # Yuriko, dragged in by Elsie.
    subtitles "Near the door, Elsie Johnson has Yuriko Oshima by the wrist, as if she's afraid Yuriko will bolt the moment she lets go."
    elsie "You said you'd stay for twenty minutes. You promised."
    yuriko "I said I'd {i}consider{/i} staying for twenty minutes."
    elsie "Just have one cup. Please? Everyone keeps asking if you're okay, because you're standing in the doorway like a vampire."
    yuriko "Fine. One. To shut everyone up."
    subtitles "She drinks it like medicine, grimacing, and hands Elsie the empty cup."
    yuriko "It's sweet. Horrible. There. Twenty minutes."

    # Ishimaru with her guitar.
    subtitles "In the corner, Ishimaru has got her guitar out of its case and is picking along with whatever's on the speaker, mostly in tune."
    ishimaru "Sorry! Sorry, is this annoying? I can stop. I'll stop. I'm stopping. ...I'm going to play one more."

    ########################################
    # Fifteen minutes in: the heat

    # IMAGE: the room a little later; a girl fanning herself with a paper plate,
    # another leaning back against the wall with her eyes closed.
    subtitles "Fifteen minutes later, somebody opens a window. It doesn't help."

    miwa "Is it hot in here? It's so hot in here. Is it just me? It's not just me, is it, everyone's gone all pink."
    kokoro "It's... yeah. I'm really warm. I feel sort of... fizzy? Like my whole body's fizzy."
    miwa "Fizzy! Yes! Oh my God, that's exactly it. Come and dance, I can't stand still, I have to move or I'm going to explode."
    kokoro "I don't really dance..."
    miwa "Everybody dances. You just haven't done it yet."

    gloria "Twenty-one-oh-four. Multiple reports of heat, flushing. Kokoro describes it as 'fizzy.' Good word. Writing that down. Fizzy..."
    subtitles "Gloria looks at her own clipboard for a while, as if the handwriting on it belongs to someone else."
    gloria "Why am I— it's very hard to hold a pen. Has anyone else noticed pens are really hard to hold?"

    # Aona takes the centre of the room.
    subtitles "Aona has climbed up onto one of the old workbenches, cup in one hand, and is dancing on it, badly and enthusiastically, to cheering."
    aona "Everybody look at me! No, look! Are you looking? This is the best party in the history of this school, and it's in a {i}ruin!{/i}"
    seraphina "Take your top off!"
    aona "Ha! As {i}if—{/i}"
    subtitles "She laughs, and keeps dancing, and then stops laughing, with an odd look on her face, as if she's actually thinking about it."
    aona "...Actually. Actually, it is really hot."

    # IMAGE: Aona pulling her uniform blouse over her head on the bench and
    # flinging it into the crowd; she's in her bra, grinning.
    subtitles "She pulls her blouse off over her head in one go without undoing any buttons and flings it into the crowd. The whole room screams. She stands up there in her bra with her arms up like she's won something."
    aona "Oh, that's {i}so{/i} much better. Why didn't I do that ages ago?"
    aona.think "*Everybody's looking at me. Every single person. Oh God, I love it. I love it, I love it.*"

    ########################################
    # The first kiss

    # IMAGE: Miwa and Kokoro dancing close under the fairy lights; Miwa tucking
    # a strand of hair behind Kokoro's ear.
    subtitles "Under the fairy lights, Miwa has got Kokoro dancing after all: slowly, badly, very close, both of them laughing every time they bump."
    miwa "Your hair's so soft. Sorry. Is that weird? I've wanted to say that for ages. I've wanted to say a lot of things for ages."
    kokoro "Like... what things?"
    miwa "Like, um. Like how you do this thing when you're reading where you bite your lip, and I have to look somewhere else, because otherwise I'd just stare at your mouth the whole lesson. Like that sort of thing."
    kokoro "Oh."
    kokoro "...You can look at it now, if you want."
    miwa.think "*Oh my God. Oh my God, okay, she said that, she actually said that, don't just stand here, do something—*"

    # IMAGE: the kiss. Miwa leaning in, Kokoro meeting her halfway; both of
    # them freezing for a second, then not pulling away.
    subtitles "Miwa kisses her. For a second they both freeze, as if waiting for somebody to stop them. Nobody does. Kokoro makes a small, surprised sound against her mouth and kisses her back, and then her hands are on Miwa's waist, holding on."
    kokoro "Mmh— is this okay? Are we allowed to—"
    miwa "I don't care. I don't care if we're allowed. Do it again."

    subtitles "Someone near the bowl whistles. Someone else says {i}finally{/i}. And then, somehow, it's like a door has opened in the room."

    ########################################
    # It spreads

    # IMAGE: Sakura and Easkey against the wall; Easkey fumbling with the
    # buttons of Sakura's blouse.
    subtitles "By the wall, Sakura Mori is fanning herself with both hands, her face bright red, and her blouse already has the top two buttons undone."
    sakura "It's that warm feeling again. Like that day in the corridor, remember? Like I'm melting from the inside."
    easkey "I- I remember. You- you opened your blouse, and I told you you c-can't, and you went all—"
    sakura "And I was so embarrassed."
    easkey "Yeah."
    subtitles "Easkey is staring at the third button. Her hands are shaking a little."
    easkey "I- I think I was wrong. That time. I think you c-can. If you want. I could... I could help?"
    subtitles "Sakura blinks at her. Then she takes Easkey's hands and puts them on the button herself."
    sakura "Yes, please. God. Please."

    # IMAGE: Sakura's blouse open, bra showing; Easkey's hands on her waist;
    # Sakura reaching behind herself to unhook the bra.
    subtitles "Easkey gets the buttons open one at a time, stammering an apology for each one. When the blouse falls open, Sakura reaches behind herself, unhooks her bra, and lets it slide off her shoulders, and just stands there with her eyes closed, bare to the waist, breathing out like she's been underwater."
    sakura "Oh, that's so much better. It's so much cooler. Touch me, it's okay, I want you to."
    easkey "Your skin's so warm—"
    easkey.think "*She's letting me. She's asking me. I've thought about this so many times, I've never, ever thought she'd ask.*"

    # Soyoon and Hatano, the rival fashionistas.
    subtitles "On the far side of the room, Soyoon Yamamoto is leaning against a cabinet with her arms folded and one eyebrow up, watching all of it with an expression of great superiority. Her cheeks are pink. Her second cup is empty."
    hatano "Oh, stop it, Soyoon, you're dying to. Look at you, you're redder than your lipstick."
    soyoon "I'm not 'dying to' do anything. I simply think it's all a bit... undignified."
    hatano "You think {i}everything's{/i} undignified. You thought my platforms were undignified."
    soyoon "Your platforms {i}were{/i} undignified."
    hatano "And you looked at them all day."
    subtitles "Soyoon opens her mouth to say something cutting. Nothing comes out. Hatano steps in close, close enough that their noses nearly touch."
    soyoon "...Fine. But only because it's you. And only because I've decided to, not because you said so."
    hatano "Obviously, your majesty."
    subtitles "Soyoon grabs a fistful of Hatano's collar and kisses her, hard, as if she's winning an argument. Hatano laughs into it. Within about a minute Soyoon's perfect hair is completely ruined, and she doesn't seem to mind at all."
    soyoon.think "*I'm going to be so furious about my hair tomorrow. Tomorrow. Not now.*"

    ########################################
    # The peak

    # IMAGE: wide shot of the room around ten. Colored fairy light, clothes on
    # the floor, pairs and threes in every corner.
    subtitles "By ten o'clock nobody's pretending it's just a party any more."
    subtitles "Blouses hang open or lie in heaps on the benches. Skirts have been kicked into corners. The fairy lights make everything gold and pink and blurry. Every corner has somebody in it, two or three together, pressed up against each other and against the walls, and under the music there's a steady sound of breathing and laughing and small, surprised moans."

    # Miwa and Kokoro, on the bench.
    # IMAGE: Kokoro sitting on the edge of a workbench, blouse off, bra pushed
    # up; Miwa standing between her knees, mouth at her breast, a hand up under
    # her skirt; Kokoro's head thrown back.
    subtitles "Kokoro is sitting on the edge of the workbench with her blouse gone and her bra pushed up out of the way, and Miwa is standing between her knees, kissing her way down her chest. Kokoro's got both hands in Miwa's hair."
    kokoro "Ahh— Miwa— hah, that's... that's so— don't stop, don't stop, okay?"
    miwa "Not stopping. Never stopping. You're so soft, how are you so {i}soft—{/i}"
    subtitles "Miwa's hand slides up under the hem of Kokoro's skirt, slowly, giving her every chance to say no. Kokoro doesn't say no. She makes a high, shaky sound, grips the edge of the bench, and pulls Miwa closer with her knees."
    kokoro "Mmnh— ahh— {i}oh—{/i} oh my God—"
    kokoro.think "*Everybody can see. Everybody can see us. And I don't— I can't make myself care, I can't, it feels too good—*"

    # Aona, now topless on the bench.
    subtitles "Aona is still up on her bench. Her bra went a while ago; somebody's wearing it on their head. She's dancing topless in the fairy lights with her arms up, and every time the crowd cheers she dances harder."
    aona "Look at me! Look! Am I the best? Tell me I'm the best!"
    seraphina "You're the best, Aona!"
    aona "I KNOW!"

    # Ikushi, caving and then owning it.
    subtitles "Ikushi is in a corner with a girl from another class, both of them with their shirts off. Ikushi keeps covering her chest with her arms, and then uncovering it, and then covering it again."
    ikushi "Okay, I'm not— this isn't really me, I'm not usually like— okay, fine. Fine! Fine."
    subtitles "She drops her arms, grabs the other girl by the waist, and kisses her, and then she's the one pushing her back against the wall."
    ikushi "...Fine. Yes. This is me now. I've decided."

    # Gloria's notes break down.
    subtitles "Gloria's clipboard is on the floor. She's sitting on a stool in her skirt and her bra, with her blouse tied round her waist by the sleeves, and a girl is kissing her neck while she tries, with enormous concentration, to keep talking."
    gloria "Twenty-two... twenty-two-something. Subject reports— hah— subject reports significant— oh, that's nice, do that again— significant increase in— in— I've completely lost my train of thought. This is fascinating. I can't think. This is the most fascinating thing that's ever happened to me."

    # Elsie and Yuriko.
    # IMAGE: Elsie and Yuriko sitting on the floor against the wall, apart from
    # the crowd; Yuriko's head on Elsie's shoulder; Elsie's glasses crooked.
    subtitles "Away from the noise, Elsie and Yuriko are sitting on the floor with their backs against the wall. Yuriko has her head on Elsie's shoulder. Her twenty minutes were up two hours ago."
    yuriko "Everybody's being so stupid."
    elsie "Mm-hm."
    yuriko "It's all so stupid. It's disgusting."
    elsie "You haven't moved your head off my shoulder in an hour, though."
    yuriko "...Shut up."
    subtitles "Yuriko is quiet for a while. Then she lifts her head, looks at Elsie for a long moment, and very carefully takes Elsie's crooked glasses off and folds them and puts them on the floor."
    yuriko "Don't say anything. Don't say one single word."
    subtitles "She kisses her, once, very softly. Elsie makes a tiny sound. Yuriko pulls back, looks at her again, and then kisses her again, less carefully."
    yuriko.think "*This is so stupid. Why does it feel like the only thing that isn't?*"

    # The Clark twins, implied only.
    # IMAGE: Luna and Seraphina at the door to the little side room at the back,
    # hands linked, both flushed; Seraphina glancing back over her shoulder,
    # Luna already pulling her through. Nothing more is shown.
    subtitles "At the back of the room there's a door to the old prep room, with a cracked frosted window in it. Seraphina Clark, for once, isn't shouting anything. She's standing by that door, and her sister is holding her hand."
    luna "Sera. Come here a second."
    seraphina "What? What is it? You've got a face."
    luna "Just come here."
    subtitles "Luna pulls her through the door. Seraphina glances back over her shoulder once, pink to the ears, and then the door swings shut behind them both, and after a moment somebody on the other side turns the key."
    subtitles "Nobody notices. Nobody's looking at anything except whoever they're with."

    # Emiko in the dark corridor.
    # IMAGE: the dark corridor outside the chemistry room; Emiko standing just
    # out of the light, arms folded, watching through the door.
    subtitles "Out in the dark corridor, just beyond where the fairy lights reach, someone is standing with her arms folded."
    emiko.think "*Everyone. Every single one of them.*"
    emiko.think "*Look at them. Nobody's scared. Nobody's crying. Even Yuriko.*"
    emiko.think "*...He should be seeing this. He'd never believe me.*"

    ########################################
    # It ebbs

    # IMAGE: late; people sitting up, pulling clothes back on, lights still
    # glowing, the bowl empty on the bench.
    subtitles "Somewhere around eleven, it starts to ebb, the way a fever breaks."
    subtitles "People sit up. They look around, blinking, as if they've just woken up somewhere unexpected. There's a lot of confused laughing, and a lot of hunting around on the floor for blouses that might or might not be theirs."

    sakura "Where's my... is this my bra? This isn't my bra. Whose bra is this?"
    easkey "I- I think that's Aona's. I think she threw it."
    aona "I'm not even going to ask how I got up here. I'm just going to get down. Very slowly."
    lin "Okay. Okay, everybody. That was... um. That was the party. Thanks for coming. There's crisps left, if anyone wants some."
    lin.think "*What just happened? What happened? I remember the bowl, and handing out the cups, and after that it's all... gold. Just gold, and warm.*"

    miwa "I should... probably go back to the dorm."
    kokoro "Yeah. Me too."
    subtitles "They don't let go of each other's hand, though. They leave like that, both of them buttoned up wrong."

    subtitles "The prep room door at the back unlocks. The Clark twins come out one after the other, not looking at each other, their hair a mess, and walk out into the corridor without a word."

    gloria "I wrote everything down. I wrote down everything. I'm going to read it all in the morning."
    gloria.think "*...Where did my clipboard go?*"

    # The girls leave in twos and threes.
    subtitles "They drift out in twos and threes into the cold night, back across the dark sports field towards the dorms, shirts inside out, shoes in their hands, giggling at nothing. Halfway across the field, somebody asks what time they got there, and nobody's really sure."

    ########################################
    # Emiko alone in the empty room

    # IMAGE: the empty chemistry room. Fairy lights still on, clothes left in
    # corners, the empty bowl. Emiko collecting bottles into a bag; Lin's
    # schoolbag on a stool, the black notebook visible inside.
    subtitles "When the last of them has gone, the room is very quiet. The fairy lights are still on. There's a sock on top of the periodic table."
    subtitles "Emiko goes along the bench and puts the empty bottles into a bag, one at a time, so they don't clink. Then she stops at Lin's schoolbag, left behind on a stool."
    subtitles "The black notebook is right at the top. She takes it out, and holds it for a second, and slips it into her own bag."
    emiko.think "*Sorry, sweetheart. You did wonderfully. But this one's going home.*"
    emiko.think "*They'll look everywhere for it on Monday. They'll blame each other. They'll never think of me.*"
    subtitles "She switches the speaker off. The silence rushes in."
    emiko.think "*Now all I have to do is tell him.*"
    emiko.think "*...And explain where two hundred millilitres of his floor cleaner went.*"
    subtitles "She turns off the fairy lights, one string at a time, and closes the door behind her."

    $ set_progress("lab_intro_discovery", 6)
    $ set_progress("school_level", 3)

    $ end_event("new_daytime", **kwargs)


# Saturday Morning after the PTA Refreshments and Party
label lab_intro_22 (**kwargs):
    $ begin_event(**kwargs)

    $ lin = Person["lin_kato"]
    $ gloria = Person["gloria_goto"]
    $ ishimaru = Person["ishimaru_maki"]
    $ miwa = Person["miwa_igarashi"]
    $ kokoro = Person["kokoro_nakamura"]
    $ sakura = Person["sakura_mori"]
    $ easkey = Person["easkey_tanaka"]
    $ aona = Person["aona_komuro"]
    $ seraphina = Person["seraphina_clark"]
    $ luna = Person["luna_clark"]

    # SCENE · lab_intro_22
    # Saturday morning in the dorms, the morning after the party. Nobody
    # remembers much. Miwa wakes up in Kokoro's bed, both still dressed, with
    # no idea how she got there. In the shared bathroom Sakura finds she has
    # Aona's bra; Aona can't remember losing it; the Clark twins are briefly
    # awkward and then normal. In Lin's room the hosts discover the notebook
    # is gone, and Gloria's party notes turn into scribble partway through.
    # In the common room, in pyjamas, everyone's sitting a little closer than
    # usual. Lin heads back to the lab to look for the notebook.
    # No headmaster present → overheard, no paperdolls.

    ########################################
    # Kokoro's room

    # IMAGE: a dorm room, curtains half open, morning light. Kokoro and Miwa in
    # a single bed, both still in last night's clothes, Kokoro's arm over Miwa.
    subtitles "Saturday morning. The dorms are quieter than they've ever been at nine o'clock, and every curtain in the building is still shut."
    subtitles "Miwa Igarashi wakes up with somebody's arm over her, and it takes her a long, slow moment to work out that the somebody is Kokoro, and the bed is Kokoro's bed."

    miwa "...Kokoro?"
    kokoro "Mmh. Five more minutes."
    miwa "Kokoro. I'm in your bed."
    subtitles "Kokoro opens her eyes. Looks at Miwa. Looks at her own arm. Doesn't move it."
    kokoro "Oh. You are."
    kokoro "Um. How... did you get here?"
    miwa "I was going to ask you that. I remember the party. I remember dancing. I remember you, um..."
    subtitles "She tries to finish the sentence and can't. There's just a warm, golden blur where the rest of the night should be."
    miwa "...I remember you. That's sort of all I've got."
    kokoro "Me too. Just... you. And the lights."

    subtitles "They lie there looking at each other. Neither of them gets up."
    miwa "I should be dying of embarrassment right now. Shouldn't I? Normally I'd have run out of here screaming."
    miwa.think "*I'm not, though. I'm not embarrassed at all. Why am I not embarrassed?*"
    kokoro "Can we just... stay like this for a minute? Before we work out what happened?"
    miwa "Yeah. Yeah, okay. A minute."
    subtitles "It turns into a lot more than a minute."

    ########################################
    # The shared bathroom

    # IMAGE: the shared dorm bathroom; girls in pyjamas and oversized sleep
    # shirts at the sinks, brushing teeth, bleary. Sakura holding up a bra.
    subtitles "In the shared bathroom it's toothbrushes, running taps, and a lot of girls in pyjamas squinting at themselves in the mirrors as if they've never seen their own faces before."
    subtitles "Sakura Mori is standing at the sink holding up a lacy pink bra by one strap, and frowning at it."
    sakura "This isn't mine. Why have I got this? I don't even own anything this pink."
    aona "Oh my God, {i}that's{/i} where it went!"
    subtitles "Aona leans out of the shower cubicle, dripping, with her hair full of shampoo."
    aona "I looked for that for, like, half an hour last night. Where did you even find it?"
    sakura "I've no idea. It was in my bag. Why were you looking for your bra at a party?"
    aona "...I actually don't know. But I've got this feeling I was {i}amazing.{/i} Like, really, really amazing. Everyone was looking at me. I think."
    subtitles "Sakura hands it over. Next to her, Easkey Tanaka has gone bright red and is brushing her teeth so hard it looks painful."
    sakura "Easkey? You okay?"
    easkey "F-fine! Fine. I just— I don't know. My face just went hot. I don't know why."
    easkey.think "*Buttons. I keep thinking about buttons. Why do I keep thinking about buttons?*"

    # The twins pass in the doorway.
    subtitles "The Clark twins come in together, the way they always do. Seraphina, who usually has something to say about everything, says nothing at all. She goes to one sink and Luna goes to the one right at the other end, and for a few seconds neither of them looks at the other."
    subtitles "Then Seraphina leans back, catches her sister's eye in the long mirror, and pulls a face. Luna snorts toothpaste. And it's normal again, or near enough."

    ########################################
    # Lin's room: the notebook is gone

    # IMAGE: Lin's dorm room. Lin on her knees, her schoolbag tipped out on the
    # floor; Ishimaru on the bed; Gloria in the doorway holding her clipboard.
    subtitles "In Lin's room, Lin's schoolbag is upside down on the floor, and Lin is on her knees going through everything that fell out of it for the third time."
    lin "It's not here. It's not here. It was in my bag, I {i}know{/i} it was in my bag, I put it right at the top so I wouldn't squash it—"
    ishimaru "Maybe you left it in the lab? You could have taken it out, to show people?"
    lin "I wouldn't show {i}people!{/i} We said we wouldn't tell anybody, I'm the one who made us say it out loud!"
    lin "...Did you take it? To look after it? You'd tell me if you'd taken it."
    ishimaru "I didn't take it! I swear! Maybe Gloria took it, she's always got it, she's always reading it—"
    gloria "I didn't take it."
    subtitles "Gloria is standing in the doorway in her pyjamas, holding her clipboard against her chest with both arms. She looks paler than usual."
    gloria "But you need to see this."

    # IMAGE: close on Gloria's clipboard. Neat entries with times at the top;
    # then the handwriting slanting, getting bigger; then scribble, and the
    # word "fizzy" underlined three times.
    subtitles "She holds it out. At the top of the page, her handwriting is tiny and precise: names, times, cups. Halfway down, it starts to slope. Then it gets bigger. Then it stops being words at all."
    subtitles "The last thing she wrote that anyone can read is {i}fizzy{/i}, underlined three times."
    gloria "I wrote this. That's my handwriting. And I don't remember writing any of it after about half past nine."
    gloria "I've never not remembered writing something. Not once, not in my whole life."
    ishimaru "Okay, that's actually scary. That's actually properly scary."

    lin "So. We've lost the notebook. And none of us can really remember the party."
    gloria "We remember the beginning. And the end. The middle's just..."
    lin "Gold."
    subtitles "Gloria looks at her."
    gloria "...Yes. Why did you say gold?"
    lin "I don't know. It just came out. It's what it looks like when I try to remember."
    subtitles "For a second none of them says anything."

    ishimaru "But it was a good party, though. Right? Everyone said it was a good party. Everyone kept saying it on the way back."
    lin "Everyone said it was the best night of their entire lives, and not one person can tell me a single thing that happened."
    lin "...Which is, honestly, kind of the most successful party anyone's ever thrown."
    gloria "That's not funny."
    lin "It's a bit funny."
    gloria "It's a bit funny."

    ########################################
    # The common room

    # IMAGE: the dorm common room, mid-morning. Girls in pyjamas on the sofas
    # with mugs and toast, sitting noticeably closer than usual. Miwa and
    # Kokoro on the end of a sofa, Kokoro leaning against Miwa's shoulder.
    subtitles "By eleven, half the dorm has ended up in the common room in their pyjamas, with toast and tea and blankets. Nobody's said anything about it, but everybody's sitting closer than they normally would. Knees touching. Somebody's feet in somebody else's lap."
    subtitles "Miwa and Kokoro come in last, together, and sit on the end of the sofa, and after a moment Kokoro leans her head on Miwa's shoulder in front of everyone."
    ishimaru "Wait. Are you two... a thing now?"
    miwa "I don't know! Maybe? I don't know if we're..."
    miwa "Is that allowed?"
    lin "Is what allowed?"
    subtitles "Miwa opens her mouth to answer, and finds she can't."
    miwa "...I don't actually know. It just felt like I should ask."

    subtitles "Nobody laughs at her. A couple of the girls on the other sofa glance at each other and then look away, as if they'd been wondering the same thing."

    # Lin gets up.
    lin "Right. I'm going back to the lab. That notebook has to be somewhere, and I'm not having it turn up in some teacher's hands on Monday morning."
    ishimaru "Now? It's Saturday! I'm in my pyjamas!"
    lin "Then put some trousers on. Gloria, bring the clipboard."
    gloria "Why?"
    lin "Because if we find out what happened last night, you're going to want to write it down."

    $ end_event("new_daytime", **kwargs)


# Saturday Evening after the PTA Refreshments and Party
label lab_intro_23 (**kwargs):
    $ begin_event(**kwargs)

    $ lin = Person["lin_kato"]
    $ gloria = Person["gloria_goto"]
    $ ishimaru = Person["ishimaru_maki"]
    $ soyoon = Person["soyoon_yamamoto"]
    $ hatano = Person["hatano_miwa"]
    $ ikushi = Person["ikushi_ito"]
    $ seraphina = Person["seraphina_clark"]
    $ elsie = Person["elsie_johnson"]
    $ aona = Person["aona_komuro"]
    $ sakura = Person["sakura_mori"]
    $ easkey = Person["easkey_tanaka"]

    # SCENE · lab_intro_23
    # Saturday evening in the dorm common room. A dozen girls in pyjamas and
    # sleep shirts on the sofas and floor cushions, pizza boxes open on the
    # coffee table, music low on a phone. Lin reports that the search of the
    # lab found nothing. Yuriko has shut herself in her room. The girls play a
    # game of piecing Friday together from fragments, and nobody can say who
    # kissed whom. Crushes get admitted out loud for the first time; there are
    # one or two nervous kisses and a hand under a shirt. Late on, Gloria tells
    # Lin, alone, that she thinks the potion was real. Lin doesn't want to
    # believe it. No headmaster present → overheard, no paperdolls.

    # IMAGE: the dorm common room in the evening. Pizza boxes, mugs, blankets,
    # a phone playing music. Girls in pyjamas, sitting close.
    subtitles "Saturday night. Somebody has ordered far too much pizza, and now the common room smells of pepperoni, garlic bread, and about six different vanilla body sprays."
    subtitles "There are a dozen of them in there, in pyjamas and big sleep shirts and fluffy socks, and the sofas only fit eight, so the rest are on the floor in a heap of cushions and blankets and each other."

    # Lin reports back.
    aona "So? Did you find your mysterious lost thing?"
    lin "No. We searched the whole lab. Every cupboard. Gloria crawled under the benches."
    gloria "I crawled under the benches."
    lin "All we found was the empty punch bowl and a sock on top of the periodic table."
    ishimaru "Whose sock {i}was{/i} that? Nobody's claimed it. It's just been sitting on top of hydrogen all day."
    lin "I put it in lost property. Let it be somebody else's problem."

    # Elsie, worried about Yuriko.
    subtitles "Elsie Johnson is sitting a little apart, on the arm of a sofa, with a slice of pizza she hasn't touched."
    ishimaru "Elsie, where's Yuriko? I thought she'd be with you."
    elsie "She's locked herself in her room. She won't come out."
    elsie "I knocked. Twice. She said she doesn't want to see anybody. Not even me."
    subtitles "She says the last part very quietly, and looks down at the pizza."
    elsie.think "*She was fine last night. Wasn't she? She had her head on my shoulder. I remember that much. I'm almost sure I remember that much.*"

    ########################################
    # The game: piecing Friday together

    lin "Okay. New game. Since apparently none of us can remember anything, we're going to put Friday back together. Everyone says one thing they definitely remember. One thing. Go."
    aona "Me first. I was on a bench. I don't know why. I just know I was up high and everybody was cheering."
    seraphina "You were dancing. Badly."
    aona "I was dancing {i}iconically.{/i}"

    hatano "Somebody played the guitar for, like, an hour. The same four chords."
    subtitles "Every head turns to Ishimaru, who goes slowly pink."
    ishimaru "It was five chords. And I said sorry. I'm pretty sure I said sorry."

    ikushi "There was a sock. On the periodic table."
    lin "We've done the sock, Ikushi."
    ikushi "Well, it's what I remember! It was a very memorable sock!"

    gloria "Kokoro said 'fizzy.' I wrote it down."
    subtitles "She doesn't say anything about how the rest of the page looks."

    # Who kissed who: nobody knows.
    seraphina "Okay, but the real question. Who kissed who? Because I know for a {i}fact{/i} people were kissing."
    lin "How do you know for a fact?"
    seraphina "Because my mouth feels like it's been kissing. Doesn't everyone's?"
    subtitles "There's a long pause, and then a lot of people touch their own lips at the same time without meaning to, and then everyone shrieks with laughter."

    hatano "Well, I know who {i}I{/i} kissed."
    soyoon "You don't know anything."
    hatano "Oh, I absolutely do."
    soyoon "I didn't kiss anyone. My hair was a disaster this morning because of the humidity in that building. That's all. The building is very humid."
    hatano "Mm-hm. The humidity was very... hands-on."
    subtitles "Soyoon throws a cushion at her. It's the least dignified thing anybody has ever seen her do, and she looks quite pleased with herself afterwards."
    soyoon.think "*I'm not going to remember it. I've decided. I'm not going to remember any of it. ...I wish I could remember all of it.*"

    ikushi "Fine. Fine! I kissed someone. I think. I can't remember who, but I'm owning it. I've decided I'm owning it."
    aona "Ikushi! Who knew!"
    ikushi "Nobody knew. Including me. Until about half an hour ago."

    subtitles "Seraphina, who has been loudest about everything all night, has gone very interested in a crust."
    lin "Sera? What about you? You've been very quiet for someone who started this."
    seraphina "Me? Oh, I kissed {i}loads{/i} of people. Everyone. All of you. I'm a legend."
    subtitles "She grins, and steals a slice off Aona's plate, and the conversation moves on. If anyone notices she didn't actually answer, nobody says so."

    ########################################
    # Crushes, out loud for the first time

    # IMAGE: later; the lights lower, fewer voices; girls lying on cushions
    # with their heads in each other's laps, talking quietly.
    subtitles "Later, somebody turns the big light off and leaves just the lamps on, and the conversation goes softer."
    aona "Okay. Truth. Has anybody here ever, like... properly fancied someone? In this school?"
    subtitles "It's quiet for a second. Normally that would be the moment someone makes a joke and changes the subject."
    hatano "...Yes."
    ikushi "Yeah. Me too."
    aona "Who?"
    hatano "I'm not saying who! I'm saying yes. That's already a lot. I've never said yes before."
    ikushi "I've never even said yes to myself before."

    subtitles "Nobody laughs. A girl on the floor with her head in somebody's lap says, very quietly, \"Same,\" and the girl whose lap it is looks down at her and doesn't say anything at all."

    # A nervous kiss; a hand under a shirt.
    # IMAGE: Sakura and Easkey on a beanbag in the corner, Easkey's hand
    # resting on Sakura's stomach, just under the hem of her sleep shirt.
    subtitles "In the corner, Sakura and Easkey have been leaning against each other on a beanbag all evening, and they've gone quiet. Easkey's hand is resting on Sakura's stomach, just under the hem of her sleep shirt, as though it ended up there by accident."
    easkey "I- is this okay? I don't know if it's okay."
    sakura "I... yeah. I think so. I think it's okay."
    subtitles "A nervous little laugh."
    sakura "Is it allowed, though?"
    easkey "I d-don't know. Nobody's said it isn't."
    subtitles "Her hand stays where it is."
    easkey.think "*Buttons. It was buttons. I undid her buttons. ...Didn't I?*"

    aona "Oi. Corner. I can see you."
    subtitles "Both of them squeak. The hand vanishes. And then, after a second, it comes back, and Aona just laughs and leaves them to it."

    hatano "Soyoon."
    soyoon "What."
    hatano "Come here a second."
    soyoon "Absolutely not. I'm eating."
    subtitles "She puts the pizza down anyway. Hatano leans over and kisses her, quick and nervous, in front of everyone. Soyoon goes rigid for a second and then, very deliberately, kisses her back."
    soyoon "...That's because of the humidity."
    hatano "Obviously."

    ########################################
    # Gloria and Lin, alone

    # IMAGE: the corridor outside the common room, late. Lin and Gloria by a
    # window, the noise of the common room muffled behind the door.
    subtitles "Near midnight, Gloria catches Lin's sleeve on her way back from the kitchen and pulls her out into the corridor, where it's dark and quiet."
    gloria "I need to tell you something, and I need you to not make a joke about it."
    lin "That's the scariest sentence you've ever said to me."
    gloria "It worked."
    lin "...What worked?"
    gloria "The potion. It worked. It actually did what it said in the notebook. Everybody at that party drank it, and then everybody lost the same three hours, and everybody remembers the same things: heat, and gold, and wanting to touch someone."
    gloria "That's not a coincidence, Lin. That's a {i}result.{/i}"

    lin "It was a {i}joke{/i}, Gloria. It was lemonade in a bowl with a silly name. We made it up. We called it Love Potion Number Nine, for God's sake."
    gloria "We made it from a formula somebody else wrote. And somebody else lost. Or took back."
    subtitles "Lin opens her mouth, and doesn't say anything."
    gloria "And look at them in there. Ikushi just said she fancies someone. Out loud. Soyoon just kissed Hatano. In front of everyone. On a {i}Saturday.{/i} Sober."
    lin "People are allowed to just... be happy, you know. Things don't always have to have a reason."
    gloria "Everything has a reason. That's what reasons are."

    lin.think "*She's right. I know she's right. I don't want her to be right.*"
    lin "...Don't tell anyone. Not the others. Not anyone."
    gloria "Who would I tell? Who would even believe me?"

    subtitles "Behind the door, somebody laughs, and somebody else says {i}shh{/i}, and the music goes up a notch."
    lin "Come on. Let's go back in. Before they wonder where we went."
    subtitles "She goes in first. Gloria stays in the dark corridor a moment longer, looking at the closed door, and then follows her."

    $ end_event("new_daytime", **kwargs)


# Sunday Mini events after the PTA Refreshments and Party
# Optional, like the level-2 sex-ed mini events: short headmaster-POV snapshots
# of the new (level 3) normal for the player to stumble on around campus. He
# knows nothing about the party; he only dosed the teachers and the mothers.

# Gym: Sunday training, shirts off, spotting
label lab_intro_24a (**kwargs):
    $ begin_event(**kwargs)

    $ aona = Person["aona_komuro"]
    $ ikushi = Person["ikushi_ito"]

    # SCENE · lab_intro_24a
    # Sunday late morning, the gym. A handful of students training on their
    # own. T-shirts knotted up or tossed on the bench, sports bras and shorts.
    # Aona on the bench press with Ikushi spotting her, hands lingering.
    # The headmaster watches from the doorway.
    $ paperdoll_manager.set_background("images/background/gym/3 1 0.webp", blur = True)

    subtitles "The gym on a Sunday morning smells of rubber mats, floor polish, and somebody's strawberry deodorant. The radio in the corner is playing to nobody."
    subtitles "There are five or six girls in here, training on their own time. Most of their T-shirts are knotted up under their ribs or lying in a heap on the bench."

    # IMAGE: Aona on the bench press, Ikushi standing over her to spot, both in
    # sports bras; Ikushi's hands hovering at Aona's waist.
    aona "Two more. Two more! Watch, Ikushi, watch me, are you watching?"
    ikushi "I'm watching. I'm literally standing right over you. Where else would I be looking?"
    subtitles "Aona racks the bar and sits up, flushed and grinning. Ikushi's hands are still resting on her waist. Neither of them seems to have noticed."

    headmaster.think "...On a Sunday. In sports bras. And nobody's rushing for a towel the second the door opens."
    headmaster.think "Last month they'd have been in baggy T-shirts down to their knees."

    $ end_event("new_daytime", **kwargs)

# School building: a Sunday study group in an empty classroom
label lab_intro_24b (**kwargs):
    $ begin_event(**kwargs)

    $ sakura = Person["sakura_mori"]
    $ easkey = Person["easkey_tanaka"]

    # SCENE · lab_intro_24b
    # Sunday afternoon, an empty classroom in the school building. Sakura is
    # tutoring Easkey, the two of them sharing one chair's worth of space at a
    # desk, Easkey leaning on Sakura's shoulder. Neither moves apart when the
    # headmaster looks in.
    $ paperdoll_manager.set_background("images/background/school building/3 1 1.webp", blur = True)

    subtitles "One classroom door on the first floor is open, which on a Sunday is unusual enough that he stops to look in."

    # IMAGE: Sakura and Easkey at one desk, chairs pushed right together,
    # Easkey's head on Sakura's shoulder, a maths book open in front of them.
    sakura "No, look, you've got it, you just did it backwards. Thirty-two. See?"
    easkey "Th-thirty-two. Oh. Oh, I hate that I get it now."
    subtitles "Easkey has her head on Sakura's shoulder while she writes. Their chairs are pushed so close together that they're really sharing one."

    headmaster "Working on a Sunday, Ms. Mori? Ms. Tanaka?"
    sakura "Oh! Hello, Mr. [headmaster_last_name]. Easkey's got a test on Tuesday."
    easkey "And I'm h-hopeless. She's saving my life."
    subtitles "Neither of them moves apart. Easkey doesn't even lift her head. She just smiles at him from Sakura's shoulder."

    headmaster.think "That's Easkey Tanaka. She can't usually look me in the eye for three seconds together."

    $ end_event("new_daytime", **kwargs)

# Courtyard: closeness on the grass, and Yuriko on her own
label lab_intro_24c (**kwargs):
    $ begin_event(**kwargs)

    $ lin = Person["lin_kato"]
    $ ishimaru = Person["ishimaru_maki"]
    $ yuriko = Person["yuriko_oshima"]

    # SCENE · lab_intro_24c
    # Sunday afternoon, the courtyard. Students lying around on the grass in
    # little heaps, heads in laps, legs over legs; Ishimaru playing guitar,
    # Lin lying with her head on Ishimaru's knee. On a bench on her own, with
    # headphones in, Yuriko glaring at all of it. Brief exchange with her.
    $ paperdoll_manager.set_background("images/background/courtyard/3 1 1.webp", blur = True)

    subtitles "The courtyard's full for a Sunday. Nobody's on the benches, though. Everyone's on the grass, in heaps: heads in laps, legs thrown over other legs, somebody braiding somebody else's hair while a third girl braids hers."
    subtitles "Ishimaru Maki is playing her guitar in the middle of it, slightly out of tune, with Lin Kato lying on her back with her head on Ishimaru's knee."

    headmaster.think "They look like a litter of puppies."
    headmaster.think "...And they don't stop when they see me. Two of them wave."

    # IMAGE: Yuriko alone on a bench at the edge of the courtyard, headphones
    # in, arms folded, scowling at the heaps on the grass.
    subtitles "There's exactly one girl on a bench. Yuriko Oshima, on her own at the far edge of the courtyard, headphones in, arms folded, glaring at the whole scene as if it's personally offended her."
    headmaster "Ms. Oshima. Not joining in?"
    subtitles "She pulls one earbud out, slowly."
    yuriko "Has everyone in this school gone soft in the head this weekend, or is it just me?"
    headmaster "...What do you mean?"
    subtitles "She looks at him for a moment, as though she's deciding whether he's worth the trouble. Then she puts the earbud back in."
    yuriko "Nothing. Forget it."
    yuriko.think "*Something happened on Friday. I know it did. I just can't remember what.*"

    headmaster.think "Soft in the head. This weekend."
    headmaster.think "I dosed five teachers and three mothers. I didn't go anywhere near the students."

    $ end_event("new_daytime", **kwargs)

# Dormitory: evening, pyjamas in the corridor, no hurry
label lab_intro_24d (**kwargs):
    $ begin_event(**kwargs)

    $ soyoon = Person["soyoon_yamamoto"]
    $ hatano = Person["hatano_miwa"]

    # SCENE · lab_intro_24d
    # Sunday evening, the dorm corridor during the headmaster's walk-round.
    # Doors open, music from a couple of rooms. Soyoon in short silky pyjamas
    # coming back from the bathroom with a towel over her shoulder, Hatano
    # leaning in her doorway. Nobody hurries to get out of sight.
    $ paperdoll_manager.set_background("images/background/school dormitory/3 1 0.webp", blur = True)

    subtitles "Sunday evening, on his usual walk through the dorms. Half the doors on the corridor are standing open, and there's music coming out of at least three rooms at once."
    subtitles "It smells of shampoo and toast and nail varnish."

    # IMAGE: Soyoon walking down the corridor in short silky pyjamas, towel
    # over her shoulder; Hatano leaning in a doorway in an oversized T-shirt.
    subtitles "Soyoon Yamamoto comes down the corridor from the bathroom in a pair of very short, very silky pyjamas, with her hair wrapped in a towel. She sees him. She doesn't speed up, and she doesn't turn back."
    soyoon "Evening, Mr. [headmaster_last_name]."
    headmaster "Ms. Yamamoto."
    subtitles "She walks past him at exactly the same pace and stops at Hatano's door, where Hatano is leaning against the frame in a T-shirt that comes to about halfway down her thighs."
    hatano "Nice pyjamas."
    soyoon "I know."

    headmaster.think "Soyoon Yamamoto. Who has, as far as I know, never once let anyone see her without her hair done."
    headmaster.think "...They're not doing it {i}at{/i} me. That's the strange part. They just don't seem to mind that I'm here."

    $ end_event("new_daytime", **kwargs)

# Cafeteria: Sunday dinner, and a word overheard
label lab_intro_24e (**kwargs):
    $ begin_event(**kwargs)

    $ adelaide = Person["adelaide_hall"]
    $ miwa = Person["miwa_igarashi"]
    $ kokoro = Person["kokoro_nakamura"]

    # SCENE · lab_intro_24e
    # Sunday dinner in the cafeteria. Adelaide Hall serving, humming, piling
    # extra portions. Miwa and Kokoro at a table sharing one plate, Miwa
    # feeding Kokoro a forkful. At the next table, girls whispering about
    # "Friday" and "the party". The headmaster overhears the word.
    $ paperdoll_manager.set_background("images/background/cafeteria/3 1 0.webp", blur = True)

    subtitles "Sunday dinner. The cafeteria smells of roast potatoes and gravy, and Adelaide Hall is behind the counter humming something, loading plates with far more than the usual portion."
    adelaide "There you are, headmaster. Extra potatoes. Don't argue. I'm in {i}such{/i} a good mood this weekend, I can't explain it."
    headmaster.think "...I can."

    # IMAGE: Miwa and Kokoro at a table, one plate between them, Miwa holding a
    # forkful up to Kokoro's mouth; both laughing.
    subtitles "At a table by the window, Miwa Igarashi and Kokoro Nakamura are sharing one plate. Miwa is holding a forkful of potato up to Kokoro's mouth, and Kokoro is laughing too hard to eat it."
    kokoro "Stop, stop, I can feed myself—"
    miwa "You could. But you're not going to."

    # IMAGE: the next table; three girls leaning in, whispering.
    subtitles "At the next table, three girls have their heads together, talking low and giggling."
    sgirl "...not since Friday. Not since the party."
    sgirl "Shh!"
    subtitles "They catch him looking and burst out laughing, and go back to their dinner."

    headmaster.think "The party."
    headmaster.think "...What party?"

    $ end_event("new_daytime", **kwargs)


# First Monday after the PTA Refreshments and Party
label lab_intro_25 (**kwargs):
    $ begin_event(**kwargs)

    $ finola = Person["finola_ryan"]
    $ lily = Person["lily_anderson"]
    $ yuriko = Person["yuriko_oshima"]

    # SCENE · lab_intro_25
    # Monday morning. The headmaster walks through the school building before
    # first period and notices small changes everywhere: an extra button
    # undone, girls walking closer, nobody being corrected. Finola is wearing
    # the cropped yellow tank from Thursday again, by choice. Yuriko scowls at
    # him. In his office Emiko confesses: the girls found his notebook in the
    # old lab, she helped them brew, and on Friday she gave them most of his
    # remaining catalyst for a party the whole school went to. He fetches the
    # jug from the storage room next door and finds it nearly empty. Anger;
    # then she gives him back his notebook; "Subject E."; then grudging
    # admiration. Wired: blurred school-building bg (3 1 1) for the walk,
    # blurred office bg (f.webp) + Emiko paperdoll for the talk.

    ########################################
    # Monday morning walk

    $ paperdoll_manager.set_background("images/background/school building/3 1 1.webp", blur = True)

    subtitles "Monday. Twenty past eight, and the corridors of the school building are full of the usual noise: lockers banging, somebody shouting about a lost PE kit, the smell of floor polish and toast."
    headmaster.think "Let's see. Whatever's left over from the weekend, it'll show up today."

    # IMAGE: the corridor; students heading to class. Small details: a blouse
    # with one more button open than usual, two girls walking with their arms
    # linked, a skirt hitched a little higher.
    subtitles "At first it looks like any Monday. Then he starts noticing things."
    subtitles "A blouse with one button more undone than it was last week. Two girls walking to class with their arms linked, which nobody seems to think is worth a second glance. A tie loosened all the way down, and nobody telling its owner to fix it."
    headmaster.think "None of it's anything, on its own. Any one of these, I'd walk straight past."
    headmaster.think "...It's all of them at once, though. Everyone, just a little."

    # IMAGE: Lily Anderson at her classroom door, letting a girl with a loose tie
    # walk straight past her.
    subtitles "At the door of her classroom, Lily Anderson watches a girl go in with her tie hanging halfway down her blouse, opens her mouth as if to say something, and then just smiles and holds the door for the next one."
    lily "Morning, everybody. In you come. Find a seat."
    headmaster.think "Lily Anderson. Who sent three girls to the toilets to fix their ties last Monday."

    # IMAGE: Finola Ryan coming down the corridor in the cropped yellow tank
    # from Thursday, ripped jeans, boots, a stack of marking under her arm.
    subtitles "Finola Ryan comes round the corner with a pile of marking under one arm, and he nearly walks into the wall."
    subtitles "It's the yellow tank top from Thursday. The cropped one. The ripped jeans. The boots. She's wearing them on purpose, to work, on a Monday, and she gives him a little nod on her way past, perfectly normal."
    finola "Morning, Mr. [headmaster_last_name]."
    headmaster "Ms. Ryan."
    finola.think "*It's just more comfortable. That's all it is. It's just more comfortable now.*"
    headmaster.think "She kept it. She went home, and slept on it, and came back and put it on again."
    headmaster.think "...It stayed. Some of it actually stayed."

    # IMAGE: Yuriko Oshima passing in the other direction, alone, scowling.
    subtitles "Yuriko Oshima goes past in the other direction, on her own, and gives him a look so sour he can feel it on the back of his neck."
    headmaster.think "The teachers I understand. And the mothers. But the students..."
    headmaster.think "'Since the party.' What party?"

    ########################################
    # The office

    $ emiko.register_paperdoll()
    $ paperdoll_manager.set_background("images/background/office building/f.webp", blur = True)

    subtitles "Back in his office, there's a cup of coffee already waiting on his desk. Emiko must have put it there. She only does that when she wants something, or when she's done something."

    # IMAGE / paperdoll: Emiko in the doorway with a folder, unusually hesitant.
    $ emiko.display(PDAImage(pose = "10", outfit = "uniform", level = 6, mood = "neutral", mouth = "closed", look = "avert"),
        PDAPreset("close_body_center", duration = 0.0),
        PDAPreset("outside", duration = 0.0))
    $ emiko.display(PDAPreset("close_body_center", duration = 0.6))
    subtitles "She knocks, which she never does, and comes in, and doesn't sit down."
    $ emiko.display(PDAImage(mouth = "open"))
    emiko "Good morning."
    $ emiko.display(PDAImage(mouth = "closed"))
    headmaster "Morning. Close the door."
    subtitles "She closes it. She stays standing with her back to it."
    $ emiko.display(PDAImage(look = "follow", mouth = "open"))
    emiko "You've seen them."
    $ emiko.display(PDAImage(mouth = "closed"))
    headmaster "I've seen them. All weekend, actually. The gym, the courtyard, the dorms. Finola Ryan's walking round in a crop top right now."
    headmaster "The teachers, fine. I dosed the teachers. The mothers, fine. But I didn't go anywhere near the students, Emiko, and every one of them's... different. And somebody in the cafeteria last night said something about a party."
    $ emiko.display(PDAImage(pose = "7", mood = "neutral", mouth = "open"))
    emiko "Yes. There was a party."
    emiko "I helped."

    # Her confession, in her own words.
    $ emiko.display(PDAImage(mouth = "closed"))
    headmaster "...Helped with what?"
    $ emiko.display(PDAImage(pose = "2", mouth = "open"))
    emiko "A couple of weeks ago, three girls from 3A found a notebook in the old lab building. Lin Kato, Gloria Goto and Ishimaru Maki. Behind a shelf."
    headmaster "A notebook."
    emiko "Your notebook."
    $ emiko.display(PDAImage(mouth = "closed"))
    headmaster "My— I've been tearing this office apart for weeks looking for that notebook!"
    $ emiko.display(PDAImage(mood = "happy", mouth = "open", look = "avert"))
    emiko "I know. I watched you. It was quite sweet."
    $ emiko.display(PDAImage(mood = "neutral", mouth = "open", look = "follow"))
    emiko "They thought it was some old teacher's research. I told them it was a love potion. They wanted to brew it, and they were going to try with or without me, so I made sure it was with me. Goggles. Gloves. All of it."
    emiko "They brewed four batches. On Friday night they threw a party in the old lab and invited the whole school. Everyone drank it. Everyone."
    $ emiko.display(PDAImage(mouth = "closed"))

    headmaster "The base formula. Without— that only lasts a few minutes. That wouldn't do {i}this.{/i}"
    subtitles "Emiko doesn't say anything. She doesn't look away, either."
    headmaster "...Emiko. What did you give them?"
    $ emiko.display(PDAImage(pose = "10", mood = "sad", mouth = "open"))
    emiko "A stabiliser."
    emiko "From your jug."

    # He goes next door to the storage room; we stay with Emiko in the office.
    $ emiko.display(PDAImage(mouth = "closed"))
    subtitles "He's out of the door before she can say anything else."
    subtitles "Through the wall she hears the storage room door bang open, something scrape on the top shelf, a paint tin hit the floor and roll."
    subtitles "Then nothing at all for quite a long time."

    # He comes back with the jug. It's nearly empty.
    subtitles "When he comes back he's holding the jug. He doesn't need to tilt it against the light. You can hear how empty it is when it moves."
    headmaster "Two hundred millilitres."
    headmaster "Do you know what you've done? That was {i}everything.{/i} That was all there is. In the whole world. I spent a week measuring that out to the {i}line{/i}, I stood in the staff room at six in the morning counting, and you just poured it into a punch bowl—"
    $ emiko.display(PDAImage(mood = "neutral", mouth = "open"))
    emiko "Not a punch bowl. Eleven bottles. Very evenly. Gloria measured it."
    headmaster "That is {i}not the point!{/i}"
    $ emiko.display(PDAImage(mouth = "closed"))
    subtitles "He puts the jug down on the desk, much too hard. The little bit left in the bottom sloshes."

    $ emiko.display(PDAImage(pose = "21", mood = "neutral", mouth = "open"))
    emiko "I'm sorry I did it behind your back. I am. I'm not going to pretend I'm not."
    emiko "But I'm not sorry I did it."
    $ emiko.display(PDAImage(mouth = "closed"))
    headmaster "You don't get to just—"
    $ emiko.display(PDAImage(mouth = "open"))
    emiko "You were carrying all of it on your own. Every single drop, every teacher, every mother, every sum at three in the morning on a mop bucket. You didn't have to."
    emiko "And if it had gone wrong, it was my name on it. Not yours. That was the whole point of not telling you."
    $ emiko.display(PDAImage(mouth = "closed"))
    headmaster.think "...God. She's been planning this since before I even found the catalyst."
    headmaster.think "And she's not wrong. That's the worst part. She's not wrong."

    # She gives him back his notebook.
    $ emiko.display(PDAImage(pose = "17", mood = "neutral", mouth = "closed", look = "avert"))
    subtitles "She opens the folder she's been holding and takes something out of it, and puts it down on the desk next to the jug."
    subtitles "A plain black notebook. The elastic band still round it."
    $ emiko.display(PDAImage(mouth = "open"))
    emiko "I took it back on Friday night, after everyone had gone. They'll never brew it again. They've spent all weekend blaming each other for losing it."
    $ emiko.display(PDAImage(mouth = "closed"))
    subtitles "He picks it up. It's his handwriting, all of it. The crossed-out numbers. 'Muddy brown, don't panic.' The question mark on page six."
    $ emiko.display(PDAImage(mood = "shining", mouth = "open", look = "follow"))
    emiko "You wrote me down, you know."
    emiko "'Subject E.'"
    $ emiko.display(PDAImage(mouth = "closed"))
    subtitles "He looks up. For a moment neither of them says anything at all."
    headmaster "...I didn't know what else to call you. In the notes."
    $ emiko.display(PDAImage(mood = "happy", mouth = "open"))
    emiko "I liked it. I'd just never seen it written down before."

    # Grudging admiration.
    $ emiko.display(PDAImage(mood = "neutral", mouth = "closed"))
    headmaster "The whole school. In one night."
    headmaster "I was going to do the teachers, then the mothers, and then sit and wait for months for it to trickle down, one careful dose at a time..."
    $ emiko.display(PDAImage(pose = "36", mood = "happy", mouth = "open"))
    emiko "And now you don't have to wait. Most of them barely remember Friday. But every one of them woke up on Saturday a little bit different."
    $ emiko.display(PDAImage(mouth = "closed"))
    headmaster.think "She went behind my back. She stole from me. She dosed every student in this building with my last catalyst."
    headmaster.think "...And it worked better than anything I'd planned."
    headmaster "I'm still furious with you."
    $ emiko.display(PDAImage(mood = "shining", mouth = "open"))
    emiko "I know. I'd be disappointed if you weren't."

    # The remaining catalyst; looking ahead.
    $ emiko.display(PDAImage(pose = "6", mood = "neutral", mouth = "closed"))
    subtitles "He tilts the jug. What's left barely covers the bottom."
    headmaster "Seventy millilitres. Seven doses, if I'm careful. That's all there is now."
    $ emiko.display(PDAImage(mouth = "open"))
    emiko "Then we'll need something else, eventually. Something you can actually make more of."
    emiko "And a proper lab to make it in. I've started a budget proposal for the old lab building. It'll be on your desk by Friday."
    $ emiko.display(PDAImage(mouth = "closed"))
    headmaster "...You've started a budget proposal."
    $ emiko.display(PDAImage(mood = "happy", mouth = "open"))
    emiko "I started it last Wednesday. I had a feeling I'd need to make it up to you."

    $ emiko.display(PDAImage(pose = "39", mood = "shining", mouth = "open"))
    emiko "Drink your coffee. It's getting cold."
    $ emiko.display(PDAMove(alignX = 1.5, duration = 1.0),
        PDAPause(duration = 1.0))
    $ emiko.clear_display()

    # Alone: the notebook, a fresh page.
    subtitles "The door closes behind her."
    subtitles "He sits there for a while with the jug on one side of him and the notebook on the other. Then he takes the elastic off, turns past all the old pages to the first clean one, and uncaps a pen."
    headmaster.think "Monday. Subject: the whole school."
    headmaster.think "...God help me. Where do I even start?"
    subtitles "He starts writing."

    $ set_progress("lab_intro", 14)

    $ end_event("new_daytime", **kwargs)

