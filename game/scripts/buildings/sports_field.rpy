##########################################
# ----- Sports Field Event Handler ----- #
##########################################

init -1 python:
    sports_field_timed_event = TempEventStorage("sports_field", "sports_field", Event(1, "sports_field.after_time_check"))
    sports_field_general_event = EventStorage("sports_field",   "sports_field", Event(1, "sports_field.after_general_check"))
    sports_field_events = {
        "check_class":    EventStorage("check_class",    "sports_field", default_fallback, "There is nobody here."),
        "teach_class":    EventStorage("teach_class",    "sports_field", default_fallback, "There is nobody here."),
        "peek_changing":  EventStorage("peek_changing",  "sports_field", default_fallback, "There is nobody here."),
        "enter_changing": EventStorage("enter_changing", "sports_field", default_fallback, "There is nobody here."),
        "steal_changing": EventStorage("steal_changing", "sports_field", default_fallback, "There is nobody here."),
    }

    sports_field_bg_images = [
        BGImage("images/background/sports field/bg c <loli> <school_level> <nude>.webp", 1, TimeCondition(daytime = "c")), # show sports field with students
        BGImage("images/background/sports field/bg 3,6 <loli> <school_level> <nude>.webp", 1, TimeCondition(daytime = "3,6")), # show sports field with few students
        BGImage("images/background/sports field/bg 7.webp", 1, TimeCondition(daytime = 7)), # show sports field at night empty
    ]
    
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

    call show_idle_image("images/background/sports field/bg 1.webp", sports_field_bg_images,
        loli = loli,
    ) from sports_field_2

    call call_event_menu (
        "What to do on the sports field", 
        sports_field_events, 
        default_fallback,
        character.subtitles,
        context = loli,
    ) from sports_field_3

    jump sports_field

########################################

###################################
# ----- Sports Field Events ----- #
###################################



###################################