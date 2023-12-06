##########################################
# ----- Sports Field Event Handler ----- #
##########################################

init -1 python:
    sports_field_timed_event = EventStorage("sports_field", "", Event(1, "sports_field.after_time_check"))
    sports_field_events = {
        "check_class":    EventStorage("check_class",    "Check on sport class",         default_fallback, "There is nobody here."),
        "teach_class":    EventStorage("teach_class",    "Teach a sport class",          default_fallback, "There is nobody here."),
        "peek_changing":  EventStorage("peek_changing",  "Peek into the changing rooms", default_fallback, "There is nobody here."),
        "enter_changing": EventStorage("enter_changing", "Enter changing rooms",         default_fallback, "There is nobody here."),
        "steal_changing": EventStorage("steal_changing", "Steal some panties",           default_fallback, "There is nobody here."),
    }



    sports_field_timed_event.check_all_events()
    map(lambda x: x.check_all_events(), sports_field_events.values())

    sports_field_bg_images = [
        BGImage("images/background/sports field/bg c <level> <nude>.webp", 1, TimeCondition(daytime = "c")), # show sports field with students
        BGImage("images/background/sports field/bg 3,6 <level> <nude>.webp", 1, TimeCondition(daytime = "3,6")), # show sports field with few students
        BGImage("images/background/sports field/bg 7.webp", 1, TimeCondition(daytime = 7)), # show sports field at night empty
    ]
    
##########################################

########################################
# ----- Sports Field Entry Point ----- #
########################################

label sports_field ():
    
    call call_available_event(sports_field_timed_event) from sports_field_1

label .after_time_check (**kwargs):

    $ school_obj = get_random_school()

    call show_idle_image(school_obj, "images/background/sports field/bg 1.webp", sports_field_bg_images) from sports_field_2

    call call_event_menu (
        "What to do on the sports field", 
        sports_field_events, 
        default_fallback,
        character.subtitles,
        char_obj = school_obj,
    ) from sports_field_3

    jump sports_field

########################################

###################################
# ----- Sports Field Events ----- #
###################################



###################################