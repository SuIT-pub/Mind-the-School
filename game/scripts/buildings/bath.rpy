###################################
# region Bath Event Handler ----- #
###################################

init -1 python:
    set_current_mod('base')

    bath_general_event = EventStorage("bath_general", "bath", fallback = Event(EVENT_ALWAYS, "bath.after_general_check"))
    register_highlighting(bath_general_event)

    #### Default bath events
    # available targets: -
    bath_events = {}

    bath_bg_images = BGStorage("images/background/bath/bg c.webp", 
        BGImage("images/background/bath/bg 1,3 <roster> <level> <nude>.webp", 1, TimeCondition(daytime = "1,3"), key = "bath_day_<level>"), # show bath with students
        BGImage("images/background/bath/bg 6 <roster> <level> <nude>.webp", 1, TimeCondition(daytime = 6), key = "bath_evening_<level>"), # show bath with students and/or teacher
        BGImage("images/background/bath/bg 7.webp", 1, TimeCondition(daytime = 7), key = "bath_night"), # show bath at night empty or with teachers
        fallback_key = "bath_empty_day",
    )
    
init 1 python:
    set_current_mod('base')

# endregion
###################################

##################################
# region Kiosk Entry Point ----- #
##################################

label bath ():
    call call_available_event(bath_general_event) from bath_4

label .after_general_check (**kwargs):
    call call_event_menu (
        "What to do in the Bath?",
        bath_events,
        default_fallback,
        character.subtitles,
        bg_image = bath_bg_images,
        fallback_text = "There is nothing to see here."
    ) from bath_3

    jump bath

# endregion
##################################

############################
# region Bath Events ----- #
############################



#endregion
############################