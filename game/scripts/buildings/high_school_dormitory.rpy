###################################################
# ----- High School Dormitory Event Handler ----- #
###################################################

init -1 python:
    high_school_dormitory_after_time_check = Event("high_school_dormitory_after_time_check", "high_school_dormitory.after_time_check", 2)
    high_school_dormitory_fallback         = Event("high_school_dormitory_fallback",         "high_school_dormitory_fallback",         2)
    high_school_dormitory_person_fallback  = Event("high_school_dormitory_person_fallback",  "high_school_dormitory_person_fallback",  2)

    high_school_dormitory_timed_event = EventStorage("high_school_dormitory", "", high_school_dormitory_after_time_check)
    high_school_dormitory_events = {
        "check_rooms":   EventStorage("check_rooms",   "Check Rooms",      high_school_dormitory_person_fallback),
        "talk_students": EventStorage("talk_students", "Talk to students", high_school_dormitory_person_fallback),
        "patrol":        EventStorage("patrol",        "Patrol building",  high_school_dormitory_person_fallback),
        "peek_students": EventStorage("peek_students", "Peek on students", high_school_dormitory_person_fallback),
    }

    high_school_dormitory_timed_event.add_event(Event(
        "first_week_event",
        ["first_week_high_school_dormitory_event"],
        1,
        TimeCondition(day = "2-4", month = 1, year = 2023),
    ))

    high_school_dormitory_timed_event.add_event(Event(
        "first_potion_event",
        ["first_potion_high_school_dormitory_event"],
        1,
        TimeCondition(day = 9),
    ))

    high_school_dormitory_bg_images = [
        BGImage("images/background/high school dormitory/bg f <level> <nude>.png", 1, TimeCondition(daytime = "f")),
        BGImage("images/background/high school dormitory/bg f <level> <nude>.png", 1, TimeCondition(daytime = "c", weekday = "w")),
        BGImage("images/background/high school dormitory/bg 7.png", 1, TimeCondition(daytime = 7)),
    ]
    
###################################################

#################################################
# ----- High School Dormitory Entry Point ----- #
#################################################

label high_school_dormitory:
    
    call call_available_event(high_school_dormitory_timed_event) from high_school_dormitory_1

label .after_time_check:

    call show_high_school_dormitory_idle_image() from high_school_dormitory_2

    call call_event_menu (
        "What to do in the High School Dorm?",
        1, 
        7, 
        high_school_dormitory_events, 
        high_school_dormitory_fallback,
        character.subtitles,
        "high_school",
    ) from high_school_dormitory_3

    jump high_school_dormitory

label show_high_school_dormitory_idle_image():

    $ max_nude, image_path = get_background(
        "images/background/high school dormitory/bg c.png",
        high_school_dormitory_bg_images,
        get_level_for_char("high_school", charList["schools"]),
    )

    show screen image_with_nude_var (image_path, max_nude)

    return

#################################################

#####################################################
# ----- High School Dormitory Fallback Events ----- #
#####################################################

label high_school_dormitory_fallback:
    subtitles "There is nothing to do here."
    return

label high_school_dormitory_person_fallback:
    subtitles "There is nobody here."
    return

#####################################################

############################################
# ----- High School Dormitory Events ----- #
############################################

# first week event
label first_week_high_school_dormitory_event:
    principal_thought "The dormitory looks alright."
    principal_thought "As far as I know, the students have to share a communal bathroom."
    principal_thought "Private bathrooms would be nice for the students, but for one I don't think we really need that and then it would need a lot of rebuilding. So that should be last on the list."
    principal_thought "Let's see if someone would let me see their room so I can check the state of these."
    #klopft
    principal "Hello? I'm Mr. Izuku the new Headmaster. Can I come in? I'm here to inspect the building."
    subtitles "..."
    principal "Hello?"

    principal_thought "Hmm nobody seems to be here. Nevermind. I just let my Secretary give me a report."

    $ set_stat_for_all("inhibition", 2, charList["schools"])

    $ set_building_blocked("high_school_dormitory")
    $ set_building_blocked("middle_school_dormitory")
    $ set_building_blocked("elementary_school_dormitory")

    jump new_day


label first_potion_high_school_dormitory_event:

    show first potion dormitory 1
    subtitles "You enter the dormitory of the high school."
    principal_thought "Mhh, where does the noise come from?"

    show first potion dormitory 2
    principal_thought "Ah I think there are some students in the room over there."

    show first potion high school dormitory 2
    principal_thought "Ahh party games!"

    show first potion high school dormitory 3
    if time.check_daytime("c"):
        principal_thought "Normally I would scold them for skipping class but today is a special day so I gladly enjoy this view."
    else:
        principal_thought "Ahh I like this view. Nothing more erotic than nudity in combination with a party game."

    $ set_building_blocked("high_school_dormitory")
    $ set_building_blocked("middle_school_dormitory")
    $ set_building_blocked("elementary_school_dormitory")

    jump new_daytime


############################################