###################################
# region Labs Event Handler ----- #
###################################

init -1 python:
    set_current_mod('base')
    
    labs_timed_event = TempEventStorage("labs_timed", "labs", fallback = Event(2, "labs.after_time_check"))
    labs_general_event = EventStorage("labs_general", "labs", fallback = Event(2, "labs.after_general_check"))
    register_highlighting(labs_timed_event, labs_general_event)

    labs_events = {}

    labs_bg_images = BGStorage("images/background/labs/bg f.webp",
        BGImage("images/background/labs/bg c <level> <nude>.webp", 1, TimeCondition(daytime = "c")), # show corridor with few students
        BGImage("images/background/labs/bg 7.webp", 1, TimeCondition(daytime = 7)), # show empty corridor at night
    )

init 1 python:
    set_current_mod('base')
    
# endregion
###################################

#################################
# region Labs Entry Point ----- #
#################################

label labs ():
    call call_available_event(labs_timed_event) from labs_1

label .after_time_check (**kwargs):
    call call_available_event(labs_general_event) from labs_4

label .after_general_check (**kwargs):
    call call_event_menu (
        "What to do at the Labs?", 
        labs_events, 
        default_fallback,
        character.subtitles,
        bg_image = labs_bg_images,
        fallback_text = "There is nothing to see here.",
    ) from labs_3

    jump labs

# endregion
#################################

############################
# region Labs Events ----- #
############################



# endregion
############################