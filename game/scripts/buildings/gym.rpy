##################################
# region Gym Event Handler ----- #
##################################

init -1 python:
    set_current_mod('base')
    def gym_events_available() -> bool:
        return (gym_timed_event.has_available_highlight_events() or
            gym_general_event.has_available_highlight_events() or
            any(e.has_available_highlight_events() for e in gym_events.values())
        )

    gym_timed_event = TempEventStorage("gym_timed", "gym", fallback = Event(2, "gym.after_time_check"))
    gym_general_event = EventStorage("gym_general", "gym", fallback = Event(2, "gym.after_general_check"))
    
    gym_events = {}
    add_storage(gym_events, EventStorage("enter_changing", "gym", fallback_text = "There is nothing to do here."))
    add_storage(gym_events, EventStorage("go_students",    "gym", fallback_text = "There is nobody here."))
    add_storage(gym_events, EventStorage("check_pe",       "gym", fallback_text = "There is nothing to do here."))
    add_storage(gym_events, EventStorage("teach_pe",       "gym", fallback_text = "There is nothing to do here."))

    gym_bg_images = BGStorage("images/background/gym/bg f.webp", ValueSelector('loli', 0),
        BGImage("images/background/gym/bg <loli> <school_level> <teacher_level> <variant> <nude>.webp", 1, TimeCondition(daytime = "c", weekday = "d")), # show gym with students
        BGImage("images/background/gym/bg 7.webp", 1, TimeCondition(daytime = 7)), # show gym at night empty
    )
    
init 1 python:
    set_current_mod('base')
    first_week_gym_event_event = Event(1, "first_week_gym_event",
        IntroCondition(),
        TimeCondition(day = "2-4", month = 1, year = 2023),
        Pattern("main", "images/events/first week/first week gym <step>.webp"),
        thumbnail = "images/events/first week/first week gym 1.webp")

    first_potion_gym_event_event = Event(1, "first_potion_gym_event",
        IntroCondition(),
        TimeCondition(day = 9, month = 1, year = 2023),
        Pattern("main", "images/events/first potion/first potion gym <step>.webp"),
        thumbnail = "images/events/first potion/first potion gym 1.webp")

    gym_event1 = Event(3, "gym_event_1",
        LevelSelector("school_level", "school"),
        StatSelector("corruption", CORRUPTION, "school"),
        RandomListSelector("topic", "shoes", "hair", "ready"),
        DictSelector("topic_text", "topic", {
            "shoes": "putting on my shoes",
            "hair": "doing my hair",
            "ready": "getting ready",
        }),
        TimeCondition(daytime = "c", weekday = "d"),
        Pattern("main", "/images/events/gym/gym_event_1 <school_level> <topic> <step>.webp"),
        thumbnail = "images/events/gym/gym_event_1 1 hair 0.webp")
    
    gym_event2 = Event(3, "gym_event_2",
        LevelSelector("school_level", "school"),
        StatSelector("inhibition", INHIBITION, "school"),
        RandomListSelector("topic", (0.75, "clothe"), "breasts", (0.15, "asses")),
        TimeCondition(daytime = "c", weekday = "d"),
        Pattern("main", "/images/events/gym/gym_event_2 <school_level> <topic> <step>.webp"),
        thumbnail = "images/events/gym/gym_event_2 1 clothe 0.webp")

    gym_event3 = Event(3, "gym_event_3",
        LevelSelector("school_level", "school"),
        RandomValueSelector("variant", 1, 1),
        DictSelector("girl_name", "variant", {
            1: "Kokoro Nakamura",
        }),
        TimeCondition(daytime = "c", weekday = "d"),
        Pattern("main", "/images/events/gym/gym_event_3 <school_level> <variant> <step>.webp"),
        thumbnail = "images/events/gym/gym_event_3 1 1 0.webp")    

    gym_action_tutorial_event = Event(2, "action_tutorial",
        NOT(ProgressCondition('action_tutorial')),
        ValueSelector('return_label', 'gym'),
        NoHighlightOption(),
        TutorialCondition(),
        Pattern("main", "/images/events/misc/action_tutorial <step>.webp"),
        override_location = "misc", thumbnail = "images/events/misc/action_tutorial 0.webp")

    gym_teach_pe_intro_storage = FragmentStorage("gym_teach_pe_intro")
    gym_teach_pe_intro_storage.add_event(
        EventFragment(3, "gym_teach_pe_intro_1",
            Pattern("main", "/images/events/gym/gym_teach_pe_intro_1 <school_level> <step>.webp"),
            thumbnail = "images/events/gym/gym_teach_pe_intro_1 1 7.webp"),
        EventFragment(1, "gym_teach_pe_intro_aona_bra",
            ProgressCondition("aona_sports_bra", 2),
            GameDataSelector("skimpy_bra", "aona_skimpy_sports_bra"),
            Pattern("main", "/images/events/gym/gym_teach_pe_intro_aona_bra <skimpy> <step>.webp", 'skimpy')),
    )

    gym_teach_pe_warm_up_storage = FragmentStorage("gym_teach_pe_warm_up")
    gym_teach_pe_warm_up_storage.add_event(
        EventFragment(3, "gym_teach_pe_warm_up_1",
            Pattern("main", "/images/events/gym/gym_teach_pe_warm_up_1 <school_level> <step>.webp"),
            thumbnail = "images/events/gym/gym_teach_pe_warm_up_1 1 2.webp"),
    )

    gym_teach_pe_main_storage = FragmentStorage("gym_teach_pe_main")
    gym_teach_pe_main_storage.add_event(
        EventFragment(3, "gym_teach_pe_main_1",
            Pattern("main", "/images/events/gym/gym_teach_pe_main_1 <school_level> <step>.webp"),
            thumbnail = "images/events/gym/gym_teach_pe_main_1 1 9.webp"),
        EventFragment(3, "gym_teach_pe_main_aona_bra",
            NOT(ProgressCondition("aona_sports_bra")),
            MoneyCondition("200+"),
            Pattern("main", "/images/events/gym/gym_teach_pe_main_aona_bra <step>.webp")),
        EventFragment(1, "gym_teach_pe_main_aona_bra_2",
            ProgressCondition("aona_sports_bra", 2),
            GameDataSelector("skimpy_bra", "aona_skimpy_sports_bra"),
            Pattern("main", "/images/events/gym/gym_teach_pe_main_aona_bra_2 <step>.webp")),
    )

    gym_teach_pe_end_storage = FragmentStorage("gym_teach_pe_end")
    gym_teach_pe_end_storage.add_event(
        EventFragment(3, "gym_teach_pe_end_1",
            thumbnail = "images/events/gym/gym_teach_pe_main_1 1 14.webp"),
    )

    gym_teach_pe_event = EventComposite(3, 'gym_teach_pe', 
        [
            gym_teach_pe_intro_storage,
            gym_teach_pe_warm_up_storage, 
            gym_teach_pe_main_storage, 
            gym_teach_pe_end_storage
        ],
        TimeCondition(daytime = "c", weekday = "d"),
        LevelSelector("school_level", "school"),
        thumbnail = "images/events/gym/gym_teach_pe_main_1 1 10.webp"
    )

    gym_general_event.add_event(
        gym_action_tutorial_event,
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
        gym_teach_pe_event,
    )

# endregion
##################################

################################
# region Gym Entry Point ----- #
################################

label gym ():
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

######################
# region Intro Event #

label first_potion_gym_event (**kwargs):
    $ begin_event(**kwargs)
    
    $ image = convert_pattern("main", step_start = 1, **kwargs)

    $ image.show(1)
    subtitles "You enter the Gym and see a group of students and teacher in a yoga session."

    $ image.show(2)
    headmaster_thought "Oh that is a sport session I can get behind!"

    $ image.show(3)
    headmaster_thought "Mhh, yes very flexible!"

    $ image.show(4)
    headmaster_thought "Oh they seem to really get into it!"

    $ set_building_blocked("gym")

    $ end_event('new_daytime', **kwargs)

# first week event
label first_week_gym_event (**kwargs):
    $ begin_event(**kwargs)

    $ image = convert_pattern("main", step_start = 1, **kwargs)
    
    $ image.show(1)
    headmaster_thought "Okay, now the Gym. I have been here shortly for my introduction speech but I haven't had the chance to get a thorough look."

    $ image.show(2)
    headmaster_thought "Mhh, doesn't look to shabby..."
    
    $ image.show(3)
    headmaster_thought "Seems to be decently stocked."
    headmaster_thought "The material is well maintained. I guess it's alright."

    $ change_stat("charm", 5, get_school())

    $ set_building_blocked("gym")

    $ end_event('new_daytime', **kwargs)

# endregion
######################

##########################
# region Teach P.E Event #

label gym_teach_pe (**kwargs):
    $ begin_event(**kwargs)

    $ get_level('school_level', **kwargs)

    call composite_event_runner(**kwargs) from _call_composite_event_runner

################
# region INTRO #
label gym_teach_pe_intro_1 (**kwargs):
    $ begin_event(**kwargs)

    $ image = convert_pattern("main", **kwargs)

    call Image_Series.show_image(image, 0, 1, 2, 3, 4, 5, 6, 7, 8, pause = True) from image_gym_teach_pe_intro_1_1

    $ end_event('map_overview', **kwargs)

label gym_teach_pe_intro_aona_bra (**kwargs):
    $ begin_event(**kwargs)

    $ bra = get_value('skimpy_bra', **kwargs)
    $ skimpy = bra != 0

    $ image = convert_pattern("main", skimpy = skimpy, **kwargs)

    $ miwa = Character("Miwa Igarashi", kind = character.sgirl)
    $ aona = Character("Aona Komuro", kind = character.sgirl)

    $ image.show(0)
    miwa "And the headmaster really took you to the city to buy a sports bra?"
    $ image.show(1)
    aona "Yes, he did. He said it was important for my health and performance."
    $ image.show(2)
    aona "It's great that he cares so much about us."
    $ image.show(3)
    miwa "Yes, I didn't think he would be that nice."
    $ image.show(4)
    aona "Didn't you talk to him as well?"
    $ image.show(5)
    miwa "Yeah you're right. He was very empathetic."
    # Aona puts on the bra
    call Image_Series.show_image(image, 6, 7, 8, 9) from image_gym_teach_pe_intro_aona_bra_1
    aona "What do you think?"
    if bra >= 1:
        $ image.show(10)
        miwa "It's a bit skimpy, isn't it?"
        if bra == 2:
            $ image.show(24)
            aona "Yeah, but I think it is quite comfortable and Mr. [headmaster_last_name] said it was good for my health."
            $ image.show(25)
            miwa "I guess you're right. I mean it really does look good on you."
            $ image.show(26)
            aona "Thank you."

            call change_stats_with_modifier('school', 'pe',
                happiness = SMALL, inhibition = DEC_SMALL) from _call_change_stats_with_modifier_17
        else:
            $ image.show(12)
            aona "Yeah unfortunately, the headmaster bought the wrong one!"
            $ image.show(13)
            miwa "What do you mean?"
            $ image.show(14)
            aona "He showed me another one to the one I wanted to buy, saying it would be good for my health, but I said I didn't like it."
            $ image.show(15)
            miwa "Quite perverted by him, isn't it?"
            $ image.show(16)
            aona "I don't know, but I think it's quite comfortable."
            $ image.show(17)
            aona "Maybe it was a genuine mistake."
            $ image.show(18)
            miwa "What do you do now?"
            $ image.show(19)
            aona "I don't know. I guess I have to wear it now. I don't want to have to run with these giant things again."
            $ image.show(20)
            miwa "I guess you're right."
            miwa "But I still think these look really nice on you."
            $ image.show(21)
            aona "Really?"
            $ image.show(22)
            miwa "Yes, really."
            $ image.show(23)
            aona "Mhh, thank you."
            
            call change_stats_with_modifier('school', 'pe',
                happiness = DEC_SMALL, inhibition = DEC_MEDIUM) from _call_change_stats_with_modifier_18
    else:
        $ image.show(10)
        miwa "Yeah, it looks really nice on you."
        $ image.show(11)
        aona "Yeah, doesn't it? And it's quite comfortable too."
        miwa "Amazing!"

        call change_stats_with_modifier('school', 'pe',
            happiness = MEDIUM, inhibition = DEC_TINY) from _call_change_stats_with_modifier_19

    $ end_event('map_overview', **kwargs)

# endregion
################

##################
# region WARM UP #

image anim_gym_teach_pe_warm_up_1_1_1 = Movie(play ="images/events/gym/gym_teach_pe_warm_up_1 1 1.webm", start_image = "images/events/gym/gym_teach_pe_warm_up_1 1 1.webp", loop = True)
image anim_gym_teach_pe_warm_up_1_1_2 = Movie(play ="images/events/gym/gym_teach_pe_warm_up_1 1 2.webm", start_image = "images/events/gym/gym_teach_pe_warm_up_1 1 2.webp", loop = True)
image anim_gym_teach_pe_warm_up_1_1_3 = Movie(play ="images/events/gym/gym_teach_pe_warm_up_1 1 3.webm", start_image = "images/events/gym/gym_teach_pe_warm_up_1 1 3.webp", loop = True)
label gym_teach_pe_warm_up_1 (**kwargs):
    $ begin_event(**kwargs)

    $ image = convert_pattern("main", **kwargs)

    $ image.show(0)
    headmaster "Alright, let's get started with the P.E. class."

    headmaster "First we start with a few warm up exercises and stretching."
    headmaster "Okay now all follow my lead."
    
    $ image.show_video(1, True)
    $ image.show_video(2, True)
    $ image.show_video(3, True)
    
    $ image.show(4)
    headmaster "Alright, that's enough."
    
    call change_stats_with_modifier('school', 'pe',
        charm = SMALL, education = TINY) from _call_change_stats_with_modifier_20

    $ end_event('map_overview', **kwargs)

# endregion
##################

###############
# region MAIN #

label gym_teach_pe_main_1 (**kwargs): # Football
    $ begin_event(**kwargs)

    $ image = convert_pattern("main", **kwargs)
    
    $ image.show(0)
    headmaster "Alright, that's enough. Now let's play some football. I will be the referee."
    $ image.show(1)
    headmaster "Please split into two teams and let's get started."
    $ image.show(2)
    sgirl "I'm sorry but how do we identify the teams? We all wear the same uniform." (name = "Sakura Mori")
    $ image.show(3)
    headmaster "Hmm, that's a good point. Unfortunately we don't have any bibs or anything like that."
    $ image.show(4)
    headmaster "I guess you just will have to remember your team mates. So now your teams please."
    # The students separate into two groups
    call Image_Series.show_image(image, 5, 6) from image_gym_teach_pe_main_1_2   
    headmaster "Alright, let's get started. The right side has the kickoff."
    $ image.show(7)
    headmaster "And... START!"
    call Image_Series.show_image(image, 8, 9, 10, 11, 12, 13) from image_gym_teach_pe_main_1_3
    
    call screen black_screen_text("1 hour later")

    $ image.show(14)
    headmaster "Alright, that's enough for today. I hope you all had fun."
    $ image.show(15)
    headmaster "Don't forget to shower and change your clothes."
    # class leaves the gym
    
    call change_stats_with_modifier('school',  'pe',
        happiness = TINY, charm = SMALL, reputation = TINY, inhibition = DEC_TINY) from _call_change_stats_with_modifier_21

    $ end_event('map_overview', **kwargs)

label gym_teach_pe_main_2 (**kwargs): # Yoga
    $ begin_event(**kwargs)

    $ image = Image_Series("/images/events/gym/gym_teach_pe_main_2 <school_level> <step>.webp", **kwargs)

    $ image.show(0)
    headmaster "Alright, today I planned to do some yoga with you."
    $ image.show(1)
    headmaster "It's a great way to relax and to improve your flexibility."
    headmaster "It's also a great way to improve your balance and to strengthen your muscles."
    $ image.show(2)
    headmaster "I hope to give you a good introduction to it so you can do it at home too."
    headmaster "Regular yoga practice can help you to improve your posture and to reduce stress."
    headmaster "It can also help you to improve your concentration and to improve your mood."
    $ image.show(3)
    headmaster "Now please all get a yoga mat and let's get started."
    # students get a yoga mat
    headmaster "Okay, now we'll just do some simple exercises to get started."
    headmaster "Please take care not to overdo it and to listen to your body."
    headmaster "If something hurts, please stop immediately."
    headmaster "And only stretch as far as you can without pain."
    # first form
    # second form, a student struggles
    headmaster "Don't be frustrated if you can't do it perfectly. It's all about practice."
    headmaster "If you're not flexible enough, just do what you can and if you repeat it often enough, you will get better."
    # third form
    # fourth form, a student is struggling
    # headmaster goes to the student and helps her
    # fifth form
    headmaster "Alright, that's enough for today. I hope you all had fun."
    headmaster "I hope you all had a good time and that you learned something new."
    headmaster "Don't forget to shower and change your clothes."

    call change_stats_with_modifier('school', 'pe',
        happiness = TINY, charm = MEDIUM, inhibition = DEC_TINY) from _call_change_stats_with_modifier_22

    $ end_event('map_overview', **kwargs)

label gym_teach_pe_main_aona_bra (**kwargs): # Running
    $ begin_event(**kwargs)

    $ image = convert_pattern("main", **kwargs)

    $ image.show(0)
    headmaster "Alright, today we will do some running."
    $ image.show(1)
    sgirl "Do we have to? Couldn't we do something else?" (name = "Aona Komuro")
    $ image.show(2)
    headmaster "Yes, it's important to keep your body in shape."
    headmaster "It's also a great way to improve your stamina and to improve your cardiovascular health."
    $ image.show(1)
    sgirl "But I don't like running." (name = "Aona Komuro")
    $ image.show(3)
    headmaster "Why that?"
    $ image.show(4)
    sgirl "Well my... Chest hurts because of... you know why." (name = "Aona Komuro")
    $ image.show(5)
    headmaster "Don't you have a sports bra?"
    $ image.show(6)
    sgirl "No, I don't." (name = "Aona Komuro")
    $ image.show(7)
    headmaster "Hmm, that's quite unfortunate. A state test is coming up and you need to be in shape for it because there will be several running tests."
    headmaster "Unfortunately I can't make an exception for you, so please bear with it for today."
    $ image.show(8)
    sgirl "..." (name = "Aona Komuro")
    $ image.show(9)
    headmaster "Alright, now please line up and let's get started. Today we will be doing sprints."
    call Image_Series.show_image(image, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22) from image_gym_teach_pe_main_aona_bra_1
    # images and animations of the girls running, Aona Komuro is struggling possibly holding her breasts
    
    call screen black_screen_text("1 hour later")

    $ image.show(23)
    headmaster "Alright, that's enough for today."
    headmaster "Don't forget to shower and change your clothes."
    # class leaves the gym
    $ image.show(24)
    headmaster "Aona, can you stay for a moment?"
    $ image.show(25)
    sgirl "Yes, Mr. [headmaster_last_name]?" (name = "Aona Komuro")
    $ image.show(26)
    headmaster "I'm sorry but you need to get a sports bra. It's important for your health and for your performance."
    $ image.show(27)
    sgirl "I know... But I don't have the money for it. Sport bras are terribly expensive for my ... size." (name = "Aona Komuro")
    $ image.show(28)
    headmaster "I see."
    $ image.show(29)
    headmaster "Hmm, I can't just give out money because of the Accounting, but I can get you one if you like."
    $ image.show(30)
    sgirl "Really? That would be great!" (name = "Aona Komuro")
    $ image.show(31)
    headmaster "Alright, let's do it like that, I'm sure I can just write it off as a business expense."
    headmaster "There is no shop nearby, but I could take you to the city after school. Would that be okay for you?"
    $ image.show(30)
    sgirl "Yes, that would be great!" (name = "Aona Komuro")
    sgirl "Thank you so much, Mr. [headmaster_last_name]!" (name = "Aona Komuro")
    $ image.show(31)
    headmaster "Not for that! I became your headmaster to help you all to become the best version of yourself."
    headmaster "And if it means spending a few bucks on a sports bra, then so be it."
    headmaster "Alright, now go and get changed. Come to my office after school, we'll then drive."
    $ image.show(30)
    sgirl "Yes, Mr. [headmaster_last_name]!" (name = "Aona Komuro")
    $ image.show(32)

    $ start_progress("aona_sports_bra")

    call change_stats_with_modifier('school', 'pe',
        happiness = TINY, charm = SMALL, reputation = TINY, inhibition = DEC_TINY) from _call_change_stats_with_modifier_23

    $ end_event('map_overview', **kwargs)

label gym_teach_pe_main_aona_bra_2 (**kwargs):
    $ begin_event(**kwargs)

    $ bra = get_value('skimpy_bra', **kwargs)

    $ image = convert_pattern("main", **kwargs)

    $ image.show(0)
    headmaster "Alright, today we will do some running."
    sgirl "*MOAN*" (name = "Students")
    $ image.show(1)
    headmaster "Yes, Yes! I know! I know! But you know the state test is coming up and you need to be in shape for it."
    $ image.show(2)
    headmaster "So now please line up and let's get started. Today we will be doing laps."
    headmaster "And go!"
    call Image_Series.show_image(image, 3, 4, 5, 6, 7) from image_gym_teach_pe_main_aona_bra_2_1
    headmaster "Alright, that's enough for today. Please shower and change your clothes."
    call Image_Series.show_image(image, 8, pause = True) from image_gym_teach_pe_main_aona_bra_2_2
    if bra == 1:
        call Image_Series.show_image(image, 9, 10, 11) from image_gym_teach_pe_main_aona_bra_2_3
        sgirl "Mr. [headmaster_last_name], I'm sorry but you bought the wrong bra." (name = "Aona Komuro")
        $ image.show(12)
        headmaster "What do you mean?"
        $ image.show(13)
        sgirl "This is the bra you offered me, which I didn't want to buy." (name = "Aona Komuro")
        $ image.show(14)
        headmaster "Oh I'm sorry. I must've swapped them by accident."
        headmaster "But why are you wearing it then?"
        $ image.show(15)
        sgirl "I didn't want to run without a bra again, so I didn't have a choice." (name = "Aona Komuro")
        $ image.show(16)
        headmaster "I see. But how did you feel in it? I mean, it looked like you were much more comfortable than before."
        $ image.show(17)
        sgirl "Well to be honest, it worked really well. It was quite comfortable and I didn't have any problems with my breasts." (name = "Aona Komuro")
        $ image.show(18)
        headmaster "And nobody cared, did they?"
        $ image.show(19)
        sgirl "Well... no." (name = "Aona Komuro")
        $ image.show(20)
        headmaster "So how about you try it on for a few more days and see how it goes?"
        $ image.show(21)
        sgirl "Mhh... Okay, I'll try it for now." (name = "Aona Komuro")
        $ image.show(22)
        headmaster "Alright, now go and get changed. You wouldn't want to miss your break, would you?"
        $ image.show(21)
        sgirl "No, thanks."

        call change_stats_with_modifier('school', 'pe',
            happiness = TINY, charm = SMALL, inhibition = DEC_SMALL) from _call_change_stats_with_modifier_24
    else:
        call change_stats_with_modifier('school', 'pe',
            happiness = SMALL, charm = SMALL, inhibition = DEC_SMALL) from _call_change_stats_with_modifier_25
    
    $ advance_progress("aona_sports_bra")

    $ end_event('map_overview', **kwargs)

# endregion
###############

##############
# region END #

label gym_teach_pe_end_1 (**kwargs):
    $ begin_event(**kwargs)

    $ end_event('new_daytime', **kwargs)

# endregion
##############
# endregion
##########################

#########################
# region Regular Events #

label gym_event_1 (**kwargs):
    $ begin_event(**kwargs)

    $ school_level = get_value('school_level', **kwargs)
    $ corruption = get_stat_value("corruption", [5, 100], **kwargs)
    $ topic_variant = get_value("topic", **kwargs)
    $ topic = get_value("topic_text", **kwargs)

    $ image = convert_pattern("main", **kwargs)

    $ image.show(0)
    subtitles "In the Gym, you see a girl getting ready for P.E."

    # if corruption >= 80:
    #     show screen black_screen_text("gym_event_1\ncorruption >= 80")
    #     sgirl "Im [topic] right now, how about a quick make out session before class starts? We got a few minutes for that." (name = girls[school_name][0])
    #     headmaster "For a girl as pretty as you? Of course I do!"
    #     subtitles "After she is ready, you spend a few minutes making out with her."
    #     call change_stats_with_modifier(school_obj, 
    #         inhibition = DEC_LARGE, corruption = MEDIUM, charm = SMALL)
    # elif corruption >= 60:
    #     show screen black_screen_text("gym_event_1\ncorruption >= 60")
    #     sgirl "Im [topic] now, how about a proper good luck kiss before class?" (name = girls[school_name][0])
    #     headmaster "That sounds like a very good measure!"
    #     subtitles "After she is ready, you french kiss her for a minute."
    #     call change_stats_with_modifier(school_obj, 
    #         inhibition = DEC_MEDIUM, corruption = MEDIUM, charm = SMALL)
    # elif corruption >= 40:
    #     show screen black_screen_text("gym_event_1\ncorruption >= 40")
    #     sgirl "just [topic] for P.E.\n Say, do you wish we would just run around nude all day?" (name = girls[school_name][0])
    #     sgirl "We just might if you asked us to." (name = girls[school_name][1])
    #     # tease headmaster -> run off
    #     sgirl "*giggle*" (name="School Girls")
    #     call change_stats_with_modifier(school_obj, 
    #         inhibition = DEC_SMALL, corruption = MEDIUM, charm = SMALL)
    # elif corruption >= 20:
    #     show screen black_screen_text("gym_event_1\ncorruption >= 20")
    #     sgirl "Just [topic] for P.E.\n Say, do you wish we would just run around in underwear all day?" (name = girls[school_name][0])
    #     sgirl "We just might if you asked us to." (name = girls[school_name][1])
    #     # tease headmaster -> run off
    #     sgirl "*giggle*" (name="School Girls")
    #     call change_stats_with_modifier(school_obj, 
    #         inhibition = DEC_SMALL, corruption = SMALL, charm = SMALL)
    if corruption > 5:
        $ image.show(1)
        sgirl "Just give me a moment more to get ready for class. You like watching me doing whatever, right?" (name="Aona Komuro")

        $ image.show(2)
        headmaster "As pretty as you are? I sure do!"

        call change_stats_with_modifier('school', 
            inhibition = DEC_SMALL, corruption = TINY, charm = TINY) from _call_change_stats_with_modifier_26
    else:
        $ image.show(1)
        sgirl "Are you getting ready for gym class too, Mr. [headmaster_last_name]?" (name="Aona Komuro")

        call change_stats_with_modifier('school', 
            inhibition = DEC_TINY, corruption = TINY, charm = TINY) from _call_change_stats_with_modifier_27
    $ end_event('new_daytime', **kwargs)

label gym_event_2 (**kwargs):
    $ begin_event(**kwargs)

    $ school_level = get_value('school_level', **kwargs)
    $ inhibition = get_stat_value("inhibition", [100], **kwargs)
    $ topic = get_value("topic", **kwargs)

    $ image = convert_pattern("main", **kwargs)

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
    call change_stats_with_modifier('school', 
        inhibition = DEC_SMALL, happiness = DEC_SMALL, reputation = DEC_SMALL) from _call_change_stats_with_modifier_28
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
    #     call change_stats_with_modifier(school_obj,
    #         inhibition = DEC_SMALL, happiness = DEC_SMALL)
    # else:
    # show screen black_screen_text("gym_event_2\ntopic_[topic] inhibition < 30")
    # sgirl "Ahh!"
    # headmaster "Sorry, is everything alright?"
    # sgirl "Yes, I was just surprised."
    # call change_stats_with_modifier(school_obj,
    #     inhibition = DEC_MEDIUM)

    $ end_event('new_daytime', **kwargs)
label .sorry (**kwargs):
    
    $ begin_event()
    
    sgirl "Okay..."
    headmaster_thought "I think she doesn't believe me..."
    call change_stats_with_modifier('school',
        happiness = DEC_MEDIUM, reputation = DEC_SMALL) from _call_change_stats_with_modifier_29
    $ end_event('new_daytime', **kwargs)
label .escape (**kwargs):
    
    $ begin_event()
    
    sgirl "Oh, I was just..."
    headmaster "It's okay. You couldn't possible know."
    subtitles "You leave the room and leave the girls behind dumbfounded."
    call change_stats_with_modifier('school',
        inhibition = DEC_MEDIUM, happiness = DEC_SMALL) from _call_change_stats_with_modifier_30
    $ end_event('new_daytime', **kwargs)

label gym_event_3 (**kwargs):
    $ begin_event(**kwargs)

    $ school_level = get_value('school_level', **kwargs)
    $ variant = get_value("variant", **kwargs)
    $ girl = get_value("girl_name", **kwargs)

    $ girl_name = girl.split(" ")[0]
    $ girl_full_name = girl

    $ image = convert_pattern("main", **kwargs)

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

    call change_stats_with_modifier('school',
        inhibition = DEC_MEDIUM, happiness = DEC_SMALL, charm = TINY, education = TINY, reputation = DEC_SMALL) from _call_change_stats_with_modifier_31
    $ end_event('new_daytime', **kwargs)

# endregion
#########################

# endregion
###########################