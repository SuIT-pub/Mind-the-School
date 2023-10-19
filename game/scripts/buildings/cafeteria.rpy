#######################################
# ----- Cafeteria Event Handler ----- #
#######################################

init -1 python:
    cafeteria_after_time_check = Event(2, "cafeteria.after_time_check")
    cafeteria_fallback         = Event(2, "cafeteria_fallback")
    cafeteria_eat_fallback     = Event(2, "cafeteria_eat_fallback")
    cafeteria_person_fallback  = Event(2, "cafeteria_person_fallback")
    cafeteria_look_fallback    = Event(2, "cafeteria_look_fallback")

    cafeteria_timed_event = EventStorage("cafeteria", "", cafeteria_after_time_check)
    cafeteria_events = {
        "eat_alone":   EventStorage("eat_alone",   "Eat alone",         cafeteria_eat_fallback),
        "eat_student": EventStorage("eat_student", "Eat with students", cafeteria_eat_fallback),
        "eat_teacher": EventStorage("eat_teacher", "Eat with teacher",  cafeteria_eat_fallback),
        "eat_look":    EventStorage("eat_look",    "Look around",       cafeteria_eat_fallback),
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

    call show_cafeteria_idle_image(school_obj) from cafeteria_2

    call call_event_menu (
        "What to do at the Cafeteria?", 
        cafeteria_events, 
        cafeteria_fallback,
        character.subtitles,
        char_obj = school_obj,
    ) from cafeteria_3

    jump cafeteria

label show_cafeteria_idle_image(school_obj):
    $ max_nude, image_path = get_background(
        "images/background/cafeteria/bg c.jpg", # show empty terrace
        cafeteria_bg_images,
        school_obj,
    )

    call show_image_with_nude_var (image_path, max_nude) from _call_show_image_with_nude_var_1

    return

#####################################

#########################################
# ----- Cafeteria Fallback Events ----- #
#########################################

label cafeteria_fallback (**kwargs):
    subtitles "There is nothing to do here."
    jump map_overview
label cafeteria_eat_fallback (**kwargs):
    subtitles "I'm not hungry."
    jump map_overview
label cafeteria_person_fallback (**kwargs):
    subtitles "There is nobody here."
    jump map_overview
label cafeteria_look_fallback (**kwargs):
    subtitles "There is nothing to see here."
    jump map_overview

#########################################

################################
# ----- Cafeteria Events ----- #
################################


################################