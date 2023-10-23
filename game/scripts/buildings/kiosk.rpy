###################################
# ----- Kiosk Event Handler ----- #
###################################

init -1 python:
    kiosk_after_time_check = Event(2, "kiosk.after_time_check")
    kiosk_fallback         = Event(2, "kiosk_fallback")
    kiosk_snack_fallback   = Event(2, "kiosk_snack_fallback")
    kiosk_person_fallback  = Event(2, "kiosk_person_fallback")

    kiosk_timed_event = EventStorage("kiosk", "", kiosk_after_time_check)
    kiosk_events = {
        "snack":    EventStorage("snack",    "Get a snack",      kiosk_snack_fallback ),
        "students": EventStorage("students", "Talk to students", kiosk_person_fallback),
    }
    
    kiosk_timed_event.add_event(Event(1,
        ["first_week_kiosk_event"],
        TimeCondition(day = "2-4", month = 1, year = 2023),
    ))
    


    kiosk_timed_event.check_all_events()
    map(lambda x: x.check_all_events(), kiosk_events.values())

    kiosk_bg_images = [
        BGImage("images/background/kiosk/bg f <name> <level> <nude> <variant>.jpg", 2, OR(TimeCondition(daytime = "f"), TimeCondition(daytime = "c", weekday = "w"))), # show kiosk with students
        BGImage("images/background/kiosk/bg f <name> <level> <nude>.jpg", 1, OR(TimeCondition(daytime = "f"), TimeCondition(daytime = "c", weekday = "w"))), # show kiosk with students
        BGImage("images/background/kiosk/bg 7.jpg", 1, TimeCondition(daytime = 7)), # show kiosk at night empty
    ]
    
###################################

#################################
# ----- Kiosk Entry Point ----- #
#################################

label kiosk ():

    call call_available_event(kiosk_timed_event) from kiosk_1

label .after_time_check (**kwargs):

    $ school_obj = get_random_school()

    call show_kiosk_idle_image(school_obj) from kiosk_2

    call call_event_menu (
        "What to do at the Kiosk?", 
        kiosk_events, 
        kiosk_fallback,
        character.subtitles,
        char_obj = school_obj,
    ) from kiosk_3

    jump kiosk

label show_kiosk_idle_image(school_obj):

    $ max_nude, image_path = get_background(
        "images/background/kiosk/bg c.jpg", # show kiosk empty
        kiosk_bg_images,
        school_obj,
    )

    call show_image_with_nude_var (image_path, max_nude) from _call_show_image_with_nude_var_8

    return

#################################

#####################################
# ----- Kiosk Fallback Events ----- #
#####################################

label kiosk_fallback (**kwargs):
    subtitles "There is nothing to see here."
    jump map_overview

label kiosk_snack_fallback (**kwargs):
    subtitles "I don't want anything."
    jump map_overview

label kiosk_person_fallback (**kwargs):
    subtitles "There is nobody here."
    jump map_overview

#####################################

############################
# ----- Kiosk Events ----- #
############################

# first week event
label first_week_kiosk_event (**kwargs):

    show first week kiosk 1 with dissolveM
    headmaster_thought "Now, somewhere here should be the kiosk..."
    show first week kiosk 2 with dissolveM
    headmaster_thought "Hmm, why is it so crowded?"

    show first week kiosk 3 with dissolveM
    headmaster "Excuse me, did something happen? Why is it so crowded here?"
    
    show first week kiosk 4 with dissolveM
    sgirl "What do you mean? It's always this full. We can't get food anywhere else than here." (name = "Lin Kato")
    
    show first week kiosk 3 with dissolveM
    headmaster "Oh I understand... Thanks."

    show first week kiosk 5 with dissolveM
    headmaster_thought "This is not acceptable. Did the former headmaster really close the kiosk?"
    headmaster_thought "That can't be right..."

    $ change_stat_for_all("reputation", 5, charList['schools'])

    $ set_building_blocked("kiosk")

    jump new_day

############################