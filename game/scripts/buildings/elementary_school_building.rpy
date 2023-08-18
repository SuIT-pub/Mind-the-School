########################################################
# ----- Elementary School Building Event Handler ----- #
########################################################

init -1 python:
    elementary_school_building_after_time_check = Event("elementary_school_building_after_time_check", "elementary_school_building.after_time_check", 2)
    elementary_school_building_fallback         = Event("elementary_school_building_fallback",         "elementary_school_building_fallback",         2)
    elementary_school_building_person_fallback  = Event("elementary_school_building_person_fallback",  "elementary_school_building_person_fallback",  2)

    elementary_school_building_timed_event = EventStorage("elementary_school_building", "", elementary_school_building_after_time_check)
    elementary_school_building_events = {
        "check_class": EventStorage("check_class", "Check Class",      elementary_school_building_person_fallback),
        "teach_class": EventStorage("teach_class", "Teach a Class",    elementary_school_building_person_fallback),
        "patrol":      EventStorage("patrol",      "Patrol building",  elementary_school_building_person_fallback),
        "students":    EventStorage("strudents",   "Talk to students", elementary_school_building_person_fallback),
    }
    
    elementary_school_building_timed_event.add_event(Event(
        "first_week_event",
        ["first_week_elementary_school_building_event"],
        1,
        TimeCondition(day = "2-4", month = 1, year = 2023),
    ))

    
    elementary_school_building_timed_event.add_event(Event(
        "first_potion_event",
        ["first_potion_elementary_school_building_event"],
        1,
        TimeCondition(day = 9),
    ))

    elementary_school_building_bg_images = [
        BGImage("images/background/elementary school building/bg c <level> <nude>.png", 1, TimeCondition(daytime = "c")),
        BGImage("images/background/elementary school building/bg 7.png", 1, TimeCondition(daytime = 7)),
    ]
    
########################################################

######################################################
# ----- Elementary School Building Entry Point ----- #
######################################################

label elementary_school_building:
    
    call call_available_event(elementary_school_building_timed_event) from elementary_school_building_1

label .after_time_check:

    call show_elementary_school_building_idle_image() from elementary_school_building_2

    call call_event_menu (
        "What to do in the Elementary School?",
        1, 
        7, 
        elementary_school_building_events, 
        elementary_school_building_fallback,
        character.subtitles,
        "elementary_school",
    ) from elementary_school_building_3

    jump elementary_school_building

label show_elementary_school_building_idle_image():    
    
    $ max_nude, image_path = get_background(
        "images/background/elementary_school_building/bg f.png",
        elementary_school_building_bg_images,
        get_level_for_char("elementary_school", charList["schools"]),
    )

    show screen image_with_nude_var (image_path, max_nude)

    return

######################################################

##########################################################
# ----- Elementary School Building Fallback Events ----- #
##########################################################

label elementary_school_building_fallback:
    subtitles "There is nothing to do here."
    return
label elementary_school_building_person_fallback:
    subtitles "There is nobody here."
    return

##########################################################

#################################################
# ----- Elementary School Building Events ----- #
#################################################

label first_potion_elementary_school_building_event:
    
    show first potion elementary school building 1
    principal_thought "Let's see how classes are today."
    
    show first potion elementary school building 2
    subtitles "You look into a classroom and the first thing you notice is that almost everyone has opened up or at least partially removed their clothes."
    subtitles "Apparently the teachers also took a drink."
    principal_thought "Hmm, I can't wait to have this view on a regular basis, but that's gonna take some time."

    $ set_building_blocked("high_school_building")
    $ set_building_blocked("middle_school_building")
    $ set_building_blocked("elementary_school_building")

    jump new_daytime


# first week event
label first_week_elementary_school_building_event:
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

    $ set_stat_for_all("education", 15, charList["schools"])

    $ set_building_blocked("high_school_building")
    $ set_building_blocked("middle_school_building")
    $ set_building_blocked("elementary_school_building")

    jump new_day

#################################################