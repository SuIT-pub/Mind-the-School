####################################################
# ----- Middle School Building Event Handler ----- #
####################################################

init -10 python:
    middle_school_building_events = {}

    middle_school_building_events["fallback"] = "middle_school_building_fallback"

    # event check before menu
    middle_school_building_events["middle_school_building"] = {
        "fallback": "middle_school_building.after_time_check", # no event
    }

    middle_school_building_events["check_class"] = {
        "fallback": "middle_school_building_person_fallback",
    }

    middle_school_building_events["teach_class"] = {
        "fallback": "middle_school_building_person_fallback",
    }

    middle_school_building_events["patrol"] = {
        "fallback": "middle_school_building_fallback",
    }

    middle_school_building_events["students"] = {
        "fallback": "middle_school_building_person_fallback",
    }

##################################################
# ----- Middle School Building Entry Point ----- #
##################################################

label middle_school_building:
    # show school corridor

    # if daytime in [1, 3, 6]:
    #     # show corridor filled with students
    # if daytime in [2, 4, 5]:
    #     # show empty corridor
    # if daytime in [7]:
    #     # show empty corridor at night

    call event_check_area("middle_school_building", middle_school_building_events)

label.after_time_check:

    $ check_events = [
        get_events_area_count("check_class", middle_school_building_events),
        get_events_area_count("teach_class", middle_school_building_events),
        get_events_area_count("patrol"     , middle_school_building_events),
        get_events_area_count("students"   , middle_school_building_events),
    ]

    if any(check_events):
        menu:
            Subtitles "What to do in the Middle School?"

            "Check class" if check_events[0] > 0:
                call event_check_area("check_class", middle_school_building_events)
            "Teach class" if check_events[1] > 0:
                call event_check_area("teach_class", middle_school_building_events)
            "Patrol building" if check_events[2] > 0:
                call event_check_area("patrol", middle_school_building_events)
            "Talk to students" if check_events[3] > 0:
                call event_check_area("students", middle_school_building_events)
            "Return":
                jump map_overview
    else:
        call middle_school_building_fallback
        jump map_overview

    jump middle_school_building

######################################################
# ----- Middle School Building Fallback Events ----- #
######################################################

label middle_school_building_fallback:
    Subtitles "There is nothing to do here."
    return
label middle_school_building_person_fallback:
    Subtitles "There is nobody here."
    return

###########################################
# ----- Middle School Building Events ----- #
###########################################
