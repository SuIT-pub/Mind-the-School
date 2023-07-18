#########################################################
# ----- Middle School Dormitory Event Handler ----- #
#########################################################

init -1 python:
    middle_school_dormitory_after_time_check = Event("middle_school_dormitory_after_time_check", "middle_school_dormitory.after_time_check", 2)
    middle_school_dormitory_fallback         = Event("middle_school_dormitory_fallback",         "middle_school_dormitory_fallback",         2)
    middle_school_dormitory_person_fallback  = Event("middle_school_dormitory_person_fallback",  "middle_school_dormitory_person_fallback",  2)

    middle_school_dormitory_timed_event = EventStorage("middle_school_dormitory", "", middle_school_dormitory_after_time_check)
    middle_school_dormitory_events = {
        "check_rooms":   EventStorage("check_rooms",   "Check Rooms",      middle_school_dormitory_person_fallback),
        "talk_students": EventStorage("talk_students", "Talk to students", middle_school_dormitory_person_fallback),
        "patrol":        EventStorage("patrol",        "Patrol building",  middle_school_dormitory_person_fallback),
        "peek_students": EventStorage("peek_students", "Peek on students", middle_school_dormitory_person_fallback),
    }

#######################################################
# ----- Middle School Dormitory Entry Point ----- #
#######################################################

label middle_school_dormitory:
    # show dorm corridor

    # if daytime in [1, 3, 6]:
    #     # show corridor filled with students and open doors
    # if daytime in [2, 4, 5]:
    #     # show empty corridor
    # if daytime in [7]:
    #     # show empty corridor at night

    call call_available_event(middle_school_building_timed_event) from _call_call_available_event_11

label .after_time_check:

    call call_event_menu (
        "What to do in the Middle School Dorm?",
        1, 
        7, 
        middle_school_dormitory_events, 
        middle_school_dormitory_events_title,
        "fallback", "middle_school_dormitory"
    ) from _call_call_event_menu_11

    jump middle_school_dormitory

###########################################################
# ----- Middle School Dormitory Fallback Events ----- #
###########################################################

label middle_school_dormitory_fallback:
    subtitles "There is nothing to do here."
    return

label middle_school_dormitory_person_fallback:
    subtitles "There is nobody here."
    return

##################################################
# ----- Middle School Dormitory Events ----- #
##################################################