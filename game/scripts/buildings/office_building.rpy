##############################################
# region Office Building Event Handler ----- #
##############################################

init -1 python:
    set_current_mod('base')
    
    office_building_timed_event   = TempEventStorage("office_building", "office_building", fallback = Event(2, "office_building.after_time_check"))
    office_building_general_event =     EventStorage("office_building", "office_building", fallback = Event(2, "office_building.after_general_check"))
    register_highlighting(office_building_timed_event, office_building_general_event)

    office_building_work_event = {}
    add_storage(office_building_work_event, EventStorage("counselling", "office_building"))
    add_storage(office_building_work_event, EventStorage("money",       "office_building"))
    add_storage(office_building_work_event, EventStorage("education",   "office_building"))
    add_storage(office_building_work_event, EventStorage("reputation",  "office_building"))

    office_building_events = {}
    add_storage(office_building_events, EventStorage("look_around",      "office_building"))
    add_storage(office_building_events, EventStorage("work",             "office_building"))
    add_storage(office_building_events, EventStorage("learn",            "office_building", ShowBlockedOption()))
    add_storage(office_building_events, EventStorage("call_secretary",   "office_building"))
    add_storage(office_building_events, EventStorage("schedule_meeting", "office_building"))


    office_building_subject_learn_events = {}
    add_storage(office_building_subject_learn_events, EventStorage("math",    "office_building", fallback_text = "There is nobody here."))
    add_storage(office_building_subject_learn_events, EventStorage("history", "office_building", fallback_text = "There is nobody here."))
    add_storage(office_building_subject_learn_events, EventStorage("pe",      "office_building", fallback_text = "There is nobody here."))

    office_building_call_secretary_events = {}
    add_storage(office_building_call_secretary_events, EventStorage("naughty_sandbox", "office_building", fallback_text = "There is nobody here."))

    office_building_bg_images = BGStorage("images/background/office building/bg f.webp",
        RandomListSelector('name', 'teacher', 'secretary'), 
        LevelSelector('level', KwargsValueSelector('', 'name')),
        BGImage("images/background/office building/c teacher.webp", 1, AND(TimeCondition(daytime = "c"), ValueCondition('name', 'teacher'))), # show headmasters/teachers office empty
        BGImage("images/background/office building/<name> <level> <variant> <nude>.webp", 1, NOT(TimeCondition(daytime = "7"))), # show headmasters/teachers office with people
        BGImage("images/background/office building/n <name>.webp", 1, TimeCondition(daytime = 7)), # show headmasters/teachers office empty at night
    )

init 1 python: 
    set_current_mod('base')  
    
    office_building_events["look_around"].add_event(
        Event(3, "office_event_1",
            TimeCondition(weekday = "d", daytime = "f"),
            Pattern("main", "images/events/office/office_event_1/office_event_1 <school_level> <step>.webp"),
            thumbnail = "images/events/office/office_event_1/office_event_1 1 0.webp"),
        Event(3, "office_event_2",
            RandomListSelector("teacher", "finola_ryan", "yulan_chen"),
            TimeCondition(weekday = "d", daytime = "f"),
            Pattern("main", "images/events/office/office_event_2/office_event_2 <teacher_level> <teacher>.webp"),
            thumbnail = "images/events/office/office_event_2/office_event_2 1 finola_ryan.webp"),
        Event(3, "office_event_3",
            TimeCondition(weekday = "d", daytime = "d"),
            LevelCondition("1-5", "school"),
            NOT(RuleCondition("student_student_relation")),
            Pattern("main", "images/events/office/office_event_3/office_event_3 <school_level> <step>.webp"),
            thumbnail = "images/events/office/office_event_3/office_event_3 1 0.webp"),
        Event(3, "office_event_4",
            TimeCondition(weekday = "d", daytime = "d"),
            Pattern("main", "images/events/office/office_event_4/office_event_4 <secretary_level> <step>.webp", "secretary_level"),
            thumbnail = "images/events/office/office_event_4/office_event_4 5 0.webp"),
    )

    office_call_secretary_event_event = EventSelect(3, "call_secretary_event", "What do you want to do?", office_building_call_secretary_events,
        override_menu_exit = 'office_building',)

    office_building_call_secretary_events["naughty_sandbox"].add_event(
        Event(3, "office_call_secretary_naughty_sandbox",
            ProgressCondition("work_office_session_naughty"),
            Pattern("main", "images/events/office/office_call_secretary_naughty_sandbox/office_call_secretary_naughty_sandbox <secretary_level> <step>.webp", 'secretary_level'),
            thumbnail = "images/events/office/office_call_secretary_naughty_sandbox/office_call_secretary_naughty_sandbox 6 3.webp"))
    
    office_building_events["call_secretary"].add_event(
        office_call_secretary_event_event,)

    office_work_office_event_event = EventSelect(3, "work_office_event", "What do you want to work on?", office_building_work_event,
        TimeCondition(weekday = "d", daytime = "d"),
        override_menu_exit = 'office_building')

    office_building_events["work"].add_event(
        office_work_office_event_event,)

    office_building_subject_learn_events['math'].add_event(
        Event(3, "learn_office_event_1", ProficiencyCondition("math", level = "10-"), ValueSelector('subject', 'math')))
    office_building_subject_learn_events['history'].add_event(
        Event(3, "learn_office_event_1", ProficiencyCondition("history", level = "10-"), ValueSelector('subject', 'history')))
    office_building_subject_learn_events['pe'].add_event(
        Event(3, "learn_office_event_1", ProficiencyCondition("pe", level = "10-"), ValueSelector('subject', 'pe')))

    office_building_events["learn"].add_event(
        EventSelect(3, "learn_subject_event", "What subject do you wanna learn?", office_building_subject_learn_events,
            TimeCondition(daytime = 1),
            MoneyCondition(500),
            override_menu_exit = 'office_building'))

    office_building_work_event["money"].add_event(
        Event(3, "work_office_money_event_1",
            TimeCondition(weekday = "d", daytime = "d"),
            Pattern("main", 'images/events/office/office_money_event_1/office_money_event_1 <step>.webp'),
            thumbnail = "images/events/office/office_money_event_1/office_money_event_1 1.webp"),)

    office_building_work_event["education"].add_event(
        Event(3, "work_office_education_event_1",
            TimeCondition(weekday = "d", daytime = "d"),
            Pattern("main", "images/events/office/office_education_event_1/office_education_event_1 <step>.webp"),
            thumbnail = "images/events/office/office_education_event_1/office_education_event_1 0.webp"),)

    office_building_work_event["reputation"].add_event(
        Event(3, "work_office_reputation_event_1",
            TimeCondition(weekday = "d", daytime = "d"),
            Pattern("main", "images/events/office/office_reputation_event_1/office_reputation_event_1 <step>.webp"),
            thumbnail = "images/events/office/office_reputation_event_1/office_reputation_event_1 1.webp"),)

    office_building_work_event["counselling"].add_event(
        Event(3, "work_office_session_event_1",
            TimeCondition(weekday = "d", daytime = "d"),
            RandomListSelector("girl_name", "yuriko_oshima", "elsie_johnson", "easkey_tanaka"),
            Pattern("main", "images/events/office/office_session_event_1/office_session_event_1 <girl_name> <school_level> <secretary_level> <step>.webp", 'girl_name', 'school_level', 'secretary_level'),
            thumbnail = "images/events/office/office_session_event_1/office_session_event_1 easkey_tanaka 1 # 4.webp"),
        Event(3, "work_office_session_event_first_naughty",
            TimeCondition(weekday = "d", daytime = "d"),
            LevelSelector('school_level', 'school'),
            LevelSelector('secretary_level', 'secretary'),
            ProgressCondition("counselling sessions", "3+"),
            NOT(ProgressCondition("work_office_session_naughty")),
            Pattern("main", "images/events/office/office_event_first_naughty/office_event_first_naughty 0 <step>.webp"),
            thumbnail = "images/events/office/office_event_first_naughty/office_event_first_naughty 0 62.webp"))

# endregion
##############################################

############################################
# region Office Building Entry Point ----- #
############################################

label office_building ():
    call call_available_event(office_building_timed_event) from office_building_1

label .after_time_check (**kwargs):
    call call_available_event(office_building_general_event) from office_building_4

label .after_general_check (**kwargs):
    call call_event_menu (
        "What do you do?", 
        office_building_events, 
        default_fallback,
        character.subtitles,
        bg_image = office_building_bg_images,
    ) from office_building_3

    jump office_building

# endregion
############################################

######################
# region Work Events #

label work_office_reputation_event_1 (**kwargs):
    $ begin_event(**kwargs)

    $ image = convert_pattern("main", **kwargs)

    $ image.show(0)
    subtitles "You decided to to some PR work, trying to improve the schools and your reputation."
    call screen black_screen_text("1h later.")
    $ image.show(1)
    headmaster_thought "I think I found a way to make the school more appealing to the public."
    $ image.show(2)
    headmaster_thought "I hope this will help to improve the reputation of the school."

    call change_stats_with_modifier('school', reputation = SMALL) from _call_change_stats_with_modifier_38

    $ end_event('new_daytime', **kwargs)

label work_office_money_event_1 (**kwargs):
    $ begin_event(**kwargs)

    $ image = convert_pattern("main", **kwargs)

    $ image.show(0)
    subtitles "You work on checking the accounts of the school."
    call screen black_screen_text("1h later.")
    # headmaster is consumed by the terrible accounting done in the past
    $ image.show(1)
    headmaster_thought "How can this be? This is a mess!"
    headmaster_thought "I need to get this sorted out."
    headmaster_thought "There is so much wrong with these accounts. It's gonna take ages to fix this."
    $ image.show(2)
    headmaster_thought "At least I was able to find some money that was lost in the system."

    call change_money_with_modifier(get_random_int(100, 500)) from _call_change_money_with_modifier

    $ end_event('new_daytime', **kwargs)

label work_office_education_event_1 (**kwargs):
    $ begin_event(**kwargs)

    $ image = convert_pattern("main", **kwargs)

    $ image.show(0)
    subtitles "You work on optimizing the teaching material for the students."
    call screen black_screen_text("1h later.")
    $ image.show(1)
    headmaster_thought "I think I found a way to make the material more interesting for the students."

    call change_stats_with_modifier('school',
        education = SMALL, happiness = TINY) from _call_change_stats_with_modifier_39
    call change_stats_with_modifier('teacher',
        happiness = SMALL, education = SMALL) from _call_change_stats_with_modifier_40

    $ end_event('new_daytime', **kwargs)

label learn_office_event_1 (**kwargs):
    $ begin_event(no_gallery = True, **kwargs)

    $ subject = get_value('subject', **kwargs)

    $ text = get_translation(subject)

    call screen black_screen_text("You spend the entire day learning more about [text].")

    $ curr_xp = get_headmaster_proficiency_xp(subject)
    $ curr_lvl = get_headmaster_proficiency_level(subject)
    $ delta = 20
    if curr_lvl > 0:
        $ delta = math.ceil(int(100 / (curr_lvl * 10)))
    $ missing = math.floor(get_headmaster_proficiency_xp_until_level(subject))
    if missing == -1:
        $ missing = 100
    $ subtitle = f"XP: {curr_xp:.0f}% -> " + "{color=#00a000}" + f"{(curr_xp + delta):.0f}%" + "{/color}"

    if delta >= missing:
        $ delta = missing
        call screen black_screen_text_with_subtitle("[text]: Lvl. " + str(curr_lvl) + " -> {color=#00a000}" + str(curr_lvl + 1) + "{/color}", "XP: {color=#00a000}100% Level Up!{/color}")
    else:
        call screen black_screen_text_with_subtitle("[text]: Lvl. " + str(curr_lvl), subtitle)

    $ change_headmaster_proficiency_xp(subject, delta)
    call change_money(-500) from _call_change_money

    $ end_event('new_day', **kwargs)

label work_office_session_event_1(**kwargs):
    $ begin_event(**kwargs)

    $ girl_name = get_value('girl_name', **kwargs)
    $ get_level('school_level', **kwargs)
    $ get_level('secretary_level', **kwargs)

    $ girl_person = get_person("class_3a", girl_name)
    $ girl = girl_person.get_character()

    $ girl_first_name = girl_person.get_first_name()
    $ girl_last_name = girl_person.get_last_name()

    $ image = convert_pattern("main", **kwargs)

    $ image.show(0)
    subtitles_Empty "*Knock* *Knock*"
    $ image.show(1)
    headmaster "Yes?"
    $ image.show(2)
    secretary "[headmaster_first_name], Ms. [girl_last_name] is here for here counselling session."
    $ image.show(3)
    headmaster "Thank you. Please let her in."
    $ image.show(4)
    sgirl "Hello Mr. [headmaster_last_name]." (name = girl_name)
    $ image.show(5)
    headmaster "Hello [girl_first_name]. Please take a seat."
    $ image.show(4)
    sgirl "Thank you."
    $ image.show(6)
    headmaster "Now where did we stop last time?"
    call screen black_screen_text("1h later.")
    $ image.show(6)
    headmaster "I think we made some progress this time. How do you feel about it?"
    $ image.show(7)
    sgirl "I feel better. Thank you for your help."
    $ image.show(8)
    headmaster "You're welcome. I'm always here to help you."
    $ image.show(9)
    sgirl "Thank you. I'll see you next time."
    $ image.show(10)
    headmaster "Goodbye."

    $ advance_progress('counselling sessions')

    call change_stats_with_modifier('school',
        happiness = MEDIUM, education = SMALL) from _call_change_stats_with_modifier_43

    $ end_event('new_daytime', **kwargs)

# endregion
######################

########################
# region First naughty #

define anim_oefn_path = "images/events/office/office_event_first_naughty/office_event_first_naughty 0 "
image anim_office_event_first_naughty_0_16 = Movie(play = anim_oefn_path + "16.webm", start_image = anim_oefn_path + "16.webp", image = anim_oefn_path + "16.webp")
image anim_office_event_first_naughty_0_17 = Movie(play = anim_oefn_path + "17.webm", start_image = anim_oefn_path + "17.webp", image = anim_oefn_path + "17.webp")
image anim_office_event_first_naughty_0_18 = Movie(play = anim_oefn_path + "18.webm", start_image = anim_oefn_path + "18.webp", image = anim_oefn_path + "18.webp")
image anim_office_event_first_naughty_0_21 = Movie(play = anim_oefn_path + "21.webm", start_image = anim_oefn_path + "21.webp", image = anim_oefn_path + "21.webp")
image anim_office_event_first_naughty_0_64 = Movie(play = anim_oefn_path + "64.webm", start_image = anim_oefn_path + "64.webp", image = anim_oefn_path + "64.webp")
image anim_office_event_first_naughty_0_65 = Movie(play = anim_oefn_path + "65.webm", start_image = anim_oefn_path + "65.webp", image = anim_oefn_path + "65.webp")
image anim_office_event_first_naughty_0_66 = Movie(play = anim_oefn_path + "66.webm", start_image = anim_oefn_path + "66.webp", image = anim_oefn_path + "66.webp")
image anim_office_event_first_naughty_0_67 = Movie(play = anim_oefn_path + "67.webm", start_image = anim_oefn_path + "67.webp", image = anim_oefn_path + "67.webp")
image anim_office_event_first_naughty_0_68 = Movie(play = anim_oefn_path + "68.webm", start_image = anim_oefn_path + "68.webp", image = anim_oefn_path + "68.webp")
image anim_office_event_first_naughty_0_69 = Movie(play = anim_oefn_path + "69.webm", start_image = anim_oefn_path + "69.webp", image = anim_oefn_path + "69.webp")
image anim_office_event_first_naughty_0_72 = Movie(play = anim_oefn_path + "72.webm", start_image = anim_oefn_path + "72.webp", image = anim_oefn_path + "72.webp")
image anim_office_event_first_naughty_0_73 = Movie(play = anim_oefn_path + "73.webm", start_image = anim_oefn_path + "73.webp", image = anim_oefn_path + "73.webp")
image anim_office_event_first_naughty_0_74 = Movie(play = anim_oefn_path + "74.webm", start_image = anim_oefn_path + "74.webp", image = anim_oefn_path + "74.webp")
image anim_office_event_first_naughty_0_75 = Movie(play = anim_oefn_path + "75.webm", start_image = anim_oefn_path + "75.webp", image = anim_oefn_path + "75.webp")
label work_office_session_event_first_naughty (**kwargs):
    $ begin_event(**kwargs)

    $ school_level = get_value('school_level', **kwargs)
    $ secretary_level = get_value('secretary_level', **kwargs)

    $ yuriko = get_person("class_3a", "yuriko_oshima").get_character()

    $ image = convert_pattern("main", video_prefix = "anim_", **kwargs)

    # secretary enters office
    call Image_Series.show_image(image, 0, 1, 2) from _call_work_office_session_event_first_naughty_1
    if time.check_daytime("3-"):
        secretary "Good Morning [headmaster_first_name]."
    else:
        secretary "Hello [headmaster_first_name]."

    secretary "I just wanted to remind you that you have a meeting with Yuriko Oshima in 30 minutes."
    $ image.show(3)
    headmaster "Oh, thank you for reminding me. I almost forgot. She asked for a counseling session, right?"
    $ image.show(4)
    secretary "Yes, she did."
    $ image.show(5)
    headmaster "Okay, I will prepare myself for that."
    $ image.show(6)
    headmaster "..."
    $ image.show(7)
    secretary "..."
    $ image.show(8)
    headmaster "Is there anything else?"
    $ image.show(9)
    secretary "You know... I really liked our time we had together last time."
    $ image.show(10)
    headmaster "What do you mean? Oh, you mean..."
    $ image.show(11)
    secretary "Yes, the fun we had with the potion. I really enjoyed it."
    $ image.show(12)
    secretary "So I thought we could... you know... there is still some time until the meeting."
    $ image.show(13)
    secretary "So maybe I could help you 'relax' a bit before that."
    $ image.show(14)
    headmaster "I see. I would very much like that."
    $ image.show(15)
    secretary "Then please lean back and let me take care of you."
    
    $ image.show_video(16, True)

    $ image.show_video(17, True)

    $ image.show_video(18, True)

    $ image.show_video(21, True)

    # secretary starts giving blow and titjob
    $ image.show(22)
    subtitles "*Knock! Knock!*"
    $ image.show(23)
    yuriko "Excuse me? Mr. [headmaster_last_name]?"
    $ image.show(24)
    headmaster_whisper "Shit! Quick under the desk!"
    call Image_Series.show_image(image, 25, 26) from _call_work_office_session_event_first_naughty_2
    headmaster "Yes come in."
    call Image_Series.show_image(image, 27, 28, 29) from _call_work_office_session_event_first_naughty_3
    headmaster "You're early."
    $ image.show(30)
    yuriko "I apologize for that. Something came up in school and I need to leave earlier. So I thought, I'd come earlier."
    $ image.show(31)
    yuriko "I wanted to ask your secretary first but I couldn't find her."
    call Image_Series.show_image(image, 32, 40) from _call_work_office_session_event_first_naughty_5
    headmaster "Oh she is probably doing some rounds."
    $ image.show(32)
    headmaster "You're really not able to take the session on the agreed time?"
    $ image.show(33)
    yuriko "I don't think so..."
    $ image.show(34)
    headmaster "Alright, then let's do it now. Take a seat."
    call Image_Series.show_image(image, 35, 36, 37, 38) from _call_work_office_session_event_first_naughty_4
    yuriko "Are you okay? You look a bit flushed."
    call Image_Series.show_image(image, 39, 40) from _call_work_office_session_event_first_naughty_6
    headmaster "Yes, I'm fine. I just had a bit of a headache. But it's getting better."
    $ image.show(41)
    headmaster "Okay what do you want to talk about today?"

    $ image.show(42)
    yuriko "Well, Mr. [headmaster_last_name], I've been feeling really stressed lately."
    $ image.show(43)
    headmaster "I see. Is there something specific that's been bothering you?"
    $ image.show(44)
    yuriko "Yes, it's mainly the pressure to perform well academically. I feel like I'm constantly under scrutiny."
    $ image.show(45)
    headmaster "I understand. Academic pressure can be overwhelming. Have you tried talking to your teachers about it?"
    $ image.show(44)
    yuriko "I haven't yet. I guess I'm afraid they won't understand or think I'm just making excuses."
    $ image.show(43)
    headmaster "I assure you, Yuriko, your feelings are valid. It's important to communicate your struggles with your teachers so they can support you."
    $ image.show(46)
    yuriko "Thank you, Mr. [headmaster_last_name]. I'll try to gather the courage to talk to them."
    $ image.show(47)
    headmaster "That's a good step forward. Remember, you're not alone in this. We're here to help you succeed."
    $ image.show(43)
    headmaster "If it is too difficult for you to talk to your teachers, how about your friends? Maybe they can help you."
    $ image.show(44)
    yuriko "It's... It's quite hard. I don't really have friends. I have Ellie, but I fear bothering her too much with my problems."
    $ image.show(48)
    headmaster "Ellie?"
    $ image.show(42)
    yuriko "Yes, Elsie Johnson. She's in my class. She's really nice and I really like her. But I don't want to be a burden to her."
    $ image.show(45)
    headmaster "I see. It's important to have someone to talk to. Maybe you can try to open up to her."
    $ image.show(43)
    headmaster "It's always good to be able to talk to someone you're close to."
    $ image.show(49)
    headmaster "I'll be always here to help yoaaaaaah!"
    # emiko starts handling your rod again
    $ image.show(50)
    yuriko "Sir, is everything okay?"
    $ image.show(51)
    headmaster "*cough* *cough* Yes, everything is fine. I just swallowed wrong."
    $ image.show(52)
    headmaster "What I wanted to say is that you can always come to me if you need help but you understand that it is difficult in my position to provide a level of intimacy that you might need."
    $ image.show(50)
    yuriko "Intimacy?"
    # emiko grins at you and then continues
    $ image.show(40)
    pause

    $ image.show(52)
    headmaster "Yes! You know humans don't work very well when being alone. We need to be close to others to feel good."
    $ image.show(53)
    headmaster "It even isn't really enough to just have people you know around you. You need to have people you trust. A sort of intimate bonding."
    headmaster "Even physical contact plays an important role in that. It's a way to show that you care about someone."
    $ image.show(54)
    yuriko "Physical contact? I don't think I can go that far..." # Yuriko blushes
    $ image.show(55)
    headmaster "Don't misunderstand. Even hugging someone can be a form of physical contact. It's not always about a sexual relationship."
    $ image.show(56)
    headmaster "Even though having sex can be the closest form of intimacy. But it's not the only one and that is not what I meant in this case."
    headmaster "That is why you really should try to talk to Elsie about your problems, your feelings and your fears. She might be able to help you."
    $ image.show(55)
    headmaster "How about you do that, and the next time we talk about how it went? Would that be okay for you?"
    $ image.show(57)
    yuriko "Yes, I think I can do that. Thank you, Mr. [headmaster_last_name]."
    $ image.show(56)
    headmaster "You're welcome, Yuriko. Now I think that settles it for today. I hope I could help you a bit."
    $ image.show(46)
    yuriko "Yes, you did. Thank you."
    $ image.show(56)
    headmaster "Thank you for entrusting yourself to me."
    headmaster "I have a lot to do, so unfortunately I can't accompany you to the door. So please just close the door behind you."
    $ image.show(31)
    yuriko "Will do. Thank you."
    $ image.show(58)
    headmaster "Have a nice day."
    # Yuriko leaves
    # emiko comes out from under the desk
    call Image_Series.show_image(image, 59, 60) from _call_work_office_session_event_first_naughty_7
    secretary "That was close."
    $ image.show(61)
    headmaster "Now I've got enough!"
    secretary "What?"
    call Image_Series.show_image(image, 62, 63, pause = True) from _call_work_office_session_event_first_naughty_8
    
    
    $ image.show_video(64)
    pause 1.0

    $ image.show_video(65)
    secretary "Oh yes! Yes! Yes!"
    headmaster "What were you thinking doing that with Yuriko sitting just in front of me!"
    secretary "I'm sorry! *moan* I couldn't resist!"
    $ image.show_video(66)
    headmaster "You will be punished for that!"
    secretary "Yes, I deserve it!... But it was so hot! *moan*"
    headmaster "I see that, you're as wet as a river!"
    $ image.show_video(67)
    headmaster "I will make sure you will never forget this!"
    headmaster "Take this!"
    $ image.show_video(68)
    secretary "OH MY GOD! YES! YES! YES!" (interact = False)
    pause 3.0
    $ image.show_video(69)
    # headmaster cums
    secretary "Oh my god! That was amazing!"
    $ image.show(70)
    headmaster "We're not finished!"
    secretary "Huh?"
    headmaster "Remember, this is your punishment."
    $ image.show(71)
    headmaster "Now get on your knees and open your mouth!"
    # headmaster deepthroats her
    $ image.show_video(72)
    secretary "Hmmpf! *gag* *gag* *gag*"
    headmaster "That's what you get for almost exposing us!"
    $ image.show_video(73)
    secretary "I'm sorry! *gag* *gag* *gag*"
    # headmaster cums in her throat
    $ image.show_video(74)
    pause 5.3
    $ image.show_video(75)
    secretary "*cough* *cough* *cough*"
    $ image.show(76)
    headmaster "Now clean yourself up and get back to work!"
    $ image.show(77)
    secretary "Yes, Master."
    # secretary collecting her stuff
    $ image.show(78)
    headmaster_thought "Master? Maybe I overdid it a bit."
    call Image_Series.show_image(image, 79, 80, 81, 82, 83, 84, 85, 86, 87, pause = True) from _call_work_office_session_event_first_naughty_9
    # shot of yuriko standing in front of the door blushed and then running away
    # emiko leaves the office quite happy and finds yurikos scarf on the floor

    $ start_progress('work_office_session_naughty')
    $ get_character_by_key('secretary').set_level(6)

    call change_stats_with_modifier('school',
        inhibition = DEC_MEDIUM, corruption = MEDIUM, happiness = DEC_SMALL) from _call_change_stats_with_modifier_41
    call change_stats_with_modifier('secretary',
        happiness = LARGE, corruption = LARGE, inhibition = DEC_MEDIUM) from _call_change_stats_with_modifier_42

    $ end_event('new_daytime', **kwargs)

# endregion
########################

##########################
# region Naughty Sandbox #

define anim_osn_path = "images/events/office/office_call_secretary_naughty_sandbox/sandbox/"
# desk - handjob
image anim_osn_desk_handjob_full_casual_5_0 = Movie(play = anim_osn_path + "desk_handjob_full_casual_5_0.webm", start_image =  anim_osn_path + "desk_handjob_full_casual_5_0.webp", image =  anim_osn_path + "desk_handjob_full_casual_5_0.webp", group = "office_secretary_naughty")
image anim_osn_desk_handjob_full_casual_5_1 = Movie(play = anim_osn_path + "desk_handjob_full_casual_5_1.webm", start_image =  anim_osn_path + "desk_handjob_full_casual_5_1.webp", image =  anim_osn_path + "desk_handjob_full_casual_5_1.webp", group = "office_secretary_naughty")
image anim_osn_desk_handjob_full_casual_5_2 = Movie(play = anim_osn_path + "desk_handjob_full_casual_5_2.webm", start_image =  anim_osn_path + "desk_handjob_full_casual_5_2.webp", image =  anim_osn_path + "desk_handjob_full_casual_5_2.webp", group = "office_secretary_naughty")
image anim_osn_desk_handjob_full_casual_6_0 = Movie(play = anim_osn_path + "desk_handjob_full_casual_6_0.webm", start_image =  anim_osn_path + "desk_handjob_full_casual_6_0.webp", image =  anim_osn_path + "desk_handjob_full_casual_6_0.webp", group = "office_secretary_naughty")
image anim_osn_desk_handjob_full_casual_6_1 = Movie(play = anim_osn_path + "desk_handjob_full_casual_6_1.webm", start_image =  anim_osn_path + "desk_handjob_full_casual_6_1.webp", image =  anim_osn_path + "desk_handjob_full_casual_6_1.webp", group = "office_secretary_naughty")
image anim_osn_desk_handjob_full_casual_6_2 = Movie(play = anim_osn_path + "desk_handjob_full_casual_6_2.webm", start_image =  anim_osn_path + "desk_handjob_full_casual_6_2.webp", image =  anim_osn_path + "desk_handjob_full_casual_6_2.webp", group = "office_secretary_naughty")
image anim_osn_desk_handjob_underwear_0     = Movie(play = anim_osn_path + "desk_handjob_underwear_0.webm",     start_image =  anim_osn_path + "desk_handjob_underwear_0.webp",     image =  anim_osn_path + "desk_handjob_underwear_0.webp",     group = "office_secretary_naughty")
image anim_osn_desk_handjob_underwear_1     = Movie(play = anim_osn_path + "desk_handjob_underwear_1.webm",     start_image =  anim_osn_path + "desk_handjob_underwear_1.webp",     image =  anim_osn_path + "desk_handjob_underwear_1.webp",     group = "office_secretary_naughty")
image anim_osn_desk_handjob_underwear_2     = Movie(play = anim_osn_path + "desk_handjob_underwear_2.webm",     start_image =  anim_osn_path + "desk_handjob_underwear_2.webp",     image =  anim_osn_path + "desk_handjob_underwear_2.webp",     group = "office_secretary_naughty")
image anim_osn_desk_handjob_nude_0          = Movie(play = anim_osn_path + "desk_handjob_nude_0.webm",          start_image =  anim_osn_path + "desk_handjob_nude_0.webp",          image =  anim_osn_path + "desk_handjob_nude_0.webp",          group = "office_secretary_naughty")
image anim_osn_desk_handjob_nude_1          = Movie(play = anim_osn_path + "desk_handjob_nude_1.webm",          start_image =  anim_osn_path + "desk_handjob_nude_1.webp",          image =  anim_osn_path + "desk_handjob_nude_1.webp",          group = "office_secretary_naughty")
image anim_osn_desk_handjob_nude_2          = Movie(play = anim_osn_path + "desk_handjob_nude_2.webm",          start_image =  anim_osn_path + "desk_handjob_nude_2.webp",          image =  anim_osn_path + "desk_handjob_nude_2.webp",          group = "office_secretary_naughty")

# desk - blowjob
image anim_osn_desk_blowjob_full_casual_5_0 = Movie(play = anim_osn_path + "desk_blowjob_full_casual_5_0.webm", start_image =  anim_osn_path + "desk_blowjob_full_casual_5_0.webp", image =  anim_osn_path + "desk_blowjob_full_casual_5_0.webp", group = "office_secretary_naughty")
image anim_osn_desk_blowjob_full_casual_5_1 = Movie(play = anim_osn_path + "desk_blowjob_full_casual_5_1.webm", start_image =  anim_osn_path + "desk_blowjob_full_casual_5_1.webp", image =  anim_osn_path + "desk_blowjob_full_casual_5_1.webp", group = "office_secretary_naughty")
image anim_osn_desk_blowjob_full_casual_5_2 = Movie(play = anim_osn_path + "desk_blowjob_full_casual_5_2.webm", start_image =  anim_osn_path + "desk_blowjob_full_casual_5_2.webp", image =  anim_osn_path + "desk_blowjob_full_casual_5_2.webp", group = "office_secretary_naughty")
image anim_osn_desk_blowjob_full_casual_5_3 = Movie(play = anim_osn_path + "desk_blowjob_full_casual_5_3.webm", start_image =  anim_osn_path + "desk_blowjob_full_casual_5_3.webp", image =  anim_osn_path + "desk_blowjob_full_casual_5_3.webp", group = "office_secretary_naughty")
image anim_osn_desk_blowjob_full_casual_6_0 = Movie(play = anim_osn_path + "desk_blowjob_full_casual_6_0.webm", start_image =  anim_osn_path + "desk_blowjob_full_casual_6_0.webp", image =  anim_osn_path + "desk_blowjob_full_casual_6_0.webp", group = "office_secretary_naughty")
image anim_osn_desk_blowjob_full_casual_6_1 = Movie(play = anim_osn_path + "desk_blowjob_full_casual_6_1.webm", start_image =  anim_osn_path + "desk_blowjob_full_casual_6_1.webp", image =  anim_osn_path + "desk_blowjob_full_casual_6_1.webp", group = "office_secretary_naughty")
image anim_osn_desk_blowjob_full_casual_6_2 = Movie(play = anim_osn_path + "desk_blowjob_full_casual_6_2.webm", start_image =  anim_osn_path + "desk_blowjob_full_casual_6_2.webp", image =  anim_osn_path + "desk_blowjob_full_casual_6_2.webp", group = "office_secretary_naughty")
image anim_osn_desk_blowjob_full_casual_6_3 = Movie(play = anim_osn_path + "desk_blowjob_full_casual_6_3.webm", start_image =  anim_osn_path + "desk_blowjob_full_casual_6_3.webp", image =  anim_osn_path + "desk_blowjob_full_casual_6_3.webp", group = "office_secretary_naughty")
image anim_osn_desk_blowjob_underwear_0 =     Movie(play = anim_osn_path + "desk_blowjob_underwear_0.webm",     start_image =  anim_osn_path + "desk_blowjob_underwear_0.webp",     image =  anim_osn_path + "desk_blowjob_underwear_0.webp",     group = "office_secretary_naughty")
image anim_osn_desk_blowjob_underwear_1 =     Movie(play = anim_osn_path + "desk_blowjob_underwear_1.webm",     start_image =  anim_osn_path + "desk_blowjob_underwear_1.webp",     image =  anim_osn_path + "desk_blowjob_underwear_1.webp",     group = "office_secretary_naughty")
image anim_osn_desk_blowjob_underwear_2 =     Movie(play = anim_osn_path + "desk_blowjob_underwear_2.webm",     start_image =  anim_osn_path + "desk_blowjob_underwear_2.webp",     image =  anim_osn_path + "desk_blowjob_underwear_2.webp",     group = "office_secretary_naughty")
image anim_osn_desk_blowjob_underwear_3 =     Movie(play = anim_osn_path + "desk_blowjob_underwear_3.webm",     start_image =  anim_osn_path + "desk_blowjob_underwear_3.webp",     image =  anim_osn_path + "desk_blowjob_underwear_3.webp",     group = "office_secretary_naughty")
image anim_osn_desk_blowjob_nude_0 =          Movie(play = anim_osn_path + "desk_blowjob_nude_0.webm",          start_image =  anim_osn_path + "desk_blowjob_nude_0.webp",          image =  anim_osn_path + "desk_blowjob_nude_0.webp",          group = "office_secretary_naughty")
image anim_osn_desk_blowjob_nude_1 =          Movie(play = anim_osn_path + "desk_blowjob_nude_1.webm",          start_image =  anim_osn_path + "desk_blowjob_nude_1.webp",          image =  anim_osn_path + "desk_blowjob_nude_1.webp",          group = "office_secretary_naughty")
image anim_osn_desk_blowjob_nude_2 =          Movie(play = anim_osn_path + "desk_blowjob_nude_2.webm",          start_image =  anim_osn_path + "desk_blowjob_nude_2.webp",          image =  anim_osn_path + "desk_blowjob_nude_2.webp",          group = "office_secretary_naughty")
image anim_osn_desk_blowjob_nude_3 =          Movie(play = anim_osn_path + "desk_blowjob_nude_3.webm",          start_image =  anim_osn_path + "desk_blowjob_nude_3.webp",          image =  anim_osn_path + "desk_blowjob_nude_3.webp",          group = "office_secretary_naughty")

# desk - missionary
image anim_osn_desk_missionary_full_casual_5_0 = Movie(play = anim_osn_path + "desk_missionary_full_casual_5_0.webm", start_image =  anim_osn_path + "desk_missionary_full_casual_5_0.webp", image =  anim_osn_path + "desk_missionary_full_casual_5_0.webp", group = "office_secretary_naughty")
image anim_osn_desk_missionary_full_casual_5_1 = Movie(play = anim_osn_path + "desk_missionary_full_casual_5_1.webm", start_image =  anim_osn_path + "desk_missionary_full_casual_5_1.webp", image =  anim_osn_path + "desk_missionary_full_casual_5_1.webp", group = "office_secretary_naughty")
image anim_osn_desk_missionary_full_casual_5_2 = Movie(play = anim_osn_path + "desk_missionary_full_casual_5_2.webm", start_image =  anim_osn_path + "desk_missionary_full_casual_5_2.webp", image =  anim_osn_path + "desk_missionary_full_casual_5_2.webp", group = "office_secretary_naughty")
image anim_osn_desk_missionary_full_casual_6_0 = Movie(play = anim_osn_path + "desk_missionary_full_casual_6_0.webm", start_image =  anim_osn_path + "desk_missionary_full_casual_6_0.webp", image =  anim_osn_path + "desk_missionary_full_casual_6_0.webp", group = "office_secretary_naughty")
image anim_osn_desk_missionary_full_casual_6_1 = Movie(play = anim_osn_path + "desk_missionary_full_casual_6_1.webm", start_image =  anim_osn_path + "desk_missionary_full_casual_6_1.webp", image =  anim_osn_path + "desk_missionary_full_casual_6_1.webp", group = "office_secretary_naughty")
image anim_osn_desk_missionary_full_casual_6_2 = Movie(play = anim_osn_path + "desk_missionary_full_casual_6_2.webm", start_image =  anim_osn_path + "desk_missionary_full_casual_6_2.webp", image =  anim_osn_path + "desk_missionary_full_casual_6_2.webp", group = "office_secretary_naughty")
image anim_osn_desk_missionary_underwear_0 =     Movie(play = anim_osn_path + "desk_missionary_underwear_0.webm",     start_image =  anim_osn_path + "desk_missionary_underwear_0.webp",     image =  anim_osn_path + "desk_missionary_underwear_0.webp",     group = "office_secretary_naughty")
image anim_osn_desk_missionary_underwear_1 =     Movie(play = anim_osn_path + "desk_missionary_underwear_1.webm",     start_image =  anim_osn_path + "desk_missionary_underwear_1.webp",     image =  anim_osn_path + "desk_missionary_underwear_1.webp",     group = "office_secretary_naughty")
image anim_osn_desk_missionary_underwear_2 =     Movie(play = anim_osn_path + "desk_missionary_underwear_2.webm",     start_image =  anim_osn_path + "desk_missionary_underwear_2.webp",     image =  anim_osn_path + "desk_missionary_underwear_2.webp",     group = "office_secretary_naughty")
image anim_osn_desk_missionary_nude_0 =          Movie(play = anim_osn_path + "desk_missionary_nude_0.webm",          start_image =  anim_osn_path + "desk_missionary_nude_0.webp",          image =  anim_osn_path + "desk_missionary_nude_0.webp",          group = "office_secretary_naughty")
image anim_osn_desk_missionary_nude_1 =          Movie(play = anim_osn_path + "desk_missionary_nude_1.webm",          start_image =  anim_osn_path + "desk_missionary_nude_1.webp",          image =  anim_osn_path + "desk_missionary_nude_1.webp",          group = "office_secretary_naughty")
image anim_osn_desk_missionary_nude_2 =          Movie(play = anim_osn_path + "desk_missionary_nude_2.webm",          start_image =  anim_osn_path + "desk_missionary_nude_2.webp",          image =  anim_osn_path + "desk_missionary_nude_2.webp",          group = "office_secretary_naughty")

# desk - doggy
image anim_osn_desk_doggy_full_casual_5_0 = Movie(play = anim_osn_path + "desk_doggy_full_casual_5_0.webm", start_image =  anim_osn_path + "desk_doggy_full_casual_5_0.webp", image =  anim_osn_path + "desk_doggy_full_casual_5_0.webp", group = "office_secretary_naughty")
image anim_osn_desk_doggy_full_casual_5_1 = Movie(play = anim_osn_path + "desk_doggy_full_casual_5_1.webm", start_image =  anim_osn_path + "desk_doggy_full_casual_5_1.webp", image =  anim_osn_path + "desk_doggy_full_casual_5_1.webp", group = "office_secretary_naughty")
image anim_osn_desk_doggy_full_casual_5_2 = Movie(play = anim_osn_path + "desk_doggy_full_casual_5_2.webm", start_image =  anim_osn_path + "desk_doggy_full_casual_5_2.webp", image =  anim_osn_path + "desk_doggy_full_casual_5_2.webp", group = "office_secretary_naughty")
image anim_osn_desk_doggy_full_casual_5_3 = Movie(play = anim_osn_path + "desk_doggy_full_casual_5_3.webm", start_image =  anim_osn_path + "desk_doggy_full_casual_5_3.webp", image =  anim_osn_path + "desk_doggy_full_casual_5_3.webp", group = "office_secretary_naughty")
image anim_osn_desk_doggy_full_casual_6_0 = Movie(play = anim_osn_path + "desk_doggy_full_casual_6_0.webm", start_image =  anim_osn_path + "desk_doggy_full_casual_6_0.webp", image =  anim_osn_path + "desk_doggy_full_casual_6_0.webp", group = "office_secretary_naughty")
image anim_osn_desk_doggy_full_casual_6_1 = Movie(play = anim_osn_path + "desk_doggy_full_casual_6_1.webm", start_image =  anim_osn_path + "desk_doggy_full_casual_6_1.webp", image =  anim_osn_path + "desk_doggy_full_casual_6_1.webp", group = "office_secretary_naughty")
image anim_osn_desk_doggy_full_casual_6_2 = Movie(play = anim_osn_path + "desk_doggy_full_casual_6_2.webm", start_image =  anim_osn_path + "desk_doggy_full_casual_6_2.webp", image =  anim_osn_path + "desk_doggy_full_casual_6_2.webp", group = "office_secretary_naughty")
image anim_osn_desk_doggy_full_casual_6_3 = Movie(play = anim_osn_path + "desk_doggy_full_casual_6_3.webm", start_image =  anim_osn_path + "desk_doggy_full_casual_6_3.webp", image =  anim_osn_path + "desk_doggy_full_casual_6_3.webp", group = "office_secretary_naughty")
image anim_osn_desk_doggy_underwear_0 =     Movie(play = anim_osn_path + "desk_doggy_underwear_0.webm",     start_image =  anim_osn_path + "desk_doggy_underwear_0.webp",     image =  anim_osn_path + "desk_doggy_underwear_0.webp",     group = "office_secretary_naughty")
image anim_osn_desk_doggy_underwear_1 =     Movie(play = anim_osn_path + "desk_doggy_underwear_1.webm",     start_image =  anim_osn_path + "desk_doggy_underwear_1.webp",     image =  anim_osn_path + "desk_doggy_underwear_1.webp",     group = "office_secretary_naughty")
image anim_osn_desk_doggy_underwear_2 =     Movie(play = anim_osn_path + "desk_doggy_underwear_2.webm",     start_image =  anim_osn_path + "desk_doggy_underwear_2.webp",     image =  anim_osn_path + "desk_doggy_underwear_2.webp",     group = "office_secretary_naughty")
image anim_osn_desk_doggy_underwear_3 =     Movie(play = anim_osn_path + "desk_doggy_underwear_3.webm",     start_image =  anim_osn_path + "desk_doggy_underwear_3.webp",     image =  anim_osn_path + "desk_doggy_underwear_3.webp",     group = "office_secretary_naughty")
image anim_osn_desk_doggy_nude_0 =          Movie(play = anim_osn_path + "desk_doggy_nude_0.webm",          start_image =  anim_osn_path + "desk_doggy_nude_0.webp",          image =  anim_osn_path + "desk_doggy_nude_0.webp",          group = "office_secretary_naughty")
image anim_osn_desk_doggy_nude_1 =          Movie(play = anim_osn_path + "desk_doggy_nude_1.webm",          start_image =  anim_osn_path + "desk_doggy_nude_1.webp",          image =  anim_osn_path + "desk_doggy_nude_1.webp",          group = "office_secretary_naughty")
image anim_osn_desk_doggy_nude_2 =          Movie(play = anim_osn_path + "desk_doggy_nude_2.webm",          start_image =  anim_osn_path + "desk_doggy_nude_2.webp",          image =  anim_osn_path + "desk_doggy_nude_2.webp",          group = "office_secretary_naughty")
image anim_osn_desk_doggy_nude_3 =          Movie(play = anim_osn_path + "desk_doggy_nude_3.webm",          start_image =  anim_osn_path + "desk_doggy_nude_3.webp",          image =  anim_osn_path + "desk_doggy_nude_3.webp",          group = "office_secretary_naughty")

# floor - handjob
image anim_osn_floor_handjob_full_casual_5_0 = Movie(play = anim_osn_path + "floor_handjob_full_casual_5_0.webm", start_image =  anim_osn_path + "floor_handjob_full_casual_5_0.webp", image =  anim_osn_path + "floor_handjob_full_casual_5_0.webp", group = "office_secretary_naughty")
image anim_osn_floor_handjob_full_casual_5_1 = Movie(play = anim_osn_path + "floor_handjob_full_casual_5_1.webm", start_image =  anim_osn_path + "floor_handjob_full_casual_5_1.webp", image =  anim_osn_path + "floor_handjob_full_casual_5_1.webp", group = "office_secretary_naughty")
image anim_osn_floor_handjob_full_casual_6_0 = Movie(play = anim_osn_path + "floor_handjob_full_casual_6_0.webm", start_image =  anim_osn_path + "floor_handjob_full_casual_6_0.webp", image =  anim_osn_path + "floor_handjob_full_casual_6_0.webp", group = "office_secretary_naughty")
image anim_osn_floor_handjob_full_casual_6_1 = Movie(play = anim_osn_path + "floor_handjob_full_casual_6_1.webm", start_image =  anim_osn_path + "floor_handjob_full_casual_6_1.webp", image =  anim_osn_path + "floor_handjob_full_casual_6_1.webp", group = "office_secretary_naughty")
image anim_osn_floor_handjob_underwear_0 =     Movie(play = anim_osn_path + "floor_handjob_underwear_0.webm",     start_image =  anim_osn_path + "floor_handjob_underwear_0.webp",     image =  anim_osn_path + "floor_handjob_underwear_0.webp",     group = "office_secretary_naughty")
image anim_osn_floor_handjob_underwear_1 =     Movie(play = anim_osn_path + "floor_handjob_underwear_1.webm",     start_image =  anim_osn_path + "floor_handjob_underwear_1.webp",     image =  anim_osn_path + "floor_handjob_underwear_1.webp",     group = "office_secretary_naughty")
image anim_osn_floor_handjob_nude_0 =          Movie(play = anim_osn_path + "floor_handjob_nude_0.webm",          start_image =  anim_osn_path + "floor_handjob_nude_0.webp",          image =  anim_osn_path + "floor_handjob_nude_0.webp",          group = "office_secretary_naughty")
image anim_osn_floor_handjob_nude_1 =          Movie(play = anim_osn_path + "floor_handjob_nude_1.webm",          start_image =  anim_osn_path + "floor_handjob_nude_1.webp",          image =  anim_osn_path + "floor_handjob_nude_1.webp",          group = "office_secretary_naughty")

# floor - blowjob
image anim_osn_floor_blowjob_full_casual_5_0 = Movie(play = anim_osn_path + "floor_blowjob_full_casual_5_0.webm", start_image =  anim_osn_path + "floor_blowjob_full_casual_5_0.webp", image =  anim_osn_path + "floor_blowjob_full_casual_5_0.webp", group = "office_secretary_naughty")
image anim_osn_floor_blowjob_full_casual_5_1 = Movie(play = anim_osn_path + "floor_blowjob_full_casual_5_1.webm", start_image =  anim_osn_path + "floor_blowjob_full_casual_5_1.webp", image =  anim_osn_path + "floor_blowjob_full_casual_5_1.webp", group = "office_secretary_naughty")
image anim_osn_floor_blowjob_full_casual_5_2 = Movie(play = anim_osn_path + "floor_blowjob_full_casual_5_2.webm", start_image =  anim_osn_path + "floor_blowjob_full_casual_5_2.webp", image =  anim_osn_path + "floor_blowjob_full_casual_5_2.webp", group = "office_secretary_naughty")
image anim_osn_floor_blowjob_full_casual_6_0 = Movie(play = anim_osn_path + "floor_blowjob_full_casual_6_0.webm", start_image =  anim_osn_path + "floor_blowjob_full_casual_6_0.webp", image =  anim_osn_path + "floor_blowjob_full_casual_6_0.webp", group = "office_secretary_naughty")
image anim_osn_floor_blowjob_full_casual_6_1 = Movie(play = anim_osn_path + "floor_blowjob_full_casual_6_1.webm", start_image =  anim_osn_path + "floor_blowjob_full_casual_6_1.webp", image =  anim_osn_path + "floor_blowjob_full_casual_6_1.webp", group = "office_secretary_naughty")
image anim_osn_floor_blowjob_full_casual_6_2 = Movie(play = anim_osn_path + "floor_blowjob_full_casual_6_2.webm", start_image =  anim_osn_path + "floor_blowjob_full_casual_6_2.webp", image =  anim_osn_path + "floor_blowjob_full_casual_6_2.webp", group = "office_secretary_naughty")
image anim_osn_floor_blowjob_underwear_0 =     Movie(play = anim_osn_path + "floor_blowjob_underwear_0.webm",     start_image =  anim_osn_path + "floor_blowjob_underwear_0.webp",     image =  anim_osn_path + "floor_blowjob_underwear_0.webp",     group = "office_secretary_naughty")
image anim_osn_floor_blowjob_underwear_1 =     Movie(play = anim_osn_path + "floor_blowjob_underwear_1.webm",     start_image =  anim_osn_path + "floor_blowjob_underwear_1.webp",     image =  anim_osn_path + "floor_blowjob_underwear_1.webp",     group = "office_secretary_naughty")
image anim_osn_floor_blowjob_underwear_2 =     Movie(play = anim_osn_path + "floor_blowjob_underwear_2.webm",     start_image =  anim_osn_path + "floor_blowjob_underwear_2.webp",     image =  anim_osn_path + "floor_blowjob_underwear_2.webp",     group = "office_secretary_naughty")
image anim_osn_floor_blowjob_nude_0 =          Movie(play = anim_osn_path + "floor_blowjob_nude_0.webm",          start_image =  anim_osn_path + "floor_blowjob_nude_0.webp",          image =  anim_osn_path + "floor_blowjob_nude_0.webp",          group = "office_secretary_naughty")
image anim_osn_floor_blowjob_nude_1 =          Movie(play = anim_osn_path + "floor_blowjob_nude_1.webm",          start_image =  anim_osn_path + "floor_blowjob_nude_1.webp",          image =  anim_osn_path + "floor_blowjob_nude_1.webp",          group = "office_secretary_naughty")
image anim_osn_floor_blowjob_nude_2 =          Movie(play = anim_osn_path + "floor_blowjob_nude_2.webm",          start_image =  anim_osn_path + "floor_blowjob_nude_2.webp",          image =  anim_osn_path + "floor_blowjob_nude_2.webp",          group = "office_secretary_naughty")

# floor - missionary
image anim_osn_floor_missionary_full_casual_5_0 = Movie(play = anim_osn_path + "floor_missionary_full_casual_5_0.webm", start_image =  anim_osn_path + "floor_missionary_full_casual_5_0.webp", image =  anim_osn_path + "floor_missionary_full_casual_5_0.webp", group = "office_secretary_naughty")
image anim_osn_floor_missionary_full_casual_5_1 = Movie(play = anim_osn_path + "floor_missionary_full_casual_5_1.webm", start_image =  anim_osn_path + "floor_missionary_full_casual_5_1.webp", image =  anim_osn_path + "floor_missionary_full_casual_5_1.webp", group = "office_secretary_naughty")
image anim_osn_floor_missionary_full_casual_5_2 = Movie(play = anim_osn_path + "floor_missionary_full_casual_5_2.webm", start_image =  anim_osn_path + "floor_missionary_full_casual_5_2.webp", image =  anim_osn_path + "floor_missionary_full_casual_5_2.webp", group = "office_secretary_naughty")
image anim_osn_floor_missionary_full_casual_6_0 = Movie(play = anim_osn_path + "floor_missionary_full_casual_6_0.webm", start_image =  anim_osn_path + "floor_missionary_full_casual_6_0.webp", image =  anim_osn_path + "floor_missionary_full_casual_6_0.webp", group = "office_secretary_naughty")
image anim_osn_floor_missionary_full_casual_6_1 = Movie(play = anim_osn_path + "floor_missionary_full_casual_6_1.webm", start_image =  anim_osn_path + "floor_missionary_full_casual_6_1.webp", image =  anim_osn_path + "floor_missionary_full_casual_6_1.webp", group = "office_secretary_naughty")
image anim_osn_floor_missionary_full_casual_6_2 = Movie(play = anim_osn_path + "floor_missionary_full_casual_6_2.webm", start_image =  anim_osn_path + "floor_missionary_full_casual_6_2.webp", image =  anim_osn_path + "floor_missionary_full_casual_6_2.webp", group = "office_secretary_naughty")
image anim_osn_floor_missionary_underwear_0 =     Movie(play = anim_osn_path + "floor_missionary_underwear_0.webm",     start_image =  anim_osn_path + "floor_missionary_underwear_0.webp",     image =  anim_osn_path + "floor_missionary_underwear_0.webp",     group = "office_secretary_naughty")
image anim_osn_floor_missionary_underwear_1 =     Movie(play = anim_osn_path + "floor_missionary_underwear_1.webm",     start_image =  anim_osn_path + "floor_missionary_underwear_1.webp",     image =  anim_osn_path + "floor_missionary_underwear_1.webp",     group = "office_secretary_naughty")
image anim_osn_floor_missionary_underwear_2 =     Movie(play = anim_osn_path + "floor_missionary_underwear_2.webm",     start_image =  anim_osn_path + "floor_missionary_underwear_2.webp",     image =  anim_osn_path + "floor_missionary_underwear_2.webp",     group = "office_secretary_naughty")
image anim_osn_floor_missionary_nude_0 =          Movie(play = anim_osn_path + "floor_missionary_nude_0.webm",          start_image =  anim_osn_path + "floor_missionary_nude_0.webp",          image =  anim_osn_path + "floor_missionary_nude_0.webp",          group = "office_secretary_naughty")
image anim_osn_floor_missionary_nude_1 =          Movie(play = anim_osn_path + "floor_missionary_nude_1.webm",          start_image =  anim_osn_path + "floor_missionary_nude_1.webp",          image =  anim_osn_path + "floor_missionary_nude_1.webp",          group = "office_secretary_naughty")
image anim_osn_floor_missionary_nude_2 =          Movie(play = anim_osn_path + "floor_missionary_nude_2.webm",          start_image =  anim_osn_path + "floor_missionary_nude_2.webp",          image =  anim_osn_path + "floor_missionary_nude_2.webp",          group = "office_secretary_naughty")

# floor - cowgirl
image anim_osn_floor_cowgirl_full_casual_5_0 = Movie(play = anim_osn_path + "floor_cowgirl_full_casual_5_0.webm", start_image =  anim_osn_path + "floor_cowgirl_full_casual_5_0.webp", image =  anim_osn_path + "floor_cowgirl_full_casual_5_0.webp", group = "office_secretary_naughty")
image anim_osn_floor_cowgirl_full_casual_5_1 = Movie(play = anim_osn_path + "floor_cowgirl_full_casual_5_1.webm", start_image =  anim_osn_path + "floor_cowgirl_full_casual_5_1.webp", image =  anim_osn_path + "floor_cowgirl_full_casual_5_1.webp", group = "office_secretary_naughty")
image anim_osn_floor_cowgirl_full_casual_5_2 = Movie(play = anim_osn_path + "floor_cowgirl_full_casual_5_2.webm", start_image =  anim_osn_path + "floor_cowgirl_full_casual_5_2.webp", image =  anim_osn_path + "floor_cowgirl_full_casual_5_2.webp", group = "office_secretary_naughty")
image anim_osn_floor_cowgirl_full_casual_6_0 = Movie(play = anim_osn_path + "floor_cowgirl_full_casual_6_0.webm", start_image =  anim_osn_path + "floor_cowgirl_full_casual_6_0.webp", image =  anim_osn_path + "floor_cowgirl_full_casual_6_0.webp", group = "office_secretary_naughty")
image anim_osn_floor_cowgirl_full_casual_6_1 = Movie(play = anim_osn_path + "floor_cowgirl_full_casual_6_1.webm", start_image =  anim_osn_path + "floor_cowgirl_full_casual_6_1.webp", image =  anim_osn_path + "floor_cowgirl_full_casual_6_1.webp", group = "office_secretary_naughty")
image anim_osn_floor_cowgirl_full_casual_6_2 = Movie(play = anim_osn_path + "floor_cowgirl_full_casual_6_2.webm", start_image =  anim_osn_path + "floor_cowgirl_full_casual_6_2.webp", image =  anim_osn_path + "floor_cowgirl_full_casual_6_2.webp", group = "office_secretary_naughty")
image anim_osn_floor_cowgirl_underwear_0 =     Movie(play = anim_osn_path + "floor_cowgirl_underwear_0.webm",     start_image =  anim_osn_path + "floor_cowgirl_underwear_0.webp",     image =  anim_osn_path + "floor_cowgirl_underwear_0.webp",     group = "office_secretary_naughty")
image anim_osn_floor_cowgirl_underwear_1 =     Movie(play = anim_osn_path + "floor_cowgirl_underwear_1.webm",     start_image =  anim_osn_path + "floor_cowgirl_underwear_1.webp",     image =  anim_osn_path + "floor_cowgirl_underwear_1.webp",     group = "office_secretary_naughty")
image anim_osn_floor_cowgirl_underwear_2 =     Movie(play = anim_osn_path + "floor_cowgirl_underwear_2.webm",     start_image =  anim_osn_path + "floor_cowgirl_underwear_2.webp",     image =  anim_osn_path + "floor_cowgirl_underwear_2.webp",     group = "office_secretary_naughty")
image anim_osn_floor_cowgirl_nude_0 =          Movie(play = anim_osn_path + "floor_cowgirl_nude_0.webm",          start_image =  anim_osn_path + "floor_cowgirl_nude_0.webp",          image =  anim_osn_path + "floor_cowgirl_nude_0.webp",          group = "office_secretary_naughty")
image anim_osn_floor_cowgirl_nude_0_cum =      Movie(play = anim_osn_path + "floor_cowgirl_nude_0_cum.webm",      start_image =  anim_osn_path + "floor_cowgirl_nude_0_cum.webp",      image =  anim_osn_path + "floor_cowgirl_nude_0_cum.webp",      group = "office_secretary_naughty")
image anim_osn_floor_cowgirl_nude_0_cum_idle = Movie(play = anim_osn_path + "floor_cowgirl_nude_0_cum_idle.webm", start_image =  anim_osn_path + "floor_cowgirl_nude_0_cum_idle.webp", image =  anim_osn_path + "floor_cowgirl_nude_0_cum_idle.webp", group = "office_secretary_naughty")
image anim_osn_floor_cowgirl_nude_1 =          Movie(play = anim_osn_path + "floor_cowgirl_nude_1.webm",          start_image =  anim_osn_path + "floor_cowgirl_nude_1.webp",          image =  anim_osn_path + "floor_cowgirl_nude_1.webp",          group = "office_secretary_naughty")
image anim_osn_floor_cowgirl_nude_2 =          Movie(play = anim_osn_path + "floor_cowgirl_nude_2.webm",          start_image =  anim_osn_path + "floor_cowgirl_nude_2.webp",          image =  anim_osn_path + "floor_cowgirl_nude_2.webp",          group = "office_secretary_naughty")
label office_call_secretary_naughty_sandbox (**kwargs):
    $ begin_event(**kwargs)

    $ level = get_level('secretary', **kwargs)

    $ image = convert_pattern("main", secretary = level, **kwargs)

    $ image.show(0)
    subtitles "You call the secretary."
    $ image.show(1)
    secretary "Yes, [headmaster_first_name]? How can I help you?"
    $ image.show(2)
    headmaster "Interested in a little fun?"
    $ image.show(3)
    secretary "I'm always up for some fun."
    
    $ naughty_map = {
        'desk': {
            'handjob':    ['full_casual_5', 'full_casual_6', 'underwear', 'nude'],
            'blowjob':    ['full_casual_5', 'full_casual_6', 'underwear', 'nude'],
            'missionary': ['full_casual_5', 'full_casual_6', 'underwear', 'nude'],
            'doggy':      ['full_casual_5', 'full_casual_6', 'underwear', 'nude'],
        },
        'floor': {
            'handjob':    ['full_casual_5', 'full_casual_6', 'underwear', 'nude'],
            'blowjob':    ['full_casual_5', 'full_casual_6', 'underwear', 'nude'],
            'missionary': ['full_casual_5', 'full_casual_6', 'underwear', 'nude'],
            'cowgirl':    ['full_casual_5', 'full_casual_6', 'underwear', 'nude'],
        }
    }

    $ cum_map = {
        'floor': {
            'cowgirl': {
                'nude': 5.333
            }
        }
    }

    call start_sandbox (
        naughty_map = naughty_map,
        cum_map = cum_map,
        level = level,
        file_preset = "images/events/office/office_call_secretary_naughty_sandbox/sandbox/<location>_<position>_<clothing>_<variant>.webm",
        movie_preset = "anim_osn_<location>_<position>_<clothing>_<variant>",
        character = character.secretary,
    **kwargs) from _call_start_sandbox

# endregion
##########################

#########################
# region Regular Events #

label office_event_1 (**kwargs):
    $ begin_event("2", **kwargs);

    $ image = convert_pattern("main", **kwargs)

    $ image.show(0)
    subtitles "You notice a girl sitting in front of the teachers office."

    $ image.show(1)
    subtitles "Apparently she is in need of counseling."

    call change_stats_with_modifier('school',
        happiness = TINY, reputation = TINY) from _call_change_stats_with_modifier_44
    call change_stats_with_modifier('teacher',
        happiness = TINY) from _call_change_stats_with_modifier_45
    
    $ end_event('new_daytime', **kwargs)

label office_event_2 (**kwargs):
    $ begin_event("2", **kwargs);

    $ teacher = get_value("teacher", **kwargs)

    $ show_pattern("main", **kwargs)
    subtitles "Even the teachers need a break from time to time."

    call change_stats_with_modifier('school',
        education = DEC_SMALL, reputation = DEC_TINY) from _call_change_stats_with_modifier_46
    call change_stats_with_modifier('teacher',
        happiness = TINY) from _call_change_stats_with_modifier_47

    $ end_event('new_daytime', **kwargs)

label office_event_3 (**kwargs):
    $ begin_event("2", **kwargs);

    $ yuriko = get_person("class_3a", "yuriko_oshima").get_character()

    $ image = convert_pattern("main", **kwargs)

    $ image.show(0)
    subtitles "You enter the office and see two students sitting there."
    
    $ call_custom_menu(False, 
        MenuElement("Ignore them", "Ignore them", EventEffect("office_event_3.ignore")),
        MenuElement("Ask why they are here", "Ask why they are here", EventEffect("office_event_3.talk")),
    **kwargs)
label .ignore (**kwargs):
    
    $ begin_event(**kwargs)
    
    $ image.show(1)
    subtitles "You ignore them and continue you way."

    call change_stats_with_modifier('teacher',
        happiness = TINY) from _call_change_stats_with_modifier_48

    $ end_event('new_daytime', **kwargs)
label .talk (**kwargs):
    
    $ begin_event(**kwargs)
    
    $ image.show(2)
    headmaster "Why are you sitting here?"
    $ image.show(3)
    yuriko "We were called here by the teacher."
    $ image.show(2)
    headmaster "Do you know why?"
    $ image.show(4)
    yuriko "Probably because we are a couple."

    $ call_custom_menu(False, 
        MenuElement("Tell about policy", "Tell about policy", EventEffect("office_event_3.policy")),
        MenuElement("Take care of it for them", "Take care of it for them", EventEffect("office_event_3.care")),
    **kwargs)
label .policy (**kwargs):
    
    $ begin_event(**kwargs)
    
    $ image.show(5)
    headmaster "Well, you know that relationships between students are not allowed."
    $ image.show(6)
    yuriko "But what does the school care about our relationship?"
    $ image.show(5)
    headmaster "It's a measure to keep you focused on your education."
    headmaster "At least hold yourself back until you are done with school."
    $ image.show(2)
    yuriko "..."
    headmaster "Now you both go back to class."

    call change_stats_with_modifier('school',
        charm = SMALL, happiness = DEC_SMALL) from _call_change_stats_with_modifier_49
    call change_stats_with_modifier('teacher',
        happiness = TINY) from _call_change_stats_with_modifier_50

    $ end_event('new_daytime', **kwargs)
label .care (**kwargs):
    
    $ begin_event(**kwargs)
    
    $ image.show(7)
    headmaster "Okay, listen. You know relationships aren't allowed here at school."
    $ image.show(6)
    yuriko "But..."
    $ image.show(7)
    headmaster "BUT, I don't like this rule either. So I will take care of it for you."
    headmaster "I think I will abandon this rule in the future."
    headmaster "Now go back to class."
    $ image.show(8)
    sgirl "Thank you!"

    $ update_quest("trigger", name = "trigger_unlock_student_relations_1")

    call change_stats_with_modifier('school',
        charm = DEC_SMALL, happiness = MEDIUM, inhibition = DEC_SMALL) from _call_change_stats_with_modifier_51
    call change_stats_with_modifier('teacher',
        happiness = DEC_SMALL) from _call_change_stats_with_modifier_52

    if get_progress("unlock_student_relationship") == -1:
        $ start_progress("unlock_student_relationship")
        $ add_notify_message("Added new rule to journal!")
        
    $ end_event('new_daytime', **kwargs)

label office_event_4 (**kwargs):
    $ begin_event(**kwargs);

    $ image = convert_pattern("main", **kwargs)

    # view of headmaster working and dozing off
    #headmaster wakes up with great view of Emiko's underboobs.
    
    call Image_Series.show_image(image, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9) from _call_show_image_office_event_4_1
    secretary "Ah, [headmaster_first_name]! You're awake!"
    $ image.show(10)
    headmaster "What? Oh, yes. Why am I here?"
    $ image.show(11)
    secretary "I found you sleeping here. You should take a break."
    $ image.show(10)
    headmaster "I'm fine, really."
    $ image.show(11)
    secretary "No, you look exhausted. You need to rest."
    headmaster "..."
    $ image.show(10)
    secretary "Just keep your eyes closed for a while. I'll be here."
    call Image_Series.show_image(image, 8, 7, 6, 5, 12) from _call_show_image_office_event_4_2
    # headmaster dozes off again

    call change_stats_with_modifier('school',
        happiness = SMALL, education = TINY) from _stats_office_event_4_1

    $ end_event('new_daytime', **kwargs)
    

# endregion
#########################

# endregion
#######################################