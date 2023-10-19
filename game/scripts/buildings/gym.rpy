#################################
# ----- Gym Event Handler ----- #
#################################

init -1 python:
    gym_after_time_check = Event(2, "gym.after_time_check")
    gym_fallback         = Event(2, "gym_fallback")
    gym_person_fallback  = Event(2, "gym_person_fallback")

    gym_timed_event = EventStorage("gym", "", gym_after_time_check)
    gym_events = {
        "teacher":        EventStorage("teacher",        "Go to teacher",                      gym_person_fallback),
        "students":       EventStorage("students",       "Go to students",                     gym_person_fallback),
        "storage":        EventStorage("storage",        "Check storage",                      gym_fallback       ),
        "peek_changing":  EventStorage("peek_changing",  "Go to Peek into the changing rooms", gym_person_fallback),
        "enter_changing": EventStorage("enter_changing", "Enter the changing rooms",           gym_fallback       ),
        "check_pe":       EventStorage("check_pe",       "Check a P.E. class",                 gym_fallback       ),
        "teach_pe":       EventStorage("teach_pe",       "Teach a P.E. class",                 gym_fallback       ),
        "steal":          EventStorage("steal",          "Steal some panties",                 gym_fallback       ),
    }

    gym_timed_event.add_event(Event(1,
        ["first_week_gym_event"],
        TimeCondition(day = "2-4", month = 1, year = 2023),
    ))

    
    gym_timed_event.add_event(Event(1,
        ["first_potion_gym_event"],
        TimeCondition(day = 9),
    ))

    gym_event1 = Event(3, 
        ["gym_event_1", "gym_event_3"], 
        TimeCondition(daytime = "c", weekday = "d")
    )

    gym_events["students"].add_event(gym_event1)
    gym_events["check_pe"].add_event(gym_event1)
    gym_events["teach_pe"].add_event(gym_event1)

    gym_events["enter_changing"].add_event(Event(3, 
        ["gym_event_2"], 
        TimeCondition(daytime = "c", weekday = "d")
    ))

    gym_timed_event.check_all_events()
    map(lambda x: x.check_all_events(), gym_events.values())

    gym_bg_images = [
        BGImage("images/background/gym/bg c <name> <level> <nude>.jpg", 1, TimeCondition(daytime = "c", weekday = "d")), # show gym with students
        BGImage("images/background/gym/bg 7.jpg", 1, TimeCondition(daytime = 7)), # show gym at night empty
    ]
    
#################################

###############################
# ----- Gym Entry Point ----- #
###############################

label gym ():

    call call_available_event(gym_timed_event) from gym_1

label .after_time_check (**kwargs):

    $ school_obj = get_random_school()

    call show_gym_idle_image(school_obj) from gym_2

    call call_event_menu (
        "What to do in the Gym?", 
        gym_events, 
        gym_fallback,
        character.subtitles,
        char_obj = school_obj,
    ) from gym_3

    jump gym

label show_gym_idle_image(school_obj):

    $ max_nude, image_path = get_background(
        "images/background/gym/bg f.jpg", # show gym empty
        gym_bg_images,
        school_obj,
    )

    call show_image_with_nude_var (image_path, max_nude) from _call_show_image_with_nude_var_5

    return

###############################

###################################
# ----- Gym Fallback Events ----- #
###################################

label gym_fallback (**kwargs):
    subtitles "There is nothing to see here."
    jump map_overview

label gym_person_fallback (**kwargs):
    subtitles "There is nobody here."
    jump map_overview

###################################

##########################
# ----- Gym Events ----- #
##########################

label first_potion_gym_event (**kwargs):
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
label first_week_gym_event (**kwargs):
    show first week gym 1 with dissolveM
    headmaster_thought "Okay, now the Gym. I have been here shortly for my introduction speech but I haven't had the chance to get a thorough look."

    show first week gym 2 with dissolveM
    headmaster_thought "Mhh, doesn't look to shabby..."
    
    show first week gym 3 with dissolveM
    headmaster_thought "Seems to be decently stocked."
    headmaster_thought "The material is well maintained. I guess it's alright."

    $ change_stat_for_all("charm", 5, charList["schools"])

    $ set_building_blocked("gym")

    jump new_day

#############################
# weekly assembly entry point
label weekly_assembly (**kwargs):

    subtitles "todo: weekly assembly"

    return

label gym_event_1 (**kwargs):
    show screen black_screen_text("gym_event_1")

    $ char_obj = get_kwargs("char_obj", **kwargs)

    $ corruption = char_obj.get_stat_number(CORRUPTION)

    $ topic = get_random_choice("putting on my shoes", "doing my hair", "getting ready")

    # Image variants: getting ready, shoes, hair
    subtitles "In the Gym, you see a girl getting ready for P.E."

    if corruption >= 80:
        show screen black_screen_text("gym_event_1\ncorruption >= 80")
        sgirl "Im [topic] right now, how about a quick make out session before class starts? We got a few minutes for that."
        headmaster "For a girl as pretty as you? Of course I do!"
        subtitles "After she is ready, you spend a few minutes making out with her."
        $ change_stats_with_modifier(char_obj, 
            inhibition = DEC_LARGE, corruption = MEDIUM, charm = SMALL)
    elif corruption >= 60:
        show screen black_screen_text("gym_event_1\ncorruption >= 60")
        sgirl "Im [topic] now, how about a proper good luck kiss before class?"
        headmaster "That sounds like a very good measure!"
        subtitles "After she is ready, you french kiss her for a minute."
        $ change_stats_with_modifier(char_obj, 
            inhibition = DEC_MEDIUM, corruption = MEDIUM, charm = SMALL)
    elif corruption >= 40:
        show screen black_screen_text("gym_event_1\ncorruption >= 40")
        sgirl "just [topic] for P.E.\n Say, do you wish we would just run around nude all day?"
        sgirl "We just might if you asked us to."
        # tease headmaster -> run off
        sgirl "*giggle*"
        $ change_stats_with_modifier(char_obj, 
            inhibition = DEC_SMALL, corruption = MEDIUM, charm = SMALL)
    elif corruption >= 20:
        show screen black_screen_text("gym_event_1\ncorruption >= 20")
        sgirl "Just [topic] for P.E.\n Say, do you wish we would just run around in underwear all day?"
        sgirl "We just might if you asked us to."
        # tease headmaster -> run off
        sgirl "*giggle*"
        $ change_stats_with_modifier(char_obj, 
            inhibition = DEC_SMALL, corruption = SMALL, charm = SMALL)
    elif corruption >= 5:
        show screen black_screen_text("gym_event_1\ncorruption >= 5")
        sgirl "Just give me a moment more to get ready for class. You like watching me doing whatever, right?"
        headmaster "As pretty as you are? I sure do!"
        $ change_stats_with_modifier(char_obj, 
            inhibition = DEC_SMALL, corruption = TINY, charm = TINY)
    else:
        show screen black_screen_text("gym_event_1\ncorruption < 5")
        sgirl "Are you getting ready for gym class too, Mr. [headmaster_last_name]?"
        $ change_stats_with_modifier(char_obj, 
            inhibition = DEC_TINY, corruption = TINY, charm = TINY)
    jump new_daytime

label gym_event_2 (**kwargs):
    show screen black_screen_text("gym_event_2")

    $ char_obj = get_kwargs("char_obj", **kwargs)

    $ inhibition = char_obj.get_stat_number(INHIBITION)

    $ topic = get_random_choice("clothe", "clothe", "clothe", "clothe", "breasts", "asses")

    if topic == "breasts":
        show screen black_screen_text("gym_event_2\ntopic_breasts")
        subtitles "You find yourself in the girls changing room with some bare breasts on display."
    elif topic == "asses":
        show screen black_screen_text("gym_event_2\ntopic_asses")
        subtitles "You find yourself in the girls changing room. You can't help but look on those bare asses."
    else:
        show screen black_screen_text("gym_event_2\ntopic_clothe")
        subtitles "You walk in on some girls changing their clothes before P.E."
    
    if inhibition >= 80:
        show screen black_screen_text("gym_event_2\ntopic_[topic] inhibition >= 80")
        subtitles "It took a few seconds for them to realize what is happening."
        sgirl "*scream*" (name="School Girls")
        headmaster "Sorry, I didn't mean to intrude."
        subtitles "You run out as fast as you can."
        $ change_stats_with_modifier(char_obj, 
            inhibition = MEDIUM, HAPPINESS = DEC_MEDIUM, REPUTATION = DEC_SMALL)
    elif inhibition >= 60:
        show screen black_screen_text("gym_event_2\ntopic_[topic] inhibition >= 60")

        $ call_custom_menu_with_text("Oops... Nice view but they don't seem too happy about me being here.", characters.headmaster_thought, False,
            ("I'm sorry, I didn't know I was in the girls locker room", "gym_event_2.sorry"),
            ("Oh pardon me but I'm conducting a walk through of all escape routes in case there's a fire.", "gym_event_2.escape"),
        **kwargs)
    elif inhibition >= 30:
        show screen black_screen_text("gym_event_2\ntopic_[topic] inhibition >= 30")
        subtitles "<GIRL NAME> is down to bra und panties, but her bra doesn't seem to fit her."
        headmaster "Be sure to wear good fitting bras to keep being as perky as you are and to keep your breasts healthy."
        $ change_stats_with_modifier(char_obj,
            inhibition = DEC_SMALL, HAPPINESS = DEC_SMALL)
    else:
        show screen black_screen_text("gym_event_2\ntopic_[topic] inhibition < 30")
        sgirl "Ahh!"
        headmaster "Sorry, is everything alright?"
        sgirl "Yes, I was just surprised."
        $ change_stats_with_modifier(char_obj,
            inhibition = DEC_MEDIUM)

    jump new_daytime
label .sorry (**kwargs):
    sgirl "Okay..."
    headmaster_thought "I think she doesn't believe me..."
    $ change_stats_with_modifier(char_obj,
        HAPPINESS = DEC_MEDIUM, REPUTATION = DEC_SMALL)
    jump new_daytime
label .escape (**kwargs):
    sgirl "Oh, I was just..."
    headmaster "It's okay. You couldn't possible know."
    subtitles "You leave the room and leave the girls behind dumbfounded."
    $ change_stats_with_modifier(char_obj,
        inhibition = DEC_MEDIUM, HAPPINESS = DEC_SMALL)
    jump new_daytime

label gym_event_3 (**kwargs):
    show screen black_screen_text("gym_event_3")

    $ char_obj = get_kwargs("char_obj", **kwargs)

    headmaster "Sorry but that top doesn't conform to the uniform policy."
    sgirl "Whaa... But my normal uniform is in the wash!"
    headmaster "That's unfortunate but you can't keep wearing this for P.E. as it is bad for the hygiene and could lead to injuries."
    sgirl "But I don't have anything else!"
    headmaster "I'm sorry but you will have to take of your top then."
    sgirl "But..."
    headmaster "I'm sorry but I can't make an exception. Better keep your timetable in mind next time."
    subtitles "<Girl Name> takes of her top and is now only wearing her bra."
    subtitles "She proceeded to take part on the P.E. class, almost dying of shame."

    $ change_stats_with_modifier(char_obj,
        inhibition = DEC_MEDIUM, happiness = DEC_LARGE, charm = TINY, education = TINY, reputation = DEC_SMALL)
    jump new_daytime