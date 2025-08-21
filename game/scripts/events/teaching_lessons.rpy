init -1 python:
    set_current_mod('base')
    
    gym_teach_pe_intro_storage = FragmentStorage("gym_teach_pe_intro")
    gym_teach_pe_entrance_storage = FragmentStorage("gym_teach_pe_entrance")
    gym_teach_pe_warm_up_storage = FragmentStorage("gym_teach_pe_warm_up")
    gym_teach_pe_main_storage = FragmentStorage("gym_teach_pe_main")
    gym_teach_pe_end_storage = FragmentStorage("gym_teach_pe_end")

init 1 python:
    set_current_mod('base')

    ########################
    # region Teaching events
    sb_event_teach_class_event = EventSelect(3, "teach_class_event", "What subject do you wanna teach?", sb_teach_events,
        TimeCondition(weekday = "d", daytime = "c"),
        KwargsSelector(show_proficiency_modifier = True),
        override_menu_exit = 'school_building')

    ###########################
    # region Theoretical Sex Ed

    sb_teach_sex_ed_intro_storage.add_event(
        EventFragment(3, 'sb_teach_sex_ed_intro_anatomy',
            CheckReplay(ValueCondition('topic', 'anatomy')),
            Pattern("main", "/images/events/teaching/sex_ed/intro_1/teaching_sex_ed_intro_1 <step>.webp")),
        EventFragment(3, 'sb_teach_sex_ed_intro_sex_curiosity',
            CheckReplay(ValueCondition('topic', 'sex_curiosity')),
            Pattern("main", "/images/events/teaching/sex_ed/intro_2/teaching_sex_ed_intro_2 <step>.webp"))
    )

    sb_teach_sex_ed_main_storage.add_event(
        EventFragment(3, 'sb_teach_sex_ed_main_anatomy_1',
            CheckReplay(ValueCondition('topic', 'anatomy')),
            Pattern("main", "/images/events/teaching/sex_ed/main/anatomy_1/teaching_sex_ed_main_anatomy_1 <step>.webp")),
        EventFragment(3, 'sb_teach_sex_ed_main_sex_curiosity_1',
            CheckReplay(ValueCondition('topic', 'sex_curiosity')),
            Pattern("main", "/images/events/teaching/sex_ed/main/sex_curiosity_1/teaching_sex_ed_main_sex_curiosity_1 <step>.webp"))
    )

    sb_teach_sex_ed_qa_storage.add_event(
        EventFragment(3, 'sb_teach_sex_ed_qa_1',
            Pattern("main", "/images/events/teaching/sex_ed/qa_1/teaching_sex_ed_qa_1 <step>.webp")),
        EventFragment(3, 'sb_teach_sex_ed_qa_2',
            Pattern("main", "/images/events/teaching/sex_ed/qa_2/teaching_sex_ed_qa_2 <step>.webp"))
    )

    sb_teach_sex_ed_event = EventComposite(3, 'sb_teach_sex_ed', [sb_teach_sex_ed_intro_storage, sb_teach_sex_ed_main_storage, sb_teach_sex_ed_qa_storage],
        TimeCondition(weekday = "d", daytime = "c"),
        LevelSelector('school_level', 'school'),
        ProficiencyCondition('sex_ed'),
        RandomListSelector('topic', 'anatomy', 'sex_curiosity'),
        Pattern("main", "/images/events/teaching/sex_ed/sb_teach_sex_ed.webp"),
        thumbnail = "/images/events/teaching/sex_ed/main_1/teaching_sex_ed_main_1 1 10.webp")

    # endregion
    ###########################

    ######################
    # region Math Teaching
    
    sb_teach_math_ld_storage.add_event(
        EventFragment(3, 'sb_teach_math_ld_1', 
            Pattern("main", "/images/events/teaching/math/ld_1/teaching_math_ld_1 <step>.webp"),
            thumbnail = "/images/events/teaching/math/ld_1/teaching_math_ld_1 1.webp"),
        EventFragment(3, 'sb_teach_math_ld_2', 
            RandomListSelector('ld_girl_name', 'seraphina_clark', 'hatano_miwa', 'soyoon_yamamoto'),
            Pattern("main", "/images/events/teaching/math/ld_2/teaching_math_ld_2 <ld_girl_name> <school_level> <step>.webp", 'ld_girl_name', 'school_level'),
            thumbnail = "/images/events/teaching/math/ld_2/teaching_math_ld_2 seraphina_clark 1 6.webp"),
        EventFragment(3, 'sb_teach_math_ld_3',
            Pattern("main", "/images/events/teaching/math/ld_3/teaching_math_ld_3 <school_level> <step>.webp"),
            thumbnail = "/images/events/teaching/math/ld_3/teaching_math_ld_3 1 0.webp"),
    )

    sb_teach_math_main_storage.add_event(
        EventFragment(3, 'sb_teach_math_main_1',
            RandomListSelector('main_girl_name', 'seraphina_clark', 'hatano_miwa'),
            RandomListSelector('main_topic', 'normal', 'sleeping'),
            Pattern("main", "/images/events/teaching/math/main_1/teaching_math_main_1 <main_girl_name> <school_level> <step>.webp", 'main_girl_name', 'school_level'),
            thumbnail = "images/events/teaching/math/main_1/teaching_math_main_1 seraphina_clark 1 0.webp"),
        EventFragment(3, 'sb_teach_math_main_2',
            LevelCondition("3-", "school"),
            Pattern("main", "/images/events/teaching/math/main_2/teaching_math_main_2 <school_level> <step>.webp", "school_level"),
            thumbnail = "images/events/teaching/math/main_2/teaching_math_main_2 1 7.webp")
    )

    sb_teach_events["math"].add_event(
        EventComposite(3, 'sb_teach_math', [sb_teach_math_ld_storage, sb_teach_math_main_storage],
            TimeCondition(weekday = "d", daytime = "c"),
            LevelSelector('school_level', 'school'),
            ProficiencyCondition('math'),
            Pattern("main", "/images/events/teaching/math/sb_teach_math.webp"),
            thumbnail = "images/events/teaching/math/main_1/teaching_math_main_1 # 1 18.webp"))
    # endregion
    ######################

    #########################
    # region History Teaching
    sb_teach_history_intro_storage.add_event(
        EventFragment(3, 'sb_teach_history_intro_f_revolution_1',
            CheckReplay(ValueCondition('topic', 'french revolution')),
            Pattern("main", "/images/events/teaching/history/french_revolution/intro_1/teaching_history_fr_intro_1 <step>.webp"))
    )

    sb_teach_history_main_storage.add_event(
        EventFragment(3, 'sb_teach_history_main_f_revolution_1',
            CheckReplay(ValueCondition('topic', 'french revolution')),
            Pattern("main", "/images/events/teaching/history/french_revolution/main_1/teaching_history_fr_main_1 <school_level> <step>.webp", 'school_level')),
        EventFragment(3, 'sb_teach_history_main_f_revolution_2',
            CheckReplay(ValueCondition('topic', 'french revolution')),
            Pattern("main", "/images/events/teaching/history/french_revolution/main_2/teaching_history_fr_main_2 <school_level> <step>.webp", 'school_level')),
    )
    
    sb_teach_events["history"].add_event(
        EventComposite(3, 'sb_teach_history', [sb_teach_history_intro_storage, sb_teach_history_main_storage],
            TimeCondition(weekday = "d", daytime = "c"),
            LevelSelector('school_level', 'school'),
            RandomListSelector('topic', 'french revolution'),
            ProficiencyCondition('history'),
            Pattern("main", "/images/events/teaching/history/sb_teach_history.webp"),
            thumbnail = "/images/events/teaching/history/french_revolution/main_1/teaching_history_fr_main_1 1 2.webp")
    )
    # endregion
    #########################

    ######################
    # region P.E. Teaching

    gym_teach_pe_intro_storage.add_event(
        EventFragment(3, "gym_teach_pe_intro_2",
            Pattern("main", "/images/events/teaching/pe/intro/intro_2/teaching_pe_intro_2 <step>.webp"),
            thumbnail = "images/events/teaching/pe/intro/intro_2/teaching_pe_intro_2 5.webp"),
    )

    gym_teach_pe_entrance_storage.add_event(
        EventFragment(3, "gym_teach_pe_entrance_1",
            Pattern("main", "/images/events/teaching/pe/entrance/entrance_1/teaching_pe_entrance_1 <school_level> <step>.webp", "school_level"),
            thumbnail = "images/events/teaching/pe/entrance/entrance_1/teaching_pe_entrance_1 1 7.webp"),
    )

    gym_teach_pe_warm_up_storage.add_event(
        EventFragment(3, "gym_teach_pe_warm_up_1",
            Pattern("main", "/images/events/teaching/pe/warm_up/warm_up_1/teaching_pe_warm_up_1 <school_level> <step>.webp"),
            thumbnail = "images/events/teaching/pe/warm_up/warm_up_1/teaching_pe_warm_up_1 1 2.webp"),
    )

    gym_teach_pe_main_storage.add_event(
        EventFragment(3, "gym_teach_pe_main_1",
            Pattern("main", "/images/events/teaching/pe/main/main_1/teaching_pe_main_1 <school_level> <step>.webp"),
            thumbnail = "images/events/teaching/pe/main/main_1/teaching_pe_main_1 1 9.webp"),
    )

    gym_teach_pe_end_storage.add_event(
        EventFragment(3, "gym_teach_pe_end_1",
            thumbnail = "images/events/teaching/pe/end/end_1/teaching_pe_end_1 1 14.webp"),
    )

    gym_teach_pe_event = EventComposite(3, 'gym_teach_pe', 
        [
            gym_teach_pe_intro_storage,
            gym_teach_pe_entrance_storage,
            gym_teach_pe_warm_up_storage, 
            gym_teach_pe_main_storage, 
            gym_teach_pe_end_storage
        ],
        TimeCondition(daytime = "c", weekday = "d"),
        LevelCondition("1-3", "school"),
        LevelSelector("school_level", "school"),
        thumbnail = "images/events/teaching/pe/intro/intro_1/teaching_pe_intro_1 1 7.webp"
    )

    # endregion
    ######################
    
    gym_events["teach_pe"].add_event(
        gym_teach_pe_event,
    )

    sb_events["teach_class"].add_event(
        sb_event_teach_class_event,
        first_class_sb_event_event
    )

    # endregion
    ########################

label first_class_sb_event (**kwargs):
    $ begin_event(**kwargs)

    $ school_class = get_value('class', **kwargs)

    $ finola = get_person("staff", "finola_ryan").get_character()

    $ image = convert_pattern("main", **kwargs)

    $ image.show(0)
    headmaster "Hello, let me introduce myself again. I'm [headmaster_first_name] [headmaster_last_name], the new headmaster of this school."
    $ image.show(1)
    headmaster "I'm actually a psychologist but I got myself a teaching license to help students like you to receive a better education."
    headmaster "Don't worry, you will still be taught by your regular teachers. I work mainly on school reform and will only occasionally teach a class."
    $ image.show(2)
    headmaster "If you have any questions or issues, feel free to come to me. I always put heavy emphasis on the well-being of my students."
    $ image.show(3)
    headmaster "Now I'd like to get to know you a bit better. Would you please all introduce yourself?"

    $ image.show(4)
    headmaster "Miss Ryan, would you like to start?"
    $ image.show(5)
    finola "Yes, of course."
    finola "My name is Finola Ryan. I'm 28 years old and I'm a teacher for English and Geography. I am also the class teacher of 3A."

    $ image.show(6)
    headmaster "Great! Now please the rest of the class."

    # students introduce themselves
    $ image.show(7)
    sgirl "Hello, I am Gloria Goto. I'm 19 years old." (name="Gloria Goto", retain = False)
    $ image.show(8)
    sgirl "Hi I am Luna Clark. I'm 18 years old." (name="Luna Clark", retain = False)
    $ image.show(9)
    sgirl "Hi I am Seraphina Clark. I'm also 18 years old." (name="Seraphina Clark", retain = False)
    $ image.show(10)
    sgirl "H-Hi, I'm Easkey Tanaka. I'm 19 years old." (name="Easkey Tanaka", retain = False)
    $ image.show(11)
    sgirl "I'm Kokoro Nakamura. I'm 20 years old." (name="Kokoro Nakamura", retain = False)
    $ image.show(12)
    sgirl "Lin Kato. 20 years old." (name="Lin Kato", retain = False)
    $ image.show(13)
    sgirl "Hello, I'm Miwa Igarashi. I'm 19 years old." (name="Miwa Igarashi", retain = False)
    $ image.show(14)
    sgirl "Hi, I'm Aona Komuro. I'm 18 years old." (name="Aona Komuro", retain = False)
    $ image.show(15)
    sgirl "Hi. Yuriko Oshima. I'm 22 years old." (name="Yuriko Oshima", retain = False)
    $ image.show(16)
    sgirl "Hello, my name is Ishimaru Maki. I'm 19 years old." (name="Ishimaru Maki", retain = False)
    $ image.show(17)
    sgirl "I'm Ikushi Ito. 20 years old." (name="Ikushi Ito", retain = False)
    $ image.show(18)
    sgirl "Sakura Mori. 21." (name="Sakura Mori", retain = False)
    $ image.show(19)
    sgirl "Hi, my name is Elsie Johnson. I'm 21 years old." (name="Elsie Johnson", retain = False)
    $ image.show(20)
    sgirl "Hi. I'm Hatano Miwa. 19 years." (name="Hatano Miwa", retain = False)
    $ image.show(21)
    sgirl "Hello. Soyoon Yamamoto. 18 years." (name="Soyoon Yamamoto", retain = False)

    $ image.show(22)
    headmaster "Thank you all for introducing yourself. I'm looking forward to working with you."
    headmaster "Now I'll return you back to Miss Ryan. Have a good day."

    $ set_game_data('first_class_3A', True)
    $ advance_progress('first_class')
    $ set_progress('first_class', 3)

    call change_stats_with_modifier(
        happiness = TINY, charm = SMALL, education = TINY) from _call_change_stats_with_modifier_53

    call change_stats_with_modifier(
        happiness = TINY, charm = SMALL, education = TINY) from _call_change_stats_with_modifier_54

    $ end_event('new_daytime', **kwargs)

###############################
# region Teach Subject Events #

########################
# region SEX EDUCATION #

label sb_teach_sex_ed (**kwargs):
    $ begin_event(**kwargs)

    $ get_value('school_level', **kwargs)

    $ get_value('topic', **kwargs)

    $ show_pattern("main", **kwargs)
    headmaster "Good morning everyone. Let's start with todays subject Sex Education."

    call composite_event_runner(**kwargs) from _call_composite_event_sex_ed_3

################
# region INTRO #

label sb_teach_sex_ed_intro_anatomy (**kwargs):
    $ begin_event(**kwargs)

    $ show_pattern("main", **kwargs)
    headmaster "Good afternoon, class. Today we'll be discussing human anatomy in the context of sexual health and development."

    $ end_event('map_entry', **kwargs)

label sb_teach_sex_ed_intro_sex_curiosity (**kwargs):
    $ begin_event(**kwargs)

    $ show_pattern("main", **kwargs)
    headmaster "I know many of you may have questions about sex and relationships. Today we'll explore some common curiosities in an open, respectful environment."

    $ end_event('map_entry', **kwargs)

# endregion
################

################
# region MAIN #

label sb_teach_sex_ed_main_anatomy_1 (**kwargs):
    $ begin_event(**kwargs)

    $ image = convert_pattern("main", **kwargs)

    headmaster "As you can see here, both males and females have external genitalia that serve important functions for reproduction and pleasure."
    headmaster "In girls, these include the labia minora and majora surrounding the vulva..."
    headmaster "...and in boys, it's their penis."
    # notice a student raising their hand
    headmaster "Yes, Gloria?"
    gloria "Why do we need both clitoris and vagina if they're for pleasure?"

    headmaster "Excellent question! The clitoris is highly sensitive and designed specifically for sexual arousal."
    headmaster "Meanwhile, the vagina has multiple purposes - it protects reproductive organs during childbirth, allows menstrual flow to exit the body..."
    headmaster "...and also enables pleasurable intercourse when engaged with a partner."

    headmaster "Boys' anatomy includes not only their penis but also testes containing sperm and seminal vesicles that produce semen."
    headmaster "Girls have ovaries producing eggs for fertilization by sperm during sex."

    $ end_event('map_entry', **kwargs)

label sb_teach_sex_ed_main_sex_curiosity_1 (**kwargs):
    $ begin_event(**kwargs)

    $ image = convert_pattern("main", **kwargs)

    headmaster "Who here has heard rumors or myths about certain sexual acts but isn't sure what's true?"
    # a few students raise their hands
    headmaster "Let's examine these together. For instance, some claim that anal sex always hurts...but for many people it can be pleasurable when done safely and with the right partner."
    
    aona "My friend says girls only want boys to penetrate them during sex?"
    headmaster "That's an oversimplification. While penetration is a common aspect of sexual intimacy, women often crave emotional connection as much as physical pleasure from their partners."
    headmaster "Communication about desires and boundaries is key."

    headmaster "Remember, it's natural to have questions about sex - but make sure you're getting accurate information rather than relying on rumors or untrustworthy sources online."
    headmaster "If you ever need advice, consider talking to a parent, teacher...or even me."

    $ end_event('map_entry', **kwargs)

# endregion
################

################
# region Q&A #

label sb_teach_sex_ed_qa_1 (**kwargs):
    $ begin_event(**kwargs)

    $ image = convert_pattern("main", **kwargs)

    kokoro "Do girls always get wet when they're excited?"
    headmaster "No, arousal can manifest in various ways besides vaginal lubrication. "
    headmaster "Some may experience tingling or warmth while others might not exhibit any external signs of excitement at all."
    kokoro "What about the difference between orgasm and just feeling good during sex?"
    headmaster "While both sensations are pleasurable, an orgasm typically involves a sudden peak of intense pleasure, often accompanied by physical contractions."
    headmaster "It's like reaching the climax in a story - everything builds up to that momentary release."

    $ end_event('map_entry', **kwargs)

label sb_teach_sex_ed_qa_2 (**kwargs):
    $ begin_event(**kwargs)

    $ image = convert_pattern("main", **kwargs)

    luna "How often do teens usually have sex?"
    headmaster "There's no one-size-fits-all answer here. Frequency depends on individual development and relationship dynamics."
    headmaster "What matters most is that both partners are comfortable with the pace and fully consensual in their sexual activities."
    headmaster "But, for most teens, it's usually multiple times a month."

    $ end_event('map_entry', **kwargs)

# endregion
################

# endregion
########################

##################
# region HISTORY #

label sb_teach_history (**kwargs):
    $ begin_event(**kwargs)

    $ get_value('school_level', **kwargs)
    $ get_value('topic', **kwargs)

    # headmaster enters room
    # call show_image ("/images/events/school building/sb_teach_history.webp", **kwargs) from _call_show_image_sb_teach_history_event_1
    $ show_pattern("main", **kwargs)
    headmaster "Good morning everyone. Let's start with todays subject History."

    call composite_event_runner(**kwargs) from _call_composite_event_runner_1

################
# region INTRO #

label sb_teach_history_intro_f_revolution_1 (**kwargs):
    $ begin_event(**kwargs)

    $ image = convert_pattern('main', **kwargs)
    # $ image = Image_Series("/images/events/school building/sb_teach_history_intro_f_revolution_1 <step>.webp", **kwargs)

    $ image.show(0)
    headmaster "Today we're going to continue learning about one of the most significant events in world history - the French Revolution."
    $ image.show(1)
    headmaster "This event, which took place from 1789 to 1799, had a profound impact on modern society and politics."
    $ image.show(2)
    headmaster "To set the stage, let's quickly review what was happening in France before the Revolution."
    $ image.show(3)
    headmaster "In the late 18th century, France was ruled by an absolute monarch, King Louis XVI."
    $ image.show(4)
    headmaster "The country was deeply in debt due to expensive wars and lavish spending on royal projects."
    $ image.show(5)
    headmaster "Meanwhile, the common people of France - including peasants, artisans, and merchants - were struggling with poverty, inequality, and limited social mobility."

    call change_stats_with_modifier('history',
        education = TINY) from _call_change_stats_with_modifier_55

    $ end_event('map_entry', **kwargs)

# endregion
################

###############
# region MAIN #

label sb_teach_history_main_f_revolution_1 (**kwargs):
    $ begin_event(**kwargs)

    $ sakura = get_person("class_3a", "sakura_mori").get_character()
    $ luna = get_person("class_3a", "luna_clark").get_character()
    $ easkey = get_person("class_3a", "easkey_tanaka").get_character()

    $ image = convert_pattern("main", **kwargs)

    $ image.show(0)
    headmaster "Now today we talk about the causes of the Revolution."
    $ image.show(1)
    headmaster "Okay I want you to open your books on page 23 and inform yourself about the causes of the French Revolution."
    $ image.show(2)
    headmaster "If you got any questions, feel free to ask."
    headmaster "I'll give you 20min to read the text and then we'll discuss it together."
    $ image.show(3)
    headmaster "Now please begin."
    call screen black_screen_text("20 minutes later.")
    $ image.show(4)
    headmaster "Okay time is up."
    $ image.show(5)
    headmaster "So, who can tell me what the main causes of the French Revolution were?"
    # sakura raises her hand
    call Image_Series.show_image(image, 6, 7) from _call_show_image_sb_teach_history_main_f_revolution_1_event_1
    headmaster "Sakura?"
    
    $ image.show(8)
    sakura "One of the main causes was the financial crisis in France."
    $ image.show(9)
    sakura "The country was deeply in debt due to expensive wars and lavish spending by the royal family."
    $ image.show(10)
    sakura "The common people were heavily taxed to pay off this debt, which led to widespread poverty and discontent."

    $ image.show(11)
    headmaster "Yes, that's correct. The financial crisis was a major factor in the Revolution. What else?"
    # Luna raises her hand
    $ image.show(12)
    headmaster "Luna?"

    $ image.show(13)
    luna "Another important cause was the social inequality."

    $ image.show(14)
    headmaster "Could you elaborate on that?"

    $ image.show(15)
    luna "Sure. In the 18th century, French society was divided into three estates: the clergy, the nobility, and the common people."
    $ image.show(16)
    luna "The clergy and nobility enjoyed special privileges and exemptions from taxes, while the common people bore the brunt of the tax burden."
    $ image.show(15)
    luna "This unequal distribution of wealth and power created resentment and social unrest among the lower classes."

    $ image.show(17)
    headmaster "Very good Luna."
    $ image.show(18)
    headmaster "There was another cause that was very important. Easkey, can you tell us what it was?"

    $ image.show(19)
    easkey "Huh? I... Uh... I-I think it was... Uhm..."
    $ image.show(20)
    easkey "I think it was the lack of representation of the common people in government decisions."

    $ image.show(21)
    headmaster "Exactly. The Third Estate, which represented the common people, had little say in government decisions despite making up the majority of the population."
    $ image.show(22)
    headmaster "This lack of political representation and voice in government led to growing discontent and demands for reform."
    $ image.show(23)
    headmaster "These were just a few of the causes of the French Revolution. It was a complex and multifaceted event with many contributing factors."
    $ image.show(24)
    headmaster "But understanding these causes is crucial to understanding the Revolution and its impact on history."

    $ image.show(25)
    headmaster "Unfortunately, that's all for today. Please read the text on page 24 for homework."
    headmaster "We'll continue our discussion another time."

    call change_stats_with_modifier('history',
        education = SMALL) from _call_change_stats_with_modifier_56

    $ end_event('new_daytime', **kwargs)

label sb_teach_history_main_f_revolution_2 (**kwargs):
    $ begin_event(**kwargs)

    $ image = convert_pattern("main", **kwargs)

    $ image.show(0)
    headmaster "Today we will talk about the early stages of the French Revolution."
    $ image.show(1)
    headmaster "More accurately, I want you to inform yourself and write a short essay until next time."
    $ image.show(2)
    headmaster "I want you to focus on three events. The national assembly, the tennis court oath and the storming of the bastille."
    $ image.show(3)
    headmaster "You get until the end of the lesson to work on it."
    $ image.show(4)
    headmaster "If you're not finished by then, please finish it by the end of the week. I'll get Ms. Ryan to collect them."
    $ image.show(5)
    headmaster "Now please start."
    call screen black_screen_text("40 minutes later.")
    $ image.show(6)
    headmaster "Okay, class is over. Please don't forget to finish your essay until the end of the week."

    call change_stats_with_modifier('history',
        education = TINY, happiness = DEC_TINY) from _call_change_stats_with_modifier_57

    $ end_event('new_daytime', **kwargs)

# endregion
###############

# endregion
##################

###############
# region MATH #

label sb_teach_math (**kwargs):
    $ begin_event(**kwargs)

    $ get_value('school_level', **kwargs)

    # headmaster enters room
    $ show_pattern("main", **kwargs)
    headmaster "Good morning everyone. Let's start with todays subject Math."

    call composite_event_runner(**kwargs) from _call_composite_event_runner_2

################
# region INTRO #

label sb_teach_math_ld_1 (**kwargs):
    $ begin_event(**kwargs)

    $ image = convert_pattern("main", **kwargs)

    $ image.show(0)
    headmaster "Is there anything you want to reiterate from the last time?"

    $ image.show(1)
    headmaster "Okay, then let's continue with the new topic."

    $ end_event('map_entry', **kwargs)

label sb_teach_math_ld_2 (**kwargs):
    $ begin_event(**kwargs)

    $ ld_girl_name = get_value('ld_girl_name', **kwargs)

    $ girl = get_person("class_3a", ld_girl_name).get_character()

    $ image = convert_pattern("main", **kwargs)

    $ image.show(0)
    headmaster "Is there anything you want to reiterate from the last time?"
    
    $ image.show(1)
    girl "Yes, I'm sorry. I didn't understand the last topic."

    $ image.show(2)
    headmaster "No problem. I'll explain it again."

    $ image.show(3)
    headmaster "Imagine..."

    $ image.show(4)
    headmaster "Imagine..."

    call black_screen_text("15 minutes later.") from _call_black_screen_text

    # call screen black_screen_text("15 minutes later.")

    $ image.show(5)
    headmaster "That is all."
    headmaster "Do you understand it better now?"

    $ image.show(6)
    girl "Yes, thank you."

    $ image.show(7)
    headmaster "Good. Now let's continue with the new topic."

    call change_stats_with_modifier('math',
        education = TINY) from _call_change_stats_with_modifier_58

    $ end_event('map_entry', **kwargs)

label sb_teach_math_ld_3 (**kwargs):
    $ begin_event(**kwargs)
    
    $ image = convert_pattern("main", **kwargs)

    $ image.show(0)
    subtitles "A student tripped while handing out assignments in class."

    $ image.show(1)
    $ call_custom_menu_with_text("What do you do?", character.subtitles, False,
        MenuElement("Leave alone", "Leave alone", EventEffect("sb_teach_math_ld_3.leave")),
        MenuElement("Help her up", "Help her up", EventEffect("sb_teach_math_ld_3.help")), 
    **kwargs)
label .leave (**kwargs):
    $ begin_event(**kwargs)
    
    $ image.show(2)
    subtitles "You decide to leave her alone."
    
    call change_stats_with_modifier('math',
        charm = DEC_TINY, happiness = DEC_TINY) from _call_change_stats_with_modifier_59
    $ end_event('new_daytime', **kwargs)
label .help (**kwargs):
    $ begin_event(**kwargs)
    
    $ image.show(3)
    subtitles "You help her up."
    
    call change_stats_with_modifier('math',
        charm = DEC_TINY, happiness = TINY) from _call_change_stats_with_modifier_60
    $ end_event('new_daytime', **kwargs)

# endregion
################

###############
# region MAIN #

label sb_teach_math_main_1 (**kwargs):
    $ begin_event("2", **kwargs)

    $ main_girl_name = get_value('main_girl_name', **kwargs)
    $ main_topic = get_value('main_topic', **kwargs)

    $ girl_person = get_person("class_3a", main_girl_name)

    $ girl_last_name = girl_person.get_last_name()

    $ girl = girl_person.get_character()

    call screen black_screen_text("30 minutes later.")

    $ image = convert_pattern("main", **kwargs)

    if main_topic == "sleeping":
        call Image_Series.show_image(image, 0, 1, 2, pause = True) from _call_sb_teach_math_main_1_1
        
        # headmaster walks over
        $ image.show(3)
        headmaster_shout "Good Morning Ms. [girl_last_name]! I hope you had a good nap!"
        
        $ image.show(4)
        girl "Eek! I'm sorry, I didn't mean to fall asleep."

        $ image.show(5)
        headmaster "It's okay, but please try to stay awake. It's important to understand the topic."

        $ image.show(6)
        headmaster "As a punishment, you have to answer the next question."

        call Image_Series.show_image(image, 7, 8, pause = False) from _call_sb_teach_math_main_1_2
        headmaster "So. What is the solution of 2x² - 5x + 3 = 0?"
        
        $ image.show(9)
        headmaster "No idea?"
        
        $ image.show(10)
        headmaster "Anyone else?"
    else:
        $ image.show(7)
        headmaster "So let's solve the equation 2x² - 5x + 3 = 0."

        $ image.show(8)
        headmaster "Does anyone know how to solve this?"

        $ image.show(10)
        headmaster "Nobody?"

    # no one knows
    $ image.show(11)
    headmaster "Okay, then let's solve it together."
    headmaster "To solve this equation, we can use the quadratic formula."
    headmaster "The quadratic formula is x = (-b ± √(b² - 4ac)) / (2a)."

    $ image.show(12)
    headmaster "Can someone tell me what a, b and c are?"
    headmaster "Nobody?"

    $ image.show(13)
    headmaster "Just imagine the equation as ax² + bx + c = 0."

    $ image.show(14)
    headmaster "So what is a, b and c?"

    $ image.show(15)
    girl "2, -5 and 3?"

    $ image.show(16)
    headmaster "Correct. So now we insert these values into the quadratic formula."
    headmaster "Now we get x = (-(-5) ± √((-5)² - 4*2*3)) / (2*2)."

    $ image.show(17)
    headmaster "We simplify this."
    headmaster "So we get x = (5 ± √(25 - 24)) / 4."

    $ image.show(18)
    headmaster "And after that we get x = (5 ± √1) / 4."

    $ image.show(19)
    headmaster "The √1 is 1, so we get x = (5 + 1) / 4 and x = (5 - 1) / 4."

    $ image.show(20)
    headmaster "So we get x = 6 / 4 and x = 4 / 4."

    $ image.show(21)
    headmaster "And the solution is x = 1.5 and x = 1."

    $ image.show(22)
    headmaster "You see it's not that hard. There is a lot written down here but it all boils down to two things."

    $ image.show(23)
    headmaster "First you have to remember the quadratic formula x = (-b ± √(b² - 4ac)) / (2a) also called the abc-formula."
    headmaster "And secondly you have to remember where a, b and c come from. From the equation ax² + bx + c = 0."

    $ image.show(24)
    headmaster "So if you remember these two things, you can solve every quadratic equation."

    $ image.show(25)
    headmaster "Now lets solve some more equations. Please open Page 44."

    call screen black_screen_text("30 minutes later.")

    $ image.show(26)
    headmaster "That is all for today"

    call change_stats_with_modifier('math',
        education = SMALL, reputation = TINY, happiness = TINY) from _call_change_stats_with_modifier_61
    
    $ end_event('new_daytime', **kwargs)

label sb_teach_math_main_2 (**kwargs):
    $ begin_event(**kwargs)

    $ seraphina = get_person("class_3a", "seraphina_clark").get_character()

    $ image = convert_pattern("main", **kwargs)

    $ image.show(0)
    headmaster "Today I want you to train your equation solving skills."

    $ image.show(1)
    headmaster "For that please open your books on page 42 and solve the equations 1 to 12."

    $ image.show(2)
    headmaster "I'll go through the rows to make sure everyone understands the topic."
    headmaster "If you have a question or don't understand something, please don't hesitate to ask."
    
    call Image_Series.show_image(image, 3, 4, 5, 6, 7) from _call_sb_teach_math_main_2_1
    headmaster "Do you need some help?"
    seraphina "Yes, I don't understand this equation." (name = "Seraphina Clark")

    $ image.show(8)
    headmaster "What is the problem?"

    $ image.show(9)
    seraphina "Well, I don't understand..."

    $ image.show(10)
    seraphina "And then..."

    $ image.show(11)
    headmaster "{i}(  Wow what a nice view down her shirt.  ){/i}" (name = '[headmaster_first_name] [headmaster_last_name] (thinking)')

    $ image.show(12)
    seraphina "Mr. [headmaster_last_name]?"

    $ image.show(13)
    headmaster "Yeah! I'm sorry. I'll help you."
    headmaster "Now, do you remember the abc-formula?"

    call screen black_screen_text('5 minutes later.')

    $ image.show(14)
    seraphina "Thank you Mr. [headmaster_last_name]."

    $ image.show(15)
    headmaster "You're welcome."

    call Image_Series.show_image(image, 16, pause = True) from _call_sb_teach_math_main_2_2

    call screen black_screen_text("1 hour later.")

    $ image.show(17)
    headmaster "That is all for today. Thanks for your attention. See you next time."

    call change_stats_with_modifier('math',
        education = SMALL, happiness = TINY, inhibition = DEC_TINY) from _call_change_stats_with_modifier_62
    
    $ end_event('new_daytime', **kwargs)

# endregion
###############

# endregion
###############

###############
# region P.E. #

label gym_teach_pe (**kwargs):
    $ begin_event("2", **kwargs)

    $ get_level('school_level', **kwargs)

    call composite_event_runner(**kwargs) from _call_composite_event_runner

################
# region INTRO #

label gym_teach_pe_intro_1 (**kwargs):
    $ begin_event("2", **kwargs)

    $ image = convert_pattern("main", **kwargs)

    call Image_Series.show_image(image, 0, 1, 2, 3, 4, 5, 6, 7, pause = True) from image_gym_teach_pe_intro_1_1

    $ end_event('map_entry', **kwargs)

label gym_teach_pe_intro_2 (**kwargs):
    $ begin_event(**kwargs)

    $ image = convert_pattern("main", **kwargs)

    call Image_Series.show_image(image, 0, 1, 2, 3, 4, 5, pause = True) from image_gym_teach_pe_intro_2_1

    $ end_event('map_entry', **kwargs)

# endregion
################

###################
# region ENTRANCE #

label gym_teach_pe_entrance_1 (**kwargs):
    $ begin_event("2", **kwargs)

    $ image = convert_pattern("main", **kwargs)

    call Image_Series.show_image(image, 0, 1, 2, 3, 4, pause = True) from image_gym_teach_pe_entrance_1_1
    headmaster "Alright, let's get started with the P.E. class."

    headmaster "First we start with a few warm up exercises and stretching."
    headmaster "Okay now all follow my lead."


    $ end_event('map_entry', **kwargs)


# endregion
###################

##################
# region WARM UP #

define anim_gtpewu1_path = "/images/events/teaching/pe/warm_up/warm_up_1/teaching_pe_warm_up_1 "
image anim_teaching_pe_warm_up_1_1_0 = Movie(play = anim_gtpewu1_path + "1 0.webm", start_image = anim_gtpewu1_path + "1 0.webp", loop = True)
image anim_teaching_pe_warm_up_1_1_1 = Movie(play = anim_gtpewu1_path + "1 1.webm", start_image = anim_gtpewu1_path + "1 1.webp", loop = True)
image anim_teaching_pe_warm_up_1_1_2 = Movie(play = anim_gtpewu1_path + "1 2.webm", start_image = anim_gtpewu1_path + "1 2.webp", loop = True)
image anim_teaching_pe_warm_up_1_2_0 = Movie(play = anim_gtpewu1_path + "2 0.webm", start_image = anim_gtpewu1_path + "2 0.webp", loop = True)
image anim_teaching_pe_warm_up_1_2_1 = Movie(play = anim_gtpewu1_path + "2 1.webm", start_image = anim_gtpewu1_path + "2 1.webp", loop = True)
image anim_teaching_pe_warm_up_1_2_2 = Movie(play = anim_gtpewu1_path + "2 2.webm", start_image = anim_gtpewu1_path + "2 2.webp", loop = True)
image anim_teaching_pe_warm_up_1_3_0 = Movie(play = anim_gtpewu1_path + "3 0.webm", start_image = anim_gtpewu1_path + "3 0.webp", loop = True)
image anim_teaching_pe_warm_up_1_3_1 = Movie(play = anim_gtpewu1_path + "3 1.webm", start_image = anim_gtpewu1_path + "3 1.webp", loop = True)
image anim_teaching_pe_warm_up_1_3_2 = Movie(play = anim_gtpewu1_path + "3 2.webm", start_image = anim_gtpewu1_path + "3 2.webp", loop = True)
image anim_teaching_pe_warm_up_1_4_0 = Movie(play = anim_gtpewu1_path + "4 0.webm", start_image = anim_gtpewu1_path + "4 0.webp", loop = True)
image anim_teaching_pe_warm_up_1_4_1 = Movie(play = anim_gtpewu1_path + "4 1.webm", start_image = anim_gtpewu1_path + "4 1.webp", loop = True)
image anim_teaching_pe_warm_up_1_4_2 = Movie(play = anim_gtpewu1_path + "4 2.webm", start_image = anim_gtpewu1_path + "4 2.webp", loop = True)
image anim_teaching_pe_warm_up_1_5_0 = Movie(play = anim_gtpewu1_path + "5 0.webm", start_image = anim_gtpewu1_path + "5 0.webp", loop = True)
image anim_teaching_pe_warm_up_1_5_1 = Movie(play = anim_gtpewu1_path + "5 1.webm", start_image = anim_gtpewu1_path + "5 1.webp", loop = True)
image anim_teaching_pe_warm_up_1_5_2 = Movie(play = anim_gtpewu1_path + "5 2.webm", start_image = anim_gtpewu1_path + "5 2.webp", loop = True)
image anim_teaching_pe_warm_up_1_6_0 = Movie(play = anim_gtpewu1_path + "6 0.webm", start_image = anim_gtpewu1_path + "6 0.webp", loop = True)
image anim_teaching_pe_warm_up_1_6_1 = Movie(play = anim_gtpewu1_path + "6 1.webm", start_image = anim_gtpewu1_path + "6 1.webp", loop = True)
image anim_teaching_pe_warm_up_1_6_2 = Movie(play = anim_gtpewu1_path + "6 2.webm", start_image = anim_gtpewu1_path + "6 2.webp", loop = True)
image anim_teaching_pe_warm_up_1_7_0 = Movie(play = anim_gtpewu1_path + "7 0.webm", start_image = anim_gtpewu1_path + "7 0.webp", loop = True)
image anim_teaching_pe_warm_up_1_7_1 = Movie(play = anim_gtpewu1_path + "7 1.webm", start_image = anim_gtpewu1_path + "7 1.webp", loop = True)
image anim_teaching_pe_warm_up_1_7_2 = Movie(play = anim_gtpewu1_path + "7 2.webm", start_image = anim_gtpewu1_path + "7 2.webp", loop = True)
image anim_teaching_pe_warm_up_1_8_0 = Movie(play = anim_gtpewu1_path + "8 0.webm", start_image = anim_gtpewu1_path + "8 0.webp", loop = True)
image anim_teaching_pe_warm_up_1_8_1 = Movie(play = anim_gtpewu1_path + "8 1.webm", start_image = anim_gtpewu1_path + "8 1.webp", loop = True)
image anim_teaching_pe_warm_up_1_8_2 = Movie(play = anim_gtpewu1_path + "8 2.webm", start_image = anim_gtpewu1_path + "8 2.webp", loop = True)
image anim_teaching_pe_warm_up_1_9_0 = Movie(play = anim_gtpewu1_path + "9 0.webm", start_image = anim_gtpewu1_path + "9 0.webp", loop = True)
image anim_teaching_pe_warm_up_1_9_1 = Movie(play = anim_gtpewu1_path + "9 1.webm", start_image = anim_gtpewu1_path + "9 1.webp", loop = True)
image anim_teaching_pe_warm_up_1_9_2 = Movie(play = anim_gtpewu1_path + "9 2.webm", start_image = anim_gtpewu1_path + "9 2.webp", loop = True)
image anim_teaching_pe_warm_up_1_10_0 = Movie(play = anim_gtpewu1_path + "10 0.webm", start_image = anim_gtpewu1_path + "10 0.webp", loop = True)
image anim_teaching_pe_warm_up_1_10_1 = Movie(play = anim_gtpewu1_path + "10 1.webm", start_image = anim_gtpewu1_path + "10 1.webp", loop = True)
image anim_teaching_pe_warm_up_1_10_2 = Movie(play = anim_gtpewu1_path + "10 2.webm", start_image = anim_gtpewu1_path + "10 2.webp", loop = True)
label gym_teach_pe_warm_up_1 (**kwargs):
    $ begin_event("2", **kwargs)

    $ image = convert_pattern("main", **kwargs)

    $ image.show_video(0, True)
    $ image.show_video(1, True)
    $ image.show_video(2, True)
    
    headmaster "Alright, that's enough."
    
    call change_stats_with_modifier('pe',
        charm = SMALL, education = TINY) from _call_change_stats_with_modifier_20

    $ end_event('map_entry', **kwargs)

# endregion
##################

###############
# region MAIN #

label gym_teach_pe_main_1 (**kwargs): # Football
    $ begin_event("2", **kwargs)

    $ sakura = get_person("class_3a", "sakura_mori").get_character()

    $ image = convert_pattern("main", **kwargs)
    
    $ image.show(0)
    headmaster "Alright, that's enough. Now let's play some football. I will be the referee."
    $ image.show(1)
    headmaster "Please split into two teams and let's get started."
    $ image.show(2)
    sakura "I'm sorry but how do we identify the teams? We all wear the same uniform."
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
    
    call change_stats_with_modifier('pe',
        happiness = TINY, charm = SMALL, reputation = TINY, inhibition = DEC_TINY) from _call_change_stats_with_modifier_21

    $ end_event('map_entry', **kwargs)

label gym_teach_pe_main_2 (**kwargs): # Yoga
    $ begin_event("2", **kwargs)

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

    call change_stats_with_modifier('pe',
        happiness = TINY, charm = MEDIUM, inhibition = DEC_TINY) from _call_change_stats_with_modifier_22

    $ end_event('map_entry', **kwargs)

# endregion
###############

##############
# region END #

label gym_teach_pe_end_1 (**kwargs):
    $ begin_event("2", **kwargs)

    $ end_event('new_daytime', **kwargs)

# endregion
##############

# endregion
###############

# endregion
###############################
