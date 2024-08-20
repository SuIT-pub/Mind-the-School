#############################################
# ----- School Building Event Handler ----- #
#############################################

init -1 python:
    def sb_events_available() -> bool:
        return (sb_timed_event.has_available_highlight_events() or
            sb_general_event.has_available_highlight_events() or
            any(e.has_available_highlight_events() for e in sb_events.values()) or
            any(e.has_available_highlight_events() for e in sb_teach_events.values()))

    sb_timed_event   = TempEventStorage("school_building", "school_building", fallback = Event(2, "school_building.after_time_check"))
    sb_general_event =     EventStorage("school_building", "school_building", fallback = Event(2, "school_building.after_general_check"))

    sb_events = {}
    add_storage(sb_events, EventStorage("teach_class",  "school_building", fallback_text = "There is nobody here."))
    add_storage(sb_events, EventStorage("patrol",       "school_building", fallback_text = "There is nobody here."))

    sb_teach_events = {}
    add_storage(sb_teach_events, EventStorage("math",    "school_building", fallback_text = "There is nobody here."))
    add_storage(sb_teach_events, EventStorage("history", "school_building", fallback_text = "There is nobody here."))

    sb_bg_images = BGStorage("images/background/school building/bg f.webp", ValueSelector('loli', 0),
        BGImage("images/background/school building/bg <loli> <school_level> <variant> <nude>.webp", 1, TimeCondition(daytime = "c", weekday = "d")),
        BGImage("images/background/school building/bg 7.webp", 1, TimeCondition(daytime = 7)),
    )

init 1 python:

    ####################
    # Default Events
    first_week_sb_event = Event(1, "first_week_sb_event",
        IntroCondition(),
        TimeCondition(day = "2-4", month = 1, year = 2023),
        thumbnail = "images/events/first week/first week school building 2.webp")

    first_potion_sb_event = Event(1, "first_potion_sb_event",
        IntroCondition(),
        TimeCondition(day = 9, month = 1, year = 2023),
        thumbnail = "images/events/first potion/first potion school building 1.webp")

    first_class_sb_event_event = Event(1, "first_class_sb_event",
        TimeCondition(weekday = "d", daytime = "c"),
        ProgressCondition('first_class', '2-'),
        RandomListSelector('class', 
            ('3A', NOT(GameDataCondition('first_class_3A', True))),
            (
                '2A', 
                AND(
                    NOT(GameDataCondition('first_class_2A', True)),
                    LoliContentCondition('1+')
                ),
            ),
            (
                '1A', 
                AND(
                    NOT(GameDataCondition('first_class_1A', True)),
                    LoliContentCondition('2')
                ),
            ), 
            realtime = True,
            alt = '3A'
        ),
        thumbnail = "images/events/school building/first_class_sb_event 3A 0 2.webp")

    sb_event1 = Event(3, "sb_event_1",
        TimeCondition(daytime = "c", weekday = "d"),
        LevelSelector('school_level', 'school'),
        thumbnail = "images/events/school building/sb_event_1 1 1.webp")

    sb_event2 = Event(3, "sb_event_2",
        TimeCondition(daytime = "c", weekday = "d"),
        LevelSelector('school_level', 'school'),
        RandomCondition(50),
        thumbnail = "images/events/school building/sb_event_2 1 0.webp")
    
    sb_event3 = Event(3, "sb_event_3",
        TimeCondition(daytime = "d", weekday = "d"),
        LevelSelector('school_level', 'school'),
        thumbnail = "images/events/school building/sb_event_3 1 1.webp")

    sb_event4 = Event(3, "sb_event_4",
        TimeCondition(daytime = "f", weekday = "d"),
        LevelSelector('school_level', 'school'),
        RandomListSelector('girl_name', 'Ikushi Ito'),
        thumbnail = "images/events/school building/sb_event_4 1 Ikushi Ito 0.webp")

    sb_event5 = Event(3, "sb_event_5",
        TimeCondition(daytime = "c", weekday = "d"),
        RandomListSelector('girls', 'Ikushi Ito', 'Soyoon Yamamoto', 'Yuriko Oshima'),
        thumbnail = "images/events/school building/sb_event_5 1 Soyoon Yamamoto 11.webp")
    ####################

    sb_action_tutorial_event = Event(2, "action_tutorial",
        NOT(ProgressCondition('action_tutorial')),
        ValueSelector('return_label', 'school_building'))



    ####################

    # sb_event_teach_class_event = Event(3, "teach_class_event",
    #     TimeCondition(weekday = "d", daytime = "c"),)

    # Teaching events
    sb_event_teach_class_event = EventSelect(3, "teach_class_event", "What subject do you wanna teach?", sb_teach_events,
        TimeCondition(weekday = "d", daytime = "c"),
        KwargsSelector(show_proficiency_modifier = True),
        override_menu_exit = 'school_building',
    )

    #################
    # Math Teaching
    sb_teach_math_ld_storage = FragmentStorage('sb_teach_math_ld')
    sb_teach_math_ld_storage.add_event(
        EventFragment(3, 'sb_teach_math_ld_1', 
            ValueCondition('learning_difficulty', False),
            thumbnail = "images/events/school building/sb_teach_math_ld_1 1.webp"),
        EventFragment(3, 'sb_teach_math_ld_2', 
            RandomListSelector('ld_girl_name', 'Seraphina Clark', 'Hatano Miwa', 'Soyoon Yamamoto'),
            ValueCondition('learning_difficulty', True),
            thumbnail = "images/events/school building/sb_teach_math_ld_2 1 Seraphina Clark 1.webp"),
        EventFragment(3, 'sb_teach_math_ld_3',
            thumbnail = "images/events/school building/sb_teach_math_ld_3 0.webp")
    )

    sb_teach_math_main_storage = FragmentStorage('sb_teach_math_main')
    sb_teach_math_main_storage.add_event(
        EventFragment(3, 'sb_teach_math_main_1',
            RandomListSelector('main_girl_name', 'Seraphina Clark', 'Hatano Miwa', 'Soyoon Yamamoto'),
            RandomListSelector('main_topic', 'normal', 'sleeping'),
            thumbnail = "images/events/school building/sb_teach_math_main_1 Seraphina Clark 1 0.webp"),
        EventFragment(3, 'sb_teach_math_main_2',
            thumbnail = "images/events/school building/sb_teach_math_main_2 1 7.webp",)
    )

    sb_teach_math_event = EventComposite(3, 'sb_teach_math', [sb_teach_math_ld_storage, sb_teach_math_main_storage],
        LevelSelector('school_level', 'school'),
        ProficiencyCondition('math'),
        thumbnail = "images/events/school building/sb_teach_math_main_1 # 1 18.webp"
    )
    #################

    sb_teach_history_intro_storage = FragmentStorage('sb_teach_history_intro')
    sb_teach_history_intro_storage.add_event(
        EventFragment(3, 'sb_teach_history_intro_f_revolution_1',
            CheckReplay(ValueCondition('topic', 'french revolution')))
    )

    sb_teach_history_main_storage = FragmentStorage('sb_teach_history_main')
    sb_teach_history_main_storage.add_event(
        EventFragment(3, 'sb_teach_history_main_f_revolution_1',
            CheckReplay(ValueCondition('topic', 'french revolution'))),
        EventFragment(3, 'sb_teach_history_main_f_revolution_2',
            CheckReplay(ValueCondition('topic', 'french revolution')))
    )

    sb_teach_history_event = EventComposite(3, 'sb_teach_history', [sb_teach_history_intro_storage, sb_teach_history_main_storage],
        LevelSelector('school_level', 'school'),
        RandomListSelector('topic', 'french revolution'),
        ProficiencyCondition('history'),
    )

    #################
    # Event insertion
    # sb_timed_event.add_event(
    # )

        # sb_action_tutorial_event,
    sb_general_event.add_event(
        first_week_sb_event, 
        first_potion_sb_event,
    )

    sb_events["teach_class"].add_event(
        first_class_sb_event_event, 
        sb_event_teach_class_event,
    )

    sb_events["patrol"].add_event(
        sb_event1, 
        sb_event3,
        sb_event4,
        sb_event5,
    )

    sb_teach_events["math"].add_event(
        sb_teach_math_event
    )

    sb_teach_events["history"].add_event(
        sb_teach_history_event
    )

    #################

##################################################

###########################################
# ----- School Building Entry Point ----- #
###########################################

label school_building ():
    call call_available_event(sb_timed_event) from school_building_1
    
label .after_time_check (**kwargs):
    call call_available_event(sb_general_event) from school_building_4

label .after_general_check (**kwargs):
    call call_event_menu (
        "What to do in the School?", 
        sb_events,
        default_fallback,
        character.subtitles,
        bg_image = sb_bg_images,
        context = loli,
    ) from school_building_3

    jump school_building

################################################

######################################
# ----- School Building Events ----- #
######################################

#####################
# Introduction Events

# first week event
label first_week_sb_event (**kwargs):
    $ begin_event(**kwargs)

    scene first week school building 1 with dissolveM
    subtitles """You enter the main building of the high school.
        
        Well, you don't really need to enter the building to get an idea of the state it's in."""
        
    scene first week school building 2 with dissolveM
    headmaster_thought """Despite my fear, the building seems to be rather well maintained.

        It could be a bit cleaner but the corridor seems rather well.

        Let's see the classrooms."""
    
    scene first week school building 3 with dissolveM
    headmaster_thought "Oh not bad as well. "

    scene first week school building 4 with dissolveM
    headmaster_thought "Hmm I think there should be a class right now, let's check."

    scene first week school building 6 with dissolveM
    headmaster_thought "Hmm looks like a normal class, but I think the students have no material?"
    headmaster_thought "Yeah, not one school girl has even one book."
    headmaster_thought "I guess the former headmaster cut back on those"

    $ change_stat("education", 5, get_school())

    $ set_building_blocked("school_building")

    $ end_event('new_day', **kwargs)

label first_potion_sb_event (**kwargs):

    $ begin_event(**kwargs)
    
    scene first potion school building 1 with dissolveM
    headmaster_thought "Let's see how classes are today."
    
    scene first potion school building 2 with dissolveM
    subtitles "You look into a classroom and the first thing you notice is that almost everyone has opened up or at least partially removed their clothes."
    subtitles "Apparently the teachers also took a drink."
    headmaster_thought "Hmm, I can't wait to have this view on a regular basis, but that's gonna take some time."

    $ set_building_blocked("school_building")
    
    $ end_event('new_daytime', **kwargs)

label first_class_sb_event (**kwargs):
    $ begin_event(**kwargs)

    $ school_class = get_value('class', **kwargs)

    $ image = Image_Series("/images/events/school building/first_class_sb_event <class> <nude> <step>.webp", **kwargs)

    $ image.show(0)
    headmaster "Hello, let me introduce myself again. I'm [headmaster_first_name] [headmaster_last_name], the new headmaster of this school."
    $ image.show(1)
    headmaster "I'm actually a psychologist but I got myself a teaching license to help students like you to receive a better education."
    headmaster "Don't worry, you will still be taught by your regular teachers. I work mainly on school reform and will only occasionally teach a class."
    $ image.show(2)
    headmaster "If you have any questions or issues, feel free to come to me. I always put heavy emphasis on the well-being of my students."
    $ image.show(3)
    headmaster "Now I'd like to get to know you a bit better. Would you please all introduce yourself?"

    if school_class == "3A":
        $ image.show(4)
        headmaster "Miss Ryan, would you like to start?"
        $ image.show(5)
        teacher3 "Yes, of course."
        teacher3 "My name is Finola Ryan. I'm 28 years old and I'm a teacher for English and Geography. I am also the class teacher of 3A."

        $ image.show(6)
        headmaster "Great! Now please the rest of the class."

        # students introduce themselves
        $ image.show(7)
        sgirl "Hello, I am Gloria Goto. I'm 19 years old." (name="Gloria Goto")
        $ image.show(8)
        sgirl "Hi I am Luna Clark. I'm 18 years old." (name="Luna Clark")
        $ image.show(9)
        sgirl "Hi I am Seraphina Clark. I'm also 18 years old." (name="Seraphina Clark")
        $ image.show(10)
        sgirl "H-Hi, I'm Easkey Tanaka. I'm 19 years old." (name="Easkey Tanaka")
        $ image.show(11)
        sgirl "I'm Kokoro Nakamura. I'm 20 years old." (name="Kokoro Nakamura")
        $ image.show(12)
        sgirl "Lin Kato. 20 years old." (name="Lin Kato")
        $ image.show(13)
        sgirl "Hello, I'm Miwa Igarashi. I'm 19 years old." (name="Miwa Igarashi")
        $ image.show(14)
        sgirl "Hi, I'm Aona Komuro. I'm 18 years old." (name="Aona Komuro")
        $ image.show(15)
        sgirl "Hi. Yuriko Oshima. I'm 22 years old." (name="Yuriko Oshima")
        $ image.show(16)
        sgirl "Hello, my name is Ishimaru Maki. I'm 19 years old." (name="Ishimaru Maki")
        $ image.show(17)
        sgirl "I'm Ikushi Ito. 20 years old." (name="Ikushi Ito")
        $ image.show(18)
        sgirl "Sakura Mori. 21." (name="Sakura Mori")
        $ image.show(19)
        sgirl "Hi, my name is Elsie Johnson. I'm 21 years old." (name="Elsie Johnson")
        $ image.show(20)
        sgirl "Hi. I'm Hatano Miwa. 19 years." (name="Hatano Miwa")
        $ image.show(21)
        sgirl "Hello. Soyoon Yamamoto. 18 years." (name="Soyoon Yamamoto")

        $ image.show(22)
        headmaster "Thank you all for introducing yourself. I'm looking forward to working with you."
        headmaster "Now I'll return you back to Miss Ryan. Have a good day."

        $ set_game_data('first_class_3A', True)
        $ advance_progress('first_class')
        if loli_content == 0:
            $ set_progress('first_class', 3)

    elif school_class == "2A":
        $ age = 1 * -5
        $ image.show(4)
        headmaster "Miss Anderson, would you like to start?"
        $ image.show(5)
        teacher1 "Yes, of course."
        teacher1 "My name is Lily Anderson. I'm 32 years old and I'm a teacher for Math and Sciences. I am also the class teacher of 2A."
        
        $ image.show(6)
        headmaster "Great! Now please the rest of the class."

        $ image.show(7)
        $ character.sgirl(f"Hello. My name is Miela Frejadottir. I am {21 + age} years old.", name="Miela Frejadottir")
        $ image.show(8)
        $ character.sgirl(f"Hi. I'm Marie Rose. I am {18 + age} years old.", name="Marie Rose")
        $ image.show(9)
        $ character.sgirl(f"Hello. I am Amelie Mori. {19 + age}.", name="Amelie Mori")
        $ image.show(10)
        $ character.sgirl(f"Hi. Thanchanok Cooper. I'm {22 + age} years old.", name="Thanchanok Cooper")
        $ image.show(11)
        $ character.sgirl(f"Hello. Sofia Harada. {18 + age} years.", name="Sofia Harada")
        $ image.show(12)
        $ character.sgirl(f"H-Hi, I'm Saito Shiori. I'm {19 + age} years old.", name="Saito Shiori")
        $ image.show(13)
        $ character.sgirl(f"Hello, my name is Nina Abe. I'm {19 + age} years old.", name="Nina Abe")
        $ image.show(14)
        $ character.sgirl(f"Hi, I'm Yukari Hashiguchi. I'm {18 + age} years old.", name="Yukari Hashiguchi")
        $ image.show(15)
        $ character.sgirl(f"I'm Yuka Tanimoto. {20 + age} years old.", name="Yuka Tanimoto")
        $ image.show(16)
        $ character.sgirl(f"Yamaoka Yuki. {21 + age}.", name="Yamaoka Yuka")
        $ image.show(17)
        $ character.sgirl(f"Hi. I'm Ivy Schmidt. {19 + age} years.", name="Ivy Schmidt")
        $ image.show(18)
        $ character.sgirl(f"Hi, my name is Hiroshi Suzuki. I'm {18 + age} years old.", name="Hiroshi Suzuki")

        $ image.show(19)
        headmaster "Thank you all for introducing yourself. I'm looking forward to working with you."
        headmaster "Now I'll return you back to Miss Anderson. Have a good day."

        # students introduce themselves
        $ set_game_data('first_class_2A', True)
        $ advance_progress('first_class')
        if loli_content <= 1:
            $ set_progress('first_class', 3)

    elif school_class == "1A":
        $ age = 2 * -5
        $ image.show(4)
        headmaster "Miss Parker, would you like to start?"

        $ image.show(5)
        teacher5 "Yes, of course."
        teacher5 "My name is Zoe Parker. I'm 24 years old and I'm a teacher for Sport and Art. I am also the class teacher of 1A."
        
        $ image.show(6)
        headmaster "Great! Now please the rest of the class."

        $ image.show(7)
        $ character.sgirl(f"Hello. My name is Sidney Martinez. I am {18 + age} years old.", name="Sidney Martinez")

        $ image.show(8)
        $ character.sgirl(f"Eunji Han. {21 + age}.", name="Eunji Han")

        $ image.show(9)
        $ character.sgirl(f"Hi. I'm Karini Ono. I am {21 + age} years old.", name="Karini Ono")

        $ image.show(10)
        $ character.sgirl(f"Hello, my name is Fio Dubois. I'm {19 + age} years old.", name="Fio Dubois")

        $ image.show(11)
        $ character.sgirl(f"Hi. Patricia Müller. I'm {22 + age} years old.", name="Patricia Müller")

        $ image.show(12)
        $ character.sgirl(f"I'm Leonidou Papadopoulos. {20 + age} years old.", name="Leonidou Papadopoulos")

        $ image.show(13)
        $ character.sgirl(f"H-Hi, I'm Elina Jansen. I'm {19 + age} years old.", name="Elina Jansen")

        $ image.show(14)
        $ character.sgirl(f"Hi, I'm Aiden O'Reilly. I'm {18 + age} years old.", name="Aiden O'Reilly")

        $ image.show(15)
        $ character.sgirl(f"Hello. Lorelyn Hosant. {18 + age} years.", name="Lorelyn Hosant")

        $ image.show(16)
        $ character.sgirl(f"Hello. I am Alice Fernandez. {19 + age}.", name="Alice Fernandez")

        $ image.show(17)
        headmaster "Thank you all for introducing yourself. I'm looking forward to working with you."
        headmaster "Now I'll return you back to Miss Parker. Have a good day."
        
        # students introduce themselves
        $ set_game_data('first_class_1A', True)
        $ advance_progress('first_class')

    call change_stats_with_modifier('school',
        happiness = TINY, charm = SMALL, education = TINY)

    call change_stats_with_modifier('teacher',
        happiness = TINY, charm = SMALL, education = TINY)

    $ end_event('new_daytime', **kwargs)

##########
## HISTORY

label sb_teach_history (**kwargs):
    $ begin_event(**kwargs)

    $ get_value('school_level', **kwargs)
    $ get_value('topic', **kwargs)

    # headmaster enters room
    call show_image ("/images/events/school building/sb_teach_history.webp", **kwargs) from _call_show_image_sb_teach_history_event_1
    headmaster "Good morning everyone. Let's start with todays subject History."

    call composite_event_runner(**kwargs)

label sb_teach_history_intro_f_revolution_1 (**kwargs):
    $ begin_event(**kwargs)

    $ image = Image_Series("/images/events/school building/sb_teach_history_intro_f_revolution_1 <step>.webp", **kwargs)

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

    call change_stats_with_modifier('school', 'history',
        education = TINY)

    $ end_event('map_overview', **kwargs)

label sb_teach_history_main_f_revolution_1 (**kwargs):
    $ begin_event(**kwargs)

    $ sakura = Character ("Sakura Mori", kind=character.sgirl)
    $ luna = Character ("Luna Clark", kind=character.sgirl)
    $ easkey = Character ("Easkey Tanaka", kind=character.sgirl)

    $ image = Image_Series("/images/events/school building/sb_teach_history_main_f_revolution_1 <school_level> <step>.webp", ['school_level'], **kwargs)

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

    call change_stats_with_modifier('school', 'history',
        education = SMALL)

    $ end_event('new_daytime', **kwargs)

label sb_teach_history_main_f_revolution_2 (**kwargs):
    $ begin_event(**kwargs)

    $ image = Image_Series("/images/events/school building/sb_teach_history_main_f_revolution_2 <school_level> <step>.webp", ['school_level'], **kwargs)

    $ image.show(0)
    headmaster "Today we will talk about the early stages of the French Revolution."
    $ image.show(1)
    headmaster "More accurately, I want you to inform yourself and write a short essay until next time."
    $ image.show(2)
    headmaster "I want you to focus on three events. The national assembly, the tennis court oath and the storming of the bastille."
    $ image.show(3)
    headmaster "You get until the end of the lesson to work on it."
    $ image.show(4)
    headmaster "If you're not finished by then, please finish it by the end of the week. I'll get Mrs. Ryan to collect them."
    $ image.show(5)
    headmaster "Now please start."
    call screen black_screen_text("40 minutes later.")
    $ image.show(6)
    headmaster "Okay, class is over. Please don't forget to finish your essay until the end of the week."

    call change_stats_with_modifier('school', 'history',
        education = TINY, happiness = DEC_TINY)

    $ end_event('new_daytime', **kwargs)

##########

#######
## MATH

label sb_teach_math (**kwargs):
    $ begin_event(**kwargs)

    $ get_value('school_level', **kwargs)

    # headmaster enters room
    call show_image ("/images/events/school building/sb_teach_math.webp", **kwargs) from _call_show_image_sb_teach_math_event_1
    headmaster "Good morning everyone. Let's start with todays subject Math."

    call composite_event_runner(**kwargs)

label sb_teach_math_ld_1 (**kwargs):
    $ begin_event(**kwargs)

    $ image = Image_Series("/images/events/school building/sb_teach_math_ld_1 <step>.webp", **kwargs)

    $ image.show(0)
    headmaster "Is there anything you want to reiterate from the last time?"

    $ image.show(1)
    headmaster "Okay, then let's continue with the new topic."

    $ end_event('map_overview', **kwargs)

label sb_teach_math_ld_2 (**kwargs):
    $ begin_event(**kwargs)

    $ ld_girl_name = get_value('ld_girl_name', **kwargs)

    $ image = Image_Series("/images/events/school building/sb_teach_math_ld_2 <ld_girl_name> <school_level> <step>.webp", ['ld_girl_name'], **kwargs)

    $ image.show(0)
    headmaster "Is there anything you want to reiterate from the last time?"
    
    $ image.show(1)
    sgirl "Yes, I'm sorry. I didn't understand the last topic." (name = ld_girl_name)

    $ image.show(2)
    headmaster "No problem. I'll explain it again."

    $ image.show(3)
    headmaster "Imagine..."

    $ image.show(4)
    headmaster "Imagine..."

    call screen black_screen_text("15 minutes later.")

    $ image.show(5)
    headmaster "That is all."
    headmaster "Do you understand it better now?"

    $ image.show(6)
    sgirl "Yes, thank you." (name = ld_girl_name)

    $ image.show(7)
    headmaster "Good. Now let's continue with the new topic."

    call change_stats_with_modifier('school', 'math'
        education = TINY)

    $ end_event('map_overview', **kwargs)

label sb_teach_math_ld_3 (**kwargs):
    $ begin_event(**kwargs)
    
    $ image = Image_Series("/images/events/school building/sb_teach_math_ld_3 <school_level> <step>.webp", **kwargs)

    $ image.show(0)
    subtitles "A student tripped while handing out assignments in class."

    $ image.show(1)
    $ call_custom_menu_with_text("What do you do?", character.subtitles, False,
        ("Leave alone", "sb_teach_math_ld_3.leave"),
        ("Help her up", "sb_teach_math_ld_3.help"), 
    **kwargs)
label .leave (**kwargs):
    $ begin_event()
    
    $ image.show(2)
    subtitles "You decide to leave her alone."
    
    call change_stats_with_modifier('school', 'math',
        charm = DEC_TINY, happiness = DEC_TINY)
    $ end_event('new_daytime', **kwargs)
label .help (**kwargs):
    $ begin_event()
    
    $ image.show(3)
    subtitles "You help her up."
    
    call change_stats_with_modifier('school', 'math',
        charm = DEC_TINY, happiness = TINY)
    $ end_event('new_daytime', **kwargs)

label sb_teach_math_main_1 (**kwargs):
    $ begin_event(**kwargs)

    $ main_girl_name = get_value('main_girl_name', **kwargs)
    $ main_topic = get_value('main_topic', **kwargs)

    $ girl_last_name = main_girl_name.split(" ")[1]

    call screen black_screen_text("30 minutes later.")

    $ image = Image_Series("/images/events/school building/sb_teach_math_main_1 <main_girl_name> <school_level> <step>.webp", ['main_girl_name'], **kwargs)

    if main_topic == "sleeping":
        call Image_Series.show_image(image, 0, 1, 2, pause = True) from _call_sb_teach_math_main_1_1
        
        # headmaster walks over
        $ image.show(3)
        headmaster_shout "Good Morning Mrs. [girl_last_name]! I hope you had a good nap!"
        
        $ image.show(4)
        sgirl "Eek! I'm sorry, I didn't mean to fall asleep." (name = main_girl_name)

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
    sgirl "2, -5 and 3?" (name = main_girl_name)

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

    call change_stats_with_modifier('school', 'math',
        education = SMALL, reputation = TINY)
    
    $ end_event('new_daytime', **kwargs)

label sb_teach_math_main_2 (**kwargs):
    $ begin_event(**kwargs)

    $ image = Image_Series("/images/events/school building/sb_teach_math_main_2 <school_level> <step>.webp", **kwargs)

    $ image.show(0)
    headmaster "Today I want you to train your equation solving skills."

    $ image.show(1)
    headmaster "For that please open your books on page 42 and solve the equations 1 to 12."

    $ image.show(2)
    headmaster "I'll go through the rows to make sure everyone understands the topic."
    headmaster "If you have a question or don't understand something, please don't hesitate to ask."
    
    call Image_Series.show_image(image, 3, 4, 5, 6, 7) from _call_sb_teach_math_main_2_1
    headmaster "Do you need some help?"
    sgirl "Yes, I don't understand this equation." (name = "Seraphina Clark")

    $ image.show(8)
    headmaster "What is the problem?"

    $ image.show(9)
    sgirl "Well, I don't understand..."

    $ image.show(10)
    sgirl "And then..."

    $ image.show(11)
    headmaster "{i}(  Wow what a nice view down her shirt.  ){/i}" (name = '[headmaster_first_name] [headmaster_last_name] (thinking)')

    $ image.show(12)
    sgirl "Mr. [headmaster_last_name]?"

    $ image.show(13)
    headmaster "Yeah! I'm sorry. I'll help you."
    headmaster "Now, do you remember the abc-formula?"

    call screen black_screen_text('5 minutes later.')

    $ image.show(14)
    sgirl "Thank you Mr. [headmaster_last_name]."

    $ image.show(15)
    headmaster "You're welcome."

    call Image_Series.show_image(image, 16, pause = True) from _call_sb_teach_math_main_2_2

    call screen black_screen_text("1 hour later.")

    $ image.show(17)
    headmaster "That is all for today. Thanks for your attention. See you next time."

    call change_stats_with_modifier('school', 'math',
        education = SMALL, happiness = DEC_TINY, inhibition = DEC_TINY)
    
    $ end_event('new_daytime', **kwargs)

#######

#######################
# General Random Events

label sb_event_1 (**kwargs): # patrol, check class
    $ begin_event(**kwargs)

    $ school_level = get_value('school_level', **kwargs)
    
    $ image = Image_Series("/images/events/school building/sb_event_1 <school_level> <step>.webp", **kwargs)

    $ image.show(0)
    subtitles "You walk through the corridors of the high school."

    $ image.show(1)
    subtitles "You come across a couple making out in the hallway."

    $ call_custom_menu_with_text("What do you do?", character.subtitles, False,
        ("Leave and let them have fun", "sb_event_1.leave"),
        ("Stop them", "sb_event_1.stop", not is_rule_unlocked("student_student_relation")), 
    **kwargs)
label .leave (**kwargs):
    
    $ begin_event()
    
    # show screen black_screen_text("sb_event_1.leave")
    $ image.show(2)
    # call show_image("/images/events/school building/sb_event_1 <name> 3.webp", SCENE, **kwargs)
    subtitles "You decide to leave them and let them have their fun."
    call change_stats_with_modifier('school',
        charm = DEC_SMALL, education = TINY, corruption = TINY, inhibition = DEC_SMALL)
    
    $ end_event('new_daytime', **kwargs)
label .stop (**kwargs):
    
    $ begin_event()
    
    # show screen black_screen_text("sb_event_1.stop")
    $ image.show(3)
    # call show_image("/images/events/school building/sb_event_1 <name> 4.webp", SCENE, **kwargs)
    headmaster "Hey you! Stop that. You know that is against the rules!"
    sgirl "We're sorry!"
    call change_stats_with_modifier('school',
        charm = MEDIUM, happiness = DEC_SMALL, education = SMALL, reputation = TINY, inhibition = DEC_TINY)
    
    $ end_event('new_daytime', **kwargs)

label sb_event_3 (**kwargs): # patrol
    $ begin_event(**kwargs)

    $ school_level = get_value('school_level', **kwargs)
    
    $ image = Image_Series("/images/events/school building/sb_event_3 <school_level> <step>.webp", **kwargs)

    $ image.show(0) # walk with girl sitting
    subtitles "As you walk through the corridors of the high school, you notice a student sitting in the corner of the hallway."
    sgirl "*sniffle*"

    $ image.show(1) # stand next to her asking
    headmaster "Are you okay?"
    
    $ image.show(2) # girl answers without looking up
    sgirl "I'm fine. It's just... No I'm fine."

    $ call_custom_menu(False,
        ("What is going on?", "sb_event_3.what"),
        ("If it's nothing, go back to class", "sb_event_3.send_class", (time.check_daytime("c") and time.check_weekday("d")) or is_replay(**kwargs)), 
    **kwargs)
label .what (**kwargs):
    
    $ begin_event()
    
    $ image.show(3) # headmaster sits next to her
    headmaster "What is going on? I can see there is something bothering you."

    $ image.show(4) # girl still doesn't look
    sgirl "I really don't want to talk about it. I'd like to be alone right now."

    $ image.show(5) # headmaster asks looking straight
    headmaster "Did someone do this to you?"

    $ image.show(6) # girl looks away, headmaster looks at her
    sgirl "..."

    $ call_custom_menu(False, 
        ("Leave her alone", "sb_event_3.leave"), 
        ("Get to the bottom of this", "sb_event_3.get_to_bottom"), 
    **kwargs)
label .leave (**kwargs):
    
    $ begin_event()
    
    $ image.show(6)
    subtitles"You hesitate for a moment, but then decide to leave her alone."

    $ image.show(7) # headmaster stands up
    headmaster "Okay, I'll leave you alone."

    $ image.show(1) # headmaster stands next to her talking
    headmaster "But if you need anything, you can always come to me. My door is always open."

    $ image.show(2) # image 2 but with girl not talking
    sgirl "..."

    $ image.show(8) # headmaster stands a bit further away looking back to her
    subtitles"You walk away with a heavy heart."

    call change_stats_with_modifier('school', 
        charm = TINY, happiness = DEC_LARGE, education = TINY, reputation = DEC_TINY)
    
    $ end_event('new_daytime', **kwargs)
label .get_to_bottom (**kwargs):
    
    $ begin_event()
    
    $ image.show(3) # headmaster looks to girl
    headmaster "I really want to help you. Please tell me what is going on."

    $ image.show(10) # headmaster looks girl doesn't answer
    sgirl "..."
    
    $ image.show(9) # headmaster rests head against wall talking
    headmaster "Please listen."

    $ image.show(10) # headmaster rests head against wall talking
    sgirl "..."
    $ image.show(9) # headmaster rests head against wall talking
    headmaster "Whatever happened to you, if some someone did or said anything."

    $ image.show(11) # girl buries head deeper into arms
    sgirl "*sniffle*"
    subtitles "She slowly and silently starts crying."

    $ image.show(12) # headmaster looks to girl
    headmaster "Let's go to my office, shall we? There it is more private and nobody will bother us. You can then decide what you want to share. Is that okay?"

    $ image.show(13) # girl looks to headmaster
    sgirl "I- I... yes... thank-"

    $ image.show(14) # headmaster and girl walk to office
    subtitles "You support her back to your office and bring her something warm to drink."

    call change_stats_with_modifier('school',
        happiness = LARGE, reputation = TINY)
    
    $ end_event('new_daytime', **kwargs)
label .send_class (**kwargs):
    
    $ begin_event()
    
    $ image.show(15) # headmaster starts walking away
    headmaster "Then you better get back to class."

    $ image.show(16) # girl looks up
    sgirl "B- But... I..."

    $ image.show(17) # headmaster looks back
    headmaster "Yes?"

    $ image.show(18) # girl again buries head in arms
    sgirl "I d-don't..."

    $ call_custom_menu(False, 
        ("Poor thing", "sb_event_3.poor_thing"), 
        ("Chin up", "sb_event_3.chin_up"), 
    **kwargs)
label .poor_thing (**kwargs):

    $ begin_event()
    
    $ image.show(19) # headmaster squats next to her
    headmaster "Look, maybe you should just take the day off. I'll notify your teacher."

    $ image.show(20) # girl looks to headmaster
    sgirl "Yes... thank you..."

    $ image.show(14) # headmaster helps girl up
    subtitles "You help her up and walk her to the dormitory."
    call change_stats_with_modifier('school',
        happiness = LARGE, reputation = TINY)
    
    $ end_event('new_daytime', **kwargs)
label .chin_up (**kwargs):
    
    $ begin_event()
    
    $ image.show(19) # headmaster squats next to her
    headmaster "Now, now, it can't be that bad. I'm sure whatever caused those tears will soon be forgotten."

    $ image.show(21) # girl says nothing
    sgirl "..."

    $ image.show(22) # headmaster stands up
    headmaster "Now, run along. Just tell the teachers you needed a breath of air. I'll take care of the rest."
    sgirl "Ok..."

    $ image.show(23) # girl walks away
    subtitles "You help her up and she walks off."
    call change_stats_with_modifier('school',
        happiness = LARGE, reputation = TINY)
    
    $ end_event('new_daytime', **kwargs)

label sb_event_4(**kwargs):
    $ begin_event(**kwargs)

    $ school_level = get_value('school_level', **kwargs)
    $ girl_name = get_value('girl_name', **kwargs)

    $ image = Image_Series("/images/events/school building/sb_event_4 <school_level> <girl_name> <step>.webp", **kwargs)

    call Image_Series.show_image(image, 0, 1) from _call_Image_Series_show_image_9
    sgirl "AHH!"

    $ image.show(2)
    subtitles "*CRASH*"
    sgirl "Ouch..."

    $ call_custom_menu_with_text("What do you do?", character.subtitles, False,
        ("Leave her alone", "sb_event_4.leave"),
        ("Help her up", "sb_event_4.help"),
        ("Point out her panties", "sb_event_4.panties"),
    **kwargs)
label .leave (**kwargs):

    $ image.show(3)
    headmaster_thought "Hmm, the others already rush to help her. No need for me to get involved."

    call change_stats_with_modifier('school',
        happiness = DEC_TINY, charm = DEC_TINY, education = TINY)

    $ end_event('new_daytime', **kwargs)
label .help (**kwargs):


    $ image.show(4)
    headmaster "Are you okay? Here let me help you."
    
    $ image.show(5)
    sgirl "Thank you."
    
    headmaster "Does anything hurt?"
    
    $ image.show(6)
    sgirl "No, I'm fine."
    
    $ image.show(7)
    headmaster "Okay then. Be more careful next time."
    
    $ image.show(8)
    sgirl "Yes, I will."

    call change_stats_with_modifier('school',
        happiness = SMALL, charm = DEC_TINY, education = TINY)

    $ end_event('new_daytime', **kwargs)
label .panties (**kwargs):

    $ image.show(9)
    headmaster "Cute panties."
    
    $ image.show(10)
    sgirl "Eh?!"
    
    $ image.show(11)
    headmaster "Oh, sorry. I didn't mean to embarrass you. But that cat paw is cute."
    
    $ image.show(12)
    sgirl "Eeeek! Pervert!"

    call Image_Series.show_image(image, 13, pause = True) from _call_Image_Series_show_image_10

    call change_stats_with_modifier('school',
        inhibition = DEC_SMALL, charm = DEC_SMALL, corruption = TINY)

    $ end_event('new_daytime', **kwargs)

label sb_event_5 (**kwargs):
    $ begin_event(**kwargs)

    $ school_level = get_level('school_level', **kwargs)
    $ girls = get_value('girls', **kwargs)

    $ image = Image_Series("/images/events/school building/sb_event_5 <school_level> <girls> <step>.webp", ['school_level', 'girls'], **kwargs)

    $ girl_char = Character(girls, kind=character.sgirl)

    call Image_Series.show_image(image, 0, 1, 2) from _call_show_image_sb_event_5_event_1
    # headmaster walks through hallway
    subtitles "*thump*"
    $ image.show(3)
    headmaster "Huh?"
    $ image.show(4)
    headmaster_thought "Hmm, is someone in the classroom?"
    headmaster_thought "That class should have physical education right now."
    $ image.show(5)
    headmaster_thought "I should check that out."
    # headmaster opens door
    # you see three girls changing clothes
    call Image_Series.show_image(image, 6, 7, 8) from _call_show_image_sb_event_5_event_2
    girl_char "Huh?!"
    # headmaster closes door
    call Image_Series.show_image(image, 7, 9, 10) from _call_show_image_sb_event_5_event_3
    headmaster "I'm sorry! I didn't mean to barge into you changing."
    headmaster "But I have to ask, why are you here? Should you be in the gym for class?"
    $ image.show(11)
    girl_char "We like to change clothes here. The changing rooms in the gym are too small and uncomfortable."
    $ image.show(10)
    headmaster "I understand. But please hurry up. You'll be late for class."
    $ image.show(11)
    girl_char "Yes, sir."

    call change_stats_with_modifier('school',
        inhibition = DEC_TINY)

    $ end_event('new_daytime', **kwargs)

