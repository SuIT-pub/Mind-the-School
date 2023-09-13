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
        BGImage("images/background/gym/bg c <school> <level> <nude>.png", 1, TimeCondition(daytime = "c", weekday = "d")), # show gym with students
        BGImage("images/background/gym/bg 7.png", 1, TimeCondition(daytime = 7)), # show gym at night empty
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
        "images/background/gym/bg f.png", # show gym empty
        gym_bg_images,
        get_level_for_char(school_name, charList["schools"]),
        school = school_name
    )

    show screen image_with_nude_var (image_path, max_nude)

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
    show first potion gym 1
    subtitles "You enter the Gym and see a group of students and teacher in a yoga session."

    show first potion gym 2
    principal_thought "Oh that is a sport session I can get behind!"

    show first potion gym 3
    principal_thought "Mhh, yes very flexible!"

    show first potion gym 4
    principal_thought "Oh they seem to really get into it!"

    $ set_building_blocked("gym")

    jump new_daytime


# first week event
label first_week_gym_event:
    show first week gym 1
    principal_thought "Okay, now the Gym. I have been here shortly for my introduction speech but I haven't had the chance to get a thorough look."

    show first week gym 2
    principal_thought "Mhh, doesn't look to shabby..."
    
    show first week gym 3
    principal_thought "Seems to be decently stocked."
    principal_thought "The material is well maintained. I guess it's alright."

    $ set_stat_for_all("charm", 15, charList["schools"])

    $ set_building_blocked("gym")

    jump new_day

#############################
# weekly assembly entry point
label weekly_assembly:

    subtitles "todo: weekly assembly"

    return

###################################
# first weekly assembly of the game
label weekly_assembly_first:

    scene expression "events/intro/intro gym 2 [loli_content].png"
    subtitles "You leave the office with the secretary and head for the Gym."
    
    #show inside gym with students walking towards their position in gym or talking to each other in groups by school
    subtitles "As you enter the hall, you'll be greeted by students standing all around the hall."
    
    #show move up stairs with secretary in front and clear view of butt
    scene expression "events/intro/intro gym 3 1.png"
    subtitles "As you and your secretary meak your way to the stage, all the students begin to form neat rows."
    secretary_whisper "The students in the left are from the high school."
    if loli_content >= 1:
        secretary_whisper "The students in the center are from the middle school."
    if loli_content == 2:
        secretary_whisper "And to the right are the elementary school students."

    scene expression "events/intro/intro gym 3 2.png"
    principal_thought "Wow she has a nice butt. I can't wait to make it mine."
    
    #show secretary stand at podium with hands on podium
    scene expression "events/intro/intro gym 4.png"
    secretary_shout "Good Morning Students!"
    crowd_shout "Good Morning!"

    #show crowd from behind Secretary (students standing in clear rows)
    scene expression "events/intro/intro gym 5 [loli_content].png"
    secretary_shout "It is with great pleasure, that I introduce you to your new Headmaster."
    secretary_shout "He will be starting today and we're all very excited to see the positive changes he will bring!"

    #show view from slightly behind crowd towards stage (secretary pointing towards principal)
    # scene expression "events/intro/intro gym 6 [loli_content].png"
    secretary_shout "But without further ado... Greet your new Headmaster Mr. [principal_last_name]!"
    subtitles "You walk to the podium."

    #show view of stagefrom front with principal standing at podium with hands on podium
    scene expression "events/intro/intro gym 7.png"
    principal_shout "Greetings to you all. I am honored to stand here today."
    principal_shout "When I came here, I saw the condition of this school and the mishaps of your former headmaster."
    principal_shout "I guarantee I won't repeat the same mistakes and I will bring this school back to its former glory and beyond."

    #show view of crowd from slightly behind but other side, principal hand on chest
    scene expression "events/intro/intro gym 8 [loli_content].png"
    principal_shout "Now a little about me. My name is [principal_first_name] [principal_last_name] and I come from the country."
    principal_shout "I taught in various schools and was also the principal of a school in the capital."

    #show principal rasing finger
    # scene expression "events/intro/intro gym 9 [loli_content].png"
    principal_shout "I want to make it clear that I will not tolerate misbehavior! {b}BUT{/b} I am a fair person."
    principal_shout "No one will be punished if they don't deserve it and I will do everything I can to make sure that you all have a nice and safe place to grow and learn!"

    #show principal with wide open arms
    # scene expression "events/intro/intro gym 10 [loli_content].png"
    principal_shout "If you ever have any problems, ideas or questions, feel free to come to me anytime. I will help wherever I can!"
    principal_shout "Thank you and let's have a great time together!"
    crowd_shout "*clapping*"

    scene office secretary 3 big smile
    secretary "Wow! That was a nice speech!"
    secretary "Now that we finished the introduction, let's start with the entry paperwork."
    principal "Alright."

    jump new_day

##########################