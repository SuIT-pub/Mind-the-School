init 1 python: 
    set_current_mod('mod')  

<<<<<<< HEAD
    # overwrite_event_image('sb_event_5', 'main', Pattern('main', 'images/test_image <step>.png'))
    mod_sb_event5 = Event(3, "sb_event_6",
        TimeCondition(daytime = "c", weekday = "d"),
        RandomListSelector('girls', 'Ikushi Ito', 'Soyoon Yamamoto', 'Yuriko Oshima'),
<<<<<<< HEAD
<<<<<<< HEAD
        Pattern('main', "/images/events/school building/sb_event_5 <school_level> <girls> <step>.webp",'school_level', 'girls', key = 'version_0_1_5'),
=======
        Pattern('main', "/images/events/school building/sb_event_5 <school_level> <girls> <step>.webp", alternative_keys = ['school_level', 'girls'], key = 'version_0_1_5'),
>>>>>>> 0308013 (added more functionality for mod framework)
=======
        Pattern('main', "/images/events/school building/sb_event_5 <school_level> <girls> <step>.webp",'school_level', 'girls', key = 'version_0_1_5'),
>>>>>>> c844caf (extracted images out of events for new modding system)
        thumbnail = "images/events/school building/sb_event_5 1 Soyoon Yamamoto 11.webp")
=======
    event_label_event = Event(3, "event_label", 
        TimeCondition(day = "5-10", month = "2-", daytime = "f"),
        RandomListSelector("girl", "Aona Komuro", "Lin Kato", "Luna Clark"),
        Pattern("main", "/images/events/school building/sb_event_4 <school_level> <girl> <step>.webp"),
        Pattern("main2", "/images/events/school building/sb_event_5 <school_level> <girl>.webp", 'school_level', 'girl'),
    )
    courtyard_events["patrol"].add_event(event_label_event)
>>>>>>> 32f8fe1 (Add translations, update version, and clean up code structure)

label event_label (**kwargs):
    $ begin_event(**kwargs);

    $ image = convert_pattern("main", **kwargs)

    $ show_pattern("main2", **kwargs)
    person "Hi I'm a dialogue text."

    $ image.show(0)
    person "Oh another image."

    $ image.show(1)
    person "Wow such simple"

    call change_stats_with_modifier("school",
        happiness = 2, inhibition = TINY)

    call change_money_with_modifier(100)

    $ end_event('new_daytime', **kwargs)