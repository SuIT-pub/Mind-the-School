###########################################
# ----- Swimming Pool Event Handler ----- #
###########################################

init -1 python:
    swimming_pool_timed_event = EventStorage("swimming_pool", "", Event(2, "swimming_pool.after_time_check"))
    swimming_pool_events = {
        "check_class":    EventStorage("check_class",    "Check on swimming class",      default_fallback, "There is nobody here."),
        "teach_class":    EventStorage("teach_class",    "Teach a swimming class",       default_fallback, "There is nobody here."),
        "peek_changing":  EventStorage("peek_changing",  "Peek into the changing rooms", default_fallback, "There is nobody here."),
        "enter_changing": EventStorage("enter_changing", "Enter changing rooms",         default_fallback, "There is nobody here."),
        "steal_changing": EventStorage("steal_changing", "Steal some panties",           default_fallback, "There is nobody here."),
    }



    swimming_pool_timed_event.check_all_events()
    map(lambda x: x.check_all_events(), swimming_pool_events.values())

    swimming_pool_bg_images = [
        BGImage("images/background/swimming pool/bg c <level> <nude>.webp", 1, TimeCondition(daytime = "c")), # show swimming pool with students
        BGImage("images/background/swimming pool/bg 3,6 <level> <nude>.webp", 1, TimeCondition(daytime = "3,6")), # show swimming pool with few students
        BGImage("images/background/swimming pool/bg 7.webp", 1, TimeCondition(daytime = 7)), # show swimming pool at night empty
    ]
    
###########################################

#########################################
# ----- Swimming Pool Entry Point ----- #
#########################################

label swimming_pool ():
    
    call call_available_event(swimming_pool_timed_event) from swimming_pool_1

label .after_time_check (**kwargs):
    
    $ school_obj = get_random_school()

    call show_idle_image(school_obj, "images/background/swimming pool/bg 1.webp", swimming_pool_bg_images) from swimming_pool_2

    call call_event_menu (
        "What to do at the swimming pool?", 
        swimming_pool_events, 
        default_fallback,
        character.subtitles,
        char_obj = school_obj,
    ) from swimming_pool_3

    jump swimming_pool

#########################################

####################################
# ----- Swimming Pool Events ----- #
####################################



####################################