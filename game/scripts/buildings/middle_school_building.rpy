####################################################
# ----- Middle School Building Event Handler ----- #
####################################################

init -1 python:
    msb_timed_event = EventStorage("middle_school_building", "", Event(2, "middle_school_building.after_time_check"))
    msb_events = {
        "check_class": EventStorage("check_class", "Check Class",      default_fallback, "There is nobody here."),
        "teach_class": EventStorage("teach_class", "Teach a Class",    default_fallback, "There is nobody here."),
        "patrol":      EventStorage("patrol",      "Patrol building",  default_fallback, "There is nobody here."),
        "students":    EventStorage("strudents",   "Talk to students", default_fallback, "There is nobody here."),
    }

    msb_timed_event.add_event(Event(1,
        ["first_week_middle_school_building_event"],
        TimeCondition(day = "2-4", month = 1, year = 2023),
    ))
    
    msb_timed_event.add_event(Event(1,
        ["first_potion_middle_school_building_event"],
        TimeCondition(day = 9),
    ))



    msb_timed_event.check_all_events()
    map(lambda x: x.check_all_events(), msb_events.values())

    msb_bg_images = [
        BGImage("images/background/middle school building/bg c <level> <nude>.webp", 1, TimeCondition(daytime = "c", weekday = "d")),
        BGImage("images/background/middle school building/bg 7.webp", 1, TimeCondition(daytime = 7)),
    ]
    
####################################################

##################################################
# ----- Middle School Building Entry Point ----- #
##################################################

label middle_school_building ():
    
    call call_available_event(msb_timed_event) from middle_school_building_1

label .after_time_check (**kwargs):

    $ school_obj = get_character("middle_school", charList["schools"])

    call show_idle_image(school_obj, "images/background/middle school building/bg f.webp", msb_bg_images) from middle_school_building_2

    call call_event_menu (
        "What to do in the Middle School?", 
        msb_events, 
        default_fallback,
        character.subtitles,
        char_obj = school_obj,
    ) from middle_school_building_3

    jump middle_school_building

##################################################

#############################################
# ----- Middle School Building Events ----- #
#############################################

label first_potion_middle_school_building_event (**kwargs):
    
    show first potion middle school building 1 with dissolveM
    headmaster_thought "Let's see how classes are today."
    
    show first potion middle school building 2 with dissolveM
    subtitles "You look into a classroom and the first thing you notice is that almost everyone has opened up or at least partially removed their clothes."
    subtitles "Apparently the teachers also took a drink."
    headmaster_thought "Hmm, I can't wait to have this view on a regular basis, but that's gonna take some time."

    $ set_building_blocked("high_school_building")
    $ set_building_blocked("middle_school_building")
    $ set_building_blocked("elementary_school_building")

    jump new_daytime


# first week event
label first_week_middle_school_building_event (**kwargs):
    show first week high school building 1 with dissolveM
    subtitles """You enter the main building of the high school.
        
        Well, you don't really need to enter the building to get an idea of the state it's in."""
        
    show first week high school building 2 with dissolveM
    headmaster_thought """Despite my fear, the building seems to be rather well maintained.

        It could be a bit cleaner but the corridor seems rather well.

        Let's see the classrooms."""
    
    show first week high school building 3 with dissolveM
    headmaster_thought "Oh not bad as well. "

    show first week high school building 4 with dissolveM
    headmaster_thought "Hmm I think there should be a class right now, let's check."

    show first week high school building 6 with dissolveM
    headmaster_thought "Hmm looks like a normal class, but I think the students have no material?"
    headmaster_thought "Yeah, not one school girl has even one book."
    headmaster_thought "I guess the former headmaster cut back on those"

    $ change_stat_for_all("education", 5, charList["schools"])

    $ set_building_blocked("high_school_building")
    $ set_building_blocked("middle_school_building")
    $ set_building_blocked("elementary_school_building")

    jump new_day
    
#############################################