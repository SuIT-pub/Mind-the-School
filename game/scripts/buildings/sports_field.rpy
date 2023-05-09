##########################################
# ----- Sports Field Event Handler ----- #
##########################################

init -10 python:
    sports_field_events = {}

    sports_field_events["fallback"] = "sports_field_fallback"

    # event check before menu
    sports_field_events["sports_field"] = {
        "fallback": "sports_field.after_time_check", # no event
    }

    sports_field_events["check_class"] = {
        "fallback": "sports_field_person_fallback",
    }

    sports_field_events["teach_class"] = {
        "fallback": "sports_field_person_fallback",
    }

    sports_field_events["peek_changing"] = {
        "fallback": "sports_field_person_fallback",
    }

    sports_field_events["enter_changing"] = {
        "fallback": "sports_field_person_fallback",
    }

    sports_field_events["steal"] = {
        "fallback": "sports_field_person_fallback",
    }

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

label.after_time_check:

    $ check_events = [
        get_events_area_count("check_class"   , sports_field_events),
        get_events_area_count("teach_class"   , sports_field_events),
        get_events_area_count("peek_changing" , sports_field_events),
        get_events_area_count("enter_changing", sports_field_events),
        get_events_area_count("steal"         , sports_field_events),
    ]

    if any(check_events):
        menu:
            Subtitles "What to do on the sports field?"

            "Check on sport class" if check_events[0] > 0:
                call event_check_area("check_class", sports_field_events)
            "Teach a sport class" if check_events[1] > 0:
                call event_check_area("teach_class", sports_field_events)
            "Take a peek in the changing rooms" if check_events[2] > 0:
                call event_check_area("peek_changing", sports_field_events)
            "Enter the changing rooms" if check_events[3] > 0:
                call event_check_area("enter_changing", sports_field_events)
            "Steal some panties" if check_events[4] > 0:
                call event_check_area("steal", sports_field_events)
            "Return":
                jump map_overview
    else:
        call sports_field_fallback
        jump map_overview

    jump sports_field

############################################
# ----- Sports Field Fallback Events ----- #
############################################

label sports_field_fallback:
    Subtitles "There is nothing to see here."
    return

label sports_field_person_fallback:
    Subtitles "There is nobody here."
    return

###################################
# ----- Sports Field Events ----- #
###################################