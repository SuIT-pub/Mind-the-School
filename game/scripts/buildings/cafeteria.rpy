#######################################
# ----- Cafeteria Event Handler ----- #
#######################################

init -1 python:
    cafeteria_after_time_check = Event("cafeteria_after_time_check", "cafeteria.after_time_check", 2)
    cafeteria_fallback         = Event("cafeteria_fallback",         "cafeteria_fallback",         2)
    cafeteria_eat_fallback     = Event("cafeteria_eat_fallback",     "cafeteria_eat_fallback",     2)
    cafeteria_person_fallback  = Event("cafeteria_person_fallback",  "cafeteria_person_fallback",  2)
    cafeteria_look_fallback    = Event("cafeteria_look_fallback",    "cafeteria_look_fallback",    2)

    cafeteria_timed_event = EventStorage("cafeteria", "", cafeteria_after_time_check)
    cafeteria_events = {
        "eat_alone":   EventStorage("eat_alone",   "Eat alone",         cafeteria_eat_fallback),
        "eat_student": EventStorage("eat_student", "Eat with students", cafeteria_eat_fallback),
        "eat_teacher": EventStorage("eat_teacher", "Eat with teacher",  cafeteria_eat_fallback),
        "eat_look":    EventStorage("eat_look",    "Look around",       cafeteria_eat_fallback),
    }

    cafeteria_bg_images = [
        BGImage("images/background/cafeteria/bg 1,6 <level> <nude>.png", 1, TimeCondition(daytime = "1,6")), # show terrace with a few students
        BGImage("images/background/cafeteria/bg 3 <level> <nude>.png", 1, TimeCondition(daytime = 3)), # show terrace full of students and teacher
        BGImage("images/background/cafeteria/bg 7.png", 1, TimeCondition(daytime = 7)), # show empty terrace at night
    ]
    
#######################################

#####################################
# ----- Cafeteria Entry Point ----- #
#####################################

label cafeteria:

    call call_available_event(cafeteria_timed_event) from cafeteria_1

label .after_time_check:

    $ school = get_random_school()

    call show_cafeteria_idle_image(school) from cafeteria_2

    call call_event_menu (
        "What to do at the Cafeteria?",
        1, 
        7, 
        cafeteria_events, 
        cafeteria_fallback,
        character.subtitles,
        school,
    ) from cafeteria_3

    jump cafeteria

label show_cafeteria_idle_image(school):
    $ max_nude, image_path = get_background(
        "images/background/cafeteria/bg c.png", # show empty terrace
        cafeteria_bg_images,
        get_level_for_char(school, charList["schools"]),
    )

    show screen image_with_nude_var (image_path, max_nude)

    return

#####################################

#########################################
# ----- Cafeteria Fallback Events ----- #
#########################################

label cafeteria_fallback:
    subtitles "There is nothing to do here."
    return
label cafeteria_eat_fallback:
    subtitles "I'm not hungry."
    return
label cafeteria_person_fallback:
    subtitles "There is nobody here."
    return
label cafeteria_look_fallback:
    subtitles "There is nothing to see here."
    return

#########################################

################################
# ----- Cafeteria Events ----- #
################################


################################