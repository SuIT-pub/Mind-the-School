##################################################
# ----- Elementary School Building Event Handler ----- #
##################################################

init -1 python:
    elementary_school_building_after_time_check = Event("elementary_school_building_after_time_check", "elementary_school_building.after_time_check", 2)
    elementary_school_building_fallback         = Event("elementary_school_building_fallback",         "elementary_school_building_fallback",         2)
    elementary_school_building_person_fallback  = Event("elementary_school_building_person_fallback",  "elementary_school_building_person_fallback",  2)

    elementary_school_building_timed_event = EventStorage("elementary_school_building", "", elementary_school_building_after_time_check)
    elementary_school_building_events = {
        "check_class": EventStorage("check_class", "Check Class",      elementary_school_building_person_fallback),
        "teach_class": EventStorage("teach_class", "Teach a Class",    elementary_school_building_person_fallback),
        "patrol":      EventStorage("patrol",      "Patrol building",  elementary_school_building_person_fallback),
        "students":    EventStorage("strudents",   "Talk to students", elementary_school_building_person_fallback),
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

    call call_available_event(elementary_school_building_timed_event) from _call_call_available_event_3

label .after_time_check:

    call call_event_menu (
        "What to do in the Elementary School?",
        1, 
        7, 
        elementary_school_building_events, 
        elementary_school_building_fallback,
    ) from _call_call_event_menu_3

    jump elementary_school_building

####################################################
# ----- Elementary School Building Fallback Events ----- #
####################################################

label elementary_school_building_fallback:
    subtitles "There is nothing to do here."
    return
label elementary_school_building_person_fallback:
    subtitles "There is nobody here."
    return

###########################################
# ----- Elementary School Building Events ----- #
###########################################