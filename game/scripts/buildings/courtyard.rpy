#######################################
# ----- Courtyard Event Handler ----- #
#######################################

init -1 python:
    courtyard_after_time_check = Event("courtyard_after_time_check", "courtyard.after_time_check", 2)
    courtyard_fallback         = Event("courtyard_fallback",         "courtyard_fallback",         2)
    courtyard_person_fallback  = Event("courtyard_person_fallback",  "courtyard_person_fallback",  2)

    courtyard_timed_event = EventStorage("courtyard", "", courtyard_after_time_check)
    courtyard_events = {
        "talk_student": EventStorage("talk_student", "Talk with students", courtyard_person_fallback),
        "talk_teacher": EventStorage("talk_teacher", "Talk with teacher",  courtyard_person_fallback),
        "patrol":       EventStorage("patrol",       "Patrol",             courtyard_person_fallback),
    }
    
    courtyard_timed_event.add_event(Event(
        "first_week_event",
        ["first_week_courtyard_event"],
        1,
        TimeCondition(day = "2-4", month = 1, year = 2023),
    ))
    
    courtyard_timed_event.add_event(Event(
        "first_potion_event",
        ["first_potion_courtyard_event"],
        1,
        TimeCondition(day = 9),
    ))

    courtyard_bg_images = [
        BGImage("images/background/courtyard/bg 1,6 <school> <level> <nude>.jpg", 1, TimeCondition(daytime = "1,6")), # show courtyard with a few students
        BGImage("images/background/courtyard/bg 1,6 <school> <level> <nude>.jpg", 1, TimeCondition(daytime = "c", weekday = "w")), # show courtyard with a few students
        BGImage("images/background/courtyard/bg 3 <school> <level> <nude>.jpg", 1, TimeCondition(daytime = 3)), # show courtyard full of students and teacher
        BGImage("images/background/courtyard/bg 7.jpg", 1, TimeCondition(daytime = 7)), # show empty courtyard at night
    ]
    
#######################################

#####################################
# ----- Courtyard Entry Point ----- #
#####################################

label courtyard:

    call call_available_event(courtyard_timed_event) from courtyard_1

label .after_time_check:

    $ school = get_random_school()

    call show_courtyard_idle_image(school) from courtyard_2

    call call_event_menu (
        "What to do at the Courtyard?",
        1, 
        7, 
        courtyard_events, 
        courtyard_fallback,
        character.subtitles,
        school,
    ) from courtyard_3

    jump courtyard

label show_courtyard_idle_image(school_name):

    $ max_nude, image_path = get_background(
        "images/background/courtyard/bg c.jpg", # show empty courtyard
        courtyard_bg_images,
        get_level_for_char(school_name, charList["schools"]),
        school = school_name
    )

    call show_image_with_nude_var (image_path, max_nude) from _call_show_image_with_nude_var_2

    return

#####################################

#########################################
# ----- Courtyard Fallback Events ----- #
#########################################

label courtyard_fallback:
    subtitles "There is nothing to see here."
    return
label courtyard_person_fallback:
    subtitles "There is nobody here."
    return

#########################################

################################
# ----- Courtyard Events ----- #
################################

label first_potion_courtyard_event:

    show first potion courtyard 1 with dissolveM
    subtitles "You walk around in the courtyard."

    show first potion courtyard 2 with dissolveM
    subtitles "The first thing you notice is the group of students sunbathing in the middle of the yard."
    
    show first potion courtyard 3 with dissolveM
    subtitles "Normally that wouldn't be such a weird thing, if they weren't in only their underwear."
    headmaster_thought "I certainly enjoy the view. Unfortunately it only lasts for today until the serum finishes settling in their bodies."

    $ set_building_blocked("courtyard")

    jump new_daytime


# first week event
label first_week_courtyard_event:
    show first week courtyard 1 with dissolveM
    subtitles "You walk through the courtyard."

    headmaster_thought "Hmm, the courtyard looks really bad..."
    
    show first week courtyard 2 with dissolveM
    headmaster_thought "Tt seems most of the appliances here are out of order."

    show first week courtyard 3 with dissolveM
    headmaster_thought "For example the public toilet is broken."

    show first week courtyard 4 with dissolveM
    headmaster_thought "At least the courtyard doesn't need immediate fixing."

    $ set_stat_for_all("happiness", 12, charList["schools"])

    $ set_building_blocked("courtyard")

    jump new_day

################################