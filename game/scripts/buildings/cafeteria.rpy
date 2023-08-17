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

#######################################

#####################################
# ----- Cafeteria Entry Point ----- #
#####################################

label cafeteria:
    # show cafeteria terrace

    # if daytime in [1, 6]:
    #     # show terrace with a few students
    # if daytime in [3]:
    #     # show terrace full of students and teacher
    # if daytime in [2, 4, 5]:
    #     # show empty terrace
    # if daytime in [7]
    #     # show empty terrace at night

    call call_available_event(cafeteria_timed_event) from _call_call_available_event_1

label .after_time_check:

    $ school = get_random_school()

    call show_cafeteria_idle_image(school)

    call call_event_menu (
        "What to do at the Cafeteria?",
        1, 
        7, 
        cafeteria_events, 
        cafeteria_fallback,
        character.subtitles,
        school,
    ) from _call_call_event_menu_1

    jump cafeteria

label show_cafeteria_idle_image(school):    
    $ image_path = "images/background/cafeteria/bg c.png"

    if time.check_daytime("1,6"):
        $ image_path = get_image_with_level(
            "images/background/cafeteria/bg 1,6 <level> <nude>.png", 
            get_level_for_char(school, charList["schools"]),
        )
    elif time.check_daytime(3):
        $ image_path = get_image_with_level(
            "images/background/cafeteria/bg 3 <level> <nude>.png", 
            get_level_for_char(school, charList["schools"]),
        )
    elif time.check_daytime(7):
        $ image_path = "images/background/cafeteria/bg 7.png"

    show screen image_with_nude_var (image_path, 0)

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