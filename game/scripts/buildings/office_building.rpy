#############################################
# ----- Office Building Event Handler ----- #
#############################################

init -1 python:
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

    office_building_bg_images = BGStorage("images/background/office building/bg f.webp",
        BGImage("images/background/office building/bg c teacher.webp", 1, TimeCondition(daytime = "c"), ValueCondition('name', 'teacher')), # show headmasters/teachers office empty
        BGImage("images/background/office building/bg c secretary <secretary_level> <nude>.webp", 1, TimeCondition(daytime = "c"), ValueCondition('name', 'secretary')), # show headmasters/teachers office with people
        BGImage("images/background/office building/bg f <name> <level> <nude>.webp", 1, TimeCondition(daytime = "f")), # show headmasters/teachers office with people
        BGImage("images/background/office building/bg 7 <name>.webp", 1, TimeCondition(daytime = 7)), # show headmasters/teachers office empty at night
    )

init 1 python:   
    office_building_general_event.add_event( 
        Event(1, "first_week_office_building_event",
            IntroCondition(),
            TimeCondition(day = "2-4", month = 1, year = 2023),
            thumbnail = "images/events/first week/first week office building 1.webp"),
        
        Event(1, "first_potion_office_building_event",
            IntroCondition(),
            TimeCondition(day = 9, month = 1, year = 2023),
            thumbnail = "images/events/first potion/first potion office 1.webp"),
    )


    office_building_events["look_around"].add_event(

        Event(3, "office_event_1",
            TimeCondition(weekday = "d", daytime = "f"),
            LevelSelector('school_level', 'school'),
            LevelSelector('teacher_level', 'teacher'),
            thumbnail = "images/events/office/office_event_1 1 0.webp"),

        Event(3, "office_event_2",
            RandomListSelector("teacher", "Finola Ryan", "Yulan Chen"),
            TimeCondition(weekday = "d", daytime = "f"),
            LevelSelector('teacher_level', 'teacher'),
            LevelSelector('school_level', 'school'),
            thumbnail = "images/events/office/office_event_2 1 Finola Ryan.webp"),

        Event(3, "office_event_3",
            TimeCondition(weekday = "d", daytime = "d"),
            NOT(RuleCondition("student_student_relation")),
            LevelSelector('school_level', 'school'),
            LevelSelector('teacher_level', 'teacher'),
            thumbnail = "images/events/office/office_event_3 1 0.webp"),
    )

    office_building_events["call_secretary"].add_event(
        Event(2, "office_call_secretary_1",
            NOT(ProgressCondition('start_sex_ed')),
            TimerCondition('start_sex_ed_timer_1', day = 3))
    )
    
    office_work_office_event_event = EventSelect(3, "work_office_event", "What do you want to work on?", office_building_work_event,
        TimeCondition(weekday = "d", daytime = "d"),
        override_menu_exit = 'office_building',
    )

    office_building_events["work"].add_event(
        office_work_office_event_event,
    )

    office_building_events["learn"].add_event(EventSelect(3, "learn_subject_event", "What subject do you wanna learn?", office_building_subject_learn_events,
        TimeCondition(daytime = 1),
        MoneyCondition("5000+"),
        override_menu_exit = 'office_building',
    ))

    office_building_work_event["money"].add_event(
        Event(3, "work_office_money_event_1",
            TimeCondition(weekday = "d", daytime = "d")),
    )

    office_building_work_event["education"].add_event(
        Event(3, "work_office_education_event_1",
            TimeCondition(weekday = "d", daytime = "d")),
    )

    office_building_work_event["reputation"].add_event(
        Event(3, "work_office_reputation_event_1",
            TimeCondition(weekday = "d", daytime = "d")),
    )

    office_building_work_event["counselling"].add_event(
        Event(3, "work_office_session_event_1",
            TimeCondition(weekday = "d", daytime = "d"),
            RandomListSelector("girl_name", "Yuriko Oshima", "Elsie Johnson", "Easkey Tanaka")),
        Event(3, "work_office_session_event_first_naughty",
            TimeCondition(weekday = "d", daytime = "d"),
            LevelSelector('school_level', 'school'),
            LevelSelector('secretary_level', 'secretary'),
            ProgressCondition("counselling sessions", "3+"),
            NOT(ProgressCondition("work_office_session_naughty")),
        )
    )

#############################################

###########################################
# ----- Office Building Entry Point ----- #
###########################################

label office_building ():
    call call_available_event(office_building_timed_event) from office_building_1

label .after_time_check (**kwargs):
    call call_available_event(office_building_general_event) from office_building_4

label .after_general_check (**kwargs):
    $ char = get_random_choice("teacher", "secretary")
    $ office_building_bg_images.add_kwargs(
        name = char,
        level = get_character_by_key(char).get_level(),
    )

    call call_event_menu (
        "Hello Headmaster! How can I help you?" if char == "secretary" else "What do you do?", 
        office_building_events, 
        default_fallback,
        character.secretary if char == "secretary" else character.subtitles,
        bg_image = office_building_bg_images,
        context = char,
    ) from office_building_3

    jump office_building

###########################################

###########################################
# ----- High School Building Events ----- #
###########################################

label first_potion_office_building_event (**kwargs):
    $ begin_event(**kwargs)
    
    show first potion office 1 with dissolveM
    subtitles "You enter the teachers office."
    headmaster_thought "Ahh the teacher seem to be eating at the kiosk as well."
    show first potion office 2 with dissolveM
    headmaster_thought "Not that I have a problem with it. Quite the opposite. That makes some things a bit easier."

    $ set_building_blocked("office_building")

    $ end_event('new_daytime', **kwargs)

# first week event
label first_week_office_building_event (**kwargs):
    $ begin_event(**kwargs)
    
    show first week office building 1 with dissolveM
    subtitles "Mhh. The office is nothing special but at least not really run down."
    subtitles "I can work with that."

    $ change_stat("education", 5, get_school())
    $ change_stat_for_all("happiness", 5, charList['staff'])
    $ change_stat_for_all("reputation", 5, charList['staff'])

    $ set_building_blocked("office_building")

    $ end_event('new_day', **kwargs)

label work_office_reputation_event_1 (**kwargs):
    $ begin_event(**kwargs)

    $ image = Image_Series("images/events/office/office_reputation_event_1 <step>.webp", **kwargs)

    $ image.show(0)
    subtitles "You decided to to some PR work, trying to improve the schools and your reputation."
    show screen black_screen_text("1h later.")
    $ image.show(1)
    headmaster_thought "I think I found a way to make the school more appealing to the public."
    $ image.show(2)
    headmaster_thought "I hope this will help to improve the reputation of the school."

    call change_stats_with_modifier('school', reputation = SMALL)

    $ end_event('new_daytime', **kwargs)

label work_office_money_event_1 (**kwargs):
    $ begin_event(**kwargs)

    $ image = Image_Series('images/events/office/office_money_event_1 <step>.webp', **kwargs)

    $ image.show(0)
    subtitles "You work on checking the accounts of the school."
    show screen black_screen_text("1h later.")
    # headmaster is consumed by the terrible accounting done in the past
    $ image.show(1)
    headmaster_thought "How can this be? This is a mess!"
    headmaster_thought "I need to get this sorted out."
    headmaster_thought "There is so much wrong with these accounts. It's gonna take ages to fix this."
    $ image.show(2)
    headmaster_thought "At least I was able to find some money that was lost in the system."

    call change_money_with_modifier(get_random_int(100, 500))

    $ end_event('new_daytime', **kwargs)

label work_office_education_event_1 (**kwargs):
    $ begin_event(**kwargs)

    $ image = Image_Series("images/events/office/office_education_event_1 <step>.webp", **kwargs)

    $ image.show(0)
    subtitles "You work on optimizing the teaching material for the students."
    show screen black_screen_text("1h later.")
    $ image.show(1)
    headmaster_thought "I think I found a way to make the material more interesting for the students."

    call change_stats_with_modifier('school',
        education = SMALL, happiness = TINY)
    call change_stats_with_modifier('teacher',
        happiness = SMALL, education = SMALL)

    $ end_event('new_daytime', **kwargs)

image anim_work_office_session_event_first_naughty_1  = Movie(play ="images/events/office/office_event_first_naughty 0 16.webm", start_image = "images/events/office/office_event_first_naughty 0 16.webp", image = "images/events/office/office_event_first_naughty 0 16.webp")
image anim_work_office_session_event_first_naughty_2  = Movie(play ="images/events/office/office_event_first_naughty 0 17.webm", start_image = "images/events/office/office_event_first_naughty 0 17.webp", image = "images/events/office/office_event_first_naughty 0 17.webp")
image anim_work_office_session_event_first_naughty_3  = Movie(play ="images/events/office/office_event_first_naughty 0 18.webm", start_image = "images/events/office/office_event_first_naughty 0 18.webp", image = "images/events/office/office_event_first_naughty 0 18.webp")
image anim_work_office_session_event_first_naughty_4  = Movie(play ="images/events/office/office_event_first_naughty 0 21.webm", start_image = "images/events/office/office_event_first_naughty 0 21.webp", image = "images/events/office/office_event_first_naughty 0 21.webp")
image anim_work_office_session_event_first_naughty_64 = Movie(play ="images/events/office/office_event_first_naughty 0 64.webm", start_image = "images/events/office/office_event_first_naughty 0 64.webp", image = "images/events/office/office_event_first_naughty 0 64.webp")
image anim_work_office_session_event_first_naughty_65 = Movie(play ="images/events/office/office_event_first_naughty 0 65.webm", start_image = "images/events/office/office_event_first_naughty 0 65.webp", image = "images/events/office/office_event_first_naughty 0 65.webp")
image anim_work_office_session_event_first_naughty_66 = Movie(play ="images/events/office/office_event_first_naughty 0 66.webm", start_image = "images/events/office/office_event_first_naughty 0 66.webp", image = "images/events/office/office_event_first_naughty 0 66.webp")
image anim_work_office_session_event_first_naughty_67 = Movie(play ="images/events/office/office_event_first_naughty 0 67.webm", start_image = "images/events/office/office_event_first_naughty 0 67.webp", image = "images/events/office/office_event_first_naughty 0 67.webp")
image anim_work_office_session_event_first_naughty_68 = Movie(play ="images/events/office/office_event_first_naughty 0 68.webm", start_image = "images/events/office/office_event_first_naughty 0 68.webp", image = "images/events/office/office_event_first_naughty 0 68.webp")
image anim_work_office_session_event_first_naughty_69 = Movie(play ="images/events/office/office_event_first_naughty 0 69.webm", start_image = "images/events/office/office_event_first_naughty 0 69.webp", image = "images/events/office/office_event_first_naughty 0 69.webp")
image anim_work_office_session_event_first_naughty_72 = Movie(play ="images/events/office/office_event_first_naughty 0 72.webm", start_image = "images/events/office/office_event_first_naughty 0 72.webp", image = "images/events/office/office_event_first_naughty 0 72.webp")
image anim_work_office_session_event_first_naughty_73 = Movie(play ="images/events/office/office_event_first_naughty 0 73.webm", start_image = "images/events/office/office_event_first_naughty 0 73.webp", image = "images/events/office/office_event_first_naughty 0 73.webp")
image anim_work_office_session_event_first_naughty_74 = Movie(play ="images/events/office/office_event_first_naughty 0 74.webm", start_image = "images/events/office/office_event_first_naughty 0 74.webp", image = "images/events/office/office_event_first_naughty 0 74.webp")
image anim_work_office_session_event_first_naughty_75 = Movie(play ="images/events/office/office_event_first_naughty 0 75.webm", start_image = "images/events/office/office_event_first_naughty 0 75.webp", image = "images/events/office/office_event_first_naughty 0 75.webp")
label work_office_session_event_first_naughty (**kwargs):
    $ begin_event(**kwargs)

    $ school_level = get_value('school_level', **kwargs)
    $ secretary_level = get_value('secretary_level', **kwargs)

    $ image = Image_Series("images/events/office/office_event_first_naughty 0 <step>.webp", **kwargs)

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
    
    scene anim_work_office_session_event_first_naughty_1 with dissolveM
    pause

    scene anim_work_office_session_event_first_naughty_2 with dissolveM
    pause

    scene anim_work_office_session_event_first_naughty_3 with dissolveM
    pause

    scene anim_work_office_session_event_first_naughty_4 with dissolveM
    pause

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
    sgirl "Sry, is everything okay?" (name = "Yuriko Oshima")
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
    
    scene anim_work_office_session_event_first_naughty_64 with dissolveM
    pause 1.0
    scene anim_work_office_session_event_first_naughty_65 with dissolveM
    secretary "Oh yes! Yes! Yes!"
    headmaster "What were you thinking doing that with Yuriko sitting just in front of me!"
    secretary "I'm sorry! *moan* I couldn't resist!"
    scene anim_work_office_session_event_first_naughty_66 with dissolveM
    headmaster "You will be punished for that!"
    secretary "Yes, I deserve it!... But it was so hot! *moan*"
    headmaster "I see that, you're as wet as a river!"
    scene anim_work_office_session_event_first_naughty_67 with dissolveM
    headmaster "I will make sure you will never forget this!"
    headmaster "Take this!"
    scene anim_work_office_session_event_first_naughty_68 with dissolveM
    secretary "OH MY GOD! YES! YES! YES!" (interact = False)
    pause 3.0
    scene anim_work_office_session_event_first_naughty_69 with dissolveM
    # headmaster cums
    secretary "Oh my god! That was amazing!"
    $ image.show(70)
    headmaster "We're not finished!"
    secretary "Huh?"
    headmaster "Remember, this is your punishment."
    $ image.show(71)
    headmaster "Now get on your knees and open your mouth!"
    # headmaster deepthroats her
    scene anim_work_office_session_event_first_naughty_72 with dissolveM
    secretary "Hmmpf! *gag* *gag* *gag*"
    headmaster "That's what you get for almost exposing us!"
    scene anim_work_office_session_event_first_naughty_73 with dissolveM
    secretary "I'm sorry! *gag* *gag* *gag*"
    # headmaster cums in her throat
    scene anim_work_office_session_event_first_naughty_74 with dissolveM
    pause 5.3
    scene anim_work_office_session_event_first_naughty_75 with dissolveM
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
        inhibition = DEC_MEDIUM, corruption = MEDIUM, happiness = DEC_SMALL)
    call change_stats_with_modifier('secretary',
        happiness = LARGE, corruption = LARGE, inhibition = DEC_MEDIUM)

    $ end_event('new_daytime', **kwargs)

label work_office_session_event_1(**kwargs):
    $ begin_event(**kwargs)

    $ girl_name = get_value('girl_name', **kwargs)
    $ get_level('school_level', **kwargs)
    $ get_level('secretary_level', **kwargs)

    $ girl_first_name, girl_last_name = split_name(girl_name)

    $ image = Image_Series("images/events/office/work_office_session_event_1 <girl_name> <school_level> <secretary_level> <step>.webp", ['girl_name', 'school_level', 'secretary_level'], **kwargs)

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
    show screen black_screen_text("1h later.")
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
        happiness = MEDIUM, education = SMALL)

    $ end_event('new_daytime', **kwargs)

label office_call_secretary_1 (**kwargs):
    $ begin_event(**kwargs)

    subtitles "You call the secretary."
    secretary "Hello, [headmaster_first_name]. How can I help you?"
    headmaster "I need your opinion on something."
    secretary "Sure, what is it?"
    headmaster "I'm thinking of introducing sex education classes in the curriculum. What do you think?"
    secretary "I think it's a great idea. It's important for students to be educated about such topics."
    secretary "But do you think the rest of the staff and also the students would agree?"
    headmaster "You're right that will be quite the hurdle, I guess I need to make sure they are ready for it before suggesting it."
    headmaster "Thank you for your input."
    secretary "You're welcome. Is there anything else?"
    headmaster "No, that's all. Thank you."
    secretary "You're welcome. Have a nice day."
    headmaster_thought "Maybe I should start work on some teaching material for the sex ed classes."
    headmaster_thought "Perhaps also introductory material on the subject."

    $ start_progress('start_sex_ed')
    $ remove_game_data('start_sex_ed_timer_1')

    $ end_event('new_daytime', **kwargs)

label office_prepare_sex_ed_material(**kwargs):
    $ begin_event(**kwargs)

    subtitles "You start working on the teaching material for the new sex ed classes"
    headmaster_thought "Hmm, what should I include here?"
    headmaster_thought "I think the material needs to be informative but also very visual and engaging."
    headmaster_thought "I guess if I distribute the this before the weekend after introducing the new classes, the students would have time to read it and maybe already take some example out of it."
    headmaster_thought "So I guess the introductory material should include information about clothing, hygiene, and the importance of consent and their psychological impacts."
    headmaster_thought "I think that including some references to visual material should be enough for now."

    $ advance_progress('start_sex_ed')

    $ end_event('new_daytime', **kwargs)

label office_event_1 (**kwargs):
    $ begin_event(**kwargs);

    $ school_level = get_value('school_level', **kwargs)
    $ teacher_level = get_value('teacher_level', **kwargs)

    $ image = Image_Series("images/events/office/office_event_1 <school_level> <step>.webp", **kwargs)

    $ image.show(0)
    subtitles "You notice a girl sitting in front of the teachers office."

    $ image.show(1)
    subtitles "Apparently she is in need of counseling."

    call change_stats_with_modifier('school',
        happiness = TINY, reputation = TINY)
    call change_stats_with_modifier('teacher',
        happiness = TINY)
    
    $ end_event('new_daytime', **kwargs)

label office_event_2 (**kwargs):
    $ begin_event(**kwargs);

    $ teacher_level = get_value('teacher_level', **kwargs)
    $ school_level = get_value('school_level', **kwargs)
    $ teacher = get_value("teacher", **kwargs)

    call show_image ("images/events/office/office_event_2 <teacher_level> <teacher>.webp", **kwargs) from _call_show_image_office_event_2
    subtitles "Even the teachers need a break from time to time."

    call change_stats_with_modifier('school',
        education = DEC_SMALL, reputation = DEC_TINY)
    call change_stats_with_modifier('teacher',
        happiness = TINY)

    $ end_event('new_daytime', **kwargs)

label office_event_3 (**kwargs):
    $ begin_event(**kwargs);

    $ school_level = get_value('school_level', **kwargs)
    $ teacher_level = get_value('teacher_level', **kwargs)

    $ image = Image_Series("images/events/office/office_event_3 <school_level> <step>.webp", **kwargs)

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
        happiness = TINY)

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
        charm = SMALL, happiness = DEC_SMALL)
    call change_stats_with_modifier('teacher',
        happiness = TINY)

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
        charm = DEC_SMALL, happiness = MEDIUM, inhibition = DEC_SMALL)
    call change_stats_with_modifier('teacher',
        happiness = DEC_SMALL)

    if get_progress("unlock_student_relationship") == -1:
        $ start_progress("unlock_student_relationship")
        $ add_notify_message("Added new rule to journal!")
        
    $ end_event('new_daytime', **kwargs)

###########################################