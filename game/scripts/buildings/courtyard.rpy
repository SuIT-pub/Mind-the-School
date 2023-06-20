#######################################
# ----- Courtyard Event Handler ----- #
#######################################

init -10 python:
    courtyard_events = {}
    courtyard_events_title = {
        "talk_student": "Talk with students",
        "talk_teacher": "Talk with teacher",
        "patrol": "Patrol",
    }

    courtyard_events["fallback"] = "courtyard_fallback"

    # event check before menu
    create_event_area(courtyard_events, "courtyard", "courtyard.after_time_check")

    create_event_area(courtyard_events, "talk_student", "courtyard_person_fallback")

    create_event_area(courtyard_events, "talk_teacher", "courtyard_person_fallback")

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

label .after_time_check:

    call call_event_menu (
        "What to do at the Courtyard?",
        1, 
        7, 
        courtyard_events, 
        courtyard_events_title,
        "fallback", "courtyard"
    )

    jump courtyard

#########################################
# ----- Courtyard Fallback Events ----- #
#########################################

label courtyard_fallback:
    subtitles "There is nothing to see here."
    return
label courtyard_person_fallback:
    subtitles "There is nobody here."
    return

################################
# ----- Courtyard Events ----- #
################################