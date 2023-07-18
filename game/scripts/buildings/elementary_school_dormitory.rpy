#########################################################
# ----- Elementary School Dormitory Event Handler ----- #
#########################################################

init -1 python:
    elementary_school_dormitory_after_time_check = Event("elementary_school_dormitory_after_time_check", "elementary_school_dormitory.after_time_check", 2)
    elementary_school_dormitory_fallback         = Event("elementary_school_dormitory_fallback",         "elementary_school_dormitory_fallback",         2)
    elementary_school_dormitory_person_fallback  = Event("elementary_school_dormitory_person_fallback",  "elementary_school_dormitory_person_fallback",  2)

    elementary_school_dormitory_timed_event = EventStorage("elementary_school_dormitory", "", elementary_school_dormitory_after_time_check)
    elementary_school_dormitory_events = {
        "check_rooms":   EventStorage("check_rooms",   "Check Rooms",      elementary_school_dormitory_person_fallback),
        "talk_students": EventStorage("talk_students", "Talk to students", elementary_school_dormitory_person_fallback),
        "patrol":        EventStorage("patrol",        "Patrol building",  elementary_school_dormitory_person_fallback),
        "peek_students": EventStorage("peek_students", "Peek on students", elementary_school_dormitory_person_fallback),
    }
    
    elementary_school_dormitory_timed_event.add_event(Event(
        "first_week_event",
        ["first_week_elementary_school_dormitory_event"],
        1,
        TimeCondition(week = 1),
    ))


#######################################################
# ----- Elementary School Dormitory Entry Point ----- #
#######################################################

label elementary_school_dormitory:
    # show dorm corridor

    # if daytime in [1, 3, 6]:
    #     # show corridor filled with students and open doors
    # if daytime in [2, 4, 5]:
    #     # show empty corridor
    # if daytime in [7]:
    #     # show empty corridor at night

    call call_available_event(elementary_school_dormitory_timed_event) from _call_call_available_event_4
    
label .after_time_check:

    call call_event_menu (
        "What to do in the Elementary School Dorm?",
        1, 
        7, 
        elementary_school_dormitory_events, 
        elementary_school_dormitory_fallback,
    ) from _call_call_event_menu_4

    jump elementary_school_dormitory

###########################################################
# ----- Elementary School Dormitory Fallback Events ----- #
###########################################################

label elementary_school_dormitory_fallback:
    subtitles "There is nothing to do here."
    return

label elementary_school_dormitory_person_fallback:
    subtitles "There is nobody here."
    return

##################################################
# ----- Elementary School Dormitory Events ----- #
##################################################

# first week event
label first_week_elementary_school_dormitory_event:
    subtitles "todo: first_week_event"

    $ set_building_blocked("high_school_dormitory")
    $ set_building_blocked("middle_school_dormitory")
    $ set_building_blocked("elementary_school_dormitory")

    jump new_day
