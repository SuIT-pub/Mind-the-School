##################################################
# ----- High School Building Event Handler ----- #
##################################################

init -1 python:
    high_school_building_after_time_check = Event("high_school_building_after_time_check", "high_school_building.after_time_check", 2)
    high_school_building_fallback         = Event("high_school_building_fallback",         "high_school_building_fallback",         2)
    high_school_building_person_fallback  = Event("high_school_building_person_fallback",  "high_school_building_person_fallback",  2)

    high_school_building_timed_event = EventStorage("high_school_building", "", high_school_building_after_time_check)
    high_school_building_events = {
        "check_class": EventStorage("check_class", "Check Class",      high_school_building_person_fallback),
        "teach_class": EventStorage("teach_class", "Teach a Class",    high_school_building_person_fallback),
        "patrol":      EventStorage("patrol",      "Patrol building",  high_school_building_person_fallback),
        "students":    EventStorage("students",    "Talk to students", high_school_building_person_fallback),
    }

    high_school_building_timed_event.add_event(Event(
        "first_week_event",
        ["first_week_high_school_building_event"],
        1,
        TimeCondition(day = "2-4", month = 1, year = 2023),
    ))

    high_school_building_timed_event.add_event(Event(
        "first_potion_event",
        ["first_potion_high_school_building_event"],
        1,
        TimeCondition(day = 9),
    ))

##################################################

################################################
# ----- High School Building Entry Point ----- #
################################################

label high_school_building:
    # show school corridor

    call call_available_event(high_school_building_timed_event) from _call_call_available_event_6

label .after_time_check:

    call show_high_school_building_idle_image()

    call call_event_menu (
        "What to do in the High School?",
        1, 
        7, 
        high_school_building_events, 
        high_school_building_fallback,
        character.subtitles,
        "high_school",
    ) from _call_call_event_menu_6

    jump high_school_building


label show_high_school_building_idle_image():    
    $ image_path = "images/background/high school building/bg f.png"

    if time.check_daytime("c"):
        $ image_path = get_image_with_level(
            "images/background/high school building/bg c <level> <nude>.png", 
            get_level_for_char("high_school", charList["schools"]),
        )
    elif time.check_daytime(7):
        $ image_path = "images/background/high school building/bg 7.png"

    show screen image_with_nude_var (image_path, 0)

    return

################################################

####################################################
# ----- High School Building Fallback Events ----- #
####################################################

label high_school_building_fallback:
    subtitles "There is nothing to do here."
    return
label high_school_building_person_fallback:
    subtitles "There is nobody here."
    return

####################################################

###########################################
# ----- High School Building Events ----- #
###########################################

# first week event
label first_week_high_school_building_event:
    
    $ hide_all()

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

label first_potion_high_school_building_event:

    show first potion high school building 1
    principal_thought "Let's see how classes are today."
    
    show first potion high school building 2
    subtitles "You look into a classroom and the first thing you notice is that almost everyone has opened up or at least partially removed their clothes."
    subtitles "Apparently the teachers also took a drink."
    principal_thought "Hmm, I can't wait to have this view on a regular basis, but that's gonna take some time."

    $ set_building_blocked("high_school_building")
    $ set_building_blocked("middle_school_building")
    $ set_building_blocked("elementary_school_building")

    jump new_daytime

# look through window, students concentrated
label hsb_peek_into_class_concentrated:
    subtitles "You are looking into one of the windows of a classroom."
    subtitles "The students are paying attention to the lesson."

    $ change_stat("education", renpy.random.random() * 0.25, "high_school", charList["schools"])

    return
    # jump new_daytime

# look through window, students not concentrated
label hsb_peek_into_class_not_concentrated:
    subtitles "You are looking into one of the windows of a classroom."
    subtitles "You see many students doing other things and the teacher struggling to get their attention."

    $ change_stat("education", renpy.random.random() - 1 * 0.5, "high_school", charList["schools"])

    return
    # jump new_daytime

# look thorugh window, students in chaos
label hsb_peek_into_class_chaos:
    subtitles "You are looking into one of the windows of a classroom."
    subtitles "Total Mayhem controls the classroom.\nYou see the teacher struggling to keep control of the class.{p}Maybe I should train the teachers more."

    $ change_stat("education", renpy.random.random() * -0.25, "high_school", charList["schools"])

    return
    # jump new_daytime

###########################################

###########################################
# ----- High School Building Scenes ----- #
###########################################


###########################################