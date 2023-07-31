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
    
    kiosk_timed_event.add_event(Event(
        "first_week_event",
        ["first_week_kiosk_event"],
        1,
        TimeCondition(week = 1),
    ))

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

# first week event
label first_week_kiosk_event:
    principal_thought "Now, somewhere here should be the kiosk..."
    principal_thought "Hmm, why is it so crowded?"
    principal "Excuse me, did something happen? Why is it so crowded here?"
    sgirl "What do you mean? It's always this full. We can't get food anywhere else than here."
    principal "Oh I understand... Thanks."
    principal_thought "This is not acceptable. Did the former headmaster really close the cafeteria?"
    principal_thought "That can't be right..."

    $ change_stat_for_all("reputation", -2)

    $ set_building_blocked("kiosk")

    jump new_day
