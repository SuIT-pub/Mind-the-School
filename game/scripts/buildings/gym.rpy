#################################
# ----- Gym Event Handler ----- #
#################################

init -1 python:
    gym_after_time_check = Event("gym_after_time_check", "gym.after_time_check", 2)
    gym_fallback         = Event("gym_fallback",         "gym_fallback",         2)
    gym_person_fallback  = Event("gym_person_fallback",  "gym_person_fallback",  2)

    gym_timed_event = EventStorage("gym", "", gym_after_time_check)
    gym_events = {
        "teacher":        EventStorage("teacher",        "Go to teacher",                      gym_person_fallback),
        "students":       EventStorage("students",       "Go to students",                     gym_person_fallback),
        "storage":        EventStorage("storage",        "Check storage",                      gym_fallback       ),
        "peek_changing":  EventStorage("peek_changing",  "Go to Peek into the changing rooms", gym_person_fallback),
        "enter_changing": EventStorage("enter_changing", "Enter the changing rooms",           gym_fallback       ),
        "steal":          EventStorage("steal",          "Steal some panties",                 gym_fallback       ),
    }

    gym_timed_event.add_event(Event(
        "first_week_event",
        ["first_week_gym_event"],
        1,
        TimeCondition(day = "2-4", month = 1, year = 2023),
    ))

    
    gym_timed_event.add_event(Event(
        "first_potion_event",
        ["first_potion_gym_event"],
        1,
        TimeCondition(day = 9),
    ))

    gym_bg_images = [
        BGImage("images/background/gym/bg c <school> <level> <nude>.jpg", 1, TimeCondition(daytime = "c", weekday = "d")), # show gym with students
        BGImage("images/background/gym/bg 7.jpg", 1, TimeCondition(daytime = 7)), # show gym at night empty
    ]
    
#################################

###############################
# ----- Gym Entry Point ----- #
###############################

label gym:

    call call_available_event(gym_timed_event) from gym_1

label .after_time_check:

    $ school = get_random_school()

    call show_gym_idle_image(school) from gym_2

    call call_event_menu (
        "What to do in the Gym?",
        1, 
        7, 
        gym_events, 
        gym_fallback,
        character.subtitles,
        school,
    ) from gym_3

    jump gym

label show_gym_idle_image(school_name):

    $ max_nude, image_path = get_background(
        "images/background/gym/bg f.jpg", # show gym empty
        gym_bg_images,
        get_level_for_char(school_name, charList["schools"]),
        school = school_name
    )

    call show_image_with_nude_var (image_path, max_nude) from _call_show_image_with_nude_var_5

    return

###############################

###################################
# ----- Gym Fallback Events ----- #
###################################

label gym_fallback:
    subtitles "There is nothing to see here."
    return

label gym_person_fallback:
    subtitles "There is nobody here."
    return

###################################

##########################
# ----- Gym Events ----- #
##########################

label first_potion_gym_event:
    show first potion gym 1 with dissolveM
    subtitles "You enter the Gym and see a group of students and teacher in a yoga session."

    show first potion gym 2 with dissolveM
    headmaster_thought "Oh that is a sport session I can get behind!"

    show first potion gym 3 with dissolveM
    headmaster_thought "Mhh, yes very flexible!"

    show first potion gym 4 with dissolveM
    headmaster_thought "Oh they seem to really get into it!"

    $ set_building_blocked("gym")

    jump new_daytime


# first week event
label first_week_gym_event:
    show first week gym 1 with dissolveM
    headmaster_thought "Okay, now the Gym. I have been here shortly for my introduction speech but I haven't had the chance to get a thorough look."

    show first week gym 2 with dissolveM
    headmaster_thought "Mhh, doesn't look to shabby..."
    
    show first week gym 3 with dissolveM
    headmaster_thought "Seems to be decently stocked."
    headmaster_thought "The material is well maintained. I guess it's alright."

    $ set_stat_for_all("charm", 15, charList["schools"])

    $ set_building_blocked("gym")

    jump new_day

#############################
# weekly assembly entry point
label weekly_assembly:

    subtitles "todo: weekly assembly"

    return
