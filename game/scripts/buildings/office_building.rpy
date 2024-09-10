##############################################
# region Office Building Event Handler ----- #
##############################################

init -1 python:
    set_current_mod('base')
    def office_building_events_available() -> bool:
        return (office_building_timed_event.has_available_highlight_events() or
            office_building_general_event.has_available_highlight_events() or
            any(e.has_available_highlight_events() for e in office_building_events.values()) or
            any(e.has_available_highlight_events() for e in office_building_work_event.values()))

    office_building_timed_event   = TempEventStorage("office_building", "office_building", fallback = Event(2, "office_building.after_time_check"))
    office_building_general_event =     EventStorage("office_building", "office_building", fallback = Event(2, "office_building.after_general_check"))

    office_building_work_event = {}
    add_storage(office_building_work_event, EventStorage("counselling", "office_building"))
    add_storage(office_building_work_event, EventStorage("money",       "office_building"))
    add_storage(office_building_work_event, EventStorage("education",   "office_building"))
    add_storage(office_building_work_event, EventStorage("reputation",  "office_building"))

    office_building_events = {}
    add_storage(office_building_events, EventStorage("look_around",    "office_building"))
    add_storage(office_building_events, EventStorage("work",           "office_building"))
    add_storage(office_building_events, EventStorage("learn",          "office_building", ShowBlockedOption()))
    add_storage(office_building_events, EventStorage("call_secretary", "office_building"))

    office_building_subject_learn_events = {}
    add_storage(office_building_subject_learn_events, EventStorage("math",    "office_building", fallback_text = "There is nobody here."))
    add_storage(office_building_subject_learn_events, EventStorage("history", "office_building", fallback_text = "There is nobody here."))
    add_storage(office_building_subject_learn_events, EventStorage("pe",      "office_building", fallback_text = "There is nobody here."))

    office_building_call_secretary_events = {}
    add_storage(office_building_call_secretary_events, EventStorage("naughty_sandbox", "office_building", fallback_text = "There is nobody here."))

    office_building_bg_images = BGStorage("images/background/office building/bg f.webp",
        RandomListSelector('name', 'teacher', 'secretary'), 
        LevelSelector('level', KwargsValueSelector('', 'name')),
        BGImage("images/background/office building/bg c teacher.webp", 1, AND(TimeCondition(daytime = "c"), ValueCondition('name', 'teacher'))), # show headmasters/teachers office empty
        BGImage("images/background/office building/bg <name> <level> <variant> <nude>.webp", 1, NOT(TimeCondition(daytime = "7"))), # show headmasters/teachers office with people
        BGImage("images/background/office building/bg 7 <name>.webp", 1, TimeCondition(daytime = 7)), # show headmasters/teachers office empty at night
    )

init 1 python: 
    set_current_mod('base')  
    
    office_building_general_event.add_event( 
        Event(1, "first_week_office_building_event",
            IntroCondition(),
            TimeCondition(day = "2-4", month = 1, year = 2023),
            Pattern("main", "images/events/first week/first week office building <step>.webp"),
            thumbnail = "images/events/first week/first week office building 1.webp"),
        
        Event(1, "first_potion_office_building_event",
            IntroCondition(),
            TimeCondition(day = 9, month = 1, year = 2023),
            Pattern("main", "images/events/first potion/first potion office <step>.webp"),
            thumbnail = "images/events/first potion/first potion office 1.webp"),

        Event(2, "action_tutorial",
            NOT(ProgressCondition('action_tutorial')),
            ValueSelector('return_label', 'office_building'),
            NoHighlightOption(),
            TutorialCondition(),
            Pattern("main", "/images/events/misc/action_tutorial <step>.webp"),
            override_location = "misc", thumbnail = "images/events/misc/action_tutorial 0.webp")
    )


    office_building_events["look_around"].add_event(

        Event(3, "office_event_1",
            TimeCondition(weekday = "d", daytime = "f"),
            LevelSelector('school_level', 'school'),
            LevelSelector('teacher_level', 'teacher'),
            Pattern("main", "images/events/office/office_event_1 <school_level> <step>.webp"),
            thumbnail = "images/events/office/office_event_1 1 0.webp"),

        Event(3, "office_event_2",
            RandomListSelector("teacher", "Finola Ryan", "Yulan Chen"),
            TimeCondition(weekday = "d", daytime = "f"),
            LevelSelector('teacher_level', 'teacher'),
            LevelSelector('school_level', 'school'),
            Pattern("main", "images/events/office/office_event_2 <teacher_level> <teacher>.webp"),
            thumbnail = "images/events/office/office_event_2 1 Finola Ryan.webp"),

        Event(3, "office_event_3",
            TimeCondition(weekday = "d", daytime = "d"),
            NOT(RuleCondition("student_student_relation")),
            LevelSelector('school_level', 'school'),
            LevelSelector('teacher_level', 'teacher'),
            Pattern("main", "images/events/office/office_event_3 <school_level> <step>.webp"),
            thumbnail = "images/events/office/office_event_3 1 0.webp"),
    )

    office_call_secretary_event_event = EventSelect(3, "call_secretary_event", "What do you want to do?", office_building_call_secretary_events,
        override_menu_exit = 'office_building',
    )

    office_building_call_secretary_events["naughty_sandbox"].add_event(
        Event(3, "office_call_secretary_naughty_sandbox",
            ProgressCondition("work_office_session_naughty"),
            Pattern("main", "images/events/office/office_call_secretary_naughty_sandbox <secretary> <step>.webp", 'secretary'),
            thumbnail = "images/events/office/office_call_secretary_naughty_sandbox 6 3.webp")
    )
    
        # Event(2, "office_call_secretary_1",
        #     NOT(ProgressCondition('start_sex_ed')),
        #     TimerCondition('start_sex_ed_timer_1', day = 3)),
    office_building_events["call_secretary"].add_event(
        office_call_secretary_event_event,
    )

    office_work_office_event_event = EventSelect(3, "work_office_event", "What do you want to work on?", office_building_work_event,
        TimeCondition(weekday = "d", daytime = "d"),
        override_menu_exit = 'office_building')

    office_building_events["work"].add_event(
        office_work_office_event_event,
    )

    office_building_subject_learn_events['math'].add_event(
        Event(3, "learn_office_event_1", ProficiencyCondition("math", level = "10-"), ValueSelector('subject', 'math')))
    office_building_subject_learn_events['history'].add_event(
        Event(3, "learn_office_event_1", ProficiencyCondition("history", level = "10-"), ValueSelector('subject', 'history')))
    office_building_subject_learn_events['pe'].add_event(
        Event(3, "learn_office_event_1", ProficiencyCondition("pe", level = "10-"), ValueSelector('subject', 'pe')))

    office_building_events["learn"].add_event(EventSelect(3, "learn_subject_event", "What subject do you wanna learn?", office_building_subject_learn_events,
        TimeCondition(daytime = 1),
        MoneyCondition("500+"),
        override_menu_exit = 'office_building'))

    office_building_work_event["money"].add_event(
        Event(3, "work_office_money_event_1",
            TimeCondition(weekday = "d", daytime = "d"),
            Pattern("main", 'images/events/office/office_money_event_1 <step>.webp'),
            thumbnail = "images/events/office/office_money_event_1 1.webp"),
    )

    office_building_work_event["education"].add_event(
        Event(3, "work_office_education_event_1",
            TimeCondition(weekday = "d", daytime = "d"),
            Pattern("main", "images/events/office/office_education_event_1 <step>.webp"),
            thumbnail = "images/events/office/office_education_event_1 0.webp"),
    )

    office_building_work_event["reputation"].add_event(
        Event(3, "work_office_reputation_event_1",
            TimeCondition(weekday = "d", daytime = "d"),
            Pattern("main", "images/events/office/office_reputation_event_1 <step>.webp"),
            thumbnail = "images/events/office/office_reputation_event_1 1.webp"),
    )

    office_building_work_event["counselling"].add_event(
        Event(3, "work_office_session_event_1",
            TimeCondition(weekday = "d", daytime = "d"),
            RandomListSelector("girl_name", "Yuriko Oshima", "Elsie Johnson", "Easkey Tanaka"),
            Pattern("main", "images/events/office/office_session_event_1 <girl_name> <school_level> <secretary_level> <step>.webp", 'girl_name', 'school_level', 'secretary_level'),
            thumbnail = "images/events/office/office_session_event_1 Easkey Tanaka 1 # 4.webp"),
        Event(3, "work_office_session_event_first_naughty",
            TimeCondition(weekday = "d", daytime = "d"),
            LevelSelector('school_level', 'school'),
            LevelSelector('secretary_level', 'secretary'),
            ProgressCondition("counselling sessions", "3+"),
            NOT(ProgressCondition("work_office_session_naughty")),
            Pattern("main", "images/events/office/office_event_first_naughty 0 <step>.webp"),
            thumbnail = "images/events/office/office_event_first_naughty 0 62.webp")
    )

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

#######################################
# region Office Building Events ----- #
#######################################

#######################
# region Intro Events #

label first_potion_office_building_event (**kwargs):
    $ begin_event(**kwargs)
    
    $ image = convert_pattern("main", step_start = 1, **kwargs)

    $ image.show(1)
    subtitles "You enter the teachers office."
    headmaster_thought "Ahh the teacher seem to be eating at the kiosk as well."
    $ image.show(2)
    headmaster_thought "Not that I have a problem with it. Quite the opposite. That makes some things a bit easier."

    $ set_building_blocked("office_building")

    $ end_event('new_daytime', **kwargs)

# first week event
label first_week_office_building_event (**kwargs):
    $ begin_event(**kwargs)
    
    $ show_pattern("main", step_start = 1, **kwargs)
    subtitles "Mhh. The office is nothing special but at least not really run down."
    subtitles "I can work with that."

    $ change_stat("education", 5, get_school())
    $ change_stat_for_all("happiness", 5, charList['staff'])
    $ change_stat_for_all("reputation", 5, charList['staff'])

    $ set_building_blocked("office_building")

    $ end_event('new_day', **kwargs)

# endregion
#######################

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

    $ subject = get_kwargs('subject', **kwargs)

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

    $ girl_first_name, girl_last_name = split_name(girl_name)

    $ image = convert_pattern("main", **kwargs)

    $ image.show(0)
    subtitles_Empty "*Knock* *Knock*"
    $ image.show(1)
    headmaster "Yes?"
    $ image.show(2)
    secretary "[headmaster_first_name], Mrs. [girl_last_name] is here for here counselling session."
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

image anim_office_event_first_naughty_0_16 = Movie(play ="images/events/office/office_event_first_naughty 0 16.webm", start_image = "images/events/office/office_event_first_naughty 0 16.webp", image = "images/events/office/office_event_first_naughty 0 16.webp")
image anim_office_event_first_naughty_0_17 = Movie(play ="images/events/office/office_event_first_naughty 0 17.webm", start_image = "images/events/office/office_event_first_naughty 0 17.webp", image = "images/events/office/office_event_first_naughty 0 17.webp")
image anim_office_event_first_naughty_0_18 = Movie(play ="images/events/office/office_event_first_naughty 0 18.webm", start_image = "images/events/office/office_event_first_naughty 0 18.webp", image = "images/events/office/office_event_first_naughty 0 18.webp")
image anim_office_event_first_naughty_0_21 = Movie(play ="images/events/office/office_event_first_naughty 0 21.webm", start_image = "images/events/office/office_event_first_naughty 0 21.webp", image = "images/events/office/office_event_first_naughty 0 21.webp")
image anim_office_event_first_naughty_0_64 = Movie(play ="images/events/office/office_event_first_naughty 0 64.webm", start_image = "images/events/office/office_event_first_naughty 0 64.webp", image = "images/events/office/office_event_first_naughty 0 64.webp")
image anim_office_event_first_naughty_0_65 = Movie(play ="images/events/office/office_event_first_naughty 0 65.webm", start_image = "images/events/office/office_event_first_naughty 0 65.webp", image = "images/events/office/office_event_first_naughty 0 65.webp")
image anim_office_event_first_naughty_0_66 = Movie(play ="images/events/office/office_event_first_naughty 0 66.webm", start_image = "images/events/office/office_event_first_naughty 0 66.webp", image = "images/events/office/office_event_first_naughty 0 66.webp")
image anim_office_event_first_naughty_0_67 = Movie(play ="images/events/office/office_event_first_naughty 0 67.webm", start_image = "images/events/office/office_event_first_naughty 0 67.webp", image = "images/events/office/office_event_first_naughty 0 67.webp")
image anim_office_event_first_naughty_0_68 = Movie(play ="images/events/office/office_event_first_naughty 0 68.webm", start_image = "images/events/office/office_event_first_naughty 0 68.webp", image = "images/events/office/office_event_first_naughty 0 68.webp")
image anim_office_event_first_naughty_0_69 = Movie(play ="images/events/office/office_event_first_naughty 0 69.webm", start_image = "images/events/office/office_event_first_naughty 0 69.webp", image = "images/events/office/office_event_first_naughty 0 69.webp")
image anim_office_event_first_naughty_0_72 = Movie(play ="images/events/office/office_event_first_naughty 0 72.webm", start_image = "images/events/office/office_event_first_naughty 0 72.webp", image = "images/events/office/office_event_first_naughty 0 72.webp")
image anim_office_event_first_naughty_0_73 = Movie(play ="images/events/office/office_event_first_naughty 0 73.webm", start_image = "images/events/office/office_event_first_naughty 0 73.webp", image = "images/events/office/office_event_first_naughty 0 73.webp")
image anim_office_event_first_naughty_0_74 = Movie(play ="images/events/office/office_event_first_naughty 0 74.webm", start_image = "images/events/office/office_event_first_naughty 0 74.webp", image = "images/events/office/office_event_first_naughty 0 74.webp")
image anim_office_event_first_naughty_0_75 = Movie(play ="images/events/office/office_event_first_naughty 0 75.webm", start_image = "images/events/office/office_event_first_naughty 0 75.webp", image = "images/events/office/office_event_first_naughty 0 75.webp")
label work_office_session_event_first_naughty (**kwargs):
    $ begin_event(**kwargs)

    $ school_level = get_value('school_level', **kwargs)
    $ secretary_level = get_value('secretary_level', **kwargs)

    $ image = convert_pattern("main", **kwargs)

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
    sgirl "Excuse me? Mr. [headmaster_last_name]?" (name = "Yuriko Oshima")
    $ image.show(24)
    headmaster_whisper "Shit! Quick under the desk!"
    call Image_Series.show_image(image, 25, 26) from _call_work_office_session_event_first_naughty_2
    headmaster "Yes come in."
    call Image_Series.show_image(image, 27, 28, 29) from _call_work_office_session_event_first_naughty_3
    headmaster "You're early."
    $ image.show(30)
    sgirl "I apologize for that. Something came up in school and I need to leave earlier. So I thought, I'd come earlier." (name = "Yuriko Oshima")
    $ image.show(31)
    sgirl "I wanted to ask your secretary first but I couldn't find her." (name = "Yuriko Oshima")
    call Image_Series.show_image(image, 32, 40) from _call_work_office_session_event_first_naughty_5
    headmaster "Oh she is probably doing some rounds."
    $ image.show(32)
    headmaster "You're really not able to take the session on the agreed time?"
    $ image.show(33)
    sgirl "I don't think so..." (name = "Yuriko Oshima")
    $ image.show(34)
    headmaster "Alright, then let's do it now. Take a seat."
    call Image_Series.show_image(image, 35, 36, 37, 38) from _call_work_office_session_event_first_naughty_4
    sgirl "Are you okay? You look a bit flushed." (name = "Yuriko Oshima")
    call Image_Series.show_image(image, 39, 40) from _call_work_office_session_event_first_naughty_6
    headmaster "Yes, I'm fine. I just had a bit of a headache. But it's getting better."
    $ image.show(41)
    headmaster "Okay what do you want to talk about today?"

    $ image.show(42)
    sgirl "Well, Mr. [headmaster_last_name], I've been feeling really stressed lately." (name = "Yuriko Oshima")
    $ image.show(43)
    headmaster "I see. Is there something specific that's been bothering you?"
    $ image.show(44)
    sgirl "Yes, it's mainly the pressure to perform well academically. I feel like I'm constantly under scrutiny." (name = "Yuriko Oshima")
    $ image.show(45)
    headmaster "I understand. Academic pressure can be overwhelming. Have you tried talking to your teachers about it?"
    $ image.show(44)
    sgirl "I haven't yet. I guess I'm afraid they won't understand or think I'm just making excuses." (name = "Yuriko Oshima")
    $ image.show(43)
    headmaster "I assure you, Yuriko, your feelings are valid. It's important to communicate your struggles with your teachers so they can support you."
    $ image.show(46)
    sgirl "Thank you, Mr. [headmaster_last_name]. I'll try to gather the courage to talk to them." (name = "Yuriko Oshima")
    $ image.show(47)
    headmaster "That's a good step forward. Remember, you're not alone in this. We're here to help you succeed."
    $ image.show(43)
    headmaster "If it is too difficult for you to talk to your teachers, how about your friends? Maybe they can help you."
    $ image.show(44)
    sgirl "It's... It's quite hard. I don't really have friends. I have Ellie, but I fear bothering her too much with my problems." (name = "Yuriko Oshima")
    $ image.show(48)
    headmaster "Ellie?"
    $ image.show(42)
    sgirl "Yes, Elsie Johnson. She's in my class. She's really nice and I really like her. But I don't want to be a burden to her." (name = "Yuriko Oshima")
    $ image.show(45)
    headmaster "I see. It's important to have someone to talk to. Maybe you can try to open up to her."
    $ image.show(43)
    headmaster "It's always good to be able to talk to someone you're close to."
    $ image.show(49)
    headmaster "I'll be always here to help yoaaaaaah!"
    # emiko starts handling your rod again
    $ image.show(50)
    sgirl "Sir, is everything okay?" (name = "Yuriko Oshima")
    $ image.show(51)
    headmaster "*cough* *cough* Yes, everything is fine. I just swallowed wrong."
    $ image.show(52)
    headmaster "What I wanted to say is that you can always come to me if you need help but you understand that it is difficult in my position to provide a level of intimacy that you might need."
    $ image.show(50)
    sgirl "Intimacy?" (name = "Yuriko Oshima")
    # emiko grins at you and then continues
    $ image.show(40)
    pause

    $ image.show(52)
    headmaster "Yes! You know humans don't work very well when being alone. We need to be close to others to feel good."
    $ image.show(53)
    headmaster "It even isn't really enough to just have people you know around you. You need to have people you trust. A sort of intimate bonding."
    headmaster "Even physical contact plays an important role in that. It's a way to show that you care about someone."
    $ image.show(54)
    sgirl "Physical contact? I don't think I can go that far..." (name = "Yuriko Oshima") # Yuriko blushes
    $ image.show(55)
    headmaster "Don't misunderstand. Even hugging someone can be a form of physical contact. It's not always about a sexual relationship."
    $ image.show(56)
    headmaster "Even though having sex can be the closest form of intimacy. But it's not the only one and that is not what I meant in this case."
    headmaster "That is why you really should try to talk to Elsie about your problems, your feelings and your fears. She might be able to help you."
    $ image.show(55)
    headmaster "How about you do that, and the next time we talk about how it went? Would that be okay for you?"
    $ image.show(57)
    sgirl "Yes, I think I can do that. Thank you, Mr. [headmaster_last_name]." (name = "Yuriko Oshima")
    $ image.show(56)
    headmaster "You're welcome, Yuriko. Now I think that settles it for today. I hope I could help you a bit."
    $ image.show(46)
    sgirl "Yes, you did. Thank you." (name = "Yuriko Oshima")
    $ image.show(56)
    headmaster "Thank you for entrusting yourself to me."
    headmaster "I have a lot to do, so unfortunately I can't accompany you to the door. So please just close the door behind you."
    $ image.show(31)
    sgirl "Will do. Thank you." (name = "Yuriko Oshima")
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

##############################
# region Sex Ed Introduction #

label office_call_secretary_1 (**kwargs):
    $ begin_event(**kwargs)

    subtitles "You call the secretary."
    secretary "Hello, [headmaster_first_name]. How can I help you?"
    headmaster "I need your opinion on something."
    secretary "Sure, what is it?"
    headmaster "I'm thinking of introducing sex education classes in the curriculum. What do you think?"
    secretary "I think it's a great idea. It's important for students to be educated about such topics."
    secretary "But do you think the rest of the staff and also the students would agree?"
    headmaster "Hmm, I guess you're right. That will be quite the hurdle, I think I need to make sure they are ready for it before suggesting it."
    headmaster "Do you have any suggestions on how to approach this?"
    secretary "I think you should start by talking to the staff and getting their input."
    secretary "To actually convince them, you could prepare some teaching material and introductory material on the subject."
    secretary "That way they can see what you have in mind and how you plan to approach it."
    headmaster "That's a good idea. Thank you for your input."
    secretary "You're welcome. Is there anything else?"
    headmaster "No, that's all. Thank you."
    secretary "You're welcome. Have a nice day."
    headmaster_thought "Then, maybe I should start work on some teaching material for the sex ed classes."

    $ start_progress('start_sex_ed') # 0 -> 1

    $ end_event('new_daytime', **kwargs)

label office_teacher_sex_ed_introduction_1(**kwargs):
    $ begin_event(**kwargs)

    headmaster_thought "Hmm, now how do I start this."
    headmaster_thought "My main problem is that the teacher will have reservations about introducing sex ed classes."
    headmaster_thought "So the best way to overcome this, would be to show them the importance of it."
    headmaster_thought "I should talk to each one of them and present them the effects of not giving the students proper sexual education."
    headmaster_thought "If I can relate to them in their own expertise, I guess that would be even better."
    headmaster_thought "But first I should meet up with them and find out what they think in general about the idea of introducing sex ed classes"

    headmaster "Emiko?"
    secretary "Yes, [headmaster_first_name]?"
    headmaster "Can you please schedule a meeting with all the teachers for tomorrow?"
    secretary "Sure, I'll take care of it. At what time?"
    headmaster "First thing in the morning. I want to discuss the introduction of the sex ed classes with them."
    secretary "Got it. I'll send out the invites right away."
    headmaster "Thank you, Emiko."

    $ advance_progress('start_sex_ed') # 1 -> 2

    $ end_event('new_daytime', **kwargs)

label office_teacher_sex_ed_introduction_2 (**kwargs):
    $ begin_event(**kwargs)

    $ finola = Character("Finola Ryan",   kind = character.teacher)
    $ chloe  = Character("Chloe Garcia",  kind = character.teacher)
    $ lily   = Character("Lily Anderson", kind = character.teacher)
    $ yulan  = Character("Yulan Chen",    kind = character.teacher)
    $ zoe    = Character("Zoe Parker",    kind = character.teacher)

    headmaster "I thank you all for coming on such short notice."
    headmaster "Since I became the new headmaster, I was closely observing the school and the students."
    headmaster "The school is nothing short but disappointing and the students and their achievements are a direct image of that."
    headmaster "But what shocked me most was the social behaviour of the students."
    headmaster "The students are surprisingly tame. But when it comes to their behaviour related to their bodies and looks, they are quite the opposite."
    headmaster "I heard of bullying and exclusion towards certain students because of their looks or their overall body form."
    headmaster "I think that this is a direct result of the lack of proper sexual education."
    headmaster "The students became too ignorant. I think they simply don't know why bodies are different and why they are changing."
    headmaster "So they did what most people do when they don't understand something. They fear it. And in conclusion they bully or fight it."
    headmaster "I think that we need to change that. We need to educate the students about their bodies and the bodies of others."
    headmaster "And for that reason I plan to add Sexual Education to the schools curriculum."
    
    finola "I disagree. I believe that sexual education is not something that should be taught in school. It is a private matter between adults!"

    headmaster "I appreciate your concerns, but we cannot ignore the fact that our students are going through puberty and they need to know how their bodies work."
    headmaster "We will provide them with accurate information about sex and relationships without promoting any particular sexual orientation or gender identity."

    chloe "But what if some of our students get too excited during the lessons? It's completely inappropriate!"

    headmaster "I agree that we need to be sensitive to their emotions, but I am certain that this will only enhance their understanding of sexuality and relationships."
    headmaster "Our research on other schools that have implemented similar programmes has shown that they have seen positive results in terms of decreased rates of teen pregnancy, STIs and sexual assault."

    lily "But it'll make our students more promiscuous!"

    headmaster "That's a common misconception about sex education. Research has shown that teaching young people about sexual health can actually prevent them from engaging in risky behaviour."
    headmaster "We can empower our students to make informed decisions about their bodies and relationships by providing accurate information and setting clear boundaries."

    yulan "We have to consider the possibility that some students won't be interested. I want to know if they will be forced to attend these classes."

    headmaster "Yes. This subject will be added to the normal curriculum. This is a topic that simply cannot be made optional."
    headmaster "It is our duty to provide all students with accurate information so that they can make informed choices about their bodies and relationships."

    zoe "I'm not fully convinced. But what if some students don't listen and still engage in risky behaviour?"

    headmaster "That's a valid concern, but we will provide them with accurate information so that they can make informed choices about their bodies."
    headmaster "If they choose to engage in risky behaviour despite this knowledge, they will have to take responsibility for their actions."
    headmaster "We will do our best to provide them with the necessary tools and resources."

    headmaster "I understand that this is a sensitive topic, but I believe that it is our responsibility to provide our students with the knowledge and skills they need to make informed decisions about their bodies and relationships."
    headmaster "We are running out of time, so I have a proposal."
    headmaster "I will work out a plan for the introduction of the new subject."
    headmaster "I'll include the specific topics that will be covered, the teaching methods that will be used, and the resources that will be available to the students."

    headmaster "I will then present this plan to you all for your feedback and suggestions."
    headmaster "I want to make sure that we are all on the same page and that we can move forward together."

    finola "I still have my doubts, but I'm willing to give it a chance."
    chloe "Yeah, let's see what you come up with."

    headmaster "Thank you all for your time. I'll keep you updated on the progress."

    $ add_notify_message("Added new rule to journal!")

    $ advance_progress('start_sex_ed') # 2 -> 3

    $ end_event('new_daytime')

label office_teacher_sex_ed_introduction_3 (**kwargs):
    $ begin_event(**kwargs)

    headmaster_thought "Now let's start working on the information material for the teachers. This needs to be perfect, so the teachers will be convinced."
    headmaster_thought "So what do I need to include in the material?"
    headmaster_thought "I think I should start with the basics. What is sexual education and why is it important?"
    headmaster_thought "Add some case studies and statistics to show the impact of sexual education on students."
    headmaster_thought "And maybe some examples of how other schools have successfully implemented sexual education programs."
    headmaster_thought "Then continue with the topics that will be covered in the classes and the teaching methods that will be used."
    headmaster_thought "That will include the resources that will be available to the students and the teachers."
    headmaster_thought "And finally, I should include a section on how the teachers can support the students and answer their questions."
    headmaster_thought "I think that should cover everything. Now I just need to put it all together."
    call screen black_screen_text("1h later.")
    headmaster_thought "Now that's done. I think I should present it to the teachers and get their feedback."
    
    $ advance_progress('start_sex_ed')

    $ end_event('new_daytime', **kwargs)

label office_teacher_sex_ed_introduction_4 (**kwargs):
    $ begin_event(**kwargs)

    $ finola = Character("Finola Ryan",   kind = character.teacher)
    $ chloe  = Character("Chloe Garcia",  kind = character.teacher)
    $ lily   = Character("Lily Anderson", kind = character.teacher)
    $ yulan  = Character("Yulan Chen",    kind = character.teacher)
    $ zoe    = Character("Zoe Parker",    kind = character.teacher)

    headmaster "Good morning, teachers. Today, I would like to present to you the importance of sexual education and the comprehensive program we are planning to implement."
    headmaster "I understand that there may be concerns and reservations about introducing this topic, but I believe it is crucial for the well-being and development of our students."
    headmaster "Let's start with the basics. What is sexual education and why is it important?"

    $ call_custom_menu_with_text("Do you want to read the entire presentation?", character.subtitles, False,
        ("Read full presentation", "office_teacher_sex_ed_introduction_4.presentation"),
        ("Skip presentation", "office_teacher_sex_ed_introduction_4.skipped_presentation"), 
    **kwargs)

label .presentation (**kwargs):
    headmaster "Sexual education is a comprehensive program that provides students with accurate and age-appropriate information about human sexuality, relationships, and reproductive health."
    headmaster "Now, you may wonder why it is important. Well, it equips students with the knowledge and skills they need to make informed decisions about their bodies, relationships, and sexual health."
    headmaster "Without proper sexual education, students may rely on misinformation or peer pressure, which can lead to risky behaviors and negative consequences."
    headmaster "But by providing accurate information, we can empower our students to develop healthy attitudes towards their bodies and relationships."
    headmaster "Now, let's dive deeper. Allow me to share some case studies and statistics to address your concerns and demonstrate the potential benefits of sexual education."
    headmaster "Research has shown that comprehensive sexual education programs can have a positive impact on students' knowledge, attitudes, and behaviors."
    headmaster "For example, a study conducted by XYZ University found that schools with comprehensive sexual education programs had lower rates of teen pregnancy and sexually transmitted infections (STIs)."
    headmaster "Another study by ABC Institute showed that students who received sexual education were more likely to delay sexual activity and use contraception when they did become sexually active."
    headmaster "These case studies and statistics demonstrate the effectiveness of sexual education in promoting healthy behaviors and reducing negative outcomes."
    headmaster "Now, let's take a look at some successful implementations of sexual education programs in other schools."
    headmaster "I understand that you may have concerns about how this program will be implemented. However, there are many schools across the country that have successfully introduced sexual education programs."
    headmaster "For instance, XYZ High School in Cityville implemented a comprehensive sexual education curriculum that included interactive classroom activities, guest speakers, and access to resources."
    headmaster "They reported positive outcomes such as increased knowledge, improved communication skills, and reduced rates of teen pregnancy and STIs."
    headmaster "By sharing these success stories, I hope to address your concerns and show that sexual education can make a positive difference in students' lives."
    headmaster "Now, let's move on to the topics that will be covered in the classes and the teaching methods that will be used."
    headmaster "I understand that you may have questions about the content and teaching methods. The sexual education classes will cover a range of topics, including but not limited to: human anatomy and reproductive systems, consent and healthy relationships, contraception and STI prevention, gender and sexual orientation, and communication skills."
    headmaster "As for the teaching methods, they will be interactive and engaging, incorporating a variety of strategies such as group discussions, role-playing, multimedia presentations, and guest speakers."
    headmaster "These methods will ensure that students actively participate in their learning and have opportunities to ask questions and share their perspectives."
    headmaster "Now, let's talk about the resources that will be available to both the students and the teachers."
    headmaster "I understand that you may have concerns about the resources and support available. Given our narrow budget, we will make the most of the limited resources we have to support students' learning."
    headmaster "While we may not have access to extensive textbooks or online materials, we will ensure that the information provided is accurate and age-appropriate."
    headmaster "In addition, we will collaborate with local health organizations and community centers to provide guest speakers and workshops on sexual education."
    headmaster "Furthermore, we have plans to renovate our school library to provide students with a comfortable space for learning and research."
    headmaster "The renovated library will be equipped with a variety of resources, including books, magazines, and reference materials."
    headmaster "We will also create dedicated areas for studying and quiet reading to enhance the learning environment."
    headmaster "By improving our library facilities, we aim to encourage students to utilize this valuable resource for their academic needs."
    headmaster "As for teacher support, we will explore free online training programs and workshops to enhance your knowledge and skills in delivering sexual education effectively."
    headmaster "Your dedication and creativity in delivering the curriculum will be crucial in overcoming the resource limitations."
    headmaster "Lastly, I would like to emphasize the importance of your role as teachers in creating a safe and inclusive learning environment for students to discuss sensitive topics related to sexual education."
    headmaster "Your support and guidance will be instrumental in addressing their concerns and providing accurate information, even with limited resources."

    call .end_presentation (**kwargs) from call_end_presentation_sex_ed_intro_1
label .skipped_presentation (**kwargs):

    call screen black_screen_text("30 Minutes later.")

    call .end_presentation (**kwargs) from call_end_presentation_sex_ed_intro_2
label .end_presentation (**kwargs):

    headmaster "By working together and making the most of what we have, we can ensure that our students receive the necessary knowledge and skills to make informed decisions and navigate their sexual health and relationships."
    headmaster "Thank you for your attention. I hope that this presentation has addressed some of your concerns and that we can move forward together in implementing comprehensive sexual education."
    
    finola "Thank you for the presentation, Headmaster. I can see the potential benefits of sexual education, but I would like some time to think about it and discuss it with my colleagues."
    chloe "I agree. It's an important topic, but we need to consider the concerns of parents and the community as well. Perhaps you could bring it up at the next PTA meeting and gather more feedback."
    lily "I appreciate the effort you've put into this presentation, Headmaster. However, I think it would be beneficial to involve parents in the decision-making process. Let's discuss it further at the next PTA meeting."
    yulan "I'm impressed with the research and success stories you've shared, Headmaster. However, I believe it's important to address any potential backlash or resistance from parents. Let's bring it up at the next PTA meeting and have a thorough discussion."
    zoe "Thank you for the detailed presentation, Headmaster. I can see the value of sexual education, but I think it's important to involve parents and the students in the decision-making process. Let's discuss it further at the next PTA meeting."

    headmaster "Thank you for your feedback. That will be all for today then."
    headmaster "I wish you all a good day and we'll see each other at the next PTA meeting."
    
    # headmaster returns to office, secretary enters

    secretary "[headmaster_first_name], how did the presentation go?"
    headmaster "It went well. The teachers had some concerns, but I think we're on the right track."
    headmaster "I probably just need to guide their thoughts in the right direction for them to support me at the pta meeting."
    headmaster "I don't expect much opposition from the student council, so I think we're good."
    headmaster "The parents should be no problem when the teachers and students agree to the change."

    $ advance_progress('start_sex_ed')

    $ end_event('new_daytime', **kwargs)

# endregion
##############################

##########################
# region Naughty Sandbox #

# desk - handjob
image anim_office_secretary_desk_handjob_full_casual_5_0 = Movie(play ="images/events/office/anim_office_secretary_desk_handjob_full_casual_5_0.webm", start_image = "images/events/office/anim_office_secretary_desk_handjob_full_casual_5_0.webp", image = "images/events/office/anim_office_secretary_desk_handjob_full_casual_5_0.webp")
image anim_office_secretary_desk_handjob_full_casual_5_1 = Movie(play ="images/events/office/anim_office_secretary_desk_handjob_full_casual_5_1.webm", start_image = "images/events/office/anim_office_secretary_desk_handjob_full_casual_5_1.webp", image = "images/events/office/anim_office_secretary_desk_handjob_full_casual_5_1.webp")
image anim_office_secretary_desk_handjob_full_casual_5_2 = Movie(play ="images/events/office/anim_office_secretary_desk_handjob_full_casual_5_2.webm", start_image = "images/events/office/anim_office_secretary_desk_handjob_full_casual_5_2.webp", image = "images/events/office/anim_office_secretary_desk_handjob_full_casual_5_2.webp")
image anim_office_secretary_desk_handjob_full_casual_6_0 = Movie(play ="images/events/office/anim_office_secretary_desk_handjob_full_casual_6_0.webm", start_image = "images/events/office/anim_office_secretary_desk_handjob_full_casual_6_0.webp", image = "images/events/office/anim_office_secretary_desk_handjob_full_casual_6_0.webp")
image anim_office_secretary_desk_handjob_full_casual_6_1 = Movie(play ="images/events/office/anim_office_secretary_desk_handjob_full_casual_6_1.webm", start_image = "images/events/office/anim_office_secretary_desk_handjob_full_casual_6_1.webp", image = "images/events/office/anim_office_secretary_desk_handjob_full_casual_6_1.webp")
image anim_office_secretary_desk_handjob_full_casual_6_2 = Movie(play ="images/events/office/anim_office_secretary_desk_handjob_full_casual_6_2.webm", start_image = "images/events/office/anim_office_secretary_desk_handjob_full_casual_6_2.webp", image = "images/events/office/anim_office_secretary_desk_handjob_full_casual_6_2.webp")
image anim_office_secretary_desk_handjob_underwear_0 = Movie(play ="images/events/office/anim_office_secretary_desk_handjob_underwear_0.webm", start_image = "images/events/office/anim_office_secretary_desk_handjob_underwear_0.webp", image = "images/events/office/anim_office_secretary_desk_handjob_underwear_0.webp")
image anim_office_secretary_desk_handjob_underwear_1 = Movie(play ="images/events/office/anim_office_secretary_desk_handjob_underwear_1.webm", start_image = "images/events/office/anim_office_secretary_desk_handjob_underwear_1.webp", image = "images/events/office/anim_office_secretary_desk_handjob_underwear_1.webp")
image anim_office_secretary_desk_handjob_underwear_2 = Movie(play ="images/events/office/anim_office_secretary_desk_handjob_underwear_2.webm", start_image = "images/events/office/anim_office_secretary_desk_handjob_underwear_2.webp", image = "images/events/office/anim_office_secretary_desk_handjob_underwear_2.webp")
image anim_office_secretary_desk_handjob_nude_0 = Movie(play ="images/events/office/anim_office_secretary_desk_handjob_nude_0.webm", start_image = "images/events/office/anim_office_secretary_desk_handjob_nude_0.webp", image = "images/events/office/anim_office_secretary_desk_handjob_nude_0.webp")
image anim_office_secretary_desk_handjob_nude_1 = Movie(play ="images/events/office/anim_office_secretary_desk_handjob_nude_1.webm", start_image = "images/events/office/anim_office_secretary_desk_handjob_nude_1.webp", image = "images/events/office/anim_office_secretary_desk_handjob_nude_1.webp")
image anim_office_secretary_desk_handjob_nude_2 = Movie(play ="images/events/office/anim_office_secretary_desk_handjob_nude_2.webm", start_image = "images/events/office/anim_office_secretary_desk_handjob_nude_2.webp", image = "images/events/office/anim_office_secretary_desk_handjob_nude_2.webp")

# desk - blowjob
image anim_office_secretary_desk_blowjob_full_casual_5_0 = Movie(play ="images/events/office/anim_office_secretary_desk_blowjob_full_casual_5_0.webm", start_image = "images/events/office/anim_office_secretary_desk_blowjob_full_casual_5_0.webp", image = "images/events/office/anim_office_secretary_desk_blowjob_full_casual_5_0.webp")
image anim_office_secretary_desk_blowjob_full_casual_5_1 = Movie(play ="images/events/office/anim_office_secretary_desk_blowjob_full_casual_5_1.webm", start_image = "images/events/office/anim_office_secretary_desk_blowjob_full_casual_5_1.webp", image = "images/events/office/anim_office_secretary_desk_blowjob_full_casual_5_1.webp")
image anim_office_secretary_desk_blowjob_full_casual_5_2 = Movie(play ="images/events/office/anim_office_secretary_desk_blowjob_full_casual_5_2.webm", start_image = "images/events/office/anim_office_secretary_desk_blowjob_full_casual_5_2.webp", image = "images/events/office/anim_office_secretary_desk_blowjob_full_casual_5_2.webp")
image anim_office_secretary_desk_blowjob_full_casual_5_3 = Movie(play ="images/events/office/anim_office_secretary_desk_blowjob_full_casual_5_3.webm", start_image = "images/events/office/anim_office_secretary_desk_blowjob_full_casual_5_3.webp", image = "images/events/office/anim_office_secretary_desk_blowjob_full_casual_5_3.webp")
image anim_office_secretary_desk_blowjob_full_casual_6_0 = Movie(play ="images/events/office/anim_office_secretary_desk_blowjob_full_casual_6_0.webm", start_image = "images/events/office/anim_office_secretary_desk_blowjob_full_casual_6_0.webp", image = "images/events/office/anim_office_secretary_desk_blowjob_full_casual_6_0.webp")
image anim_office_secretary_desk_blowjob_full_casual_6_1 = Movie(play ="images/events/office/anim_office_secretary_desk_blowjob_full_casual_6_1.webm", start_image = "images/events/office/anim_office_secretary_desk_blowjob_full_casual_6_1.webp", image = "images/events/office/anim_office_secretary_desk_blowjob_full_casual_6_1.webp")
image anim_office_secretary_desk_blowjob_full_casual_6_2 = Movie(play ="images/events/office/anim_office_secretary_desk_blowjob_full_casual_6_2.webm", start_image = "images/events/office/anim_office_secretary_desk_blowjob_full_casual_6_2.webp", image = "images/events/office/anim_office_secretary_desk_blowjob_full_casual_6_2.webp")
image anim_office_secretary_desk_blowjob_full_casual_6_3 = Movie(play ="images/events/office/anim_office_secretary_desk_blowjob_full_casual_6_3.webm", start_image = "images/events/office/anim_office_secretary_desk_blowjob_full_casual_6_3.webp", image = "images/events/office/anim_office_secretary_desk_blowjob_full_casual_6_3.webp")
image anim_office_secretary_desk_blowjob_underwear_0 = Movie(play ="images/events/office/anim_office_secretary_desk_blowjob_underwear_0.webm", start_image = "images/events/office/anim_office_secretary_desk_blowjob_underwear_0.webp", image = "images/events/office/anim_office_secretary_desk_blowjob_underwear_0.webp")
image anim_office_secretary_desk_blowjob_underwear_1 = Movie(play ="images/events/office/anim_office_secretary_desk_blowjob_underwear_1.webm", start_image = "images/events/office/anim_office_secretary_desk_blowjob_underwear_1.webp", image = "images/events/office/anim_office_secretary_desk_blowjob_underwear_1.webp")
image anim_office_secretary_desk_blowjob_underwear_2 = Movie(play ="images/events/office/anim_office_secretary_desk_blowjob_underwear_2.webm", start_image = "images/events/office/anim_office_secretary_desk_blowjob_underwear_2.webp", image = "images/events/office/anim_office_secretary_desk_blowjob_underwear_2.webp")
image anim_office_secretary_desk_blowjob_underwear_3 = Movie(play ="images/events/office/anim_office_secretary_desk_blowjob_underwear_3.webm", start_image = "images/events/office/anim_office_secretary_desk_blowjob_underwear_3.webp", image = "images/events/office/anim_office_secretary_desk_blowjob_underwear_3.webp")
image anim_office_secretary_desk_blowjob_nude_0 = Movie(play ="images/events/office/anim_office_secretary_desk_blowjob_nude_0.webm", start_image = "images/events/office/anim_office_secretary_desk_blowjob_nude_0.webp", image = "images/events/office/anim_office_secretary_desk_blowjob_nude_0.webp")
image anim_office_secretary_desk_blowjob_nude_1 = Movie(play ="images/events/office/anim_office_secretary_desk_blowjob_nude_1.webm", start_image = "images/events/office/anim_office_secretary_desk_blowjob_nude_1.webp", image = "images/events/office/anim_office_secretary_desk_blowjob_nude_1.webp")
image anim_office_secretary_desk_blowjob_nude_2 = Movie(play ="images/events/office/anim_office_secretary_desk_blowjob_nude_2.webm", start_image = "images/events/office/anim_office_secretary_desk_blowjob_nude_2.webp", image = "images/events/office/anim_office_secretary_desk_blowjob_nude_2.webp")
image anim_office_secretary_desk_blowjob_nude_3 = Movie(play ="images/events/office/anim_office_secretary_desk_blowjob_nude_3.webm", start_image = "images/events/office/anim_office_secretary_desk_blowjob_nude_3.webp", image = "images/events/office/anim_office_secretary_desk_blowjob_nude_3.webp")

# desk - missionary
image anim_office_secretary_desk_missionary_full_casual_5_0 = Movie(play ="images/events/office/anim_office_secretary_desk_missionary_full_casual_5_0.webm", start_image = "images/events/office/anim_office_secretary_desk_missionary_full_casual_5_0.webp", image = "images/events/office/anim_office_secretary_desk_missionary_full_casual_5_0.webp")
image anim_office_secretary_desk_missionary_full_casual_5_1 = Movie(play ="images/events/office/anim_office_secretary_desk_missionary_full_casual_5_1.webm", start_image = "images/events/office/anim_office_secretary_desk_missionary_full_casual_5_1.webp", image = "images/events/office/anim_office_secretary_desk_missionary_full_casual_5_1.webp")
image anim_office_secretary_desk_missionary_full_casual_5_2 = Movie(play ="images/events/office/anim_office_secretary_desk_missionary_full_casual_5_2.webm", start_image = "images/events/office/anim_office_secretary_desk_missionary_full_casual_5_2.webp", image = "images/events/office/anim_office_secretary_desk_missionary_full_casual_5_2.webp")
image anim_office_secretary_desk_missionary_full_casual_6_0 = Movie(play ="images/events/office/anim_office_secretary_desk_missionary_full_casual_6_0.webm", start_image = "images/events/office/anim_office_secretary_desk_missionary_full_casual_6_0.webp", image = "images/events/office/anim_office_secretary_desk_missionary_full_casual_6_0.webp")
image anim_office_secretary_desk_missionary_full_casual_6_1 = Movie(play ="images/events/office/anim_office_secretary_desk_missionary_full_casual_6_1.webm", start_image = "images/events/office/anim_office_secretary_desk_missionary_full_casual_6_1.webp", image = "images/events/office/anim_office_secretary_desk_missionary_full_casual_6_1.webp")
image anim_office_secretary_desk_missionary_full_casual_6_2 = Movie(play ="images/events/office/anim_office_secretary_desk_missionary_full_casual_6_2.webm", start_image = "images/events/office/anim_office_secretary_desk_missionary_full_casual_6_2.webp", image = "images/events/office/anim_office_secretary_desk_missionary_full_casual_6_2.webp")
image anim_office_secretary_desk_missionary_underwear_0 = Movie(play ="images/events/office/anim_office_secretary_desk_missionary_underwear_0.webm", start_image = "images/events/office/anim_office_secretary_desk_missionary_underwear_0.webp", image = "images/events/office/anim_office_secretary_desk_missionary_underwear_0.webp")
image anim_office_secretary_desk_missionary_underwear_1 = Movie(play ="images/events/office/anim_office_secretary_desk_missionary_underwear_1.webm", start_image = "images/events/office/anim_office_secretary_desk_missionary_underwear_1.webp", image = "images/events/office/anim_office_secretary_desk_missionary_underwear_1.webp")
image anim_office_secretary_desk_missionary_underwear_2 = Movie(play ="images/events/office/anim_office_secretary_desk_missionary_underwear_2.webm", start_image = "images/events/office/anim_office_secretary_desk_missionary_underwear_2.webp", image = "images/events/office/anim_office_secretary_desk_missionary_underwear_2.webp")
image anim_office_secretary_desk_missionary_nude_0 = Movie(play ="images/events/office/anim_office_secretary_desk_missionary_nude_0.webm", start_image = "images/events/office/anim_office_secretary_desk_missionary_nude_0.webp", image = "images/events/office/anim_office_secretary_desk_missionary_nude_0.webp")
image anim_office_secretary_desk_missionary_nude_1 = Movie(play ="images/events/office/anim_office_secretary_desk_missionary_nude_1.webm", start_image = "images/events/office/anim_office_secretary_desk_missionary_nude_1.webp", image = "images/events/office/anim_office_secretary_desk_missionary_nude_1.webp")
image anim_office_secretary_desk_missionary_nude_2 = Movie(play ="images/events/office/anim_office_secretary_desk_missionary_nude_2.webm", start_image = "images/events/office/anim_office_secretary_desk_missionary_nude_2.webp", image = "images/events/office/anim_office_secretary_desk_missionary_nude_2.webp")

# desk - doggy
image anim_office_secretary_desk_doggy_full_casual_5_0 = Movie(play ="images/events/office/anim_office_secretary_desk_doggy_full_casual_5_0.webm", start_image = "images/events/office/anim_office_secretary_desk_doggy_full_casual_5_0.webp", image = "images/events/office/anim_office_secretary_desk_doggy_full_casual_5_0.webp")
image anim_office_secretary_desk_doggy_full_casual_5_1 = Movie(play ="images/events/office/anim_office_secretary_desk_doggy_full_casual_5_1.webm", start_image = "images/events/office/anim_office_secretary_desk_doggy_full_casual_5_1.webp", image = "images/events/office/anim_office_secretary_desk_doggy_full_casual_5_1.webp")
image anim_office_secretary_desk_doggy_full_casual_5_2 = Movie(play ="images/events/office/anim_office_secretary_desk_doggy_full_casual_5_2.webm", start_image = "images/events/office/anim_office_secretary_desk_doggy_full_casual_5_2.webp", image = "images/events/office/anim_office_secretary_desk_doggy_full_casual_5_2.webp")
image anim_office_secretary_desk_doggy_full_casual_5_3 = Movie(play ="images/events/office/anim_office_secretary_desk_doggy_full_casual_5_3.webm", start_image = "images/events/office/anim_office_secretary_desk_doggy_full_casual_5_3.webp", image = "images/events/office/anim_office_secretary_desk_doggy_full_casual_5_3.webp")
image anim_office_secretary_desk_doggy_full_casual_6_0 = Movie(play ="images/events/office/anim_office_secretary_desk_doggy_full_casual_6_0.webm", start_image = "images/events/office/anim_office_secretary_desk_doggy_full_casual_6_0.webp", image = "images/events/office/anim_office_secretary_desk_doggy_full_casual_6_0.webp")
image anim_office_secretary_desk_doggy_full_casual_6_1 = Movie(play ="images/events/office/anim_office_secretary_desk_doggy_full_casual_6_1.webm", start_image = "images/events/office/anim_office_secretary_desk_doggy_full_casual_6_1.webp", image = "images/events/office/anim_office_secretary_desk_doggy_full_casual_6_1.webp")
image anim_office_secretary_desk_doggy_full_casual_6_2 = Movie(play ="images/events/office/anim_office_secretary_desk_doggy_full_casual_6_2.webm", start_image = "images/events/office/anim_office_secretary_desk_doggy_full_casual_6_2.webp", image = "images/events/office/anim_office_secretary_desk_doggy_full_casual_6_2.webp")
image anim_office_secretary_desk_doggy_full_casual_6_3 = Movie(play ="images/events/office/anim_office_secretary_desk_doggy_full_casual_6_3.webm", start_image = "images/events/office/anim_office_secretary_desk_doggy_full_casual_6_3.webp", image = "images/events/office/anim_office_secretary_desk_doggy_full_casual_6_3.webp")
image anim_office_secretary_desk_doggy_underwear_0 = Movie(play ="images/events/office/anim_office_secretary_desk_doggy_underwear_0.webm", start_image = "images/events/office/anim_office_secretary_desk_doggy_underwear_0.webp", image = "images/events/office/anim_office_secretary_desk_doggy_underwear_0.webp")
image anim_office_secretary_desk_doggy_underwear_1 = Movie(play ="images/events/office/anim_office_secretary_desk_doggy_underwear_1.webm", start_image = "images/events/office/anim_office_secretary_desk_doggy_underwear_1.webp", image = "images/events/office/anim_office_secretary_desk_doggy_underwear_1.webp")
image anim_office_secretary_desk_doggy_underwear_2 = Movie(play ="images/events/office/anim_office_secretary_desk_doggy_underwear_2.webm", start_image = "images/events/office/anim_office_secretary_desk_doggy_underwear_2.webp", image = "images/events/office/anim_office_secretary_desk_doggy_underwear_2.webp")
image anim_office_secretary_desk_doggy_underwear_3 = Movie(play ="images/events/office/anim_office_secretary_desk_doggy_underwear_3.webm", start_image = "images/events/office/anim_office_secretary_desk_doggy_underwear_3.webp", image = "images/events/office/anim_office_secretary_desk_doggy_underwear_3.webp")
image anim_office_secretary_desk_doggy_nude_0 = Movie(play ="images/events/office/anim_office_secretary_desk_doggy_nude_0.webm", start_image = "images/events/office/anim_office_secretary_desk_doggy_nude_0.webp", image = "images/events/office/anim_office_secretary_desk_doggy_nude_0.webp")
image anim_office_secretary_desk_doggy_nude_1 = Movie(play ="images/events/office/anim_office_secretary_desk_doggy_nude_1.webm", start_image = "images/events/office/anim_office_secretary_desk_doggy_nude_1.webp", image = "images/events/office/anim_office_secretary_desk_doggy_nude_1.webp")
image anim_office_secretary_desk_doggy_nude_2 = Movie(play ="images/events/office/anim_office_secretary_desk_doggy_nude_2.webm", start_image = "images/events/office/anim_office_secretary_desk_doggy_nude_2.webp", image = "images/events/office/anim_office_secretary_desk_doggy_nude_2.webp")
image anim_office_secretary_desk_doggy_nude_3 = Movie(play ="images/events/office/anim_office_secretary_desk_doggy_nude_3.webm", start_image = "images/events/office/anim_office_secretary_desk_doggy_nude_3.webp", image = "images/events/office/anim_office_secretary_desk_doggy_nude_3.webp")

# floor - handjob
image anim_office_secretary_floor_handjob_full_casual_5_0 = Movie(play ="images/events/office/anim_office_secretary_floor_handjob_full_casual_5_0.webm", start_image = "images/events/office/anim_office_secretary_floor_handjob_full_casual_5_0.webp", image = "images/events/office/anim_office_secretary_floor_handjob_full_casual_5_0.webp")
image anim_office_secretary_floor_handjob_full_casual_5_1 = Movie(play ="images/events/office/anim_office_secretary_floor_handjob_full_casual_5_1.webm", start_image = "images/events/office/anim_office_secretary_floor_handjob_full_casual_5_1.webp", image = "images/events/office/anim_office_secretary_floor_handjob_full_casual_5_1.webp")
image anim_office_secretary_floor_handjob_full_casual_6_0 = Movie(play ="images/events/office/anim_office_secretary_floor_handjob_full_casual_6_0.webm", start_image = "images/events/office/anim_office_secretary_floor_handjob_full_casual_6_0.webp", image = "images/events/office/anim_office_secretary_floor_handjob_full_casual_6_0.webp")
image anim_office_secretary_floor_handjob_full_casual_6_1 = Movie(play ="images/events/office/anim_office_secretary_floor_handjob_full_casual_6_1.webm", start_image = "images/events/office/anim_office_secretary_floor_handjob_full_casual_6_1.webp", image = "images/events/office/anim_office_secretary_floor_handjob_full_casual_6_1.webp")
image anim_office_secretary_floor_handjob_underwear_0 = Movie(play ="images/events/office/anim_office_secretary_floor_handjob_underwear_0.webm", start_image = "images/events/office/anim_office_secretary_floor_handjob_underwear_0.webp", image = "images/events/office/anim_office_secretary_floor_handjob_underwear_0.webp")
image anim_office_secretary_floor_handjob_underwear_1 = Movie(play ="images/events/office/anim_office_secretary_floor_handjob_underwear_1.webm", start_image = "images/events/office/anim_office_secretary_floor_handjob_underwear_1.webp", image = "images/events/office/anim_office_secretary_floor_handjob_underwear_1.webp")
image anim_office_secretary_floor_handjob_nude_0 = Movie(play ="images/events/office/anim_office_secretary_floor_handjob_nude_0.webm", start_image = "images/events/office/anim_office_secretary_floor_handjob_nude_0.webp", image = "images/events/office/anim_office_secretary_floor_handjob_nude_0.webp")
image anim_office_secretary_floor_handjob_nude_1 = Movie(play ="images/events/office/anim_office_secretary_floor_handjob_nude_1.webm", start_image = "images/events/office/anim_office_secretary_floor_handjob_nude_1.webp", image = "images/events/office/anim_office_secretary_floor_handjob_nude_1.webp")

# floor - blowjob
image anim_office_secretary_floor_blowjob_full_casual_5_0 = Movie(play ="images/events/office/anim_office_secretary_floor_blowjob_full_casual_5_0.webm", start_image = "images/events/office/anim_office_secretary_floor_blowjob_full_casual_5_0.webp", image = "images/events/office/anim_office_secretary_floor_blowjob_full_casual_5_0.webp")
image anim_office_secretary_floor_blowjob_full_casual_5_1 = Movie(play ="images/events/office/anim_office_secretary_floor_blowjob_full_casual_5_1.webm", start_image = "images/events/office/anim_office_secretary_floor_blowjob_full_casual_5_1.webp", image = "images/events/office/anim_office_secretary_floor_blowjob_full_casual_5_1.webp")
image anim_office_secretary_floor_blowjob_full_casual_5_2 = Movie(play ="images/events/office/anim_office_secretary_floor_blowjob_full_casual_5_2.webm", start_image = "images/events/office/anim_office_secretary_floor_blowjob_full_casual_5_2.webp", image = "images/events/office/anim_office_secretary_floor_blowjob_full_casual_5_2.webp")
image anim_office_secretary_floor_blowjob_full_casual_6_0 = Movie(play ="images/events/office/anim_office_secretary_floor_blowjob_full_casual_6_0.webm", start_image = "images/events/office/anim_office_secretary_floor_blowjob_full_casual_6_0.webp", image = "images/events/office/anim_office_secretary_floor_blowjob_full_casual_6_0.webp")
image anim_office_secretary_floor_blowjob_full_casual_6_1 = Movie(play ="images/events/office/anim_office_secretary_floor_blowjob_full_casual_6_1.webm", start_image = "images/events/office/anim_office_secretary_floor_blowjob_full_casual_6_1.webp", image = "images/events/office/anim_office_secretary_floor_blowjob_full_casual_6_1.webp")
image anim_office_secretary_floor_blowjob_full_casual_6_2 = Movie(play ="images/events/office/anim_office_secretary_floor_blowjob_full_casual_6_2.webm", start_image = "images/events/office/anim_office_secretary_floor_blowjob_full_casual_6_2.webp", image = "images/events/office/anim_office_secretary_floor_blowjob_full_casual_6_2.webp")
image anim_office_secretary_floor_blowjob_underwear_0 = Movie(play ="images/events/office/anim_office_secretary_floor_blowjob_underwear_0.webm", start_image = "images/events/office/anim_office_secretary_floor_blowjob_underwear_0.webp", image = "images/events/office/anim_office_secretary_floor_blowjob_underwear_0.webp")
image anim_office_secretary_floor_blowjob_underwear_1 = Movie(play ="images/events/office/anim_office_secretary_floor_blowjob_underwear_1.webm", start_image = "images/events/office/anim_office_secretary_floor_blowjob_underwear_1.webp", image = "images/events/office/anim_office_secretary_floor_blowjob_underwear_1.webp")
image anim_office_secretary_floor_blowjob_underwear_2 = Movie(play ="images/events/office/anim_office_secretary_floor_blowjob_underwear_2.webm", start_image = "images/events/office/anim_office_secretary_floor_blowjob_underwear_2.webp", image = "images/events/office/anim_office_secretary_floor_blowjob_underwear_2.webp")
image anim_office_secretary_floor_blowjob_nude_0 = Movie(play ="images/events/office/anim_office_secretary_floor_blowjob_nude_0.webm", start_image = "images/events/office/anim_office_secretary_floor_blowjob_nude_0.webp", image = "images/events/office/anim_office_secretary_floor_blowjob_nude_0.webp")
image anim_office_secretary_floor_blowjob_nude_1 = Movie(play ="images/events/office/anim_office_secretary_floor_blowjob_nude_1.webm", start_image = "images/events/office/anim_office_secretary_floor_blowjob_nude_1.webp", image = "images/events/office/anim_office_secretary_floor_blowjob_nude_1.webp")
image anim_office_secretary_floor_blowjob_nude_2 = Movie(play ="images/events/office/anim_office_secretary_floor_blowjob_nude_2.webm", start_image = "images/events/office/anim_office_secretary_floor_blowjob_nude_2.webp", image = "images/events/office/anim_office_secretary_floor_blowjob_nude_2.webp")

# floor - missionary
image anim_office_secretary_floor_missionary_full_casual_5_0 = Movie(play ="images/events/office/anim_office_secretary_floor_missionary_full_casual_5_0.webm", start_image = "images/events/office/anim_office_secretary_floor_missionary_full_casual_5_0.webp", image = "images/events/office/anim_office_secretary_floor_missionary_full_casual_5_0.webp")
image anim_office_secretary_floor_missionary_full_casual_5_1 = Movie(play ="images/events/office/anim_office_secretary_floor_missionary_full_casual_5_1.webm", start_image = "images/events/office/anim_office_secretary_floor_missionary_full_casual_5_1.webp", image = "images/events/office/anim_office_secretary_floor_missionary_full_casual_5_1.webp")
image anim_office_secretary_floor_missionary_full_casual_5_2 = Movie(play ="images/events/office/anim_office_secretary_floor_missionary_full_casual_5_2.webm", start_image = "images/events/office/anim_office_secretary_floor_missionary_full_casual_5_2.webp", image = "images/events/office/anim_office_secretary_floor_missionary_full_casual_5_2.webp")
image anim_office_secretary_floor_missionary_full_casual_6_0 = Movie(play ="images/events/office/anim_office_secretary_floor_missionary_full_casual_6_0.webm", start_image = "images/events/office/anim_office_secretary_floor_missionary_full_casual_6_0.webp", image = "images/events/office/anim_office_secretary_floor_missionary_full_casual_6_0.webp")
image anim_office_secretary_floor_missionary_full_casual_6_1 = Movie(play ="images/events/office/anim_office_secretary_floor_missionary_full_casual_6_1.webm", start_image = "images/events/office/anim_office_secretary_floor_missionary_full_casual_6_1.webp", image = "images/events/office/anim_office_secretary_floor_missionary_full_casual_6_1.webp")
image anim_office_secretary_floor_missionary_full_casual_6_2 = Movie(play ="images/events/office/anim_office_secretary_floor_missionary_full_casual_6_2.webm", start_image = "images/events/office/anim_office_secretary_floor_missionary_full_casual_6_2.webp", image = "images/events/office/anim_office_secretary_floor_missionary_full_casual_6_2.webp")
image anim_office_secretary_floor_missionary_underwear_0 = Movie(play ="images/events/office/anim_office_secretary_floor_missionary_underwear_0.webm", start_image = "images/events/office/anim_office_secretary_floor_missionary_underwear_0.webp", image = "images/events/office/anim_office_secretary_floor_missionary_underwear_0.webp")
image anim_office_secretary_floor_missionary_underwear_1 = Movie(play ="images/events/office/anim_office_secretary_floor_missionary_underwear_1.webm", start_image = "images/events/office/anim_office_secretary_floor_missionary_underwear_1.webp", image = "images/events/office/anim_office_secretary_floor_missionary_underwear_1.webp")
image anim_office_secretary_floor_missionary_underwear_2 = Movie(play ="images/events/office/anim_office_secretary_floor_missionary_underwear_2.webm", start_image = "images/events/office/anim_office_secretary_floor_missionary_underwear_2.webp", image = "images/events/office/anim_office_secretary_floor_missionary_underwear_2.webp")
image anim_office_secretary_floor_missionary_nude_0 = Movie(play ="images/events/office/anim_office_secretary_floor_missionary_nude_0.webm", start_image = "images/events/office/anim_office_secretary_floor_missionary_nude_0.webp", image = "images/events/office/anim_office_secretary_floor_missionary_nude_0.webp")
image anim_office_secretary_floor_missionary_nude_1 = Movie(play ="images/events/office/anim_office_secretary_floor_missionary_nude_1.webm", start_image = "images/events/office/anim_office_secretary_floor_missionary_nude_1.webp", image = "images/events/office/anim_office_secretary_floor_missionary_nude_1.webp")
image anim_office_secretary_floor_missionary_nude_2 = Movie(play ="images/events/office/anim_office_secretary_floor_missionary_nude_2.webm", start_image = "images/events/office/anim_office_secretary_floor_missionary_nude_2.webp", image = "images/events/office/anim_office_secretary_floor_missionary_nude_2.webp")

# floor - cowgirl
image anim_office_secretary_floor_cowgirl_full_casual_5_0 = Movie(play ="images/events/office/anim_office_secretary_floor_cowgirl_full_casual_5_0.webm", start_image = "images/events/office/anim_office_secretary_floor_cowgirl_full_casual_5_0.webp", image = "images/events/office/anim_office_secretary_floor_cowgirl_full_casual_5_0.webp")
image anim_office_secretary_floor_cowgirl_full_casual_5_1 = Movie(play ="images/events/office/anim_office_secretary_floor_cowgirl_full_casual_5_1.webm", start_image = "images/events/office/anim_office_secretary_floor_cowgirl_full_casual_5_1.webp", image = "images/events/office/anim_office_secretary_floor_cowgirl_full_casual_5_1.webp")
image anim_office_secretary_floor_cowgirl_full_casual_5_2 = Movie(play ="images/events/office/anim_office_secretary_floor_cowgirl_full_casual_5_2.webm", start_image = "images/events/office/anim_office_secretary_floor_cowgirl_full_casual_5_2.webp", image = "images/events/office/anim_office_secretary_floor_cowgirl_full_casual_5_2.webp")
image anim_office_secretary_floor_cowgirl_full_casual_6_0 = Movie(play ="images/events/office/anim_office_secretary_floor_cowgirl_full_casual_6_0.webm", start_image = "images/events/office/anim_office_secretary_floor_cowgirl_full_casual_6_0.webp", image = "images/events/office/anim_office_secretary_floor_cowgirl_full_casual_6_0.webp")
image anim_office_secretary_floor_cowgirl_full_casual_6_1 = Movie(play ="images/events/office/anim_office_secretary_floor_cowgirl_full_casual_6_1.webm", start_image = "images/events/office/anim_office_secretary_floor_cowgirl_full_casual_6_1.webp", image = "images/events/office/anim_office_secretary_floor_cowgirl_full_casual_6_1.webp")
image anim_office_secretary_floor_cowgirl_full_casual_6_2 = Movie(play ="images/events/office/anim_office_secretary_floor_cowgirl_full_casual_6_2.webm", start_image = "images/events/office/anim_office_secretary_floor_cowgirl_full_casual_6_2.webp", image = "images/events/office/anim_office_secretary_floor_cowgirl_full_casual_6_2.webp")
image anim_office_secretary_floor_cowgirl_underwear_0 = Movie(play ="images/events/office/anim_office_secretary_floor_cowgirl_underwear_0.webm", start_image = "images/events/office/anim_office_secretary_floor_cowgirl_underwear_0.webp", image = "images/events/office/anim_office_secretary_floor_cowgirl_underwear_0.webp")
image anim_office_secretary_floor_cowgirl_underwear_1 = Movie(play ="images/events/office/anim_office_secretary_floor_cowgirl_underwear_1.webm", start_image = "images/events/office/anim_office_secretary_floor_cowgirl_underwear_1.webp", image = "images/events/office/anim_office_secretary_floor_cowgirl_underwear_1.webp")
image anim_office_secretary_floor_cowgirl_underwear_2 = Movie(play ="images/events/office/anim_office_secretary_floor_cowgirl_underwear_2.webm", start_image = "images/events/office/anim_office_secretary_floor_cowgirl_underwear_2.webp", image = "images/events/office/anim_office_secretary_floor_cowgirl_underwear_2.webp")
image anim_office_secretary_floor_cowgirl_nude_0 = Movie(play ="images/events/office/anim_office_secretary_floor_cowgirl_nude_0.webm", start_image = "images/events/office/anim_office_secretary_floor_cowgirl_nude_0.webp", image = "images/events/office/anim_office_secretary_floor_cowgirl_nude_0.webp")
image anim_office_secretary_floor_cowgirl_nude_1 = Movie(play ="images/events/office/anim_office_secretary_floor_cowgirl_nude_1.webm", start_image = "images/events/office/anim_office_secretary_floor_cowgirl_nude_1.webp", image = "images/events/office/anim_office_secretary_floor_cowgirl_nude_1.webp")
image anim_office_secretary_floor_cowgirl_nude_2 = Movie(play ="images/events/office/anim_office_secretary_floor_cowgirl_nude_2.webm", start_image = "images/events/office/anim_office_secretary_floor_cowgirl_nude_2.webp", image = "images/events/office/anim_office_secretary_floor_cowgirl_nude_2.webp")
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

    call start_sandbox (
        naughty_map = naughty_map,
        level = level,
        file_preset = "images/events/office/anim_office_secretary_<location>_<position>_<clothing>_<variant>.webm",
        movie_preset = "anim_office_secretary_<location>_<position>_<clothing>_<variant>",
        character = character.secretary,
    **kwargs) from _call_start_sandbox

# endregion
##########################

#########################
# region Regular Events #

label office_event_1 (**kwargs):
    $ begin_event(**kwargs);

    $ school_level = get_value('school_level', **kwargs)
    $ teacher_level = get_value('teacher_level', **kwargs)

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
    $ begin_event(**kwargs);

    $ teacher_level = get_value('teacher_level', **kwargs)
    $ school_level = get_value('school_level', **kwargs)
    $ teacher = get_value("teacher", **kwargs)

    $ show_pattern("main", **kwargs)
    subtitles "Even the teachers need a break from time to time."

    call change_stats_with_modifier('school',
        education = DEC_SMALL, reputation = DEC_TINY) from _call_change_stats_with_modifier_46
    call change_stats_with_modifier('teacher',
        happiness = TINY) from _call_change_stats_with_modifier_47

    $ end_event('new_daytime', **kwargs)

label office_event_3 (**kwargs):
    $ begin_event(**kwargs);

    $ school_level = get_value('school_level', **kwargs)
    $ teacher_level = get_value('teacher_level', **kwargs)

    $ image = convert_pattern("main", **kwargs)

    $ image.show(0)
    subtitles "You enter the office and see two students sitting there."
    
    $ call_custom_menu(False, 
        ("Ignore them", "office_event_3.ignore"),
        ("Ask why they are here", "office_event_3.talk"),
    **kwargs)
label .ignore (**kwargs):
    
    $ begin_event()
    
    $ image.show(1)
    subtitles "You ignore them and continue you way."

    call change_stats_with_modifier('teacher',
        happiness = TINY) from _call_change_stats_with_modifier_48

    $ end_event('new_daytime', **kwargs)
label .talk (**kwargs):
    
    $ begin_event()
    
    $ image.show(2)
    headmaster "Why are you sitting here?"
    $ image.show(3)
    sgirl "We were called here by the teacher."
    $ image.show(2)
    headmaster "Do you know why?"
    $ image.show(4)
    sgirl "Probably because we are a couple."

    $ call_custom_menu(False, 
        ("Tell about policy", "office_event_3.policy"),
        ("Take care of it for them", "office_event_3.care"),
    **kwargs)
label .policy (**kwargs):
    
    $ begin_event()
    
    $ image.show(5)
    headmaster "Well, you know that relationships between students are not allowed."
    $ image.show(6)
    sgirl "But what does the school care about our relationship?"
    $ image.show(5)
    headmaster "It's a measure to keep you focused on your education."
    headmaster "At least hold yourself back until you are done with school."
    $ image.show(2)
    sgirl "..."
    headmaster "Now you both go back to class."

    call change_stats_with_modifier('school',
        charm = SMALL, happiness = DEC_SMALL) from _call_change_stats_with_modifier_49
    call change_stats_with_modifier('teacher',
        happiness = TINY) from _call_change_stats_with_modifier_50

    $ end_event('new_daytime', **kwargs)
label .care (**kwargs):
    
    $ begin_event()
    
    $ image.show(7)
    headmaster "Okay, listen. You know relationships aren't allowed here at school."
    $ image.show(6)
    sgirl "But..."
    $ image.show(7)
    headmaster "BUT, I don't like this rule either. So I will take care of it for you."
    headmaster "I think I will abandon this rule in the future."
    headmaster "Now go back to class."
    $ image.show(8)
    sgirl "Thank you!"

    call change_stats_with_modifier('school',
        charm = DEC_SMALL, happiness = MEDIUM, inhibition = DEC_SMALL) from _call_change_stats_with_modifier_51
    call change_stats_with_modifier('teacher',
        happiness = DEC_SMALL) from _call_change_stats_with_modifier_52

    if get_progress("unlock_student_relationship") == -1:
        $ start_progress("unlock_student_relationship")
        $ add_notify_message("Added new rule to journal!")
        
    $ end_event('new_daytime', **kwargs)

# endregion
#########################

# endregion
#######################################