##########################################
# ----- Sports Field Event Handler ----- #
##########################################

init -10 python:
    sports_field_events = {}
    sports_field_events_title = {
        "check_class": "Check on sport class",
        "teach_class": "Teach a sport class",
        "peek_changing": "Peek into the changing rooms",
        "enter_changing": "Enter changing rooms",
        "steal_changing": "Steal some panties",
    }

    sports_field_events["fallback"] = "sports_field_fallback"

    # event check before menu
    create_event_area(sports_field_events, "sports_field", "sports_field.after_time_check")

    create_event_area(sports_field_events, "check_class", "sports_field_person_fallback")

    create_event_area(sports_field_events, "teach_class", "sports_field_person_fallback")

    create_event_area(sports_field_events, "peek_changing", "sports_field_person_fallback")

    create_event_area(sports_field_events, "enter_changing", "sports_field_person_fallback")

    create_event_area(sports_field_events, "steal", "sports_field_person_fallback")

########################################
# ----- Sports Field Entry Point ----- #
########################################

label sports_field:
    # show sports field

    # if daytime in [1]:
    #     # show empty sports field
    # if daytime in [2, 4, 5]:
    #     # show sports field with students
    # if daytime in [3, 6]:
    #     # show sports field with few students
    # if daytime in [7]:
    #     # show sports field at night empty

    call event_check_area("sports_field", sports_field_events)

label .after_time_check:

    call call_event_menu (
        "What to do on the sports field",
        1, 
        7, 
        sports_field_events, 
        sports_field_events_title,
        "fallback", "sports_field",
    )

    jump sports_field

############################################
# ----- Sports Field Fallback Events ----- #
############################################

label sports_field_fallback:
    subtitles "There is nothing to see here."
    return

label sports_field_person_fallback:
    subtitles "There is nobody here."
    return

###################################
# ----- Sports Field Events ----- #
###################################