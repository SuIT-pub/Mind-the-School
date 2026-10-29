# TEMPLATE: time-triggered story beat — runs from time_event_check when the date/daytime
# arrives, before the player gets the map. Priority 1 blocks everything else that check;
# priority 2 runs in sequence with the other checks (then end with 'none' + return).

init 1 python:
    set_current_mod('base')

    my_story_beat_event = Event(EVENT_BLOCKING, "my_story_beat",
        TimeCondition(day = 12, month = 1, year = 2023, daytime = 1),
        NOT(EventSeenCondition(True, "my_story_beat")),          # one-shot safety
        Pattern("main", "images/events/story/my_story_beat/my_story_beat <step>.webp"),
        thumbnail = "images/events/story/my_story_beat/my_story_beat 1.webp",
        title = "My Story Beat")

    time_check_events.add_event(my_story_beat_event)

label my_story_beat (**kwargs):
    $ begin_event(**kwargs)
    $ image = convert_pattern("main", **kwargs)
    $ image.show(0)
    subtitles "The morning it happens."
    $ end_event(END_NEW_DAYTIME, **kwargs)
