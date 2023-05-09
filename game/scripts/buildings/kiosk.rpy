#################################
# ----- Kiosk Event Handler ----- #
#################################

init -10 python:
    kiosk_events = {}

    kiosk_events["fallback"] = "kiosk_fallback"

    # event check before menu
    kiosk_events["kiosk"] = {
        "fallback": "kiosk.after_time_check", # no event
    }

    kiosk_events["snack"] = {
        "fallback": "kiosk_snack_fallback",
    }

    kiosk_events["students"] = {
        "fallback": "kiosk_person_fallback",
    }

###############################
# ----- Kiosk Entry Point ----- #
###############################

label kiosk:
    # show kiosk inside

    # if daytime in [1, 3, 6]:
    #     # show kiosk with students
    # if daytime in [2, 4, 5]:
    #     # show kiosk empty
    # if daytime in [7]:
    #     # show kiosk at night empty

    call event_check_area("kiosk", kiosk_events)

label.after_time_check:

    $ check_events = [
        get_events_area_count("snack"   , kiosk_events),
        get_events_area_count("students", kiosk_events),
    ]

    if any(check_events):
        menu:
            Subtitles "What to do at the Kiosk?"

            "Get a snack" if check_events[0] > 0:
                call event_check_area("snack", kiosk_events)
            "Talk to students" if check_events[1] > 0:
                call event_check_area("students", kiosk_events)
            "Return":
                jump map_overview
    else:
        call kiosk_fallback
        jump map_overview

    jump kiosk

###################################
# ----- Kiosk Fallback Events ----- #
###################################

label kiosk_fallback:
    Subtitles "There is nothing to see here."
    return

label kiosk_snack_fallback:
    Subtitles "I don't want anything."
    return

label kiosk_person_fallback:
    Subtitles "There is nobody here."
    return

##########################
# ----- Kiosk Events ----- #
##########################