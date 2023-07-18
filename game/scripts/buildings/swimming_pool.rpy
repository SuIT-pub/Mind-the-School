##########################################
# ----- Swimming Pool Event Handler ----- #
##########################################

init -1 python:
    swimming_pool_after_time_check = Event("swimming_pool_after_time_check", "swimming_pool.after_time_check", 2)
    swimming_pool_fallback         = Event("swimming_pool_fallback",         "swimming_pool_fallback",         2)
    swimming_pool_person_fallback  = Event("swimming_pool_person_fallback",  "swimming_pool_person_fallback",  2)

    swimming_pool_timed_event = EventStorage("swimming_pool", "", swimming_pool_fallback)
    swimming_pool_events = {
        "check_class":    EventStorage("check_class",    "Check on swimming class",      swimming_pool_person_fallback),
        "teach_class":    EventStorage("teach_class",    "Teach a swimming class",       swimming_pool_person_fallback),
        "peek_changing":  EventStorage("peek_changing",  "Peek into the changing rooms", swimming_pool_person_fallback),
        "enter_changing": EventStorage("enter_changing", "Enter changing rooms",         swimming_pool_person_fallback),
        "steal_changing": EventStorage("steal_changing", "Steal some panties",           swimming_pool_person_fallback),
    }

########################################
# ----- Swimming Pool Entry Point ----- #
########################################

label swimming_pool:
    # show swimming pool

    # if daytime in [1]:
    #     # show empty swimming pool
    # if daytime in [2, 4, 5]:
    #     # show swimming pool with students
    # if daytime in [3, 6]:
    #     # show swimming pool with few students
    # if daytime in [7]:
    #     # show swimming pool at night empty

    call call_available_event(swimming_pool_timed_event) from _call_call_available_event_14

label .after_time_check:

    call call_event_menu (
        "What to do at the swimming pool?",
        1, 
        7, 
        swiming_pool_events, 
        swiming_pool_fallback,
    ) from _call_call_event_menu_14

    jump swimming_pool

############################################
# ----- Swimming Pool Fallback Events ----- #
############################################

label swimming_pool_fallback:
    subtitles "There is nothing to see here."
    return

label swimming_pool_person_fallback:
    subtitles "There is nobody here."
    return

###################################
# ----- Swimming Pool Events ----- #
###################################