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
        TimeCondition(week = 1),
    ))


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

    call call_available_event(gym_timed_event) from _call_call_available_event_5

label .after_time_check:

    call call_event_menu (
        "What to do in the Gym?",
        1, 
        7, 
        gym_events, 
        gym_events_fallback,
    ) from _call_call_event_menu_5

    jump gym

###################################
# ----- Gym Fallback Events ----- #
###################################

label gym_fallback:
    subtitles "There is nothing to see here."
    return

label gym_person_fallback:
    subtitles "There is nobody here."
    return

##########################
# ----- Gym Events ----- #
##########################

# first week event
label first_week_gym_event:
    subtitles "todo: first_week_event"

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

    scene expression "events/intro/intro gym 1.png"
    subtitles "You leave the office with the secretary and head for the Gym."
    
    #show inside gym with students walking towards their position in gym or talking to each other in groups by school
    scene expression "events/intro/intro gym 2 [loli_content].png"
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
    scene expression "events/intro/intro gym 6 [loli_content].png"
    secretary_shout "But without further ado... Greet your new Headmaster [principal_name]!"
    subtitles "You walk to the podium."

    #show view of stagefrom front with principal standing at podium with hands on podium
    scene expression "events/intro/intro gym 7.png"
    principal_shout "Greetings to you all. I am honored to stand here today."
    principal_shout "When I came here, I saw the condition of this school and the mishaps of your former headmaster."
    principal_shout "I guarantee I won't repeat the same mistakes and I will bring this school back to its former glory and beyond."

    #show view of crowd from slightly behind but other side, principal hand on chest
    scene expression "events/intro/intro gym 8 [loli_content].png"
    principal_shout "Now a little about me. My name is [principal_name] and I come from the country."
    principal_shout "I taught in various schools and was also the principal of a school in the capital."

    #show principal rasing finger
    scene expression "events/intro/intro gym 9 [loli_content].png"
    principal_shout "I want to make it clear that I will not tolerate misbehavior! {b}BUT{/b} I am a fair person."
    principal_shout "No one will be punished if they don't deserve it and I will do everything I can to make sure that you all have a nice and safe place to grow and learn!"

    #show principal with wide open arms
    scene expression "events/intro/intro gym 10 [loli_content].png"
    principal_shout "If you ever have any problems, ideas or questions, feel free to come to me anytime. I will help wherever I can!"
    principal_shout "Thank you and let's have a great time together!"
    crowd_shout "*clapping*"

    scene office secretary 3 big smile
    secretary "Wow! That was a nice speech!"
    secretary "Now that everything's settled, let's start your first day as principal here. Shall we?"

    jump new_daytime
