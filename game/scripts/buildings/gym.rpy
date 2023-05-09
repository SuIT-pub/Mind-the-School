#################################
# ----- Gym Event Handler ----- #
#################################

init -10 python:
    gym_events = {}

    gym_events["fallback"] = "gym_fallback"

    # event check before menu
    gym_events["gym"] = {
        "fallback": "gym.after_time_check", # no event
    }

    gym_events["teacher"] = {
        "fallback": "gym_person_fallback",
    }

    gym_events["students"] = {
        "fallback": "gym_person_fallback",
    }

###############################
# ----- Gym Entry Point ----- #
###############################

label gym:
    # show gym inside

    # if daytime in [1, 3, 6]:
    #     # show gym empty
    # if daytime in [2, 4, 5]:
    #     # show gym with students
    # if daytime in [7]:
    #     # show gym at night empty

    call event_check_area("gym", gym_events)

label.after_time_check:

    $ check_events = [
        get_events_area_count("teacher"       , gym_events),
        get_events_area_count("students"      , gym_events),
        get_events_area_count("storage"       , gym_events),
        get_events_area_count("peek_changing" , gym_events),
        get_events_area_count("enter_changing", gym_events),
        get_events_area_count("steal"         , gym_events),
    ]

    if any(check_events):
        menu:
            Subtitles "What to do in the Gym?"

            "Go to teacher" if check_events[0] > 0:
                call event_check_area("teacher", gym_events)
            "Go to students" if check_events[1] > 0:
                call event_check_area("students", gym_events)
            "Check storage" if check_events[2] > 0:
                call event_check_area("storage", gym_events)
            "Take a peek in the changing rooms" if check_events[3] > 0:
                call event_check_area("peek_changing", gym_events)
            "Enter the changing rooms" if check_events[4] > 0:
                call event_check_area("enter_changing", gym_events)
            "Steal some panties" if check_events[5] > 0:
                call event_check_area("steal", gym_events)
            "Return":
                jump map_overview
    else:
        call gym_fallback
        jump map_overview

    jump gym

###################################
# ----- Gym Fallback Events ----- #
###################################

label gym_fallback:
    Subtitles "There is nothing to see here."
    return

label gym_person_fallback:
    Subtitles "There is nobody here."
    return

##########################
# ----- Gym Events ----- #
##########################

#############################
# weekly assembly entry point
label weekly_assembly:

    if today() == "1.1.2023":
        jump weekly_assembly_first

    Subtitles "todo: weekly assembly"

    return

###################################
# first weekly assembly of the game
label weekly_assembly_first:

    scene expression "events/intro/intro gym 1.png"
    Subtitles "You leave the office with the secretary and head for the Gym."
    
    #show inside gym with students walking towards their position in gym or talking to each other in groups by school
    scene expression "events/intro/intro gym 2 [loli_content].png"
    Subtitles "As you enter the hall, you'll be greeted by students standing all around the hall."
    
    #show move up stairs with secretary in front and clear view of butt
    scene expression "events/intro/intro gym 3 1.png"
    Subtitles "As you and your secretary meak your way to the stage, all the students begin to form neat rows."
    char_Secretary_whisper "The students in the left are from the high school."
    if loli_content >= 1:
        char_Secretary_whisper "The students in the center are from the middle school."
    if loli_content == 2:
        char_Secretary_whisper "And to the right are the elementary school students."

    scene expression "events/intro/intro gym 3 2.png"
    char_Principal_thought "Wow she has a nice butt. I can't wait to make it mine."
    
    #show secretary stand at podium with hands on podium
    scene expression "events/intro/intro gym 4.png"
    char_Secretary_shout "Good Morning Students!"
    char_Crowd_shout "Good Morning!"

    #show crowd from behind Secretary (students standing in clear rows)
    scene expression "events/intro/intro gym 5 [loli_content].png"
    char_Secretary_shout "It is with great pleasure, that I introduce you to your new Headmaster."
    char_Secretary_shout "He will be starting today and we're all very excited to see the positive changes he will bring!"

    #show view from slightly behind crowd towards stage (secretary pointing towards principal)
    scene expression "events/intro/intro gym 6 [loli_content].png"
    char_Secretary_shout "But without further ado... Greet your new Headmaster [principal_name]!"
    Subtitles "You walk to the podium."

    #show view of stagefrom front with principal standing at podium with hands on podium
    scene expression "events/intro/intro gym 7.png"
    char_Principal_shout "Greetings to you all. I am honored to stand here today."
    char_Principal_shout "When I came here, I saw the condition of this school and the mishaps of your former headmaster."
    char_Principal_shout "I guarantee I won't repeat the same mistakes and I will bring this school back to its former glory and beyond."

    #show view of crowd from slightly behind but other side, principal hand on chest
    scene expression "events/intro/intro gym 8 [loli_content].png"
    char_Principal_shout "Now a little about me. My name is [principal_name] and I come from the country."
    char_Principal_shout "I taught in various schools and was also the principal of a school in the capital."

    #show principal rasing finger
    scene expression "events/intro/intro gym 9 [loli_content].png"
    char_Principal_shout "I want to make it clear that I will not tolerate misbehavior! {b}BUT{/b} I am a fair person."
    char_Principal_shout "No one will be punished if they don't deserve it and I will do everything I can to make sure that you all have a nice and safe place to grow and learn!"

    #show principal with wide open arms
    scene expression "events/intro/intro gym 10 [loli_content].png"
    char_Principal_shout "If you ever have any problems, ideas or questions, feel free to come to me anytime. I will help wherever I can!"
    char_Principal_shout "Thank you and let's have a great time together!"
    char_Crowd_shout "*clapping*"

    scene office secretary 3 big smile
    char_Secretary "Wow! That was a nice speech!"
    char_Secretary "Now that everything's settled, let's start your first day as principal here. Shall we?"

    jump new_daytime
