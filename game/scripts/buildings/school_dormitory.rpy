# education < 80
label sd_event_1 (**kwargs):
    $ image = Image_Series("images/events/school dormitory/sd_event_1 <name> <level> <step>.png", name = "high_school", **kwargs)

    $ girl_name = "Easkey Tanaka"

    $ begin_event()

    $ char_obj = get_kwargs("char_obj", **kwargs)

    $ education = char_obj.get_stat_number(EDUCATION)
    $ inhibition = char_obj.get_stat_number(INHIBITION)

    if education > 50 and get_random_int(0, 1) == 0:
        $ image.show(0)
        sgirl "Umm, hello!" (name = girl_name)
        $ image.show(1)
        headmaster "Hello there, is everything okay?"
        if inhibition >= 90:
            $ image.show(2)
            sgirl "Yeah Mr. [headmaster_last_name], but would you please knock before entering next time?" (name = girl_name)
            $ image.show(3)
            headmaster "Ah yes... yes of course."
            $ change_stats_with_modifier(char_obj,
                HAPPINESS = DEC_TINY)
            jump new_daytime
        else:
            $ image.show(5)
            sgirl "Yeah Mr. [headmaster_last_name], you just surprised me." (name = girl_name)
            $ image.show(6)
            headmaster "Oh, sorry about that."
            $ change_stats_with_modifier(char_obj,
                HAPPINESS = DEC_TINY, education = MEDIUM)
            jump new_daytime
    else:
        $ image.show(4)
        sgirl "hmm... This homework is hard. Why do I need to learn this anyway?" (name = girl_name)
        $ change_stats_with_modifier(char_obj,
            education = SMALL)
        jump new_daytime

label sd_event_2 (**kwargs):
    $ char_obj = get_kwargs("char_obj", **kwargs)
    $ inhibition = char_obj.get_stat_number(INHIBITION)

    $ location = get_random_choice("dorm_room", "shower")
    $ topic = []

    $ topic_set = 1 if inhibition > get_random_int(30, 50) else 2

    if topic_set == 1:
        $ topic = ["ah", "ahhh", "oh", "eeek", (0.05, "panties"), (0.02, "breasts")]
    else:
        $ topic = ["guys_stop", "huh", "reason", "dressing", "blush"]

    $ log_val("topic", topic)

    $ topic = get_random_choice(*topic)

    $ girl_name = get_random_choice("Aona Komuro", "Lin Kato", "Gloria Goto")

    if location == "shower":
        $ girl_name = get_random_choice("Sakura Mori", "Elsie Johnson", "Ishimaru Maki")

    $ image = Image_Series("images/events/school dormitory/sd_event_2 <name> <topic> <location> <girl> <level> <step>.png", name = "high_school", location = location, topic = topic, girl = girl_name, **kwargs)
    $ image2 = Image_Series("images/events/school dormitory/sd_event_2 <location> <step>.png", location = location)

    $ begin_event()

    if topic == "ah":
        $ image.show(0)
        sgirl "Ah!" (name = girl_name)
        $ change_stats_with_modifier(char_obj,
            happiness = DEC_TINY, inhibition = DEC_TINY)
    elif topic == "ahhh":
        $ image.show(0)
        sgirl "AHHH!!!" (name = girl_name)
        $ change_stats_with_modifier(char_obj,
            happiness = DEC_TINY, inhibition = DEC_TINY, reputation = DEC_TINY)
    elif topic == "eeek":
        $ image.show(0)
        sgirl "Eek!" (name = girl_name)
        $ change_stats_with_modifier(char_obj,
            happiness = DEC_LARGE, inhibition = DEC_TINY)
    elif topic in ["panties", "breasts"]:
        $ image.show(0)
        $ random_say(
            "Ah!!! Look away, please, you can see my [topic]!",
            "Ah!!! Look away, please, I don't want guys seeing my [topic]!",
            "Eek! Stop! Don't stare at my [topic]!",
            person = character.sgirl, name = girl_name)
        $ change_stats_with_modifier(char_obj,
            happiness = DEC_LARGE, inhibition = DEC_TINY, charm = MEDIUM)
    elif topic == "oh":
        $ image.show(0)
        sgirl "Oh!" (name = girl_name)
        $ image.show(1)
        headmaster "I'm terribly sorry."
        $ image.show(2)
        sgirl "I-it's ok..." (name = girl_name)
        $ image.show(3)
        subtitles "You quickly make an exit."
        $ change_stats_with_modifier(char_obj,
            inhibition = DEC_TINY, happiness = DEC_MEDIUM)
        jump new_daytime
    # elif topic == "guys_stop":
    #     $ image.show(0)
    #     sgirl "Excuse me!\n Can you guys stop running in and out of here?!"
    #     $ change_stats_with_modifier(char_obj,
    #         inhibition = DEC_TINY, morale = DEC_SMALL)
    # elif topic == "huh":
    #     $ image.show(0)
    #     $ random_say(
    #         ("Umm... What are you doing in here?", character.sgirl),
    #         ("Mr. [headmaster_last_name]? What are you doing in here?", character.sgirl),
    #     )
    #     $ change_stats_with_modifier(char_obj,
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
    #     $ change_stats_with_modifier(char_obj,
    #         charm = MEDIUM, inhibition = DEC_MEDIUM);
    #     jump new_daytime;
    # elif topic == "blush":
    #     $ image.show(0)
    #     $ random_say(
    #         ("Ah! What are you doing here?", character.sgirl),
    #         ("Oh! Mr. [headmaster_last_name]!"),
    #     )
    #     $ change_stats_with_modifier(char_obj,
    #         charm = MEDIUM, inhibition = DEC_MEDIUM)
    # elif topic == "dressing":
    #     $ image.show(0)
    #     $ random_say(
    #         ("Umm, do you mind?", character.sgirl),
    #         ("I'm getting dressed! GET OUT!", character.sgirl),
    #     )
    #     $ change_stats_with_modifier(char_obj,
    #         inhibition = DEC_TINY, charm = SMALL)

    
    $ random_say(
        {'say': "Oh, wrong door, bye!", 'image': 0},
        {'say': "Sorry, I'm leaving!", 'image': 0},
        {'say': "So sorry!", 'if': topic_set == 1, 'image': 0},
        {'say': "I'm terribly sorry!", 'if': topic_set == 1, 'image': 0},
        {'say': "I'm leaving, I'm leaving!", 'if': topic_set == 1, 'image': 0},
        {'say': "You hastily beat a retreat.", 'person': character.subtitles, 'if': topic_set == 1, 'image': 1},
        {'say': "Good view, bad timing.", 'person': character.subtitles, 'if': topic_set == 1, 'image': 1},
        person = character.headmaster, image = image2)
        # ("Oh, sorry.", topic_set == 2),
        # ("Oh, sorry about that!", topic_set == 2),
        # ("Sorry miss, wrong door obviously!", topic_set == 2),
        # ("Nice view, wrong door. Sorry!", topic_set == 2),
        # ("Bad timing I see. Sorry about that!", topic_set == 2),
        # ("After a quick look at the sexy girl, you apologize and leave.", character.subtitles, topic_set == 2),
        # ("A nice view, but you quickly leave anyway.", character.subtitles, topic_set == 2),

    jump new_daytime







