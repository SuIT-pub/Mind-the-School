#######################################
# ----- Courtyard Event Handler ----- #
#######################################

init -1 python:
    courtyard_after_time_check = Event("courtyard_after_time_check", "courtyard.after_time_check", 2)
    courtyard_fallback         = Event("courtyard_fallback",         "courtyard_fallback",         2)
    courtyard_person_fallback  = Event("courtyard_person_fallback",  "courtyard_person_fallback",  2)

    courtyard_timed_event = EventStorage("courtyard", "", courtyard_after_time_check)
    courtyard_events = {
        "talk_student": EventStorage("talk_student", "Talk with students", courtyard_person_fallback),
        "talk_teacher": EventStorage("talk_teacher", "Talk with teacher",  courtyard_person_fallback),
        "patrol":       EventStorage("patrol",       "Patrol",             courtyard_person_fallback),
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

    call call_available_event(courtyard_timed_event) from _call_call_available_event_2

label .after_time_check:

    call call_event_menu (
        "What to do at the Courtyard?",
        1, 
        7, 
        courtyard_events, 
        courtyard_fallback,
    ) from _call_call_event_menu_2

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