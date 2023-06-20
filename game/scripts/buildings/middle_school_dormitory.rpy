#########################################################
# ----- Middle School Dormitory Event Handler ----- #
#########################################################

init -10 python:
    middle_school_dormitory_events = {}
    middle_school_dormitory_events_title = {
        "check_rooms": "Check Rooms",
        "talk_students": "Talk to students",
        "patrol": "Patrol building",
        "peek_students": "Peek on students",
    }

    middle_school_dormitory_events["fallback"] = "middle_school_dormitory_fallback"

    # event check before menu
    create_event_area(middle_school_dormitory_events, "middle_school_dormitory", "middle_school_dormitory.after_time_check")

    create_event_area(middle_school_dormitory_events, "check_rooms", "middle_school_dormitory_person_fallback")

    create_event_area(middle_school_dormitory_events, "talk", "middle_school_dormitory_person_fallback")

    create_event_area(middle_school_dormitory_events, "patrol", "middle_school_dormitory_person_fallback")

    create_event_area(middle_school_dormitory_events, "peek", "middle_school_dormitory_person_fallback")

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

    call event_check_area("middle_school_dormitory", middle_school_dormitory_events)

label .after_time_check:

    call call_event_menu (
        "What to do in the Middle School Dorm?",
        1, 
        7, 
        middle_school_dormitory_events, 
        middle_school_dormitory_events_title,
        "fallback", "middle_school_dormitory"
    )

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