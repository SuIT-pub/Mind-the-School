##########################################
# ----- Sports Field Event Handler ----- #
##########################################

init -1 python:
    sports_field_after_time_check = Event(1, "sports_field.after_time_check")
    sports_field_fallback = Event(1, "sports_field_fallback")
    sports_field_person_fallback = Event(1, "sports_field_person_fallback")

    sports_field_timed_event = EventStorage("sports_field", "", sports_field_after_time_check)
    sports_field_events = {
        "check_class":    EventStorage("check_class",    "Check on sport class",         sports_field_person_fallback),
        "teach_class":    EventStorage("teach_class",    "Teach a sport class",          sports_field_person_fallback),
        "peek_changing":  EventStorage("peek_changing",  "Peek into the changing rooms", sports_field_person_fallback),
        "enter_changing": EventStorage("enter_changing", "Enter changing rooms",         sports_field_person_fallback),
        "steal_changing": EventStorage("steal_changing", "Steal some panties",           sports_field_person_fallback),
    }



    sports_field_timed_event.check_all_events()
    map(lambda x: x.check_all_events(), sports_field_events.values())

    sports_field_bg_images = [
        BGImage("images/background/sports field/bg c <level> <nude>.jpg", 1, TimeCondition(daytime = "c")), # show sports field with students
        BGImage("images/background/sports field/bg 3,6 <level> <nude>.jpg", 1, TimeCondition(daytime = "3,6")), # show sports field with few students
        BGImage("images/background/sports field/bg 7.jpg", 1, TimeCondition(daytime = 7)), # show sports field at night empty
    ]
    
##########################################

########################################
# ----- Sports Field Entry Point ----- #
########################################

label sports_field ():
    
    call call_available_event(sports_field_timed_event) from sports_field_1

label .after_time_check (**kwargs):

    $ school_obj = get_random_school()

    call show_sports_field_idle_image(school_obj) from sports_field_2

    call call_event_menu (
        "What to do on the sports field", 
        sports_field_events, 
        sports_field_fallback,
        character.subtitles,
        char_obj = school_obj,
    ) from sports_field_3

    jump sports_field

label show_sports_field_idle_image(school_obj):    

    $ max_nude, image_path = get_background(
        "images/background/sports field/bg 1.jpg", # show empty sports field
        sports_field_bg_images,
        school_obj,
    )

    call show_image_with_nude_var (image_path, max_nude) from _call_show_image_with_nude_var_13

    return

########################################

############################################
# ----- Sports Field Fallback Events ----- #
############################################

label sports_field_fallback (**kwargs):
    subtitles "There is nothing to see here."
    jump map_overview

label sports_field_person_fallback (**kwargs):
    subtitles "There is nobody here."
    jump map_overview

############################################

###################################
# ----- Sports Field Events ----- #
###################################



###################################