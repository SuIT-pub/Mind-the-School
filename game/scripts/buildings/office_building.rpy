#############################################
# ----- Office Building Event Handler ----- #
#############################################

init -1 python:
    def office_building_events_available() -> bool:
        return (office_building_timed_event.has_available_highlight_events() or
            office_building_general_event.has_available_highlight_events() or
            any(e.has_available_highlight_events() for e in office_building_events.values()))

    office_building_timed_event = TempEventStorage("office_building", "office_building", Event(2, "office_building.after_time_check"))
    office_building_general_event = EventStorage("office_building", "office_building", Event(2, "office_building.after_general_check"))

    office_building_work_event = {}
    add_storage(office_building_work_event, EventStorage("councelling", "office_building"))

    office_building_events = {}
    add_storage(office_building_events, EventStorage("look_around", "office_building"))
    add_storage(office_building_events, EventStorage("work",        "office_building"))

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
            thumbnail = "images/events/office/office_event_1 1 0.webp"),

        Event(3, "office_event_2",
            RandomListSelector("teacher", "Finola Ryan", "Yulan Chen"),
            TimeCondition(weekday = "d", daytime = "f"),
            thumbnail = "images/events/office/office_event_2 1 Finola Ryan.webp"),

        Event(3, "office_event_3",
            TimeCondition(weekday = "d", daytime = "d"),
            NOT(RuleCondition("student_student_relation")),
            thumbnail = "images/events/office/office_event_3 1 0.webp"),
    )

    
    office_building_events["work"].add_event(
        Event(3, "work_office_event",
            TimeCondition(weekday = "d", daytime = "d")),
    )

    office_building_work_event["councelling"].add_event(
        Event(3, "work_office_money_event_1",
            TimeCondition(weekday = "d", daytime = "d")),
        Event(3, "work_office_education_event_1",
            TimeCondition(weekday = "d", daytime = "d")),
        Event(3, "work_office_session_event_naughty_1",
            TimeCondition(weekday = "d", daytime = "d"),
            ProgressCondition("school sessions", "5+"),
            ProgressSelector("naughty_sessions", "work_office_session_naughty")),
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

label work_office_event (**kwargs):
    call call_event_menu (
        "What subject do you wanna teach?", 
        office_building_work_event,
        default_fallback,
        character.subtitles,
        override_menu_exit = 'office_building',
        **kwargs
    ) from work_office_event_1

    jump office_building

label work_office_money_event_1 (**kwargs):
    $ begin_event(**kwargs)

    subtitles "You work on checking the accounts of the school."
    show screen black_screen_text("1h later.")
    # headmaster is consumed by the terrible accounting done in the past
    headmaster_thought "How can this be? This is a mess!"
    headmaster_thought "I need to get this sorted out."
    headmaster_thought "There is so much wrong with these accounts. It's gonna take ages to fix this."
    headmaster_thought "At least I was able to find some money that was lost in the system."

    call change_money_with_modifier(get_random_int(100, 500))

    $ end_event('new_daytime', **kwargs)

label work_office_education_event_1 (**kwargs):
    $ begin_event(**kwargs)

    $ school_obj = get_char_value('school_obj', **kwargs)
    $ teacher_obj = get_char_value('teacher_obj', **kwargs)

    subtitles "You work on optimizing the teaching material for the students."
    show screen black_screen_text("1h later.")
    headmaster_thought "I think I found a way to make the material more interesting for the students."

    call change_stats_with_modifier(school_obj,
        education = SMALL, happiness = TINY)
    call change_stats_with_modifier(teacher_obj,
        happiness = SMALL, education = SMALL)

    $ end_event('new_daytime', **kwargs)

image anim_work_office_session_event_naughty_1_1 = Movie(play ="images/events/office/office_event_naughty_1 0 16.webm", start_image = "images/events/office/office_event_naughty_1 0 16.webp", image = "images/events/office/office_event_naughty_1 0 16.webp")
image anim_work_office_session_event_naughty_1_2 = Movie(play ="images/events/office/office_event_naughty_1 0 17.webm", start_image = "images/events/office/office_event_naughty_1 0 17.webp", image = "images/events/office/office_event_naughty_1 0 17.webp")
image anim_work_office_session_event_naughty_1_3 = Movie(play ="images/events/office/office_event_naughty_1 0 18.webm", start_image = "images/events/office/office_event_naughty_1 0 18.webp", image = "images/events/office/office_event_naughty_1 0 18.webp")
image anim_work_office_session_event_naughty_1_4 = Movie(play ="images/events/office/office_event_naughty_1 0 21.webm", start_image = "images/events/office/office_event_naughty_1 0 21.webp", image = "images/events/office/office_event_naughty_1 0 21.webp")
label work_office_session_event_naughty_1 (**kwargs):
    $ begin_event(**kwargs)

    $ school_obj = get_char_value('school_obj', **kwargs)
    $ secretary_obj = get_char_value('secretary_obj', **kwargs)
    $ naughty_sessions = get_value("naughty_sessions", **kwargs)

    if naughty_sessions == -1:
        $ naughty_sessions = 0
        $ kwargs["naughty_sessions"] = 0

    $ image = Image_Series("images/events/office/office_event_naughty_1 <naughty_sessions> <step>.webp", **kwargs)

    if naughty_sessions == 0:
        # secretary enters office
        call Image_Series.show_image(image, 0, 1, 2) from _call_work_office_session_event_naughty_1_1
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
        
        scene anim_work_office_session_event_naughty_1_1 with dissolveM
        pause

        scene anim_work_office_session_event_naughty_1_2 with dissolveM
        pause

        scene anim_work_office_session_event_naughty_1_3 with dissolveM
        pause

        scene anim_work_office_session_event_naughty_1_4 with dissolveM
        pause

        # secretary starts giving blow and titjob
        $ image.show(22)
        subtitles "*Knock! Knock!*"
        $ image.show(23) # TODO: make image
        sgirl "Excuse me? Mr. [headmaster_last_name]?" (name = "Yuriko Oshima")
        $ image.show(24)
        headmaster_whisper "Shit! Quick under the desk!"
        call Image_Series.show_image(image, 25, 26) from _call_work_office_session_event_naughty_1_2
        headmaster "Yes come in."
        call Image_Series.show_image(image, 27, 28, 29) from _call_work_office_session_event_naughty_1_3
        headmaster "You're early."
        $ image.show(30)
        sgirl "I apologize for that. Something came up in school and I need to leave earlier. So I thought, I'd come earlier." (name = "Yuriko Oshima")
        $ image.show(31)
        sgirl "I wanted to ask your secretary first but I couldn't find her." (name = "Yuriko Oshima")
        call Image_Series.show_image(image, 32, 40) from _call_work_office_session_event_naughty_1_5
        headmaster "Oh she is probably doing some rounds."
        $ image.show(32)
        headmaster "You're really not able to take the session on the agreed time?"
        $ image.show(33)
        sgirl "I don't think so..." (name = "Yuriko Oshima")
        $ image.show(34)
        headmaster "Alright, then let's do it now. Take a seat."
        call Image_Series.show_image(image, 35, 36, 37, 38) from _call_work_office_session_event_naughty_1_4
        sgirl "Are you okay? You look a bit flushed." (name = "Yuriko Oshima")
        $ image.show(39)
        headmaster "Yes, I'm fine. I just had a bit of a headache. But it's getting better."
        $ image.show(40)
        headmaster "Okay what do you want to talk about today?"

        sgirl "Well, Mr. [headmaster_last_name], I've been feeling really stressed lately." (name = "Yuriko Oshima")
        headmaster "I see. Is there something specific that's been bothering you?"
        sgirl "Yes, it's mainly the pressure to perform well academically. I feel like I'm constantly under scrutiny." (name = "Yuriko Oshima")
        headmaster "I understand. Academic pressure can be overwhelming. Have you tried talking to your teachers about it?"
        sgirl "I haven't yet. I guess I'm afraid they won't understand or think I'm just making excuses." (name = "Yuriko Oshima")
        headmaster "I assure you, Yuriko, your feelings are valid. It's important to communicate your struggles with your teachers so they can support you."
        sgirl "Thank you, Mr. [headmaster_last_name]. I'll try to gather the courage to talk to them." (name = "Yuriko Oshima")
        headmaster "That's a good step forward. Remember, you're not alone in this. We're here to help you succeed."
        headmaster "If it is too difficult for you to talk to your teachers, how about your friends? Maybe they can help you."
        sgirl "It's... It's quite hard. I don't really have friends. I have Ellie, but I fear bothering her too much with my problems." (name = "Yuriko Oshima")
        headmaster "Ellie?"
        sgirl "Yes, Elsie Johnson. She's in my class. She's really nice and I really like her. But I don't want to be a burden to her." (name = "Yuriko Oshima")
        headmaster "I see. It's important to have someone to talk to. Maybe you can try to open up to her."
        headmaster "It's always good to be able to talk to someone you're close to. I'll be always here to help yoaaaaaah!"
        # emiko starts handling your rod again
        sgirl "Sry, is everything okay?" (name = "Yuriko Oshima")
        headmaster "*cough* *cough* Yes, everything is fine. I just swallowed wrong."
        headmaster "What I wanted to say is that you can always come to me if you need help but you understand that it is difficult in my position to provide a level of intimacy that you might need."
        sgirl "Intimacy?" (name = "Yuriko Oshima")
        # emiko grins at you and then continues
        headmaster "Yes! You know humans don't work very well when being alone. We need to be close to others to feel good."
        headmaster "It even isn't really enough to just have people you know around you. You need to have people you trust. A sort of intimate bonding."
        headmaster "Even physical contact plays an important role in that. It's a way to show that you care about someone."
        sgirl "Physical contact? I don't think I can go that far..." (name = "Yuriko Oshima") # Yuriko blushes
        headmaster "Don't missunderstand. Even hugging someone can be a form of physical contact. It's not always about a sexual relationship."
        headmaster "Even though having sex can be the closest form of intimacy. But it's not the only one and that is not what I meant in this case."
        headmaster "That is why you really should try to talk to Elsie about your problems, your feelings and your fears. She might be able to help you."
        headmaster "How about you do that, and the next time we talk about how it went? Would that be okay for you?"
        sgirl "Yes, I think I can do that. Thank you, Mr. [headmaster_last_name]." (name = "Yuriko Oshima")
        headmaster "You're welcome, Yuriko. Now I think that settles it for today. I hope I could help you a bit."
        sgirl "Yes, you did. Thank you." (name = "Yuriko Oshima")
        headmaster "Thank you for entrusting yourself to me."
        headmaster "I have a lot to do, so unfortunately I can't accompany you to the door. So please just close the dorr behind you."
        sgirl "Will do. Thank you." (name = "Yuriko Oshima")
        headmaster "Have a nice day."
        # Yuriko leaves
        # emiko comes out from under the desk
        secretary "That was close."
        headmaster "Now I've got enough!"
        secretary "What?"
        # headmaster pushes her on the desk pulls up her skirt and pushes himself into her
        secretary "Oh yes! Yes! Yes!"
        headmaster "What were you thinking doing that with Yuriko sitting just in front of me!"
        secretary "I'm sorry! *moan* I couldn't resist!"
        headmaster "You will be punished for that!"
        secretary "Yes, I deserve it!... But it was so hot! *moan*"
        headmaster "I see that, you're as wet as a river!"
        headmaster "I will make sure you will never forget this!"
        headmaster "Take this!"
        secretary "OH MY GOD! YES! YES! YES!"
        # headmaster cums
        secretary "Oh my god! That was amazing!"
        headmaster "We're not finished!"
        secretary "Huh?"
        headmaster "Remember, this is your punishement."
        headmaster "Now get on your knees and open your mouth!"
        # headmaster deepthroats her
        secretary "Hmmpf! *gag* *gag* *gag*"
        headmaster "That's what you get for almost exposing us!"
        secretary "I'm sorry! *gag* *gag* *gag*"
        # headmaster cums in her throat
        secretary "*cough* *cough* *cough*"
        headmaster "Now clean yourself up and get back to work!"
        secretary "Yes, Master."
        # secretary collecting her stuff
        headmaster_thought "Master? Maybe I overdid it a bit."
        # shot of yuriko standing in front of the door blushed and then running away
        # emiko leaves the office quite happy and finds yurikos scarf on the floor

        $ start_progress('work_office_session_naughty')

        call change_stats_with_modifier(school_obj,
            inhibition = DEC_MEDIUM, corruption = MEDIUM, happiness = DEC_SMALL)
        call change_stats_with_modifier(secretary_obj,
            happiness = LARGE, corruption = LARGE, inhibition = DEC_MEDIUM)

        $ end_event('new_daytime', **kwargs)
    elif naughty_sessions == 1:
        pass

# TODO: make images
label office_event_1 (**kwargs):
    $ begin_event(**kwargs);

    $ school_obj = get_char_value('school_obj', **kwargs)
    $ teacher_obj = get_char_value('teacher_obj', **kwargs)

    $ image = Image_Series("images/events/office/office_event_1 <school_level> <step>.webp", **kwargs)

    $ image.show(0)
    subtitles "You notice a girl sitting in front of the teachers office."

    $ image.show(1)
    subtitles "Apparently she is in need of counseling."

    call change_stats_with_modifier(school_obj,
        happiness = TINY, reputation = TINY)
    call change_stats_with_modifier(teacher_obj,
        happiness = TINY)
    
    $ end_event('new_daytime', **kwargs)

# TODO: make images
label office_event_2 (**kwargs):
    $ begin_event(**kwargs);

    $ teacher_obj = get_char_value('teacher_obj', **kwargs)
    $ school_obj = get_char_value('school_obj', **kwargs)
    $ teacher = get_value("teacher", **kwargs)

    call show_image ("images/events/office/office_event_2 <teacher_level> <teacher>.webp", **kwargs) from _call_show_image_office_event_2
    subtitles "Even the teachers need a break from time to time."

    call change_stats_with_modifier(school_obj,
        education = DEC_SMALL, reputation = DEC_TINY)
    call change_stats_with_modifier(teacher_obj,
        happiness = TINY)

    $ end_event('new_daytime', **kwargs)

# TODO: make images
label office_event_3 (**kwargs):
    $ begin_event(**kwargs);

    $ school_obj = get_char_value('school_obj', **kwargs)
    $ teacher_obj = get_char_value('teacher_obj', **kwargs)

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

    call change_stats_with_modifier(teacher_obj,
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

    call change_stats_with_modifier(school_obj,
        charm = SMALL, happiness = DEC_SMALL)
    call change_stats_with_modifier(teacher_obj,
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

    call change_stats_with_modifier(school_obj,
        charm = DEC_SMALL, happiness = MEDIUM, inhibition = DEC_SMALL)
    call change_stats_with_modifier(teacher_obj,
        happiness = DEC_SMALL)

    if get_progress("unlock_student_relationship") == -1:
        $ start_progress("unlock_student_relationship")
        $ add_notify_message("Added new rule to journal!")
        
    $ end_event('new_daytime', **kwargs)

###########################################