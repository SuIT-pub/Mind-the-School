############################################
# region Swimming Pool Event Handler ----- #
############################################

init -1 python:
    set_current_mod('base')
    
    swimming_pool_timed_event = TempEventStorage("swimming_pool", "swimming_pool", fallback = Event(2, "swimming_pool.after_time_check"))
    swimming_pool_general_event = EventStorage("swimming_pool",   "swimming_pool", fallback = Event(2, "swimming_pool.after_general_check"))
    register_highlighting(swimming_pool_timed_event, swimming_pool_general_event)

    swimming_pool_events = {}

    swimming_pool_bg_images = BGStorage("images/background/swimming pool/bg 1.webp", ValueSelector('loli', 0),
        BGImage("images/background/swimming pool/bg c <loli> <school_level> <nude>.webp", 1, TimeCondition(daytime = "c")), # show swimming pool with students
        BGImage("images/background/swimming pool/bg 3,6 <loli> <school_level> <nude>.webp", 1, TimeCondition(daytime = "3,6")), # show swimming pool with few students
        BGImage("images/background/swimming pool/bg 7.webp", 1, TimeCondition(daytime = 7)), # show swimming pool at night empty
    )
    
init 1 python:
    set_current_mod('base')

# endregion
############################################

##########################################
# region Swimming Pool Entry Point ----- #
##########################################

label swimming_pool ():
    call call_available_event(swimming_pool_timed_event) from swimming_pool_1

label .after_time_check (**kwargs):
    call call_available_event(swimming_pool_general_event) from swimming_pool_4

label .after_general_check (**kwargs):
    call call_event_menu (
        "What to do at the swimming pool?", 
        swimming_pool_events, 
        default_fallback,
        character.subtitles,
        bg_image = swimming_pool_bg_images,
    ) from swimming_pool_3

    jump swimming_pool

# endregion
##########################################

#####################################
# region Swimming Pool Events ----- #
#####################################



# endregion
#####################################