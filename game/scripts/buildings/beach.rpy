####################################
# region Beach Event Handler ----- #
####################################

init -1 python:
    set_current_mod('base')
    
    beach_general_event = EventStorage("beach_general", "beach", fallback = Event(2, "beach.after_general_check"))
    register_highlighting(beach_general_event)

    #### Default beach events
    # available targets: -
    beach_events = {}

    beach_bg_images = BGStorage("images/background/beach/bg c.webp", 
        BGImage("images/background/beach/bg 1,3 <loli> <level> <nude>.webp", 1, TimeCondition(daytime = "1,3")), # show bath with students
        BGImage("images/background/beach/bg 6 <loli> <level> <nude>.webp", 1, TimeCondition(daytime = 6)), # show bath with students and/or teacher
        BGImage("images/background/beach/bg 7.webp", 1, TimeCondition(daytime = 7)), # show bath at night empty or with teachers
    )
    
init 1 python:
    set_current_mod('base')

# endregion
####################################

##################################
# region Beach Entry Point ----- #
##################################

label beach ():
    call call_available_event(beach_general_event) from beach_4

label .after_general_check (**kwargs):
    call call_event_menu (
        "What to do at the Beach?",
        beach_events,
        default_fallback,
        character.subtitles,
        bg_image = beach_bg_images,
        fallback_text = "There is nothing to see here."
    ) from beach_3

    jump beach

# endregion
##################################

#############################
# region Beach Events ----- #
#############################



# endregion
#############################