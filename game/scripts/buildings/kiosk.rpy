###################################
# ----- Kiosk Event Handler ----- #
###################################

init -10 python:
    kiosk_events = {}
    kiosk_events_title = {
        "snack": "Get a snack",
        "students": "Talk to students",
    }

    kiosk_events["fallback"] = "kiosk_fallback"

    # event check before menu
    create_event_area(kiosk_events, "kiosk", "kiosk.after_time_check")

    create_event_area(kiosk_events, "snack", "kiosk_snack_fallback")

    create_event_area(kiosk_events, "students", "kiosk_person_fallback")

#################################
# ----- Kiosk Entry Point ----- #
#################################

label kiosk:
    # show kiosk inside

    # if daytime in [1, 3, 6]:
    #     # show kiosk with students
    # if daytime in [2, 4, 5]:
    #     # show kiosk empty
    # if daytime in [7]:
    #     # show kiosk at night empty

    call event_check_area("kiosk", kiosk_events)

label .after_time_check:

    call call_event_menu (
        "What to do at the Kiosk?",
        1, 
        7, 
        kiosk_events, 
        kiosk_events_title,
        "fallback", "kiosk"
    )

    jump kiosk

#####################################
# ----- Kiosk Fallback Events ----- #
#####################################

label kiosk_fallback:
    subtitles "There is nothing to see here."
    return

label kiosk_snack_fallback:
    subtitles "I don't want anything."
    return

label kiosk_person_fallback:
    subtitles "There is nobody here."
    return

############################
# ----- Kiosk Events ----- #
############################