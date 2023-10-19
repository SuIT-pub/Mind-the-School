###########################################
# ----- Swimming Pool Event Handler ----- #
###########################################

init -1 python:
    swimming_pool_after_time_check = Event(2, "swimming_pool.after_time_check")
    swimming_pool_fallback         = Event(2, "swimming_pool_fallback")
    swimming_pool_person_fallback  = Event(2, "swimming_pool_person_fallback")

    swimming_pool_timed_event = EventStorage("swimming_pool", "", swimming_pool_after_time_check)
    swimming_pool_events = {
        "check_class":    EventStorage("check_class",    "Check on swimming class",      swimming_pool_person_fallback),
        "teach_class":    EventStorage("teach_class",    "Teach a swimming class",       swimming_pool_person_fallback),
        "peek_changing":  EventStorage("peek_changing",  "Peek into the changing rooms", swimming_pool_person_fallback),
        "enter_changing": EventStorage("enter_changing", "Enter changing rooms",         swimming_pool_person_fallback),
        "steal_changing": EventStorage("steal_changing", "Steal some panties",           swimming_pool_person_fallback),
    }



    swimming_pool_timed_event.check_all_events()
    map(lambda x: x.check_all_events(), swimming_pool_events.values())

    swimming_pool_bg_images = [
        BGImage("images/background/swimming pool/bg c <level> <nude>.jpg", 1, TimeCondition(daytime = "c")), # show swimming pool with students
        BGImage("images/background/swimming pool/bg 3,6 <level> <nude>.jpg", 1, TimeCondition(daytime = "3,6")), # show swimming pool with few students
        BGImage("images/background/swimming pool/bg 7.jpg", 1, TimeCondition(daytime = 7)), # show swimming pool at night empty
    ]
    
###########################################

#########################################
# ----- Swimming Pool Entry Point ----- #
#########################################

label swimming_pool ():
    
    call call_available_event(swimming_pool_timed_event) from swimming_pool_1

label .after_time_check (**kwargs):
    
    $ school_obj = get_random_school()

    call show_swimming_pool_idle_image(school_obj) from swimming_pool_2

    call call_event_menu (
        "What to do at the swimming pool?", 
        swimming_pool_events, 
        swimming_pool_fallback,
        character.subtitles,
        char_obj = school_obj,
    ) from swimming_pool_3

    jump swimming_pool

label show_swimming_pool_idle_image(school_obj):

    $ max_nude, image_path = get_background(
        "images/background/swimming pool/bg 1.jpg", # show empty swimming pool
        swimming_pool_bg_images,
        school_obj,
    )

    call show_image_with_nude_var (image_path, max_nude) from _call_show_image_with_nude_var_14

    return

#########################################

#############################################
# ----- Swimming Pool Fallback Events ----- #
#############################################

label swimming_pool_fallback (**kwargs):
    subtitles "There is nothing to see here."
    jump map_overview

label swimming_pool_person_fallback (**kwargs):
    subtitles "There is nobody here."
    jump map_overview

#############################################

####################################
# ----- Swimming Pool Events ----- #
####################################



####################################