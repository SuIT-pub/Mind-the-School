##################################
# region Gym Event Handler ----- #
##################################

init -1 python:
    set_current_mod('base')
    
    gym_timed_event = TempEventStorage("gym_timed", "gym", fallback = Event(2, "gym.after_time_check"))
    gym_general_event = EventStorage("gym_general", "gym", fallback = Event(2, "gym.after_general_check"))
    register_highlighting(gym_timed_event, gym_general_event)
    
    gym_events = {}
    add_storage(gym_events, EventStorage("enter_changing", "gym", fallback_text = "There is nothing to do here."))
    add_storage(gym_events, EventStorage("go_students",    "gym", fallback_text = "There is nobody here."))
    add_storage(gym_events, EventStorage("check_pe",       "gym", fallback_text = "There is nothing to do here."))
    add_storage(gym_events, EventStorage("teach_pe",       "gym", fallback_text = "There is nothing to do here."))
    add_storage(gym_events, EventStorage("relax",          "gym", fallback_text = "There is nothing to do here."))

    gym_bg_images = BGStorage("images/background/gym/f.webp", 
        BGImage("images/background/gym/<school_level> <variant> <nude>.webp", 1, TimeCondition(daytime = "c", weekday = "d")), # show gym with students
        BGImage("images/background/gym/n.webp", 1, TimeCondition(daytime = 7)), # show gym at night empty
    )
    
init 1 python:
    set_current_mod('base')

    gym_event1 = Event(3, "gym_event_1",
        LevelSelector("school_level", "school"),
        RandomListSelector("topic", "shoes", "hair", "ready"),
        DictSelector("topic_text", "topic", {
            "shoes": "putting on my shoes",
            "hair": "doing my hair",
            "ready": "getting ready",
        }),
        TimeCondition(daytime = "c", weekday = "d"),
        Pattern("main", "/images/events/gym/gym_event_1/gym_event_1 <school_level> <step>.webp"),
        thumbnail = "images/events/gym/gym_event_1/gym_event_1 1 0.webp")
    
    gym_event2 = Event(3, "gym_event_2",
        TimeCondition(daytime = "c", weekday = "d"),
        LevelCondition("5-", "school"),
        LevelSelector("school_level", "school"),
        RandomListSelector("topic", (0.75, "clothe"), "breasts", (0.15, "asses")),
        Pattern("main", "/images/events/gym/gym_event_2/gym_event_2 <school_level> <topic> <step>.webp"),
        thumbnail = "images/events/gym/gym_event_2/gym_event_2 1 clothe 0.webp")

    gym_event3 = Event(3, "gym_event_3",
        TimeCondition(daytime = "c", weekday = "d"),
        LevelCondition("3-", "school"),
        LevelSelector("school_level", "school"),
        Pattern("main", "/images/events/gym/gym_event_3/gym_event_3 <school_level> <step>.webp"),
        thumbnail = "images/events/gym/gym_event_3/gym_event_3 1 0.webp")    

    gym_event4 = Event(3, "gym_event_4",
        TimeCondition(daytime = "c", weekday = "d"),
        LevelCondition("2-4", "school"),
        Pattern("main", "/images/events/gym/gym_event_4/gym_event_4 <step>.webp"),
        thumbnail = "images/events/gym/gym_event_4/gym_event_4 0.webp")

    gym_event5 = Event(3, "gym_event_5",
        TimeCondition(daytime = "c", weekday = "d"),
        LevelCondition("2-4", "school"),
        Pattern("main", "/images/events/gym/gym_event_5/gym_event_5 <school_level> <step>.webp"),
        thumbnail = "images/events/gym/gym_event_5/gym_event_5 5 0.webp")

    gym_event6 = Event(3, "gym_event_6",
        TimeCondition(daytime = "c", weekday = "d"),
        LevelCondition("2+", "school"),
        ProgressCondition("yoga_classes", "10"),
        GameDataSelector("outfit", "yoga_outfit_set"),
        Pattern("main", "/images/events/gym/gym_event_6/gym_event_6 <outfit> <level> <step>.webp", "outfit"),
        thumbnail = "images/events/gym/gym_event_6/gym_event_6 3 8 2.webp")

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
        gym_event6,
    )
    gym_events["relax"].add_event(
        gym_event4,
        gym_event5,
    )
    

# endregion
##################################

################################
# region Gym Entry Point ----- #
################################

label gym ():
    if time.get_daytime() in [2, 4, 5]:
        $ play_sound(audio.gym_active, True, 0.2, 1.0)
    else:
        $ play_sound(audio.empty_room, True, 0.8, 1.0)

    call call_available_event(gym_timed_event) from gym_1
label .after_time_check (**kwargs):
    call call_available_event(gym_general_event) from gym_4
label .after_general_check (**kwargs):
    call call_event_menu (
        "What to do in the Gym?", 
        gym_events, 
        default_fallback,
        character.subtitles,
        bg_image = gym_bg_images,
    ) from gym_3

    jump gym

# endregion
################################

###########################
# region Gym Events ----- #
###########################

#########################
# region Regular Events #

define anim_ge1_path = "images/events/gym/gym_event_1/gym_event_1 "

image anim_gym_event_1_7_3 = Movie(play = anim_ge1_path + "7 3.webm", start_image = anim_ge1_path + "7 3.webp", loop = True)
image anim_gym_event_1_8_3 = Movie(play = anim_ge1_path + "8 3.webm", start_image = anim_ge1_path + "8 3.webp", loop = True)
image anim_gym_event_1_8_4 = Movie(play = anim_ge1_path + "8 4.webm", start_image = anim_ge1_path + "8 4.webp")
image anim_gym_event_1_8_5 = Movie(play = anim_ge1_path + "8 5.webm", start_image = anim_ge1_path + "8 5.webp")
image anim_gym_event_1_8_6 = Movie(play = anim_ge1_path + "8 6.webm", start_image = anim_ge1_path + "8 6.webp", loop = True)
image anim_gym_event_1_9_3 = Movie(play = anim_ge1_path + "9 3.webm", start_image = anim_ge1_path + "9 3.webp", loop = True)
image anim_gym_event_1_9_4 = Movie(play = anim_ge1_path + "9 4.webm", start_image = anim_ge1_path + "9 4.webp", loop = True)
image anim_gym_event_1_9_5 = Movie(play = anim_ge1_path + "9 5.webm", start_image = anim_ge1_path + "9 5.webp", loop = True)
image anim_gym_event_1_9_6 = Movie(play = anim_ge1_path + "9 6.webm", start_image = anim_ge1_path + "9 6.webp", loop = True)
image anim_gym_event_1_9_7 = Movie(play = anim_ge1_path + "9 7.webm", start_image = anim_ge1_path + "9 7.webp")
image anim_gym_event_1_9_8 = Movie(play = anim_ge1_path + "9 8.webm", start_image = anim_ge1_path + "9 8.webp", loop = True)
image anim_gym_event_1_10_3 = Movie(play = anim_ge1_path + "10 3.webm", start_image = anim_ge1_path + "10 3.webp", loop = True)
image anim_gym_event_1_10_4 = Movie(play = anim_ge1_path + "10 4.webm", start_image = anim_ge1_path + "10 4.webp", loop = True)
image anim_gym_event_1_10_5 = Movie(play = anim_ge1_path + "10 5.webm", start_image = anim_ge1_path + "10 5.webp", loop = True)
image anim_gym_event_1_10_6 = Movie(play = anim_ge1_path + "10 6.webm", start_image = anim_ge1_path + "10 6.webp", loop = True)
image anim_gym_event_1_10_7 = Movie(play = anim_ge1_path + "10 7.webm", start_image = anim_ge1_path + "10 7.webp", loop = True)
image anim_gym_event_1_10_8 = Movie(play = anim_ge1_path + "10 8.webm", start_image = anim_ge1_path + "10 8.webp")
image anim_gym_event_1_10_9 = Movie(play = anim_ge1_path + "10 9.webm", start_image = anim_ge1_path + "10 9.webp")
image anim_gym_event_1_10_10 = Movie(play = anim_ge1_path + "10 10.webm", start_image = anim_ge1_path + "10 10.webp", loop = True)
label gym_event_1 (**kwargs):
    $ begin_event("3", **kwargs)

    $ school_level = get_value('school_level', **kwargs)

    $ aona = get_person("class_3a", "aona_komuro").get_character()

    $ image = convert_pattern("main", video_prefix = "anim_", **kwargs)

    $ image.show(0)
    subtitles "In the Gym, you see a girl getting ready for P.E."
    
    if school_level == 10:
        $ image.show(1)
        aona "Im making my hair right now, how about a quick pre-workout before class starts? We got a few minutes for that."
        $ image.show(2)
        headmaster "For a girl as pretty as you? Of course I do!"
        $ image.show_video(3, pause = True)
        $ image.show_video(4, pause = True)
        $ image.show_video(5, pause = True)
        $ image.show_video(6, pause = True)
        $ image.show_video(7, pause = True)
        $ image.show_video(8)
        $ renpy.pause(5.33)
        $ image.show_video(9)
        $ renpy.pause(5.33)
        $ image.show_video(10)
        aona "That was an amazing warmup, Mr. [headmaster_last_name]!"
        call change_stats_with_modifier(
            inhibition = DEC_LARGE, corruption = LARGE, charm = SMALL) from _call_change_stats_with_modifier_26
    elif school_level == 9:
        $ image.show(1)
        aona "Im making my hair right now, how about a quick pre-workout before class starts? We got a few minutes for that."
        $ image.show(2)
        headmaster "For a girl as pretty as you? Of course I do!"
        $ image.show_video(3, pause = True)
        $ image.show_video(4, pause = True)
        $ image.show_video(5, pause = True)
        $ image.show_video(6, pause = True)
        $ image.show_video(7)
        $ renpy.pause(5.33)
        $ image.show_video(8)
        aona "That was an amazing warmup, Mr. [headmaster_last_name]!"
        call change_stats_with_modifier(
            inhibition = DEC_LARGE, corruption = LARGE, charm = SMALL) from _call_change_stats_with_modifier_29
    elif school_level == 8:
        $ image.show(1)
        aona "Im making my hair right now, how about a quick snack before class starts? We got a few minutes for that."
        $ image.show(2)
        headmaster "For a girl as pretty as you? Of course I do!"
        $ image.show_video(3, pause = True)
        $ image.show_video(4)
        $ renpy.pause(5.33)
        $ image.show_video(5)
        $ renpy.pause(1)
        $ image.show_video(6)
        aona "Thanks for the snack, Mr. [headmaster_last_name]!"
        call change_stats_with_modifier(
            inhibition = DEC_LARGE, corruption = MEDIUM, charm = SMALL) from _call_change_stats_with_modifier_30
    elif school_level == 7:
        $ image.show(1)
        aona "Im fixing my hair right now, how about a proper good luck kiss before class?"
        $ image.show(2)
        headmaster "That sounds like a very good measure!"
        $ image.show_video(3, pause = True)
        call change_stats_with_modifier(
            inhibition = DEC_MEDIUM, corruption = MEDIUM, charm = SMALL) from _call_change_stats_with_modifier_85
    elif school_level >= 5:
        $ image.show(1)
        aona "Just fixing my hair for P.E.\n Say, do you wish we would just run around nude all day?"
        $ image.show(2)
        aona "We just might if you asked us to."
        $ image.show(3)
        aona "*giggle*" (name="School Girls")
        call change_stats_with_modifier(
            inhibition = DEC_SMALL, corruption = SMALL, charm = SMALL) from _call_change_stats_with_modifier_86
    else:
        $ image.show(1)
        aona "Are you getting ready for gym class too, Mr. [headmaster_last_name]?"

        call change_stats_with_modifier(
            inhibition = DEC_TINY, corruption = TINY, charm = TINY) from _call_change_stats_with_modifier_27
    $ end_event('new_daytime', **kwargs)

label gym_event_2 (**kwargs):
    $ begin_event("2", **kwargs)

    $ topic = get_value("topic", **kwargs)

    $ image = convert_pattern("main", **kwargs)

    $ image.show(0)
    if topic == "breasts":
        subtitles "You find yourself in the girls changing room with some bare breasts on display."
    elif topic == "asses":
        subtitles "You find yourself in the girls changing room. You can't help but look on those bare asses."
    else:
        subtitles "You walk in on some girls changing their clothes before P.E."
    
    $ image.show(1)
    subtitles "It took a few seconds for them to realize what is happening."
    $ image.show(2)
    sgirl "*scream*" (name="School Girls", retain = False)
    $ image.show(3)
    headmaster "Sorry, I didn't mean to intrude."
    $ image.show(4)
    subtitles "You run out as fast as you can."
    call change_stats_with_modifier(
        inhibition = DEC_SMALL, happiness = DEC_SMALL, reputation = DEC_SMALL) from _call_change_stats_with_modifier_28

    $ end_event('new_daytime', **kwargs)

label gym_event_3 (**kwargs):
    $ begin_event("2", **kwargs)

    $ image = convert_pattern("main", **kwargs)

    $ kokoro = get_person("class_3a", "kokoro_nakamura").get_character()
    $ zoe = get_person("staff", "zoe_parker").get_character()

    $ image.show(0)
    headmaster "Miss Nakamura! I'm sorry but that top doesn't conform to the uniform policy."
    $ image.show(1)
    kokoro "Whaa... But my normal uniform is in the wash!"
    $ image.show(2)
    headmaster "That's unfortunate but you can't keep wearing this for P.E. It is bad for the hygiene."
    headmaster "The sport clothing is made of special materials that are designed to be worn during sports and have antibacterial properties."
    headmaster "I'm sorry but you will have to take of your top."
    $ image.show(3)
    kokoro "But..."
    $ image.show(4)
    headmaster "Miss Nakamura!"
    $ image.show(5)
    kokoro "O-Okay!"
    $ image.show(6)
    $ image.show(7)
    headmaster "Miss Nakamura, what is that? You are wearing a laced bra as well?!"
    $ image.show(8)
    kokoro "I-I'm sorry, my clothing is..."
    $ image.show(9)
    headmaster "This one is even worse! Laced bras are a hazard during sports and can cause injuries!"
    headmaster "You will have to take that off as well!"
    $ image.show(10)
    kokoro "But..."
    $ image.show(11)
    zoe "Mr. [headmaster_last_name], don't you think that is a bit too much?"
    $ image.show(12)
    headmaster "Miss Parker, I'm sorry but I can't allow this. She has to learn that the rules are there for a reason."
    $ image.show(13)
    headmaster "Miss Nakamura, you will have to take off your bra."
    $ image.show(14)
    kokoro "But..."
    $ image.show(15)
    headmaster "No buts, Miss Nakamura!"
    $ image.show(16)
    kokoro "*whimper*"
    call Image_Series.show_image(image, 17, 18) from _call_gym_event_3_1
    kokoro "*sob*"
    $ image.show(19)
    headmaster "Good, now continue with the class."
    $ image.show(20)
    zoe "..."
    call Image_Series.show_image(image, 21, pause = True) from _call_gym_event_3_2

    call change_stats_with_modifier(
        inhibition = DEC_MEDIUM, happiness = DEC_SMALL, charm = TINY, education = TINY, reputation = DEC_SMALL) from _call_change_stats_with_modifier_31
    $ end_event('new_daytime', **kwargs)

label gym_event_4 (**kwargs):
    $ begin_event(**kwargs)

    $ ishimaru = get_person_char_with_key("class_3a", "ishimaru_maki")
    $ easkey = get_person_char_with_key("class_3a", "easkey_tanaka")

    $ image = convert_pattern("main", **kwargs)

    # two girls bump into each other in the locker room
    call Image_Series.show_image(image, 0, 1, 2) from _call_gym_event_4_1
    easkey "Huh!?" #1
    $ image.show(3)
    ishimaru "Oh! I'm sorry!" #2
    $ image.show(4)
    easkey "It's okay..." #1
    # girls feel awkward
    $ image.show(5)
    easkey "..." #2
    $ image.show(6)
    ishimaru "okay, bye!" #1
    $ image.show(7)
    easkey "Bye!" #2

    call change_stats_with_modifier(
        inhibition = DEC_SMALL, corruption = TINY) from _stats_gym_event_4_1

    $ end_event('new_daytime', **kwargs)

label gym_event_5 (**kwargs):
    $ begin_event("2", **kwargs)

    $ image = convert_pattern("main", **kwargs)

    $ image.show(0)
    sgirl "Haaa..., I wish I could get a massage right now..." #1
    $ image.show(1)
    sgirl "My muscles are so tight..." #1
    $ image.show(2)
    sgirl "Oh yeah that would be awesome!" #2

    call change_stats_with_modifier(
        inhibition = DEC_TINY, happiness = DEC_TINY) from _stats_gym_event_5_1

    $ end_event('new_daytime', **kwargs)
    
label gym_event_6 (**kwargs):
    $ begin_event("2", **kwargs)
    
    $ image = convert_pattern("main", **kwargs)
    
    call Image_Series.show_image(image, 0, 1, 2, pause = True) from _call_gym_event_6_1
    headmaster_thought "..."

    call change_stats_with_modifier(
        inhibition = TINY, charm = TINY) from _stats_gym_event_6_1

    $ end_event('new_daytime', **kwargs)
    

# endregion
#########################

# endregion
###########################