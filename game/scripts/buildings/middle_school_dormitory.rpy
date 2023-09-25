#####################################################
# ----- Middle School Dormitory Event Handler ----- #
#####################################################

init -1 python:
    middle_school_dormitory_after_time_check = Event("middle_school_dormitory_after_time_check", "middle_school_dormitory.after_time_check", 2)
    middle_school_dormitory_fallback         = Event("middle_school_dormitory_fallback",         "middle_school_dormitory_fallback",         2)
    middle_school_dormitory_person_fallback  = Event("middle_school_dormitory_person_fallback",  "middle_school_dormitory_person_fallback",  2)

    middle_school_dormitory_timed_event = EventStorage("middle_school_dormitory", "", middle_school_dormitory_after_time_check)
    middle_school_dormitory_events = {
        "check_rooms":   EventStorage("check_rooms",   "Check Rooms",      middle_school_dormitory_person_fallback),
        "talk_students": EventStorage("talk_students", "Talk to students", middle_school_dormitory_person_fallback),
        "patrol":        EventStorage("patrol",        "Patrol building",  middle_school_dormitory_person_fallback),
        "peek_students": EventStorage("peek_students", "Peek on students", middle_school_dormitory_person_fallback),
    }
    
    middle_school_dormitory_timed_event.add_event(Event(
        "first_week_event",
        ["first_week_middle_school_dormitory_event"],
        1,
        TimeCondition(day = "2-4", month = 1, year = 2023),
    ))
    
    middle_school_dormitory_timed_event.add_event(Event(
        "first_potion_event",
        ["first_potion_middle_school_dormitory_event"],
        1,
        TimeCondition(day = 9),
    ))

    middle_school_dormitory_bg_images = [
        BGImage("images/background/middle school dormitory/bg f <level> <nude>.jpg", 1, TimeCondition(daytime = "f")),
        BGImage("images/background/middle school dormitory/bg f <level> <nude>.jpg", 1, TimeCondition(daytime = "c", weekday = "w")),
        BGImage("images/background/middle school dormitory/bg 7.jpg", 1, TimeCondition(daytime = 7)),
    ]
    
#####################################################

###################################################
# ----- Middle School Dormitory Entry Point ----- #
###################################################

label middle_school_dormitory:
    
    call call_available_event(middle_school_dormitory_timed_event) from middle_school_dormitory_1

label .after_time_check:

    call show_middle_school_dormitory_idle_image() from middle_school_dormitory_2

    call call_event_menu (
        "What to do in the Middle School Dorm?",
        1, 
        7, 
        middle_school_dormitory_events, 
        middle_school_dormitory_fallback,
        character.subtitles,
        "middle_school",
    ) from middle_school_dormitory_3

    jump middle_school_dormitory

label show_middle_school_dormitory_idle_image():

    $ max_nude, image_path = get_background(
        "images/background/middle school dormitory/bg c.jpg",
        middle_school_dormitory_bg_images,
        get_level_for_char("middle_school", charList["schools"]),
    )

    call show_image_with_nude_var (image_path, max_nude) from _call_show_image_with_nude_var_11

    return

###################################################

#######################################################
# ----- Middle School Dormitory Fallback Events ----- #
#######################################################

label middle_school_dormitory_fallback:
    subtitles "There is nothing to do here."
    return

label middle_school_dormitory_person_fallback:
    subtitles "There is nobody here."
    return

#######################################################

##############################################
# ----- Middle School Dormitory Events ----- #
##############################################

label first_potion_middle_school_dormitory_event:

    show first potion dormitory 1 with dissolveM
    subtitles "You enter the dormitory of the middle school."
    headmaster_thought "Mhh, where does the noise come from?"

    show first potion dormitory 2 with dissolveM
    headmaster_thought "Ah I think there are some students in the room over there."

    show first potion middle school dormitory 2 with dissolveM
    headmaster_thought "Ahh party games!"

    show first potion middle school dormitory 3 with dissolveM
    if time.check_daytime("c"):
        headmaster_thought "Normally I would scold them for skipping class but today is a special day so I gladly enjoy this view."
    else:
        headmaster_thought "Ahh I like this view. Nothing more erotic than nudity in combination with a party game."

    $ set_building_blocked("high_school_dormitory")
    $ set_building_blocked("middle_school_dormitory")
    $ set_building_blocked("elementary_school_dormitory")

    jump new_daytime

# first week event
label first_week_middle_school_dormitory_event:
    
    show first week high school dormitory 1 with dissolveM
    headmaster_thought "The dormitory looks alright."

    show first week high school dormitory 2 with dissolveM
    headmaster_thought "As far as I know, the students have to share a communal bathroom."
    headmaster_thought "Private bathrooms would be nice for the students, but for one I don't think we really need that and then it would need a lot of rebuilding. So that should be last on the list."
    
    show first week high school dormitory 3 with dissolveM
    headmaster_thought "Let's see if someone would let me see their room so I can check the state of these."
    
    show first week high school dormitory 4 with dissolveM
    headmaster "Hello? I'm Mr. [headmaster_last_name] the new Headmaster. Can I come in? I'm here to inspect the building."
    subtitles "..."
    headmaster "Hello?"

    show first week high school dormitory 5 with dissolveM
    headmaster_thought "Hmm nobody seems to be here. Nevermind. I just let my Secretary give me a report."

    $ set_stat_for_all("inhibition", 2, charList["schools"])

    $ set_building_blocked("high_school_dormitory")
    $ set_building_blocked("middle_school_dormitory")
    $ set_building_blocked("elementary_school_dormitory")

    jump new_day

##############################################