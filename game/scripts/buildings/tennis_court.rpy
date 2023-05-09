##########################################
# ----- Tennis Court Event Handler ----- #
##########################################

init -10 python:
    tennis_court_events = {}

    tennis_court_events["fallback"] = "tennis_court_fallback"

    # event check before menu
    tennis_court_events["tennis_court"] = {
        "fallback": "tennis_court.after_time_check", # no event
    }

    tennis_court_events["check_class"] = {
        "fallback": "tennis_court_person_fallback",
    }

    tennis_court_events["teach_class"] = {
        "fallback": "tennis_court_person_fallback",
    }

    tennis_court_events["peek_changing"] = {
        "fallback": "tennis_court_person_fallback",
    }

    tennis_court_events["enter_changing"] = {
        "fallback": "tennis_court_person_fallback",
    }

    tennis_court_events["steal"] = {
        "fallback": "tennis_court_person_fallback",
    }

########################################
# ----- Tennis Court Entry Point ----- #
########################################

label tennis_court:
    # show tennis court

    # if daytime in [1]:
    #     # show empty tennis court
    # if daytime in [2, 4, 5]:
    #     # show tennis court with students
    # if daytime in [3, 6]:
    #     # show tennis court with few students
    # if daytime in [7]:
    #     # show tennis court at night empty

    call event_check_area("tennis_court", tennis_court_events)

label.after_time_check:

    $ check_events = [
        get_events_area_count("check_class"   , tennis_court_events),
        get_events_area_count("teach_class"   , tennis_court_events),
        get_events_area_count("peek_changing" , tennis_court_events),
        get_events_area_count("enter_changing", tennis_court_events),
        get_events_area_count("steal"         , tennis_court_events),
    ]

    if any(check_events):
        menu:
            Subtitles "What to do on the sports field?"

            "Check on sports class" if check_events[0] > 0:
                call event_check_area("check_class", tennis_court_events)
            "Teach a sports class" if check_events[1] > 0:
                call event_check_area("teach_class", tennis_court_events)
            "Take a peek in the changing rooms" if check_events[2] > 0:
                call event_check_area("peek_changing", tennis_court_events)
            "Enter the changing rooms" if check_events[3] > 0:
                call event_check_area("enter_changing", tennis_court_events)
            "Steal some panties" if check_events[4] > 0:
                call event_check_area("steal", tennis_court_events)
            "Return":
                jump map_overview
    else:
        call tennis_court_fallback
        jump map_overview

    jump tennis_court

############################################
# ----- Tennis Court Fallback Events ----- #
############################################

label tennis_court_fallback:
    Subtitles "There is nothing to see here."
    return

label tennis_court_person_fallback:
    Subtitles "There is nobody here."
    return

###################################
# ----- Tennis Court Events ----- #
###################################