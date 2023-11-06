# education < 80
label sd_event_1 (**kwargs):
    $ char_obj = get_kwargs("char_obj", **kwargs)

    $ education = char_obj.get_stat_number(EDUCATION)
    $ inhibition = char_obj.get_stat_number(INHIBITION)

    if education > 50 and get_random_int(0, 1) == 0:
        show screen black_screen_text("sd_event_1\n education > 50 and 50%")
        sgirl "Umm, hello!"
        headmaster "Hello there, is everything okay?"
        if inhibition >= 90:
            show screen black_screen_text("sd_event_1\n education > 50 and 50%\ninhibition >= 90")
            sgirl "Yeah Mr. [headmaster_last_name], but would you please knock before entering next time?"
            headmaster "Ah yes... yes of course."
            $ change_stats_with_modifier(char_obj,
                HAPPINESS = DEC_TINY)
            jump new_daytime
        else:
            show screen black_screen_text("sd_event_1\n education <= 50 or 50%")
            sgirl "Yeah Mr. [headmaster_last_name], you just surprised me."
            headmaster "Oh, sorry about that."
            $ change_stats_with_modifier(char_obj,
                HAPPINESS = DEC_TINY, education = MEDIUM)
            jump new_daytime
    else:
        show screen black_screen_text("sd_event_1\n education <= 50 or 50%")
        sgirl "hmm... This homework is hard. Why do I need to learn this anyway?"
        $ change_stats_with_modifier(char_obj,
            education = SMALL)
        jump new_daytime

label sd_event_2 (**kwargs):
    $ char_obj = get_kwargs("char_obj", **kwargs)
    $ inhibition = char_obj.get_stat_number(INHIBITION)

    $ location = get_random_choice("dorm_room", "shower")
    $ topic = []

    if inhibition > get_random_int(30, 50):
        $ topic = ["ah", "ahhh", "oh", "eeek", "panties", "breast", "breasts", "bra"]
    else:
        $ topic = ["guys_stop", "huh", "reason", "dressing", "blush"]

    $ topic = get_random_choice(topic)

    show screen black_screen_text("sd_event_2\n topic == '[topic]'")
    if topic == "ah":
        sgirl "Ah!"
        $ change_stats_with_modifier(char_obj,
            HAPPINESS = DEC_TINY, inhibition = DEC_TINY)
    elif topic == "ahhh":
        sgirl "AHHH!!!"
        $ change_stats_with_modifier(char_obj,
            HAPPINESS = DEC_TINY, inhibition = DEC_TINY, reputation = DEC_TINY)
    elif topic == "eeek":
        sgirl "Eek!"
        $ change_stats_with_modifier(char_obj,
            HAPPINESS = DEC_LARGE, inhibition = DEC_TINY)
    elif topic in ["panties", "breast", "breasts"]:
        $ random_say(
            ("Ah!!! Look away, please, you can see my [topic]!", character.sgirl),
            ("Ah!!! Look away, please, I don't want guys seeing my [topic]!", character.sgirl),
            ("Eek! Stop! Don't stare at my [topic]!", character.sgirl)
        )
        $ change_stats_with_modifier(char_obj,
            HAPPINESS = DEC_LARGE, inhibition = DEC_TINY, charm = MEDIUM)
    






