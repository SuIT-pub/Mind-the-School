##################################
# ----- Labs Event Handler ----- #
##################################

init -1 python:
    labs_after_time_check = Event("labs_after_time_check", "labs.after_time_check", 2)
    labs_fallback         = Event("labs_fallback",         "labs_fallback",         2)
    labs_person_fallback  = Event("labs_person_fallback",  "labs_person_fallback",  2)

    labs_timed_event = EventStorage("labs", "", labs_after_time_check)
    labs_events = {
        "check_chemistry": EventStorage("check_chemistry", "Check chemistry classes", labs_person_fallback),
        "teach_chemistry": EventStorage("teach_chemistry", "Teach chemistry classes", labs_person_fallback),
        "check_biology":   EventStorage("check_biology",   "Check biology classes",   labs_person_fallback),
        "teach_biology":   EventStorage("teach_biology",   "Teach biology classes",   labs_person_fallback),
        "drug_lab":        EventStorage("drug_lab",        "Go to drug lab",          labs_fallback       ),
    }

################################
# ----- Labs Entry Point ----- #
################################

label labs:
    # show labs corridor inside

    # if daytime in [1, 3, 6]:
    #     # show corridor with few students
    # if daytime in [2, 4, 5]:
    #     # show empty corridpr
    # if daytime in [7]:
    #     # show empty corridor at night

    call call_available_event(labs_timed_event) from _call_call_available_event_9

label .after_time_check:

    call call_event_menu (
        "What to do at the Labs?",
        1, 
        7, 
        labs_events, 
        labs_fallback,
    ) from _call_call_event_menu_9

    jump labs

####################################
# ----- Labs Fallback Events ----- #
####################################

label labs_fallback:
    subtitles "There is nothing to see here."
    return

label labs_person_fallback:
    subtitles "There is nobody here."
    return

###########################
# ----- Labs Events ----- #
###########################