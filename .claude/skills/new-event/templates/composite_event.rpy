# TEMPLATE: composite event — an intro, then a shuffled run of fragments pulled from
# FragmentStorages, then (optionally) an end fragment. Model: truth_or_dare_4.

init 1 python:
    set_current_mod('base')

    my_round_storage = FragmentStorage("my_rounds",
        FragmentRepeatOption(RandomValueSelector("", 2, 4, True), False))   # 2–4 rounds, no repeats
    my_end_storage = FragmentStorage("my_rounds_end")

    sd_events["look_around"].add_event(EventComposite(3, "my_composite",
        [my_round_storage, my_end_storage],
        TimeCondition(daytime="n"),
        LevelCondition("2+", char_obj="school"),
        # Re-rolled before every fragment so each round can feature someone else.
        IterativeListSelector("girls", "ikushi_ito", "lin_kato", "miwa_igarashi", options=[FragmentRerollOption()]),
        Pattern("base", "images/events/dorm/my_composite/my_composite <school_level> <step>.webp"),
        thumbnail = "images/events/dorm/my_composite/my_composite 2 0.webp",
        title = "My Composite"))

    my_round_storage.add_event(
        EventFragment(2, "my_composite_round_1", ReplayCategoryOption("my_composite"),
            Pattern("main", "images/events/dorm/my_composite/round_1 <girls> <school_level> <step>.webp")),
        EventFragment(2, "my_composite_round_2", LevelCondition("3+", char_obj="school"), ReplayCategoryOption("my_composite"),
            Pattern("main", "images/events/dorm/my_composite/round_2 <girls> <school_level> <step>.webp")),
    )
    my_end_storage.add_event(
        EventFragment(2, "my_composite_end", ReplayCategoryOption("my_composite"),
            Pattern("main", "images/events/dorm/my_composite/end <school_level> <step>.webp")))

label my_composite (**kwargs):
    $ begin_event(**kwargs)
    $ image = convert_pattern("base", **kwargs)
    $ image.show(0)
    subtitles "Intro."
    call composite_event_runner(**kwargs) from _my_composite_run

label my_composite_round_1 (**kwargs):
    $ begin_event(**kwargs)
    $ girl = get_person_value("girls", **kwargs)
    $ image = convert_pattern("main", **kwargs)     # resolves against the fragment's patterns
    $ image.show(0)
    girl.say "Round one."
    $ end_event("map_entry", **kwargs)              # hands over to the next fragment

label my_composite_round_2 (**kwargs):
    $ begin_event(**kwargs)
    $ girl = get_person_value("girls", **kwargs)
    $ image = convert_pattern("main", **kwargs)
    $ image.show(0)
    girl.say "Round two."
    $ end_event("map_entry", **kwargs)

label my_composite_end (**kwargs):
    $ begin_event(**kwargs)
    $ image = convert_pattern("main", **kwargs)
    $ image.show(0)
    subtitles "Wrap-up."
    call change_stats_with_modifier(inhibition=DEC_TINY) from _my_composite_end_1
    $ end_event("new_daytime", **kwargs)
