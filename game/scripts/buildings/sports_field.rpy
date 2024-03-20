##########################################
# ----- Sports Field Event Handler ----- #
##########################################

init -1 python:
    def sports_field_events_available() -> bool:
        return (sports_field_timed_event.has_available_highlight_events() or
            sports_field_general_event.has_available_highlight_events() or
            any(e.has_available_highlight_events() for e in sports_field_events.values()))

    sports_field_timed_event = TempEventStorage("sports_field", "sports_field", Event(1, "sports_field.after_time_check"))
    sports_field_general_event = EventStorage("sports_field",   "sports_field", Event(1, "sports_field.after_general_check"))
    sports_field_events = {}

    sports_field_bg_images = BGStorage("images/background/sports field/bg 1.webp",
        BGImage("images/background/sports field/bg c <loli> <school_level> <nude>.webp", 1, TimeCondition(daytime = "c")), # show sports field with students
        BGImage("images/background/sports field/bg 3,6 <loli> <school_level> <nude>.webp", 1, TimeCondition(daytime = "3,6")), # show sports field with few students
        BGImage("images/background/sports field/bg 7.webp", 1, TimeCondition(daytime = 7)), # show sports field at night empty
    )
    
# init 1 python:

##########################################

########################################
# ----- Sports Field Entry Point ----- #
########################################

label sports_field ():
    call call_available_event(sports_field_timed_event) from sports_field_1

label .after_time_check (**kwargs):
    call call_available_event(sports_field_general_event) from sports_field_4

label .after_general_check (**kwargs):
    $ loli = get_random_loli()
    $ sports_field_bg_images.add_kwargs(loli = loli)

    call call_event_menu (
        "What to do on the sports field", 
        sports_field_events, 
        default_fallback,
        character.subtitles,
        bg_image = sports_field_bg_images,
        context = loli,
    ) from sports_field_3

    jump sports_field

########################################

###################################
# ----- Sports Field Events ----- #
###################################



###################################