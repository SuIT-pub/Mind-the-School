#############################################
# ----- Office Building Event Handler ----- #
#############################################

init -1 python:
    office_building_timed_event = TempEventStorage("office_building", "office_building", Event(2, "office_building.after_time_check"))
    office_building_general_event = EventStorage("office_building", "office_building", Event(2, "office_building.after_general_check"))
    office_building_events = {
        "look_around": EventStorage("look_around",   "office_building"),
        "tutorial":    EventStorage("tutorial",      "office_building"),
        "paperwork":   EventStorage("paperwork",     "office_building"),
        "learn":       EventStorage("learn_subject", "office_building"),
    }

    office_building_bg_images = [
        BGImage("images/background/office building/bg c teacher.webp", 1, TimeCondition(daytime = "c"), ValueCondition('name', 'teacher')), # show headmasters/teachers office empty
        BGImage("images/background/office building/bg c secretary <secretary_level> <nude>.webp", 1, TimeCondition(daytime = "c"), ValueCondition('name', 'secretary')), # show headmasters/teachers office with people
        BGImage("images/background/office building/bg f <name> <teacher_level> <nude>.webp", 1, TimeCondition(daytime = "f")), # show headmasters/teachers office with people
        BGImage("images/background/office building/bg 7 <name>.webp", 1, TimeCondition(daytime = 7)), # show headmasters/teachers office empty at night
    ]

init 1 python:    
    first_week_office_building_event_event = Event(1, "first_week_office_building_event",
        TimeCondition(day = "2-4", month = 1, year = 2023),
        thumbnail = "images/events/first week/first week office building 1.webp")
    
    first_potion_office_building_event_event = Event(1, "first_potion_office_building_event",
        TimeCondition(day = 9, month = 1, year = 2023),
        thumbnail = "images/events/first potion/first potion office 1.webp")

    office_event1 = Event(3, "office_event_1",
        TimeCondition(weekday = "d", daytime = "d"),
        thumbnail = "images/events/office/office_event_1 1 0.webp")

    office_event2 = Event(3, "office_event_2",
        RandomListSelector("teacher", "Finola Ryan", "Yulan Chen"),
        TimeCondition(weekday = "d", daytime = "d"),
        thumbnail = "images/events/office/office_event_2 1 Finola Ryan.webp")

    office_event3 = Event(3, "office_event_3",
        TimeCondition(weekday = "d", daytime = "d"),
        NOT(RuleCondition("student_student_relation")),
        thumbnail = "images/events/office/office_event_3 1 0.webp")


    office_building_timed_event.add_event(
        first_potion_office_building_event_event,
        first_week_office_building_event_event,
    )

    office_building_events["look_around"].add_event(
        office_event1, 
        office_event2, 
        office_event3,
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

    call show_idle_image("images/background/office building/bg f.webp", office_building_bg_images) from office_building_2

    call call_event_menu (
        "Hello Headmaster! How can I help you?" if char_obj.get_name() == "secretary" else "What do you do?", 
        office_building_events, 
        default_fallback,
        character.secretary if char == "secretary" else character.subtitles,
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

    $ change_stats_with_modifier(school_obj,
        happiness = TINY, reputation = TINY)
    $ change_stats_with_modifier(teacher_obj,
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

    $ change_stats_with_modifier(school_obj,
        education = DEC_SMALL, reputation = DEC_TINY)
    $ change_stats_with_modifier(teacher_obj,
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

    $ change_stats_with_modifier(teacher_obj,
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

    $ change_stats_with_modifier(school_obj,
        charm = SMALL, happiness = DEC_SMALL)
    $ change_stats_with_modifier(teacher_obj,
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

    $ change_stats_with_modifier(school_obj,
        charm = DEC_SMALL, happiness = MEDIUM, inhibition = DEC_SMALL)
    $ change_stats_with_modifier(teacher_obj,
        happiness = DEC_SMALL)

    if get_progress("unlock_student_relationship") == -1:
        $ start_progress("unlock_student_relationship")
        $ renpy.notify("Updated the Journal!")
        
    $ end_event('new_daytime', **kwargs)

###########################################