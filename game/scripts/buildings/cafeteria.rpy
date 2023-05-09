#######################################
# ----- Cafeteria Event Handler ----- #
#######################################

init -10 python:
    cafeteria_events = {}

    cafeteria_events["fallback"] = "cafeteria_fallback"

    # event check before menu
    cafeteria_events["cafeteria"] = {
        "fallback": "cafeteria.after_time_check", # no event
    }

    cafeteria_events["eat_alone"] = {
        "fallback": "cafeteria_eat_fallback",
    }

    cafeteria_events["eat_student"] = {
        "fallback": "cafeteria_person_fallback",
    }

    cafeteria_events["eat_teacher"] = {
        "fallback": "cafeteria_person_fallback",
    }

    cafeteria_events["look"] = {
        "fallback": "cafeteria_look_fallback",
    }

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

label.after_time_check:

    $ check_events = [
        get_events_area_count("eat_alone"  , cafeteria_events),
        get_events_area_count("eat_student", cafeteria_events),
        get_events_area_count("eat_teacher", cafeteria_events),
        get_events_area_count("look"       , cafeteria_events),
    ]

    if any(check_events):
        menu:
            Subtitles "What to do at the cafeteria?"
            
            "Eat alone" if check_events[0] > 0:
                call event_check_area("eat_alone", cafeteria_events)
            "Eat with students" if check_events[1] > 0:
                call event_check_area("eat_student", cafeteria_events)
            "Eat with teacher" if check_events[2] > 0:
                call event_check_area("eat_teacher", cafeteria_events)
            "Look around" if check_events[3] > 0:
                call event_check_area("look", cafeteria_events)
            "Return":
                jump map_overview
    else:
        call cafeteria_fallback
        jump map_overview

    jump cafeteria

#########################################
# ----- Cafeteria Fallback Events ----- #
#########################################

label cafeteria_fallback:
    Subtitles "There is nothing to do here."
    return
label cafeteria_eat_fallback:
    Subtitles "I'm not hungry."
    return
label cafeteria_person_fallback:
    Subtitles "There is nobody here."
    return
label cafeteria_look_fallback:
    Subtitles "There is nothing to see here."
    return

################################
# ----- Cafeteria Events ----- #
################################