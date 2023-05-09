#########################################################
# ----- Middle School Dormitory Event Handler ----- #
#########################################################

init -10 python:
    middle_school_dormitory_events = {}

    middle_school_dormitory_events["fallback"] = "middle_school_dormitory_fallback"

    # event check before menu
    middle_school_dormitory_events["middle_school_dormitory"] = {
        "fallback": "middle_school_dormitory.after_time_check", # no event
    }

    middle_school_dormitory_events["check_rooms"] = {
        "fallback": "middle_school_dormitory_person_fallback",
    }

    middle_school_dormitory_events["talk"] = {
        "fallback": "middle_school_dormitory_person_fallback",
    }

    middle_school_dormitory_events["patrol"] = {
        "fallback": "middle_school_dormitory_person_fallback",
    }

    middle_school_dormitory_events["peek"] = {
        "fallback": "middle_school_dormitory_person_fallback",
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

    call event_check_area("middle_school_dormitory", middle_school_dormitory_events)

label.after_time_check:

    $ check_events = [
        get_events_area_count("check_rooms", middle_school_dormitory_events),
        get_events_area_count("talk"       , middle_school_dormitory_events),
        get_events_area_count("patrol"     , middle_school_dormitory_events),
        get_events_area_count("peek"       , middle_school_dormitory_events),
    ]

    if any(check_events):
        menu:
            Subtitles "What to do in the Middle School Dorm?"
            
            "Check rooms" if check_events[0] > 0:
                call event_check_area("check_rooms", middle_school_dormitory_events)
            "Talk to students" if check_events[1] > 0:
                call event_check_area("talk", middle_school_dormitory_events)
            "Patrol building" if check_events[2] > 0:
                call event_check_area("patrol", middle_school_dormitory_events)
            "Peek on students" if check_events[3] > 0:
                call event_check_area("peek", middle_school_dormitory_events)
            "Return":
                jump map_overview
    else:
        call middle_school_building_fallback
        jump map_overview

    jump middle_school_dormitory

###########################################################
# ----- Middle School Dormitory Fallback Events ----- #
###########################################################

label middle_school_dormitory_fallback:
    Subtitles "There is nothing to do here."
    return

label middle_school_dormitory_person_fallback:
    Subtitles "There is nobody here."
    return

##################################################
# ----- Middle School Dormitory Events ----- #
##################################################