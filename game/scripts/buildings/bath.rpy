##################################
# ----- Bath Event Handler ----- #
##################################

init -1 python:    
    bath_after_time_check = Event(2, "bath.after_time_check")
    bath_fallback         = Event(2, "bath_fallback")
    bath_enter_fallback   = Event(2, "bath_enter_fallback")
    bath_peek_fallback    = Event(2, "bath_peek_fallback")

    bath_timed_event = EventStorage("bath", "", bath_after_time_check)
    bath_events = {
        "male_enter":   EventStorage("male_enter",   "Enter the male bath",       bath_enter_fallback),
        "female_enter": EventStorage("female_enter", "Enter the female bath",     bath_enter_fallback),
        "female_peek":  EventStorage("female_peek",  "Peek into the female bath", bath_peek_fallback ),
        "mixed_enter":  EventStorage("mixed_enter",  "Enter the mixed bath",      bath_enter_fallback),
        "mixed_peek":   EventStorage("mixed_peek",   "Peek into the mixed bath",  bath_peek_fallback ),
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

    call show_bath_idle_image(school_obj) from bath_2

    call call_event_menu (
        "What to do in the Bath?",
        bath_events,
        bath_fallback,
        character.subtitles,
        char_obj = school_obj,
    ) from bath_3

    jump bath

label show_bath_idle_image(school_obj):    

    $ max_nude, image_path = get_background(
        "images/background/bath/bg c.jpg", # show bath empty
        bath_bg_images,
        school_obj,
    )

    call show_image_with_nude_var (image_path, max_nude) from _call_show_image_with_nude_var

    return

##################################

####################################
# ----- Bath Fallback Events ----- #
####################################

label bath_fallback (**kwargs):
    subtitles "There is nothing to see here."
    jump map_overview

label bath_peek_fallback (**kwargs):
    subtitles "There is nobody here."
    jump map_overview

label bath_enter_fallback (**kwargs):
    subtitles "I don't want to take a bath."
    jump map_overview

####################################

###########################
# ----- Bath Events ----- #
###########################


###########################