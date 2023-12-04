##########################################
# ----- Tennis Court Event Handler ----- #
##########################################

init -1 python:
    tennis_court_timed_event = EventStorage("tennis_court", "", Event(2, "tennis_court.after_time_check"))
    tennis_court_events = {
        "check_class":    EventStorage("check_class",    "Check on tennis class",        default_fallback, "There is nobody here."),
        "teach_class":    EventStorage("teach_class",    "Teach a tennis class",         default_fallback, "There is nobody here."),
        "peek_changing":  EventStorage("peek_changing",  "Peek into the changing rooms", default_fallback, "There is nobody here."),
        "enter_changing": EventStorage("enter_changing", "Enter changing rooms",         default_fallback, "There is nobody here."),
        "steal_changing": EventStorage("steal_changing", "Steal some panties",           default_fallback, "There is nobody here."),
    }



    tennis_court_timed_event.check_all_events()
    map(lambda x: x.check_all_events(), tennis_court_events.values())

    tennis_court_bg_images = [
        BGImage("images/background/tennis court/bg c <level> <nude>.jpg", 1, TimeCondition(daytime = "c")), # show tennis court with students
        BGImage("images/background/tennis court/bg 3,6 <level> <nude>.jpg", 1, TimeCondition(daytime = "3,6")), # show tennis court with few students
        BGImage("images/background/tennis court/bg 7.jpg", 1, TimeCondition(daytime = 7)), # show tennis court at night empty
    ]
    
##########################################

########################################
# ----- Tennis Court Entry Point ----- #
########################################

label tennis_court ():
    
    call call_available_event(tennis_court_timed_event) from tennis_court_1

label .after_time_check (**kwargs):

    $ school_obj = get_random_school()

    call show_idle_image(school_obj, "images/background/tennis court/bg 1.jpg", tennis_court_bg_images) from tennis_court_2

    call call_event_menu (
        "What to do at the tennis court?", 
        tennis_court_events, 
        default_fallback,
        character.subtitles,
        char_obj = school_obj,
    ) from tennis_court_3

    jump tennis_court

########################################

###################################
# ----- Tennis Court Events ----- #
###################################



###################################