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

    labs_bg_images = [
        BGImage("images/background/labs/bg c <level> <nude>.png", 1, TimeCondition(daytime = "c")), # show corridor with few students
        BGImage("images/background/labs/bg 7.png", 1, TimeCondition(daytime = 7)), # show empty corridor at night
    ]
    
##################################

################################
# ----- Labs Entry Point ----- #
################################

label labs:
    
    call call_available_event(labs_timed_event) from labs_1

label .after_time_check:
    
    $ school = get_random_school()

    call show_labs_idle_image(school) from labs_2

    call call_event_menu (
        "What to do at the Labs?",
        1, 
        7, 
        labs_events, 
        labs_fallback,
        character.subtitles,
        school,
    ) from labs_3

    jump labs

label show_labs_idle_image(school):    
    $ image_path = "images/background/labs/bg f.png" # show empty corridor

    $ max_nude, image_path = get_background(
        "images/background/labs/bg f.png",
        labs_bg_images,
        get_level_for_char(school, charList["schools"]),
    )

    show screen image_with_nude_var (image_path, 0)

    return

################################

####################################
# ----- Labs Fallback Events ----- #
####################################

label labs_fallback:
    subtitles "There is nothing to see here."
    return

label labs_person_fallback:
    subtitles "There is nobody here."
    return

####################################

###########################
# ----- Labs Events ----- #
###########################



###########################