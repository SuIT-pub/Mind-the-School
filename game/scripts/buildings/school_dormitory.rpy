# education < 80
label sd_event_1 (**kwargs):
    $ image = Image_Series("images/events/school dormitory/sd_event_1 <name> <level> <step>.png", name = "high_school", **kwargs)

    $ begin_event()

    $ char_obj = get_kwargs("char_obj", **kwargs)

    $ education = char_obj.get_stat_number(EDUCATION)
    $ inhibition = char_obj.get_stat_number(INHIBITION)

    if education > 50 and get_random_int(0, 1) == 0:
        show screen black_screen_text("sd_event_1\n education > 50 and 50%")
        $ image.show(0)
        sgirl "Umm, hello!"
        $ image.show(1)
        headmaster "Hello there, is everything okay?"
        if inhibition >= 90:
            show screen black_screen_text("sd_event_1\n education > 50 and 50%\ninhibition >= 90")
            $ image.show(2)
            sgirl "Yeah Mr. [headmaster_last_name], but would you please knock before entering next time?"
            $ image.show(3)
            headmaster "Ah yes... yes of course."
            $ change_stats_with_modifier(char_obj,
                HAPPINESS = DEC_TINY)
            jump new_daytime
        else:
            show screen black_screen_text("sd_event_1\n education <= 50 or 50%")
            $ image.show(2)
            sgirl "Yeah Mr. [headmaster_last_name], you just surprised me."
            $ image.show(3)
            headmaster "Oh, sorry about that."
            $ change_stats_with_modifier(char_obj,
                HAPPINESS = DEC_TINY, education = MEDIUM)
            jump new_daytime
    else:
        show screen black_screen_text("sd_event_1\n education <= 50 or 50%")
        $ image.show(4)
        sgirl "hmm... This homework is hard. Why do I need to learn this anyway?"
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
        $ topic = ["ah", "ahhh", "oh", "eeek", "panties", "breast", "breasts", "bra"]
    else:
        $ topic = ["guys_stop", "huh", "reason", "dressing", "blush"]

    $ topic = get_random_choice(topic)

    show screen black_screen_text("sd_event_2\n topic == '[topic]'")
    if topic == "ah":
        sgirl "Ah!"
        $ change_stats_with_modifier(char_obj,
            happiness = DEC_TINY, inhibition = DEC_TINY)
    elif topic == "ahhh":
        sgirl "AHHH!!!"
        $ change_stats_with_modifier(char_obj,
            happiness = DEC_TINY, inhibition = DEC_TINY, reputation = DEC_TINY)
    elif topic == "eeek":
        sgirl "Eek!"
        $ change_stats_with_modifier(char_obj,
            happiness = DEC_LARGE, inhibition = DEC_TINY)
    elif topic in ["panties", "breast", "breasts"]:
        $ random_say(
            ("Ah!!! Look away, please, you can see my [topic]!", character.sgirl),
            ("Ah!!! Look away, please, I don't want guys seeing my [topic]!", character.sgirl),
            ("Eek! Stop! Don't stare at my [topic]!", character.sgirl),
        )
        $ change_stats_with_modifier(char_obj,
            happiness = DEC_LARGE, inhibition = DEC_TINY, charm = MEDIUM)
    elif topic == "oh":
        sgirl "Oh!"
        headmaster "I'm terribly sorry."
        sgirl "I-it's ok..."
        subtitles "You quickly make an exit."
        $ change_stats_with_modifier(char_obj,
            inhibition = DEC_TINY, happiness = DEC_MEDIUM)
        jump new_daytime;
    elif topic == "guys_stop":
        sgirl "Excuse me!\n Can you guys stop running in and out of here?!"
        $ change_stats_with_modifier(char_obj,
            inhibition = DEC_TINY, morale = DEC_SMALL)
    elif topic == "huh":
        $ random_say(
            ("Umm... What are you doing in here?", character.sgirl),
            ("Mr. [headmaster_last_name]? What are you doing in here?", character.sgirl),
        )
        $ change_stats_with_modifier(char_obj,
            inhibition = DEC_TINY, morale = DEC_SMALL)
    elif topic == "reason":
        sgirl "Hey Mr. [headmaster_last_name]!"
        headmaster "Hello there!"
        if get_random_int(0, 1000) == 0:
            sgirl "General Kenobi!"
        sgirl "Any particular reason I get a visit?"
        headmaster "Oh no, I just saw an open door and..."
        sgirl "Oh, silly me, would you mind closing it on your way out?"
        headmaster "No problem."
        $ change_stats_with_modifier(char_obj,
            charm = MEDIUM, inhibition = DEC_MEDIUM);
        jump new_daytime;
    elif topic == "blush":
        $ random_say(
            ("Ah! What are you doing here?", character.sgirl),
            ("Oh! Mr. [headmaster_last_name]!"),
        )
        $ change_stats_with_modifier(char_obj,
            charm = MEDIUM, inhibition = DEC_MEDIUM)
    elif topic == "dressing":
        $ random_say(
            ("Umm, do you mind?", character.sgirl),
            ("I'm getting dressed! GET OUT!", character.sgirl),
        )
        $ change_stats_with_modifier(char_obj,
            inhibition = DEC_TINY, charm = SMALL)

    $ random_say(character.headmaster,
        "Oh, wrong door, bye!",
        "Sorry, I'm leaving!",
        ("So sorry!", topic_set == 1),
        ("I'm terribly sorry!", topic_set == 1),
        ("I'm leaving, I'm leaving!", topic_set == 1),
        ("You hastily beat a retreat.", character.subtitles, topic_set == 1),
        ('say':"Good view, bad timing.", character.subtitles, topic_set == 1),
        ("Oh, sorry.", topic_set == 2),
        ("Oh, sorry about that!", topic_set == 2),
        ("Sorry miss, wrong door obviously!", topic_set == 2),
        ("Nice view, wrong door. Sorry!", topic_set == 2),
        ("Bad timing I see. Sorry about that!", topic_set == 2),
        ("After a quick look at the sexy girl, you apologize and leave.", character.subtitles, topic_set == 2),
        ("A nice view, but you quickly leave anyway.", character.subtitles, topic_set == 2),
    )

    jump new_daytime







