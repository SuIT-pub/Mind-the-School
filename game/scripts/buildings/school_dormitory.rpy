####################################################
# region High School Dormitory Event Handler ----- #
####################################################

init -1 python:
    set_current_mod('base')
    
    sd_timed_event = TempEventStorage("school_dormitory", "school_dormitory", fallback = Event(2, "school_dormitory.after_time_check"))
    sd_general_event = EventStorage("school_dormitory",   "school_dormitory", fallback = Event(2, "school_dormitory.after_general_check"))
    register_highlighting(sd_timed_event, sd_general_event)

    sd_events = {}
    add_storage(sd_events, EventStorage("peek_students", "school_dormitory", fallback_text = "There is nobody here."))
    add_storage(sd_events, EventStorage("look_around", "school_dormitory", fallback_text = "There is nothing to see here."))

    sd_bg_images = BGStorage("images/background/school dormitory/c.webp",
        BGImage("images/background/school dormitory/<school_level> <variant> <nude>.webp", 1, OR(TimeCondition(daytime = "f"), TimeCondition(daytime = "c", weekday = "w"))),
        BGImage("images/background/school dormitory/n.webp", 1, TimeCondition(daytime = 7)),
    )

init 1 python:
    set_current_mod('base')

    sd_event1 = Event(3, "sd_event_1",
        LevelSelector('school_level', 'school'),
        StatSelector('education', EDUCATION, "school", [89, 100]),
        StatSelector('inhibition', INHIBITION, "school", [50, 100]),
        OR(
            TimeCondition(weekday = "d", daytime = "f"), 
            TimeCondition(weekday = "d", daytime = "n"), 
            TimeCondition(weekday = "w")
        ),
        Pattern("main", "images/events/school dormitory/sd_event_1/sd_event_1 <school_level> <step>.webp"),
        thumbnail = "images/events/school dormitory/sd_event_1/sd_event_1 1 0.webp")

    sd_event2 = Event(3, "sd_event_2",
        LevelSelector('school_level', 'school'),
        RandomValueSelector('inhibition_limit', 30, 50),
        StatSelector('inhibition', INHIBITION, "school", []),
        RandomListSelector('location', "dorm_room", "shower"),
        ConditionSelector("topic_set", KeyCompareCondition("inhibition", "inhibition_limit", ">="), 1, 2, realtime = True),
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
                RandomListSelector('', "aona_komuro", "lin_kato", "gloria_goto"), 
                ValueCondition("location", "dorm_room")
            ),
            (
                RandomListSelector('', "sakura_mori", "elsie_johnson", "ishimaru_maki"), 
                ValueCondition("location", "shower")
            ),
        ),
        OR(
            TimeCondition(weekday = "d", daytime = "f"), 
            TimeCondition(weekday = "d", daytime = "n"), 
            TimeCondition(weekday = "w")
        ),
        LevelCondition("5-", "school"),
        Pattern("main", "images/events/school dormitory/sd_event_2/sd_event_2 <topic> <location> <girl_name> <school_level> <step>.webp", "school_level"),
        Pattern("end", "images/events/school dormitory/sd_event_2/sd_event_2 <location> <step>.webp"),
        thumbnail = "images/events/school dormitory/sd_event_2/sd_event_2 ah dorm_room aona_komuro 1 0.webp")

    sd_event3 = Event(3, "sd_event_3",
        LevelSelector('school_level', 'school'),
        RandomListSelector('topic', "normal", (0.1, "panties"), (0.02, "nude")),
        TimeCondition(daytime = "6,7"),
        LevelCondition("2-", "school"),
        Pattern("main", "images/events/school dormitory/sd_event_3/sd_event_3 <topic> <school_level> <step>.webp", "school_level"),
        thumbnail = "images/events/school dormitory/sd_event_3/sd_event_3 normal # 0.webp")

    sd_event4 = Event(3, "sd_event_4",
        TimeCondition(daytime = "f"),
        LevelCondition("5-", "school"),
        Pattern("main", "images/events/school dormitory/sd_event_4/sd_event_4 <school_level> <step>.webp", "school_level"),
        thumbnail = "images/events/school dormitory/sd_event_4/sd_event_4 1 0.webp"
    )

    sd_event5 = Event(3, "sd_event_5",
        TimeCondition(daytime = "1,6,7"),
        Pattern("main", "images/events/school dormitory/sd_event_5/sd_event_5 <school_level> <step>.webp", "school_level"),
        thumbnail = "images/events/school dormitory/sd_event_5/sd_event_5 1 1.webp"
    )

    sd_events["peek_students"].add_event(sd_event1, sd_event2, sd_event3, sd_event5)
    sd_events["look_around"].add_event(sd_event4)

# endregion
###################################################

#############################################
# region School Dormitory Entry Point ----- #
#############################################

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

# endregion
#############################################

########################################
# region School Dormitory Events ----- #
########################################

#########################
# region Regular Events #

label sd_event_1 (**kwargs):
    $ begin_event(**kwargs)

    $ school_level = get_value('school_level', **kwargs)
    $ inhibition = get_stat_value('inhibition', [89, 100], **kwargs)
    $ education = get_stat_value('education', [50, 100], **kwargs)

    $ easkey = get_person("class_3a", "easkey_tanaka").get_character()

    $ image = convert_pattern("main", **kwargs)

    if education > 50:
        $ image.show(0)
        easkey "Umm, hello!"
        $ image.show(1)
        headmaster "Hello there, is everything okay?"
        # if inhibition >= 90:
        $ image.show(2)
        easkey "Yeah Mr. [headmaster_last_name], but would you please knock before entering next time?"
        $ image.show(3)
        headmaster "Ah yes... yes of course."
        call change_stats_with_modifier('school',
            happiness = DEC_TINY) from _call_change_stats_with_modifier_73
        $ end_event(**kwargs)
        # else:
        #     $ image.show(5)
        #     easkey "Yeah Mr. [headmaster_last_name], you just surprised me."
        #     $ image.show(6)
        #     headmaster "Oh, sorry about that."
        #     call change_stats_with_modifier('school',
        #         happiness = DEC_TINY, education = MEDIUM) from _call_change_stats_with_modifier_74
        #     $ end_event(**kwargs)
    else:
        $ image.show(4)
        easkey "hmm... This homework is hard. Why do I need to learn this anyway?"
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

    $ girl = get_person("class_3a", girl_name).get_character()

    $ image = convert_pattern("main", **kwargs)
    $ image2 = convert_pattern("end", **kwargs)

    if topic == "ah":
        $ image.show(0)
        girl "Ah!"
        call change_stats_with_modifier('school',
            happiness = DEC_TINY, inhibition = DEC_TINY) from _call_change_stats_with_modifier_76
    elif topic == "ahhh":
        $ image.show(0)
        girl "AHHH!!!"
        call change_stats_with_modifier('school',
            happiness = DEC_TINY, inhibition = DEC_TINY, reputation = DEC_TINY) from _call_change_stats_with_modifier_77
    elif topic == "eeek":
        $ image.show(0)
        girl "Eek!"
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
        girl "Oh!"
        $ image.show(1)
        headmaster "I'm terribly sorry."
        $ image.show(2)
        girl "I-it's ok..."
        $ image2.show(1)
        subtitles "You quickly make an exit."
        call change_stats_with_modifier('school',
            inhibition = DEC_TINY, happiness = DEC_MEDIUM) from _call_change_stats_with_modifier_80
        $ end_event(**kwargs)
    # elif topic == "guys_stop":
    #     $ image.show(0)
    #     girl "Excuse me!\n Can you guys stop running in and out of here?!"
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
    #     girl "Hey Mr. [headmaster_last_name]!"
    #     $ image.show(1)
    #     headmaster "Hello there!"
    #     $ image.show(2)
    #     if get_random_int(0, 1000) == 0:
    #         girl "General Kenobi!"
    #     girl "Any particular reason I get a visit?"
    #     $ image.show(3)
    #     headmaster "Oh no, I just saw an open door and..."
    #     $ image.show(4)
    #     girl "Oh, silly me, would you mind closing it on your way out?"
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

    $ soyoon = get_person("class_3a", "soyoon_yamamoto").get_character()

    $ image = convert_pattern("main", **kwargs)

    $ image.show(0)
    subtitles "Looks like some of the students are ready to bunk."
    headmaster "I'm sorry, I didn't realize..."
    $ image.show(1)
    soyoon "Mm- Mr. [headmaster_last_name]"
    $ image.show(0)
    headmaster "Bye!"
    
    if topic == "normal":
        call change_stats_with_modifier('school', inhibition = DEC_SMALL) from _call_change_stats_with_modifier_81
    elif topic == "panties":
        call change_stats_with_modifier('school', inhibition = DEC_MEDIUM) from _call_change_stats_with_modifier_82
    elif topic == "nude":
        call change_stats_with_modifier('school', inhibition = DEC_LARGE) from _call_change_stats_with_modifier_83

    $ end_event(**kwargs)

label sd_event_4 (**kwargs):
    $ begin_event(**kwargs)

    $ image = convert_pattern("main", **kwargs)

    call Image_Series.show_image(image, 0, 1, 2, 3, 4) from _call_sd_event_4_1
    headmaster_thought "That was strange..."

    call change_stats_with_modifier('school',
        corruption = SMALL
    ) from _call_sd_event_4_2

    $ end_event(**kwargs)

define anim_sde5_path = "images/events/school dormitory/sd_event_5/sd_event_5 "
image anim_sd_event_5_7_5   = Movie(play = anim_sde5_path + "7 5.webm",   start_image = anim_sde5_path + "7 5.webp", loop = True)
image anim_sd_event_5_7_6   = Movie(play = anim_sde5_path + "7 6.webm",   start_image = anim_sde5_path + "7 6.webp", loop = True)
image anim_sd_event_5_7_7   = Movie(play = anim_sde5_path + "7 7.webm",   start_image = anim_sde5_path + "7 7.webp", loop = True)
image anim_sd_event_5_7_8   = Movie(play = anim_sde5_path + "7 8.webm",   start_image = anim_sde5_path + "7 8.webp")
image anim_sd_event_5_7_9   = Movie(play = anim_sde5_path + "7 9.webm",   start_image = anim_sde5_path + "7 9.webp")
image anim_sd_event_5_7_10  = Movie(play = anim_sde5_path + "7 10.webm",  start_image = anim_sde5_path + "7 10.webp", loop = True)
image anim_sd_event_5_8_5   = Movie(play = anim_sde5_path + "8 5.webm",   start_image = anim_sde5_path + "8 5.webp", loop = True)
image anim_sd_event_5_8_6   = Movie(play = anim_sde5_path + "8 6.webm",   start_image = anim_sde5_path + "8 6.webp", loop = True)
image anim_sd_event_5_8_7   = Movie(play = anim_sde5_path + "8 7.webm",   start_image = anim_sde5_path + "8 7.webp", loop = True)
image anim_sd_event_5_8_8   = Movie(play = anim_sde5_path + "8 8.webm",   start_image = anim_sde5_path + "8 8.webp", loop = True)
image anim_sd_event_5_8_9   = Movie(play = anim_sde5_path + "8 9.webm",   start_image = anim_sde5_path + "8 9.webp", loop = True)
image anim_sd_event_5_8_10  = Movie(play = anim_sde5_path + "8 10.webm",  start_image = anim_sde5_path + "8 10.webp", loop = True)
image anim_sd_event_5_8_11  = Movie(play = anim_sde5_path + "8 11.webm",  start_image = anim_sde5_path + "8 11.webp")
image anim_sd_event_5_8_12  = Movie(play = anim_sde5_path + "8 12.webm",  start_image = anim_sde5_path + "8 12.webp", loop = True)
image anim_sd_event_5_9_5   = Movie(play = anim_sde5_path + "9 5.webm",   start_image = anim_sde5_path + "9 5.webp", loop = True)
image anim_sd_event_5_9_6   = Movie(play = anim_sde5_path + "9 6.webm",   start_image = anim_sde5_path + "9 6.webp", loop = True)
image anim_sd_event_5_9_7   = Movie(play = anim_sde5_path + "9 7.webm",   start_image = anim_sde5_path + "9 7.webp", loop = True)
image anim_sd_event_5_9_8   = Movie(play = anim_sde5_path + "9 8.webm",   start_image = anim_sde5_path + "9 8.webp", loop = True)
image anim_sd_event_5_9_9   = Movie(play = anim_sde5_path + "9 9.webm",   start_image = anim_sde5_path + "9 9.webp", loop = True)
image anim_sd_event_5_9_10  = Movie(play = anim_sde5_path + "9 10.webm",  start_image = anim_sde5_path + "9 10.webp", loop = True)
image anim_sd_event_5_9_11  = Movie(play = anim_sde5_path + "9 11.webm",  start_image = anim_sde5_path + "9 11.webp")
image anim_sd_event_5_9_12  = Movie(play = anim_sde5_path + "9 12.webm",  start_image = anim_sde5_path + "9 12.webp", loop = True)
image anim_sd_event_5_10_5  = Movie(play = anim_sde5_path + "10 5.webm",  start_image = anim_sde5_path + "10 5.webp", loop = True)
image anim_sd_event_5_10_6  = Movie(play = anim_sde5_path + "10 6.webm",  start_image = anim_sde5_path + "10 6.webp", loop = True)
image anim_sd_event_5_10_7  = Movie(play = anim_sde5_path + "10 7.webm",  start_image = anim_sde5_path + "10 7.webp", loop = True)
image anim_sd_event_5_10_8  = Movie(play = anim_sde5_path + "10 8.webm",  start_image = anim_sde5_path + "10 8.webp", loop = True)
image anim_sd_event_5_10_9  = Movie(play = anim_sde5_path + "10 9.webm",  start_image = anim_sde5_path + "10 9.webp", loop = True)
image anim_sd_event_5_10_10 = Movie(play = anim_sde5_path + "10 10.webm", start_image = anim_sde5_path + "10 10.webp", loop = True)
image anim_sd_event_5_10_11 = Movie(play = anim_sde5_path + "10 11.webm", start_image = anim_sde5_path + "10 11.webp")
image anim_sd_event_5_10_12 = Movie(play = anim_sde5_path + "10 12.webm", start_image = anim_sde5_path + "10 12.webp", loop = True)
label sd_event_5 (**kwargs):
    $ begin_event(**kwargs)

    $ luna = get_person("class_3a", "luna_clark").get_character()
    $ seraphina = get_person("class_3a", "seraphina_clark").get_character()

    $ school_level = get_level('school_level', **kwargs)
    $ image = convert_pattern("main", **kwargs)

    $ image.show(0)
    subtitles "You peek into a room."
    $ image.show(1)
    headmaster_thought "Oh the siblings are changing."
    $ image.show(2)
    headmaster_thought "But nice view!"

    $ call_custom_menu_with_text("Continue watching?", character.subtitles, False,
        MenuElement("Leave", "Leave", EventEffect("sd_event_5.leave")),
        MenuElement("Stay watching", "Stay watching", EventEffect("sd_event_5.stay")), 
    **kwargs)

label .leave (**kwargs):
    $ begin_event(**kwargs)

    headmaster_thought "Well better head off. Wouldn't want to get caught."

    call change_stats_with_modifier('school',
        inhibition = DEC_TINY
    ) from _call_sd_event_5_leave_1

    $ end_event("new_daytime", **kwargs)

label .stay (**kwargs):
    $ begin_event(**kwargs)

    if school_level >= 8:
        $ image.show(3)
        luna "Oh Mr. [headmaster_last_name], you're watching?"
        $ image.show(4)
        seraphina "Why not join us?"
        $ image.show_video(5)
        seraphina "Ahh, you're so big!"
        $ image.show_video(6, pause = True)
        $ image.show_video(7, pause = True)
        $ image.show_video(8, pause = True)
        $ image.show_video(9, pause = True)
        $ image.show_video(10, pause = True)
        $ image.show_video(11)
        $ renpy.pause(5.3333)
        $ image.show_video(12)
        luna "Mr. [headmaster_last_name], that was amazing!"

        call change_stats_with_modifier('school',
            inhibition = DEC_SMALL, corruption = SMALL, charm = TINY, happiness = SMALL
        ) from _call_sd_event_5_stay_6
    elif school_level >= 7:
        $ image.show(3)
        luna "Oh Mr. [headmaster_last_name], you're watching?"
        $ image.show(4)
        seraphina "Do you like what you see?"
        luna "Why not make it fair and show us yours?"
        $ image.show_video(5)
        seraphina "Wow Mr. [headmaster_last_name], you're quite big!"
        $ image.show_video(6)
        seraphina "Hmm, you like that?"
        $ image.show_video(7, pause = True)
        $ image.show_video(8)
        $ renpy.pause(7.61)
        $ image.show_video(9)
        $ renpy.pause(5.3333)
        $ image.show_video(10, pause = True)
        luna "Thanks for the meal!"

        call change_stats_with_modifier('school',
            inhibition = DEC_SMALL, corruption = SMALL, charm = TINY, happiness = SMALL
        ) from _call_sd_event_5_stay_5
    elif school_level >= 5:
        $ image.show(3)
        seraphina "Oh Mr. [headmaster_last_name], you're watching?"
        $ image.show(4)
        luna "Do you like what you see?"
        $ image.show(5)
        seraphina "Here let us show you more."
        
        call change_stats_with_modifier('school',
            inhibition = DEC_SMALL, charm = TINY, happiness = TINY
        ) from _call_sd_event_5_stay_4
    elif school_level >= 3:
        $ image.show(3)
        seraphina "Oh Mr. [headmaster_last_name]!"
        $ image.show(4)
        luna "What are you doing here?"
        $ image.show(5)
        seraphina "Could you please leave?"
        headmaster "Oh, sorry!"

        call change_stats_with_modifier('school',
            inhibition = DEC_SMALL, reputation = DEC_SMALL, happiness = DEC_TINY
        ) from _call_sd_event_5_stay_3
    else:
        call Image_Series.show_image(image, 3, 4) from _call_sd_event_5_stay_1
        seraphina "Mr. [headmaster_last_name]!"
        $ image.show(5)
        luna "Get out!"

        call change_stats_with_modifier('school',
            inhibition = DEC_TINY, reputation = DEC_SMALL, happiness = DEC_SMALL
        ) from _call_sd_event_5_stay_2

    $ end_event("new_daytime", **kwargs)
    

# endregion
#########################

# endregion
########################################