#########################################################
# ----- Elementary School Dormitory Event Handler ----- #
#########################################################

init -10 python:
    elementary_school_dormitory_events = {}
    elementary_school_dormitory_events_title = {
        "check_rooms": "Check Rooms",
        "talk_students": "Talk to students",
        "patrol": "Patrol building",
        "peek_students": "Peek on students",
    }

    elementary_school_dormitory_events["fallback"] = "elementary_school_dormitory_fallback"

    # event check before menu
    create_event_area(elementary_school_dormitory_events, "elementary_school_dormitory", "elementary_school_dormitory.after_time_check")

    create_event_area(elementary_school_dormitory_events, "check_rooms", "elementary_school_dormitory_person_fallback")

    create_event_area(elementary_school_dormitory_events, "talk_students", "elementary_school_dormitory_person_fallback")

    create_event_area(elementary_school_dormitory_events, "patrol", "elementary_school_dormitory_person_fallback")

    create_event_area(elementary_school_dormitory_events, "peek", "elementary_school_dormitory_person_fallback")

#######################################################
# ----- Elementary School Dormitory Entry Point ----- #
#######################################################

label elementary_school_dormitory:
    # show dorm corridor

    # if daytime in [1, 3, 6]:
    #     # show corridor filled with students and open doors
    # if daytime in [2, 4, 5]:
    #     # show empty corridor
    # if daytime in [7]:
    #     # show empty corridor at night

    call event_check_area("elementary_school_dormitory", elementary_school_dormitory_events)

label .after_time_check:

    call call_event_menu (
        "What to do in the Elementary School Dorm?",
        1, 
        7, 
        elementary_school_dormitory_events, 
        elementary_school_dormitory_events_title,
        "fallback", "elementary_school_dormitory"
    )

    jump elementary_school_dormitory

###########################################################
# ----- Elementary School Dormitory Fallback Events ----- #
###########################################################

label elementary_school_dormitory_fallback:
    subtitles "There is nothing to do here."
    return

label elementary_school_dormitory_person_fallback:
    subtitles "There is nobody here."
    return

##################################################
# ----- Elementary School Dormitory Events ----- #
##################################################