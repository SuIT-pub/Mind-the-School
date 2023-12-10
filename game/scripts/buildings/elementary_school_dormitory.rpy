#########################################################
# ----- Elementary School Dormitory Event Handler ----- #
#########################################################

init -1 python:
    esd_timed_event = EventStorage("elementary_school_dormitory", "", Event(2, "elementary_school_dormitory.after_time_check"))
    esd_events = {
        "check_rooms":   EventStorage("check_rooms",   "Check Rooms",      default_fallback, "There is nobody here."),
        "talk_students": EventStorage("talk_students", "Talk to students", default_fallback, "There is nobody here."),
        "patrol":        EventStorage("patrol",        "Patrol building",  default_fallback, "There is nobody here."),
        "peek_students": EventStorage("peek_students", "Peek on students", default_fallback, "There is nobody here."),
    }
    
    esd_timed_event.add_event(Event(1,
        ["first_week_elementary_school_dormitory_event"],
        TimeCondition(day = "2-4", month = 1, year = 2023),
    ))

    esd_timed_event.add_event(Event(1,
        ["first_potion_elementary_school_dormitory_event"],
        TimeCondition(day = 9, month = 1, year = 2023),
    ))



    esd_timed_event.check_all_events()
    map(lambda x: x.check_all_events(), esd_events.values())

    esd_bg_images = [
        BGImage("images/background/elementary school dormitory/bg f <level> <nude>.webp", 1, TimeCondition(daytime = "f")),
        BGImage("images/background/elementary school dormitory/bg f <level> <nude>.webp", 1, TimeCondition(daytime = "c", weekday="w")),
        BGImage("images/background/elementary school dormitory/bg 7.webp", 1, TimeCondition(daytime = 7)),
    ]
    
#########################################################

#######################################################
# ----- Elementary School Dormitory Entry Point ----- #
#######################################################

label elementary_school_dormitory ():

    call call_available_event(esd_timed_event) from elementary_school_dormitory_1
    
label .after_time_check (**kwargs):

    $ school_obj = get_character("elementary_school", charList["schools"])

    call show_idle_image(school_obj, "images/background/elementary school dormitory/bg c.webp", esd_bg_images) from elementary_school_dormitory_2

    call call_event_menu (
        "What to do in the Elementary School Dorm?", 
        esd_events, 
        default_fallback,
        character.subtitles,
        char_obj = school_obj,
    ) from elementary_school_dormitory_3

    jump elementary_school_dormitory

#######################################################

##################################################
# ----- Elementary School Dormitory Events ----- #
##################################################

# first week event
label first_week_elementary_school_dormitory_event (**kwargs):
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
    headmaster_thought "Hmm nobody seems to be here. Forget it. I'll just let my Secretary give me a report."
    
    $ change_stat_for_all("inhibition", -3, charList["schools"])
    $ change_stat_for_all("happiness", 3, charList["schools"])

    $ set_building_blocked("high_school_dormitory")
    $ set_building_blocked("middle_school_dormitory")
    $ set_building_blocked("elementary_school_dormitory")

    jump new_day

label first_potion_elementary_school_dormitory_event (**kwargs):

    show first potion dormitory 1 with dissolveM
    subtitles "You enter the dormitory of the elementary school."
    headmaster_thought "Mhh, where does the noise come from?"

    show first potion dormitory 2 with dissolveM
    headmaster_thought "Ah I think there are some students in the room over there."

    show first potion elementary school dormitory 2 with dissolveM
    headmaster_thought "Ahh party games!"

    show first potion elementary school dormitory 3 with dissolveM
    if time.check_daytime("c"):
        headmaster_thought "Normally I would scold them for skipping class but today is a special day so I gladly enjoy this view."
    else:
        headmaster_thought "Ahh I like this view. Nothing more erotic than nudity in combination with a party game."

    $ set_building_blocked("high_school_dormitory")
    $ set_building_blocked("middle_school_dormitory")
    $ set_building_blocked("elementary_school_dormitory")

    jump new_daytime

##################################################