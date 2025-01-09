########################################
# region Courtyard Event Handler ----- #
########################################

init -1 python:
    set_current_mod('base')
    
    courtyard_timed_event = TempEventStorage("courtyard_timed", "courtyard", fallback = Event(2, "courtyard.after_time_check"))
    courtyard_general_event = EventStorage("courtyard_general", "courtyard", fallback = Event(2, "courtyard.after_general_check"))
    register_highlighting(courtyard_timed_event, courtyard_general_event)
    
    courtyard_events = {}
    add_storage(courtyard_events, EventStorage("patrol", "courtyard", fallback_text = "There is nobody here."))

    courtyard_bg_images = BGStorage("images/background/courtyard/c.webp",
        BGImage("images/background/courtyard/<school_level> <nude> <variant>.webp", 1, TimeCondition(daytime = "f")),
        BGImage("images/background/courtyard/n.webp", 1, TimeCondition(daytime = 7)), # show empty courtyard at night
    )

init 1 python:
    set_current_mod('base')

    courtyard_event1 = Event(3, "courtyard_event_1",
        LevelCondition('1-3', char_obj = 'school'),
        LevelSelector('school_level', 'school'),
        RandomListSelector('girl_name', 'easkey_tanaka'),
        RandomValueSelector('variant', 1, 1),
        OR(TimeCondition(daytime = "f", weekday = "d"), TimeCondition(daytime = "d", weekday = "w")),
        Pattern("main", "images/events/courtyard/courtyard_event_1/courtyard_event_1 <girl_name> <school_level> <step>.webp"),
        thumbnail = "images/events/courtyard/courtyard_event_1/courtyard_event_1 easkey_tanaka 1 0.webp")

    courtyard_event2 = Event(3, "courtyard_event_2",
        OR(TimeCondition(daytime = "f", weekday = "d"), TimeCondition(daytime = "d", weekday = "w")),
        LevelSelector('school_level', 'school'),
        Pattern("main", "images/events/courtyard/courtyard_event_2/courtyard_event_2 <school_level> <step>.webp"),
        thumbnail = "images/events/courtyard/courtyard_event_2/courtyard_event_2 1 0.webp")

    courtyard_event3 = Event(3, "courtyard_event_3",
        TimeCondition(daytime = "f", weekday = "d"),
        LevelSelector('school_level', 'school'),
        Pattern("main", "images/events/courtyard/courtyard_event_3/courtyard_event_3 <school_level> <step>.webp"),
        thumbnail = "images/events/courtyard/courtyard_event_3/courtyard_event_3 1 0.webp")

    courtyard_event4 = Event(3, "courtyard_event_4",
        OR(TimeCondition(weekday = "d", daytime = "f"),
            TimeCondition(weekday = "w", daytime = "d")),
        LevelCondition("3-", "school"),
        RandomListSelector('girl_name', 'luna_clark', "gloria_goto", "ikushi_ito", "ishimaru_maki"),
        Pattern("main", "images/events/courtyard/courtyard_event_4/courtyard_event_4 <school_level> <girl_name> <step>.webp"),
        thumbnail = "images/events/courtyard/courtyard_event_4/courtyard_event_4 1 gloria_goto 1.webp")

    courtyard_event5 = Event(3, "courtyard_event_5",
        OR(TimeCondition(weekday = "d", daytime = "f"),
            TimeCondition(weekday = "w", daytime = "d")),
        LevelSelector('school_level', 'school'),
        Pattern("main", "images/events/courtyard/courtyard_event_5/courtyard_event_5 <school_level>.webp"),
        thumbnail = "images/events/courtyard/courtyard_event_5/courtyard_event_5 1.webp")

    courtyard_event6 = Event(3, "courtyard_event_6",
        TimeCondition(weekday = "d", daytime = "2,4"),
        LevelSelector('school_level', 'school'),
        RandomListSelector('girl_name', 'seraphina_clark'),
        Pattern("main", "images/events/courtyard/courtyard_event_6/courtyard_event_6 <girl_name> <school_level> <step>.webp"),
        thumbnail = "images/events/courtyard/courtyard_event_6/courtyard_event_6 seraphina_clark 1 0.webp")

    courtyard_event7 = Event(3, "courtyard_event_7",
        OR(
            TimeCondition(daytime = "f", weekday = "d"),
            TimeCondition(daytime = "d", weekday = "w"),
        ),
        RandomListSelector("girl_name", "easkey_tanaka", "elsie_johnson", "seraphina_clark", "soyoon_yamamoto"),
        Pattern("main", "images/events/courtyard/courtyard_event_7/courtyard_event_7 <girl_name> <school_level> <step>.webp"),
        thumbnail = "images/events/courtyard/courtyard_event_7/courtyard_event_7 easkey_tanaka 1 0.webp"
    )

    courtyard_event8 = Event(3, "courtyard_event_8",
        TimeCondition(daytime = "f", weekday = "d"),)

    courtyard_events["patrol"].add_event(
        courtyard_event1, 
        courtyard_event2, 
        courtyard_event3,
        courtyard_event4,
        courtyard_event5,
        courtyard_event6,
        courtyard_event7,
    )

# endregion
########################################

######################################
# region Courtyard Entry Point ----- #
######################################

label courtyard ():
    call call_available_event(courtyard_timed_event) from courtyard_1

label .after_time_check (**kwargs):
    call call_available_event(courtyard_general_event) from courtyard_4

label .after_general_check (**kwargs):
    call call_event_menu (
        "What to do at the Courtyard?", 
        courtyard_events, 
        default_fallback,
        character.subtitles,
        bg_image = courtyard_bg_images,
        fallback_text = "There is nothing to see here."
    ) from courtyard_3

    jump courtyard

# endregion
######################################

#################################
# region Courtyard Events ----- #
#################################

#########################
# region Regular Events #

label courtyard_event_1 (**kwargs):
    $ begin_event("2", **kwargs)

    $ school_level = get_value('school_level', **kwargs)

    $ image = convert_pattern("main", **kwargs)

    $ image.show(0)
    subtitles "You walk along the courtyard when a gist of wind blows up the girls skirt in front of you."
    $ call_custom_menu_with_text("How do you react?", character.subtitles, False,
        ("Look", "courtyard_event_1.look"),
        ("Look away", "courtyard_event_1.look_away"),
    **kwargs)
label .look (**kwargs):
    $ begin_event()
    
    $ image.show(1)
    subtitles "You take the chance to stare directly ahead and burn that image into your brain and retina."
    $ image.show(2)
    subtitles "The girl looks at you, screams, covers herself and runs away."
    $ image.show(3)
    sgirl "PERVERT!"

    call change_stats_with_modifier('school',
        happiness = DEC_SMALL, reputation = DEC_TINY, inhibition = DEC_SMALL) from _call_change_stats_with_modifier_9
    
    $ end_event("new_daytime", **kwargs)
label .look_away (**kwargs):
    
    $ begin_event()
    
    $ image.show(4)
    subtitles "You quickly look away, but the image is already burned into your brain."
    $ image.show(5)
    subtitles "The girl looks at you ashamed of the situation and runs away. Glad you didn't stare."

    call change_stats_with_modifier('school',
        happiness = TINY, reputation = TINY, inhibition = DEC_TINY) from _call_change_stats_with_modifier_10
    
    $ end_event("new_daytime", **kwargs)

label courtyard_event_2 (**kwargs):
    $ begin_event(**kwargs)

    $ school_level = get_value('school_level', **kwargs)

    $ image = convert_pattern("main", **kwargs)

    $ yuriko = get_person("class_3a", "yuriko_oshima").get_character()

    $ image.show(0)
    subtitles "You notice a girl sitting alone in the courtyard, apparently left out by the others."
    $ call_custom_menu_with_text("What do you do?", character.subtitles, False,
        ("Talk to her", "courtyard_event_2.talk"),
        ("Leave her alone", "courtyard_event_2.leave"),
    **kwargs)
label .talk (**kwargs):
    
    $ begin_event()
    
    $ image.show(2)
    headmaster "Hey, are you alright?"
    $ image.show(3)
    yuriko "Oh, hi. I'm fine, just a bit tired."
    $ image.show(4)
    headmaster "You look a bit lonely. Why don't you join the others?"
    $ image.show(5)
    yuriko "I don't really like them. They are all so... shallow."
    $ image.show(6)
    headmaster "I see. Well, I'm sure you'll find some friends eventually."
    $ image.show(7)
    yuriko "..."
    $ image.show(8)
    headmaster "If you need anything, just ask me. See you later."
    $ image.show(9)
    yuriko "Thanks, bye."
    
    call change_stats_with_modifier('school',
        happiness = DEC_TINY, reputation = TINY) from _call_change_stats_with_modifier_11
    $ end_event("new_daytime", **kwargs)
label .leave (**kwargs):
    
    $ begin_event()
    
    $ image.show(1)
    subtitles "You decide to leave her alone."
    
    call change_stats_with_modifier('school',
        happiness = DEC_SMALL, reputation = DEC_SMALL) from _call_change_stats_with_modifier_12
    $ end_event("new_daytime", **kwargs)

label courtyard_event_3 (**kwargs):
    $ begin_event(**kwargs)
    
    $ school_level = get_value('school_level', **kwargs)
    $ image = convert_pattern("main", **kwargs)

    call Image_Series.show_image(image, 0, 1) from _call_show_image_courtyard_event_3_1
    subtitles "You notice a group of girls taking a break together."

    call change_stats_with_modifier('school',
        charm = SMALL, happiness = TINY, education = TINY, reputation = SMALL) from _call_change_stats_with_modifier_13
    
    $ end_event("new_daytime", **kwargs)

label courtyard_event_4(**kwargs):
    $ begin_event("2", **kwargs)

    $ image = convert_pattern("main", **kwargs)

    call Image_Series.show_image(image, 0, 1, 2) from _call_Image_Series_show_image_3
    headmaster "Interesting..."
    
    call change_stats_with_modifier('school',
        happiness = DEC_TINY, charm = TINY, inhibition = DEC_SMALL) from _call_change_stats_with_modifier_14

    $ end_event("new_daytime", **kwargs)

label courtyard_event_5(**kwargs):
    $ begin_event(**kwargs)

    $ school_level = get_value('school_level', **kwargs)

    # headmaster walks by
    # students walk by talking with each other
    $ show_pattern("main", **kwargs)
    subtitles "You come across a group of students talking to each other."

    call change_stats_with_modifier('school',
        happiness = SMALL, charm = SMALL) from _call_change_stats_with_modifier_15

    $ end_event("new_daytime", **kwargs)

label courtyard_event_6(**kwargs):
    $ begin_event("2", **kwargs)

    $ school_level = get_value('school_level', **kwargs)

    $ seraphina = get_person("class_3a", "seraphina_clark").get_character()

    $ image = convert_pattern("main", **kwargs)

    # headmaster approaches a student sitting on the courtyard
    $ image.show(0)
    headmaster "Excuse me, but what are you doing here?"

    # student looks up kinda surprised
    $ image.show(1)
    seraphina "I'm taking my break sir."

    # headmaster looking rather angry
    $ image.show(2)
    headmaster "Class already started. You should be in class."

    # student surprised
    $ image.show(3)
    seraphina "Really?!"

    # headmaster nods
    $ image.show(4)
    headmaster "Yes. Now run along and check the time next time so you don't arrive late!"
    
    # student runs off
    $ image.show(5)
    seraphina "Sorry!"

    call change_stats_with_modifier('school',
        charm = DEC_TINY, education = SMALL) from _call_change_stats_with_modifier_16

    $ end_event("new_daytime", **kwargs)

label courtyard_event_7(**kwargs):
    $ begin_event(**kwargs)

    $ image = convert_pattern("main", **kwargs)

    $ image.show(0)
    call Image_Series.show_image(image, 0, 1, 2, 3) from _call_show_image_courtyard_event_7_1
    headmaster "Nice!"
    call Image_Series.show_image(image, 4, 5, 6, 7, 8, 9, pause = True) from _call_show_image_courtyard_event_7_2

    call change_stats_with_modifier('school',
        charm = TINY, inhibition = DEC_SMALL
    ) from _call_courtyard_event_7_1

    $ end_event("new_daytime", **kwargs)

label courtyard_event_8(**kwargs):
    $ begin_event(**kwargs)

    $ image = convert_pattern("main", **kwargs)

    $ ishimaru = get_person("class_3a", "ishimaru_maki").get_character()

    $ image.show(0)
    # You find a girl playing the guitar. You sit down and listen to her play.
    # She looks up and smiles at you.
    # You smile back and she continues playing.
    # You sit there for a while and listen to her play.
    # She finishes her song and you clap.
    headmaster "That was beautiful!"
    ishimaru "Thank you, I was just practicing."
    headmaster "You're really good. Keep it up!"
    ishimaru "Thanks, I will."
    # headmaster leaves

    call change_stats_with_modifier('school',
        charm = SMALL, happiness = MEDIUM
    ) from _call_courtyard_event_8_1

    $ end_event("new_daytime", **kwargs)

# endregion
#########################

# endregion
#################################