##################################
# ----- Bath Event Handler ----- #
##################################

init -10 python:
    bath_events = {}
    bath_events_title = {
        "male_enter": "Enter the male bath",
        "female_enter": "Enter the female bath",
        "female_peek": "Peek into the female bath",
        "mixed_enter": "Enter the mixed bath",
        "mixed_peek": "Peek into the mixed bath",
    }

    bath_events["fallback"] = "bath_fallback"



    # event check before menu
    create_event_area(bath_events, "bath", "bath.after_time_check")

    create_event_area(bath_events, "male_enter", "bath_enter_fallback")

    create_event_area(bath_events, "female_enter", "bath_enter_fallback")

    create_event_area(bath_events, "female_peek", "bath_peek_fallback")

    create_event_area(bath_events, "mixed_enter", "bath_enter_fallback")

    create_event_area(bath_events, "mixed_peek", "bath_peek_fallback")


###############################
# ----- Kiosk Entry Point ----- #
###############################

label bath:
    # show bath inside

    # if daytime in [1, 3]:
    #     # show bath with students
    # if daytime in [6]:
    #     # show bath with students and/or teacher
    # if daytime in [2, 4, 5]:
    #     # show bath empty
    # if daytime in [7]:
    #     # show bath at night empty or with teachers

    call event_check_area("bath", bath_events)

label .after_time_check:

    call call_event_menu (
        "What to do in the Bath?",
        1, 
        7, 
        bath_events, 
        bath_events_title,
        "fallback", "bath"
    )

    jump bath

####################################
# ----- Bath Fallback Events ----- #
####################################

label bath_fallback:
    subtitles "There is nothing to see here."
    return

label bath_peek_fallback:
    subtitles "There is nobody here."
    return

label bath_enter_fallback:
    subtitles "I don't want to take a bath."
    return

###########################
# ----- Bath Events ----- #
###########################