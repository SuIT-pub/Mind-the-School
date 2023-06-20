##################################################
# ----- Elementary School Building Event Handler ----- #
##################################################

init -10 python:
    elementary_school_building_events = {}
    elementary_school_building_events_title = {
        "check_class": "Check Class",
        "teach_class": "Teach a Class",
        "patrol": "Patrol building",
        "students": "Talk to students",
    }

    elementary_school_building_events["fallback"] = "elementary_school_building_fallback"

    # event check before menu
    create_event_area(elementary_school_building_events, "elementary_school_building", "elementary_school_building.after_time_check")

    create_event_area(elementary_school_building_events, "check_class", "elementary_school_building_person_fallback")

    create_event_area(elementary_school_building_events, "teach_class", "elementary_school_building_person_fallback")

    create_event_area(elementary_school_building_events, "patrol", "elementary_school_building_fallback")

    create_event_area(elementary_school_building_events, "students", "elementary_school_building_person_fallback")

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

label .after_time_check:

    call call_event_menu (
        "What to do in the Elementary School?",
        1, 
        7, 
        elementary_school_building_events, 
        elementary_school_building_events_title,
        "fallback", "elementary_school_building"
    )

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