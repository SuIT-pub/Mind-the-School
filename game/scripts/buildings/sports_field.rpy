###########################################
# region Sports Field Event Handler ----- #
###########################################

init -1 python:
    set_current_mod('base')
    
    sports_field_general_event = EventStorage("sports_field",   "sports_field", fallback = Event(1, "sports_field.after_general_check"))
    register_highlighting(sports_field_general_event)

    #### Default sports field events
    # available targets: -
    sports_field_events = {}

    sports_field_bg_images = BGStorage("images/background/sports field/bg 1.webp", ValueSelector('roster', 0),
        BGImage("images/background/sports field/bg c <roster> <school_level> <nude>.webp", 1, TimeCondition(daytime = "c"), key = "sports_field_class_<school_level>"), # show sports field with students
        BGImage("images/background/sports field/bg 3,6 <roster> <school_level> <nude>.webp", 1, TimeCondition(daytime = "3,6"), key = "sports_field_free_<school_level>"), # show sports field with few students
        BGImage("images/background/sports field/bg 7.webp", 1, TimeCondition(daytime = 7), key = "sports_field_night"), # show sports field at night empty
        fallback_key = "sports_field_empty_day",
    )
    
init 1 python:
    set_current_mod('base')

# endregion
###########################################

#########################################
# region Sports Field Entry Point ----- #
#########################################

label sports_field ():
    call empty_label from sports_field_1
    call call_available_event(sports_field_general_event) from sports_field_4

label .after_general_check (**kwargs):
    call call_event_menu (
        "What to do on the sports field", 
        sports_field_events, 
        default_fallback,
        character.subtitles,
        bg_image = sports_field_bg_images,
    ) from sports_field_3

    jump sports_field

# endregion
#########################################

####################################
# region Sports Field Events ----- #
####################################



# endregion
####################################