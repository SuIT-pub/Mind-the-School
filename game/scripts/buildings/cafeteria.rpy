#######################################
# ----- Cafeteria Event Handler ----- #
#######################################

init -10 python:
    cafeteria_events = {}
    cafeteria_events_title = {
        "eat_alone": "Eat alone",
        "eat_student": "Eat with students",
        "eat_teacher": "Eat with teacher",
        "look": "Look around",
    }

    cafeteria_events["fallback"] = "cafeteria_fallback"

    # event check before menu
    create_event_area(cafeteria_events, "cafeteria", "cafeteria.after_time_check")

    create_event_area(cafeteria_events, "eat_alone", "cafeteria_eat_fallback")

    create_event_area(cafeteria_events, "eat_student", "cafeteria_person_fallback")

    create_event_area(cafeteria_events, "eat_teacher", "cafeteria_person_fallback")

    create_event_area(cafeteria_events, "look", "cafeteria_look_fallback")

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

    call event_check_area("cafeteria", cafeteria_events)

label .after_time_check:

    call call_event_menu (
        "What to do at the Cafeteria?",
        1, 
        7, 
        cafeteria_events, 
        cafeteria_events_title,
        "fallback", "cafeteria"
    )

    jump cafeteria

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

################################
# ----- Cafeteria Events ----- #
################################