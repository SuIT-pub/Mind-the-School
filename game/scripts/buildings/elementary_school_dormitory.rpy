#########################################################
# ----- Elementary School Dormitory Event Handler ----- #
#########################################################

init -10 python:
    elementary_school_dormitory_events = {}

    elementary_school_dormitory_events["fallback"] = "elementary_school_dormitory_fallback"

    # event check before menu
    elementary_school_dormitory_events["elementary_school_dormitory"] = {
        "fallback": "elementary_school_dormitory.after_time_check", # no event
    }

    elementary_school_dormitory_events["check_rooms"] = {
        "fallback": "elementary_school_dormitory_person_fallback",
    }

    elementary_school_dormitory_events["talk"] = {
        "fallback": "elementary_school_dormitory_person_fallback",
    }

    elementary_school_dormitory_events["patrol"] = {
        "fallback": "elementary_school_dormitory_person_fallback",
    }

    elementary_school_dormitory_events["peek"] = {
        "fallback": "elementary_school_dormitory_person_fallback",
    }

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

label.after_time_check:

    $ check_events = [
        get_events_area_count("check_rooms", elementary_school_dormitory_events),
        get_events_area_count("talk"       , elementary_school_dormitory_events),
        get_events_area_count("patrol"     , elementary_school_dormitory_events),
        get_events_area_count("peek"       , elementary_school_dormitory_events),
    ]

    if any(check_events):
        menu:
            Subtitles "What to do in the Elementary School Dorm?"
            
            "Check rooms" if check_events[0] > 0:
                call event_check_area("check_rooms", elementary_school_dormitory_events)
            "Talk to students" if check_events[1] > 0:
                call event_check_area("talk", elementary_school_dormitory_events)
            "Patrol building" if check_events[2] > 0:
                call event_check_area("patrol", elementary_school_dormitory_events)
            "Peek on students" if check_events[3] > 0:
                call event_check_area("peek", elementary_school_dormitory_events)
            "Return":
                jump map_overview
    else:
        call elementary_school_building_fallback
        jump map_overview

    jump elementary_school_dormitory

###########################################################
# ----- Elementary School Dormitory Fallback Events ----- #
###########################################################

label elementary_school_dormitory_fallback:
    Subtitles "There is nothing to do here."
    return

label elementary_school_dormitory_person_fallback:
    Subtitles "There is nobody here."
    return

##################################################
# ----- Elementary School Dormitory Events ----- #
##################################################