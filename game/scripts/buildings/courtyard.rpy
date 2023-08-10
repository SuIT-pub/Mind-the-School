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


#####################################
# ----- Courtyard Entry Point ----- #
#####################################

label courtyard:
    # show courtyard overview

    # if daytime in [1, 6]:
    #     # show courtyard with a few students
    # if daytime in [3]:
    #     # show courtyard full of students and teacher
    # if daytime in [2, 4, 5]:
    #     # show empty courtyard
    # if daytime in [7]
    #     # show empty courtyard at night

    call call_available_event(courtyard_timed_event) from _call_call_available_event_2

label .after_time_check:

    call call_event_menu (
        "What to do at the Courtyard?",
        1, 
        7, 
        courtyard_events, 
        courtyard_fallback,
    ) from _call_call_event_menu_2

    jump courtyard

#########################################
# ----- Courtyard Fallback Events ----- #
#########################################

label courtyard_fallback:
    subtitles "There is nothing to see here."
    return
label courtyard_person_fallback:
    subtitles "There is nobody here."
    return

################################
# ----- Courtyard Events ----- #
################################


label first_potion_courtyard_event:

    subtitles "You walk around in the courtyard."
    subtitles "The first thing you notice is the group of students sunbathing in the middle of the yard."
    subtitles "Normally that wouldn't be such a weird thing, if they weren't in only their underwear."
    principal_thought "I certainly enjoy the view. Unfortunately it only lasts for today until the serum finishes settling in their bodies."

    $ set_building_blocked("courtyard")

    jump new_daytime


# first week event
label first_week_courtyard_event:
    subtitles "You walk through the courtyard."

    principal_thought "Hmm, the courtyard doesn't look too bad. At least it is kept clean."
    principal_thought "But it seems most of the appliances here are out of order."
    principal_thought "For example the public toilet is broken."
    principal_thought "At least the courtyard doesn't need immediate fixing."

    $ set_stat_for_all("happiness", 12)

    $ set_building_blocked("courtyard")

    jump new_day
