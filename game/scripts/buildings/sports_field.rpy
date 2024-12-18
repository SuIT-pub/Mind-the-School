###########################################
# region Sports Field Event Handler ----- #
###########################################

init -1 python:
    set_current_mod('base')
    
    sports_field_timed_event = TempEventStorage("sports_field", "sports_field", fallback = Event(1, "sports_field.after_time_check"))
    sports_field_general_event = EventStorage("sports_field",   "sports_field", fallback = Event(1, "sports_field.after_general_check"))
    register_highlighting(sports_field_timed_event, sports_field_general_event)

    sports_field_events = {}

    sports_field_bg_images = BGStorage("images/background/sports field/bg 1.webp", ValueSelector('loli', 0),
        BGImage("images/background/sports field/bg c <loli> <school_level> <nude>.webp", 1, TimeCondition(daytime = "c")), # show sports field with students
        BGImage("images/background/sports field/bg 3,6 <loli> <school_level> <nude>.webp", 1, TimeCondition(daytime = "3,6")), # show sports field with few students
        BGImage("images/background/sports field/bg 7.webp", 1, TimeCondition(daytime = 7)), # show sports field at night empty
    )
    
init 1 python:
    set_current_mod('base')

# endregion
###########################################

#########################################
# region Sports Field Entry Point ----- #
#########################################

label sports_field ():
    call call_available_event(sports_field_timed_event) from sports_field_1

label .after_time_check (**kwargs):
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