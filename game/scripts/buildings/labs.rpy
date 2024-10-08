##################################
# ----- Labs Event Handler ----- #
##################################

init -1 python:
    def labs_events_available() -> bool:
        return (labs_timed_event.has_available_highlight_events() or
            labs_general_event.has_available_highlight_events() or
            any(e.has_available_highlight_events() for e in labs_events.values()))

    labs_timed_event = TempEventStorage("labs_timed", "labs", fallback = Event(2, "labs.after_time_check"))
    labs_general_event = EventStorage("labs_general", "labs", fallback = Event(2, "labs.after_general_check"))
    labs_events = {}

    labs_bg_images = BGStorage("images/background/labs/bg f.webp",
        BGImage("images/background/labs/bg c <level> <nude>.webp", 1, TimeCondition(daytime = "c")), # show corridor with few students
        BGImage("images/background/labs/bg 7.webp", 1, TimeCondition(daytime = 7)), # show empty corridor at night
    )

init 1 python:
    
    labs_action_tutorial_event = Event(2, "action_tutorial",
        NOT(ProgressCondition('action_tutorial')),
        ValueSelector('return_label', 'labs'),
        NoHighlightOption(),
        TutorialCondition(),
        override_location = "misc", thumbnail = "images/events/misc/action_tutorial 0.webp")

    labs_general_event.add_event(
        labs_action_tutorial_event
    )

    
##################################

################################
# ----- Labs Entry Point ----- #
################################

label labs ():
    call call_available_event(labs_timed_event) from labs_1

label .after_time_check (**kwargs):
    call call_available_event(labs_general_event) from labs_4

label .after_general_check (**kwargs):
    call call_event_menu (
        "What to do at the Labs?", 
        labs_events, 
        default_fallback,
        character.subtitles,
        bg_image = labs_bg_images,
        fallback_text = "There is nothing to see here.",
    ) from labs_3

    jump labs

################################

###########################
# ----- Labs Events ----- #
###########################



###########################