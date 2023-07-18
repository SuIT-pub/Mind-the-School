####################################################
# ----- Middle School Building Event Handler ----- #
####################################################

init -1 python:
    middle_school_building_after_time_check = Event("middle_school_building_after_time_check", "middle_school_building.after_time_check", 2)
    middle_school_building_fallback         = Event("middle_school_building_fallback",         "middle_school_building_fallback",         2)
    middle_school_building_person_fallback  = Event("middle_school_building_person_fallback",  "middle_school_building_person_fallback",  2)

    middle_school_building_timed_event = EventStorage("middle_school_building", "", middle_school_building_after_time_check)
    middle_school_building_events = {
        "check_class": EventStorage("check_class", "Check Class",      middle_school_building_person_fallback),
        "teach_class": EventStorage("teach_class", "Teach a Class",    middle_school_building_person_fallback),
        "patrol":      EventStorage("patrol",      "Patrol building",  middle_school_building_person_fallback),
        "students":    EventStorage("strudents",   "Talk to students", middle_school_building_person_fallback),
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

    call call_available_event(middle_school_building_timed_event) from _call_call_available_event_10

label .after_time_check:

    call call_event_menu (
        "What to do in the Middle School?",
        1, 
        7, 
        middle_school_building_events, 
        middle_school_building_fallback
    ) from _call_call_event_menu_10

    jump middle_school_building

######################################################
# ----- Middle School Building Fallback Events ----- #
######################################################

label middle_school_building_fallback:
    subtitles "There is nothing to do here."
    return
label middle_school_building_person_fallback:
    subtitles "There is nobody here."
    return

###########################################
# ----- Middle School Building Events ----- #
###########################################
