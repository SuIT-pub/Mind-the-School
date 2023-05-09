#######################################
# ----- Courtyard Event Handler ----- #
#######################################

init -10 python:
    courtyard_events = {}

    courtyard_events["fallback"] = "courtyard_fallback"

    # event check before menu
    courtyard_events["courtyard"] = {
        "fallback": "courtyard.after_time_check", # no event
    }

    courtyard_events["talk_student"] = {
        "fallback": "courtyard_person_fallback",
    }

    courtyard_events["talk_teacher"] = {
        "fallback": "courtyard_person_fallback",
    }

#####################################
# ----- Courtyard Entry Point ----- #
#####################################

label courtyard:
    # show courtyard overview

    # if daytime in [1, 6]:
    #     # show courtyard with a few students
    # if daytime in [3]:
    #     # show courtyard full of students and teacher
    # if daytime in [2, 4, 5]:
    #     # show empty courtyard
    # if daytime in [7]
    #     # show empty courtyard at night

    call event_check_area("courtyard", courtyard_events)

label.after_time_check:

    $ check_events = [
        get_events_area_count("talk_student", courtyard_events),
        get_events_area_count("talk_teacher", courtyard_events),
        get_events_area_count("patrol"      , courtyard_events),
    ]

    if any(check_events):
        menu:
            Subtitles "What to do at the Courtyard?"
            
            "Talk with students" if check_events[0] > 0:
                call event_check_area("talk_student", courtyard_events)
            "Talk with teacher" if check_events[1]  >0:
                call event_check_area("talk_teacher", courtyard_events)
            "Patrol" if check_events[2] > 0:
                call event_check_area("patrol", courtyard_events)
            "Return":
                jump map_overview
    else:
        call courtyard_fallback
        jump map_overview

    jump courtyard

#########################################
# ----- Courtyard Fallback Events ----- #
#########################################

label courtyard_fallback:
    Subtitles "There is nothing to see here."
    return
label courtyard_person_fallback:
    Subtitles "There is nobody here."
    return

################################
# ----- Courtyard Events ----- #
################################