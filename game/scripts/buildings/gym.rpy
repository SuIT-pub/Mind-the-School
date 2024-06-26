#################################
# ----- Gym Event Handler ----- #
#################################

init -1 python:
    def gym_events_available() -> bool:
        return (gym_timed_event.has_available_highlight_events() or
            gym_general_event.has_available_highlight_events() or
            any(e.has_available_highlight_events() for e in gym_events.values()))

    gym_timed_event = TempEventStorage("gym_timed", "gym", Event(2, "gym.after_time_check"))
    gym_general_event = EventStorage("gym_general", "gym", Event(2, "gym.after_general_check"))
    
    gym_events = {}
    add_storage(gym_events, EventStorage("enter_changing", "gym", default_fallback, "There is nothing to do here."))
    add_storage(gym_events, EventStorage("go_students",    "gym", default_fallback, "There is nobody here."))
    add_storage(gym_events, EventStorage("check_pe",       "gym", default_fallback, "There is nothing to do here."))
    add_storage(gym_events, EventStorage("teach_pe",       "gym", default_fallback, "There is nothing to do here."))

    gym_bg_images = BGStorage("images/background/gym/bg f.webp",
        BGImage("images/background/gym/bg <loli> <school_level> <teacher_level> <variant> <nude>.webp", 1, TimeCondition(daytime = "c", weekday = "d")), # show gym with students
        BGImage("images/background/gym/bg 7.webp", 1, TimeCondition(daytime = 7)), # show gym at night empty
    )
    
init 1 python:
    first_week_gym_event_event = Event(1, "first_week_gym_event",
        IntroCondition(),
        TimeCondition(day = "2-4", month = 1, year = 2023),
        thumbnail = "images/events/first week/first week gym 1.webp")

    first_potion_gym_event_event = Event(1, "first_potion_gym_event",
        IntroCondition(),
        TimeCondition(day = 9, month = 1, year = 2023),
        thumbnail = "images/events/first potion/first potion gym 1.webp")

    gym_event1 = Event(3, "gym_event_1",
        StatSelector("corruption", CORRUPTION, "school"),
        RandomListSelector("topic", "shoes", "hair", "ready"),
        DictSelector("topic_text", "topic", {
            "shoes": "putting on my shoes",
            "hair": "doing my hair",
            "ready": "getting ready",
        }),
        TimeCondition(daytime = "c", weekday = "d"),
        thumbnail = "images/events/gym/gym_event_1 1 hair 0.webp")
    
    gym_event2 = Event(3, "gym_event_2",
        StatSelector("inhibition", INHIBITION, "school"),
        RandomListSelector("topic", (0.75, "clothe"), "breasts", (0.15, "asses")),
        TimeCondition(daytime = "c", weekday = "d"),
        thumbnail = "images/events/gym/gym_event_2 1 clothe 0.webp")

    gym_event3 = Event(3, "gym_event_3",
        RandomValueSelector("variant", 1, 1),
        DictSelector("girl_name", "variant", {
            1: "Kokoro Nakamura",
        }),
        TimeCondition(daytime = "c", weekday = "d"),
        thumbnail = "images/events/gym/gym_event_3 1 1 0.webp")    

    gym_teach_pe_1_event = Event(3, "gym_teach_pe_1",
        TimeCondition(daytime = "c", weekday = "d"),
        thumbnail = "images/events/gym/gym_teach_pe_1 1 9.webp")

    gym_general_event.add_event(
        first_week_gym_event_event,
        first_potion_gym_event_event,
    )

    gym_events["enter_changing"].add_event(
        gym_event2,
    )
    gym_events["go_students"].add_event(
        gym_event1, 
        gym_event3,
    )
    gym_events["check_pe"].add_event(
        gym_event1, 
        gym_event3,
    )
    gym_events["teach_pe"].add_event(
        gym_event1, 
        gym_event3,
        gym_teach_pe_1_event,
    )

#################################

###############################
# ----- Gym Entry Point ----- #
###############################

label gym ():
    call call_available_event(gym_timed_event) from gym_1

label .after_time_check (**kwargs):
    call call_available_event(gym_general_event) from gym_4

label .after_general_check (**kwargs):
    $ loli = get_random_loli()
    $ gym_bg_images.add_kwargs(loli = loli)

    call call_event_menu (
        "What to do in the Gym?", 
        gym_events, 
        default_fallback,
        character.subtitles,
        bg_image = gym_bg_images,
        context = loli,
    ) from gym_3

    jump gym

###############################

##########################
# ----- Gym Events ----- #
##########################

label first_potion_gym_event (**kwargs):
    $ begin_event(**kwargs)
    
    show first potion gym 1 with dissolveM
    subtitles "You enter the Gym and see a group of students and teacher in a yoga session."

    show first potion gym 2 with dissolveM
    headmaster_thought "Oh that is a sport session I can get behind!"

    show first potion gym 3 with dissolveM
    headmaster_thought "Mhh, yes very flexible!"

    show first potion gym 4 with dissolveM
    headmaster_thought "Oh they seem to really get into it!"

    $ set_building_blocked("gym")

    $ end_event('new_daytime', **kwargs)


# first week event
label first_week_gym_event (**kwargs):
    
    $ begin_event(**kwargs)
    
    show first week gym 1 with dissolveM
    headmaster_thought "Okay, now the Gym. I have been here shortly for my introduction speech but I haven't had the chance to get a thorough look."

    show first week gym 2 with dissolveM
    headmaster_thought "Mhh, doesn't look to shabby..."
    
    show first week gym 3 with dissolveM
    headmaster_thought "Seems to be decently stocked."
    headmaster_thought "The material is well maintained. I guess it's alright."

    $ change_stat("charm", 5, get_school())

    $ set_building_blocked("gym")

    $ end_event('new_daytime', **kwargs)

#############################
# weekly assembly entry point
label weekly_assembly (**kwargs):

    subtitles "todo: weekly assembly"

    return

image anim_gym_teach_pe_1_10 = Movie(play ="images/events/gym/gym_teach_pe_1 1 10.webm", start_image = "images/events/gym/gym_teach_pe_1 1 10.webp", loop = True)
image anim_gym_teach_pe_1_11 = Movie(play ="images/events/gym/gym_teach_pe_1 1 11.webm", start_image = "images/events/gym/gym_teach_pe_1 1 11.webp", loop = True)
image anim_gym_teach_pe_1_12 = Movie(play ="images/events/gym/gym_teach_pe_1 1 12.webm", start_image = "images/events/gym/gym_teach_pe_1 1 12.webp", loop = True)

label gym_teach_pe_1 (**kwargs):
    $ begin_event(**kwargs)

    # headmaster changes clothing in changing room
    # headmaster heads to gym

    $ school_obj = get_char_value('school_obj', **kwargs)

    $ image = Image_Series("/images/events/gym/gym_teach_pe_1 <school_level> <step>.webp", **kwargs)

    call Image_Series.show_image(image, 0, 1, 2, 3, 4, 5, 6, 7, 8, pause = True) from gym_teach_pe_1_1

    $ image.show(9)
    headmaster "Alright, let's get started with the P.E. class."

    headmaster "First we start with a few warm up exercises and stretching. After that I planned for you to play a round of football."
    headmaster "Okay now all follow my lead."
    
    scene anim_gym_teach_pe_1_10 with dissolveM
    pause
    scene anim_gym_teach_pe_1_11 with dissolveM
    pause
    scene anim_gym_teach_pe_1_12 with dissolveM
    pause
    
    call Image_Series.show_image(image, 13, 14) from gym_teach_pe_1_2
    headmaster "Alright, that's enough. Now let's play some football. I will be the referee."
    $ image.show(15)
    headmaster "Please split into two teams and let's get started."
    $ image.show(16)
    sgirl "I'm sorry but how do we identify the teams? We all wear the same uniform." (name = "Sakura Mori")
    $ image.show(17)
    headmaster "Hmm, that's a good point. Unfortunately we don't have any bibs or anything like that."
    $ image.show(18)
    headmaster "I guess you just will have to remember your team mates. So now your teams please."
    # The students seperate into two groups
    call Image_Series.show_image(image, 19, 20) from gym_teach_pe_1_3   
    headmaster "Alright, let's get started. The right side has the kickoff."
    $ image.show(21)
    headmaster "And... START!"
    call Image_Series.show_image(image, 22, 23, 24, 25, 26, 27) from gym_teach_pe_1_4
    
    call screen black_screen_text("1 hour later")

    $ image.show(28)
    headmaster "Alright, that's enough for today. I hope you all had fun."
    $ image.show(29)
    headmaster "Don't forget to shower and change your clothes."
    # class leaves the gym
    
    $ change_stats_with_modifier(get_school(), 
        happiness = TINY, charm = SMALL, reputation = TINY, inhibition = DEC_TINY)

    $ end_event('new_daytime', **kwargs)

label gym_event_1 (**kwargs):
    $ begin_event(**kwargs)

    $ school_obj = get_char_value('school_obj', **kwargs)
    $ corruption = get_stat_value("corruption", [5, 100], **kwargs)
    $ topic_variant = get_value("topic", **kwargs)
    $ topic = get_value("topic_text", **kwargs)

    $ image = Image_Series("/images/events/gym/gym_event_1 <school_level> <topic> <step>.webp", **kwargs)

    $ image.show(0)
    subtitles "In the Gym, you see a girl getting ready for P.E."

    # if corruption >= 80:
    #     show screen black_screen_text("gym_event_1\ncorruption >= 80")
    #     sgirl "Im [topic] right now, how about a quick make out session before class starts? We got a few minutes for that." (name = girls[school_name][0])
    #     headmaster "For a girl as pretty as you? Of course I do!"
    #     subtitles "After she is ready, you spend a few minutes making out with her."
    #     $ change_stats_with_modifier(school_obj, 
    #         inhibition = DEC_LARGE, corruption = MEDIUM, charm = SMALL)
    # elif corruption >= 60:
    #     show screen black_screen_text("gym_event_1\ncorruption >= 60")
    #     sgirl "Im [topic] now, how about a proper good luck kiss before class?" (name = girls[school_name][0])
    #     headmaster "That sounds like a very good measure!"
    #     subtitles "After she is ready, you french kiss her for a minute."
    #     $ change_stats_with_modifier(school_obj, 
    #         inhibition = DEC_MEDIUM, corruption = MEDIUM, charm = SMALL)
    # elif corruption >= 40:
    #     show screen black_screen_text("gym_event_1\ncorruption >= 40")
    #     sgirl "just [topic] for P.E.\n Say, do you wish we would just run around nude all day?" (name = girls[school_name][0])
    #     sgirl "We just might if you asked us to." (name = girls[school_name][1])
    #     # tease headmaster -> run off
    #     sgirl "*giggle*" (name="School Girls")
    #     $ change_stats_with_modifier(school_obj, 
    #         inhibition = DEC_SMALL, corruption = MEDIUM, charm = SMALL)
    # elif corruption >= 20:
    #     show screen black_screen_text("gym_event_1\ncorruption >= 20")
    #     sgirl "Just [topic] for P.E.\n Say, do you wish we would just run around in underwear all day?" (name = girls[school_name][0])
    #     sgirl "We just might if you asked us to." (name = girls[school_name][1])
    #     # tease headmaster -> run off
    #     sgirl "*giggle*" (name="School Girls")
    #     $ change_stats_with_modifier(school_obj, 
    #         inhibition = DEC_SMALL, corruption = SMALL, charm = SMALL)
    if corruption > 5:
        $ image.show(1)
        sgirl "Just give me a moment more to get ready for class. You like watching me doing whatever, right?" (name="Aona Komuro")

        $ image.show(2)
        headmaster "As pretty as you are? I sure do!"

        $ change_stats_with_modifier(school_obj, 
            inhibition = DEC_SMALL, corruption = TINY, charm = TINY)
    else:
        $ image.show(1)
        sgirl "Are you getting ready for gym class too, Mr. [headmaster_last_name]?" (name="Aona Komuro")

        $ change_stats_with_modifier(school_obj, 
            inhibition = DEC_TINY, corruption = TINY, charm = TINY)
    $ end_event('new_daytime', **kwargs)

label gym_event_2 (**kwargs):
    $ begin_event(**kwargs)

    $ school_obj = get_char_value('school_obj', **kwargs)
    $ inhibition = get_stat_value("inhibition", [100], **kwargs)
    $ topic = get_value("topic", **kwargs)

    $ image = Image_Series("/images/events/gym/gym_event_2 <school_level> <topic> <step>.webp", **kwargs)

    $ image.show(0)
    if topic == "breasts":
        subtitles "You find yourself in the girls changing room with some bare breasts on display."
    elif topic == "asses":
        subtitles "You find yourself in the girls changing room. You can't help but look on those bare asses."
    else:
        subtitles "You walk in on some girls changing their clothes before P.E."
    
    # if inhibition >= 80:
    $ image.show(1)
    subtitles "It took a few seconds for them to realize what is happening."
    $ image.show(2)
    sgirl "*scream*" (name="School Girls")
    $ image.show(3)
    headmaster "Sorry, I didn't mean to intrude."
    $ image.show(4)
    subtitles "You run out as fast as you can."
    $ change_stats_with_modifier(school_obj, 
        inhibition = DEC_SMALL, HAPPINESS = DEC_MEDIUM, REPUTATION = DEC_SMALL)
    # elif inhibition >= 60:
    #     show screen black_screen_text("gym_event_2\ntopic_[topic] inhibition >= 60")

    #     $ call_custom_menu_with_text("Oops... Nice view but they don't seem too happy about me being here.", character.headmaster_thought, False,
    #         ("I'm sorry, I didn't know I was in the girls locker room", "gym_event_2.sorry"),
    #         ("Oh pardon me but I'm conducting a walk through of all escape routes in case there's a fire.", "gym_event_2.escape"),
    #     **kwargs)
    # elif inhibition >= 30:
    #     show screen black_screen_text("gym_event_2\ntopic_[topic] inhibition >= 30")
    #     subtitles "<GIRL NAME> is down to bra und panties, but her bra doesn't seem to fit her."
    #     headmaster "Be sure to wear good fitting bras to keep being as perky as you are and to keep your breasts healthy."
    #     $ change_stats_with_modifier(school_obj,
    #         inhibition = DEC_SMALL, HAPPINESS = DEC_SMALL)
    # else:
    # show screen black_screen_text("gym_event_2\ntopic_[topic] inhibition < 30")
    # sgirl "Ahh!"
    # headmaster "Sorry, is everything alright?"
    # sgirl "Yes, I was just surprised."
    # $ change_stats_with_modifier(school_obj,
    #     inhibition = DEC_MEDIUM)

    $ end_event('new_daytime', **kwargs)
label .sorry (**kwargs):
    
    $ begin_event()
    
    sgirl "Okay..."
    headmaster_thought "I think she doesn't believe me..."
    $ change_stats_with_modifier(school_obj,
        HAPPINESS = DEC_MEDIUM, REPUTATION = DEC_SMALL)
    $ end_event('new_daytime', **kwargs)
label .escape (**kwargs):
    
    $ begin_event()
    
    sgirl "Oh, I was just..."
    headmaster "It's okay. You couldn't possible know."
    subtitles "You leave the room and leave the girls behind dumbfounded."
    $ change_stats_with_modifier(school_obj,
        inhibition = DEC_MEDIUM, HAPPINESS = DEC_SMALL)
    $ end_event('new_daytime', **kwargs)

label gym_event_3 (**kwargs):
    $ begin_event(**kwargs)

    $ school_obj = get_char_value('school_obj', **kwargs)
    $ variant = get_value("variant", **kwargs)
    $ girl = get_value("girl_name", **kwargs)

    $ girl_name = girl.split(" ")[0]
    $ girl_full_name = girl

    $ image = Image_Series("/images/events/gym/gym_event_3 <school_level> <variant> <step>.webp", **kwargs)


    $ image.show(0)
    headmaster "Sorry but that top doesn't conform to the uniform policy."
    $ image.show(1)
    sgirl "Whaa... But my normal uniform is in the wash!" (name = girl_full_name)
    $ image.show(2)
    headmaster "That's unfortunate but you can't keep wearing this for P.E. as it is bad for the hygiene and could lead to injuries."
    headmaster "The sport clothing is made of special materials that are designed to be worn during sports and have antibacterial properties."
    $ image.show(3)
    sgirl "But I don't have anything else!" (name = girl_full_name)
    $ image.show(4)
    headmaster "I'm sorry but you will have to take of your top then."
    $ image.show(5)
    sgirl "But..." (name = girl_full_name)
    headmaster "I'm sorry but I can't make an exception. Better keep your timetable in mind next time."
    $ image.show(6)
    subtitles "[girl_name] takes of her top and is now only wearing her bra."
    $ image.show(7)
    subtitles "She proceeded to take part on the P.E. class, almost dying of shame."

    $ change_stats_with_modifier(school_obj,
        inhibition = DEC_MEDIUM, happiness = DEC_LARGE, charm = TINY, education = TINY, reputation = DEC_SMALL)
    $ end_event('new_daytime', **kwargs)