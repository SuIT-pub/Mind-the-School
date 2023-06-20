##########################################
# ----- Swimming Pool Event Handler ----- #
##########################################

init -10 python:
    swimming_pool_events = {}
    swimming_pool_events_title = {
        "check_class": "Check on swimming class",
        "teach_class": "Teach a swimming class",
        "peek_changing": "Peek into the changing rooms",
        "enter_changing": "Enter changing rooms",
        "steal_changing": "Steal some panties",
    }

    swimming_pool_events["fallback"] = "swimming_pool_fallback"

    # event check before menu
    create_event_area(swimming_pool_events, "swimming_pool", "swimming_pool.after_time_check")

    create_event_area(swimming_pool_events, "check_class", "swimming_pool_person_fallback")

    create_event_area(swimming_pool_events, "teach_class", "swimming_pool_person_fallback")

    create_event_area(swimming_pool_events, "peek_changing", "swimming_pool_person_fallback")

    create_event_area(swimming_pool_events, "enter_changing", "swimming_pool_person_fallback")

    create_event_area(swimming_pool_events, "steal", "swimming_pool_person_fallback")

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

    call event_check_area("swimming_pool", swimming_pool_events)

label .after_time_check:

    call call_event_menu (
        "What to do at the swimming pool?",
        1, 
        7, 
        swiming_pool_events, 
        swiming_pool_events_title,
        "fallback", "swimming_pool",
    )

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