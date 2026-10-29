# TEMPLATE: threshold / resolution / measure scene — never in a map pool, only fired by
# an EventEffect on the Situation (situations.rpy), e.g.
#     AutoThreshold("Hint text.", EventEffect("my_thresh_scene"), main=-12, direction=-1),
#     PositiveResolution("ALL", ValueEffect("my_sit_resolved", "positive"), EventEffect("my_sit_positive_resolve")),
# EventEffect calls the event directly: its conditions are NOT checked.

init 1 python:
    set_current_mod('base')

    my_sit_scene_events = EventStorage("my_sit_scenes", "misc")
    my_sit_scene_events.add_event(
        Event(EVENT_ALWAYS, "my_thresh_scene", override_location="misc", title="My Threshold"),
        Event(EVENT_ALWAYS, "my_sit_positive_resolve",
            Pattern("main", "images/events/my_sit/my_sit_positive_resolve/my_sit_positive_resolve 1.webp"),
            override_location="misc",
            title="My Situation — Resolved"),
    )

label my_thresh_scene (**kwargs):
    $ begin_event(**kwargs)

    # Fallback background first: works before any scene art exists.
    $ paperdoll_manager.set_background("images/background/office building/secretary 5 1 0.webp", blur = True)
    $ emiko.register_paperdoll()
    $ emiko.display(PDAImage(pose = "12", outfit = "uniform", level = 5, mood = "neutral", mouth = "open"),
        PDAPreset("close_body_center", duration = 0.4))
    emiko.say "The campus reacts."
    headmaster.think "And so do I."

    $ end_event(END_NONE, **kwargs)
    return

label my_sit_positive_resolve (**kwargs):
    $ begin_event(**kwargs)
    $ paperdoll_manager.set_background("images/background/office building/secretary 5 1 0.webp", blur = True)
    $ show_pattern("main", **kwargs)
    subtitles "The payoff."
    $ end_event(END_NONE, **kwargs)
    return
