####################################################
# ----- Middle School Building Event Handler ----- #
####################################################

init -1 python:
    middle_school_building_after_time_check = Event("middle_school_building_after_time_check", "middle_school_building.after_time_check", 2)
    middle_school_building_fallback         = Event("middle_school_building_fallback",         "middle_school_building_fallback",         2)
    middle_school_building_person_fallback  = Event("middle_school_building_person_fallback",  "middle_school_building_person_fallback",  2)

    middle_school_building_timed_event = EventStorage("middle_school_building", "", middle_school_building_after_time_check)
    middle_school_building_events = {
        "check_class": EventStorage("check_class", "Check Class",      middle_school_building_person_fallback),
        "teach_class": EventStorage("teach_class", "Teach a Class",    middle_school_building_person_fallback),
        "patrol":      EventStorage("patrol",      "Patrol building",  middle_school_building_person_fallback),
        "students":    EventStorage("strudents",   "Talk to students", middle_school_building_person_fallback),
    }

    middle_school_building_timed_event.add_event(Event(
        "first_week_event",
        ["first_week_middle_school_building_event"],
        1,
        TimeCondition(day = "2-4", month = 1, year = 2023),
    ))
    
    middle_school_building_timed_event.add_event(Event(
        "first_potion_event",
        ["first_potion_middle_school_building_event"],
        1,
        TimeCondition(day = 9),
    ))


##################################################
# ----- Middle School Building Entry Point ----- #
##################################################

label middle_school_building:
    
    $ image_path = "images/background/middle school building/bg f.png"

    if time.check_daytime("c"):
        $ image_path = get_image_with_level(
            "images/background/middle school building/bg c {level} {nude}.png", 
            "middle_school", 
            charList["schools"]
        )

    if time.check_daytime(7):
        $ image_path = "images/background/middle school building/bg 7.png"

    show screen image_with_nude_var (image_path, 0)


    call call_available_event(middle_school_building_timed_event) from _call_call_available_event_10

label .after_time_check:

    call call_event_menu (
        "What to do in the Middle School?",
        1, 
        7, 
        middle_school_building_events, 
        middle_school_building_fallback
    ) from _call_call_event_menu_10

    jump middle_school_building

######################################################
# ----- Middle School Building Fallback Events ----- #
######################################################

label middle_school_building_fallback:
    subtitles "There is nothing to do here."
    return
label middle_school_building_person_fallback:
    subtitles "There is nobody here."
    return

###########################################
# ----- Middle School Building Events ----- #
###########################################

label first_potion_middle_school_building_event:
    
    show first potion middle school building 1
    principal_thought "Let's see how classes are today."
    
    show first potion middle school building 2
    subtitles "You look into a classroom and the first thing you notice is that almost everyone has opened up or at least partially removed their clothes."
    subtitles "Apparently the teachers also took a drink."
    principal_thought "Hmm, I can't wait to have this view on a regular basis, but that's gonna take some time."

    $ set_building_blocked("high_school_building")
    $ set_building_blocked("middle_school_building")
    $ set_building_blocked("elementary_school_building")

    jump new_daytime


# first week event
label first_week_middle_school_building_event:
    show first week high school building 1
    subtitles """You enter the main building of the high school.
        
        Well, you don't really need to enter the building to get an idea of the state it's in."""
        
    show first week high school building 2
    principal_thought """Despite my fear, the building seems to be rather well maintained.

        It could be a bit cleaner but the corridor seems rather well.

        Let's see the classrooms."""
    
    show first week high school building 3
    principal_thought "Oh not bad as well. "

    show first week high school building 4
    principal_thought "Hmm I think there should be a class right now, let's check."

    show first week high school building 6
    principal_thought "Hmm looks like a normal class, but I think the students have no material?"
    principal_thought "Yeah, not one school girl has even one book."
    principal_thought "I guess the former principal cut back on those"

    $ set_stat_for_all("education", 15, schools)

    $ set_building_blocked("high_school_building")
    $ set_building_blocked("middle_school_building")
    $ set_building_blocked("elementary_school_building")

    jump new_day