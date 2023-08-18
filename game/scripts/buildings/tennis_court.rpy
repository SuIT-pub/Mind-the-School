##########################################
# ----- Tennis Court Event Handler ----- #
##########################################

init -1 python:
    tennis_court_after_time_check = Event("tennis_court_after_time_check", "tennis_court.after_time_check", 2)
    tennis_court_fallback         = Event("tennis_court_fallback",         "tennis_court_fallback",         2)
    tennis_court_person_fallback  = Event("tennis_court_person_fallback",  "tennis_court_person_fallback",  2)

    tennis_court_timed_event = EventStorage("tennis_court", "", tennis_court_after_time_check)
    tennis_court_events = {
        "check_class":    EventStorage("check_class",    "Check on tennis class",        tennis_court_fallback),
        "teach_class":    EventStorage("teach_class",    "Teach a tennis class",         tennis_court_fallback),
        "peek_changing":  EventStorage("peek_changing",  "Peek into the changing rooms", tennis_court_fallback),
        "enter_changing": EventStorage("enter_changing", "Enter changing rooms",         tennis_court_fallback),
        "steal_changing": EventStorage("steal_changing", "Steal some panties",           tennis_court_fallback),
    }

    tennis_court_bg_images = [
        BGImage("images/background/tennis court/bg c <level> <nude>.png", 1, TimeCondition(daytime = "c")), # show tennis court with students
        BGImage("images/background/tennis court/bg 3,6 <level> <nude>.png", 1, TimeCondition(daytime = "3,6")), # show tennis court with few students
        BGImage("images/background/tennis court/bg 7.png", 1, TimeCondition(daytime = 7)), # show tennis court at night empty
    ]
    
##########################################

########################################
# ----- Tennis Court Entry Point ----- #
########################################

label tennis_court:
    
    call call_available_event(tennis_court_timed_event) from tennis_court_1

label .after_time_check:

    $ school = get_random_school()

    call show_tennis_court_idle_image(school) from tennis_court_2

    call call_event_menu (
        "What to do at the tennis court?",
        1, 
        7, 
        tennis_court_events, 
        tennis_court_fallback,
        character.subtitles,
        school,
    ) from tennis_court_3

    jump tennis_court from tennis_court_4

label show_tennis_court_idle_image(school):

    $ max_nude, image_path = get_background(
        "images/background/tennis court/bg 1.png", # show empty tennis court
        tennis_court_bg_images,
        get_level_for_char(school, charList["schools"]),
    )

    show screen image_with_nude_var (image_path, max_nude)

    return

########################################

############################################
# ----- Tennis Court Fallback Events ----- #
############################################

label tennis_court_fallback:
    subtitles "There is nothing to see here."
    return

label tennis_court_person_fallback:
    subtitles "There is nobody here."
    return

############################################

###################################
# ----- Tennis Court Events ----- #
###################################



###################################