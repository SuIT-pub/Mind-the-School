##################################
# ----- Bath Event Handler ----- #
##################################

init -1 python:    
    bath_after_time_check = Event("bath_after_time_check", "bath.after_time_check", 2)
    bath_fallback         = Event("bath_fallback",         "bath_fallback",         2)
    bath_enter_fallback   = Event("bath_enter_fallback",   "bath_enter_fallback",   2)
    bath_peek_fallback    = Event("bath_peek_fallback",    "bath_peek_fallback",    2)

    bath_timed_event = EventStorage("bath", "", bath_after_time_check)
    bath_events = {
        "male_enter":   EventStorage("male_enter",   "Enter the male bath",       bath_enter_fallback),
        "female_enter": EventStorage("female_enter", "Enter the female bath",     bath_enter_fallback),
        "female_peek":  EventStorage("female_peek",  "Peek into the female bath", bath_peek_fallback ),
        "mixed_enter":  EventStorage("mixed_enter",  "Enter the mixed bath",      bath_enter_fallback),
        "mixed_peek":   EventStorage("mixed_peek",   "Peek into the mixed bath",  bath_peek_fallback ),
    }
    
##################################

#################################
# ----- Kiosk Entry Point ----- #
#################################

label bath:
    # show bath inside

    # if daytime in [1, 3]:
    #     # show bath with students
    # if daytime in [6]:
    #     # show bath with students and/or teacher
    # if daytime in [2, 4, 5]:
    #     # show bath empty
    # if daytime in [7]:
    #     # show bath at night empty or with teachers

    call call_available_event(bath_timed_event) from _call_call_available_event

label .after_time_check:

    $ school = get_random_school()

    call show_bath_idle_image(school)

    call call_event_menu (
        "What to do in the Bath?",
        1, 
        7, 
        bath_events,
        bath_fallback,
        character.subtitles,
        school,
    ) from _call_call_event_menu

    jump bath

label show_bath_idle_image(school):    
    $ image_path = "images/background/bath/bg c.png"

    if time.check_daytime("1,3"):
        $ image_path = get_image_with_level(
            "images/background/bath/bg 1,3 <level> <nude>.png", 
            get_level_for_char(school, charList["schools"]),
        )
    elif time.check_daytime(6):
        $ image_path = get_image_with_level(
            "images/background/bath/bg 6 <level> <nude>.png", 
            get_level_for_char(school, charList["schools"]),
        )
    elif time.check_daytime(7):
        $ image_path = "images/background/bath/bg 7.png"

    show screen image_with_nude_var (image_path, 0)

    return

##################################

####################################
# ----- Bath Fallback Events ----- #
####################################

label bath_fallback:
    subtitles "There is nothing to see here."
    return

label bath_peek_fallback:
    subtitles "There is nobody here."
    return

label bath_enter_fallback:
    subtitles "I don't want to take a bath."
    return

####################################

###########################
# ----- Bath Events ----- #
###########################


###########################