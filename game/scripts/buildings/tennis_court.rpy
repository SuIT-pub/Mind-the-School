##########################################
# ----- Tennis Court Event Handler ----- #
##########################################

init -1 python:
    tennis_court_timed_event = TempEventStorage("tennis_court", "tennis_court", Event(2, "tennis_court.after_time_check"))
    tennis_court_general_event = EventStorage("tennis_court",   "tennis_court", Event(2, "tennis_court.after_general_check"))
    tennis_court_events = {}



    tennis_court_bg_images = BGStorage("images/background/tennis court/bg 1.webp",
        BGImage("images/background/tennis court/bg c <level> <nude>.webp", 1, TimeCondition(daytime = "c")), # show tennis court with students
        BGImage("images/background/tennis court/bg 3,6 <level> <nude>.webp", 1, TimeCondition(daytime = "3,6")), # show tennis court with few students
        BGImage("images/background/tennis court/bg 7.webp", 1, TimeCondition(daytime = 7)), # show tennis court at night empty
    )

# init 1 python:

##########################################

########################################
# ----- Tennis Court Entry Point ----- #
########################################

label tennis_court ():
    call call_available_event(tennis_court_timed_event) from tennis_court_1

label .after_time_check (**kwargs):
    call call_available_event(tennis_court_general_event) from tennis_court_4

label .after_general_check (**kwargs):
    $ loli = get_random_loli()

    $ tennis_court_bg_images.add_kwargs(loli = loli)

    call call_event_menu (
        "What to do at the tennis court?", 
        tennis_court_events, 
        default_fallback,
        tennis_court_bg_images
        character.subtitles,
        context = loli,
    ) from tennis_court_3

    jump tennis_court

########################################

###################################
# ----- Tennis Court Events ----- #
###################################



###################################