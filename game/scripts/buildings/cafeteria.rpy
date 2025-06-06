########################################
# region Cafeteria Event Handler ----- #
########################################

init -1 python:
    set_current_mod('base')
    
    cafeteria_timed_event = TempEventStorage("cafeteria_timed", "cafeteria", fallback = Event(2, "cafeteria.after_time_check"))
    cafeteria_general_event = EventStorage("cafeteria_general", "cafeteria", fallback = Event(2, "cafeteria.after_general_check"))
    register_highlighting(cafeteria_timed_event, cafeteria_general_event)

    cafeteria_events = {}
    add_storage(cafeteria_events, EventStorage("look_around",  "cafeteria", fallback_text = "Nothing to see here."))
    add_storage(cafeteria_events, EventStorage("order_food",  "cafeteria", fallback_text = "I'm not hungry."))
    add_storage(cafeteria_events, EventStorage("eat_alone",   "cafeteria", fallback_text = "I'm not hungry."))

    cafeteria_bg_images = BGStorage("images/background/cafeteria/c.webp", 
        BGImage("images/background/cafeteria/<school_level> <variant> <nude>.webp", 1, 
            OR(TimeCondition(daytime = '3,6', weekday = 'd'), TimeCondition(daytime = 'd', weekday = 'w'))),
        BGImage("images/background/cafeteria/<parent_level> <nude>.webp", 1, 
            OR(TimeCondition(daytime = 'c', weekday = 'd'), TimeCondition(daytime = 'd', weekday = 'w'))),
        BGImage("images/background/cafeteria/n.webp", 1, 
            TimeCondition(daytime = 7)))

        
init 1 python:
    set_current_mod('base')
    cafeteria_construction_event = Event(1, "cafeteria_construction",
        ProgressCondition("unlock_cafeteria", "2"),
        Pattern("main", "images/events/cafeteria/cafeteria_construction/cafeteria_construction <step>.webp"))

    cafeteria_event_1_event = Event(3, "cafeteria_event_1",
        TimeCondition(daytime = "d"),
        RandomListSelector("topic", "coffee", "tea", "warm milk"),
        Pattern("main", "images/events/cafeteria/cafeteria_event_1/cafeteria_event_1 <parent_level> <step>.webp"),
        thumbnail = "images/events/cafeteria/cafeteria_event_1/cafeteria_event_1 1 4.webp")
    
    cafeteria_event_2_event = Event(3, "cafeteria_event_2",
        TimeCondition(daytime = "1,6"),
        TimeSelector("time", "daytime"),
        RandomListSelector("char_class", "parent", ("school", RuleCondition('school_jobs')), realtime = True),
        ConditionSelector("level", CompareCondition("char_class", "parent"), 
            LevelSelector("", "parent"), 
            LevelSelector("", "school"),
            realtime = True
        ),
        RandomListSelector("girl_name", 
            ("adelaide_hall", CompareCondition('char_class', 'parent')),
            (
                RandomListSelector('', 'miwa_igarashi', 'luna_clark'), 
                CompareCondition('char_class', 'school')
            ),   
            realtime = True
        ),
        RandomListSelector('topic', (0.7, 'apron'), (0.2, 'breasts'), 'nude'),
        NumCompareCondition("level", 3, "<="),
        Pattern("main", "images/events/cafeteria/cafeteria_event_2/cafeteria_event_2 <girl_name> <topic> <level> <step>.webp", "level"),
        thumbnail = "images/events/cafeteria/cafeteria_event_2/cafeteria_event_2 adelaide_hall apron 1 0.webp")

    cafeteria_event_3_event = Event(3, "cafeteria_event_3",
        TimeCondition(weekday = "d", daytime = "d"),
        NOT(RuleCondition('school_jobs')),
        LevelSelector("parent_level", "parent"),
        ProgressSelector("unlock_school_jobs_value", "unlock_school_jobs"),
        ConditionSelector("unlock_school_jobs", CompareCondition("unlock_school_jobs_value", -1), 
            1, 
            ProgressSelector("", "unlock_school_jobs")
        ),
        RandomListSelector('topic', (0.4, 'normal'), 'tripped', 'overwhelmed'),
        Pattern("main", "images/events/cafeteria/cafeteria_event_3/cafeteria_event_3 <parent_level> <topic> <step>.webp"),
        thumbnail = "images/events/cafeteria/cafeteria_event_3/cafeteria_event_3 1 overwhelmed 19.webp")

    cafeteria_event_4_event = Event(3, "cafeteria_event_4",
        OR(
            TimeCondition(weekday = "d", daytime = "1,6"),
            TimeCondition(weekday = "w", daytime = "d")
        ),
        RuleCondition('school_jobs'),
        LevelCondition("1-6", "school"),
        LevelSelector("parent_level", "parent"),
        LevelSelector("school_level", "school"),
        RandomListSelector("amount", "1 Girl", "2 Girls", "3 Girls"),
        RandomListSelector("girl_1", 'miwa_igarashi'),
        RandomListSelector("girl_2",
            (1, "None", NOT(OR(
                CompareCondition('amount', "2 Girls"),
                CompareCondition('amount', '3 Girls')
            ))),
            'elsie_johnson',
            'luna_clark',
        ),
        RandomListSelector('girl_3',
            (1, 'None', NOT(CompareCondition('amount', '3 Girls'))),
            'sakura_mori',
        ),
        RandomListSelector('topic', 'normal'),
        Pattern("main", "images/events/cafeteria/cafeteria_event_4/cafeteria_event_4 <school_level> <girl_1> <girl_2> <girl_3>.webp"),
        thumbnail = "images/events/cafeteria/cafeteria_event_4/cafeteria_event_4 1 miwa_igarashi luna_clark None.webp")

    cafeteria_event_5_event = Event(3, "cafeteria_event_5",
        TimeCondition(weekday = "d", daytime = "f"),
        LevelSelector("school_level", "school"),
        Pattern("main", "images/events/cafeteria/cafeteria_event_5/cafeteria_event_5 <school_level> <step>.webp", 'classes'),
        thumbnail = "images/events/cafeteria/cafeteria_event_5/cafeteria_event_5 1 1.webp")

    cafeteria_event_6_event = Event(3, "cafeteria_event_6",
        TimeCondition(weekday = "d", daytime = "3,6"),
        Pattern("main", "images/events/cafeteria/cafeteria_event_6/cafeteria_event_6 <school_level> <step>.webp"),
        thumbnail = "images/events/cafeteria/cafeteria_event_6/cafeteria_event_6 2.webp")

    cafeteria_event_7_event = Event(3, "cafeteria_event_7",
        TimeCondition(weekday = "d", daytime = "6,7"),
        LevelCondition("1-3", "school"),
        Pattern("main", "images/events/cafeteria/cafeteria_event_7/cafeteria_event_7 <step>.webp"),
        thumbnail = "images/events/cafeteria/cafeteria_event_7/cafeteria_event_7 4.webp")

    cafeteria_general_event.add_event(
        cafeteria_construction_event
    )
    cafeteria_events["order_food"].add_event(
        cafeteria_event_1_event,
        cafeteria_event_2_event,
        cafeteria_event_3_event,
        cafeteria_event_4_event,
    )
    cafeteria_events["eat_alone"].add_event(
        cafeteria_event_5_event, 
    )
    cafeteria_events["look_around"].add_event(
        cafeteria_event_6_event,
        cafeteria_event_7_event,
    )

# endregion
########################################

######################################
# region Cafeteria Entry Point ----- #
######################################

label cafeteria ():
    call call_available_event(cafeteria_timed_event) from cafeteria_1

label .after_time_check (**kwargs):
    call call_available_event(cafeteria_general_event) from cafeteria_4

label .after_general_check (**kwargs):
    call call_event_menu (
        "What to do at the Cafeteria?", 
        cafeteria_events,
        default_fallback,
        character.subtitles,
        bg_image = cafeteria_bg_images,
    ) from cafeteria_3

    jump cafeteria

# endregion
######################################

#################################
# region Cafeteria Events ----- #
#################################

label cafeteria_construction(**kwargs):
    show screen black_screen_text("cafeteria_construction")

    if not contains_game_data("cafeteria_construction_end"):
        $ set_game_data("cafeteria_construction_end", time.day_to_string())

    $ end_time = Time(get_game_data("cafeteria_construction_end"))
    $ time_comparison = compare_time(time, end_time)

    $ image = convert_pattern("main", **kwargs)

    if time_comparison == -1:
        $ begin_event()

        $ day_difference = get_day_difference(time, end_time)
        $ image.show(0)
        headmaster "The cafeteria is under construction. It will be finished in [day_difference] days."

        $ end_event('map_overview', **kwargs)
    else:
        $ begin_event()

        $ set_progress("unlock_cafeteria", 3)
        $ image.show(1)
        headmaster "The cafeteria is finally finished. I can eat here now."

        $ update_quest("trigger", name = "cafeteria_opening")

        $ end_event('next_daytime', **kwargs)

#########################
# region Regular Events #

label cafeteria_event_1(**kwargs):
    $ begin_event(**kwargs)

    $ topic = get_value("topic", **kwargs)

    $ image = convert_pattern("main", **kwargs)
    
    $ adelaide = find_person("adelaide_hall").get_character()

    $ image.show(0)
    adelaide "Hello Mr. [headmaster_last_name] and welcome! What can I help you with?"

    $ image.show(1)
    headmaster "I would like to have a [topic]."

    $ image.show(2)
    adelaide "Sure, I'll get it for you right away."

    # $ image.show(3)
    # $ renpy.pause()
    call Image_Series.show_image(image, 4, 5) from _call_Image_Series_show_image
    adelaide "Here you go."
    headmaster "Thank you."

    call change_stats_with_modifier('parent',
        happiness = SMALL, charm = TINY) from _call_change_stats_with_modifier

    $ end_event('new_daytime', **kwargs)

label cafeteria_event_2(**kwargs):
    $ begin_event("2", **kwargs)

    $ char_class = get_value('char_class', **kwargs)
    $ time_ob = get_value('time', **kwargs)
    $ girl_name = get_value('girl_name', **kwargs)

    $ image = convert_pattern("main", **kwargs)

    $ girl_person = find_person(girl_name)
    $ girl = girl_person.get_character()
    $ girl_first_name = girl_person.get_first_name()

    # headmaster walks into the cafeteria pantry where someone is changing clothes
    $ image.show(0)
    if time_ob == 1:
        headmaster_thought "It seems [girl_first_name] is getting ready for work."
    else:
        headmaster_thought "Ah, [girl_first_name] is finishing up her work."

    $ image.show(1)
    headmaster "I'm sorry, I didn't mean to disturb you."
    $ image.show(2)
    girl "Eh? Please leave, I'm changing."

    call change_stats_with_modifier(char_class,
        happiness = DEC_TINY, inhibition = DEC_SMALL) from _call_change_stats_with_modifier_1

    $ end_event('new_daytime', **kwargs)

label cafeteria_event_3(**kwargs):
    $ begin_event(**kwargs)

    $ get_value('parent_level', **kwargs)
    $ topic = get_value('topic', **kwargs)
    if topic != 'overwhelmed':
        $ kwargs['unlock_school_jobs'] = 1
    $ unlock_school_jobs = get_stat_value('unlock_school_jobs', [2, 3], **kwargs)

    $ person = get_person("parents", "adelaide_hall").get_character()

    $ school_job_progress = get_progress('school_job_progress')

    $ image = convert_pattern("main", **kwargs)

    # headmaster enters and walks to counter
    # subtitles "You enter the cafeteria and step to the counter."
    if topic == "overwhelmed":
        # headmaster at counter talks
        $ image.show(0)
        headmaster "Hello, I would like to have a..."
        # Adelaide is seen working multiple tasks
        $ image.show(1)
        person "Sorry, I'm a bit busy. Could you wait a little bit please?"
        # view back to headmaster
        $ image.show(2)
        headmaster "Sure, no problem."
        # Adelaide approaches headmaster looking rather exhausted
        call Image_Series.show_image(image, 3, 4, 5, 6) from _call_Image_Series_show_image_1
        person "Sorry for the wait. What would you like to have?"
        # view back to headmaster
        $ image.show(7)
        headmaster "I'd like to have a sandwich and a coffee please."
        # Adelaide prepares the order
        $ image.show(8)
        person "Sure, I'll get it for you right away."
        # view back to headmaster
        $ image.show(9)
        headmaster "A busy day today?"
        # Adelaide pauses to talk with the headmaster
        $ image.show(10)
        person "You could say that. I'm a bit overwhelmed with work. "
        person "Today there just too much work to do for one person."

        if unlock_school_jobs != 2:
            $ unlock_school_jobs = set_progress('unlock_school_jobs', unlock_school_jobs)
            if unlock_school_jobs < 2:
                $ school_job_progress = advance_progress('school_job_progress')

            # Adelaide gives the order to the headmaster
            $ image.show(11)
            person "Well anyway, here is your order. Have a nice day."
            $ image.show(12)
            headmaster "Thank you, you too."

            if school_job_progress >= 3 and unlock_school_jobs < 2:
                $ set_progress('unlock_school_jobs', 2)

            call change_stats_with_modifier('parent',
                happiness = DEC_SMALL, charm = TINY) from _call_change_stats_with_modifier_2

            $ end_event('new_daytime', **kwargs)

        elif unlock_school_jobs == 2:
            # headmaster looks to be in thought
            $ image.show(13)
            headmaster "Mhh I see. I could help you out if you want."
            # Adelaide looks happy
            $ image.show(14)
            person "Really? That would be great. I would really appreciate it."
            # headmaster goes behind the counter
            $ image.show(15)
            headmaster "No problem. What do you want me to do?"
            # Adelaide gives headmaster a task
            $ image.show(16)
            person "Well, I need someone to help me with the dishes. Could you do that?"
            # headmaster thumbs up
            $ image.show(17)
            headmaster "Sure, I can do that."
            # Adelaide thumbs up
            $ image.show(18)
            parent "Thank you! After that you could help with..."

            call screen black_screen_text("2 hours later")

            $ hide_all()

            # Adelaide approaches headmaster rather exhausted
            $ image.show(19)
            person "Thank you so much for your help. I really appreciate it."

            # Headmaster looks exhausted as well
            $ image.show(20)
            headmaster "You're welcome. I'm glad I could help you out."

            # Headmaster and Adelaide start discussion
            $ image.show(21)
            headmaster "You know, what do you think about hiring some students to help you out?"
            $ image.show(22)
            person "You mean part time. Wouldn't that distract them from their studies?"
            $ image.show(21)
            headmaster "Maybe, but I think it would be a good opportunity for them to learn some responsibility."
            headmaster "And it would give them some experience for their future. Also I'm sure you both would profit from that."
            headmaster "I'm sure you are well aware that even though the school provides everything necessary for the students, there are still some students who struggle due to their low income families."
            $ image.show(22)
            parent "Yes those poor girl. I always try to help them as much as I can, but I still have to cover the costs and I'm already working non-profit here."
            $ image.show(21)
            headmaster "That's really admirable. I'm sure the students are really grateful for your help."
            headmaster "So I guess we both agree that it would be a good idea to hire some students to help you out."
            $ image.show(23)
            parent "Yes, definitely. I'll support that Idea at the PTA meeting and will convince the other parents to do so as well."
            $ image.show(24)
            headmaster "Great, I'm looking forward to it."
            # Adelaide gives headmaster a sandwich and a coffee
            $ image.show(25)
            person "Thank you so much for your help. Also I made your sandwich and coffee. You definitely earned it."
            # Headmaster takes the sandwich and coffee
            $ image.show(26)
            headmaster "Oh thank you I completely forgot about that."

            $ set_progress('unlock_school_jobs', 3)

            $ add_notify_message("Added new rule to journal!")

            $ time.progress_time()
            
            call change_stats_with_modifier('parent',
                happiness = MEDIUM, charm = SMALL, reputation = MEDIUM) from _call_change_stats_with_modifier_3

            $ end_event('new_daytime', **kwargs)

    elif topic == "tripped":
        # headmaster approaches counter
        $ image.show(0)
        headmaster "Hello, I would like to have a..."
        # Adelaide is seen falling behind the counter
        $ image.show(1)
        person "Ahh!"
        subtitles "*CRASH*"
        # headmaster looks over the counter
        $ image.show(2)
        headmaster "Oh no! Are you okay?"
        # Adelaide lying behind counter
        $ image.show(3)
        person "Yes, I'm fine. I just tripped over my own feet."
        # headmaster leaps over counter
        $ image.show(4)
        headmaster "Here, let me help you."
        # headmaster crouches next to adelaide
        $ image.show(5)
        headmaster "Does anything hurt?"
        # adelaide rubs her ankle
        $ image.show(6)
        person "Yes, my ankle hurts a bit."
        # headmaster takes a look at the ankle
        $ image.show(7)
        headmaster "Let me take a look at it."
        $ image.show(8)
        headmaster "It seems like you sprained your ankle. You should go to the nurse's office and get it checked out."
        # adelaide tries to stand up
        $ image.show(9)
        person "I don't think it's that bad. I can still walk."
        # headmaster helps adelaide up
        $ image.show(10)
        headmaster "No I insist. I'll take care of the kitchen while you're away."
        # adelaide looks at headmaster
        person "Okay, thank you."
        # headmaster works in the kitchen
        $ image.show(11)
        subtitles "You spend the next hours working in the kitchen."

        call change_stats_with_modifier('parent',
            happiness = SMALL, charm = DEC_TINY, reputation = SMALL) from _call_change_stats_with_modifier_4

        $ end_event('new_daytime', **kwargs)

    else:
        # headmaster approaches counter
        $ image.show(0)
        headmaster "Hello, I would like to have a coffee please."
        # Adelaide prepares the order
        person "Sure, I'll get it for you right away."
        # Adelaide gives the order to the headmaster
        $ image.show(1)
        person "Here you go."
        # headmaster takes the sandwich and coffee
        headmaster "Thank you."

        call change_stats_with_modifier('parent',
            happiness = SMALL, charm = TINY) from _call_change_stats_with_modifier_5

        $ end_event('new_daytime', **kwargs)

label cafeteria_event_4(**kwargs):
    $ begin_event(**kwargs)

    $ parent_level = get_value('parent_level', **kwargs)
    $ school_level = get_value('school_level', **kwargs)
    $ amount = get_value("amount", **kwargs)
    $ girl_1 = get_value("girl_1", **kwargs)
    $ girl_2 = get_value("girl_2", **kwargs)
    $ girl_3 = get_value("girl_3", **kwargs)
    $ topic = get_value("topic", **kwargs)
    
    $ show_pattern("main", **kwargs)

    headmaster_thought "It seems Adelaide is already putting the girls to work."
    if amount == "2 Girls" or amount == "3 Girls":
        headmaster_thought "I'm glad that so many girls are ready to help her."

    call change_stats_with_modifier('school',
        happiness = SMALL, charm = MEDIUM, education = TINY) from _call_change_stats_with_modifier_6

    call change_stats_with_modifier('parent',
        happiness = MEDIUM, charm = TINY) from _call_change_stats_with_modifier_7

    $ end_event('new_daytime', **kwargs)

label cafeteria_event_5(**kwargs):
    $ begin_event("2", **kwargs)

    $ image = convert_pattern("main", **kwargs)

    # Headmaster walks to empty table with his food
    $ image.show(0)
    subtitles "You take your lunch, sit down at a table and observe your surroundings."

    # Headmaster looks around
    call empty_label from _call_Image_Series_show_image_2
    $ image.show(1)
    headmaster_thought "It seems like the students are enjoying their lunch break."

    call change_stats_with_modifier('school',
        happiness = SMALL, charm = MEDIUM) from _call_cafeteria_event_5_1

    $ end_event('new_daytime', **kwargs)

label cafeteria_event_6(**kwargs):
    $ begin_event(**kwargs)

    $ image = convert_pattern("main", **kwargs)

    $ image.show(0)
    subtitles "The food seems to be at least somewhat tasty."
    $ image.show(1)

    call change_stats_with_modifier('school',
        happiness = SMALL
    ) from _call_cafeteria_event_6_1

    $ end_event('new_daytime', **kwargs)

label cafeteria_event_7(**kwargs):
    $ begin_event(**kwargs)

    $ image = convert_pattern("main", **kwargs)

    $ luna = get_person("class_3a", "luna_clark").get_character()
    $ seraphina = get_person("class_3a", "seraphina_clark").get_character()

    $ image.show(0)
    headmaster "What are you girls doing here at this time?"

    $ image.show(1)
    luna "Oh hello Mr. [headmaster_last_name]. We are baking a cake."
    $ image.show(2)
    seraphina "Yeah. We already got permission from Mrs. Hall."

    $ image.show(3)
    headmaster "Oh I see. That's nice! But I have one question."
    $ image.show(4)
    headmaster "Why are you only wearing underwear below your aprons?"

    $ image.show(5)
    luna "We do?"
    $ image.show(6)
    luna "Eeeek! I forgot!"
    $ image.show(7)
    seraphina "Well we didn't want to get our clothes dirty."
    $ image.show(8)
    luna "Please don't look!"

    $ image.show(9)
    headmaster "I see. Well, that's reasonable I guess."
    $ image.show(10)
    headmaster "I'll leave you to it then. Remember to clean up afterwards."

    luna "*whimper*"
    $ image.show(11)
    seraphina "Yes, we will. Thank you Mr. [headmaster_last_name]."
    $ image.show(12)
    seraphina "Now calm down Luna. There is nothing to it."
    $ image.show(13)
    luna "But he saw our underwear!"
    $ image.show(14)
    seraphina "So what? Calm down."

    call change_stats_with_modifier('school',
        happiness = DEC_TINY, inhibition = DEC_SMALL
    ) from _call_cafeteria_event_7_1

    $ end_event('new_daytime', **kwargs)

# endregion
#########################

# endregion
#################################