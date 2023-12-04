#######################################
# ----- Cafeteria Event Handler ----- #
#######################################

init -1 python:
    cafeteria_timed_event = EventStorage("cafeteria", "", Event(2, "cafeteria.after_time_check"))
    cafeteria_events = {
        "eat_alone":   EventStorage("eat_alone",   "Eat alone",         default_fallback, "I'm not hungry."),
        "eat_student": EventStorage("eat_student", "Eat with students", default_fallback, "I'm not hungry."),
        "eat_teacher": EventStorage("eat_teacher", "Eat with teacher",  default_fallback, "I'm not hungry."),
        "eat_look":    EventStorage("eat_look",    "Look around",       default_fallback, "I'm not hungry."),
    }

    cafeteria_timed_event.check_all_events()
    map(lambda x: x.check_all_events(), cafeteria_events.values())

    cafeteria_bg_images = [
        BGImage("images/background/cafeteria/bg 1,6 <level> <nude>.jpg", 1, TimeCondition(daytime = "1,6")), # show terrace with a few students
        BGImage("images/background/cafeteria/bg 3 <level> <nude>.jpg", 1, TimeCondition(daytime = 3)), # show terrace full of students and teacher
        BGImage("images/background/cafeteria/bg 7.jpg", 1, TimeCondition(daytime = 7)), # show empty terrace at night
    ]
    
#######################################

#####################################
# ----- Cafeteria Entry Point ----- #
#####################################

label cafeteria ():

    call call_available_event(cafeteria_timed_event) from cafeteria_1

label .after_time_check (**kwargs):

    $ school_obj = get_random_school()

    call show_idle_image(school_obj, "images/background/cafeteria/bg c.jpg", cafeteria_bg_images) from cafeteria_2

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


################################