##################################
# ----- Labs Event Handler ----- #
##################################

init -1 python:
    labs_timed_event = EventStorage("labs", "", Event(2, "labs.after_time_check"))
    labs_events = {
        "check_chemistry": EventStorage("check_chemistry", "Check chemistry classes", default_fallback, "There is nobody here."),
        "teach_chemistry": EventStorage("teach_chemistry", "Teach chemistry classes", default_fallback, "There is nobody here."),
        "check_biology":   EventStorage("check_biology",   "Check biology classes",   default_fallback, "There is nobody here."),
        "teach_biology":   EventStorage("teach_biology",   "Teach biology classes",   default_fallback, "There is nobody here."),
        "drug_lab":        EventStorage("drug_lab",        "Go to drug lab",          default_fallback, "There is nothing to see here."),
    }



    labs_timed_event.check_all_events()
    map(lambda x: x.check_all_events(), labs_events.values())

    labs_bg_images = [
        BGImage("images/background/labs/bg c <level> <nude>.webp", 1, TimeCondition(daytime = "c")), # show corridor with few students
        BGImage("images/background/labs/bg 7.webp", 1, TimeCondition(daytime = 7)), # show empty corridor at night
    ]
    
##################################

################################
# ----- Labs Entry Point ----- #
################################

label labs ():
    
    call call_available_event(labs_timed_event) from labs_1

label .after_time_check (**kwargs):
    
    $ school_obj = get_random_school()

    call show_idle_image(school_obj, "images/background/labs/bg f.webp", labs_bg_images) from labs_2

    call call_event_menu (
        "What to do at the Labs?", 
        labs_events, 
        default_fallback,
        character.subtitles,
        char_obj = school_obj,
        fallback_text = "There is nothing to see here.",
    ) from labs_3

    jump labs

################################

###########################
# ----- Labs Events ----- #
###########################



###########################