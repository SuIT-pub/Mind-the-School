##################################################
# ----- Elementary School Building Event Handler ----- #
##################################################

init -10 python:
    elementary_school_building_events = {}

    elementary_school_building_events["fallback"] = "elementary_school_building_fallback"

    # event check before menu
    elementary_school_building_events["elementary_school_building"] = {
        "fallback": "elementary_school_building.after_time_check", # no event
    }

    elementary_school_building_events["check_class"] = {
        "fallback": "elementary_school_building_person_fallback",
    }

    elementary_school_building_events["teach_class"] = {
        "fallback": "elementary_school_building_person_fallback",
    }

    elementary_school_building_events["patrol"] = {
        "fallback": "elementary_school_building_fallback",
    }

    elementary_school_building_events["students"] = {
        "fallback": "elementary_school_building_person_fallback",
    }

################################################
# ----- Elementary School Building Entry Point ----- #
################################################

label elementary_school_building:
    # show school corridor

    # if daytime in [1, 3, 6]:
    #     # show corridor filled with students
    # if daytime in [2, 4, 5]:
    #     # show empty corridor
    # if daytime in [7]:
    #     # show empty corridor at night

    call event_check_area("elementary_school_building", elementary_school_building_events)

label.after_time_check:

    $ check_events = [
        get_events_area_count("check_class", elementary_school_building_events),
        get_events_area_count("teach_class", elementary_school_building_events),
        get_events_area_count("patrol"     , elementary_school_building_events),
        get_events_area_count("students"   , elementary_school_building_events),
    ]

    if any(check_events):
        menu:
            Subtitles "What to do in the Elementary School?"

            "Check class" if check_events[0] > 0:
                call event_check_area("check_class", elementary_school_building_events)
            "Teach class" if check_events[1] > 0:
                call event_check_area("teach_class", elementary_school_building_events)
            "Patrol building" if check_events[2] > 0:
                call event_check_area("patrol", elementary_school_building_events)
            "Talk to students" if check_events[3] > 0:
                call event_check_area("students", elementary_school_building_events)
            "Return":
                jump map_overview
    else:
        call elementary_school_building_fallback
        jump map_overview

    jump elementary_school_building

####################################################
# ----- Elementary School Building Fallback Events ----- #
####################################################

label elementary_school_building_fallback:
    Subtitles "There is nothing to do here."
    return
label elementary_school_building_person_fallback:
    Subtitles "There is nobody here."
    return

###########################################
# ----- Elementary School Building Events ----- #
###########################################