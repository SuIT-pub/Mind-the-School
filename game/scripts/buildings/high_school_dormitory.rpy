###################################################
# ----- High School Dormitory Event Handler ----- #
###################################################

init -1 python:
    high_school_dormitory_after_time_check = Event(2, "high_school_dormitory.after_time_check")
    high_school_dormitory_fallback         = Event(2, "high_school_dormitory_fallback")
    high_school_dormitory_person_fallback  = Event(2, "high_school_dormitory_person_fallback")

    high_school_dormitory_timed_event = EventStorage("high_school_dormitory", "", high_school_dormitory_after_time_check)
    high_school_dormitory_events = {
        "check_rooms":   EventStorage("check_rooms",   "Check Rooms",      high_school_dormitory_person_fallback),
        "talk_students": EventStorage("talk_students", "Talk to students", high_school_dormitory_person_fallback),
        "patrol":        EventStorage("patrol",        "Patrol building",  high_school_dormitory_person_fallback),
        "peek_students": EventStorage("peek_students", "Peek on students", high_school_dormitory_person_fallback),
    }

    high_school_dormitory_timed_event.add_event(Event(1,
        ["first_week_high_school_dormitory_event"],
        TimeCondition(day = "2-4", month = 1, year = 2023),
    ))

    high_school_dormitory_timed_event.add_event(Event(1,
        ["first_potion_high_school_dormitory_event"],
        TimeCondition(day = 9),
    ))

    event1 = Event(3, 
        ["sd_event_1", "sd_event_2"],
        OR(TimeCondition(weekday = "d", daytime = "f"), TimeCondition(daytime = "d", weekday = "w"))
    )

    high_school_dormitory_events["check_rooms"].add_event(event1)
    high_school_dormitory_events["peek_students"].add_event(event1)

    high_school_dormitory_timed_event.check_all_events()
    map(lambda x: x.check_all_events(), high_school_dormitory_events.values())

    high_school_dormitory_bg_images = [
        BGImage("images/background/high school dormitory/bg f <level> <nude>.jpg", 1, TimeCondition(daytime = "f")),
        BGImage("images/background/high school dormitory/bg f <level> <nude>.jpg", 1, TimeCondition(daytime = "c", weekday = "w")),
        BGImage("images/background/high school dormitory/bg 7.jpg", 1, TimeCondition(daytime = 7)),
    ]
    
###################################################

#################################################
# ----- High School Dormitory Entry Point ----- #
#################################################

label high_school_dormitory ():
    
    call call_available_event(high_school_dormitory_timed_event) from high_school_dormitory_1

label .after_time_check (**kwargs):

    $ school_obj = get_character("high_school", charList["schools"])

    call show_high_school_dormitory_idle_image(school_obj) from high_school_dormitory_2

    call call_event_menu (
        "What to do in the High School Dorm?", 
        high_school_dormitory_events, 
        high_school_dormitory_fallback,
        character.subtitles,
        char_obj = school_obj,
    ) from high_school_dormitory_3

    jump high_school_dormitory

label show_high_school_dormitory_idle_image(school_obj):

    $ max_nude, image_path = get_background(
        "images/background/high school dormitory/bg c.jpg",
        high_school_dormitory_bg_images,
        school_obj,
    )

    call show_image_with_nude_var (image_path, max_nude) from _call_show_image_with_nude_var_7

    return

#################################################

#####################################################
# ----- High School Dormitory Fallback Events ----- #
#####################################################

label high_school_dormitory_fallback (**kwargs):
    subtitles "There is nothing to do here."
    jump map_overview

label high_school_dormitory_person_fallback (**kwargs):
    subtitles "There is nobody here."
    jump map_overview

#####################################################

############################################
# ----- High School Dormitory Events ----- #
############################################

# first week event
label first_week_high_school_dormitory_event (**kwargs):
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

    $ change_stat_for_all("inhibition", -3, charList["schools"])
    $ change_stat_for_all("happiness", 3, charList["schools"])

    $ set_building_blocked("high_school_dormitory")
    $ set_building_blocked("middle_school_dormitory")
    $ set_building_blocked("elementary_school_dormitory")

    jump new_day


label first_potion_high_school_dormitory_event (**kwargs):

    show first potion dormitory 1 with dissolveM
    subtitles "You enter the dormitory of the high school."
    headmaster_thought "Mhh, where does the noise come from?"

    show first potion dormitory 2 with dissolveM
    headmaster_thought "Ah I think there are some students in the room over there."

    show first potion high school dormitory 2 with dissolveM
    headmaster_thought "Ahh party games!"

    show first potion high school dormitory 3 with dissolveM
    if time.check_daytime("c"):
        headmaster_thought "Normally I would scold them for skipping class but today is a special day so I gladly enjoy this view."
    else:
        headmaster_thought "Ahh I like this view. Nothing more erotic than nudity in combination with a party game."

    $ set_building_blocked("high_school_dormitory")
    $ set_building_blocked("middle_school_dormitory")
    $ set_building_blocked("elementary_school_dormitory")

    jump new_daytime


############################################