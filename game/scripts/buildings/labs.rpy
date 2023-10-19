##################################
# ----- Labs Event Handler ----- #
##################################

init -1 python:
    labs_after_time_check = Event(2, "labs.after_time_check")
    labs_fallback         = Event(2, "labs_fallback")
    labs_person_fallback  = Event(2, "labs_person_fallback")

    labs_timed_event = EventStorage("labs", "", labs_after_time_check)
    labs_events = {
        "check_chemistry": EventStorage("check_chemistry", "Check chemistry classes", labs_person_fallback),
        "teach_chemistry": EventStorage("teach_chemistry", "Teach chemistry classes", labs_person_fallback),
        "check_biology":   EventStorage("check_biology",   "Check biology classes",   labs_person_fallback),
        "teach_biology":   EventStorage("teach_biology",   "Teach biology classes",   labs_person_fallback),
        "drug_lab":        EventStorage("drug_lab",        "Go to drug lab",          labs_fallback       ),
    }



    labs_timed_event.check_all_events()
    map(lambda x: x.check_all_events(), labs_events.values())

    labs_bg_images = [
        BGImage("images/background/labs/bg c <level> <nude>.jpg", 1, TimeCondition(daytime = "c")), # show corridor with few students
        BGImage("images/background/labs/bg 7.jpg", 1, TimeCondition(daytime = 7)), # show empty corridor at night
    ]
    
##################################

################################
# ----- Labs Entry Point ----- #
################################

label labs ():
    
    call call_available_event(labs_timed_event) from labs_1

label .after_time_check (**kwargs):
    
    $ school_obj = get_random_school()

    call show_labs_idle_image(school_obj) from labs_2

    call call_event_menu (
        "What to do at the Labs?", 
        labs_events, 
        labs_fallback,
        character.subtitles,
        char_obj = school_obj,
    ) from labs_3

    jump labs

label show_labs_idle_image(school):    
    $ image_path = "images/background/labs/bg f.jpg" # show empty corridor

    $ max_nude, image_path = get_background(
        "images/background/labs/bg f.jpg",
        labs_bg_images,
        school_obj,
    )

    call show_image_with_nude_var (image_path, 0) from _call_show_image_with_nude_var_9
    return

################################

####################################
# ----- Labs Fallback Events ----- #
####################################

label labs_fallback (**kwargs):
    subtitles "There is nothing to see here."
    jump map_overview

label labs_person_fallback (**kwargs):
    subtitles "There is nobody here."
    jump map_overview

####################################

###########################
# ----- Labs Events ----- #
###########################



###########################