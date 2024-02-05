#######################################
# ----- Cafeteria Event Handler ----- #
#######################################

init -1 python:
    cafeteria_timed_event = TempEventStorage("cafeteria", "", "cafeteria", Event(2, "cafeteria.after_time_check"))
    cafeteria_general_event = EventStorage("cafeteria", "", "cafeteria", Event(2, "cafeteria.after_general_check"))
    cafeteria_events = {
        "eat_alone":   EventStorage("eat_alone",   "Eat alone",         "cafeteria", default_fallback, "I'm not hungry."),
        "eat_student": EventStorage("eat_student", "Eat with students", "cafeteria", default_fallback, "I'm not hungry."),
        "eat_teacher": EventStorage("eat_teacher", "Eat with teacher",  "cafeteria", default_fallback, "I'm not hungry."),
        "eat_look":    EventStorage("eat_look",    "Look around",       "cafeteria", default_fallback, "I'm not hungry."),
    }

    cafeteria_bg_images = [
        BGImage("images/background/cafeteria/bg 1,6 <level> <nude>.webp", 1, TimeCondition(daytime = "1,6")), # show terrace with a few students
        BGImage("images/background/cafeteria/bg 3 <level> <nude>.webp", 1, TimeCondition(daytime = 3)), # show terrace full of students and teacher
        BGImage("images/background/cafeteria/bg 7.webp", 1, TimeCondition(daytime = 7)), # show empty terrace at night
    ]
    
init 1 python:
    cafeteria_construction_event = Event(1, "cafeteria_construction",
        ProgressCondition("unlock_cafeteria", "2"))

    cafeteria_event_1_event = Event(3, "cafeteria_event_1",
        TimeCondition(daytime = "d"),
        RandomListSelector("topic", "coffee", "tea", "warm milk"),
        thumbnail = "")
    
    cafeteria_event_2_event = Event(3, "cafeteria_event_2",
        TimeCondition(daytime = "1,6"),
        TimeSelector("time", "daytime"),
        RandomListSelector("girl_name", "Adelaide Hall",
            (
                RandomListSelector('', 'Miwa Igarashi'),
                RuleCondition('school_jobs')
            ),
        ),
        RandomListSelector('topic', (0.7, 'apron'), (0.1, 'underwear'), (0.07, 'bra'), 'breasts', 'nude'),
        thumbnail = "")

    cafeteria_event_3_event = Event(3, "cafeteria_event_3",
        OR(
            TimeCondition(weekday = "d", daytime = "f")
        ),
        NOT(RuleCondition('school_jobs')),
        ProgressSelector("unlock_school_jobs_value", "unlock_school_jobs"),
        ConditionSelector("unlock_school_jobs", CompareCondition("unlock_school_jobs_value", -1), 
            1, 
            ProgressSelector("", "unlock_school_jobs")
        ),
        RandomListSelector('topic', (0.5, 'normal'), (0.2, 'tripped'), (0.15, 'tripped_injury'), 'overwhelmed'),
        thumbnail = "")

    cafeteria_event_4_event = Event(3, "cafeteria_event_4",
        OR(
            TimeCondition(weekday = "d", daytime = "f"),
            TimeCondition(weekday = "w", daytime = "d")
        ),
        RuleCondition('school_jobs'),
        RandomListSelector("amount", "1 Girl", "2 Girls", "3 Girls"),
        RandomListSelector("girl_1", 'Miwa Igarashi'),
        RandomListSelector("girl_2",
            (1, "None", NOT(OR(
                CompareCondition('amount', "2 Girls"),
                CompareCondition('amount', '3 Girls')
            ))),
            'Elsie Johnson',
            ('Luna Clark', loli_content >= 1),
        ),
        RandomListSelector('girl_3',
            (1, 'None', NOT(CompareCondition('amount', '3 Girls'))),
            'Sakura Mori',
        ),
        RandomListSelector('topic', 'normal'),
        thumbnail = "")

    cafeteria_event_5_event = Event(3, "cafeteria_event_5",
        TimeCondition(weekday = "d", daytime = "f"),
        RandomListSelector('classes', 
            ('3A', LoliContentCondition(0)),
            (RandomListSelector('', '3A', '2A', '2A 3A'), LoliContentCondition(1)),
            (RandomListSelector('', '1A', '1A 2A', '1A 2A, 3A', '1A 3A', '2A', '2A 3A', '3A'), LoliContentCondition(2))
        ),
        thumbnail = "")


    cafeteria_general_event.add_event(
        cafeteria_construction_event
    )
    cafeteria_events["eat_alone"].add_event(
        cafeteria_event_3_event, 
        cafeteria_event_4_event, 
        cafeteria_event_5_event
    )
    cafeteria_events["eat_student"].add_event(
        cafeteria_event_3_event, 
        cafeteria_event_4_event
    )
    cafeteria_events["eat_teacher"].add_event(
        cafeteria_event_3_event, 
        cafeteria_event_4_event
    )
    cafeteria_events["eat_look"].add_event(
        cafeteria_event_2_event
    )


#######################################

#####################################
# ----- Cafeteria Entry Point ----- #
#####################################

label cafeteria ():
    call call_available_event(cafeteria_timed_event) from cafeteria_1

label .after_time_check (**kwargs):
    call call_available_event(cafeteria_general_event) from cafeteria_4

label .after_general_check (**kwargs):
    $ school_obj = get_school()

    call show_idle_image(school_obj, "images/background/cafeteria/bg c.webp", cafeteria_bg_images) from cafeteria_2

    call call_event_menu (
        "What to do at the Cafeteria?", 
        cafeteria_events,
        default_fallback,
        character.subtitles,
        char_obj = school_obj,
    ) from cafeteria_3

    jump cafeteria

#####################################

################################
# ----- Cafeteria Events ----- #
################################

label cafeteria_construction(**kwargs):
    show screen black_screen_text("cafeteria_construction")

    if not contains_game_data("cafeteria_construction_end"):
        $ set_game_data("cafeteria_construction_end", time.day_to_string())

    $ end_time = Time(get_game_data("cafeteria_construction_end"))
    $ time_comparison = compare_time(time, end_time)

    if time_comparison == -1:
        $ begin_event()

        $ day_difference = get_day_difference(time, end_time)
        headmaster "The cafeteria is under construction. It will be finished in [day_difference] days."

        $ end_event('map_overview', **kwargs)
    else:
        $ begin_event(**kwargs)

        $ set_progress("unlock_cafeteria", 3)
        headmaster "The cafeteria is finally finished. I can eat here now."

        $ end_event('next_daytime', **kwargs)

label cafeteria_event_1(**kwargs):
    $ begin_event(**kwargs)

    $ char_obj = get_char_value(**kwargs)
    $ topic = get_value("topic", **kwargs)

    show screen black_screen_text("cafeteria_event_1\n" + topic)

    # Adelaide greets Headmaster
    parent "Hello Mr. [headmaster_last_name] and welcome! What can I help you with?" (name = 'Adelaide Hall')

    # Headmaster orders
    headmaster "I would like to have a [topic]."

    # Adelaide gets off to prepare the order
    parent "Sure, I'll get it for you right away." (name = 'Adelaide Hall')

    # Headmaster meanwhile looks into the cafeteria

    $ end_event('new_daytime', **kwargs)

label cafeteria_event_2(**kwargs):
    $ begin_event(**kwargs)

    $ char_obj = get_char_value(**kwargs)
    $ time_ob = get_value('time', **kwargs)
    $ girl_name = get_value('girl_name', **kwargs)
    $ topic = get_value('topic', **kwargs)

    show screen black_screen_text("cafeteria_event_2\nTime: " + str(time_ob) + "\n" + girl_name)

    # headmaster walks into the cafeteria pantry where someone is changing clothes
    if time_ob == 1:
        headmaster_thought "It seems [girl_name] is getting ready for work."
    else:
        headmaster_thought "Ah, [girl_name] is finishing up her work."

    headmaster "I'm sorry, I didn't mean to disturb you."
    sgirl "Eh? Please leave, I'm changing."

    $ end_event('new_daytime', **kwargs)

label cafeteria_event_3(**kwargs):
    $ begin_event(**kwargs)

    $ char_obj = get_char_value(**kwargs)
    $ unlock_school_jobs = get_value('unlock_school_jobs', **kwargs)
    $ topic = get_value('topic', **kwargs)

    $ name = "Adelaide Hall"

    $ school_job_progress = get_progress('school_job_progress')

    show screen black_screen_text("cafeteria_event_3\nSchool Job Progress: " + str(unlock_school_jobs) + "\n" + girl_name + "\n" + topic)

    $ image = Image_Series("images/background/cafeteria/cafeteria_event_3 <level> <school_jobs>.webp")

    # headmaster enters and walks to counter
    subtitles "You enter the cafeteria and step to the counter."
    if topic == "overwhelmed":
        # headmaster at counter talks
        headmaster "Hello, I would like to have a..."
        # Adelaide is seen working multiple tasks
        parent "Sorry, I'm a bit busy. Could you wait a little bit please?" (name = name)
        # view back to headmaster
        headmaster "Sure, no problem."
        # view on headmaster waiting in front of the counter looking around
        subtitles "You wait for a while."
        # Adelaide approaches headmaster looking rather exhausted
        parent "Sorry for the wait. What would you like to have?" (name = name)
        # view back to headmaster
        headmaster "I'd like to have a sandwich and a coffee please."
        # Adelaide prepares the order
        parent "Sure, I'll get it for you right away." (name = name)
        # view back to headmaster
        headmaster "A busy day today?"
        # Adelaide pauses to talk with the headmaster
        parent "You could say that. I'm a bit overwhelmed with work. " (name = name)
        parent "Today there just too much work to do for one person." (name = name)

        if unlock_school_jobs != 2:
            $ unlock_school_jobs = set_progress('unlock_school_jobs', unlock_school_jobs)
            $ school_job_progress = advance_progress('school_job_progress')

            # Adelaide gives the order to the headmaster
            parent "Well anyway, here is your order. Have a nice day." (name = name)
            headmaster "Thank you, you too."

            if school_job_progress >= 3:
                $ set_progress('unlock_school_jobs', 2)
        elif unlock_school_jobs == 2:

            # headmaster looks to be in thought
            headmaster "Mhh I see. I could help you out if you want."
            # Adelaide looks happy
            parent "Really? That would be great. I would really appreciate it." (name = name)
            # headmaster goes behind the counter
            headmaster "No problem. What do you want me to do?"
            # Adelaide gives headmaster a task
            parent "Well, I need someone to help me with the dishes. Could you do that?" (name = name)
            # headmaster thumbs up
            headmaster "Sure, I can do that."
            # Adelaide thumbs up
            parent "Thank you! After that you could help with..."

            call screen black_screen_text("2 hours later")

            $ hide_all()

            # Adelaide approaches headmaster rather exhausted
            parent "Thank you so much for your help. I really appreciate it." (name = name)

            # Headmaster looks exhausted as well
            headmaster "You're welcome. I'm glad I could help you out."

            # Headmaster and Adelaide start discussion
            headmaster "You know, what do you think about hiring some students to help you out?"
            parent "You mean part time. Wouldn't that distract them from their studies?" (name = name)
            headmaster "Maybe, but I think it would be a good opportunity for them to learn some responsibility."
            headmaster "And it would give them some experience for their future. Also I'm sure you both would profit from that."
            headmaster "I'm sure you are well aware that even though the school provides everything necessary for the students, there are still some students who struggle due to their low income families."
            parent "Yes those poor girl. I always try to help them as much as I can, but I still have to cover the costs and I'm already working non-profit here."
            headmaster "That's really admirable. I'm sure the students are really grateful for your help."
            headmaster "So I guess we both agree that it would be a good idea to hire some students to help you out."
            parent "Yes, definitely. I'll support that Idea at the PTA meeting and will convince the other parents to do so as well."
            headmaster "Great, I'm looking forward to it."
            # Adelaide gives headmaster a sandwich and a coffee
            parent "Thank you so much for your help. Also I made your sandwich and coffee. You definitely earned it." (name = name)
            # Headmaster takes the sandwich and coffee
            headmaster "Oh thank you I completely forgot about that. See you later."
            # Adelaide waves
            parent "Bye."

            $ set_progress('unlock_school_jobs', 3)

            $ time.progress_time()

    elif topic == "tripped" or topic == "tripped_injury":

        # headmaster approaches counter
        headmaster "Hello, I would like to have a..."
        # Adelaide is seen falling behind the counter
        parent "Ahh!" (name = name)
        subtitles "*CRASH*"
        # headmaster looks over the counter
        headmaster "Oh no! Are you okay?"
        # Adelaide lying behind counter
        parent "Yes, I'm fine. I just tripped over my own feet." (name = name)
        # headmaster leaps over counter
        headmaster "Here, let me help you."
        # headmaster crouches next to adelaide
        headmaster "Does anything hurt?"

        if topic == "tripped_injury":
            # adelaide rubs her ankle
            parent "Yes, my ankle hurts a bit." (name = name)
            # headmaster takes a look at the ankle
            headmaster "Let me take a look at it."
            headmaster "It seems like you sprained your ankle. You should go to the nurse's office and get it checked out."
            # adelaide tries to stand up
            parent "I don't think it's that bad. I can still walk." (name = name)
            # headmaster helps adelaide up
            headmaster "No I insist. I'll take care of the kitchen while you're away."
            # adelaide looks at headmaster
            parent "Okay, thank you." (name = name)
            # headmaster works in the kitchen
            subtitles "You spend the next hours working in the kitchen."
        else:
            # adelaide already standing up again
            parent "No, I'm fine. I just need to be more careful." (name = name)
            # headmaster helps adelaide up
            headmaster "Okay, but if you need anything just let me know."
            # adelaide looks at headmaster
            parent "Thank you." (name = name)
    else:
        # headmaster approaches counter
        headmaster "Hello, I would like to have a sandwich and a coffee please."
        # Adelaide prepares the order
        parent "Sure, I'll get it for you right away." (name = name)
        # Adelaide gives the order to the headmaster
        parent "Here you go." (name = name)
        # headmaster takes the sandwich and coffee
        headmaster "Thank you."
    $ end_event('new_daytime', **kwargs)

label cafeteria_event_4(**kwargs):
    $ begin_event(**kwargs)

    $ char_obj = get_char_value(**kwargs)
    $ amount = get_value("amount", **kwargs)
    $ girl_1 = get_value("girl_1", **kwargs)
    $ girl_2 = get_value("girl_2", **kwargs)
    $ girl_3 = get_value("girl_3", **kwargs)
    $ topic = get_value("topic", **kwargs)
    
    show screen black_screen_text("cafeteria_event_4\n" + amount + "\n Girls: " + (', '.join([girl_1, girl_2, girl_3])) + "\n" + topic)

    subtitles "To be added."
    # Adelaide is seen working helped by students

    $ end_event('new_daytime', **kwargs)

label cafeteria_event_5(**kwargs):
    $ begin_event(**kwargs)

    $ char_obj = get_char_value(**kwargs)
    $ classes = get_value("classes", **kwargs)

    $ image = Image_Series("images/background/cafeteria/cafeteria_event_5 <level> <classes> <step>.webp")

    # Headmaster walks to empty table with his food
    $ image.show(0)
    subtitles "You take your lunch, sit down at a table and observe your surroundings."

    # Headmaster looks around
    $ image.show(1)
    headmaster_thought "It seems like the students are enjoying their lunch break."

    $ end_event('new_daytime', **kwargs)

################################