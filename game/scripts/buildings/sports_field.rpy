##########################################
# ----- Sports Field Event Handler ----- #
##########################################

init -1 python:
    set_current_mod('base')
    def sports_field_events_available() -> bool:
        return (sports_field_timed_event.has_available_highlight_events() or
            sports_field_general_event.has_available_highlight_events() or
            any(e.has_available_highlight_events() for e in sports_field_events.values()))

    sports_field_timed_event = TempEventStorage("sports_field", "sports_field", fallback = Event(1, "sports_field.after_time_check"))
    sports_field_general_event = EventStorage("sports_field",   "sports_field", fallback = Event(1, "sports_field.after_general_check"))
    sports_field_events = {}

    sports_field_bg_images = BGStorage("images/background/sports field/bg 1.webp", ValueSelector('loli', 0),
        BGImage("images/background/sports field/bg c <loli> <school_level> <nude>.webp", 1, TimeCondition(daytime = "c")), # show sports field with students
        BGImage("images/background/sports field/bg 3,6 <loli> <school_level> <nude>.webp", 1, TimeCondition(daytime = "3,6")), # show sports field with few students
        BGImage("images/background/sports field/bg 7.webp", 1, TimeCondition(daytime = 7)), # show sports field at night empty
    )
    
init 1 python:
    set_current_mod('base')
    
    sports_field_action_tutorial_event = Event(2, "action_tutorial",
        NOT(ProgressCondition('action_tutorial')),
        ValueSelector('return_label', 'sports_field'),
        NoHighlightOption(),
        TutorialCondition(),
        Pattern("main", "/images/events/misc/action_tutorial <step>.webp"),
        override_location = "misc", thumbnail = "images/events/misc/action_tutorial 0.webp")

    sports_field_general_event.add_event(
        sports_field_action_tutorial_event
    )


##########################################

########################################
# ----- Sports Field Entry Point ----- #
########################################

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

########################################

###################################
# ----- Sports Field Events ----- #
###################################



###################################