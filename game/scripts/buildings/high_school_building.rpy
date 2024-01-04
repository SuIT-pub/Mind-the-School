##################################################
# ----- High School Building Event Handler ----- #
##################################################

init -1 python:
    hsb_timed_event = TempEventStorage("hsb", "", Event(2, "high_school_building.after_time_check"))
    hsb_events = {
        "check_class": EventStorage("check_class", "Check Class",      default_fallback, "There is nobody here."),
        "teach_class": EventStorage("teach_class", "Teach a Class",    default_fallback, "There is nobody here."),
        "patrol":      EventStorage("patrol",      "Patrol building",  default_fallback, "There is nobody here."),
        "students":    EventStorage("students",    "Talk to students", default_fallback, "There is nobody here."),
    }

    hsb_timed_event.add_event(Event(1,
        ["first_week_hsb_event"],
        TimeCondition(day = "2-4", month = 1, year = 2023),
    ))

    hsb_timed_event.add_event(Event(1,
        ["first_potion_hsb_event"],
        TimeCondition(day = 9, month = 1, year = 2023),
    ))

    event1 = Event(3, 
        ["sb_event_1"],
        TimeCondition(daytime = "c", weekday = "d"),
    )

    hsb_events["teach_class"].add_event(event1)
    hsb_events["teach_class"].add_event(Event(3,
        ["sb_event_2"],
        TimeCondition(daytime = "c", weekday = "d"),
    ))
    
    hsb_events["patrol"].add_event(event1)
    hsb_events["patrol"].add_event(Event(3, 
        ["sb_event_3"], 
        TimeCondition(daytime = "d")
    ))



    hsb_timed_event.check_all_events()
    map(lambda x: x.check_all_events(), hsb_events.values())

    hsb_bg_images = [
        BGImage("images/background/high school building/bg c <level> <nude>.webp", 1, TimeCondition(daytime = "c", weekday = "d")),
        BGImage("images/background/high school building/bg 7.webp", 1, TimeCondition(daytime = 7)),
    ]

##################################################

################################################
# ----- High School Building Entry Point ----- #
################################################

label high_school_building ():

    call call_available_event(hsb_timed_event) from high_school_building_1

label .after_time_check (**kwargs):

    $ school_obj = get_character("high_school", charList["schools"])

    call show_idle_image(school_obj, "images/background/high school building/bg f.webp", hsb_bg_images) from high_school_building_2

    call call_event_menu (
        "What to do in the High School?", 
        hsb_events,
        default_fallback,
        character.subtitles,
        char_obj = school_obj,
    ) from high_school_building_3

    jump high_school_building

################################################

###########################################
# ----- High School Building Events ----- #
###########################################

# first week event
label first_week_hsb_event (**kwargs):
    
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

label first_potion_hsb_event (**kwargs):

    show first potion high school building 1 with dissolveM
    headmaster_thought "Let's see how classes are today."
    
    show first potion high school building 2 with dissolveM
    subtitles "You look into a classroom and the first thing you notice is that almost everyone has opened up or at least partially removed their clothes."
    subtitles "Apparently the teachers also took a drink."
    headmaster_thought "Hmm, I can't wait to have this view on a regular basis, but that's gonna take some time."

    $ set_building_blocked("high_school_building")
    $ set_building_blocked("middle_school_building")
    $ set_building_blocked("elementary_school_building")

    jump new_daytime

###########################################

###########################################
# ----- High School Building Scenes ----- #
###########################################


###########################################