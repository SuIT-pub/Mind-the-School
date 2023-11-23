#############################################
# ----- Office Building Event Handler ----- #
#############################################

init -1 python:
    office_building_after_time_check = Event(2, "office_building.after_time_check")
    office_building_fallback         = Event(2, "office_building_fallback")

    office_building_timed_event = EventStorage("office_building", "", office_building_after_time_check)
    office_building_events = {
        "look_around": EventStorage("look",      "Look around",         office_building_fallback),
        "tutorial":    EventStorage("tutorial",  "About the school...", office_building_fallback),
        "paperwork":   EventStorage("paperwork", "Do paperwork",        office_building_fallback),
        "messages":    EventStorage("messages",  "Check messages",      office_building_fallback),
        "internet":    EventStorage("internet",  "Surf internet",       office_building_fallback),
        "council":     EventStorage("council",   "Council work",        office_building_fallback),
    }
    
    office_building_timed_event.add_event(Event(1,
        ["first_week_office_building_event"],
        TimeCondition(day = "2-4", month = 1, year = 2023),
    ))
    
    office_building_timed_event.add_event(Event(1,
        ["first_potion_office_building_event"],
        TimeCondition(day = 9),
    ))

    office_building_events["look_around"].add_event(Event(3,
        ["office_event_1", "office_event_2"],
        TimeCondition(weekday = "d", daytime = "d"),
    ))

    office_building_events["look_around"].add_event(Event(3,
        ["office_event_3"],
        TimeCondition(weekday = "d", daytime = "d"),
        NOT(RuleCondition("student_student_relation")),
    ))

    office_building_timed_event.check_all_events()
    map(lambda x: x.check_all_events(), office_building_events.values())

    office_building_bg_images = [
        BGImage("images/background/office building/bg c teacher.jpg", 1, TimeCondition(daytime = "c"), ValueCondition('name', 'teacher')), # show headmasters/teachers office empty
        BGImage("images/background/office building/bg c secretary <level> <nude>.jpg", 1, TimeCondition(daytime = "c"), ValueCondition('name', 'secretary')), # show headmasters/teachers office with people
        BGImage("images/background/office building/bg f <name> <level> <nude>.jpg", 1, TimeCondition(daytime = "f")), # show headmasters/teachers office with people
        BGImage("images/background/office building/bg 7 <name>.jpg", 1, TimeCondition(daytime = 7)), # show headmasters/teachers office empty at night
    ]
    
#############################################

###########################################
# ----- Office Building Entry Point ----- #
###########################################

label office_building ():

    call call_available_event(office_building_timed_event) from office_building_1

label .after_time_check (**kwargs):

    $ char = get_random_choice("teacher", "secretary")

    $ char_obj = get_character(char, charList['staff'])

    call show_office_building_idle_image(char_obj) from office_building_2



    call call_event_menu (
        "Hello Headmaster! How can I help you?" if char_obj.get_name() == "secretary" else "What do you do?", 
        office_building_events, 
        office_building_fallback,
        character.secretary if char_obj.get_name() == "secretary" else character.subtitles,
        char_obj = char_obj,
    ) from office_building_3

    jump office_building

label show_office_building_idle_image(char_obj):

    $ max_nude, image_path = get_background(
        "images/background/office building/bg f.jpg", # show headmasters office empty
        office_building_bg_images,
        char_obj
    )

    call show_image_with_nude_var (image_path, max_nude) from _call_show_image_with_nude_var_12

    return

###########################################

####################################################
# ----- High School Building Fallback Events ----- #
####################################################

label office_building_fallback (**kwargs):
    subtitles "There is nothing to do here."
    jump map_overview

####################################################

###########################################
# ----- High School Building Events ----- #
###########################################

label first_potion_office_building_event (**kwargs):

    show first potion office 1 with dissolveM
    subtitles "You enter the teachers office."
    headmaster_thought "Ahh the teacher seem to be eating at the kiosk as well."
    show first potion office 2 with dissolveM
    headmaster_thought "Not that I have a problem with it. Quite the opposite. That makes some things a bit easier."

    $ set_building_blocked("office_building")

    jump new_daytime

# first week event
label first_week_office_building_event (**kwargs):

    show first week office building 1 with dissolveM
    subtitles "Mhh. The office is nothing special but at least not really run down."
    subtitles "I can work with that."

    $ change_stat_for_all("education", 5, charList['schools'])
    $ change_stat_for_all("happiness", 5, charList['staff'])
    $ change_stat_for_all("reputation", 5, charList['staff'])

    $ set_building_blocked("office_building")

    jump new_day

# TODO: make images
label office_event_1 (**kwargs):
    $ image = Image_Series("images/events/office/office_event_1 <name> <level> <step>.png", name = "high_school", **kwargs)

    $ begin_event();

    $ image.show(0)
    subtitles "You notice a girl sitting in front of the teachers office."

    $ image.show(1)
    subtitles "Apparently she is in need of counseling."

    $ change_stats_with_modifier(kwargs["char_obj"],
        happiness = TINY, reputation = TINY)
    $ change_stats_with_modifier(get_character("teacher", charList['staff']),
        happiness = TINY)
    
    jump new_daytime

# TODO: make images
label office_event_2 (**kwargs):
    $ begin_event();
    
    call show_image(get_image("images/events/office/office_event_2 <level> <variant>.png", **kwargs)[1])
    subtitles "Even the teachers need a break from time to time."

    $ change_stats_with_modifier(kwargs["char_obj"],
        education = DEC_SMALL, reputation = DEC_TINY)
    $ change_stats_with_modifier(get_character("teacher", charList['staff']),
        happiness = TINY)

    jump new_daytime

# TODO: make images
label office_event_3 (**kwargs):
    $ image = Image_Series("images/events/office/office_event_3 <name> <level> <step>.png", name = "high_school", **kwargs)

    $ begin_event();

    $ image.show(0)
    subtitles "You enter the office and see two students sitting there."
    
    $ call_custom_menu(False, 
        ("Ignore them", "office_event_3.ignore"),
        ("Ask why here", "office_event_3.talk"),
    **kwargs)

label .ignore (**kwargs):
    $ image.show(1)
    subtitles "You ignore them and continue you way."

    $ change_stats_with_modifier(get_character("teacher", charList['staff']),
        happiness = TINY)

    jump new_daytime

label .talk (**kwargs):
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

    $ change_stats_with_modifier(kwargs["char_obj"],
        charm = SMALL, happiness = DEC_SMALL)
    $ change_stats_with_modifier(get_character("teacher", charList['staff']),
        happiness = TINY)

    jump new_daytime

label .care (**kwargs):
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

    $ change_stats_with_modifier(kwargs["char_obj"],
        charm = DEC_SMALL, happiness = MEDIUM, inhibition = DEC_SMALL)
    $ change_stats_with_modifier(get_character("teacher", charList['staff']),
        happiness = DEC_SMALL)

    if get_progress("unlock_student_relationship") == -1:
        $ start_progress("unlock_student_relationship")

    jump new_daytime

###########################################