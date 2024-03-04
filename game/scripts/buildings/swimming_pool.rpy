###########################################
# ----- Swimming Pool Event Handler ----- #
###########################################

init -1 python:
    swimming_pool_timed_event = TempEventStorage("swimming_pool", "swimming_pool", Event(2, "swimming_pool.after_time_check"))
    swimming_pool_general_event = EventStorage("swimming_pool",   "swimming_pool", Event(2, "swimming_pool.after_general_check"))
    swimming_pool_events = {
        "check_class":    EventStorage("check_class",    "swimming_pool", default_fallback, "There is nobody here."),
        "teach_class":    EventStorage("teach_class",    "swimming_pool", default_fallback, "There is nobody here."),
        "peek_changing":  EventStorage("peek_changing",  "swimming_pool", default_fallback, "There is nobody here."),
        "enter_changing": EventStorage("enter_changing", "swimming_pool", default_fallback, "There is nobody here."),
        "steal_changing": EventStorage("steal_changing", "swimming_pool", default_fallback, "There is nobody here."),
    }

    swimming_pool_bg_images = [
        BGImage("images/background/swimming pool/bg c <loli> <school_level> <nude>.webp", 1, TimeCondition(daytime = "c")), # show swimming pool with students
        BGImage("images/background/swimming pool/bg 3,6 <loli> <school_level> <nude>.webp", 1, TimeCondition(daytime = "3,6")), # show swimming pool with few students
        BGImage("images/background/swimming pool/bg 7.webp", 1, TimeCondition(daytime = 7)), # show swimming pool at night empty
    ]
    
# init 1 python:

###########################################

#########################################
# ----- Swimming Pool Entry Point ----- #
#########################################

label swimming_pool ():
    call call_available_event(swimming_pool_timed_event) from swimming_pool_1

label .after_time_check (**kwargs):
    call call_available_event(swimming_pool_general_event) from swimming_pool_4

label .after_general_check (**kwargs):
    $ loli = get_random_loli()

    call show_idle_image("images/background/swimming pool/bg 1.webp", swimming_pool_bg_images
        loli = loli,
    ) from swimming_pool_2

    call call_event_menu (
        "What to do at the swimming pool?", 
        swimming_pool_events, 
        default_fallback,
        character.subtitles,
        context = loli,
    ) from swimming_pool_3

    jump swimming_pool

#########################################

####################################
# ----- Swimming Pool Events ----- #
####################################



####################################