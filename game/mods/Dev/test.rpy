init 1 python: 
    set_current_mod('mod')  

    event_label_event = Event(3, "event_label", 
        TimeCondition(day = "5-10", month = "2-", daytime = "f"),
        RandomListSelector("girl", "Aona Komuro", "Lin Kato", "Luna Clark"),
        Pattern("main", "/images/events/school building/sb_event_4 <school_level> <girl> <step>.webp"),
        Pattern("main2", "/images/events/school building/sb_event_5 <school_level> <girl>.webp", 'school_level', 'girl'),
    )
    courtyard_events["patrol"].add_event(event_label_event)

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