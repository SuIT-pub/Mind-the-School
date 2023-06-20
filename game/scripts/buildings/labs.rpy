#################################
# ----- Labs Event Handler ----- #
#################################

init -10 python:
    labs_events = {}
    labs_events_title = {
        "check_chemistry": "Check chemistry classes",
        "teach_chemistry": "Teach chemistry classes",
        "check_biology": "Check biology classes",
        "teach_biology": "Teach biology classes",
        "drug_lab": "Go to drug lab",
    }

    labs_events["fallback"] = "labs_fallback"

    # event check before menu
    create_event_area(labs_events, "labs", "labs.after_time_check")

###############################
# ----- Labs Entry Point ----- #
###############################

label labs:
    # show labs corridor inside

    # if daytime in [1, 3, 6]:
    #     # show corridor with few students
    # if daytime in [2, 4, 5]:
    #     # show empty corridpr
    # if daytime in [7]:
    #     # show empty corridor at night

    call event_check_area("labs", labs_events)

label .after_time_check:

    call call_event_menu (
        "What to do at the Labs?",
        1, 
        7, 
        labs_events, 
        labs_events_title,
        "fallback", "kiosk"
    )

    $ check_events = [
        get_events_area_count("check_chemistry", labs_events),
        get_events_area_count("teach_chemistry", labs_events),
        get_events_area_count("check_biology"  , labs_events),
        get_events_area_count("teach_biology"  , labs_events),
        get_events_area_count("drug_lab"       , labs_events),
    ]

    if any(check_events):
        menu:
            subtitles "What to do at the Labs?"

            "Check chemistry classes" if check_events[0] > 0:
                call event_check_area("check_chemistry", labs_events)
            "Teach chemistry classes" if check_events[1] > 0:
                call event_check_area("teach_chemistry", labs_events)
            "Check biology classes" if check_events[2] > 0:
                call event_check_area("check_biology", labs_events)
            "Teach biology classes" if check_events[3] > 0:
                call event_check_area("teach_biology", labs_events)
            "Go to drug lab" if check_events[4] > 0:
                call event_check_area("drug_lab", labs_events)
            "Return":
                jump map_overview
    else:
        call labs_fallback
        jump map_overview

    jump labs

###################################
# ----- Labs Fallback Events ----- #
###################################

label labs_fallback:
    subtitles "There is nothing to see here."
    return

label labs_snack_fallback:
    subtitles "I don't want anything."
    return

label labs_person_fallback:
    subtitles "There is nobody here."
    return

##########################
# ----- Labs Events ----- #
##########################