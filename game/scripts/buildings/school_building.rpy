# TODO: make images
label sb_event_1 (**kwargs): # patrol, check class
    # show screen black_screen_text("sb_event_1")
    $ image = Image_Series("/images/events/school building/sb_event_1 <name> <step>.png", **kwargs)

    # call show_image("/images/events/school building/sb_event_1 <name> 1.png", SCENE, **kwargs)
    $ image.show(0)
    subtitles "You walk through the corridors of the high school."

    # call show_image("/images/events/school building/sb_event_1 <name> 2.png", SCENE, **kwargs)
    $ image.show(1)
    subtitles "You come across a couple making out in the hallway."

    $ call_custom_menu_with_text("What do you do?", character.subtitles, False,
        ("Leave and let them have fun", "sb_event_1.leave"),
        ("Stop them", "sb_event_1.stop", not is_rule_unlocked("student_student_relation", "high_school")), 
    **kwargs)
label .leave (**kwargs):
    # show screen black_screen_text("sb_event_1.leave")
    $ image.show(2)
    # call show_image("/images/events/school building/sb_event_1 <name> 3.png", SCENE, **kwargs)
    subtitles "You decide to leave them and let them have their fun."
    $ change_stats_with_modifier(kwargs["char_obj"],
        charm = DEC_SMALL, education = TINY, corruption = TINY, inhibition = DEC_SMALL)
    jump new_daytime

label .stop (**kwargs):
    # show screen black_screen_text("sb_event_1.stop")
    $ image.show(3)
    # call show_image("/images/events/school building/sb_event_1 <name> 4.png", SCENE, **kwargs)
    headmaster "Hey you! Stop that. You know that is against the rules!"
    sgirl "We're sorry!"
    $ change_stats_with_modifier(kwargs["char_obj"],
        charm = MEDIUM, happiness = DEC_SMALL, education = SMALL, reputation = TINY, inhibition = DEC_TINY)
    jump new_daytime

# TODO: make images
label sb_event_2 (**kwargs): # teach class
    show screen black_screen_text("sb_event_2")
    subtitles "A student tripped while handing out assignments in class."

    $ call_custom_menu_with_text("What do you do?", character.subtitles, False,
        ("Leave alone", "sb_event_2.leave"),
        ("Help her up", "sb_event_2.help"), 
    **kwargs)

label .leave (**kwargs):
    show screen black_screen_text("sb_event_2.leave")
    subtitles "You decide to leave her alone."
    $ change_stats_with_modifier(kwargs["char_obj"],
        charm = DEC_TINY, education = TINY)
    jump new_daytime

label .help (**kwargs):
    show screen black_screen_text("sb_event_2.help")
    subtitles "You help her up."
    $ change_stats_with_modifier(kwargs["char_obj"],
        charm = DEC_TINY, happiness = SMALL, education = TINY)
    jump new_daytime

# TODO: make images
label sb_event_3 (**kwargs): # patrol
    show screen black_screen_text("sb_event_3")
    subtitles "As you walk through the corridors of the high school, you notice a student sitting in the corner of the hallway."
    sgirl "*sniffle*"
    headmaster "Are you okay?"
    sgirl "I'm fine. It's just... No I'm fine."

    $ call_custom_menu(False,
        ("What is going on?", "sb_event_3.what"),
        ("If it's nothing, go back to class", "sb_event_3.send_class", time.check_daytime("c")), 
    **kwargs)

label .what (**kwargs):
    show screen black_screen_text("sb_event_3.what")
    headmaster "What is going on? I can see there is something bothering you."
    sgirl "I really don't want to talk about it. I'd like to be alone right now."
    headmaster "Did someone do this to you?"
    sgirl "..."
    $ call_custom_menu(False, 
        ("Leave her alone", "sb_event_3.leave"), 
        ("Get to the bottom of this", "sb_event_3.get_to_bottom"), 
    **kwargs)

label .leave (**kwargs):
    show screen black_screen_text("sb_event_3.what.leave")
    subtitles"You hesitate for a moment, but then decide to leave her alone."
    headmaster "Okay, I'll leave you alone."
    headmaster "But if you need anything, you can always come to me. My door is always open."
    sgirl "..."
    subtitles"You walk away with a heavy heart."
    $ change_stats_with_modifier(kwargs["char_obj"], 
        charm = TINY, happiness = DEC_LARGE, education = TINY, reputation = DEC_TINY)
    jump new_daytime

label .get_to_bottom (**kwargs):
    show screen black_screen_text("sb_event_3.what.get_to_bottom")
    headmaster "I really want to help you. Please tell me what is going on."
    sgirl "..."
    #sit down next to her
    headmaster "Please listen."
    sgirl "..."
    headmaster "Whatever happened to you, if some someone did or said anything."
    sgirl "*sniffle*"
    subtitles "She slowly and silently starts crying."
    headmaster "Let's go to my office, shall we? There it is more private and nobody will bother us. You can then decide what you want to share. Is that okay?"
    sgirl "I- I... yes... thank-"
    #she starts shaking
    subtitles "You support her back to your office and bring her something warm to drink."
    $ change_stats_with_modifier(kwargs["char_obj"],
        happiness = LARGE, reputation = TINY)
    jump new_daytime

label .send_class (**kwargs):
    show screen black_screen_text("sb_event_3.send_class")
    headmaster "Then you better get back to class."
    sgirl "B- But... I..."
    headmaster "Yes?"
    sgirl "I d-don't..."
    $ call_custom_menu(False, 
        ("Poor thing", "sb_event_3.poor_thing"), 
        ("Chin up", "sb_event_3.chin_up"), 
    **kwargs)

label .poor_thing (**kwargs):
    show screen black_screen_text("sb_event_3.send_class.poor_thing")
    headmaster "Look, maybe you should just take the day off. I'll notify your teacher."
    sgirl "Yes... thank you..."
    subtitles "You help her up and walk her to the dormitory."
    $ change_stats_with_modifier(kwargs["char_obj"],
        happiness = LARGE, reputation = TINY)
    jump new_daytime

label .chin_up (**kwargs):
    show screen black_screen_text("sb_event_3.send_class.poor_thing")
    headmaster "Now, now, it can't be that bad. I'm sure whatever caused those tears will soon be forgotten."
    sgirl "..."
    headmaster "Now, run along. Just tell the teachers you needed a breath of air. I'll take care of the rest."
    sgirl "Ok..."
    subtitles "You help her up and she walks off."
    $ change_stats_with_modifier(kwargs["char_obj"],
        happiness = LARGE, reputation = TINY)
    jump new_daytime
