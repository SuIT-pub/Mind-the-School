##########################################
# ----- Tennis Court Event Handler ----- #
##########################################

init -10 python:
    tennis_court_events = {}
    tennis_court_events_title = {
        "check_class": "Check on tennis class",
        "teach_class": "Teach a tennis class",
        "peek_changing": "Peek into the changing rooms",
        "enter_changing": "Enter changing rooms",
        "steal_changing": "Steal some panties",
    }

    tennis_court_events["fallback"] = "tennis_court_fallback"

    # event check before menu
    create_event_area(tennis_court_events, "tennis_court", "tennis_court.after_time_check")

    create_event_area(tennis_court_events, "check_class", "tennis_court_person_fallback")

    create_event_area(tennis_court_events, "teach_class", "tennis_court_person_fallback")

    create_event_area(tennis_court_events, "peek_changing", "tennis_court_person_fallback")

    create_event_area(tennis_court_events, "enter_changing", "tennis_court_person_fallback")

    create_event_area(tennis_court_events, "steal", "tennis_court_person_fallback")

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

label .after_time_check:

    call call_event_menu (
        "What to do at the tennis court?",
        1, 
        7, 
        tennis_court_events, 
        tennis_court_events_title,
        "fallback", "tennis_court",
    )

    jump tennis_court

############################################
# ----- Tennis Court Fallback Events ----- #
############################################

label tennis_court_fallback:
    subtitles "There is nothing to see here."
    return

label tennis_court_person_fallback:
    subtitles "There is nobody here."
    return

###################################
# ----- Tennis Court Events ----- #
###################################