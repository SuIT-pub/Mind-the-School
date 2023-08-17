##########################################
# ----- Sports Field Event Handler ----- #
##########################################

init -1 python:
    sports_field_after_time_check = Event("sports_field_after_time_check", "sports_field.after_time_check", 1)
    sports_field_fallback = Event("sports_field_fallback", "sports_field_fallback", 1)
    sports_field_person_fallback = Event("sports_field_person_fallback", "sports_field_person_fallback", 1)

    sports_field_timed_event = EventStorage("sports_field", "", sports_field_after_time_check)
    sports_field_events = {
        "check_class":    EventStorage("check_class",    "Check on sport class",         sports_field_person_fallback),
        "teach_class":    EventStorage("teach_class",    "Teach a sport class",          sports_field_person_fallback),
        "peek_changing":  EventStorage("peek_changing",  "Peek into the changing rooms", sports_field_person_fallback),
        "enter_changing": EventStorage("enter_changing", "Enter changing rooms",         sports_field_person_fallback),
        "steal_changing": EventStorage("steal_changing", "Steal some panties",           sports_field_person_fallback),
    }

##########################################

########################################
# ----- Sports Field Entry Point ----- #
########################################

label sports_field:
    # show sports field

    # if daytime in [1]:
    #     # show empty sports field
    # if daytime in [2, 4, 5]:
    #     # show sports field with students
    # if daytime in [3, 6]:
    #     # show sports field with few students
    # if daytime in [7]:
    #     # show sports field at night empty

    call call_available_event(sports_field_timed_event) from _call_call_available_event_13

label .after_time_check:

    $ school = get_random_school()

    call show_sports_field_idle_image(school)

    call call_event_menu (
        "What to do on the sports field",
        1, 
        7, 
        sports_field_events, 
        sports_field_fallback,
        character.subtitles,
        school,
    ) from _call_call_event_menu_13

    jump sports_field

label show_sports_field_idle_image(school):    
    $ image_path = "images/background/sports field/bg 1.png"

    if time.check_daytime("c"):
        $ image_path = get_image_with_level(
            "images/background/sports field/bg c <level> <nude>.png", 
            get_level_for_char(school, charList["schools"]),
        )
    elif time.check_daytime("3,6"):
        $ image_path = get_image_with_level(
            "images/background/sports field/bg 3,6 <level> <nude>.png", 
            get_level_for_char(school, charList["schools"]),
        )
    elif time.check_daytime(7):
        $ image_path = "images/background/sports field/bg 7.png"

    show screen image_with_nude_var (image_path, 0)

    return

########################################

############################################
# ----- Sports Field Fallback Events ----- #
############################################

label sports_field_fallback:
    subtitles "There is nothing to see here."
    return

label sports_field_person_fallback:
    subtitles "There is nobody here."
    return

############################################

###################################
# ----- Sports Field Events ----- #
###################################



###################################