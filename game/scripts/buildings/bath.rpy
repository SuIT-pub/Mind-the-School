##################################
# ----- Bath Event Handler ----- #
##################################

init -1 python:
    bath_timed_event = EventStorage("bath", "", Event(2, "bath.after_time_check"))
    bath_events = {
        "male_enter":   EventStorage("male_enter",   "Enter the male bath",       default_fallback, "I don't want to take a bath."),
        "female_enter": EventStorage("female_enter", "Enter the female bath",     default_fallback, "I don't want to take a bath."),
        "female_peek":  EventStorage("female_peek",  "Peek into the female bath", default_fallback, "There is nobody here."       ),
        "mixed_enter":  EventStorage("mixed_enter",  "Enter the mixed bath",      default_fallback, "I don't want to take a bath."),
        "mixed_peek":   EventStorage("mixed_peek",   "Peek into the mixed bath",  default_fallback, "There is nobody here."       ),
    }

    bath_timed_event.check_all_events()
    map(lambda x: x.check_all_events(), bath_events.values())

    bath_bg_images = [
        BGImage("images/background/bath/bg 1,3 <level> <nude>.jpg", 1, TimeCondition(daytime = "1,3")), # show bath with students
        BGImage("images/background/bath/bg 6 <level> <nude>.jpg", 1, TimeCondition(daytime = 6)), # show bath with students and/or teacher
        BGImage("images/background/bath/bg 7.jpg", 1, TimeCondition(daytime = 7)), # show bath at night empty or with teachers
    ]
    
##################################

#################################
# ----- Kiosk Entry Point ----- #
#################################

label bath ():

    call call_available_event(bath_timed_event) from bath_1

label .after_time_check (**kwargs):

    $ school_obj = get_random_school()

    call show_idle_image(school_obj, "images/background/bath/bg c.jpg", bath_bg_images) from bath_2

    call call_event_menu (
        "What to do in the Bath?",
        bath_events,
        default_fallback,
        character.subtitles,
        char_obj = school_obj,
        fallback_text = "There is nothing to see here."
    ) from bath_3

    jump bath

##################################

###########################
# ----- Bath Events ----- #
###########################


###########################