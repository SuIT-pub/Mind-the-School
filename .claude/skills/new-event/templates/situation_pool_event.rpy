# TEMPLATE: situation pool event — exists only while <my_sit> is active and its bar sits
# inside the SituationPool band. Requires on the Situation (situations.rpy):
#     SituationPool("my_band", -10, 15),

init 1 python:
    set_current_mod('base')

    sb_events["patrol"].add_event(Event(
        3,
        "my_band_scene",
        TimeCondition(weekday="d", daytime="f"),
        LevelCondition("1-", char_obj="school"),
        SituationPoolCondition("my_sit", "my_band"),
        # Key MUST be the composite "situation:<sit>:<bar>" for get_bar_value to find it.
        SituationBarSelector("situation:my_sit:main", "my_sit", "main"),
        Pattern("main", "images/events/my_sit/my_band_scene/my_band_scene <step>.webp"),
        thumbnail = "images/events/my_sit/my_band_scene/my_band_scene 1.webp",
        title = "My Band Scene"))

label my_band_scene (**kwargs):
    $ begin_event(**kwargs)
    $ standing = get_bar_value("my_sit", "main", 0, **kwargs)

    $ image = convert_pattern("main", **kwargs)
    $ image.show(0)
    subtitles "Scene."

    if standing <= -5:
        headmaster.think "Reactive line for a low bar."

    # Push this situation directly (no-op unless active) …
    $ situation_manager.apply_progress_change("situation:my_sit:main", 2)
    # … and/or move stats, which drift the bar through its stat_weights.
    call change_stats_with_modifier(reputation=TINY) from _my_band_scene_1
    $ end_event("new_daytime", **kwargs)
