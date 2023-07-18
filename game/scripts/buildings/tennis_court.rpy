##########################################
# ----- Tennis Court Event Handler ----- #
##########################################

init -1 python:
    tennis_court_after_time_check = Event("tennis_court_after_time_check", "tennis_court.after_time_check", 2)
    tennis_court_fallback         = Event("tennis_court_fallback",         "tennis_court_fallback",         2)
    tennis_court_person_fallback  = Event("tennis_court_person_fallback",  "tennis_court_person_fallback",  2)

    tennis_court_timed_event = EventStorage("tennis_court", "", tennis_court_fallback)
    tennis_court_events = {
        "check_class":    EventStorage("check_class",    "Check on tennis class",        tennis_court_fallback),
        "teach_class":    EventStorage("teach_class",    "Teach a tennis class",         tennis_court_fallback),
        "peek_changing":  EventStorage("peek_changing",  "Peek into the changing rooms", tennis_court_fallback),
        "enter_changing": EventStorage("enter_changing", "Enter changing rooms",         tennis_court_fallback),
        "steal_changing": EventStorage("steal_changing", "Steal some panties",           tennis_court_fallback),
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

    call call_available_event(tennis_court_timed_event) from _call_call_available_event_15

label .after_time_check:

    call call_event_menu (
        "What to do at the tennis court?",
        1, 
        7, 
        tennis_court_events, 
        tennis_court_fallback,
    ) from _call_call_event_menu_15

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