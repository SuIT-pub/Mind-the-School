###################################
# ----- Kiosk Event Handler ----- #
###################################

init -1 python:
    kiosk_after_time_check = Event("kiosk_after_time_check", "kiosk.after_time_check", 2)
    kiosk_fallback         = Event("kiosk_fallback",         "kiosk_fallback",         2)
    kiosk_snack_fallback   = Event("kiosk_snack_fallback",   "kiosk_snack_fallback",   2)
    kiosk_person_fallback  = Event("kiosk_person_fallback",  "kiosk_person_fallback",  2)

    kiosk_timed_event = EventStorage("kiosk", "", kiosk_after_time_check)
    kiosk_events = {
        "snack":    EventStorage("snack",    "Get a snack",      kiosk_snack_fallback ),
        "students": EventStorage("students", "Talk to students", kiosk_person_fallback),
    }
    
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

    call call_available_event(kiosk_timed_event) from _call_call_available_event_8

label .after_time_check:

    call call_event_menu (
        "What to do at the Kiosk?",
        1, 
        7, 
        kiosk_events, 
        kiosk_events_fallback,
    ) from _call_call_event_menu_8

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