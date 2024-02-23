##################################
# ----- Labs Event Handler ----- #
##################################

init -1 python:
    labs_timed_event = TempEventStorage("labs_timed", "labs", Event(2, "labs.after_time_check"))
    labs_general_event = EventStorage("labs_general", "labs", Event(2, "labs.after_general_check"))
    labs_events = {
    }

    labs_bg_images = [
        BGImage("images/background/labs/bg c <level> <nude>.webp", 1, TimeCondition(daytime = "c")), # show corridor with few students
        BGImage("images/background/labs/bg 7.webp", 1, TimeCondition(daytime = 7)), # show empty corridor at night
    ]

# init 1 python:
    
##################################

################################
# ----- Labs Entry Point ----- #
################################

label labs ():
    call call_available_event(labs_timed_event) from labs_1

label .after_time_check (**kwargs):
    call call_available_event(labs_general_event) from labs_4

label .after_general_check (**kwargs):
    $ school_obj = get_school()

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