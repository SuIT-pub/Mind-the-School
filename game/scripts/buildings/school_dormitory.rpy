###################################################
# ----- High School Dormitory Event Handler ----- #
###################################################

init -1 python:
    set_current_mod('base')
    def sd_events_available() -> bool:
        return (sd_timed_event.has_available_highlight_events() or
            sd_general_event.has_available_highlight_events() or
            any(e.has_available_highlight_events() for e in sd_events.values()))

    sd_timed_event = TempEventStorage("school_dormitory", "school_dormitory", fallback = Event(2, "school_dormitory.after_time_check"))
    sd_general_event = EventStorage("school_dormitory",   "school_dormitory", fallback = Event(2, "school_dormitory.after_general_check"))

    sd_events = {}
    add_storage(sd_events, EventStorage("peek_students", "school_dormitory", fallback_text = "There is nobody here."))

    sd_bg_images = BGStorage("images/background/school dormitory/bg c.webp", ValueSelector('loli', 0),
        BGImage("images/background/school dormitory/bg <loli> <school_level> <variant> <nude>.webp", 1, OR(TimeCondition(daytime = "f"), TimeCondition(daytime = "c", weekday = "w"))),
        BGImage("images/background/school dormitory/bg 7.webp", 1, TimeCondition(daytime = 7)),
    )

init 1 python:
    set_current_mod('base')    
    first_week_school_dormitory_event_event = Event(1, "first_week_school_dormitory_event",
        IntroCondition(),
        TimeCondition(day = "2-4", month = 1, year = 2023),
        Pattern("main", "images/events/first week/first week school dormitory <step>.webp"),
        thumbnail = "images/events/first week/first week school dormitory 1.webp")

    first_potion_school_dormitory_event_event = Event(1, "first_potion_school_dormitory_event",
        IntroCondition(),
        TimeCondition(day = 9, month = 1, year = 2023),
        Pattern("main", "images/events/first potion/first potion school dormitory <step>.webp"),
        thumbnail = "images/events/first potion/first potion school dormitory 3.webp")

    sd_event1 = Event(3, "sd_event_1",
        LevelSelector('school_level', 'school'),
        StatSelector('education', EDUCATION, "school"),
        StatSelector('inhibition', INHIBITION, "school"),
        OR(
            TimeCondition(weekday = "d", daytime = "f"), 
            TimeCondition(weekday = "d", daytime = "n"), 
            TimeCondition(weekday = "w")
        ),
        Pattern("main", "images/events/school dormitory/sd_event_1 <school_level> <step>.webp"),
        thumbnail = "images/events/school dormitory/sd_event_1 1 0.webp")

    sd_event2 = Event(3, "sd_event_2",
        LevelSelector('school_level', 'school'),
        RandomValueSelector('inhibition_limit', 30, 50),
        StatSelector('inhibition', INHIBITION, "school"),
        RandomListSelector('location', "dorm_room", "shower"),
        ConditionSelector("topic_set", KeyCompareCondition("inhibition", "inhibition_limit", ">="), 1, 2),
        RandomListSelector('topic', 
            (
                RandomListSelector('', "ah", "ahhh", "oh", "eeek", (0.05, "panties"), (0.02, "breasts")), 
                NumCompareCondition("topic_set", 1, "==")
            ),
            (
                RandomListSelector('', "guys_stop", "huh", "reason", "dressing", "blush"), 
                NumCompareCondition("topic_set", 2, "==")
            ),
        ),
        RandomListSelector('girl_name',
            (
                RandomListSelector('', "Aona Komuro", "Lin Kato", "Gloria Goto"), 
                ValueCondition("location", "dorm_room")
            ),
            (
                RandomListSelector('', "Sakura Mori", "Elsie Johnson", "Ishimaru Maki"), 
                ValueCondition("location", "shower")
            ),
        ),
        OR(
            TimeCondition(weekday = "d", daytime = "f"), 
            TimeCondition(weekday = "d", daytime = "n"), 
            TimeCondition(weekday = "w")
        ),
        Pattern("main", "images/events/school dormitory/sd_event_2 <topic> <location> <girl_name> <school_level> <step>.webp"),
        Pattern("end", "images/events/school dormitory/sd_event_2 <location> <step>.webp"),
        thumbnail = "images/events/school dormitory/sd_event_2 ah dorm_room Aona Komuro 1 0.webp")

    sd_event3 = Event(3, "sd_event_3",
        LevelSelector('school_level', 'school'),
        StatSelector('inhibition', INHIBITION, "school"),
        RandomListSelector('topic', "normal", (0.1, "panties"), (0.02, "nude")),
        TimeCondition(daytime = "6,7"),
        Pattern("main", "images/events/school dormitory/sd_event_3 <topic> <school_level> <step>.webp"),
        thumbnail = "images/events/school dormitory/sd_event_3 normal 1 0.webp")

    sd_action_tutorial_event = Event(2, "action_tutorial",
        NOT(ProgressCondition('action_tutorial')),
        ValueSelector('return_label', 'school_dormitory'),
        NoHighlightOption(),
        TutorialCondition(),
        Pattern("main", "/images/events/misc/action_tutorial <step>.webp"),
        override_location = "misc", thumbnail = "images/events/misc/action_tutorial 0.webp")

    sd_general_event.add_event(
        sd_action_tutorial_event,
        first_week_school_dormitory_event_event,
        first_potion_school_dormitory_event_event,
    )

    # sd_events["peek_students"].add_event(sd_event2)
    sd_events["peek_students"].add_event(sd_event1, sd_event2, sd_event3)
    
###################################################

############################################
# ----- School Dormitory Entry Point ----- #
############################################

label school_dormitory ():
    call call_available_event(sd_timed_event) from school_dormitory_1

label .after_time_check (**kwargs):
    call call_available_event(sd_general_event) from school_dormitory_4

label .after_general_check (**kwargs):
    call call_event_menu (
        "What to do in the High School Dorm?", 
        sd_events, 
        default_fallback,
        character.subtitles,
        bg_image = sd_bg_images,
    ) from school_dormitory_3

    jump school_dormitory

#################################################

#######################################
# ----- School Dormitory Events ----- #
#######################################

label first_week_school_dormitory_event (**kwargs):
    $ begin_event(**kwargs)

    $ image = convert_pattern("main", step_start = 1, **kwargs)
    
    $ image.show(1)
    headmaster_thought "The dormitory looks alright."

    $ image.show(2)
    headmaster_thought "As far as I know, the students have to share a communal bathroom."
    headmaster_thought "Private bathrooms would be nice for the students, but for one I don't think we really need that and then it would need a lot of rebuilding. So that should be last on the list."
    
    $ image.show(3)
    headmaster_thought "Let's see if someone would let me see their room so I can check the state of these."
    
    $ image.show(4)
    headmaster "Hello? I'm Mr. [headmaster_last_name] the new Headmaster. Can I come in? I'm here to inspect the building."
    subtitles "..."
    headmaster "Hello?"

    $ image.show(5)
    headmaster_thought "Hmm nobody seems to be here. Nevermind. I just let my Secretary give me a report."

    $ change_stat("inhibition", -3, get_school())
    $ change_stat("happiness", 3, get_school())

    $ set_building_blocked("school_dormitory")

    $ end_event('new_day', **kwargs)

label first_potion_school_dormitory_event (**kwargs):
    $ begin_event(**kwargs)

    $ image = convert_pattern("main", step_start = 1, **kwargs)
    
    $ image.show(1)
    subtitles "You enter the dormitory of the high school."
    headmaster_thought "Mhh, where does the noise come from?"

    $ image.show(2)
    headmaster_thought "Ah I think there are some students in the room over there."

    $ image.show(3)
    headmaster_thought "Ahh party games!"

    $ image.show(4)
    if time.check_daytime("c"):
        headmaster_thought "Normally I would scold them for skipping class but today is a special day so I gladly enjoy this view."
    else:
        headmaster_thought "Ahh I like this view. Nothing more erotic than nudity in combination with a party game."

    $ set_building_blocked("school_dormitory")

    $ end_event('new_daytime', **kwargs)

label sd_event_1 (**kwargs):
    $ begin_event(**kwargs)

    $ school_level = get_value('school_level', **kwargs)
    $ inhibition = get_stat_value('inhibition', [89, 100], **kwargs)
    $ education = get_stat_value('education', [50, 100], **kwargs)

    $ image = convert_pattern("main", **kwargs)

    if education > 50:
        $ image.show(0)
        sgirl "Umm, hello!" (name = "Easkey Tanaka")
        $ image.show(1)
        headmaster "Hello there, is everything okay?"
        if inhibition >= 90:
            $ image.show(2)
            sgirl "Yeah Mr. [headmaster_last_name], but would you please knock before entering next time?" (name = "Easkey Tanaka")
            $ image.show(3)
            headmaster "Ah yes... yes of course."
            call change_stats_with_modifier('school',
                happiness = DEC_TINY) from _call_change_stats_with_modifier_73
            $ end_event(**kwargs)
        else:
            $ image.show(5)
            sgirl "Yeah Mr. [headmaster_last_name], you just surprised me." (name = "Easkey Tanaka")
            $ image.show(6)
            headmaster "Oh, sorry about that."
            call change_stats_with_modifier('school',
                happiness = DEC_TINY, education = MEDIUM) from _call_change_stats_with_modifier_74
            $ end_event(**kwargs)
    else:
        $ image.show(4)
        sgirl "hmm... This homework is hard. Why do I need to learn this anyway?" (name = "Easkey Tanaka")
        call change_stats_with_modifier('school',
            education = SMALL) from _call_change_stats_with_modifier_75
        $ end_event(**kwargs)

label sd_event_2 (**kwargs):
    $ begin_event(**kwargs)

    $ school_level = get_value('school_level', **kwargs)
    $ location = get_value('location', **kwargs)
    $ girl_name = get_value('girl_name', **kwargs)
    $ topic = get_value('topic', **kwargs)
    $ topic_set = get_value('topic_set', **kwargs)

    $ image = convert_pattern("main", **kwargs)
    $ image2 = convert_pattern("end", **kwargs)

    if topic == "ah":
        $ image.show(0)
        sgirl "Ah!" (name = girl_name)
        call change_stats_with_modifier('school',
            happiness = DEC_TINY, inhibition = DEC_TINY) from _call_change_stats_with_modifier_76
    elif topic == "ahhh":
        $ image.show(0)
        sgirl "AHHH!!!" (name = girl_name)
        call change_stats_with_modifier('school',
            happiness = DEC_TINY, inhibition = DEC_TINY, reputation = DEC_TINY) from _call_change_stats_with_modifier_77
    elif topic == "eeek":
        $ image.show(0)
        sgirl "Eek!" (name = girl_name)
        call change_stats_with_modifier('school',
            happiness = DEC_MEDIUM, inhibition = DEC_TINY) from _call_change_stats_with_modifier_78
    elif topic in ["panties", "breasts"]:
        $ image.show(0)
        $ random_say(
            "Ah!!! Look away, please, you can see my [topic]!",
            "Ah!!! Look away, please, I don't want guys seeing my [topic]!",
            "Eek! Stop! Don't stare at my [topic]!",
            person = character.sgirl, name = girl_name)
        call change_stats_with_modifier('school',
            happiness = DEC_MEDIUM, inhibition = DEC_TINY, charm = MEDIUM) from _call_change_stats_with_modifier_79
    elif topic == "oh":
        $ image.show(0)
        sgirl "Oh!" (name = girl_name)
        $ image.show(1)
        headmaster "I'm terribly sorry."
        $ image.show(2)
        sgirl "I-it's ok..." (name = girl_name)
        $ image.show(3)
        subtitles "You quickly make an exit."
        call change_stats_with_modifier('school',
            inhibition = DEC_TINY, happiness = DEC_MEDIUM) from _call_change_stats_with_modifier_80
        $ end_event(**kwargs)
    # elif topic == "guys_stop":
    #     $ image.show(0)
    #     sgirl "Excuse me!\n Can you guys stop running in and out of here?!"
    #     call change_stats_with_modifier(school_obj,
    #         inhibition = DEC_TINY, morale = DEC_SMALL)
    # elif topic == "huh":
    #     $ image.show(0)
    #     $ random_say(
    #         ("Umm... What are you doing in here?", character.sgirl),
    #         ("Mr. [headmaster_last_name]? What are you doing in here?", character.sgirl),
    #     )
    #     call change_stats_with_modifier(school_obj,
    #         inhibition = DEC_TINY, morale = DEC_SMALL)
    # elif topic == "reason":
    #     $ image.show(0)
    #     sgirl "Hey Mr. [headmaster_last_name]!"
    #     $ image.show(1)
    #     headmaster "Hello there!"
    #     $ image.show(2)
    #     if get_random_int(0, 1000) == 0:
    #         sgirl "General Kenobi!"
    #     sgirl "Any particular reason I get a visit?"
    #     $ image.show(3)
    #     headmaster "Oh no, I just saw an open door and..."
    #     $ image.show(4)
    #     sgirl "Oh, silly me, would you mind closing it on your way out?"
    #     $ image.show(5)
    #     headmaster "No problem."
    #     call change_stats_with_modifier(school_obj,
    #         charm = MEDIUM, inhibition = DEC_MEDIUM);
    #     jump new_daytime;
    # elif topic == "blush":
    #     $ image.show(0)
    #     $ random_say(
    #         ("Ah! What are you doing here?", character.sgirl),
    #         ("Oh! Mr. [headmaster_last_name]!"),
    #     )
    #     call change_stats_with_modifier(school_obj,
    #         charm = MEDIUM, inhibition = DEC_MEDIUM)
    # elif topic == "dressing":
    #     $ image.show(0)
    #     $ random_say(
    #         ("Umm, do you mind?", character.sgirl),
    #         ("I'm getting dressed! GET OUT!", character.sgirl),
    #     )
    #     call change_stats_with_modifier(school_obj,
    #         inhibition = DEC_TINY, charm = SMALL)

    
    $ random_say(
        ("Oh, wrong door, bye!", 0),
        ("Sorry, I'm leaving!", 0),
        ("So sorry!", topic_set == 1, 0),
        ("I'm terribly sorry!", topic_set == 1, 0),
        ("I'm leaving, I'm leaving!", topic_set == 1,  0),
        ("You hastily beat a retreat.", character.subtitles, topic_set == 1, 1),
        ("Good view, bad timing.", character.subtitles, topic_set == 1, 1),
        person = character.headmaster, image = image2)
        # ("Oh, sorry.", topic_set == 2),
        # ("Oh, sorry about that!", topic_set == 2),
        # ("Sorry miss, wrong door obviously!", topic_set == 2),
        # ("Nice view, wrong door. Sorry!", topic_set == 2),
        # ("Bad timing I see. Sorry about that!", topic_set == 2),
        # ("After a quick look at the sexy girl, you apologize and leave.", character.subtitles, topic_set == 2),
        # ("A nice view, but you quickly leave anyway.", character.subtitles, topic_set == 2),

    $ end_event(**kwargs)

label sd_event_3 (**kwargs):
    $ begin_event(**kwargs)

    $ school_level = get_value('school_level', **kwargs)
    $ topic = get_value('topic', **kwargs)

    $ image = convert_pattern("main", **kwargs)

    # if inhibition >= 80:
    $ image.show(0)
    subtitles "Looks like some of the students are ready to bunk."
    headmaster "I'm sorry, I didn't realize..."
    $ image.show(1)
    sgirl "Mm- Mr. [headmaster_last_name]"
    $ image.show(0)
    headmaster "Bye!"
    
    if topic == "normal":
        call change_stats_with_modifier('school', inhibition = DEC_SMALL) from _call_change_stats_with_modifier_81
    elif topic == "panties":
        call change_stats_with_modifier('school', inhibition = DEC_MEDIUM) from _call_change_stats_with_modifier_82
    elif topic == "nude":
        call change_stats_with_modifier('school', inhibition = DEC_LARGE) from _call_change_stats_with_modifier_83

    $ end_event(**kwargs)
