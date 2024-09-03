###########################################
# ----- Swimming Pool Event Handler ----- #
###########################################

init -1 python:
    set_current_mod('base')
    def swimming_pool_events_available() -> bool:
        return (swimming_pool_timed_event.has_available_highlight_events() or
            swimming_pool_general_event.has_available_highlight_events() or
            any(e.has_available_highlight_events() for e in swimming_pool_events.values()))

    swimming_pool_timed_event = TempEventStorage("swimming_pool", "swimming_pool", fallback = Event(2, "swimming_pool.after_time_check"))
    swimming_pool_general_event = EventStorage("swimming_pool",   "swimming_pool", fallback = Event(2, "swimming_pool.after_general_check"))
    swimming_pool_events = {}

    swimming_pool_bg_images = BGStorage("images/background/swimming pool/bg 1.webp", ValueSelector('loli', 0),
        BGImage("images/background/swimming pool/bg c <loli> <school_level> <nude>.webp", 1, TimeCondition(daytime = "c")), # show swimming pool with students
        BGImage("images/background/swimming pool/bg 3,6 <loli> <school_level> <nude>.webp", 1, TimeCondition(daytime = "3,6")), # show swimming pool with few students
        BGImage("images/background/swimming pool/bg 7.webp", 1, TimeCondition(daytime = 7)), # show swimming pool at night empty
    )
    
init 1 python:
    set_current_mod('base')
    
    swimming_pool_action_tutorial_event = Event(2, "action_tutorial",
        NOT(ProgressCondition('action_tutorial')),
        ValueSelector('return_label', 'swimming_pool'),
        NoHighlightOption(),
        TutorialCondition(),
        Pattern("main", "/images/events/misc/action_tutorial <step>.webp"),
        override_location = "misc", thumbnail = "images/events/misc/action_tutorial 0.webp")

    swimming_pool_general_event.add_event(
        swimming_pool_action_tutorial_event
    )


###########################################

#########################################
# ----- Swimming Pool Entry Point ----- #
#########################################

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

#########################################

####################################
# ----- Swimming Pool Events ----- #
####################################



####################################