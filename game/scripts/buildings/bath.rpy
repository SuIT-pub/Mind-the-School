##################################
# ----- Bath Event Handler ----- #
##################################

init -1 python:
    bath_timed_event = TempEventStorage("bath_timed", "bath", Event(2, "bath.after_time_check"))
    bath_general_event = EventStorage("bath_general", "bath", Event(2, "bath.after_general_check"))
    bath_events = {}

    bath_bg_images = BGStorage("images/background/bath/bg c.webp", 
        BGImage("images/background/bath/bg 1,3 <loli> <level> <nude>.webp", 1, TimeCondition(daytime = "1,3")), # show bath with students
        BGImage("images/background/bath/bg 6 <loli> <level> <nude>.webp", 1, TimeCondition(daytime = 6)), # show bath with students and/or teacher
        BGImage("images/background/bath/bg 7.webp", 1, TimeCondition(daytime = 7)), # show bath at night empty or with teachers
    )
    
# init 1 python:

##################################

#################################
# ----- Kiosk Entry Point ----- #
#################################

label bath ():
    call call_available_event(bath_timed_event) from bath_1

label .after_time_check (**kwargs):
    call call_available_event(bath_general_event) from bath_4

label .after_general_check (**kwargs):
    $ loli = get_random_loli()

    $ bath_bg_images.add_kwargs(loli = loli)

    call call_event_menu (
        "What to do in the Bath?",
        bath_events,
        default_fallback,
        bath_bg_images,
        character.subtitles,
        context = loli
        fallback_text = "There is nothing to see here."
    ) from bath_3

    jump bath

##################################

###########################
# ----- Bath Events ----- #
###########################


###########################