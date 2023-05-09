##########################################
# ----- Swimming Pool Event Handler ----- #
##########################################

init -10 python:
    swimming_pool_events = {}

    swimming_pool_events["fallback"] = "swimming_pool_fallback"

    # event check before menu
    swimming_pool_events["swimming_pool"] = {
        "fallback": "swimming_pool.after_time_check", # no event
    }

    swimming_pool_events["check_class"] = {
        "fallback": "swimming_pool_person_fallback",
    }

    swimming_pool_events["teach_class"] = {
        "fallback": "swimming_pool_person_fallback",
    }

    swimming_pool_events["peek_changing"] = {
        "fallback": "swimming_pool_person_fallback",
    }

    swimming_pool_events["enter_changing"] = {
        "fallback": "swimming_pool_person_fallback",
    }

    swimming_pool_events["steal"] = {
        "fallback": "swimming_pool_person_fallback",
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

    call event_check_area("swimming_pool", swimming_pool_events)

label.after_time_check:

    $ check_events = [
        get_events_area_count("check_class"   , swimming_pool_events),
        get_events_area_count("teach_class"   , swimming_pool_events),
        get_events_area_count("peek_changing" , swimming_pool_events),
        get_events_area_count("enter_changing", swimming_pool_events),
        get_events_area_count("steal"         , swimming_pool_events),
    ]

    if any(check_events):
        menu:
            Subtitles "What to do on the sports field?"

            "Check on swimming class" if check_events[0] > 0:
                call event_check_area("check_class", swimming_pool_events)
            "Teach a swimming class" if check_events[1] > 0:
                call event_check_area("teach_class", swimming_pool_events)
            "Take a peek in the changing rooms" if check_events[2] > 0:
                call event_check_area("peek_changing", swimming_pool_events)
            "Enter the changing rooms" if check_events[3] > 0:
                call event_check_area("enter_changing", swimming_pool_events)
            "Steal some panties" if check_events[4] > 0:
                call event_check_area("steal", swimming_pool_events)
            "Return":
                jump map_overview
    else:
        call swimming_pool_fallback
        jump map_overview

    jump swimming_pool

############################################
# ----- Swimming Pool Fallback Events ----- #
############################################

label swimming_pool_fallback:
    Subtitles "There is nothing to see here."
    return

label swimming_pool_person_fallback:
    Subtitles "There is nobody here."
    return

###################################
# ----- Swimming Pool Events ----- #
###################################