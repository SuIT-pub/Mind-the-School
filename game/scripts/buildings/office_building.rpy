#############################################
# ----- Office Building Event Handler ----- #
#############################################

init -1 python:
    def office_building_events_available() -> bool:
        return (office_building_timed_event.has_available_highlight_events() or
            office_building_general_event.has_available_highlight_events() or
            any(e.has_available_highlight_events() for e in office_building_events.values()))

    office_building_timed_event = TempEventStorage("office_building", "office_building", Event(2, "office_building.after_time_check"))
    office_building_general_event = EventStorage("office_building", "office_building", Event(2, "office_building.after_general_check"))

    office_building_work_event = EventStorage("office_building", "office_building")

    office_building_events = {}
    add_storage(office_building_events, EventStorage("look_around", "office_building"))
    add_storage(office_building_events, EventStorage("work",        "office_building"))

    office_building_bg_images = BGStorage("images/background/office building/bg f.webp",
        BGImage("images/background/office building/bg c teacher.webp", 1, TimeCondition(daytime = "c"), ValueCondition('name', 'teacher')), # show headmasters/teachers office empty
        BGImage("images/background/office building/bg c secretary <secretary_level> <nude>.webp", 1, TimeCondition(daytime = "c"), ValueCondition('name', 'secretary')), # show headmasters/teachers office with people
        BGImage("images/background/office building/bg f <name> <level> <nude>.webp", 1, TimeCondition(daytime = "f")), # show headmasters/teachers office with people
        BGImage("images/background/office building/bg 7 <name>.webp", 1, TimeCondition(daytime = 7)), # show headmasters/teachers office empty at night
    )

init 1 python:   
    office_building_general_event.add_event( 
        Event(1, "first_week_office_building_event",
            IntroCondition(),
            TimeCondition(day = "2-4", month = 1, year = 2023),
            thumbnail = "images/events/first week/first week office building 1.webp"),
        
        Event(1, "first_potion_office_building_event",
            IntroCondition(),
            TimeCondition(day = 9, month = 1, year = 2023),
            thumbnail = "images/events/first potion/first potion office 1.webp"),
    )


    office_building_events["look_around"].add_event(

        Event(3, "office_event_1",
            TimeCondition(weekday = "d", daytime = "f"),
            thumbnail = "images/events/office/office_event_1 1 0.webp"),

        Event(3, "office_event_2",
            RandomListSelector("teacher", "Finola Ryan", "Yulan Chen"),
            TimeCondition(weekday = "d", daytime = "f"),
            thumbnail = "images/events/office/office_event_2 1 Finola Ryan.webp"),

        Event(3, "office_event_3",
            TimeCondition(weekday = "d", daytime = "d"),
            NOT(RuleCondition("student_student_relation")),
            thumbnail = "images/events/office/office_event_3 1 0.webp"),
    )

    
    office_building_events["work"].add_event(
        Event(3, "work_office_event",
            TimeCondition(weekday = "d", daytime = "d")),
    )

    office_building_work_event.add_event(
        Event(3, "work_office_money_event_1",
            TimeCondition(weekday = "d", daytime = "d")),
        Event(3, "work_office_education_event_1",
            TimeCondition(weekday = "d", daytime = "d")),
        Event(3, "work_office_session_event_1",
            TimeCondition(weekday = "d", daytime = "d"),
            ConditionSelector("first_naughty_session", ProgressCondition("unlocked_work_office_session_naughty"),
                0,
                RandomValueSelector("", 0, 1), 
                True
            ),
            ProgressSelector("unlocked_naughty_sessions", "unlocked_work_office_session_naughty"),
            RandomListSelector("girl_name", "Seraphina Clark", "Gloria Goto", "Lin Kato", "Miwa Igarashi"),
        ),
    )

#############################################

###########################################
# ----- Office Building Entry Point ----- #
###########################################

label office_building ():
    call call_available_event(office_building_timed_event) from office_building_1

label .after_time_check (**kwargs):
    call call_available_event(office_building_general_event) from office_building_4

label .after_general_check (**kwargs):
    $ char = get_random_choice("teacher", "secretary")
    $ office_building_bg_images.add_kwargs(
        name = char,
        level = get_character_by_key(char).get_level(),
    )

    call call_event_menu (
        "Hello Headmaster! How can I help you?" if char == "secretary" else "What do you do?", 
        office_building_events, 
        default_fallback,
        character.secretary if char == "secretary" else character.subtitles,
        bg_image = office_building_bg_images,
        context = char,
    ) from office_building_3

    jump office_building

###########################################

###########################################
# ----- High School Building Events ----- #
###########################################

label first_potion_office_building_event (**kwargs):
    $ begin_event(**kwargs)
    
    show first potion office 1 with dissolveM
    subtitles "You enter the teachers office."
    headmaster_thought "Ahh the teacher seem to be eating at the kiosk as well."
    show first potion office 2 with dissolveM
    headmaster_thought "Not that I have a problem with it. Quite the opposite. That makes some things a bit easier."

    $ set_building_blocked("office_building")

    $ end_event('new_daytime', **kwargs)

# first week event
label first_week_office_building_event (**kwargs):
    $ begin_event(**kwargs)
    
    show first week office building 1 with dissolveM
    subtitles "Mhh. The office is nothing special but at least not really run down."
    subtitles "I can work with that."

    $ change_stat("education", 5, get_school())
    $ change_stat_for_all("happiness", 5, charList['staff'])
    $ change_stat_for_all("reputation", 5, charList['staff'])

    $ set_building_blocked("office_building")

    $ end_event('new_day', **kwargs)

label work_office_event (**kwargs):
    call call_event_menu (
        "What subject do you wanna teach?", 
        office_building_work_event,
        default_fallback,
        character.subtitles,
        override_menu_exit = 'office_building',
        **kwargs
    ) from work_office_event_1

    jump office_building

label work_office_money_event_1 (**kwargs):
    $ begin_event(**kwargs)

    subtitles "You work on checking the accounts of the school."
    show screen black_screen_text("1h later.")
    # headmaster is consumed by the terrible accounting done in the past
    headmaster_thought "How can this be? This is a mess!"
    headmaster_thought "I need to get this sorted out."
    headmaster_thought "There is so much wrong with these accounts. It's gonna take ages to fix this."
    headmaster_thought "At least I was able to find some money that was lost in the system."

    $ change_money_with_modifier(get_random_int(100, 500))

    $ end_event('new_daytime', **kwargs)

label work_office_education_event_1 (**kwargs):
    $ begin_event(**kwargs)

    $ school_obj = get_char_value('school_obj', **kwargs)
    $ teacher_obj = get_char_value('teacher_obj', **kwargs)

    subtitles "You work on optimizing the teaching material for the students."
    show screen black_screen_text("1h later.")
    headmaster_thought "I think I found a way to make the material more interesting for the students."

    call change_stats_with_modifier(school_obj,
        education = SMALL, happiness = TINY)
    call change_stats_with_modifier(teacher_obj,
        happiness = SMALL, education = SMALL)

    $ end_event('new_daytime', **kwargs)

label work_office_session_event_1 (**kwargs):
    $ begin_event(**kwargs)

    $ school_obj = get_char_value('school_obj', **kwargs)
    $ secretary_obj = get_char_value('secretary_obj', **kwargs)
    $ first_naughty_session = get_value("first_naughty_session", **kwargs)
    $ unlocked_naughty_sessions = get_value("unlocked_naughty_sessions", **kwargs)
    $ girl_name = get_value("girl_name", **kwargs)



    if unlocked_naughty_sessions != -1:
        menu:
            "Do you wanna call Emiko for a naughty session?"
            "Call Emiko":
                jump .naughty_session
            "No":
                jump .normal_session

    if first_naughty_session == 1:
        jump .first_naughty_session

    jump .normal_session    

label .first_naughty_session (**kwargs):
    pass
label .naughty_session (**kwargs):
    pass
label .normal_session (**kwargs):
    pass

# TODO: make images
label office_event_1 (**kwargs):
    $ begin_event(**kwargs);

    $ school_obj = get_char_value('school_obj', **kwargs)
    $ teacher_obj = get_char_value('teacher_obj', **kwargs)

    $ image = Image_Series("images/events/office/office_event_1 <school_level> <step>.webp", **kwargs)

    $ image.show(0)
    subtitles "You notice a girl sitting in front of the teachers office."

    $ image.show(1)
    subtitles "Apparently she is in need of counseling."

    call change_stats_with_modifier(school_obj,
        happiness = TINY, reputation = TINY)
    call change_stats_with_modifier(teacher_obj,
        happiness = TINY)
    
    $ end_event('new_daytime', **kwargs)

# TODO: make images
label office_event_2 (**kwargs):
    $ begin_event(**kwargs);

    $ teacher_obj = get_char_value('teacher_obj', **kwargs)
    $ school_obj = get_char_value('school_obj', **kwargs)
    $ teacher = get_value("teacher", **kwargs)

    call show_image ("images/events/office/office_event_2 <teacher_level> <teacher>.webp", **kwargs) from _call_show_image_office_event_2
    subtitles "Even the teachers need a break from time to time."

    call change_stats_with_modifier(school_obj,
        education = DEC_SMALL, reputation = DEC_TINY)
    call change_stats_with_modifier(teacher_obj,
        happiness = TINY)

    $ end_event('new_daytime', **kwargs)

# TODO: make images
label office_event_3 (**kwargs):
    $ begin_event(**kwargs);

    $ school_obj = get_char_value('school_obj', **kwargs)
    $ teacher_obj = get_char_value('teacher_obj', **kwargs)

    $ image = Image_Series("images/events/office/office_event_3 <school_level> <step>.webp", **kwargs)

    $ image.show(0)
    subtitles "You enter the office and see two students sitting there."
    
    $ call_custom_menu(False, 
        ("Ignore them", "office_event_3.ignore"),
        ("Ask why they are here", "office_event_3.talk"),
    **kwargs)

label .ignore (**kwargs):
    
    $ begin_event()
    
    $ image.show(1)
    subtitles "You ignore them and continue you way."

    call change_stats_with_modifier(teacher_obj,
        happiness = TINY)

    $ end_event('new_daytime', **kwargs)

label .talk (**kwargs):
    
    $ begin_event()
    
    $ image.show(2)
    headmaster "Why are you sitting here?"
    $ image.show(3)
    sgirl "We were called here by the teacher."
    $ image.show(2)
    headmaster "Do you know why?"
    $ image.show(4)
    sgirl "Probably because we are a couple."

    $ call_custom_menu(False, 
        ("Tell about policy", "office_event_3.policy"),
        ("Take care of it for them", "office_event_3.care"),
    **kwargs)

label .policy (**kwargs):
    
    $ begin_event()
    
    $ image.show(5)
    headmaster "Well, you know that relationships between students are not allowed."
    $ image.show(6)
    sgirl "But what does the school care about our relationship?"
    $ image.show(5)
    headmaster "It's a measure to keep you focused on your education."
    headmaster "At least hold yourself back until you are done with school."
    $ image.show(2)
    sgirl "..."
    headmaster "Now you both go back to class."

    call change_stats_with_modifier(school_obj,
        charm = SMALL, happiness = DEC_SMALL)
    call change_stats_with_modifier(teacher_obj,
        happiness = TINY)

    $ end_event('new_daytime', **kwargs)

label .care (**kwargs):
    
    $ begin_event()
    
    $ image.show(7)
    headmaster "Okay, listen. You know relationships aren't allowed here at school."
    $ image.show(6)
    sgirl "But..."
    $ image.show(7)
    headmaster "BUT, I don't like this rule either. So I will take care of it for you."
    headmaster "I think I will abandon this rule in the future."
    headmaster "Now go back to class."
    $ image.show(8)
    sgirl "Thank you!"

    call change_stats_with_modifier(school_obj,
        charm = DEC_SMALL, happiness = MEDIUM, inhibition = DEC_SMALL)
    call change_stats_with_modifier(teacher_obj,
        happiness = DEC_SMALL)

    if get_progress("unlock_student_relationship") == -1:
        $ start_progress("unlock_student_relationship")
        $ add_notify_message("Added new rule to journal!")
        
    $ end_event('new_daytime', **kwargs)

###########################################